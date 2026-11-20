#!/usr/bin/env python3
"""Harvest a completed zhuating CPU kernel: download output, merge its hop_best.csv
into the current best bank, and run full dual-path certification.

Usage:
  .venv/bin/python scripts/harvest_merge.py <kernel-slug> <baseline.csv> <baseline-report.json> <out-dir>

Does NOT submit. Prints the merged score, changed puzzles and net gain so the
operator can decide whether to submit (only if strictly better than the board).
"""
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PY = str(REPO / ".venv/bin/python")
KAGGLE = str(REPO / ".venv/bin/kaggle")
TOKEN = Path.home() / ".kaggle/access_token_zhuating"


def env():
    e = dict(os.environ)
    e["KAGGLE_API_TOKEN"] = TOKEN.read_text().strip()
    e["HTTPS_PROXY"] = "http://127.0.0.1:7897"
    e["HTTP_PROXY"] = "http://127.0.0.1:7897"
    return e


def main():
    slug, baseline, baseline_report, outdir = sys.argv[1:5]
    outdir = Path(outdir)
    dl = outdir / "kernel_output"
    dl.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([KAGGLE, "kernels", "output", f"zhuating/{slug}", "-p", str(dl)],
                       env=env(), capture_output=True, text=True, timeout=600)
    print("download rc", r.returncode, (r.stderr or "")[-200:])
    cand = dl / "hop_best.csv"
    if not cand.exists():
        hits = list(dl.rglob("hop_best.csv"))
        if not hits:
            print("NO hop_best.csv in output; files:", [p.name for p in dl.rglob('*') if p.is_file()][:20])
            return
        cand = hits[0]
    summary = dl / "SUMMARY.json"
    if summary.exists():
        print("SUMMARY:", summary.read_text()[:600])
    merged = outdir / "merged"
    r = subprocess.run([PY, "-m", "squares", "merge", "--baseline", baseline,
                        "--baseline-report", baseline_report, "--candidate", str(cand),
                        "--output-dir", str(merged), "--workers", "2"],
                       cwd=REPO, capture_output=True, text=True, timeout=1800)
    print("merge rc", r.returncode)
    print((r.stdout or "")[-800:])
    if r.returncode != 0:
        print((r.stderr or "")[-800:])
        return
    r = subprocess.run([PY, "-m", "squares", "score", str(merged / "submission.csv"),
                        "--mode", "both", "--workers", "2",
                        "--output-dir", str(merged / "validation")],
                       cwd=REPO, capture_output=True, text=True, timeout=1800)
    print("score rc", r.returncode)
    print((r.stdout or "")[-600:])
    print("MERGED_FILE:", merged / "submission.csv")


if __name__ == "__main__":
    main()