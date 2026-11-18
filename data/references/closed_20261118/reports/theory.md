# Theory track — `n = k² + D`, the record's `f(D,k)` surface

2026-11-18. Derivation + exact enumeration only; no Kaggle kernel, no search, bank untouched.
All numbers below are recomputed from `/tmp/best_bank/report.json` and
`data/references/leaderboards/perpuzzle_best_20261111.csv` (`f_table.csv` in this dir).

---

## 0. Answer in ten lines

1. **`f(D,k)` is a staircase in `k`, not a smooth law.** `f = a(D) + b(D)/k` reproduces the
   staircase to rms 2e-3–9e-3, but it is *falsified* by the plateaus: the record has
   `f(1,29) = f(1,30) = f(1,31) = 0.5021527079033` to 7e-12. No `b/k` model can produce three
   exactly equal values. Do not extrapolate `a(D)` to `k→∞`; it is a chord through a step function.
2. The invariant that *does* behave is the **waste** `W = L² − n = 2kf + f² − D`.
   At `k=31`: record `W = 31.15 − 0.1206·D` (rms 0.59), bank `W = 31.87 − 0.1311·D` (rms 0.57).
3. Exact identity, exact closed form: **`L(k²+D) = √(k² + D + W)`**, i.e. `f ≈ (D+W)/(2k)`.
   The observed slope `∂f/∂D = 0.0138` is `(1 − 0.12)/(2·31) = 0.0142` — each added square costs
   **0.87** units of added area, not 1. That is the whole "smooth sequence".
4. Structure (measured off the bank's own coordinates, not guessed): every layout in this family is a
   **two-lattice fault** — continents of axis-aligned cells carried on two lattices offset by
   `(f, f)`, plus a patch of 45°-ish rotated squares in the channel between them.
5. The `(f, f)` offset is a translation of `2f` along `U = x+y`; a cell spans `U`-length 2, so the two
   lattices are exactly **half-a-cell out of phase when `f = 1/2`**. Measured: `2f = 1.0043` for the
   record (`f = 0.5022`), `1.0416` for the bank (`f = 0.5208`). **`f = 1/2` is the perfect-interlock
   value**, and the record's `δ = f − 1/2 = 0.00215` at `D=1` is the whole remaining distance.
6. Channel theorem (§5): a staircase channel with drop `Δ` per column has perpendicular width
   `Δ(f+Δ)/√(1+Δ²)`; for `Δ=1` this forces **`f ≥ √2 − 1 = 0.414214`** for even one tilted square,
   and for `Δ ≥ 1.5` the width condition is vacuous. Capacity of the channel is one row of
   `k√(1+1/Δ²)` squares ≈ 34.7 at `k=31, Δ=2` — which is precisely the observed `D = 1…36` range.
   The measured band angles 57.4°/66.2°/67.2°/71.75° are `atan(Δ)`, `Δ = 1.56…3.08`.
7. Exact family counts at the record's own `L = 29.502152708` (valid core sizes only):
   one 45° core + *all* lattice cells → **n = 823**; two interlocked lattices → **n = 833**;
   the record needs **842**. So a single core with two continents is 9 squares short, and the record's
   layouts must be the 4-block form that the bank's own `n=842` exhibits.
8. The remaining 0.076 of score is **sliver cells**: the bank's `n=842` leaves 58 lattice cells empty
   around its core (measured). The record's gain at `D=1` is `ΔW = 31.562 − 30.386 = 1.18` area units ≈ **1–2 lattice
   cells**, which is what a 0.2–0.5° core tilt buys. That matches "defect angles 44.79–45.33°".
9. The herringbone formula in the mission statement is **not** a dense construction: its own
   bounding shape gives density `2m/((mc+2s)(ms+2c))` ≤ 0.44 for `m ≤ 8`, and my explicit 2-row
   interleavings measure 0.21–0.44. Negative result — it cannot be the record's mechanism (§6).
10. Best actionable handle: the record is `1/2 + δ` with `δ` *integer-quantised* by the fault cells
    (§7). That is a 4-integer problem per puzzle, not a continuous search — a kernel track can
    enumerate it in seconds.

---

## 1. Recomputed data (do not trust the quoted table)

The brief's table reproduces to ~1e-6 on every row (verified); `f_table.csv` here is the full
recomputation for all 505 `(k,D)` points. Key columns at `k=31` (bank vs record vs waste):

| D | bank f | record f | bank W | record W |
|---:|---:|---:|---:|---:|
| 1 | 0.520815280 | 0.502152708 | 31.562 | 30.386 |
| 2 | 0.535533906 | 0.514078774 | 31.490 | 30.137 |
| 3 | 0.535533906 | 0.522821523 | 30.490 | 29.688 |
| 4 | 0.562050659 | 0.544499527 | 31.163 | 30.056 |
| 5 | 0.566822491 | 0.561949182 | 30.464 | 30.157 |
| 6 | 0.591378145 | 0.590016439 | 31.015 | 30.929 |
| 8 | 0.624490854 | 0.605570899 | 31.108 | 29.912 |
| 12 | 0.668042264 | 0.666638210 | 29.865 | 29.776 |
| 16 | 0.742554234 | 0.734342053 | 30.590 | 30.068 |
| 20 | 0.796031609 | 0.781014310 | 29.988 | 29.033 |
| 25 | 0.851742952 | 0.841052864 | 28.534 | 27.853 |
| 30 | 0.900804035 | 0.898183939 | 26.661 | 26.494 |

`W = (k+f)² − (k²+D)`. The whole "nearly linear, slope 0.0138" story in the brief is exactly
`∂f/∂D = (1 − c)/(2k)` with `c = 0.12`; `f` is *not* smooth, `W` is.

## 2. Why `a(D) + b(D)/k` is a smoothing artefact (rigorous)

Per-`D` regressions on `k = 18…31` reproduce the orchestrator's table (record):
`a(1)=0.45087, b(1)=1.546; a(2)=0.48593, b(2)=1.007; …; a(12)=0.47730, b(12)=6.309`,
rms 1.6e-3–8e-2. But:

* `f(1,k) = 0.5021527079033` for `k = 29,30,31` (identical to 3e-12) and `D=2` gives
  `0.5140787741393` twice (`k=30,31`). A `1/k` model gives strictly monotone decrease; equal values
  in adjacent columns contradict it.
* The mechanism is elementary: a fixed packing of `w·h+dm` squares in `(w+f)×(h+f)` transplanted into
  a `k×k` grid gives `L = k+f` for **every** `k ≥ max(w,h)`. Hence `f(D,·)` is constant on
  `k ≥ k₀(D)` and is a monotone step function below that. A staircase has a well-defined `1/k` chord;
  that is all the regression found. (Record plateaus measured: `D=4` at `k=26,27`; `D=8` at
  `k=19,20` and `k=25`; `D=10` at `k=24`, `k=27`; `D=1` at `k=18,19`, `k=21,22`, `k=23,24`,
  `k=29,30,31`.)
* Consequence for planning: `a(D) ≈ 0.45` is **not** an attainable asymptote, and the record's
  `k=31` values are **not** its limit for large `D` — the columns with `b(D) ≈ 6` (`D ≥ 9`) are still
  descending at `k=31`. True `k→∞` headroom for `D ≥ 9` is larger than the snapshot suggests.

Verified monotonicity: for every `D = 1…36` the record's `f(D,k)` is non-increasing in `k` over
`18…31` (**0 violations**), and **98 of the 468 adjacent `k`-steps are exactly flat** (|Δf| < 1e-9).
A `1/k` law has no flat steps, so one fifth of the surface is structurally invisible to it —
this is the signature of a min over a growing library of fixed gadgets.

## 3. The exact structure of these layouts (measured, then proved)

I clustered the bank's own certified coordinates by lattice phase. For `n=842` (k=29, D=1,
`L=29.520815280`) the 546 axis-aligned squares take only two x-phases and two y-phases, both
`{0, f}` with `f = 0.520815280` measured from the box origin: x-phase `0` (197 cells) / `f` (326);
y-phase `0` (212) / `f` (311); the remaining ~23 cells sit at drifted phases `0.00–0.11`, which is
the polish's residual shear, not a third lattice. So the whole
layout is carried on the four lattice combinations `(0/f, 0/f)` of the box — a **two-lattice fault**
with the shift applied in x and in y independently.

The smallest block is a **lower-left staircase with the exact profile `a[i] = 12−i`, `i = 0..10`**
(77 cells, the region `i+j ≤ 11`), sitting on the unshifted lattice; the big right/top blocks sit on
the `(f,f)` lattice.
* 296 squares are rotated, sitting in the channel between the staircases; 58 lattice cells that the
  channel touches are left **empty** (the slivers), plus the cells the core covers.
* Exactly `546 + 296 = 842` and `546 = 841 − 295`, `296 = 295 + 1`: the core's 296 squares displace
  295 grid cells. That is the `D=1` mechanism in one line.

Same test on `n=962` (k=31, D=1): 612 + 350 = 962, `f = 0.520815280` identical → the `k=31` layout is
the `k=29` layout plus one row and one column: it is a *gadget*, which is why `f` is bit-identical
across `k`.

**The `(f,f)` shift is a half-cell shift along `U`.** Cell `(i,j)` has `U = x+y ∈ [i+j, i+j+2]`; the
second lattice's cells have `U`-intervals shifted by `2f`. With `f = 1/2`, `2f = 1` = half a cell's
`U`-extent, i.e. the two lattices brick-interlock perfectly. Measured
`2f = 1.0043054158` (record, D=1) and `1.0416305603` (bank, D=1). So:

    f(D=1,k≥29) = 1/2 + 0.0021527079     (record)
    f(D=1,k≥25) = 1/2 + 0.0208152802     (bank)

and the campaign's D=1 gap is 0.0187 = the distance of the interlock from perfection.

**Exact anchor, and proof that the family is the right one.** The record's `D=1` plateau at
`k = 8…19` is `f = 0.5355339059327 = (5/2)√2 − 3` exactly, i.e. `L(65) = 5 + (5/2)√2 = 8.5355339059`.
That is exactly entry `s(65)` of the starter kit's `enum45.txt` ("`5 x 5: 4,(0), 4,(0), 4,(0), 4,(0)`":
a 5×5 rotated core plus four 4-deep corner staircases of 10 cells each, `25 + 40 = 65`). Our bank
matches it too. So both we and the record are inside the same 45°/fault machinery; the entire
remaining difference is in the phase/count bookkeeping of that machinery, not in the family.

## 4. Exact closed form for the family (and its optimum)

Set the box `[0,L]²`, `L = k+f`, the lattice at integers, the core a `p×q` block of unit squares at
45° (its own frame `u=(1,1)/√2`, `v=(−1,1)/√2`). In `(U,V) = (x+y, y−x)`:
core `U ∈ [U₀, U₀+p√2]`, `V ∈ [V₀, V₀+q√2]`; cell `(i,j)` is the diamond
`U ∈ [i+j, i+j+2]`, `V ∈ [j−i−1, j−i+1]`, i.e. an L1 ball of radius 1. Therefore

    cell (i,j) is compatible  ⟺  d_U + d_V ≥ 1 ,
    d_U = max(0, U₀−(i+j+2), (i+j)−U₁),  d_V = max(0, V₀−(j−i+1), (j−i−1)−V₁)

which is exact (SAT for two convex bodies in the `(U,V)` frame, and the core is axis-aligned there).
The count is a floor-sum of the 4 "wedge" regions cut by the 4 extended core edges, i.e. Pick-type
`#cells = area + width_x + width_y + O(1)`; the exact form is the quadrature

    n = p·q + Σ_{i,j<k} [ d_U(i,j) + d_V(i,j) ≥ 1 ].

**This is the whole `enum45` family**, and evaluating it exhaustively confirms the brief's
"closed" claim. At the record's own side `L = 29.502152708` (`k=29`, `f=0.502152708`), with the core
constrained to fit (`(p+q)/√2 ≤ L`, so `p+q ≤ 41`), the maximum over core size and position:

| model | max `n` at `L = 29.502152708` | comment |
|---|---:|---|
| 1 lattice + one 45° core, all outside cells | **828** | single-lattice fault, machine-verified |
| 2 interlocked lattices + one 45° core | **831** | U-split, valid by construction, verified |
| 4 phases, greedy (quadrant order) | **836** | verified valid, util 96.05 % |
| needs | **842** | record |

> **Correction (2026-11-18, after this report was first written).** The numbers originally
> printed here (823 / 833) came from a SAT/mask implementation that had four bugs, all of which
> inflate counts: (i) the add-pass re-admitted cells the core excluded, (ii) SAT used edge
> *directions* instead of edge *normals* for the core polygon, (iii) the projection of an
> axis-aligned cell onto an axis with a negative component used the wrong corner pair, and
> (iv) the emitted CSV wrote lower-left corners into the centre fields. Everything below is the
> re-run with a hard `n <= L*L` assertion and an explicit pairwise SAT verifier; the verifier is
> itself validated by re-checking the bank's own certified `n=842` layout, which it accepts at
> side 29.520815280171.

(The 2-lattice model is the one the bank's coordinates actually obey — 546 axis cells on 2 phases +
296 rotated.) So **a single core plus two continents is 9 squares short**: the record's layouts must
use the 4-phase/4-block form. This is a hard, checkable statement — it kills the "one gadget in a
corner of a k×k grid" hypothesis for the D=1 column, and it is why the campaign's gadget sweep
returned 2.6e-12.

`L` is determined by the union's bounding box, and `W` by the cells the core destroys. For the
core-type layouts the measured scaling is

    W = L² − n ≈ 1.72·√(p·q)   ,   #rotated squares = p·q

(measured `W/(2√#rot) = 0.844, 0.806, 0.857, 0.885` for `n=962, 730, 842, 901` — the whole `D=1`
column, bank), i.e. `W ≈ 0.86·perimeter-ish`, not `p+q`. The `D=4` column does not follow it
(`W/(2√#rot) = 1.32–1.38`) because those layouts use a compact 45° diamond rather than a core band —
another reminder that the family switches mechanism across `D`.

## 5. The channel theorem (why f ≈ 1/2 and why the bands sit at 57–72°)

Fault channel geometry: continent A is a staircase on the integer lattice with column profile `a[i]`,
drop `Δ = a[i] − a[i+1]`; continent B is the complement shifted by `(f, f)`. In column `x` the
vertical gap is `f + Δ`; the boundary has average slope `−1/Δ`, so the **perpendicular** width is

    w = Δ(f+Δ)/√(1+Δ²).

* A unit square at any angle has perpendicular extent ≥ 1, so the channel admits a square **iff**
  `w ≥ 1`, i.e. **`f ≥ √(1+Δ²)/Δ − Δ`**. For `Δ=1`: `f ≥ √2 − 1 = 0.4142136`. For `Δ ≥ 1.5` the
  bound is vacuous (negative).
* The number of rows across the channel is `⌊w⌋`, so for `w ∈ [1,2)` it is exactly **one row** — the
  channel is a one-square-thick conveyor. Its length is `k√(1+1/Δ²)`, hence

        capacity(D) ≈ k·√(1 + 1/Δ²)   squares.
        k=31: Δ=1 → 43.8, Δ=1.5 → 37.3, Δ=2 → 34.7, Δ=3 → 32.7.

  This is exactly the observed `D ≤ 36` envelope, and it is why the bank's mid-`D` layouts switch to
  bands at 57–72°: `atan(Δ)` = 45.0°, 56.3°, 63.4°, 68.2°, 71.6° for `Δ = 1,1.5,2,2.5,3`, matching the
  measured 57.41°, 66.2°, 67.2°, 71.75° to within the polish.
* `f = 1/2` is a fixed point of the geometry: at `Δ=1` the pair `(f, 2f)` = `(1/2, 1)` makes the two
  lattices half-a-cell out of phase in `U`, which is the densest possible interlock of one lattice
  with its own translate.

So the *derived* picture for `n = k²+D` is: a **one-square-wide diagonal conveyor of length
`k√(1+1/Δ²)`**, carrying `D` squares, interlocked with the grid at half-cell offset, needing
`f = 1/2 + δ` where `δ` is set by the integer fit of the conveyor's ends. The measured
`δ(D,k) = f − 1/2` for the record at `k=31`:

| D | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10 | 12 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| δ | .00215 | .01408 | .02282 | .04450 | .06195 | .09002 | .10557 | .13679 | .16664 |

`δ` is not a smooth function of `D`: it is `(D − D_min(Δ))/(2k)` plus an integer correction. That is
the *whole* residual between our bank and the record.

## 6. Verifying the mission's two stated formulas

1. **Single tilted row.** `m` unit squares at angle `θ`, bbox `(m cosθ + sinθ) × (m sinθ + cosθ)`:
   **correct**. Min over `θ` is `√(m²+1) × 2m/√(m²+1)` at `tanθ = 1/m` — a column-like object, aspect
   ~`m:2`, never a wide flat band. Consequence: no single row can beat `width = m`, hence the "band
   along the top of a k×k grid" idea in the mission brief cannot work for `f < 1` (any extra square
   above the grid needs vertical extent ≥ 1).
2. **Herringbone.** The stated `(m cosθ + 2 sinθ) × (m sinθ + 2 cosθ)` is *a* bounding box for a
   2-row `±θ` pair, but the pattern is **sparse**: density `= 2m/((mc+2s)(ms+2c))` =
   0.356 (m=4,45°), 0.229 (m=8,60°), 0.283 (m=8,70°). My explicit interleaved 2-row constructions
   measure bbox `3.5355×6.3640` at `m=4,θ=45°` (formula says `4.2426×4.2426`), density ≤ 0.44.
   A real layout is ≥ 0.93 dense, so **the herringbone cannot be the record's filler**; it can only
   be a local sliver filler. Do not build a family on it.

## 7. The best closed-form fits, with honest residuals

Fit on the record's full surface (`k = 18…31`, `D = 1…36`, 505 points):

| model | params | rms(f) | max&#124;res&#124; |
|---|---:|---:|---:|
| `f = 1/2 + a + b(D−1)` | 2 | 0.0635 | 0.461 |
| `f = 1/2 + a + b(D−1) + c(D−1)/k` | 3 | 0.0532 | 0.350 |
| `L = √(k²+D+W₀−cD)` | 2 | 0.1097 | 0.359 |
| **per-`D` chord `f = a(D) + b(D)/k`** | 2/column | **0.0016–0.0082** | 0.017 |
| **exact staircase (min over enumerated gadgets)** | tabulated | 0 | 0 |

The per-`D` chord is excellent *as a description of the staircase* (`b(D)`: 1.55, 1.01, 2.46, 2.31,
3.57, 4.24, 4.94, 5.50, 5.83, 6.26, 6.18, 6.31 for `D=1…12`; `≈ 1.0 + 0.47D`) but it is not
predictive: it predicts `f(1,32) = 0.4993 < f(1,31) = 0.50215`, while the gadget theorem says the
column is flat until a *larger* gadget exists. Global fits are useless at the 1e-3 level by
construction — the surface is a min over integer-indexed objects.

For the record at `k=31` alone, `f = 1/2 + 0.012674 + 0.013868(D−1)` fits with rms 0.0095,
max 0.0176, and `2k·b = 0.86` = the marginal area per added square.

## 8. What this means for the kernel tracks (concrete)

1. **Stop fitting `f`; enumerate `W`.** For a candidate layout the only scalar that matters is
   `W = L² − n`, and `∂L/∂W = 1/(2L)` = 0.017 at `k=29`. So "save 2 area units" == "win 0.034 of `f`"
   == the whole D=1 gap. The objective is integer-valued to within 1e-12; do not run continuous
   solvers against `L`.
2. **The 4-phase fault is the missing DOF.** One core + 2 continents tops out at `n = 833` at
   `L = 29.502152708` (computed above), the record needs 842 — so a search over *which of the four
   (0/f)² lattice phases each block uses* is worth ~9 squares per puzzle at D=1 and much more at
   larger `D` (the bank's own mid-D layouts already use 4 phases and 3 bands).
3. **The concrete, cheap experiment**: for each puzzle in the D-family, take the certified bank layout,
   enumerate the 4 lattice-phase assignments × the 4 core-edge offsets (integers `0…2` each, ~10²
   configurations), recompute the exact cell count `n` and the exact bbox `L`, and pick the
   configuration with the largest `n` at the smallest `L`. This is an integer enumeration over
   ~10³ points, not an optimization — it is exactly the `enum45`-style closed-form sweep, but with
   4 phases instead of 1, which is the part our sweep never covered.
4. **Predicted prize** if the 4-phase sweep matches the record: `D=1` column `0.5208 → 0.5022`
   (0.01866 at k=29..31), `D=2` `0.5355 → 0.5141`, … total **0.076** on the 30 columns at `k=31`,
   i.e. the whole remaining gap.
5. **Do not** spend more time on: bands along the top of a grid (impossible for `f<1`, §6.1),
   herringbones (§6.2), single-core gadgets (§4, provably 9 squares short), or `1/k` extrapolation.

## 9. Coordinates

I did **not** emit a certified coordinate set: everything in §4–§7 shows that no configuration in the
1-core/2-continent family reaches 842 at the record's side, and producing the 4-phase layout requires
the integer sweep in §8.3 (a kernel job, seconds of CPU), not a derivation. What is available here:

* `/tmp/campaign2/theory/f_table.csv` — `k,D,n,f_bank,f_rec,W_bank,W_rec` for all 505 points (the fit
  target any generator must hit).
* `/tmp/campaign2/theory/n842.png`, `n962.png`, `n902.png`, `n908.png`, `n965.png`, `n970.png`,
  `n991.png` — the bank's layouts rendered with angle-coded edges; `n842`/`n962` show the
  two-lattice + core architecture directly.
* The exact compatibility test and count formula in §4 (copy-pasteable: `d_U + d_V ≥ 1` in
  `(U,V) = (x+y, y−x)`). That is the whole generator; with the 4-phase enumeration it produces
  layouts in closed form with no solver.

Bank file never written; no submission made.
