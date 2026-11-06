import csv
import math

import pytest

from squares.submission import (
    COLUMNS,
    generate_grid,
    read_submission,
    summarize_submission,
    write_submission,
)


def test_decimal_text_round_trip_and_parent_directory(tmp_path):
    rows = generate_grid(1)
    rows[0].update(
        x="0.50000000000000000000000000000000000000000000000001",
        y="+5.0000000000000000000000000000000000000000000000001e-1",
        angle="-0.0000000000000000000000000000000000000000000000001",
    )
    destination = tmp_path / "nested" / "submission.csv"
    write_submission(rows, destination)
    assert read_submission(destination) == rows


def test_reordered_columns_are_accepted_and_preserve_row_order(tmp_path):
    rows = list(reversed(generate_grid(3)))
    source = tmp_path / "reordered.csv"
    with source.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(reversed(COLUMNS)))
        writer.writeheader()
        writer.writerows(rows)
    assert read_submission(source) == rows
    write_submission(read_submission(source), tmp_path / "written.csv")
    assert read_submission(tmp_path / "written.csv") == rows


@pytest.mark.parametrize(
    "header",
    [
        "id,n,square_id,x,y",
        "id,n,square_id,x,y,angle,extra",
        "id,n,square_id,x,x,angle",
    ],
)
def test_bad_header_is_rejected(tmp_path, header):
    source = tmp_path / "bad.csv"
    source.write_text(header + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="six unique columns"):
        read_submission(source)


@pytest.mark.parametrize("line", ["0,1,0,0.5,0.5", "0,1,0,0.5,0.5,0,extra"])
def test_missing_or_extra_row_cells_are_rejected(tmp_path, line):
    source = tmp_path / "bad.csv"
    source.write_text(",".join(COLUMNS) + "\n" + line + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Row 2"):
        read_submission(source)


@pytest.mark.parametrize(
    ("column", "value", "message"),
    [
        ("id", "-1", "id must be nonnegative"),
        ("id", "0.0", "id must be an integer"),
        ("n", "0", "n must be between"),
        ("n", "1001", "n must be between"),
        ("n", "1.0", "n must be an integer"),
        ("square_id", "1", "square_id must be between"),
        ("x", "NaN", "decimal literal"),
        ("y", "inf", "decimal literal"),
        ("x", "sqrt(2)", "decimal literal"),
        ("x", "1e400", "must be finite"),
        ("x", "1" * 101, "at most 100 characters"),
        ("x", "10000.00000000000000000000000000001", r"abs\(x\)"),
        ("y", "-10001", r"abs\(y\)"),
        ("angle", "100.00001", r"abs\(angle\)"),
    ],
)
def test_invalid_fields_fail_before_writing(tmp_path, column, value, message):
    rows = generate_grid(1)
    rows[0][column] = value
    target = tmp_path / "submission.csv"
    with pytest.raises(ValueError, match=message):
        write_submission(rows, target)
    assert not target.exists()


def test_duplicate_numeric_ids_are_rejected(tmp_path):
    rows = generate_grid(2)
    rows[1]["id"] = "00"
    with pytest.raises(ValueError, match="duplicate id 0"):
        write_submission(rows, tmp_path / "bad.csv")


def test_missing_square_is_rejected(tmp_path):
    rows = generate_grid(3)[:-1]
    with pytest.raises(ValueError, match="n=3: expected 3 rows, got 2"):
        write_submission(rows, tmp_path / "bad.csv")


def test_duplicate_square_is_rejected(tmp_path):
    rows = generate_grid(2)
    rows[-1]["square_id"] = "0"
    with pytest.raises(ValueError, match="duplicate square_id 0 for n=2"):
        write_submission(rows, tmp_path / "bad.csv")


def test_whole_puzzle_partial_submission_is_valid(tmp_path):
    rows = [row for row in generate_grid(5) if row["n"] == "5"]
    write_submission(rows, tmp_path / "partial.csv")
    assert summarize_submission(rows) == {
        "rows": 5,
        "puzzles": 1,
        "min_n": 5,
        "max_n": 5,
        "missing_puzzles": 999,
    }


def test_header_only_submission_means_all_puzzles_missing(tmp_path):
    write_submission([], tmp_path / "empty.csv")
    rows = read_submission(tmp_path / "empty.csv")
    assert summarize_submission(rows) == {
        "rows": 0,
        "puzzles": 0,
        "min_n": None,
        "max_n": None,
        "missing_puzzles": 1000,
    }


def test_grid_has_complete_unit_spaced_packings():
    rows = generate_grid(25)
    assert len(rows) == 25 * 26 // 2
    assert [int(row["id"]) for row in rows] == list(range(len(rows)))
    for n in range(1, 26):
        group = [row for row in rows if int(row["n"]) == n]
        points = {(float(row["x"]), float(row["y"])) for row in group}
        assert len(points) == n
        assert {int(row["square_id"]) for row in group} == set(range(n))
        assert all(row["angle"] == "0" for row in group)
        side = max(max(x for x, _ in points), max(y for _, y in points)) + 0.5
        assert side == math.ceil(math.sqrt(n))
        # Distinct lattice centers guarantee separation along at least one axis.
        assert all(x % 1 == 0.5 and y % 1 == 0.5 for x, y in points)


@pytest.mark.parametrize("max_n", [0, 1001, -1, 1.5, True])
def test_invalid_grid_range(max_n):
    with pytest.raises(ValueError, match="max_n"):
        generate_grid(max_n)
