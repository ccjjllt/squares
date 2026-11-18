# Global fixed-side annealer — campaign2 / anneal track

Date: 2026-11-18. Target list per orchestrator re-ordering: 804, 491, 970, 328, 908
(moderate), then 842/902/963 (rigid-group-hard). Bank at comparison time:
**22.128441824806618**, SHA-256 `9c981e6ea9a44c076587256936948e636936a84ad0668af6b75e946f4fa527e9`
(500500 rows, 1000/1000 valid — re-read from `/tmp/best_bank/report.json`).

## 1. Headline

**A certified improvement was found and dual-route verified.** It is real but tiny:
**−7.075e-9** on the score, from two puzzles (n=804, n=970). The annealer itself found
**no** improvement; the gain came from a deterministic exact contact-LP compaction that
is the rigorous limit of *continuous* motion.

The important result is the negative one: these layouts are **jammed**. The maximum
continuous bbox reduction (exact LP, translations only) is **≤ 1.0e-7** for every one of
the eight targets, while the required reduction is **0.0075–0.0215** — a factor of
**10⁵–10⁶** short. Simulated annealing from the bank layout, with 5×10⁵ moves/s and
per-square `(x,y,θ)` plus void-transport / row-shift / contact-cluster / half-space /
swap moves and T=1e-3 basin-hopping kicks, cannot reach feasibility at **any** side below
the bank side, and its energy obeys `E ≈ k·δ²` (`k = 0.65–2.5`) — i.e. the packings behave
as jammed elastic solids, not as loose assemblies with slack to give.

## 2. Certified result

Command (exactly the required route):

```sh
.venv/bin/python -m squares merge --baseline /tmp/best_bank/submission.csv \
  --baseline-report /tmp/best_bank/report.json \
  --candidate /tmp/campaign2/anneal/out/candidate.csv \
  --output-dir /tmp/campaign2/anneal/out/merge
```

| n | L old (bank) | L new | ΔL | Δscore |
|---|---|---|---|---|
| 804 | 28.82715434994971394 | 28.827154170406834371703830656 | −1.7954288e-7 | −6.3319891e-9 |
| 970 | 31.6366520306808742987… | 31.6366520075352128660… | −2.3145661e-8 | −7.4316240e-10 |

* `merge_report.json`: `changed_puzzles = [804, 970]`, `invalid_candidates = []`,
  `net_gain = {text: 7.075151575719474e-09, float64: 7.075151575719474e-09}`.
* Score: **22.128441817731467 (text) / 22.12844181773147 (float64)** — both strictly below
  **22.128441824806618**. 998 unchanged groups inherit the bank's 1000/1000-valid report.
* Merged file: `/tmp/campaign2/anneal/out/merge/submission.csv`, 500500 rows, 1000 puzzles,
  exactly n rows per puzzle, SHA-256 `63996fdadc8b4d13935ff6c6aa4064c3a8c428d3ff1c575c79b1b4869115589d`.
* Independent check on the emitted candidate (not the library): explicit pairwise SAT over
  all pairs within 1.5, max penetration **0.0**, min separation **+2.13e-10**;
  `assert n <= L*L` passes. No overlap, no bbox violation.
* `/tmp/best_bank/submission.csv` was **not** modified. Nothing was submitted.

The gain is microscopic by design: §3 shows the layouts have no continuous slack, so this
is the exact limit of what any continuous method can produce. It is nonetheless a strict,
certified improvement on both routes.

## 3. Why the gap cannot be closed (four independent measurements)

### 3.1 The layouts are pitch-1 rigid-block patchworks, not loose packings
Nearest-neighbour histogram on every live layout: minimum and median centre distance are
**exactly 1.000000** for the dominant orientation groups (0°/90°, 45°, and the −23.7° /
66.3° grains). The area deficit (3.2–5.5 %) is concentrated in a few large holes. Rendering
`view_804.png`, `view_842.png`, `view_491.png` shows it directly: axis-aligned grid frames
with 45° or ±23.7° rotated grains inset, plus a handful of visible holes.

Consequence: uniform scaling of the centres to the record side compresses **every contact**
by `δ/S` (not by `δ`). Measured: 2 399–3 286 pairs with penetrations 0.5–0.9e-3 at the
record side, i.e. a *uniform* 6e-4-scale overlap — an over-constrained contact network.

### 3.2 Exact contact LP: the maximum continuous bbox shrink is ~1e-7
Formulation (`lp_maxdelta.py`, `lp_compact2.py`): maximise the four-sided bbox shrink `δ`
subject to every pair separation staying ≥ 0, with translations only. Translation-only
pair constraints are **exact** — the linearised separation `|d·a| + s·(Δu·a) − rsum` is a
lower bound on the true separation, because `|x+δ| ≥ x+δ`; so a feasible LP solution
applied verbatim is provably non-overlapping. (Rotations were deliberately excluded: at
45°/90° the support function `0.5(|u·a|+|v·a|)` has a kink, the analytic derivative has an
O(dθ) error, and a rotation-enabled LP reports spurious feasibility — verified by applying
one: `Σpen²` jumps from 9.2e-4 to 6.2e-2. This also explains the earlier "contact LP
accepted everything" result.)

Result, exact and verified, starting from the bank side of each layout:

| n | max continuous shrink δ* (per side) | min pair gap in bank layout |
|---|---|---|
| 804 | 1.035e-7 | 6.59e-10 |
| 970 | 3.858e-8 | 8.43e-10 |
| 908 | 7.87e-13 | 4.93e-14 |
| 963 | 6.95e-14 | ≤1e-14 |
| 491 / 328 / 842 / 902 | 0 (LP infeasible for any δ>0) | 1e-14 … 1e-10 |

The binding quantity is the smallest gap in the layout: these packings were already
polished to ~1e-10 contacts, so there is nothing left for a continuous motion to harvest.
Applying the LP and iterating (with a 1e-9 pair margin and HiGHS tolerances at 1e-10) gives
exactly the two improvements in §2 and stops dead for the other six.

### 3.3 Annealer: `E ≈ k·δ²`, never feasible at any side below the bank
The fixed-side annealer (`kernel/kernel.py`; numba, local-cell-list Metropolis,
~5×10⁵ moves/s/core) minimises `Σ max(0,pen)² + 1e3·Σ wall²`. Moves: single translate,
single rotate, row/column shift, contact-cluster translate, pair swap, void teleport into
an empty pocket, and half-space translate. Temperature and move amplitude are
self-calibrated from the measured initial penetration (`T0=(p0/2)²`, `T1=(p0/250)²`,
`σ=1.2 p0`). Shrink mode: adaptive `dS` from 2e-5, accept only if the *exact* check is
clean.

Outcome (short diagnostic run, 4 workers, 20 s/puzzle; full results in
`local_run/result_*.json`):

| n | gap to record | E at record side (init) | E after anneal | max pen | bad pairs | E/δ² | shrink mode |
|---|---|---|---|---|---|---|---|
| 328 | 0.01483 | 6.186e-4 | 4.549e-4 | 1.81e-3 | 858 | 2.07 | jam at S_bank |
| 491 | 0.01422 | 2.124e-4 | 1.318e-4 | 1.77e-3 | 737 | 0.65 | jam at S_bank |
| 804 | 0.01709 | 9.156e-4 | 6.410e-4 | 1.39e-3 | 2319 | 2.19 | jam at S_bank |
| 842 | 0.01866 | 1.036e-3 | 7.636e-4 | 1.53e-3 | 2272 | 2.19 | jam at S_bank |
| 902 | 0.02146 | 1.307e-3 | 1.003e-3 | 1.52e-3 | 2327 | 2.18 | jam at S_bank |
| 908 | 0.01969 | 1.185e-3 | 8.922e-4 | 1.44e-3 | 2550 | 2.30 | jam at S_bank |
| 963 | 0.02146 | 1.631e-3 | 1.172e-3 | 1.64e-3 | 2907 | 2.55 | jam at S_bank |
| 970 | 0.00749 | 7.119e-5 | 5.360e-5 | 5.15e-4 | 1326 | 0.96 | jam at S_bank |

Every puzzle anneals `Σpen²` down by 20–38 % but the **maximum** penetration *grows*
(from ~8e-4 to ~1.5e-3): the search redistributes overlap rather than removing it, which is
the signature of a frustrated/jammed state. Basin hopping with T=1e-3 kicks accepted **0**
improving states in every run (`acc=0`), and no shrink step was ever feasible. The shrink
mode never moved: it fails at `dS=2e-5` and, after 9 halvings, at `dS≈4e-8`.

### 3.4 No free cell anywhere: the `n → n+1` insertion exploit is unavailable
The record sequence shows `L(907)=30.60588388152593` and `L(908)=30.60588450856970`, i.e.
consecutive records almost identical — the classic signature of inserting one square into a
vacant cell. A numba scan over **all 1000 bank layouts** for an axis-aligned unit square
with ≥1e-6 clearance found **zero** free cells (`free_positions=0` for every n). Our
layouts are tight; that route is closed for us.

## 4. Residual overlap vs side (the requested curve)

`E_best(d)` from the annealer, `d = S_bank − S`, 13 sides from the bank side to the record
side, 1.2e5 moves per side (full data: `local_run/result_*.json`, `lp_curve.json`).
Representative rows (all eight puzzles behave identically):

| n | d=0.25·gap | d=0.50·gap | d=0.75·gap | d=gap | E/δ² |
|---|---|---|---|---|---|
| 804 | 1.98e-5 | 8.29e-5 | 1.94e-4 | 6.41e-4 | 2.19 |
| 902 | 2.75e-5 | 1.07e-4 | 2.40e-4 | 1.00e-3 | 2.18 |
| 963 | 3.51e-5 | 1.43e-4 | 3.30e-4 | 1.17e-3 | 2.55 |
| 970 | 2.20e-6 | 8.74e-6 | 2.03e-5 | 5.36e-5 | 0.96 |
| 491 | 5.41e-6 | 2.07e-5 | 4.77e-5 | 1.32e-4 | 0.65 |

`E` is the sum of squared SAT penetrations; it is strictly positive for every `d>0` and
scales like `d²`, i.e. the packings are linearly elastic against bbox shrink with a finite
stiffness. Interpolating, the side at which the residual would vanish under this
extrapolation is `d ≈ 0` — there is no finite compressible range. The symmetric LP
diagnostic (`lp_curve.json`, rotations allowed at |dθ|≤2e-3) reports a "crossing" at
`d = 0.0026–0.0091` (15–64 % of the gap), but that number is an artefact of the 45°/90°
support-function kink (§3.2) and cannot be realised: applying those solutions increases
penetration by 2–70×.

## 5. The annealer (mission deliverable)

* Code: `/tmp/campaign2/anneal/kernel/kernel.py` (self-contained, 733 lines, numba).
  Phases per puzzle: (1) residual-vs-side curve, (2) adaptive shrink mode with
  accept-only-if-exactly-feasible, (3) T=1e-3 kick / quench basin hopping at
  `S_record − 1e-6`, always restoring the best state, checkpointing every phase.
* Throughput measured locally: **5×10⁵ moves/s/core** (804 bodies, ~2 400 active pairs),
  i.e. ~7×10⁹ moves per puzzle in 4 h on one core, ~4×10¹⁰ for the 8-puzzle kernel.
* Move mix actually exercised: translate 42 %, rotate 18 %, row shift 12 %, contact-cluster
  18 %, swap 4.5 %, void teleport 3 %, half-space shift 2.5 %.
* **Kernel push status: blocked.** `ccjjllt/sis-anneal-fixed-side-20261118` is prepared
  (`kernel-metadata.json`, CPU only, `enable_gpu: false`, bank dataset mounted) and was
  re-pushed every 2.5 min throughout the session; every attempt returned
  `Maximum batch CPU session count of 5 reached`. The kernel is deterministic in its
  protocol and can be pushed unchanged when a slot frees. Its results are not in this
  report; the numbers above are from the same code run locally on a short budget, plus the
  exact LP results which are budget-independent.

## 6. What this rules out

1. **Any continuous compaction of the live layouts.** The exact translation-only LP bounds
   the achievable shrink at ≤1.0e-7 per side; the required shrink is 7.5e-3–2.1e-2.
2. **Scale-separated annealing.** `E ∝ δ²` with stiffness 0.65–2.55 and no feasible side
   below `S_bank` means the annealer has no gradient toward feasibility: it trades many
   small overlaps for a few large ones.
3. **Vacancy-assisted creep.** Removing 1/2/4/8 squares and re-running the exact creep
   still yields zero compression: at 2.8 contacts per square the network remains
   hyperstatic (isostatic ratio 1.0–1.7) and a few vacancies do not floppify it.
4. **`n → n+1` free-cell insertion.** No vacant unit cell exists in any of the 1000
   layouts.
5. **The rotation-enabled contact LP as evidence.** It reports spurious feasibility; any
   claim based on it must be verified by applying the field (we did; it fails).

The positive statement: the remaining gap requires a **discontinuous re-arrangement**
(contact breaking/reforming), i.e. a genuinely different packing, not a deformation. That
is consistent with the rigid-group certificate (0.053-cell pass-through) and with every
prior hop/glide/fq/LNS negative result in this campaign.

## 7. Artifacts

```
/tmp/campaign2/anneal/
  REPORT.md                       this file
  out/candidate.csv               compacted 804+970 (1774 rows, 17-digit round-trip)
  out/merge/submission.csv        certified merged submission (SHA 63996fda…)
  out/merge/merge_report.json     dual-route certification, changed=[804,970]
  local_run/result_*.json         per-puzzle curves, shrink attempts, hot-phase log
  lp_curve.json                   LP t_min(d) for all 8 targets
  batch_compact.json              per-puzzle LP compaction outcome
  kernel/kernel.py                the annealer (ready to push)
  kernel/kernel-metadata.json     ccjjllt/sis-anneal-fixed-side-20261118, CPU
  core.py fast.py lp_maxdelta.py lp_compact2.py lp_creep.py vacancy.py freecell.py
```

Reproduce the win:

```sh
cd /Users/zhaohuaxiang/ccjjllt/squares
.venv/bin/python /tmp/campaign2/anneal/lp_compact2.py 804   # -> gain 8.98e-8 per side
.venv/bin/python /tmp/campaign2/anneal/lp_compact2.py 970
# emit + merge as in §2 (candidate already written)
```

No submission was made; the orchestrator owns that. `/tmp/best_bank/submission.csv` is
untouched.
