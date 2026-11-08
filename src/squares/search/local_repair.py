"""Bounded, fixed-angle LP repair for nearly feasible unit-square packings.

Coordinates are centres and angles are radians. Each nearby pair keeps its
current most-separated signed SAT axis: this is a conservative convex subset
of non-overlap, not a continuous packing solver. Returned layouts pass a fresh
float64 SAT and bounding-box check; callers must still use the official metric.
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from scipy.spatial import cKDTree


def _pair_constraints(packing, pairs):
    """Return signed best axes and signed separation (positive is clear)."""
    if not len(pairs):
        return np.empty((0, 2)), np.empty(0)
    i, j = pairs.T
    a, b = packing[i, 2], packing[j, 2]
    axes = np.stack(
        [
            np.stack([np.cos(a), np.sin(a)], axis=-1),
            np.stack([-np.sin(a), np.cos(a)], axis=-1),
            np.stack([np.cos(b), np.sin(b)], axis=-1),
            np.stack([-np.sin(b), np.cos(b)], axis=-1),
        ],
        axis=1,
    )
    projection = np.einsum("pd,pad->pa", packing[j, :2] - packing[i, :2], axes)
    best = np.argmax(np.abs(projection), axis=1)
    selected = projection[np.arange(len(pairs)), best]
    normals = axes[np.arange(len(pairs)), best] * np.where(selected < 0, -1, 1)[:, None]
    # For two unit squares this support radius is the same on all four axes.
    radius = 0.5 * (1 + np.abs(np.cos(a - b)) + np.abs(np.sin(a - b)))
    return normals, np.abs(selected) - radius


def repair_fixed_angles(
    packing: np.ndarray,
    *,
    target_side: float | None = None,
    max_displacement: float = 1e-3,
    clearance: float = 2e-10,
    active_only: bool = True,
    neighbor_layers: int = 1,
    time_limit: float = 2.0,
    max_pairs: int = 50_000,
) -> tuple[np.ndarray | None, dict]:
    """Repair centres inside a fixed box with a sparse minimum-L1-shift LP.

    ``max_displacement`` bounds each centre's Euclidean movement. The linear
    trust box uses +/- max_displacement/sqrt(2) on each coordinate, so all
    potentially new contacts are covered by a 2*max_displacement neighbour
    margin. ``active_only`` moves violating endpoints and their requested
    neighbour layers; False allows every centre to move. Angles never change.

    By default the target is the input's measured bounding side. A caller may
    allow a slightly larger target, but must compare the returned *actual*
    side to its incumbent. Failure proves only failure within these fixed
    separation choices, active set, trust bounds and time budget.

    HiGHS receives the remaining ``time_limit`` after model construction.
    This is not a process-level hard timeout; the caller owns that outer limit.
    """
    started = time.monotonic()
    report = {"method": "fixed_angle_lp", "officially_scored": False}

    def finish(status, result=None):
        report.update(status=status, elapsed_seconds=time.monotonic() - started)
        return result, report

    try:
        p = np.array(packing, dtype=np.float64, copy=True)
    except (TypeError, ValueError):
        return finish("invalid_coordinates")
    if p.ndim != 2 or p.shape[1] != 3 or not 1 <= len(p) <= 1000 or not np.isfinite(p).all():
        return finish("invalid_coordinates")
    if (
        not math.isfinite(max_displacement)
        or max_displacement <= 0
        or not math.isfinite(clearance)
        or clearance <= 0
        or not math.isfinite(time_limit)
        or time_limit <= 0
        or type(neighbor_layers) is not int
        or neighbor_layers < 0
        or type(max_pairs) is not int
        or max_pairs < 1
    ):
        raise ValueError(
            "Repair limits must be positive, with nonnegative integer neighbour layers"
        )
    half = 0.5 * (np.abs(np.cos(p[:, 2])) + np.abs(np.sin(p[:, 2])))
    p[:, :2] -= (p[:, :2] - half[:, None]).min(axis=0)
    raw_side = float(np.max((p[:, :2] + half[:, None]).max(axis=0)))
    box = raw_side if target_side is None else float(target_side)
    if not math.isfinite(box) or box < 1:
        raise ValueError("target_side must be finite and at least one")
    report.update(
        n=len(p),
        raw_L=raw_side,
        target_L=box,
        clearance=clearance,
        max_displacement=max_displacement,
        active_only=active_only,
    )
    # Small positive guard absorbs solver/float arithmetic; final checks below
    # require actual clearance and never accept a negative SAT separation.
    solver_tolerance = 1e-10
    guard = max(64 * np.finfo(float).eps * max(1.0, box), 20 * solver_tolerance * max_displacement)
    margin = 2 * max_displacement + 2 * clearance + guard
    pairs = cKDTree(p[:, :2]).query_pairs(math.sqrt(2) + margin, output_type="ndarray")
    report["neighbor_pairs"] = len(pairs)
    if len(pairs) > max_pairs:
        return finish("pair_budget_exceeded")
    normals, separation = _pair_constraints(p, pairs)
    report["initial_min_separation"] = float(separation.min()) if len(pairs) else None
    bad = separation < clearance
    active = np.zeros(len(p), dtype=bool)
    active[pairs[bad].ravel()] = True
    active |= np.any(p[:, :2] - half[:, None] < 0, axis=1)
    active |= np.any(p[:, :2] + half[:, None] > box, axis=1)
    if not active.any():
        report.update(repaired_L=raw_side, moved_squares=0, max_actual_displacement=0.0)
        return finish("already_clear", p)
    if active_only:
        for _ in range(neighbor_layers):
            touch = active[pairs].any(axis=1)
            active[pairs[touch].ravel()] = True
    else:
        active[:] = True
    ids = np.flatnonzero(active)
    index = np.full(len(p), -1, dtype=int)
    index[ids] = np.arange(len(ids))
    report["active_squares"] = len(ids)
    dimension = 2 * len(ids)
    # Displacements are scaled by max_displacement, making tiny physical
    # corrections well above HiGHS' absolute feasibility tolerance.
    cap = (1 - 1e-8) / math.sqrt(2)
    lower = np.maximum(-cap, (half[ids, None] + guard - p[ids, :2]) / max_displacement)
    upper = np.minimum(cap, (box - half[ids, None] - guard - p[ids, :2]) / max_displacement)
    if np.any(lower > upper):
        return finish("trust_region_cannot_fit_box")
    variable_bounds = list(zip(lower.ravel(), upper.ravel(), strict=True))
    variable_bounds.extend([(0, None)] * dimension)
    row_ids, columns, values, rhs = [], [], [], []
    for (i, j), normal, gap in zip(pairs, normals, separation, strict=True):
        if not (active[i] or active[j]):
            continue
        row = len(rhs)
        for square, sign in ((i, 1), (j, -1)):
            if active[square]:
                for axis in (0, 1):
                    row_ids.append(row)
                    columns.append(2 * index[square] + axis)
                    values.append(sign * normal[axis])
        rhs.append((gap - clearance - guard) / max_displacement)
    for coordinate in range(dimension):
        for sign in (1, -1):
            row_ids.extend([len(rhs), len(rhs)])
            columns.extend([coordinate, dimension + coordinate])
            values.extend([sign, -1])
            rhs.append(0.0)
    matrix = coo_matrix((values, (row_ids, columns)), shape=(len(rhs), 2 * dimension)).tocsr()
    objective = np.r_[np.zeros(dimension), np.ones(dimension)]
    remaining = time_limit - (time.monotonic() - started)
    if remaining <= 0:
        return finish("budget_exhausted_before_solve")
    solve_started = time.monotonic()
    result = linprog(
        objective,
        A_ub=matrix,
        b_ub=np.asarray(rhs),
        bounds=variable_bounds,
        method="highs-ds",
        options={
            "time_limit": remaining,
            "primal_feasibility_tolerance": solver_tolerance,
            "dual_feasibility_tolerance": solver_tolerance,
        },
    )
    report.update(
        solver_status=int(result.status),
        solver_message=str(result.message),
        solve_seconds=time.monotonic() - solve_started,
        lp_variables=2 * dimension,
        lp_constraints=len(rhs),
    )
    if not result.success or result.x is None or not np.isfinite(result.x).all():
        return finish("solver_rejected")
    repaired = p.copy()
    repaired[ids, :2] += max_displacement * result.x[:dimension].reshape(-1, 2)
    moved = np.linalg.norm(repaired[:, :2] - p[:, :2], axis=1)
    lo = (repaired[:, :2] - half[:, None]).min(axis=0)
    hi = (repaired[:, :2] + half[:, None]).max(axis=0)
    actual_side = float(np.max(hi - lo))
    # Rebuild neighbours, independently of which constraints were active.
    check_pairs = cKDTree(repaired[:, :2]).query_pairs(
        math.sqrt(2) + 2 * clearance + guard, output_type="ndarray"
    )
    _, checked = _pair_constraints(repaired, check_pairs)
    report.update(
        repaired_L=actual_side,
        final_min_separation=float(checked.min()) if len(checked) else None,
        max_actual_displacement=float(moved.max()),
        moved_squares=int((moved > 0).sum()),
    )
    if moved.max() > max_displacement or np.any(lo < 0) or np.any(hi > box) or actual_side > box:
        return finish("postcheck_bounds_failed")
    if len(checked) and np.any(checked < clearance):
        return finish("postcheck_clearance_failed")
    return finish("repaired_float64", repaired)
