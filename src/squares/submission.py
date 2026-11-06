"""Read, validate and write submissions without rounding coordinate text.

These checks cover the file format and per-puzzle structure only. Geometric
feasibility must still be checked with the official metric.
"""

from __future__ import annotations

import csv
import math
import re
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from decimal import Decimal, InvalidOperation
from pathlib import Path

COLUMNS = ("id", "n", "square_id", "x", "y", "angle")
MAX_N = 1000

_COLUMN_SET = set(COLUMNS)
_INTEGER_RE = re.compile(r"[+-]?[0-9]+")
_DECIMAL_RE = re.compile(r"[+-]?(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
_MAX_LITERAL_CHARS = 100
_LIMITS = {"x": Decimal("10000"), "y": Decimal("10000"), "angle": Decimal("100")}

Row = dict[str, str]


def _validate_columns(columns: Sequence[str] | None) -> None:
    if columns is None or len(columns) != len(COLUMNS) or set(columns) != _COLUMN_SET:
        raise ValueError(
            f"CSV must contain exactly these six unique columns: {', '.join(COLUMNS)}; "
            f"got {columns!r}"
        )


def _integer(value: str, column: str, row_number: int) -> int:
    if not _INTEGER_RE.fullmatch(value.strip()):
        raise ValueError(f"Row {row_number}: {column} must be an integer, got {value!r}")
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Row {row_number}: invalid {column} integer") from exc


def _validate_decimal(value: str, column: str, row_number: int) -> None:
    literal = value.strip()
    if len(literal) > _MAX_LITERAL_CHARS or not _DECIMAL_RE.fullmatch(literal):
        raise ValueError(
            f"Row {row_number}: {column} must be a decimal literal of at most "
            f"{_MAX_LITERAL_CHARS} characters"
        )
    try:
        decimal = Decimal(literal)
        finite_double = math.isfinite(float(literal))
    except (ValueError, OverflowError, InvalidOperation) as exc:
        raise ValueError(f"Row {row_number}: invalid {column} decimal") from exc
    if not decimal.is_finite() or not finite_double:
        raise ValueError(f"Row {row_number}: {column} must be finite")
    if decimal.copy_abs() > _LIMITS[column]:
        raise ValueError(f"Row {row_number}: abs({column}) must be <= {_LIMITS[column]}")


def _validate_rows(rows: Sequence[Mapping[str, str]]) -> Counter[int]:
    seen_ids: set[int] = set()
    counts: Counter[int] = Counter()
    square_ids: dict[int, set[int]] = defaultdict(set)
    for row_number, row in enumerate(rows, start=2):
        if set(row) != _COLUMN_SET:
            raise ValueError(f"Row {row_number}: expected exactly {', '.join(COLUMNS)}")
        if any(not isinstance(value, str) for value in row.values()):
            raise ValueError(f"Row {row_number}: every field must be text (no missing cells)")
        identifier = _integer(row["id"], "id", row_number)
        if identifier < 0:
            raise ValueError(f"Row {row_number}: id must be nonnegative")
        if identifier in seen_ids:
            raise ValueError(f"Row {row_number}: duplicate id {identifier}")
        seen_ids.add(identifier)

        n = _integer(row["n"], "n", row_number)
        if not 1 <= n <= MAX_N:
            raise ValueError(f"Row {row_number}: n must be between 1 and {MAX_N}")
        square_id = _integer(row["square_id"], "square_id", row_number)
        if not 0 <= square_id < n:
            raise ValueError(f"Row {row_number}: square_id must be between 0 and {n - 1}")
        if square_id in square_ids[n]:
            raise ValueError(f"Row {row_number}: duplicate square_id {square_id} for n={n}")
        square_ids[n].add(square_id)
        counts[n] += 1
        for column in _LIMITS:
            _validate_decimal(row[column], column, row_number)

    for n, count in sorted(counts.items()):
        if count != n:
            raise ValueError(f"n={n}: expected {n} rows, got {count}")
        # Range and uniqueness above, together with the count, prove 0..n-1 coverage.
    return counts


def read_submission(path: str | Path) -> list[Row]:
    """Read a CSV and validate its schema, retaining coordinate strings verbatim.

    Partial submissions are accepted when each included puzzle is complete.
    A header-only file is also accepted: every puzzle then receives grid fallback.
    """
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        try:
            reader = csv.DictReader(handle, strict=True)
            _validate_columns(reader.fieldnames)
            rows = list(reader)
        except csv.Error as exc:
            raise ValueError(f"Invalid CSV: {exc}") from exc
    _validate_rows(rows)
    return rows


def write_submission(rows: Sequence[Mapping[str, str]], path: str | Path) -> None:
    """Write validated rows in their existing order; never convert values to floats."""
    _validate_rows(rows)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def generate_grid(max_n: int = MAX_N) -> list[Row]:
    """Create ordinary unit-spaced grid packings for puzzles 1 through max_n."""
    if type(max_n) is not int or not 1 <= max_n <= MAX_N:
        raise ValueError(f"max_n must be an integer between 1 and {MAX_N}")
    rows: list[Row] = []
    for n in range(1, max_n + 1):
        width = math.isqrt(n - 1) + 1
        for square_id in range(n):
            rows.append(
                {
                    "id": str(len(rows)),
                    "n": str(n),
                    "square_id": str(square_id),
                    "x": f"{square_id % width}.5",
                    "y": f"{square_id // width}.5",
                    "angle": "0",
                }
            )
    return rows


def summarize_submission(rows: Sequence[Mapping[str, str]]) -> dict[str, int | None]:
    """Validate rows and summarize their coverage of the 1,000 competition puzzles."""
    counts = _validate_rows(rows)
    return {
        "rows": len(rows),
        "puzzles": len(counts),
        "min_n": min(counts, default=None),
        "max_n": max(counts, default=None),
        "missing_puzzles": MAX_N - len(counts),
    }
