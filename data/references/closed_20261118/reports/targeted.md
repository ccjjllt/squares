# Targeted external search — the 16 high-value indices

Track: hunt the 16 specific indices that hold most of the remaining gap.
No Kaggle kernel used, no submission made, `/tmp/best_bank/submission.csv` untouched.
Local work = downloads, Kaggle/API/web reads, bbox arithmetic, report.

Bank at the start of this track: score **22.128441824806618**, SHA-256
`9c981e6ea9a44c076587256936948e636936a84ad0668af6b75e946f4fa527e9`.
Bank at the end (2026-11-18T05:44Z): score **22.128396684529527**, SHA-256
`bb6d5f2a1eeccf457f3b97ad6c06d09103bff594e04c73966a2fc3dc6fc5086f` — `auto_pipeline.py` moved it
by −4.51e-8 while this track ran. **All 16 target puzzles are byte-identical across that drift**,
so every L in this report is exact against either version.


---

## TL;DR

**No candidate found. Zero of the 16 target sides have published coordinates — and this is now
established from the record-keepers' own correspondence, not just from a failed sweep.**

Three results:

1. **Provenance of the targets is now settled.** The 16 target sides are entries of Kaggle's
   *per-puzzle leaderboard*, which is a **side-only** table (columns `n, L, score, TeamName,
   DateSubmitted`), produced by the Kaggle staff notebook
   `inversion/squares-in-squares-per-puzzle-leaderboard` from `best_puzzle_scores.csv`.
   15 of the 16 are held by **team "Cats and boxes 😼" = user `pjmathematician`**, Kaggle rank 1
   (22.0399510810, 85 submissions); n=333 was team "Vaibhav" on Oct 29 and had passed to
   Cats and boxes by Nov 11, so the Nov-11 snapshot attributes all 16 to the rank-1 team.
   The Squares Project itself has tried to import these entries and
   concluded they state no packing — verbatim, in `jlevy/squares` issue #929 and on
   `squaremath.org/cases/299.html`: *"It is unpublished and states no packing. We cannot verify
   it and make no claim about it."*

2. **The rank-1 team's own public work contains none of them.** `pjmathematician` has exactly one
   squares notebook, `three-square-packings-that-beat-the-records`, which publishes coordinates
   for **n = 232, 260, 299 only** — all three are *behind* the live bank — and says explicitly
   *"These are not our final versions for these n, so there is still room to improve them."*
   Its own prose describes the method that produced the private records: replace the rigid
   single-angle band with bigger tilted regions at many slightly different angles, then relax
   numerically. That is a private search, not a published construction.

3. **The whole public coordinate corpus was scanned and it is the bank.** 44 public artefacts —
   every full-size public notebook output and every squares dataset that exists, including the
   three biggest merges of merges — were downloaded and evaluated on the 16 indices.
   **0 wins.** At 12 of the 16 the best public artefact is *bit-identical* to the live bank; at
   the other 4 it is behind. Nothing in public gets closer than the bank anywhere (§4.1, K14).
   This supersedes the brief's "183 kernels / 406 datasets" sweep with a verified pointwise
   statement on exactly these indices.

Per-n outcome: **FOUND — none**, for all 16. See §3 for the per-n table and §4 for the full
query ledger.


**Structural bonus for whoever picks this up next** (§6): the 16 gaps are not 16 independent
numbers. Three of them (842, 901, 962) differ from the bank by exactly the *same* amount,
0.0186625719, i.e. they are one liftable gadget `f = 0.5021527079`; two more (902, 963) share
`f = 0.5140787741`. Reconstructing **one** D=1 gadget is worth **1.867e-3**, not 6.4e-4.

---

## 1. What the targets actually are

Measured against the live bank (`L = max bbox` of the 500500-row submission, +1 for the centre
convention). `snapshot` = `data/references/leaderboards/perpuzzle_best_20261111.csv`.
Re-verified at 2026-11-18T05:44Z against bank SHA `bb6d5f2a…`: the 16 L values below are
unchanged by the 22.1284418 → 22.1283967 drift.

| n | bank L | snapshot (11-11) | ΔL | Δscore | record holder (11-11) |
|---:|---:|---:|---:|---:|---|
| 328 | 18.614368938491 | 18.599535464806 | 0.014833 | 8.190e-4 | Cats and boxes 😼 |
| 902 | 30.535533905933 | 30.514078774139 | 0.021455 | 7.144e-4 | Cats and boxes 😼 |
| 963 | 31.535533905933 | 31.514078774129 | 0.021455 | 6.914e-4 | Cats and boxes 😼 |
| 908 | 30.625574725146 | 30.605884508570 | 0.019690 | 6.534e-4 | Cats and boxes 😼 |
| 842 | 29.520815280171 | 29.502152707903 | 0.018663 | 6.432e-4 | Cats and boxes 😼 |
| 491 | 22.684143606359 | 22.669926930403 | 0.014217 | 6.416e-4 | Cats and boxes 😼 |
| 367 | 19.682794505625 | 19.670856797022 | 0.011938 | 6.231e-4 | Cats and boxes 😼 |
| 901 | 30.520815280171 | 30.502152707908 | 0.018663 | 6.217e-4 | Cats and boxes 😼 |
| 803 | 28.811202562357 | 28.793943440230 | 0.017259 | 6.091e-4 | Cats and boxes 😼 |
| 969 | 31.624490853785 | 31.605570898559 | 0.018920 | 6.078e-4 | Cats and boxes 😼 |
| 747 | 27.810271339177 | 27.793759657056 | 0.016512 | 6.041e-4 | Cats and boxes 😼 |
| 804 | 28.827154349934 | 28.810060585415 | 0.017094 | 6.029e-4 | Cats and boxes 😼 |
| 962 | 31.520815280171 | 31.502152707911 | 0.018663 | 6.017e-4 | Cats and boxes 😼 |
| 843 | 29.535533905933 | 29.518244283132 | 0.017290 | 5.955e-4 | Cats and boxes 😼 |
| 333 | 18.770654870107 | 18.760014153077 | 0.010641 | 5.831e-4 | Cats and boxes 😼 |
| 456 | 21.846667192844 | 21.834217586917 | 0.012450 | 5.830e-4 | Cats and boxes 😼 |

**Sum of these 16 = 0.01019502** of score, measured on the live bank. (The brief quoted
0.01245 / 26 % of the gap; against today's bank the 16 recompute to 1.0195e-2 — same
order, the difference is the bank having absorbed other donors since that estimate. The
figure is unchanged by the −4.51e-8 drift during this track.)

---

## 2. The provenance result (the main finding)

### 2.1 The table is a leaderboard, not a catalogue

`inversion/squares-in-squares-per-puzzle-leaderboard` (Kaggle staff account `inversion`,
157 votes, last run 2026-11-17) is public; I pulled its source. It does no geometry at all:

```python
df = pd.read_csv("best_puzzle_scores.csv",
                 dtype={"n": int, "L": str, "score": str, "TeamName": str, "DateSubmitted": str})
df = df[df["TeamName"] != "-"]           # drop puzzles nobody has beaten the baseline at
```

`best_puzzle_scores.csv` carries `TeamName` and `DateSubmitted` — Kaggle submission metadata.
A copy of that table with team and date is inside the public dataset
`lostdecimal27/squares-in-squares-bank` as `perpuzzle_best.csv` (2026-10-29 snapshot), and a
newer copy in `udishiken/square-in-square-22-26` (v2, 25.7 MB).

Oct-29 copy, our 16 rows:

```
 328 18.59953546480645036  Cats and boxes 😼  2026-10-27 00:05:22
 333 18.76307892479625085  Vaibhav           2026-10-28 07:11:24
 367 19.67972381411735632  Cats and boxes 😼  2026-10-28 02:29:33
 456 21.83421758691674064  Cats and boxes 😼  2026-10-27 21:40:44
 491 22.67453091084894093  Cats and boxes 😼  2026-10-28 14:35:06
 747 27.79375965705617066  Cats and boxes 😼  2026-10-28 04:56:40
 803 28.79394344023012786  Cats and boxes 😼  2026-10-28 09:50:56
 804 28.81006058541475556  Cats and boxes 😼  2026-10-28 00:02:27
 842 29.50989197457572138  Cats and boxes 😼  2026-10-28 09:50:56
 843 29.52745178050245453  Cats and boxes 😼  2026-10-28 14:35:06
 901 30.50659102933784055  Cats and boxes 😼  2026-10-27 16:54:56
 902 30.52427210294281863  Cats and boxes 😼  2026-10-29 02:31:42
 908 30.60588450859370367  Cats and boxes 😼  2026-10-27 00:05:22
 962 31.50659102934455634  Cats and boxes 😼  2026-10-27 16:54:56
 963 31.52262363886089836  Cats and boxes 😼  2026-10-28 02:29:33
 969 31.60588450855228471  Cats and boxes 😼  2026-10-27 07:06:47
```

Two things this reveals that a side-only table cannot:

* The team kept **submitting and improving** between Oct 27 and Nov 11: n=842 went
  `29.5098919745757` → `29.5021527079033`, n=902 `30.5242721029428` → `30.5140787741393`.
  These are submissions to a private notebook/kernel, evolving over two weeks.
* On Oct 29 the D=1 family was **not** consistent (`842: 0.50989`, `901: 0.50659`,
  `962: 0.50659`); by Nov 11 it is (`0.5021527079` for all three). So the final state is one
  gadget, found on one k and lifted by adding a row+column (`+2k+1` squares costs nothing).

### 2.2 The record-keepers say the entries carry no packing

`jlevy/squares` is the register of record that has been chasing exactly these numbers. Its
issue comments and case pages state the conclusion directly (found via GitHub issue search and
web search; full text in `/tmp/campaign2/targeted/evidence_quotes.md`):

> "The Kaggle per-puzzle leaderboard (staff notebook `inversion/squares-in-squares-per-puzzle-leaderboard`)
> also lists a side-only entry for n = 299: **17.7936369918**, team Cats and boxes 😼, 2026-10-27.
> **It is unpublished and states no packing. We cannot verify it and make no claim about it.**"
> — `kenaznia-doga`, jlevy/squares#929, 2026-11-09

> "A Kaggle per-puzzle side the update quotes, 17.793636991 for Cats and boxes,
> **states no packing and is no report**."
> — `squaremath.org/cases/299.html`

The same sentence, with the same side-only value, appears for n = 303 (#930), n = 270 (#936),
n = 268 (#928). The Squares Project has the same leaderboard we do and has *also* concluded the
coordinates are unavailable.

### 2.3 The record holder's public output

Rank-1 identification from the public leaderboard CSV
(`squares-in-squares-publicleaderboard-2026-11-17T18:48:51.csv`):

```
1,17176026,"Cats and boxes 😼","2026-11-14 12:08:29",22.0399510810,85,pjmathematician
2,17192272,VitalyR,             "2026-11-14 09:39:47",22.0479990757,47,vitalyankh
3,17172870,"Chris Deotte",      "2026-11-17 12:35:38",22.0490584128,17,cdeotte
4,17235908,"Sunstone North Lab","2026-11-17 15:55:05",22.0555557826,96,burtonlancaster
5,17198102,"inspector gadget",  "2026-11-16 14:44:29",22.0580926280,40,"grennwolf,tonylica"
```

`pjmathematician` owns exactly one squares-in-squares notebook:
`three-square-packings-that-beat-the-records` (2026-10-26, 12 votes). Pulled and executed:

| n | their public side | live bank | verdict |
|---:|---:|---:|---|
| 232 | 15.763777868 | 15.759531624 | behind 4.25e-3 |
| 260 | 16.642148765 | 16.633520940 | behind 8.63e-3 |
| 299 | 17.813285545 | 17.801004434 | behind 1.23e-2 |

None of our 16. Their notebook markdown — the only public description of the method that made
the records — says:

> "**The common thread.** The records are clean, rigid patterns with one angle per tilted region,
> the kind you can describe in a formula. The new packings are less tidy: bigger tilted regions,
> many slightly different angles, and a different layout. The extra freedom is what pays."
> … "These are not our final versions for these n, so there is still room to improve them."

and explains the three teasers as: n=299 "no diagonal band at all", n=260 "much thicker band
(104 tilted squares instead of 60)", n=232 "both tilted regions at a shallow ~28°".

That is precisely the engine the campaign's own `templates` / `engine` tracks are building;
nothing about it is published as data.

### 2.4 The rest of the top 10 publish nothing either

`kaggle kernels list --user <member> -s squares` and `kaggle datasets list --user <member>` for
every member of the top-10 teams (`vitalyankh`, `burtonlancaster`, `cdeotte`, `grennwolf`,
`tonylica`, `kentonishioka`, `koi51koi`, `mech39`, `naniwazu`, `physics0523`, `maikanamuo`,
`nevska`, `misfyre`) return **no squares-in-squares kernel and no squares dataset**, apart from
the already-scanned `cdeotte/squares-in-squares-22-315-data` (5.9 MB, 22.315 — far behind) and
`nevska/squares-in-squares-explorer-files` (2.3 MB, in the scan list). `pjmathematician` owns no
squares dataset at all.


---

## 3. Per-puzzle outcome

| n | outcome | why |
|---:|---|---|
| 328 | **not found** | leaderboard-only; Mishapolk/franciscouzo/Couzo all equal or behind the bank |
| 902 | **not found** | as above; shares the D=2 constant with 963 |
| 963 | **not found** | as above |
| 908 | **not found** | as above |
| 842 | **not found** | the single most valuable target; no public artefact holds `29.5021527` |
| 491 | **not found** | as above |
| 367 | **not found** | as above |
| 901 | **not found** | derived from the same gadget as 842 |
| 803 | **not found** | as above |
| 969 | **not found** | as above |
| 747 | **not found** | as above |
| 804 | **not found** | as above |
| 962 | **not found** | derived from the same gadget as 842 |
| 843 | **not found** | as above |
| 333 | **not found** | leaderboard-only (team Vaibhav, then Cats and boxes) |
| 456 | **not found** | as above; the Zenodo `k²−⌈√(32k)⌉−1` family reaches n=456 for k=22 but only proves `s < 22`, far above our 21.8342 |

**No certified candidate exists, so there is no merge directory and no dual-route score for this
track.** Nothing was passed to `python -m squares merge`.

---

## 4. Search ledger — every query, platform, result

### 4.1 Kaggle artefacts (the productive corpus)

| # | What | Result |
|---|---|---|
| K1 | `kaggle competitions leaderboard squares-in-squares --download` (2026-11-17T18:48) | 2202 teams; rank 1 = `pjmathematician` 22.0399510810 |
| K2 | `kaggle kernels list --competition squares-in-squares --sort-by scoreDescending` (60 rows) | best public LB in titles is 22.134; **no public notebook is ahead of the bank (22.1284)** |
| K3 | `kaggle kernels list --competition squares-in-squares --sort-by voteCount` (60 rows) | surfaced the per-puzzle-leaderboard notebook and all merge notebooks |
| K4 | `kaggle datasets list -s "squares in squares"` (page 1) + `-s "per puzzle"` + `-s "jammed squares"` + `-s "layout atlas"` | full dataset inventory below |
| K5 | `inversion/squares-in-squares-per-puzzle-leaderboard` — source pulled | **decisive**: reads `best_puzzle_scores.csv` (`n,L,score,TeamName,DateSubmitted`); no geometry |
| K6 | `pjmathematician/three-square-packings-that-beat-the-records` — source + output pulled, code executed | 3 packings (232/260/299), **all behind the bank** |
| K7 | `jazivxt/boxed-in-sub` — output downloaded (500500 rows) | 0/16 wins; 367/803/747/804/333 all behind |
| K8 | `areebbb/squares-in-squares-the-last-1e-9` — output + `per_n.csv`, `per_n_gap.csv`, log | 0/16 wins; its `src` attribution is unreliable (see §5) |
| K9 | `alexchilton/fault-line-dp-basin-hopping-lb-22-2620` — `c0.csv`, `cq.csv` | 0/16 wins; 328/491/842/843/901/902/908/456/963/969/962 exact ties, 367/803/747/804/333 behind |
| K10 | `malyshevdanil/squares-in-squares-living-atlas-of-tight-packings` | 0/16 wins |
| K11 | `rosswade/jammed-squares-contact-forces-and-fast-lp-search` | 0/16 wins |
| K12 | Dataset `asteriospanoras/squares-in-squares-best` (22.132015818, 2026-11-17) | 0/16 wins; 11 exact ties |
| K13 | Dataset `lostdecimal27/squares-in-squares-bank` | contains `perpuzzle_best.csv` = the side-only leaderboard with team+date (§2.1) |
| K14 | **44-artefact automated scan**, `scan_sources.py` — every full-size public notebook output and every squares dataset that exists (all 38 distinct 1000-size sources from areebbb's log, plus the 5 remaining squares datasets) | **completed: 0 wins in 44 sources.** Per-source rows in `/tmp/campaign2/targeted/scan/results*.tsv` |
| K15 | 7 large notebooks that hit the 420 s cap in K14 (`penguin069/*` ×6, `lucifer19/think-select-reclose`, 34 versions) | retried at a 3000 s cap, `retry_sources.py`: **all 7 completed, 0 wins** (`scan/retry_*.tsv`) |

**K14 + K15 in full.** For each of the 16 n, the smallest L reached by *any* of the 44 public
artefacts, and how it compares with the live bank:

| n | best L over 44 public artefacts | best source | above target | vs bank |
|---:|---:|---|---:|---:|
| 328 | 18.614368938491 | penguin069 | 0.014833 | 0 |
| 902 | 30.535533905933 | penguin069 | 0.021455 | +1.4e-13 |
| 963 | 31.535533905933 | penguin069 | 0.021455 | +1.1e-14 |
| 908 | 30.625574725146 | sigmaborov | 0.019690 | 0 |
| 842 | 29.520815280171 | malyshevdanil | 0.018663 | 0 |
| 491 | 22.684143606359 | penguin069 | 0.014217 | 0 |
| 367 | 19.687652890047 | nilanjansaha123 | 0.016796 | **+4.9e-03 behind bank** |
| 901 | 30.520815280171 | penguin069 | 0.018663 | 0 |
| 803 | 28.815051656904 | alexchilton | 0.021108 | **+3.9e-03 behind bank** |
| 969 | 31.624490853785 | sigmaborov | 0.018920 | 0 |
| 747 | 27.810663454806 | sigmaborov | 0.016904 | **+3.9e-04 behind bank** |
| 804 | 28.827154349934 | rosswade | 0.017094 | 0 |
| 962 | 31.520815280172 | penguin069 | 0.018663 | +2.0e-13 |
| 843 | 29.535533905933 | penguin069 | 0.017290 | 0 |
| 333 | 18.771328504181 | sigmaborov | 0.011314 | **+6.7e-04 behind bank** |
| 456 | 21.846667192844 | penguin069 | 0.012450 | 0 |

At **12 of the 16 the best public artefact equals the bank to ≤2e-13**; at the remaining 4
(367, 803, 747, 333) it is *behind* the bank. Nothing gets closer than the bank anywhere. The
union of the whole public coordinate corpus **is** the bank at these indices.



### 4.1b The stronger test: the bank already dominates the public corpus at *every* n

Rather than only asking "is any source better at my 16", I also asked "is any source better at
*any* of the 1000", on the full submissions pulled before the K14 sweep:

| source | puzzles where it beats the live bank by >1e-9 (out of 1000) |
|---|---:|
| `asteriospanoras/squares-in-squares-best` (22.132015818) | **0** |
| `alexchilton/fault-line-dp…` `c0.csv` (22.132020) | **0** |
| `alexchilton/fault-line-dp…` `cq.csv` | **0** |
| `areebbb/squares-in-squares-the-last-1e-9` | **0** |
| `jazivxt/boxed-in-sub` | 1 — n=2, and it is a *malformed* row (L = 1.8536 < 2 is impossible for two unit squares), not a packing |

This is the strongest form of the negative: the live bank is the pointwise minimum of the public
coordinate corpus, so a public artefact cannot hold any of the 16 leaderboard sides. It also
independently confirms the round-1 conclusion that the Kaggle per-puzzle record is a *different*
object from the public coordinate corpus.

Public-source inventory seen by `areebbb`'s own scan log (38 distinct full-size sources; best
totals): `alexchilton/fault-line-dp…22.13202`, `rosswade/jammed-squares…22.13204`,
`asteriospanoras…22.13335`, `penguin069/{fresh-lattice,public-changed-grain}…22.13339`,
`sigmaborov…22.13351`, `alexchilton/squares-101…22.13351`, `penguin069/{changed-grain-hardening,
whole-packing-warp,learned-birth-chains,public-neural-recovery}…22.1337`,
`kmmmvs/squares-public-merge-daily 22.13437`, `lucifer19/think-select-reclose 22.13506`,
`grennwolf/top-1-santa 22.13517`, `amirhezekiahespanto/debut 22.13518`,
`malyshevdanil/living-atlas 22.13529`, `avazaku/* 22.137`, `navneetprabhat…22.137`,
`samanyu1808/sis-submit 22.158`, `prvsiyan…22.163`, `nilanjansaha123…22.163`,
`evgendvorkin…22.1748`, `jonathan1506…22.1757`, `lianlian99…22.1774/22.179`,
`busyaprime…22.1946`, `mzishran…22.1959`, `kirilltym…22.2155`, `jazivxt/boxed-in-sub 26.7225`.
**Every one is worse in total than our bank, and none contained a better side at any of the 16.**

### 4.2 GitHub

| # | Query | Platform | Result |
|---|---|---|---|
| G1 | `square packing records` (sort=updated) | GitHub repo API | only Mishapolk (already imported) |
| G2 | `n842 square packing`, `square-packing 328`, `s(842) packing` | GitHub repo API | **0 results each** |
| G3 | 755 round-2 repos, regex over name+description for all 16 n | local index of round-2 `gh/repos.json` | 0 real hits (2 false positives on usernames `archowdhury328`, `RAH333`) |
| G4 | `RAH333/squares-in-squares-optimization` | clone | 240 KB, script + README only, **no data** |
| G5 | `repo:jlevy/squares s(842)`, `s(328)`, `n = 842`, `902 OR 963 OR 908` | GitHub **issue** search | nothing for these n; hits are Mishapolk #732 (328–10000, already imported) and Muglich #686 (328–998, already imported) |
| G6 | `pjmathematician` user search | GitHub users API | 0 accounts — they are Kaggle-only |
| G7 | `franciscouzo/square-packing` | `git clone --depth 1` | timed out at 300 s (repo too large); round-1 already scanned the full `certified_bounds.json` = 0 wins |
| G8 | Literal-string **code** search (`"29.502152708"`, `"n=328"`, `"s(842)"` across GitHub) | GitHub code search API | **not possible**: code search requires authentication and no `GITHUB_TOKEN`/`gh` exists in this environment. grep.app (Vercel checkpoint), searchcode.com (410/404) and `github.com/search` HTML (timeouts) all refused. This is the one gap in coverage — see §7 |

### 4.3 Web

| # | Query | Result |
|---|---|---|
| W1 | `"29.5021527" square packing` | only `squaremath.org/cases/29.html` (n=29, unrelated), MathWorld, Ostashev, leapsinbounds — **no hit on the decimal** |
| W2 | `"18.599535" squares in square` | only geo-coordinate false positives |
| W3 | `"22.669926930" OR "18.760014153" OR "31.605570898"` | only MathWorld / wand125 / Friedman — **no hit** |
| W4 | `"30.514078774" OR "31.514078774" OR "28.793943440"` | only lat/long converters — **no hit** |
| W5 | `kaggle "squares in squares" solution first place github notebook` | surfaced the per-puzzle leaderboard notebook, `grennwolf/top-1-santa`, `mdmuqtadirfuad/certified-method`, `DigitalEuan`, `Shubin123/unitSquares` |
| W6 | `square packing "n=328" unit squares best known side` | jlevy `muglich-issue686` (328–998 certificates — already imported), squares project profiles |
| W7 | `"Cats and boxes" kaggle "squares in squares" pjmathematician` | **the key hit**: `jlevy/squares` #929/#930/#936/#928 comments + `squaremath.org/cases/299.html` stating the entries are side-only and unpublished |

### 4.4 Papers / data repositories

| # | Source | Result |
|---|---|---|
| P1 | arXiv API `all:"packing unit squares"`, newest 15 | 2609.37410 (rectangle bound), 2412.21017, 2404.09835, 1603.02368 — none carries finite-n coordinates for n>324 |
| P2 | Zenodo `"square packing"`, 12 newest | see P3–P5 |
| P3 | Zenodo 23714459 — *Packing k²−⌈√(32k)⌉−1 unit squares in a square of side less than k* (Fang, 2026-10-27) | proof that `s(k²−⌈√(32k)⌉−1) < k`; certificates only for 38 values of k, k300/k600. The only n of ours this family reaches is **456 (k=22)**, and it proves only `s<22`, i.e. worse than our 21.8342. **No use** |
| P4 | Zenodo 23819397 — *Filled-end two-band L packings … 5134 certified upper bounds, n = 1182–9946* | **out of range**, no n ≤ 1000 |
| P5 | Zenodo 21938978 — *Counterexample to Erdős's f(k²+1)=k (Problem #106)* | sides like `6 + 193/514959` for 37 squares are **area-impossible** for unit squares ⇒ a different problem. **No use** |
| P6 | OSF API `"square packing"` | HTTP error / non-JSON (blocked) |
| P7 | figshare API | **403 Forbidden** (blocked) |
| P8 | OEIS `id:A005842` | confirmed again: minimal integer m holding squares of sides **1…n** (distinct consecutive squares term). Not our problem |
| P9 | OEIS numeric search `18.599535`, `29.5021527` | "No results" (OEIS is integer-only; decimals can never match) |
| P10 | `square-packing.franciscouzo.com` | TCP failure from here (000); its repo index is the same data round 1 scanned |

### 4.5 Corpora the brief named, and where they stand

* **Individual-puzzle repos** (`dpre4ai__n90-square-packing`, `ebdeleeuw__square-packing-n70`,
  `BalthasarStrauss__Squares-packing_S-29-_New-Record`, …): the round-2 `repos/` tree already
  holds 42 of them. Searching for *our* n in repo names/descriptions across the 755-repo index
  gives **0**; no single-puzzle repo for 328/842/902/… exists. The named example repos are all
  small n (29, 70, 90, 68, 156, 172, 179, …).
* **Numeric fingerprint**: searched on web (W1–W4) and OEIS (P9). Nothing.
* **Competition-adjacent**: done thoroughly — K1–K14, W5–W7. Best public LB anywhere is 22.134
  (`asteriospanoras`), i.e. behind the bank; the leaderboard and the per-puzzle table are
  public, the coordinates are not.
* **Papers with supplementary coordinate tables**: P1–P7. None for n>324 except Mishapolk/Couzo/
  Muglich, all already imported.
* **Erich Friedman / Packomania / OEIS**: P8, P9; round-1 conclusion stands and was re-verified
  for these n only.

---

## 5. Two traps worth recording for the next round

1. **`per_n_gap.csv` `src` column is not trustworthy.** `areebbb`'s notebook attributes the
   frontier side at 13 of our 16 n to `datasets/asteriospanoras/squares-in-squares-best` with the
   log line `frontier (union of all teams' per-size bests): 22.050884`. But the current version
   of that dataset has `29.520815280171444` at n=842 (our bank's value), not `29.5021527079`.
   Reading its `src` literally sends you on a 13-puzzle wild goose chase. The dataset was
   re-uploaded between the two reads (its own README shows two different self-scores,
   22.134373451549 and 22.132015818), and an older version evidently shipped a *leaderboard*
   table as if it were its own `per_n_L.csv`.
2. **22.050884 is not a public-artefact union.** `areebbb`'s "frontier" total equals
   `perpuzzle_best_20261111.csv` to 6 decimals, which is why it looks like proof that the
   coordinates are public. It is not: the union total was inflated by ingesting a copy of the
   side-only leaderboard CSV as a "sizes" source. The real public-artefact union is no better
   than the bank, consistent with the bank having absorbed every public donor. **Do not treat
   `22.050884` as reachable.**

---

## 6. What the 16 actually cost, and the cheapest real route

The 16 are **13 distinct constants**, not 16:

| constant | n it lifts | Δscore if reconstructed |
|---|---|---|
| `f = 0.5021527079` (D=1, k+  f) | **842, 901, 962** | **1.867e-3** |
| `f = 0.5140787741` (D=2) | **902, 963** | **1.406e-3** |
| `f = 0.5182442831` (D=2, k=29) | 843 | 5.955e-4 |
| `f = 0.5995354648` (D=4) | 328 | 8.190e-4 |
| `f = 0.6058845086` (D=8) | 908 | 6.534e-4 |
| `f = 0.6055708986` (D=8, k=31) | 969 | 6.078e-4 |
| `f = 0.6699269304` (D=7) | 491 | 6.416e-4 |
| `f = 0.6708567970` (D=6) | 367 | 6.231e-4 |
| `f = 0.7939434402` (D=19) | 803 | 6.091e-4 |
| `f = 0.7937596571` (D=18) | 747 | 6.041e-4 |
| `f = 0.8100605854` (D=20) | 804 | 6.029e-4 |
| `f = 0.7600141531` (D=9) | 333 | 5.831e-4 |
| `f = 0.8342175869` (D=15) | 456 | 5.830e-4 |

Evidence that 842/901/962 are one liftable gadget (not three coincidences): the ΔL values agree
to **2e-12** (`0.018662571941`, `0.018662572264`, `0.018662572740`), and Oct 29's leaderboard
shows 901 and 962 carrying a *different* shared value before being replaced. Adding a row+column
to a `k+f` packing gives `(k+1)+f` with `+2k+1` squares, which is exactly the 842→901→962 step.

Our bank's existing D=1 gadget is `f = 0.52081528` (the published Ellsworth construction, used at
k=25…31). The record is only **0.01866 better than ours** — this is a *relaxed variant of the
same anatomy*, not a new topology. The rank-1 team's own words describe the move: enlarge the
tilted region and let its angles float (~14–21 distinct values) instead of one rigid band angle.

**Recommendation for the orchestrator.** Stop searching for these 16 externally; the coordinates
do not exist outside the record holder's private runs. Spend the effort on the generative
strategy the campaign already owns: take the bank's D=1 corner gadget at 842, replace the single
hard-coded band angle with a free per-square angle block, and relax. One success is worth
1.867e-3 — larger than the entire round-1 Mishapolk import (+1.040e-3).

---

## 7. Coverage gap (honest statement)

One capability was unavailable and it is the only place a literal-string match could still hide:

* **GitHub code search** (searching file *contents* across all of GitHub for `29.502152708`,
  `n=842`, `s(842)`, …) requires an authenticated token. This environment has no `GITHUB_TOKEN`
  and no `gh` CLI, and the unauthenticated public alternatives all refused: grep.app → Vercel
  security checkpoint, searchcode.com → 404/410, `github.com/search?type=code` → login wall,
  `github.com/search?type=repositories` HTML → connection timeout.
  Repository-name/description search (755 repos), README-targeted search (round 2's `repos2.json`)
  and issue search were all available and returned nothing for these n.

Everything else in the brief's list was executed and is recorded above.

---

## 8. Artifacts

```
/tmp/campaign2/targeted/REPORT.md                  this file
/tmp/campaign2/targeted/scan_sources.py            automated artefact scanner (44 sources, 4 shards)
/tmp/campaign2/targeted/retry_sources.py            retry for the 7 large notebooks (3000 s cap)
/tmp/campaign2/targeted/scan/results*.tsv          per-source result rows (n → L, wins)
/tmp/campaign2/targeted/scan/retry_*.tsv           retry rows
/tmp/campaign2/targeted/ko/{boxedin,areebbb,chilton,ross,maly}/   notebook outputs pulled
/tmp/campaign2/targeted/ds/{asterio,lostd}/        dataset contents
/tmp/campaign2/targeted/ds/lostd/perpuzzle_best.csv   the side-only leaderboard, with team+date
/tmp/campaign2/targeted/lb/squares-in-squares-publicleaderboard-2026-11-17T18:48:51.csv
/tmp/campaign2/targeted/pjm/three-square-packings-that-beat-the-records.{ipynb,log}
/tmp/campaign2/targeted/pjm_packings.csv           rank-1 team's 3 public packings (all behind bank)
/tmp/campaign2/targeted/kpull/squares-in-squares-per-puzzle-leaderboard.ipynb   provenance proof
/tmp/campaign2/targeted/evidence_quotes.md         verbatim quotes from jlevy#929 etc.
/tmp/campaign2/targeted/rah333/                    checked, no data
```

Reproduction of the per-puzzle comparison (this is the whole check; it is cheap):

```sh
cd /Users/zhaohuaxiang/ccjjllt/squares
.venv/bin/python - <<'PY'
import pandas as pd
T=[328,902,963,908,842,491,367,901,803,969,747,804,962,843,333,456]
bank=pd.read_csv("/tmp/best_bank/submission.csv")
b={n:max(g.x.max()-g.x.min(),g.y.max()-g.y.min())+1.0 for n,g in bank.groupby("n")}
d=pd.read_csv("/tmp/campaign2/targeted/ds/asterio/submission.csv")   # or any scanned source
c={n:max(g.x.max()-g.x.min(),g.y.max()-g.y.min())+1.0 for n,g in d.groupby("n")}
print([n for n in T if b[n]-c[n] > 1e-9])     # -> [] for every source tested
PY
```

`/tmp/best_bank/submission.csv` was never modified. Nothing was submitted to Kaggle.
