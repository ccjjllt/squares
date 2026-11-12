"""Thickened multi-angle tilted-region move for targeted Squares-in-Squares puzzles.

Follows the structural lead of the rank-1 notebook
``pjmathematician/three-square-packings-that-beat-the-records``: instead of the
rigid single-angle diagonal band of the published records, use a *thicker*
tilted region whose squares carry many slightly different angles (and/or two
separate tilted corner blocks), then let the Rust ``fq`` fixed-side shrink
repair and compress it.

Variants (all preserve the square count exactly):
  T<d>  thicken: upright squares whose centre is within ``d`` of a tilted square
        are converted to the local tilted angle (+ jitter).
  I<s>  interface: only tilted squares adjacent to the upright region get a
        large angle jitter; the block interior gets a small one.
  A<s>  all tilted squares get an angle jitter.
  K<s>  global basin hop: every square gets a small angle jitter.
  C     corner flip for globally rotated layouts (911): the two extreme
        corners become upright blocks.
  S<fff> shrink the whole packing by 1-fff/1000 (a looser start), then shrink.
  B<d>  rotate each tilted block rigidly by d degrees about its own centroid
        (internally feasible; only the two interfaces are disturbed).

Every candidate is certified with the vendored official v20 metric on exactly
the float literals written out.  Only improved complete groups are written.

Write scope: outputs/experiments/research_20261111/multiangle/ only.

Usage:
  .venv/bin/python scripts/experiments/multiangle_20261111.py \
      --baseline outputs/merged/v124_plus_daily44_public2_penguin/submission.csv \
      --targets 971,911,910,791,972,908,969 --deadline 9 --seeds 1,2
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from squares._vendor import official_metric as metric  # noqa: E402

FQ = Path(
    "/private/var/folders/9s/sdk1x32s58g8dycwh6c74bqc0000gp/T/opencode"
    "/square-packing/search/packer/target/release/fq"
)
WORK = Path("outputs/experiments/research_20261111/multiangle")
T0 = time.time()


def log(*a: object) -> None:
    print(f"{time.strftime('%H:%M:%S')} [{time.time() - T0:6.0f}s]", *a, flush=True)


# ---------------------------------------------------------------- geometry
def side_and_shift(P: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    t = P[:, 2]
    c, s = np.cos(t) * 0.5, np.sin(t) * 0.5
    X = np.concatenate([P[:, 0] + c - s, P[:, 0] - c - s, P[:, 0] - c + s, P[:, 0] + c + s])
    Y = np.concatenate([P[:, 1] + s + c, P[:, 1] - s + c, P[:, 1] - s - c, P[:, 1] + s - c])
    L = float(max(X.max() - X.min(), Y.max() - Y.min()))
    return L, np.array([X.min(), Y.min()]), P


def normalize(P: np.ndarray) -> tuple[np.ndarray, float]:
    L, lo, _ = side_and_shift(P)
    Q = P.copy()
    Q[:, 0] -= lo[0]
    Q[:, 1] -= lo[1]
    L2, lo2, _ = side_and_shift(Q)
    Q[:, 0] -= lo2[0]
    Q[:, 1] -= lo2[1]
    return Q, float(max(L, L2))


def tilt_deg(P: np.ndarray) -> np.ndarray:
    return np.degrees(np.mod(P[:, 2], np.pi / 2))


def is_upright(P: np.ndarray, eps: float = 1e-3) -> np.ndarray:
    d = tilt_deg(P)
    return np.minimum(d, 90.0 - d) < eps


def write_fq(path: Path, P: np.ndarray, s: float) -> None:
    with path.open("w") as f:
        f.write(f"{len(P)} {s:.17f}\n")
        for x, y, t in P:
            f.write(f"{x:.17f} {y:.17f} {math.degrees(t):.17f}\n")


def read_fq(path: Path) -> tuple[float, np.ndarray]:
    tok = path.read_text().split()
    n, s = int(tok[0]), float(tok[1])
    v = np.array([float(q) for q in tok[2 : 2 + 3 * n]], float).reshape(n, 3)
    v[:, 2] = np.radians(v[:, 2])
    return s, v


def run_fq(P: np.ndarray, s0: float, deadline: float, seed: int, tag: str,
           work: Path, freeze: np.ndarray | None = None, shrink: bool = True,
           d0: float = 1e-2, dmin: float = 2e-6, loosen: float = 1.02,
           kick: float = 0.0) -> tuple[float, np.ndarray, dict]:
    inp = work / "work" / f"in_{tag}.txt"
    out = work / "work" / f"out_{tag}.txt"
    inp.parent.mkdir(parents=True, exist_ok=True)
    write_fq(inp, P, s0)
    cmd = [str(FQ), "quench", "--in", str(inp), "--out", str(out),
           "--seed", str(seed), "--deadline", str(deadline)]
    if shrink:
        cmd += ["--shrink", "--d0", str(d0), "--dmin", str(dmin), "--loosen", str(loosen)]
    else:
        cmd += ["--loosen", str(loosen), "--kick", str(kick)]
    if freeze is not None and freeze.any():
        idx = np.flatnonzero(freeze)
        # freeze syntax: comma separated indices / ranges
        parts, start, prev = [], int(idx[0]), int(idx[0])
        for i in idx[1:]:
            i = int(i)
            if i == prev + 1:
                prev = i
                continue
            parts.append(f"{start}-{prev}" if prev > start else f"{start}")
            start = prev = i
        parts.append(f"{start}-{prev}" if prev > start else f"{start}")
        cmd += ["--freeze", ",".join(parts)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    info: dict = {}
    for line in p.stdout.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                info = json.loads(line)
            except json.JSONDecodeError:
                pass
    if not out.exists():
        return float("nan"), P, info
    return read_fq(out)


def certify(n: int, P: np.ndarray) -> tuple[float, np.ndarray] | None:
    rows = [
        {"n": str(n), "square_id": str(i), "x": repr(float(a)),
         "y": repr(float(b)), "angle": repr(float(t))}
        for i, (a, b, t) in enumerate(P)
    ]
    _, _, L_txt, why = metric.evaluate_single_puzzle(n, rows)
    if why != "ok" or L_txt is None:
        return None
    return float(L_txt), P


# -------------------------------------------------------------- candidates
def neighbours(P: np.ndarray) -> np.ndarray:
    """True for squares with another square's centre within 1.45 units."""
    D = np.sqrt(((P[:, None, :2] - P[None, :, :2]) ** 2).sum(-1))
    np.fill_diagonal(D, 99.0)
    return D.min(1) < 1.45


def build_variant(P: np.ndarray, L: float, kind: str, rng: np.random.Generator) -> np.ndarray:
    Q = P.copy()
    up = is_upright(P)
    deg = tilt_deg(P)
    sigma = math.radians(float(kind[1:]) if kind[1:].replace(".", "").isdigit() else 2.0)
    if kind.startswith("A"):
        Q[~up, 2] += rng.normal(0, sigma, (~up).sum())
        Q[~up, :2] += rng.normal(0, 0.015, ((~up).sum(), 2))
    elif kind.startswith("I"):
        nb = neighbours(P)
        near = (~up) & nb
        inner = (~up) & ~nb
        Q[near, 2] += rng.normal(0, 4.0 * sigma, near.sum())
        Q[near, :2] += rng.normal(0, 0.03, (near.sum(), 2))
        Q[inner, 2] += rng.normal(0, sigma, inner.sum())
        Q[up & nb, :2] += rng.normal(0, 0.01, ((up & nb).sum(), 2))
    elif kind.startswith("K"):
        Q[:, 2] += rng.normal(0, sigma, len(Q))
        Q[:, :2] += rng.normal(0, 0.01, (len(Q), 2))
    elif kind.startswith("T"):
        d = float(kind[1:])
        ti = np.flatnonzero(~up)
        # distance from each upright centre to nearest tilted centre
        D = np.sqrt(((P[up][:, None, :2] - P[ti][None, :, :2]) ** 2).sum(-1))
        ui = np.flatnonzero(up)
        take = D.min(1) < d
        conv = ui[take]
        if len(conv):
            # local angle = angle of closest tilted square (same mod-pi/2 branch)
            near = ti[D.argmin(1)[take]]
            Q[conv, 2] = P[near, 2] + rng.normal(0, math.radians(1.5), len(conv))
            Q[conv, :2] += rng.normal(0, 0.02, (len(conv), 2))
        # also jitter existing tilted angles a little
        Q[~up, 2] += rng.normal(0, math.radians(0.8), (~up).sum())
    elif kind == "C":
        # two extreme corners -> upright, interior of global rotated lattice jittered
        Q[:, 2] += rng.normal(0, math.radians(0.6), len(Q))
        for cx, cy in ((0, 0), (L, L), (0, L), (L, 0)):
            dd = np.hypot(P[:, 0] - cx, P[:, 1] - cy)
            corner = dd < 0.30 * L
            Q[corner, 2] = rng.choice([0.0, math.pi / 2], corner.sum())
    elif kind.startswith("S"):
        f = float(kind[1:]) / 1000.0
        Q[:, :2] = L / 2 + (Q[:, :2] - L / 2) * f
        Q[~up, 2] += rng.normal(0, math.radians(0.6), (~up).sum())
        Q[up, 2] = 0.0
    elif kind.startswith("B"):
        # rotate each tilted block as a rigid body about its centroid
        delta = math.radians(float(kind[1:]))
        ti = np.flatnonzero(~up)
        if len(ti):
            # split into 2 blocks by the sign of (y - x) after removing the mean
            q = ti
            key = P[q, 1] - P[q, 0]
            for side in (key > np.median(key), key <= np.median(key)):
                idx = q[side]
                if len(idx) < 10:
                    continue
                c = P[idx, :2].mean(0)
                d = P[idx, :2] - c
                R = np.array([[math.cos(delta), -math.sin(delta)],
                              [math.sin(delta), math.cos(delta)]])
                Q[idx, :2] = d @ R.T + c
                Q[idx, 2] += delta
    else:
        raise ValueError(kind)
    Q, _ = normalize(Q)
    return Q


# ------------------------------------------------------------------ driver
def jobs_for(n: int, P: np.ndarray, L: float, variants: list[str], seeds: list[int],
             deadline: float, shrink: bool) -> list[dict]:
    out = []
    for v in variants:
        for seed in seeds:
            out.append({"n": n, "variant": v, "seed": seed, "deadline": deadline,
                        "shrink": shrink, "L0": L})
    return out


def run_job(job: dict) -> dict:
    n, v, seed = job["n"], job["variant"], job["seed"]
    base = pd.read_csv(job["base"])
    g = base[base.n == n].sort_values("square_id")
    P = g[["x", "y", "angle"]].to_numpy(float)
    P, L0 = normalize(P)
    rng = np.random.default_rng(1000 * n + 17 * seed + sum(map(ord, v)))
    Q = build_variant(P, L0, v, rng)
    tag = f"{n}_{v}_{seed}"
    s, R = run_fq(Q, L0, job["deadline"], seed, tag, Path(job["work"]),
                  shrink=job["shrink"])
    if not np.isfinite(s) or not len(R):
        return {**job, "ok": False, "s": None}
    R, Lr = normalize(R)
    cert = certify(n, R)
    if cert is None:
        return {**job, "ok": False, "s": float(s), "msg": "invalid"}
    Lc, Rc = cert
    return {**job, "ok": True, "s": float(s), "L": Lc, "P": Rc}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", default="outputs/merged/v124_plus_daily44_public2_penguin/submission.csv")
    ap.add_argument("--targets", default="971,911,910,791,972,908,969")
    ap.add_argument("--variants", default="T2.0,T3.5,A1.0,A2.5,I1.0,I2.0,K0.5")
    ap.add_argument("--seeds", default="1,2")
    ap.add_argument("--deadline", type=float, default=9.0)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--quench", action="store_true", help="plain kick quench instead of shrink")
    ap.add_argument("--out", default=str(WORK))
    args = ap.parse_args()
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    base = pd.read_csv(args.baseline)
    targets = [int(x) for x in args.targets.split(",") if x]
    variants = [x for x in args.variants.split(",") if x]
    seeds = [int(x) for x in args.seeds.split(",") if x]

    # current L per target
    cur = {}
    for n in targets:
        g = base[base.n == n].sort_values("square_id")
        P, L = normalize(g[["x", "y", "angle"]].to_numpy(float))
        cur[n] = (L, P)

    specs = []
    for n in targets:
        L, _ = cur[n]
        specs += jobs_for(n, None, L, variants, seeds, args.deadline, not args.quench)
    for s in specs:
        s["base"] = args.baseline
        s["work"] = str(outdir)

    log(f"{len(specs)} jobs, {args.workers} workers, deadline {args.deadline}s")
    results = []
    with Pool(args.workers) as pool:
        for r in pool.imap_unordered(run_job, specs):
            results.append(r)
            if r.get("ok") and r["L"] < cur[r["n"]][0] - 1e-10:
                log(f"  WIN n={r['n']} {r['variant']} seed={r['seed']} "
                    f"L {cur[r['n']][0]:.12f} -> {r['L']:.12f}")
            else:
                got = f"{r['L']:.9f}" if r.get("ok") else ("invalid" if r.get("msg") else "no-out")
                log(f"  n={r['n']:3d} {r['variant']:5s} s{r['seed']} L0={r['L0']:.6f} -> {got}")

    # collect best per n / variant
    best: dict[int, dict] = {}
    for r in results:
        if not r.get("ok"):
            continue
        if r["n"] not in best or r["L"] < best[r["n"]]["L"]:
            best[r["n"]] = r

    rows = []
    for n, r in sorted(best.items()):
        if r["L"] < cur[n][0] - 1e-10:
            for i, (x, y, t) in enumerate(r["P"]):
                rows.append({"id": n, "n": n, "square_id": i,
                             "x": repr(float(x)), "y": repr(float(y)),
                             "angle": repr(float(t))})
    if rows:
        pd.DataFrame(rows).to_csv(outdir / "improved_groups.csv", index=False)
    slim = [{k: v for k, v in r.items() if k != "P"} for r in results]
    pd.DataFrame(slim).to_csv(outdir / "runs.csv", index=False)
    summary = [
        {"n": n, "L_before": cur[n][0],
         "L_best": best[n]["L"] if n in best else None,
         "variant": best[n]["variant"] if n in best else None,
         "seed": best[n]["seed"] if n in best else None,
         "gain": (cur[n][0] - best[n]["L"]) if n in best else 0.0,
         "wins": sum(1 for r in results if r.get("ok") and r["n"] == n and r["L"] < cur[n][0] - 1e-10),
         "runs": sum(1 for r in results if r["n"] == n)}
        for n in targets
    ]
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    log("summary:")
    for s in summary:
        log(f"  n={s['n']:3d} L {s['L_before']:.12f} best "
            f"{s['L_best'] if s['L_best'] is None else round(s['L_best'], 12)} "
            f"gain {(s['gain'] or 0):.3e} wins {s['wins']}/{s['runs']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
