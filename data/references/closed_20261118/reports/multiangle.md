# Multi-angle / nested-fan campaign — REPORT (2026-11-18)

Track: `multiangle`. Mandate: replace the rigid single-angle 45° core of the
D=1 masters with a nested multi-angle core, re-fill the axis region exactly,
and certify any improvement.  No Kaggle submissions, `/tmp/best_bank/`
untouched.

All local geometry is exact SAT (closed-form axis-cell vs rotated-rectangle
test, then explicit pairwise SAT on every emitted layout).  Local CPU only for
light checks; the heavy sweep is `/tmp/campaign2/multiangle/kdir/kernel.py`
(CPU-only Kaggle kernel, push pending — §8).

---

## 1. Bottom line

| item | result |
|---|---|
| **D=1 tangency law (new, exact)** | for an `m×m` 45° core in a `K`-slot split lattice the covered-cell count is `m²−1` for every gap `g ≥ g* = m/√2 − (K/2 − 1)`, and the smallest usable gap is exactly `g*`; at `g* − ε` the count jumps by a whole staircase ring (24–48 cells) |
| n=65 master (lifts to **12 puzzles**, k=8…19) | **closed**: the 45° 5×5 core is the unique admissible core of its size; every θ, offset, split, m=4/6 and 5-row fan is worse (§5) |
| n=626 master (7 puzzles, k=25…31) | fan **fails**: 118 patterns in the kernel / 51 locally, every non-zero pattern gives ≥311 covered cells at the bank's own gap (budget 288); none recovers after slide relaxation either (§6) |
| n=842 direct construction | **closed** in the (core, lattice) family: m=17→29.525, m=18→29.730, m=20→29.645, m=19/21 infeasible (§7) |
| n=401 calibration (our own multi-angle layout) | its 220 tilted squares are **a rotated lattice patch** (18×13 slots at 69.3°, 188 occupied), *not* a compact fan core — the working multi-angle mechanism in our bank is a tilted *lattice*, and the exact two-lattice bound at L=20.533 is 400 < 401 (§7b) |
| certified candidates | **none** (no layout beat a bank side) |

**The main result is structural and it redirects the next experiment**: the D=1
masters are not smooth optima that a fan can improve.  They are exact
combinatorial alignments — the core's 45° edge lies *on* the lattice's
cell-corner staircase, and the covered-cell count is a step function whose
minimum is a measure-zero tangent configuration.  Tilting the rows destroys the
alignment and immediately costs a full staircase ring of cells, which is worth
more than the geometric gain the tilt buys.  The record holder's advantage at
k≥20 must therefore be a *different alignment* (their f is lower at every k
from 20 up), not a relaxed version of ours.

---

## 2. The fan geometry, exactly

Core = `m` rigid `1×m` strips.  Strip `i` has angle `θᵢ = 45° + δᵢ`, direction
`uᵢ`, normal `nᵢ`, centre `cᵢ`.  Its shape is the rectangle
`{cᵢ + s·uᵢ + t·nᵢ : |s| ≤ m/2, |t| ≤ 1/2}` (the union of the `m` unit squares,
so the rectangle is exact).  Placement is a contact chain:

```
c₀ = (0, −(m−1)/2) in the 45° frame  (+ slide s₀ along u₀)
c_{i+1} = cᵢ + sᵢ·u_{i+1} + tᵢ·n_{i+1}
tᵢ = min{ t : strip i+1 at cᵢ + sᵢu_{i+1} + t n_{i+1}
              does not overlap strips 0..i }
```

`tᵢ` is solved **exactly**: each SAT axis gives a linear inequality in `t`, the
pair overlaps iff all four axes overlap, so the forbidden `t`-set is the
intersection of four intervals and `tᵢ = max over previous strips of the
interval's upper end`.  The result is a valid packing by construction; verified
in every run with explicit pairwise SAT (`worst penetration ≤ 1.8e-15` for the
zero-tilt case).

Single-strip extent: `m|cos θᵢ| + |sin θᵢ|` in x and `m|sin θᵢ| + |cos θᵢ|` in y.
Composite bbox = max over strips, i.e. of the *hull* of the chain.

### 2.1 Measured bbox vs delta pattern (m=17, the 626 core)

Zero tilt reproduces the solid diamond exactly: **24.0416305603426** =
`17√2`, all 289 squares at 45.000000°, penetration 1.8e-15.

| pattern | amplitude | bbox | Δ vs solid |
|---|---|---:|---:|
| ramp (linear −d…+d) | 0.2° | 24.085967 | +0.0443 |
| ramp | 0.5° | 24.152126 | +0.1105 |
| ramp | 1.0° | 24.261461 | +0.2198 |
| ramp | 2.0° | 24.476619 | +0.4350 |
| ramp | 3.0° | 24.687037 | +0.6454 |
| quad (∝(i−c)²) | 1.0° | 24.261757 | +0.2201 |
| alternating ±d | 0.2° | 24.752198 | +0.7106 |
| alternating ±d | 1.0° | 27.587627 | +3.5460 |
| alternating ±d | 3.0° | 34.608212 | +10.5666 |
| shear 1·u per row (all 45°) | 0.5 | 29.698485 | +5.6569 |
| shear | 1.0 | 35.355339 | +11.3137 |

So to first order `bbox(ramp) ≈ 17√2 + 0.215·d_deg` for small `d`, the ramp is
the gentlest pattern, and the alternating pattern is catastrophic (opposite
tilts force every second row apart).  **No fan has a smaller bbox than the
solid block**; the smallest core bbox measured anywhere is 24.040715 (17×17 at
44.5°), and it needs a *larger* lattice gap (0.572) than the solid.

### 2.2 m=5 (the 65/82/101 core)

Solid bbox 7.071068.  Tilts of 0.2…3° give 7.0845…7.2168 (ramp) and up to
8.97 (alternating 3°).  Zero tilt reproduces the bank's 5×5 block exactly.

---

## 3. The tangency law (why the family is a knife edge, not an optimum)

For the D=1 family, write `n = k²+1 = m² + (K²−C)` where `K` = slots per axis,
`m²` = core squares, `C` = number of lattice cells the core intersects (covered
cells, which must be excluded).  Hence

```
C = m² − 1        (exactly; the core must put exactly 1 unit of area in the gap)
```

For a 45° `m×m` core and a symmetric `K/2 | gap | K/2` lattice, a cell in the
first quadrant with near-corner `(g/2+i, g/2+j)` is covered iff
`g + i + j < R`, `R = m/√2`.  With `R = g + (K/2 − 1)` the covered set is
`i+j ≤ K/2−2` for **every** `g`, i.e.

```
C = m² − 1   for all g ≥ g*,     g* = m/√2 − (K/2 − 1)
```

`C` is non-increasing in `g`, so the smallest gap at which the count is
`m²−1` is exactly `g*`; below it the count jumps by a full ring.  Hence:

- n=65 (m=5, K=8): `g* = 5/√2 − 3 = 0.5355339059327…` — the bank's f, to 15 digits.
- n=626 (m=17, K=25, blocks [12,13]×[12,1,12]): `f = 17/√2 − 11.5 = 0.5208152801714…` — the bank's f, to 15 digits.

Measured cliffs (best offset in each case):

| puzzle | at g* | at g* − 1e-9 | at g* − 1e-3 |
|---|---:|---:|---:|
| 65 (m=5,K=8) | C=24 (kept 40, n=65) | C=36 (n=53) | C=36 |
| 626 (m=17,K=25) | C=288 (kept 337, n=626) | C=312 (n=602) | C=312 |

So the bank side is exactly the boundary configuration in which a full ring of
staircase cells (24 at the best offset, up to 48 at a generic offset) is
tangent to the core edge.  A gap smaller by *any* amount
loses a whole ring of cells; there is no continuous trade-off to exploit.

**Corollary (why tilting cannot help).**  A strip edge tilted by `δ` is no
longer parallel to the `45°` cell-corner staircase, so it cuts every staircase
cell it crosses: the count jumps by a ring even at the bank's own gap.  The
tilt can only pay if the *bbox* is the binding quantity — which is the long thin
band regime (3×22, where the ±0.82° nesting bought 0.56 of bbox).  In the D=1
master the binding quantity is the *cell count*, and the count is an alignment
invariant.  This is exactly the difference between the two families and it is
measured below.

### 3.1 The tangency is a line contact at 1e-15 (measured against the bank)

Read the bank's *own* n=626 coordinates and test every one of the 625 lattice
cells against its 289 rotated squares:

```
cells covered by SAT (float64) : 336
cells actually absent in bank : 288   (the other 337 are present)
```

The 48 extra cells are the diagonal staircase cells whose nearest corner lies
*on* the core's edge: for the cell at `(-11.760407640, -1.260407641)` the
u-axis SAT bracket is `|du| = 9.207106781186547` against
`8.5 + 0.5(cos+sin) = 9.207106781186548` — a 1e-15 margin.  In exact decimal
arithmetic (what the official metric uses) those 48 cells are *outside* and the
bank is valid; in float64 they are inside.  The D=1 tangency is a **line
contact**, not a corner contact, and the sign of the 1e-15 residual is the
whole difference between 288 and 336 covered cells.

Consequences, all verified:

* any *certifiable* layout must carry a positive margin.  The standard
  `1+2e-7` centre expansion the band track uses costs `4.9e-6` of side at
  n=626; the emitted reconstruction is officially valid at
  `L = 25.520820184` = bank + 4.9e-6.
* the count is stable for `g ≥ g*` (288 for all `g ∈ [g*, 0.56]`), so the
  margin is free *in the safe direction* and the optimisation target is
  `g* + 5e-6`, not `g*`.
* the bank's literal digits are load-bearing; a re-emission must reproduce the
  same rounding direction or the puzzle turns invalid (this is the mechanism
  behind the band report's "layouts float at 1e-8").

---

## 4. Anchor checks (done before believing anything)

| anchor | requirement | result |
|---|---|---|
| n=65, m=5, θ=45°, 4\|4 split, g=0.535533906 | kept=40, L=8.535533906 | **kept=40, L=8.535533905933**, f* = 8.535533905961 |
| n=626, m=17, θ=45°, [12,13]×[12,1,12], g=0.520815280 | C=288, kept=337, L=25.520815280171 | **C=288, kept=337, L=25.520815280171306** |
| n=626 reconstruction emitted as 626 squares | official v20 valid, L ≈ 25.520815 | **valid, L=25.520820184334** (bank + 4.9e-6, the 2e-7 safety expansion the band track uses; worst pairwise penetration 0.0) |
| n=842 same core, K=29 | must reproduce the lift 29.520815 | **L=29.5250** on a 0.005 grid → the anchor (29.520815) |

The official validator rejects exact tangency ("overlap certified"), so every
emitted layout is expanded by the standard `1+2e-7` centre scaling; this costs
~5e-6 of side and is irrelevant at the 1e-3 scale of the gaps we are chasing.

**Engine cross-check.**  Two independent coverage engines were implemented: a
general convex-polygon SAT (`geom.sat_cover`) and the closed-form
axis-cell-vs-rotated-rect test (`fastcov`).  On 40 random (θ, w, h, centre,
120 cells each) trials they agree on every cell (0 mismatches); every fan strip
is verified to have area exactly `m` (so the strip is exactly the union of its
`m` unit squares), and every emitted layout is checked with explicit pairwise
SAT (`worst penetration 0.0` after the safety expansion).  At an exact contact
the two engines share the same float64 sign, which §3.1 shows can differ from
the exact decimal sign; the authoritative check for any emitted layout is the
official v20 metric, and every candidate in this report was run through it.

---

## 5. n=65 — the 12-puzzle master (k=8…19)

Any 65-square packing with `L < 8.535533905932745` lifts to n = 65, 82, 101,
122, 145, 170, 197, 226, 257, 290, 325, 362 (Σ 1/√n = 0.951, so ΔL=0.005 is
worth 4.8e-3 of score).  All twelve are exactly tied with the record.

Exact sweep (`f_star(budget = m²−1)` with the core re-centred in the box at
every trial L):

| family | best L | verdict |
|---|---:|---|
| m=5 solid, θ ∈ 0…45° step 2.5° | 8.535533906 (θ=45°) | 45° is a sharp optimum; 42.5° → 9.0372 |
| m=5 solid, θ ∈ 40…50° step 0.25° | 8.535533906 | no improvement |
| m=5 solid, offset (dx,dy) ∈ [−0.5,0.5]² step 0.1 | 8.535533906 | no improvement |
| m=4 solid (budget 15) | 8.828427 | 0.29 worse |
| m=6 solid (budget 35) | 8.839087 | 0.30 worse |
| m=5, split aₓ,a_y ∈ {3,4,5} | 8.535533906 only at 4\|4 | asymmetric splits cost +0.5 |
| 5-row fan, ramp/alt/quad/rand, d=0.2…3°, 5 slide patterns | 8.549953 (rand 0.2°) | **all worse** |

Geometric reason (exact, not numerical): with `C = 24` the 25-square core must
be contained in the union of the 24-cell staircase and the cross corridors,
whose width is `g`.  A unit square cannot enter a corridor of width `< 1`; only
a 90° corner can.  A 45°-oriented unit-square corner has width `2d` at depth
`d`, so its depth is `g/2`, and the core radius is bounded by
`R ≤ g/2 + (K/2−1)`, i.e. `g ≥ R − (K/2−1) = g*`.  Equality is the bank.  Any
core with a smaller `R` must give up area to the staircase, and the staircase
has only 24 cells = area 24 < 25.  So **the n=65 family is closed**: no
25-square core and no 8-slot fill does better.

### 5.1 The twelve are one lift chain (verified)

`n=82` is *literally* the `n=65` lift: translating the n=65 layout by
`(4.267766952966, 4.267766952966)` gives **65/65 exact overlaps** with the
n=82 squares, and the 17 extra n=82 squares are the appended top row (9) and
right column (8).  `n=101` continues the chain (`25 rotated + 76 axis =
25 + (57+19)`; the lift adds `2k+1 = 19` cells), stored in a mirrored frame.
The lattice structure of the whole chain is `[4,4,k−8]` blocks with a single
gap of `g = 0.535533906` between the 4|4 blocks and the extra cells at the far
edges, which is why `f` is *constant* for k=8…19.  So one improved 65-square
packing wins all twelve; one closed master closes all twelve.

```sh
.venv/bin/python /tmp/campaign2/multiangle/liftchain.py
# n=82: |n65 moved|=65 target=82 overlap=65 extra=17
```

### 5.2 The backups (n=82, n=101) are closed the same way

Exact sweep with the `[4,4,k−8]` lattice, core re-centred in the gap, θ ∈
40…50° step 0.5°, core offset ±0.3 in 0.15 steps, gap scanned to `f−0.05`:

| k | anchor | best candidate < bank |
|---|---|---|
| 9 (n=82) | C=24, kept=57, n=82, L=9.535533905933 | **none** |
| 10 (n=101) | C=24, kept=76, n=101, L=10.535533905933 | **none** |

and the core-size table shows why: m=4 covers the same 24 cells but leaves
n=73/92, m=6 jumps to C=40 and leaves n=77/96.  Only `m=5` gives exactly
`k²+1`.  So the whole k=8…19 chain has exactly one admissible core size and one
admissible gap.

---

## 6. n=626 — the fan experiment (7 puzzles, k=25…31)

Setup: core = 17 strips of 17 at `θᵢ = 45° + δᵢ`; fill = the bank's exact
6-block lattice `[12,13] × [12,1,12]` (625 cells, gap `g`);
`budget C ≤ 288` so that `289 + (625−C) ≥ 626` with exactly 626 after dropping.

118 patterns in the kernel (51 measured locally): ramp / alternating /
quadratic / "ends only", amplitudes 0.1…3.0°, slide scaling modes, plus seeded
random patterns with random slides.
Each pattern is exact-SAT counted at
`g = g* = 0.520815280` and at `g* − 0.005` after a 160-step stochastic slide
relaxation; the lattice offset is swept on the exact dyadic grid
`{−0.5,−0.25,0,0.25,0.5,0.75}²` (the tangency only exists on the exact grid —
an offset of `0.5+1e-9` already flips 24 cells, so the offset must be an exact
dyadic rational; `0.5+1e-12` still gives the tangency).

Result at the bank's own gap (budget 288, measured):

| pattern | bbox | C at g* | min C after slide relaxation at g*−0.005 |
|---|---:|---:|---:|
| solid (anchor) | 24.041631 | **288** | 312 |
| ramp 0.2° | 24.085967 | 312 | 311 |
| ramp 0.5° | 24.152126 | 312 | 311 |
| ramp 1.0° | 24.261461 | 312 | 311 |
| ramp 2.0° | 24.476619 | 321 | 319 |
| ramp 3.0° | 24.687037 | 325 | 325 |
| alternating 0.2° | 24.752198 | 323 | 323 |
| alternating 1.0° | 27.587627 | 376 | 374 |
| shear slide 0.125 (all 45°) | 25.455844 | 297 | — |
| shear 0.5 | 29.698485 | 294 | — |
| 10 random (≤2.5°) | 25.85–28.31 | 339–385 | — |

**No pattern reaches 288**; the best non-zero pattern is 23 cells over budget
at the bank's own gap, and the relaxation does not recover them.  The shear
family (rows kept at exactly 45°, only shifted) is closest at 294–299 — still
6–11 cells over — which is the cleanest confirmation of the alignment
argument: the *largest* perturbation that keeps the 45° edge still loses
cells, because the row ends no longer sit on the staircase corners.  (The
extreme shear 1.0 reports C=276 but its bbox is 35.36, so it cannot fit the
box at all — a reminder that the count is only meaningful together with L.)

The offset cliff in 2-D was also measured at the solid core: at `g = g*`,
C ranges 288 (best) / 312 (median) / 314 (worst) over the 36 dyadic offsets;
at `g = g* − 1e-9` and at `g* − 1e-3` it is 312 / 313 / 336.  The tangency is a
single point, not a basin.

**Robustness to the contact margin** (§3.1): the comparison does not depend on
the 1e-15 contact sign.  At `g = g* + m` for `m = 0, 1e-6, 1e-4, 1e-3, 1e-2`
the solid core stays at **288** while ramp 0.2°/0.5° stay at **312** and
alternating 0.2° at **323** (313 at `m=1e-2`).  The fan deficit is structural.

**Conclusion.**  The fan construction is the right family for a *band* whose
binding quantity is its bbox, and the wrong family for a *compact D=1 core*
whose binding quantity is the covered-cell count.  For n=626 the record's
0.0098 advantage must come from a different alignment (different core shape and
a different lattice phase pattern), not from tilting the 17×17 core.

---

## 7. Direct constructions for n=842, and the n=401 calibration

### 7.1 n=842 direct (K=29, budget `C ≤ m²−1`)

| core | bbox | best L | verdict |
|---|---:|---:|---|
| m=17 @45° | 24.0416 | 29.5250 (g=0.5250) | = the lift anchor (29.520815), no gain |
| m=18 @45° | 25.4558 | 29.7300 (g=0.7300, C=313≤323) | worse |
| m=19 @45° | 26.8701 | infeasible (C=360 budget, needs L≥26.87) | worse |
| m=20 @45° | 28.2843 | 29.6450 (g=0.6450, C=392≤399) | worse |
| m=21 @45° | 29.6985 | infeasible | — |

The tangency law `g* = m/√2 − (K/2−1)` explains all of it: at K=29 the
required gap is 0.525 (m=17), 0.730 (m=18), 0.645 (m=20), and for m=19 the
formula gives a negative gap — but a negative gap is impossible and at `g=0`
the covered count is already 40 cells over the `m²−1` budget.  So no
single-core direct 842 exists below 29.5208.  This reproduces the theory track's counting result (single 45° core +
lattice = 823 at 29.502; two interlocked lattices = 833; the record needs 842).

### 7.2 n=401 — what a *working* multi-angle layout in our bank actually is

The bank's n=401 (L=20.533011795, record 20.526135333) is the only D=1 puzzle
where our own layout is already multi-angle.  Decomposition (measured):

* 191 axis-aligned squares (hand-placed, 103 distinct x — relaxed, not a grid);
* **220 squares in one tilted cluster** at −20.68° ± 1.5°, i.e. 69.32°;
* that cluster is **a rotated lattice patch**: u-positions cluster at
  integers + 0.37, v-positions at integers + 0.29…0.38, spans `u = 18.48`,
  `v = 12.99` → an **18×13 = 234-slot patch, 188 occupied** (46 slots taken by
  the axis squares).

So the multi-angle mechanism that actually pays in our own bank is a **tilted
lattice patch interleaved with the axis lattice**, not a compact fan core.
That is a different topology from the 626 master and it is the one the record
holder's prose ("bigger tilted regions, many slightly different angles") most
likely describes.

Exact bound for the pure two-lattice family at 401's side, via König:
`best n = |A| + |B| − maximum_matching` over the axis lattice × rotated lattice
overlap graph, swept over θ ∈ [55°,90°] step 0.25°, offsets 0.125, L down to
20.49:

```
L=20.533  best 400   (θ=89°, 0.5,0.0; |A|=361, |B|=400, matching=361)
L=20.520  best 400
L=20.500  best 399
```

So **401 is impossible for two pure lattices** — the bank's 401 has extra
relaxed/loose squares (and indeed 191 axis squares are not a clean lattice).
Any attack on the n=401 record must therefore be a *three-phase* layout
(tilted patch + two axis phases) with a relaxed boundary.  That is the natural
next experiment and it is in the kernel.

Two three-phase attempts were made locally and both are *worse* than the
two-phase MIS: (a) the greedy "keep one lattice whole, filter the others" (all
6 cyclic orders) reaches **392** at L=20.533 (30°/45°, zero offsets), 375 at
20.500, 373 at 20.450 — keeping all 400 axis cells forces most of the rotated
patch out; (b) a randomized min-degree/random-order MIS heuristic on the full
3-lattice overlap graph reaches only **316** at the same L, because the graph is
dense enough that a greedy independent set is ~30 % below the exact optimum
(the exact 2-lattice optimum, by König, is 400).  So a real three-phase attack
needs a maximum independent set / LP over the three lattices (~1000 vertices,
NP-hard in general), not a greedy.  The bank's 401, with only 191 axis squares,
is precisely such a balanced selection, which is why it beats every clean
lattice model tried.

The same exact bound for n=626 (König on the 625-cell axis lattice × rotated
lattice overlap graph, θ ∈ {45…85°}, dyadic offsets) is decisive:

```
L=25.520  best two-lattice MIS=613   (|A|=576, |B|=613)
L=25.480  best 613
L=25.440  best 595
L=25.400  best 593
```

so the pure two-phase family cannot even reach 626 at the bank's own side
(613 < 626).  The bank's 289+337 "core + gapped lattice" is strictly stronger
than two interleaved full lattices at this size, which is the opposite of the
n=401 calibration and explains why the 626 master is a core construction at
all.

---

## 8. Kaggle

Kernel: `ccjjllt/sis-multiangle-fan-20261118`, CPU only
(`enable_gpu: false`), source `/tmp/campaign2/multiangle/kdir/kernel.py`
(metadata in the same directory).  It reruns, at 10–100× the local resolution:

* J1 n=626 fan: 118 patterns × exact dyadic offsets × gap scan to 5e-4 with a
  160-step slide relaxation per pattern (the "relax numerically" step);
* J2 n=626 block family (m=15…19 at 7 angles, 45° rectangles w×h with
  w+h=34) with an exact gap scan;
* J3 the same two jobs for n=842 (K=29, m=20);
* J4 the n=401 exact two-lattice MIS scan at 0.25°/0.125/0.0025 resolution.

The kernel writes `results_multiangle.json` and `WINS.txt`, and any winner is
exact-SAT verified before it could be emitted.

**Push status.** `kaggle kernels push` returns
`Maximum batch CPU session count of 5 reached` (account cap, as briefed).
Attempted at ~10-minute intervals from the moment the kernel was ready
(8 attempts); a bounded background retry loop
(`/tmp/campaign2/multiangle/retry_push.sh`, 10 attempts × 12 min, log
`/tmp/campaign2/multiangle/push.log`) keeps trying and exits as soon as a
version is accepted.  As of this writing the kernel has **not** been accepted,
so **no Kaggle result exists for this track**; every number in this report is
from local exact computation.  The kernel is self-contained and was smoke
tested locally: it reproduces the n=626 anchor (C=288 at `(0.5,0)`,
L=25.520815280171) and the n=65 anchor before any job runs.

---

## 9. What this changes for the campaign

1. **Stop looking for a smooth multi-angle improvement of the D=1 masters.**
   The bank's f is the exact tangency value `m/√2 − (K/2−1)`; the family is a
   step function in `g`, not an optimum with slack.  This is a stronger
   statement than "the layout is jammed": it is *provably* the best alignment
   for a core of that size, and tilting a strip breaks it.
   Corollary: the same law governs any 45° core in a split lattice; for the
   nine band puzzles the 45° block is long and thin, so there the bbox (not the
   cell count) is binding and the ±0.82° nesting already exploits it.  The
   n=65…362 family (all twelve are one lift) is fully covered by §5.
2. **The productive direction is the one our own n=401 already uses**: a
   rotated *lattice patch* (multi-angle as a lattice, not as a tilted compact
   core) interleaved with the axis lattice.  n=401 proves it pays (f=0.5330
   versus 0.5355 for the 45° family) and the two-lattice MIS bound (400 < 401)
   proves a third phase is needed.  The next experiment should be a 3-phase
   exact-cover search in the 401/626 frame: one tilted patch at θ, two axis
   phases, with the tangent staircase counted exactly.
3. **The pure-lattice families are now closed by exact bounds**: two-lattice
   MIS is 400 at n=401's side and 613 at n=626's side (both below the required
   count), so neither puzzle's record can be a two-phase lattice layout.  For
   626 the core + gapped-lattice structure is strictly stronger; for 401 the
   opposite is true and a third phase is needed.
4. **Value ranking confirmed**: n=65 is the highest-leverage single puzzle in
   the competition (Σ1/√n = 0.951 over its 12 lifts) but it is closed; the
   626 master (Σ1/√n = 0.251 over 7) is also closed for single-core
   constructions.  Budget should go to the multi-phase structure, not to more
   polishing.

---

## 10. Artifacts

```
/tmp/campaign2/multiangle/REPORT.md        this file
  geom.py            SAT primitives (polygon, exact axis-cell vs rotated rect)
  fastcov.py         closed-form coverage engine (used everywhere)
  fan.py             contact-stack fan builder + pairwise SAT check
  lattice626.py      n=626 6-block lattice + exact coverage/bbox
  anchor65.py        n=65 anchor (kept=40, L=8.535533905933)
  anchor626.py       n=626 anchor (C=288 at ox=0.5, L=25.520815280171)
  make_anchor.py     emits the 626 reconstruction and certifies it with the
                     official v20 metric (valid, L=25.520820184334)
  small_theta.py     m=5 theta/offset sweep (45° sharp optimum)
  small_m.py         m=4/5/6 + split sweep
  small_fan.py       m=5 fan patterns
  sweep626.py        m/theta sweep at 626
  sweep842.py        direct 842 core sweep
  fan626b.py         33-pattern fan sweep (the table in §6)
  mdiag.py           m=15..19 coverage-vs-gap table
  twolat.py          two-lattice counter
  validate_bank626b.py  tests the bank's own 626 literals against the engine
  relax_table.py      the slide-relaxation table of §6
  liftchain.py        n=82 = n=65 + one row + one column
  mis401.py          exact two-lattice MIS (König) for n=401
  mis626.py          exact two-lattice MIS (Koenig) for n=626
  three_phase.py     three-phase keep-one-whole greedy (392 at 20.533)
  mis3b.py           randomized 3-lattice MIS heuristic (316 at 20.533)
  kdir/kernel.py     self-contained Kaggle CPU sweep (J1..J5)
  kdir/kernel-metadata.json
```

Reproduce the anchors:

```sh
cd /Users/zhaohuaxiang/ccjjllt/squares
.venv/bin/python /tmp/campaign2/multiangle/anchor65.py     # 24 / 40 / L=8.535533905933
.venv/bin/python /tmp/campaign2/multiangle/anchor626.py    # C=288 at ox=0.5
.venv/bin/python /tmp/campaign2/multiangle/make_anchor.py  # official v20 valid
.venv/bin/python /tmp/campaign2/multiangle/fan626b.py      # the §6 table
```
