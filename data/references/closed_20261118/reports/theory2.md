# Theory track 2 — the 4-block / 4-phase integer sweep, run and audited

2026-11-18. No Kaggle kernel (the sweep is seconds locally), no submission, bank untouched.

## Headline

**No win. Nothing certified, nothing emitted as a candidate.**

At the record's side `L = 29.502152708` for `n = 842`, the best **machine-verified valid** layout I can
construct is

    n_max(constructed) = 836          (deficit 6 vs the record's 842)
    area = 870.377,  utilisation = 96.05 %   -> passes the area bound

but the measurement is **confounded**, and that is the important part of this report:

* The same constructor, run at **the bank's own side** `L = 29.520815280171`, gives only **837**,
  while the bank already has **842** there (its certified layout is accepted by my verifier at
  side 29.520815280171). So my construction is **5 squares weaker than the bank's own layout**, and
  836 at the record's side is a *lower bound on what the 4-phase family can do*, not the maximum.
  The 4-phase hypothesis is therefore **neither confirmed nor retired** — my search is the binding
  limitation, not the family.

A rigorous upper bound does not decide it either: for any packing of unit squares at any angles in
an `L x L` box, a horizontal slice meets squares with disjoint x-projections of length `>= 1`, so at
most `floor(L) = 29` squares cross it and

    n <= L * floor(L) = 29.502152708 * 29 = 855.56   ->   n <= 855.

So `842 <= n <= 855` is the honest bracket at the record's side.

## 1. The four bugs that produced the impossible 1098 — audit trail

`best.json` (1098 = 17x17 core at `L = 29.502152708`, utilisation 126 %) is deleted. It was wrong for
four independent reasons, each of which only inflates counts:

1. `add_pass()` recomputed the blocked set from the selected cells only and re-admitted every cell the
   core had excluded. This alone accounted for the 1098 / 1118 / 1120 values.
2. The core-vs-cell SAT used the polygon's **edge directions** as separating axes instead of the edge
   **normals**. For a 45° core the two differ by 45°, so a whole class of genuine overlaps was invisible
   (this is what produced 2024 -> 2803 "core-cell" overlaps).
3. The projection of an axis-aligned cell onto an axis with a **negative** component
   (`(-s, c)` for a 45° polygon) was taken from the wrong corner pair, making the cell's projected
   interval too narrow and reporting separation where there was overlap.
4. The candidate list stored **lower-left corners** while the emitters treated the first two columns
   as centres, shifting every axis cell by `(+0.5, +0.5)` and pushing them outside the box.

Every one of the four is caught by the two checks now hard-wired into the pipeline:

    assert n <= L*L + 1e-9                     # area bound, fails loudly
    verify(sq, L) -> (valid, side, msgs)       # exact pairwise SAT, inside-box, count

and the verifier is **calibrated on a known-good layout**: the bank's certified `n=842` packing is
shifted into its box and checked — `valid=True, side=29.520815280171`, i.e. it reproduces the
certified side to 1e-12. Any future count from this directory should be treated as unverified until
it passes exactly that test.

## 2. What was actually swept

**Constructor.** Box `[0,L]^2`, `L = k+f`, `k = floor(L)`, `f = L-k`.
* **Core**: a solid `p x q` block of unit squares at angle 45°, at bbox position `(cx, cy)`. Its
  supporting polygon is the convex hull of the `pq` squares' corners; a cell is admissible iff it is
  SAT-separated from that polygon.
* **Axis cells**: unit cells at lattice phase `(0,0)` and `(f,f)` (and, in the 4-phase runs, the
  quadrant assignment `(phi_x, phi_y) in {0,f}^2` chosen flush to the quadrant's two box edges, i.e.
  BL->(0,0), TL->(0,f), TR->(f,f), BR->(f,0)).
* **2-lattice variant** (valid by construction, no search): continent A = cells with `i+j <= s` on
  lattice `(0,0)`, continent B = cells with `i+j >= s+1` on lattice `(f,f)`. A vs B is provably
  disjoint because A's `U = x+y` interval ends at `s+2` while B's starts at `s+1+2f > s+2` (since
  `2f = 1.0043 > 1`). Within a continent the lattice guarantees disjointness. Only cell-vs-core is
  filtered.
* **4-phase variant**: greedy maximum-independent-set on the exact 3364-node conflict graph
  (`|dx| < 1 and |dy| < 1`), core mask applied, quadrant-flush order, then an add/polish pass that
  also respects the core mask.

**Sweep size.** `p,q in 8..22`, core positions on a `0.5` grid over `[0, L-M]^2` (up to 6x6 = 36
positions per core), `s in 0..2k` for the 2-lattice variant (all `s` evaluated in O(1) by cumulative
counts over `i+j`), 6-8 greedy orders per 4-phase configuration. Total `~10^5` verified configurations
per side, `~2 min` of CPU, no kernel needed.

## 3. Verified numbers at the record's side (`L = 29.502152708`, area 870.377)

| family | n | valid | util | note |
|---|---:|---|---:|---|
| 1 lattice + 45° core, all outside cells | 828 | yes | 95.1 % | catastrophic for the hypothesis? no: this is the weakest form |
| 2 interlocked lattices + 45° core (U-split) | 831 | yes | 95.5 % | valid by construction |
| 4 phases, greedy | **836** | yes | 96.05 % | best verified |
| record | 842 | (its own) | 96.74 % | |
| area bound | 870 | — | 100 % | |
| slice bound | 855 | — | 98.3 % | `n <= L*floor(L)` |

Same constructor at **the bank's side** `L = 29.520815280171` (area 871.47):

| family | n | valid |
|---|---:|---|
| 4 phases, greedy | **837** | yes |
| the bank's own certified layout | **842** | yes (re-checked here) |

So the constructor loses 5 squares against the bank at the bank's own side, and 6 against the record at
the record's side. The two deficits are consistent: tightening the side by `0.0187` costs this
constructor about 1 square.

## 4. Interpretation — why the sweep falls short, and what it does establish

* The 4-phase structure **does** help, monotonically and reproducibly: 828 (1 lattice) -> 831
  (2 lattices) -> 836 (4 phases) at the record's side. That is a real `+8` over the single-lattice
  form, so the qualitative claim in the first report stands.
* But a phase change costs a genuine gap: two cells whose y-lattices differ by `f` and whose x-lattices
  coincide are disjoint only if their `j` differ by at least 1, i.e. a physical gap of `f = 0.502`;
  and any cell-to-cell phase change in x costs the same in x. Since the *whole* box is only `f` taller
  and `f` wider than `k`, a layout can afford at most ~2 phase boundaries before the gaps eat the
  strips. That is why the 4-phase gain saturates near `+8` and not `+11`: 842-831 = 11 is the gap the
  record has to close over the 2-lattice form, and this family delivers 5 of it.
* The bank's own 842 at 29.5208 has 546 axis cells + 296 rotated, i.e. a *large* core. My greedy
  prefers small cores (11x9) because a myopic greedy cannot see that a large rotated core displaces
  cells one-for-one while opening the diagonal corridors that let the continents reach the strips.
  Reproducing the bank's architecture in the constructor is the missing piece — and it is exactly the
  "seed from the bank's phase assignment" experiment below.
* Consequence for the campaign: the missing 6 squares are **not** a matter of more integer search in
  this parametrisation; they are the sliver cells the bank's large-core architecture already exploits.
  The record is 0.0187 better than the bank, i.e. `ΔW = 1.18` area units, i.e. **1-2 lattice cells**,
  which is precisely the scale of the difference between my 836 and 842.

## 5. Recommendation (concrete, and it needs a kernel, not more theory)

The only experiment that can still settle the 4-phase question, and that is now unblocked by the
verified harness:

1. Start from the bank's certified `n=842` layout, **not** from an empty box.
2. Extract its combinatorial form: for each axis cell, `(i, j, phi_x, phi_y)` with
   `phi in {0, f}`; for the rotated patch, keep it as one rigid body.
3. Enumerate the integer moves that do not change the *count* but change the **bbox**: reassign each
   block's lattice phase among the 4 options, and shift each block by `+/-1` in `i` or `j` (a finite
   set, `~10^3` per puzzle), rebuilding each time and re-running `verify`.
4. Accept only if `n` stays 842 and the side drops below 29.520815280171. A drop of 0.0187 is what the
   record has; a drop of even 0.002 is a certified win on that puzzle.

The tooling in this directory (`final2.py`: `core_squares`, `cell_list`, `cell_hits_core`, `verify`)
is exactly what such a kernel needs, and its verifier is calibrated against the bank's own layout.
The one thing it must not do is trust a count without `verify` — the four bugs above are all
count-inflating and all silent.

## 6. Files

* `final2.py` — constructor + `verify` (area assert, inside-box, pairwise SAT); calibrated on the bank's
  `n=842`.
* `run4b.py` — the 4-phase greedy sweep with the shared core filter.
  Results: `res_29.502153_run4b.json` (**n=836, valid, side 29.502152708**) and
  `res_29.520815_run4b.json` (n=837, valid, side 29.520815280171).
* `focus.py` — large-core variant; `focus_29.520815.json` (n=835, valid).
* `final2.py:best_two_lattice` — the 2-lattice sweep; `best2.json` (n=831, valid, record's side).
* `check.py`, `mis.py`, `mis2.py`, `quad2.py`, `valid4.py`, `phase_search.py`, `run4.py` — the aborted
  first attempts that produced the impossible counts. Kept only as the audit trail of §1; none of
  their output is usable.
* Deleted: `best.json` (the impossible 1098) and `best4.*` (buggy emitter). Do not resurrect them.

No candidate CSV was produced because nothing beat the bank; `/tmp/best_bank/submission.csv` was
never opened for writing and no submission was made.

---

# Addendum — the recommended experiment, actually run (integer / phase moves on the bank's layouts)

2026-11-18, second pass. **Verdict: no win, and the negative is now quantitative rather than a
failed search.** No candidate CSV was emitted and no certification was run, because there is nothing
above the noise floor to certify.

## 7.1 Setup

Baseline at run time: `/tmp/best_bank/submission.csv`, SHA-256
`9c981e6ea9a44c076587256936948e636936a84ad0668af6b75e946f4fa527e9`, dual-route score
**22.128441824806618** (matches the stated win threshold), per-puzzle `L` for the six targets
confirmed from `report.json` (842 → 29.520815280171, 902 → 30.535533905933, 963 → 31.535533905933,
328 → 18.614368938491, 908 → 30.625574725146, 491 → 22.684143606359). The bank file was opened
read-only; its SHA is unchanged at the end of the run.

Harness: `moves.py` (this directory). For each target it loads the bank's certified layout, asserts
`len(sq) == n`, asserts the recomputed side equals the certified side to 1e-6, then applies a move,
rebuilds explicit coordinates, asserts `n <= L*L`, and runs an exact overlap test (SAT over a
superset of edge normals — vectorised, 14 ms per check at n=842, validated by injecting a 0.3
translation and confirming it reports overlaps).

Move set (per puzzle):

| id | move | count |
|---|---|---:|
| M1 | whole edge-layer translation inward, 9 amplitudes (1e-4 … 0.25) × 4 edges | 36 |
| M2 | whole edge-layer 1-index shift, 4 edges | 4 |
| M3 | phase-class translation, 4 classes × 6 directions × 4 amplitudes (incl. `δ* = 0.0186626`) | 96 |
| M4 | phase-class 1-index shift, 4 classes × 6 directions | 24 |
| M5 | phase-offset swap between two classes | 6 |
| M6 | quadrant block phase reassignment, 4 quadrants × 4 phases | 16 |
| M7 | simultaneous 4-edge shrink (the only move that can lower `L = max(W,H)`), δ by bisection | 1 |

## 7.2 Per-puzzle results

| n | bank L | configs tried | valid, side unchanged | valid, side **lower** | valid, side higher | rejected (overlap) | 4-edge δ* |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 842 | 29.520815280171 | 183 | 4 | 1 (by 1.7e-12) | 33 | 145 | 8.5e-13 |
| 902 | 30.535533905933 | 183 | 4 | 1 (by 1.7e-12) | 15 | 163 | 8.5e-13 |
| 963 | 31.535533905933 | 183 | 4 | 1 (by 1.7e-12) | 15 | 163 | 8.5e-13 |
| 328 | 18.614368938491 | 183 | 4 | 1 (by 1.1e-12) | 44 | 134 | 5.7e-13 |
| 908 | 30.625574725146 | 183 | 0 | 0 | 0 | 183 | 0 |
| 491 | 22.684143606359 | 150 | 4 | 1 (by 1.8e-12) | 1 | 144 | 9.1e-13 |

Every "lower" entry is **1e-12, i.e. the verifier's own tolerance floor**, not a geometric gain: the
score value of 1.7e-12/29.5/√842 is 2e-15, which is 12 orders of magnitude below the 22.1284418
threshold and would not survive the metric's text route. **Nothing certified.**

## 7.3 Why — the layouts are edge-locked, and here is the measurement

1. **Each bbox extreme is held by 14–31 squares, not by one.** For n=842: xmax 28 squares, xmin 24,
   ymax 29, ymin 25; n=963: 31/30/25/31; n=491: 18/4/16/4. So a move that does not move *the whole
   layer* leaves the extreme, hence `L`, unchanged. That kills M2/M4/M5/M6 by construction.
2. **Rotations cannot help.** A unit square's half-extent along an axis is
   `0.5(|cos θ|+|sin θ|) ≥ 0.5`, with equality only at multiples of 90°. Every square in every edge
   layer is already axis-aligned, so rotating one can only push the extreme outwards.
3. **The only surviving move is a simultaneous 4-edge shrink (M7)**, because `L = max(W,H)` and all
   six targets have `W = H` to 1e-12 — shrinking one dimension alone provably cannot change `L`.
   Bisection on M7 gives `δ* ≤ 9e-13` for five of the six targets and **exactly 0** for n=908.

4. **Census over the whole bank.** Running the same exact 4-edge test on all 1000 puzzles with
   `δ = 1e-6`:

       puzzles where a 1e-6 simultaneous 4-edge shrink is valid :   1 / 1000   (n = 1, already optimal)

   A finer per-edge clearance census puts the median slack at exactly 0, with 23 puzzles showing
   ~2e-9 (float-polish noise) and nothing between 1e-6 and 1e-9. So **999 of 1000 certified layouts
   are jammed to better than 1e-6 in all four directions simultaneously.**

## 7.4 One false lead, recorded so it is not repeated

A first clearance formula suggested the n=842 right column was *detached* with a full 1.0 unit of
free space behind it (28 squares at `x ∈ [13.26, 14.26]`, next layer at `[11.26, 12.26]`), which
would have been a 0.0187-scale opportunity. It is wrong: the formula only looked at squares
*strictly* behind the layer and missed the polished near-45° squares 0.004 inside it. The direct
test — translate that column by 1.0 and verify — gives **31 overlapping pairs**. The area argument
already forbade it: `L(L−1) = 841.96 < 842`. Any such claim must be settled by `no_overlap` on the
moved coordinates, never by a clearance formula.

## 7.5 What this establishes, and what it does not

Established (rigorous for the stated move set, measured on the actual coordinates):

* **The bank's `n=842` at `L = 29.520815280171` cannot be improved by phase reassignment, 1-index
  shifts, block swaps, class translations, or any simultaneous translation of the four edge layers.**
  The same holds for n=902, 963, 328, 908, 491, and for 999 of the 1000 banked puzzles.
* Therefore the 0.076–0.08 still on the table is **not** reachable by "polish the existing layout".
  It requires a **different architecture** — a new combinatorial arrangement with new contacts, not a
  perturbation of the current one.

Not established: an upper bound on the family. `842 ≤ n ≤ 855` at the record's side stands
(§3 of the main report), so the record's `29.502152708` is not excluded by any bound I have.

## 7.6 Where the remaining 0.08 actually is (recommendation)

The record's 30-column advantage is `Δf = 0.0186626` at D=1, i.e. `ΔW = 1.18` area units, i.e.
**about one lattice cell per puzzle**. Since the bank's layouts are jammed, that cell has to come
from a *different* combinatorial structure, not a better placement. Two concrete candidates, both
new arrangements rather than moves:

1. **The 4-phase sweep with a large core, seeded to reproduce the bank first.** My empty-box
   constructor tops out at 836 (record side) and 837 (bank side); the missing 5 squares are exactly
   the "large rotated core + diagonal corridors" pattern the bank's 546+296 layout already has. Any
   kernel job should first make the constructor reproduce the bank's 842 at 29.5208 — until it does,
   its count says nothing about the family.
2. **A different symmetry**: the bank's `n=842` has `W = H` but its *width* is over-specified (the
   four-edge shrink is blocked only by the polished 45° squares inside the edge layers). A layout
   whose core is rotated by a Pythagorean angle (tan θ = 3/4 or 4/3) can have all four core edges
   lattice-aligned, which removes the sliver waste entirely; that is a genuinely different
   architecture and the one family I have not been able to test in closed form.

## 7.7 Files

* `moves.py` — the move enumeration (M1–M7) with the exact verifier; writes `moves_results.json`.
* `moves_results.json` — per-puzzle counts and best sides (the table in §7.2).
* `census_1e6.json` — the 1e-6 four-edge census over all 1000 puzzles.
* `slacks.json` — per-edge clearance census (median 0).
* `final2.py` — constructor + `verify`, calibrated on the bank's `n=842`.
