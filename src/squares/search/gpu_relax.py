"""Minimal CuPy wrapper for lightningv08's public FP64 packing L-BFGS kernel.

The CUDA kernel is retained unchanged in third_party/cuda_packing. This module
does not import or execute the upstream notebook's experiment pipeline.
Angles are radians, coordinates denote centres, and the squares have side one.
"""

from __future__ import annotations

import math
import time
from pathlib import Path

import numpy as np


def bounds(packing: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    p = np.asarray(packing, dtype=np.float64)
    half = 0.5 * (np.abs(np.cos(p[:, 2])) + np.abs(np.sin(p[:, 2])))
    return (p[:, :2] - half[:, None]).min(0), (p[:, :2] + half[:, None]).max(0)


def side(packing: np.ndarray) -> float:
    lo, hi = bounds(packing)
    return float(np.max(hi - lo))


def normalize(packing: np.ndarray) -> np.ndarray:
    p = np.asarray(packing, dtype=np.float64).copy()
    p[:, :2] -= bounds(p)[0]
    return p


def compress_centres(packing: np.ndarray, target_side: float) -> np.ndarray:
    """Compress centres only: unit-square size is never changed."""
    p = normalize(packing)
    original = side(p)
    if original > 1.00000001:
        p[:, :2] = 0.5 + (p[:, :2] - 0.5) * ((target_side - 1) / (original - 1))
    return p


def repair_with_diagnostics(
    packing: np.ndarray, *, clearance: float = 2e-10, max_factor: float = 1.00005
) -> tuple[np.ndarray | None, dict]:
    """Measure the SAT residual and conservatively repair it by centre dilation.

    The scale needed to remove the worst local overlap can erase a small box
    improvement. Report that cost even when the repair is rejected.
    """
    from scipy.spatial import cKDTree

    p = np.asarray(packing, dtype=np.float64)
    if p.ndim != 2 or p.shape[1] != 3 or not len(p) or not np.isfinite(p).all():
        return None, {"repair_status": "invalid_coordinates"}
    p = normalize(p)
    raw_side = side(p)
    pairs = cKDTree(p[:, :2]).query_pairs(math.sqrt(2) + 1e-6, output_type="ndarray")
    factor, penetration = 1.0, 0.0
    if len(pairs):
        i, j = pairs.T
        delta = p[j, :2] - p[i, :2]
        a, b = p[i, 2], p[j, 2]
        projections = np.maximum.reduce(
            [
                np.abs(delta[:, 0] * np.cos(a) + delta[:, 1] * np.sin(a)),
                np.abs(-delta[:, 0] * np.sin(a) + delta[:, 1] * np.cos(a)),
                np.abs(delta[:, 0] * np.cos(b) + delta[:, 1] * np.sin(b)),
                np.abs(-delta[:, 0] * np.sin(b) + delta[:, 1] * np.cos(b)),
            ]
        )
        radius = 0.5 * (1 + np.abs(np.cos(a - b)) + np.abs(np.sin(a - b)))
        factor = max(1.0, float(np.max((radius + clearance) / np.maximum(projections, 1e-30))))
        penetration = max(0.0, float(np.max(radius - projections)))
    report = {
        "raw_L": raw_side,
        "max_pair_penetration": penetration,
        "required_dilation": factor,
        "neighbor_pairs": len(pairs),
        "repair_status": "scale_limit" if factor > max_factor else "repaired",
        "repaired_L": None,
    }
    if factor > max_factor:
        return None, report
    p[:, :2] *= factor
    p = normalize(p)
    report["repaired_L"] = side(p)
    return p, report


def repair_small_overlaps(
    packing: np.ndarray, *, clearance: float = 2e-10, max_factor: float = 1.00005
) -> np.ndarray | None:
    """Uniform centre dilation for tiny SAT penetrations, not score certification."""
    return repair_with_diagnostics(packing, clearance=clearance, max_factor=max_factor)[0]


class CudaRelaxer:
    """One CUDA block per trajectory; batches contain only one value of n."""

    def __init__(self, device: int = 0, kernel_path: str | Path | None = None):
        import cupy as cp

        self.cp = cp
        self.device = cp.cuda.Device(device)
        self.device.use()
        if kernel_path is None:
            kernel_path = (
                Path(__file__).resolve().parents[3]
                / "third_party/cuda_packing/gpu_topology_kernel.cu"
            )
        self.kernel_path = Path(kernel_path)
        self.module = cp.RawModule(
            code=self.kernel_path.read_text(),
            options=("--std=c++17",),
            name_expressions=["eval", "lbfgs"],
        )
        self.function = self.module.get_function("lbfgs")
        self.evaluate = self.module.get_function("eval")
        properties = cp.cuda.runtime.getDeviceProperties(device)
        name = properties["name"]
        self.info = {
            "device_index": device,
            "name": name.decode() if isinstance(name, bytes) else str(name),
            "total_memory_bytes": int(properties["totalGlobalMem"]),
            "multiprocessors": int(properties["multiProcessorCount"]),
            "cupy_version": cp.__version__,
            "precision": "float64",
            "threads_per_trajectory": 256,
        }

    def quench(self, packings: np.ndarray, lengths: np.ndarray, steps: int = 600):
        cp = self.cp
        host = np.ascontiguousarray(packings, dtype=np.float64)
        lengths = np.asarray(lengths, dtype=np.float64)
        if host.ndim != 3 or host.shape[2] != 3 or lengths.shape != (len(host),):
            raise ValueError("Expected packings (batch,n,3) and lengths (batch,)")
        if not np.isfinite(host).all() or not np.isfinite(lengths).all() or np.any(lengths <= 1):
            raise ValueError("Nonfinite input or invalid container length")
        if not 1 <= steps <= 5000:
            raise ValueError("steps must be between 1 and 5000")
        batch, n, _ = host.shape
        if batch < 1 or n < 1:
            raise ValueError("Cannot relax an empty batch or packing")
        nc = int(math.ceil((float(lengths.max()) + 6) / 1.5)) + 1
        q = cp.asarray(host)
        boxes = cp.asarray(lengths)
        heads = cp.empty((batch, nc * nc), cp.int32)
        links = cp.empty((batch, n), cp.int32)
        trigs = cp.empty((batch, n, 2), cp.float64)
        history_length = 8
        work = cp.empty((batch, 5, n, 3), cp.float64)
        history = cp.empty((batch, 2, history_length, n, 3), cp.float64)
        output = cp.empty((batch, 3), cp.float64)
        start, end = cp.cuda.Event(), cp.cuda.Event()
        wall_start = time.monotonic()
        start.record()
        self.function(
            (batch,),
            (256,),
            (
                q,
                work,
                history,
                output,
                np.int32(n),
                np.int32(nc),
                boxes,
                heads,
                links,
                trigs,
                np.int32(steps),
                np.int32(history_length),
            ),
        )
        # Upstream lbfgs can leave mp from its final rejected line-search trial.
        # Recompute both residual diagnostics on the coordinates actually returned.
        evaluated = cp.empty((batch, 2), cp.float64)
        self.evaluate(
            (batch,),
            (256,),
            (q, work, evaluated, np.int32(n), np.int32(nc), boxes, heads, links, trigs),
        )
        end.record()
        end.synchronize()
        result = cp.asnumpy(q)
        stats = cp.asnumpy(output)
        stats[:, :2] = cp.asnumpy(evaluated)
        return (
            result,
            stats,
            {
                "cuda_seconds": float(cp.cuda.get_elapsed_time(start, end) / 1000),
                "wall_seconds": time.monotonic() - wall_start,
                "batch": batch,
                "n": n,
                "steps": steps,
            },
        )
