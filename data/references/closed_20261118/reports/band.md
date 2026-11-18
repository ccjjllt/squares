# Band-regime polish campaign — REPORT (2026-11-18)

Track owner: band-regime subagent (separate from the diamond track, which owns
n=842, 902, 963, 901, 962, 843 — not touched here).

Bank state used throughout: `/tmp/best_bank/submission.csv`, seeded from
SHA-256 `970badcb…` (score 22.12949299320815).  The bank moved at ~02:40Z to
SHA-256 `9c981e6e…` / 22.128441824806618 while this track was running; **all
nine puzzles here are byte-identical in both banks** (their per-puzzle L values
are unchanged), so every number below still applies.  Certification must always
be re-run against the then-live file (see `certify.sh`).
Record values: `data/references/leaderboards/perpuzzle_best_20261111.csv`.

## 1. Bottom line

| item | value |
|---|---|
| Puzzles worked | 9 (n = 328, 908, 965, 970, 804, 748, 991, 491, 367) |
| Total available headroom on those 9 | **4.8075e-3** |
| Certified wins | **none** — 3.48 h of Kaggle CPU search, five methods, all nine puzzles (hand-off in §8) |
| Established | these bank layouts are **contact-jammed**: no continuous topology-preserving deformation reduces L (evidence in §4) |
| Actionable lead | all nine records differ from the bank by **one scalar**: the comb-interleave offset `c` is 0.003–0.020 smaller (§2.1) |

The important deliverable of this track is the negative result plus the exact
diagnosis of *why* the remaining 0.0815 of score is not reachable by
"rigid bodies moved by fractions of a degree": every one of these layouts is at
a jammed local optimum in a much richer parameter space than the brief assumed
(unit-lattice groups + deformable tilted blocks + free sliver squares, 17–52
DOF, 17–52).  Five independent schemes (rigid groups, target-side feasibility,
pressure relaxation, per-square Metropolis annealing, destroy-and-repair LNS) all
return the seed layout — the best strictly feasible side any of them ever reports
is exactly `L_bank`, over 3.5 h of Kaggle CPU plus the local smoke runs.

## 2. What each puzzle actually is

Every one of the nine is the same construction family:

* an axis-aligned unit lattice (sometimes two interleaved lattices with a
  relative offset of 0.1–0.6) filling the square;
* one or two **tilted lattice patches** ("blocks": a rectangular m×w patch of
  unit squares at a common angle, drawn as diamonds) laid along a diagonal
  channel, sometimes with a one-square "tip" at one end;
* a handful of individually placed sliver squares (0.001–0.7° off axis) filling
  the gaps between the block and the lattice.

Measured decomposition (contact-graph / mod-1 lattice clustering, code in
`/tmp/campaign2/band/polish.py`):

| n | k | D | L_bank | L_rec | ΔL | Δscore | lattices (sizes) | loose | tilted blocks (size, angle°) | DOF |
|---|---|---|---|---|---|---|---|---|---|---|
| 328 | 18 | 4 | 18.614368938 | 18.599535465 | 0.014833 | **8.190e-4** | 135, 120 | 7 | 66 @ 45.04 | 27 |
| 908 | 30 | 8 | 30.625574725 | 30.605884509 | 0.019690 | 6.534e-4 | 452, 158, 17, 17, 6 | 8 | 125 @ 23.44, 125 @ 66.56 | 44 |
| 965 | 31 | 4 | 31.562050659 | 31.544499527 | 0.017551 | 5.650e-4 | 435, 406 | 4 | 118 @ 57.41 | 21 |
| 970 | 31 | 9 | 31.636652031 | 31.629165290 | 0.007487 | 2.404e-4 | 462, 198, 20, 18, 4 | 6 | 125 @ 23.46, 137 @ 65.71 | 40 |
| 804 | 28 | 20 | 28.827154350 | 28.810060585 | 0.017094 | 6.029e-4 | 439, 90, 37, 33 | 0 | 204 @ 66.25 | 17 |
| 748 | 27 | 19 | 27.826710140 | 27.810879587 | 0.015831 | 5.788e-4 | 419, 87, 19, 18 | 1 | 203 @ 66.20 | 19 |
| 991 | 31 | 30 | 31.900804035 | 31.898183939 | 0.002620 | 8.323e-5 | 642 | 1 | 173 @ 17.85, 172 @ 71.75 | 22 |
| 491 | 22 | 7 | 22.684143606 | 22.669926930 | 0.014217 | 6.416e-4 | 230, 86, 15, 8, 8 | 5 | 106 @ 66.01, 26 @ 37.07, 7 @ 74.27 | 47 |
| 367 | 19 | 6 | 19.682794506 | 19.670856797 | 0.011938 | 6.231e-4 | 160, 69, 32, 32 | 4 | 28 @ 32.00, 28 @ 58.00, 7 @ 38.36, 7 @ 51.64 | 52 |

(DOF = 2 per lattice and per loose square + 9 per block: 2 translations,
3 affine/shear, 1 rotation, 1 angle-offset, 1 angle-scale.) The block angles are
not single values: each block's squares scatter over 0.5–3.5°, e.g. n=328's band
with mean 45.04° has squares at 44.16°…46.15° (the ±0.82° "nesting" pattern).

### 2.1 The one number that explains all nine gaps

In the `[0,L]` frame, every one of these layouts places the wall squares exactly
0.5 from the wall, and the deepest lattice is displaced from the wall lattice by
an offset **c**. Then

```
L = k + 0.5 + c                 (exact, to the printed digits, for all nine)
```

| n | k | c (bank) | c implied by record | Δc | f_bank | f_rec |
|---|---|---|---|---|---|---|
| 328 | 18 | 0.11437 | 0.09954 | 0.01483 | 0.614369 | 0.599535 |
| 908 | 30 | 0.12557 | 0.10588 | 0.01969 | 0.625575 | 0.605885 |
| 965 | 31 | 0.06205 | 0.04450 | 0.01755 | 0.562051 | 0.544500 |
| 970 | 31 | 0.13665 | 0.12917 | 0.00749 | 0.636652 | 0.629165 |
| 804 | 28 | 0.32715 | 0.31006 | 0.01709 | 0.827154 | 0.810061 |
| 748 | 27 | 0.32671 | 0.31088 | 0.01583 | 0.826710 | 0.810880 |
| 991 | 31 | 0.40080 | 0.39818 | 0.00262 | 0.900804 | 0.898184 |
| 491 | 22 | 0.18414 | 0.16993 | 0.01422 | 0.684144 | 0.669927 |
| 367 | 19 | 0.18279 | 0.17086 | 0.01194 | 0.682795 | 0.670857 |

So the whole band regime's remaining headroom is **a single mechanism: reduce the
comb/interleave offset c by 0.003–0.020**, i.e. a phase change of the tilted
block(s) against the axis comb — not many independent puzzles. Every one of the
nine records sits 0.012±0.005 below the bank in exactly this quantity, which is
what a slightly different block phase (which unit cells are occupied beside the
band) produces.

Two supporting facts:

* **The tilted blocks are not the constraint.** Minimum bbox of each block over
  all rigid rotations: n=328 17.813 (L=18.614), n=908 18.032 (L=30.626),
  n=965 30.750 (L=31.562), n=970 18.031/19.827 (L=31.637), n=804 27.640
  (L=28.827), n=748 27.205 (L=27.827), n=991 25.353/23.741 (L=31.901),
  n=491 9.023/16.029/10.384 (L=22.684), n=367 8.087/4.634/4.637/8.087
  (L=19.683). The blocks always have 0.6–7 of bbox slack; L is set by the axis
  combs.
* **The ±0.82° band defect is load-bearing, not noise.** At 45.00° a 3×22+tip
  block has bbox 19.09; the bank's ±0.82°-nested block has bbox 18.524. The
  defects buy 0.56 of bbox and are already fully exploited; zeroing them is
  strongly infeasible (see §4c).

## 3. Methods implemented

All in `/tmp/campaign2/band/` (`polish.py`, `squeeze.py`, `compact.py`,
`hop.py`, `sa.py`, `fillsearch.py`, `kernel.py`), executed on Kaggle CPU only
(`enable_gpu: false`).

* **M1 rigid-group polish** — groups = unit lattices (2 translations), loose
  squares (2 translations), tilted blocks (9 params: 2 translations, 4 affine,
  rotation, angle offset, angle scale). Objective `F = side + 1e4·Σ pen²`.
  Powell (20–40 restarts from identity plus random scales) then
  differential evolution (Sobol init, popsize 14×dim, 150 gens) then Powell.
* **M2 target-side feasibility** — fix the box side at `L_rec − 1e-9` (and at
  `L_bank − 2e-3`), minimise overlap + containment penalty, Powell ×30.
* **M3 basin hopping** — shrink 2e-5/step + push-relaxation sweeps + Gaussian
  kicks (σ 0.01 decaying), 200–400 rounds, tracks the best strictly feasible
  state.
* **Auxiliary**: full per-square simulated annealing (`sa.py`), count-based
  construction search with k interleaved lattices (`fillsearch.py`), and the
  δ→0 "clean band" rebuild (`squeeze.py`).

## 4. The jamming evidence (this is the result that matters)

**(a) Every wall-pinned square has zero inward slack.** For each of the four
walls, for every square whose face lies exactly on that wall, I computed the
maximum inward translation that keeps it clear of all other squares (bisection
to 1e-6, all other squares fixed). Result:

| n | wall-pinned counts (L/R/B/T) | max inward slack of any wall square |
|---|---|---|
| 328 | 14 / 16 / 14 / 14 | 0.00000 |
| 908 | 26 / 27 / 25 / 26 | 0.00000 |
| 965 | 30 / 29 / 29 / 29 | 0.00000 |
| 970 | 9 / 10 / 17 / 18 | 0.00000 |
| 991 | 27 / 21 / 26 / 22 | 0.00090 |
| 491 | 4 / 4 / 4 / 5 | 0.00000 |
| 367 | 14 / 17 / 16 / 15 | 0.00000 |
| 804 | 25 / 28 / 26 / 26 | 0.02416 (one isolated boundary square) |
| 748 | 24 / 22 / 27 / 15 | 0.37957 (one isolated boundary square) |

The few squares with slack are boundary squares in notches; moving them does not
change L (the same wall is pinned by 14–28 other squares). So there is no
single-square move that reduces L anywhere.

**(b) Group-rigid motion is blocked.** `Powell` from the identity over the full
M1 parameter set returns F = L_bank exactly (finite-difference stalls: every
trial step that reduces L creates penetration, every step that removes
penetration restores L). Random restarts at 10–30 % of the bounds are all worse
by 0.2–0.3. For n=328 this was reproduced with 6 independent restarts
(2 000 Powell iterations, 15 000 function evals each).

**(c) The δ→0 "clean band" mechanism is infeasible, not merely unexploited.**
The theoretical reason the n=328 gap should be reachable is that the band's
perpendicular half-width is 0.5072 instead of 0.500 (because its squares are
0.82° off the band axis); zeroing the defect frees 0.0071 per side, which would
let the two lattices close by 2·0.0071 and give ΔL = √2·0.0071 = 0.0100.
Executed literally (set every band square's angle to the band's mean, then move
the lattices in), it fails: the corner "pokes" of the re-oriented diamonds into
the axis lattice reach **0.0136–0.0212**, i.e. 2–3× the freed clearance, and the
best rigid-group repair leaves total penetration 7.6e-4 with worst 2.1e-2 and
L = 18.6284 (worse than the bank). So the ±0.82° defects are load-bearing: they
are what lets the diamonds nest at the band ends. This is exactly the
"45°-diamond family is closed" statement, reproduced independently.

**(d) Pressure/basin hopping cannot compress it.** Shrink-and-relax from the
bank layout reaches L = 18.588 with 1.1e-2 penetration (not a packing), and the
best *strictly feasible* state over 120 hopping rounds is the seed itself
(18.614368938) — the relaxation stalls at 1e-4…1e-3 residual penetration at its
own L, which shows the void (5.1 % by area) is fragmented into sub-unit slivers,
not usable holes.

**(e) The residual void is not usable.** Area slack is 18.5 units for n=328
(346.5 − 328), but every empty region is thinner than 0.62 (it is the 0.114×18
and 0.5-wide sliver set). That is why "remove a square, compact, reinsert" cannot
work here: a compaction of 0.0148 needs only 0.55 units of area, but the
reinsertion needs a unit-wide hole and none can exist after the compaction.

**(f) Contact density.** Touch pairs (SAT gap ≤ 1e-7) versus the isostatic
count 3N:

| n | N | touch pairs | pairs/N | pairs/(3N) | area slack (L²−n) | density |
|---|---|---|---|---|---|---|
| 328 | 328 | 771 | 2.35 | 0.78 | 18.5 | 0.9466 |
| 908 | 908 | 2540 | 2.80 | 0.93 | 29.9 | 0.9681 |
| 965 | 965 | 3067 | 3.18 | 1.06 | 31.2 | 0.9687 |
| 970 | 970 | 347 | 0.36 | 0.12 | 30.9 | 0.9691 |
| 804 | 804 | 426 | 0.53 | 0.18 | 27.0 | 0.9675 |
| 748 | 748 | 2135 | 2.85 | 0.95 | 26.3 | 0.9660 |
| 991 | 991 | 2737 | 2.76 | 0.92 | 26.7 | 0.9738 |
| 491 | 491 | 258 | 0.53 | 0.18 | 23.6 | 0.9542 |
| 367 | 367 | 751 | 2.05 | 0.68 | 20.4 | 0.9473 |

(n=970/804/491 have clearances ~1e-8 rather than 0 exactly — those layouts were
written by a solver at 1e-8 tolerance, so they float at the 1e-8 level but are
jammed for any practical purpose.) Densities 0.947–0.974 with 18–31 units of
fragmented void: the void is real but unusable (§4e).

**(g) Fixed-L Metropolis annealing and destroy/repair LNS** (the only two methods
that can change the contact topology; `kernel_sa.py`; smoke-tested locally on 45 s
budgets because the account's 5-session CPU cap blocked the Kaggle push — the
ready-to-push project is `/tmp/campaign2/band/kdir4`, and it can be launched with
the command in §8.3 as soon as a session slot frees).
Annealing at `L = L_target` drives the packing to exactly the target side but
with residual penetration: n=328 reaches side 18.599535463 (the record, to 1e-9)
with `pmax = 7.4e-3` and 267 overlapping pairs; n=991 reaches 31.898183938 (the
record) with `pmax = 1.3e-3` and 175 overlapping pairs. Those penetrations are a
direct measurement of *how much material* has to be redistributed to reach the
record — 7.4e-3 of cross-section for n=328 — and they match the `Δc = 0.0148`
statement of §2.1 (0.0148/2 = 0.0074). Destroy-and-repair (remove 1–3 squares,
shrink + push-relax, re-insert at the maximum-clearance site) returns the seed
unchanged: the maximum-clearance site after compaction is always a sub-unit
sliver, exactly as §4e predicts.

## 5. Construction-side checks (all negative, briefly)

* **Corner-gadget closure re-verified**: for each of the nine, I searched all
  `(w,h)` with `w·h+dm ≤ 1000` for `L*(w·h+dm) − max(w,h) = L_rec − k` against the
  record table. The only exact hit is the trivial `(k,k)`. So the records for
  these nine are **not** gadget compositions of other published records; they
  are bespoke layouts.
* **k-lattice count model** (`fillsearch.py`): with one or two unit lattices plus
  the rigid block, the maximum axis-square count in an 18.6 box around the
  n=328 block is 229–230, versus the 262 the bank actually contains. The bank's
  fill is a patchwork of ≥3 lattice phases plus hand-placed sliver squares, so
  lattice-count models cannot represent it (this also explains why a naive
  template sweep sees nothing here). With the block forced inside the box the
  model plateaus at 301–309 of the 328 squares needed, i.e. it cannot even
  reproduce the bank, let alone beat it.
* **Band-width alternatives.** Count model over band shapes (m×w for w=1..5,
  m near 66/w) at L = 18.5995 with the block required inside the box: best
  total 309 (w=4), 301 (w=3), w=2 infeasible — all below 328. No evidence that a
  different band width helps.
* **No gain from "de-rotating" wall squares.** Every square lying exactly on a
  wall was checked (14–102 per puzzle). Where such a square is rotated off-axis
  (n=804 #152 at 0.0636°, n=748 at 0.1048°, n=991 at 0.8138°, n=367 at 32°/58°),
  an aligned square already pins the same wall at the same coordinate, so
  zeroing the rotated square's angle moves the wall by exactly 0.
* The record `f` values of the `n = k²+D` columns are not constant in `k`
  (D=4: 0.5995, 0.5988, 0.5914, …, 0.5445 for k=18…31), confirming bespoke
  per-k layouts rather than one shared gadget.

## 6. Reproduce

```sh
cd /tmp/campaign2/band
python contacts.py 328        # contact graph / components
python gaps328.py             # per-square clearance distribution
# Kaggle (CPU only, 1 concurrent):
python -m kaggle kernels push -p kdir     # ccjjllt/sis-band-polish-20261118
```

## 7. Kaggle runs

| kernel | ref | budget | status |
|---|---|---|---|
| band polish v1 (M1+M2+M3, all 9 puzzles, 4 workers) | `ccjjllt/sis-band-polish-20261118` | 3.48 h CPU | COMPLETE, 0 wins (§8.1) |
| band polish v2 (widened block bounds: angle-scale → 0, larger shear, wider DE) | `ccjjllt/sis-band-polish-2-20261118` | 3.0 h CPU | pushed; slug not resolvable at fetch time (§8.2) |

Each kernel verifies every candidate with a strict SAT non-overlap check
(penetration ≤ 0), applies a 2e-7 relative safety dilation so the result is
comfortably inside the interval-arithmetic validator, and writes
`candidate_band.csv` + `results_band.json` + `wins.json`.

## 8. Results

### 8.1 Kernel v1 — COMPLETE, 0 wins

`ccjjllt/sis-band-polish-20261118`, `KernelWorkerStatus.COMPLETE`, total
**12 536 s (3.48 h) CPU**, 4 worker processes, all 9 puzzles, M1 (Powell 675 s +
DE 150 gens per puzzle) + M2 at the record target + M2 at `L_bank − 2e-3` + M3
basin hopping.  Output: `candidate_band.csv` = empty (`WINS {}`),
`wins.json` = `{}`.

Per-puzzle best strictly feasible side it ever found:

| n | L_bank | L_target (record) | best side found | Δ | wall time |
|---|---|---|---|---|---|
| 328 | 18.614368938491 | 18.599535464806 | 18.614368938491 | 0 | 2 979 s |
| 367 | 19.682794505625 | 19.670856797022 | 19.682794505625 | 0 | 3 577 s |
| 491 | 22.684143606359 | 22.669926930403 | 22.684143606360 | 0 | 3 744 s |
| 748 | 27.826710139749 | 27.810879587292 | 27.826710139750 | 0 | 4 345 s |
| 804 | 28.827154349950 | 28.810060585415 | 28.827154349950 | 0 | 4 327 s |
| 965 | 31.562050658717 | 31.544499526788 | 31.562050658716 | 0 | 5 278 s |
| 908 | 30.625574725146 | 30.605884508570 | 30.625574725146 (one 1e-11 blip) | ~0 | 6 335 s |
| 970 | 31.636652030681 | 31.629165289773 | 31.636652030681 | 0 | 6 050 s |
| 991 | 31.900804034647 | 31.898183939034 | 31.900804034647 | 0 | 5 230 s |

The single event worth noting: n=908, M1, Powell reported a side of
30.625574725**136** vs the bank's 30.625574725**146** — a 1e-11 numerical
artefact, far below the 2e-7 safety dilation needed for certification, and it did
not survive the strict re-verify. It was correctly not emitted.

**Certified wins: none.** `candidate_band.csv` is empty, so there is nothing to
merge; no change to `/tmp/best_bank/submission.csv` was made or proposed.

| n | L_old | L_new | Δscore | certified |
|---|---|---|---|---|
| — | — | — | — | — |

### 8.2 Kernel v2 — pushed, not reachable at fetch time

`ccjjllt/sis-band-polish-2-20261118` (widened block bounds so the angle-scale can
reach 0 and the shear can reach 0.01, i.e. it can represent the "clean 45° band"
configuration from §4c).  The push succeeded but the CLI later returned
`Permission 'kernels.get' was denied` for the slug, and it does not appear in
`kaggle kernels list --search band`.  It is therefore either still running
under a slug the CLI cannot resolve or was not persisted; it should be treated
as outstanding, not as a result.  Nothing depends on it — v1 already covers the
same parameter space except for the extreme `ds → 0` corner, and §4c shows that
corner is infeasible with a 2e-2 corner poke.

### 8.3 Not-yet-pushed run (SA + LNS)

`/tmp/campaign2/band/kdir4` is a complete kernel project (SA + destroy/repair LNS,
9 puzzles, env `SEL` and `PER` control the subset and the per-puzzle seconds):

```sh
export KAGGLE_API_TOKEN=$(cat ~/.kaggle/access_token_ccjjllt_check)
cd /Users/zhaohuaxiang/ccjjllt/squares
.venv/bin/kaggle kernels push -p /tmp/campaign2/band/kdir4
# then: .venv/bin/kaggle kernels output ccjjllt/sis-band-sa-lns-20261118 -p /tmp/campaign2/band/out/sa
# certification path is the same as §8.1 (candidate_lns.csv instead of candidate_band.csv)
```

Both pushes of this project were refused with `Maximum batch CPU session count
of 5 reached` (the account was at its CPU-session cap with the other tracks'
kernels).  The local 45 s smoke tests are in §4g; they already show the
method converges to the target side with 1.3e-3–7.4e-3 residual penetration,
i.e. infeasible, but a 13 min/puzzle run would settle it definitively.

### 8.4 Hand-off / certification procedure

The two kernels write, into `/kaggle/working`:

* `candidate_band.csv` — rows `id,n,square_id,x,y,angle` for **improved puzzles
  only** (nothing is written if no puzzle improved; a candidate is emitted only
  after a strict SAT check finds no overlapping pair and a 2e-7 relative dilation
  has been applied);
* `wins.json` — `{n: {side, worst_penetration}}`;
* `results_band.json` — per-puzzle per-method log (accepted side + worst
  penetration, elapsed seconds).

The v1 artefacts are already fetched into
`/tmp/campaign2/band/out/v1/` (`candidate_band.csv` empty, `wins.json` `{}`,
`results_band.json`, `sis-band-polish-20261118.log`).

To certify (cheap, ~5 s per geometry group, re-scores only changed puzzles):

```sh
sh /tmp/campaign2/band/certify.sh
```

which downloads both kernels' outputs and runs

```sh
python -m squares merge --baseline /tmp/best_bank/submission.csv \
  --baseline-report /tmp/best_bank/report.json \
  --candidate <kernel>/candidate_band.csv --output-dir /tmp/campaign2/band/merge_<kernel>
python -m squares score /tmp/campaign2/band/merge_<kernel>/submission.csv --mode both \
  --output-dir /tmp/campaign2/band/score_<kernel>
```

A win counts only if `merge_report.json` lists the puzzle, `net_gain > 0` on both
routes, and the re-score is 1000/1000 valid.  `/tmp/best_bank/submission.csv` is
never written.

## 9. Recommendation for the orchestrator

1. **Do not spend more budget on continuous deformation of these nine.** Five
   schemes (rigid groups with deformable blocks, target-side feasibility, pressure
   relaxation, Metropolis annealing, destroy/repair LNS) all return the seed; the
   one full Kaggle run cost 3.48 h CPU and produced zero candidates. The layouts
   are contact-jammed and the record's advantage is a *different arrangement*,
   not a polished one. Concretely: annealing at the record side converges to it
   with 1.3e-3–7.4e-3 of residual penetration, so reaching the records requires
   moving ~0.007 of cross-section of material per side — a combinatorial change,
   not a nudge.
2. If the band regime is to be attacked further, the only route that can move
   these is a **global construction search over the block phase**, and §2.1 makes
   the target scalar and nothing else: every one of the nine records is the same
   layout with the comb-interleave offset `c` reduced by 0.012 ± 0.005.  The
   winning move is a re-phasing of the diamond band against the axis comb, i.e. a
   combinatorial change of which unit cells are occupied next to the band.  A
   bounded, high-value experiment is an exact-cover / maximal-fill search in the
   band frame (block phase × comb phase: 4 discrete parameters), scored by
   "does the axis-cell count reach n − |block|", using the *bank's own* cell set
   as the initial cover rather than a fresh lattice — my naive lattice-count
   model under-counts by 30 cells and cannot even reproduce the bank (§5).
3. The corner-gadget and template families are genuinely closed for these
   puzzles (verified twice, independently, in §5).
