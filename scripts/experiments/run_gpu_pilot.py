"""Bounded GPU packing search with preserved source rows and incremental outputs.

The supervisor enforces the wall-clock budget, including compilation and CPU
scoring. It only terminates the worker process group created by this invocation.
No Kaggle submission is made by this script.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(variable, "1")

FIELDS = ("id", "n", "square_id", "x", "y", "angle")


def finite_float(value):
    """Keep diagnostic JSON valid even if an optimizer trajectory diverges."""
    value = float(value)
    return value if math.isfinite(value) else None


def atomic_json(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def append_event(path, record):
    with Path(path).open("a") as handle:
        handle.write(json.dumps(record, allow_nan=False) + "\n")
        handle.flush()
    print(json.dumps(record, allow_nan=False), flush=True)


def evaluate_rows(n, rows):
    import pandas as pd

    from squares._vendor import official_metric as metric

    text_rows = [{key: row[key] for key in FIELDS if key != "id"} for row in rows]
    raw = metric.evaluate_single_puzzle(n, text_rows)
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    frame = pd.read_csv(io.StringIO(stream.getvalue()), float_precision="round_trip")
    converted = metric._parse_submission_csv(frame.drop(columns=["id"]).to_csv(index=False))
    replay = metric.evaluate_single_puzzle(n, converted[n])
    return {
        "text": {"score": raw[1], "L": raw[2], "reason": raw[3]},
        "float64": {"score": replay[1], "L": replay[2], "reason": replay[3]},
    }


def rows_for_packing(packing, original_rows):
    rows = []
    for i, (point, original) in enumerate(zip(packing, original_rows, strict=True)):
        rows.append(
            {
                "id": original["id"],
                "n": original["n"],
                "square_id": str(i),
                "x": format(float(point[0]), ".17g"),
                "y": format(float(point[1]), ".17g"),
                "angle": format(float(point[2]), ".17g"),
            }
        )
    return rows


def persist_groups(output, improvements, all_original, state):
    """Unchanged groups retain each original numeric literal verbatim."""
    partial = output / "improved_groups.csv"
    full = output / "submission.csv"
    for destination, groups in (
        (partial, {n: improvements[n]["rows"] for n in improvements}),
        (
            full,
            {
                n: improvements[n]["rows"] if n in improvements else rows
                for n, rows in all_original.items()
            },
        ),
    ):
        temporary = destination.with_suffix(".csv.tmp")
        with temporary.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
            writer.writeheader()
            for n in sorted(groups):
                writer.writerows(groups[n])
        temporary.replace(destination)
    gains = [
        {key: value for key, value in item.items() if key != "rows"}
        for _, item in sorted(improvements.items())
    ]
    atomic_json(output / "per_n_gains.json", gains)
    state["improved_count"] = len(improvements)
    state["confirmed_score_gain"] = math.fsum(item["score_gain_float64"] for item in gains)
    state["submission_sha256"] = hashlib.sha256(full.read_bytes()).hexdigest()
    atomic_json(output / "summary.json", state)


def array_digest(packing):
    import numpy as np

    return hashlib.sha256(np.ascontiguousarray(packing, dtype="<f8").tobytes()).hexdigest()


def persist_donors(output, winners, winner_meta, near_misses, near_meta, baseline_hash):
    """Keep certified tight winners as well as structurally useful warm states.

    Unknown baseline lineage is explicit in winners.json, and is not offered to
    chain generation as a fictitious depth-zero source.
    """
    import numpy as np

    def save(name, arrays, entries):
        temporary = output / f"{name}.tmp.npz"
        np.savez_compressed(temporary, **arrays)
        temporary.replace(output / f"{name}.npz")
        atomic_json(
            output / f"{name}.json",
            {
                "baseline_sha256": baseline_hash,
                "archive_sha256": hashlib.sha256((output / f"{name}.npz").read_bytes()).hexdigest(),
                "candidates": entries,
            },
        )

    ordered = [winner_meta[key] for key in sorted(winners)]
    save("winners", winners, ordered)
    combined, metadata, seen = {}, [], set()
    for arrays, entries in ((winners, ordered), (near_misses, near_meta)):
        for entry in entries:
            if entry.get("chain_depth") is None:
                continue
            key = entry["key"]
            digest = array_digest(arrays[key])
            if digest in seen:
                continue
            seen.add(digest)
            combined[key] = arrays[key]
            metadata.append(entry)
    save("donors", combined, metadata)


def warm_schedule(before, candidate_side, slack, staged, factor):
    """Descending box slack; the first stage never squeezes the dry candidate."""
    if not staged:
        return [slack]
    start = max(slack, candidate_side - before + 1e-4)
    schedule = [start]
    while schedule[-1] * factor > slack:
        schedule.append(schedule[-1] * factor)
    if schedule[-1] > slack:
        schedule.append(slack)
    return schedule


def solve_tight(relaxer, starts, boxes, args, state, deadline):
    import numpy as np

    trials = np.array(starts, copy=True)
    stats = np.full((len(trials), 3), np.nan)
    valid = np.isfinite(trials).all(axis=(1, 2))
    if valid.any() and time.monotonic() < deadline - 5:
        trials[valid], stats[valid], timing = relaxer.quench(
            trials[valid], boxes[valid], steps=args.steps
        )
        state["cuda_seconds"] += timing["cuda_seconds"]
    initial_stats = stats.copy()
    refine_completed = 0
    for _ in range(args.refine_passes):
        if time.monotonic() >= deadline - 8 or np.all(stats[:, 1] < 2e-11):
            break
        valid = np.isfinite(trials).all(axis=(1, 2))
        if not valid.any():
            break
        trials[valid], stats[valid], timing = relaxer.quench(
            trials[valid], boxes[valid], steps=args.refine_steps
        )
        state["cuda_seconds"] += timing["cuda_seconds"]
        refine_completed += 1
    return trials, initial_stats, stats, refine_completed


def worker(args):
    import numpy as np

    from squares.search.gpu_relax import (
        CudaRelaxer,
        compress_centres,
        normalize,
        repair_small_overlaps,
        repair_with_diagnostics,
        side,
    )
    from squares.search.structure import packing_hash

    started = time.monotonic()
    deadline = started + args.seconds
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    baseline_hash = hashlib.sha256(args.baseline.read_bytes()).hexdigest()
    state = {
        "schema_version": 1,
        "status": "starting",
        "baseline": str(args.baseline),
        "baseline_sha256": baseline_hash,
        "time_budget_seconds": args.seconds,
        "seed": args.seed,
        "batch": args.batch,
        "steps": args.steps,
        "warm_steps": args.warm_steps,
        "warm_passes": args.warm_passes,
        "warm_slack": args.warm_slack,
        "staged_warm": args.staged_warm,
        "warm_shrink_factor": args.warm_shrink_factor,
        "incumbent_passes": args.incumbent_passes,
        "incumbent_step": args.incumbent_step,
        "incumbent_n": list(dict.fromkeys(args.incumbent_n)),
        "continuation_batches_completed": 0,
        "local_repair": args.local_repair,
        "local_repair_max_penetration": args.local_repair_max_penetration,
        "local_repair_explore_every": args.local_repair_explore_every,
        "local_repair_attempts": 0,
        "local_repair_seconds": 0.0,
        "device": args.device,
        "refine_steps": args.refine_steps,
        "refine_passes": args.refine_passes,
        "compression_depth_min": args.depth_min,
        "compression_depth_max": args.depth_max,
        "control": "frozen input baseline; matched perturbations and target boxes",
        "improved_count": 0,
        "confirmed_score_gain": 0.0,
        "cuda_seconds": 0.0,
        "batches_completed": 0,
        "candidates_examined": 0,
        "measurement": (
            "Per changed n: official v20 text and pandas round_trip; "
            "no full-baseline score assumed."
        ),
    }
    atomic_json(output / "summary.json", state)
    original = {}
    with args.baseline.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("Baseline must have id,n,square_id,x,y,angle columns")
        for row in reader:
            original.setdefault(int(row["n"]), []).append(row)
    for n, rows in original.items():
        rows.sort(key=lambda row: int(row["square_id"]))
        if len(rows) != n or [int(row["square_id"]) for row in rows] != list(range(n)):
            raise ValueError(f"Malformed baseline n={n}")
    if set(original) != set(range(1, 1001)):
        raise ValueError("Pilot requires a complete baseline for n=1..1000")
    bank = {
        n: np.array([[float(row[c]) for c in ("x", "y", "angle")] for row in rows])
        for n, rows in original.items()
    }
    # Controls must not inherit a structure-arm improvement from an earlier batch.
    control_bank = {n: p.copy() for n, p in bank.items()}
    lengths = {n: side(p) for n, p in bank.items()}
    manifest = json.loads(args.manifest.read_text())
    manifest_hash = manifest.get("baseline", {}).get("sha256")
    if manifest_hash != baseline_hash:
        raise ValueError("Candidate manifest uses a different baseline")
    entries = manifest["candidates"] if isinstance(manifest, dict) else manifest
    entries = entries[: args.max_candidates]
    loaded = np.load(args.candidates, allow_pickle=False)
    entries = [entry for entry in entries if int(entry["n"]) in bank]
    state["candidate_pool_count"] = len(entries)
    improvements, baseline_scores = {}, {}
    # A valid source-preserving submission exists even if compilation later fails.
    persist_groups(output, improvements, original, state)
    if not entries and not args.incumbent_n:
        state.update(status="completed", reason="empty_candidate_pool")
        atomic_json(output / "summary.json", state)
        return
    relaxer = CudaRelaxer(args.device, args.kernel)
    state.update(status="running", hardware=relaxer.info)
    atomic_json(output / "summary.json", state)
    rng = np.random.default_rng(args.seed)
    near_misses = {}
    near_meta = []
    winners, winner_meta = {}, {}
    lineage = manifest.get("baseline_lineage", {})
    baseline_meta = {
        n: {
            "chain_depth": lineage.get(str(n), {}).get("chain_depth"),
            "parent_operator": lineage.get(str(n), {}).get(
                "parent_operator", lineage.get(str(n), {}).get("operator", "baseline")
            ),
            "parents": lineage.get(str(n), {}).get(
                "parents",
                lineage.get(str(n), {}).get(
                    "ancestry",
                    [{"source": str(args.baseline), "sha256": baseline_hash, "n": n}],
                ),
            ),
        }
        for n in bank
    }
    bank_meta = {n: dict(meta) for n, meta in baseline_meta.items()}
    last_followed = {}
    halv = args.batch // 2
    depths = np.geomspace(args.depth_min, args.depth_max, halv)
    event_path = output / "events.jsonl"

    def accept(n, packing, *, meta, origin, operator, key, step, trajectory, round_no):
        if n not in baseline_scores:
            baseline_scores[n] = evaluate_rows(n, original[n])
        initial = baseline_scores[n]
        if any(route["reason"] != "ok" for route in initial.values()):
            append_event(
                event_path,
                {
                    "event": "baseline_not_valid",
                    "n": n,
                    "result": initial,
                },
            )
            return False
        rows = rows_for_packing(packing, original[n])
        measured = evaluate_rows(n, rows)
        previous = improvements[n]["after"] if n in improvements else initial
        if not all(
            measured[mode]["reason"] == "ok"
            and measured[mode]["score"] < previous[mode]["score"] - args.min_score_gain
            for mode in ("text", "float64")
        ):
            return False
        previous_digest = array_digest(bank[n])
        bank[n] = packing.copy()
        bank_meta[n] = dict(meta)
        lengths[n] = side(packing)
        improvements[n] = {
            "n": n,
            "candidate_key": key,
            "origin": origin,
            "operator": operator,
            "round": round_no,
            "seed": args.seed,
            "trajectory": trajectory,
            "compression_depth": step,
            "parents": meta["parents"],
            "chain_depth": meta["chain_depth"],
            "parent_operator": meta["parent_operator"],
            "previous_incumbent_array_sha256": previous_digest,
            "before": initial,
            "after": measured,
            "score_gain_float64": initial["float64"]["score"] - measured["float64"]["score"],
            "rows": rows,
        }
        winner_key = f"winner_{n:04d}"
        winners[winner_key] = packing.copy()
        winner_meta[winner_key] = {
            "key": winner_key,
            "n": n,
            "donor_kind": "winner",
            "parent_candidate": key,
            "parent_operator": meta["parent_operator"],
            "last_operator": operator,
            "chain_depth": meta["chain_depth"],
            "ancestry": meta["parents"],
            "L_float": lengths[n],
            "not_officially_scored": False,
            "scores": measured,
            "array_sha256": array_digest(packing),
            "state_sha256": packing_hash(packing),
            "previous_incumbent_array_sha256": previous_digest,
        }
        state["elapsed_seconds"] = time.monotonic() - started
        persist_groups(output, improvements, original, state)
        persist_donors(output, winners, winner_meta, near_misses, near_meta, baseline_hash)
        return True

    def repair_arm(indices, trials, before):
        repaired = {b: repair_with_diagnostics(trials[b]) for b in indices}
        if not args.local_repair:
            return repaired
        from squares.search.local_repair import repair_fixed_angles

        candidates = [
            b
            for b, (_, diag) in repaired.items()
            if diag.get("raw_L") is not None
            and diag["raw_L"] < before - 2e-8
            and diag.get("max_pair_penetration", math.inf) <= 2e-4
        ]
        state["local_repair_arms"] = state.get("local_repair_arms", 0) + 1
        near = [
            b
            for b in candidates
            if repaired[b][1]["max_pair_penetration"] <= args.local_repair_max_penetration
        ]
        selected = sorted(
            near, key=lambda b: (repaired[b][1]["max_pair_penetration"], repaired[b][1]["raw_L"])
        )[:2]
        # Empirical scheduling only: occasionally probe a larger residual so
        # this acceleration does not assert that skipped states are infeasible.
        if (
            args.local_repair_explore_every
            and state["local_repair_arms"] % args.local_repair_explore_every == 0
        ):
            other = [b for b in candidates if b not in selected]
            if other:
                selected = selected[:1] + [
                    min(other, key=lambda b: repaired[b][1]["max_pair_penetration"])
                ]
        for b in selected:
            remaining = deadline - time.monotonic() - 8
            if remaining < 0.1:
                break
            old, diag = repaired[b]
            raw_length = diag["raw_L"]
            target = raw_length + 0.25 * (before - raw_length)
            tick = time.monotonic()
            local, local_diag = repair_fixed_angles(
                trials[b],
                target_side=target,
                max_displacement=1e-3,
                clearance=2e-10,
                active_only=True,
                neighbor_layers=1,
                time_limit=min(2.0, remaining),
            )
            state["local_repair_attempts"] += 1
            state["local_repair_seconds"] += time.monotonic() - tick
            diag["local_repair"] = local_diag
            if (
                local is not None
                and side(local) < before - 2e-8
                and (old is None or side(local) < side(old))
            ):
                diag["dilation_repaired_L"] = diag.get("repaired_L")
                diag["repaired_L"] = side(local)
                diag["repair_status"] = "local_repaired"
                repaired[b] = local, diag
        return repaired

    def continue_incumbent(n, round_no):
        if not args.incumbent_passes or last_followed.get(n) == array_digest(bank[n]):
            return
        step = min(args.depth_max, max(args.depth_min, args.incumbent_step))
        for pass_no in range(args.incumbent_passes):
            if time.monotonic() >= deadline - 8 or step < args.depth_min:
                break
            before = lengths[n]
            source_hash = array_digest(bank[n])
            source_meta = dict(bank_meta[n])
            # Do not expand or return to the original candidate: follow the last
            # certified feasible state directly into the next compression step.
            perturbations = np.zeros((halv, n, 3))
            perturbations[1:, :, :2] = rng.normal(0, min(2e-5, step / 4), (halv - 1, n, 2))
            perturbations[1:, :, 2] = rng.normal(0, min(1e-5, step / 8), (halv - 1, n))
            starts = np.array(
                [
                    compress_centres(normalize(source) + jitter, before - step)
                    for source in (bank[n], control_bank[n])
                    for jitter in perturbations
                ]
            )
            boxes = np.full(args.batch, before - step)
            tick = time.monotonic()
            trials, _, stats, passes = solve_tight(relaxer, starts, boxes, args, state, deadline)
            accepted_count, checked, diagnostics = 0, 0, []
            for kind, indices in (("incumbent", range(halv)), ("control", range(halv, args.batch))):
                promising = []
                arm_repairs = repair_arm(indices, trials, lengths[n])
                for b in indices:
                    packing, repair = arm_repairs[b]
                    diagnostics.append(
                        {
                            "trajectory": b,
                            "arm": kind,
                            "final_max_penetration": finite_float(stats[b, 1]),
                            **repair,
                        }
                    )
                    if packing is not None and side(packing) < lengths[n] - 2e-8:
                        promising.append((side(packing), b, packing))
                for _, b, packing in sorted(promising, key=lambda item: item[0])[:2]:
                    if time.monotonic() >= deadline - 5:
                        break
                    checked += 1
                    accepted_count += accept(
                        n,
                        packing,
                        meta=source_meta if kind == "incumbent" else baseline_meta[n],
                        origin=kind,
                        operator="incumbent_continuation"
                        if kind == "incumbent"
                        else "direct_relax",
                        key=f"incumbent_{n}_{pass_no}",
                        step=step,
                        trajectory=b,
                        round_no=round_no,
                    )
            append_event(
                event_path,
                {
                    "event": "continuation",
                    "n": n,
                    "pass": pass_no,
                    "round": round_no,
                    "source_array_sha256": source_hash,
                    "before_L": before,
                    "after_retained_L": lengths[n],
                    "step": step,
                    "accepted": accepted_count,
                    "official_candidates_scored": checked,
                    "trajectories": diagnostics,
                    "refine_passes_completed": passes,
                    "seconds": time.monotonic() - tick,
                },
            )
            state["continuation_batches_completed"] += 1
            state["elapsed_seconds"] = time.monotonic() - started
            atomic_json(output / "summary.json", state)
            step = min(args.depth_max, step * 1.25) if accepted_count else step / 2
        last_followed[n] = array_digest(bank[n])

    # Explicit incumbents need no synthetic structural identity candidate.
    for n in dict.fromkeys(args.incumbent_n):
        if time.monotonic() >= deadline - 8:
            break
        continue_incumbent(n, round_no=-1)

    for round_no in range(args.rounds):
        for index, entry in enumerate(entries):
            if time.monotonic() >= deadline - 8:
                break
            key = entry.get("key", entry.get("npz_key", entry.get("id")))
            n = int(entry["n"])
            candidate = np.array(loaded[key], dtype=np.float64, copy=True)
            if candidate.shape != (n, 3) or not np.isfinite(candidate).all():
                raise ValueError(f"Malformed candidate {key}")
            if entry.get("array_sha256"):
                # Transport integrity must not depend on platform-specific trig
                # rounding in geometric normalization.
                array_hash = hashlib.sha256(
                    np.ascontiguousarray(candidate, dtype="<f8").tobytes()
                ).hexdigest()
                if array_hash != entry["array_sha256"]:
                    raise ValueError(f"Candidate array hash mismatch: {key}")
            elif entry.get("state_sha256") and packing_hash(candidate) != entry["state_sha256"]:
                raise ValueError(f"Candidate state hash mismatch: {key}")
            incumbent = control_bank[n]
            before = lengths[n]
            seeds, boxes, labels = [], [], []
            # Common random numbers and identical boxes pair the two arms.
            perturbations = np.zeros((halv, n, 3))
            perturbations[1:, :, :2] = rng.normal(0, 2e-4, (halv - 1, n, 2))
            perturbations[1:, :, 2] = rng.normal(0, 1e-4, (halv - 1, n))
            schedule = warm_schedule(
                before,
                side(candidate),
                args.warm_slack,
                args.staged_warm,
                args.warm_shrink_factor,
            )
            for kind, source in (("structure", candidate), ("control", incumbent)):
                for j, depth in enumerate(depths):
                    p = normalize(source) + perturbations[j]
                    seeds.append(compress_centres(p, before + schedule[0]))
                    labels.append((kind, j, float(depth)))
            tick = time.monotonic()
            warm = np.array(seeds)
            boxes = np.full(args.batch, before + schedule[0])
            warm_stats = np.full((args.batch, 3), np.nan)
            warm_passes_completed = 0
            warm_stages = []
            for stage_index, slack in enumerate(schedule):
                if time.monotonic() >= deadline - 8:
                    break
                if stage_index:
                    # Only tighten trajectories that solved the preceding box;
                    # stalled rows get more relaxation at their last box.
                    ready = np.isfinite(warm).all(axis=(1, 2)) & (warm_stats[:, 1] <= 1e-5)
                    for b in np.flatnonzero(ready):
                        next_box = max(
                            before + slack, before + (boxes[b] - before) * args.warm_shrink_factor
                        )
                        warm[b] = compress_centres(warm[b], next_box)
                        boxes[b] = next_box
                for _ in range(args.warm_passes):
                    valid = np.isfinite(warm).all(axis=(1, 2))
                    if not valid.any():
                        break
                    warm[valid], warm_stats[valid], timing = relaxer.quench(
                        warm[valid], boxes[valid], steps=args.warm_steps
                    )
                    state["cuda_seconds"] += timing["cuda_seconds"]
                    warm_passes_completed += 1
                    if time.monotonic() >= deadline - 8 or np.all(warm_stats[:, 1] < 2e-11):
                        break
                warm_stages.append(
                    {
                        "slack": slack,
                        "box_by_trajectory": [float(v) for v in boxes],
                        "at_requested_box": int(
                            np.isclose(boxes, before + slack, rtol=0, atol=1e-10).sum()
                        ),
                        "max_penetration_by_trajectory": [
                            finite_float(v) for v in warm_stats[:, 1]
                        ],
                    }
                )
            # Save one best feasible near-miss per structural parent immediately.
            # It remains available if the following tight solve hits the hard budget.
            near_options = []
            for b in range(halv):
                if warm_stats[b, 1] <= 1e-5:
                    p = repair_small_overlaps(warm[b])
                    if p is not None and side(p) <= before + 0.01:
                        near_options.append((side(p), b, p))
            if near_options:
                length, b, p = min(near_options, key=lambda item: item[0])
                near_key = f"near_{key}"
                if near_key not in near_misses or length < side(near_misses[near_key]):
                    near_misses[near_key] = p
                    near_meta = [item for item in near_meta if item["key"] != near_key]
                    near_meta.append(
                        {
                            "key": near_key,
                            "n": n,
                            "parent_candidate": key,
                            "parent_operator": entry.get("operator", "unknown"),
                            "chain_depth": entry.get("parameters", {}).get("chain_depth", 0),
                            "ancestry": entry.get("parents", []),
                            "L_float": length,
                            "not_officially_scored": True,
                            "donor_kind": "near_miss",
                            "array_sha256": array_digest(p),
                            "state_sha256": packing_hash(p),
                        }
                    )
                    temporary = output / "near_misses.tmp.npz"
                    np.savez_compressed(temporary, **near_misses)
                    temporary.replace(output / "near_misses.npz")
                    atomic_json(output / "near_misses.json", {"candidates": near_meta})
                    persist_donors(
                        output, winners, winner_meta, near_misses, near_meta, baseline_hash
                    )
            if time.monotonic() >= deadline - 8:
                break
            target = np.array([before - depth for _, _, depth in labels])
            tight_starts = np.array(
                [compress_centres(p, length) for p, length in zip(warm, target, strict=True)]
            )
            if args.staged_warm:
                reached = np.isclose(boxes, before + args.warm_slack, rtol=0, atol=1e-10)
                tight_starts[~reached] = np.nan
            trials, initial_stats, stats, refine_completed = solve_tight(
                relaxer, tight_starts, target, args, state, deadline
            )
            checked, accepted = 0, 0
            best_by_kind = {"structure": None, "control": None}
            diagnostics = []
            # Score at most two promising results per arm; larger energy alone never earns a gain.
            for kind, indices in (("structure", range(halv)), ("control", range(halv, args.batch))):
                promising = []
                arm_repairs = repair_arm(indices, trials, lengths[n])
                for b in indices:
                    p, repair = arm_repairs[b]
                    diagnostics.append(
                        {
                            "trajectory": b,
                            "arm": kind,
                            "depth": labels[b][2],
                            "target_L": float(target[b]),
                            "initial_energy": finite_float(initial_stats[b, 0]),
                            "initial_max_penetration": finite_float(initial_stats[b, 1]),
                            "final_energy": finite_float(stats[b, 0]),
                            "final_max_penetration": finite_float(stats[b, 1]),
                            "final_iterations": int(stats[b, 2])
                            if np.isfinite(stats[b, 2])
                            else None,
                            **repair,
                        }
                    )
                    if p is not None:
                        length = side(p)
                        best_by_kind[kind] = min(
                            best_by_kind[kind] if best_by_kind[kind] is not None else math.inf,
                            length,
                        )
                        if length < lengths[n] - 2e-8:
                            promising.append((length, b, p))
                for _length, b, p in sorted(promising, key=lambda x: x[0])[:2]:
                    if time.monotonic() >= deadline - 5:
                        break
                    checked += 1
                    source_meta = (
                        {
                            "chain_depth": entry.get("parameters", {}).get("chain_depth"),
                            "parent_operator": entry.get("operator", "unknown"),
                            "parents": entry.get("parents", []),
                        }
                        if kind == "structure"
                        else baseline_meta[n]
                    )
                    accepted += accept(
                        n,
                        p,
                        meta=source_meta,
                        origin=kind,
                        operator=entry.get("operator", "unknown")
                        if kind == "structure"
                        else "direct_relax",
                        key=key,
                        step=labels[b][2],
                        trajectory=b,
                        round_no=round_no,
                    )
            event = {
                "event": "batch",
                "round": round_no,
                "candidate_index": index,
                "candidate_key": key,
                "n": n,
                "operator": entry.get("operator", "unknown"),
                "before_L": before,
                "after_retained_L": lengths[n],
                "best_float_repaired_L_by_arm": best_by_kind,
                "refine_passes_completed": refine_completed,
                "warm_passes_completed": warm_passes_completed,
                "warm_stages": warm_stages,
                "trajectories": diagnostics,
                "official_candidates_scored": checked,
                "accepted": accepted,
                "minimum_energy": float(np.nanmin(stats[:, 0]))
                if np.isfinite(stats[:, 0]).any()
                else None,
                "seconds": time.monotonic() - tick,
                "elapsed_seconds": time.monotonic() - started,
            }
            append_event(event_path, event)
            state["batches_completed"] += 1
            state["candidates_examined"] += 1
            state["elapsed_seconds"] = time.monotonic() - started
            atomic_json(output / "summary.json", state)
            continue_incumbent(n, round_no)
        if time.monotonic() >= deadline - 8:
            break
    state.update(status="completed", elapsed_seconds=time.monotonic() - started)
    persist_groups(output, improvements, original, state)
    persist_donors(output, winners, winner_meta, near_misses, near_meta, baseline_hash)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline",
        type=Path,
        default=Path("outputs/submissions/merged_research_20261107/submission.csv"),
        help="Complete reference CSV; defaults to the verified final submission",
    )
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seconds", type=float, default=900)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--steps", type=int, default=600)
    parser.add_argument("--warm-steps", type=int, default=200)
    parser.add_argument("--warm-passes", type=int, default=1)
    parser.add_argument("--warm-slack", type=float, default=0.003)
    parser.add_argument("--staged-warm", action="store_true")
    parser.add_argument("--warm-shrink-factor", type=float, default=0.5)
    parser.add_argument("--incumbent-passes", type=int, default=0)
    parser.add_argument("--incumbent-step", type=float, default=1e-4)
    parser.add_argument("--incumbent-n", type=int, action="append", default=[])
    parser.add_argument("--local-repair", action="store_true")
    parser.add_argument("--local-repair-max-penetration", type=float, default=2e-4)
    parser.add_argument("--local-repair-explore-every", type=int, default=0)
    parser.add_argument("--refine-passes", type=int, default=0)
    parser.add_argument("--refine-steps", type=int, default=2000)
    parser.add_argument("--depth-min", type=float, default=2e-5)
    parser.add_argument("--depth-max", type=float, default=1e-2)
    parser.add_argument("--rounds", type=int, default=2)
    parser.add_argument("--max-candidates", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20261107)
    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--kernel", type=Path)
    parser.add_argument("--min-score-gain", type=float, default=1e-10)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not 0 <= args.local_repair_max_penetration <= 2e-4:
        parser.error("--local-repair-max-penetration must lie in [0, 2e-4]")
    if args.local_repair_explore_every < 0:
        parser.error("--local-repair-explore-every must be nonnegative")
    if args.batch < 4 or args.batch % 2:
        parser.error("--batch must be even and at least 4")
    if not all(1 <= steps <= 5000 for steps in (args.steps, args.warm_steps, args.refine_steps)):
        parser.error("All step counts must be between 1 and 5000")
    if args.warm_passes < 1 or not 0 < args.warm_slack <= 0.1:
        parser.error("--warm-passes must be positive and 0 < --warm-slack <= 0.1")
    if not 0.1 <= args.warm_shrink_factor <= 0.9:
        parser.error("--warm-shrink-factor must be between 0.1 and 0.9")
    if not 0 <= args.incumbent_passes <= 100 or not 0 < args.incumbent_step < 1:
        parser.error("--incumbent-passes must be 0..100 and --incumbent-step between 0 and 1")
    if any(not 1 <= n <= 1000 for n in args.incumbent_n):
        parser.error("--incumbent-n must be between 1 and 1000")
    if args.incumbent_n and not args.incumbent_passes:
        parser.error("--incumbent-n requires positive --incumbent-passes")
    if args.refine_passes < 0:
        parser.error("--refine-passes must be nonnegative")
    if not 0 < args.depth_min <= args.depth_max < 1:
        parser.error("Compression depths must satisfy 0 < min <= max < 1")
    if not math.isfinite(args.min_score_gain) or args.min_score_gain < 0:
        parser.error("--min-score-gain must be finite and nonnegative")
    if (
        not math.isfinite(args.seconds)
        or args.seconds < 30
        or args.rounds < 1
        or args.max_candidates < 1
    ):
        parser.error("Budget must be >=30 seconds, with positive rounds and candidate count")
    return args


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.worker:
        try:
            worker(args)
        except Exception as exc:
            path = args.output_dir / "summary.json"
            state = json.loads(path.read_text()) if path.exists() else {}
            state.update(status="error", error=f"{type(exc).__name__}: {exc}")
            atomic_json(path, state)
            raise
        return 0
    started = time.monotonic()
    child = subprocess.Popen(
        [sys.executable, "-u", str(Path(__file__).resolve()), *sys.argv[1:], "--worker"],
        start_new_session=True,
    )
    timed_out = False
    try:
        code = child.wait(timeout=args.seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(child.pid, signal.SIGTERM)
        try:
            child.wait(timeout=3)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait()
        code = 0
    path = args.output_dir / "summary.json"
    state = json.loads(path.read_text()) if path.exists() else {}
    state["supervisor_elapsed_seconds"] = time.monotonic() - started
    state["worker_exit_code"] = child.returncode
    if timed_out:
        state["status"] = "budget_exhausted"
        state["note"] = (
            "Hard wall-clock limit reached; only atomically checkpointed results retained."
        )
    atomic_json(path, state)
    print(json.dumps(state, indent=2), flush=True)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
