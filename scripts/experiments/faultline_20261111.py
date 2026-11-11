"""Fault-line gadget DP for targeted n, adapted from the public notebook

    alexchilton, "Fault-line DP + Basin Hopping - LB 22.2620"
    https://www.kaggle.com/code/alexchilton/fault-line-dp-basin-hopping-lb-22-2620

whose starter-kit dataset ships ``fault_dp.py`` (rebuilt there from Chris
Deotte's FTMC / fault-line composition).  The construction, in its own words:

    n = K^2 + D.  Lower-left continent: upright cells on the integer lattice.
    Upper-right continent: the same lattice shifted by F.  Along the
    anti-diagonal fault a chain of gadgets (crops of donor packings, w x h
    cells holding w*h + dm squares inside [0, w+f] x [0, h+f]) adds D squares;
    the box side is K + f.

This file keeps that algorithm but:
  * restricts the DP surplus dimension to the target puzzles (DMAX small),
  * runs extraction in two worker processes (CPU budget),
  * certifies each composed packing with the repo's vendored official v20
    metric after the exact float64 round trip the board performs,
  * writes only improved, certified full-n groups.

Write scope: outputs/experiments/research_20261111/faultline/ only.

Usage:
  .venv/bin/python scripts/experiments/faultline_20261111.py \
      --base outputs/merged/v124_plus_daily44/submission.csv \
      --targets 971,911,910,791,972 --out outputs/experiments/research_20261111/faultline
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from multiprocessing import Pool

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from squares._vendor import official_metric as metric  # noqa: E402

WMAX = 31
DMAX = 24
FMAX = 0.97
E = 1e-9
THR = np.array([0.0, 0.3, 0.45, 0.6, 0.75, 0.9])  # bins for the free tip lengths Ybr / Xtl
NB = len(THR)
SYMS = [(sx, sy, tr) for sx in (1, -1) for sy in (1, -1) for tr in (0, 1)]
T0 = time.time()


def log(*a: object) -> None:
    print(f"{time.strftime('%H:%M:%S')} [{time.time() - T0:6.0f}s]", *a, flush=True)


def side(sq: np.ndarray) -> float:
    """Container side over exact corner extents (float64)."""
    x, y, t = sq[:, 0], sq[:, 1], sq[:, 2]
    c, s = np.cos(t) * 0.5, np.sin(t) * 0.5
    X = np.concatenate([x + c - s, x - c - s, x - c + s, x + c + s])
    Y = np.concatenate([y + s + c, y - s + c, y - s - c, y + s - c])
    return float(max(X.max() - X.min(), Y.max() - Y.min()))


def float_text(sq: np.ndarray) -> list[tuple[str, str, str]]:
    return [(repr(float(a)), repr(float(b)), repr(float(t))) for a, b, t in sq]


def certify(n: int, sq: np.ndarray) -> tuple[float, np.ndarray] | None:
    """Official metric on the doubles the board parses from repr literals."""
    rows = [
        {"n": str(n), "square_id": str(i), "x": a, "y": b, "angle": t}
        for i, (a, b, t) in enumerate(float_text(sq))
    ]
    _, _, detail, why = metric.evaluate_single_puzzle(n, rows)
    if why != "ok" or detail is None:
        return None
    return float(detail), sq


def certify_ladder(n: int, sq: np.ndarray) -> tuple[float, np.ndarray] | None:
    r = certify(n, sq)
    for eps in (1e-12, 1e-11, 1e-10):
        if r is not None:
            return r
        c = (sq[:, :2].min(0) + sq[:, :2].max(0)) / 2
        s2 = sq.copy()
        s2[:, :2] = c + (sq[:, :2] - c) * (1 + eps)
        r = certify(n, s2)
    return r


def load_csv(path: str) -> dict[int, np.ndarray]:
    out: dict[int, np.ndarray] = {}
    for n, g in pd.read_csv(path).groupby("n"):
        sq = g.sort_values("square_id")[["x", "y", "angle"]].to_numpy(float)
        if len(sq) == n:
            out[int(n)] = sq
    return out


def mapped(sq: np.ndarray, sym: tuple[int, int, int]):
    """Donor under a dihedral map, translated so its bounding box starts at (0, 0)."""
    sx, sy, tr = sym
    x, y, t = sq[:, 0] * sx, sq[:, 1] * sy, sq[:, 2] * sx * sy
    if tr:
        x, y, t = y, x, -t
    he = 0.5 * (np.abs(np.cos(t)) + np.abs(np.sin(t)))
    x, y = x - (x - he).min(), y - (y - he).min()
    return np.c_[x, y, t], x - he, x + he, y - he, y + he


def extract_chunk(donors: list[np.ndarray]) -> list[np.ndarray]:
    """Per-key minimum-f gadget rows for one chunk of donors."""
    W = np.arange(1, WMAX + 1)
    DM = np.arange(1, DMAX + 1)
    best: dict[int, np.ndarray] = {}
    for di, sq in enumerate(donors):
        n = len(sq)
        L = side(sq)
        parts = []
        for si, sym in enumerate(SYMS):
            _, xlo, xhi, ylo, yhi = mapped(sq, sym)
            for h in range(1, min(WMAX, math.ceil(L)) + 1):
                R = np.maximum(np.maximum(xhi[:, None] - W[None, :], (yhi - h)[:, None]), 0.0)
                order = np.argsort(R, axis=0, kind="stable")
                Rs = np.take_along_axis(R, order, axis=0)
                ybr = np.minimum.accumulate(
                    np.where(xhi[order] > W[None, :] + 1e-9, ylo[order], np.inf), axis=0
                )
                xtl = np.minimum.accumulate(
                    np.where(yhi[order] > h + 1e-9, xlo[order], np.inf), axis=0
                )
                idx = W[:, None] * h + DM[None, :] - 1  # (w, dm)
                ok = (idx < n) & (W[:, None] <= math.ceil(L))
                wi, dj = np.nonzero(ok)
                k = idx[wi, dj]
                f = Rs[k, wi]
                m = f <= FMAX
                wi, dj, k, f = wi[m], dj[m], k[m], f[m]
                parts.append(
                    np.c_[
                        wi + 1,
                        np.full(len(f), h),
                        dj + 1,
                        f,
                        np.minimum(ybr[k, wi], 9.0),
                        np.minimum(xtl[k, wi], 9.0),
                        np.full(len(f), di),
                        np.full(len(f), si),
                    ]
                )
        P = np.concatenate(parts) if parts else np.zeros((0, 8))
        if not len(P):
            continue
        qb = np.maximum(np.searchsorted(THR, P[:, 4], side="right") - 1, 0)
        qt = np.maximum(np.searchsorted(THR, P[:, 5], side="right") - 1, 0)
        key = (((P[:, 0] * 32 + P[:, 1]) * 64 + P[:, 2]) * NB + qb) * NB + qt
        o = np.lexsort((P[:, 3], key))
        first = np.r_[True, key[o][1:] != key[o][:-1]]
        for kk, row in zip(key[o][first].astype(np.int64), P[o][first]):
            if kk not in best or row[3] < best[kk][3]:
                best[kk] = row
        if di % 250 == 0:
            log(f"  worker: donor {di}/{len(donors)}, keys {len(best)}")
    return list(best.values())


def merge_extract(rows: list[list[np.ndarray]]) -> np.ndarray:
    best: dict[int, np.ndarray] = {}
    for chunk in rows:
        for row in chunk:
            qb = max(int(np.searchsorted(THR, row[4], side="right")) - 1, 0)
            qt = max(int(np.searchsorted(THR, row[5], side="right")) - 1, 0)
            key = (((int(row[0]) * 32 + int(row[1])) * 64 + int(row[2])) * NB + qb) * NB + qt
            if key not in best or row[3] < best[key][3]:
                best[key] = row
    G = np.array(list(best.values())) if best else np.zeros((0, 8))
    qb = np.maximum(np.searchsorted(THR, G[:, 4], side="right") - 1, 0)
    qt = np.maximum(np.searchsorted(THR, G[:, 5], side="right") - 1, 0)
    M = np.full((WMAX + 2, WMAX + 2, DMAX + 2, NB, NB), np.inf)
    for (w, h, d, f), b, t in zip(G[:, :4], qb, qt):
        M[int(w), int(h), int(d), b, t] = min(M[int(w), int(h), int(d), b, t], f)
    for ax in (0, 1):
        M = np.minimum.accumulate(M, axis=ax)
    for ax in (2, 3, 4):
        M = np.flip(np.minimum.accumulate(np.flip(M, axis=ax), axis=ax), axis=ax)
    keep = G[:, 3] <= M[G[:, 0].astype(int), G[:, 1].astype(int), G[:, 2].astype(int), qb, qt] + 1e-15
    log(f"gadgets: {len(G)} per-key, {int(keep.sum())} after dominance")
    return G[keep]


def run_dp(G: np.ndarray):
    gw, gh, gd = G[:, 0].astype(int), G[:, 1].astype(int), G[:, 2].astype(int)
    gf, gx = G[:, 3], G[:, 5]
    gq = np.maximum(np.searchsorted(THR, G[:, 4], side="right") - 1, 0)
    shape = (WMAX + 1, WMAX + 1, DMAX + 1, NB)
    dp = np.full(shape, np.inf)
    PG = np.full(shape, -1, np.int32)
    PM = np.zeros(shape, np.int8)
    PQ = np.zeros(shape, np.int8)
    dp[0, 0, 0, NB - 1] = 0.0

    def relax(cw2, h0, d, q, src, g, mode):
        vals, qprev = src.min(axis=2), src.argmin(axis=2)
        tgt = dp[cw2, h0 : h0 + vals.shape[0], d : d + vals.shape[1], q]
        better = vals < tgt
        if better.any():
            tgt[better] = vals[better]
            PG[cw2, h0 : h0 + vals.shape[0], d : d + vals.shape[1], q][better] = g
            PM[cw2, h0 : h0 + vals.shape[0], d : d + vals.shape[1], q][better] = mode
            PQ[cw2, h0 : h0 + vals.shape[0], d : d + vals.shape[1], q][better] = qprev[better]

    for cw in range(WMAX + 1):
        cur = dp[cw]
        if not np.isfinite(cur).any():
            continue
        for g in range(len(G)):
            w, h, d, f = gw[g], gh[g], gd[g], gf[g]
            if cw + w > WMAX:
                continue
            val = np.maximum(cur, f)
            ok0 = (THR[None, None, :] >= f + E) | (gx[g] >= cur + E)
            relax(
                cw + w,
                h,
                d,
                gq[g],
                np.where(ok0, val, np.inf)[: WMAX + 1 - h, : DMAX + 1 - d],
                g,
                0,
            )
            if cw == 0:
                continue
            if h + 1 <= WMAX:
                relax(cw + w, h + 1, d, gq[g], val[: WMAX - h, : DMAX + 1 - d], g, 2)
            if cw + w + 1 <= WMAX:
                relax(cw + w + 1, h, d, gq[g], val[: WMAX + 1 - h, : DMAX + 1 - d], g, 1)
    return dp, PG, PM, PQ


def chain(dp, PG, PM, PQ, G, K, D):
    sub = dp[: K + 1, : K + 1, D, :]
    if not np.isfinite(sub).any():
        return None, None
    cw, ch, q = np.unravel_index(np.argmin(sub), sub.shape)
    f, d, out = sub[cw, ch, q], D, []
    guard = 0
    while cw or ch or d:
        guard += 1
        if guard > 10000:
            return None, None
        g, mode, qp = PG[cw, ch, d, q], PM[cw, ch, d, q], PQ[cw, ch, d, q]
        if g < 0:
            return None, None
        out.append((int(g), int(mode)))
        w, h, dd = int(G[g, 0]), int(G[g, 1]), int(G[g, 2])
        cw, ch, d, q = cw - w - (mode == 1), ch - h - (mode == 2), d - dd, qp
    return float(f), out[::-1]


def crop(donor: np.ndarray, sym: int, w: int, h: int, dm: int):
    sq, _, xhi, _, yhi = mapped(donor, SYMS[sym])
    R = np.maximum(np.maximum(xhi - w, yhi - h), 0.0)
    take = np.argsort(R, kind="stable")[: w * h + dm]
    return sq[take], R[take].max()


def compose(K: int, D: int, f: float, links, G: np.ndarray, donors: list[np.ndarray]) -> np.ndarray:
    M = len(links)
    F = f + (M + 2) * E
    a, b, gad = np.full(K, K), np.full(K, K), []
    ox, oy = 0, K
    for m, (g, mode) in enumerate(links):
        w, h, dm, di, si = (int(v) for v in G[g, [0, 1, 2, 6, 7]])
        if m:
            ox += mode == 1
            oy -= mode == 2
        oy -= h
        if mode == 1:
            a[ox - 1] = b[ox - 1] = oy + h
        a[ox : ox + w], b[ox : ox + w] = oy, oy + h
        sq, fg = crop(donors[di], si, w, h, dm)
        assert fg <= f + 1e-12, (fg, f)
        sq = sq.copy()
        sq[:, :2] *= 1 + 1e-11
        sq[:, 0] += ox + E * (1 + m)
        sq[:, 1] += oy + E * (M - m)
        gad.append(sq)
        ox += w
    a[ox:], b[ox:] = 0, 0
    assert oy >= 0 and ox <= K, (ox, oy)
    assert all(a[i + 1] <= b[i] for i in range(K - 1)) and all(a <= b)
    cells = [(i + 0.5, j + 0.5, 0.0) for i in range(K) for j in range(a[i])]
    cells += [(i + 0.5 + F, j + 0.5 + F, 0.0) for i in range(K) for j in range(b[i], K)]
    sq = np.concatenate([np.array(cells).reshape(-1, 3)] + gad)
    assert len(sq) == K * K + D, (len(sq), K * K + D)
    return sq


def base_rows(path: str) -> tuple[dict[int, np.ndarray], dict[int, float]]:
    cur = load_csv(path)
    return cur, {n: side(sq) for n, sq in cur.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--targets", default="971,911,910,791,972,634,862,687,328")
    ap.add_argument("--donors", default="", help="comma-separated extra CSV files")
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()
    targets = [int(v) for v in args.targets.split(",") if v]
    os.makedirs(args.out, exist_ok=True)

    cur, L0 = base_rows(args.base)
    donor_paths = [args.base] + [p for p in args.donors.split(",") if p]
    seen, donors = set(), []
    for p in donor_paths:
        kept = 0
        for n, sq in load_csv(p).items():
            L = side(sq)
            if L >= math.ceil(math.sqrt(n)) - 1e-9:
                continue  # only packings below their grid side are donors
            key = (n, round(L, 9))
            if key not in seen:
                seen.add(key)
                donors.append(sq)
                kept += 1
        log(f"donors from {p}: {kept}")
    log(f"{len(donors)} donors")

    chunks = [donors[i:: args.workers] for i in range(args.workers)]
    t = time.time()
    with Pool(args.workers) as pool:
        parts = pool.map(extract_chunk, chunks)
    G = merge_extract(parts)
    log(f"extract {time.time() - t:.0f}s")
    np.save(os.path.join(args.out, "gadgets.npy"), G)
    dp, PG, PM, PQ = run_dp(G)
    log("dp done")

    report = {"base": args.base, "donors": len(donors), "gadgets": int(len(G)), "targets": {}}
    lines = ["id,n,square_id,x,y,angle"]
    total_gain = 0.0
    for n in targets:
        K = math.isqrt(n)
        D = n - K * K
        old = L0.get(n)
        f, links = chain(dp, PG, PM, PQ, G, K, D)
        entry = {"K": K, "D": D, "old_L": old, "f": f, "links": links}
        if old is None or f is None:
            entry["status"] = "no DP chain"
            report["targets"][str(n)] = entry
            log(f"n={n}: no chain (K={K}, D={D})")
            continue
        bound = K + f + 2 * E
        entry["dp_side"] = bound
        if bound >= old - 1e-7:
            entry["status"] = "DP not below current"
            report["targets"][str(n)] = entry
            log(f"n={n}: DP {bound:.9f} >= ours {old:.9f} (K={K}, f={f:.6f})")
            continue
        sq = compose(K, D, f, links, G, donors)
        r = certify_ladder(n, sq)
        if r is None:
            entry["status"] = "DP below but not certified"
            report["targets"][str(n)] = entry
            log(f"n={n}: DP {bound:.9f} < ours {old:.9f} but NOT certified; links={links}")
            continue
        L1, sq1 = r
        gain = (old - L1) / math.sqrt(n)
        entry.update({"status": "certified", "new_L": L1, "gain": gain})
        report["targets"][str(n)] = entry
        total_gain += gain
        log(f"n={n}: CERTIFIED {L1:.9f} vs {old:.9f}, gain {gain:.6e}, {len(links)} gadgets")
        txt = float_text(sq1)
        for i, (x, y, t) in enumerate(txt):
            lines.append(f"{len(lines) - 1},{n},{i},{x},{y},{t}")
    report["total_gain"] = total_gain
    with open(os.path.join(args.out, "report.json"), "w") as fh:
        json.dump(report, fh, indent=2, default=float)
    out_csv = os.path.join(args.out, "improved_groups.csv")
    with open(out_csv, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    log(f"wrote {out_csv} with {len(lines) - 1} rows, total gain {total_gain:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
