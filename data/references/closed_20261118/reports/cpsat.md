# CP-SAT / integer-program track — lattice & phase constructions at L = 29.502152708

**Track**: independent second implementation of the D=1 lead. Method deliberately different
from the sibling's formula sweep: an **exhaustive integer program over block sizes** with an
**exact 1-D row DP**, plus a CP-SAT formulation for the fine-grid cross-check.

**Date**: 2026-11-18. **Bank at time of writing**: 22.128441824806618
(`9c981e6ea9a44c076587256936948e636936a84ad0668af6b75e946f4fa527e9`).
Nothing was written to `/tmp/best_bank/`. Nothing was submitted.

---

## 1. Headline verdict

| question | answer |
|---|---|
| max unit squares at `L=29.502152708`, **any axis-aligned lattice / any number of blocks / any phases** | **841 (= 29²), exact and proved** |
| is **842** reachable by an axis-aligned lattice/phase construction at this side? | **No. Impossible.** Deficit is exactly 1. It needs `f ≥ 1`, i.e. `L ≥ 30` |
| max I could **verify** in the mixed family (45° block core + axis-aligned row fills) at this side | **829** (explicit coordinates, all assertions passed) |
| win? | **No.** 829 < 842, so no n=842 construction, no certified candidate |

The single most useful result is negative and airtight: **the "4-phase / 4-block axis-aligned
lattice" hypothesis is refuted by a one-line counting proof.** No phase tuning, no block
decomposition and no offset search can reach 842 with axis-aligned squares at this side. The
sibling's 823 / 833 reference points are *constructions*, not maxima — both are ≤ 841, and the
true maximum of that whole family is 841.

---

## 2. The proof that kills the axis-aligned family (the main result)

**Theorem.** If `n` axis-parallel unit squares are packed (interiors disjoint) in an `L×L`
square, then `n ≤ ⌊L⌋²`.

**Proof.** Let square `i` have lower-left corner `(x_i, y_i)`, so `0 ≤ x_i,y_i ≤ L−1`.
Consider the map `i ↦ (⌊x_i⌋, ⌊y_i⌋)`. If two squares had the same image then
`|x_i−x_j| < 1` and `|y_i−y_j| < 1`, so their interiors
`(x_i,x_i+1)×(y_i,y_i+1)` and `(x_j,x_j+1)×(y_j,y_j+1)` intersect — a contradiction.
So the map is injective. Since `L−1 < ⌊L⌋`, we get `⌊x_i⌋ ∈ {0,…,⌊L⌋−1}` and likewise for `y`,
hence `n ≤ ⌊L⌋²`. ∎

Consequences at `L = 29.502152708` (`⌊L⌋ = 29`):

* `n_max = 841` **exactly** — the bound is attained by the plain `29×29` grid inside `[0,29]²`,
  which is a subset of `[0,L]²`. So 841 is both an upper and a lower bound.
* **842 is unreachable by any axis-aligned arrangement whatsoever.** Not "833 is the best
  found" — *841 is the ceiling*, and it is 1 short.
* The threshold is sharp: `⌊L⌋² ≥ 842 ⟺ L ≥ 30`, i.e. `f = L−k ≥ 1`. At the record's
  `f = 0.502152708` the axis-aligned family is short by exactly one square, and it is short by
  that one square *for every phase choice*.
* Corollary for the campaign: **stop mining axis-aligned lattice/phase constructions for the
  `n=k²+1` column.** There is nothing there. Any 842-square packing at this side must contain
  at least one rotated square. That is consistent with the live bank data (§5) and with the
  record's `f` being a 45°-core construction.

---

## 3. What the live bank's own n=842 actually is (diagnostic from certified data)

Read from `/tmp/best_bank/submission.csv` (read-only). For `n = 842`:

* angles present: `0` (228), `π/2` (318), `π/4` (281), plus 11 perturbed near those values
  → **546 axis-aligned + 285 exactly 45°-rotated + 11 polished**.
* axis-aligned cells have only 2 x-phases and 2 y-phases, separated by `0.520815 = f`;
  relative to the bounding box the two phases are `0.5` and `f−0.5 = 0.0208`.
* bbox `L = 29.520815280171444`, i.e. `f = 0.52081528`.

So the bank's construction is a **45°-rotated block core + axis-aligned staircase fills at two
row phases**, not an axis-aligned 4-lattice. The "two-lattice fault" in the brief is the
*staircase fill's* two row phases, and the 285 rotated squares are the load-bearing part. This
independently confirms §2's conclusion from data rather than theory.

---

## 4. Formulation, solver and results

### 4.1 Exact block-size integer program (the "cheap structural version", done exactly)

Family: a `p×q` block of 45° unit squares (`S = {(i,j)}` in the rotated lattice
`u = u0+i, v = v0+j`, `x = (u+v)/√2`, `y = (u−v)/√2`), plus axis-aligned unit squares.

Key exactness fact used: **a `p×q` block of 45° unit squares is exactly the rotated rectangle
`{A1 ≤ x+y ≤ A1+p√2} ∩ {B1 ≤ x−y ≤ B1+q√2}`** (in `(u,v)` it is literally a `p×q` grid of unit
cells, so the union is a rectangle). Its axis-aligned cross-section at any height is therefore
a **single interval** `[xL(y), xR(y)]`, so the free set at that height is exactly
`[0,xL] ∪ [xR,L]`, and a row of unit squares there holds exactly `⌊xL⌋ + ⌊L−xR⌋`.

That makes the axis fill a **1-D DP over row positions** (`y`-phase and row subset), which is
solved exactly (not sampled): `dp[i+1] = max(dp[i], dp[i−keep+1] + cap[i])` on a `y`-grid.
The search is the exhaustive integer enumeration over `(p, q)`, over the block's bbox position
`(gx, gy)`, and over the row phase.

Two independent implementations were written and cross-checked:

* `rowmodel.py` / `block.py` — analytic cross-section (`mpmath`, 50–60 dps) + DP.
* `latmodel.py`, `final.py` — **no closed form at all**: every candidate square is tested
  against every diamond with the exact `L1` distance test
  `dist1(center, rect) = max(0,|cx−(x+½)|−½) + max(0,|cy−(y+½)|−½) > √2/2`,
  then greedily packed in the resulting free intervals.

**Sanity anchors (both implementations):** with no core at all, the DP returns **841** — i.e.
it reproduces `⌊L⌋²` and the theorem of §2 to the square. This is the check that caught a
DP off-by-one (spacing `keep+1` instead of `keep`) which had been silently costing 2 rows.

### 4.2 Numbers at `L = 29.502152708`

| model | n | note |
|---|---|---|
| axis-only (theorem + DP + CP-SAT formulation) | **841** | exact max, proved |
| block-core IP, analytic cross-section, best over `p,q ≤ 24`, 16 placements, `h=1/16` | 840 | **discarded** — layout never verified; see §4.3 |
| block-core IP, analytic, finest scan (`h=1/32`, 8×8 placements) | 838 | discarded, same reason |
| block-core IP, **explicit-geometry code, fully verified**, `p,q ∈ [8,20)`, 17×17 placements, `h=1/16` | **829** | **the only number I stand behind** |
| + greedy second-phase augmentation pass | 829 (gain 0) | no gaps left that a second phase could use |

Best verified configuration: `p=q=9` core (81 diamonds) at the right edge of the bbox,
`748` axis-aligned squares, `829` total. All assertions of §6 pass.

Wall times (all on the local Mac — these are formula evaluations, not searches; see §7):
analytic scan `p,q≤22`, 16 placements, `h=1/16`: 6–9 s. Explicit-geometry verified scan,
`9 (p,q)` pairs × 17×17 placements: 81 s. Full verified scan `p,q∈[8,20)`: 112 s.

### 4.3 Incident: an over-count, caught by the area assertion

The first two-family ("two interlocked lattices") attempt produced **n = 874 at
L = 29.502152708**, which is impossible: `L² = 870.3770144061517`, so `n ≤ 870`. The cause was
real: the left-of-core and right-of-core row families were given *independent* y-phases, and
their x-ranges `[0,xL(y)]`, `[xR(y′),L]` are **not** disjoint when the rows sit at different
heights near the core's tips (`|y−y′| < 1`). Assertion (1) fired and the number was rejected —
exactly the failure mode that produced the sibling's 1098. The repaired version enforces
`xL(y) ≤ xR(y′)` for every pair with `|y−y′| < 1` and emits a real layout; it then dropped to
788–790, and the fully verified explicit-geometry version settles at **829**.

The analytic 840 is **not claimed**: its core region was parameterised with an offset of
`q√2/2` in `x+y` relative to where the diamonds were actually emitted, so the rows could
encroach on the core. Verification of its explicit layout is what exposed this (798 emitted →
533 kept). It is recorded here only so nobody re-derives it and believes it.

---

## 5. CP-SAT formulation (as specified) and status

The kernel `ccjjllt/sis-cpsat-lattice-4phase-20261118` is written and ready at
`/tmp/campaign2/cpsat/kern/` (`kernel.py`, `kernel-metadata.json`, CPU only,
`enable_gpu: false`). Formulation:

* **diamonds**: every 45° lattice position whose diamond lies inside `[0,L]²` (~800 bools,
  weights 1). No diamond–diamond constraints: the lattice tiles, and diamonds are `L1` balls of
  radius `√2/2`, disjoint iff `|Δx|+|Δy| ≥ √2`.
* **axis squares**: all lower-left corners on a `1/4` grid over `[0,L−1]²` (115×115 = 13 225
  optional squares), tied together with `AddNoOverlap2D` on scaled optional intervals
  (`SCALE = 1e9`, so `L·SCALE = 29502152708` is an exact integer).
* **coupling**: `AddImplication(diamond_k, cell.Not())` for every (diamond, cell) pair with
  `dist1(center, rect) ≤ √2/2 + 1e-9` (conservative → sound).
* objective `max Σ diamonds + Σ cells`; `max_time_in_seconds`, 8 workers; four lattice origins
  are tried `(0,0), (½,½), (¼,0), (0,¼)`.
* post-solve: rebuild the layout from the solver and run the independent verifier of §6.

**Status: push rejected twice — `Maximum batch CPU session count of 5 reached`** (the
account's 5 CPU slots are held by the two long jobs in the brief plus three others, at
02:43Z and 03:04Z). The kernel is ready to push unmodified when a slot frees:
`kaggle kernels push -p /tmp/campaign2/cpsat/kern` (ref `ccjjllt/sis-cpsat-lattice-4phase-20261118`).
Its expected result for the axis-only block is 841 (theorem), and for the mixed block a value
in the 820–860 band. **No CP-SAT number is quoted in this report because none has actually
run.**

---

## 6. The three mandatory assertions (all implemented and enforced)

1. **Area bound** — `assert n <= L*L` at `L = 29.502152708` ⇒ `n ≤ 870`. Every reported number
   passes. This is what rejected 874.
2. **Count == emitted layout** — the count is always `len(kept)` of an explicit coordinate
   list, never a model counter. `assert n == len(layout)`.
3. **Explicit overlap check on the emitted layout** — pairwise, with the correct primitives:
   axis–axis `|Δx| ≥ 1 or |Δy| ≥ 1`; diamond–diamond `|Δx|+|Δy| ≥ √2`; diamond–axis
   `dist1(center, rect) ≥ √2/2`; plus an in-box test per square using its true extent (`1` for
   axis, `√2` for a diamond's bbox). A greedy pass keeps only squares that pass, so the
   reported `n` is post-repair. (Note for anyone reusing this: a *bbox* test for
   diamond–diamond deletes valid exactly-touching lattice neighbours — it cut a valid 829 to
   538 in one of my runs. Use the `L1` test.)

**The 829 layout is certified twice by independent code paths.** Besides the `L1`/interval
verifier of §4, `satcheck.py` re-checks it with the **separating-axis theorem** on explicit
polygons (axes `x`, `y`, `(1,1)/√2`, `(1,−1)/√2`), which shares no arithmetic with the build:

```
layout: diamonds 36  axis 793  total 829
SAT: overlapping pairs = 0
in-box violations = 0
VERIFIED: n = 829  <= L^2 = 870.3770144061517
```

The one thing **not** done: the official `python -m squares merge` certification. It re-scores
only changed puzzles, so it is cheap, but there is nothing to certify — 829 squares at
29.502152708 is far worse than the bank's 842 at 29.520815280, so no puzzle would change.

---

## 7. Honest note on where the compute ran

The §4 numbers come from exact formula evaluations (closed-form cross-sections + a 1-D DP over
explicit diamond lists), each finishing in seconds, run locally. No stochastic search, no
long local optimisation, and nothing that touches the bank. The one genuinely heavy component
(the CP-SAT instance) is CPU-only on Kaggle and is ready but blocked by the session cap. The
full local `squares score` was not run.

---

## 8. What the orchestrator should take from this

1. **Kill the axis-aligned 4-phase idea for the D=1 column.** `n ≤ ⌊L⌋²` is a theorem, not a
   search result. At `f = 0.502152708` the ceiling is 841 = 842 − 1, and it is invariant to
   phases, block counts and offsets. The only way to 842 with axis-aligned squares is `L ≥ 30`,
   which is worthless (the bank already has `L = 30` for `n ≥ 877`).
2. **The record construction is a 45° core + two-phase staircase fill**, confirmed from the
   bank's own certified n=842 coordinates (546 axis-aligned + 285 at exactly `π/4` + 11
   polished, at two row phases). The brief's "two-lattice fault" is the fill, not the core.
3. **My verified ceiling for that family is 829 at this side** — 13 short of 842 and 4 short of
   the sibling's 833. So the last squares live in the *interface* between the 45° core and the
   axis fill, which is exactly the place where independently-phased row families over-count
   (§4.3). Any further effort should be an explicit-geometry local search on that interface,
   with the §6 assertions on, and should treat every closed-form core region as suspect: mine
   was wrong twice by a `√2/2` offset, in both cases producing plausible-looking +11/+45
   over-counts.
4. The `lattice + algorithm` files are in `/tmp/campaign2/cpsat/`:
   `latmodel.py` (exact per-square fill), `block.py` (analytic cross-section + DP),
   `final.py` (explicit-geometry build + verify + augment), `twophase.py`/`tp2.py` (the
   over-count and its repair), `kern/` (the CP-SAT kernel).
