#!/bin/bash
# Monitor the live Kaggle CPU kernels for `squares-in-squares`.
#
# Usage:
#   scripts/watch_kernels.sh                  # one snapshot
#   scripts/watch_kernels.sh --loop 300       # every 5 min, forever
#   scripts/watch_kernels.sh --loop 300 --harvest
#   scripts/watch_kernels.sh --all            # also show recent finished/error kernels
#
# `--harvest` triggers `/tmp/campaign2/cpp_harvest/harvest_cpp.sh` the first
# time a kernel reaches COMPLETE. The harvester downloads the output, converts
# improved sqpack files, runs `squares merge`, and installs only a dual-route
# 1000/1000 strict improvement. The bank is never edited directly here.
set -u

REPO="$(cd "$(dirname "$0")/.." && pwd)"
MODE="once"
INTERVAL=300
HARVEST=0
ALL=0
LOG="${KERNEL_MONITOR_LOG:-/tmp/campaign2/kernel_monitor.log}"
PROBE="$REPO/scripts/kaggle_kernel_status.py"

usage() { sed -n '2,18p' "$0"; exit 0; }

while [ $# -gt 0 ]; do
  case "$1" in
    -l|--loop) MODE="loop"; INTERVAL="${2:-300}"; shift 2 ;;
    --once) MODE="once"; shift ;;
    --harvest) HARVEST=1; shift ;;
    --all) ALL=1; shift ;;
    --log) LOG="${2:-}"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "unknown option: $1" >&2; usage ;;
  esac
done

mkdir -p "$(dirname "$LOG")" /tmp/campaign2
if [ ! -f "$PROBE" ]; then
  echo "ERROR: missing $PROBE" >&2
  exit 1
fi

ARGS=()
[ "$HARVEST" = "1" ] && ARGS+=(--harvest)
[ "$ALL" = "1" ] && ARGS+=(--all)

snapshot() {
  {
    "$REPO/.venv/bin/python" "$PROBE" "${ARGS[@]}"
  } 2>&1 | tee -a "$LOG"
}

if [ "$MODE" = "loop" ]; then
  trap 'echo "[watch-kernels] stopped"; exit 0' INT TERM
  while true; do
    snapshot
    sleep "$INTERVAL"
  done
else
  snapshot
fi
