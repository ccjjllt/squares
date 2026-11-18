# External open-source mining, round 2 — squares-in-squares (2026-11-18)

Track: non-Kaggle mathematical literature, code ecosystems and catalogues, plus
download-only sweeps of every public Kaggle packing dataset. No Kaggle kernel used;
local work was download, format conversion, comparison and merge-certification only.

Reference bank at the time of every comparison in this report:

```
/tmp/best_bank/submission.csv
score  text    22.128441824806618
       float64 22.12844182480662
SHA-256 9c981e6ea9a44c076587256936948e636936a84ad0668af6b75e946f4fa527e9
valid 1000/1000 on both routes
```

The bank did not move during this round (SHA and score re-checked at the end).

---

## TL;DR

**Net gain vs the live bank: `+5.813682868449632e-11`**
(text route and float64 route identical; 9 puzzles).

That is the whole gain. It comes from **one** source, `Mishapolk/square-packing-records`,
and it is *not* a new packing: it is the same exact rational certificates round 1 already
imported, re-serialised with a **1e-14** centre dilation instead of round 1's **1e-11**.
The exact certificate side is unchanged; only the float64 padding round 1 paid for safety
is recovered. See §1 for the caveat and the fragile-clearance warning.

Everything else is a genuine zero. This round checked **70+ named sources** (27 GitHub record/certificate repos, 8 merged
submission repos, 25 public Kaggle packing datasets including a 408 MB Nov-17 "private
packings" bundle with 50 full 1000-puzzle submissions, all 972 `jlevy/squares` issues,
Zenodo/DataCite/figshare, arXiv, StackExchange, other language ecosystems and forks).
**No other source beats the bank at any n = 1..1000.** Most are exact duplicates of the
bank; the nearest usable miss is 2.45e-12 *behind* (kenaznia n=156), and the only other
sub-bank exact sides are 1e-14-level gaps (dostashev n=129/176, Mishapolk n=147) that no
float64-safe dilation can preserve.

The conclusion the campaign asked for is therefore: **the external channel is now
exhausted.** The live bank equals the entire published mathematical frontier for n ≤ 324
(round 1) and now dominates every public n > 324 artefact we can find, including all
fresh Nov-17 Kaggle bundles. The remaining 0.0776 of score headroom to the Kaggle
per-puzzle snapshot lives only in private Kaggle submissions whose coordinates are not
published anywhere.

---

## 1. The certified improvement

### 1.1 What changed

The nine numbers below are the *same exact certificate geometries* as before
(`Mishapolk/square-packing-records` @ `b637e6cf59c23781c813e8442bfdccb5aa5f3954`,
generated 2026-11-16T23:31:54Z, index `certified_bounds.json`).
Round 1 converted the certificates with

```
x' = S/2 + (1 + 1e-11)(x - S/2)
```

which costs ≈ `1.5e-10` in L per puzzle. The float64 route accepts `1e-14` as well, at
a cost of ≈ `1.5e-13`, so the same packings score lower.

| n | L_bank (50-digit) | L_new | ΔL | Δscore |
|---:|---|---:|---:|---:|
| 156 | 12.977053087494753100517 | 12.977053087494733500000 | 1.960052e-14 | 1.557243e-15 |
| 180 | 13.915618502787467993018 | 13.915618502787446840000 | 2.115302e-14 | 1.553262e-15 |
| 210 | 14.971214601727903623965 | 14.971214601588332179615 | 1.395714e-10 | 9.631407e-12 |
| 260 | 16.633520939996095921759 | 16.633520939839918160000 | 1.561778e-10 | 9.685584e-12 |
| 262 | 16.698115018856375578272 | 16.698115018699552959840 | 1.568226e-10 | 9.688470e-12 |
| 268 | 16.871868135103098943689 | 16.871868135102336050000 | 7.628937e-13 | 4.662978e-14 |
| 272 | 16.965501175989870067416 | 16.965501175830377940000 | 1.594921e-10 | 9.670487e-12 |
| 292 | 17.590016439395992384274 | 17.590016439230261176626 | 1.657312e-10 | 9.698686e-12 |
| 295 | 17.698115018866375578865 | 17.698115018699560299840 | 1.668153e-10 | 9.712453e-12 |

Sum of Δscore = **5.81368e-11** (merge report says `5.813682868449632e-11`; the
per-puzzle `score` column is a float64, so the last two digits differ from the exact sum).

Exact source certificate sides `S` before conversion (all ≈1.5e-13 below `L_new`, which
is the price of the 1e-14 dilation):

```
156 -> 12.977053087494616   180 -> 13.915618502787316   210 -> 14.971214601588191
260 -> 16.633520939839762   262 -> 16.698115018699394   268 -> 16.871868135102179
272 -> 16.965501175830216   292 -> 17.590016439230091   295 -> 17.698115018699394
```

Interpretation of the three groups:

- **n = 210, 260, 262, 272, 292, 295** — the bank contains round 1's 1e-11-dilated import.
  The true certificate side is 1.4–1.7e-10 below the bank L; this round recovers that
  padding by using 1e-14.
- **n = 156, 180, 268** — the bank was *already* within 1.4e-13 (n=156, 180) or
  9.2e-13 (n=268) of the certificate side (those coordinates came from Kaggle/registry,
  not from round 1). Round 1's 1e-11 dilation was larger than the entire remaining gap,
  which is why they were not wins then. At 1e-14 they are.

### 1.2 Certified candidate

```
/tmp/campaign2/external2/merge_wins_d1e-14/submission.csv
SHA-256 7fb3972926be2468efa55b7209e78414053a6579cc38842b763105a3f6a0e3e8

/tmp/campaign2/external2/merge_wins_d1e-14/merge_report.json
SHA-256 1c7e392563525b52104861bf65995a9f6cb59d61d025feeb3feae37e48cd222c
changed_puzzles [156, 180, 210, 260, 262, 268, 272, 292, 295]
net_gain {"text": 5.813682868449632e-11, "float64": 5.813682868449632e-11}

/tmp/campaign2/external2/merge_wins_d1e-14/report.json
text    score 22.128441824748480  valid 1000  invalid_submitted 0  missing 0
float64 score 22.128441824748485  valid 1000  invalid_submitted 0  missing 0
```

Determinism check: three independent merges — this 9-group candidate, the wider
11-group `cand_mish_all_d1e-14.csv` (2801 rows; n=299 and n=307 included but correctly
rejected as non-improving), and a repeat run into `merge_mish_all_d1e-14_repeat/` — all
produced the bit-identical submission `7fb3972926be…`. Line-diff against the bank:
exactly **2195 changed rows**, all inside those nine puzzles (Σn = 2195); no other row
moved.

Candidate diff used:
`/tmp/campaign2/external2/cand_mish_wins_d1e-14.csv` (2195 rows, 6 columns, nine groups;
the 11-group superset is `cand_mish_all_d1e-14.csv`), built from the certificates at the
pinned commit:

```
https://raw.githubusercontent.com/Mishapolk/square-packing-records/b637e6cf59c23781c813e8442bfdccb5aa5f3954/certificates/0000-0999/nNNN.cert
```

| n | certificate | SHA-256 |
|---:|---|---|
| 156 | `certificates/0000-0999/n156.cert` | `05e95f39700a9ef8…` |
| 180 | `certificates/0000-0999/n180.cert` | `bfe9c58f0f97d2ac…` |
| 210 | `certificates/0000-0999/n210.cert` | `a8c474129b3f4323…` |
| 260 | `certificates/0000-0999/n260.cert` | `b059dfa9d855aa14…` |
| 262 | `certificates/0000-0999/n262.cert` | `c5ff84393899ddd0…` |
| 268 | `certificates/0000-0999/n268.cert` | `9a6b2bf4a1139eae…` |
| 272 | `certificates/0000-0999/n272.cert` | `0cd6d68332f84a88…` |
| 292 | `certificates/0000-0999/n292.cert` | `bc044512137a02bc…` |
| 295 | `certificates/0000-0999/n295.cert` | `7778560e076f207d…` |

Full SHA-256s and the exact per-puzzle Δ are in
`/tmp/campaign2/external2/wins_mishapolk2.csv`.

### 1.3 Caveat — read before merging into the bank

- **This is a conversion improvement, not new geometry.** If the campaign's rule is that
  only new packings count, treat the gain as 0 and this candidate as a no-op. If the rule
  is "the submission score is what counts", it is a real, dual-route-certified 5.81e-11.
- **The clearances are ~1e-13, not ~1e-10.** Any later process that re-parses the bank's
  coordinates through float64 and writes them back (normalising, re-centring, re-merging
  by value rather than by reference) can destroy these nine puzzles. The merge tool
  copies unchanged rows verbatim, so the current bank transfer is safe; a future
  optimiser that rewrites whole files is not.
- A `5e-15` variant (`cand_mish_all_d5e-15.csv`) certifies too and nets `5.8179683293246853e-11`,
  a further +4.3e-14, at roughly half the clearance. Not recommended; it buys nothing
  measurable and doubles the fragility.
- `n = 299` and `n = 307` certificates are also sub-bank (9.9e-14, 7.8e-14) but the
  float64-safe dilation costs more than the gap; they do **not** change and are not in
  the candidate.

---

## 2. Why every other source is zero — the gap structure

This is the quantitative reason the external channel cannot help any more.

The Kaggle per-puzzle snapshot (`data/references/leaderboards/perpuzzle_best_20261111.csv`,
total `22.050883571266684`) is still `0.0775582535` better than the bank. Splitting it:

- **386 puzzles** have `bank_L − snapshot_L > 1e-9`; the gross score headroom in those
  puzzles is `0.080466` (other puzzles where the bank is better offset part of it).
- The largest examples are all high-n: n=963 `31.5355339059 → 31.5140787741`
  (2.15e-2, Δscore 6.9e-4), n=902 (2.15e-2), n=908 (1.97e-2), n=969 (1.89e-2),
  n=842 (1.87e-2), n=328 (1.48e-2), n=491 (1.42e-2).

Those sides exist only in teams' Kaggle submissions. **No public artefact anywhere — not
GitHub, not Zenodo, not any Kaggle dataset — contains coordinates at those sides.** We
verified this directly against the strongest public artefacts, which all stop at or above
the bank (see §3). The best full public merge (prvsiyan 2026-11-01) is `22.2602811725`,
still 0.132 behind the bank; the freshest (kmmmvs private bundle 2026-11-17) contains 50
full submissions and improves **zero** puzzles.

At the other end, for n ≤ 324 the bank is the published mathematical frontier to ≤5.3e-14
(round 1's jlevy comparison), and every new exact-certificate repo this round either
matches that frontier or is behind it.

---

## 3. Source ledger — everything checked this round

Legend: "coverage" is n covered in 1..1000; "result" is per-puzzle comparison against the
live bank (threshold 1e-9 for CSV geometry; exact rational comparison for certificates).
Sources marked **(r1)** were already mined in round 1 and are listed only where this
round re-checked or extended them.

### 3.1 GitHub — new record repositories (all cloned, certificates parsed)

| # | Source | URL | Coverage | Result |
|---|---|---|---|---:|
| 1 | **Mishapolk/square-packing-records** (r1, refreshed) | github.com/Mishapolk/square-packing-records | 328–10000 + 13 new n | **9 wins, +5.8137e-11** (conversion, §1). Commit `b637e6c` unchanged since round 1; 0 forks; no newer branch/tag |
| 2 | **kenaznia-doga** 21 repos (`s156`…`s307-upper-bound`, incl. duplicates and the Nov-16 `s292`) | github.com/kenaznia-doga/s156-upper-bound (and siblings) | 156–307 | 0 wins. Exact witnesses are the same geometries as the bank; closest n=156 2.45e-12 behind, the others 2.6e-12…3.4e-12 behind. `s292` (Nov 16) 17.590104218682 vs bank 17.590016439396: **8.78e-5 behind** |
| 3 | **dostashev/square-packing** | github.com/dostashev/square-packing | 129–304, 12 records | 0 wins. n=129 and n=176 are 1.41e-14 and 1.28e-14 **below** the bank, but that is far under the float64-safe dilation cost (~1.2e-13), so they are not importable; everything else is 1.7e-5…8.5e-3 behind |
| 4 | **BuddenPing/square-packing-certificates** (PingYou) | github.com/BuddenPing/square-packing-certificates | 105–302 | 0 wins. n=105 5.2e-12 behind; n=272 8.53e-5 behind; n=302 2.61e-4 behind; n=146 1.38e-8 behind |
| 5 | **RobertBarnettProjects/square-packing-research** | github.com/RobertBarnettProjects/square-packing-research | 146, 261, 2043 | 0 wins. n=261 +2.51e-13 behind; n=146 1.38e-8 behind |
| 6 | **HyukdongKim/square-packing-exact-sides** | github.com/HyukdongKim/square-packing-exact-sides | 172, 263, 297 | 0 wins (minpoly certificates for the same sides as the bank) |
| 7 | **tonclap/sqinsq** | github.com/tonclap/sqinsq | 152, 236, 238, 268, 1453, 2043 | 0 wins; registry s(238)=15.939655 vs bank 15.924107 (1.6e-2 behind) |
| 8 | **SidG2k1/square-packing-refinements** | github.com/SidG2k1/square-packing-refinements | 14 refinements | 0 wins (all SQUISH refinements already at/below the bank) |
| 9 | **lollipoll/couzo-five-exact-certificates** | github.com/lollipoll/couzo-five-exact-certificates | 105, 130, 263, 272, 292 | 0 wins |
| 10 | **ebdeleeuw/square-packing-n70** | github.com/ebdeleeuw/square-packing-n70 | 70 | 0 wins; 8.88096037156625 vs bank 8.88096037155558 (1.02e-11 behind) |
| 11 | **dpre4ai/n90-square-packing** + **jazivxt/n90-square-packing-certificate** | github.com/dpre4ai/n90-square-packing | 90 | 0 wins; 9.998277166926 vs bank 9.994038766583 (4.24e-3 behind) |
| 12 | **BalthasarStrauss/Squares-packing_S-29-_New-Record** | github.com/BalthasarStrauss/Squares-packing_S-29-_New-Record | 29 | 0 wins; 5.933885 vs bank 5.933833 (5.2e-5 behind) |
| 13 | **chelokot/square-packing-archive** | github.com/chelokot/square-packing-archive | 11–89 | 0 wins; historical configurations at or behind proven optima |
| 14 | **NicolasCampailla/Packing-Records** | github.com/NicolasCampailla/Packing-Records | — | no unit-square-in-square data (pentagons, hexagons, triangles) |
| 15 | **zeel991/packing-certify** | github.com/zeel991/packing-certify | — | circle packings only |
| 16 | **0100001001101111/aletheia-packing-records** | github.com/0100001001101111/aletheia-packing-records | — | circle packings, claims withdrawn |
| 17 | **Ge-limin/math** | github.com/Ge-limin/math | — | Grassmannian/line packings and max–min points, not squares |
| 18 | **05oz/certify** | github.com/05oz/certify | — | Keller map, QEC, tournament packings; no square packing |
| 19 | **ArtificialZeng/AI-Has-Taste** | github.com/ArtificialZeng/AI-Has-Taste | — | 457 manuscripts; no square-packing artefact found |
| 20 | **Richman-Tan/frontier-lab** | github.com/Richman-Tan/frontier-lab | — | circles in a square only |
| 21 | **muellan/packing** (AM benchmarks) | github.com/muellan/packing | 1–100 | 0 wins; `min-Square(Square)` solutions sit just above integer sides (bank far below) |
| 22 | **sergey-sonkin/squares** | github.com/sergey-sonkin/squares | — | Rust implementation, test JSON only |
| 23 | **Davidebyzero/packing_squares_in_squares__tools** | github.com/Davidebyzero/packing_squares_in_squares__tools | — | Ellsworth's checkers/refiners; no data files |
| 24 | **corentinlaudicina/SquaresInSquares** | github.com/corentinlaudicina/SquaresInSquares | 1–1000 side table | 0 wins; `known_optima_1_1000.csv` is a side-only table, all ≥ bank |
| 25 | **jlevy/squares forks** | github.com/jlevy/squares/forks | — | 6 forks (`Guzhou0806`, `TT1nKer`, `hipotures`, `Kleddamag`, `what-social-construct`, `BuddenPing`); none adds packing data |
| 26 | **evand/square-packing fork** | github.com/evand/square-packing | — | 1 fork (`wand125/square-packing-1`); no new data |
| 27 | **Mishapolk fork check** | — | — | 0 forks, 0 stars, single `main` branch, latest commit 2026-11-16T23:31:56Z |

### 3.2 GitHub — merged-submission and pipeline repos (full 1000-puzzle CSVs evaluated)

| # | Source | URL | Claimed total | Result |
|---|---|---|---|---:|
| 28 | **bestbryant/claude_code_squaresinsquares** | github.com/bestbryant/claude_code_squaresinsquares | 22.374700578810 | 0 wins; 557 `solutions/nN.npy`, per-puzzle merge of public notebooks |
| 29 | **yugavka/square_in_squares** | github.com/yugavka/square_in_squares | 22.2557026 | 0 wins; 11 `published_sources` files + 20 `auto/` notebook snapshots + own packer hops all evaluated |
| 30 | **sosudo/squares_in_squares** | github.com/sosudo/squares_in_squares | 22.297308538 | 0 wins; 11 candidate portfolios, best 22.2973 |
| 31 | **chaydavs/squares-in-squares** | github.com/chaydavs/squares-in-squares | — | 0 wins; `portfolio_v5.npz` (1000 groups) |
| 32 | **Shubin123/unitSquares** | github.com/Shubin123/unitSquares | 22.372005 (public merge) | 0 wins; 475 public-notebook layouts + 6 own improvements |
| 33 | **oceanwang525-creator/squares-in-squares** | github.com/oceanwang525-creator/squares-in-squares | — | 0 wins; `external_union_nov14/final.csv` (65 hard puzzles, 46k rows) |
| 34 | **penguin069 GPU glide replay** (Kaggle dataset) | kaggle.com/datasets/penguin069/squares-gpu-glide-replay-data | — | 0 wins (baseline submission only) |
| 35 | **DigitalEuan / Minuii / cubres / TobiasHFS / corentinlaudicina / omerfisler / rushikesh648 / munimtechnologies / AHFE0924 / Samanyu-dev (r1, spot)** | — | 22.218–22.374 | 0 wins (r1 result unchanged; no new artefacts) |

### 3.3 Kaggle datasets — download-only sweep (no kernel used)

Every dataset returned by `kaggle datasets list -s "squares in squares"` and
`-s "square packing"` was downloaded and every CSV evaluated per puzzle. Where the
dataset ships a full submission, the whole 1000-puzzle file was scored.

| # | Dataset | Updated | Coverage | Result |
|---|---|---|---|---:|
| 36 | **kmmmvs/squares-in-squares-private-packings** | 2026-11-17 | 1.5 GB bundle; 156 CSVs, 50 full submissions | **0 wins on all 50 full submissions**; includes `local_bank.csv` (same as bank), 17 `packing_coordinate_diff.csv` groups, 50+ team submissions (malyshev, sigma, busy, jazivxt, seshu, mufasa, …) |
| 37 | asteriospanoras/squares-in-squares-best | 2026-11-17 | 1000 | 0 wins |
| 38 | rosswade/jammed-squares-engine-packings | 2026-11-17 | 1000 + improvements | 0 wins |
| 39 | avazaku/squares-contact-lp-cusp-bounds-465-998 | 2026-11-15 | 465–998, many per-n | 0 wins |
| 40 | tecnicaaliena/squares-in-squares-literature-packings | 2026-11-15 | 1000 | 0 wins |
| 41 | samanyu1808/sis-final-packings | 2026-11-14 | 1000 | 0 wins; 443 puzzles bit-equal to the bank, 557 behind |
| 42 | jonathan1506/joegun-squares-packings | 2026-11-13 | 1000 | 0 wins |
| 43 | mzishran/squares-in-squares-merged-packings-1000-puzzles | 2026-11-13 | 1000 | 0 wins |
| 44 | busyaprime/squares-in-squares-fq-quenched-packings | 2026-11-11 | packings.csv | 0 wins |
| 45 | pablodiegoo/unit-square-packing-certified-bounds | 2026-11-09 | 1000 | 0 wins |
| 46 | alexchilton/squares-in-squares-starter-kit | 2026-11-17 | 1000 (`best.csv`, `best_current.csv`) | 0 wins |
| 47 | prvsiyan/squares-in-squares-verified-packings-20261101 | 2026-11-01 | 1000 | 0 wins; 630 puzzles bit-equal to the bank, 370 behind |
| 48 | prvsiyan/squares-auto-updater-live | 2026-11-02 | 1000 | 0 wins |
| 49 | dariushafshar/squares-in-squares-certified-packings (v11) | 2026-10-24 | 1000 | 0 wins |
| 50 | lostdecimal27/squares-in-squares-bank | 2026-10-29 | 1000 | 0 wins (it is a snapshot of the same Kaggle donor pool) |
| 51 | cdeotte/squares-in-squares-22-315-data | 2026-10-24 | 1000 | 0 wins |
| 52 | lightningv08/squares-in-squares-layout-atlas | 2026-10-24 | 547+545 | 0 wins |
| 53 | alimaadl3lim3d/squares-in-squares-kaggle-safe-blend | 2026-10-30 | 1000 | 0 wins |
| 54 | skarin/squares-in-squares-certified-santa-guide | 2026-10-22 | 543 | 0 wins |
| 55 | az05192000gmailcom/squares-in-squares-l-band-packings | 2026-11-05 | 1000 | 0 wins |
| 56 | az05192000gmailcom/squares-in-squares-stretched-packings | 2026-11-06 | 1000 | 0 wins |
| 57 | nevska/squares-in-squares-explorer-files | 2026-11-16 | viewer data | 0 wins |
| 58 | ruoxuanzhuang/squares-in-squares-two-fault-dp-packings | 2026-11-05 | 744, 978 | 0 wins |
| 59 | jazivxt/n90-square-packing-certificate | 2026-11-15 | 90 | 0 wins (same as #11) |
| 60 | kmmmvs/squares-in-squares-best-packings | 2026-11-02 | 1000 | 0 wins (also scanned inside yugavka's `auto/`) |

### 3.4 `jlevy/squares` — issues, PRs and mirrors

All **972** issues/PRs (REST pagination, 10 pages) were dumped and scanned for claimed
sides. Recent registration requests specifically:

| Issue | Claim | Result |
|---|---|---|
| #1012 (Nov 17) | "public Kaggle packings below the register for n=109,270" | both sides are **exactly the bank**: n=109 10.949289580943, n=270 16.9274660649 (pointer *to* our donor pool, not a new source) |
| #1009 (Mishapolk, Nov 16) | 7 lowered bounds (Part A) + 6 refinements (Part B) | Part A: the 6 round-1 wins (210,260,262,272,292,295) plus n=268, which this round captures by re-dilation; Part B: n=156 and n=180 are captured, n=299/307 are sub-bank but below the dilation cost, n=147 is 1.7e-14 below the bank (also below the dilation cost), n=270 is behind |
| #992 (Lara, Nov 15) | s(977) ≤ 17+21/√2 = 31.84924 | **behind**: bank n=977 = 31.7425542342 |
| #895 (Yim, Nov 4) | s(260) 16.6339825019 | behind bank 16.6335209400 by 4.6e-4 |
| #984/#985 (Ono) | s(228) 15.596043120921, s(147) 12.651043556588 | behind: bank 15.596043116632, 12.651043553173 |
| #1001 (JonathanGun) | n=127,204,232,264,305 | r1 result: all behind, closest n=204 +1.56e-10 |
| #1005/#1006/#1007 (Özden/de Winter) | n=292, 262, 295 | all superseded by Mishapolk / bank |
| #1011 (jlevy) | intake of #1005–1007 | no new geometry |
| #846 (Mishapolk, Oct 30) | 14 upper bounds, n=105–308 | all already at/below the bank (n=130,182,268 included) |
| #847 (Karimi, Oct 30) | 5134 bounds n=1182–9946 | **out of range** (no n ≤ 1000) |
| #941/#942 (de Winter) | 15 + 16 bounds n=413–910 | all behind (r1 scanned the same repo folders) |
| PRs | 808 items, all authored by `jlevy` (intake lanes) | no external PR carries coordinates |

Also checked: `packing/resources/papers/` (48 papers, all r1-covered topics), the 303-source
`packing/resources/web/` mirror (adds `esummins-packing` = n=11 lower bounds,
`yim-certificates` = measure/lower-bound certificates, `external-square-certificates` =
n=17/11 proofs — none carries square-packing coordinates), and `packing/atlas/known-best`
(only n ≤ 324, matches the bank). No new data.

### 3.5 Papers and supplementary material (the round-1 gap)

Round 1 read the papers; this round read their **data deposits**.

| Source | What is deposited | Result |
|---|---|---|
| **Zenodo / DataCite** (125 records matching "square packing", incl. figshare/OSF mirrors) | certificates, code and tables for 2026 square-packing papers | **no in-range coordinates better than the bank.** The only record tables are: Karimi `filled_records.csv` n=1182–9946 (out of range); Fang's two-strip / filled-end constructions n=1182–9944 (out of range); Fang's `k²−⌈√(32k)⌉−1` theorem with certificates only for k=300, 600 (n=89901+); Fang's `n²−n+1` construction (n ≥ 211, side < n but far above the bank's 14.7–17.8 at those n); the rest are proofs/lower bounds (s(44)=7, s(12), n=11, s(17), k²−5 family) |
| **arXiv 2026** (`packing unit squares`, `squares in a square`, `square packing`) | "Soft-to-Rigid" (Ostashev — data in his GitHub repo, checked #3), "Optimally Packing a Large Square" (asymptotic), axis-parallel 7/8-square formulas, online packing | no coordinate data beyond repos already checked |
| **OEIS, MathWorld, Packomania, Friedman survey** (r1) | — | no best-known non-integer sides with coordinates; Packomania is circles only |
| **MathOverflow / Math.SE / Puzzling / Code Golf** (StackExchange API, 4 sites × 15 hits) | n=11 thread (proved optimum = bank), code-golf tiling/perfect-square threads | no explicit construction beating the bank |

### 3.6 Other ecosystems

GitHub repo search with `language:Julia` (0 repos), `language:Fortran` (0),
`language:Rust` (6), `language:C++` (10), plus 36 readme-targeted queries (530 unique
repos): only implementations and the sources already listed. OR-library-style benchmark
collections (`muellan/packing`, `hfu622/2DISP-BKVs`, `NestabPacking/stripPackingDataset`)
are different problems or behind. No Rosetta/code-golf artefact with coordinates.

---

## 4. Closest external attempts (for the record)

These are the nearest things to a win that exist anywhere outside the bank. All are
**behind or non-importable**, except the Mishapolk rows captured in §1.

| n | Source | source S | bank L | bank − S |
|---:|---|---:|---:|---:|
| 156 | kenaznia-doga/s156-upper-bound | 12.977053087497204 | 12.977053087494753 | −2.45e-12 |
| 172 | kenaznia-doga/s172-upper-bound | 13.614689853286215 | 13.614689853283598 | −2.62e-12 |
| 261 | RobertBarnett n261.cert | 16.678779875343206 | 16.678779875342957 | −2.49e-13 |
| 129 | dostashev n0129.sqcert | 11.870013850404465 | 11.870013850404478 | +1.41e-14 (below bank, below dilation cost) |
| 176 | dostashev n0176.sqcert | 13.795872318436407 | 13.795872318436420 | +1.28e-14 (below bank, below dilation cost) |
| 105 | BuddenPing/PingYou | 10.789303783748159 | 10.789303783742994 | −5.16e-12 |
| 90 | JoostdeWinter (r1) | 9.994038766610 | 9.994038766582889 | −2.71e-11 |
| 204 | JonathanGun (r1) | 14.802646843107 | 14.802646842951363 | −1.56e-10 |
| **268** | **Mishapolk n268.cert** | **16.871868135102179** | **16.871868135103099** | **+9.21e-13 (captured)** |
| 963 | Mishapolk n963.cert | 31.535533905933 | 31.535533905932983 | +2.46e-13 (below the float64-safe dilation cost) |

The pattern is unmistakable: outside Mishapolk the best any source does is 2.45e-12
behind (kenaznia n=156), or 1.41e-14 *below* the bank (dostashev n=129) — a gap that no
float64-safe dilation can preserve. The bank already contains every one of these
packings to float rounding.

---

## 5. What this means for the campaign

1. **External mining is finished for this competition.** Every published coordinate set
   in range is now either in the bank or behind it. The last two external wins were
   Mishapolk's Nov-16 certificates (round 1) and the residual float64 padding on the same
   certificates (this round, 5.81e-11).
2. **The only remaining 0.0776 is Kaggle-private.** 386 puzzles are still behind the
   Nov-11 per-puzzle snapshot, up to 2.1e-2 at n=963/902. No public artefact has
   coordinates at those sides. Closing that gap requires new private submissions or a
   search, not more source mining.
3. **Do not re-run this sweep.** The new-repo space was searched 3 ways (repo search ×36
   queries, readme search ×18, language filters ×12), 530 unique repos triaged, every
   repo with coordinate data cloned or metadata-cloned, and every public Kaggle dataset
   with packing data downloaded. A future round should only poll the handful of live
   sources in §6, not re-scan.
4. **If the orchestrator wants the 5.81e-11**, consume
   `merge_wins_d1e-14/submission.csv` (SHA `7fb3972926be…`). If the campaign's
   accounting only credits new geometry, record the round as **net 0** and keep the
   analysis: the bank is now provably ahead of the entire public external corpus.

---

## 6. Updated do-not-revisit list

Do not re-mine any of the following unless the stated artefact is **newer than
2026-11-18**:

**Round-1 list, still valid:** Kingbird/Ellsworth catalogue; `jlevy/squares` witnesses
n≤324 and the 324-entry frontier; `franciscouzo/square-packing`; `JoostdeWinter/square-packing`;
`TheSnakeFang/squarepack-certs`; `JonathanGun/square-packing-upper-bounds`; `itsnaka/squish-certs`;
`ry-xu/square_packing`; `evand/square-packing`; Packomania; OEIS (A005842/A092137/A003059/A360610);
Karimi (n≥1182); Friedman EJC DS#7; arXiv asymptotic/axis-parallel papers; the n=11
Math.SE thread; code-golf/Reddit threads; `griffcass/square-packing`.

**Added this round:**

- `Mishapolk/square-packing-records` — **poll only** (it is the only live external seam;
  re-read `certified_bounds.json` for a new `generated` timestamp / new commit).
- `kenaznia-doga/*` (21 repos) — all at or behind; `s292` (Nov 16) behind by 8.8e-5.
- `dostashev/square-packing`, `BuddenPing/square-packing-certificates`,
  `RobertBarnettProjects/square-packing-research`, `HyukdongKim/square-packing-exact-sides`,
  `tonclap/sqinsq`, `SidG2k1/square-packing-refinements`,
  `lollipoll/couzo-five-exact-certificates`, `ebdeleeuw/square-packing-n70`,
  `dpre4ai/n90-square-packing`, `jazivxt/n90-square-packing-certificate`,
  `BalthasarStrauss/Squares-packing_S-29-_New-Record`, `chelokot/square-packing-archive`.
- `NicolasCampailla/Packing-Records`, `zeel991/packing-certify`,
  `0100001001101111/aletheia-packing-records`, `Ge-limin/math`, `05oz/certify`,
  `ArtificialZeng/AI-Has-Taste`, `Richman-Tan/frontier-lab` — different problems.
- `muellan/packing`, `sergey-sonkin/squares`, `Davidebyzero/packing_squares_in_squares__tools`,
  `corentinlaudicina/SquaresInSquares` (side-only table).
- All merged-submission repos: `bestbryant/claude_code_squaresinsquares`,
  `yugavka/square_in_squares`, `sosudo/squares_in_squares`, `chaydavs/squares-in-squares`,
  `Shubin123/unitSquares`, `oceanwang525-creator/squares-in-squares`.
- All public Kaggle packing datasets, in particular the whole
  `kmmmvs/squares-in-squares-private-packings` bundle (Nov 17) and every dataset in §3.3.
- `jlevy/squares` issues/PRs up to #1012 (pointer traffic only), `packing/resources/papers`,
  `packing/resources/web`, `packing/atlas/known-best`.
- Zenodo/DataCite/figshare square-packing deposits (Karimi, Fang, proofs, lower bounds).
- GitHub forks of Mishapolk (0), Joost (0), franciscouzo (0), evand (1, empty),
  jlevy (6, no data).

**Worth polling (cheap, once per round):**
`Mishapolk/square-packing-records` commit/`certified_bounds.json`;
`dogaozden.com/math/live/square-packing/tracker.html` (live record tracker, sides only);
`kenaznia-doga` new `sNNN-upper-bound` repos; the `jlevy/squares` issues #1013+;
new Kaggle datasets by `kmmmvs`, `samanyu1808`, `prvsiyan`, `asteriospanoras`.

---

## 7. Reproduction

Certified re-dilation (this round's only change):

```sh
cd /Users/zhaohuaxiang/ccjjllt/squares
.venv/bin/python -m squares merge \
  --baseline /tmp/best_bank/submission.csv \
  --baseline-report /tmp/best_bank/report.json \
  --candidate /tmp/campaign2/external2/cand_mish_wins_d1e-14.csv \
  --output-dir /tmp/campaign2/external2/merge_wins_d1e-14 --workers 4
# -> changed [156,180,210,260,262,268,272,292,295]
# -> text 22.128441824748480 / float64 22.128441824748485, valid 1000/1000 each
# -> submission SHA 7fb3972926be2468efa55b7209e78414053a6579cc38842b763105a3f6a0e3e8
```

The 1e-14 conversion itself (from the pinned certificates):

```
x' = S/2 + (1 + 1e-14)(x - S/2),  y' = S/2 + (1 + 1e-14)(y - S/2),  angle = 2*atan(t)
```

Reference no-op merge proving the strongest full-coverage public dataset cannot move the
bank:

```sh
.venv/bin/python -m squares merge \
  --baseline /tmp/best_bank/submission.csv \
  --baseline-report /tmp/best_bank/report.json \
  --candidate /tmp/campaign2/external2/cand_prvsiyan.csv \
  --output-dir /tmp/campaign2/external2/merge_prvsiyan --workers 4
# -> changed [], net_gain 0, submission SHA identical to the bank (9c981e6e…)
#    502 groups re-scored, 0 improvements
```

Artifacts:

```
/tmp/campaign2/external2/REPORT.md                          this report
/tmp/campaign2/external2/wins_mishapolk2.csv                the 9 rows: n, cert, SHA, L, ΔL, Δscore
/tmp/campaign2/external2/cand_mish_wins_d1e-14.csv          2195-row diff candidate (recommended, 9 groups)
/tmp/campaign2/external2/cand_mish_all_d1e-14.csv           2801-row superset (11 groups; 299/307 no-op)
/tmp/campaign2/external2/cand_mish_all_d5e-15.csv           smaller-dilation variant (+4.3e-14, not recommended)
/tmp/campaign2/external2/merge_wins_d1e-14/                 certified candidate (submission/report/merge_report)
/tmp/campaign2/external2/merge_mish_all_d1e-14_repeat/      bit-identical repeat merge
/tmp/campaign2/external2/merge_prvsiyan/                    certified null result vs the strongest public dataset
/tmp/campaign2/external2/mish2/n*.cert                      13 Mishapolk certificates used for the census
/tmp/campaign2/external2/gh/repos.json, gh/repos2.json       530-repo triage (repo + readme searches)
/tmp/campaign2/external2/gh/lang_repos.json                  language-filtered search
/tmp/campaign2/external2/jl_all/issues_p1_10.json            all 972 jlevy issues/PRs
/tmp/campaign2/external2/kag/x/                              every downloaded Kaggle dataset
/tmp/campaign2/external2/kmm_scan.log                        50-submission scan of the Nov-17 private bundle
/tmp/campaign2/external2/scan_sub_csv.py, scan_certs.py, eval_csv.py   evaluation tools
```

`/tmp/best_bank/submission.csv` was never modified. Nothing was submitted to Kaggle.
