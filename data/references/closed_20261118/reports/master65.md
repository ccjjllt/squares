# n=65 master-gadget campaign — REPORT (2026-11-18)

Track: `master65` (single target n = 65 = 8²+1, the 12-puzzle D=1 lever
k = 8..19). **Outcome: no improvement. The family is closed at exactly the
bank's side.** Nothing was pushed to Kaggle and nothing was submitted;
`/tmp/best_bank/` was only read.

---

## 1. Bottom line

| | |
|---|---|
| Bank n=65 | `L = 8.535533905932745`, `f = L−8 = 0.5355339059327449` |
| Record n=65 | `8.535533905932730` (tie; record = `5 + 2.5√2 = 8.535533905932738`) |
| Best found below the bank | **n = 64** (not 65) at every f < f\* |
| Exact family ceiling | `f* = 2.5√2 − 3 = 0.5355339059327378` = the bank's f to 1.4e-14 |
| Binding constraint | staircase tangency of the solid 5×5 45° core against the split 8×8 grid; the four tip squares of the core are kinematically locked |
| Value forgone | `≈ 0.95 · Δf`; a master at f=0.53 would have been ≈ 5.2e-3 |

The bank's n=65 is *not* a loose local optimum: it is the exact algebraic
optimum of the entire "axis split grid + solid rotated core" family, and the
count function has a **16-square cliff** immediately below it.

---

## 2. The exact family ceiling (counting formula)

Architecture (verified to be the bank's own): box `[0,L]²`, `L = 8 + f`;
axis unit cells in a 2-phase split grid — 4 columns flush left, 4 flush right,
gap `f` in the middle (same in y), 64 cells at
`±(0.5 + f/2 + i)`, `i = 0..3`. Core: `m×m` block of unit squares at angle θ
on the θ-lattice, centred at the box centre.

For the 45° core the cell/square overlap test is an exact octagon
(`|dx|≤1.2071, |dy|≤1.2071, |dx±dy|≤1.7071` with
`1.2071 = 1/2 + 1/√2`, `1.7071 = (1+√2)/√2`), so the count is exact:

```
K(m,f) = # { (i,j) in [0,3]^2 :  i + j <  m/√2 − f }      (per quadrant)
n(m,f) = m² + 64 − 4·K(m,f)
```

* m=5: `K=6` iff `f ≥ 5/√2 − 3 = 0.5355339059327378`; then **n = 65**.
  Below it `K=10` and **n collapses to 49** (16 cells are lost in one step).
* m=4: `K=6` at all admissible f, but `n = 16 + 64 − 24 = 56`.
* m=6: bbox 6√2 = 8.485 requires f ≥ 0.485; at f = 0.4855 `K=10` → **n = 60**;
  `K=6` needs `f < 6/√2 − 3 = 1.2426` (L ≤ 9.24, n = 76) — outside the window.
* m ≥ 7 is excluded outright by the 45° bbox `m√2 > L` (only m ≤ L/√2 = 6.04
  fits below L = 8.5355).

θ ≠ 45°, asymmetric arm splits, off-centre cores, solid rectangles
`(5,6),(6,5),(4,7),(7,4),(4,8),(8,4),(6,6),(3,9),(9,3),(7,5),(5,7)`,
gaps 0.45–0.5355, centre offsets ±0.5: all ≤ 62 at g = 0.5355 and worse below
(this reproduces, independently, the negative your multi-angle track reported).

**Tangency bound (multi-angle track, exact):**
`f = m/√2 − (K/2 − 1) = 5/√2 − 3 = 0.5355339059327`, with the covered count
24 for every `g ≥ g*` — i.e. the bank's f *is* the bound, and the bound is
attained only at equality.

### 2.1 Anchor (reproduced exactly)

`m=5, θ=45°, centred, f = 0.5355339059327449` →
64 cells, **kept 40, core 25, n = 65, L = 8.535533905932745**, and the kept
set matches the bank's 40 axis cells to 2.7e-15 (`core.py: anchor()`).
The bank sits 1.4e-14 *above* the exact threshold, which is why it is valid
(all 16 tangency cells have zero-area contact).

### 2.2 Why the cliff cannot be repaired

At `f < f*` the 16 cells on the staircase line `i+j=3` are penetrated by
0.00391 (at f=0.53). They are touched by the **outer ring** of the core:
per quadrant the corner tip (uv `(±2,±2)`, i.e. xy `(0,±2.828)`) covers two
of them and the edge squares uv `(±2,±1)/(±1,±2)` cover the other two.
A tip square is edge-adjacent to both its in-block neighbours, so *any*
inward displacement `d` gives `|Δu| = 1−d < 1` **and** `|Δv| = d < 1` against
one neighbour — i.e. an overlap. The tip can move only *outward* (worse).
Removing the 4 tips buys 8 cells but costs 4 squares (net +4 from the 49
floor); removing the whole 12-square outer ring buys all 16 cells but costs
12 squares (n = 53). No rearrangement of the solid family recovers the 16.

---

## 3. Independent exhaustive / stochastic negatives

1. **Small-core exhaustion** (`smallcore.py`, exact bitmask DFS over all
   45°-lattice sites × 8 fractional offsets): the minimum size of the killed
   cell set for a k-square core is **exactly k** for every k = 2..8, at every
   f tested (0.5355, 0.5300). Hence `ρ = |C| − |R| ≤ 0` for all cores of ≤ 8
   squares, i.e. `n ≤ 64`.
2. **Simulated annealing over arbitrary 45° core sets** (`search45.py`,
   10 fractional lattice offsets × 6 seeds × 250k moves, objective
   `ρ = |C| − |killed|`): best `ρ = 0` at f = 0.5350, 0.5340, 0.5320, 0.5300.
   The optimum found is a 4-square pinwheel in the central cross
   (xy ≈ `(4.2675, 3.5604), (3.5604, 4.2675), (4.9746, 4.2675), (4.2675, 4.9746)`
   at 45°) which kills exactly 4 cells → **n = 64** (60 kept + 4).
3. **Void-packing decoupling** (`voidpack.py`): with the kept set fixed to the
   staircase `i+j ≥ 3` (40 cells), `n = 40 + m(V)` needs **25** squares in
   `V = 24 cells + cross` (area 32.25–32.85). At f = f\* the solid diamond
   attains exactly 25; at f ≤ 0.53 the best SA residual is E ≈ 5e1 (no
   packing) and a rigid 5×5 scan over θ = 45°±8°, offsets ±0.7 gives ≥ 7
   overlapping kept cells minimum. The other patterns are worse by area/width:
   `i+j ≥ 4` (24 kept) needs 41 squares inside a 40-cell plus whose fat area
   is only 40.5 vs the 48.25 available (and the arms are 0.5 wide);
   `i+j ≥ 2` (52 kept) needs 13 squares inside a 4.5×4.5 plus of arm width 2.5
   where the axis maximum is exactly 12.
4. **C++ GA (multi-angle track):** best near-miss at `h = 8.5338` with
   residual cost `4.6e-6` — i.e. strictly infeasible, and 2e-3 above the side
   needed for any score.
5. **Full 65-square fixed-side SA** (prepared, see §4): the only completed
   local runs are short smoke tests from the bank layout — at L = 8.5350 /
   8.5300 they stall at residual energy ≈5e-5 with a box violation (5 s
   budget), and at 8.5200 at 4.2e-4; no feasible state below the bank. A
   longer 300 s local run was killed by the harness before producing output.
   The 420 s Kaggle ladder was built but not run (stand-down).

---

## 4. Assets kept (documented negatives, not pushed)

* `/tmp/campaign2/master65/sa_kdir/` — complete n=65 fixed-side annealer
  (kernel.py + anneal_core.py + kernel-metadata.json, id
  `ccjjllt/sis-sa65-20261118`, no dataset/competition sources, internet off).
  * 65-square bank seed in `[0,L]²` embedded as zlib+base64;
  * targets `[8.535533905932745, 8.5350, 8.5340, 8.5330, 8.5320, 8.5300,
    8.5280, 8.5250, 8.5200]`, 2 bank + 1 bank-jitter + 1 random-construction
    seed per target, 420 s each, 4 workers;
  * structure-aware `gen_seed` (45° core blocks 5×5/4×4/5×6/4×6/6×6/6×6-corner
    + split-grid axis fill, uv jitter shrinking to 0): produces valid
    65-square seeds for L ≥ 8.5455 (22/25 trials), fails at L = 8.5355 only
    because the strict 1e-8 clearance rejects the tangent cells — itself a
    confirmation of the tangency bound;
  * smoke-tested locally: `E = 0.0` at L = 8.5355339, E = 5.2e-5 at 8.5300
    (5 s), E = 4.2e-4 (jitter seed) at 8.5200.
  **Not pushed** (per stand-down); the account's 5-session CPU cap was never
  consumed by this track.
* `/tmp/campaign2/master65/core.py` — exact anchor + SAT counter + family sweep.
* `search45.py`, `sweep45.py`, `longsa.py`, `smallcore.py` — exact bitmask
  core search (the machinery that produced the k≤8 exhaustion and ρ=0 results).
* `voidpack.py`, `void.py` — the decoupled void-packing formulation.
* `build_sa65.py`, `patch_gen*.py`, `seed65.b64` — kernel build artefacts.

## 5. Recommendation

Do not spend further budget on n=65. The 12-puzzle lever is closed by an exact
algebraic bound (`5 + 2.5√2`), not by search luck: the bank's layout is the
unique attaining configuration, the count function has a 16-square cliff just
below it, and every relaxing dimension (core size, angle, arm split, void
pattern, per-row phase — rows are flush so they have no phase freedom) makes
the count strictly worse. A win would require a 65-square packing in a
*different* architecture, which no track (this one, the multi-angle GA, the
C++ engine's n=65 exclusion) has found; the remaining slots are better spent
on the top-16 set and the band search as you directed.
