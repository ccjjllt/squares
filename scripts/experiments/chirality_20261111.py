"""Chirality-flip and stretch probes on the current best packing (2026-11-11).

Ideas taken from public notebooks:
  * jonathan1506/joegun-22-2004-stretch-fault-line-dp-fq-quench: "flipped arms"
    (one tilted band reflected, then fq-quenched) and stretch.
  * az05192000gmailcom/22-2401-stretching-good-packings-to-nearby-n: cut a
    tilted arm column/row and re-insert it, then quench.
  * malyshevdanil living-atlas contact polish, via squares.search.free_polish.

Each candidate is certified by the vendored official v20 metric on the exact
float64 literals the board parses.  Only strict improvements are written.

Write scope: outputs/experiments/research_20261111/faultline/ (chirality_*).
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


def flip_band(P: np.ndarray, mask: np.ndarray, axis: int) -> np.ndarray:
    """Reflect the band across the line through its centre along `axis`, negate angles."""
    Q = P.copy()
    c = 0.5 * (P[mask, axis].min() + P[mask, axis].max())
    Q[mask, axis] = 2 * c - Q[mask, axis]
    Q[mask, 2] = -Q[mask, 2]
    return S.normalize(Q)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--targets", default="971,910,908,642,849,634,687,328")
    ap.add_argument("--out", required=True)
    ap.add_argument("--polish-seeds", default="0,1,2")
    ap.add_argument("--polish-seconds", type=float, default=12.0)
    ap.add_argument("--flip", action="store_true")
    ap.add_argument("--flip-seconds", type=float, default=10.0)
    args = ap.parse_args()
    targets = [int(v) for v in args.targets.split(",") if v]
    seeds = [int(v) for v in args.polish_seeds.split(",") if v]
    os.makedirs(args.out, exist_ok=True)
    df = pd.read_csv(args.base)
    groups = {int(n): g.sort_values("square_id")["square_id"].to_numpy() for n, g in df.groupby("n")}
    raw = {int(n): g.sort_values("square_id")[["x", "y", "angle"]].to_numpy(float) for n, g in df.groupby("n")}
    report: dict = {"targets": {}}
    lines = ["id,n,square_id,x,y,angle"]
    total = 0.0
    for n in targets:
        P = raw[n]
        L0 = S.side_length(P)
        entry: dict = {"old_L": L0, "polish": [], "flips": []}
        best = None
        # --- free-angle contact polish of the current packing -----------------
        for seed in seeds:
            Q, trace, sec = polish(P, rounds=28, seed=seed, max_seconds=args.polish_seconds)
            Lq = S.side_length(Q)
            certL, why = certify(n, Q)
            row = {"seed": seed, "L": Lq, "certified": certL is not None, "why": why, "steps": len(trace)}
            if certL is not None and certL < L0 - 1e-10:
                row["accepted"] = True
                if best is None or certL < best[0]:
                    best = (certL, Q)
            entry["polish"].append(row)
            log(f"n={n} polish seed={seed}: {Lq:.9f} cert={certL is not None} {why}")
        # --- chirality flip of one tilted band --------------------------------
        if args.flip:
            bands = S.bands(P)
            entry["bands"] = [
                {"count": int(m.sum()), "axis": int(ax), "mean_tilt": float(S.tilt(P)[m].mean())}
                for m, ax, _ in bands
            ]
            for bi, (m, ax, _) in enumerate(bands):
                if abs(float(S.tilt(P)[m].mean())) < 2.0:
                    continue
                Q = flip_band(P, m, ax)
                pairs, sep = S.separations(Q)
                worst = float(sep.min()) if len(sep) else 0.0
                row = {"band": bi, "axis": int(ax), "members": int(m.sum()), "flip_worst_pen": worst}
                row["flip_overlaps"] = int((sep < -1e-9).sum()) if len(sep) else 0
                if worst < -0.3:
                    # overlaps are far too deep for a local repulsion; try a
                    # short soft-contact quench anyway, it is the only repair
                    # we have without the Rust fq binary.
                    Qq, info = soft_quench(
                        Q,
                        eps_schedule=(0.05, 0.02, 0.01, 3e-3),
                        weight=3.0,
                        max_iter_per_stage=120,
                        max_seconds=args.flip_seconds,
                        jitter=0.0,
                    )
                    row["soft_after_L"] = float(info["after_L"])
                    row["soft_improved"] = bool(info.get("improved", False))
                    Q = Qq
                Qp, trace, sec = polish(Q, rounds=28, seed=bi, max_seconds=args.polish_seconds)
                Lq = S.side_length(Qp)
                certL, why = certify(n, Qp)
                row.update({"L": Lq, "certified": certL is not None, "why": why, "steps": len(trace)})
                if certL is not None and certL < L0 - 1e-10:
                    row["accepted"] = True
                    if best is None or certL < best[0]:
                        best = (certL, Qp)
                entry["flips"].append(row)
                log(f"n={n} flip band={bi} ax={ax}: worst {worst:.3f} -> {Lq:.9f} cert={certL is not None} {why}")
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
    with open(os.path.join(args.out, "chirality_report.json"), "w") as fh:
        json.dump(report, fh, indent=2)
    with open(os.path.join(args.out, "chirality_improved.csv"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    log(f"total gain {total:.6f}; rows {len(lines) - 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
