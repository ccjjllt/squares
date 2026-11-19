#!/bin/bash
# Keep a Colab T4 GA session alive across free-tier reclamations.
#
# The session list is checked without touching the kernel; only when the session
# is gone does the script create a new one, bootstrap /content/sis from the
# private Kaggle bundle (current bank + fresh per-puzzle records) and launch the
# 4 GA workers.  A live session is never restarted.
#
# Usage: nohup scripts/colab_keeper.sh --loop 300 >> /tmp/campaign2/colab_keeper.log 2>&1 &
set -u

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SESSION="${COLAB_SESSION:-gpu1}"
ACCOUNT="${COLAB_ACCOUNT:-ccjjllt0}"
PROXY="${COLAB_PROXY:-http://127.0.0.1:7897}"
LOG="${COLAB_KEEPER_LOG:-/tmp/campaign2/colab_keeper.log}"
LOOP=0
[ "${1:-}" = "--loop" ] && LOOP="${2:-300}"

export PATH="$HOME/.local/bin:$PATH"
export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring
export COLAB_PROXY="$PROXY" COLAB_ACCOUNT="$ACCOUNT"

log() { echo "[$(date -u +%H:%M:%SZ)] $*" | tee -a "$LOG"; }

session_id() {
  local out
  out="$(colabx sessions 2>/dev/null)" || return 2   # 2 = unknown (network/proxy)
  echo "$out" | sed -n "s/^\[$SESSION\] \([^ ]*\).*/\1/p"
}

start_ga() {
  colabx exec -s "$SESSION" --timeout 180 2>/dev/null <<'PY' | tail -2
import subprocess
print(subprocess.run(["bash","-lc",
  "cd /content/sis && pgrep -f 'colab_pkg/ga.py' | wc -l"],capture_output=True,text=True).stdout.strip(), "ga procs")
PY
  colabx exec -s "$SESSION" --timeout 180 2>/dev/null <<'PY' | tail -4
import subprocess
cmd = ("cd /content/sis && setsid nohup env NPROC=4 MAX_MIN=600 "
       "bash run_colab.sh > run.out 2>&1 < /dev/null &")
print(subprocess.run(["bash","-lc",cmd],capture_output=True,text=True).stdout)
print("launch requested")
PY
}

bootstrap() {
  local tok
  tok="$(cat "$HOME/.kaggle/access_token_ccjjllt_check")"
  colabx exec -s "$SESSION" --timeout 1800 \
    -f "$REPO/scripts/colab_bootstrap_remote.py" --env KAGGLE_API_TOKEN="$tok" 2>/dev/null \
    | grep -E 'step|prepared|Tesla|BOOTSTRAP|downloaded' | tail -10
}

ensure() {
  local sid
  sid="$(session_id)"; local rc=$?
  [ $rc -eq 2 ] && { log "session list unavailable; skip this tick"; return 1; }
  if [ -n "$sid" ]; then
    local prev; prev="$(cat /tmp/campaign2/colab_runtime_id 2>/dev/null || true)"
    if [ "$sid" != "$prev" ]; then
      printf '%s\n' "$sid" > /tmp/campaign2/colab_runtime_id
      log "runtime $sid"
    fi
    return 0
  fi
  # One empty listing can be a transient API/proxy hiccup; confirm before
  # replacing a healthy runtime (an unnecessary `new` costs the VM).
  sleep 20
  sid="$(session_id)"
  [ -n "$sid" ] && return 0
  # Free-tier quota often reclaims new accounts' runtimes after ~15 min.  If the
  # last runtime died young twice, stop hammering for 90 min instead of burning
  # allocations on sessions that cannot accumulate GA progress.
  BACKOFF=/tmp/campaign2/colab_backoff_epoch
  CREATED=/tmp/campaign2/colab_created_epoch
  now="$(date +%s)"
  if [ -f "$BACKOFF" ] && [ "$now" -lt "$(cat "$BACKOFF")" ]; then
    log "in backoff until $(date -u -r "$(cat "$BACKOFF")" '+%H:%MZ'); not creating"
    return 1
  fi
  if [ -f "$CREATED" ]; then
    local life=$(( now - $(cat "$CREATED") ))
    if [ "$life" -lt 1500 ]; then
      echo $(( now + 5400 )) > "$BACKOFF"
      log "last runtime lived ${life}s (<25min); backing off 90min"
      return 1
    fi
  fi
  log "session $SESSION confirmed missing; creating T4"
  if ! colabx new -s "$SESSION" --gpu T4 >/dev/null 2>&1; then
    log "colab new failed (capacity/quota); will retry"
    return 1
  fi
  sleep 15
  sid="$(session_id)"
  [ -n "$sid" ] || { log "new session not listed; retry later"; return 1; }
  printf '%s\n' "$sid" > /tmp/campaign2/colab_runtime_id
  date +%s > /tmp/campaign2/colab_created_epoch
  log "session up ($sid); bootstrapping"
  bootstrap
  log "launching GA"
  start_ga
  return 0
}

if [ "$LOOP" -gt 0 ]; then
  log "keeper start; session=$SESSION account=$ACCOUNT every ${LOOP}s"
  while true; do ensure; sleep "$LOOP"; done
else
  ensure
fi
