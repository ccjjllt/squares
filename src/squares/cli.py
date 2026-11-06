"""Command-line entry point for reproducible packing experiments."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from squares import __version__
from squares.submission import (
    MAX_N,
    generate_grid,
    read_submission,
    summarize_submission,
    write_submission,
)


def _positive(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if number < 1:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def _max_n(value: str) -> int:
    number = _positive(value)
    if number > MAX_N:
        raise argparse.ArgumentTypeError(f"must not exceed {MAX_N}")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local tools for Kaggle Squares in Squares")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    baseline = commands.add_parser("baseline", help="Generate an axis-aligned grid submission")
    baseline.add_argument("--max-n", type=_max_n, default=MAX_N)
    baseline.add_argument("--output", type=Path, default=Path("outputs/grid.csv"))
    inspect = commands.add_parser("inspect", help="Validate CSV structure (not overlap geometry)")
    inspect.add_argument("submission", type=Path)
    score = commands.add_parser("score", help="Run official v20 per-puzzle geometry evaluation")
    score.add_argument("submission", type=Path)
    score.add_argument("--mode", choices=("text", "float64", "both"), default="both")
    score.add_argument("--max-n", type=_max_n, default=MAX_N, help="Score n=1..max-n")
    score.add_argument("--workers", type=_positive, default=4)
    score.add_argument("--output-dir", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "baseline":
            rows = generate_grid(args.max_n)
            write_submission(rows, args.output)
            print(
                json.dumps(
                    {
                        "output": str(args.output),
                        **summarize_submission(rows),
                        "formula_score_on_generated_scope": sum(
                            math.ceil(math.sqrt(n)) / math.sqrt(n) - 1
                            for n in range(1, args.max_n + 1)
                        ),
                        "geometry_evaluated": False,
                    },
                    indent=2,
                )
            )
        elif args.command == "inspect":
            print(json.dumps(summarize_submission(read_submission(args.submission)), indent=2))
        else:
            from squares.metrics import score_submission, write_report

            modes = ("text", "float64") if args.mode == "both" else (args.mode,)
            print(f"Scoring n=1..{args.max_n}, modes={','.join(modes)}", file=sys.stderr)
            report = score_submission(
                args.submission, modes=modes, max_n=args.max_n, workers=args.workers
            )
            output_dir = args.output_dir or Path("outputs") / f"{args.submission.stem}-score"
            write_report(report, output_dir)
            print(
                json.dumps(
                    {
                        "scope": report["scope"],
                        "runs": {
                            mode: {key: value for key, value in run.items() if key != "per_puzzle"}
                            for mode, run in report["runs"].items()
                        },
                        "report": str(output_dir / "report.json"),
                        "elapsed_seconds": report["elapsed_seconds"],
                    },
                    indent=2,
                )
            )
            if any(run["invalid_submitted"] for run in report["runs"].values()):
                return 1
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
