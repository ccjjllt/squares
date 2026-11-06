"""Regression checks for geometry, precision routes and official metric parity."""

import csv
import hashlib
import json
import math
from pathlib import Path

import pandas as pd
import pytest

from squares._vendor import official_metric as metric
from squares.metrics import score_submission, write_report
from squares.submission import generate_grid, write_submission


def _write(tmp_path: Path, rows: list[dict[str, str]]) -> Path:
    path = tmp_path / "submission.csv"
    write_submission(rows, path)
    return path


def _puzzle(run: dict, n: int) -> dict:
    return next(result for result in run["per_puzzle"] if result["n"] == n)


def test_small_grid_matches_formula_in_both_precision_routes(tmp_path):
    path = _write(tmp_path, generate_grid(5))
    report = score_submission(path, max_n=5)
    expected = sum(math.ceil(math.sqrt(n)) / math.sqrt(n) - 1 for n in range(1, 6))

    assert report["scope"] == {"min_n": 1, "max_n": 5, "full_competition": False}
    for run in report["runs"].values():
        assert run["score"] == pytest.approx(expected)
        assert (run["valid"], run["invalid_submitted"], run["missing"]) == (5, 0, 0)
        assert [row["n"] for row in run["per_puzzle"]] == list(range(1, 6))
        assert float(_puzzle(run, 4)["L"]) == 2.0
        assert _puzzle(run, 4)["score"] == 0.0


def test_partial_submission_charges_missing_puzzles(tmp_path):
    path = _write(tmp_path, generate_grid(1))
    report = score_submission(path, max_n=4)

    for run in report["runs"].values():
        assert (run["valid"], run["invalid_submitted"], run["missing"]) == (1, 0, 3)
        assert run["score"] == pytest.approx(sum(metric.infeasible_score(n) for n in (2, 3, 4)))
        assert _puzzle(run, 1)["status"] == "valid"
        for n in (2, 3, 4):
            result = _puzzle(run, n)
            assert result["status"] == "missing"
            assert result["L"] is None
            assert result["score"] == metric.infeasible_score(n)


def test_overlapping_perfect_square_is_invalid_despite_zero_penalty(tmp_path):
    rows = [row for row in generate_grid(4) if row["n"] == "4"]
    for row in rows:
        row.update(x="0.5", y="0.5")
    path = _write(tmp_path, rows)
    report = score_submission(path, max_n=4)

    for run in report["runs"].values():
        result = _puzzle(run, 4)
        assert (run["valid"], run["invalid_submitted"], run["missing"]) == (0, 1, 3)
        assert result["status"] == "invalid"
        assert result["score"] == 0.0
        assert result["L"] is None
        assert "overlap" in result["reason"].lower()


def test_float64_round_trip_can_change_validity_without_changing_score(tmp_path):
    rows = [row for row in generate_grid(2) if row["n"] == "2"]
    rows[1]["x"] = "1.4999999999999999999"
    path = _write(tmp_path, rows)
    report = score_submission(path, max_n=2)
    original = _puzzle(report["runs"]["text"], 2)
    rounded = _puzzle(report["runs"]["float64"], 2)

    assert original["status"] == "invalid"
    assert original["L"] is None
    assert "overlap" in original["reason"].lower()
    assert rounded["status"] == "valid"
    assert float(rounded["L"]) == 2.0
    assert original["score"] == rounded["score"]


def test_tiny_positive_gap_is_valid(tmp_path):
    rows = [row for row in generate_grid(2) if row["n"] == "2"]
    rows[1]["x"] = "1.500000000001"
    path = _write(tmp_path, rows)

    for run in score_submission(path, max_n=2)["runs"].values():
        result = _puzzle(run, 2)
        assert result["status"] == "valid"
        assert float(result["L"]) > 2.0


def test_spawn_workers_match_serial_results(tmp_path):
    path = _write(tmp_path, generate_grid(4))
    serial = score_submission(path, max_n=4, workers=1)
    parallel = score_submission(path, max_n=4, workers=2)
    assert serial["runs"] == parallel["runs"]


@pytest.mark.parametrize("mode", ["text", "float64"])
def test_wrapper_matches_official_entry_point(tmp_path, monkeypatch, mode):
    path = _write(tmp_path, generate_grid(3))
    report = score_submission(path, max_n=3, modes=(mode,))
    if mode == "text":
        submission = pd.read_csv(path, dtype=str, keep_default_na=False)
    else:
        submission = pd.read_csv(
            path,
            float_precision="round_trip",
            dtype={"id": str, "n": str, "square_id": str, "x": float, "y": float, "angle": float},
            keep_default_na=False,
        )
    solution = pd.DataFrame({"id": [0, 1, 2], "n": [1, 2, 3]})
    monkeypatch.chdir(tmp_path)
    # The official function prefers /kaggle/working when it exists. Route only
    # that directory probe away from the host, keeping all writes in tmp_path.
    original_path = Path
    monkeypatch.setattr(
        metric,
        "Path",
        lambda path: (
            original_path("absent-kaggle-working")
            if path == "/kaggle/working"
            else original_path(path)
        ),
    )

    assert metric.score(solution, submission, "id") == report["runs"][mode]["score"]
    assert (tmp_path / "submission_details.csv").is_file()


def test_vendored_metric_is_unchanged_and_hash_matches_provenance():
    vendored = Path(metric.__file__)
    original = Path(__file__).resolve().parents[1] / "research" / "official_metric.py"
    provenance = json.loads(vendored.with_suffix(".metadata.json").read_text())

    assert vendored.read_bytes() == original.read_bytes()
    assert hashlib.sha256(vendored.read_bytes()).hexdigest() == provenance["sha256"]
    assert provenance["metadata"]["current_version_number"] == 20


def test_report_files_preserve_missing_status_and_both_routes(tmp_path):
    path = _write(tmp_path, generate_grid(1))
    report = score_submission(path, max_n=3)
    output_dir = tmp_path / "reports" / "partial"
    write_report(report, output_dir)

    assert json.loads((output_dir / "report.json").read_text()) == report
    with (output_dir / "per_puzzle.csv").open(newline="") as stream:
        records = list(csv.DictReader(stream))
    assert len(records) == 6
    assert {row["mode"] for row in records} == {"text", "float64"}
    assert all(row["status"] == "missing" and row["L"] == "" for row in records if row["n"] != "1")
