"""Select complete, officially evaluated puzzle groups across experiment outputs."""

from __future__ import annotations

import hashlib
import json
import math
import multiprocessing
import platform
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import mpmath
import pandas as pd

from squares._vendor import official_metric as metric
from squares.metrics import MODES, _as_csv, _evaluate, _prepare, write_report
from squares.submission import MAX_N, read_submission, summarize_submission, write_submission


def _groups(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[int(row["n"])].append(row)
    for group in groups.values():
        group.sort(key=lambda row: int(row["square_id"]))
    return dict(groups)


def _digest(rows):
    # IDs are reattached from the baseline. No float conversion or geometry
    # normalization: distinct source literals must remain distinct candidates.
    geometry = [[row[key] for key in ("x", "y", "angle")] for row in rows]
    return hashlib.sha256(json.dumps(geometry, separators=(",", ":")).encode()).hexdigest()


def _score_group(job):
    n, digest, rows = job
    text = _as_csv(rows)
    return (n, digest), {mode: _evaluate((n, _prepare(text, mode)[n])) for mode in MODES}


def _valid(result):
    try:
        return (
            result["status"] == "valid"
            and result["reason"] == "ok"
            and math.isfinite(float(result["L"]))
            and math.isfinite(float(result["score"]))
            and float(result["score"]) >= 0
        )
    except (KeyError, TypeError, ValueError, OverflowError):
        return False


def _cached_baseline_checked(path, source_hash, metric_hash):
    report = json.loads(Path(path).read_text())
    if report["input"]["sha256"] != source_hash or report["metric"]["sha256"] != metric_hash:
        raise ValueError("Baseline report is not bound to this CSV and official metric")
    if report["scope"] != {"min_n": 1, "max_n": MAX_N, "full_competition": True}:
        raise ValueError("Baseline report must cover all 1,000 puzzles")
    for name, version in (("pandas", pd.__version__), ("mpmath", mpmath.__version__)):
        if report["environment"].get(name) != version:
            raise ValueError(f"Baseline report uses different {name}; re-score without cache")
    expected_parser = "pandas C engine, float_precision=round_trip, explicit float64"
    if report.get("float64_parser") != expected_parser:
        raise ValueError("Baseline report uses a different float64 parsing route")
    by_mode = {}
    for mode in MODES:
        run = report["runs"][mode]
        entries = run["per_puzzle"]
        records = {entry["n"]: entry for entry in entries}
        if len(entries) != MAX_N or set(records) != set(range(1, MAX_N + 1)):
            raise ValueError(f"Incomplete or duplicate {mode} baseline puzzle scores")
        if not all(_valid(record) for record in records.values()):
            raise ValueError(f"The {mode} baseline contains invalid geometry")
        if not math.isclose(
            math.fsum(record["score"] for record in records.values()),
            float(run["score"]),
            rel_tol=0,
            abs_tol=1e-10,
        ):
            raise ValueError(f"Inconsistent {mode} baseline score total")
        by_mode[mode] = records
    return {n: {mode: by_mode[mode][n] for mode in MODES} for n in range(1, MAX_N + 1)}


def _cached_baseline(path, source_hash, metric_hash):
    try:
        return _cached_baseline_checked(path, source_hash, metric_hash)
    except (KeyError, TypeError, OverflowError) as exc:
        raise ValueError(
            "Baseline report must contain full, valid text and float64 scores"
        ) from exc


def merge_submissions(baseline, candidates, output_dir, *, baseline_report=None, workers=4):
    """Merge only whole valid groups, preserving coordinate text and baseline IDs.

    A supplied full official score report is reused only for the identical
    baseline CSV, pinned metric and parser environment. All new geometry is
    evaluated on both routes. No competition submission occurs here.
    """
    started = time.monotonic()
    baseline, output_dir = Path(baseline), Path(output_dir)
    paths = list(dict.fromkeys([baseline.resolve(), *(Path(p).resolve() for p in candidates)]))
    destinations = [
        output_dir / name
        for name in (
            "submission.csv",
            "submission.csv.tmp",
            "report.json",
            "per_puzzle.csv",
            "merge_report.json",
        )
    ]
    protected = set(paths)
    if baseline_report:
        protected.add(Path(baseline_report).resolve())
    if any(path.resolve() in protected for path in destinations):
        raise ValueError("Merge output must not overwrite an input CSV or score report")
    if workers < 1:
        raise ValueError("workers must be positive")
    metric_path = Path(metric.__file__)
    metric_hash = hashlib.sha256(metric_path.read_bytes()).hexdigest()
    provenance = json.loads(metric_path.with_suffix(".metadata.json").read_text())
    if metric_hash != provenance["sha256"]:
        raise RuntimeError("Vendored official metric hash differs from recorded provenance")
    baseline_rows = read_submission(baseline)
    base = _groups(baseline_rows)
    if set(base) != set(range(1, MAX_N + 1)):
        raise ValueError("Merge requires a complete baseline for n=1..1000")
    baseline_hash = hashlib.sha256(baseline.read_bytes()).hexdigest()
    base_keys = {n: (n, _digest(rows)) for n, rows in base.items()}
    variants = {base_keys[n]: {"rows": rows, "source": 0} for n, rows in base.items()}
    sources = [
        {
            "path": str(baseline.resolve()),
            "sha256": baseline_hash,
            "puzzles": MAX_N,
            "new_geometry_groups": MAX_N,
        }
    ]
    for source_index, path in enumerate(paths[1:], 1):
        rows = read_submission(path)
        groups = _groups(rows)
        added = 0
        for n, group in groups.items():
            key = (n, _digest(group))
            if key not in variants:
                # The id fields may come from an independently indexed partial
                # file. Use baseline identifiers for every alternative.
                attached = [
                    {**original, **{field: row[field] for field in ("x", "y", "angle")}}
                    for row, original in zip(group, base[n], strict=True)
                ]
                variants[key] = {"rows": attached, "source": source_index}
                added += 1
        sources.append(
            {
                "path": str(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "puzzles": len(groups),
                "new_geometry_groups": added,
            }
        )
    scores = {}
    if baseline_report:
        cached = _cached_baseline(baseline_report, baseline_hash, metric_hash)
        scores.update({base_keys[n]: result for n, result in cached.items()})
    jobs = [
        (n, digest, item["rows"])
        for (n, digest), item in variants.items()
        if (n, digest) not in scores
    ]
    if workers == 1 or len(jobs) < 2:
        for key, result in map(_score_group, jobs):
            scores[key] = result
    else:
        with ProcessPoolExecutor(
            max_workers=workers, mp_context=multiprocessing.get_context("spawn")
        ) as pool:
            for key, result in pool.map(_score_group, jobs, chunksize=1):
                scores[key] = result
    for n, key in base_keys.items():
        if not all(_valid(result) for result in scores[key].values()):
            raise ValueError(f"Baseline n={n} is invalid; repair the baseline before merging")

    chosen = dict(base_keys)
    rejected, alternatives = [], defaultdict(list)
    for key in variants:
        n, _ = key
        result = scores[key]
        if not all(_valid(record) for record in result.values()):
            rejected.append({"n": n, "source": variants[key]["source"], "scores": result})
        else:
            alternatives[n].append(key)
    for n, keys in alternatives.items():
        # Primary target is the official-style float64 path. Require neither
        # route to regress against the baseline; tie-break by text score, then
        # stable source order (baseline first).
        safe = [
            key
            for key in keys
            if all(
                scores[key][mode]["score"] <= scores[base_keys[n]][mode]["score"] for mode in MODES
            )
        ]
        chosen[n] = min(
            safe,
            key=lambda key: (
                scores[key]["float64"]["score"],
                scores[key]["text"]["score"],
                variants[key]["source"],
            ),
        )
    selections = []
    for n, key in sorted(chosen.items()):
        selections.append(
            {
                "n": n,
                "source": variants[key]["source"],
                "geometry_sha256": key[1],
                "changed": key != base_keys[n],
                "scores": scores[key],
                "gain": {
                    mode: scores[base_keys[n]][mode]["score"] - scores[key][mode]["score"]
                    for mode in MODES
                },
            }
        )
    output_rows = [row for n in sorted(chosen) for row in variants[chosen[n]]["rows"]]
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / "submission.csv"
    temporary = output_dir / "submission.csv.tmp"
    write_submission(output_rows, temporary)
    temporary.replace(output)
    output_hash = hashlib.sha256(output.read_bytes()).hexdigest()
    report = {
        "schema_version": 1,
        "input": {
            "path": str(output.resolve()),
            "sha256": output_hash,
            **summarize_submission(output_rows),
        },
        "metric": {
            "version": provenance["metadata"]["current_version_number"],
            "sha256": metric_hash,
            "source_url": provenance["source_url"],
        },
        "environment": {
            "python": platform.python_version(),
            "pandas": pd.__version__,
            "mpmath": mpmath.__version__,
        },
        "scope": {"min_n": 1, "max_n": MAX_N, "full_competition": True},
        "workers": workers,
        "float64_parser": "pandas C engine, float_precision=round_trip, explicit float64",
        "evaluation": "Selected complete groups evaluated independently; unchanged baseline may "
        "reuse the bound full report. Final serialized file should be fully scored "
        "before competition submission.",
        "runs": {
            mode: {
                "score": math.fsum(scores[chosen[n]][mode]["score"] for n in chosen),
                "valid": MAX_N,
                "invalid_submitted": 0,
                "missing": 0,
                "per_puzzle": [scores[chosen[n]][mode] for n in sorted(chosen)],
            }
            for mode in MODES
        },
        "elapsed_seconds": time.monotonic() - started,
    }
    write_report(report, output_dir)
    merge_report = {
        "schema_version": 1,
        "baseline_report": str(baseline_report) if baseline_report else None,
        "sources": sources,
        "submission_sha256": output_hash,
        "unique_geometry_groups_scored": len(jobs),
        "changed_puzzles": [item["n"] for item in selections if item["changed"]],
        "net_gain": {mode: math.fsum(item["gain"][mode] for item in selections) for mode in MODES},
        "selected": selections,
        "invalid_candidates": rejected,
        "score": {mode: report["runs"][mode]["score"] for mode in MODES},
        "competition_submitted": False,
    }
    (output_dir / "merge_report.json").write_text(json.dumps(merge_report, indent=2) + "\n")
    return {
        key: value
        for key, value in merge_report.items()
        if key not in ("selected", "invalid_candidates")
    }
