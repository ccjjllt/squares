#!/usr/bin/env python3
"""Bootstrap the SIS Colab GA session from the 2026-11-20 bundle (merged bank).

Run inside a rainer T4 session:
  colabx exec -s sisgpu -f scripts/colab_bootstrap_20261120.py --timeout 1800 \
    --env KAGGLE_API_TOKEN="$(cat ~/.kaggle/access_token_ccjjllt_check)"

The new dataset stores the sis tree as sis.zip, so after unzipping the dataset
download we unzip sis.zip once more to obtain /content/sis.
"""
import os
import subprocess
import sys

TOKEN = os.environ.get("KAGGLE_API_TOKEN", "")
ROOT = "/content/sis"
DATASET = "ccjjllt/sis-ga-bundle-20261120"

if not TOKEN:
    sys.exit("KAGGLE_API_TOKEN is not set")

DL = r'''
import os, requests
tok = os.environ["KAGGLE_API_TOKEN"]
url = "https://www.kaggle.com/api/v1/datasets/download/%s"
r = requests.get(url, headers={"Authorization": "Bearer " + tok}, timeout=600, stream=True)
r.raise_for_status()
n = 0
with open("/content/sis_bundle.zip", "wb") as fh:
    for chunk in r.iter_content(1 << 16):
        if chunk:
            fh.write(chunk)
            n += len(chunk)
print("downloaded", n, "bytes")
''' % DATASET


def sh(cmd, **kw):
    return subprocess.run(["bash", "-lc", cmd], capture_output=True, text=True, **kw)


print("=== step 1: download dataset ===", flush=True)
if os.path.isdir(ROOT):
    print("ROOT already exists, skipping download")
else:
    r = subprocess.run(["python", "-c", DL], env=dict(os.environ, KAGGLE_API_TOKEN=TOKEN))
    if r.returncode != 0:
        sys.exit("dataset download failed")
    os.makedirs("/content/sis", exist_ok=True)
    subprocess.run(["unzip", "-q", "-o", "/content/sis_bundle.zip", "-d", "/content/sis"], check=True)
    print(sh("ls -la /content/sis").stdout)

print("=== step 2: deps ===", flush=True)
r = sh("pip install -q cupy-cuda12x numba scipy")
print("pip rc", r.returncode, (r.stderr or "")[-400:], flush=True)

print("=== step 3: prepare ===", flush=True)
if os.path.exists(os.path.join(ROOT, "work", "runs", "starts", "index.json")):
    print("work/ already prepared")
else:
    r = subprocess.run(["python", "prepare_colab.py"], cwd=ROOT, capture_output=True, text=True, timeout=1800)
    print("rc", r.returncode)
    print((r.stdout or "")[-2000:])
    print((r.stderr or "")[-2000:])

print("=== step 4: sanity ===", flush=True)
for cmd in [
    "nvidia-smi --query-gpu=name,memory.total --format=csv,noheader",
    "ls /content/sis/work/runs/starts/n*.npy | wc -l",
    "head -3 /content/sis/work/runs/sweep_ns.txt",
    "df -h /content | tail -1",
]:
    r = sh(cmd)
    print(cmd, "->", (r.stdout or r.stderr).strip(), flush=True)

print("BOOTSTRAP DONE", flush=True)