#!/usr/bin/env python3
"""Auto-harvest completed zhuating CPU kernels: merge certified wins into the running
best bank, dual-path certify, and submit ONLY if strictly better than the board best
and daily quota remains. Chains the baseline so successive harvests compound.

State lives in outputs/research_20261120/auto_harvest_state.json. Prints an event line
on each harvest/submit (consumed by the monitor as a notification). Never stops kernels.
"""
import csv
import datetime
import io
import json
import os
import subprocess
import time
from pathlib import Path

REPO = Path("/Users/zhaohuaxiang/ccjjllt/squares")
PY = str(REPO / ".venv/bin/python")
KAGGLE = str(REPO / ".venv/bin/kaggle")
OUT = REPO / "outputs/research_20261120"
STATE = OUT / "auto_harvest_state.json"
ZHUATING = Path.home() / ".kaggle/access_token_zhuating"
CCJJLLT = Path.home() / ".kaggle/access_token_ccjjllt_check"
PROXY = "http://127.0.0.1:7897"
KERNELS = ["sis-gadget-quench-20261120", "sis-splice-20261120", "sis-cpu-hhop-20261120",
           "sis-cpu-wide-20261120", "sis-cpu-fq-hhop-20261120", "sis-tartan-mip-20261120"]


def log(m):
    print(f"[{datetime.datetime.now(datetime.timezone.utc):%H:%M:%SZ}] {m}", flush=True)


def env(token):
    e = dict(os.environ)
    e["KAGGLE_API_TOKEN"] = token.read_text().strip()
    e["HTTPS_PROXY"] = PROXY
    e["HTTP_PROXY"] = PROXY
    return e


def kstatus(slug):
    r = subprocess.run([KAGGLE, "kernels", "status", f"zhuating/{slug}"],
                       env=env(ZHUATING), capture_output=True, text=True, timeout=120)
    for s in ("COMPLETE", "ERROR", "CANCELLED", "RUNNING", "QUEUED"):
        if s in (r.stdout or ""):
            return s
    return "UNKNOWN"


def board():
    r = subprocess.run([KAGGLE, "competitions", "submissions", "squares-in-squares", "--csv"],
                       env=env(CCJJLLT), capture_output=True, text=True, timeout=240)
    rows = list(csv.DictReader(io.StringIO(r.stdout)))
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    vals, used = [], 0
    for row in rows:
        if "COMPLETE" in (row.get("status") or ""):
            try:
                vals.append(float(row["publicScore"]))
            except (TypeError, ValueError):
                pass
        if (row.get("date") or "").startswith(today):
            used += 1
    return used, (min(vals) if vals else None)


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"best_path": str(OUT / "merged_fqharden/submission.csv"),
            "best_report": str(OUT / "merged_fqharden/validation/report.json"),
            "best_score": 22.106026487050045, "harvested": []}


def save_state(s):
    STATE.write_text(json.dumps(s, indent=2))


def harvest(slug, st):
    dl = OUT / f"auto_{slug}"
    dl.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([KAGGLE, "kernels", "output", f"zhuating/{slug}", "-p", str(dl)],
                       env=env(ZHUATING), capture_output=True, text=True, timeout=600)
    summ = dl / "SUMMARY.json"
    final_name = None
    if summ.exists():
        try:
            final_name = json.loads(summ.read_text()).get("final_file")
        except Exception:  # noqa: BLE001
            pass
        log(f"{slug} SUMMARY: {summ.read_text()[:300]}")
    cand = None
    if final_name:
        hits = list(dl.rglob(final_name))
        if hits:
            cand = hits[0]
    if cand is None:
        for nm in ("closure_best.csv", "full_best.csv", "hop_best.csv"):
            hits = list(dl.rglob(nm))
            if hits:
                cand = hits[0]
                break
    if cand is None:
        log(f"{slug}: COMPLETE but no best csv (likely 0 wins); mark harvested")
        st["harvested"].append(slug)
        save_state(st)
        return
    log(f"{slug}: harvesting {cand.name}")
    merged = OUT / f"auto_merged_{slug}"
    r = subprocess.run([PY, "-m", "squares", "merge", "--baseline", st["best_path"],
                        "--baseline-report", st["best_report"], "--candidate", str(cand),
                        "--output-dir", str(merged), "--workers", "2"],
                       cwd=REPO, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        log(f"{slug}: merge FAILED {(r.stderr or '')[-300:]}")
        st["harvested"].append(slug)
        save_state(st)
        return
    r = subprocess.run([PY, "-m", "squares", "score", str(merged / "submission.csv"),
                        "--mode", "both", "--workers", "2",
                        "--output-dir", str(merged / "validation")],
                       cwd=REPO, capture_output=True, text=True, timeout=1800)
    rep = json.loads((merged / "validation/report.json").read_text())
    score = float(rep["runs"]["text"]["score"])
    valid = rep["runs"]["text"]["valid"] == 1000 and rep["runs"]["float64"]["valid"] == 1000
    log(f"{slug}: merged score {score:.12f} valid={valid} (prev best {st['best_score']:.12f})")
    st["harvested"].append(slug)
    if valid and score < st["best_score"] - 1e-10:
        st["best_path"] = str(merged / "submission.csv")
        st["best_report"] = str(merged / "validation/report.json")
        st["best_score"] = score
        save_state(st)
        used, best = board()
        if used < 9 and (best is None or score < best - 1e-10):
            msg = (f"auto-harvest {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%MZ}: "
                   f"local {score:.10f} dual-route 1000/1000 ({slug})")
            rs = subprocess.run([KAGGLE, "competitions", "submit", "squares-in-squares",
                                 "-f", str(merged / "submission.csv"), "-m", msg],
                                env=env(CCJJLLT), capture_output=True, text=True, timeout=400)
            log(f"{slug}: SUBMIT {(rs.stdout or rs.stderr or '').strip()[-200:]}")
        else:
            log(f"{slug}: improved local best to {score:.12f} but skip submit (used={used}, board={best})")
    else:
        save_state(st)
        log(f"{slug}: no strict improvement over running best; not submitted")


def main():
    log("auto-harvest start")
    while True:
        st = load_state()
        for slug in KERNELS:
            if slug in st["harvested"]:
                continue
            try:
                s = kstatus(slug)
            except Exception as exc:  # noqa: BLE001
                log(f"{slug}: status err {exc}")
                continue
            if s == "COMPLETE":
                try:
                    harvest(slug, st)
                except Exception as exc:  # noqa: BLE001
                    log(f"{slug}: harvest err {exc}")
            elif s == "ERROR":
                log(f"{slug}: ERROR (needs diagnosis)")
                st["harvested"].append(slug)
                save_state(st)
        time.sleep(300)


if __name__ == "__main__":
    main()