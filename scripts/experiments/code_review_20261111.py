"""Insertion ("vacancy") operator: build an (n+1)-packing from an n-packing.

New vs. our pipeline and vs. public code reviewed 2026-11-11:
  * alexchilton/closure.py only *deletes* a square from n+1 (downward closure) and
    expands whole border rows; nilanjansaha `drop_to`/`expand` do the same.
  * lucifer19 `vacancy_scan` (cell 79) is the only public insertion probe we found,
    but its obstacle is `convex_hull(all corners - new_square)`, i.e. the convex
    hull of the whole packing, which covers nearly the entire box; it is a
    diagnostic that reports "geometric leads", not a constructor.
Here the free space for the new square's centre is tested exactly with SAT
against every existing square (4 separating axes per pair), for a grid of
candidate centres and a sweep of angles, with a monotone binary search on the
container side T in [L_n, L_{n+1}).

Only a candidate that the official interval metric accepts after the float64
round trip is reported as a win.

Usage:
  .venv/bin/python scripts/experiments/code_review_20261111.py \
      --base outputs/merged/v124_plus_daily44/submission.csv --top 12
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from squares._vendor import official_metric as metric  # noqa: E402
from squares.search.structure import corners, normalize, side_length  # noqa: E402

OUT = ROOT / "outputs/experiments/research_20261111/code_review"


def load_base(path: Path) -> dict[int, np.ndarray]:
    out: dict[int, np.ndarray] = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    by_n: dict[int, list[tuple[int, float, float, float]]] = {}
    for r in rows:
        by_n.setdefault(int(r["n"]), []).append(
            (int(r["square_id"]), float(r["x"]), float(r["y"]), float(r["angle"]))
        )
    for n, g in by_n.items():
        if len(g) != n:
            continue
        g.sort()
        out[n] = np.array([[x, y, a] for _, x, y, a in g], dtype=float)
    return out


def free_centers(P: np.ndarray, T: float, angle: float, grid: int, clearance: float = 2e-10):
    """Candidate centres (m,2) where a unit square at `angle` fits in [0,T]^2.

    P must already be normalised to bbox min (0,0) and side <= T.
    Exact SAT against every existing square: disjoint if some axis separates.
    """
    n = len(P)
    h = 0.5 * (abs(math.cos(angle)) + abs(math.sin(angle)))
    lo, hi = h, T - h
    if hi < lo:
        return np.empty((0, 2))
    xs = np.linspace(lo, hi, grid)
    C = corners(P)                                    # (n,4,2)
    ai = P[:, 2]
    ex = np.stack([np.stack([np.cos(ai), np.sin(ai)], -1),
                   np.stack([-np.sin(ai), np.cos(ai)], -1)], axis=1)  # (n,2,2)
    an = np.array([[math.cos(angle), math.sin(angle)],
                   [-math.sin(angle), math.cos(angle)]])
    u = np.array([[0.5 * math.cos(angle) - 0.5 * math.sin(angle), 0.5 * math.sin(angle) + 0.5 * math.cos(angle)],
                  [-0.5 * math.cos(angle) - 0.5 * math.sin(angle), -0.5 * math.sin(angle) + 0.5 * math.cos(angle)],
                  [-0.5 * math.cos(angle) + 0.5 * math.sin(angle), -0.5 * math.sin(angle) - 0.5 * math.cos(angle)],
                  [0.5 * math.cos(angle) + 0.5 * math.sin(angle), 0.5 * math.sin(angle) - 0.5 * math.cos(angle)]])
    proj_i = np.einsum("nkd,ncd->nkc", ex, C)          # existing on its own axes (n,2,4)
    U_i = np.einsum("nkd,ld->nkl", ex, u)              # new corners on existing axes (n,2,4)
    proj_C_new = np.einsum("kd,ncd->nkc", an, C)       # existing on new axes (n,2,4)
    U_new = np.einsum("kd,ld->kl", an, u)              # new corners on new axes (4,2)->(2,4)

    pts = np.stack(np.meshgrid(xs, xs, indexing="ij"), -1).reshape(-1, 2)  # (m,2)
    free = np.ones(len(pts), dtype=bool)
    chunk = 192
    for s in range(0, len(pts), chunk):
        q = pts[s:s + chunk]
        cc_i = np.einsum("md,nkd->mnk", q, ex)         # (m,n,2)
        pn = cc_i[..., None] + U_i[None]               # (m,n,2,4)
        gap_i = np.maximum(pn.min(-1) - proj_i.max(-1), proj_i.min(-1) - pn.max(-1))
        cn = (np.einsum("md,kd->mk", q, an)[:, None, :, None] + U_new[None, None])  # (m,1,2,4)
        gap_n = np.maximum(cn.min(-1) - proj_C_new.max(-1), proj_C_new.min(-1) - cn.max(-1))
        gap = np.maximum(gap_i, gap_n).max(-1)          # (m,n) best axis
        free[s:s + chunk] = (gap.min(1) >= clearance)
    return pts[free]


def repair(P: np.ndarray, clearance: float = 4e-10) -> np.ndarray | None:
    """Uniform centre dilation until every pair is separated (mirrors public repair)."""
    from scipy.spatial import cKDTree

    P = normalize(P)
    pairs = cKDTree(P[:, :2]).query_pairs(math.sqrt(2) + 1e-4, output_type="ndarray")
    if len(pairs):
        i, j = pairs.T
        a = P[:, 2]
        c, s = np.cos(a), np.sin(a)
        d = P[j, :2] - P[i, :2]
        ux = np.column_stack((c[i], -s[i], c[j], -s[j]))
        uy = np.column_stack((s[i], c[i], s[j], c[j]))
        pr = d[:, 0, None] * ux + d[:, 1, None] * uy
        dth = a[j] - a[i]
        rad = 0.5 * (1 + np.abs(np.cos(dth)) + np.abs(np.sin(dth))) + clearance
        f = float(np.max(rad / np.maximum(np.abs(pr).max(1), 1e-30)))
        if f > 1.0005:
            return None
        P = P.copy()
        P[:, :2] *= max(1.0, f)
    return normalize(P)


def certify(n: int, P: np.ndarray) -> tuple[float, np.ndarray] | None:
    P = normalize(P)
    for eps in (0.0, 1e-12, 1e-11, 1e-10):
        Q = P.copy()
        if eps:
            c = (Q[:, :2].min(0) + Q[:, :2].max(0)) / 2
            Q[:, :2] = c + (Q[:, :2] - c) * (1 + eps)
        rows = [{"n": str(n), "square_id": str(i), "x": repr(float(x)),
                 "y": repr(float(y)), "angle": repr(float(t))} for i, (x, y, t) in enumerate(Q)]
        _, _, L, why = metric.evaluate_single_puzzle(n, rows)
        if why == "ok":
            return float(L), Q
    return None


def insertion(P: np.ndarray, Tmax: float, angles: list[float], grid: int):
    """Best (T, angle, centre) with T < Tmax, or None."""
    P = normalize(P)
    L0 = side_length(P)
    clr = -1e-9                     # accept exact tangency; repair() adds clearance
    best = None
    for ang in angles:
        pts = free_centers(P, Tmax - 1e-9, ang, grid, clearance=clr)
        if not len(pts):
            continue
        # monotone feasibility in T: binary search the smallest feasible side
        lo, hi = L0, Tmax - 1e-9
        for _ in range(9):
            mid = 0.5 * (lo + hi)
            ok = len(free_centers(P, mid, ang, grid, clearance=clr))
            if ok:
                hi = mid
            else:
                lo = mid
        pts = free_centers(P, hi, ang, grid, clearance=clr)
        if len(pts) and (best is None or hi < best[0]):
            best = (hi, ang, pts[0])
    return best


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=Path, default=ROOT / "outputs/merged/v124_plus_daily44/submission.csv")
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--grid", type=int, default=64)
    ap.add_argument("--seconds", type=float, default=600.0)
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    base = load_base(args.base)
    L = {n: side_length(P) for n, P in base.items()}
    # upward-closure candidates: empty area inside the parent box (slack), then gap
    ranked = sorted((n for n in range(1, 1000) if L[n] < L[n + 1] - 1e-9),
                    key=lambda n: (L[n] ** 2 - n) + 2.0 * (L[n + 1] - L[n]), reverse=True)
    targets = ranked[: args.top]
    print(f"base={args.base} parents tested={targets}", flush=True)
    print("n  L_n      L_n+1    float gap   angle   T*        certified gain", flush=True)

    angles = [math.radians(a) for a in (0, 7.5, 15, 22.5, 30, 37.5, 45, 52.5, 60, 67.5, 75, 82.5)]
    wins = {}
    t0 = time.time()
    for n in targets:
        if time.time() - t0 > args.seconds:
            print("time budget reached", flush=True)
            break
        P = base[n]
        r = insertion(P, L[n + 1], angles, args.grid)
        if r is None:
            print(f"{n:<4} {L[n]:.6f} {L[n+1]:.6f}  none", flush=True)
            continue
        T, ang, c = r
        Q = np.vstack([P, [[c[0], c[1], ang]]])
        Q = repair(Q)
        cert = certify(n + 1, Q) if Q is not None else None
        if cert is None:
            print(f"{n:<4} {L[n]:.6f} {L[n+1]:.6f}  {L[n+1]-T:.2e}  {math.degrees(ang):5.1f}  "
                  f"{T:.6f}  NOT CERTIFIED", flush=True)
            continue
        Lc, Qc = cert
        gain = (L[n + 1] - Lc) / math.sqrt(n + 1)
        print(f"{n:<4} {L[n]:.6f} {L[n+1]:.6f}  {L[n+1]-T:.2e}  {math.degrees(ang):5.1f}  "
              f"{T:.6f}  {gain:+.3e}  L={Lc:.9f}", flush=True)
        if gain > 1e-10 and Lc < L[n + 1] - 1e-9:
            wins[n + 1] = {"parent": n, "L": Lc, "gain": gain,
                           "packing": Qc.tolist()}

    if wins:
        with open(OUT / "insertion_wins.json", "w") as f:
            json.dump(wins, f, indent=1)
        print(f"WINS {len(wins)} total gain {sum(w['gain'] for w in wins.values()):.6e}", flush=True)
    else:
        print("WINS 0", flush=True)


if __name__ == "__main__":
    main()
