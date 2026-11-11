"""Targeted CPU nonlinear packing compression for "Squares in Squares".

Strategy (fixed-angle contact LP, brief item (a)): with angles frozen the
non-overlap test along a pair's most-separated SAT axis and the containment
test are *linear* in the centres.  Shrinking the container by ``dL`` is then a
pure LP feasibility problem, and any feasible point is a genuine packing
(verified afterwards with exact float64 SAT).  When the LP is infeasible the
contact graph is rigid at those angles, which is a certificate that no
infinitesimal fixed-angle motion can compress this layout.

Sub-commands
    diagnose   per-n evidence for the top-gap puzzles (LP infeasibility ladder)
    sweep      run the compression LP over a range of n, keep only exact wins
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from squares.search.structure import (  # noqa: E402
    bounds,
    candidate_pairs,
    normalize,
    separations,
    side_length,
)

CLEARANCE = 0.0


def pair_axes(P: np.ndarray, pairs: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Signed best SAT axis normal and gap (positive = clear) for each pair."""
    i, j = pairs[:, 0], pairs[:, 1]
    a, b = P[i, 2], P[j, 2]
    axes = np.stack(
        [
            np.stack([np.cos(a), np.sin(a)], -1),
            np.stack([-np.sin(a), np.cos(a)], -1),
            np.stack([np.cos(b), np.sin(b)], -1),
            np.stack([-np.sin(b), np.cos(b)], -1),
        ],
        axis=1,
    )
    d = P[j, :2] - P[i, :2]
    proj = np.einsum("pd,pad->pa", d, axes)
    k = np.abs(proj).argmax(1)
    sel = proj[np.arange(len(pairs)), k]
    normals = axes[np.arange(len(pairs)), k] * np.where(sel < 0, -1, 1)[:, None]
    rad = 0.5 * (1 + np.abs(np.cos(a - b)) + np.abs(np.sin(a - b)))
    return normals, np.abs(sel) - rad


def check(P: np.ndarray, tol: float = -1e-9) -> dict:
    """Exact float64 validity of a layout."""
    Q = np.asarray(P, dtype=np.float64)
    xmin, ymin, xmax, ymax = bounds(Q)
    L = float(max(xmax - xmin, ymax - ymin))
    pairs, sep = separations(Q, candidate_pairs(Q, margin=1e-6))
    return {
        "L": L,
        "width": float(xmax - xmin),
        "height": float(ymax - ymin),
        "min_sep": float(sep.min()) if len(sep) else math.inf,
        "n_pairs": int(len(pairs)),
        "inside": bool(xmin >= -1e-9 and ymin >= -1e-9),
        "valid": bool(
            xmin >= -1e-9 and ymin >= -1e-9 and (len(sep) == 0 or sep.min() >= tol)
        ),
    }


def restore_lp(
    P: np.ndarray,
    target: float,
    trust: float = 0.02,
    clearance: float = CLEARANCE,
    time_limit: float = 30.0,
) -> tuple[np.ndarray | None, dict]:
    """Repair/compress to ``target`` with frozen angles; verified layout or None."""
    n = len(P)
    L = side_length(P)
    half = 0.5 * (np.abs(np.cos(P[:, 2])) + np.abs(np.sin(P[:, 2])))
    # Any centre moves at most trust per axis, so 2*sqrt(2)*trust covers every
    # pair that could become a new contact.
    margin = 2 * math.sqrt(2) * trust + 1e-6
    pairs = candidate_pairs(P, margin=margin)
    normals, gap = pair_axes(P, pairs)
    rows: list = []
    cols: list = []
    vals: list = []
    rhs: list = []
    for (i, j), nv, g in zip(pairs, normals, gap):
        r = len(rhs)
        rows += [r, r, r, r]
        cols += [2 * i, 2 * i + 1, 2 * j, 2 * j + 1]
        vals += [nv[0], nv[1], -nv[0], -nv[1]]
        rhs.append(g - clearance)
    for k in range(2 * n):
        r = len(rhs)
        rows += [r, r]
        cols += [k, 2 * n + k]
        vals += [1.0, -1.0]
        rhs.append(0.0)
        r = len(rhs)
        rows += [r, r]
        cols += [k, 2 * n + k]
        vals += [-1.0, -1.0]
        rhs.append(0.0)
    A = coo_matrix((vals, (rows, cols)), shape=(len(rhs), 4 * n)).tocsr()
    lo = np.stack([half, half], 1).ravel() - P[:, :2].ravel()
    hi = np.stack([target - half, target - half], 1).ravel() - P[:, :2].ravel()
    bnds = [(max(-trust, lo[k]), min(trust, hi[k])) for k in range(2 * n)]
    bnds += [(0.0, None)] * (2 * n)
    report = {
        "n": n,
        "before_L": L,
        "target_L": target,
        "dL": L - target,
        "pairs": int(len(pairs)),
        "trust": trust,
        "status": None,
        "feasible": False,
    }
    if any(b[0] > b[1] for b in bnds[: 2 * n]):
        report["status"] = "trust_region_outside_box"
        return None, report
    c = np.r_[np.zeros(2 * n), np.ones(2 * n)]
    res = linprog(
        c,
        A_ub=A,
        b_ub=np.asarray(rhs),
        bounds=bnds,
        method="highs",
        options={
            "primal_feasibility_tolerance": 1e-10,
            "dual_feasibility_tolerance": 1e-9,
            "time_limit": time_limit,
        },
    )
    report["status"] = int(res.status)
    report["message"] = str(res.message)[:120]
    if res.status != 0 or res.x is None:
        return None, report
    Q = P.copy()
    Q[:, :2] += res.x[: 2 * n].reshape(-1, 2)
    chk = check(Q)
    report.update(
        after_L=chk["L"],
        min_sep=chk["min_sep"],
        inside=chk["inside"],
        move_max=float(np.abs(res.x[: 2 * n]).max()),
        sum_abs_move=float(res.x[2 * n :].sum()),
    )
    # The LP uses the argmax SAT axis per pair, which is a valid separating
    # certificate, so a clean post-check makes the result admissible.
    ok = chk["inside"] and chk["min_sep"] >= -1e-9 and chk["L"] <= target + 1e-7
    report["feasible"] = bool(ok)
    if not ok:
        report["status"] = "postcheck_rejected"
        return None, report
    return Q, report


def compress_lp(
    P: np.ndarray,
    dL: float,
    trust: float = 0.02,
    clearance: float = CLEARANCE,
    time_limit: float = 30.0,
) -> tuple[np.ndarray | None, dict]:
    """Shrink the box by ``dL`` with frozen angles; returns a verified layout."""
    L = side_length(P)
    Q, rep = restore_lp(P, L - dL, trust, clearance, time_limit)
    if Q is not None and rep["after_L"] >= L - 1e-9:
        rep["feasible"] = False
        rep["status"] = "no_strict_gain"
        return None, rep
    return Q, rep



def descend(
    P: np.ndarray, dLs: list[float], trust: float = 0.02, rounds: int = 3
) -> tuple[np.ndarray, list[dict]]:
    """Greedy ladder with ascending targets.

    Feasibility is monotone in ``dL`` at a fixed layout, so the first failing
    target ends the ladder; only geometries that admit a 1e-6 shrink are ever
    asked for more.
    """
    cur = P.copy()
    trace: list[dict] = []
    for dL in dLs:
        for _ in range(rounds):
            Q, rep = compress_lp(cur, dL, trust=trust)
            trace.append(rep)
            if Q is None:
                return cur, trace
            if rep["after_L"] >= side_length(cur) - 1e-9:
                return cur, trace
            cur = Q
    return cur, trace


def load_groups(csv_path: Path) -> dict[int, np.ndarray]:
    df = pd.read_csv(csv_path)
    out: dict[int, np.ndarray] = {}
    for n, g in df.groupby("n", sort=True):
        out[int(n)] = normalize(g[["x", "y", "angle"]].to_numpy(float))
    return out


def ladder_diagnose(P: np.ndarray, dLs: list[float]) -> list[dict]:
    """Feasibility ladder at frozen angles (infeasible => rigid contact graph)."""
    out = []
    for dL in dLs:
        t0 = time.time()
        Q, rep = compress_lp(P, dL)
        rep["seconds"] = time.time() - t0
        rep["won"] = Q is not None
        if Q is not None:
            out.append(rep)
            break  # monotone in dL: larger shrink already impossible
        out.append(rep)
    return out


def kick_rounds(
    P: np.ndarray,
    *,
    depths: tuple[float, ...] = (1e-3, 1e-3, 1e-3, 4e-3, 12e-3, 1e-3, 1e-3, 3e-2),
    noises: tuple[tuple[float, float], ...] = (
        (0.0, 0.0),
        (0.0, 0.0),
        (0.0, 0.0),
        (2e-3, 1e-3),
        (15e-3, 6e-3),
    ),
    seed: int = 0,
    kind: str = "noise",
    band_deg: float = 5.0,
) -> tuple[np.ndarray, list[dict], int]:
    """Public-notebook style depth/noise schedule with LP restore (CPU port).

    Each round perturbs the incumbent (white noise or a coherent rotation of
    the tilted band), repairs at the incumbent side with trust 0.12, then
    demands ``L - depth`` through a 0.12 -> 0.02x4 restore ladder.  Only
    exact-valid layouts with a strictly smaller side are kept.
    """
    rng = np.random.default_rng(seed)
    cur = P.copy()
    base_L = side_length(cur)
    trace: list[dict] = []
    wins = 0
    for rnd, depth in enumerate(depths):
        nx, na = noises[min(rnd, len(noises) - 1)]
        if nx == 0.0 and na == 0.0 and depth > 4e-3:
            depth = 1e-3  # zero-noise rounds cannot jump; keep them cheap
        Q = cur.copy()
        if kind == "band" and na > 0:
            tilt = np.abs(
                (np.degrees(Q[:, 2]) % 90 + 45) % 90 - 45
            ) > band_deg
            if tilt.any():
                delta = rng.uniform(-na, na)
                Q[tilt, 2] += delta
                Q[tilt, :2] += rng.uniform(-nx, nx, (int(tilt.sum()), 2))
        elif nx > 0 or na > 0:
            Q[:, :2] += rng.uniform(-nx, nx, (len(Q), 2))
            Q[:, 2] += rng.uniform(-na, na, len(Q))
        Q = normalize(Q)
        Lp = side_length(Q)
        # 1) repair at the perturbed side, generous trust
        R, rep = restore_lp(Q, Lp, trust=0.12)
        entry = {"round": rnd, "depth": depth, "noise": [nx, na], "perturbed_L": Lp}
        if R is None:
            entry.update(stage="repair_failed", status=rep.get("status"))
            trace.append(entry)
            continue
        # 2) demand L - depth, trust 0.12 then 0.02 x4
        target = side_length(R) - depth

        got = None
        for k, tr in enumerate((0.12, 0.02, 0.02, 0.02, 0.02)):
            S, r2 = restore_lp(R, target, trust=tr)
            if S is not None:
                got = S
                entry.update(stage=f"target_ok@{tr}", after_L=side_length(S))
                break
            entry.update(stage=f"target_fail@{tr}", status=r2.get("status"))
        if got is not None and side_length(got) < base_L - 1e-9:
            cur = got
            base_L = side_length(got)
            wins += 1
            entry["win"] = True
        trace.append(entry)
    return cur, trace, wins


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", default=str(ROOT / "outputs/merged/v124_plus_daily44/submission.csv"))
    ap.add_argument("--out-dir", default=str(ROOT / "outputs/experiments/research_20261111/cpu_opt"))
    ap.add_argument("--mode", choices=["diagnose", "sweep", "kick"], default="diagnose")
    ap.add_argument("--n-list", default="971,911,910,791,972")
    ap.add_argument("--min-n", type=int, default=2)
    ap.add_argument("--max-n", type=int, default=1000)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--shards", type=int, default=1)
    ap.add_argument("--trust", type=float, default=0.02)
    ap.add_argument("--attempts", type=int, default=3)
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--kinds", default="noise,band")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    groups = load_groups(Path(args.baseline))

    if args.mode == "diagnose":
        ns = [int(v) for v in args.n_list.split(",") if v]
        ladders = [3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5, 3e-6, 1e-6]
        rows = []
        for n in ns:
            P = groups[n]
            before = side_length(P)
            chk = check(P)
            lad = ladder_diagnose(P, ladders)
            best = None
            for dL in ladders:
                Q, rep = compress_lp(P, dL)
                if Q is not None:
                    chkq = check(Q)
                    best = {"dL": dL, **chkq}
                    Q_out = Q
                    break
            rows.append(
                {
                    "n": n,
                    "before_L": before,
                    "score": before / math.sqrt(n) - 1,
                    "min_sep": chk["min_sep"],
                    "n_pairs": chk["n_pairs"],
                    "valid": chk["valid"],
                    "LP": lad,
                    "first_feasible": best,
                }
            )
            print(
                f"n={n} L={before:.9f} minsep={chk['min_sep']:.2e} "
                f"pairs={chk['n_pairs']} | "
                + " ".join(
                    f"dL={r['dL']:.0e}:{'OK' if r['won'] else 'INFEAS'}"
                    for r in lad
                ),
                flush=True,
            )
            if best is not None:
                np.save(out_dir / f"lp_win_{n}.npy", Q_out)
        (out_dir / "diagnose.json").write_text(json.dumps(rows, indent=1))
        return 0

    if args.mode == "kick":
        ns = [int(v) for v in args.n_list.split(",") if v]
        kinds = [k for k in args.kinds.split(",") if k]
        all_rows = []
        for n in ns:
            P = groups[n]
            before = side_length(P)
            best = P.copy()
            rows = []
            t0 = time.time()
            for kind in kinds:
                for seed in range(args.attempts):
                    Q, trace, wins = kick_rounds(P, seed=1000 * seed + n, kind=kind)
                    Lq = side_length(Q)
                    rows.append(
                        {
                            "n": n,
                            "kind": kind,
                            "seed": seed,
                            "before_L": before,
                            "after_L": Lq,
                            "wins": wins,
                            "valid": check(Q)["valid"],
                            "trace": trace,
                        }
                    )
                    if check(Q)["valid"] and Lq < side_length(best) - 1e-9:
                        best = Q
                    if time.time() - t0 > args.seconds:
                        break
                if time.time() - t0 > args.seconds:
                    break
            after = side_length(best)
            print(
                f"n={n} {before:.9f} -> {after:.9f} "
                f"(gain {(before - after) / math.sqrt(n):+.3e}) "
                f"{len(rows)} attempts {time.time() - t0:.1f}s",
                flush=True,
            )
            if after < before - 1e-9:
                np.save(out_dir / f"kick_win_{n}.npy", best)
            all_rows.append(
                {
                    "n": n,
                    "before_L": float(before),
                    "after_L": float(after),
                    "gain": float((before - after) / math.sqrt(n)),
                    "attempts": rows,
                }
            )
        (out_dir / "kick.json").write_text(json.dumps(all_rows, indent=1))
        return 0

    # sweep
    t_start = time.time()
    ns = [
        n
        for n in range(args.min_n, args.max_n + 1)
        if n % args.shards == args.shard and n in groups
    ]
    dLs = [1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3]
    winners: list[dict] = []
    for k, n in enumerate(ns):
        P = groups[n]
        before = side_length(P)
        cur, trace = descend(P, dLs, trust=args.trust, rounds=3)
        after = side_length(cur)
        if after < before - 1e-9:
            chk = check(cur)
            if chk["valid"]:
                winners.append(
                    {
                        "n": n,
                        "before_L": float(before),
                        "after_L": float(after),
                        "gain": float((before - after) / math.sqrt(n)),
                        "min_sep": chk["min_sep"],
                        "rounds": len([t for t in trace if t.get("feasible")]),
                    }
                )
                np.save(out_dir / f"win_{n}.npy", cur)
        if k % 50 == 0:
            print(
                f"[shard {args.shard}] {k}/{len(ns)} n={n} winners={len(winners)} "
                f"t={time.time() - t_start:.1f}s",
                flush=True,
            )
    (out_dir / f"sweep_shard{args.shard}.json").write_text(
        json.dumps(
            {
                "shard": args.shard,
                "shards": args.shards,
                "range": [args.min_n, args.max_n],
                "seconds": time.time() - t_start,
                "winners": winners,
            },
            indent=1,
        )
    )
    print(
        f"[shard {args.shard}] done {len(ns)} puzzles, {len(winners)} winners, "
        f"gain {sum(w['gain'] for w in winners):.8f}, {time.time() - t_start:.1f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
