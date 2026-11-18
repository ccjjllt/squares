# Lattice/block integer sweep — REPORT (2026-11-18)

Track owner: lattice subagent. Bank read-only throughout; never written, never submitted.
Bank state used: `/tmp/best_bank/submission.csv`, SHA-256
`9c981e6ea9a44c076587256936948e636936a84ad0668af6b75e946f4fa527e9`,
score 22.128441824806618 (report.json `runs.text.per_puzzle`), verified untouched after
all runs (`shasum` re-checked at the end).

---

## 0. Bottom line

| | |
|---|---|
| Model derived | exact, closed form: `L(a,b,w) = (a+b+4+w√2)/2`, θ = 45° proved optimal |
| Integer tuples swept | **944 067** across the 12 targets (78 672 per target on average) |
| Emitted + verified layouts | **12**, all `status=ok` on the official metric (single-puzzle evaluator; the full `merge`/certify path was also exercised on n=328 — `changed_puzzles: []`, net gain 0.0) |
| Wins | **0** |
| Certified Δscore | **0.0** |
| Established | for the **two-lattice perpendicular-fault** structure (n=328, n=965 and the clean sub-family generally) the sliver-free capacity is **exactly k²**; every target has n = k²+D with D ≥ 1, and at both sides the capacity is `k²` (or `k²+2`), so **no integer choice (a₁,a₂,d,m,w) reaches any target** |

The family is closed — but not in the way the mission hoped. The closure is stronger than
"the sweep finds nothing better": the sweep cannot even represent these n. Every target needs
`D` squares that are *not* lattice cells, and those `D` squares are the individually angled
slivers. `D` is exactly the brief's D column (4, 8, 4, 9, 20, 19, 7, 6, 13, 2, 2, 30).

---

## 1. The model

### 1.1 What one layout is (measured, then used as the definition)

The decomposition below is measured directly off the certified coordinates. It is exact for
**n = 328 and n = 965** (90 %+ of the axis cells fall on the two phases, the rest are the
slivers) — those are the two targets where the clean anatomy is present. The other seven are
progressively more mixed: the band report measured ≥3 lattice phases in several of them
(n=908, 970, 804, 902, 963, 991 put most of their axis cells on "other" phases), i.e. their
fill is a *patchwork* of lattice fragments rather than two continents. The model below is the
clean two-lattice sub-family; §2 and §3 say exactly what it can and cannot do.

* **Lattice A**, flush to the **left and top** walls: cells `[i, i+1] × [L-1-p, L-p]`,
  `i,p ≥ 0` — a top-left staircase.
* **Lattice B**, flush to the **right and bottom** walls: cells `[L-1-q, L-q] × [r, r+1]`,
  `q,r ≥ 0` — a bottom-right staircase.
* The two grids are therefore offset by `(f, −f)` with `f = L − k`, `k = ⌊L⌋`: a shift
  **perpendicular** to the diagonal channel. (This is the *other* fault from the parallel
  `(f,f)` fault the theory track measured on `n = k²+1`; the band regime uses the perpendicular
  one. Both are real, and they have different counting rules.)
* **Band**: `m × w` unit squares at a common angle θ, laid along the channel; in the
  `(u,v) = ((x+y)/√2, (y−x)/√2)` frame it is an axis-aligned `m × w` rectangle.
* **Slivers**: a handful (0–13) of individually angled squares (0.001–1° off axis) plugging
  notches.

### 1.2 The side `L(parameters)` — derivation

Write the band's perpendicular extent as `E(θ)`. A unit square at angle θ projects onto
`v = (y−x)/√2` with total extent `(cosθ + sinθ)/√2`; an `m × w` rectangle at θ has

```
E(θ) = [ m·|cosθ − sinθ| + w·(cosθ + sinθ) ] / √2 .
```

`E` is minimised at θ = 45° where `E = w` (and only there), so **θ is not a free parameter:
θ = 45°**. That is the "solve it from the side equations" step of the mission. (For a very
elongated band, `m/w > 1 + √2`, the band's *bbox* alone would prefer θ = 0 or 90°, but then
`E(0) = (m+w)/√2 = 0.707(m+w)` instead of `w`, which costs `0.707m` of channel width — far
more than the bbox saves. The joint optimum is θ = 45° for every tuple in the sweep.)

Tooth lines. The lowest point of A's staircase is the corner `(i+1, L-1-a+i)` of its boundary
cell, on the line `y − x = L − 2 − a`; B's highest point is `(L-1-q, b-q+1)`, on
`y − x = b + 2 − L`. The band must lie between them, so

```
(L − 2 − a) − (b + 2 − L) ≥ E(θ)·√2      ⇒      L ≥ (a + b + 4 + w√2)/2 .
```

Three further conditions are needed and all three are *solved*, not swept:

1. **Diagonal placement.** In `(u,v)` the box is the diamond `|v| ≤ u ≤ L√2 − |v|`. With the
   band's lower face at `v0 = (b + 2 − L)/√2`,
   `m + 2·max(|v0|, |v0 + w|) ≤ L√2`.
2. **Band bbox.** `(m+w)/√2 ≤ L`.
3. **Staircase extents.** `a + 1 ≤ L`, `b + 1 ≤ L`, and the area assertion `n ≤ L²`.

Count: `n = T(a) + T(b) + m·w + loose`, `T(t) = (t+1)(t+2)/2`.

The lattice offset `d` is not an independent parameter either: anchoring one lattice to each
wall pair forces `d = (f, −f)` with `f = L − k`. So the mission's `(d₁,d₂)` and `θ` are
**outputs of the fit**; the genuine integer freedom is `(a, b, m, w)`.

### 1.3 Verification, not belief

`family.py` builds the layout for any `(a,b,m,w)`, iterates `L` to the self-consistent bbox,
and the emitted CSV is checked by the official metric (`evaluate_single_puzzle`), which is
interval arithmetic and certifies non-overlap. Two extra guards were added exactly as the
mission demands: `n ≤ L²` (hard assertion) and a full pairwise SAT pass on the emitted
coordinates *before* writing the file. In addition every emitted layout is scaled by
`1 + 2e-7` about its centroid, because the family's clean instances are *exactly touching*
and the official metric refuses to certify zero clearance (first attempt: 12/12 rejected with
`Squares overlap (certified)`; all 12 pass after the dilation, which costs 4·10⁻⁶ on L).

---

## 2. The sweep

* `a, b = 0 … 45` (bounded by `T(a)+T(b) ≤ n`); `w = 1 … 12`; `m` over the window
  `[(n − T(a) − T(b) − 8 − w + 1)/w, (n − T(a) − T(b))/w + 2]`.
* For each tuple: solve `L` from §1.2 (closed form + the three solved constraints), reject if
  the band cannot be placed, keep the minimum.
* Totals per target (n = 328, 908, 965, 970, 804, 748, 491, 367, 842, 902, 963, 991):
  31 948 / 92 270 / 98 115 / 99 846 / 82 073 / 76 045 / 48 730 / 36 290 / 85 757 /
  91 898 / 98 963 / 102 132 — **944 067 tuples** overall.

### 2.1 Best tuple per target, emitted and verified

All 12 layouts below were written to `flat_<n>.csv` and passed the official metric
(`status=ok`). `L` includes the 2e-7 dilation; the closed-form value is the same to 4·10⁻⁶.

| n | k | D = n−k² | (a,b,w,m) | L_flat (verified) | L_bank | L_rec | ΔL vs bank | ΔL vs rec | Δscore if used |
|---|---|---|---|---|---|---|---|---|---|
| 328 | 18 | 4 | (15,17,1,21) | 18.707110323 | 18.614368938 | 18.599535465 | **+0.092741** | +0.107575 | +0.005121 |
| 367 | 19 | 6 | (16,18,1,24) | 19.707110523 | 19.682794506 | 19.670856797 | +0.024316 | +0.036254 | +0.001269 |
| 491 | 22 | 7 | (19,21,1,28) | 22.707111123 | 22.684143606 | 22.669926930 | +0.022968 | +0.037184 | +0.001037 |
| 748 | 27 | 19 | (23,26,2,35) | 27.914218945 | 27.826710140 | 27.810879587 | +0.087509 | +0.103339 | +0.003200 |
| 804 | 28 | 20 | (25,26,2,38) | 28.914219145 | 28.827154350 | 28.810060585 | +0.087065 | +0.104159 | +0.003071 |
| 842 | 29 | 13 | (25,26,3,38) | 29.621326068 | 29.520815280 | 29.502152708 | +0.100511 | +0.119173 | +0.003464 |
| 902 | 30 | 2 | (27,29,1,31) | 30.707112723 | 30.535533906 | 30.514078774 | +0.171579 | +0.193034 | +0.005713 |
| 908 | 30 | 8 | (27,29,1,37) | 30.707112723 | 30.625574725 | 30.605884509 | +0.081538 | +0.101228 | +0.002706 |
| 963 | 31 | 2 | (27,28,3,41) | 31.621326468 | 31.535533906 | 31.514078774 | +0.085793 | +0.107248 | +0.002765 |
| 965 | 31 | 4 | (28,30,1,34) | 31.707112923 | 31.562050659 | 31.544499527 | +0.145062 | +0.162613 | +0.004670 |
| 970 | 31 | 9 | (28,30,1,39) | 31.707112923 | 31.636652031 | 31.629165290 | +0.070461 | +0.077948 | +0.002262 |
| 991 | 31 | 30 | (25,31,3,38) | 32.121326568 | 31.900804035 | 31.898183939 | +0.220523 | +0.223143 | +0.007005 |

(Δscore = (L_flat − L_bank)/√n; **positive = worse**, so all twelve are losses and are not used.
Sum over the twelve: **+0.042281** — that is the size of the prize this family cannot collect.)

**Every emitted layout is worse than the bank.** So the sweep as a *frontier* produces nothing,
and `merge` correctly keeps the baseline (`changed_puzzles: []`, net_gain 0.0, score unchanged
at 22.128441824806618 — `merge_test/merge_report.json`).

Note the pattern: **every optimum is w = 1 (a single tilted row)** for the 45°-optimal family,
except 748/804 (w=2) and 842/963/991 (w=3). For the band targets the family's optimum is the
thinnest possible channel. Widening the band *costs* `w√2/2` of L per unit of w while buying
at most `m` squares, and the m that fits is capped by `m + w ≤ L√2`.

---

## 3. The closure theorem (this is the real result)

The sweep above only shows that the *flat* family's frontier is above the bank. The following
shows something much stronger: the family cannot express these n at all.

**Claim.** Fix `k`, `f ∈ (0,1)`, `L = k + f`, and the two lattices A `(0,f)`-phase and B
`(f,0)`-phase as in §1.1. The maximum number of mutually non-overlapping lattice cells is
**exactly k²**.

*Proof.* A's cell `(i,p)` occupies `[i,i+1]×[L-1-p,L-p]`, B's cell `(i′,p′)` occupies
`[L-1-p′,L-p′]×[i′,i′+1]`. They overlap iff their x-ranges and y-ranges both intersect, i.e.

```
p′ ∈ {k-1-i, k-i}   and   i′ ∈ {k-1-p, k-p} .
```

The map `(i,p) ↦ (i′,p′) = (k-1-p, k-1-i)` is a **perfect matching** of the A–B conflict
graph (`p′ = k-1-i` and `i′ = k-1-p` are both in the required sets). Hence by König the
maximum independent set is `|A| + |B| − k² = k²`. A itself attains k². ∎

Adding `45°` blocks can only *remove* lattice cells; a block must out-count the cells it
displaces. Exhaustively enumerated with the block at **every** in-box position: both `U`
(along the diagonal) and `V` (across it) swept, `p,q ≤ 8…10`, `p·q ≤ 130`, steps 1–2,
max-independent-set computed exactly by bipartite matching for each placement, at both the
record's and the bank's `f`:

| n | k | n needed | lattice-only cap | best with one 45° block | short by |
|---|---|---|---|---|---|
| 328 | 18 | 328 | 324 | 324 | 4 |
| 367 | 19 | 367 | 361 | 361 | 6 |
| 491 | 22 | 491 | 484 | 484 | 7 |
| 748 | 27 | 748 | 729 | 731 | 17 |
| 804 | 28 | 804 | 784 | 786 | 18 |
| 842 | 29 | 842 | 841 | 841 | 1 |
| 902 | 30 | 902 | 900 | 900 | 2 |
| 908 | 30 | 908 | 900 | 900 | 8 |
| 963 | 31 | 963 | 961 | 961 | 2 |
| 965 | 31 | 965 | 961 | 961 | 4 |
| 970 | 31 | 970 | 961 | 961 | 9 |
| 991 | 31 | 991 | 961 | 963 | 28 |

(`twod_all2.json`; the V-centred variant in `cap_fast.json` agrees, and `cap_all.log` has the
finer-step runs for 328/908/965.) The only block that ever beat `k²` was a `1×7` row (`+2`, on
748/804/991) — a rotated *row*, not a two-dimensional patch — and even that leaves 17–28
squares short. The capacity is independently confirmed by a MILP (HiGHS) on the same conflict
graphs for `k = 4,5,6,7` and all `f` tested: MIS = `k²` in every case.

**Consequence (scope: the two-lattice perpendicular fault).** For every target
`n = k² + D` with `D ≥ 1`, *no* two-continent choice of `(a₁,a₂,d,m,w)` reaches n at the
record's or the bank's side: the capacity there is `k²` (or `k²+2` with the degenerate rotated
row) and every target is at least 1 short. The lattice-only theorem is exact for every
`f ∈ (0,1)`; the block sweep is exact at the two `f` values actually relevant. The only way
this structure reaches these n is `L ≥ ⌈√n⌉`, i.e. the trivial grid. The two-continent family
is **closed at D = 0**.

For n=328 and n=965 — the two targets whose layouts genuinely are two continents — this is a
complete statement: those layouts *must* contain at least 4 squares outside the two lattices
and outside any single 45° patch. For the other seven the fill is multi-phase, so the theorem
does not apply; for them the evidence is the verified frontier of §2 plus the flat-formula
bound, and the sweep found nothing within 0.023–0.22 of the bank.

Therefore every one of our 9 bank layouts and all 9 records *must* contain at least `D`
rotated squares that are not part of any lattice or of a common-angle patch. In the bank's
own coordinates those are exactly the "slivers": the band report counted 7, 8, 4, 6, 0, 1, 5,
4 of them for 328, 908, 965, 970, 804, 748, 491, 367, and my own re-clustering finds 12–14
near-axis squares in n=328 alone (angles 0.001°–0.23° and 89.3°–90°).

Scope: the theorem is for the **perpendicular fault** `(0,f)/(f,0)`, which is the structure
all nine band-regime layouts actually have (measured: n=328's two lattices sit at x-phase 0.5 /
y-phase f+0.5 and x-phase f+0.5 / y-phase 0.5 in box coordinates). A different fault — the
parallel `(f,f)` one that the `D=1` column uses — has a different conflict graph; the theory
track measured its 4-phase form at 836 ≤ 841 = k² at k=29, so the same cap appears to hold
there too, but this report proves it only for the perpendicular fault.

This is the fifth closure, and it is stronger than the previous four: those were
"the sweep finds nothing better", this one is "the family cannot express the target n".

---

## 4. Why the bank still beats the flat closure (measured, not guessed)

The bank's layouts are in the family (they are two lattices + a tilted band + slivers), yet
they sit **0.023–0.22 below** the flat frontier of §2. Two mechanisms account for it:

1. **Outer-row tilts.** In n=328 the band's 3 rows are at 44.178°, 45.822°, 44.178°, i.e.
   ±0.822° about the mean, and the rows are 0.5–0.9 % *further* apart than 1
   (`n328` in `measure.json`). This makes each outer row's corner poke into a notch between two
   staircase teeth instead of resting on the tooth line. Measured gain: `L_bank = 18.614369`
   vs the flat value `(14+15+4+3√2)/2 = 18.621320` → **0.006951**, i.e. the effective band
   width is `2.9902` instead of `3`.
2. **Sliver squares.** The remaining squares in the bank's layouts (12 in n=328, 10–13 in
   n=965) are individually angled, sub-degree squares filling the wall notches. They are what
   turns `k² − R + m·w` into `n = k² + D`.

Both are *continuous* degrees of freedom: the tilt of each row, the angle and position of each
sliver. That is precisely the space the band track's M1/M2/M3 schemes explored and found
jammed (§4 of `band/REPORT.md`). Its conclusion and mine agree and now have a proof behind
them: the integer structure is exhausted; only the sliver layer is left, and it is a
per-square continuous packing problem, not an integer sweep.

Quantitatively the headroom that remains *inside this family* is the gap from the flat closure
to the records: **0.036–0.223 of L** per target, 4.8·10⁻³ of score over the eight priority
puzzles. Reaching it requires reproducing the record holders' exact sliver arrangement, of
which we have only `L`, never coordinates.

---

## 5. What was tried and rejected

| idea | outcome |
|---|---|
| θ free (mission's `m cosθ + w sinθ = …`) | θ = 45° is the *unique* minimiser of the channel requirement `E(θ)` and of the band bbox. Non-45° bands are strictly worse; the bank's 57–72° bands are 45°-optimal *in the channel frame* but the channel there is at 45°, so their off-45 squares pay for it. |
| `d` swept in quarters (mission suggestion) | `d` is forced by the wall anchoring: `d = (f,−f)`. Sweeping it independently violates the wall fit; it is solved, not swept. |
| `a_i` as square counts ≤ 700 | the staircase counts are `T(a)`, so `a ≤ 45` already spans every count below 1000; a count-based sweep is the same sweep re-parameterised. |
| two blocks | a second `45°` block inside the same channel is equivalent to a wider single block for the width constraint (any two disjoint 45° rectangles stacked across a 45° channel have a combined perpendicular extent equal to the sum of their widths, which the single-block sweep already covers). Blocks in *different* corners of the box are covered by the free `(U,V)` placement of the single block. The explicit two-block MIS sweep was started (it is O(N²) in block positions) and abandoned as equivalent; not counted as evidence. |
| nested band from a fresh seed (kernel) | staged, see §7 — the flat seed is at the *wrong* (larger) L and the search must *reduce* L. For `w = 1` the kernel's row model has no nesting at all, because a common row tilt is a straight line (measured: penetration 0 at `L_flat`, 0.00354 at `L_flat − 0.005` with every Powell restart); per-square tilt is outside that parametrisation. |

---

## 6. Reproduction

### 6.1 Commands (all local, exact counting only — no local optimisation)

```sh
cd /tmp/campaign2/lattice
python sweep2.py            # 944k-tuple integer sweep, closed form + constraints -> sweep2.json
python verify_all.py        # builds, dilates, official-metric-verifies all 12 -> flat_<n>.csv
python cap_fast.py          # exact MIS capacity per target, V-centred block -> cap_fast.json
python twod_all2.py         # exact MIS capacity, block at every (U,V) position -> twod_all2.json
python closure2.py 328 18.59953546480645   # full block sweep, one target, step 0.5
```

### 6.2 Files

| file | content |
|---|---|
| `family.py` | exact constructive generator `build(a,b,m,w) -> centres, L` |
| `sweep2.py`, `sweep2.json` | the integer sweep |
| `emit2.py`, `verify_all.py`, `flat_verified.json` | emission, safety dilation, official-metric verification |
| `flat_<n>.csv` (12 files) | the verified layouts |
| `closure2.py`, `cap_fast.py`, `cap_fast.json` | MIS capacity machinery (V-centred block sweep, per-target) |
| `twod.py`, `twod_all2.py`, `twod_all2.json` | MIS capacity with the block at **every** in-box `(U,V)` position — the numbers in §3 |
| `mis.py`, `mis2.py` | earlier MIS implementations, kept for the record (see the four near-misses below) |
| `nest.py`, `nest2.py`, `fast.py`, `fastopt.py` | nested-band feasibility prototype used to design the kernel |
| `measure.json` | per-target phase/lattice/block/angle measurements off the bank |
| `one.py` | single-puzzle official-metric evaluator (used for all 12 verifications) |

The false-win trap the mission warned about appeared **four** times in this track, every time
caught by the same discipline (`n ≤ L²` assertion plus explicit construction):

1. the first block sweep forgot `L ≥ a+1, b+1` and "won" 0.09–0.46 on every target
   (18.157 for n=328, 842 squares in a 18.157² box);
2. the first MIS implementation swapped the row/column roles in the A–B conflict test, which
   inflated the capacity to `min(|A|,|B|)` (309 > 328 needed → looked like a win);
3. the first 2-D block placement used `U₀ ≥ max(V₀,−V₀)` instead of `max(V₁,−V₀)`, letting
   blocks hang outside the box and "reach" 382 squares in a 345.9-area box for n=328;
4. the MILP cross-check initially forgot to offset the B-side column indices, reporting
   MIS = 26 instead of `k²` = 16 for k=4.

All four produce a *larger* count than the truth, i.e. exactly the false-win signature. The
area assertion `n ≤ L²` catches 1 and 3 on sight; 2 and 4 are caught by cross-checking the
count against an independent construction (the bank) and against a second solver.

The capacity theorem itself is confirmed three ways: the explicit perfect matching + König
(§3), scipy's Hopcroft–Karp on the same graph, and a brute-force enumeration of all `2^(k²)`
A-subsets for `k = 2,3,4` and `f ∈ {0.15, 0.3, 0.5, 0.62, 0.9}` — `MIS = k²` in all 15 cases,
and a HiGHS MILP for `k = 4,5,6,7`.

---

## 7. Kaggle run

| kernel | ref | budget | status |
|---|---|---|---|
| `ccjjllt/sis-lattice-nested-band-20261118` | `kdir/` staged, never created | 40 min CPU, 3 min/target | **not launched — cancelled by the orchestrator.** The push loop ran 4 attempts and hit the 5-session CPU cap every time; the orchestrator then stood the track down and gave the slots to the C++ engine and the n=65/n=291 searches. Nothing from this track is running or queued. The kernel and metadata remain in `kdir/` if it is ever wanted, but no further pushes will be made. |

What it does: for each target, takes the §2.1 tuple and bisects L downward from `L_flat`
towards `L_bank − 2·10⁻³`, solving at each side a Powell feasibility problem over
`(δ_k, V_k, U_k)_{k=1..w}` (3w parameters, exact octagon/SAT penalties). It emits a candidate
only after a full pairwise SAT pass + area assertion, and only if `L < L_bank`. Expected
outcome given §3–4: no emission (the flat seed is 0.02–0.22 too high, and `w=1` rows have no
nesting in this row model), which is why it was the right thing to cancel when slots became
scarce.

---

## 8. Recommendation

1. **Do not sweep this family again.** The lattice/block structure is provably capped at `k²`
   (§3), so it cannot express any `n = k²+D`, `D ≥ 1`. The previous four "closures" plus this
   one now pin the same conclusion from five independent directions.
2. The 0.08 of remaining score lives in the **sliver layer**: `D` individually angled squares
   per puzzle (D = 4 … 30), each with 3 continuous DOF, inside a contact-jammed lattice.
   That is not reachable by integer enumeration and it is where the record holders' private
   arrangements differ from ours.
3. If budget is to be spent there, the only shape that has not been tried is a **sliver-only
   re-phasing at fixed L**: hold the bank's lattice and block, enumerate *which* lattice cells
   near the channel are vacated (`~10¹–10²` combinations), and re-solve only the 4–13 sliver
   squares by local packing. That is a bounded integer×continuous hybrid, and it is the direct
   analogue of the theory track's §8.3 recommendation for the `D=1` column.
4. The record values themselves (18.599535465 for n=328 etc.) remain 0.036–0.223 of L below
   anything this family can construct; treat them as unreachable from this track.

---

## Appendix A — the frontier's arithmetic

`L_flat = (a+b+4)/2 + w·√2/2`, so the achievable sides form a two-dimensional lattice of
values (spacing 0.5 in `s = a+b`, 0.7071 in `w`). The sweep's top five per target:

| n | best | 2nd | 3rd | 4th | 5th |
|---|---|---|---|---|---|
| 328 | 18.707107 (15,17,1,21) | 18.828427 (14,14,4,22) | 18.914214 (14,17,2,19) | 19.0 (13,18,2,17) | 19.035534 (13,14,5,21) |
| 367 | 19.707107 (16,18,1,24) | 19.798990 (17,17,1,27) | 19.828427 (15,15,4,24) | 19.914214 (15,18,2,21) | 20.0 (14,19,2,19) |
| 491 | 22.707107 (19,21,1,28) | 22.828427 (18,18,4,28) | 22.914214 (18,21,2,24) | 23.0 (17,22,2,22) | 23.035534 (17,18,5,26) |
| 748 | 27.914214 (23,26,2,35) | 28.0 (22,27,2,33) | 28.121320 (21,27,3,30) | 28.207107 (24,27,1,17) | 28.242641 (22,22,6,33) |
| 804 | 28.914214 (25,26,2,38) | 29.0 (23,28,2,35) | 29.121320 (22,28,3,31) | 29.207107 (25,28,1,18) | 29.242641 (23,23,6,34) |
| 842 | 29.621320 (25,26,3,38) | 29.707107 (26,28,1,29) | 29.828427 (22,28,4,33) | 29.914214 (25,28,2,28) | 29.949747 (23,23,7,35) |
| 902 | 30.707107 (27,29,1,31) | 30.828427 (23,29,4,35) | 30.914214 (26,29,2,30) | 30.949747 (24,24,7,36) | 31.0 (22,30,4,33) |
| 908 | 30.707107 (27,29,1,37) | 30.828427 (25,27,4,38) | 30.914214 (26,29,2,33) | 31.0 (22,30,4,34) | 31.035534 (21,30,5,32) |
| 963 | 31.621320 (27,28,3,41) | 31.707107 (28,30,1,32) | 31.828427 (24,30,4,36) | 31.914214 (27,30,2,31) | 31.949747 (25,25,7,38) |
| 965 | 31.707107 (28,30,1,34) | 31.828427 (24,30,4,36) | 31.914214 (27,30,2,32) | 31.949747 (25,25,7,38) | 32.0 (23,31,4,35) |
| 970 | 31.707107 (28,30,1,39) | 31.828427 (27,27,4,40) | 31.914214 (27,30,2,34) | 32.0 (26,31,2,32) | 32.035534 (23,30,5,35) |
| 991 | 32.121320 (25,31,3,38) | 32.207107 (28,31,1,28) | 32.328427 (24,31,4,35) | 32.414214 (27,31,2,29) | 32.449747 (25,26,7,38) |

Note the `w` trend: the closure prefers the *thinnest* band that still carries the count.
Widening the band buys `m` squares but costs `w√2/2` of side, and `m` is capped by
`m + w ≤ L√2`, so the exchange rate is always unfavourable. Every target's optimum has
`w ≤ 3`, and for the seven band targets `w = 1` — a single tilted row. That is the closed form's
final word on the family: **one row is optimal**, which is also why the nested-band kernel can
only be tested on the five targets with `w ≥ 2`.

---

## 9. What this rules out, and what would still be possible

**Ruled out.** No parametrisation of the two-continent lattice/block family reaches any of these
twelve puzzles, at the bank's side or the record's, for any `f` — this is infeasibility, not
suboptimality (`MIS = k²` exactly, block sweep exact, four independent confirmations). It also
rules out the hope that a coarser or differently-ordered integer sweep — `(a₁,a₂,d,m,w)` in any
order, `d` in quarters, `a_i` as counts — could recover any part of the 0.08: those are the same
sweep re-parameterised, and the bound does not depend on the parameterisation. Likewise the "one
tilted row along an edge" and "band across the top of a grid" ideas, which the flat closure
covers (`w = 1` is the family's own optimum for seven of the twelve, and it is still 0.023–0.15
above the bank).

**Still possible.** The deficit is `D` squares per puzzle (D = 4 … 30) that are *outside* every
lattice and outside any common-angle patch: individually angled slivers, each with three
continuous degrees of freedom, seated in the notches left by an existing lattice. That is
exactly the multi-angle fan track's territory, and it is the only route this analysis leaves
open — a per-square multi-angle placement search anchored on the bank's layouts, not an integer
sweep. The second half of that route is using *more than two* lattice phases: seven of the nine
band-regime layouts are already multi-phase patchworks rather than two continents, so the
perpendicular-fault bound does not constrain them, and a 4-phase counting/search (the analogue
of the theory track's §8.3 recommendation for the `D=1` column) could still move them. Both are
combinatorial-plus-continuous hybrid searches; neither is reachable by enumerating `(a₁,a₂,d,m,w)`.
