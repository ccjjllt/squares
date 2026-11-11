#!/usr/bin/env python3
"""Public-frontier gap ranking and candidate extraction (2026-11-11).

Subcommands
-----------
gaps
    Compute exact per-n L for a complete submission with the vendored official
    v20 geometry code, join the 2026-10-29 per-puzzle record table, and write a
    ranked gap table plus a markdown report.

candidates
    Compare complete n groups from candidate submission files against a
    baseline, certify every strictly-better group with the official evaluator
    on both scoring routes, and emit a partial CSV that keeps the winning
    coordinate text verbatim (IDs are reattached from the baseline).

No competition submission is made. CPU use is capped at two worker processes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import multiprocessing
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import mpmath
import pandas as pd

from squares._vendor import official_metric as metric
from squares.metrics import _as_csv, _evaluate, _prepare
from squares.submission import COLUMNS, read_submission

MAX_WORKERS = 2


def sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def groups(rows):
    out = defaultdict(list)
    for row in rows:
        out[int(row["n"])].append(row)
    for group in out.values():
        group.sort(key=lambda row: int(row["square_id"]))
    return dict(out)


def exact_L_worker(job):
    n, rows = job
    _, side = metric._build_squares(n, rows)
    return n, metric._format_detail(side)


def exact_L_map(path: str | Path, workers: int = MAX_WORKERS) -> dict[int, str]:
    rows = groups(read_submission(path))
    work = [(n, rows[n]) for n in sorted(rows)]
    if workers <= 1:
        results = [exact_L_worker(item) for item in work]
    else:
        with ProcessPoolExecutor(
            max_workers=min(workers, len(work)),
            mp_context=multiprocessing.get_context("spawn"),
        ) as pool:
            results = list(pool.map(exact_L_worker, work, chunksize=4))
    return dict(results)


def float_L_map(path: str | Path) -> dict[int, float]:
    """Fast bounding-side screen; exact values are recomputed for finalists."""
    frame = pd.read_csv(path, dtype={"x": str, "y": str, "angle": str})
    x = frame["x"].astype(float).to_numpy()
    y = frame["y"].astype(float).to_numpy()
    angle = frame["angle"].astype(float).to_numpy()
    n = frame["n"].to_numpy()
    c, s, h = None, None, 0.5
    import numpy as np

    c = np.cos(angle)
    s = np.sin(angle)
    dx1 = h * c - h * s
    dy1 = h * s + h * c
    dx2 = -h * c - h * s
    dy2 = -h * s + h * c
    xs = np.stack([x + dx1, x + dx2, x - dx1, x - dx2])
    ys = np.stack([y + dy1, y + dy2, y - dy1, y - dy2])
    out = {}
    for key in np.unique(n):
        mask = n == key
        out[int(key)] = max(
            float(xs[:, mask].max() - xs[:, mask].min()),
            float(ys[:, mask].max() - ys[:, mask].min()),
        )
    return out


def read_record(path: str | Path):
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        return {
            int(row["n"]): row
            for row in csv.DictReader(handle)
        }


def fmt(value, digits=15) -> str:
    return f"{float(value):.{digits}f}"


def gap_rows(base_L, record):
    rows = []
    for n in range(1, 1001):
        rec = record[n]
        L_ours = mpmath.mpf(base_L[n])
        L_rec = mpmath.mpf(rec["L"])
        K = math.isqrt(n)
        D = n - K * K
        score_ours = max(mpmath.mpf(0), L_ours / mpmath.sqrt(n) - 1)
        score_rec = max(mpmath.mpf(0), L_rec / mpmath.sqrt(n) - 1)
        gap = score_ours - score_rec
        rows.append(
            {
                "n": n,
                "K": K,
                "D": D,
                "L_ours": base_L[n],
                "L_record": rec["L"],
                "f_ours": mpmath.nstr(L_ours - K, 25),
                "f_best": mpmath.nstr(L_rec - K, 25),
                "score_ours": float(score_ours),
                "score_record": float(score_rec),
                "gap": float(gap),
                "team": rec["team"],
                "date": rec["date"],
            }
        )
    rows.sort(key=lambda row: (-row["gap"], row["n"]))
    return rows


def write_gap_csv(rows, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = (
        "rank", "n", "K", "D", "L_ours", "L_record", "f_ours", "f_best",
        "score_ours", "score_record", "gap", "team", "date",
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for rank, row in enumerate(rows, start=1):
            out = {"rank": rank, **row}
            out["f_ours"] = fmt(row["f_ours"], 15)
            out["f_best"] = fmt(row["f_best"], 15)
            out["score_ours"] = fmt(row["score_ours"], 15)
            out["score_record"] = fmt(row["score_record"], 15)
            out["gap"] = fmt(row["gap"], 15)
            writer.writerow(out)


def write_subset_csv(rows, path: Path, limit: int | None = None) -> None:
    fields = (
        "rank", "n", "K", "D", "L_ours", "L_record", "f_ours", "f_best",
        "score_ours", "score_record", "gap", "team", "date",
    )
    selected = rows if limit is None else rows[:limit]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for rank, row in enumerate(selected, start=1):
            writer.writerow({
                "rank": rank, "n": row["n"], "K": row["K"], "D": row["D"],
                "L_ours": row["L_ours"], "L_record": row["L_record"],
                "f_ours": fmt(row["f_ours"], 15), "f_best": fmt(row["f_best"], 15),
                "score_ours": fmt(row["score_ours"], 15),
                "score_record": fmt(row["score_record"], 15),
                "gap": fmt(row["gap"], 15), "team": row["team"], "date": row["date"],
            })


def markdown_table(rows, limit=None) -> str:
    selected = rows if limit is None else rows[:limit]
    lines = [
        "| rank | n | K | D | f_ours | f_best | gap | team |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |",
    ]
    for rank, row in enumerate(selected, start=1):
        lines.append(
            f"| {rank} | {row['n']} | {row['K']} | {row['D']} | "
            f"{fmt(row['f_ours'], 9)} | {fmt(row['f_best'], 9)} | "
            f"{fmt(row['gap'], 12)} | {row['team']} |"
        )
    return "\n".join(lines)


def command_gaps(args) -> int:
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    base_L = exact_L_map(args.baseline)
    record = read_record(args.record)
    rows = gap_rows(base_L, record)
    write_gap_csv(rows, out_dir / "gap_ranking.csv")
    write_subset_csv([r for r in rows if r["gap"] > 1e-12][:30], out_dir / "gap_top30.csv")
    write_subset_csv([r for r in rows if r["n"] <= 200 and r["gap"] > 1e-12], out_dir / "gap_top_n_le_200.csv")
    write_subset_csv([r for r in rows if 201 <= r["n"] <= 600 and r["gap"] > 1e-12], out_dir / "gap_top_201_600.csv")
    write_subset_csv([r for r in rows if r["n"] >= 601 and r["gap"] > 1e-12], out_dir / "gap_top_601_1000.csv")
    (out_dir / "baseline_L_exact.csv").write_text(
        "n,L\n" + "".join(f"{n},{base_L[n]}\n" for n in range(1, 1001)),
        encoding="utf-8",
    )

    positive = [row for row in rows if row["gap"] > 1e-12]
    noise_positive = [row for row in rows if row["gap"] > 0]
    ours_better = [row for row in rows if row["gap"] < -1e-12]
    material_better = [row for row in rows if row["gap"] < -1e-6]
    total_gap = math.fsum(row["gap"] for row in positive)
    total_score = math.fsum(row["score_ours"] for row in rows)
    record_score = math.fsum(row["score_record"] for row in rows)
    regions = {
        "n<=200": [row for row in rows if row["n"] <= 200],
        "201<=n<=600": [row for row in rows if 201 <= row["n"] <= 600],
        "601<=n<=1000": [row for row in rows if row["n"] >= 601],
    }
    region_gap = {name: math.fsum(r["gap"] for r in subset if r["gap"] > 1e-12) for name, subset in regions.items()}
    region_count = {name: sum(1 for r in subset if r["gap"] > 1e-12) for name, subset in regions.items()}
    region_count_raw = {name: sum(1 for r in subset if r["gap"] > 0) for name, subset in regions.items()}

    report = [
        "# Public frontier gap ranking",
        "",
        f"- Baseline: `{args.baseline}`",
        f"- Baseline SHA-256: `{sha256(args.baseline)}`",
        f"- Record table: `{args.record}` (SHA-256 `{sha256(args.record)}`)",
        f"- Baseline official-style total score (exact mpmath sides): `{total_score:.15f}`",
        f"- Record-table total score: `{record_score:.15f}`",
        f"- Puzzles with gap > 1e-12 (real gaps): **{len(positive)} / 1000**",
        f"- Puzzles with raw gap > 0 (includes sub-1e-12 rounding noise): **{len(noise_positive)}**",
        f"- Puzzles where this file is better than the 2026-10-29 record: **{len(ours_better)}**"
        f" (material, gap < -1e-6: {', '.join(str(r['n']) for r in material_better) or 'none'})",
        f"- Total remaining gap (sum of real positive gaps): **{total_gap:.12f}**",
        f"- Net sum including puzzles we already lead: `{math.fsum(r['gap'] for r in rows):.12f}`",
        "",
        "## Gap by region",
        "",
        "| region | puzzles with gap>1e-12 | raw gap>0 | remaining gap |",
        "| :--- | ---: | ---: | ---: |",
    ]
    for name in regions:
        report.append(
            f"| {name} | {region_count[name]} | {region_count_raw[name]} | {region_gap[name]:.12f} |"
        )
    report += ["", "## Top 30 gaps", "", markdown_table(positive, 30), ""]
    for name, subset in regions.items():
        report += [f"## Top 15 gaps, {name}", "", markdown_table([r for r in subset if r["gap"] > 1e-12], 15), ""]
    report += [
        "## Notes",
        "",
        "- `f = L - floor(sqrt(n))`; `gap = (L_ours - L_record) / sqrt(n)`.",
        "- `L_ours` is measured from the submitted decimal strings with the vendored official v20",
        "  geometry at 60 dps, matching `submission_details.csv`.",
        "- The record table is the 2026-10-29 mirror from `lostdecimal27/squares-in-squares-bank`;",
        "  re-downloading that dataset on 2026-11-11 produced the identical SHA-256,",
        "  so no newer public record table exists in the dataset.",
    ]
    (out_dir / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({
        "baseline_sha256": sha256(args.baseline),
        "total_score": total_score,
        "record_score": record_score,
        "count_gap_positive": len(positive),
        "count_ours_better": len(ours_better),
        "total_remaining_gap": total_gap,
        "region_gap": region_gap,
        "region_count": region_count,
        "top5": [
            {k: row[k] for k in ("n", "K", "D", "gap", "team")}
            for row in positive[:5]
        ],
    }, indent=2))
    return 0


def certify_group(n: int, rows, base_L_text: str):
    official = metric.evaluate_single_puzzle(n, rows)
    _, score, L_text, reason = official
    if L_text is None or reason != "ok":
        return None
    payload = {
        "n": n,
        "status": "valid",
        "reason": reason,
        "score": score,
        "L": L_text,
        "L_base": base_L_text,
        "gain": float(mpmath.mpf(base_L_text) - mpmath.mpf(L_text)) / math.sqrt(n),
    }
    text = _as_csv(rows)
    for mode in ("text", "float64"):
        prepared = _prepare(text, mode)[n]
        result = _evaluate((n, prepared))
        payload[f"{mode}_score"] = result["score"]
        payload[f"{mode}_L"] = result["L"]
        payload[f"{mode}_status"] = result["status"]
    payload["both_modes_improve"] = (
        payload["text_score"] < float(mpmath.mpf(base_L_text) / mpmath.sqrt(n) - 1) - 1e-15
        and payload["float64_score"] < float(mpmath.mpf(base_L_text) / mpmath.sqrt(n) - 1) - 1e-15
    )
    return payload


def command_candidates(args) -> int:
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    base_rows = groups(read_submission(args.baseline))
    base_L_text = exact_L_map(args.baseline)
    base_L = {n: float(mpmath.mpf(text)) for n, text in base_L_text.items()}
    base_score = {n: max(0.0, base_L[n] / math.sqrt(n) - 1.0) for n in base_L}

    source_reports = []
    source_groups = {}
    winners = {}
    for path_str in args.candidate:
        path = Path(path_str)
        try:
            rows = groups(read_submission(path))
        except (ValueError, csv.Error) as exc:
            source_reports.append({
                "path": str(path.resolve()),
                "sha256": sha256(path),
                "n_groups": 0,
                "float_wins_checked": 0,
                "certified_wins": 0,
                "wins": [],
                "skipped": str(exc),
            })
            continue
        source_groups[str(path.resolve())] = rows
        raw_float = float_L_map(path)
        preliminary = []
        for n, L in raw_float.items():
            if n in base_L and (base_L[n] - L) / math.sqrt(n) > 5e-12:
                preliminary.append(n)
        checked = []
        for n in sorted(preliminary):
            base_text = base_L_text[n]
            _, cand_L_text = exact_L_worker((n, rows[n]))
            if not mpmath.mpf(cand_L_text) < mpmath.mpf(base_text):
                continue
            certified = certify_group(n, rows[n], base_text)
            if certified is None or not certified["both_modes_improve"]:
                continue
            certified["source"] = str(path.resolve())
            certified["source_sha256"] = sha256(path)
            checked.append(certified)
            current = winners.get(n)
            if current is None or mpmath.mpf(certified["L"]) < mpmath.mpf(current["L"]):
                winners[n] = certified
        source_reports.append({
            "path": str(path.resolve()),
            "sha256": sha256(path),
            "n_groups": len(rows),
            "float_wins_checked": len(preliminary),
            "certified_wins": len(checked),
            "wins": [c["n"] for c in checked],
        })

    ordered = [winners[n] for n in sorted(winners)]
    # Reattach baseline IDs; coordinate text stays exactly as submitted.
    output_rows = []
    for item in ordered:
        n = item["n"]
        base_group = base_rows[n]
        cand_group = source_groups[item["source"]][n]
        for base_row, cand_row in zip(base_group, cand_group, strict=True):
            out = dict(cand_row)
            out["id"] = base_row["id"]
            output_rows.append(out)

    candidate_path = out_dir / "candidate_public.csv"
    with candidate_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(output_rows)

    net_gain = math.fsum(item["gain"] for item in ordered)
    new_total = math.fsum(base_score.values()) - net_gain
    payload = {
        "baseline": str(Path(args.baseline).resolve()),
        "baseline_sha256": sha256(args.baseline),
        "baseline_total_score": math.fsum(base_score.values()),
        "candidate_public": str(candidate_path.resolve()),
        "candidate_sha256": sha256(candidate_path),
        "rows": len(output_rows),
        "winning_n": [item["n"] for item in ordered],
        "net_gain": net_gain,
        "projected_total_score": new_total,
        "sources": source_reports,
        "wins": ordered,
    }
    (out_dir / "candidate_report.json").write_text(json.dumps(payload, indent=2) + "\n")

    report = [
        "# Public candidate extraction, 2026-11-11",
        "",
        f"- Baseline: `{args.baseline}` (SHA-256 `{sha256(args.baseline)}`)",
        f"- Baseline total: `{math.fsum(base_score.values()):.15f}`",
        f"- Candidate file: `{candidate_path}` (SHA-256 `{sha256(candidate_path)}`)",
        f"- Winning complete n groups: **{len(ordered)}** ({', '.join(str(i['n']) for i in ordered) or 'none'})",
        f"- Net gain: **{net_gain:.12f}**",
        f"- Projected total: **{new_total:.15f}**",
        "",
        "| n | K | D | L_base | L_candidate | gain | text score | float64 score | source |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |",
    ]
    for item in ordered:
        n = item["n"]
        report.append(
            f"| {n} | {math.isqrt(n)} | {n - math.isqrt(n) ** 2} | "
            f"{item['L_base']} | {item['L']} | {item['gain']:.12f} | "
            f"{item['text_score']:.15f} | {item['float64_score']:.15f} | "
            f"{item['source']} |"
        )
    report += ["", "## Sources checked", ""]
    for source in source_reports:
        if source.get("skipped"):
            report.append(
                f"- `{source['path']}` SHA `{source['sha256']}`: skipped ({source['skipped']})"
            )
            continue
        report.append(
            f"- `{source['path']}` SHA `{source['sha256']}`: "
            f"{source['n_groups']} groups, {source['certified_wins']} certified wins"
            + (f" ({source['wins']})" if source["wins"] else "")
        )
    report += [
        "",
        "All winning groups were certified with `official_metric.evaluate_single_puzzle`",
        "and both the text and float64 round-trip routes improve on the baseline.",
    ]
    (out_dir / "candidate_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in (
        "candidate_sha256", "rows", "winning_n", "net_gain",
        "projected_total_score", "baseline_total_score",
    )}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    gaps = sub.add_parser("gaps")
    gaps.add_argument("--baseline", required=True)
    gaps.add_argument("--record", default="data/references/leaderboards/perpuzzle_best_20261029.csv")
    gaps.add_argument("--output-dir", required=True)
    gaps.set_defaults(func=command_gaps)

    cand = sub.add_parser("candidates")
    cand.add_argument("--baseline", required=True)
    cand.add_argument("--candidate", action="append", required=True)
    cand.add_argument("--output-dir", required=True)
    cand.set_defaults(func=command_candidates)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
