"""Local diagnostics using the unchanged official v20 per-puzzle evaluator.

The float64 route is a pinned pandas simulation, not a promise about Kaggle's
backend parser. Use processes, not threads: mpmath's contexts are global.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import multiprocessing
import platform
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import mpmath
import pandas as pd

from squares._vendor import official_metric as metric
from squares.submission import COLUMNS, MAX_N, read_submission, summarize_submission

MODES = ("text", "float64")


def _evaluate(work: tuple[int, list[dict[str, str]]]) -> dict:
    n, rows = work
    # Unexpected errors intentionally propagate rather than becoming a penalty.
    n, score, length, reason = metric.evaluate_single_puzzle(n, rows)
    return {
        "n": n,
        "score": score,
        "L": length,
        "status": "valid" if length is not None else "invalid",
        "reason": reason,
    }


def _as_csv(rows: list[dict[str, str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def _prepare(text: str, mode: str) -> dict[int, list[dict[str, str]]]:
    if mode == "float64":
        frame = pd.read_csv(
            io.StringIO(text),
            engine="c",
            float_precision="round_trip",
            dtype={
                "id": str,
                "n": str,
                "square_id": str,
                "x": "float64",
                "y": "float64",
                "angle": "float64",
            },
            keep_default_na=False,
        )
        text = frame.to_csv(index=False)
    return metric._parse_submission_csv(text)


def score_submission(
    path: str | Path,
    *,
    modes: tuple[str, ...] = MODES,
    max_n: int = MAX_N,
    workers: int = 1,
) -> dict:
    """Score n=1..max_n, charging grid penalties for absent puzzles.

    Strict file validation happens before geometry evaluation. Invalid submitted
    geometry and missing puzzles are reported separately, even for zero penalties.
    """
    if not modes or len(set(modes)) != len(modes) or any(mode not in MODES for mode in modes):
        raise ValueError(f"modes must be unique values from {MODES}")
    if not 1 <= max_n <= MAX_N:
        raise ValueError(f"max_n must be between 1 and {MAX_N}")
    if workers < 1:
        raise ValueError("workers must be positive")
    if not hasattr(mpmath.mpf(1), "man"):
        raise RuntimeError("Official v20 requires mpmath 1.4.1; run uv sync --locked")

    started = time.monotonic()
    path = Path(path)
    rows = read_submission(path)
    text = _as_csv(rows)
    metric_path = Path(metric.__file__)
    provenance = json.loads(metric_path.with_suffix(".metadata.json").read_text())
    metric_hash = hashlib.sha256(metric_path.read_bytes()).hexdigest()
    if metric_hash != provenance["sha256"]:
        raise RuntimeError("Vendored metric hash does not match its recorded provenance")

    report = {
        "schema_version": 1,
        "input": {
            "path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            **summarize_submission(rows),
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
        "scope": {"min_n": 1, "max_n": max_n, "full_competition": max_n == MAX_N},
        "workers": workers,
        "float64_parser": "pandas C engine, float_precision=round_trip, explicit float64",
        "runs": {},
    }
    for mode in modes:
        puzzles = _prepare(text, mode)
        work = [(n, puzzles[n]) for n in sorted(puzzles) if n <= max_n]
        if workers == 1 or len(work) < 2:
            results = [_evaluate(item) for item in work]
        else:
            with ProcessPoolExecutor(
                max_workers=min(workers, len(work)),
                mp_context=multiprocessing.get_context("spawn"),
            ) as pool:
                results = list(pool.map(_evaluate, work, chunksize=1))
        seen = {result["n"] for result in results}
        results.extend(
            {
                "n": n,
                "score": metric.infeasible_score(n),
                "L": None,
                "status": "missing",
                "reason": "missing from submission",
            }
            for n in range(1, max_n + 1)
            if n not in seen
        )
        results.sort(key=lambda result: result["n"])
        report["runs"][mode] = {
            "score": sum(result["score"] for result in results),
            "valid": sum(result["status"] == "valid" for result in results),
            "invalid_submitted": sum(result["status"] == "invalid" for result in results),
            "missing": sum(result["status"] == "missing" for result in results),
            "per_puzzle": results,
        }
    report["elapsed_seconds"] = time.monotonic() - started
    return report


def write_report(report: dict, output_dir: str | Path) -> None:
    """Write a self-contained JSON report and a flat per-puzzle CSV."""
    output_dir = Path(output_dir)
    targets = [output_dir / "report.json", output_dir / "per_puzzle.csv"]
    if Path(report["input"]["path"]).resolve() in [p.resolve() for p in targets]:
        raise ValueError("Report output would overwrite the input submission")
    output_dir.mkdir(parents=True, exist_ok=True)
    targets[0].write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with targets[1].open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=("mode", "n", "score", "L", "status", "reason"))
        writer.writeheader()
        for mode, run in report["runs"].items():
            writer.writerows({"mode": mode, **result} for result in run["per_puzzle"])
