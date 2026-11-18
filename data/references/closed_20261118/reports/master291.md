# n = 291 (k=17, D=2) — exact family closure and the two-core lattice

Track: `master291`. Target: find any 291-square packing with `L < 17.53553390593279`
(the bank value, which ties the public record `17.53553390593273`).

Bank used for the analysis: `/tmp/best_bank/submission.csv`,
SHA-256 `9c981e6ea9a44c076587256936948e636936a84ad0668af6b75e946f4fa527e9`,
score 22.128441824806618 (never modified by this track).

While this track ran, other tracks advanced the live bank to
SHA-256 `bb6d5f2a1eeccf457f3b97ad6c06d09103bff594e04c73966a2fc3dc6fc5086f`,
score 22.128396684529527. **The n=291 group is byte-identical in both** (241 axis +
50 at 45°, bbox `17.53553390593279`), so every n=291 conclusion holds, and the lift +
merge in §7 was re-run against the *live* bank as well (same result: 0 changed puzzles).

---

## 1. Bottom line

| | |
|---|---|
| Bank's n=291 layout | **exactly reproduced in closed form** (§2), n=291, L = `14 + 5√2/2` |
| Lay-out optimum for that core pair | **241 axis squares is the exact MILP maximum** over the 2-offset 4-phase lattice at that L (not just "found") |
| Alternative core arrangements (20 distinct, 22 rows) | **all need L ≥ 18.0** — a 0.464 deficit, not a near miss (§4) |
| Two-offset lattice phase sweep | min L over the whole family is `17 + f`, attained **only** at `f = 5√2/2 − 3` (§5) |
| One more square anywhere? | **no** — 0 admissible placements over 90 angles × 0.02 grid (§6) |
| Best verified 291 L | **17.535533905932738** (= bank, tie with record) |
| Lifted candidate | built and certified through `squares merge` — **net gain 0.0** (tie), pipeline verified (§7) |
| Kaggle SA kernel | `ccjjllt/sis-sa291-20261118` v1 errored after 3.5 s on a packaging bug (`anneal_core` imported as a module that was concatenated into the script) — that slot produced nothing; a second session `sis-sa291b-20261118` ran 19:46–21:13Z and then became inaccessible (no output downloadable); the corrected build is smoke-tested and ready in `kdir/`, pushes blocked by the 5-session CPU cap (§8) |

`f = L − k = 5√2/2 − 3 = 0.5355339059327378` is a clean algebraic number, and the whole
layout is exactly rigid: the reproduction below matches the bank's coordinates to 6e-14
with **zero** overlapping pairs.

---

## 2. Exact closed-form reproduction of the bank's n=291

Code: `/tmp/campaign2/master291/repro.py` (prints `axis cell sets identical: True`,
`core cell sets identical: True`, `pairwise SAT min separation = -4.6e-14`, `overlapping pairs = 0`).

```
L = 14 + 5*sqrt(2)/2 = 17.535533905932738
f = L - 17          = 5*sqrt(2)/2 - 3 = 0.5355339059327378
```

**Core — 50 squares at exactly π/4.** In rotated coordinates
`u = (x+y)/√2`, `v = (x−y)/√2` they are two solid **5×5** grids (axis-aligned in (u,v)):

| block | u range | v range |
|---|---|---|
| B1 | `[5/√2, 5/√2 + 5]` = `[3.5355339, 8.5355339]` | `[−2.5, 2.5]` |
| B2 | `[23/√2, 23/√2 + 5]` = `[16.2634560, 21.2634560]` | `[−2.5, 2.5]` |

Everything is algebraic: `u0(B1) = 5/√2`, `u0(B2) = 23/√2`, so the u-gap is
`d = 18/√2 − 5 = 9√2 − 5 = 7.727922061357855` and the two block **centres are exactly
`(9, 9)` apart in (x, y)** (`u`-separation `9√2`).

**Axis — 241 squares on the four-phase lattice** `x, y ∈ {i+½} ∪ {i+½+f}`.
Writing phase `(px,py)` for `x = i+½+px·f, y = j+½+py·f`, the cell set is exactly

```
(0,0)  4x4 corner triangles        j=0..3 :  i in [0, 3-j]
                                   j=9..12:  i in [9, 21-j]
(0,1)  lower-left triangle         j=4..7 :  i in [0, j-4]
                                   j=8    :  i in [0, 7]
                                   j=9..12:  i in [0, 8]
                                   j=13..16: i in [0, j-4]
(1,0)  middle band + NE triangle   j=0..3 :  i in [4+j, 16]
                                   j=4..8 :  i in [8, 16]
                                   j=9..12:  i in [13+(j-9), 16]
(1,1)  two off-diagonal triangles   j=4..7 :  i in [11-j, 7]
                                   j=13..16: i in [29-j, 16]
```

Counts 20 + 100 + 101 + 20 = **241**. Bounding box is exactly `17.535533905932738`
square, so `n = 291 ≤ L² = 307.495`.

Why the layout works: the axis lattice is a **perfect diamond tiling in (u,v)**
(a unit square at `(i+½,j+½)` maps to a 45° diamond of area 1 with covolume 1).
The two 5×5 blocks are therefore *exactly* the set of diamond cells they cover, and the
"staircase waste" around each block is the (thin) part of the removed diamonds lying
outside the block. That waste is thinner than a unit square in every direction, which is
verified exactly, for all 90 orientations, by the free-region scan in §6.

---

## 3. The exact free-region / capacity counter

Two independent tools, both in this directory:

* `geom.py` / `model.py` — angle-aware SAT (4 separating axes, exact for convex polygons),
  box tests, block geometry, 4-phase candidate generation.
* `milpfill.py` — **exact** maximum number of axis-aligned unit squares that fit in
  `[0,L]²` clear of the fixed 45° cores, restricted to the four-phase lattice
  `{i+a} ∪ {i+a+s}` per axis (all four phase combinations allowed).
  Formulated as a set-packing MILP over clique covers (a column's y-slots and every
  column pair with `Δx<1` are interval graphs, so maximal cliques give the exact
  conflict constraints). Solved with HiGHS via `scipy.optimize.milp`; every solve below
  returned `status = 0` (optimal) with `dual_bound = incumbent`, typically in 0.03–0.2 s.
* `gridmilp.py` — the same model on an arbitrary fine grid (used for the sanity bound in §6).

Validation: with the bank's two cores at `L = 17.53553390593279`, `a = 0.5`, `s = f`,
the MILP returns **241**, i.e. it reproduces the bank's axis count *as the proved maximum*,
not merely as a feasible value.

---

## 4. Family table — minimal L for n = 291

Method: for each core arrangement the cores are translated as a rigid group over a 7×7
placement grid **restricted to placements that keep the whole core group inside
`[0,L]²`** (this check matters — see the note below), the lattice offset is swept over
`s ∈ {0.50, 0.52, f, 0.56}` with the lattice flush (`a = 0.5`), and the *exact* capacity
is computed at three box sides. `cap` = exact axis-square maximum; `target` = `291 − n_core`;
"—" = the core group's own bounding box does not fit at that L (so the row is
geometry-limited, not capacity-limited).

| arrangement | n_core | target | cap @ 17.5355339 | cap @ 17.99 | cap @ 18.001 | minimal L |
|---|---:|---:|---:|---:|---:|---:|
| **two 5×5, d = 9√2−5 (bank)** | 50 | 241 | **241** | 241 | 246 | **17.535533905932738** |
| two 5×5, d = 9√2−5, any *other* placement | 50 | 241 | 233 | 233 | 246 | ≥ 18.0 |
| two 5×5, d = 5.0 | 50 | 241 | 234 | 235 | 246 | 18.0 |
| two 5×5, d = 6.5 | 50 | 241 | 236 | 236 | 246 | 18.0 |
| two 5×5, d = 9.0 | 50 | 241 | — (bbox 17.70) | 237 | 246 | 18.0 |
| two 5×5, d = 9.5 | 50 | 241 | — | — | — | ≥ 18.06 (bbox) |
| two 5×5, d = 7.0, v-shift 1.0 | 50 | 241 | 233 | 234 | 246 | 18.0 |
| two 5×5, d = 7.0, v-shift 2.0 | 50 | 241 | — (bbox) | 233 | 246 | 18.0 |
| **solid 5×10** (blocks merged) | 50 | 241 | 237 | 237 | 254 | 18.0 |
| 10×5 rectangle | 50 | 241 | 237 | 238 | 254 | 18.0 |
| one 5×5 | 25 | 266 | 265 | 265 | 285 | 18.0 |
| two 4×4, d = 4 | 32 | 259 | 250 | 247 | 275 | 18.0 |
| two 4×4, d = 6 | 32 | 259 | 253 | 254 | 276 | 18.0 |
| two 4×4, d = 4, v-shift 2 | 32 | 259 | 250 | 252 | 274 | 18.0 |
| three 4×4 | 48 | 243 | — (bbox 17.56) | 233 | 247 | 18.0 |
| fan 5×5 + 4×4 | 41 | 250 | 241 | 241 | 259 | 18.0 |
| fan 5×5 + 3×3 | 34 | 257 | 250 | 250 | 268 | 18.0 |
| fan 5×5 + 5×4 | 45 | 246 | 237 | 237 | 255 | 18.0 |
| 6×5 rectangle | 30 | 261 | 258 | 258 | 280 | 18.0 |
| 4×6 rectangle | 24 | 267 | 232 | 232 | 254 | > 18.0 |
| 6×4 rectangle | 24 | 267 | 234 | 235 | 253 | > 18.0 |
| 6×6 minus a corner | 35 | 256 | 249 | 251 | 276 | 18.0 |

**Validity note (a bug I found and fixed).** The first version of `family.cap` only
required the core group's bounding-box *size* to be ≤ L, not its *position* — a 5×10
block at `v0 = −2.5` hangs below `y = 0` unless translated up by 2.803, and one
placement sweep did exactly that and reported a spurious `cap = 242` at `L = 17.5`
(i.e. 292 squares). With the position constraint added, that arrangement gives 237 at
`17.5355` → `min L = 18.0`. All the numbers above are from the corrected code
(`family.cap` + `family.best_cap`, `family_final.py`), and the bank row is unchanged.
Every core arrangement in the table is also verified to sit fully inside `[0,L]²`.

Because capacity is a *step function*, a coarse L-sample could in principle miss a
narrow spike like the bank's. I therefore re-scanned the four closest alternatives
(`6×5`, `6×6−corner`, `fan 5×5+4×4`, `two 4×4 d=6`) at `L = 17.56, 17.60, 17.65, 17.70,
17.75, 17.80, 17.85, 17.90, 17.95`: they stay flat (258/249-251/241/253-254), never
reaching their targets (`scan_gap.log`). There is no second spike.

Two robust facts:

1. **Nothing except the bank's own arrangement reaches its target below L = 18.0.**
   The two 5×5 family is not merely "tight", it is a spike: every other separation
   (`d = 5, 6.5, 9, 9.5`), every v-shift, the merged 5×10 block, and every different
   core shape loses 1–34 squares at the bank's L.
2. **Everything becomes feasible at L = 18.0** (the next lattice line, `17 + 1`), where
   the capacity jumps by 5–35 squares. So the family's second-best option is
   `L = 18.0` — **0.464 worse**, not 1e-3.

The "18.0" column also explains why: capacity is a *step function of L* that only jumps
when a new lattice row/column becomes admissible, i.e. at `L = 17+f` and `L = 18`.
There is no continuous middle ground.

This reproduces, at n=291, the same phenomenon the sibling track found for n=65:
the solid two-block 45° family is **closed with a sharp cliff at exactly the bank's gap**.

---

## 5. The phase sweep — the cliff is exactly at `f = 5√2/2 − 3`

`milpfill` with the bank's cores, `a = 0.5`, both lattice offsets equal to `s`,
box side pinned at `L = 17 + s` (both lattices flush):

| s | L | cap |
|---|---|---|
| 0.400 … 0.520 | 17.40 … 17.52 | 217 |
| 0.53553390 (f − 1e-5) | 17.5355239 | **217** |
| **0.535533905932738 (f)** | **17.535533905932738** | **241** |
| f + 1e-5 | 17.5355439 | 241 |
| 0.54 … 0.70 | 17.54 … 17.70 | 241 → min L = 17+s |

and scanning `s` from 0.518 to 0.538 in 5e-4 steps the only change is
`217 → 241` between `s = 0.5355` and `s = 0.5360`. Refining to 1e-5 pins the jump at
`s = f` to within 1e-5. **The 24-square gain that makes 291 possible exists only at
exactly `s = f`, i.e. exactly at the bank's side.**

Full 2-D sweep over both the lattice origin `a` and the phase `s` at `L = 17+f`:

| s \ a | 0.50 | 0.55 | 0.60 | 0.65 | 0.70 | 0.80 | 0.90 | 1.00 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **f** | **241** | 209 | 209 | 209 | 209 | 209 | 209 | 209 |
| 0.55 | 211 | 209 | 209 | 209 | 209 | 209 | 209 | 209 |
| 0.60 | 211 | 209 | 209 | 209 | 209 | 209 | 209 | 209 |
| 0.65 | 211 | 209 | 209 | 209 | 209 | 209 | 209 | 209 |
| 0.70 | 211 | 209 | 209 | 209 | 209 | 209 | 209 | 209 |

`(a, s) = (0.5, f)` is the unique maximum; a 0.05 shift in the lattice origin costs 32
squares. Independently, an origin sweep at `L = 17.5` (a ∈ 0.50…1.50 × s ∈ 0.50…0.60)
caps out at **217**, so no admissible lattice reaches 241 at any smaller side.

---

## 6. Is one more square possible anywhere? (angle-aware free-region scan)

`voidscan.py` computes, for every angle θ ∈ [0°, 90°) and a 0.02 centre grid, the
region of admissible centres of an extra unit square by rasterising the union of the
Minkowski octagons `O_k ⊖ S(θ)` and intersecting with the box constraint.

Result at the bank's L: **0 admissible centres over all 90 angles** (and 0 at a coarse
0.04 grid for 0°/30°/45° as well). The 16.49 units of waste area (`L² − 291`) are
entirely slivers thinner than `1/√2`; there is no hole a unit square of *any*
orientation can occupy. Removing the 16.49 is not an insertion problem.

Related negative: in (u,v) the axis squares are a *perfect* diamond tiling, so the
staircase region around a 45° block has width `< 1` and cannot host a 45° square either.

## 6b. Fine-grid capacity bound (why "more offsets" does not help)

`gridmilp.py` on the bank's cores:

| grid | offsets effectively available | max axis @ L = 17.5355 |
|---|---|---:|
| step 0.50, off 0.0 (2 offsets {0, 0.5}) | 2 | 217 |
| step 0.25, off 0.0 (4 offsets) | 4 | 217 |
| step 0.25, off 0.25/0.5/0.75 | 4 | 209 |
| step f/2 (≈65 offsets, dense) | many | 200 |

Adding lattice offsets **lowers** the capacity: every extra column within `Δx < 1`
forces its y-set to be disjoint from its neighbours', and with 3+ mutually conflicting
columns per unit you need 4 disjoint y-partitions out of 17 rows. The two-offset
`{0, f}` configuration is the only one that partitions cleanly. (A fine grid cannot
represent the bank's layout at all — `f` is irrational — so these rows are upper
bounds for *other* lattices, not for the bank's.)

A pure axis-lattice upper bound: with no cores, axis-parallel unit squares in `[0,L]²`
number at most `⌊L⌋² = 289`, and the two 45° diamonds (area 50) block at least 50 of
those cells, leaving ≤ 239 from the `17×17` core, plus the two border strips of width
`f` supplied by the second phase — which is exactly how the bank reaches 241.

---

## 7. Best verified 291 layout, lift and certification

* `master291.csv` — the closed-form layout of §2 (291 rows `x,y,angle`).
* Verification (`repro.py`): `n = 291`, `L = 17.535533905932738`,
  pairwise SAT min separation `−4.6e-14` with **0** overlapping pairs,
  `291 ≤ L² = 307.495`.
* Lift: `python /tmp/campaign2/lift.py --master master291.csv --k0 17 --D 2 --ks 17 18 19 20 21 22 23 24`
  → `gadget w=17 h=17 D=2 f=0.535533905932738 n0=291`, 3420 rows
  (`n = 291, 326, 363, 402, 443, 486, 531, 578` at `L = k + f`).
* Certification:
  `.venv/bin/python -m squares merge --baseline /tmp/best_bank/submission.csv --baseline-report /tmp/best_bank/report.json --candidate lift291.csv --output-dir merge_test`
  → `changed_puzzles: []`, `net_gain: {text: 0.0, float64: 0.0}`,
  output SHA-256 identical to the baseline. Repeated against the live bank
  (`bb6d5f2a…`, 22.128396684529527): `--output-dir merge_test_live`, same result.
  **The pipeline is verified end-to-end**: it rejects a tie and will accept any strict
  improvement.

The exact algebraic value `17.535533905932738` is 5e-14 *below* the bank's stored
`17.53553390593279` (CSV rounding), i.e. the reproduction is at the algebraic optimum
of the construction, not an approximation. That difference is far below the merge
threshold and changes nothing.

---

## 8. Fixed-side annealing (Kaggle CPU)

Kernel: `ccjjllt/sis-sa291-20261118` (`enable_gpu: false`, no external data).
Design: 291 squares × 3 DOF (x, y, θ), fixed side, exact 4-axis square-square SAT
penetration with a numba neighbour list, Metropolis on `Σ depth² + Σ wall²`, with
single-square moves **and rigid group moves** (the 45° core block and the four lattice
phase groups) so that whole sub-structures can translate/rotate.
Side ladder 17.5355 → 17.5350 → 17.5340 → 17.5330 → 17.5300 → 17.5250 → 17.5200 →
17.5100 → 17.5000, 3 bank seeds + 1 random 2-core construction per rung, 4 workers.

Status log (facts only):

| when (UTC) | what |
|---|---|
| 19:37 | push of v1 accepted (orchestrator freed a slot) |
| 19:40 | v1 **ERROR after 3.5 s**: `ModuleNotFoundError: No module named 'anneal_core'` — the numba core had been concatenated into `kernel.py` but the worker still `import`ed it as a module. Log: `out/sis-sa291-20261118.log`. **That slot produced no result.** |
| 19:41→ | fixed build (functions used in-module, random-seed generator also repaired) smoke-tested locally end-to-end at reduced size: 4 tasks, 2 workers, bank seed reproduces `E=0` at `L=17.5355`, near-miss at `L=17.53` (`E=6.2e-5`) |
| 19:46–21:13 | an unrelated session keyed `ccjjllt/sis-sa291b-20261118` was observed `RUNNING` by the watcher; it then became inaccessible (`Permission 'kernels.get' was denied`) and no output could be downloaded |
| every push since | rejected: `Maximum batch CPU session count of 5 reached` (retried ~10 times at 10–15 min intervals) |

The corrected build is at `/tmp/campaign2/master291/kdir/`
(`kernel.py` 20 257 B + `kernel-metadata.json`), self-contained (no dataset sources, no
internet), 4 workers. Ready to push as soon as a slot frees.

### 8.1 E-vs-L curve (local, bank seed, independent re-verification)

`curve.py` — bank layout as seed, fixed number of single-square Metropolis moves per
rung (≈45.6M moves, ~8 s), `E = Σ max(0,depth)² + Σ wall²`, `minsep` = minimum pairwise
separation (negative = penetration), `wall` = max wall violation. Raw data in
`curve.json` / `curve.log`:

| L | ΔL vs bank | E before | E after SA | minsep | wall | feasible |
|---|---:|---:|---:|---:|---:|---|
| 17.535533906 | 0 | 0 | 0 | +1.8e-15 | 0 | **yes** |
| 17.535000000 | 5.3e-4 | 1.03e-5 | 6.3e-7 | −7.0e-5 | 5.8e-5 | no |
| 17.534000000 | 1.5e-3 | 8.47e-5 | 4.6e-6 | −1.77e-4 | 1.47e-4 | no |
| 17.533000000 | 2.5e-3 | 2.31e-4 | 1.26e-5 | −2.89e-4 | 2.36e-4 | no |
| 17.530000000 | 5.5e-3 | 1.10e-3 | 5.86e-5 | −5.38e-4 | 4.73e-4 | no |
| 17.525000000 | 1.05e-2 | 3.99e-3 | 2.11e-4 | −1.09e-3 | 9.23e-4 | no |
| 17.520000000 | 1.55e-2 | 8.69e-3 | 4.61e-4 | −1.65e-3 | 1.31e-3 | no |

**Diagnostic (this is the useful part).** The SA reduces the overlap energy by 1–2
orders of magnitude but settles at a *fixed fraction* of the contraction:

```
minsep ≈ −0.11 … −0.13 × ΔL          (and wall ≈ 0.09 × ΔL)
```

i.e. the residual penetration is a constant ~12 % of the requested shrink, not a
transient. More time or more seeds move this equilibrium only marginally; it is the
signature of a contact-jammed configuration (this matches the band track's
four-scheme null result and the polish track's `396/396` zero-slack scan). To legalize
291 at any `L < 17.5355` the search would have to change the *contact graph*, which is
exactly what §4/§5 prove no neighbouring construction does.

### 8.2 Smoke observations already available

* Local burn-in at `L = 17.5355` reproduces the seed exactly (`E = 0`) — the seed is feasible.
* `L = 17.535` (ΔL = 5.3e-4): SA drives `E` from `1.03e-5` to `6.3e-7` (min separation
  still `−7.0e-5`, wall `5.8e-5`) — a very near miss that does **not** legalize.
* `L = 17.533` (ΔL = 2.5e-3): `E` from `2.31e-4` to `1.26e-5`, min sep `−2.9e-4`.
* Every rung below 17.5355 stayed infeasible, with the residual penetration tracking
  ~12 % of ΔL (see the table above).

---

## 9. Conclusion and recommendation

1. **n = 291 is at its algebraic optimum for every family we can test.**
   The layout is exactly `L = 14 + 5√2/2`, the axis fill is the *proved* MILP maximum
   (241) for those cores, and both the core arrangement and the lattice phase are
   unique global optima: shifting the lattice origin by 0.05, the phase by 1e-5, or the
   two-block separation by 0.1 each costs 4–32 squares.
2. **The family is not "nearly closed", it is a spike.** The next feasible side for any
   neighbouring construction is `L = 18.0` (+0.464). This is the same sharp-cliff
   structure the n=65 track proved for the solid 5×5 four-quadrant family.
3. **Nothing can be inserted.** An angle-aware Minkowski free-region scan over 90
   orientations finds zero admissible placements for one extra unit square.
4. Therefore the remaining value on k = 17…23 is **0** from this family. The annealer is
   the only route left, and it has to beat a configuration that is exact-contact jammed
   in 6 independent directions; the E-vs-L curve is the diagnostic for whether it is
   worth another slot.
5. A better use of a slot than a longer 291 search: **k = 24…31, D = 2** — the bank is
   still at `f = 0.5355` there while the record is at `f = 0.5348 (k=24)`, `0.5311
   (k=25)`, `0.5239 (k=26/27)`, `0.5216 (k=28)`, `0.5182 (k=29)`, `0.5141 (k=30/31)`.
   Those 8 record gaps are worth `~1.4e-2` in total and are *known to be reachable*,
   because the record holder is there.

## 10. Reproduce

```sh
cd /tmp/campaign2/master291
PY=/Users/zhaohuaxiang/ccjjllt/squares/.venv/bin/python
$PY repro.py            # closed-form layout + pairwise-SAT proof + n/L asserts  (§2)
$PY run_family3.py      # family table: exact capacity per arrangement         (§4)
$PY curve.py            # E-vs-L annealing curve from the bank seed            (§8.1)
$PY voidscan.py         # angle-aware free-region scan, 90 angles              (§6)
$PY - <<'EOF'           # phase sweep + cliff pinning                          (§5)
import sys; sys.path.insert(0,'/tmp/campaign2/master291')
import model as M; from milpfill import maxfill
F = 5*2**0.5/2 - 3
c1 = M.Block(3.53553390593279,-2.5,5,5); c2 = M.Block(16.263455967290643,-2.5,5,5)
for ds in (-1e-5, 0.0, 1e-5):
    print(ds, maxfill(17+F+ds, [c1,c2], 0.5, F+ds, F+ds, time_limit=20)[0])
EOF
# lift + certification (§7)
$PY /tmp/campaign2/lift.py --master master291.csv --k0 17 --D 2 \
    --ks 17 18 19 20 21 22 23 24 --out lift291.csv
cd /Users/zhaohuaxiang/ccjjllt/squares && .venv/bin/python -m squares merge \
  --baseline /tmp/best_bank/submission.csv --baseline-report /tmp/best_bank/report.json \
  --candidate /tmp/campaign2/master291/lift291.csv --output-dir /tmp/campaign2/master291/merge_test
```

## 11. Files

| file | what |
|---|---|
| `repro.py` | closed-form n=291 constructor + verification (`master291.csv` generated from it) |
| `master291.csv` | the 291-row `x,y,angle` master used for the lift |
| `lift291.csv` | lifted candidate, n = 291…578 (k = 17…24) |
| `merge_test/` | `squares merge` output: 0 changed puzzles, net gain 0 |
| `model.py`, `geom.py` | angle-aware SAT, block geometry, 4-phase candidate generation |
| `milpfill.py` | exact capacity MILP (2-offset 4-phase lattice), HiGHS |
| `gridmilp.py` | exact capacity MILP on an arbitrary fine grid |
| `family.py`, `run_family3.py` | family sweep driver + table |
| `sweep_phase.py`, `phase_sweep.json` | phase-offset sweep (§5, coarse) |
| `voidscan.py`, `voidscan2.log` | angle-aware free-region scan (§6) |
| `anneal_core.py`, `curve.py`, `curve.json` | numba SA core and the E-vs-L curve (§8.1) |
| `kdir/` | Kaggle kernel (`kernel.py` + metadata), smoke-tested |
| `family_table.json`, `family_final.log`, `scan_gap.log` | raw family-sweep output (corrected run / spike re-scan) |
| `merge_test_live/` | the same merge repeated against the live bank |

## 12. Handoff / what to do with the SA output

**Status: no SA output exists yet.** The session `ccjjllt/sis-sa291b-20261118` that the
watcher saw running between 19:46 and 21:13 UTC is no longer reachable
(`Permission 'kernels.get' was denied`), so nothing can be downloaded from it; my own
slug's only session is the 3.5 s crash. The corrected build in `kdir/` has not run.
The numbers in §8.1 are therefore the local, independently re-verified fallback.

The kernel (when it does run) writes:

| file | content |
|---|---|
| `candidate_sa291.csv` | submission-format, **only** the n=291 group, best feasible layout found |
| `best291.csv` | `x,y,angle` master, written **only if** a feasible layout with `L < 17.53553390593279` was found |
| `results_sa291.json` | per-task `{kind, L, seed, E, ok, why}` |

Decision rule on landing:

1. If `best291.csv` exists → verify it (`repro.py`-style pairwise SAT + `n == 291` +
   `n <= L²`), then lift and merge exactly as in §7. Expected value
   `≈ 0.35 × (17.5355 − L)`.
2. If only `results_sa291.json` exists → read the `E` column. A run whose best `E` is
   `> 1e-9` did not legalize anything; no candidate to certify. Use the `E`-vs-`L`
   shape (§8.1) to decide whether a longer run is worth a slot. Given
   `minsep ≈ −0.12·ΔL` and the closure proof, my recommendation is **not** to spend
   another slot on 291.
3. Higher-value use of the next free slot: **k = 24…31, D = 2** (n = 578, 627, 678,
   731, 786, 843, 902, 963). The bank is at `f = 0.5355` on all of them while the
   record is at `0.5348 / 0.5311 / 0.5239 / 0.5216 / 0.5182 / 0.5141`, i.e.
   `Σ Δscore ≈ 1.4e-2` and, unlike 291, **demonstrably reachable** — the record holder
   is already there.
