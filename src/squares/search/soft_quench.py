"""Soft-contact quench with epsilon hardening (fq/soft MVE, CPU-only).

New loss, never tested in this repo: minimize
``E = S_soft(P) + w * sum(softplus(-sep / eps))`` over free centres and
angles with L-BFGS-B, then harden ``eps`` through a schedule and re-admit
through exact nonlinear SAT repair. ``S_soft`` is a smooth max of the
bounding-box extents; the penalty gradient fixes each pair's argmax SAT
axis (straight-through approximation, line-searched on the true energy).

Callers must still run the official metric; only dual-path wins count.
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.optimize import minimize
from scipy.spatial import cKDTree

from .structure import CONTACT_RADIUS, corners, normalize, side_length

_CLEARANCE = 2e-10


def _smin(z: np.ndarray, tau: float, axis: int = -1) -> tuple[np.ndarray, np.ndarray]:
    """Smooth min value (squeezed) with softmax weights (full shape)."""
    m = z.min(axis=axis, keepdims=True)
    e = np.exp(np.clip(-(z - m) * tau, -50, 50))
    s = e.sum(axis=axis, keepdims=True)
    return (m - np.log(s) / tau).squeeze(axis), (e / s)


def _smax(z: np.ndarray, tau: float, axis: int = -1) -> tuple[np.ndarray, np.ndarray]:
    m = z.max(axis=axis, keepdims=True)
    e = np.exp(np.clip((z - m) * tau, -50, 50))
    s = e.sum(axis=axis, keepdims=True)
    return (m + np.log(s) / tau).squeeze(axis), (e / s)


def _soft_side(p: np.ndarray, temp: float = 50.0) -> tuple[float, np.ndarray, np.ndarray]:
    """Fully smooth bounding-box side and its exact gradient."""
    n = len(p)
    C = corners(p)
    x, y = p[:, 0], p[:, 1]
    gx = np.zeros((n, 2))
    ga = np.zeros(n)
    ext = np.zeros(2)
    dext_dcenter = np.zeros((2, n, 2))
    dext_dangle = np.zeros((2, n))
    for dim in (0, 1):
        proj = C[:, :, dim]
        cmin, wmin_c = _smin(proj, temp, axis=1)
        cmax, wmax_c = _smax(proj, temp, axis=1)
        gmin, wmin_s = _smin(cmin, temp, axis=0)
        gmax, wmax_s = _smax(cmax, temp, axis=0)
        ext[dim] = gmax - gmin
        dext_dcenter[dim, :, dim] = wmax_s * 1.0 + wmin_s * -1.0
        rot = np.stack(
            [-(C[:, c, 1] - y) if dim == 0 else (C[:, c, 0] - x) for c in range(4)],
            axis=1,
        )
        dext_dangle[dim] = (wmax_s[:, None] * (wmax_c * rot)).sum(axis=1) - (
            wmin_s[:, None] * (wmin_c * rot)
        ).sum(axis=1)
    side, wdim = _smax(ext, temp, axis=0)
    for dim in (0, 1):
        gx += wdim[dim] * dext_dcenter[dim]
        ga += wdim[dim] * dext_dangle[dim]
    return float(side), gx, ga


def _pair_cache(p: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Candidate pairs, argmax SAT axis normals (m,2) and gaps (m,)."""
    tree = cKDTree(p[:, :2])
    pairs = tree.query_pairs(CONTACT_RADIUS + 1e-6, output_type="ndarray")
    if not len(pairs):
        return pairs, np.empty((0, 2)), np.empty(0)
    C = corners(p)
    i, j = pairs[:, 0], pairs[:, 1]
    ai, aj = p[i, 2], p[j, 2]
    axes = np.stack(
        [
            np.stack([np.cos(ai), np.sin(ai)], -1),
            np.stack([-np.sin(ai), np.cos(ai)], -1),
            np.stack([np.cos(aj), np.sin(aj)], -1),
            np.stack([-np.sin(aj), np.cos(aj)], -1),
        ],
        axis=1,
    )
    pi = np.einsum("mad,mcd->mac", axes, C[i])
    pj = np.einsum("mad,mcd->mac", axes, C[j])
    gap = np.maximum(pj.min(-1) - pi.max(-1), pi.min(-1) - pj.max(-1))
    k = gap.argmax(axis=1)
    return pairs, axes[np.arange(len(pairs)), k], gap[np.arange(len(pairs)), k]


def _energy_grad(
    v: np.ndarray, n: int, weight: float, eps: float, temp: float = 50.0, tau: float = 200.0
) -> tuple[float, np.ndarray]:
    p = v.reshape(n, 3)
    side, gx, ga = _soft_side(p, temp)
    energy = side
    g = np.zeros((n, 2))
    ga_pair = np.zeros(n)
    pairs, normals, gaps = _pair_cache(p)
    if len(pairs):
        # Energy uses the exact SAT gap (unbiased): hinge-squared penalty is
        # exactly zero for satisfied contacts. Softmax weights are used only
        # for averaging supporter gradients across ties.
        h = np.clip((_CLEARANCE - gaps) / eps, 0.0, None)
        energy += weight * float((h * h).sum())
        dE_dgap = -2.0 * weight * h / eps
        i, j = pairs[:, 0], pairs[:, 1]
        C = corners(p)
        x, y = p[:, 0], p[:, 1]
        ci = C[i]
        cj = C[j]
        proj_i = (ci * normals[:, None, :]).sum(-1)
        proj_j = (cj * normals[:, None, :]).sum(-1)
        # center part: gap grows when j moves +n and i moves -n.
        nz = dE_dgap != 0.0
        if nz.any():
            nn = normals[nz]
            dd = dE_dgap[nz]
            np.add.at(g, i[nz], -dd[:, None] * nn)
            np.add.at(g, j[nz], dd[:, None] * nn)
            # angle part: hard side choice, softmax-averaged supporters.
            act = np.flatnonzero(nz)
            pi_a = proj_i[act]
            pj_a = proj_j[act]
            side_a = pj_a.min(axis=1) - pi_a.max(axis=1)
            side_b = pi_a.min(axis=1) - pj_a.max(axis=1)
            use_a = side_a >= side_b
            tie = np.abs(side_a - side_b) <= 1e-12
            for t, idx in enumerate(act.tolist()):
                ii, jj = int(i[idx]), int(j[idx])
                nx, ny = normals[idx]
                d_i = -(C[ii, :, 1] - y[ii]) * nx + (C[ii, :, 0] - x[ii]) * ny
                d_j = -(C[jj, :, 1] - y[jj]) * nx + (C[jj, :, 0] - x[jj]) * ny
                if tie[t]:
                    wa = wb = 0.5
                elif use_a[t]:
                    wa, wb = 1.0, 0.0
                else:
                    wa, wb = 0.0, 1.0
                wi_max = np.exp(np.clip((pi_a[t] - pi_a[t].max()) * tau, -50, 0))
                wi_max /= wi_max.sum()
                wj_min = np.exp(np.clip(-(pj_a[t] - pj_a[t].min()) * tau, -50, 0))
                wj_min /= wj_min.sum()
                wi_min = np.exp(np.clip(-(pi_a[t] - pi_a[t].min()) * tau, -50, 0))
                wi_min /= wi_min.sum()
                wj_max = np.exp(np.clip((pj_a[t] - pj_a[t].max()) * tau, -50, 0))
                wj_max /= wj_max.sum()
                ga_pair[ii] += dE_dgap[idx] * (
                    wb * float((wi_min * d_i).sum()) - wa * float((wi_max * d_i).sum())
                )
                ga_pair[jj] += dE_dgap[idx] * (
                    wa * float((wj_min * d_j).sum()) - wb * float((wj_max * d_j).sum())
                )
        grad = np.concatenate([(gx + g).ravel(), ga + ga_pair])
    else:
        grad = np.concatenate([gx.ravel(), ga])
    return energy, grad


def descend(
    packing: np.ndarray,
    *,
    weight: float = 1.0,
    eps: float = 3e-3,
    iters: int = 40,
    step0: float = 3e-4,
    max_seconds: float = 120.0,
) -> tuple[np.ndarray, dict]:
    """Damped gradient descent with Armijo backtracking on the true energy.

    L-BFGS-B's Wolfe search aborts on SAT axis/neighbor switches; this loop
    only needs a descent direction and validates every trial on the exact
    energy, so kinks merely shrink the step.
    """
    p = normalize(np.asarray(packing, dtype=np.float64))
    n = len(p)
    x = p.ravel().copy()
    e, g = _energy_grad(x, n, weight, eps)
    started = time.perf_counter()
    trace = []
    step = step0
    for it in range(iters):
        if time.perf_counter() - started > max_seconds:
            break
        norm = float(np.abs(g).max())
        if not math.isfinite(norm) or norm == 0:
            break
        d = -g / norm
        scale = max(1, n)
        accepted = False
        for _ in range(24):
            t = step
            e2, _ = _energy_grad(x + t * d, n, weight, eps)
            if e2 < e - 1e-4 * t * norm / scale:
                x = x + t * d
                e = e2
                step = min(1e-2, step * 1.5)
                accepted = True
                break
            step *= 0.5
            if step < 1e-7:
                break
        e, g = _energy_grad(x, n, weight, eps)
        trace.append({"it": it, "fun": e / scale, "step": step, "accepted": accepted})
        if not accepted:
            break
    best = normalize(x.reshape(n, 3))
    return best, {
        "fun": e / max(1, n),
        "side": side_length(best),
        "trace": trace,
        "seconds": time.perf_counter() - started,
    }


def soft_quench(
    packing: np.ndarray,
    *,
    eps_schedule: tuple[float, ...] = (3e-3, 1e-3, 3e-4, 1e-4),
    weight: float = 1.0,
    max_iter_per_stage: int = 60,
    max_seconds: float = 300.0,
    seed: int = 0,
    jitter: float = 1e-4,
) -> tuple[np.ndarray, dict]:
    """Minimize the soft-contact energy through an epsilon hardening schedule.

    Intended for dry (slightly infeasible) candidates: the penalty drives
    overlaps out while the smooth side term compresses. Only symmetry
    breaking noise is added; dry inputs are already outside feasibility and
    larger kicks would destroy their structure. Energy/gradient are scaled
    by 1/n for L-BFGS conditioning.
    """
    rng = np.random.default_rng(seed)
    base = normalize(np.asarray(packing, dtype=np.float64))
    n = len(base)
    before = side_length(base)
    start = base.copy()
    start[:, 2] += rng.uniform(-jitter, jitter, n)
    start[:, :2] += rng.uniform(-jitter, jitter, (n, 2))
    x0 = normalize(start).ravel()
    started = time.perf_counter()
    trace = []
    best = normalize(base.copy())
    best_side = before
    scale = max(1, n)
    for eps in eps_schedule:
        if time.perf_counter() - started > max_seconds:
            break

        def _f(v: np.ndarray, _e: float = eps) -> tuple[float, np.ndarray]:
            e, gr = _energy_grad(v, n, weight, _e)
            return e / scale, gr / scale

        res = minimize(
            _f,
            x0,
            jac=True,
            method="L-BFGS-B",
            options={"maxiter": max_iter_per_stage, "ftol": 1e-9, "gtol": 1e-7},
        )
        cand = normalize(res.x.reshape(n, 3))
        s = side_length(cand)
        trace.append({"eps": eps, "fun": float(res.fun) * scale, "side": s, "nit": int(res.nit)})
        x0 = res.x
        if s < best_side:
            best, best_side = cand, s
    return best, {
        "n": n,
        "before_L": before,
        "after_L": best_side,
        "gain": before / math.sqrt(n) - best_side / math.sqrt(n),
        "improved": bool(best_side < before - 1e-9),
        "trace": trace,
        "seconds": time.perf_counter() - started,
    }
