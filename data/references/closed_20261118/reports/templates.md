# Grid + bands track — closed-form template constructors + rigid-body polish

**Track:** constructive-template researcher (grid + bands family)
**Date:** 2026-11-18
**Baseline moved three times during this session** (frontier merges, all verified against
`/tmp/best_bank/report.json`, whose score field agrees with the CSV to 2.6e-14):

| time | SHA-256 (first 16) | score |
|---|---|---|
| session start (brief) | `6f6e9da8e3c79591` | 22.129502357094957 |
| 01:18Z merge | `9bdbce2bc63adc7f` | 22.129495171822438 |
| ~02:05Z merge (**live**) | `19877e21aeb72822` | **22.129481982260582** |

The one improvement this track produced (n=683) was certified against `9bdbce2b`, and the
~02:05Z merge has since absorbed it: the live bank now carries `L(683) = 26.636652007054913`,
exactly this track's value. Re-merging the candidate against the live bank gives
`changed_puzzles=[751]`, `net_gain = 6.7e-16` (a tie), score unchanged. **This track has no
outstanding win against the live bank.**

## Verdict, in numbers

| item | number |
|---|---|
| closed-form families implemented | **5** (exact, closed-form `L`) |
| parameter settings swept | **30 089** (ELL 3919, DIAG 637, CROSS 30, EDGE 2437, FLOOR 23 066) |
| n covered by the best-of-all exact construction | **999** (1000 with deletion closure) |
| puzzles where an exact construction beats the live bank | **0** |
| puzzles where an exact construction **ties** the bank's `L` to < 1e-9 | **509** |
| median `dscore` by which the bank beats the best exact construction | **+2.4e-3** |
| rigid-body squeeze at `s0 − 1e-6` (top target n=328) | **infeasible** (max violation 5.0e-7) |
| win produced and certified (vs bank `9bdbce2b`) | **n=683**, dL = 5.694e-5, dscore = **2.179e-6** |
| that candidate's score (text / float64) | **22.12949299320815 / 22.129492993208153** |
| that candidate's validity | **1000/1000 on both routes** |
| win still outstanding vs the live bank | **0** (absorbed by the ~02:05Z merge) |

**The closed-form template space is exhausted: the live bank already equals or beats every
exact `grid + band` construction on all 1000 puzzles.** This independently reproduces the parallel
track's finding (47/82 ties, 35/82 bank-better) on a wider family set, and it is *proved*
below for the whole `corner-staircases + rotated block` grammar, not just observed.

The one certified win (n=683, now absorbed) does **not** come from a new template: it comes
from the kit's fault-line DP fed with the refreshed starter-kit donors. With the kit donors
alone (control run) the DP finds exactly the same two improvements, so my 657 exact donor
layouts added **zero** gadgets. This is stated plainly because it changes what the result
means: the win was a donor-refresh artefact, and the durable output of this track is the
negative bound in §3.

---

## 1. Families implemented (all exact, closed form)

`tpl.py` / `kernel/kernel.py`. All coordinates are closed forms; every construction is
validated with an exact SAT separation test before use, and emitted with 40+ significant
digits after a `1e-9` dilation (the metric's interval arithmetic cannot certify a zero-width
contact between rotated squares; a `1e-9` gap costs 3e-8 in `L`, i.e. 1e-9 of score).

### ELL — Ellsworth/Göbel 45° family (four corner staircases + `w×h` 45° block)
```
L = max( (TL+BR+2)/2 + w/√2 , (TR+BL+2)/2 + h/√2 )
n = TL(TL+1)/2 + TR(TR+1)/2 + BR(BR+1)/2 + BL(BL+1)/2 + w·h
```
Parameter grid: the complete published enumeration (`enum45.txt`, 718 verified shapes,
n ≤ 2117) plus the `add_L` extension (side +1, `2⌊L+1⌋−1` squares) iterated to n ≤ 1000.
Implemented twice: gobel's verified builder and an independent re-implementation
(`tpl.fam_ellsworth`) that agree to 1e-9 on all 421 covered n.

### DIAG — two diagonal triangles of a `P×P` lattice + a row of `m` 45° diamonds
Two complementary staircases (`i−j ≥ 1`, `j−i ≥ 1`, i.e. the `P−2` interior diagonal cells
are removed) shifted by `(0,t)` and `(t,0)`, `t = 1/√2`, with a row of `m` 45° diamonds in the
resulting corridor:
```
n = P² − (P−2) + m        L = P + 1/√2        m ≤ 1 + √2(P−2)
⟹ D = n − K² ≤ (√2−1)K + 3 − 2√2 = 0.414214·K + 0.1716
```
Parameter grid: `P = 2..39`, `m = 1..m_max(P)` (637 n covered). This family reproduces the
bank's values **exactly** on n = 262, 449, 447, 788 … and is the exact closed form of the
"45° diagonal band" layouts (e.g. the bank's n=262 layout is this construction bit-for-bit).

### CROSS — `K×K` grid with a cross gap `g` (vertical) / `h` (horizontal) + one 45° diamond
The diamond's four tangent lines force `g + h = √2`, and the box is `(K+g)×(K+h)`:
```
n = K² + 1        L = K + max(g,h) ≥ K + 1/√2   (equality iff g = h = 1/√2)
```
Parameter grid: `K = 2..32`, `(g,h)` on the constraint line. This is the generalised n=5
construction (`2+1/√2`); it can never do better than `K + 1/√2`.

### EDGE — brief family 1: fault-line stack with a horizontal tilted band
`s` upright rows (split below/above the band) of `k = ⌊L⌋` squares, plus a band of `m` squares
at angle `θ` spanning the full width. The two side equations give
```
q = s/(m−1),   cosθ − sinθ = q,   θ = arccos(q/√2) − π/4
L = m·cosθ + sinθ = [ (m+1)·√(2−q²) + s ] / 2
n = ⌊L⌋·s + m
```
Parameter grid: `m = 2..499`, `s = 1..m−1` (965 n). Median `dscore` deficit vs the bank:
**+0.630** — the wasted `L−K` strip on the right of each block makes this family structurally
much worse than the fault-DP compositions.

### FLOOR — brief family 2: axis `a×b` grid + a band of `m` 45° diamonds on its top edge
```
L = max( a, (m+1)/√2, b + (m+1)/√2 ),      n = a·b + m
```
Parameter grid: `m = 1..199`, `a,b = 1..33` (882 n). Median deficit **+0.137**.

Sweep driver: `sweep.py` → `sweep_result.json` (each family is also swept with **deletion
closure**: a packing of `n'` squares at `L` is a packing of every `n ≤ n'` at the same `L`).

---

## 2. Sweep result (against the live bank)

| family | n covered | wins | gain | median `(L_bank − L_family)/√n` |
|---|---:|---:|---:|---:|
| ELL (45° staircase+block, all 718 shapes + extensions) | 421 | **0** | 0 | −0.00125 |
| DIAG (two triangles + 45° row) | 637 | **0** | 0 | −0.02632 |
| CROSS (cross gap + 1 diamond) | 30 | **0** | 0 | −0.00869 |
| EDGE (full-width tilted band) | 965 | **0** | 0 | −0.63035 |
| FLOOR (band on an edge) | 882 | **0** | 0 | −0.13740 |
| **best of all** | **999** | **0** | **0** | −0.00238 |
| best of all + deletion closure | **1000** | **0** | **0** | 0 for 509 puzzles, > 0 for the rest |

Closest puzzles (`L_bank − L_exact`, the best 8 after excluding n=1):

| n | family | L_bank | L_exact | dL |
|---:|---|---:|---:|---:|
| 994 | DIAG | 31.940885 | 32.707107 | −0.766 |
| 866 | EDGE | 29.878974 | 30.000000 | −0.121 |
| 990 | EDGE | 31.894887 | 32.015617 | −0.121 |
| 809 | EDGE | 28.889722 | 29.000000 | −0.110 |
| 597 | EDGE | 24.894065 | 25.000000 | −0.106 |

(the 509 exact ties are the family-DIAG puzzles: 262, 449, 447, 788, … where the bank *is* the
closed-form construction.)

---

## 3. Why there is no slack (the useful part)

These four statements together close the family. All are elementary; the numbers are
reproduced in `sweep.py` / `polish*.py`.

**(T1) A rotated block resting on lattice staircases is optimal at 45°.**
For a `w×h` block whose sides are along `θ` and `θ+90°`, resting on the four 45° staircase
lines of the Ellsworth construction, the side length is
```
L(ψ) = max( A/2 + (w cosψ + h sinψ)/√2 ,  B/2 + (w sinψ + h cosψ)/√2 ),   ψ = θ − 45°
A = TL+BR+2,  B = TR+BL+2.
```
Both arguments increase on `[0°, arctan(min/max)]` and both are symmetric about `ψ = 45°`
(the axis-aligned block), so the only stationary candidates are `ψ = 0` (45° block) and
`ψ = 45°` (axis-aligned). `ψ = 45°` was built explicitly and SAT-checked over 25 340
parameter sets that would have beaten the bank: **0 valid winning layouts**. `ψ = 0` is the
Ellsworth enumeration: **0 wins**. Free angles therefore add nothing.

**(T2) The perpendicular-shift trick has a hard floor of `1/√2`.**
Two lattice continents shifted by `t·(q,p)/√(p²+q²)` open a corridor of perpendicular width
`t` at a cost `L = P + t·max(p,q)/√(p²+q²)`. Since `max(p,q)/√(p²+q²) ≥ 1/√2` with equality
iff `p = q`, the cheapest corridor is the 45° one — i.e. family DIAG is the optimum of the
whole "two lattice blocks + one shifted band" topology.

**(T3) Corridor capacity caps the level `f = 0.7071` at `D ≤ 0.414K`.**
A unit square has perpendicular extent `|cos δ| + |sin δ| ≥ 1` in every direction, so a
corridor must be ≥ 1 wide; at 45° that costs exactly `1/√2` of `L`. The 1-wide corridor is
`√2 P` long, so it holds `m ≤ 1+√2(P−2)` diamonds, and the diagonal cull removes `P−2` cells.
Hence `n ≤ P² + 0.414P` at `L = P + 1/√2`. For `D > 0.414K` the next available level is
`f = 1.414` (a 2-wide corridor), which is worse than the trivial grid.

**(T4) The cross-gap threshold is `g+h ≥ √2`.**
A diamond in a `g×h` hole must be tangent to all four hole corners; its four tangent lines
`x±y = const` then give `(g+h)²/2 = 1` (unit area), so `g+h = √2` and
`L ≥ K + max(g,h) ≥ K + 1/√2`.

**Consequence.** Closed forms reach `f = 0.7071` only for `D ≤ 0.414K`, and never below
`0.7071`. The live bank's frontier, measured in `D/K` bins, is

| `D/K` | 0.0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0 | 1.1 | 1.2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bank `f` median | .521 | .536 | .601 | .657 | .707 | .756 | .795 | .827 | .870 | .906 | .943 | .981 | 1.000 |
| record `f` median | .511 | .536 | .594 | .657 | .705 | .751 | .786 | .824 | .870 | .900 | .941 | .977 | 1.000 |

which is `f ≈ 0.50 + 0.40·D/K`: **strictly below 0.7071 for every `D/K < 0.52`**, and for
`D/K > 0.52` no closed form exists at all. That is exactly why the sweep returns 0 wins on
all 1000 puzzles, and it is the quantitative reason the 79.3 % "grid+bands" gap cannot be
taken by templates.

---

## 4. Rigid-body polish (the redirected stage): implemented, and jammed

`polish.py` implements exactly the prescribed method: detect rigid bodies (axis-connected
clusters with translation only; angle-clustered tilted blocks with translation + one common
angle delta), then either
* (`squeeze`) fix the side at a target `s*` and minimise `max(box violation, inter-body
  overlap)`, or
* (`make_fun`) minimise `s = max(bbox)` with a squared-overlap penalty.
`polish_max.py` is the Chebyshev feasibility probe used below.

**Sanity check passes**: at the bank's own side (`s* = s₀ = 18.614368938` for n=328, 12
bodies, 31 free parameters) the sieve returns a feasible configuration at 3.6e-15 —
so the machinery is correct.

**Result (n=328, the largest single gap in the competition, 8.19e-4):** with `s* = s₀ − d`:

| `d` | max box violation | max inter-body overlap |
|---:|---:|---:|
| 1e-6 | 5.0e-7 | 4.9e-7 |
| 1e-5 | 5.0e-6 | 4.9e-6 |
| 1e-4 | 5.0e-5 | 4.7e-5 |
| 1e-3 | 5.0e-4 | 3.8e-4 |
| 4.4e-3 (= record side) | 3.2e-3 | 7.9e-3 |

The violation is *exactly* `d/2` at every scale: the layout is **exactly jammed**. There is no
rigid-body motion that removes even 1e-6 of side length — 100× below the project's existing
fixed-angle LP threshold. Coarse rigid bodies (31 parameters) and fine per-square freedom
(the earlier LP at 1e-6) agree, which is the expected signature of the hyperstatic contact
graphs reported in `/tmp/sub_diag/REPORT.md` (face contacts 1.02–1.49× isostatic).

Interpretation, stated carefully: this does not disprove the orchestrator's defect-angle
observation. It shows that **the record's defect angles are not reachable from our layouts by
rigid deformation**: our layouts sit at the bottom of *their own* basin (as the project's
`SQUISH` note says), and the record's 0.2–0.8° defects belong to a different arrangement
(different contacts), not to a continuous deformation of ours. Reaching them needs a
*re-composition* (new bodies/new contacts), which is the fault-DP/gadget lane.

---

## 5. Certified result (and its absorption)

**Win: n = 683**, certified against bank `9bdbce2b` = 22.129495171822438. Source: kit
fault-line DP (2-gadget chain, modes `[0,1]`) with the refreshed starter-kit donors;
`L 26.636708943546028 → 26.636652007054914` (dL = 5.694e-5, dscore = 2.179e-6).

| file | contents |
|---|---|
| `/tmp/campaign2/templates/candidate.csv` | 500500 rows, live bank with only the n=683 block replaced (text-level edit; float64 round-tripping the bank breaks 40 puzzles on 1e-16 contacts) |
| `/tmp/campaign2/templates/merge/merge_report.json` | merge gate: `changed_puzzles = [683, 751]`, `net_gain.text = net_gain.float64 = 2.178614286307834e-06`, `competition_submitted = false` |
| `/tmp/campaign2/templates/score/` | `squares score --mode both`: **text 22.12949299320815, float64 22.129492993208153, 1000/1000 valid, 0 invalid, 0 missing** |
| `/tmp/campaign2/templates/sweep_result.json` | per-family sweep, per-puzzle `L_exact` vs `L_bank` |

The merged submission is `/tmp/campaign2/templates/merge/submission.csv` (SHA-256
`ec33adff47aff4114c144ffa7916653427f468bc43de55d5493c71920a709be3`), identical in score to
the candidate.

n=751 is a 1.4e-14 tie against the live bank (it was a 4.5e-8 win against the 01:18 snapshot
the kernel started from); the merge gate accepts it as non-regressive. It adds nothing.

**Against the live bank** (`19877e21` = 22.129481982260582) the same candidate now yields
`changed_puzzles=[751]`, `net_gain.text = net_gain.float64 = 6.66e-16`, score unchanged at
22.129481982260582 (`/tmp/campaign2/templates/merge_live/`): both wins were absorbed by the
~02:05Z frontier merge. **Reported as found — there is no outstanding win from this track.**

## 6. Kernel

* ref: **`ccjjllt/sis-closed-form-grid-band-templates-20261118`** (CPU, `enable_gpu: false`,
  COMPLETE, 2248 s, 1356 donors, 3 DP passes + a kit-only control pass).
* code: `/tmp/campaign2/templates/kernel/kernel.py` + `kernel-metadata.json`.
* downloaded output: `/tmp/campaign2/templates/kout2/` — `run_report.json` (137 kB, includes
  the per-puzzle `L_exact` table), `improved_groups.csv` (1434 rows = the two wins),
  `dp_control.log`, `dp_exact{1,2,3}.log`, and the kernel log.
* control attribution: `control_dp_wins = [683, 751]` — identical to the treatment run, so the
  657 exact donor layouts contributed **no** gadget. Reported as found.

## 7. What this means for the campaign

1. **Templates are not the missing 79.3 %.** The live bank equals or beats the *entire* closed-form
   `grid + band` grammar (45° staircase+block, two-triangle diagonal row, cross gap,
   full-width tilted band, edge band) on all 1000 puzzles; 509 of those are exact ties. Any
   further template work is negative-expected-value.
2. **The remaining slack is composition, not geometry.** The bank's frontier `f ≈ 0.50+0.40·D/K`
   is set by the fault-line DP's gadget inventory. The only lever seen in this track is a
   better gadget for a binding key (the kit-donor refresh alone produced the 683 win), which is
   the gadget track's lane.
3. **Publishing the negative bound is worth more than another sweep**: `f ≥ 1/√2` for any
   single-corridor band, `D ≤ 0.414K` at that level, and `L ≥ K + max(g,h)` for cross gaps
   tell the next agent immediately which constructions cannot pay.
4. The rigid-body polish is safe to keep as a *gate* (it certifies jammedness at 1e-6 in
   seconds per puzzle) but it cannot create slack; do not spend kernel hours on it.

## 8. Reproduce

```sh
cd /Users/zhaohuaxiang/ccjjllt/squares
.venv/bin/python /tmp/campaign2/templates/sweep.py --json /tmp/campaign2/templates/sweep_result.json
.venv/bin/python /tmp/campaign2/templates/polish_max.py 328 18.614367938490983 18.614368938490983
.venv/bin/python /tmp/campaign2/templates/build_candidate.py /tmp/campaign2/templates/ktest/fault_exact 683
.venv/bin/python -m squares merge --baseline /tmp/best_bank/submission.csv \
  --baseline-report /tmp/best_bank/report.json \
  --candidate /tmp/campaign2/templates/candidate.csv --output-dir /tmp/campaign2/templates/merge
.venv/bin/python -m squares score /tmp/campaign2/templates/merge/submission.csv --mode both \
  --output-dir /tmp/campaign2/templates/score
```
