"""CPU-validated quench for dry slab/crossover candidates (no GPU needed).

For each dry candidate: dilation repair + fixed-angle LP repair, then official
v20 single-puzzle evaluation. Winners (valid + beats baseline on text route)
are written as improved_groups.csv for `squares merge` dual-path validation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from squares._vendor import official_metric as metric
from squares.search.gpu_relax import normalize, repair_small_overlaps
from squares.search.local_repair import repair_fixed_angles
from squares.search.structure import side_length


def load_baseline(path: Path) -> dict[int, np.ndarray]:
    frame = pd.read_csv(path, float_precision="round_trip")
    out = {}
    for n, group in frame.groupby("n", sort=True):
        n = int(n)
        if len(group) == n:
            arr = group.sort_values("square_id")[["x", "y", "angle"]].to_numpy(np.float64)
            out[n] = normalize(arr)
    return out


def to_rows(n: int, packing: np.ndarray, start_id: int) -> list[dict]:
    rows = []
    for sid in range(n):
        x, y, a = packing[sid]
        rows.append(
            {
                "id": str(start_id + sid),
                "n": str(n),
                "square_id": str(sid),
                "x": repr(float(x)),
                "y": repr(float(y)),
                "angle": repr(float(a)),
            }
        )
    return rows


def eval_text(n: int, rows: list[dict]):
    lines = [f"{r['id']},{r['n']},{r['square_id']},{r['x']},{r['y']},{r['angle']}" for r in rows]
    parsed = metric._parse_submission_csv("id,n,square_id,x,y,angle\n" + "\n".join(lines) + "\n")
    return metric.evaluate_single_puzzle(n, parsed[n])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--baseline", type=Path, required=True)
    ap.add_argument("--candidates", type=Path, required=True, help="candidates.npz")
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--max-repairs", type=int, default=48)
    ap.add_argument("--time-limit", type=float, default=2.0)
    args = ap.parse_args()
    started = time.monotonic()
    baseline = load_baseline(args.baseline)
    lengths = {n: side_length(p) for n, p in baseline.items()}
    manifest = json.loads(args.manifest.read_text())
    metas = {c["key"]: c for c in manifest["candidates"]}
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    z = np.load(args.candidates, allow_pickle=False)
    keys = [k for k in z.files][: args.max_repairs]
    winners: dict[int, tuple] = {}
    attempts = repaired_ok = 0
    log = []
    next_id = 0
    for key in keys:
        P = np.asarray(z[key], dtype=np.float64)
        meta = metas.get(key, {})
        n = int(meta.get("n", len(P)))
        base_L = lengths[n]
        attempts += 1
        cands = []
        d = repair_small_overlaps(P)
        if d is not None:
            cands.append(("dilation", d))
        for active_only in (True, False):
            for target in (None, base_L - 5e-9):
                try:
                    r, rep = repair_fixed_angles(
                        P,
                        target_side=target,
                        max_displacement=1e-3,
                        active_only=active_only,
                        neighbor_layers=1,
                        time_limit=args.time_limit,
                    )
                except ValueError:
                    continue
                if r is not None:
                    cands.append((f"lp_a{int(active_only)}_t{target is None}", r))
        best = None
        for how, q in cands:
            rows = to_rows(n, normalize(q), 0)
            try:
                _, score, Lstr, reason = eval_text(n, rows)
            except Exception as exc:  # noqa: BLE001
                log.append({"key": key, "n": n, "how": how, "error": str(exc)})
                continue
            if Lstr is None or reason != "ok":
                continue
            repaired_ok += 1
            L = float(Lstr)
            gain = base_L / (n**0.5) - L / (n**0.5)
            if L < base_L - 1e-9 and gain > 1e-10:
                if best is None or L < best[0]:
                    best = (L, gain, how, q)
        if best is not None:
            L, gain, how, q = best
            if n not in winners or L < winners[n][0]:
                winners[n] = (L, gain, how, key, q, meta)
                log.append({"key": key, "n": n, "how": how, "L": L, "gain": gain, "WIN": True})
    rows_out = []
    per_n = {}
    for n in sorted(winners):
        L, gain, how, key, q, meta = winners[n]
        qn = normalize(q)
        rws = to_rows(n, qn, next_id)
        next_id += n
        rows_out.extend(rws)
        per_n[str(n)] = {
            "L": L,
            "gain": gain,
            "how": how,
            "candidate": key,
            "dry_excess_L": meta.get("dry_excess_L"),
            "topology_hash": meta.get("topology_hash"),
        }
    imp = out / "improved_groups.csv"
    if rows_out:
        import csv

        with imp.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=("id", "n", "square_id", "x", "y", "angle"))
            w.writeheader()
            w.writerows(rows_out)
    sha = hashlib.sha256(imp.read_bytes()).hexdigest() if rows_out else None
    summary = {
        "baseline": str(args.baseline),
        "candidates": str(args.candidates),
        "attempted": attempts,
        "repaired_valid": repaired_ok,
        "winners": len(winners),
        "net_gain": sum(v[1] for v in winners.values()),
        "per_n": per_n,
        "log": log,
        "elapsed_seconds": time.monotonic() - started,
        "improved_groups_sha256": sha,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out / "per_n_gains.json").write_text(json.dumps(per_n, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "log"}, indent=2))


if __name__ == "__main__":
    main()
