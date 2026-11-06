import json
import subprocess
import sys

from squares.submission import generate_grid, write_submission


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "squares", *map(str, args)],
        text=True,
        capture_output=True,
        check=False,
    )


def test_baseline_and_inspect(tmp_path):
    path = tmp_path / "grid.csv"
    generated = run_cli("baseline", "--max-n", 4, "--output", path)
    assert generated.returncode == 0, generated.stderr
    assert json.loads(generated.stdout)["geometry_evaluated"] is False
    inspected = run_cli("inspect", path)
    assert inspected.returncode == 0, inspected.stderr
    assert json.loads(inspected.stdout)["rows"] == 10


def test_score_invalid_geometry_returns_failure_and_report(tmp_path):
    path = tmp_path / "overlap.csv"
    rows = generate_grid(2)
    rows[-1]["x"] = "0.5"
    write_submission(rows, path)
    result = run_cli(
        "score", path, "--max-n", 2, "--workers", 1, "--output-dir", tmp_path / "report"
    )
    assert result.returncode == 1, result.stderr
    report = json.loads((tmp_path / "report" / "report.json").read_text())
    assert report["runs"]["text"]["invalid_submitted"] == 1


def test_structure_error_returns_clear_message(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("id,n,x\n0,1,0.5\n")
    result = run_cli("inspect", path)
    assert result.returncode == 2
    assert "six unique columns" in result.stderr
    assert "Traceback" not in result.stderr


def test_invalid_scope_is_rejected():
    result = run_cli("baseline", "--max-n", 1001)
    assert result.returncode == 2
    assert "must not exceed 1000" in result.stderr
