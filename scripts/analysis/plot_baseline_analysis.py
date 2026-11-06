"""Static scientific figures for the baseline research summary."""

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".cache/matplotlib"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd

RESULTS = ROOT / "outputs/analysis/baseline"
TABLES = RESULTS / "tables"
SUMMARIES = RESULTS / "summaries"
FIGURES = RESULTS / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)
summary = json.loads((SUMMARIES / "baseline_summary.json").read_text())
bands = summary["score_by_n_band"]
x = np.arange(len(bands))
fig, ax = plt.subplots(figsize=(10, 5.6), constrained_layout=True)
for offset, key, label, color in [
    (-.18, "score_share", "Share of our total score", "#98a9bb"),
    (.18, "record_gap_share", "Share of gap to dated records", "#007d8a"),
]:
    vals = [100 * item[key] for item in bands]
    bars = ax.bar(x + offset, vals, .34, label=label, color=color)
    ax.bar_label(bars, labels=[f"{v:.1f}%" for v in vals], padding=3, fontsize=10)
ax.set_xticks(x, [f"{item['n_from']}–{item['n_to']}" for item in bands])
ax.set_xlabel("Puzzle size n")
ax.set_ylabel("Share (%)")
ax.set_ylim(0, 48)
ax.set_title("Where the score is vs. where known improvement remains", loc="left", pad=16)
ax.legend(frameon=False, loc="upper left")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=.15)
ax.set_axisbelow(True)
fig.text(.01, -.02, "Baseline: 22.2427257787. Record snapshot: 29 Oct 2026 (not the live leaderboard).", fontsize=9, color="#555555")
fig.savefig(FIGURES / "score_vs_record_gap.png", dpi=180, bbox_inches="tight")
plt.close(fig)

df = pd.read_csv(TABLES / "atlas_v79_vs_submitted.csv")
mat = np.full((32, 41), np.nan)
for row in df.itertuples():
    if row.K >= 18 and row.D <= 40:
        mat[row.K, row.D] = max(0, row.public_record_gap_approx)*1000
fig, ax = plt.subplots(figsize=(10, 5.6), constrained_layout=True)
im = ax.imshow(mat[18:32], aspect="auto", origin="lower", extent=(-.5,40.5,17.5,31.5), cmap="viridis", vmin=0)
k = np.arange(18,32)
ax.plot(k-8,k,color="#ffb347",lw=1.8,label="D = K − 8")
ax.add_patch(Rectangle((6.5,21.5),5,10,fill=False,edgecolor="white",lw=1.4,linestyle="--",label="D = 7…11, K ≥ 22"))
ax.set_xlabel("Extra squares D = n − K²")
ax.set_ylabel("K = floor(√n)")
ax.set_title("Remaining record gap after the public Atlas v79 update", loc="left",pad=14)
fig.colorbar(im,ax=ax,label="Potential score reduction × 1,000")
ax.legend(frameon=True,facecolor="white",loc="upper right")
fig.text(.01,-.02,"Float64 lengths for Atlas; targets use 29 Oct record snapshot. Blank cells are invalid (K, D) combinations for n ≤ 1,000.",fontsize=9,color="#555555")
fig.savefig(FIGURES / "record_gap_families.png",dpi=180,bbox_inches="tight")
