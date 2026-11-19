#!/bin/bash
# Wait until any of the night kernels reaches a terminal state, then exit so the
# operator session wakes up.  Read-only: never downloads, merges or installs.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
K="$REPO/.venv/bin/kaggle"
export KAGGLE_API_TOKEN="$(cat "$HOME/.kaggle/access_token_ccjjllt_check")"
export HTTPS_PROXY="http://127.0.0.1:7897" HTTP_PROXY="http://127.0.0.1:7897"
SLUGS="${*:-sis-cpp-engine-gap2-20261118/1 sis-cpp-engine-gap2-20261118 sis-alexkit-wide-20261118 sis-alexkit-d1d2-20261118 sis-alexkit-wide2-20261118}"
REPORT=/tmp/campaign2/kernel_done.txt
: > "$REPORT"
while true; do
  for s in $SLUGS; do
    st="$("$K" kernels status "ccjjllt/$s" 2>&1 | tail -1)"
    case "$st" in
      *COMPLETE*|*ERROR*|*CANCELLED*)
        printf '%s %s\n' "$(date -u +%FT%TZ)" "$st" >> "$REPORT"
        if [ "$(wc -l < "$REPORT")" -ge 1 ]; then
          # one terminal kernel is enough to wake the operator
          echo "TERMINAL: $st"
          exit 0
        fi ;;
    esac
  done
  sleep 240
done
