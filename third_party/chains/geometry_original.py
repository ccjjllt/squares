import math
from types import SimpleNamespace
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import connected_components

# ---------- geometry: a packing is an (n, 3) array of rows (x, y, angle in radians) ----------
HALF = 0.5
CONTACT_RADIUS = math.sqrt(2.0)

def corners(P: np.ndarray) -> np.ndarray:
    """Corners of every square, shape ``(n, 4, 2)``, in the metric's order."""
    x, y, a = P[:, 0], P[:, 1], P[:, 2]
    c, s = np.cos(a), np.sin(a)
    dx1, dy1 = HALF * c - HALF * s, HALF * s + HALF * c
    dx2, dy2 = -HALF * c - HALF * s, -HALF * s + HALF * c
    cx = np.stack([x + dx1, x + dx2, x - dx1, x - dx2], axis=-1)
    cy = np.stack([y + dy1, y + dy2, y - dy1, y - dy2], axis=-1)
    return np.stack([cx, cy], axis=-1)


def bounds(P: np.ndarray) -> tuple[float, float, float, float]:
    """Axis-aligned bounding box ``(xmin, ymin, xmax, ymax)`` over all corners."""
    C = corners(P)
    return C[..., 0].min(), C[..., 1].min(), C[..., 0].max(), C[..., 1].max()


def side_length(P: np.ndarray) -> float:
    """Container side ``L = max(width, height)``, as the metric measures it."""
    xmin, ymin, xmax, ymax = bounds(P)
    return float(max(xmax - xmin, ymax - ymin))


def score(n: int, L: float) -> float:
    return L / math.sqrt(n) - 1.0


def normalize(P: np.ndarray) -> np.ndarray:
    """Translate so the bounding box starts at the origin."""
    xmin, ymin, _, _ = bounds(P)
    Q = P.copy()
    Q[:, 0] -= xmin
    Q[:, 1] -= ymin
    return Q


def candidate_pairs(P: np.ndarray, margin: float = 0.0) -> np.ndarray:
    """Index pairs ``(m, 2)`` whose centres are close enough to possibly touch."""
    if len(P) < 2:
        return np.empty((0, 2), dtype=np.int64)
    tree = cKDTree(P[:, :2])
    return tree.query_pairs(CONTACT_RADIUS + margin, output_type="ndarray")


def separations(P: np.ndarray, pairs: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Signed SAT separation for each candidate pair.

    Positive values are the widest gap over the four edge-normal axes (the pair
    is disjoint); negative values are minus the penetration depth (the pair
    overlaps by that much along its shallowest axis).  Returns ``(pairs, sep)``.
    """
    if pairs is None:
        pairs = candidate_pairs(P)
    if len(pairs) == 0:
        return pairs, np.empty(0)
    C = corners(P)
    i, j = pairs[:, 0], pairs[:, 1]
    ai, aj = P[i, 2], P[j, 2]
    # (m, 4, 2): the two edge normals of each square of the pair.
    axes = np.stack(
        [
            np.stack([np.cos(ai), np.sin(ai)], -1),
            np.stack([-np.sin(ai), np.cos(ai)], -1),
            np.stack([np.cos(aj), np.sin(aj)], -1),
            np.stack([-np.sin(aj), np.cos(aj)], -1),
        ],
        axis=1,
    )
    # (m, 4 axes, 4 corners) projections.
    pi = np.einsum("mad,mcd->mac", axes, C[i])
    pj = np.einsum("mad,mcd->mac", axes, C[j])
    gap = np.maximum(pj.min(-1) - pi.max(-1), pi.min(-1) - pj.max(-1))
    return pairs, gap.max(-1)


def min_separation(P: np.ndarray) -> float:
    """Smallest signed separation over all pairs (``inf`` when nothing is close)."""
    _, sep = separations(P)
    return float(sep.min()) if len(sep) else math.inf


geo = SimpleNamespace(corners=corners, bounds=bounds, side_length=side_length, score=score, normalize=normalize,
                      candidate_pairs=candidate_pairs, separations=separations, min_separation=min_separation)

# ---------- band detection and the slab moves ----------
def tilt(P: np.ndarray) -> np.ndarray:
    """Angle of each square in (-45, 45] degrees."""
    a = np.degrees(P[:, 2]) % 90
    return np.where(a > 45, a - 90, a)


def bands(P: np.ndarray, min_count: int = 40, gap: float = 0.5, link: float = 1.2) -> list[tuple[np.ndarray, int, float]]:
    """[(mask, axis, period)] per big tilted class; axis 0 = a band along x (cut it with a vertical line).

    A class is a run of tilt angles (|tilt| > 5 deg) with no hole wider than ``gap`` degrees, so a band
    whose angles a re-quench spread over a few tenths stays one class.  Two bands with the same angle
    (one per wall, README 26.27) fall in one run; it is split when its squares form two or more
    spatial groups of ``min_count`` (centres closer than ``link`` are linked).
    """
    t = tilt(P)
    idx = np.flatnonzero(np.abs(t) > 5)
    idx = idx[np.argsort(t[idx])]
    out = []
    for run in np.split(idx, np.flatnonzero(np.diff(t[idx]) > gap) + 1):
        if len(run) < min_count:
            continue
        for part in _spatial_groups(P[run, :2], min_count, link):
            m = np.zeros(len(P), bool)
            m[run[part]] = True
            ext = np.ptp(P[m, :2], axis=0)
            out.append((m, 0 if ext[0] > ext[1] else 1, 1 / np.cos(np.radians(np.abs(t[m]).mean()))))
    return out


def _spatial_groups(X: np.ndarray, min_count: int, link: float) -> list[np.ndarray]:
    """Indices of each linked group of at least ``min_count`` centres; the whole set if there are fewer than two."""
    G = cKDTree(X).sparse_distance_matrix(cKDTree(X), link)
    _, lab = connected_components(G, directed=False)
    big = [np.flatnonzero(lab == i) for i, c in enumerate(np.bincount(lab)) if c >= min_count]
    if len(big) >= 2:
        return big
    return _split_l(X, min_count) or [np.arange(len(X))]


def _split_l(X: np.ndarray, min_count: int) -> list[np.ndarray] | None:
    """Two bands of the same angle that touch at a corner (an L): split by row occupancy (README 26.36).

    Along each axis, the rows (unit bins) crossed by the band running along that axis hold many
    squares and those crossed by the other band few; the rows above half of the maximum are the first
    band.  Accepted only if both parts have ``min_count`` squares, one is wide and the other tall.
    """
    ext = np.ptp(X, axis=0)
    if ext.min() < 0.5 * ext.max():
        return None
    for axis in (1, 0):  # bin along y: rows of a band along x; then the transposed case
        b = np.floor(X[:, axis] - X[:, axis].min()).astype(int)
        cnt = np.bincount(b)
        rows = cnt > 0.5 * cnt.max()
        A = np.flatnonzero(rows[b])
        Bp = np.flatnonzero(~rows[b])
        if min(len(A), len(Bp)) < min_count:
            continue
        ea, eb = np.ptp(X[A], axis=0), np.ptp(X[Bp], axis=0)
        long_a, long_b = 1 - axis, axis  # A runs across the bins, B along them
        if ea[long_a] > ea[1 - long_a] and eb[long_b] > eb[1 - long_b]:
            return [A, Bp]
    return None


def grow(P: np.ndarray, axis: int, xc: float, p: float) -> np.ndarray:
    """One slab at coordinate xc along ``axis``: shift everything beyond it by p, copy the rows' last square."""
    w = np.where(np.abs(tilt(P)) < 0.01, 1.0, p)  # copy distance: 1 in upright rows, p in tilted ones
    x = P[:, axis]
    near = (x > xc - w) & (x <= xc)
    dup = P[near].copy()
    dup[:, axis] += w[near]
    Q = P.copy()
    Q[x > xc, axis] += p
    return np.vstack([Q, dup])


def overlaps(P: np.ndarray, tol: float = 1e-9) -> int:
    _, sep = geo.separations(P, geo.candidate_pairs(P))
    return int((sep < -tol).sum())


def best_grow(P: np.ndarray, axis: int, mask: np.ndarray, p: float, tries: int = 60) -> tuple[np.ndarray, float, int]:
    """The cut across the middle of the band (30-70 % of its extent) with fewest overlaps, then smallest side."""
    lo, hi = np.percentile(P[mask, axis], [30, 70])
    best = None
    for xc in np.linspace(lo, hi, tries):
        Q = grow(P, axis, xc, p)
        key = (overlaps(Q), geo.side_length(Q))
        if best is None or key < best[0]:
            best = (key, Q, xc)
    (k, _), Q, xc = best
    return Q, float(xc), k


def grow_all(P: np.ndarray, tries: int = 60) -> tuple[np.ndarray, int] | None:
    """One slab in each band of a two-band packing (one along x, one along y); None for other structures."""
    P = geo.normalize(P)
    B = bands(P)
    if len(B) != 2 or {a for _, a, _ in B} != {0, 1}:
        return None
    Q, k = P, 0
    for m, axis, p in B:
        mask = np.r_[m, np.zeros(len(Q) - len(P), bool)]
        Q, _, k = best_grow(Q, axis, mask, p, tries)
    return geo.normalize(Q), k


def periods(P: np.ndarray) -> np.ndarray:
    """Row period of every square: 1 upright, 1/cos(theta) tilted (the spacing of a lattice row)."""
    return 1 / np.cos(np.radians(np.abs(tilt(P))))


def cut(P: np.ndarray, axis: int, xc: float, sign: int = 1) -> np.ndarray:
    """A generic slab at xc along ``axis``, for any mix of upright and tilted rows.

    sign = +1: every square of the window (xc - w, xc] is copied by its own period w and the part
    beyond the cut moves by the largest w in the window (rows with a smaller period keep slack).
    sign = -1: the window is removed and the part beyond moves back by the smallest w (rows with a
    larger period keep a gap).  Exact for perfect lattice rows; other contacts are checked later.
    """
    w = periods(P)
    x = P[:, axis]
    near = (x > xc - w) & (x <= xc)
    if not near.any():
        return P.copy()
    Q = P.copy()
    if sign > 0:
        dup = P[near].copy()
        dup[:, axis] += w[near]
        Q[x > xc, axis] += w[near].max()
        return np.vstack([Q, dup])
    Q[x > xc, axis] -= w[near].min()
    return Q[~near]


def shrink_all(P: np.ndarray, tries: int = 60, depth: float = 0.02) -> tuple[np.ndarray, int] | None:
    """One slab removed through each band of a two-band packing (``cut`` with sign -1 inside the
    band's 30-70 % extent): K - 1, with a gap of p - 1 left in the band rows for the optimiser."""
    P = geo.normalize(P)
    B = bands(P)
    if len(B) != 2 or {a for _, a, _ in B} != {0, 1}:
        return None
    Q = P
    for m, axis, _ in B:
        lo, hi = np.percentile(P[m, axis], [30, 70])
        best = None
        for xc in np.linspace(lo, hi, tries):
            R = cut(Q, axis, xc, -1)
            if len(R) == len(Q) or geo.min_separation(R) < -depth:
                continue
            key = geo.side_length(R)
            if best is None or key < best[0]:
                best = (key, R)
        if best is None:
            return None
        Q = best[1]
    return geo.normalize(Q), overlaps(Q)


# ---------- joint crossover ----------
def _reflect(P: np.ndarray, c: int, L: float) -> np.ndarray:
    """Mirror coordinate c about the middle of the box (the angles change sign)."""
    Q = P.copy()
    Q[:, c] = L - Q[:, c]
    Q[:, 2] = -Q[:, 2]
    return Q


def canonical(P: np.ndarray) -> np.ndarray | None:
    """The packing reflected so that its band along x lies on the floor and its band along y on the
    right wall (README 26.35); None if it is not a two-band packing with both bands on walls."""
    P = geo.normalize(P)
    L = geo.side_length(P)
    B = bands(P)
    if len(B) != 2 or {a for _, a, _ in B} != {0, 1}:
        return None
    for m, axis, _ in B:
        c = 1 - axis
        cc = geo.corners(P)[m][..., c]
        lo, hi = cc.min() < 0.05, cc.max() > L - 0.05
        if not (lo or hi):
            return None
        if (axis == 0 and hi and not lo) or (axis == 1 and lo and not hi):  # floor band on top / right band on the left
            P = _reflect(P, c, L)
    return geo.normalize(P)


def _row_phase(P: np.ndarray, mask: np.ndarray, axis: int, p: float) -> float:
    """Phase (mod p) along ``axis`` of the band row nearest the wall: circular mean of x mod p."""
    c = 1 - axis
    y = P[mask, c]
    row = mask.copy()
    row[mask] = y < y.min() + 0.3
    ang = 2 * np.pi * (P[row, axis] % p) / p
    return float((np.angle(np.exp(1j * ang).mean()) % (2 * np.pi)) * p / (2 * np.pi))


def crossover(T: np.ndarray, A: np.ndarray, axis: int, store_L: dict[int, float], tries: int = 15,
              depth: float = 0.02, below: int = 40) -> tuple[np.ndarray, float] | None:
    """T's part before a cut across its ``axis`` band + A's part after it, the band lattices aligned (README 26.35).

    Both packings in ``canonical`` form.  The cut c runs over the middle 30-70 % of T's band; A's part
    starts at c_A = c - delta with delta = (phase_T - phase_A) + k p, every k that puts c_A in the
    middle of A's band, refined by +-0.01.  Squares of A's part that overlap T's part deeper than
    ``depth`` are dropped.  Returns (child, dry excess) for the child with the lowest dry side relative
    to the store at any m in [n' - below, n'], or None.
    """
    BT = {a: (m, p) for m, a, p in bands(T)}
    BA = {a: (m, p) for m, a, p in bands(A)}
    if axis not in BT or axis not in BA:
        return None
    (mT, pT), (mA, pA) = BT[axis], BA[axis]
    if np.sign(tilt(T)[mT].mean()) != np.sign(tilt(A)[mA].mean()):
        return None
    p = 0.5 * (pT + pA)
    d0 = _row_phase(T, mT, axis, p) - _row_phase(A, mA, axis, p)
    loT, hiT = np.percentile(T[mT, axis], [30, 70])
    loA, hiA = np.percentile(A[mA, axis], [30, 70])
    best = None
    for c in np.linspace(loT, hiT, tries):
        left = T[T[:, axis] <= c]
        for k in range(int(np.floor((c - hiA - d0) / p)), int(np.ceil((c - loA - d0) / p)) + 1):
            for eps in (-0.01, 0.0, 0.01):
                delta = d0 + k * p + eps
                cA = c - delta
                if not loA <= cA <= hiA:
                    continue
                right = A[A[:, axis] > cA].copy()
                right[:, axis] += delta
                X = np.vstack([left, right])
                pairs, sep = geo.separations(X)
                bad = pairs[(sep < -depth) & (pairs[:, 0] < len(left)) & (pairs[:, 1] >= len(left)), 1]
                bad = np.concatenate([bad, pairs[(sep < -depth) & (pairs[:, 1] < len(left)) & (pairs[:, 0] >= len(left)), 0]])
                X = np.delete(X, np.unique(bad), 0)
                if geo.min_separation(X) < -depth:
                    continue
                X = geo.normalize(X)
                n2, s = len(X), geo.side_length(X)
                ms = [m for m in range(max(1, n2 - below), min(n2, 1000) + 1) if m in store_L]
                if not ms:
                    continue
                ex = min(s - store_L[m] for m in ms)
                if best is None or ex < best[1]:
                    best = (X, ex)
    return best
