# External open-source mining — squares-in-squares (2026-11-18)

Track: non-Kaggle mathematical literature, catalogues, GitHub and fora.
No Kaggle kernel used. Local work = downloads, format conversion, certification only.

## TL;DR

**One source wins: `Mishapolk/square-packing-records` (GitHub).**
Its exact-rational certificates give **6 puzzles** strictly below the live bank:

| n | bank L | new L | ΔL | Δscore |
|---:|---:|---:|---:|---:|
| 210 | 14.973001116587651538 | 14.971214601727902860 | 1.786515e-03 | 1.232812e-04 |
| 260 | 16.633520950169838670 | 16.633520939996095933 | 1.017374e-08 | 6.309487e-10 |
| 262 | 16.707106781186563893 | 16.698115018856373837 | 8.991762e-03 | 5.555129e-04 |
| 272 | 16.965586474837710540 | 16.965501175989871285 | 8.529885e-05 | 5.172002e-06 |
| 292 | 17.590016442846415856 | 17.590016439395991910 | 3.450424e-09 | 2.019208e-10 |
| 295 | 17.704232790736071479 | 17.698115018866374726 | 6.117772e-03 | 3.561904e-04 |

**Net gain vs live bank: +1.0401574539622427e-3**
(bank 22.129481982260582 → candidate 22.128441824806618).

Certificate sides before dilation (the true source `L`): n=210 → `14.971214601588191`,
n=260 → `16.633520939839762`, n=262 → `16.698115018699394`,
n=272 → `16.965501175830216`, n=292 → `17.590016439230091`,
n=295 → `17.698115018699394`. The `new L` column above is the 1e-11-dilated value that
both scoring routes accept.

Dual-route certified, **1000/1000 valid on both `text` and `float64`**:

- Candidate: `/tmp/campaign2/external/merge_final/submission.csv`
  SHA-256 `9c981e6ea9a44c076587256936948e636936a84ad0668af6b75e946f4fa527e9`
- Merge report: `/tmp/campaign2/external/merge_final/merge_report.json`
  SHA-256 `79ce973442fe521ea3f42bc0a451357d420cc2f995e2cf5a7d8df520e0b828e6`
- Official score report: `/tmp/campaign2/external/score_final/report.json`
  SHA-256 `e0d0155ac3f2c32e7a2fa6d30c8ed49f3dc0e24264a4a83547b651b7b6bc1ee3`
  - `text`    **22.128441824806618**, valid 1000, invalid_submitted 0, missing 0
  - `float64` **22.12844182480662**, valid 1000, invalid_submitted 0, missing 0

The candidate was merged against bank SHA-256
`19877e21aeb728221bbcb9fb53e3e47ac2dca027180f378b84c351aabfd8cf43`
(score `22.129481982260582`, read from `/tmp/best_bank/report.json` at merge time).
**The bank moves continuously — re-run the merge before consuming this.**

The rest of the literature/code space is uniformly behind the Kaggle bank. That is the
second result of this report: outside Kaggle, only one source produced a net win over the
bank after cross-source dominance — Mishapolk (2026-11-16). Its only near-competitor,
JoostdeWinter, found two of the same puzzles but at strictly larger sides. Every other
catalogue tested is at or below the bank.

---

## 1. Winning source: Mishapolk / Mykhailo Polkovskyi

Repo: <https://github.com/Mishapolk/square-packing-records> (pushed 2026-11-16T23:32Z)
Index: `certified_bounds.json` generated `2026-11-16T23:31:54Z`, `max_n=10000`.

Format of each certificate (`certificates/0000-0999/nNNN.cert`):

```
n S
x y t        (one line per unit square)
```

- `S` and all coordinates are exact rationals; `x,y` are square centres in the closed
  container `[0,S]^2`; `t = tan(theta/2)` with `cos θ=(1−t²)/(1+t²)`, `sin θ=2t/(1+t²)`.
- Verified with the repo's own exact verifier `verify_bound_certificate.py` (stdlib
  `fractions`, 50-digit-equivalent exact arithmetic). All six printed
  `"valid": true, "strict_valid": true, wall_margin_sign: 1, pair_margin_sign: 1`.
- SHA-256 of each downloaded certificate matches the `certificate_sha256` recorded in
  `certified_bounds.json`:

| n | certificate SHA-256 |
|---:|---|
| 210 | `a8c474129b3f432390bb33f4e7818ecf4d11650cd3acda9091584d65120683b4` |
| 260 | `b059dfa9d855aa14b04635ca1d4ea7d01d8171b64b7c5e21a02bb3914124654f` |
| 262 | `c5ff84393899ddd099f2c987ea73d7e82f3a65e9136afb9bdc3282a06b3c19bd` |
| 272 | `0cd6d68332f84a8856cb47a2f0bfc36116901e6b200dc6041a54fe5552f68778` |
| 292 | `bc044512137a02bcf4024898844760b65215984883f1d1f9f42ac65aa540a57b` |
| 295 | `7778560e076f207db1913635e1148607011b80e6a0aa96dd614049613abf2cc5` |

All six are credited in the index to *Mykhailo Polkovskyi (Mishapolk)* and are ordinary
records in `certified_bounds.json` (`kind: "certificate"`), not derived/deletion bounds.

### 1.1 Why a dilation was needed (important for any future import)

The exact certificates are valid at rational precision but their clearances are far below
float64 epsilon. Written out verbatim, the **text** route accepts them and the **float64**
route rejects them with `infeasible: Squares overlap (certified)` — exactly the failure the
brief warns about. The first merge attempt against a verbatim transcription changed only
n=292 for that reason.

Format conversion applied (deterministic, **not** an optimisation): a uniform dilation of
centres about the container centre,

```
x' = S/2 + (1 + 1e-11)·(x − S/2),   y' = S/2 + (1 + 1e-11)·(y − S/2)
```

with angles unchanged. This costs ~1.5e-10 in L per puzzle (see the per-puzzle table
above; the smallest bank gap, n=292 at 3.45e-9, still survives with a 20× margin) and
raises the minimum float64 clearance to ~1e-10. Both routes then certify.
The raw (undilated) rigid transform of the certificates is kept in
`/tmp/campaign2/external/candidate_mishapolk.csv` for provenance; the certified file is
`/tmp/campaign2/external/candidate_mishapolk_d11.csv`
(SHA-256 `c1f68c6711aabb9431c191cbcc41f02fce824788cdeb163dfddd91f0c3debd99`).
A compact 6-group diff, `/tmp/campaign2/external/candidate_mishapolk_diff.csv` (1591 rows),
re-merges to the **bit-identical** submission (same SHA-256 `9c981e6e…`); use it if the
bank has drifted since this report.

### 1.2 Position vs the Kaggle per-puzzle snapshot (context, not a complaint)

`data/references/leaderboards/perpuzzle_best_20261111.csv` (total 22.0508835713) is still
better than the new candidate at some of these n:

| n | new L | Kaggle snapshot L | relation |
|---:|---:|---:|---|
| 210 | 14.9712146017 | 14.9712106325 | snapshot 4.0e-6 better |
| 260 | 16.6335209400 | 16.6335209503 | **candidate 1.0e-8 better** |
| 262 | 16.6981150189 | 16.6981150187 | equal (candidate +1.6e-10) |
| 272 | 16.9655011760 | 16.9655011759 | snapshot 1.2e-10 better |
| 292 | 17.5900164394 | 17.5890539434 | snapshot 9.6e-4 better |
| 295 | 17.6981150189 | 17.6980429294 | snapshot 7.2e-5 better |

So this win is **against the live bank**, which was behind the record at these puzzles.
It is not a claim that these are new world records. At n=262 the Kaggle record is exactly
the Mishapolk value, i.e. the same packing is already in the public record; we recovered
its coordinates.

### 1.3 Other checks on Mishapolk

- `certified_bounds.json` for all n≤1000: exactly these 6 wins; 591 ties, 403 behind.
- The 108 certificate files in `certificates/0000-0999/` that are **not** registered as
  `kind: "certificate"` (n=5,10,11,…,324: exact certificates of the catalogue packings)
  were downloaded and compared separately: **0 wins**, 93 ties, 15 behind.
- `certificates/manifest.json` (n=328..10000, 390 entries with n≤1000): **0 wins**.
- `upper_bounds.json` verified field is stale relative to `certified_bounds.json`
  (e.g. n=262 still shows 16.707106781187); use `certified_bounds.json`.

---

## 2. Source ledger — everything consulted

Legend: “coverage” = n covered in 1..1000; “result” = per-puzzle comparison against the
live bank (EPS 1e-11 on L unless stated).

| # | Source | What it is | Coverage | Result |
|---|---|---|---:|---|
| 1 | **Kingbird catalogue** (Ellsworth, ex-Friedman) `kingbird.myphotos.cc/packing/squares_in_squares.html` + triangular table + compared page | best-known sides, SVG constructions, polynomial sides | 1–324 pictured; specials 626,1453,1765,1850,2043 | 0 wins; 132 exact ties, 78 behind (210 numeric entries) |
| 2 | **jlevy/squares** (The Squares Project, `squaremath.org`) | Witness/v2 YAML with exact coordinates, n=1..324; frontier results; expanded bounds 325..1024 | 1–324 + 325–1024 derived | 0 wins; 324 witnesses match bank to ≤5.3e-14; expanded bounds also 0 wins |
| 3 | **franciscouzo/square-packing** | `certified_bounds.json`, `known_best.json`, `upper_bounds.json`, 6958 files, per-n certificates | 1–10000 | 0 wins (600 ties, 400 behind); “verified” certificates also 0 wins |
| 4 | **Mishapolk/square-packing-records** | 5467 exact rational certificates | 328–10000 + imported small-n records | **6 wins, +1.040157e-3** |
| 5 | **JoostdeWinter/square-packing** | 12 small-n packings, 15 above-324, 22 “above324_refined” against Kaggle, 2 from n=297 | 90–991 | 0 additional wins after Mishapolk; bank equal at 132,157,172,199,297,332,409 (~5e-14), better at 90,227,229,260; Joost beats the bank at 262,295 but Mishapolk beats it further |
| 6 | **TheSnakeFang/squarepack-certs** | 230 glued composites + 17 direct square packings, exact certificates | 306–1125 | 0 wins; composites behind by ≥1.3e-2, direct packings by ≥2.2e-3 |
| 7 | **JonathanGun/square-packing-upper-bounds** | 5 exact witnesses (n=127,204,232,264,305) improving Tomáš Kodaj Kaggle packings | 127–305 | 0 wins; closest n=204, bank better by 1.6e-10 |
| 8 | **itsnaka/squish-certs** | 435 SQUISH certificate files | small n | imported in #3; 0 wins |
| 9 | **ry-xu/square_packing** | 25 exact certificates n=51..295 | 51–295 | imported in #3; 0 wins |
| 10 | **evand/square-packing** | Atlas / exact solver; already used by campaign | 1–324 | no new data beyond #1/#2 |
| 11 | **Karimi (Zenodo + Preprints 202610.2669)** | `filled_records.csv` n=1182–9946; preprint “window bound, 5308 improved bounds” n=1182–9944 | 1182–9946 | **out of range**, no n≤1000 |
| 12 | **forloopcodes/least-space-squares** | closed-form construction library + numeric polishing | all n (generated) | constructions are the literature family; not a record source (not executed) |
| 13 | **Kaggle-competitor GitHub repos** (DigitalEuan, Minuii, cubres, TobiasHFS, corentinlaudicina, munimtechnologies, Shubin123, omerfisler, rushikesh648) | pipelines / submissions | 1–1000 | two published CSVs scanned: DigitalEuan 22.21806, Minuii 22.25699, **0 per-puzzle wins**; others have no large data artifacts |
| 14 | **OEIS** | A005842, A092137, A003059, A360610, … | — | no sequence of best-known non-integer sides. A005842 is *distinct* squares 1..n (different problem); A003059 is ceil(√n); A092137 lower bounds only. Nothing usable |
| 15 | **Packomania** | circles in square/rectangle/circle, spheres in cube | — | no unit-square-in-square packings; nothing usable |
| 16 | **arXiv / journal** | Friedman EJC DS#7 survey (2009); McClenagan arXiv:2602.01484; Bui arXiv:2508.04603; arXiv:2610.22622 & 2610.28504 (axis-parallel 7/8); Karakuş 2026 lower bounds | ≤100 (survey) / asymptotic | survey behind (n≤100); 2026 papers are asymptotic or axis-parallel small-n; lower bounds carry no coordinates |
| 17 | **StackExchange / code-golf / Reddit / MathWorld** | n=11 Math.SE thread; code-golf tiling/perfect-square threads; Reddit announcement of the 1–324 expansion | small n | no explicit construction beating the bank; n=11 is proven optimal (bank = optimum). Reddit thread only announces the catalogue |
| 18 | **Wikipedia “Square packing”, MathWorld** | summary tables n≤20-ish | small n | behind / same proven optima |
| 19 | **griffcass/square-packing** | 39 SLP-polished packings n=103..307, catalogue-format coordinates, 50-digit verified | 103–307 | 0 wins; closest n=152, bank better by 5.0e-9; n=106 bank better by 2.9e-5 |

---

## 3. Evidence detail — why the rest is “behind” rather than “not checked”

### 3.1 Kingbird / Ellsworth catalogue (the canonical literature table)

Parsed the triangular table into 210 numeric entries (n=1..324, plus 626, 1453, 1765, 1850,
2043). Comparison against the bank:

```
entries 210 : wins 0, exact ties 132, behind 78
closest behind: n=68   bank 8.79879523721829  cat 8.79879614026010  (9.03e-7)
                n=110  bank 10.99678339663160 cat 10.99679327401957 (9.88e-6)
                n=266  bank 16.82302875075649 cat 16.82306208283780 (3.33e-5)
```

Where the catalogue is behind, the Kaggle bank has already polished the same construction
(the gap is typically 1e-7…3e-2, not a different topology). The catalogue's own
“alternative/older” page (`squares_in_squares__compared.html`) was parsed for all 34
tables it contains (n=10..89): 0 wins, 27 ties, 7 behind.

Special large-n alternative packings (`square-NNN_r1*.svg`), parsed with Ellsworth's own
`parse_svg_packing.py` at 20 digits:

| n | construction source | literature s | bank L | verdict |
|---:|---|---:|---:|---|
| 446 | `square-446_r1.svg` | 21.6571944495 | 21.6230652121 | behind 3.41e-2 |
| 682 | `square-682_r1b.svg` | 26.6213203436 | 26.6087125784 | behind 1.26e-2 |
| 791 | `square-791_r1.svg` | 28.7284733482 | 28.6087125784 | behind 1.20e-1 |
| 968 | `square-968_r1b.svg` | 31.6213203436 | 31.6058838815 | behind 1.54e-2 |
| 626 | main catalogue | 25.5208152802 | 25.5208152802 | exact tie |

This also kills the obvious hope that the literature's large-n “diagonal strip/Göbel”
constructions might beat Kaggle at n>324: they are 1e-2…1e-1 behind.

### 3.2 jlevy/squares == the bank for n≤324

Parsed all 324 `packing/witnesses/known-best/n-NNN.yaml` files, including algebraic-number
sides (root of `minimal_polynomial` inside `isolating_interval`, evaluated as
`Σ c_i λ^i`). Result:

```
324 parsed : wins 0 ; largest |bank − witness| = 5.3e-14
closest: n=297, 304, 290, 291, 308 all agree to ≤5.3e-14
```

This is the strongest single piece of evidence that the bank **is** the 2026 Squares Project
frontier for n≤324, not merely close to it. The project's `expanded_reference_bounds.json`
(construction 325..1024 derived from the 324 catalogue) was also parsed: **0 wins**.

### 3.3 franciscouzo — 1000 entries, zero wins

`certified_bounds.json` (generated 2026-10-28, max_n=10000):

```
n≤1000: 0 wins, 600 exact ties, 400 behind
```

`upper_bounds.json`, using only the `verified` field (i.e. `certificates/best/nNNN.cert`),
not the `reported` field:

```
0 wins, 614 ties, 386 behind
```

`known_best.json` (435 entries n≤1000, imports squish + ry-xu): **0 wins**.

Note on `upper_bounds.json`'s `reported` field: it mirrors the Kaggle per-puzzle
leaderboard. Taking `min(verified, reported)` superficially produces “71 wins”, but every
one of those is the known headroom to the Nov-11 Kaggle snapshot, and **0** of them beat
`perpuzzle_best_20261111.csv`. They are side lengths without coordinates and contain no
new information.

### 3.4 JoostdeWinter — fresh, but already absorbed

54 certificate/pose files parsed (51 unique n: 40 `.cert` + 14 `*_exact.json`, with n=227,229,260 in both), all with exact rational sides:

```
0 additional wins after the Mishapolk candidate
bank == Joost to ≤5e-14 at n = 132, 157, 172, 199, 297, 332, 409
bank better at n = 90 (2.7e-11), 227 (1.7e-4), 229 (1.3e-5), 260 (1.2e-2)
Joost is better than the bank at n=262 (+7.4e-3) and n=295 (+4.5e-3);
    both are superseded by the Mishapolk certificates used here.
```

His `above324/` (15, n=413..910) and `above324_refined/` (22, n=597..991, explicitly
“refines public Kaggle packings”) are all behind the bank. The closest anywhere in the
repo are n=229 (+1.3e-5) and n=227 (+1.7e-4), both small-n folders.

### 3.5 TheSnakeFang composites

230 exact glued packings (`composites/table.csv`), of which 22 land in 1..1000, plus 17
direct packings. Every one is behind, most by ~1e-2…6e-2 (the construction is a
theorem-driven worst-case family, not a record hunt). The best in-range composite is
n=994, behind by 5.8e-2; the closest direct packing is n=308, behind by 2.2e-3.

### 3.6 JonathanGun

Five exact witnesses. All behind the bank, two only at the 1e-10 level:

| n | bank | JonathanGun | bank − src |
|---:|---:|---:|---:|
| 127 | 11.800829570323 | 11.801753890487 | 9.24e-4 |
| 204 | 14.802646842951 | 14.802646843107 | 1.56e-10 |
| 232 | 15.759531623540 | 15.759531627557 | 4.02e-9 |
| 264 | 16.773807597984 | 16.773807598002 | 1.83e-11 |
| 305 | 17.945762359468 | 17.945762359659 | 1.91e-10 |

The bank has already absorbed Kodaj's public Kaggle packing plus a further polish at these n.

### 3.7 OEIS details

- **A005842** — “minimal integer m such that an m×m square contains non-overlapping squares
  of sides 1, …, n”. This is the *distinct consecutive squares* problem, **not** n unit
  squares; unusable.
- **A092137** — lower bound for this problem (`ceil(sqrt(n))` family); no constructions.
- **A003059** — `ceil(sqrt(n))`; the trivial grid.
- **A360610** — axis-parallel counts; its own note says better packings exist when rotation
  is allowed, and points at Friedman.
- No OEIS sequence carries the non-integer best-known sides (OEIS is integer-valued), and
  none carries coordinates. Nothing to import.

### 3.8 Forums / papers

- Math.SE “Eleven unit squares inside a larger square” — n=11 is solved (Trump 1979,
  Stromquist 2003); bank is at the proven optimum `3.877083590022814…`.
- Code-golf threads found are different problems (tiling 1/n×(1/(n+1)) rectangles, perfect
  squared squares, consecutive-square packing), not n equal unit squares with rotation.
- Reddit r/math thread only announces the catalogue expansion 1–100 → 1–324.
- Friedman EJC survey DS#7 (2009) covers n≤100; every value is ≤ the 2026 catalogue.
- arXiv 2602.01484 (McClenagan) and 2508.04603 (Bui): asymptotic `O(x^{3/5})` waste, no
  finite-n coordinate tables.
- arXiv 2610.22622 / 2610.28504: exact formulas for **axis-parallel** packing of 7 and 8
  squares. Our bank is already at the corresponding optima (n≤10 exact).
- Karakuş 2026 and the Squares Project lower-bound programme: lower bounds only, no
  coordinates. (They would matter for proving optimality, not for improving L.)

---

## 4. What this means for the campaign

1. **Stop looking outward for n≤324.** The bank equals the live 2026 catalogue to ≤5.3e-14
   at all 324 n. There is no separate “mathematical literature” frontier to import there.
2. **The only external seam found is freshly published certificates at small/mid n.**
   Mishapolk's repo (Nov 16) is the sole live source; its wins this round were all at
   n=210–295 even though its catalogue spans 328–10000, because the bank has already
   absorbed the 325–1000 records (Joost, JonathanGun, SnakeFang, franciscouzo all show
   bank ≥ source). Check Mishapolk's `certified_bounds.json` again before each future
   round — it is regenerated frequently and was the only winning file this round.
3. **The real frontier remains the Kaggle per-puzzle record** (snapshot total 22.0508836,
   candidate total 22.1284418). External literature cannot close that gap; at 4 of the 6
   wins the Kaggle record is still better and only the coordinates are missing.
4. **Do not revisit:** Kingbird, jlevy/squaremath, franciscouzo, JoostdeWinter,
   TheSnakeFang, JonathanGun, squish, ry-xu, evand, Packomania, OEIS, Karimi (n≥1182),
   Friedman survey, arXiv asymptotic/axis-parallel papers, the fora listed above.
5. **Reusable lesson:** exact rational certificates with ~1e-20 clearances need a
   deterministic dilation (~1e-11 relative) before the float64 route accepts them. Budget
   ~1.5e-10 of L per puzzle for that, and check the smallest bank gap first.

---

## 5. Reproduction

```sh
cd /Users/zhaohuaxiang/ccjjllt/squares
.venv/bin/python -m squares merge \
  --baseline /tmp/best_bank/submission.csv \
  --baseline-report /tmp/best_bank/report.json \
  --candidate /tmp/campaign2/external/candidate_mishapolk_diff.csv \
  --output-dir /tmp/campaign2/external/merge_final --workers 4
.venv/bin/python -m squares score \
  /tmp/campaign2/external/merge_final/submission.csv --mode both \
  --output-dir /tmp/campaign2/external/score_final
```

Certificate verification (independent, exact rational):

```sh
python3 /tmp/campaign2/external/mish/verify_bound_certificate.py \
  /tmp/campaign2/external/mish/n262.cert
# -> {"valid": true, "strict_valid": true, "wall_margin_sign": 1,
#     "pair_margin_sign": 1, "accepted": true}
```

Artifacts:

```
/tmp/campaign2/external/candidate_mishapolk.csv        raw rigid transcription (text-route valid only)
/tmp/campaign2/external/candidate_mishapolk_d11.csv    dilated, both-route valid (full 500500-row candidate)
/tmp/campaign2/external/candidate_mishapolk_diff.csv   6-group diff, 1591 rows (recommended for re-merge)
/tmp/campaign2/external/merge_final/submission.csv     merged 500500-row submission
/tmp/campaign2/external/merge_final/merge_report.json
/tmp/campaign2/external/merge_diff/                    second merge from the diff (bit-identical output)
/tmp/campaign2/external/score_final/report.json        official dual-route report
/tmp/campaign2/external/wins_mishapolk.csv             the 6 rows: bank/new/Δ/Δscore/snapshot
/tmp/campaign2/external/mish/n{210,260,262,272,292,295}.cert
/tmp/campaign2/external/jdw/                           JoostdeWinter clone (scanned)
/tmp/campaign2/external/jlevy_sparse/                  jlevy witnesses n=1..324 (scanned)
/tmp/campaign2/external/griffcass_repo/                griffcass 39 packings (scanned, behind)
```

`/tmp/best_bank/submission.csv` was never modified. Nothing was submitted to Kaggle.
