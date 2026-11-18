# master-626: exact ceiling of the 45°-core split-lattice family

**Bottom line: no packing below L = 25.520815280171 was found, and none exists in the
"one solid 45° square core + axis-aligned cells" architecture — including its most general
form (arbitrary row positions, arbitrary per-row x-phases, arbitrary core position, any
core size and any core angle). At the record side L = 25.511048764 the family tops out at
exactly 625 cells, i.e. one square short. The bank's 626-square layout is the exact
optimum of the family, sitting on a measure-zero tangent threshold.**

**No verified alternative core alignment beats 25.520815280171.** Every alignment tested
here — and the fan/shear variants tested by the sibling track — is strictly worse: the
17×17 tangent core, 12..18 cores at every position, rotated cores at atan(3/4), atan(4/3),
5/12, 12/5, 8/15, 15/8, 7/24, 24/7 and a 20°..70° sweep, 45° rectangular cores 14..19 per
side, and every non-zero fan pattern (>= 311 covered slots against the 288 budget). The one
profitable configuration in the whole architecture is the 17×17 tangent core at
`f = 17/√2 − 11.5`, which is exactly the bank.

All numbers below are from exact enumeration / exact integer counting and every claimed
packing was verified by full pairwise SAT (no overlaps, inside box, n <= L²+1e-9).

---

## 1. What the bank's n = 626 layout is (re-measured, confirmed)

| item | value |
|---|---|
| squares | 626 = 337 axis-aligned + 289 at exactly 45° |
| axis columns | 25: `0..11` and `12.52081528017144..24.52081528017144` (one gap 0.52081528017144) |
| axis rows | 25: `0..11`, isolated row at `12.26040764008572`, `13.52081528017144..24.52081528017144` (two gaps of 0.26040764008572037) |
| core | solid 17×17 block at 45°, centre `(11.76040764008572, 12.26040764008572)` in cell-centre coords, i.e. the diamond `|x-cx|+|y-cy| <= 17/√2` |
| kept cells per column | 24,22,…,2 \| 2,4,…,24,25 |
| kept cells per row | 25,23,…,1,3,…,25 |
| side | **25.520815280171426**, independently SAT-verified (min pair gap −6.7e−16, 0 overlaps, 0 outside) |

The diamond's bbox is `17√2 = 24.0416`; it pokes into the gap cross. The four quadrant
"staircases" are the exact optimal packings of the four free triangles (each square's far
corner must lie outside the diamond — greedy staircase is optimal).

## 2. The family and its exact counting formula

Lattice (per axis): `A` slots, a gap `h_l`, and `B` slots (or `A`, gap `h_l`, one isolated
middle slot, gap `h_r`, `B`, for the "mid" mode used on y by the bank). Core: solid
`m×m` block at 45°, i.e. the diamond of L1 radius `R = m/√2`, centred at `(cx,cy)`.

A unit cell at cell-offsets `(u,v)` from the core (0 = nearest) is **kept** iff

```
h_x + h_y + c + u + v >= R ,        c = 0.5·(#axes in "mid" mode)
```

so each quadrant keeps

```
Q(a,b,t) = #{(u,v) in [0,a)×[0,b) : u+v >= t} = a·b − t(t+1)/2   (a,b >= t)
t_q = ceil(R − c − h_x − h_y)
```

and

```
n = Q(A,C,t_bl) + Q(A,D,t_tl) + Q(B,C,t_br) + Q(B,D,t_tr)
    + (isolated middle-row cells) + (isolated middle-column cells) + m²
side L = max(A+B+h_l+h_r (+1 if mid), C+D+h_b+h_t (+1 if mid))
```

This model reproduces the bank **exactly**: `A=12,B=13,C=D=12`, `h=0.26040764008572037`,
`m=17`, all four `t=11` ⇒ 78+90+78+90 = 336 + 1 middle-row cell + 289 = **626** at
`L = 25.52081528017144`. The column/row counts match the measured bank exactly.

## 3. The closure (why the family cannot beat 25.520815280171)

The four quadrant sums are `s1=h_l+h_b, s2=h_l+h_t, s3=h_r+h_b, s4=h_r+h_t`, and

```
s1 + s4 = s2 + s3 = Sx + Sy = 2f          (f = L − 25 for 25 slots per axis)
```

`t_q = 11` (the only regime that yields 626, because it subtracts only 66 per quadrant
instead of 78) requires `s_q >= R − c − 11`. Summing over the four quadrants:

```
4f = Σ s_q >= 4(R − c − 11)   ⇒   f >= R − c − 11 = 17/√2 − 11.5 = 0.5208152801714407
```

So at **any** `f` below that value at least two quadrants fall to `t = 12`. More strongly,
if `f < τ = R−c−11` then `s1+s4 = 2f < 2τ`, so at most one of `{s1,s4}` and at most one of
`{s2,s3}` can reach `τ` — **at most two quadrants** can be in the good regime.

Exhaustive breakpoint enumeration (all integer block splits, all modes, all gap positions
including asymmetric/off-centre cores, all `m`; the count is a step function whose optimum
lies on the lines `P±cy ∈ Z`, enumerated exactly) gives:

| L | max n over the whole family | attained by |
|---:|---:|---|
| **25.5208152801714407** | **626** | m=17, 12/13 × 12/1/12 split, all t=11 (the bank) |
| 25.52081528 (1.7e-10 below) | 625 | m=12 |
| 25.511048764 (k=25 record) | **625** | m=12 |
| 25.502152708 (k=29..31 record) | 625 | m=12 |
| 25.500000000 | 625 | m=12 |

So the bank is *exactly* the family optimum, and the first rung of the ladder
(25.511048764) is unreachable by one square.

(The sub-`g*` values in this table are the maxima of the *strictly larger* row family of
§4, which contains the split lattice; they are therefore valid upper bounds for both. The
plain split-lattice enumeration alone gives 617 at 25.511048764.)

## 3b. Tangency bound and the covered-count table

The bound can be written in the form used by the sibling track:

```
tangency gap   g* = m/√2 − (K/2 − 1) = 17/√2 − 11.5 = 0.520815280171307
               (K = 25 lattice slots per axis, so K/2 − 1 = 11.5)
```

(the bank file's side, 25.520815280171426, is this value to 1.2e−13, i.e. float
precision; the exact tangency is at L* = 25.520815280171307)

i.e. the side `L = K + f` at which the 17×17 diamond's boundary exactly passes through the
far corners of the `t = 11` boundary cells. For the bank's split (12/13 columns,
12/1/12 rows) the number of **covered** lattice slots (the 625 slots that the diamond
intersects, which is what has to be paid for) is a two-valued step function of the gap:

| g (gap) | L = 25+g | covered slots | kept | n = 914 − covered |
|---:|---:|---:|---:|---:|
| 0.000 | 25.000000000 | 337 | 288 | 577 |
| 0.100 | 25.100000000 | 336 | 289 | 578 |
| 0.300 | 25.300000000 | 336 | 289 | 578 |
| 0.500 | 25.500000000 | 336 | 289 | 578 |
| 0.510 | 25.510000000 | 336 | 289 | 578 |
| 0.520 | 25.520000000 | 336 | 289 | 578 |
| 0.520800 | 25.520800000 | 336 | 289 | 578 |
| **0.520815280171 (=g\*)** | **25.520815280171** | **288** | **337** | **626** |
| 0.521 | 25.521000000 | 288 | 337 | 626 |
| 0.550 | 25.550000000 | 288 | 337 | 626 |
| 0.800 | 25.800000000 | 288 | 337 | 626 |
| 1.000 | 26.000000000 | 288 | 337 | 626 |
| 1.500 | 26.500000000 | 288 | 337 | 626 |

Two exact statements follow:

1. **288 is the minimum covered count of the gapped-lattice family at this side.** Over
   all `g <= g*` the minimum of `covered(g)` is 288 and it is attained *only* at
   `g = g*`; for every `g < g*` the count is 336 (a 48-cell cliff, see §3). Since
   `n = 914 − covered`, no member of the family has `n >= 626` below the tangent side.
2. For `g > g*` the covered count stays at 288 but the side grows linearly, so the family
   only gets worse. The tangent point is the unique optimum, not merely a local one.

The covered-count budget is what makes the fan/shear variants hopeless: every non-zero fan
pattern of the same core reports **>= 311 covered slots against the 288 budget**, i.e. it
loses at least 23 cells at the same side.

## 4. The generalised row family (strictly larger) also caps at 625

The most general arrangement of axis cells around **one convex rotated-square core** was
solved exactly by a row decomposition: for a row at height `y` the core blocks an interval
`(lo(y), hi(y))` (widest over the cell's own height band), and the row's capacity is

```
g(y) = [lo−0.5]⁺ + 1  +  [L−1.5−hi]⁺ + 1       (cells packed from both box edges)
```

Rows only need pairwise spacing >= 1, so the total is a 1-D weighted-interval scheduling
problem; `g` is monotone in `|y−cy|`, so the optimum is two edge blocks plus at most one
middle row. This family allows **per-row x-phases and independent row positions** — it is
strictly more general than the split lattice (it contains the bank exactly: 337 axis cells
at `cx,cy = (11.7604, 12.2604)`).

Result (exact breakpoint enumeration over `P±cy ∈ Z`):

| L | best axis cells + core = n |
|---:|---|
| 25.520815280171 | 337 + 289 = **626** (bank; m=17) |
| 25.511048764 | 481 + 144 = **625** (m=12) |
| 25.502152708 | 481 + 144 = **625** |
| 25.500000000 | 481 + 144 = **625** |

Verified constructions at L = 25.511048764 (all SAT-clean, 0 overlaps, 0 outside,
n <= L²): `cand_m12.csv` (625 cells: 481 axis + 12×12 core), `cand_m14.csv` (621),
`cand_m16.csv` (617), `cand_m17.csv` (602). The 625-cell one is one square short of 626 —
nothing in the family can add the last square.

## 5. Alternatives tested and rejected (all exact counts, all worse)

| variant | best n at L=25.511048764 | note |
|---|---:|---|
| core angle θ = atan(3/4) | ≤ 605 | 45° wins by a wide margin |
| core angle θ = atan(4/3), 5/12, 12/5, 8/15, 15/8, 7/24, 24/7 | ≤ 605 | |
| θ swept 20°..70° (5° steps) | ≤ 608 | |
| 45° rectangle cores p×q (14..19)² | ≤ 617 | square core is best |
| core shifted off the gap centre ("extra lattice phase") | ≤ 625 | enumeration includes all shifts |
| 'gap' vs 'mid' vs 'void' modes per axis | — | bank's (gap, mid) is optimal |
| 26 slots / axis | impossible (L < 26) | |

## 5b. No 626th square fits in the best 625-cell layout (any angle)

The 625-cell layout at L = 25.511048764 (481 axis + 12×12 core) has 25.81 of free
area, so it is natural to ask whether one extra square placed at *any* angle closes
the gap. A grid search over (x, y) (step 0.06) × 37 angles (0°, 45°, 5°..175° step 5°)
with the exact 6-axis SAT against all 625 squares finds **no feasible placement at any
angle and any position**. The free area is entirely in slivers thinner than one unit
square (it is the 0.5-wide halo between the diamond and the row-packed cells). The same
holds for the m=14 and m=16 variants. So the 625-cell construction is saturated.

## 5c. Two cores are impossible in this box

Two solid 45° `m×m` cores need a centre separation of `m√2` in one of the four
diagonal-aligned directions, so both bounding boxes (`m√2` each) must fit. At
L = 25.51 the only disjoint pairs that fit are `m ≤ 11` arranged diagonally
(e.g. centres offset by ±4 in both axes), and the exact row DP gives only
`2·121 + 65 = 307` cells. Two large diamonds simply do not fit — the 45° diamond is
too "fat". The multi-core route is closed.

## 6. Engine / local-search status

`/tmp/campaign2/engine` (contact-force + fast-LP port) reproduces the bank layout
(E = 4.5e-24 at L = 25.520815280171). At the record side L = 25.511048764 the L-BFGS
penalty relaxer stops after 0.1 s with **1936 overlapping pairs** and max penetration
8.25e-4: the bank layout is a single rigid body, exactly as the earlier rigidity study
found. No local repair exists — the 0.0098 deficit cannot be removed by continuous motion.

A fixed-side annealer (numba) was packaged at `kernel/` as a contingency. **It was not
pushed**: rejected by the CPU-session cap on the first attempt, then stood down on
instruction, so no Kaggle compute was spent on 626. The annealer route is anyway the wrong
vehicle for this gap — the target needs a change of architecture, not a local repair.

## 7. What the record must be doing (and what is left)

Since the entire "one solid square core + axis cells" architecture is closed at exactly
25.520815280171 (626) and 625 below it, and no 626th square fits in the best 625 layout at
any angle, the record's 626 at 25.511048764 needs a **different architecture**. Two
directions were eliminated here (two large cores cannot fit; extra core squares are net
loss because every rotated 2×k notch is too small to host an axis unit square). What is
left is a genuinely different core alignment/size, or a tilted-lattice-patch plus
third-phase construction — not reachable by this core, as the f=0.502152 record itself
shows. The C++ engine's GA on the top-16 puzzles is the right vehicle for that; local row
optimisation is exhausted. The gap to close is exactly one unit square (0.5 of area,
0.0098 of side).

## 8. Files

| file | contents |
|---|---|
| `REPORT.md` | this report |
| `exact.py` | exact 4-quadrant model + breakpoint enumeration (family ceiling) |
| `rowexact.py` | exact row-family breakpoint enumeration (`P±cy ∈ Z`) |
| `verifyrow.py` | builds the best row-family constructions from the enumeration |
| `verify.py` | numpy exact pairwise-SAT verifier (containment, n<=L², min gap) |
| `slot.py` | any-angle single-square insertion search |
| `twocore.py` | two-core row DP |
| `anglescan.py`, `rectcore.py`, `anglerow.py` | rotated / rectangular core scans |
| `cand_m12.csv` … `cand_m17.csv` | SAT-clean row-family constructions at L=25.511048764 (625/621/609/617/602 cells) |
| `kernel/` | Kaggle CPU kernel (fixed-side annealer) + metadata — **not pushed** |
| `push.log` | the single refused push attempt (CPU cap), then stood down |

The bank (`/tmp/best_bank/`) was not modified and nothing was submitted to Kaggle.
No merge was run because no candidate has n = 626 with a smaller side (the 625-cell
constructions are ceiling witnesses for the family, not submissions for n=626).
