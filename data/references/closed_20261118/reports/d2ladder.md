# D = 2 ladder (k = 24…31, n = k²+2) — C++20 GA campaign

Status: **COMPLETE 22:52:59Z. Result: no candidate — 17/17 valid jobs, 0 legal
improvements, every D=2 side unchanged, certified gain 0.0.** Kernel
`ccjjllt/sis-d2-ladder-20261118` v1, pushed 21:25:26Z.

## 1. What is being attacked

The bank's D=2 column for n = k²+2 is the lifted n=291 two-core gadget, i.e.
`f = L − k = 0.535533906` at every k = 24…31. The public record's D=2 column is
strictly better from k=24 on:

| k | n | bank f | record f | Δf | Δ(L²/2n) = kΔf/n |
|---:|---:|---:|---:|---:|---:|
| 24 | 578 | 0.535534 | 0.534784 | 7.50e-4 | 3.11e-5 |
| 25 | 627 | 0.535534 | 0.531087 | 4.45e-3 | 1.77e-4 |
| 26 | 678 | 0.535534 | 0.523860 | 1.17e-2 | 4.48e-4 |
| 27 | 731 | 0.535534 | 0.523851 | 1.17e-2 | 4.32e-4 |
| 28 | 786 | 0.535534 | 0.521592 | 1.39e-2 | 4.97e-4 |
| 29 | 843 | 0.535534 | 0.518244 | 1.73e-2 | 5.95e-4 |
| 30 | 902 | 0.535534 | 0.514079 | 2.15e-2 | 7.14e-4 |
| 31 | 963 | 0.535534 | 0.514079 | 2.15e-2 | 6.91e-4 |

Total 3.583e-3 of score; 902+963 alone are 1.404e-3, and the six k≥26 puzzles are
3.375e-3, which is why the queue puts 902/963/843/786 first.

**The record column looks like two masters plus four singletons.** The record f is
*identical* at (26, 27) = 0.523860 and at (30, 31) = 0.514079, and the engine's lift
identity `n = k²+2` at `L = k+f` is exactly the gadget relation (w = h = k, D = 2).
So a single better master at n=678 would cover 731, and a single better master at
n=902 would cover 963 — those two finds alone are 2.284e-3 of the 3.583e-3 (64 %).
The remaining 1.30e-3 is the four singletons 786 (4.97e-4), 843 (5.95e-4), 627
(1.77e-4), 578 (3.11e-5). This is inference from the published f values, not from the
record's coordinates, but it is the strongest available targeting signal.

Unlike n=291 this column is **demonstrably reachable**: the record holder already sits
there. The engine cannot invent the record's construction, so the run is a search from
the bank's own (contact-jammed) lift seeds plus the engine's N±1 and lattice seeding.

## 2. Package

`kdir/` — self-contained Kaggle CPU kernel, no dataset, no internet:

* `kernel.py` 713 212 B = `kernel/self_template.py` with `MODE = "ga"`, `BUDGET_H = 1.5`
  and a D=2-only queue (below), plus **PAYLOAD** = `payload_d2.tar.gz` base64 (699 184 B).
* `payload_d2.tar.gz` 524 386 B = the verified C++20 engine tree
  (`src/`, `third_party/`, `tools/`, `schedules/`, `data/`, `Makefile`) **plus 24
  strictly-valid sqpack/1 seeds** in `best/`: the eight targets 578 627 678 731 786 843
  902 963 and their N−1/N+1 neighbours 577 579 626 628 677 679 730 732 785 787 842 844
  901 903 962 964. Seeds are `tool/bank_to_sqpack.py` conversions (side = certified bank
  L + ≤3.3e-11, meta carries `L_report`).
* `kernel-metadata.json` — id `ccjjllt/sis-d2ladder-20261118`, private, `enable_gpu:
  false`, `enable_internet: false`, no sources. Kaggle slugified the title, so the live
  ref is **`ccjjllt/sis-d2-ladder-20261118`**.

Queue (`MODE=ga`, 1 worker, `ga.threads = 4`, 280 s/job, 24 jobs queued):

| round | schedule | seed | order |
|---|---|---|---|
| 1 | `ga-explore.json` | 1 | 902 963 843 786 731 678 627 578 |
| 2 | `ga-seeded.json` | 1 | 902 963 843 786 731 678 627 578 |
| 3 | `ga-explore.json` | 2 | 902 963 843 786 731 678 627 578 |

Biggest record gap first in every round, so 902/963/843/786 always get budget before
the mid-k puzzles. 16 jobs fit inside the 4800 s runner window (280 s each); round 3
only starts if the box is faster than the deadline math assumes. `start.mirror` is
false in both schedules (verified in the JSON). The runner passes no `--neighbors`, so
the engine default `--neighbors best/` is active and the GA seeds islands from
`best/(N+1)` minus a square, `best/(N−1)` plus a square, and the grid/diagonal lattices.

## 3. Local smoke test (the exact payload)

Extracted `payload_d2.tar.gz`, built `make engine CXX=clang++`, then:

* `--check-schedule` ga-explore / ga-seeded → accepted (hashes `06ffed3cbd260456` /
  `45926bb07fdc2c6c`);
* `--N 578 --seed 1 --time 5 --schedule ga-seeded --start best/578.json
  --neighbors best` → output written, `tools/validate.py --n 578` **valid**
  (tight side 24.535533905956388, min pair gap 9.98e-13);
* seed itself validates strictly (`tools/validate.py best/578.json` → valid).

## 4. Local probe telemetry

### 4.1 Short probes (150 s, ga-explore, 10-core Mac, threads=4)

| n | generations | ratchets | legal improvements | best side | island costs (h) |
|---:|---:|---:|---:|---|---|
| 578 | 144 | 2 | 0 | unchanged 24.535533906 | 4/7 islands cost **0.0** at h = 24.535534, rest ≤ 4.2e-3 |
| 902 | 75 | 2 | 0 | unchanged 30.535533906 | 2 islands cost 2e-9 at h = 30.535503 (−3.1e-5), 1 cost 6.8e-3 |

Reading: at n=578 the lift seed is **feasible (cost 0) but cannot be shrunk even by
1e-6** — the same contact-jammed signature the 291 track measured. At n=902 the ratchet
descends ~3e-5 in 150 s on the best islands but never crosses into a legal improvement.

### 4.2 Long probes (900 s = 3.2× a Kaggle job)

| n | schedule | generations | ratchets | resets | legal improvements | h_final | h_final / first ratchet target |
|---:|---|---:|---:|---:|---:|---|---|
| 902 | ga-explore s3 | 607 | 27 | 64 | **0** | 30.535503370429 | `side·(1−1e-6)` **exactly** |
| 786 | ga-seeded s1 | 1191 | 36 | 150 | **0** | 28.529826799179 | `side·(1−2e-4)` **exactly** |

The 150 s and 900 s n=902 probes (75 vs 607 generations) return the **identical**
h_final to 15 digits. That is the decisive fact: `h_final` is not a reached side, it is
the *first ratchet target below the bank seed*, `side·(1−step)` — the GA never once
advanced past its first shrink attempt, on any island, in 900 s at either n.

Why: `ga.cpp` ratchets when the population cost is below `tol = 1e-9`, and with
`penalty = depth2` that admits penetrations up to `√1e-9 ≈ 3.2e-5`; the ratchet then
*sets the next target box* below that soft fit. The exact gate is `legalize()` and
`legal_improvements`, which stayed **0** in every run. The honest near-miss numbers are
therefore: 902's start/up islands reach cost 2.5e-9 (depth ≈ 5e-5) at their first target
and stop; 786's islands `down`/`lattice` ratchet from their own worse sources down to
the bank side and stop there (the population cost at the first target below the bank is
6.7e-3, i.e. depth ≈ 8e-2).

At n=578 the seed is *exactly* feasible (cost 0), and the very first adaptive step
(`eps` collapsed to its 1e-9 floor) already fails: h_final = `side·(1−1e-9)`. The lift
seed cannot absorb a **1e-9** shrink, let alone the 7.5e-4 the record needs at k=24.

Extrapolation: 902's soft ratchet did not advance at all between 150 s and 900 s, and
0 exact improvements occurred in 607/1191 generations. The record needs 2.15e-2 at that
n. `destroy` (1 beat-best in 900 s), `strip` (2) and `relocate` (0) — the only
topology-changing moves — do not fire.

Implication for the 1.5 h run: each 280 s Kaggle job ≈ 40–70 % of the local generation
count (4 vCPU vs 10-core M-series), so ~16 jobs ≈ 2 × (60–120) generations per target.
This is a **telemetry** run for the D=2 column, not an expected 2e-2 jump. The useful
output is the per-k h_final / island-cost / legal_improvements record, and the
conclusion it supports: the bank's D=2 seeds are rigidly contact-jammed and the GA's
first-ratchet wall is identical at 150 s and 900 s, so **a longer run in this basin is
not worth a slot**; the record's construction is a different family.

## 5. Result — **no candidate. Zero strict improvements. Certified gain 0.0.**

Kernel `ccjjllt/sis-d2-ladder-20261118` v1: pushed 21:25:26Z, **COMPLETE 22:52:59Z**.
Build `make engine CXX=g++` succeeded in 38.6 s; runner 4856 s; **17 jobs started
(the 7 remaining queue entries were skipped by `--until`); 17/17 valid, 0 failed,
0 stored to `best/`, 0 legal improvements** (the last job, 902 explore s2, completed
with `stop budget` at 281 s; `out/ledger.jsonl` is a 300 s snapshot copy and holds 16
rows, while the final `results.json` counts 3 jobs for n=902).

All eight targets came back at exactly the seed side (`best_raw == start_side`), i.e.
the bank is untouched. `sqpack_to_csv.py` over the downloaded `out/out/best` emits
**0 winning puzzles** (exit 1), so there is nothing to certify and no merge was run
against `/tmp/best_bank` (SHA-256 `55090172…`, report score 22.128332; the D=2 column
is identical to the 11-18 bank at f = 0.535533906 on all eight n).

### 5.1 Per-job telemetry (from `out/out/ledger.jsonl` + `results.json`)

| N | schedule | generations | ratchets | legal | h_final | Δ = start − h_final | min island cost | √cost (depth) |
|---:|---|---:|---:|---:|---|---:|---:|---:|
| 902 | explore s1 | 16 | 1 | 0 | 30.535511004 | 2.29e-5 | 1.56e-10 | 1.25e-5 |
| 963 | explore s1 | 5 | 1 | 0 | 31.535486603 | 4.73e-5 | 3.16e-09 | 5.62e-5 |
| 843 | explore s1 | 13 | 1 | 0 | 29.535489603 | 4.43e-5 | 6.29e-10 | 2.51e-5 |
| 786 | explore s1 | 20 | 1 | 0 | 28.535512504 | 2.14e-5 | 1.47e-10 | 1.21e-5 |
| 731 | explore s1 | 27 | 1 | 0 | 27.535523580 | 1.03e-5 | 3.16e-11 | 5.62e-6 |
| 678 | explore s1 | 25 | 1 | 0 | 26.535514004 | 1.99e-5 | 3.02e-11 | 5.49e-6 |
| 627 | explore s1 | 27 | 1 | 0 | 25.535514754 | 1.92e-5 | 3.39e-11 | 5.82e-6 |
| 578 | explore s1 | 28 | 1 | 0 | 24.535497103 | 3.68e-5 | 1.51e-11 | **3.88e-6** |
| 902 | seeded s1 | 28 | 1 | 0 | 30.529426799 | 6.11e-3 | 1.99e-05 | 4.46e-3 |
| 963 | seeded s1 | 7 | 1 | 0 | 31.529226799 | 6.31e-3 | 2.11e-05 | 4.59e-3 |
| 843 | seeded s1 | 23 | 1 | 0 | 29.529626799 | 5.91e-3 | 1.81e-05 | 4.25e-3 |
| 786 | seeded s1 | 34 | 1 | 0 | 28.529826799 | 5.71e-3 | 1.74e-05 | 4.17e-3 |
| 731 | seeded s1 | 45 | 1 | 0 | 27.530026799 | 5.51e-3 | 1.56e-05 | 3.95e-3 |
| 678 | seeded s1 | 42 | 1 | 0 | 26.530226799 | 5.31e-3 | 1.49e-05 | 3.86e-3 |
| 627 | seeded s1 | 44 | 1 | 0 | 25.530426799 | 5.11e-3 | 1.32e-05 | 3.63e-3 |
| 578 | seeded s1 | 47 | 1 | 0 | 24.530626799 | 4.91e-3 | 3.44e-05 | 5.87e-3 |
| 902 | explore s2 | (cut) | – | 0 | – | – | – | – |

`ga-seeded` confirms the local probe exactly: **h_final = start_side·(1−2e-4) for every
target** — one blind ratchet step, never a second. `ga-explore` lands 1–2 adaptive steps
below the seed (`eps` ≤ 1.5e-6) with soft cost 1.5e-11…3.2e-9, i.e. penetration depth
3.9e-6…5.6e-5, and **0 exact legalizations anywhere**.

### 5.2 Why 280 s jobs were too short at these N

Local 150 s at n=902 produced 75 generations; the Kaggle 280 s job produced **16**
(4 vCPU vs 10-core M-series, and the 7-island seeding/prepare phase eats a fixed
slice that does not shrink with N). Per-job generation counts are 5 (n=963) to 47
(n=578) — the GA barely leaves its initialization. If this schedule is ever rerun at
k≈30, jobs should be ≥600 s (or islands reduced), otherwise half the budget is prepare.

### 5.3 Distance to the record

| N | achieved depth √cost | side gap still needed to the record |
|---:|---:|---:|
| 578 | 3.9e-6 | 7.50e-4 (≈190×) |
| 627 | 5.8e-6 | 4.45e-3 (≈760×) |
| 678 | 5.5e-6 | 1.17e-2 (≈2100×) |
| 731 | 5.6e-6 | 1.17e-2 (≈2100×) |
| 786 | 1.2e-5 | 1.39e-2 (≈1160×) |
| 843 | 2.5e-5 | 1.73e-2 (≈690×) |
| 902 | 1.2e-5 | 2.15e-2 (≈1720×) |
| 963 | 5.6e-5 | 2.15e-2 (≈380×) |

And the same measurement at 150 s and 900 s locally returned the *identical* h_final at
n=902 (30.535503370429 to 15 digits), with 75 vs 607 generations. Time in this basin
does not move the wall.

## 6. Conclusion / recommendation

1. **The D=2 column is not reachable by this engine from the bank's seeds.** 17 valid
   jobs, 431+ generations, 0 legal improvements, every side bit-identical to the bank.
   The lift seeds are rigidly contact-jammed: n=578's seed is exactly feasible and
   cannot absorb a 1e-9 shrink.
2. **A longer GA run in the same basin is not worth a slot.** 6× more local time at
   n=902 changed nothing; `ga-seeded`'s ratchet never passes its first 2e-4 step, and
   `ga-explore`'s adaptive step collapses to its 1e-9 floor with 0 legalizations.
3. **If this column is pursued, it needs a construction, not a search.** The record
   looks like two masters — n=678 (covers 731) and n=902 (covers 963) — at
   f = 0.523860 / 0.514079, plus four singletons; those two finds are 64 % of the
   3.583e-3. That is a MILP/lattice job in the style of the n=291 track (exact
   two-offset fill around fixed 45° cores), with the target box `L = k + f_record`.
4. The run cost one CPU slot for 81 minutes and produced no candidate; the bank and
   `/tmp/best_bank` were never written to.

## 7. Files

| file | what |
|---|---|
| `REPORT.md` | this report |
| `kdir/kernel.py`, `kdir/kernel-metadata.json` | pushed kernel v1 (COMPLETE) |
| `payload_d2.tar.gz` | engine tree + 24 seeds |
| `make_kernel.py` | template → kernel.py (payload, MODE, budget, D2 queue) |
| `harvest.sh` | status → download → ledger/telemetry → strict-win converter → gates → merge (paths under `out/out/`) |
| `out/out/results.json`, `out/out/ledger.jsonl`, `out/out/summary.md` | Kaggle output (`improvements: []`, 16 ledger rows) |
| `out/sis-d2-ladder-20261118.log` | full kernel log |
| `probe578.*`, `probe902.*` | 150 s local ga-explore telemetry |
| `long902.*`, `long786.*` | 900 s local probes (the 6× time control) |
| `smoke/` | extracted payload, local engine, validated 578 run |
| `queue_ga_check.json` | expanded queue (24 jobs) used for the pre-push check |
| `cand.csv` | converter output: header only (0 winning puzzles) |
| `push.log` | push record |
