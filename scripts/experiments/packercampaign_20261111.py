#!/usr/bin/env python3
"""Thin wrapper for the 2026-11-11 evand/square-packing campaign (subagent G).

The engine lives in an external clone (temp dir); this wrapper only calls it and converts its store to our
submission format, then runs our merge / score certification:

  # 1) import our merged baseline as the store's parents (once)
  python3 -c "from pk.families import migrate; migrate()"   # the events pool reads packing.family
  python3 pk.py import outputs/experiments/research_20261111/packercampaign/import_all \
      --source our:v124merged --status polished
  # 2) register + run the campaign (4 workers, 0.62 CPU-h)
  python -m pk.events add ours_takeover_20261111
  for i in 1 2 3 4; do python -m pk.events work --campaign ours_takeover_20261111 --max-idle 90 & done
  # 3) collect + certify
  uv run python scripts/experiments/packercampaign_20261111.py --stage collect
  uv run python scripts/experiments/packercampaign_20261111.py --stage verify
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EXT = Path("/private/var/folders/9s/sdk1x32s58g8dycwh6c74bqc0000gp/T/opencode/square-packing")
PK = EXT / "search" / "packer"
PY = EXT / ".venv-pk" / "bin" / "python"
OUT = REPO / "outputs/experiments/research_20261111/packercampaign"
BASE = REPO / "outputs/merged/v124_plus_daily44_public2"
NS = [971, 911, 910, 791, 972, 793, 908, 969, 862, 687, 328]


def run(cmd: list[str], **kw) -> None:
    print("$", " ".join(map(str, cmd)), flush=True)
    subprocess.run(cmd, check=True, **kw)


def collect(stage_dir: Path) -> None:
    stage_dir.mkdir(parents=True, exist_ok=True)
    run([sys.executable, str(OUT / "collect.py"), str(PK / "runs/store.sqlite"), str(BASE / "submission.csv"),
         str(stage_dir), *map(str, NS)])


def verify(stage_dir: Path) -> None:
    cand = stage_dir / "improved_groups.csv"
    merged = stage_dir / "merged"
    run(["uv", "run", "squares", "merge", "--baseline", str(BASE / "submission.csv"),
         "--baseline-report", str(BASE / "report.json"), "--candidate", str(cand),
         "--output-dir", str(merged), "--workers", "2"], cwd=REPO)
    run(["uv", "run", "squares", "score", str(merged / "submission.csv"), "--mode", "both", "--workers", "2",
         "--output-dir", str(merged / "validation")], cwd=REPO)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["collect", "verify", "all"], default="all")
    ap.add_argument("--dir", type=Path, default=OUT)
    a = ap.parse_args()
    if a.stage in ("collect", "all"):
        collect(a.dir)
    if a.stage in ("verify", "all"):
        verify(a.dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
