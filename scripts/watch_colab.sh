#!/bin/bash
# Monitor the Colab T4 GA session for `squares-in-squares`.
#
# Usage:
#   scripts/watch_colab.sh                 # one status snapshot
#   scripts/watch_colab.sh --loop 300      # snapshot every 5 min
#   scripts/watch_colab.sh --harvest       # snapshot + build/download/merge candidate
#   scripts/watch_colab.sh --loop 600 --harvest
#
# Options:
#   -s, --session NAME   Colab session name (default: sis)
#   -l, --loop SECONDS   repeat forever with this interval
#       --once           one snapshot (default)
#       --harvest        run make_submission.py in Colab, download candidate_colab.csv,
#                        then run `squares merge` locally (never installs)
#       --log PATH       append output here (default: /tmp/campaign2/colab_monitor.log)
#   -h, --help           show this help
#
# This script is read-only with respect to the live bank. It never submits to Kaggle
# and never installs a candidate; --harvest only prints the certified merge report.
set -u

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SESSION="sis"
MODE="once"
INTERVAL=300
HARVEST=0
LOG="${COLAB_MONITOR_LOG:-/tmp/campaign2/colab_monitor.log}"
REMOTE="$REPO/scripts/colab_status_remote.py"
HARVEST_REMOTE="$REPO/scripts/colab_harvest_remote.py"
CAND="/tmp/campaign2/colab_candidate.csv"
MERGE_DIR="/tmp/campaign2/colab_merge"

usage() { sed -n '2,20p' "$0"; exit 0; }

while [ $# -gt 0 ]; do
  case "$1" in
    -s|--session) SESSION="${2:-}"; shift 2 ;;
    -l|--loop) MODE="loop"; INTERVAL="${2:-300}"; shift 2 ;;
    --once) MODE="once"; shift ;;
    --harvest) HARVEST=1; shift ;;
    --log) LOG="${2:-}"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "unknown option: $1" >&2; usage ;;
  esac
done

mkdir -p "$(dirname "$LOG")" /tmp/campaign2

# colabx selects the account and routes through the local proxy.  Direct TLS to
# colab.research.google.com is reset on this Mac; 7900 fails on
# POST /tun/m/assign, 7897 works.
export PATH="$HOME/.local/bin:$PATH"
export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring
export COLAB_PROXY="${COLAB_PROXY:-http://127.0.0.1:7897}"
export COLAB_ACCOUNT="${COLAB_ACCOUNT:-ccjjllt0}"
COLAB="${COLAB:-colabx}"

if ! command -v "$COLAB" >/dev/null 2>&1; then
  echo "ERROR: $COLAB not found in PATH" >&2
  exit 1
fi
if [ ! -f "$REMOTE" ]; then
  echo "ERROR: missing $REMOTE" >&2
  exit 1
fi

snapshot() {
  {
    echo "===== $(date -u +%Y-%m-%dT%H:%M:%SZ) session=$SESSION ====="
    "$COLAB" sessions 2>&1 | grep -E "\[$SESSION\]" || echo "SESSION $SESSION: not listed"
    "$COLAB" exec -s "$SESSION" -f "$REMOTE" --timeout 120 2>&1 \
      | grep -v -E 'Could not (read|save) the OAuth token|You will be asked to sign in again' \
      || true
  } | tee -a "$LOG"
}

harvest() {
  [ -f "$HARVEST_REMOTE" ] || { echo "[harvest] missing $HARVEST_REMOTE" >&2; return 1; }
  echo "[harvest] running make_submission.py in $SESSION"
  "$COLAB" exec -s "$SESSION" -f "$HARVEST_REMOTE" --timeout 600 2>&1 \
    | grep -v -E 'Could not (read|save) the OAuth token|You will be asked to sign in again' \
    | tee -a "$LOG"
  rm -f "$CAND"
  if ! "$COLAB" download -s "$SESSION" /content/sis/candidate_colab.csv "$CAND" >>"$LOG" 2>&1; then
    echo "[harvest] no candidate downloaded (file may not exist yet)" | tee -a "$LOG"
    return 1
  fi
  if [ ! -s "$CAND" ]; then
    echo "[harvest] candidate is empty" | tee -a "$LOG"
    return 1
  fi
  echo "[harvest] candidate rows: $(wc -l < "$CAND")" | tee -a "$LOG"
  rm -rf "$MERGE_DIR"
  ( cd "$REPO" && .venv/bin/python -m squares merge \
      --baseline /tmp/best_bank/submission.csv \
      --baseline-report /tmp/best_bank/report.json \
      --candidate "$CAND" --output-dir "$MERGE_DIR" ) 2>&1 | tee -a "$LOG"
}

if [ "$MODE" = "loop" ]; then
  trap 'echo "[watch] stopped"; exit 0' INT TERM
  while true; do
    snapshot
    if [ "$HARVEST" = "1" ]; then harvest; fi
    sleep "$INTERVAL"
  done
else
  snapshot
  if [ "$HARVEST" = "1" ]; then harvest; fi
fi
