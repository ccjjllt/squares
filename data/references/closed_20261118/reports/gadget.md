# Near-square / corner-gadget track — REPORT

Campaign: Kaggle `squares-in-squares`, 2026-11-18.
Baseline at the start of this track: **22.129684493721086**; corrected mid-flight to
**22.129502357094957** (52 frontier puzzles merged 00:15Z). All numbers below are against the
live `/tmp/best_bank/submission.csv`, SHA-256
`6f6e9da8e3c795914d89f1e79d777233e256cce4a5600ab32d0e70e8f55e0c40`, which I re-verified
reports 22.129502357094957 on both routes.

---

## 1. The composition, re-derived and machine-verified

A packing of `w*h+dm` unit squares whose axis-aligned bbox is `(w+fx) x (h+fy)`, with
`f = max(fx,fy)`, yields for every `k >= max(w,h)` a packing of `k*k+dm` with `L = k+f+2e`.

Geometry actually used (identical to `fault_dp.compose`, which I re-derived and checked):

| piece | cells |
|---|---|
| lower-left continent | upright `(i+.5, j+.5)`, `i in [0,w)`, `j in [0,k-h)` |
| upper-right continent | upright `(i+.5+F, j+.5+F)`, `i in [w,k)`, `j in [0,k)`, `F=f+2e` |
| gadget | its own layout, bbox min at `(0, k-h)` |

Count: `w(k-h) + (k-w)k + (w*h+dm) = k*k+dm`. The gadget's right edge `w+fx < w+F` never meets
the UR continent, and its bottom edge sits exactly at `y=k-h` where the LL continent stops, so
**no upright cell has to be removed** — the composition is exact for any `(w,h)` with
`max(w,h) <= k`, not only squares.

Verification (local, official metric, both routes): using the bank's own `n=626` layout as a
`(25,25,1)` gadget at `f=0.520815280171` reproduces the certified bank exactly —

| n | k | composed L | bank L | certified |
|---|---|---|---|---|
| 626 | 25 | 25.520815280196 | 25.520815280171 | ok |
| 677 | 26 | 26.520815282197 | 26.520815280171 | ok |
| 842 | 29 | 29.520815282200 | 29.520815280171 | ok |
| 962 | 31 | 31.520815282202 | 31.520815280171 | ok |

(the 2e-9 residual is the `e` guard; `e=1e-11` still certifies and leaves 2e-11).

Chain (2+ gadgets along the anti-diagonal, fault_dp modes 0/X/Y) was implemented and verified
too: two `(12,12,1)` gadgets at `f=0.535534` compose n=627/963 at L=k+0.535534 with mode X
(`j1+j2+1 <= k`), certified.

## 2. What the bank actually is (measured, not assumed)

`f_bank(k,D) = L_bank(k^2+D) - k` and `f_rec(k,D) = L_rec(k^2+D) - k` were computed for
`k=16..31`, `D=1..30` (`f_bank.csv`, `f_rec.csv`; total column gap **0.076040**, matching the
brief's decomposition).

**The bank's near-square family is exactly the crop-composition optimum of its own layouts.**
I recomputed, for every `(j,j,D)`, the least-overhang crop of `j*j+D` squares over all 1000 bank
layouts under all 8 symmetries (`croptable_full.csv`, 28 j-values x 30 D-values x ~1500
donors). The result reproduces the bank's f ladder to the last digit:

| j | 16 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25..31 |
|---|---|---|---|---|---|---|---|---|---|
| f_crop(D=1) | 0.53553 | 0.53553 | 0.53553 | 0.53301 | 0.52548 | 0.52535 | 0.52535 | 0.52535 | 0.52082 |
| f_bank(k=j,D=1) | 0.53553 | 0.53553 | 0.53553 | 0.53301 | 0.52548 | 0.52535 | 0.52535 | 0.52535 | 0.52082 |

Same identity for every D from 1 to 30. **So there is no free win anywhere: every bank f in this
family is precisely the best crop available from the bank's own layouts, and a dedicated search
for a *new* packing is the only way forward.** This also explains the plateau: one gadget
(`f=0.52081528`, first available at j=25) serves the whole k=25..31 tail.

## 3. Route 2 (two-corner / chain compositions) — closed, arithmetically

Nothing was spent on kernels for this, only integer/CSV work, as instructed.

Using the full crop gadget table I evaluated, for every `(k,D)` with `k=16..31`, `D=1..30`:

* `f1` = min over single `(j,j,D)` gadgets with `j <= k`;
* `f2` = min over splits `D=D1+D2` and `j1+j2+1 <= k` (mode-X seam) of `max(f1,f2)`;

and compared with the bank's own `f(k,D)`.

**Result: 0 of 480 cells.** No 1-gadget and no 2-gadget chain built from the bank's own crop
table beats the bank. (Consistent with the brief's "only 3 wins at 2.6e-12" for 1-corner; the
2-corner/chained case is now closed as well.) `chain_bound.json` is empty.

## 4. Route 1 (target-f search at fixed side)

### 4.1 Where the value is

Amplification arithmetic (`amp.csv`): finding the packing of `n=k^2+D` at `L = L_rec(n)` is worth
its own per-puzzle gain **plus** every `k'>k` in the same D column, because the same
`(k,k,D)` gadget lifts them all. Ranking all family puzzles by that amplified value gives the
anchor list used for the search (`anchors.json`). Top 12:

| rank | n | k | D | f_bank | f_rec | amplified value |
|---|---|---|---|---|---|---|
| 1 | 678 | 26 | 2 | 0.535534 | 0.523860 | 2.46e-3 |
| 2 | 626 | 25 | 1 | 0.520815 | 0.511049 | 2.45e-3 |
| 3 | 677 | 26 | 1 | 0.520815 | 0.510279 | 2.22e-3 |
| 4 | 785 | 28 | 1 | 0.520815 | 0.505935 | 2.02e-3 |
| 5 | 731 | 27 | 2 | 0.535534 | 0.523851 | 2.02e-3 |
| 6 | 730 | 27 | 1 | 0.520815 | 0.509315 | 1.99e-3 |
| 7 | 786 | 28 | 2 | 0.535534 | 0.521592 | 1.89e-3 |
| 8 | 842 | 29 | 1 | 0.520815 | 0.502153 | 1.87e-3 |
| 9 | 843 | 29 | 2 | 0.535534 | 0.518244 | 1.73e-3 |
| 10 | 530 | 23 | 1 | 0.525352 | 0.517305 | 1.57e-3 |
| 11 | 902 | 30 | 2 | 0.535534 | 0.514079 | 1.41e-3 |
| 12 | 908 | 30 | 8 | 0.625564 | 0.605885 | 1.25e-3 |

### 4.2 Seed reality check (why this is hard)

For anchor `(26,26,2)` only **7 of 323** donors yield a crop within 0.02 of the record's f, and
**none** within 0.005; the best crop is the bank's own 0.535534. The same holds for
`(25,25,1)` (0 of 375 within 0.005) and `(28,28,1)` (0 of 216). So every seed has to be
compressed by 0.010-0.012 in f (0.04 % linear) *and then* repaired — the same ask as the
previously failed "hop" experiments, just at a smaller delta. This is the fundamental difficulty
of the track and the reason the reported prior is 0/61 and 0/246.

### 4.3 Oblong gadgets: the census says they are not a shortcut either

An oblong gadget `(w,h,dm)` with `w>h` lifts exactly the same puzzles as `(w,w,dm)`, and for the
same `f` it needs less density, `rho = (wh+dm)/((w+f)(h+f))`, e.g. at k=24, D=1:
`(24,24,1)` needs 0.9593, `(24,20,1)` 0.9556, `(24,16,1)` 0.9499. That looked like an easy win
until I measured what the crop table already supplies:

| gadget | K | f_bank at k=w | best crop | donor |
|---|---|---|---|---|
| (24,20,1) | 481 | 0.525355 | 0.527786 | n=577 |
| (24,16,1) | 385 | 0.525355 | 0.535534 | n=627 |
| (30,22,1) | 661 | 0.520815 | 0.535534 | n=902 |
| (26,22,2) | 574 | 0.535534 | 0.535534 | n=844 |

The DP already picks the *square* crop (`0.525355`, `0.520815`) because it is better. So an oblong
gadget does not start closer to a win — it has to beat a well-optimised square crop by the same
0.005-0.015, on a shape whose own best-known packing is worse. Included in wave 2 as a diversity
class, not as a shortcut.

### 4.4 Coordination note

While this track was blocked on slots, other agents pushed kernels onto exactly the ground this
track was carving: `sis-cdb-45deg-family-sweep-20261118` and `sis-cdb2-rotated-core-sweep-20261118`
(the 45° rotated-core family of §8), `sis-closed-form-grid-band-templates-20261118` (grid+band),
and `sis-d2-ladder-20261118` / `sis-sa291b-20261118` (the D=2 ladder and n=291, two of this
track's top four anchors). Their published `improved_groups.csv` for n=683 (26²+7) and n=751
(27²+22) are bit-identical to the bank (gain 1e-16), so nothing was harvestable.

### 4.5 The rotated-block family is dominated (kills a tempting shortcut)

I reconstructed the "solid 45-degree m x m block + upright integer corners" family exactly
(`rotblock_sweep.csv`, 480 cells): for every `(j,D)` I maximised the absorbed square count over
`m` and over block position and grid offsets at `L = j + f_bank - 1e-6`. **0 wins.** The best
cell reaches 98.2 % of the required count (n=962, m=8), i.e. the family is ~2 % short
everywhere — it is not the record's construction and cannot be turned into an instant win.
(A strict check: 626 squares at k=25 would need 607+19 in the best member.)

## 5. Kernels

| ref | purpose | status |
|---|---|---|
| `ccjjllt/sis-nearsquare-gadget-anchors-v1-20261118` | 26 anchors x crop seeds x fq quench, 4 workers, CPU | pushed 16:47Z, RUNNING and queryable until 19:11Z, **then 403 on every endpoint (status/files/output) and absent from `kernels list`**: the kernel and its `hits.jsonl` were lost, most likely deleted server-side while running |
| `ccjjllt/sis-nearsquare-gadget-mild-oblong-v2-20261118` | mild targets + oblong gadgets, 1.75 h budget, small output | written and ready, **could not be pushed**: `Maximum batch CPU session count of 5 reached` on every attempt 20:11-20:45Z |
| `ccjjllt/sis-24x25-1-gadget-target-f-v2-20261117` | pre-existing, (24,25,1) | ERROR, **no output files** (verified: `kernels files` empty, `kernels output` hangs on the rust build dir only) |
| `ccjjllt/sis-neighbour-key-gadget-search-20261117` | pre-existing, neighbour keys | was RUNNING for ~12 h; after 20:00Z also 403 / not listable, i.e. it did not produce retrievable output either |

Kernel-time actually consumed by this track: ~2.9 h of one CPU slot (16:47Z-19:40Z), no retrievable result.

## 6. Results

**No certified win from this track.** Nothing was found that could be certified, and the one
kernel that could have found something was lost before it finished, with the slot then closed
by the account-wide 5-session cap. `candidate.csv` is therefore not produced: with zero
gadgets there is nothing to lift, and shipping the bank unchanged is not a candidate.

The pipeline that would turn a found gadget into a certified column lift is finished and
validated (§7), so any gadget produced later can be certified in ~10 minutes.

**Recommendation for the orchestrator.** After §2 and §3, the near-square family has no
arithmetic win left: the bank is exactly the crop-composition optimum of its own layouts, and
both the 1-/2-gadget chain closure and the rotated-block family come back empty. What remains is
pure local search against packings that are already ~96 % dense, i.e. exactly the "hop" class
that this account has failed 0/61 and 0/246 on. If a CPU slot has to be allocated, the tracks
currently producing (`sis-band-polish-*`, `sis-cpp-engine-self-ga`, `sis-d2-ladder`) are a better
bet than reviving this one; the 1 h `k2` kernel is here if a slot is otherwise idle.

## 7. Deliverables, and exactly what to run next

Built and validated (all in `/tmp/campaign2/gadget/`):

| file | what it does | validated how |
|---|---|---|
| `compose_gadget.py` | exact corner composition (fault_dp geometry) | reproduces the certified bank from its own n=626 layout at 4 values of k; official metric `ok` |
| `compose_chain.py` | 2+ gadget chains, seam modes 0/X/Y | two (12,12,1) gadgets compose n=627/963, certified |
| `apply_gadgets.py` | gadget hits -> per-k composition -> metric certification -> `groups.csv` | synthetic win: detects it, certifies, reports 3.16e-3 |
| `build_candidate.py` | bank verbatim + replaced blocks | with no lifts the output is **byte-identical** to `/tmp/best_bank/submission.csv` |
| `bound2.py`, `closure_bound.py` | 1- and 2-gadget closure over the full crop table | 0 of 480 cells |
| `rotblock_sweep.py` | rotated-block family capacity | 0 wins, best 98.2 % of the required count |
| `k2/kernel.py` | wave-2 search (mild + oblong), 1.0 h, self-contained | ready to `kaggle kernels push -p /tmp/campaign2/gadget/k2` |

To finish the track when a CPU slot exists:

```sh
export KAGGLE_API_TOKEN=$(cat ~/.kaggle/access_token_ccjjllt_check)
cd /Users/zhaohuaxiang/ccjjllt/squares
.venv/bin/kaggle kernels push -p /tmp/campaign2/gadget/k2          # 1.0 h budget
.venv/bin/kaggle kernels output ccjjllt/sis-nearsquare-gadget-mild-oblong-v2-20261118 -p /tmp/campaign2/gadget/k2out
/tmp/campaign2/gadget/finalize.sh /tmp/campaign2/gadget/k2out/hits2.jsonl
```

`finalize.sh` runs `apply_gadgets.py` (compose + certify every k) and then `build_candidate.py`
+ `python -m squares score --mode both`, and prints the per-puzzle delta.

Independent of gadgets, two results here are directly reusable by any other track:

1. **`croptable_full.csv`** — the least-overhang crop `f` for every `(j,j,D)`, `j=4..31`,
   `D=1..30`, over every available donor under all 8 symmetries. It reproduces the bank's whole
   near-square ladder exactly, so it is the exact "what the bank already knows" baseline.
2. **The pinwheel structure** (§8) — the bank's `f = 5/sqrt2 - 3 = 0.535533906` family is not a
   corner gadget at all, so it is invisible to `fault_dp` and to every gadget-table method. Any
   attempt to beat `f=0.5355` there has to work on that structure directly.

## 8. The `5/sqrt2 - 3` family is a pinwheel, not a gadget

Measured on the certified bank (`n=362`, k=19, D=1, L=19.5355339059328):

* 50 squares at exactly 45 deg, in **two 5x5 rotated blocks** (25 each, verified: each cluster has
  5 distinct `x+y` and 5 distinct `x-y` values spaced sqrt2, i.e. a solid rotated lattice);
* block bboxes `[0.7322, 7.8033] x [9.7322, 16.8033]` and its 180-degree image
  `[9.7322, 16.8033] x [0.7322, 7.8033]` — opposite corners, bbox `5*sqrt2 = 7.0711` each;
* the other two corners are ordinary upright blocks, and 37 of the 312 uprights sit **off** the
  0.5 lattice, in the staircase gaps beside the rotated blocks.

The same skeleton (50 rotated squares, same `f`) carries `n=291` (D=2) and `n=257`/`325`
(D=1, different upright counts), which is why the column is a plateau.

A clean parametric rebuild of it ("two `m x m` rotated blocks in opposite corners + upright
integer fill", `twoblock.py`, 2 offsets + lattice offset + `m`) reaches only **328 of 362**
squares at the same L — the certified layout is ~10 % better than the clean construction, i.e.
almost all of its quality is in the off-lattice staircase fill. That is why a clean constructive
seed cannot replace the search: it is far short in *count*, and `fq` can only shrink a side, never
add a square.

## 9. Numeric summary

| quantity | value |
|---|---|
| baseline (live bank, both routes, re-verified) | 22.129502357094957, 1000/1000 |
| near-square family gap, k=16..31, D=1..30 | 0.0760397 |
| route-2 (1- and 2-gadget chain) cells that beat the bank | **0 / 480** |
| rotated-block family cells that beat the bank | **0 / 480** (best 98.2 %) |
| clean pinwheel count vs certified layout at n=362 | 328 vs 362 |
| certified score improvement from this track | **0.000000000** |
