# Public-frontier harvest — Squares in Squares (2026-11-17/18)

_All times below are UTC. The local machine is UTC+8; local 01:10 on Nov 18 = 17:10Z on Nov 17._

Track: public artifact harvesting for the `squares-in-squares` campaign.
Machine used only for Kaggle API reads/downloads, CSV I/O, `squares merge`, `squares score`.
**0 Kaggle kernels used, 0 optimisation runs.** Work dir `/tmp/campaign2/harvest/`.

## Headline

| item | value |
|---|---|
| Certified merges produced | 3 (`merge_m1`, `merge_m2`, `merge_m3`) |
| Our delta over the live bank at merge time | +2.557e-7 (m1), +2.072e-9 (m2), **+1.1011e-5 (m3)** |
| Best merged CSV | `/tmp/campaign2/harvest/merge_m4/submission.csv` |
| Best score (dual route) | **22.129481982260582** (text and float64, 1000/1000 valid) |
| SHA-256 | `19877e21aeb728221bbcb9fb53e3e47ac2dca027180f378b84c351aabfd8cf43` |
| Status | adopted as the live bank at 18:12Z; **superseded at 18:17Z** by the optimisation track's 6-puzzle merge (bank 22.128441824807). m4 remains a valid, certified artifact and carries our +1.1011e-5 into the bank. |
| Delta vs brief-start bank 22.129684493721086 | **2.025114605e-4**; of that the orchestrator's own merges account for 1.9150e-4 and **our harvest 1.1011e-5** (plus 2.56e-7 absorbed into the bank at 17:18Z) |

The entire *old* public state (kernels, datasets, GitHub records, local caches)
is already inside the live bank. The cash flow came from **three fresh uploads**:
a 4-puzzle update in the alexchilton starter kit (17:06Z, absorbed by the
orchestrator at 17:18Z) and `areebbb`'s "The Last 1e-9" re-run at **17:48Z**,
which we downloaded **one minute later** and certified for **+1.1011e-5** —
the largest public donation found this session (43x the earlier areebbb delta).

## Bank drift observed (important)

| UTC | Bank SHA (short) | Bank score | Event |
|---|---|---|---|
| brief start | `b0ecc093…` | 22.129684493721086 | quoted in BRIEF |
| 16:15Z | `6f6e9da8…` | 22.129502357094957 | orchestrator merged 52 frontier puzzles |
| 17:10Z (m1 baseline) | `6f6e9da8…` | 22.129502357094957 | our `merge_m1` → 22.129502101395065 |
| 17:18Z | `9bdbce2b…` | 22.129495171822438 | auto-pipeline merged starter-kit `best_current.csv` (n=127,683,751,800) |
| 17:29Z (m2 baseline) | `9bdbce2b…` | 22.129495171822438 | our `merge_m2` → 22.129495169750346 |
| 17:48Z | `9bdbce2b…` | 22.129495171822438 | areebbb re-runs "The Last 1e-9" (new upload) |
| 17:56Z (m3 baseline) | `9bdbce2b…` | 22.129495171822438 | our `merge_m3` → **22.129484160874867** |
| 17:55Z | `970badcb…` | 22.12949299320815 | auto-pipeline merged a new n=683 packing (ΔL 5.69e-5) |
| 18:05Z (m4 baseline) | `970badcb…` | 22.12949299320815 | our `merge_m4` → **22.129481982260582** |
| 18:12Z | `19877e21…` | **22.129481982260582** | orchestrator **adopted our m4 file as the live bank** (SHA now equals `merge_m4/submission.csv`) |
| 18:17Z | `9c981e6e…` | 22.128441824807 | optimisation track merged 6 puzzles (n=262 ΔL 8.99e-3, n=295 6.12e-3, n=210 1.79e-3, n=272, 260, 292); supersedes m4 |

All merges were run against the **live** `/tmp/best_bank/submission.csv` with a
`report.json` whose `input.sha256` matched the CSV at that moment.
At 18:12Z the orchestrator adopted `merge_m4/submission.csv` as the new bank
(bank SHA `19877e21…`, score 22.129481982260582), so the m4 delta is now live.

## Certified merges

### merge_m1 — areebbb + penguin069 (2026-11-17 ~17:10Z)

- Baseline: live bank `6f6e9da8…`, 22.129502357094957
- Candidates:
  - `areebbb/squares-in-squares-the-last-1e-9` → `submission.csv`,
    SHA-256 `ba5211f48e5afcc918dcc70905e50afd1a9de8c4a8886a27df36275e3c51a318`
  - `penguin069/squares-fresh-lattice-box-homotopy-cpu-pilot` → `submission.csv`
- Changed puzzles: **20**; net gain **2.556998925928866e-07** on both routes
- Result: **22.129502101395065**, text = float64, 1000/1000 valid
  (`/tmp/campaign2/harvest/score_m1/report.json`, 205 s)
- Largest win: n=127, L 11.800832428563 → 11.800829569245 (Δ 2.858e-6, +2.537e-7 score)

### merge_m2 — areebbb residual (2026-11-17 ~17:29Z)

- Baseline: live bank `9bdbce2b…`, 22.129495171822438
- Candidate: the same areebbb `submission.csv` (its n=127 win was already in the
  new bank via the starter kit; 19 residual micro-wins remained)
- Changed puzzles: **20**; net gain **2.0720904991833322e-09** on both routes
- Result: **22.129495169750346**, text = float64, 1000/1000 valid
  (`/tmp/campaign2/harvest/score_m2/report.json`, 184 s)

| n | old L | new L | dL | score gain |
|---|---|---|---|---|
| 127 | 11.800829570323 | 11.800829569245 | 1.078e-09 | 9.567e-11 |
| 330 | 18.687652890045 | 18.687652889775 | 2.692e-10 | 1.482e-11 |
| 340 | 18.920975596329 | 18.920975595529 | 8.002e-10 | 4.340e-11 |
| 442 | 21.525482581390 | 21.525482579010 | 2.380e-09 | 1.132e-10 |
| 448 | 21.687501911902 | 21.687501911686 | 2.164e-10 | 1.022e-11 |
| 599 | 24.916816140207 | 24.916816137707 | 2.499e-09 | 1.021e-10 |
| 601 | 24.953949977949 | 24.953949964470 | 1.348e-08 | 5.498e-10 |
| 632 | 25.637038698794 | 25.637038698322 | 4.722e-10 | 1.878e-11 |
| 705 | 26.974530459553 | 26.974530450092 | 9.461e-09 | 3.563e-10 |
| 741 | 27.707243773679 | 27.707243771478 | 2.201e-09 | 8.087e-11 |
| 748 | 27.826710141126 | 27.826710139749 | 1.376e-09 | 5.033e-11 |
| 758 | 27.953986016121 | 27.953986014356 | 1.765e-09 | 6.410e-11 |
| 807 | 28.860408935860 | 28.860408933085 | 2.775e-09 | 9.767e-11 |
| 809 | 28.889721754318 | 28.889721753000 | 1.318e-09 | 4.635e-11 |
| 851 | 29.665313616296 | 29.665313614491 | 1.805e-09 | 6.188e-11 |
| 875 | 29.988197357494 | 29.988197357313 | 3.181e-09 | 1.076e-10 |
| 911 | 30.670688893665 | 30.670688890925 | 2.741e-09 | 9.080e-11 |
| 926 | 30.870319668204 | 30.870319664714 | 3.490e-09 | 1.147e-10 |
| 933 | 30.943865819814 | 30.943865818447 | 1.366e-09 | 4.473e-11 |
| 986 | 31.851742951826 | 31.851742951550 | 2.762e-10 | 8.797e-12 |

### merge_m3 — areebbb 17:48Z upload (2026-11-17 ~17:56Z)

- Baseline: live bank `9bdbce2b…`, 22.129495171822438
- Candidate: `areebbb/squares-in-squares-the-last-1e-9` → `submission.csv`
  (last run **17:48:01Z**, raw file 43,090,417 bytes,
  SHA-256 `4346b114bfd7bb31f62b16739b4da4bdef4d2524dfdec1d3e37ba07feb789186`;
  trimmed 24-group candidate SHA-256
  `b1e7fb8dfc59b2955f6979ec42e2e3ca160a7fb68fd67a7ed98d0c93eafd6938`)
- Changed puzzles: **24**; net gain **1.101094756905674e-05** on both routes
- Result: **22.129484160874867**, text = float64, 1000/1000 valid
  (`/tmp/campaign2/harvest/score_m3/report.json`, 187 s)
- Four structural wins carry 99.9 % of the delta (n=549, 932, 651, 995);
  the other 20 are the residual 1e-9-scale groups from the earlier version.

| n | old L | new L | dL | score gain |
|---|---|---|---|---|
| 549 | 23.890790406574 | 23.890626769981 | 1.636e-04 | 6.984e-06 |
| 932 | 30.936107061644 | 30.936051601525 | 5.546e-05 | 1.817e-06 |
| 651 | 25.942466524602 | 25.942429188188 | 3.734e-05 | 1.463e-06 |
| 995 | 31.942989104539 | 31.942965602978 | 2.350e-05 | 7.450e-07 |
| 601 | 24.953949977949 | 24.953949964470 | 1.348e-08 | 5.498e-10 |
| 705 | 26.974530459553 | 26.974530450092 | 9.461e-09 | 3.563e-10 |
| 926 | 30.870319668204 | 30.870319664714 | 3.490e-09 | 1.147e-10 |
| 442 | 21.525482581390 | 21.525482579010 | 2.380e-09 | 1.132e-10 |
| 875 | 29.988197357494 | 29.988197354313 | 3.181e-09 | 1.076e-10 |
| 599 | 24.916816140207 | 24.916816137707 | 2.499e-09 | 1.021e-10 |
| 807 | 28.860408935860 | 28.860408933085 | 2.775e-09 | 9.767e-11 |
| 127 | 11.800829570323 | 11.800829569245 | 1.078e-09 | 9.567e-11 |
| 911 | 30.670688893665 | 30.670688890925 | 2.741e-09 | 9.080e-11 |
| 741 | 27.707243773679 | 27.707243771478 | 2.201e-09 | 8.087e-11 |
| 758 | 27.953986016121 | 27.953986014356 | 1.765e-09 | 6.410e-11 |
| 851 | 29.665313616296 | 29.665313614487 | 1.808e-09 | 6.199e-11 |
| 748 | 27.826710141126 | 27.826710139749 | 1.376e-09 | 5.033e-11 |
| 809 | 28.889721754318 | 28.889721753000 | 1.318e-09 | 4.635e-11 |
| 933 | 30.943865819814 | 30.943865818447 | 1.366e-09 | 4.473e-11 |
| 340 | 18.920975596329 | 18.920975595529 | 8.002e-10 | 4.340e-11 |
| 632 | 25.637038698794 | 25.637038698319 | 4.755e-10 | 1.891e-11 |
| 330 | 18.687652890045 | 18.687652889775 | 2.692e-10 | 1.482e-11 |
| 448 | 21.687501911902 | 21.687501911686 | 2.164e-10 | 1.022e-11 |
| 986 | 31.851742951826 | 31.851742951550 | 2.762e-10 | 8.797e-12 |

## What was scanned

### Kaggle kernels
- Full competition enumeration: **183 kernels** (sort `dateRun`, `scoreDescending`,
  `voteCount`, `dateCreated`, `hotness`, paged to exhaustion), plus broader
  `kernels_list(search=…)` sweeps (`squares in squares`, `square packing`,
  `squares`, `boxed in`, `fault dp`, `jammed squares`, …) → **2,418** raw refs,
  filtered to **210** genuinely relevant notebooks.
- Downloaded and screened the current output of ~50 notebooks, including every
  ref updated after 2026-11-13 and every fresh ref after 2026-11-16:
  `areebbb/squares-in-squares-the-last-1e-9`,
  `alexchilton/fault-line-dp-basin-hopping-lb-22-2620`,
  `alexchilton/squares-101-the-starter-kit-14-300-downloads`,
  `asteriospanoras/squares-22-134-play-with-boxes-best-public-lb`,
  `nilanjansaha123/s-in-s-certified-portfolio-merge-proj-quench`,
  `nilanjansaha123/certified-merge-projection-quench-gpu-screen`,
  `sigmaborov/squares-in-squares-certified-contact-polish`,
  `jazivxt/boxed-in-sub`, `penguin069/*` (all 8 unions/pilots),
  `malyshevdanil/squares-in-squares-living-atlas-of-tight-packings`,
  `kmmmvs/squares-public-merge-daily`, `seshurajup/1000-puzzles-ensemble-lb-22-2095`,
  `samanyu1808/sis-submit-v2-certified-search`,
  `pablodiegoo/squares-in-squares-starter-notebook`,
  `lucifer19/think-select-reclose`, `grennwolf/squares-in-squares-top-1-santa-2025`,
  `dedquoc/square-square-fast-numba-accelerated-simulated`,
  `pjmathematician/three-square-packings-that-beat-the-records`,
  `inversion/squares-in-squares-per-puzzle-leaderboard`, …
- `kernels_list(user=…)` sweep over 27 known participants (CLIST handle mapping
  in §"Team identities") and over the CLIST top-13 handles; only
  `pjmathematician`'s 3-packing notebook turned out to exist, and it is behind
  the bank (n=299 17.81329, n=260 16.64215, n=232 15.76378 — all worse).

### Kaggle datasets
- **406 datasets** enumerated via 11 search terms + 29 author names; **143**
  titles/references are square-packing related; the strongest **80** were
  file-listed and screened (submissions, `best_current.csv`, per-puzzle tables,
  batch diffs, `local_bank.csv`, portfolio bundles, research archive).
- Novel artifacts screened with no wins:
  `kmmmvs/squares-in-squares-private-packings` (`local_bank.csv`,
  `batch_1350_packing_coordinate_diff.csv`),
  `kmmmvs/squares-in-squares-best-packings`,
  `davidwarshawsky/squares-in-squares-research-archive` (11k files; 211
  `improvements.csv` / `packing_coordinate_diff.csv` re-screened),
  `rosswade/jammed-squares-engine-packings` (`engine_improvements.csv`),
  `asteriospanoras/squares-in-squares-best`, `jazivxt/boxed-in`,
  `cshara/squares-in-squares-current-best`,
  `shzgong/squares-in-squares-source-tracked-index` (1,030 candidate layouts),
  `alexchilton/squares-in-squares-starter-kit`,
  `prvsiyan/squares-auto-updater-live`, `lightningv08/squares-in-squares-layout-atlas`,
  `busyaprime/*`, `samanyu1808/sis-final-packings`, `avazaku/*`,
  `tecnicaaliena/squares-in-squares-literature-packings`, and 50+ more.

### GitHub / web
- `evand/square-packing` + `jlevy/squares` atlas: all **324** `known-best`
  witnesses (`reported_side` vs bank). **Zero** records beat the bank; the best
  raw diff was 6e-14 (serialization noise). Direct fetch of per-n rational
  witnesses was validated on `n-029`.
- `Shubin123/unitSquares`: **475** verified Kaggle packings (`data/kaggle/*.bin`,
  f64) + 6 GPU finds — 0 wins.
- `AHFE0924/Squares-Feeder/latest_public.csv` (auto-updated every 4 h from Kaggle
  top notebooks, 500,500 rows) — 0 wins.
- `TheSnakeFang/squarepack-certs`: 17 direct packings (n=308…814) + 230
  composites — all worse than bank (e.g. n=651 25.9915 vs bank 25.9425).
- `pjmathematician/three-square-packings-that-beat-the-records` (n=232/260/299)
  — all worse than bank.
- `chelokot/square-packing-archive`, `squaremath.org` atlas/case pages,
  Erich Friedman / David Ellsworth tables — side-only or already merged.
- GitHub repo sweep (12 repos found by `search/repositories?sort=updated`):
  `Samanyu-dev/squares_in_squares`, `Minuii/squares-in-squares`,
  `DigitalEuan/squares_in_squares`, `corentinlaudicina/SquaresInSquares`,
  `munimtechnologies/squares-in-squares-search`,
  `himkkkkkkkk/kaggle-square-in-square`, `dpre4ai/n90-square-packing`,
  `TobiasHFS/kaggle-squares-in-squares`, `Belloblaze-web3/...`,
  `cubres/...`, `omerfisler/...`, `anopheles/packingproblem` — every CSV
  screened; 0 wins. `corentinlaudicina` has only side-value tables.
- Kaggle **discussions**: all 33 topics + messages scanned for links; new refs
  `shzgong/squares-in-squares-source-tracked-index`, `AHFE0924/Squares-Feeder`,
  `cdeotte/squares-in-squares-l-cut-gpu-squeeze-22-39`, `jkaren/...`,
  `grennwolf/...` all screened.

### Local re-screening (no network)
- 626 cached candidate CSVs in `/tmp/frontier_agent` and `/tmp/frontier_watch_ds`
  were re-checked through the cheap numpy bbox screen; 211 `improvements.csv` /
  `packing_coordinate_diff.csv` files rebuilt into after-packings and screened.
  No wins beyond the bank.

## Team identities (from CLIST standings, used to target author sweeps)

`Cats and boxes 😼 = pjmathematician` · `VitalyR = vitalyankh` ·
`inspector gadget = grennwolf | tonylica` · `Chris Deotte = cdeotte` ·
`Sunstone North Lab = burtonlancaster` · `square1000 = naniwazu | physics0523 | kentoni…` ·
`Maika Namuo = maikanamuo` · `Nick Sarris = misfyre` · `shiv = sos54352` ·
`Nevska = nevska` · `Shadoks = gfonsecabr` · `William Toner = thunder12345`.

Sweeping all of their public kernels/datasets produced no unpublished packing
artifact. The top team's per-puzzle records are unpublished side-only leaderboard
entries (confirmed by the Squares Project issue threads, e.g. n=299 17.7936…).

## Negative findings worth recording

- Every full public submission screened (dozens) is a **subset/merge of the bank**:
  hundreds of identical-L groups, zero strictly better ones.
- `best_current.csv` (starter kit, 2026-11-17 17:06Z) had 4 real wins
  (n=127, 683, 751, 800, total +7.185e-6); the auto-pipeline merged them at
  17:18Z before we could — confirming the moving-frontier behaviour.
- `areebbb`'s "Last 1e-9" is the only recurring donor: its 16:58Z version gave
  +2.557e-7 (m1) and +2.072e-9 residual (m2); its **17:48Z re-run gave
  +1.1011e-5 (m3)** with four structural wins (n=549, 651, 932, 995) and 20
  micro-wins. Both uploads landed inside the moving-frontier window after a
  bank merge (16:15Z and 16:15Z respectively) and were downloaded within
  ~1–2 min of publication. Watch this ref every cycle.
- The kmmmvs `certified_mixed_components.csv` donor ledger (2,085 events) was
  parsed; every donor ref it names is either in the scanned set or deleted
  (`ntumlnoob/first-22-268681355-...` now returns 0 public kernels). Its own
  `submission.csv` (25.5 MB) is a strict subset of the bank.
- No candidate from any atlas/GitHub/literature source was within 1e-6 of the
  bank except the above.

## Polling (running)

`/tmp/campaign2/harvest/poll2.py` runs every **5 min** in the background
(`poll_loop.log`), re-lists competition kernels by `dateRun`, datasets by
`updated` for all search terms, and re-scans only changed/new refs. State is in
`state.json` (`kernel_meta`, `dataset_meta`, `candidates`). A companion
`automerge.py` runs after every poll: it re-screens the candidate pool against
the live bank, merges only if something beats the bank, full-scores both routes,
and updates `best.json` / `ledger.tsv` only when the score is strictly lower.
The loop caught the 17:48Z areebbb upload at 17:49Z and retried the
asteriospanoras RUNNING kernel until it completed.

**End-of-session status (18:28Z):** live bank `9c981e6e…` = **22.128441824807**
(optimisation track's 18:17Z merge), m4 = 22.129481982260582 is superseded as a
global best but was adopted by the bank at 18:12Z, so its +1.1011e-5 is live.
No candidate in the pool beats the 18:17Z bank. The poll/automerge loop is left
running; any further public upload that beats 22.128441824807 will be merged,
scored and appended to the ledger automatically.

## Kernel budget

**None used.** If a future cycle needs one (e.g. to run the per-puzzle leaderboard
notebook to refresh the record table), request 1 CPU kernel from the orchestrator.

## Files

- Best merged CSV: `/tmp/campaign2/harvest/merge_m4/submission.csv`
  (SHA-256 `19877e21aeb728221bbcb9fb53e3e47ac2dca027180f378b84c351aabfd8cf43`)
- Its official-metric report: `/tmp/campaign2/harvest/score_m4/report.json`
- Merge report: `/tmp/campaign2/harvest/merge_m4/merge_report.json`
- Earlier merges (superseded): `/tmp/campaign2/harvest/merge_m3/`,
  `/tmp/campaign2/harvest/merge_m2/`, `/tmp/campaign2/harvest/merge_m1/`
- Auto-merger: `/tmp/campaign2/harvest/automerge.py` (screens every 5 min,
  merges only when a candidate beats the live bank and the current best)
- Ledger: `/tmp/campaign2/harvest/ledger.tsv`
