# CDB / 45-degree central-block track — constructive result

**Verdict: the family is closed. Zero constructions inside it beat the live bank.**
Enumerated exhaustively and certified exactly: the bank's `L` equals the exact family optimum on
**47 of the 82** CDB puzzles (including every puzzle with gap_score ≥ 45 except 263/448/330),
the bank is *strictly better* than the family on the other **35**, and the family is better on
**none**. No puzzle is won, so no `candidate.csv` is emitted (the mission requires it to be
strictly below the bank on both routes; there is nothing to merge).

Baseline used, re-read from the live file at the end of the work:

| | |
|---|---|
| `/tmp/best_bank/submission.csv` | sha256 `9bdbce2bc63adc7f4cdc68860ae6bc797e0ecd6acf880a626b5a44b21dd5908e` |
| certified total (text = float64) | **22.129495171822438** |
| CDB total gap bank → record snapshot (82 puzzles) | **0.0100427** |
| reachable by construction in this family | **0.0000000** (0 puzzles) |
| residual, therefore a *continuous* (non-integer-parameter) effect | **0.0100427** |

The bank moved twice while this track ran (`22.1296844937` → `22.1295023571` → `22.1294951718`);
the CDB puzzles' `L` values were **identical** in all three snapshots (902 = 30.535533905933,
842 = 29.520815280171, 626 = 25.520815280171, …). The sweep was executed on the
`6f6e9da8…` snapshot and re-checked against the final `9bdbce2b…` snapshot: 0 wins both times.

The one thing this track does deliver is a proof-grade negative: **the 45°-central-block gap is not
a template-search gap**. Further compute on 45° diamond templates is wasted.

---

## 1. The family, exactly

One `w × h` block of unit squares turned 45°, plus four corner staircases with `TL, TR, BR, BL`
rows of upright cells (`T(t) = t(t+1)/2` cells each), plus **corner sharing** (two adjacent
staircases share the last cell on their common side: one square fewer, that adjacency relaxed by 1).

With `d1 = (x − y + s)/√2` (distance from the TL/BL side) and `d2 = (x + y)/√2`, the block occupies
`d1 ∈ [(TL+1)/√2, (TL+1)/√2 + w]` and `d2 ∈ [(BL+1)/√2, (BL+1)/√2 + h]`; a staircase with `t` rows
is contained in the L1 triangle of radius `t+1` around its box corner, so the block is separated
from it by the corresponding 45° line. Hence

```
side   s = max( (TL+BR+2)/2 + w/√2 ,          # block spans d1 between the TL and BR staircases
                (TR+BL+2)/2 + h/√2 ,          # block spans d2 between the TR and BL staircases
                (w+h)/√2 ,                    # block bounding box
                TL+TR, TR+BR, BR+BL, BL+TL ,  # adjacent staircases must not collide (-1 if shared)
                TL+1, TR+1, BR+1, BL+1 ,      # staircase inside the box
                (TL+BL+2+√2(w+h))/3 ,         # block corner at x ≥ 0
                TL−BL+w√2, BL−TL+h√2 )        # block corner at y ≥ 0
count  n = w·h + T(TL)+T(TR)+T(BR)+T(BL) − #shared
valid  ⟺ s ≤ TL+BL+2  and  s ≤ TR+BR+2     (block's near corner inside the box)
```

**Validation (exact).** All 718 shapes with coordinates in the starter kit's published enumerator
output (`enum45.txt`, Ellsworth's `enum-45deg-rect-packings`) were re-derived from these formulas:

```
mismatches: 0 / 718      (count exact on every shape; side agrees to < 1e-6 on every shape)
```

Coordinate emitter: `kernel/cdb_family.py::build()`, mpmath at 60 digits; the whole layout is
dilated by `1e-13` about its centre so exact irrational contacts survive the float64 round trip.
`measure(build(...)) − s ≈ 2e-12`.

Anchors reproduced exactly: `s(5) = 2 + 1/√2`, `s(10) = 3.70710678`,
`s(626) = 13.5 + 17/√2 = 25.520815280171306`.

## 2. Sweep — exhaustive for n ≤ 1000

```
TL,TR,BR,BL ≤ 32          any family layout with n ≤ 1000 has t+1 ≤ s ≤ 32
1 ≤ w,h ≤ 48, w·h ≤ 1000  and w+h ≤ √2·33
sharing: none, and TR+BR  (the other three sides are reflected relabellings of the same tuples)
closures: deletion  L(n) = min_{n' ≥ n} s(n')   and  L-border extension
          n → n + 2⌊s+1⌋ − 1 at side s+1, repeated
```

3 643 579 valid `(shape, side, count)` triples after the box-validity filter. 17 s locally,
130 s on the Kaggle CPU kernel. Output `family_frontier.csv` (n, L_family, L_bank, delta).

Family-only score if the family were used alone for all 1000 puzzles: **26.855430666950** — the
family covers only part of the field and the bank dominates it everywhere.

**The two structural identities that close this track.** The bank's whole `n = k²+1` column
(626, 677, 730, 785, 842, 901, 962, all at f = 0.520815280171) is exactly the L-border chain of the
single shape `(w,h)=(17,17)`, staircases `(12,13,13,12)`, TR+BR shared:

```
s = 13.5 + 17/√2 = 25.520815280171      n = 289 + 78+91+91+78 − 1 = 626
626 → 677 → 730 → 785 → 842 → 901 → 962   (+1 side and +2⌊s⌋−1 squares per step)
```

and the bank's `n = k²+2` column (902, 963) is exactly `(w,h)=(5,36)`, staircases `(26,4,26,4)`:
`s = 27 + 5/√2 = 30.535533905933`, `n = 180 + 702 + 20 = 902`.

## 3. Per-puzzle table (top 20 CDB by gap_score)

`L_family` is the certified exact family optimum after both closures. Nothing here is bankable.

| n | L_bank = L_family (live) | L_record | L_family−L_bank | L_record−L_bank | Δscore if record reached |
|---|---|---|---|---|---|
| 902 | 30.535533905933 | 30.514078774139 | −2.1e-13 | −0.021455 | 7.144e-04 |
| 963 | 31.535533905933 | 31.514078774129 | −2.5e-13 | −0.021455 | 6.914e-04 |
| 842 | 29.520815280171 | 29.502152707903 | −1.4e-13 | −0.018663 | 6.432e-04 |
| 901 | 30.520815280171 | 30.502152707908 | −1.5e-13 | −0.018663 | 6.217e-04 |
| 962 | 31.520815280171 | 31.502152707911 | −1.7e-13 | −0.018663 | 6.017e-04 |
| 843 | 29.535533905933 | 29.518244283132 | −1.9e-13 | −0.017290 | 5.955e-04 |
| 263 | 16.733166007899 | 16.724372709143 | family **16.778174593052** (+4.5e-02) | −0.008793 | 5.422e-04 |
| 448 | 21.687501911902 | 21.681077732282 | family **21.692388155425** (+4.9e-03) | −0.006424 | 3.035e-04 |
| 785 | 28.520815280171 | 28.505934753290 | −1.6e-13 | −0.014881 | 5.311e-04 |
| 786 | 28.535533905933 | 28.521591626147 | −1.8e-13 | −0.013942 | 4.973e-04 |
| 330 | 18.687652890045 | 18.683795337473 | family **18.707106781187** (+1.9e-02) | −0.003858 | 2.124e-04 |
| 730 | 27.520815280171 | 27.509315397951 | −1.9e-13 | −0.011500 | 4.256e-04 |
| 964 | 31.535533905933 | 31.522821522787 | family **31.556349186104** (+2.1e-02) | −0.012712 | 4.094e-04 |
| 677 | 26.520815280171 | 26.510279061851 | −1.7e-13 | −0.010536 | 4.049e-04 |
| 626 | 25.520815280171 | 25.511048764219 | −1.2e-13 | −0.009767 | 3.903e-04 |
| 295 | 17.704232790736 | 17.698042929394 | family **17.707106781187** (+2.9e-03) | −0.006190 | 3.604e-04 |
| 537 | 23.692388155425 | 23.684143606359 | family **23.707106781187** (+1.5e-02) | −0.008245 | 3.558e-04 |
| 451 | 21.756097560976 | 21.750123248970 | family **21.763455967291** (+7.4e-03) | −0.005974 | 2.813e-04 |
| 636 | 25.727922061358 | 25.721006714198 | −1.4e-13 | −0.006915 | 2.742e-04 |
| 494 | 22.736096174508 | 22.730791153395 | family **22.742640687119** (+6.5e-03) | −0.005305 | 2.387e-04 |

Full 82-row table: `kernel_out/cdb_table.csv`. 47/82 CDB rows have `L_family − L_bank` between
−2.5e-13 and 0 (the bank *is* the family optimum); the other 35 are rows where the bank is better
and the family value is shown in bold.

Bold rows are the important negative evidence: those 35 puzzles are CDB by the classifier's
geometry signature but their bank layout is *not* in this family (263's 9×9 diamond + 184 upright
cells, 964, 903, 844, 537, 451, 494, 409, 332, 578, 536, 297, 787, 732, 679 …), so the classifier's
"CDB" label over-counts the family by 43 %.

## 4. Why the residual cannot be constructed (the useful part)

1. **Waste identity.** A family layout's unfillable area is exactly the four staircase slivers,
   `waste = Σ(tᵢ+1)/2`, measured 25.31 at `s = 25.52` (`w+h = 34`) and 30.35 at `s = 29.54`
   (`w+h = 41`) — i.e. `0.744` and `0.740` per unit of `w+h`, against the `1/√2 = 0.707` floor for
   a straight 45° edge. A rasterisation of the free space (`pockets.py`) confirms: four slivers of
   thickness ≈ `1/(2√2)`, no pocket admits a unit cell. So this is the floor of the whole class,
   not a bad choice of parameters.
2. **The core shape is already optimal.** Any 45°-rotated polyomino core (herringbone, two diamonds
   at ±45°, chain of blocks, core + upright band) pays the same L1-boundary cost per unit of
   perimeter, and for fixed area the rectangle minimises the perimeter. Numerically confirmed: the
   bank's own `n = 902` is a **three-diamond chain** (3 × 5×5, 74 cells at 45°) and its `L` equals
   the single `5×36` block's `L` to 2e-13. Splitting the core never helps.
3. **The record values are not of this algebra.** `f = L − k` for the D=1 column is
   `0.50215270790331 / …907698 / …910792` at k = 29/30/31 — constant to 7e-12 (same gadget re-used),
   but not of the form `(P+2)/2 + w/√2` for any integers (`(P+2)/2 = f + b/√2` is non-integral for
   every `b ≤ 24`), not a low-degree algebraic number (PSLQ on `[1,f,f²,f³,f⁴]` yields only
   spurious relations, |coeff| ~ 10³, with no real root near `f`), and not reachable by any family
   shape with `w,h ≤ 48`. Its 842 wastes **28.377** area units against the exact family's
   **30.348** — 1.97 units shaved off four slivers. That is a continuous deformation of the same
   contact topology, not an integer construction.
4. **Consequence.** The 0.0100427 CDB residual needs either a topology-preserving *global* search
   (the record holder's own method: the record layouts carry defect angles at 44.79°–45.33° and
   0.0002°–0.55°, i.e. numerically polished positions) or an exact solve of the tangency system with
   non-integer sliver offsets. Local search is dead here (already known); integer-parameter
   construction is now also dead here (this report).

## 5. Artifacts

| path | content |
|---|---|
| `/tmp/campaign2/cdb/kernel/cdb_family.py` | exact family: `side()`, `count()`, `build()` (50-digit coordinates), `measure()` |
| `/tmp/campaign2/cdb/kernel/kernel.py` | exhaustive sweep + closures + exact emitters + official-metric certification |
| `/tmp/campaign2/cdb/kernel/kernel-metadata.json` | CPU kernel metadata (`enable_gpu: false`) |
| `/tmp/campaign2/cdb/famL2.npy`, `famN.npy`, `famS.npy` | sweep frontier (n → exact side) |
| `/tmp/campaign2/cdb/validate2.py` | 718-shape validation of the formulas (0 mismatches) |
| `/tmp/campaign2/cdb/pockets.py` | free-space rasteriser (sliver widths, fillability) |
| `/tmp/campaign2/cdb/kernel_out/` | downloaded Kaggle kernel output (below) |
| `/tmp/campaign2/cdb/donor_check/` | end-to-end dual-route certification of the emitters (below) |

### Kaggle kernel (CPU, `enable_gpu: false`)

* ref: `ccjjllt/sis-cdb-45deg-family-sweep-20261118` — status **COMPLETE**, elapsed 130 s
* ran on `/kaggle/input/datasets/ccjjllt/sis-bank-20261117/submission.csv`
  sha256 `6f6e9da8e3c795914d89f1e79d777233e256cce4a5600ab32d0e70e8f55e0c40`
  (bank at push time, total `22.129502357094935`); re-checked against the final live
  `9bdbce2b…` / `22.129495171822438`: identical CDB `L` values, still 0 wins
* kernel verdict: `wins: 0`, `equal_to_bank: 420`, `family_frontier_total: 26.85543066694967`
* outputs: `run_report.json`, `family_frontier.csv`, `cdb_table.csv`,
  `family_donor_layouts.csv` (exact 50-digit layouts, certified with the unmodified official
  metric: n = 902, 626, 636, 627, 489, 584, 688, 368, 406), `improved_groups.csv` (header only),
  `sis-cdb-45deg-family-sweep-20261118.log`

### End-to-end emitter certification (dual route)

The 9 certified donor layouts were dropped into the live bank and scored with
`python -m squares score --mode both`:

```
text    22.129495171823269   1000/1000 valid, 0 invalid, 0 missing
float64 22.129495171823269   1000/1000 valid, 0 invalid, 0 missing
bank    22.129495171822438   (difference +8.3e-13 = the deliberate 1e-13 dilation on 9 puzzles)
```

So the exact closed-form emitter is certified on both routes and reproduces the bank's CDB layouts
to within the dilation it needs to be certifiable — and beats nothing.

## 6. Recommendation to the orchestrator

* Stop 45° diamond / central-block *template* work. 47/82 CDB puzzles are already at the exact
  family optimum and the other 35 use constructions outside the family that the bank already has.
  The whole 82-puzzle gap is a continuous polish gap.
* The 0.0100427 CDB residual is the second-largest family after grid+bands and is worth ~0.010 of
  score, but the only route is a topology-preserving global search seeded with the exact family
  layouts (free parameters: the four sliver offsets + block position/angle), i.e. what the record
  holder evidently did. Budget it as a search track, not a construction track.
* The classifier's `family_guess == CDB` over-counts this family by 43 %; 35 of the 82 "CDB" puzzles
  are not 45°-central-block constructions at all.
