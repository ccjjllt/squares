# staircase65 — staircase-polyomino core at n = 65: documented NEGATIVE

Track: `staircase65` (subagent). Target: beat the bank's `n=65` layout
`L = 8.535533905932745`, which is exactly tied with the record and lifts to
twelve puzzles `n = 65, 82, 101, 122, 145, 170, 197, 226, 257, 290, 325, 362`
via `/tmp/campaign2/lift.py --k0 8 --D 1 --ks 8 … 19` (0.77·ΔL on offer).

**Verdict: closed. No 65-square packing below 8.535533905932745 exists in this
family. No candidate CSV, no Kaggle push, no submission.** The result is
consistent with, and now bounded exactly by, the sibling track's tangency
theorem (§2). Total compute spent: ~12 min of local CPU; the Kaggle account
was not touched (0 kernels pushed, 0 submissions).

Bank baseline used throughout: `/tmp/best_bank/submission.csv`
`n=65` group (25 squares at 45°, 40 at 0°).

---

## 1. The exact anchor (plan step 1) — reproduced to the last digit

`anchor.py` re-counts the bank's own geometry with an explicit
angle-aware SAT test (4 separating axes, **corners touching allowed**;
`overlap()` returns True only for positive-area intersection):

| quantity | value |
|---|---|
| core squares (angle π/4, integer `(u,v)` centres in `[-2,2]²`) | 25 |
| axis squares (angle 0) | 40 |
| split-grid parameter `t = f/2` recovered from the axis lattice | `0.2677669529663687` |
| **covered** grid cells (positive-area overlap with the core) | **24** |
| kept axis cells | 40 |
| `n = 25 + 64 − 24` | **65** |
| pairwise SAT over all 65 squares | **0 overlaps** |
| `L = max(x-span, y-span)` | **8.535533905932745** (error 0.0) |

Covered cells are exactly `i+j ≤ 2` in each 4×4 quadrant (`4 + 8 + 12 = 24`);
the kept set is exactly the four staircase triangles `i+j ≥ 3`
(10 cells each). The counting identity `n = 64 − c + 25 = 89 − c` therefore
requires `c = 24`, confirmed.

The bank layout is a **knife-edge**, not a plateau point in every direction:
at `du=dv=0`, `c(t)` is 40 up to `t = 0.2677669529…` and drops to 24 exactly at
`t* = (5/√2−3)/2`. Any core offset (`du,dv ≠ 0`) raises `c` to 28–32 at `t*`,
i.e. `n ≤ 61`. That is the "cliff" seen by earlier tracks.

---

## 2. Exact tangency bound (sibling track) — the family is tight at the bank

The sibling track proved the tangency bound for this construction:

```
f = m/√2 − (K/2 − 1)          (m = core side in cells, K = grid side in cells)

n = 65:  m = 5, K = 8   →   f = 5/√2 − 3 = 0.5355339059327378
```

The bank's `n=65` gap is `f = L − 8 = 0.5355339059327450`, i.e. **identical to
the bound to 3e-15**. The bound is attained only by the solid `5×5` core at
`45°` in the `8×8` split grid, and the covered count is `24` for every gap
`g ≥ g*`; at `g* − ε` a full ring of 24–48 cells appears (the cliff). The
C++ GA's best near-miss `h = 8.5338` carries 4.6e-6 residual overlap, i.e. it
is infeasible, not unfinished.

## 3. Corridor argument (same conclusion from the geometry side)

The only region where the 45° core can poke out of the 64-cell union is the
cross corridor of width `2t` between the four quadrant blocks. A unit 45°
square needs its full diamond (width `√2` in `x` and `y`) to enter a corridor;
for any `2t < 1` no cell can be *inside* the corridor. The only admissible
contact is the **90° corner-on-side** contact used by the solid `5×5` at its
four tips (each tip touches the staircase inner corner at one point). A
staircase boundary cannot improve this: its steps are `1/√2` in `(x,y)`, while
the axis staircase has steps `1`, so a staircase core can only trade
corner contacts for edge contacts at a strictly larger channel width
(the measured floor of the staircase family is `8.8284 > 8.5355`, §4).
Equivalently: no unit square fits in a corridor narrower than 1; only a
90° corner can, and the solid core already uses the four available corners.

---

## 4. What was actually swept (plan steps 2–3)

Family: a **25-cell 45° polyomino core** (rows in `v`, row lengths
`l_0..l_{m-1}` with `1 ≤ l_i ≤ 6`, `Σ l_i = 25`, `m ∈ 4..7`, unimodal
lengths) with monotone integer `u`-offsets `s_i` (`0 ≤ s_{i+1}−s_i ≤ 2`),
against the `8×8` split grid (four `4×4` quadrants, inner edge at `t`,
`L_grid = 8 + 2t`). Shapes canonicalised under the 8 dihedral symmetries:
**4 261 distinct polyominoes**.

For every shape × offset `(du,dv) ∈ {0,0.1,…,0.9}²`, the smallest `t` with
`covered = 24` was found by bisection on the exact positive-area overlap test,
and `L` was taken from the **true bbox of kept cells ∪ core** (this matters:
at `t=0` a core can cover only 24 cells by poking outside the 8×8 square, and
the naive `L = 8+2t` under-reports it — the corrected code does not).

| | |
|---|---|
| shapes swept | 4 261 |
| shapes with a `c=24` plateau | 4 261 |
| **minimum L** | **8.535533905952** (= bank, solid `5×5`, `du=dv=0`, `t*=0.267766953`) |
| shapes with `L < 8.5355339` | **0** |
| second best | **8.818376618429** (`t=0.409188309`), next 3 shapes same value |
| next | 8.828427125 (`= 8 + 2(√2−1)`, the corridor floor) — 9 shapes |
| `L < 8.9` | 68 shapes |
| `L < 9.0` | 869 shapes |
| median / max | 9.101 / 9.394 |

### Best L per shape family (row-length pattern, best over offsets/shapes)

| pattern | best L | Δ vs bank |
|---|---|---|
| **(5,5,5,5,5)** — solid 5×5 | **8.535533906** | 0 |
| (2,6,6,6,5) | 8.818376618 | +0.28284 |
| (3,5,6,6,5) | 8.818376618 | +0.28284 |
| (1,5,6,6,4,3) | 8.818376618 | +0.28284 |
| (1,2,3,4,5,5,5) | 8.818376618 | +0.28284 |
| (1,6,6,6,6) | 8.828427125 | +0.29289 |
| (1,4,4,4,4,4,4) | 8.828427125 | +0.29289 |
| (4,4,4,4,4,5) | 8.838477631 | +0.30294 |
| **(3,4,5,5,4,3,1)** (brief example) | 8.949747468 | +0.41421 |
| **(2,4,5,5,5,4)** (brief example) | 9.010407640 | +0.47487 |
| **(1,4,5,5,5,4,1)** (brief example) | 9.071067812 | +0.53553 |
| **(2,5,5,5,5,3)** (brief example) | 9.091168825 | +0.55563 |

The explicit staircase shapes named in the plan are all **worse than the bank
by 0.41–0.56**, not close. The shapes that come nearest (still `+0.283`) are
near-solid `5×5`-ish bodies with one extra row (`W,H = (5,6)` or `(6,6)`), i.e.
they approach the rectangle, not the staircase.

### Exact count for the best non-solid shape

`rows = (2,6,6,6,5)`, offsets `(0,0,0,0,0)`, `du=0, dv=0.3`, `t=0.409188309`:

* `covered c = 24`, kept `40`, core `25` → **n = 65**
* `L = 8.818376618429` (`≈ 5 + 2.7√2`)
* explicit pairwise SAT over all 65 squares: **0 overlaps**
* so it is a *valid* 65-square packing — just 0.28284 worse than the bank.

This is the exact count the track asked for: the staircase family does produce
valid `n=65` packings, but the best of them is `L = 8.8184`, and the unique
optimum over the whole family is the bank's solid-5×5 `L = 8.5355`.

---

## 5. Kaggle status

* **No kernel pushed. No submission made.** The account's 5-session cap was
  not touched; nothing was retried.
* No `candidate.csv` was produced: the mission requires a candidate strictly
  below the bank on both scoring routes, and there is none.
* Work was stopped on instruction once the sibling track's exact bound and the
  corridor argument closed the family; the sweep numbers above are from the
  local run already completed.

## 6. Artifacts (all local, `/tmp/campaign2/staircase65/`)

| path | content |
|---|---|
| `geom.py` | SAT (4 axes, touching allowed), closed-form axis-vs-45° overlap, bbox/side |
| `anchor.py` | exact reproduction of the bank `n=65` (c=24, n=65, L exact, 0 overlaps) |
| `shapes.py` | staircase-polyomino generator (unimodal rows, monotone offsets, D4 canon) |
| `search.py` | coverage count / minimal-`t` bisection / true bbox |
| `sweep_sym.py` | 4 261 shapes × 100 offsets sweep; writes `sweep_sym.json` |
| `sweep_sym.json` | per-shape best `(L, du, dv, t, cells)` |

## 7. Bottom line for the campaign

The remaining `n=65` hope was a non-rectangular core. It is now closed by two
independent arguments (exact tangency bound `f = 5/√2−3`, corridor/90°-corner
argument) and by an exhaustive sweep of 4 261 staircase polyominoes with a
minimum of `8.535533905952` — the bank itself. The twelve-puzzle
`n = k²+1, k = 8..19` lift therefore requires a **different contact
topology**, not a staircase core in the split grid. Do not spend further
compute on 45° polyomino cores at `K = 8`.
