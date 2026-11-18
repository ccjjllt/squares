# Frontier scout report — Squares in Squares

Scanned public Kaggle kernels/datasets for packings that beat the bank, since
**2026-11-16 06:00 UTC**. Work done in `/tmp/frontier_agent/`; `/tmp/best_bank`,
`/tmp/best_merge` and running pipelines were not modified.

Generated: **2026-11-17 ~09:35 UTC** (17:35 local).

## URGENT FLAG

**No candidate with net gain > 1e-3 was found.** The largest new certified gain is
**+2.280573e-4** (one puzzle, n=448). A second, certified-but-negligible gain
**+1.21e-13** (n=756, last-digit/rounding level) was also found.

## Headline findings

| # | Source (new run) | Artifact | Puzzle | Bank L | Candidate L (certified) | ΔL | Score gain | Certified merge report |
|---|---|---|---|---|---|---|---|---|
| 1 | `penguin069/squares-public-neural-recovery-union` (2026-11-17 07:32 UTC) | `effective_pandas_roundtrip.csv` | **448** | 21.692388155425210 | 21.6875610915765471985884… | 4.8271e-3 | **2.2805733e-4** | `/tmp/frontier_agent/merge_combined/merge_report.json` |
| 1b | `penguin069/squares-neural-recovery-certified-union` (2026-11-17 07:13 UTC) | `effective_pandas_roundtrip.csv` | 448 | same | same | same | same | same geometry as #1 |
| 2 | `cshara/squares-in-squares-current-best` (dataset, 2026-11-17 04:17 UTC) | `submission.csv` | 756 | 27.92112542377555 | 27.9211254237722196759… | 3.33e-12 | 1.2107e-13 | `/tmp/frontier_agent/merge_cshara/merge_report.json` |

Best combined artifact (bank at 09:11 UTC + #1 + #2):

- `/tmp/frontier_agent/merge_combined/submission.csv`
- SHA-256 `69b60e9b66530604f4c3fd3f1633e9f94f0626b8ebb58810d47b9fa2748f31c6`
- Score **22.13102364696328** (valid 1000/1000 in both `text` and `float64` modes)
- Net gain `2.280573305886e-4`; changed puzzles `[448, 756]`
- Full official-metric report: `/tmp/frontier_agent/merge_combined/report.json`
- Per-puzzle report: `/tmp/frontier_agent/merge_combined/per_puzzle.csv`

Winning candidate inputs (raw Kaggle downloads):

- `/tmp/frontier_agent/kernels/penguin069__squares-public-neural-recovery-union/effective_pandas_roundtrip.csv`
  SHA-256 `572a63a522059acdbf1256a83b0bf47670b3446c9b640a5e6f577a0b1d6cec07`
- `/tmp/frontier_agent/kernels/penguin069__squares-neural-recovery-certified-union/effective_pandas_roundtrip.csv`
  SHA-256 `2150007558c99e79635b13acf66a89dfee6721a3adcd963a3250e6ff601ddd53`
- Candidate with the required `id` column added (used for merge):
  `/tmp/frontier_agent/cand_penguin_neural.csv`
  SHA-256 `394d046ab67a75dd7a31786b69c8c1085db92e30f4ae670facbce4fb0d32458e`
- `/tmp/frontier_agent/datasets/cshara__squares-in-squares-current-best/submission.csv`
  SHA-256 `349dff6ad6de4b52214f7b88c2fa8a866da1c3321de2c9dc709a5683049df532`

Interpretation of #1: both neural-recovery kernels were built from the
`squares-four-birth-cpu-research` baseline; their overall local totals
(22.1337706 and 22.1345283) are *worse* than the bank, but n=448 is better.
That is exactly the case per-puzzle merging exists for.

Interpretation of #2: the 3.3e-12 L difference is float64 serialization noise on
the same packing family. The official metric does certify it, but it is not a
real optimization gain; do not treat it as a discovery.

## Bank drift during the scan (important)

The bank was updated by the main pipeline twice while this scan was running:

| When (UTC) | Bank SHA-256 (short) | Score | Bank report input |
|---|---|---|---|
| start (~07:25) | `a124696965be1af6…` | 22.131554120976524 | `/tmp/sub_frontier/merge_jazivxt_boxed-in-sub/submission.csv` |
| 08:55 | `a0cdef1fbf0f9759…` | 22.131262138211326 | `/tmp/sub_cpu/merge_fault_quench/submission.csv` |
| 09:11 (current at report time) | `9b0bcce13ddc7879…` | 22.131251704293867 | `/tmp/sub_cpu/merge_hop367/submission.csv` |

The n=448 win is absent from **all three** versions (verified by merge: the
candidate group is selected as `changed`, and current-bank merge report lists
`changed_puzzles: [448, 756]`). The cshara n=756 difference is absent from the
current bank only at the 1e-13 level.

Merges run against different bank snapshots:

- vs start bank: `/tmp/frontier_agent/merge_penguin_neural/` → 22.131326063646057
- vs 08:55 bank: `/tmp/frontier_agent/merge_penguin_neural_curbank/` → 22.13103408088086
- vs 09:11 bank (final, recommended): `/tmp/frontier_agent/merge_combined/` → **22.13102364696328**

## Method

Per-puzzle L was computed from each candidate as the official metric does:
for each unit square, half-extent `h = (|cos a| + |sin a|)/2`; L is
`max(max_x - min_x, max_y - min_y)` over all corners of all n squares.
Comparison against the bank used `EPS = 1e-12` on L. Groups with row count ≠ n
were treated as incomplete and excluded (this matters: shard files in some
archives contain split groups that produce fake tiny L values).

Commands used (abridged):

```bash
export KAGGLE_API_TOKEN=$(cat ~/.kaggle/access_token_ccjjllt_check)
K=.venv/bin/kaggle

$K kernels list --competition squares-in-squares --sort-by dateRun --page-size 100 --csv
$K kernels output <ref> -p /tmp/frontier_agent/kernels/<tag>
$K datasets list --search squares-in-squares --sort-by updated --page-size 100 --csv
$K datasets download <ref> -p /tmp/frontier_agent/datasets/<tag> --unzip

# per-puzzle comparison
.venv/bin/python /tmp/frontier_agent/compare.py /tmp/best_bank/submission.csv <candidate.csv>

# certification
.venv/bin/squares merge --baseline /tmp/best_bank/submission.csv \
  --baseline-report /tmp/best_bank/report.json \
  --candidate /tmp/frontier_agent/cand_penguin_neural.csv \
  --candidate /tmp/frontier_agent/datasets/cshara__squares-in-squares-current-best/submission.csv \
  --output-dir /tmp/frontier_agent/merge_combined --workers 4
```

Key output snippets:

```
bank puzzles=1000 score=22.131262138211298
kernels/penguin069__squares-public-neural-recovery-union/effective_pandas_roundtrip.csv
  rows=500500 n=1000 wins=1 gain=0.000228057
   n= 448 bank=21.692388155425210 cand=21.687561091576548
            d=4.827e-03 gain=2.281e-04 rows=448
```

```
merge_combined/merge_report.json
  "changed_puzzles": [448, 756]
  "net_gain": {"text": 0.00022805733058861577,
               "float64": 0.00022805733058861577}
  "score":    {"text": 22.13102364696328,
               "float64": 22.13102364696328}
merge_combined/report.json
  input sha256 69b60e9b66530604f4c3fd3f1633e9f94f0626b8ebb58810d47b9fa2748f31c6
  text    score 22.13102364696328 valid 1000 invalid 0 missing 0
  float64 score 22.13102364696328 valid 1000 invalid 0 missing 0
```

## Coverage: every source tested

Files: `/tmp/frontier_agent/scan_results_all.json` (217 unique candidate files,
SHA-256 deduplicated; 0-gain sources included). Data dirs: `kernels/`,
`datasets/`, plus `amir_v43/44/45` and `npz_ga_contact_input_0.csv`.

### A. Kernels with lastRunTime ≥ 2026-11-16 06:00 UTC

| Kernel | lastRun (UTC) | Files tested | Rows (max) | Puzzles | Wins | Best gain |
|---|---|---|---|---|---|---|
| `jazivxt/boxed-in-sub` | 11-17 06:31 | 1 | 500500 | 1000 | 0 | 0 |
| `amirhezekiahespanto/debut-top-150-22-13x-v45` | 11-17 05:46 (still RUNNING) | v43, v44, v45 outputs | 500500 | 1000 | 0 | 0 |
| `alexchilton/squares-101-the-starter-kit-14-000-downloads` | 11-17 04:28 | 1 | 500500 | 1000 | 0 | 0 |
| `kmmmvs/squares-public-merge-daily` | 11-17 03:56 and 08:27 | 1 (identical SHA both runs) | 500500 | 1000 | 0 | 0 |
| `alexchilton/fault-line-dp-basin-hopping-lb-22-2620` | 11-17 03:05; re-run 09:10 in flight | 2 (submission=merged) | 500500 | 1000 | 0 | 0 |
| `asteriospanoras/squares-22-134-play-with-boxes-best-public-lb` | 11-17 01:28 | log only (scores a dataset; writes no submission) | — | — | 0 | 0 |
| `nilanjansaha123/s-in-s-certified-portfolio-merge-proj-quench` | 11-17 00:20, re-run 07:35 | 1 | 296974 | 557 | 0 | 0 |
| `nilanjansaha123/certified-merge-projection-quench-gpu-screen` | 11-17 00:17, re-run 07:50 | 1 | 296974 | 557 | 0 | 0 |
| `inversion/squares-in-squares-per-puzzle-leaderboard` | 11-16 21:03 | log only | — | — | 0 | 0 |
| `nevska/squares-in-squares-explorer` | 11-16 18:56 | `public_frontier.csv` (1000 sides, no coordinates) | — | 1000 | 0 | 0 |
| `samanyu1808/sis-submit-v2-certified-search` | 11-16 18:45 | 1 | 500500 | 1000 | 0 | 0 |
| `penguin069/squares-certified-recovered-grain-union` | 11-16 18:42 | 1 (`effective_pandas_roundtrip.csv`) | 500500 | 1000 | 0 | 0 |
| `lucifer19/think-select-reclose` | 11-16 18:04 | 34 (`submission.csv` + v24…v57 anchors) | 500500 | 1000 | 0 | 0 |
| `areebbb/squares-in-squares-merge-28-certify-shrink` | 11-16 16:02 | 1 | 500500 | 1000 | 0 | 0 |
| `pablodiegoo/squares-in-squares-starter-notebook` | 11-16 15:34 | 1 | 500500 | 1000 | 0 | 0 |
| `grennwolf/squares-in-squares-top-1-santa-2025` | 11-16 13:38 | log only | — | — | 0 | 0 |
| `seshurajup/1000-puzzles-ensemble-lb-22-2095` | 11-16 13:16 | 1 | 500500 | 1000 | 0 | 0 |
| `penguin069/squares-ga-contact-certified-current-union` | 11-16 12:47 | 4 (`submission.csv`, effective CSV, decoded NPZ submission, checkpoint ZIP) | 500500 | 1000 | 0 | 0 |
| `malyshevdanil/squares-in-squares-living-atlas-of-tight-packings` | 11-16 07:14 | 3 | 500500 | 1000 | 0 | 0 |
| **`penguin069/squares-neural-recovery-certified-union`** | **11-17 07:13** | **1** | **500500** | **1000** | **1** | **2.280573e-4** |
| **`penguin069/squares-public-neural-recovery-union`** | **11-17 07:32** | **1** | **500500** | **1000** | **1** | **2.280573e-4** |

### B. Datasets updated ≥ 2026-11-16 06:00 UTC

| Dataset | lastUpdated (UTC) | Files tested | Rows (max) | Puzzles | Wins | Best gain |
|---|---|---|---|---|---|---|
| `alexchilton/squares-in-squares-starter-kit` | 11-17 04:27 | 3 | 500500 | 1000 | 0 | 0 |
| **`cshara/squares-in-squares-current-best`** | **11-17 04:17** | **2** | **500500** | **1000** | **1** | **1.2107e-13** |
| `asteriospanoras/squares-in-squares-best` | 11-17 01:27 | 1 | 500500 | 1000 | 0 | 0 |
| `kmmmvs/squares-in-squares-private-packings` | 11-16 23:06 | 45 (incl. `public_source_update_20261116_2150`, `portfolio_bundle`, `local_bank.csv`) | 500500 | 1000 | 0 | 0 |
| `romywicaksono/squares-pipeline` | 11-16 21:22 | 1 | 500500 | 1000 | 0 | 0 |
| `nevska/squares-in-squares-explorer-files` | 11-16 18:56 | viewer/cache/frontier files; no submission or coordinates | — | — | 0 | 0 |

Excluded as unrelated after listing their files: `astridvillalobos/daily-machine-learning-practice`
(a generic ML notebook), `carsonrodrigues/kaggle-medal-line-tracker` (medal tables).

### C. Explicitly requested checks + extra competition datasets

| Dataset | Version checked | Result |
|---|---|---|
| `busyaprime/squares-in-squares-fq-quenched-packings` | 11-11 12:05 | `packings.csv` covers only 26 n; 0 wins |
| `samanyu1808/sis-final-packings` | 11-14 20:46 | `submission.csv`; 0 wins |
| `lostdecimal27/squares-in-squares-bank` | last updated 10-29; no new version | bank's 11-16 copy already absorbed; nothing new |
| `avazaku/squares-contact-lp-cusp-bounds-465-998` | 11-15 19:35 | 6 files; 0 wins |
| `tecnicaaliena/squares-in-squares-literature-packings` | 11-15 19:35 | 0 wins |
| `mzishran/squares-in-squares-merged-packings-1000-puzzles` | 11-13 | 0 wins |
| `prvsiyan/squares-verified-best-of-1105` | 11-13 | 0 wins |
| `davidwarshawsky/squares-in-squares-research-archive` | 11-13 | 91 CSVs incl. `harvest10_stage/certified_wins.csv`; 0 wins |
| `jonathan1506/joegun-squares-packings` | 11-13 | 0 wins |
| `lucifer19/think-select-reclose-v52-certified-snapshot` | 11-13 | zlib geometry snapshot; v52 anchor already tested (0 wins) |
| `penguin069/squares-gpu-glide-replay-data` | 11-14 | `baseline_submission.csv`; 0 wins |
| `jazivxt/n90-square-packing-certificate` | 11-15 | n=90 L=9.99827717 vs bank 9.99403877 (worse) |

## Evidence and negative results

1. **amirhezekiahespanto/debut-top-150-22-13x-v45** is still running at report
   time. Versions 43/44/45 were downloadable and tested:
   v43 22.146935, v44 22.146213, v45 22.136777 — all **0 wins**. A newer run,
   if it completes after this report, is not covered.
2. **alexchilton/fault-line-dp-basin-hopping-lb-22-2620** re-ran at 09:10 UTC
   and is still running; the available outputs (03:05 version) are **0 wins**.
3. **penguin069/squares-certified-recovered-grain-union** does not publish
   `submission.csv` in its output list. Its `effective_pandas_roundtrip.csv`
   was tested (0 wins). The missing submission was recovered from
   `kmmmvs/squares-in-squares-private-packings/public_source_update_20261116_2150/sources/145454497/v1/submission.csv`
   (SHA `1e59f4b69df3…`, matching the kernel's declared submission SHA) and also
   tested: **0 wins**.
4. `penguin069/squares-whole-grain-tpu-data` (source bundle referenced by the
   recovered-grain kernel) is private: download returns "You don't have access
   to this resource".
5. The two neural-recovery kernels' output contains only
   `effective_pandas_roundtrip.csv` (no plain `submission.csv`). That CSV is
   the serialized submission (verified for the sibling `ga-contact` kernel:
   effective vs `submission.csv` differ by ≤7.1e-15), so it is a valid input.
6. Shard files in `davidwarshawsky`'s archive (e.g. `parts/wins_*_partN.csv`)
   initially look like large wins, but they are row-splits of a larger file;
   per-n groups are incomplete. After requiring `rows_per_n == n`, all archive
   files are **0 wins**. This trap is documented so nobody re-reports it.
7. All winners were checked against the current bank snapshot (09:11 UTC) and
   still merge as `changed` groups.

## Artifact index

| Path | SHA-256 | What |
|---|---|---|
| `/tmp/frontier_agent/cand_penguin_neural.csv` | `394d046ab67a75dd7a31786b69c8c1085db92e30f4ae670facbce4fb0d32458e` | n=448 candidate with `id` column, merge input |
| `/tmp/frontier_agent/merge_combined/submission.csv` | `69b60e9b66530604f4c3fd3f1633e9f94f0626b8ebb58810d47b9fa2748f31c6` | best merged output (22.13102364696328) |
| `/tmp/frontier_agent/merge_combined/merge_report.json` | — | per-puzzle merge decisions/evidence |
| `/tmp/frontier_agent/merge_combined/report.json` | — | full official v20 score, text+float64 |
| `/tmp/frontier_agent/merge_penguin_neural_curbank/` | — | penguin-only merge vs 08:55 bank |
| `/tmp/frontier_agent/merge_cshara/` | — | cshara-only merge (22.131251704293746) |
| `/tmp/frontier_agent/scan_results_all.json` | — | all 217 tested files, SHA, wins, gains |
| `/tmp/frontier_agent/compare.py`, `run_scan.py` | — | comparison code used |

## Bottom line

- **New public find:** `penguin069/squares-public-neural-recovery-union` /
  `penguin069/squares-neural-recovery-certified-union`, n=448, certified
  **+2.280573e-4** score.
- **No source exceeding 1e-3**; nothing warranting the urgent label by the
  requested threshold.
- The cshara n=756 “win” is real to the official metric but only +1.21e-13;
  ignore it as noise.
- Recommend merging `/tmp/frontier_agent/cand_penguin_neural.csv` into the
  bank (or taking `/tmp/frontier_agent/merge_combined/submission.csv` if the
  bank is still at SHA `9b0bcce1…`).
