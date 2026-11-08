"""Prepare bounded CPU geometry candidates for a later GPU relaxation pilot.

No optimization, Kaggle upload, or submission happens here. Inputs retain their
original CSV files; the NPZ is explicitly a float64 search-state representation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd

from squares.search.structure import (
    bands,
    canonical,
    crossovers,
    describe_structure,
    generate_slabs,
    normalize,
    packing_hash,
    packing_signature,
    separations,
    side_length,
    tilt,
)


def load_packings(path: Path) -> dict[int, np.ndarray]:
    frame = pd.read_csv(path, float_precision="round_trip")
    return {
        int(n): normalize(group.sort_values("square_id")[["x", "y", "angle"]].to_numpy(np.float64))
        for n, group in frame.groupby("n", sort=True)
        if len(group) == int(n)
    }


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline",
        type=Path,
        default=Path("outputs/submissions/merged_research_20261107/submission.csv"),
        help="Complete reference CSV; defaults to the verified final submission",
    )
    parser.add_argument("--donor", type=Path, action="append", default=[])
    parser.add_argument(
        "--records",
        type=Path,
        default=Path("data/references/leaderboards/perpuzzle_best_20261029.csv"),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-candidates", type=int, default=96)
    parser.add_argument("--max-parents", type=int, default=32)
    parser.add_argument("--max-parents-per-n", type=int, default=2)
    parser.add_argument("--slab-beam-width", type=int, default=2)
    parser.add_argument("--crossover-children", type=int, default=1)
    parser.add_argument(
        "--baseline-lineage-json",
        type=Path,
        help="Explicit n-to-lineage mapping for known baseline winners; no depth is inferred",
    )
    parser.add_argument(
        "--parent-n",
        type=int,
        action="append",
        default=[],
        help="Restrict parent puzzles to these n values; repeat for a focused chain experiment",
    )
    parser.add_argument("--max-crossover-pairs", type=int, default=20)
    parser.add_argument("--cuts", type=int, default=6)
    parser.add_argument("--max-seconds", type=float, default=240)
    parser.add_argument("--max-dry-excess", type=float, default=0.12)
    parser.add_argument("--seed", type=int, default=20261107)
    parser.add_argument("--near-misses-npz", "--donor-pool-npz", type=Path)
    parser.add_argument("--near-misses-json", "--donor-pool-json", type=Path)
    parser.add_argument(
        "--near-only-parents",
        "--donor-only-parents",
        action="store_true",
        help="Use only the supplied donor pool; baseline stays the comparison reference",
    )
    parser.add_argument(
        "--parent-manifest",
        type=Path,
        help="Resolve lineage for older near-miss outputs lacking chain_depth",
    )
    parser.add_argument("--max-chain-depth", type=int, choices=(1, 2, 3), default=3)
    args = parser.parse_args()
    if (
        any(
            value < 1
            for value in (
                args.max_candidates,
                args.max_parents,
                args.max_parents_per_n,
                args.slab_beam_width,
                args.crossover_children,
                args.cuts,
            )
        )
        or args.max_crossover_pairs < 0
    ):
        parser.error(
            "Candidate/parent/beam/cut limits must be positive; crossover pairs may be zero"
        )
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("--max-seconds must be finite and positive")
    if not math.isfinite(args.max_dry_excess) or args.max_dry_excess < 0:
        parser.error("--max-dry-excess must be finite and nonnegative")
    if bool(args.near_misses_npz) != bool(args.near_misses_json):
        parser.error("--near-misses-npz and --near-misses-json must be provided together")
    if args.near_only_parents and (not args.near_misses_npz or args.donor):
        parser.error(
            "--near-only-parents requires near-miss inputs and cannot be combined with --donor"
        )
    if any(not 1 <= n <= 1000 for n in args.parent_n):
        parser.error("--parent-n must be in 1..1000")
    parent_ns = set(args.parent_n)
    started = time.monotonic()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    baseline = load_packings(args.baseline)
    if set(baseline) != set(range(1, 1001)):
        raise ValueError("The initial baseline must contain every complete n=1..1000")
    baseline_lineage = {}
    if args.baseline_lineage_json:
        supplied = json.loads(args.baseline_lineage_json.read_text())
        if not isinstance(supplied, dict):
            raise ValueError("Baseline lineage must be an explicit n-to-metadata mapping")
        for raw_n, entry in supplied.items():
            n = int(raw_n)
            if str(n) in baseline_lineage or n not in baseline or not isinstance(entry, dict):
                raise ValueError(f"Invalid or duplicate baseline lineage n={raw_n}")
            depth = entry.get("chain_depth")
            if type(depth) is not int or depth < 0:
                raise ValueError(
                    f"Baseline lineage n={n} needs an explicit nonnegative chain_depth"
                )
            baseline_lineage[str(n)] = entry
    lengths = {n: side_length(p) for n, p in baseline.items()}
    record_L = {}
    if args.records.exists():
        frame = pd.read_csv(args.records)
        record_L = {
            int(r.n): float(r.L)
            for r in frame.itertuples()
            if math.isfinite(float(r.L)) and float(r.L) >= math.sqrt(int(r.n)) - 1e-8
        }
    target_gap = {
        n: max(0.0, (lengths[n] - record_L.get(n, lengths[n])) / math.sqrt(n)) for n in lengths
    }
    parents, routes, source_info, seen_states = [], [], [], set()
    if args.near_misses_npz:
        near_info = json.loads(args.near_misses_json.read_text())
        entries = near_info["candidates"] if isinstance(near_info, dict) else near_info
        # When a winner and a warm state coincide numerically, keep the winner's
        # known lineage and score evidence instead of dropping it in input order.
        entries = sorted(
            entries,
            key=lambda entry: (
                not (
                    entry.get("donor_kind") == "winner"
                    or entry.get("not_officially_scored") is False
                )
            ),
        )
        ancestry_index = {}
        if args.parent_manifest:
            previous = json.loads(args.parent_manifest.read_text())
            if previous.get("baseline", {}).get("sha256") != file_hash(args.baseline):
                raise ValueError("Parent manifest belongs to a different baseline")
            ancestry_index = {entry["key"]: entry for entry in previous["candidates"]}
        digest = file_hash(args.near_misses_npz)
        source_info.append(
            {
                "path": str(args.near_misses_npz),
                "sha256": digest,
                "metadata": str(args.near_misses_json),
                "metadata_sha256": file_hash(args.near_misses_json),
                "kind": "relaxed_donor_pool",
            }
        )
        with np.load(args.near_misses_npz, allow_pickle=False) as archive:
            for entry in entries:
                key, n = entry["key"], int(entry["n"])
                if parent_ns and n not in parent_ns:
                    continue
                packing = np.asarray(archive[key], dtype=np.float64)
                if packing.shape != (n, 3) or not np.isfinite(packing).all() or n not in lengths:
                    raise ValueError(f"Malformed near-miss state {key}")
                source_array_hash = hashlib.sha256(
                    np.ascontiguousarray(packing, dtype="<f8").tobytes()
                ).hexdigest()
                if entry.get("array_sha256") and source_array_hash != entry["array_sha256"]:
                    raise ValueError(f"Donor array hash mismatch: {key}")
                previous = ancestry_index.get(entry.get("parent_candidate"), {})
                depth = entry.get("chain_depth", previous.get("parameters", {}).get("chain_depth"))
                if depth is None:
                    raise ValueError(f"Missing chain depth for {key}; supply --parent-manifest")
                if type(depth) is not int or not 0 <= depth <= 3:
                    raise ValueError(f"Invalid chain depth {depth!r} for {key}")
                packing = normalize(packing)
                signature = packing_signature(packing)
                if signature in seen_states:
                    continue
                seen_states.add(signature)
                desc = describe_structure(packing)
                routes.append(
                    {
                        "source": str(args.near_misses_npz),
                        "key": key,
                        "chain_depth": depth,
                        "record_gap_score": target_gap[n],
                        **desc,
                    }
                )
                if not desc["two_band_eligible"]:
                    continue
                operator = entry.get("parent_operator", previous.get("operator"))
                parents.append(
                    {
                        "packing": packing,
                        "description": desc,
                        "gap": target_gap[n],
                        "warm": True,
                        "meta": {
                            "source": str(args.near_misses_npz),
                            "sha256": digest,
                            "key": key,
                            "n": n,
                            "chain_depth": depth,
                            "state_sha256": packing_hash(packing),
                            "source_array_sha256": source_array_hash,
                            "source_reported_state_sha256": entry.get("state_sha256"),
                            "geometry_signature": signature,
                            "parent_candidate": entry.get("parent_candidate"),
                            "parent_operator": operator,
                            "ancestry": entry.get("ancestry", previous.get("parents", [])),
                            "not_officially_scored": bool(entry.get("not_officially_scored", True)),
                            "donor_kind": entry.get("donor_kind", "near_miss"),
                            "scores": entry.get("scores"),
                        },
                    }
                )
    paths = [] if args.near_only_parents else list(dict.fromkeys([args.baseline, *args.donor]))
    for path in paths:
        digest = file_hash(path)
        source_info.append({"path": str(path), "sha256": digest})
        packs = baseline if path == args.baseline else load_packings(path)
        for n, packing in packs.items():
            if parent_ns and n not in parent_ns:
                continue
            if n < 300:
                continue
            state_hash = packing_hash(packing)
            signature = packing_signature(packing)
            if signature in seen_states:
                continue
            seen_states.add(signature)
            desc = describe_structure(packing)
            route = {"source": str(path), "n": n, "record_gap_score": target_gap.get(n, 0), **desc}
            routes.append(route)
            if desc["two_band_eligible"]:
                lineage = baseline_lineage.get(str(n), {}) if path == args.baseline else {}
                parents.append(
                    {
                        "packing": packing,
                        "meta": {
                            "source": str(path),
                            "sha256": digest,
                            "n": n,
                            "chain_depth": lineage.get("chain_depth", 0),
                            "parent_operator": lineage.get(
                                "parent_operator", lineage.get("operator")
                            ),
                            "ancestry": lineage.get("parents", lineage.get("ancestry", [])),
                            "baseline_lineage": lineage or None,
                            "state_sha256": state_hash,
                            "geometry_signature": signature,
                        },
                        "description": desc,
                        "gap": target_gap.get(n, 0),
                        "warm": False,
                    }
                )
    # A per-n cap avoids a large family consuming the complete parent budget.
    parents.sort(key=lambda p: (not p.get("warm", False), -p["gap"], p["description"]["L"]))
    chosen, per_n = [], {}
    for parent in parents:
        n = parent["meta"]["n"]
        if per_n.get(n, 0) >= args.max_parents_per_n:
            continue
        chosen.append(parent)
        per_n[n] = per_n.get(n, 0) + 1
        if len(chosen) >= args.max_parents:
            break

    candidates, seen_children = [], set()
    rng = np.random.default_rng(args.seed)

    def add(packing, operator, parent_list, parameters):
        n = len(packing)
        if n not in lengths:
            return
        packing = normalize(packing)
        digest = packing_hash(packing)
        # Slab orders can produce exactly the same geometry in a different row
        # order. Keep the original state digest for provenance, but deduplicate
        # children much more tightly than the coarse parent-diversity heuristic.
        signature = packing_signature(packing, decimals=12)
        if signature in seen_children:
            return
        dry_L = side_length(packing)
        excess = dry_L - lengths[n]
        if excess > args.max_dry_excess:
            return
        _, sep = separations(packing)
        overlaps = int((sep < -1e-9).sum())
        worst = float(sep.min()) if len(sep) else 0.0
        if worst < -0.05:
            return
        parent_depths = [p["meta"].get("chain_depth", 0) for p in parent_list]
        child_depth = max(parent_depths, default=0) + int(operator.startswith("slab_"))
        if child_depth > args.max_chain_depth:
            return
        seen_children.add(signature)
        candidates.append(
            (
                packing,
                {
                    "n": n,
                    "operator": operator,
                    "parents": [p["meta"] for p in parent_list],
                    "dry_L": dry_L,
                    "baseline_L": lengths[n],
                    "dry_excess_L": excess,
                    "dry_overlap_pairs": overlaps,
                    "min_separation": worst,
                    "target_record_gap_score": target_gap.get(n, 0),
                    "state_sha256": digest,
                    "array_sha256": hashlib.sha256(
                        np.ascontiguousarray(packing, dtype="<f8").tobytes()
                    ).hexdigest(),
                    "geometry_signature": signature,
                    "parameters": {
                        **parameters,
                        "chain_depth": child_depth,
                        "parent_chain_depths": parent_depths,
                    },
                    "nonce": int(rng.integers(0, 2**31)),
                },
            )
        )

    for i, parent in enumerate(chosen):
        if time.monotonic() - started > args.max_seconds:
            break
        if parent["meta"].get("chain_depth", 0) >= args.max_chain_depth:
            continue
        previous_operator = parent["meta"].get("parent_operator", "") or ""
        directions = (
            (previous_operator.removeprefix("slab_"),)
            if parent.get("warm") and previous_operator in ("slab_up", "slab_down")
            else ("up", "down")
        )
        for child, parameters in generate_slabs(
            parent["packing"],
            tries=args.cuts,
            beam_width=args.slab_beam_width,
            directions=directions,
        ):
            add(child, "slab_" + parameters["direction"], [parent], parameters)
        print(
            json.dumps(
                {
                    "stage": "slabs",
                    "parent": i + 1,
                    "n": parent["meta"]["n"],
                    "candidates": len(candidates),
                },
                separators=(",", ":"),
            ),
            flush=True,
        )

    cross_jobs = []
    canonical_parents = [p for p in chosen if p["description"]["canonical_eligible"]]
    for i, a in enumerate(canonical_parents):
        aa = canonical(a["packing"])
        ath = {axis: float(np.abs(tilt(aa)[mask]).mean()) for mask, axis, _ in bands(aa)}
        for b in canonical_parents[i + 1 :]:
            if abs(a["description"]["L"] - b["description"]["L"]) > 0.3:
                continue
            bb = canonical(b["packing"])
            bth = {axis: float(np.abs(tilt(bb)[mask]).mean()) for mask, axis, _ in bands(bb)}
            for axis in (0, 1):
                if abs(ath[axis] - bth[axis]) <= 1:
                    cross_jobs.extend([(a, b, axis), (b, a, axis)])
    cross_jobs.sort(key=lambda job: -(job[0]["gap"] + job[1]["gap"]))
    for i, (a, b, axis) in enumerate(cross_jobs[: args.max_crossover_pairs]):
        if time.monotonic() - started > args.max_seconds:
            break
        for child in crossovers(
            a["packing"],
            b["packing"],
            axis,
            lengths,
            tries=max(3, args.cuts // 2),
            max_children=args.crossover_children,
        ):
            add(child[0], "crossover", [a, b], child[1])
        print(
            json.dumps(
                {"stage": "crossover", "pair": i + 1, "candidates": len(candidates)},
                separators=(",", ":"),
            ),
            flush=True,
        )

    # Round-robin n/operator prevents a single family or transform filling the pilot.
    buckets = {}
    for item in sorted(
        candidates, key=lambda item: (item[1]["dry_excess_L"], -item[1]["target_record_gap_score"])
    ):
        meta = item[1]
        buckets.setdefault((meta["n"], meta["operator"]), []).append(item)
    ordering = sorted(
        buckets, key=lambda key: (-target_gap.get(key[0], 0), buckets[key][0][1]["dry_excess_L"])
    )
    selected = []
    while len(selected) < args.max_candidates and any(buckets.values()):
        for key in ordering:
            if buckets[key]:
                selected.append(buckets[key].pop(0))
            if len(selected) >= args.max_candidates:
                break
    arrays, metadata = {}, []
    for i, (packing, meta) in enumerate(selected):
        key = f"candidate_{i:06d}"
        arrays[key] = np.ascontiguousarray(packing, np.float64)
        metadata.append({"id": key, "key": key, **meta})
    np.savez_compressed(out / "candidates.npz", **arrays)
    manifest = {
        "schema_version": 1,
        "angles": "radians",
        "seed": args.seed,
        "baseline": {
            "path": str(args.baseline),
            "sha256": file_hash(args.baseline),
            "score_estimate": sum(lengths[n] / math.sqrt(n) - 1 for n in lengths),
        },
        "baseline_lengths": {str(n): L for n, L in lengths.items()},
        "sources": source_info,
        "candidate_archive": "candidates.npz",
        "parent_deduplication": (
            "normalized centers, square-periodic angles, row-order independent, "
            "rounded to 1e-6; heuristic only"
        ),
        "child_deduplication": (
            "normalized centers, square-periodic angles, row-order independent, "
            "rounded to 1e-12; original full-precision state retained"
        ),
        "candidates": metadata,
        "eligible_parents": len(parents),
        "selected_parents": len(chosen),
        "selected_parent_counts": {str(n): count for n, count in sorted(per_n.items())},
        "max_parents_per_n": args.max_parents_per_n,
        "slab_beam_width": args.slab_beam_width,
        "crossover_children": args.crossover_children,
        "generated_candidates": len(candidates),
        "preparation_seconds": time.monotonic() - started,
        "max_chain_depth": args.max_chain_depth,
        "parent_n_filter": sorted(parent_ns),
        "near_miss_input": str(args.near_misses_npz) if args.near_misses_npz else None,
        "near_only_parents": args.near_only_parents,
        "baseline_lineage": baseline_lineage,
        "baseline_lineage_source": (
            {
                "path": str(args.baseline_lineage_json),
                "sha256": file_hash(args.baseline_lineage_json),
            }
            if args.baseline_lineage_json
            else None
        ),
        "target_gap_reference": str(args.records),
        "target_gap_note": "Dated record gaps guide selection; they are not predicted gains.",
        "geometry_note": (
            "Dry geometry may overlap. These are search inputs, not valid submissions."
        ),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (out / "structure_routes.json").write_text(json.dumps(routes, indent=2) + "\n")
    print(
        json.dumps(
            {
                "output": str(out),
                "selected_candidates": len(selected),
                "operators": {
                    op: sum(c["operator"] == op for c in metadata)
                    for op in sorted({c["operator"] for c in metadata})
                },
                "actual_n": sorted({c["n"] for c in metadata}),
                "preparation_seconds": manifest["preparation_seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
