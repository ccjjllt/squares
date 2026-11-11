"""Long-tail structural probes on the current best packing (2026-11-11).

Targets: n whose per-n score gap ``(L - L_best)/sqrt(n)`` is in the long tail
(1e-4 .. 6e-4), prioritising n in 200..600 plus 147/156/199.

Why insertion: the local optimum is saturated (cold polish never moves), and a
global mirror is an isometry, so neither can open a new basin.  The record gap
is ~1e-4..6e-4 in score, i.e. 0.01%..0.3% in L, which is exactly the scale of
"neighbouring n's layout re-used at this n".  So the moves are

  I  insert one square into the largest gap of the n-1 layout, then polish
     (two candidate orientations: upright and the dominant lattice tilt);
  D  delete one boundary square from the n+1 layout, then polish;
  R  deep second-round polish of anything that certified below the incumbent.

Every candidate is serialized as ``repr(float)`` and certified with the
vendored official v20 metric.  ``structure.normalize`` output can overlap at
the 1e-15 level (translation changes the float64 rounding), which the interval
metric rejects, so every candidate is dilated by a 4e-11 centre clearance -
the same repair the repo's own polish uses - before certification; that costs
~1e-9 in L.

Write scope: outputs/experiments/research_20261111/longtail/.
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
from squares.search.gpu_relax import repair_with_diagnostics  # noqa: E402

T0 = time.time()
CLEARANCE = 4e-11


def log(*a):
    print(f"{time.strftime('%H:%M:%S')} [{time.time() - T0:6.0f}s]", *a, flush=True)


def certify(n: int, Q: np.ndarray) -> tuple[float | None, str]:
    rows = [
        {
            "n": str(n),
            "square_id": str(i),
            "x": repr(float(x)),
            "y": repr(float(y)),
            "angle": repr(float(t)),
        }
        for i, (x, y, t) in enumerate(Q)
    ]
    _, _, detail, why = metric.evaluate_single_puzzle(n, rows)
    if why != "ok" or detail is None:
        return None, why
    return float(detail), "ok"


def make_feasible(P: np.ndarray, max_factor: float = 1.002) -> np.ndarray | None:
    out, _ = repair_with_diagnostics(P, clearance=CLEARANCE, max_factor=max_factor)
    return out


def worst_pair(P: np.ndarray) -> float:
    _, sep = S.separations(P)
    return float(sep.min()) if len(sep) else math.inf


def select_targets(Ls: dict[int, float], ref_L: dict[int, float], exclude: set[int],
                   limit: int) -> list[tuple[int, float]]:
    rows = []
    for n, L in Ls.items():
        if n in exclude or n not in ref_L:
            continue
        sg = (L - ref_L[n]) / math.sqrt(n)
        if 1e-4 <= sg <= 6e-4:
            rows.append((n, sg))
    special = {147, 156, 199}
    prio = {n: (0 if n in special else 1 if 200 <= n <= 600 else 2) for n, _ in rows}
    rows.sort(key=lambda t: (prio[t[0]], -t[1]))
    return rows[:limit]


# ---------------------------------------------------------------- insertion
def gap_candidates(P: np.ndarray, angle_deg: float, cells: int = 44) -> np.ndarray:
    """Centres of the largest empty places for one unit square at ``angle_deg``."""
    L = S.side_length(P)
    h = 0.5 * (abs(math.cos(math.radians(angle_deg)))
               + abs(math.sin(math.radians(angle_deg))))
    grid = np.linspace(h, L - h, cells)
    gx, gy = np.meshgrid(grid, grid, indexing="xy")
    cand = np.column_stack([gx.ravel(), gy.ravel(),
                            np.full(gx.size, math.radians(angle_deg))])
    # keep candidates strictly inside the incumbent box
    cand = cand[(cand[:, 0] >= h) & (cand[:, 0] <= L - h)
                & (cand[:, 1] >= h) & (cand[:, 1] <= L - h)]
    if not len(cand):
        return cand
    m = len(cand)
    Rp = S.normalize(P)
    tree = cKDTree(Rp[:, :2])
    # cheap prefilter: nearest existing centre distance, keep the roomiest half
    d, _ = tree.query(cand[:, :2], k=1)
    keep = np.argsort(-d)[: max(64, m // 6)]
    cand = cand[keep]
    # exact SAT against the real neighbours for the survivors
    combo = np.vstack([Rp, cand])
    tree2 = cKDTree(combo[:, :2])
    pairs = tree2.query_pairs(math.sqrt(2) + 1e-9, output_type="ndarray")
    sel = (pairs[:, 0] >= len(Rp)) | (pairs[:, 1] >= len(Rp))
    pairs = pairs[sel]
    if not len(pairs):
        return cand
    pairs2, sep = S.separations(combo, pairs)
    idx_new = np.where(pairs2[:, 0] >= len(Rp), pairs2[:, 0] - len(Rp),
                       pairs2[:, 1] - len(Rp))
    score = np.full(len(cand), np.inf)
    np.minimum.at(score, idx_new, sep)
    order = np.argsort(-score)
    return cand[order], score[order]


def insert_square(P: np.ndarray, angle_deg: float,
                  min_gap: float = -0.01) -> tuple[np.ndarray | None, float, float | None]:
    """Append one square in the roomiest place of the incumbent box.

    Returns ``(Q, box_extra, gap)``; ``Q`` is None when no candidate clears
    ``min_gap`` (deeper starts cannot be repaired by polish) and the third
    entry is then still the best gap found, for diagnostics.
    """
    got = gap_candidates(P, angle_deg)
    if got is None:
        return None, 0.0, None
    cands, scores = got
    if not len(cands):
        return None, 0.0, None
    best_gap = float(scores[0])
    if best_gap < min_gap:
        return None, 0.0, best_gap
    L = S.side_length(P)
    Q = S.normalize(np.vstack([P, cands[0]]))
    return Q, float(S.side_length(Q) - L), best_gap


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--base-report", required=True)
    ap.add_argument("--ref", default="data/references/leaderboards/perpuzzle_best_20261029.csv")
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=45)
    ap.add_argument("--time-budget", type=float, default=900.0)
    ap.add_argument("--polish-seconds", type=float, default=4.0)
    ap.add_argument("--rounds", type=int, default=36)
    ap.add_argument("--second-rounds", type=int, default=90)
    ap.add_argument("--second-seconds", type=float, default=10.0)
    ap.add_argument("--max-delete", type=int, default=1)
    ap.add_argument("--exclude", default="971,911,910,791,972,908,634,687,328,642")
    ap.add_argument("--only", default="", help="comma list of n, overrides selection")
    ap.add_argument("--skip-delete", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    df = pd.read_csv(args.base)
    raw = {
        int(n): g.sort_values("square_id")[["x", "y", "angle"]].to_numpy(float)
        for n, g in df.groupby("n")
    }
    Ls = {n: S.side_length(P) for n, P in raw.items()}
    with open(args.base_report) as fh:
        rep = json.load(fh)
    off = {int(r["n"]): float(r["L"]) for r in rep["runs"]["text"]["per_puzzle"] if r["L"]}
    ref = pd.read_csv(args.ref)
    refL = dict(zip(ref.n.astype(int), ref.L.astype(float)))

    if args.only:
        targets = [(int(v), (Ls[int(v)] - refL[int(v)]) / math.sqrt(int(v)))
                   for v in args.only.split(",") if v]
    else:
        exclude = {int(v) for v in args.exclude.split(",") if v}
        targets = select_targets(Ls, refL, exclude, args.limit)
    log(f"{len(targets)} targets: {[n for n, _ in targets]}")

    report: dict = {"base": args.base, "settings": vars(args), "targets": {},
                    "moves": 0, "polish_calls": 0, "certified": 0,
                    "status_counts": {}}
    improved: dict[int, np.ndarray] = {}
    started = time.time()

    for ti, (n, sg) in enumerate(targets):
        if time.time() - started > args.time_budget:
            log(f"time budget reached after {ti} targets")
            break
        P = raw[n].copy()
        L0, L0off = Ls[n], off[n]
        entry: dict = {"n": n, "L": L0, "L_official": L0off, "score_gap": sg,
                       "moves": [], "structure": {}}
        tilt = S.tilt(P)
        band_tilt = float(np.median(tilt[np.abs(tilt) > 5])) if np.any(np.abs(tilt) > 5) else 0.0
        entry["structure"] = {"band_tilt": band_tilt,
                              "upright": int((np.abs(tilt) < 1e-9).sum())}
        best: tuple[float, np.ndarray] | None = None
        winners: list[tuple[str, np.ndarray]] = []

        def run(tag: str, Q0: np.ndarray | None, seed: int, rounds: int, seconds: float,
                max_factor: float = 1.002) -> None:
            nonlocal best
            row: dict = {"move": tag}
            report["moves"] += 1
            if Q0 is None:
                row["status"] = "move_failed"
                report["status_counts"]["move_failed"] = report["status_counts"].get("move_failed", 0) + 1
                entry["moves"].append(row)
                return
            w = worst_pair(Q0)
            row["start_worst"] = round(w, 9)
            row["start_L"] = S.side_length(Q0)
            report["polish_calls"] += 1
            Q1, trace, sec = polish(Q0, rounds=rounds, seed=seed, max_seconds=seconds)
            Q2 = make_feasible(Q1, max_factor=max_factor)
            report["certified"] += 1
            cert, why = (None, "repair_failed") if Q2 is None else certify(n, Q2)
            row.update({"L": S.side_length(Q1), "certified": cert is not None,
                        "why": why, "steps": len(trace), "secs": round(sec, 2)})
            key = "ok" if cert is not None else why.split(":")[0]
            report["status_counts"][key] = report["status_counts"].get(key, 0) + 1
            if cert is not None and cert < L0off - 1e-10:
                row["accepted"] = True
                winners.append((tag, Q2))
                if best is None or cert < best[0]:
                    best = (cert, Q2)
            entry["moves"].append(row)
            log(f"n={n} {tag}: L={S.side_length(Q1):.9f} cert={cert is not None}"
                f" {'' if cert is not None else why}")

        # --- I: insert into the n-1 layout ---------------------------------
        if n - 1 in raw:
            Pprev = raw[n - 1]
            for ang in (0.0, band_tilt):
                ins = insert_square(Pprev, ang)
                Q, extra, gap = ins
                if Q is None:
                    entry["moves"].append({"move": f"I_ins{ang:+.1f}",
                                           "status": "no_gap", "best_gap": gap})
                    report["status_counts"]["no_gap"] = (
                        report["status_counts"].get("no_gap", 0) + 1)
                    log(f"n={n} I_ins{ang:+.1f}: no gap (best {gap})")
                    continue
                run(f"I_ins{ang:+.1f}", Q, int(abs(ang)) % 7, args.rounds,
                    args.polish_seconds)
                entry["moves"][-1].update({"box_extra": extra, "gap": gap})

        # --- D: delete a boundary square from the n+1 layout ----------------
        if not args.skip_delete and n + 1 in raw and args.max_delete > 0:
            Pn = raw[n + 1]
            cands: list[tuple[float, int]] = []
            for idx in (int(np.argmax(Pn[:, 0])), int(np.argmax(Pn[:, 1])),
                        int(np.argmin(Pn[:, 0])), int(np.argmin(Pn[:, 1]))):
                if idx not in [c[1] for c in cands]:
                    cands.append((Ls[n + 1], idx))
            for _, idx in cands[: args.max_delete]:
                Qd = S.normalize(np.delete(Pn, idx, axis=0))
                run(f"D_del{idx}", Qd, idx, args.rounds, args.polish_seconds)

        # --- R: deep second round on the winning move -----------------------
        if winners:
            tag0, Q0 = winners[0]
            for seed in (1, 2):
                run(f"R_deep{seed}_{tag0}", Q0, seed, args.second_rounds,
                    args.second_seconds)

        if best is not None:
            cert, Qb = best
            gained = L0off - cert
            improved[n] = Qb
            entry.update({"status": "accepted", "new_L": cert, "gain_L": gained,
                          "gain_score": gained / math.sqrt(n)})
            log(f"n={n}: ACCEPT {cert:.9f} vs {L0off:.9f} L-gain {gained:.3e} "
                f"score-gain {gained / math.sqrt(n):.3e}")
        else:
            entry["status"] = "no improvement"
        report["targets"][str(n)] = entry

    lines = ["id,n,square_id,x,y,angle"]
    total_gain = 0.0
    for n in sorted(improved):
        Q = improved[n]
        for i, (x, y, t) in enumerate(Q):
            lines.append(f"{len(lines) - 1},{n},{i},{repr(float(x))},{repr(float(y))},"
                         f"{repr(float(t))}")
        total_gain += (off[n] - S.side_length(Q)) / math.sqrt(n)
    with open(os.path.join(args.out, "improved_groups.csv"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    report["wins"] = sorted(improved)
    report["total_gain"] = total_gain
    report["elapsed"] = time.time() - T0
    with open(os.path.join(args.out, "longtail_report.json"), "w") as fh:
        json.dump(report, fh, indent=2)
    log(f"wins {sorted(improved)} total L-based score gain {total_gain:.6f}")
    log(f"moves {report['moves']} polish {report['polish_calls']} {report['status_counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
