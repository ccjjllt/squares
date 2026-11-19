#!/usr/bin/env python3
"""Status probe for the live Kaggle CPU kernels of the squares campaign.

Reads `kaggle kernels status` for the active refs, tracks transitions in a
small JSON state file, and optionally harvests a kernel the first time it
reaches COMPLETE. The harvest goes through the existing
`/tmp/campaign2/cpp_harvest/harvest_cpp.sh` (download -> sqpack_to_csv ->
`squares merge` -> install only when dual-route 1000/1000 and strictly better).

This script never submits to Kaggle and never edits the bank directly.
"""
import argparse
import concurrent.futures
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
KAGGLE = REPO / ".venv" / "bin" / "kaggle"
TOKEN = Path.home() / ".kaggle" / "access_token_ccjjllt_check"
HARVEST = Path("/tmp/campaign2/cpp_harvest/harvest_cpp.sh")

# tag, ref, nominal start (UTC)
KERNELS = [
    ("self-polish", "ccjjllt/sis-cpp-engine-self-polish-20261118", "2026-11-17T20:09:34Z"),
    ("broad-seeded", "ccjjllt/sis-cpp-engine-broad-seeded-20261118", "2026-11-17T23:21:21Z"),
    ("nearmiss", "ccjjllt/sis-cpp-engine-nearmiss-20261118", "2026-11-17T23:34:35Z"),
    ("polish2", "ccjjllt/sis-cpp-engine-polish2-20261118", "2026-11-18T00:44:37Z"),
]
EXTRA = [
    ("d2-gadget", "ccjjllt/sis-d2-gadget-678-902-20261118", "2026-11-18T00:42:11Z"),
    ("self-broad", "ccjjllt/sis-cpp-engine-self-broad-20261118", "2026-11-17T23:08:35Z"),
]


def env():
    e = dict(os.environ)
    if TOKEN.exists():
        e["KAGGLE_API_TOKEN"] = TOKEN.read_text().strip()
    return e


def query(ref):
    try:
        r = subprocess.run(
            [str(KAGGLE), "kernels", "status", ref],
            capture_output=True, text=True, env=env(), timeout=150,
        )
    except Exception as exc:  # noqa: BLE001
        return "QUERY_ERR", str(exc)[:100]
    text = (r.stdout + r.stderr).strip()
    m = re.search(r"KernelWorkerStatus\.([A-Z_]+)", text)
    if m:
        return m.group(1), ""
    return "UNKNOWN", text.splitlines()[-1][:120] if text else "no output"


def age(start, now):
    try:
        t = dt.datetime.fromisoformat(start.replace("Z", "+00:00"))
        mins = max(0, int((now - t).total_seconds() // 60))
        return f"{mins // 60}h{mins % 60:02d}m"
    except Exception:  # noqa: BLE001
        return "-"


def harvest(tag, ref):
    if not HARVEST.exists():
        print(f"[harvest] missing {HARVEST}")
        return 127
    print(f"[harvest] {tag} COMPLETE -> {HARVEST} {ref} {tag}", flush=True)
    try:
        r = subprocess.run(
            ["bash", str(HARVEST), ref, tag],
            cwd=str(REPO / ".."), capture_output=True, text=True,
            env=env(), timeout=3600,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[harvest] {tag} exception: {type(exc).__name__}: {exc}")
        return 124
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    if out:
        print(out[-4000:])
    if err:
        print("[harvest stderr] " + err[-1000:])
    print(f"[harvest] {tag} rc={r.returncode}")
    return r.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--harvest", action="store_true", help="harvest a kernel on first COMPLETE")
    ap.add_argument("--all", action="store_true", help="include recently finished/error kernels")
    ap.add_argument("--state", default="/tmp/campaign2/kernel_watch_state.json")
    args = ap.parse_args()

    refs = KERNELS + (EXTRA if args.all else [])
    now = dt.datetime.now(dt.timezone.utc)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        statuses = dict(zip([r[0] for r in refs], ex.map(lambda x: query(x[1]), refs)))

    state_path = Path(args.state)
    try:
        state = json.loads(state_path.read_text())
    except Exception:  # noqa: BLE001
        state = {}

    print(f"===== {now.strftime('%Y-%m-%dT%H:%M:%SZ')} =====")
    print(f"{'kernel':16s} {'status':12s} {'age':>8s}")
    for tag, ref, start in refs:
        st, note = statuses[tag]
        prev = state.get(tag, {})
        prev_st = prev.get("status")
        rec = prev or {}
        rec["ref"] = ref
        rec["status"] = st
        rec["last_seen"] = now.isoformat()
        rec.setdefault("first_seen", now.isoformat())
        state[tag] = rec
        print(f"{tag:16s} {st:12s} {age(start, now):>8s}" + (f"  {note}" if note else ""))
        if prev_st and prev_st != st:
            print(f"  [transition] {prev_st} -> {st}")

        if st == "COMPLETE" and args.harvest and not rec.get("harvested"):
            rc = harvest(tag, ref)
            rec["harvested"] = True
            rec["harvest_rc"] = rc
            rec["harvested_at"] = now.isoformat()
        elif st == "COMPLETE" and rec.get("harvested"):
            print(f"  [harvest] already done (rc={rec.get('harvest_rc')})")
        elif st == "ERROR":
            print("  [status] kernel errored; no harvest")

    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
