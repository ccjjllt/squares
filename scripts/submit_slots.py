#!/usr/bin/env python3
"""Submit the certified bank at fixed UTC slots, only when it beats the board.

The 2026-11-18 15:00Z slot was missed because the old scheduler slept in one
long `time.sleep()`; this version polls the clock every 30 s, keeps a state file
so a slot fires once per day, and passes the local proxy to the Kaggle CLI.

Usage:
  scripts/submit_slots.py --slots 09:00,15:00,21:00        # run forever
  scripts/submit_slots.py --slots 15:00 --check            # print decision only

A slot fires within the first 10 minutes after its time.  A submission is made
only if the bank is strictly better than the best COMPLETE public score and the
daily quota (10) is not exhausted.
"""
import argparse
import csv
import datetime
import io
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BANK = Path("/tmp/best_bank")
TOKEN = Path.home() / ".kaggle/access_token_ccjjllt_check"
SUBMIT = "/tmp/kaggle_ccjjllt_submit.py"
STATE = BANK / "slot_state.json"
PROXY = "http://127.0.0.1:7897"
PY = sys.executable


def env():
    e = dict(os.environ)
    e["KAGGLE_API_TOKEN"] = TOKEN.read_text().strip()
    e.setdefault("HTTPS_PROXY", PROXY)
    e.setdefault("HTTP_PROXY", PROXY)
    return e


def log(msg):
    print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%SZ')}] {msg}", flush=True)


def board():
    r = subprocess.run([str(REPO / ".venv/bin/kaggle"), "competitions", "submissions",
                        "squares-in-squares", "--csv"],
                       capture_output=True, text=True, env=env(), timeout=240)
    rows = list(csv.DictReader(io.StringIO(r.stdout)))
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    vals, used = [], 0
    for row in rows:
        if "COMPLETE" not in (row.get("status") or ""):
            continue
        try:
            vals.append(float(row["publicScore"]))
        except (TypeError, ValueError):
            pass
        if (row.get("date") or "").startswith(today):
            used += 1
    return used, (min(vals) if vals else None)


def fire(slot, check=False):
    report = json.loads((BANK / "report.json").read_text())
    score = float(report["runs"]["text"]["score"])
    sha = json.loads((BANK / "report.json").read_text())["input"]["sha256"] if "input" in report else ""
    used, best = board()
    need = best is None or score < best - 1e-10
    log(f"slot {slot}Z: bank {score:.12f} best public {best} used {used} -> "
        f"{'submit' if (need and used < 9) else 'skip'}")
    if check or not need or used >= 9:
        return False
    res = subprocess.run([PY, SUBMIT, str(BANK / "submission.csv"),
                          f"{slot}Z checkpoint {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d}: "
                          f"local {score:.10f} dual-route 1000/1000"],
                         capture_output=True, text=True, env=env(), timeout=300)
    log("submit: " + (res.stdout.strip().replace("\n", " ") or res.stderr.strip()[-300:]))
    return res.returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slots", default="09:00,15:00,21:00")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    slots = [s.strip() for s in args.slots.split(",") if s.strip()]
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    if args.check:
        for s in slots:
            fire(s, check=True)
        return
    log(f"scheduler start; slots {slots}")
    while True:
        now = datetime.datetime.now(datetime.timezone.utc)
        hhmm = now.strftime("%H:%M")
        day = now.strftime("%Y-%m-%d")
        for s in slots:
            h, m = map(int, s.split(":"))
            slot_dt = now.replace(hour=h, minute=m, second=0, microsecond=0)
            delta = (now - slot_dt).total_seconds()
            if 0 <= delta <= 600 and state.get(s) != day:
                if fire(s):
                    state[s] = day
                    STATE.write_text(json.dumps(state))
        time.sleep(30)


if __name__ == "__main__":
    main()
