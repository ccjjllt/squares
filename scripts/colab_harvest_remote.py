#!/usr/bin/env python3
"""Run make_submission.py inside the Colab session (called by watch_colab.sh --harvest)."""
import subprocess

ROOT = "/content/sis"
r = subprocess.run(
    ["python", "make_submission.py"],
    cwd=ROOT,
    capture_output=True,
    text=True,
    timeout=600,
)
print("RC", r.returncode)
print(r.stdout)
if r.stderr:
    print(r.stderr[-2000:])
