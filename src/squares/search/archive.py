"""Contact-topology donor archive (P0).

Replaces coordinate-rounding-only dedup (packing_signature) with a topology
key so each n keeps 4-8 structurally different donors: winners + heterogeneous
topologies + near-miss warm states. Pure CPU, no GPU dependency.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

import numpy as np

from .structure import bands, candidate_pairs, normalize, separations, tilt


def topology_hash(packing: np.ndarray, eps: float = 1e-7) -> str:
    """Weisfeiler-Lehman (2 rounds) hash over the contact graph.

    Nodes: tilt bin (upright / tilt sign) + band id (-1 when not two-band).
    Edges: contact when signed SAT separation <= eps (touching or slight
    overlap); near edges are ignored so quench noise does not flip topology.
    """
    P = normalize(np.asarray(packing, dtype=np.float64))
    n = len(P)
    if n == 0:
        return hashlib.sha256(b"empty").hexdigest()
    if n == 1:
        return hashlib.sha256(b"single").hexdigest()
    t = tilt(P)
    node_tilt = np.where(np.abs(t) < 5.0, 0, np.where(t > 0, 1, -1)).astype(int)
    band_id = np.full(n, -1, dtype=int)
    try:
        found = bands(P)
        if len(found) == 2:
            for bid, (mask, _, _) in enumerate(found):
                band_id[mask] = bid
    except Exception:
        pass
    pairs = candidate_pairs(P)
    adj: list[set[int]] = [set() for _ in range(n)]
    if len(pairs):
        _, sep = separations(P, pairs)
        for (i, j), s in zip(pairs.tolist(), sep.tolist(), strict=False):
            if s <= eps:
                adj[int(i)].add(int(j))
                adj[int(j)].add(int(i))
    labels = [f"{a}:{b}" for a, b in zip(node_tilt.tolist(), band_id.tolist(), strict=False)]
    for _ in range(2):
        new_labels = []
        for v in range(n):
            neigh = sorted(labels[u] for u in adj[v])
            new_labels.append(labels[v] + "|" + ",".join(neigh))
        # compress to short stable ids
        uniq = {lab: f"{i}" for i, lab in enumerate(sorted(set(new_labels)))}
        labels = [uniq[lab] for lab in new_labels]
    labels.sort()
    deg = sorted(len(s) for s in adj)
    payload = (";".join(labels) + "#" + ",".join(map(str, deg))).encode()
    return hashlib.sha256(payload).hexdigest()


@dataclass
class Donor:
    key: str
    n: int
    topology_hash: str
    geometry_signature: str
    chain_depth: int = 0
    L_float: float = 0.0
    score_gain: float | None = None
    donor_kind: str = "near_miss"
    ancestry: list[dict] = field(default_factory=list)
    array_sha256: str = ""


class TopologyArchive:
    """Per-n capped archive: winners + heterogeneous topologies + near-miss.

    Policy: each n keeps at most max_per_n (default 8) donors:
      2 winners (largest gain) + 2异构topology + rest by smallest L.
    Same topology keeps at most 2 (smallest L + farthest seam).
    """

    def __init__(self, max_per_n: int = 8, explore_fraction: float = 0.2):
        self.max_per_n = max_per_n
        self.explore_fraction = explore_fraction
        self._by_n: dict[int, list[Donor]] = {}

    def add(self, donor: Donor) -> bool:
        lst = self._by_n.setdefault(donor.n, [])
        # exact geometry dup -> keep better L
        for i, d in enumerate(lst):
            if d.geometry_signature == donor.geometry_signature:
                if donor.L_float < d.L_float:
                    lst[i] = donor
                    return True
                return False
        lst.append(donor)
        self._evict(donor.n)
        return True

    def _evict(self, n: int) -> None:
        lst = self._by_n.get(n, [])
        if len(lst) <= self.max_per_n:
            return
        # group by topology, keep at most 2 per topology (smallest L first)
        by_topo: dict[str, list[Donor]] = {}
        for d in sorted(lst, key=lambda d: d.L_float):
            by_topo.setdefault(d.topology_hash, []).append(d)
        pruned: list[Donor] = []
        for donors in by_topo.values():
            pruned.extend(donors[:2])
        # rank: winners first, then smallest L; keep cap
        pruned.sort(
            key=lambda d: (
                0 if d.donor_kind == "winner" else 1,
                d.L_float,
            )
        )
        self._by_n[n] = pruned[: self.max_per_n]

    def sample_parents(self, n: int, k: int, exclude_family: set[str] | None = None) -> list[Donor]:
        lst = list(self._by_n.get(n, []))
        if exclude_family:
            lst = [d for d in lst if d.topology_hash not in exclude_family]
        # exploit winners + explore heterogeneous: interleave by topology rarity
        winners = [d for d in lst if d.donor_kind == "winner"]
        others = [d for d in lst if d.donor_kind != "winner"]
        out: list[Donor] = []
        i = j = 0
        # ~20% explore: every 5th pick from others-first ordering
        while len(out) < k and (i < len(winners) or j < len(others)):
            if len(out) % 5 == 4 and j < len(others):
                out.append(others[j])
                j += 1
            elif i < len(winners):
                out.append(winners[i])
                i += 1
            elif j < len(others):
                out.append(others[j])
                j += 1
            else:
                break
        return out

    def topology_counts(self, n: int) -> dict[str, int]:
        out: dict[str, int] = {}
        for d in self._by_n.get(n, []):
            out[d.topology_hash[:12]] = out.get(d.topology_hash[:12], 0) + 1
        return out

    def __len__(self) -> int:
        return sum(len(v) for v in self._by_n.values())
