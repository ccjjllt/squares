"""Describe the submitted portfolio and compare it with dated public records.

This is a research analysis, not a validator. Certified lengths are read from
the existing official-metric report; angles are descriptive float64 statistics.
"""

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "outputs/analysis/baseline"
TABLES = RESULTS / "tables"
SUMMARIES = RESULTS / "summaries"
SOURCE = ROOT / "data/public/stretching_v2/submission.csv"
REPORT = ROOT / "outputs/submissions/public_stretching_v2/validation/report.json"
RECORDS = ROOT / "data/references/leaderboards/perpuzzle_best_20261029.csv"


def describe_angles(group):
    angles = np.remainder(np.degrees(group.angle.to_numpy()), 90.0)
    signed = np.where(angles >= 45, angles - 90, angles)
    mask = np.abs(signed) > 0.05
    # Approximate families: gaps > 0.25 degrees; merge the circular end gap.
    ordered = np.sort(angles)
    gaps = np.diff(np.r_[ordered, ordered[0] + 90.0])
    clusters = max(1, int((gaps > 0.25).sum()))
    tilted = signed[mask]
    strong_mask = np.abs(signed) > 3
    return {
        "tilted_count": int(mask.sum()),
        "tilted_fraction": float(mask.mean()),
        "strong_tilt_count_gt_3deg": int(strong_mask.sum()),
        "strong_tilt_fraction_gt_3deg": float(strong_mask.mean()),
        "angle_clusters_025deg": clusters,
        "tilted_abs_angle_median": float(np.median(np.abs(tilted))) if len(tilted) else 0.0,
        "tilted_signed_min": float(tilted.min()) if len(tilted) else 0.0,
        "tilted_signed_max": float(tilted.max()) if len(tilted) else 0.0,
    }


def records(rows):
    return json.loads(rows.to_json(orient="records", double_precision=14))


def approximate_lengths(path):
    squares = pd.read_csv(path)
    half_extent = 0.5 * (np.abs(np.cos(squares.angle)) + np.abs(np.sin(squares.angle)))
    squares["min_x"] = squares.x - half_extent
    squares["max_x"] = squares.x + half_extent
    squares["min_y"] = squares.y - half_extent
    squares["max_y"] = squares.y + half_extent
    bounds = squares.groupby("n").agg(
        min_x=("min_x", "min"), max_x=("max_x", "max"),
        min_y=("min_y", "min"), max_y=("max_y", "max"),
    )
    bounds["public_L_approx"] = np.maximum(bounds.max_x-bounds.min_x, bounds.max_y-bounds.min_y)
    return bounds[["public_L_approx"]].reset_index()


def main():
    TABLES.mkdir(parents=True, exist_ok=True)
    SUMMARIES.mkdir(parents=True, exist_ok=True)
    certified = json.loads(REPORT.read_text())
    df = pd.DataFrame(certified["runs"]["text"]["per_puzzle"])
    df["L_text"] = df.L
    df["L"] = df.L.astype(float)
    geometry = pd.read_csv(SOURCE)
    angles = pd.DataFrame(
        [{"n": n, **describe_angles(group)} for n, group in geometry.groupby("n")]
    )
    df = df.merge(angles, on="n", validate="one_to_one")
    df["K"] = np.floor(np.sqrt(df.n)).astype(int)
    df["D"] = df.n - df.K**2
    df["f"] = df.L - df.K
    df["g"] = (df.D + 4) / df.K
    df["grid_L"] = np.ceil(np.sqrt(df.n))
    df["grid_score"] = df.grid_L / np.sqrt(df.n) - 1
    df["grid_equivalent_length"] = np.abs(df.L - df.grid_L) < 1e-8
    df["improvement_over_grid"] = df.grid_score - df.score

    old = pd.read_csv(RECORDS, dtype={"L": str})
    old["record_L_text"] = old.L
    old["record_L"] = pd.to_numeric(old.L, errors="coerce")
    invalid = old[(~np.isfinite(old.record_L)) | (old.record_L <= 0)]
    old = old[np.isfinite(old.record_L) & (old.record_L > 0)]
    below_area = old[old.record_L < np.sqrt(old.n) - 1e-8]
    old = old[old.record_L >= np.sqrt(old.n) - 1e-8]
    old = old.rename(columns={"team": "record_team", "date": "record_date"})
    df = df.merge(
        old[["n", "record_L", "record_L_text", "record_team", "record_date"]],
        on="n",
        how="left",
        validate="one_to_one",
    )
    df["record_gap_L"] = df.L - df.record_L
    df["record_gap_score"] = df.record_gap_L / np.sqrt(df.n)
    df["positive_record_gap_score"] = df.record_gap_score.clip(lower=0)
    df["record_f"] = df.record_L - df.K
    # 1e-8 in score separates structural gaps from serialization-level variation.
    useful = df[df.record_gap_score > 1e-8].sort_values("record_gap_score", ascending=False)
    top_columns = [
        "n", "K", "D", "L", "score", "record_L", "record_gap_L", "record_gap_score",
        "f", "record_f", "g", "tilted_count", "tilted_fraction", "angle_clusters_025deg",
        "tilted_abs_angle_median", "record_team", "record_date",
    ]
    df.to_csv(TABLES / "baseline_per_puzzle_analysis.csv", index=False)
    useful[top_columns].to_csv(TABLES / "record_gap_candidates.csv", index=False)

    intervals = [(1, 100), (101, 324), (325, 499), (500, 749), (750, 1000)]
    buckets = []
    for lo, hi in intervals:
        part = df[df.n.between(lo, hi)]
        buckets.append({
            "n_from": lo, "n_to": hi, "count": len(part),
            "score": float(part.score.sum()),
            "score_share": float(part.score.sum()/df.score.sum()),
            "grid_equivalent_count": int(part.grid_equivalent_length.sum()),
            "positive_record_gap": float(part.positive_record_gap_score.sum()),
            "record_gap_share": float(part.positive_record_gap_score.sum()/df.positive_record_gap_score.sum()),
        })
    k_stats = df.groupby("K").agg(
        count=("n", "size"), score=("score", "sum"),
        gap=("positive_record_gap_score", "sum"),
        mean_tilted_fraction=("tilted_fraction", "mean"),
    ).reset_index()
    k_stats.to_csv(TABLES / "baseline_by_K.csv", index=False)
    phase = df[(df.n >= 325) & (df.D > 0)].copy()
    phase["g_bin"] = pd.cut(phase.g, [0,.3,.5,.7,.9,1.1,1.3,1.5,3], right=False)
    phase_stats = phase.groupby("g_bin", observed=True).agg(
        count=("n", "size"), positive_record_gap=("positive_record_gap_score", "sum")
    ).reset_index()
    phase_stats["g_bin"] = phase_stats.g_bin.astype(str)
    phase_stats.to_csv(TABLES / "baseline_by_phase_g.csv", index=False)
    summary = {
        "baseline": {"path": str(SOURCE.relative_to(ROOT)),
                     "sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                     "submitted_score": certified["runs"]["text"]["score"],
                     "row_count": len(geometry), "puzzles": len(df)},
        "record_snapshot": {
            "source": "https://www.kaggle.com/datasets/lostdecimal27/squares-in-squares-bank",
            "version": 2, "published": "2026-10-29T17:41:21.223Z",
            "retrieved": "2026-11-06", "latest_record_date_in_file": old.record_date.max(),
            "ignored_nonpositive_or_nonfinite_records": len(invalid),
            "ignored_below_area_records": len(below_area),
            "note": "Dated mirror of host per-puzzle leaderboard; record coordinates not provided here. Positive gap is a target, not a predicted algorithm gain.",
        },
        "score_by_n_band": buckets,
        "total_grid_score": float(df.grid_score.sum()),
        "score_improvement_over_grid": float(df.improvement_over_grid.sum()),
        "grid_equivalent_length_count": int(df.grid_equivalent_length.sum()),
        "perfect_square_count": int((df.D == 0).sum()),
        "all_upright_count": int((df.tilted_count == 0).sum()),
        "all_upright_with_better_record": records(df[(df.tilted_count == 0) & (df.record_gap_score > 1e-8)][top_columns]),
        "grid_equivalent_with_better_record": records(df[df.grid_equivalent_length & (df.record_gap_score > 1e-8)][top_columns]),
        "tilted_squares": int(df.tilted_count.sum()),
        "tilted_square_fraction": float(df.tilted_count.sum()/len(geometry)),
        "strong_tilted_squares_gt_3deg": int(df.strong_tilt_count_gt_3deg.sum()),
        "strong_tilted_square_fraction_gt_3deg": float(df.strong_tilt_count_gt_3deg.sum()/len(geometry)),
        "has_multiple_orientation_clusters_count": int((df.angle_clusters_025deg > 2).sum()),
        "positive_record_gap_total": float(df.positive_record_gap_score.sum()),
        "positive_record_gap_count_gt_1e_minus8": len(useful),
        "baseline_beats_old_record_count_gt_1e_minus8": int((df.record_gap_score < -1e-8).sum()),
        "top10_record_gap_sum": float(useful.head(10).record_gap_score.sum()),
        "top20_record_gap_sum": float(useful.head(20).record_gap_score.sum()),
        "top50_record_gap_sum": float(useful.head(50).record_gap_score.sum()),
        "top20_record_gap": records(useful.head(20)[top_columns]),
        "top20_score_contributors": records(df.sort_values("score",ascending=False).head(20)[top_columns]),
        "score_n_le_324": float(df[df.n <=324].score.sum()),
        "score_n_ge_325": float(df[df.n >=325].score.sum()),
        "record_gap_n_le_324": float(df[df.n <=324].positive_record_gap_score.sum()),
        "record_gap_n_ge_325": float(df[df.n >=325].positive_record_gap_score.sum()),
        "record_gap_K_ge_20": float(df[df.K >=20].positive_record_gap_score.sum()),
        "gap_by_K_top10": records(k_stats.sort_values("gap",ascending=False).head(10)),
        "gap_by_phase_g_for_n_ge_325": records(phase_stats),
    }
    newest = ROOT / "data/public/atlas_v79/submission.csv"
    if newest.exists():
        comparison = df.merge(approximate_lengths(newest),on="n",validate="one_to_one")
        comparison["public_score_approx"] = comparison.public_L_approx / np.sqrt(comparison.n)-1
        comparison["public_improvement_approx"] = comparison.score-comparison.public_score_approx
        comparison["public_record_gap_approx"] = (comparison.public_L_approx-comparison.record_L)/np.sqrt(comparison.n)
        comparison["best_of_length_approx"] = np.minimum(comparison.L,comparison.public_L_approx)
        comparison["offset_D_minus_K"] = comparison.D-comparison.K
        comparison.to_csv(TABLES / "atlas_v79_vs_submitted.csv",index=False)
        new_candidates = comparison[comparison.public_record_gap_approx > 1e-8].sort_values("public_record_gap_approx",ascending=False)
        cols = ["n","K","D","g","public_L_approx","record_L","public_record_gap_approx","record_team","record_date"]
        new_candidates[cols].to_csv(TABLES / "post_atlas_record_gap_candidates.csv",index=False)
        summary["new_public_comparison"] = {
            "source": "https://www.kaggle.com/code/malyshevdanil/squares-in-squares-living-atlas-of-tight-packings",
            "version": 79, "path": str(newest.relative_to(ROOT)),
            "sha256": hashlib.sha256(newest.read_bytes()).hexdigest(),
            "note": "Lengths computed with float64 corner extents, not a collision/official-score evaluation. Parent agent performs official scoring separately.",
            "approx_total_score": float(comparison.public_score_approx.sum()),
            "approx_improvement": float(comparison.public_improvement_approx.sum()),
            "materially_improved_count_score_gt_1e_minus8": int((comparison.public_improvement_approx > 1e-8).sum()),
            "materially_worse_count_score_gt_1e_minus8": int((comparison.public_improvement_approx < -1e-8).sum()),
            "top20_improvements": records(comparison.sort_values("public_improvement_approx",ascending=False).head(20)[["n","L","public_L_approx","public_improvement_approx"]]),
            "best_of_both_approx_score": float((comparison.best_of_length_approx / np.sqrt(comparison.n)-1).sum()),
            "record_positive_gap_after_new_public": float(comparison.public_record_gap_approx.clip(lower=0).sum()),
            "top20_post_public_record_gap": records(new_candidates.head(20)[cols]),
        }
        family = comparison[(comparison.K>=18) & comparison.offset_D_minus_K.between(-10,-7)]
        family[cols+["offset_D_minus_K"]].to_csv(TABLES / "family_K_squared_plus_K_minus_7_to_10.csv",index=False)
        small_D = comparison[(comparison.K>=22) & comparison.D.between(7,11)]
        small_D[cols].to_csv(TABLES / "family_K_squared_plus_7_to_11.csv",index=False)
        summary["post_public_families"] = {
            "K_squared_plus_K_minus_7_to_10": {
                "K_range": [18,31], "count": len(family),
                "positive_record_gap": float(family.public_record_gap_approx.clip(lower=0).sum()),
                "per_offset": records(family.groupby("offset_D_minus_K").agg(count=("n","size"),gap=("public_record_gap_approx","sum")).reset_index()),
                "main_example_n": [498,544,592],
                "main_example_record_f": records(comparison[comparison.n.isin([498,544,592])][["n","K","D","record_f","public_record_gap_approx"]]),
            },
            "K_squared_plus_7_to_11": {
                "K_range": [22,31], "count": len(small_D),
                "positive_record_gap": float(small_D.public_record_gap_approx.clip(lower=0).sum()),
                "main_example_n": [971,972,911,791,910,908,793,634,848],
            },
            "note": "Families are research prioritization groups, not proven layout transfer rules. The two selected groups are disjoint.",
        }
    (SUMMARIES / "baseline_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({k:v for k,v in summary.items() if k not in ["top20_record_gap","top20_score_contributors","all_upright_with_better_record","grid_equivalent_with_better_record"]},indent=2))
    print(useful[top_columns].head(20).to_string(index=False))


if __name__ == "__main__":
    main()
