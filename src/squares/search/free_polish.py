"""Free-angle sequential sparse-LP contact polish (CPU-only).

Adapted from the public Living Atlas notebook
(malyshevdanil/squares-in-squares-living-atlas-of-tight-packings,
``search/contact_polish.py``, itself marked "Adapted from lightningv08,
Apache-2.0"). The vectorized trust-region LP builder, kink handling and
exact nonlinear SAT admission are the upstream ideas; the surrounding
plumbing (packing I/O, official scoring, merge) stays this repo's own.

Kept verbatim: ``search_geometry.py`` GAP/normalize/repair semantics are
reused through :mod:`squares.search.structure` equivalents.
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from scipy.spatial import cKDTree

from .structure import normalize, side_length


def _repair(p: np.ndarray, clearance: float = 4e-11) -> np.ndarray | None:
    """Uniform dilation repair mirroring the public ``repair`` semantics."""
    from .gpu_relax import repair_with_diagnostics

    out, _ = repair_with_diagnostics(p, clearance=clearance, max_factor=1.003)
    return out


def polish(
    p: np.ndarray,
    rounds: int = 28,
    seed: int = 0,
    max_seconds: float = 15.0,
) -> tuple[np.ndarray, list[dict], float]:
    """Trust-region sequential LP over free centers/angles.

    Returns ``(best_packing, trace, seconds)``. Each LP step optimizes
    ``3n`` displacements plus the box side with sparse SAT constraints and
    admits the trial only through exact nonlinear SAT ``repair`` with a
    strictly smaller side. Callers must still run the official metric.
    """
    p = normalize(np.asarray(p, dtype=np.float64))
    n = len(p)
    rng = np.random.default_rng(seed)
    started = time.perf_counter()
    step = 0.025
    trace: list[dict] = []
    acc: dict[str, object] = {"rows": [], "cols": [], "vals": [], "bounds": [], "offset": 0}

    def add(cc: np.ndarray, vv: np.ndarray, bb: np.ndarray) -> None:
        bb = np.asarray(bb)
        count = len(bb)
        rows = acc["rows"]
        assert isinstance(rows, list)
        rows.append(np.repeat(np.arange(acc["offset"], acc["offset"] + count), cc.shape[1]))
        assert isinstance(acc["cols"], list)
        acc["cols"].append(cc.ravel())
        assert isinstance(acc["vals"], list)
        acc["vals"].append(vv.ravel())
        assert isinstance(acc["bounds"], list)
        acc["bounds"].append(bb)
        acc["offset"] = acc["offset"] + count

    for _ in range(rounds):
        if time.perf_counter() - started > max_seconds:
            break
        L = side_length(p)
        theta = p[:, 2]
        c, s = np.cos(theta), np.sin(theta)
        h = (np.abs(c) + np.abs(s)) / 2
        edges = cKDTree(p[:, :2]).query_pairs(1.75, output_type="ndarray")
        if not len(edges):
            break
        i, j = edges.T
        d = p[j, :2] - p[i, :2]
        ux = np.column_stack((c[i], -s[i], c[j], -s[j]))
        uy = np.column_stack((s[i], c[i], s[j], c[j]))
        proj = d[:, 0, None] * ux + d[:, 1, None] * uy
        ranks = np.abs(proj)
        ranks = ranks + rng.uniform(-2e-12, 2e-12, ranks.shape)
        chosen = ranks.argmax(1)
        rr = np.arange(len(i))
        sign = np.sign(proj[rr, chosen])
        vx = sign * ux[rr, chosen]
        vy = sign * uy[rr, chosen]
        rotation = -d[:, 0] * vy + d[:, 1] * vx
        delta = theta[j] - theta[i]
        cd, sd = np.cos(delta), np.sin(delta)
        rad = (1 + np.abs(cd) + np.abs(sd)) / 2
        dr = (-sd * np.sign(cd) + cd * np.sign(sd)) / 2
        dist = np.abs(proj[rr, chosen])
        own = chosen < 2
        columns = np.column_stack((3 * i, 3 * i + 1, 3 * j, 3 * j + 1, 3 * i + 2, 3 * j + 2))
        values = np.column_stack(
            (vx, vy, -vx, -vy, -dr - np.where(own, rotation, 0), dr - np.where(own, 0, rotation))
        )
        for _key in ("rows", "cols", "vals", "bounds"):
            acc[_key] = []  # type: ignore[literal-required]
        acc["offset"] = 0
        add(columns, values, dist - rad - 4e-11)
        kink = np.flatnonzero(np.minimum(np.abs(cd), np.abs(sd)) < 1e-8)
        for slope in (-0.5, 0.5):
            vv = values[kink].copy()
            vv[:, 4] = -slope - np.where(own[kink], rotation[kink], 0)
            vv[:, 5] = slope - np.where(own[kink], 0, rotation[kink])
            add(columns[kink], vv, dist[kink] - rad[kink] - 4e-11)
        k = np.arange(n)
        dh = (-s * np.sign(c) + c * np.sign(s)) / 2
        aligned = np.minimum(np.abs(c), np.abs(s)) < 1e-8
        for dim in (0, 1):
            for upper in (False, True):
                ids = k
                extra = k[aligned]
                for ids_, deriv in (
                    (ids, dh),
                    (extra, np.full(len(extra), -0.5)),
                    (extra, np.full(len(extra), 0.5)),
                ):
                    cc = np.column_stack((3 * ids_ + dim, 3 * ids_ + 2, np.full(len(ids_), 3 * n)))
                    vv = np.column_stack(
                        (
                            np.full(len(ids_), 1.0 if upper else -1.0),
                            deriv,
                            np.full(len(ids_), -1.0 if upper else 0.0),
                        )
                    )
                    bb = L - p[ids_, dim] - h[ids_] if upper else p[ids_, dim] - h[ids_]
                    add(cc, vv, bb)
        kk = np.arange(3 * n)
        uu = 3 * n + 1 + kk
        for sgn in (-1.0, 1.0):
            add(np.column_stack((kk, uu)), np.tile([sgn, -1.0], (3 * n, 1)), np.zeros(3 * n))
        mat = coo_matrix(
            (
                np.concatenate(acc["vals"]),  # type: ignore[arg-type]
                (np.concatenate(acc["rows"]), np.concatenate(acc["cols"])),  # type: ignore[arg-type]
            ),
            shape=(acc["offset"], 6 * n + 1),  # type: ignore[arg-type]
        ).tocsr()
        rhs = np.concatenate(acc["bounds"])  # type: ignore[arg-type]
        objective = np.zeros(6 * n + 1)
        objective[3 * n] = 1
        objective[3 * n + 1 :] = 2e-6
        trust = np.tile([step, step, step * 0.4], n)
        limits = list(zip(-trust, trust, strict=True)) + [(-step, step)] + [(0, None)] * (3 * n)
        fit = linprog(
            objective,
            A_ub=mat,
            b_ub=rhs,
            bounds=limits,
            method="highs",
            options={
                "primal_feasibility_tolerance": 1e-10,
                "dual_feasibility_tolerance": 1e-9,
                "time_limit": 2,
            },
        )
        if not fit.success:
            step *= 0.4
            if step < 2e-7:
                break
            continue
        move = fit.x[: 3 * n].reshape(n, 3)
        winner = None
        for alpha in (1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125):
            trial = _repair(p + alpha * move)
            if (
                trial is not None
                and side_length(trial) < L - 2e-10
                and (winner is None or side_length(trial) < side_length(winner))
            ):
                winner = trial
        if winner is None:
            step *= 0.4
            if step < 2e-7:
                break
        else:
            p = winner
            trace.append({"before": L, "after": side_length(p), "trust": step})
            step = min(0.06, step * 1.3)
    return p, trace, time.perf_counter() - started


def polish_packing(
    packing: np.ndarray,
    *,
    target_n: int | None = None,
    rounds: int = 28,
    seed: int = 0,
    max_seconds: float = 60.0,
) -> tuple[np.ndarray | None, dict]:
    """Polish one packing; return ``(best, report)`` with strict improvement."""
    base = normalize(np.asarray(packing, dtype=np.float64))
    if target_n is not None and len(base) != target_n:
        raise ValueError("packing n does not match target_n")
    before = side_length(base)
    best, trace, seconds = polish(base, rounds=rounds, seed=seed, max_seconds=max_seconds)
    after = side_length(best)
    gain = before / math.sqrt(len(base)) - after / math.sqrt(len(base))
    report = {
        "n": len(base),
        "before_L": before,
        "after_L": after,
        "gain": gain,
        "improved": bool(after < before - 1e-9),
        "iterations": len(trace),
        "seconds": seconds,
    }
    return (best if report["improved"] else None, report)
