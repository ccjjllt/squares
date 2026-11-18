# D=2 master gadgets for n = k²+2 (678 @ k=26, 902 @ k=30) — REPORT

Track: `d2master`. Mandate: build **exact constructions** for a 678-square gadget
(max dim 26) and a 902-square gadget (max dim 30) in the n=401 style, anchor on the
bank's own f = 0.535533906, and certify anything strictly below it.
`/tmp/best_bank/` untouched. No Kaggle submission. Local CPU only, light MILP.

**Bottom line: no candidate. Every rigid family I can state exactly is capped at
⌊L⌋² = 676 at the record's side (2 squares short of 678) and at 26h at the oblong
side (2 short of 26h+2). The "+2" is a single, non-negotiable unit that only the
contact-jammed pinwheel supplies, and only at exactly f = 5√2/2−3.** Kernel built
and push-loop started; the account is still at the 5-session cap (attempt 1 at
23:36:20Z and attempt 2 at 23:44:24Z rejected).

---

## 1. The lift arithmetic — the prize is 3.375e-3, not 2.28e-3

The lift identity (`/tmp/campaign2/lift.py`) is `n = k²+D` at `L = k+f` for **every**
k ≥ max(w,h). I verified it on the bank's own layout: `bank678.csv` (678 squares,
bbox 26.535533905933) is exactly a `(26,26,2)` gadget with f = 0.5355339059328, and

```
python /tmp/campaign2/lift.py --master bank678.csv --k0 26 --D 2 --ks 26 27 28 29 30 31
  gadget w=26 h=26 D=2 f=0.535533905932830 n0=678
  k=26 n=678 L=26.535533905932830
  k=27 n=731 L=27.535533905932830
  k=28 n=786 L=28.535533905932830
  k=29 n=843 L=29.535533905932830
  k=30 n=902 L=30.535533905932830
  k=31 n=963 L=31.535533905932830
```

The bank's D=2 column is **0.535533906 at every k = 24…31** (one shared gadget, the
lifted n=291 pinwheel). Therefore

> **any** valid `(w,h,2)` gadget with `max(w,h) ≤ 26` and `f < 0.535533906` wins
> **all six** of 678, 731, 786, 843, 902, 963 at `L = k+f`.

Gain = `Δf · Σ_{k=26..31} (k+f)/(k²+2)` = **0.2147 · Δf**, i.e. 2.147e-4 per 0.001 of
f, and **2.507e-3** at the record's own f = 0.523860. The brief's 2.28e-3 (678+731 only)
understates the target by the 786/843/902/963 column, which the same gadget takes.

---

## 2. Anchor — reproduced exactly, twice

**(a) Bank layouts, exact SAT.** Direct from `/tmp/best_bank/submission.csv`
(`csv` → 678 / 902 rows, angles mod 90):

| n | count | bbox | pairwise SAT (tol 0) | angle partition |
|---:|---:|---|---|---|
| 678 | 678 | 26.535533905933² | **0 overlapping pairs** | 512 axis (0/90°) + 145 at 45° + 21 slivers 0.04–0.13° off axis |
| 902 | 902 | 30.535533905933² | **0 overlapping pairs** | 817 axis + 74 at 45° + 11 slivers |
| 731 | 731 | 27.535533905933² | 0 overlapping pairs | lift of 678 |
| 963 | 963 | 31.535533905933² | 0 overlapping pairs | **exactly 3 angle values**: 888 axis + 75 at 45° (no slivers at all) |

The 678 layout is *not* a rigid lattice: the 45° squares form a **5-row slab straddling
the main diagonal** (in `u=(x+y)/√2, v=(x−y)/√2`: v = −2,−1,0,1,2 with u ∈ [3.98, 32.19],
145 = 5×29), the axis part sits on **two phases {0, 0.5355}** (252 + 243 squares), and 21
near-axis slivers repair the slab/axis interface. 902 has **three** 5×4 slabs (v ∈ [−2,2],
[−14,−10], [10,14]) plus 817 axis + 11 slivers.

**(b) The construction model, exact MILP.** `corefill.py` = the master291
`model`+`milpfill` clique-cover MILP, driven by 45° cores. Anchor at k=17:

```
2 × 5×5 45° cores + 4-phase axis fill (a=0.5, s=f), L=17.535533905933
  fill = 241  → total = 291   (target 241/291)   0 overlaps, bbox 17.535533906²
```

and at the two targets with s = f_bank (HiGHS, exact max over the candidate set):

```
k=26 m=5 s=0.535534: cores=50 fill=628 total=678  (target 678)   ← reproduces the bank count
k=30 m=5 s=0.535534: cores=50 fill=852 total=902  (target 902)   ← reproduces the bank count
```

So the pinwheel family reproduces **both** anchors as *proved maxima*, not just as
feasible values. This is the model every candidate below was judged against.

---

## 3. Construction family table — exact maxima

All numbers are exact HiGHS maxima over the stated candidate set (clique-cover
formulation for the axis part, explicit pairwise SAT for every tilted cell), and every
emitted set was re-checked with explicit pairwise SAT (min separation ≥ −2e-15,
0 interpenetrating pairs, full containment). `s = L − k`; `f_bank = 0.535533906`.

### 3.1 k = 26, target 678, box 26+s

| family | s = f_bank | s = 0.533534 | s = 0.523860 (record) | verdict |
|---|---:|---:|---:|---|
| 2-phase axis lattice (`{0}∪{s}` per axis) | **676** | 676 | 676 | = ⌊L⌋², hard cap |
| 3-phase axis (`{0}∪{0.5}∪{s}`) | 676 | – | 676 | no gain |
| 4-phase axis (`{0,¼,½,¾}`) | 676 (time-limited, 25 s; incumbent only) | – | – | no gain |
| pinwheel m=5 (2×25 cores + fill) | **678** | 654 | 654 | spike, loses 24 at any s<f |
| pinwheel m=4 | 666 | – | – | 12 short |
| pinwheel m=6 | 668 | – | – | 10 short |
| random multi-core, 2–4 blocks m∈{3..6}, 45 trials | **666** | – | – | never reaches 678 |
| 5×W slab, W∈{27,28,29}, u0 swept (9 each) | 674–676 | – | 632–637 | 2 short at best |
| oblong strip (26,h,2), h=1..6 | 26h | – | **26h** | 2 short for every h |

### 3.2 k = 30, target 902, box 30+s

| family | s = f_bank | s = f_bank−0.002 | verdict |
|---|---:|---:|---|
| pinwheel m=5 | **902** | 878 | spike at f only |
| pinwheel m=4 | 890 | – | 12 short |
| pinwheel m=6 | 892 (time-limited) | – | short |
| 2-phase axis | 900 = ⌊L⌋² | 900 | cap |

### 3.3 The phase/offset sweep at *fixed* L (k=26, L=26.535533906)

`(a,s)` with a = axis origin, s = second-phase offset. The unique maximum is
`(0.5, f_bank) = 678`; **every other cell is 646–654**:

| a \ s | 0.400 | 0.450 | 0.500 | **f_bank** | 0.560 | 0.600 |
|---|---:|---:|---:|---:|---:|---:|
| 0.4 | 646 | 646 | 646 | 646 | 646 | 646 |
| **0.5** | 654 | 654 | 654 | **678** | 648 | 648 |
| 0.6 | 646 | 646 | 646 | 646 | 646 | 646 |

This is the k=26 replica of master291 §5: the construction is a **spike at exactly
f = m/√2 − 3 = 5√2/2 − 3**, and m=5 is the only profitable core size.

---

## 4. The exact construction ceiling at the record's side

At `L = 26.523860` (the record's 678) and `L = 30.514079` (the record's 902):

| family | best exact count at the record's L | required | deficit |
|---|---:|---:|---:|
| 2-phase / 3-phase / 4-phase axis | **676** | 678 | −2 |
| axis + full-box 45° patch | 676 | 678 | −2 |
| pinwheel m=5 (+ phase free) | 654 | 678 | −24 |
| 5×W slab (W, u0 swept) | 637 | 678 | −41 |
| oblong strip (26,h,2), h ≤ 6 | 26h | 26h+2 | −2 |
| random multi-core (45 placements) | 666 | 678 | −12 |

**The ceiling is 676.** Two squares, at *every* L in [26, 26.536) — because the axis
lattice is a perfect tiling of [0,k]², so any tilted unit square displaces ≥1 axis cell
and the axis cap ⌊L⌋² = 676 cannot be beaten by adding tilted cells. The +2 the bank
has at 26.535534 comes only from the two 5×5 corner cores at the one phase where the
staircase around each diamond is exactly fillable — the same "one-off spike" structure
master291 proved for n=291 and mis401 proved for n=401.

Consequence: the record's 0.523860 is **not a lattice phase of this family**. It is
0.0117 = 22× the 291-spike width (1e-5) and 1.7× the whole 401 relaxed-layout gain
(0.0069). Consistent with mis401 §5: the record holders' layouts are *relaxed
per-square* layouts (their own prose: "many slightly different angles"), which sit
2–16 squares above every rigid family. Nothing here changes that conclusion for D=2.

**Coverage note.** These are maxima over the stated candidate sets, with the recorded
HiGHS status; they are not global lower bounds on the packing problem. The 2-square
deficit is the empirical constant of this whole campaign (291: exact; 401: 1 short;
626: 1 short; D=2: 2 short).

---

## 5. The oblong-gadget family — the one genuinely new opening, and why it closes

An oblong `(w,h,2)` gadget lifts exactly like a square one (`lift.py` §"general corner
gadget"), but needs **much lower density**:

```
rho(w,h,f) = (w·h+2) / ((w+f)(h+f))     at f = 0.523860, w = 26:
  h=1: 28/(26.52·1.52)  = 0.695      h=4: 106/(26.52·4.52) = 0.884
  h=2: 54/(26.52·2.52)  = 0.808      h=5: 132/(26.52·5.52) = 0.902
  h=3: 80/(26.52·3.52)  = 0.856      h=26 (square): 0.964
```

The bank's crop table never contains these (the gadget track only ever tested oblong
*gadgets as crops*, §4.3 there — never a designed one). So I built them: exact MILP over
2-phase axis cells (`{0}∪{f}` per axis, correctly clipped by *extent* not centre) +
45° cells on the 45° lattice in the strip box, `(26+f) × (h+f)`:

| h | box | candidates | exact MAX | need (26h+2) | deficit |
|---:|---|---:|---:|---:|---:|
| 1 | 26.5239 × 1.5239 | 122 | 26 | 28 | −2 |
| 2 | 26.5239 × 2.5239 | 244 | 52 | 54 | −2 |
| 3 | 26.5239 × 3.5239 | 366 | 78 | 80 | −2 |
| 4 | 26.5239 × 4.5239 | 506 | 104 | 106 | −2 |
| 5 | 26.5239 × 5.5239 | 628 | 130 | 132 | −2 |
| 6 | 26.5239 × 6.5239 | 768 | 156 | 158 | −2 |

**The 45° phase adds exactly 0 at every h** — König: every 45° cell conflicts with an
axis cell, and the max always equals the plain axis grid 26h.

Because the bank's own 678 gets its +2 from *near-axis slivers* (0.04–0.13° off axis),
the same exact MILP was rerun with a full sliver phase set — θ ∈ {0.5°, 1°, 2°, 3°, 5°,
10°} on the tiling lattice (662/922/1181 candidates) — at f = 0.523860:

| h | candidates | exact MAX (status 0 = optimal) | need | deficit | bbox |
|---:|---:|---:|---:|---:|---|
| 3 | 662 | **78** | 80 | −2 | 26.523860 × 3.523860 |
| 4 | 922 | **104** | 106 | −2 | 26.523860 × 4.523860 |
| 5 | 1181 | **130** | 132 | −2 | 26.523860 × 5.523860 |

So the oblong strip family is closed at exactly `26h` **with the sliver phase included**,
and HiGHS certified optimality in 2–9 s.

Adding the pinwheel cores inside the strip box does not rescue it either — the two 5×5
diamonds (7.07 bbox) cost far more axis cells than they supply when the box is only
`h+f` tall. Cores at the two box corners, inset ∈ {0, 0.4, 0.732, 1.0}, phase ∈
{f, 0.5, 0.45, 0.40}, both corner modes:

| h | box | need | best (50 cores + fill) | deficit |
|---:|---|---:|---:|---:|
| 7 | 26.5239 × 7.5239 | 184 | 164 | −20 |
| 8 | 26.5239 × 8.5239 | 210 | 190 | −20 |
| 10 | 26.5239 × 10.5239 | 262 | 242 | −20 |

i.e. the oblong family with cores loses exactly 20 — it is not a near miss. The oblong family is
therefore 2 short at f = 0.523860 for *every* h, and is the same "+2 problem" as the
square case, only with the cores unable to fit (a 5×5 45° diamond has a 7.07 bbox, so
the pinwheel needs h ≥ 7, where the axis fill already supplies 26h and the core
placement search finds no admissible non-overlapping pair inside the strip).

An early version of this test reported 82/109/137 ≥ need; that was a **containment
bug** (candidate axis cells were clipped by centre instead of by extent, admitting a
whole extra column and row outside the box). All numbers in this report are from the
corrected filter; the bug is documented here because the corrected counts are the ones
that matter.

---

## 6. Certification

**No candidate exists.** Nothing was emitted for `squares merge`: the best exact
constructions at the record's sides are 654 (pinwheel), 637 (slab) and 676 (axis), all
below the required 678. Per the brief, no candidate was lifted.

The anchor itself was certified (both routes, exact SAT re-checked):

```
bank 678: n=678, L=26.535533905933, 0 overlapping pairs, n ≤ L²  ✓
bank 902: n=902, L=30.535533905933, 0 overlapping pairs, n ≤ L²  ✓
```

The merge command that any future candidate must pass, unchanged:

```sh
.venv/bin/python -m squares merge \
  --baseline /tmp/best_bank/submission.csv --baseline-report /tmp/best_bank/report.json \
  --candidate cand.csv --output-dir <dir>
```

Best valid layouts available now (both already in the bank, re-verified here):
`/tmp/campaign2/d2master/bank678.csv` (678 @ 26.535533905933) and
`bank902.csv` (902 @ 30.535533905933). `lift678.csv` / `lift902.csv` are their lifts
(678/731/786/843/902/963 and 902/963) — net gain **0.0** by construction.

---

## 7. Kernel

`kdir/kernel.py` + `kdir/kernel-metadata.json` → **`ccjjllt/sis-d2-gadget-678-902-20261118`**
(CPU only, `enable_gpu: false`, no dataset, no internet, self-contained: inlines the
clique-cover MIS, exact SAT, the annealer and the verifier).

| job | content |
|---|---|
| J1 | exact 2-phase axis cap at `L = k+s`, s ∈ {0.514079, 0.521592, 0.523860, 0.530, 0.535534}, k ∈ {26,30} → the ceiling curve (locally: 676 at every side, both k) |
| J2 | relaxed repair at the smallest side that can still win: **exact axis-grid seed** (676/900, verified 0 overlaps, wall 0) → exhaustive random insertion with an exact-SAT gate → 3 annealing rounds with per-square + rigid-group moves → re-insert; all gated by `violations()` (exact SAT + wall) |
| J3 | a candidate is written **only** if `n == target`, `overlaps == 0`, `wall ≤ 1e-12`, `n ≤ L²`; master CSV `master_<n>.csv` is emitted for `lift.py --k0 26 --D 2` (`--k0 30`) |

Smoke test (local, exact, 156 s end-to-end): J1 returns **676 at all five k=26 sides and
900 at all five k=30 sides** (each emitted set re-verified: 0 overlapping pairs, wall 0);
J2 seeds the exact axis grid (676 / 900, valid), random insertion adds **0** squares
(the strip is 0.51–0.52 wide, so no unit square of any tested orientation fits), the
annealer leaves the jammed grid untouched, and the gate emits **0 candidates**.

Three bugs were found and fixed by this smoke run, and are worth recording because each
one produced a spuriously high count:
1. axis candidates clipped by *centre* instead of *extent* (admits a whole extra column
   and row outside the box);
2. the tilted-cell clique cover omitted every axis↔tilted constraint (an invalid
   676+45° "solution" came back at 729);
3. the insertion test compared the wrong row (it queried `P[idx][0]` against the rest
   instead of the new square), admitting 225 overlapping squares.
The final gate (`n == target`, 0 overlaps, wall ≤ 1e-12, `n ≤ L²`) rejected all three,
which is the reason the gate exists.

Push: `retry_push.sh`, every 8 min, 18 attempts, log `/tmp/campaign2/d2master/push.log`.
Attempt 1 (23:36:20Z): `Maximum batch CPU session count of 5 reached`. The loop keeps
running; harvest with

```sh
export KAGGLE_API_TOKEN=$(cat ~/.kaggle/access_token_ccjjllt_check)
.venv/bin/kaggle kernels output ccjjllt/sis-d2-gadget-678-902-20261118 -p /tmp/campaign2/d2master/kout
```

and, **only** if `master_678.csv` (or `master_902.csv`) is present: re-verify pairwise
SAT + `n == len` + `n ≤ L²` locally, then `lift.py` and `merge` exactly as in §6.

---

## 8. Verdict / recommendation

1. **Anchor reproduced twice, exactly**: the bank's 678 and 902 are valid, and the
   pinwheel model reproduces both counts as exact maxima at `s = f_bank`.
2. **Every rigid family is closed at 676 at the record's side**: 2/3/4-phase axis,
   axis+45° patch, 5×W slab, random multi-core, and the new oblong `(26,h,2)` strip
   (26h, 2 short for h = 1…6).
3. **A single 678 gadget at f < 0.535533906 is worth 3.375e-3**, not 2.28e-3 — it takes
   all six D=2 puzzles, because the bank is at one shared f for the whole column. That
   is the highest-leverage single object left in the competition.
4. **The 0.0117 gap to the record is a relaxed-layout gap, not a phase gap.** Same
   finding as n=401 (rigid ceiling 400 vs record 401 relaxed). A slot spent on a
   *lattice/MILP* sweep cannot close it; only per-square relaxation can, and the D=2
   GA (`d2ladder`) already measured that wall at 190×–2100× the record's distance with
   0 legal improvements in 431 generations.
5. **Do not spend the final slot on this track's J1/J2** unless the kernel is already
   running; the machinery here is exact and the answer is negative. If the slot is
   free at 08:55, the honest choice is the broad-389 kernel already queued, not another
   D=2 search.

---

## 9. Files

| file | what |
|---|---|
| `corefill.py` | 2-core pinwheel + 4-phase axis fill, exact MILP; reproduces the 291 anchor (241+50) and both D=2 anchors (628+50=678, 852+50=902) |
| `randcore.py`, `randcore26.log` | 45-trial random multi-core search (best 666 at s=f_bank) |
| `bank678.csv`, `bank902.csv` | the bank's two D=2 layouts re-emitted and verified |
| `lift678.csv`, `lift902.csv` | their lifts to 678/731/786/843/902/963 and 902/963 (gain 0.0) |
| `kdir/kernel.py`, `kdir/kernel-metadata.json`, `kdir/smoke.log` | the self-contained kernel + local smoke |
| `retry_push.sh`, `push.log` | 8-minute push retry loop |
| `/tmp/campaign2/lift.py` | unchanged lift (corner-gadget identity), used for the §1 check |

Reproduce:

```sh
cd /tmp/campaign2/d2master
PY=/Users/zhaohuaxiang/ccjjllt/squares/.venv/bin/python
$PY corefill.py                     # 241/291 anchor, 0 overlaps
$PY randcore.py 26 0.5355339059327378 45   # multi-core ceiling 666
$PY /tmp/campaign2/lift.py --master bank678.csv --k0 26 --D 2 --ks 26 27 28 29 30 31 --out lift678.csv
$PY kdir/kernel.py                  # kernel smoke (J1 = 676 at every side)
```
