#!/usr/bin/env python3
"""Prepare starts.csv + targets.csv for the zhuating Kaggle CPU hop campaign.

Selects the largest per-puzzle gaps of the certified merged candidate against the
2026-11-19 per-puzzle record snapshot, force-includes the six strategic puzzles,
and tiers variant/minute budgets to fit a ~9 h 4-vCPU session.
"""
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/zhaohuaxiang/ccjjllt/squares")
MERGED = ROOT / "outputs/research_20261120/merged_submit/submission.csv"
REC = ROOT / "data/references/leaderboards/perpuzzle_best_20261119.csv"
OUT = Path("/tmp/sis_campaign_20261120/starts_ds")
PRIORITY = [730, 678, 234, 491, 803, 969]


def side(g):
    x = g.x.to_numpy(float)
    y = g.y.to_numpy(float)
    t = g.angle.to_numpy(float)
    c, s = np.cos(t) * 0.5, np.sin(t) * 0.5
    X = np.concatenate([x + c - s, x - c - s, x - c + s, x + c + s])
    Y = np.concatenate([y + s + c, y - s + c, y - s - c, y + s - c])
    return float(max(X.max() - X.min(), Y.max() - Y.min()))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(MERGED, usecols=["n", "square_id", "x", "y", "angle"],
                     float_precision="round_trip")
    rec = pd.read_csv(REC).set_index("n")["L"]
    rows = []
    for n, g in df.groupby("n"):
        n = int(n)
        L = side(g.sort_values("square_id"))
        rL = float(rec.get(n, L))
        rows.append((n, L, rL, (L - rL) / math.sqrt(n)))
    tab = pd.DataFrame(rows, columns=["n", "L", "record_L", "gap_score"])
    tab = tab[tab.gap_score > 1e-9].sort_values("gap_score", ascending=False).reset_index(drop=True)
    top = tab.head(100)
    extra = tab[tab.n.isin(PRIORITY) & ~tab.n.isin(top.n)]
    sel = (pd.concat([top, extra]).drop_duplicates("n")
           .sort_values("gap_score", ascending=False).reset_index(drop=True))
    sel["rank"] = range(len(sel))

    def tier(r):
        if r < 25:
            return 3, 12
        if r < 65:
            return 2, 10
        return 1, 10

    sel["variants"], sel["minutes"] = zip(*sel["rank"].map(tier))
    starts = df[df.n.isin(sel.n)].sort_values(["n", "square_id"]).reset_index(drop=True)
    starts.insert(0, "id", range(len(starts)))
    starts.to_csv(OUT / "starts.csv", index=False)
    sel[["n", "L", "record_L", "gap_score", "variants", "minutes", "rank"]].to_csv(
        OUT / "targets.csv", index=False)
    pm = int((sel.variants * sel.minutes).sum())
    print(f"targets={len(sel)} process_minutes={pm} wall_h={pm / 4 / 60:.2f} "
          f"gap_mass={sel.gap_score.sum():.6f}")
    print("priority_included:", [n for n in PRIORITY if n in set(sel.n)])
    print(sel.head(15).to_string(index=False))


if __name__ == "__main__":
    main()