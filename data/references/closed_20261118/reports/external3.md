# External harvest, round 3 — new sources for n = 200…1000

Date: 2026-11-18. Subagent track: non-Kaggle catalogues, new Kaggle artefacts,
GitHub/GitLab/HuggingFace, papers, personal pages.

**Bank untouched:** `/tmp/best_bank/submission.csv` SHA-256
`9c981e6ea9a44c076587256936948e636936a84ad0668af6b75e946f4fa527e9`,
score `22.128441824806618` (`text`) / `22.12844182480662` (`float64`), 1000/1000 valid,
re-verified at the end of this round. No file under `/tmp/best_bank/` was modified.
Nothing was submitted to Kaggle.

---

## TL;DR

**Zero certified wins. Zero strict decreases at any n under a 1e-12 margin.**

More than **60,000 new puzzle groups** with coordinates were parsed this round, including
several corpora that had never been imported:

| corpus | groups | result |
|---|---:|---|
| `chaydavs` portfolio v5 (npz) | 1,000 | 0 wins (exact ties at 902/903/963/964) |
| `bestbryant/…/solutions/*.npy` | 557 | 0 wins (closest is a tie) |
| `Shubin123/unitSquares/data/kaggle/*.bin` | 475 | 0 wins (closest −4.6e-9, i.e. behind) |
| `leeyoung9527/…/dp_donors.npz` | 820 | 0 wins |
| `davidwarshawsky/…research-archive` batch certifications | 19 × 1,000 | 0 wins (batch scores 22.2559–22.2650) |
| `yugavka/…/published_sources` | 29 CSVs | 0 wins |
| Kaggle post-11-11 datasets/kernels (full submissions) | ~20 × 1,000 | 0 wins |
| Mishapolk-style exact certificates from new contributors | 70+ files | 0 wins (bank equal or better) |

The closest anything came was **4.3e-9 behind** the bank (Ono's exact `n=228` certificate)
and **2.6e-12 behind** (Ozden's `n=179`); several sources tie the bank to ≤1e-14.
There is therefore **no merge directory and no dual-route score for this track**: there
was nothing to merge. The bank remains the pointwise minimum of every public coordinate
corpus tested.

---

## 1. Method and conventions

For every candidate file:

1. Parse n and the square list. Three coordinate conventions occur and were all handled:
   - Kaggle CSV: rows `n, square_id, x, y, angle` with **centres** and **angle in radians**;
   - certificate: header `n S` then `x y t` with **centres** and `t = tan(θ/2)`;
   - atlas / JSON: **corners** (exact rationals), or centres with **degrees**.
2. Reconstruct all four corners of every unit square and compute

   `L = max(max_x − min_x, max_y − min_y)`

   over the true rotated corners — **not** `max(x)−min(x)+1` on centres. This matters:
   the naive centre formula produces a false `n=597` "win" of +3.9e-2 on
   `tecnicaaliena/…literature-packings`, which vanishes once rotation is applied.
3. Compare with the bank's per-puzzle `L` from
   `/tmp/best_bank/report.json → runs.text.per_puzzle` (decimal string, parsed to float
   only for comparison; the bank is self-consistent at 3.6e-15).
4. A win is declared only if `L_candidate < L_bank − 1e-12`. Anything inside 1e-12 is
   float64 noise of the same packing (bank self-comparison produces exactly this band).

Angle unit is per source: Kaggle-format CSVs and the metric are radians; the
`jonathan1506` `layouts.json` and `dpre4ai` `n90.csv` are degrees and were converted;
certificates use the half-tangent. 90° rotations are treated as equivalent when checking
a diff against the bank (a square rotated by π/2 is the same square).

---

## 2. Source ledger

### 2.1 Catalogues / classical pages

| # | Source | URL | What it contains | Coords? | Coverage | Result |
|---|---|---|---|---:|---|---|
| C1 | Packomania / E. Specht | `https://www.packomania.com/` | index parsed: circles in square/circle/rect/triangle/polygons, spheres, 4D/5D/6D hyperspheres, bidisperse catalogues. **No square-in-square section** | none | — | nothing to import |
| C2 | Magdeburg mirror | `https://hydra.nat.uni-magdeburg.de/packing/` | connection timeout (40 s, twice). Packomania index is the same catalogue and has no squares | none | — | nothing |
| C3 | Walter Trump personal site | `www.walter-trump.de` (many variants) | DNS does not resolve; `web.archive.org` and `archive.org` unreachable from this environment | — | n ≤ 11 historically | Trump's n=11 packing is the proven optimum already in the bank (`3.877083590022814…`); no n ≥ 200 material exists on that page |
| C4 | The Squares Project (website) | `https://squaremath.org/` | page alias JSON lists cases **1…324 only**; `sitemap.xml` 404 | 1–324 | 1–324 | round-1 already imported; no n>324 witness exists on the site |
| C5 | The Squares Project (repo atlas) | `github.com/jlevy/squares` `packing/atlas/known-best/` | 324 rendering + 198 regularized files, all n ≤ 324; `bound-citations.json` is side-only | 1–324 | 1–324 | 0 new |
| C6 | jlevy `resources/web/` external archive | same repo, 200+ dated packets | exact certificates/poses for Ono, de Winter, Yim, Ozden, Lara, Joost, Khalili, JoGoon, etc. | yes | 90–992 | **0 wins**; see §2.3 |
| C7 | OEIS | `oeis.org` | queries: “unit squares packing”, “squares in a square”, A005842, A092137, A003059, A374528, A360610. A005842 is the *distinct consecutive squares* problem; all sequences are integer-valued, no sequence carries non-integer record sides and none carries coordinates. A374528 links a PDF of **squares-in-circles** data, not squares-in-squares | none | — | nothing |
| C8 | Friedman packing pages | `erich-friedman.github.io/packing/squinsqu/` | 154-byte redirect to Kingbird; no data files (no zip/csv/dat) | n ≤ 100 | — | Kingbird already imported (round 1) |
| C9 | MathPuzzle (Ed Pegg) | `mathpuzzle.com` | square-packing page is 2003 tiling/distinct-square material; no n≥200 coordinates | none | small n | nothing |
| C10 | David Ellsworth tools | `github.com/Davidebyzero/packing_squares_in_squares__tools` | 30 KB, 4 files: parser, refiner, 45° enumerator, checker. **No stored packings** | code only | — | nothing |

### 2.2 Papers, preprints, data repositories

| # | Source | What it contained | Coords for n ≤ 1000? | Result |
|---|---|---|---|---:|
| P1 | Karimi, *Structure-Guided Search…*, preprints.org **202611.0242** (DOI 10.20944/preprints202611.0242.v1) | direct fetch 403 (Akamai); full abstract/data statement recovered via OpenAlex and jlevy issue #847. Data statement: filled-end records **5134 rows, n = 1182–9946**; earlier two-band records **5308 rows** | **no** (min n 1182) | out of range |
| P2 | Karimi Zenodo records 23681704 / 23624432 (+ GitHub `mohsensbu-jpg/*`) | `filled_records.csv` 5134 rows, min n 1182; `records.csv` from the two-strip zip also min n 1182 | **no** | out of range |
| P3 | Zenodo 23165915 / GitHub `squarepacker/k2-minus-c` | theorem `s(k²−c)=k` for every fixed c and large k; explicit bound only `k²−N ≥ 0.0353 log k`. Experiments are 7/9-square local gadgets, not n≤1000 packings | no usable general construction | bank already has `L=k` exactly for all `n=k²−c`, c ≤ 23 at k=30 |
| P4 | Zenodo 23463480 (Fang), 23624411/23624432 (Fang/Karimi), 24099177 (lower bounds), 23853803 (point-cover checker) | `s(n²−n+1)<n`, two-strip/theory, lower bounds | all n ≥ 1182 or theorem-only | nothing |
| P5 | OpenAlex sweep, `from_publication_date:2025-01-01`, 50 newest | 2026 items: Karimi ×2, Fang, Bui/McClenagan asymptotics, axis-parallel n=7/8 exact formulas, “5/9 theorem”, square-in-rectangle, sphere-in-square, dynamic bin packing | none carries finite-n packing coordinates for 200 ≤ n ≤ 1000 | nothing |
| P6 | arXiv API `all:"packing unit squares"`, newest 40 | 2609.37410 (rectangle bound), 2412.21017, 2404.09835, 1603.02368; plus 2610.22622 / 2610.28504 (axis-parallel n=7,8) | none | nothing |
| P7 | HAL API | 1 hit: 2012 thesis on packing/colouring, no unit-square coordinate table | no | nothing |
| P8 | OSF / figshare | OSF API non-JSON/HTP error; figshare 403 (both already blocked in round 2) | — | unreachable |
| P9 | Zenodo “squares packing” newest | API rejected multi-term queries with HTTP 400; single-term pages returned only unrelated records; the relevant records were reached via OpenAlex above | — | nothing new |

### 2.3 Recent exact-certificate contributors (via jlevy archive / their repos)

All were parsed from exact rationals and converted to true rotated bboxes.

| contributor | n | source side | bank L | verdict |
|---|---:|---:|---:|---|
| Roberto Ono, `n228.strict.cert` | 228 | 15.596043120920791 | 15.596043116631693 | bank better 4.29e-9 |
| Roberto Ono, `n147.strict.cert` | 147 | 12.651043556587695 | 12.651043553172650 | bank better 3.42e-9 |
| Joost de Winter, issue #996 | 90 | 9.994038857546 | 9.994038766582889 | bank better 9.10e-8 |
| Kaelan Yim, 14 exact certs | 130, 299, 303, 553, 599, 600, 601, 602, 604, 645, 647, 648, 699, 700 | 11.902430645982…, … | — | 0 wins; n=130 bank better 2.1e-13, n=303 bank better 1.2e-13; all others behind 4.1e-3…2.1e-2 |
| Ozden (kenaznia-doga), 14 candidate YAML/JSON | 156, 172, 179, 180, 199, 204, 228, 232, 237, 268, 269, 270, 292, 299, 303, 307 | exact corners | — | 0 wins; several ties at ≤3.4e-12; n=179 bank better 2.6e-12, n=292 bank better 8.8e-5, n=269 bank better 1.1e-2 |
| Miguel Lara, `square-s977` | 977 | 31.85 (17+21/√2) | 31.742554234195 | behind 1.07e-1 |
| Joost Aug-2026 report (n=68,126,206; no coords released) | 68, 126, 206 | 8.80219, 11.77474, 14.87222 | 8.79880, 11.74264, 14.86016 | all behind 3.4e-3…3.2e-2 |
| Hyukdong Kim `s297` exact field | 297 | 17.740417287544 | 17.739455558289 | behind 9.6e-4 |
| JoGoon (issue #1001) | 127, 204, 232, 264, 305 | exact | — | round-1 already showed bank better; unchanged |
| Khalili/Gharabaghi `s(k²−5)=k`, `moh63-dev/k2m5-family` | k²−5 | k | k exactly | 0 wins, exact tie at k=15…31 |

### 2.4 Kaggle datasets (including everything updated after 2026-11-11)

| dataset | files inspected | contents | result |
|---|---|---|---:|
| `udishiken/square-in-square-22-26` **v2** | **all 3**: `perpuzzle_best.csv` (side-only, n,L,team,date), `targets.csv` (676 rows, `n,K,D,f_ours,f_best,gap`), `submission.csv` (25.6 MB) | full coordinates only in submission | submission: **0 wins**; targets: 676 side-only targets, 370 with `K+f_best < bank L` — no coordinates |
| `cshara/squares-in-squares-current-best` (11-17) | `best_submission.csv`, `submission.csv` | full submissions | 0 wins both |
| `rosswade/jammed-squares-engine-packings` (11-17) | `engine_improvements.csv` (77 puzzles), `per_puzzle_best.csv` (side-only) | coordinate diffs, true-rotation bbox | 0 wins |
| `alexchilton/squares-in-squares-starter-kit` (11-17) | `best.csv`, `best_current.csv`, `couzo.csv`, `couzo_big.csv`, `hop.csv`, `quench.csv`, code | full + partial | 0 wins in every file |
| `tecnicaaliena/squares-in-squares-literature-packings` (11-15) | `submission.csv`, `puzzle_scores.csv`, attribution | **angles in radians** | 0 wins (naive centre bbox falsely suggests n=597; see §3) |
| `samanyu1808/sis-final-packings` (11-14) | `submission.csv`, per-puzzle table | full submission | 0 wins |
| `mzishran/…merged-packings-1000-puzzles` (11-13) | `merged_submission.csv` | full submission | 0 wins |
| `jonathan1506/joegun-squares-packings` (11-13) | `submission.csv`, 15 JSONs incl. `layouts.json` (8 coordinate layouts, degrees), side table | full + layouts | 0 wins |
| `romywicaksono/squares-pipeline` (11-16) | `submission_best.csv`, code | full submission | 0 wins |
| `davidwarshawsky/squares-in-squares-research-archive` (11-13) | all 19 `*_full_certification.json` + 1 coordinate diff + manifest + component table | kmmvs-style private portfolio, base = malyshev-v32 | **0 wins in all 19 batches** (scores 22.2559–22.2650) |
| `leeyoung9527/sis-public-dp-donors-20261113` | `dp_donors.npz` (poses 353,061×3, lengths, labels), `sources.json` | 820 donor packings (816 with n≤1000) | 0 wins |
| `mdmuqtadirfuad/sis-certified-portfolio` | `portfolio.csv` | 553 puzzle groups | 0 wins |
| `ruoxuanzhuang/…two-fault-dp-packings` | `packings.csv` | n=744, 978 | 0 wins |
| `busyaprime/squares-in-squares-fq-quenched-packings` | `packings.csv`, logs | 26 groups | 0 wins |
| `penguin069/squares-gpu-glide-replay-data`, `…boxed55-certified-inputs-20261115` | `baseline_submission.csv` (full), manifests | public unions | 0 wins both |
| `asteriospanoras/squares-in-squares-best` (11-17) | full submission, already scanned in round 2 | full | 0 (round 2: 0 at all 16 targets and pointwise at all 1000) |
| `kmmmvs/squares-in-squares-private-packings` (11-17) | do-not-revisit per brief (407 MB bundle) | full | exhausted in round 1/2 |
| `prvsiyan/squares-verified-best-of-1105` (11-13) | round-2 merge produced **the same SHA as the bank** | full | 0 |
| `avazaku/…`, `lomnafsk/sis-ga-payload`, `jazivxt/n90-…` | code or single-n | — | 0 (n=90 is 9.998277, behind bank 9.9940388) |

### 2.5 Kaggle kernels (new/updated after 2026-11-11)

Outputs pulled and compared in full (true rotated bbox, 1e-12 margin):

| kernel | result |
|---|---:|
| `nilanjansaha123/its-a-secret` (556 puzzles) | 0 wins |
| `tomkodaj/squares-in-squares-22-1636` | 0 wins |
| `adityasingh157735/unit-square-packing-octagonal-45-cavity-solver` | 0 wins |
| `dedquoc/square-square-fast-numba-accelerated-simulated` | 0 wins |
| `woshichenyanyan/notebook074c5de1fd` | 0 wins |
| `penguin069/*` certified-union kernels (11-14…11-17) | public unions; pull aborted on size after 120 s; their input datasets' baselines were compared (0 wins) and round 2 already proved public unions cannot beat the bank pointwise |
| `nevska/squares-in-squares-explorer` | viewer only; `viewer_cache.json` holds per-cell rendering (`cells`, `overlaps`, `costs`), not packing coordinates |

### 2.6 GitHub / other code hosts

| repository | contents | result |
|---|---|---:|
| `larasmiguel/square-s977` | `n977_coordinates.csv` (977 squares, radians), exact construction + checker | 0 (31.85 vs bank 31.74255) |
| `RobertoOno/squares-in-square` | exact certs n=147, 228; n≤228 only | 0 (bank better by 3.4e-9 / 4.3e-9) |
| `bestbryant/claude_code_squaresinsquares` | **557 `solutions/n*.npy`** (n=5…999) + full `submission.csv.gz` | 0 wins; many exact ties |
| `Shubin123/unitSquares` | **475 `data/kaggle/n*.bin`** float64 (x,y,angle) | 0 wins; closest −4.6e-9 (n=26) |
| `yugavka/square_in_squares` | 29 `published_sources/*.csv.gz` including ntumlnoob, alexchilton delta, az0519…, packer_bneck, couzo/evand certs | 0 wins in all 29 |
| `DigitalEuan/squares_in_squares` | 5 full submissions (11-15) | 0 wins |
| `Minuii/squares-in-squares` | `submission_final.csv` | 0 wins |
| `moh63-dev/k2m5-family` | proof + Lean; `s(k²−5)=k` | exact ties at k=15…31 |
| `squarepacker/k2-minus-c` | proof + local gadgets (7/9 squares) | no full packings |
| `dpre4ai/n90-square-packing` | n=90 exact construction | 9.998277 vs bank 9.9940388 |
| `munimtechnologies/squares-in-squares-search` | pre-registered search, code only | no data |
| `TobiasHFS/kaggle-squares-in-squares`, `corentinlaudicina/SquaresInSquares` | generators/runner, no saved packings | no data |
| `raojohng/squares-in-squares` | interactive atlas n=1…6 | n≤6 |
| `anopheles/packingproblem` | Kingbird viewer, fetches SVGs at runtime | duplicate of C/round 1 |
| `wand125/square-packing` | 111 MB Lean proofs for squares-in-**triangles**, plus `tools/transfer/data/ub.json` | not this problem |
| `0100001001101111/aletheia-packing-records` | withdrawn **circle**-packing claims (n=600/700/800 circles) | not this problem |
| `HyukdongKim/square-packing-exact-sides` | exact s(297)=17.740417… | behind bank |
| `RobertBarnettProjects/square-packing-research` | superseded certs n=70,103,123,129,146,237,295 | superseded; bank better |
| `Ge-limin/math` | subspace packings (Grassmann), 719 manuscripts | not this problem |
| `muellan/packing/min-Square(Square)` | side tables n≤100 for non-unit squares (`hi=1`, `hi=i`) | different problem, no coords |
| GitLab API `search=square packing` | 2 repos: a Python toy (2019), a Firefox theme | nothing |
| Codeberg / SourceForge / Bitbucket | 429 rate-limit / 403 / 404 | unreachable |
| HuggingFace | DNS → `103.214.168.106`, TCP 443 refused; `hf-mirror.com` 502; no datasets could be listed | **blocked**, no data obtained |
| GitHub code search | `api.github.com/search/code` → 401 “Requires authentication”; no `GITHUB_TOKEN`/`gh`; after ~100 contents reads the API also returned 60/h rate-limit and abuse-detection responses | **coverage gap**, same as round 2 |

---

## 3. Near misses and traps (for the next round)

Closest things to a win, all validated as *behind*:

| n | source | candidate L | bank L | bank − candidate |
|---:|---|---:|---:|---:|
| 228 | Ono exact cert | 15.596043120920791 | 15.596043116631693 | **+4.29e-9** |
| 147 | Ono exact cert | 12.651043556587695 | 12.651043553172650 | **+3.42e-9** |
| 26 | Shubin `.bin` | bank + 4.63e-9 | 5.82842712675… | −4.63e-9 |
| 90 | de Winter #996 | 9.994038857546 | 9.994038766582889 | +9.10e-8 |
| 179 | Ozden exact | 13.880960371558224 | 13.880960371555620 | +2.60e-12 |
| 307 | Ozden exact | 17.979230960387362 | 17.979230960383962 | +3.40e-12 |
| 130 | Yim exact | 11.902430645982246 | 11.902430645982033 | +2.13e-13 |
| 303 | Yim exact | 17.901789273153195 | 17.901789273153078 | +1.17e-13 |

The pattern is consistent: where a public contributor is within 1e-8…1e-13 of the bank,
the bank holds a *slightly tighter polished version of the same packing*. There is no
topological novelty left in the public corpus at these n.

Traps worth recording:

1. **Radians vs centre-bbox.** `tecnicaaliena/…literature-packings` explicitly stores
   angles in **radians**. Computing `max(x)−min(x)+1` on centres (ignoring rotation)
   reports a fake win at `n=597` of `+3.933e-2`. Using the true rotated corners gives
   **0 wins**. Any future importer must use corner bbox; this source alone would generate
   a large false positive.
2. **Degrees.** `jonathan1506/joegun` `layouts.json` and `dpre4ai/n90.csv` use **degrees**.
   Converting them as radians makes the bbox wrong and can hide or invent wins.
3. **π/2 equivalence in diffs.** `davidwarshawsky` coordinate diffs store `before_angle`
   in radians and use π/2 where the bank stores 0; compare angles modulo π/2 when
   reconstructing. Its base is **malyshev-v32**, not the bank, so a naive row-replacement
   reconstructs the wrong packing for most groups (1 checked / 33 skipped). The full
   certification files are the authoritative per-puzzle list; all 19 batches are behind.
4. **Duplicate corpora.** `chaydavs/portfolio_v5.npz`, `Shubin123/data/kaggle/*.bin` and
   `bestbryant/solutions/*.npy` largely overlap (same public Kaggle donors). Do not
   double-count them as independent evidence.
5. **Side-only targets.** `udishiken/targets.csv` is a useful *target* table (676 n,
   370 with `K+f_best < bank L`), but it is side-only. It confirms the round-2 finding:
   the remaining gap is in the Kaggle per-puzzle leaderboard, not in any public artefact.

---

## 4. Why the result is a genuine negative, not a failed sweep

For every new full corpus this round, the check was not only “does it beat the 16
targets” but “does it beat the bank at **any** n”. The strongest form:

- `chaydavs` 1,000 groups: 0 wins, exact ties at 902, 903, 963, 964 (target n!).
- `Shubin123` 475 groups: 0 wins; best is 4.6e-9 *behind*.
- `bestbryant` 557 groups: 0 wins, many ties.
- `leeyoung` 816 groups: 0 wins.
- `davidwarshawsky` 19 full certifications: 0 wins at all 1,000 n each.
- `yugavka` 29 source CSVs (including ntumlnoob and alexchilton deltas that were not in
  round 1's 38-source list): 0 wins.
- Kaggle 11-11…11-18 artefacts: 0 wins.

So the bank is the pointwise minimum not just of the sources round 1/2 imported, but of
these newly discovered coordinate corpora as well. The 16 high-value gaps remain a
private-search problem.

---

## 5. Hard do-not-revisit list (round 4)

Do **not** re-download, re-parse or re-check any of the following; each was fully parsed
this round (or in round 1/2 and re-confirmed here):

**Catalogues / pages**
- `packomania.com` (Specht) and the Magdeburg mirror — no square-in-square data at all.
- `walter-trump.de` (dead) and archive.org copies — n≤11 only; Trump's packing is the
  proven bank optimum.
- `squaremath.org` cases/sitemap — cases 1…324 only.
- `jlevy/squares` `packing/atlas/known-best` and `packing/cases` — 1…324 only.
- `erich-friedman.github.io/packing/squinsqu/` — redirect to Kingbird, no data files.
- `mathpuzzle.com` square-packing page — 2003 tiling, irrelevant.
- OEIS A005842/A092137/A003059/A374528/A360610 and OEIS search — integer-only, no
  coordinate sequence exists.

**Papers / repositories**
- Karimi `202611.0242` and Zenodo 23681704 / 23624432 / 23624411 — n ≥ 1182 only.
- Fang `n²−n+1` and `k²−⌈√(32k)⌉−1` records — theorem-only or n ≥ 1182.
- `squarepacker/k2-minus-c`, `moh63-dev/k2m5-family` — asymptotic / `k²−5`; bank exactly
  equals k at every k=15…31.
- OpenAlex/arXiv/HAL/Zenodo sweeps for 2025–2026 square-packing papers — no finite-n
  coordinate tables for 200…1000.
- OSF, figshare — blocked.

**GitHub (fully cleared)**
- `larasmiguel/square-s977`, `RobertoOno/squares-in-square` (n=147/228),
  `bestbryant/claude_code_squaresinsquares` (557 `.npy`),
  `Shubin123/unitSquares` (475 `.bin`), `yugavka/square_in_squares` (29 CSVs),
  `DigitalEuan/squares_in_squares` (5 submissions), `Minuii/squares-in-squares`,
  `dpre4ai/n90-square-packing`, `wand125/square-packing`,
  `TobiasHFS/kaggle-squares-in-squares`, `corentinlaudicina/SquaresInSquares`,
  `munimtechnologies/squares-in-squares-search`, `raojohng/squares-in-squares`,
  `anopheles/packingproblem`, `Davidebyzero/packing_squares_in_squares__tools`,
  `0100001001101111/aletheia-packing-records`, `HyukdongKim/square-packing-exact-sides`,
  `RobertBarnettProjects/square-packing-research`, `Ge-limin/math`, `muellan/packing`.
- GitHub search for “square packing”, “squares in squares”, “packing squares” —
  no new repo beyond the list above; code search remains unavailable without a token.

**Kaggle**
- `udishiken/square-in-square-22-26` v2 (all 3 files),
  `cshara/squares-in-squares-current-best`,
  `rosswade/jammed-squares-engine-packings`,
  `alexchilton/squares-in-squares-starter-kit`,
  `tecnicaaliena/squares-in-squares-literature-packings`,
  `samanyu1808/sis-final-packings`,
  `mzishran/…merged-packings-1000-puzzles`,
  `jonathan1506/joegun-squares-packings`,
  `romywicaksono/squares-pipeline`,
  `davidwarshawsky/squares-in-squares-research-archive` (all 19 batches),
  `leeyoung9527/sis-public-dp-donors-20261113`,
  `mdmuqtadirfuad/sis-certified-portfolio`,
  `ruoxuanzhuang/…two-fault-dp-packings`,
  `busyaprime/squares-in-squares-fq-quenched-packings`,
  `penguin069/squares-gpu-glide-replay-data`,
  `penguin069/squares-boxed55-certified-inputs-20261115`,
  `nevska/squares-in-squares-explorer-files` (viewer cache only),
  and every dataset/kernel tagged “squares” updated between 2026-11-11 and 2026-11-18.
- Kernels: `nilanjansaha123/its-a-secret`, `tomkodaj/squares-in-squares-22-1636`,
  `adityasingh157735/unit-square-packing-octagonal-45-cavity-solver`,
  `dedquoc/square-square-fast-numba-accelerated-simulated`,
  `woshichenyanyan/notebook074c5de1fd`.
- The rank-1 team's `three-square-packings-that-beat-the-records` and the per-puzzle
  leaderboard provenance were already settled in round 2; do not re-derive.

**Still open (not a re-visit, an infrastructure gap)**
- HuggingFace was network-blocked; if a future round has access, search
  `datasets?search=squares`, `unit squares`, `packing` and inspect any dataset with
  per-n coordinates. This is the only source family we could not read at all.
- GitHub code search (file contents) still needs an authenticated token; the literal
  decimals of the 16 targets were already searched on the web and OEIS by round 2.

---

## 6. Artifacts

```
/tmp/campaign2/external3/REPORT.md                  this file
/tmp/campaign2/external3/cmp2.py                    true-rotation bbox comparator (radians)
/tmp/campaign2/external3/parsecert.py               n S / x y t certificate parser
/tmp/campaign2/external3/applydiff.py               before/after diff applier (mod pi/2)
/tmp/campaign2/external3/kag_udishiken/             udishiken v2 (3 files)
/tmp/campaign2/external3/kag_new/                   post-11-11 Kaggle datasets
/tmp/campaign2/external3/kag_new/dw/                19 davidwarshawsky batch certifications
/tmp/campaign2/external3/ko_new/                    post-11-11 Kaggle kernel outputs
/tmp/campaign2/external3/gh/                        GitHub tarballs (Ono, Lara, k2m5, dpre4ai, …)
/tmp/campaign2/external3/yim/                       Kaelan Yim 14 exact certificates
/tmp/campaign2/external3/cand/bestbryant_submission.csv
```

Reproduction of the pointwise check (for any candidate file):

```sh
cd /Users/zhaohuaxiang/ccjjllt/squares
.venv/bin/python - <<'PY'
import sys; sys.path.insert(0, '/tmp/campaign2/external3')
from cmp2 import compare
compare('/path/to/candidate.csv', tol=1e-12)   # prints every strict win
PY
```

`/tmp/best_bank/submission.csv` was never modified. Nothing was submitted to Kaggle.
