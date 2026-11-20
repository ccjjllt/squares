#!/usr/bin/env python3
"""Characterize construction families of priority puzzles from the merged candidate.

Prints angle structure (mod 90 degrees), tilted/axial counts and bounding box so
the cross-puzzle band generator can target the right donor structures.
"""
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/zhaohuaxiang/ccjjllt/squares")
MERGED = ROOT / "outputs/research_20261120/merged_submit/submission.csv"
TARGETS = [730, 678, 328, 365, 234, 491, 803, 969, 785, 842, 901, 962]


def main():
    df = pd.read_csv(MERGED, usecols=["n", "square_id", "x", "y", "angle"],
                     float_precision="round_trip")
    for n in TARGETS:
        g = df[df.n == n].sort_values("square_id")
        x = g.x.to_numpy(float)
        y = g.y.to_numpy(float)
        t = g.angle.to_numpy(float)
        deg = np.degrees(t) % 90.0
        tilted = int(((deg > 5) & (deg < 85)).sum())
        axial = int(((deg <= 5) | (deg >= 85)).sum())
        c, s = np.cos(t) * 0.5, np.sin(t) * 0.5
        X = np.concatenate([x + c - s, x - c - s, x - c + s, x + c + s])
        Y = np.concatenate([y + s + c, y - s + c, y - s - c, y + s - c])
        L = max(X.max() - X.min(), Y.max() - Y.min())
        hist, edges = np.histogram(deg, bins=[0, 5, 15, 30, 45, 60, 75, 85, 90])
        hstr = " ".join(f"{int(edges[i])}-{int(edges[i+1])}:{hist[i]}" for i in range(len(hist)))
        tilt_angles = np.unique(np.round(deg[(deg > 5) & (deg < 85)], 2))
        top_angles = sorted(tilt_angles.tolist())[:8]
        print(f"n={n:4d} L={L:.6f} frac={L-math.isqrt(n):.6f} tilted={tilted:4d} axial={axial:4d}")
        print(f"      hist {hstr}")
        print(f"      tilt angles sample {top_angles}")


if __name__ == "__main__":
    main()