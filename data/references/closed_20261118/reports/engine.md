# Engine port — contact-force + fast-LP re-packing (rosswade notebook), 2026-11-18

**Track stood down at 20:40Z. No certified wins, no candidate CSV: the only kernel was deleted
by the orchestrator at ~19:48Z to free a CPU session slot, before it could be downloaded.**

| item | value |
|---|---|
| source | `rosswade/jammed-squares-contact-forces-and-fast-lp-search` (public notebook) |
| port | complete, self-contained Kaggle CPU kernel, validated locally (see §3) |
| target list | **389 puzzles**, computed from the bank + record CSVs (not hardcoded) |
| bank at build time | `22.129502357094957`, SHA-256 `6f6e9da8…f55e0c40` |
| record snapshot | `22.050883571266684` (`perpuzzle_best_20261111.csv`) |
| **remaining gap on those 389** | **0.081525953** |
| kernel run 1 (6 h budget) | `ccjjllt/sis-engine-port-contact-forces-fast-lp-20261118`, pushed 16:59Z, RUNNING and readable until 19:19Z, **deleted ~19:48Z** → 2 h 49 min of compute, no output retrievable |
| kernel run 2 (4 h budget) | `ccjjllt/sis-contact-lp-repack-20261118`, never started: push rejected at the 5-CPU-session cap (20:09/20:15/20:20/20:26/20:31Z), then stood down |
| deliverables | `improved_groups.csv`: **none exists**; `candidate.csv`: **not built** (nothing to certify) |

## 1. What was ported

Source notebook downloaded to
`/tmp/rw_engine/jammed-squares-contact-forces-and-fast-lp-search.ipynb` (all 58 cells read).
Ported verbatim — numerical code unchanged:

| notebook cell | contents |
|---|---|
| 1 | `load_highspy()` (wheel dir → pip → mirror fallback), constants |
| 8, 9 | `pair_gap`, `corners`, `extent`, `side`, `neighbour_pairs`, `min_gap_over`, `min_gap`, `to_origin`, `fold` |
| 15 | `find_bodies` / `_weld` (rigid bodies: bars, grid, singles) |
| 23 | `move_bodies` |
| 24 | `lp_rows` (rigid-body contact/wall rows, two branches of ρ) |
| 25 | `class Compactor` (`direction`, `repair`, `improve`, `compact`) |
| 27 | `_energy`, `_pairs_with_free`, `relax` (compiled L-BFGS penalty relaxer) |
| 34 | `_pairs_of`, `class LocalLP` (incremental min-side LP) |
| 36 | `class Hopper` (force-guided re-packing) |
| 45–46 | `band_summary`, `find_cut`, `change_length`, `transplant` (one bar per band) |
| 49 | `l_border` + deletion closure |
| 51 | `min_gap_strict`, `open_contacts` (3e-12 gap on every contact) |

Dropped: plotting/reporting cells (2–7, 10–22, 26, 28–33, 37–44, 47–48, 52–57), the
`public` / `per_puzzle_best.csv` input layer, and the submission assembly. Replaced by:

- seed: `/kaggle/input/**/submission.csv`, the bank dataset `ccjjllt/sis-bank-20261117`
  (27–29 MB size filter), layouts as `(x, y, angle)`;
- target list: `TARGETS = {n: record_L}` for every n with `bank L > record L`, generated at build
  time from `/tmp/best_bank/submission.csv` + `perpuzzle_best_20261111.csv` and re-filtered at run
  time against the actual bank file (`L0[n] > record_L + 1e-12`);
- output: `improved_groups.csv` (`id,n,square_id,x,y,angle`) + `run_report.json`, checkpointed to
  `/kaggle/working` at most every 20 s (atomic replace) so a mid-run download is usable.

Files: `/tmp/campaign2/engine/engine_core.py`, `driver.py`, `build_kernel.py`,
`kernel.py` (59.7 kB, ready to push), `push2/kernel-metadata.json`,
`merge_candidate.py`, `certify.sh`.

## 2. Changes marked `PORT:` (all defensive; none touch the numerics)

1. `LocalLP.evaluate`: `setBasis` only when the base solve was optimal (highspy raises on
   `setBasis(None)`).
2. `Hopper.trial`: if the force vector sums to ≤ 0 (possible after a reset), fall back to uniform
   weights over the loose set instead of `NaN` probabilities (the notebook would die there).
3. `new_solver`: `threads=1` (one LP per worker process).
4. Driver: uniform-force fallback when `Hopper.applicable()` is false.
5. Driver: acceptance requires the *opened* layout (all gaps ≥ 3e-12) to beat the bank by > 1e-7 of
   side; noise-level "wins" (3.5e-8) are rejected.
6. Driver: `transplant` scan (≤150 band packings, both directions, 900 s cap) before the search,
   and deletion + L-border closure after each pass.

## 3. Local validation (all numbers reproduced on the real bank layouts)

- `compact` on a slab-reopened bank layout returns to the original side: n=199 `+3.93e-12` of
  14.614689853 (7 LPs, 0.9 s); n=963 `+0.00e+00` of 31.535533906 (3 LPs).
- `LocalLP.evaluate` on a deliberately loose valid packing (5×5 grid at pitch 1.05, side 5.2)
  returns **5.18** — one trust-region step, as designed.
- `Hopper` on that same packing: **5.2 → 5.000000000017562** in 3 s (1,574,519 trials, 1 win) —
  end-to-end control that the search + LP + compact path works.
- 8 random bank targets × 15 s after warm-up: 0 real wins (one 3.5e-8 noise-level move, now
  rejected by the 1e-7 margin).
- 2-puzzle smoke through the built kernel: 721,889 trials, 79,697 relax fits, 0 promising,
  0 wins — i.e. on mature bank layouts most trials still die before the LP.
- Candidate assembly tested on a no-op input: the rebuilt 500,500-row file scores
  `22.129502357094953` (text) / `22.129502357094957` (float64) and `squares merge` accepts it
  (`0 changed puzzles`).

## 4. Negative result A — half the bank is welded into bodies `Hopper` can never move

Measured over the 389 target layouts (`find_bodies` at tol 1e-3):

| squares in bodies of size | share |
|---|---|
| ≤ 2 | 26.9 % |
| 3–12 (the notebook's `loose` rule) | 15.8 % |
| 13–40 | 6.6 % |
| **> 40** | **50.8 %** |

`Hopper` only frees squares in bodies ≤ 2 plus neighbours in bars ≤ 12, so **half the squares are
immovable**, and **7 target puzzles are a single welded body** (`295, 298, 605, 762, 877, 937,
1000`; 6 more have < 10 loose squares). For these the engine is structurally inert — `w.sum() = 0`
and no trial can change anything. This alone caps what any run of this engine can return on our
bank, independently of the time budget.

## 5. Negative result B — the record's 0.2–0.7° defect is not reachable by rigid-body local search

Intel: the record layouts of the 45° central-block (CDB) family are the bank's topology with the
core rotated 0.2–0.7° off 45° (record D=1 `f = 0.502152708`, worth 1.97 waste units). Tested
directly on n=842 (bank 29.520815280, record 29.502152708):

| experiment | result |
|---|---|
| rotate the core body (232 squares) by 0.1° | 0.025 corner displacement, overlaps up to 0.045 |
| `relax`, free = squares within r+2 of the core | `E = 15.9` after 400 L-BFGS iterations, `min_gap` −1.19 → no fit |
| `relax`, free = all 842 squares, box S+0.08 | converges to `E ≈ 0` but the packing collapses (two squares coincide, gap −1.207); `compact` returns `ov = 1.2` → rejected |
| `compact` from any rotated state | `ov = 1.2`, correctly rejected; no invalid layout ever passed the acceptance gate |

Why: the CDB layouts are **1–3 welded bodies** (n=842: 232 + 127 + 91 squares). Rotating the core
by even 0.1° puts a 0.045 overlap into a neighbouring rigid block; no local move can absorb it,
and freeing everything lets the relaxer collapse the packing instead of sliding the blocks.
Getting to the record's position needs a different contact graph — a construction/gadget change —
which is consistent with the campaign's "fixed-angle contact LP at target side" negative
(hyperstatic contact graphs) and with the D=1 column needing a new gadget, not a polish.

## 6. Bank movement seen during this track

| time (Z) | bank score | SHA-256 (first 16) |
|---|---|---|
| 16:20 | 22.129502357094957 | `6f6e9da8e3c79591` (kernel seed) |
| 17:18 | 22.129495171822438 | `9bdbce2bc63adc7f` (28 puzzles changed, 26 in the 389) |
| 18:16 | 22.128441824806618 | `9c981e6ea9a44c07` |

The Kaggle dataset `ccjjllt/sis-bank-20261117` stayed pinned at the 16:20 file
(27,595,882 bytes), so a re-run of `kernel.py` would seed ~28 puzzles from stale (worse) layouts;
`merge` filters those out, but ~7 % of the compute would be spent re-finding known gains.

## 7. If this engine is ever run again

- `kernel.py` (59.7 kB) + `push2/kernel-metadata.json` are ready; nothing else is needed.
- Budget knobs live in `driver.py`: `SIS_BUDGET` (default 4 h), pass schedule
  `seq = [30, 30, 40, 40, 50, 50, 60, 60, 80, 80]` seconds, `CORES = min(8, cpu_count)`,
  389 targets, improved puzzles re-queued first.
- Set `SIS_OUT` / `SIS_TARGETS_JSON` for a local smoke (used for all the validation above).
- Download + certify is one command: `/tmp/campaign2/engine/certify.sh <kernel-ref>`
  (fetch → `candidate.csv` vs the **live** bank → `squares score --mode both` →
  `squares merge` → score the merged file).
- Expectation, stated honestly: with half the squares immovable (§4) and 0 promising evaluations
  in ~70 k local trials on mature bank layouts, this engine is a low-yield polish tool on *our*
  bank. Its 52-puzzle gain in the campaign came from *public* layouts that were less welded and
  less polished. The C++20 engine (L-BFGS/GA) is the better route for the same 389 targets.
