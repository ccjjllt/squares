"""From-scratch K^2+D template families for targeted n (research 2026-11-11).

Templates (all built from scratch, not by editing a merged layout):

  T1 row strip      : (K-t) x K upright lattice frozen at the bottom-left; the
                      remaining t*K + D squares live in the top band
                      [0,L] x [K-t, L] and the right band [K, L] x [0, K-t].
  T2 staircase fault: K x K lattice cut by a monotone staircase; one side is
                      translated by (fx, fy); step notches host the D extras.
  T3 straight seam  : K x K lattice cut along a straight line at angle phi,
                      one part slid, D squares inserted along the seam.
  T4 corner block   : b x b corner block (b^2 ~ D) freed; b^2+D squares packed
                      into the b+f corner square.

Everything is then handed to the public Rust `fq` fixed-side shrink
(`fq quench --shrink --freeze ...`), which grows to feasibility and then
shrinks the box with the frozen part held absolutely fixed.  Any resulting
packing is certified with the repo's vendored official v20 metric on the exact
doubles that survive the float64 round trip.

Write scope: outputs/experiments/research_20261111/templates/ only.

Usage:
  uv run python scripts/experiments/template_k2d_20261111.py --n 971 \
      --templates T1 --seeds 6 --deadline 25 --out outputs/experiments/research_20261111/templates
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from squares._vendor import official_metric as metric  # noqa: E402

FQ = Path(
    "/private/var/folders/9s/sdk1x32s58g8dycwh6c74bqc0000gp/T/opencode/"
    "square-packing/search/packer/target/release/fq"
)
BASE = ROOT / "outputs/merged/v124_plus_daily44_public2/submission.csv"
RECORDS = ROOT / "data/references/leaderboards/perpuzzle_best_20261029.csv"
OUT = ROOT / "outputs/experiments/research_20261111/templates"

T0 = time.time()


def log(*a: object) -> None:
    print(f"{time.strftime('%H:%M:%S')} [{time.time() - T0:6.0f}s]", *a, flush=True)


# ---------------------------------------------------------------- geometry ---


def extents(P: np.ndarray) -> tuple[float, float]:
    x, y, t = P[:, 0], P[:, 1], P[:, 2]
    c, s = np.cos(t) / 2, np.sin(t) / 2
    X = np.concatenate([x + c - s, x - c - s, x - c + s, x + c + s])
    Y = np.concatenate([y + s + c, y - s + c, y - s - c, y + s - c])
    return float(X.max() - X.min()), float(Y.max() - Y.min())


def side(P: np.ndarray) -> float:
    w, h = extents(P)
    return max(w, h)


def corners(P: np.ndarray) -> np.ndarray:
    x, y, t = P[:, 0], P[:, 1], P[:, 2]
    c, s = np.cos(t) / 2, np.sin(t) / 2
    dx1, dy1 = c - s, s + c
    dx2, dy2 = -c - s, -s + c
    cx = np.stack([x + dx1, x + dx2, x - dx1, x - dx2], axis=-1)
    cy = np.stack([y + dy1, y + dy2, y - dy1, y - dy2], axis=-1)
    return np.stack([cx, cy], axis=-1)


def min_gap(P: np.ndarray) -> tuple[float, float]:
    """(min pair gap, min wall clearance) for the axis-aligned box [0,L]^2 of P."""
    C = corners(P)
    L = max(C[..., 0].max() - C[..., 0].min(), C[..., 1].max() - C[..., 1].min())
    wall = min(
        (C[..., 0] - C[..., 0].min()).min(),
        (C[..., 1] - C[..., 1].min()).min(),
        (L - (C[..., 0] - C[..., 0].min())).min(),
        (L - (C[..., 1] - C[..., 1].min())).min(),
    )
    # SAT gap: positive = separated
    from scipy.spatial import cKDTree

    n = len(P)
    tree = cKDTree(P[:, :2])
    best = 1.0
    for i in range(n):
        for j in tree.query_ball_point(P[i, :2], 1.5):
            if j <= i:
                continue
            # overlap iff projections overlap on all 4 axes
            g = -1e9
            for ax in range(4):
                ui = np.array([math.cos(i * 0.0)])  # placeholder
            # exact: use separating axes of both squares
            ci, cj = C[i], C[j]
            axes = []
            for k in range(2):
                e = ci[(k + 1) % 4] - ci[k]
                axes.append(e / np.linalg.norm(e))
            for k in range(2):
                e = cj[(k + 1) % 4] - cj[k]
                axes.append(e / np.linalg.norm(e))
            for u in axes:
                pi = ci @ u
                pj = cj @ u
                g = max(g, max(pi.min() - pj.max(), pj.min() - pi.max()))
            best = min(best, g)
    return best, wall


def sat_overlap(P: np.ndarray, L: float) -> tuple[int, float, float]:
    """Count overlapping pairs and max penetration at fixed side L (box re-centred)."""
    C = corners(P)
    lo = np.array([C[..., 0].min(), C[..., 1].min()])
    C = C - lo
    wall = min(C[..., 0].min(), C[..., 1].min(), L - C[..., 0].max(), L - C[..., 1].max())
    from scipy.spatial import cKDTree

    tree = cKDTree(P[:, :2] - lo)
    cnt = 0
    pen = 0.0
    worst = None
    for i in range(len(P)):
        for j in tree.query_ball_point(P[i, :2] - lo, 1.5):
            if j <= i:
                continue
            ci, cj = C[i], C[j]
            axes = []
            for k in range(2):
                e = ci[(k + 1) % 4] - ci[k]
                axes.append(e / np.linalg.norm(e))
            for k in range(2):
                e = cj[(k + 1) % 4] - cj[k]
                axes.append(e / np.linalg.norm(e))
            ov = 1e9
            for u in axes:
                pi, pj = ci @ u, cj @ u
                ov = min(ov, min(pi.max(), pj.max()) - max(pi.min(), pj.min()))
            if ov > 1e-12:
                cnt += 1
                if ov > pen:
                    pen, worst = ov, (i, j)
    return cnt, pen, wall, worst


def certify(n: int, P: np.ndarray) -> tuple[float, np.ndarray] | None:
    """Official v20 metric on the exact doubles repr() round-trips."""
    rows = [
        {"n": str(n), "square_id": str(i), "x": repr(float(a)), "y": repr(float(b)), "angle": repr(float(t))}
        for i, (a, b, t) in enumerate(P)
    ]
    _, _, detail, why = metric.evaluate_single_puzzle(n, rows)
    if why != "ok" or detail is None:
        return None
    return float(detail), P


# --------------------------------------------------------------- templates ---


def lattice(K: int, rows: int, cols: int, ox: float = 0.0, oy: float = 0.0) -> np.ndarray:
    y, x = np.mgrid[0:rows, 0:cols]
    return np.c_[x.ravel() + 0.5 + ox, y.ravel() + 0.5 + oy, np.zeros(rows * cols)]


def zigzag_strip(width: float, height: float, count: int, theta: float, rng: np.random.Generator) -> np.ndarray:
    """`count` squares in a strip [0,width] x [0,height] as interleaved +-theta rows."""
    out = []
    h = math.cos(theta) + math.sin(theta)  # bbox of one tilted square
    pitch = max(0.55, min(1.0, width / max(count, 1) * 0.98))
    # two interleaved rows at +-theta, vertical pitch vp
    vp = max(0.80, min(h, height / max(1, math.ceil(count / (width / max(pitch, 0.5))))))
    col = 0
    row = 0
    used = 0
    while used < count:
        for k in range(max(1, int(width / pitch))):
            if used >= count:
                break
            th = theta if (k + row) % 2 == 0 else -theta
            xx = min(width - h / 2, (k + 0.5) * pitch)
            yy = min(height - h / 2, (row + 0.5) * vp)
            out.append((xx, yy, th))
            used += 1
        row += 1
    return np.array(out[:count], float)


def template_T1(n: int, t: int, L: float, seed: int, pattern: str) -> tuple[np.ndarray, np.ndarray, int]:
    """Returns (P, frozen_mask, lattice_count). Lattice is (K-t) x K upright, frozen."""
    K = math.isqrt(n)
    D = n - K * K
    lat = lattice(K, K - t, K)
    free = n - len(lat)
    rng = np.random.default_rng(seed)
    band_h = L - (K - t)
    band_w = L
    right_w = L - K
    pts = []
    if pattern == "grid":
        # t full rows of K upright, then D extras spread along the residual band
        rows = []
        for r in range(t):
            for c in range(K):
                pts.append((c + 0.5 + (band_w - K) / 2, K - t + r + 0.5, 0.0))
        extra = free - t * K
        for k in range(extra):
            xx = (k + 0.5) * band_w / max(extra, 1)
            pts.append((min(band_w - 0.75, max(0.75, xx)), K - t + t + 0.5 * band_h * 0.5 + 0.2, 0.7))
    elif pattern == "zigzag":
        th = math.radians(rng.choice([15, 20, 25, 30, 35, 40]))
        # fill the top band, then the right band
        a = zigzag_strip(band_w, band_h, min(free, int(band_w * band_h * 2)), th, rng)
        a[:, 1] += K - t
        pts.extend(a.tolist())
        rest = free - len(a)
        if rest > 0:
            b = zigzag_strip(right_w, K - t, rest, th, rng)
            pts.extend(b.tolist())
    elif pattern == "rows":
        m = 0
        while len(pts) < free:
            y = K - t + 0.5 + m
            x = 0.5
            while x < band_w - 0.5 and len(pts) < free:
                pts.append((x, y, 0.0))
                x += 1.0
            m += 1
        pts = pts[:free]
    else:  # random
        for _ in range(free):
            pts.append((rng.uniform(0.5, L - 0.5), rng.uniform(K - t + 0.5, L - 0.5), rng.uniform(-0.7, 0.7)))
    P = np.vstack([lat, np.array(pts, float)])
    mask = np.zeros(n, bool)
    mask[: len(lat)] = True
    return P, mask, len(lat)


def template_capacity(K: int, t: int, m: int, L: float, seed: int) -> tuple[np.ndarray, np.ndarray, int]:
    """(K-t) x K frozen lattice + m free squares in the top band, for capacity probes."""
    lat = lattice(K, K - t, K)
    rng = np.random.default_rng(seed)
    band_h = L - (K - t)
    pts = []
    nrow = int(math.floor(band_h))
    for r in range(max(1, nrow)):
        for c in range(K):
            if len(pts) >= m:
                break
            pts.append((c + 0.5, K - t + r + 0.5, 0.0))
    while len(pts) < m:
        pts.append((rng.uniform(0.6, L - 0.6), rng.uniform(K - t + 0.6, L - 0.6), rng.uniform(-0.7, 0.7)))
    P = np.vstack([lat, np.array(pts[:m], float)])
    mask = np.zeros(len(P), bool)
    mask[: len(lat)] = True
    return P, mask, len(lat)


def template_global(n: int, L: float, seed: int) -> tuple[np.ndarray, np.ndarray, int]:
    """From scratch: K x K upright grid + (n-K^2) extras with random pose in the top band."""
    K = math.isqrt(n)
    D = n - K * K
    lat = lattice(K, K, K, ox=(L - K) / 2)
    rng = np.random.default_rng(seed)
    pts = [(rng.uniform(0.6, L - 0.6), rng.uniform(K - 0.2, L - 0.6), rng.uniform(-0.7, 0.7)) for _ in range(D)]
    P = np.vstack([lat, np.array(pts, float)])
    return P, np.zeros(n, bool), len(lat)


def template_T4(n: int, L: float, seed: int) -> tuple[np.ndarray, np.ndarray, int]:
    K = math.isqrt(n)
    D = n - K * K
    b = max(1, int(round(math.sqrt(D))))
    # lattice minus the top-right b x b block
    rows, cols = np.mgrid[0:K, 0:K]
    keep = ~((rows >= K - b) & (cols >= K - b))
    y, x = rows[keep], cols[keep]
    lat = np.c_[x + 0.5, y + 0.5, np.zeros(len(x))]
    free = n - len(lat)
    rng = np.random.default_rng(seed)
    pts = []
    for _ in range(free):
        pts.append((rng.uniform(K - b + 0.3, L - 0.3), rng.uniform(K - b + 0.3, L - 0.3), rng.uniform(-0.6, 0.6)))
    P = np.vstack([lat, np.array(pts, float)])
    mask = np.zeros(n, bool)
    mask[: len(lat)] = True
    return P, mask, len(lat)


def write_fq(path: Path, P: np.ndarray, s: float) -> None:
    with path.open("w") as f:
        f.write(f"{len(P)} {s:.6f}\n")
        for x, y, t in P:
            f.write(f"{x:.6f} {y:.6f} {math.degrees(t):.6f}\n")


def read_fq(path: Path) -> tuple[float, np.ndarray]:
    tok = path.read_text().split()
    n = int(tok[0])
    s = float(tok[1])
    v = np.array([float(q) for q in tok[2 : 2 + 3 * n]], float).reshape(n, 3)
    v[:, 2] = np.radians(v[:, 2])
    return s, v


def run_fq(P: np.ndarray, mask: np.ndarray, s0: float, deadline: float, seed: int, work: Path,
           shrink: bool = True, loosen: float = 1.02, spec_tag: str = "") -> tuple[float, np.ndarray, dict]:
    """fq fixed-side shrink with the frozen mask (or a plain quench); returns (s, P, info)."""
    tag = f"{spec_tag}_{seed}" if spec_tag else str(seed)
    inp, out = work / f"in_{tag}.txt", work / f"out_{tag}.txt"
    write_fq(inp, P, s0)
    idx = np.flatnonzero(mask)
    freeze = f"{idx[0]}-{idx[-1]}" if len(idx) and idx[-1] - idx[0] + 1 == len(idx) else ",".join(map(str, idx))
    cmd = [
        str(FQ), "quench", "--in", str(inp), "--out", str(out),
        "--seed", str(seed), "--deadline", str(deadline),
    ]
    if shrink:
        cmd += ["--shrink", "--d0", "2e-2", "--dmin", "2e-6", "--loosen", str(loosen)]
    else:
        cmd += ["--loosen", "1.0", "--kick", str(0.02)]
    if len(idx):
        cmd += ["--freeze", freeze]
    p = subprocess.run(cmd, capture_output=True, text=True)
    info: dict = {}
    for line in p.stdout.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                info = json.loads(line)
            except json.JSONDecodeError:
                pass
    if not out.exists():
        return float("nan"), P, info
    s, Q = read_fq(out)
    return s, Q, info


def build(spec: dict) -> tuple[np.ndarray, np.ndarray, int]:
    n, tmpl, seed, s0 = spec["n"], spec["template"], spec["seed"], spec["s0"]
    if tmpl.startswith("T1"):
        t = int(tmpl.split("_t")[1])
        return template_T1(n, t, s0, seed, spec["pattern"])
    if tmpl == "T4":
        return template_T4(n, s0, seed)
    if tmpl == "CAP":
        return template_capacity(spec["K"], spec["t"], spec["m"], s0, seed)
    if tmpl == "GLOBAL":
        return template_global(n, s0, seed)
    raise ValueError(tmpl)


def job(spec: dict) -> dict:
    n = spec["n"]
    work = Path(spec["work"])
    work.mkdir(parents=True, exist_ok=True)
    P, mask, nlat = build(spec)
    tag = spec["template"] + (
        f"-t{spec['t']}" if "t" in spec else "") + (f"-m{spec['m']}" if "m" in spec else "")
    s, Q, info = run_fq(P, mask, spec["s0"], spec["deadline"], spec["seed"], work, shrink=not spec.get("quench"), spec_tag=tag)
    if not np.isfinite(s):
        return {**spec, "ok": False, "s": None}
    # normalise: box starts at 0
    C = corners(Q)
    Q = Q.copy()
    Q[:, 0] -= C[..., 0].min()
    Q[:, 1] -= C[..., 1].min()
    L = side(Q)
    cnt, pen, wall, worst = sat_overlap(Q, L)
    cert = certify(n, Q) if cnt == 0 and pen <= 1e-12 else None
    return {
        **spec, "ok": True, "s": s, "L": L, "pairs": cnt, "pen": pen,
        "wall": wall, "worst": worst, "cert": (cert[0] if cert else None),
        "viol": info.get("viol"), "P": Q,
    }


def load_base(n: int) -> np.ndarray | None:
    import pandas as pd

    df = pd.read_csv(BASE)
    g = df[df.n == n].sort_values("square_id")
    if len(g) != n:
        return None
    return g[["x", "y", "angle"]].to_numpy(float)


def best_holes(P: np.ndarray, L: float, k: int, rng: np.random.Generator) -> list[tuple[float, float]]:
    """k well-spread points of locally maximal distance to the existing squares."""
    from scipy.spatial import cKDTree

    tree = cKDTree(P[:, :2])
    xs = np.linspace(0.5, L - 0.5, 90)
    ys = np.linspace(0.5, L - 0.5, 90)
    GX, GY = np.meshgrid(xs, ys)
    d, _ = tree.query(np.c_[GX.ravel(), GY.ravel()])
    order = np.argsort(-d)
    out: list[tuple[float, float]] = []
    for idx in order:
        p = (float(GX.ravel()[idx]), float(GY.ravel()[idx]))
        if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 2.0 for q in out):
            out.append(p)
            if len(out) >= k:
                break
    return out


def job_insert(spec: dict) -> dict:
    """Insert k squares into the donor layout and try a fixed-side shrink below the current L."""
    n = spec["n"]
    work = Path(spec["work"])
    work.mkdir(parents=True, exist_ok=True)
    donor = spec["donor"]
    P = load_base(donor)
    if P is None:
        return {**spec, "ok": False}
    rng = np.random.default_rng(spec["seed"])
    k = n - donor
    holes = best_holes(P, float(P.max()) + 0.5, k, rng)
    add = np.array([(x, y, 0.0) for x, y in holes], float)
    Q = np.vstack([P, add])
    mask = np.zeros(len(Q), bool)
    if spec.get("frozen"):
        mask[: len(P)] = True
    s, R, info = run_fq(Q, mask, spec["s0"], spec["deadline"], spec["seed"], work, shrink=True, loosen=spec.get("loosen", 1.02), spec_tag="INS" + str(spec["donor"]))
    if not np.isfinite(s):
        return {**spec, "ok": False}
    C = corners(R)
    R = R.copy()
    R[:, 0] -= C[..., 0].min()
    R[:, 1] -= C[..., 1].min()
    L = side(R)
    cnt, pen, wall, worst = sat_overlap(R, L)
    cert = certify(n, R) if cnt == 0 and pen <= 1e-12 else None
    return {**spec, "ok": True, "s": s, "L": L, "pairs": cnt, "pen": pen, "wall": wall,
            "cert": (cert[0] if cert else None), "viol": info.get("viol"), "P": R}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=971)
    ap.add_argument("--templates", default="T1")
    ap.add_argument("--mode", default="templates", choices=["templates", "cap", "insert"])
    ap.add_argument("--caps", default="34,36,38,40,41")
    ap.add_argument("--donors", default="969")
    ap.add_argument("--loosen", type=float, default=1.02)
    ap.add_argument("--frozen", action="store_true")
    ap.add_argument("--ds", type=float, default=0.0)
    ap.add_argument("--L", type=float, default=None, help="fixed side for capacity probes")
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--deadline", type=float, default=20.0)
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    out = Path(a.out)
    work = out / "work" / f"n{a.n}"
    work.mkdir(parents=True, exist_ok=True)

    Ls = {int(r["n"]): float(r["L"]) for r in __import__("csv").DictReader(RECORDS.open())}
    n = a.n
    K = math.isqrt(n)
    Lrec = a.L if a.L is not None else Ls[n]
    log(f"n={n} K={K} D={n - K * K} record L={Lrec:.9f}")

    specs = []
    if a.mode == "cap":
        # capacity probe: how many squares fit in the top band at fixed L with the lattice frozen?
        for t in (1, 2):
            for m in [int(q) for q in a.caps.split(",")]:
                specs.append(dict(n=n, template="CAP", K=K, t=t, m=m, seed=0, s0=a.L, deadline=a.deadline, work=str(work)))
    else:
        for seed in range(a.seeds):
            if a.mode == "insert":
                for donor in [int(q) for q in a.donors.split(",")]:
                    specs.append(dict(n=n, donor=donor, template="INSERT", seed=seed, loosen=a.loosen,
                                      s0=a.L + a.ds * seed, deadline=a.deadline, frozen=a.frozen,
                                      work=str(work / f"don{donor}")))
                continue
            for tmpl in a.templates.split(","):
                if tmpl == "T1":
                    for t in (1, 2):
                        specs.append(dict(
                            n=n, template=f"T1_t{t}", pattern="grid", seed=seed, s0=Lrec + 0.02,
                            deadline=a.deadline, work=str(work),
                        ))
                elif tmpl == "T4":
                    specs.append(dict(
                        n=n, template="T4", pattern="random", seed=seed, s0=Lrec + 0.02,
                        deadline=a.deadline, work=str(work),
                    ))
                elif tmpl == "GLOBAL":
                    specs.append(dict(
                        n=n, template="GLOBAL", pattern="grid", seed=seed, s0=Lrec + 0.9,
                        deadline=a.deadline, work=str(work), quench=True,
                    ))
    log(f"{len(specs)} runs")
    fn = job_insert if a.mode == "insert" else job
    with Pool(min(3, len(specs))) as pool:
        res = pool.map(fn, specs)
    good = sorted([r for r in res if r.get("cert") is not None], key=lambda r: r["cert"])
    for r in sorted(res, key=lambda r: (r.get("cert") is None, r.get("cert") or 1e9)):
        log(
            f"{r['template']} seed={r['seed']:2d} L={r.get('L')} cert={r.get('cert')} "
            f"pairs={r.get('pairs')} pen={r.get('pen')} wall={r.get('wall')}"
        )
    if good:
        best = good[0]
        log(f"BEST {best['template']} seed={best['seed']} L={best['cert']}")
        np.save(out / f"best_n{n}.npy", best["P"])
        (out / f"best_n{n}.json").write_text(json.dumps({k: v for k, v in best.items() if k != "P"}, default=str, indent=1))


if __name__ == "__main__":
    main()
