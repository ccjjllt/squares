"""Gap insertion probe: take the best packing for a nearby m and insert one
unit square into the largest cavity, then contact-polish.

This is the +1 case of the public stretch/insertion family
(az05192000gmailcom/22-2401-stretching-good-packings-to-nearby-n; JoeGun's
"Stretch" section): a donor m < n with a smaller side is extended by one
square and shaken back into feasibility.  The cavity search below is ours.

Only certified strict improvements are written.
Write scope: outputs/experiments/research_20261111/faultline/.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from squares._vendor import official_metric as metric  # noqa: E402
from squares.search import structure as S  # noqa: E402
from squares.search.free_polish import polish  # noqa: E402
from squares.search.soft_quench import soft_quench  # noqa: E402

T0 = time.time()


def log(*a):
    print(f"{time.strftime('%H:%M:%S')} [{time.time() - T0:6.0f}s]", *a, flush=True)


def certify(n: int, sq: np.ndarray):
    rows = [
        {"n": str(n), "square_id": str(i), "x": repr(float(x)), "y": repr(float(y)), "angle": repr(float(t))}
        for i, (x, y, t) in enumerate(sq)
    ]
    _, _, detail, why = metric.evaluate_single_puzzle(n, rows)
    return (float(detail), why) if why == "ok" and detail else (None, why)


def pair_sep(P: np.ndarray, centers: np.ndarray, angle: float, nbr: np.ndarray) -> np.ndarray:
    """SAT separation between each candidate (center, angle) and its neighbours."""
    M, K = nbr.shape
    j = nbr.ravel()
    cy = P[j, 1]
    cx = P[j, 0]
    aj = P[j, 2]
    # candidate corners
    ca, sa = math.cos(angle), math.sin(angle)
    cdx = 0.5 * (np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]]) @ np.array([[ca, sa], [-sa, ca]]).T)
    # P corners (K,4,2) per candidate row via broadcast
    C = S.corners(P)  # (n,4,2)
    cj = C[j].reshape(M, K, 4, 2)
    cc = centers[:, None, :] + cdx[None, :, :]  # (M,4,2)
    axes = np.stack(
        [
            np.stack([np.full(M * K, ca), np.full(M * K, sa)], -1),
            np.stack([np.full(M * K, -sa), np.full(M * K, ca)], -1),
            np.stack([np.cos(aj), np.sin(aj)], -1),
            np.stack([-np.sin(aj), np.cos(aj)], -1),
        ],
        axis=1,
    ).reshape(M, K, 4, 2)
    pc = np.einsum("mkad,mcd->mkac", axes, cc)
    pj = np.einsum("mkad,mkcd->mkac", axes, cj)
    gap = np.maximum(pj.min(-1) - pc.max(-1), pc.min(-1) - pj.max(-1))
    return gap.max(-1)  # (M,K)


def cavity_candidates(P: np.ndarray, step: float = 0.3, angles_deg=(0, 20, 40, 45)):
    P = S.normalize(P)
    L = S.side_length(P)
    g = np.arange(0.35, L - 0.35 + 1e-9, step)
    tree = cKDTree(P[:, :2])
    out = []
    for ang in angles_deg:
        a = math.radians(ang)
        h = 0.5 * (abs(math.cos(a)) + abs(math.sin(a)))
        gx = g[(g > h) & (g < L - h)]
        if len(gx) < 2:
            continue
        X, Y = np.meshgrid(gx, gx, indexing="ij")
        cent = np.column_stack([X.ravel(), Y.ravel()])
        k = min(8, len(P))
        _, nbr = tree.query(cent, k=k)
        sep = pair_sep(P, cent, a, nbr)
        score = sep.min(1)
        top = np.argsort(score)[-12:]
        out.extend((float(score[t]), float(cent[t, 0]), float(cent[t, 1]), ang) for t in top)
    out.sort(reverse=True)
    seen, res = set(), []
    for s, x, y, ang in out:
        key = (round(x, 2), round(y, 2))
        if key in seen:
            continue
        seen.add(key)
        res.append((s, x, y, ang))
        if len(res) >= 12:
            break
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--targets", default="971,910,908,642,849")
    ap.add_argument("--donors", default="", help="comma-separated n offsets tried in order")
    ap.add_argument("--out", required=True)
    ap.add_argument("--top", type=int, default=4)
    ap.add_argument("--polish-seconds", type=float, default=8.0)
    ap.add_argument("--soft-seconds", type=float, default=5.0)
    args = ap.parse_args()
    offsets = [int(v) for v in args.donors.split(",") if v] or [-1, -2, 1]
    targets = [int(v) for v in args.targets.split(",") if v]
    os.makedirs(args.out, exist_ok=True)
    df = pd.read_csv(args.base)
    raw = {int(n): g.sort_values("square_id")[["x", "y", "angle"]].to_numpy(float) for n, g in df.groupby("n")}
    L = {n: S.side_length(sq) for n, sq in raw.items()}
    report: dict = {"targets": {}}
    lines = ["id,n,square_id,x,y,angle"]
    total = 0.0
    for n in targets:
        L0 = L[n]
        entry: dict = {"old_L": L0, "attempts": []}
        best = None
        for off in offsets:
            m = n + off
            if m not in raw or L[m] >= L0 - 1e-12:
                continue
            P = S.normalize(raw[m])
            cands = cavity_candidates(P)
            entry["attempts"].append({"donor": m, "donor_L": L[m], "cavities": len(cands),
                                      "best_gap": cands[0][0] if cands else None})
            log(f"n={n} donor m={m} L={L[m]:.6f} cavities={len(cands)} best_gap={cands[0][0]:.4f}")
            for r, (gap, x, y, ang) in enumerate(cands[: args.top]):
                Q = np.vstack([P, np.array([[x, y, math.radians(ang)]])])
                if gap < -0.02:
                    Q, _info = soft_quench(
                        Q,
                        eps_schedule=(0.03, 0.01, 3e-3, 1e-3),
                        weight=3.0,
                        max_iter_per_stage=100,
                        max_seconds=args.soft_seconds,
                        jitter=0.0,
                    )
                for seed in (0, 1):
                    Qp, trace, sec = polish(Q, rounds=28, seed=seed, max_seconds=args.polish_seconds)
                    Lq = S.side_length(Qp)
                    certL, why = certify(n, Qp)
                    ok = certL is not None and certL < L0 - 1e-10
                    entry["attempts"].append(
                        {"donor": m, "cavity": r, "gap": gap, "seed": seed, "L": Lq,
                         "certified": certL is not None, "why": why, "accepted": ok}
                    )
                    log(f"  n={n} m={m} cav={r} gap={gap:.3f} seed={seed}: L={Lq:.9f} "
                        f"cert={certL is not None} {why}")
                    if ok and (best is None or certL < best[0]):
                        best = (certL, Qp)
        if best is not None:
            Lb, Qb = best
            gain = (L0 - Lb) / math.sqrt(n)
            total += gain
            entry.update({"new_L": Lb, "gain": gain, "status": "accepted"})
            log(f"n={n}: ACCEPT {Lb:.9f} vs {L0:.9f} gain {gain:.3e}")
            for i, (x, y, t) in enumerate(Qb):
                lines.append(f"{len(lines) - 1},{n},{i},{repr(float(x))},{repr(float(y))},{repr(float(t))}")
        else:
            entry["status"] = "no improvement"
        report["targets"][str(n)] = entry
    report["total_gain"] = total
    with open(os.path.join(args.out, "insert_report.json"), "w") as fh:
        json.dump(report, fh, indent=2)
    with open(os.path.join(args.out, "insert_improved.csv"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    log(f"total gain {total:.6f}; rows {len(lines) - 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
