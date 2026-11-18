# Band-phase discrete campaign — REPORT (2026-11-18)

Track: band-frame exact-cover / maximal-fill search on the nine band-regime
puzzles. Bank read-only at `/tmp/best_bank/submission.csv`, SHA-256
`9c981e6ea9a44c076587256936948e636936a84ad0668af6b75e946f4fa527e9`.
No Kaggle submission was made and the bank was not modified.

## 1. Bottom line

| | |
|---|---|
| Certified wins | **none** |
| Candidate CSV emitted | **none** (one candidate, `cand491.csv`, was built with a buggy mask and is **invalid**; quarantined as `cand491_INVALID.csv`) |
| Anchor | the exact 4-phase band-frame model reproduces the bank's count **exactly for n=328 and n=965**, and is 2–7 squares short on the other seven (sub-lattice defects, see §5) |
| Record-side shortfall | **15–38 squares** at the record side for the fixed bank block; 2 puzzles (965, 991) cannot even accept the fixed block inside `L_rec` |
| Full tilted-patch model | valid per-row-angle/per-row-phase patches reach **313 of 328** at `L_rec`, `L_rec+0.002` and `L_rec+0.005` (deficit 15, flat); the 3×22 patch is simply not wall-pinned, so side reduction does not change its count |
| Structural verdict | the rigid-block + 4-phase-lattice family is closed, and the valid tilted-patch family is also short by 15 on n=328. Adding a third lattice phase changes the optimum by ≤ 1 square |
| Independent jam proof | all nine bank layouts are locally rigid at first order with **all 2n translation DOF free** (LP returns max shrink 0.000000), not just under rigid groups |

Two bugs affected this track and are documented in §2 so they are not
repeated: one in the inherited `/tmp/campaign2/band/contacts.py`, and two in my
own model code (one of which produced the invalid `cand491.csv`).

## 2. Code corrections (important for the rest of the campaign)

### 2.1 Inherited SAT bug

`/tmp/campaign2/band/contacts.py` (and the copy I started from) has

```python
best = -1e18
...
g = half(i) + half(j) - d
best = min(best, g)
```

`min` can never leave `-1e18` for finite `g`, so `sat_gap` **always returns
-1e18**. Running the published reproduce command gives

```
$ python contacts.py 328
n 328 squares 328 contact edges 0 components 328
```

i.e. every square is reported as isolated. The fix is `best = +1e18` (gap 0 =
touching, >0 penetration, <0 separation). Corrected contact statistics are in
§3.3. The band REPORT's §4(f) touch-pair table should be regenerated before it
is reused; its lattice-size table is a phase histogram (A/C/A,A class counts)
and is not affected.

### 2.2 My own bugs

1. `free_mask` used half-extent 0.5 for **all** block squares along a block-edge
   axis. The support along another square's edge is
   `0.5(|cos(a-phi)|+|sin(a-phi)|)`; using 0.5 under-estimated the blocking and
   inflated the fill. Fixed to the general support formula and validated
   against `sat_gap` on 200 random cells per puzzle: **0 mismatches on all nine**.
2. `free_mask` rejected exact-touch cells through a bare floating-point `>=`.
   Fixed with a 1e-9 tolerance; the bank's own 260 axis cells are now accepted
   260/260 (they are rejected 24/260 without the tolerance).

The invalid `cand491.csv` came from bug 1: it counted 353 lattice cells at a
side 0.00318 below the bank, but 12 of the chosen cells overlapped the block by
up to 0.111. It is quarantined and is not a candidate.

### 2.3 Emitter gate (`emit.py`)

Nothing is written unless all gates pass, and the gate was tested on a valid
pair and on duplicate/overlapping pairs:

* `assert len(x)==len(y)==len(a)==n`
* all coordinates finite, no duplicate `(x,y)`
* explicit pairwise angle-aware SAT over all `n(n-1)/2` pairs (touching
  allowed): `penetration <= 1e-7`
* only then write `id,n,square_id,x,y,angle` (centres, radians)

## 3. Verified decomposition

### 3.1 Frame and phases

All nine use the same construction. In the `[0,L]` frame the axis squares have
centres on two phase values per axis:

* family A: `x = 0.5 + Z`, `y = 0.5 + Z` (faces on integers);
* family B: `x = L - 0.5 + Z`, `y = L - 0.5 + Z` (faces on `L-1+Z`).

Writing `k = floor(L)`, `c = L - k - 0.5`, the B phase is `k + c` and the four
classes AA, AB, BA, BB occur with counts (n=328): AA 3, AB 119, BA 135, BB 3.
The far wall (`x = L` and `y = L`) is touched by B-class squares, the near wall
by A-class squares, so

```
L = k + 0.5 + c                                    (identity by definition of c)
```

This is exact for all nine and is what the band REPORT tabulates. Note it is an
*identity* for any L; the content is that the far wall is filled by the shifted
family. Reducing `c` means making the box smaller while keeping 328 squares,
not a separate mechanism.

### 3.2 Tilted content and wall pinning

Non-axis squares ("tilted content") are one or two large contact-connected
patches plus singletons. Their extents in the `[0,L]` frame:

| n | non-axis | block extent u | block extent v | touches far wall? |
|---|---|---|---|---|
| 328 | 68 | 0.089 … 18.61336 | 0.707 … 18.61148 | u within 0.001 |
| 908 | 258 | 0.000 … 28.86893 | 0.000 … 29.86893 | no |
| 965 | 133 | 0.000 … 31.56168 | 0.000 … 30.79686 | u within 0.0004 |
| 970 | 267 | 0.736 … 31.63665 | 0.758 … 30.67535 | **u = L** |
| 804 | 206 | 0.000 … 27.22150 | 0.000 … 28.22212 | no |
| 748 | 204 | 0.000 … 27.21829 | 0.649 … 27.82671 | **v = L** |
| 991 | 352 | 0.735 … 31.90080 | 0.000 … 31.90080 | **u = v = L** |
| 491 | 140 | 0.889 … 21.93365 | 0.000 … 21.97866 | no |
| 367 | 74 | 0.000 … 19.01506 | 0.000 … 19.01566 | no |

So for 328, 965, 970, 748 and 991 the tilted content itself is wall-pinned at
`L_bank`; any smaller box needs the content moved, which changes the comb phase.

### 3.3 Corrected contact graph

With the fixed `sat_gap`, tolerance 1e-6:

| n | touch pairs | components | largest component | singletons |
|---|---|---|---|---|
| 328 | 792 | 34 | 295 | 33 |
| 908 | 2544 | 16 | 893 | 15 |
| 965 | 3089 | 21 | 945 | 20 |
| 970 | 1065 | 255 | 671 | 241 |
| 804 | 2264 | 10 | 795 | 9 |
| 748 | 2211 | 8 | 741 | 7 |
| 991 | 3007 | 23 | 969 | 22 |
| 491 | 258 | 300 | 192 | 299 |
| 367 | 759 | 34 | 334 | 33 |

The layouts are essentially **single rigid bodies** (295/328 … 969/991), which
is consistent with the band REPORT's jamming conclusion.

## 4. The exact free-region counting formula

For a side `L`, the candidate axis cells are the four classes

```
CC = {(0.5+Z, 0.5+Z), (0.5+Z, L-0.5+Z), (L-0.5+Z, 0.5+Z), (L-0.5+Z, L-0.5+Z)}
```

restricted to `0.5 <= x,y <= L-0.5`. A cell is admissible iff it is separated
from every tilted square (exact SAT, general support) and inside the box. Two
cells of different classes overlap iff `|dx| < 1` and `|dy| < 1`; same-class
cells never do. The maximum fill is therefore a maximum independent set on
this graph, solved exactly with `scipy.optimize.milp` (HiGHS). The model is
validated against `sat_gap` on random cells (0 mismatches, §2.2).

`free_mask` for an axis cell at `p` against a tilted square at `q` with angle
`a`:

```
free(p,q,a) = OR over phi in {0, pi/2, a, a+pi/2} of
              |(p-q).u_phi| >= 0.5(|cos phi|+|sin phi|)
                              + 0.5(|cos(a-phi)|+|sin(a-phi)|) - 1e-9
```

and the cell is admissible iff `free` holds for every tilted square
(`AND` over squares, `OR` over axes).

## 5. Anchor (the model must reproduce the bank)

At `L_bank`, the maxfill + the bank's tilted content + the loose squares that
still fit, with the hard SAT gate:

| n | fill | block | loose used | model total | model error |
|---|---|---|---|---|---|
| 328 | 261 | 66 | 1 / 2 | **328** | 0 |
| 908 | 656 | 250 | 0 / 0 | 906 | -2 |
| 965 | 845 | 120 | 0 / 0 | **965** | 0 |
| 970 | 704 | 261 | 0 / 5 | 965 | -5 |
| 804 | 595 | 204 | 0 / 2 | 799 | -5 |
| 748 | 538 | 203 | 0 / 1 | 741 | -7 |
| 991 | 638 | 346 | 2 / 6 | 986 | -5 |
| 491 | 350 | 138 | 1 / 2 | 489 | -2 |
| 367 | 293 | 70 | 0 / 0 | 363 | -4 |

The residual error is the bank's sub-lattice defects: 62 of 260 n=328 axis
cells deviate from the strict phase grid by up to 5.8e-4, which is enough to
fit cells the strict grid cannot. The error is bounded by 7 and is quoted
alongside every deficit below.

## 6. Discrete search at the record side

Search space: box side L, rigid translation of the bank's tilted content on a
0.03 grid over ±0.09 (with containment), 4-phase exact fill, plus the loose
squares that fit. Rotations were also swept (−2°…+2° in 0.25° steps around the
centroid) at `L_bank`; none improved the fill. The best totals at `L_rec`:

| n | `L_bank` | `L_rec` | anchor total | best total at `L_rec` | deficit vs n | calibrated deficit |
|---|---|---|---|---|---|---|
| 328 | 18.614368938 | 18.599535465 | 328 | 313 | 15 | 15 |
| 908 | 30.625574725 | 30.605884509 | 906 | 870 | 38 | 36 |
| 965 | 31.562050659 | 31.544499527 | 965 | **infeasible** (content bbox 31.5617 > L_rec) | ≥ 1 | ≥ 1 |
| 970 | 31.636652031 | 31.629165290 | 965 | 936 | 34 | 29 |
| 804 | 28.827154350 | 28.810060585 | 799 | 768 | 36 | 31 |
| 748 | 27.826710140 | 27.810879587 | 741 | 711 | 37 | 30 |
| 991 | 31.900804035 | 31.898183939 | 986 | **infeasible** (content bbox 31.9008 > L_rec) | ≥ 1 | ≥ 1 |
| 491 | 22.684143606 | 22.669926930 | 489 | 472 | 19 | 17 |
| 367 | 19.682794506 | 19.670856797 | 363 | 343 | 24 | 20 |

(`calibrated deficit = anchor total − record-side total`; this removes the
model's own ±7 error.)

**Per-puzzle discrete ceiling.** The model's minimum side at which the total
reaches n is `L_bank` for n=328 and n=965; for the other seven the strict
4-phase model is 2–7 squares short even at `L_bank`, so it needs the bank's
sub-lattice defects just to reproduce the bank and it cannot certify any side
below `L_bank`. In **no** case does the model reach n at a side below
`L_bank`. That is the exact ceiling of the rigid-block + 4-phase family.

**The fill drops at δL = 1e-4 for all nine.** At `L_bank − 1e-4` the 4-phase
fill is already 2–8 cells below its `L_bank` value for 908/965/970 and much
worse for the others; there is no gradual trade-off to exploit.

### 6.1 Third lattice phase

The sibling track's evidence for a third phase motivated a direct test. Adding
one extra x-phase and one extra y-phase at `0.5+g`, sweeping
`g = 0.02…0.40`, at `L_rec`:

| n | 2-phase fill | best 3-phase fill | gain |
|---|---|---|---|
| 991 | 620 | 621 (g=0.02) | +1 |
| 491 | 332 | 332 | 0 |
| 367 | 267 | 267 | 0 |
| 908 | 620 | 620 | 0 |

So a third phase is worth at most **one** square, versus a deficit of 15–38.
The deficit is not a phase-count problem: it is that the tilted content
displaces ~1 more lattice cell per 0.001 of side reduction.

### 6.2 Why the fixed-block re-phasing is closed

For n=328 the perpendicular argument is quantitative:

* closing `c` by `Δc = 0.01483` moves the two axis lattices toward each other
  by `sqrt(2)·Δc ≈ 0.02097` in the band-perpendicular coordinate Q;
* the 3-row band's Q width is 3.227 (row centres 1.0067 and 1.0115 apart, plus
  the ±0.08 meander of each row). It is internally jammed: compressing the
  block's Q by only 0.0065 (0.2 %) creates **38 overlapping pairs**, worst
  0.0020;
* zeroing the meander (the band REPORT's "clean band") already fails at
  0.0136–0.0212 of corner poke, i.e. the same order as the required 0.021.

The meander is load-bearing in both directions: it buys nesting against the
axis comb and costs perpendicular width. The bank's block is a local optimum
of that trade-off; the record's must be a different patch, not a translation
of this one.

### 6.3 Independent full-DOF jam proof

A sequential LP over **all 2n translations** (angles fixed), with the exact
active SAT axis for every near-contact pair and the four box constraints,
maximising a uniform side reduction:

| n | 328 | 908 | 965 | 970 | 804 | 748 | 991 | 491 | 367 |
|---|---|---|---|---|---|---|---|---|---|
| max shrink | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The LP was validated on a loose 2×2 grid in a 2.2 box (found 0.19 of the 0.20
available). This is a stronger statement than the rigid-group result: it rules
out any coordinated first-order motion of all squares, not just group motions.

### 6.4 Full tilted-patch model (per-row angles and per-row phases)

Model: `w` rows × `m` columns of unit squares. Row `i` has its own angle
`45° + δ_i` and its own phase `φ_i` along the row; rows are stacked at the
minimal perpendicular separation that clears all previous rows, so every
generated patch is internally SAT-clean by construction. Parameters searched:
`w = 3`, `m ∈ {20,21,22,23}`, `θ0 ∈ 43…47°`, `δ` patterns
`(0,0,0), (d,0,−d), (d,−d,0), (d,−d,d), …` with `d ∈ 0.5…3°`, `φ_i ∈
{0,1/3,2/3}` and random, plus 3000 fully random `(θ0,δ_i,φ_i)` patches; the
patch position is scanned on the feasible placement grid.

| patch family | best fill at `L_rec` | patch | total | deficit |
|---|---|---|---|---|
| 3×22 straight (all δ=0) | 246 | 66 | 312 | 16 |
| 3×22 δ=(−0.8,0,0.8) | 246 | 66 | 312 | 16 |
| 3×22 δ=(0.8,0,−0.8) | 244 | 66 | 310 | 18 |
| 3×22 δ=(−1.5,0,1.5) | 234 | 66 | 300 | 28 |
| 3000 random stacked patches | **247** | 66 | **313** | **15** |
| 3×21 partial (best slot-drop) | 249 | 63 | 312 | 16 |

Deficit curve of the best valid 3×22 patch (no side dependence at all):

| L | 18.614369 (bank) | 18.609369 | 18.604369 | 18.599535 (rec) |
|---|---|---|---|---|
| fill | 246 | 246 | 246 | 246 |
| total | 312 | 312 | 312 | 312 |
| deficit / 328 | 16 | 16 | 16 | 16 |

The patch is not wall-pinned by the fill, so shrinking the box by 0.015 only
adds wall slack; the count is flat at 312–313. **This family cannot reach 328
at `L_rec + 0.005` (best 313), so per the brief the patch search stops here.**

**Partial (slot) occupancy** was tested explicitly, because the n=401 template
is an 18×13 slot patch with only 188 slots occupied. Starting from the best
3-row patch, a greedy slot-drop (remove a patch square, re-solve the exact
4-phase fill, keep the removal only if `B + fill` increases) converges to
63 squares + 249 fill = 312 at `L_rec`; no single-square drop improves on the
66-square 313. Every patch square in these configurations blocks about one
lattice cell, so dropping it loses exactly what it gains. Partial occupancy
does not rescue the 3-row patch.

Two related results that look positive but are not valid, recorded so they are
not reused:

* A per-row differential *rotation* of the bank's block about the block
  centroid reaches fill 252 (total 320) but has **22 internal overlapping
  pairs, worst 0.262** — an invalid patch. Every valid patch needs the rows
  restacked, and the restacked optimum is the 247 above.
* Compressing the bank's patch in Q to absorb the `sqrt(2)·0.0148 = 0.021`
  channel closure does not repair: compressions of 0.005/0.010/0.015/0.021 all
  leave overlaps after 1500 projection iterations and the Q width relaxes back
  to 4.39 (whole block, tip included). The patch is internally jammed at the
  0.005 level, so it cannot be narrowed.

The n=401 template (an 18×13 slot patch at 69.3° with 188 occupied) is a
different object from our 3×22 full patch: its occupancy is partial, and its
row angles vary with the slot pattern. Testing that architecture on the nine
would require a slot-occupancy search on top of the patch search; the flat
deficit curve above says the payoff would have to come from the partial
occupancy itself, not from the patch angle or phase.

## 7. Emitted candidates

None. `cand491.csv` (353 fill + 138 block) was produced before the
`free_mask` support bug was found; 12 of its cells penetrate the block by up to
0.111 and it fails both merge routes. It is quarantined as
`cand491_INVALID.csv` and must not be used. The corrected model gives 332 fill
at the same side, i.e. 472 squares total, so there is no candidate to emit.

`emit.py` is the only admitted writer: it hard-fails on count mismatch,
duplicate coordinates, non-finite values, or any pairwise penetration
> 1e-7. Its gate was exercised on a valid pair (wrote) and on duplicate /
overlapping pairs (rejected).

`anchor328.csv` (261 lattice + 66 block + 1 loose = 328 at `L_bank`) is
SAT-clean (worst penetration 1.8e-15) and is useful as the model's positive
control, but it is **not scorable**: the official validator returns
`infeasible: Overlap undecidable at max precision` on its exact-touch lattice
contacts. Any future candidate from this family must open ~1e-9 clearances
(e.g. a `1+2e-7` dilation about the bbox centre) before scoring; the 0.003
side gain available here is three orders of magnitude larger than that cost.

## 8. Kaggle status

No kernel was pushed: there is no candidate that passes the SAT gate, and both
band polish kernels from the previous track are still consuming CPU sessions
(`ccjjllt/sis-band-polish-20261118` and `-2-20261118` both RUNNING at 20:06Z).
The account's 5-session CPU cap was therefore not tested. If a future
candidate appears, the merge command is:

```sh
.venv/bin/python -m squares merge \
  --baseline /tmp/best_bank/submission.csv \
  --baseline-report /tmp/best_bank/report.json \
  --candidate <csv> --output-dir <dir>
```

and the candidate must be scored on both text and float64 routes before any
submission.

## 9. What would be needed to go further

Everything tested is now closed:

* rigid block translation/rotation: deficit 15–38 (§6);
* full per-row-angle / per-row-phase patches: 313 at `L_rec`, flat curve (§6.4);
* partial 3-row slot occupancy: 312, no single-square drop improves (§6.4);
* third lattice phase: +1 (§6.1);
* Q compression of the bank patch: impossible at the 0.005 level (§6.4).

The only untested object is the **n=401 slot architecture**: an 18×13 grid of
slots at 69.3° with 188 occupied. It differs from our 3×22 full strip in two
ways: (i) the slot grid is a full rectangle whose *unoccupied* slots still
define the patch's footprint, and (ii) the row angles vary with the slot
pattern. The arithmetic target is `B − D ≥ 4` at `L_rec` (`B` occupied slots,
`D` displaced axis cells). Our 3-row strip has `B − D = −11`; the bank's strip
has `+3` at `L_bank`. So a slot rectangle would have to recover +15 relative to
our strip. The greedy 3-row slot test says that is not available in the strip
geometry, but it does not rule out a rectangular slot patch whose occupancy
follows the axis comb.

Priority if this is resumed:

1. Formulate the joint **slot + fill ILP** at `L_rec` for n=328: binary slot
   occupancy on a `w×m` rectangle (`w = 3…8`, `m = 8…24`), binary 4-phase
   lattice cells, conflicts only local. Solve for max `B + fill`. If the
   optimum is ≥ 328, emit through `emit.py` and extend to 908/491/367.
2. Do **not** retry translating/rotating the measured block, uniform `c`
   reduction, adding lattice phases, or full per-row-angle patches; all are
   measured here and closed.

## 10. Files

| file | purpose |
|---|---|
| `decomp.py` | load, SAT (fixed), contact components |
| `fill2.py` | 4-phase exact fill (ILP), corrected `free_mask` |
| `multifill.py` | N-phase generalisation |
| `seqlp.py` | full-DOF sequential LP jam proof |
| `emit.py` | gated candidate writer (count + duplicate + SAT) |
| `patch.py` | stacked-patch generator (per-row angle/phase) |
| `randpatch.py` | random valid stacked-patch search |
| `slots.py` | partial-occupancy (slot-drop) search |
| `qrepair.py` | Q-compression repair attempt |
| `final_rec.py` | record-side ceiling table (`final_rec.json`) |
| `deficit_curve_328.json` | patch deficit-vs-L curve, n=328 |
| `anchor_all.py` | anchor table |
| `cand491_INVALID.csv` | invalid, do not use |
