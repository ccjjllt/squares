#!/bin/bash
# Safe Colab harvest: probe the kernel, restart it if wedged, pull the GA
# candidate, certify it against the bank and install only a strict, dual-route
# 1000/1000 improvement.  Never submits to Kaggle.
#
# Usage:
#   scripts/colab_harvest_safe.sh                 # one pass
#   scripts/colab_harvest_safe.sh --loop 1800     # every 30 min
#
# The Colab kernel occasionally stops answering exec requests while the GA
# workers keep running; `restart-kernel` frees it without killing the detached
# workers, so the probe retries once through a restart.
set -u

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SESSION="${COLAB_SESSION:-gpu1}"
ACCOUNT="${COLAB_ACCOUNT:-ccjjllt0}"
PROXY="${COLAB_PROXY:-http://127.0.0.1:7897}"
LOG="${COLAB_HARVEST_LOG:-/tmp/campaign2/colab_harvest.log}"
CAND="/tmp/campaign2/colab_candidate.csv"
MERGE="/tmp/campaign2/colab_merge"
MIN_GAIN="${MIN_GAIN:-1e-10}"
LOOP=0
[ "${1:-}" = "--loop" ] && LOOP="${2:-1800}"

export PATH="$HOME/.local/bin:$PATH"
export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring
export COLAB_PROXY="$PROXY" COLAB_ACCOUNT="$ACCOUNT"

log() { echo "[$(date -u +%H:%M:%SZ)] $*" | tee -a "$LOG"; }

probe() {
  # No session -> nothing to probe (the keeper owns recreation).
  colabx sessions 2>/dev/null | grep -q "\[$SESSION\]" || return 1
  printf 'print("PROBE_OK")\n' | colabx exec -s "$SESSION" --timeout 45 2>/dev/null | grep -q PROBE_OK
}

FAILS=/tmp/campaign2/kernel_fail_count
ensure_kernel() {
  if probe; then rm -f "$FAILS"; return 0; fi
  local n; n=$(( $(cat "$FAILS" 2>/dev/null || echo 0) + 1 ))
  echo "$n" > "$FAILS"
  if [ "$n" -lt 2 ]; then
    # One failed probe can be a CLI/proxy hiccup; do not touch the runtime.
    log "probe failed ($n); retry next pass"
    return 1
  fi
  log "probe failed twice; restarting kernel (detached GA workers survive)"
  colabx restart-kernel -s "$SESSION" >/dev/null 2>&1
  sleep 30
  if probe; then rm -f "$FAILS"; return 0; fi
  sleep 60
  probe && rm -f "$FAILS"
}

harvest() {
  ensure_kernel || { log "kernel unreachable after restart; skip"; return 1; }

  rm -f "$CAND"
  colabx exec -s "$SESSION" --timeout 600 -f "$REPO/scripts/colab_harvest_remote.py" 2>&1 \
    | grep -E 'RC |winning puzzles|n=[0-9]+ ' | tail -6 | tee -a "$LOG"
  colabx download -s "$SESSION" /content/sis/candidate_colab.csv "$CAND" >/dev/null 2>&1 || {
    log "no candidate to download"; return 0; }
  [ -s "$CAND" ] || { log "empty candidate"; return 0; }
  log "candidate rows: $(wc -l < "$CAND")"

  rm -rf "$MERGE"
  "$REPO/.venv/bin/python" -m squares merge \
    --baseline /tmp/best_bank/submission.csv \
    --baseline-report /tmp/best_bank/report.json \
    --candidate "$CAND" --output-dir "$MERGE" --workers 2 >"$MERGE.stdout" 2>&1 || {
      log "merge failed (see $MERGE.stdout)"; return 1; }
  "$REPO/.venv/bin/python" - "$MERGE" "$MIN_GAIN" <<'PY' | tee -a "$LOG"
import json, subprocess, sys
md, thr = sys.argv[1], float(sys.argv[2])
rep = json.load(open(f"{md}/report.json"))
gain = json.load(open(f"{md}/merge_report.json"))["net_gain"]["text"]
ok = rep["runs"]["text"]["valid"] == 1000 and rep["runs"]["float64"]["valid"] == 1000
print(f"merge gain {gain:.6e} valid {rep['runs']['text']['valid']}/{rep['runs']['float64']['valid']}")
if ok and gain > thr:
    r = subprocess.run([sys.executable, "/tmp/campaign2/install_candidate.py",
                        "--merge-dir", md, "--install"], capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:])
else:
    print("not installing (gain below threshold or route invalid)")
PY
}

mkdir -p /tmp/campaign2
if [ "$LOOP" -gt 0 ]; then
  log "loop start, every ${LOOP}s, session=$SESSION account=$ACCOUNT"
  trap 'log "loop stopped"; exit 0' INT TERM
  while true; do harvest; sleep "$LOOP"; done
else
  harvest
fi
