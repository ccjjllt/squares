#!/usr/bin/env python3
"""Remote status probe for the Colab T4 GA session.

Printed by `colab exec -s <session> -f scripts/colab_status_remote.py`.
Read-only: never starts, stops, or modifies the run.
"""
import glob
import os
import subprocess
import time

ROOT = os.environ.get("COLAB_ROOT", "/content/sis")


def sh(cmd):
    try:
        r = subprocess.run(["bash", "-lc", cmd], capture_output=True, text=True, timeout=30)
        return (r.stdout or "").strip()
    except Exception as exc:  # noqa: BLE001
        return "ERR " + type(exc).__name__ + ": " + str(exc)


def tail(path, n=5):
    try:
        with open(path) as fh:
            return "".join(fh.readlines()[-n:]).rstrip()
    except Exception:
        return ""


print("NOW", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
print("GPU", sh("nvidia-smi --query-gpu=name,utilization.gpu,memory.used,temperature.gpu "
                "--format=csv,noheader") or "no nvidia-smi")

procs = sh("pgrep -af '/content/sis/colab_pkg/(ga|polish|rank).py' | wc -l")
print("PROCS", procs or "0")
ga_pids = sh("pgrep -f '/content/sis/colab_pkg/ga.py' | head -1")
print("ELAPSED", sh("ps -o etime= -p %s" % ga_pids).strip() if ga_pids else "not running")

imp = os.path.join(ROOT, "work", "runs", "improvements.csv")
if os.path.exists(imp):
    lines = open(imp, errors="replace").read().splitlines()
    print("IMPROVEMENTS", max(0, len(lines) - 1))
    for line in lines[-4:]:
        print("  " + line)
else:
    print("IMPROVEMENTS 0 (file missing)")

for path in sorted(glob.glob(os.path.join(ROOT, "work", "logs", "ga_*.log")))[:4]:
    print("LOG %s" % os.path.basename(path))
    for line in tail(path, 3).splitlines():
        print("  " + (line[:360] + ("..." if len(line) > 360 else "")))

cand = os.path.join(ROOT, "candidate_colab.csv")
if os.path.exists(cand):
    print("CANDIDATE", sh("ls -lh %s | awk '{print $5, $6, $7, $8}'" % cand))
    print("CANDIDATE_ROWS", sh("wc -l < %s" % cand))
else:
    print("CANDIDATE missing")

print("STARTS", sh("ls %s/work/runs/starts/n*.npy 2>/dev/null | wc -l" % ROOT))
print("CAND_DONE", sh("ls %s/work/runs/cand_done 2>/dev/null | wc -l" % ROOT))
print("DISK", sh("df -h /content | tail -1 | awk '{print $4\" free\"}'"))
