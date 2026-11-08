"""Package a private, bounded Kaggle pilot without copying any credentials."""

import argparse
import base64
import hashlib
import io
import json
import lzma
import zipfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--account", default="qingyu1232")
    parser.add_argument("--slug", default="squares-structural-gpu-pilot-01")
    parser.add_argument("--seconds", type=int, default=900)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--steps", type=int, default=600)
    parser.add_argument("--warm-steps", type=int, default=200)
    parser.add_argument("--warm-passes", type=int, default=1)
    parser.add_argument("--warm-slack", type=float, default=0.003)
    parser.add_argument("--refine-passes", type=int, default=0)
    parser.add_argument("--refine-steps", type=int, default=2000)
    parser.add_argument("--depth-min", type=float, default=2e-5)
    parser.add_argument("--depth-max", type=float, default=1e-2)
    parser.add_argument("--rounds", type=int, default=2)
    parser.add_argument("--max-candidates", type=int, default=100)
    parser.add_argument("--run-name", default="pilot01")
    parser.add_argument("--kernel-source", action="append", default=[])
    parser.add_argument("--dataset-source", action="append", default=[])
    parser.add_argument("--staged-warm", action="store_true")
    parser.add_argument("--warm-shrink-factor", type=float, default=0.5)
    parser.add_argument("--incumbent-passes", type=int, default=0)
    parser.add_argument("--incumbent-step", type=float, default=1e-4)
    parser.add_argument("--incumbent-n", type=int, action="append", default=[])
    parser.add_argument("--local-repair", action="store_true")
    parser.add_argument("--local-repair-max-penetration", type=float, default=2e-4)
    parser.add_argument("--local-repair-explore-every", type=int, default=0)
    args = parser.parse_args()
    if not args.kernel_source and not args.dataset_source:
        parser.error(
            "Supply --kernel-source or --dataset-source containing the pinned baseline CSV"
        )
    if not args.run_name.replace("_", "").replace("-", "").isalnum():
        parser.error("--run-name must be a simple directory name")
    manifest = json.loads((args.candidates_dir / "manifest.json").read_text())
    baseline_hash = manifest["baseline"]["sha256"]
    buffer = io.BytesIO()
    files = []
    for folder in [ROOT / "src/squares", ROOT / "third_party/cuda_packing"]:
        files.extend(p for p in folder.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    files.append(ROOT / "scripts/experiments/run_gpu_pilot.py")
    digests = {}
    # Whole-bundle LZMA can share a dictionary across similar candidate arrays.
    # Compressing each NPZ member separately misses that structure and exceeds
    # Kaggle's one-megabyte source limit for even modest search pools.
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as archive:
        for p in sorted(files):
            target = str(p.relative_to(ROOT))
            archive.write(p, target)
            digests[target] = hashlib.sha256(p.read_bytes()).hexdigest()
        for name in ["candidates.npz", "manifest.json"]:
            p = args.candidates_dir / name
            content = p.read_bytes()
            if name.endswith(".npz"):
                with np.load(p, allow_pickle=False) as loaded:
                    raw = io.BytesIO()
                    np.savez(raw, **{key: loaded[key] for key in loaded.files})
                    content = raw.getvalue()
            archive.writestr("inputs/" + name, content)
            digests["inputs/" + name] = hashlib.sha256(content).hexdigest()
    payload = lzma.compress(buffer.getvalue(), preset=9)
    encoded = base64.b64encode(payload).decode()
    script = f"""# Private bounded research pilot. Public sources credited in bundled manifests.
import base64, hashlib, io, json, lzma, os, subprocess, sys, zipfile
from pathlib import Path

WORK = Path('/kaggle/working')
PROJECT = WORK / 'workspace'
PROJECT.mkdir(exist_ok=True)
zipfile.ZipFile(io.BytesIO(lzma.decompress(base64.b64decode({encoded!r})))).extractall(PROJECT)
expected = {baseline_hash!r}
matches = [p for p in Path('/kaggle/input').rglob('submission.csv')
           if hashlib.sha256(p.read_bytes()).hexdigest() == expected]
if not matches:
    raise RuntimeError('Pinned baseline not mounted; refusing to substitute another version')
baseline = matches[0]
print(json.dumps({{'stage':'baseline_ready','sha256':expected,'bytes':baseline.stat().st_size}}),flush=True)
subprocess.run([sys.executable,'-m','pip','install','--quiet','mpmath==1.4.1'],check=True)
import cupy as cp, mpmath, pandas as pd, scipy
environment = {{'gpu_count':cp.cuda.runtime.getDeviceCount(),'mpmath':mpmath.__version__,
               'pandas':pd.__version__,'scipy':scipy.__version__,'baseline_sha256':expected}}
(WORK/'environment.json').write_text(json.dumps(environment,indent=2))
print(json.dumps(environment),flush=True)
env = os.environ.copy()
env['PYTHONPATH'] = str(PROJECT/'src')
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']: env[k]='1'
command = [sys.executable,'-u',str(PROJECT/'scripts/experiments/run_gpu_pilot.py'),
           '--baseline',str(baseline),'--candidates',str(PROJECT/'inputs/candidates.npz'),
           '--manifest',str(PROJECT/'inputs/manifest.json'),'--output-dir',str(WORK/{args.run_name!r}),
           '--seconds',{str(args.seconds)!r},'--batch',{str(args.batch)!r},
           '--steps',{str(args.steps)!r},'--warm-steps',{str(args.warm_steps)!r},
           '--warm-passes',{str(args.warm_passes)!r},'--warm-slack',{str(args.warm_slack)!r},
           '--refine-passes',{str(args.refine_passes)!r},'--refine-steps',{str(args.refine_steps)!r},
           '--depth-min',{str(args.depth_min)!r},'--depth-max',{str(args.depth_max)!r},
           '--rounds',{str(args.rounds)!r},'--max-candidates',{str(args.max_candidates)!r},'--device','0']
command += ['--warm-shrink-factor',{str(args.warm_shrink_factor)!r},
            '--incumbent-passes',{str(args.incumbent_passes)!r},
            '--incumbent-step',{str(args.incumbent_step)!r}]
if {args.staged_warm!r}: command += ['--staged-warm']
if {args.local_repair!r}: command += ['--local-repair']
command += ['--local-repair-max-penetration',{str(args.local_repair_max_penetration)!r},
            '--local-repair-explore-every',{str(args.local_repair_explore_every)!r}]
for n in {args.incumbent_n!r}: command += ['--incumbent-n',str(n)]
result = subprocess.run(command,env=env,cwd=PROJECT)
print('PILOT_EXIT_CODE',result.returncode,flush=True)
raise SystemExit(result.returncode)
"""
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "pilot.py").write_text(script)
    metadata = {
        "id": f"{args.account}/{args.slug}",
        "title": args.slug.replace("-", " "),
        "code_file": "pilot.py",
        "language": "python",
        "kernel_type": "script",
        "is_private": True,
        "enable_gpu": True,
        "enable_internet": True,
        "machine_shape": "NvidiaTeslaT4",
        "competition_sources": [],
        "dataset_sources": args.dataset_source,
        "kernel_sources": args.kernel_source,
    }
    (args.output_dir / "kernel-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    record = {
        "baseline_sha256": baseline_hash,
        "bundle_sha256": hashlib.sha256(buffer.getvalue()).hexdigest(),
        "archive_bytes": len(buffer.getvalue()),
        "compressed_bytes": len(payload),
        "code_bytes": len(script),
        "files": digests,
        "search_seconds": args.seconds,
        "metadata": metadata,
        "search_parameters": {
            key: getattr(args, key)
            for key in (
                "batch",
                "steps",
                "warm_steps",
                "warm_passes",
                "warm_slack",
                "refine_passes",
                "refine_steps",
                "depth_min",
                "depth_max",
                "rounds",
                "max_candidates",
                "run_name",
                "staged_warm",
                "warm_shrink_factor",
                "incumbent_passes",
                "incumbent_step",
                "incumbent_n",
                "local_repair",
                "local_repair_max_penetration",
                "local_repair_explore_every",
            )
        },
    }
    (args.output_dir / "bundle_manifest.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k not in ["files", "metadata"]}, indent=2))


if __name__ == "__main__":
    main()
