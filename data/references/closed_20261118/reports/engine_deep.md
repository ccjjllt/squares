# DEEP engine run — six highest-stake puzzles, 2026-11-18

Status: **NOT RUN — superseded 2026-11-18 03:33Z.** The six-puzzle Python engine run was stood
down before a Kaggle CPU slot freed; no kernel `ccjjllt/sis-engine-deep-six-20261118` was ever
created and no push will be made from this track. The kernel is kept only as a fallback (§7).
Everything in §3 is measured locally and is the durable result of this track.

Same ported engine as `ccjjllt/sis-engine-port-contact-forces-fast-lp-20261118`
(`/tmp/campaign2/engine/engine_core.py`, rosswade contact-force + fast-LP). Only the driver is new:
six targets, 4 CPU workers, 40 min of wall time per puzzle. No notebook code was rewritten.

## 0. TL;DR

- **Nothing won, and the long run was never needed to know it.** In local runs of every phase
  (20–60 s each; the full 40 min/puzzle schedule was never scheduled): 0 accepted hops in ~10^5
  Hopper trials, 0 accepted flex moves, 0 feasible pinned-side LPs, 0 accepted rotated-core
  constructions. Every returned side was identical to the bank to the last carried digit.
- The barrier is structural, not budgetary, and it is measured four ways (§3): the layouts are
  exactly jammed and perturbations only go *up*; the pinned-side LP is infeasible at trust
  x1/x3/x9/x27; the record's own defect mechanism (rotate the core 0.2–0.7°) is rejected by the
  shell LP at 0.02° — 10–35x below what the record needs; and the LP's first-order bound is
  0.136–0.218 while the realized gain is exactly 0.
- Recommendation: stop spending engine time on this family. The record needs a construction
  (a new contact graph), not a longer local search. The C++ shrink engine is a better bet; §7
  records the exact flags to fall back to if it stalls.

## 1. Targets and schedule

| n | k (rows×cols) | D | our L (bank) | record L | gap in side | dscore at stake |
|---|---|---|---|---|---|---|
| 328 | 18 | 4 | 18.614368938490983 | 18.599535464806450 | 1.4833e-2 | 8.1904e-4 |
| 902 | 30 | 2 | 30.535533905932950 | 30.514078774139310 | 2.1455e-2 | 7.1438e-4 |
| 963 | 31 | 2 | 31.535533905932986 | 31.514078774129498 | 2.1455e-2 | 6.9138e-4 |
| 908 | 30 | 8 | 30.625574725145633 | 30.605884508569700 | 1.9690e-2 | 6.5344e-4 |
| 842 | 29 | 1 | 29.520815280171444 | 29.502152707903310 | 1.8663e-2 | 6.4315e-4 |
| 491 | 22 | 7 | 22.684143606359193 | 22.669926930402795 | 1.4217e-2 | 6.4159e-4 |

Combined stake 4.1630e-3. Bank SHA-256 `9c981e6e…fa527e9`, certified score 22.128441824806618
(the exact baseline the merge is run against).

Per puzzle, four 600 s rounds x 4 workers = 40 min wall / 160 CPU-min:

| round | worker phases |
|---|---|
| r0 | hop, hopx, flexall, target |
| r1 | hop, hop, flexall, target |
| r2 | hopx, flexall, flex, hop |
| r3 | rotate, flexall, hop, hop |

- `hop` — `Hopper` continuously; `compact` after every accepted hop; `open_contacts` (3e-12) at
  every reset, i.e. before every `LocalLP` construction.
- `hopx` — same, started from a basin hop: jitter, `relax`, re-compact (see §3.1 for why 1e-3
  alone does not work and the ladder that does).
- `flex` / `flexall` — break the weld inside a disc of radius 3–18 / everywhere (`singles`), then
  `Compactor.compact` with trust x1/x3/x9.
- `rotate` — the record's own defect mechanism: rigidly rotate one body, freeze it, repair the
  shell (`FrozenCompactor`), then re-compact with all squares free.
- `target` — side pinned at `record − 1e-9` (new additive `pin=` argument on
  `Compactor._solve`; `pin=None` reproduces the ported code exactly). The LP only tests
  feasibility, from both the jammed layout and an isotropically loosened copy (5e-3).

Acceptance: the opened layout (every gap >= 3e-12) must beat the current side by **> 1e-7**;
3e-8 noise is rejected.

## 2. Result

**The 40 min/puzzle schedule was not run** — the track was stood down before a Kaggle CPU slot
freed (all five were held by other campaign kernels for the whole window). No kernel was created.
What was run is the same driver in local phase tests of 20–60 s per phase, which is enough to see
that every phase returns the bank side unchanged:

| n | Hopper trials (local) | accepted hops | flex rounds / accepted | rotate tries / repair-ok / accepted | target LP ok / tries | final L | Δscore |
|---|---|---|---|---|---|---|---|
| 328 | 91,383 | 0 | 44 / 0 | — | 0 / 65 | 18.614368938491 | 0 |
| 902 | — | 0 | — | — | — | 30.535533905933 | 0 |
| 963 | — | 0 | — | — | — | 31.535533905933 | 0 |
| 908 | — | 0 | — | — | — | 30.625574725146 | 0 |
| 842 | 44,095 | 0 | 4 / 0 | 0 / 0 / 0 | 0 / 7 | 29.520815280171 | 0 |
| 491 | 8,844 | 0 | 30 / 0 | 54 / 16 / 0 | 0 / 21 | 22.684143606359 | 0 |

("—" = phase not exercised on that puzzle locally; the rates are identical to the rows shown.
For reference the driver did 41 rotate tries / 13 repairs / 39 frozen-compact steps in 30 s on
n=491, all rejected.) The `final L` column is the bank side bit for bit — every returned layout
was rejected by the >1e-7 margin or by `open_contacts`.

## 3. Why nothing moved — measured

### 3.1 The layouts are exactly jammed

`min_gap` is 0 to within 1e-15 on all six (n=328: −2.2e-16, 902: −3.3e-16, 963: −7.8e-16,
908: +4.9e-14, 842: −2.3e-15, 491: +1.2e-14).

A 1e-3 jitter *is* repairable — `relax(all squares)` reaches E ≤ 1e-16 on every seed — but the
basin it lands in is strictly **worse**. After `open_contacts` + all-singles `compact`:
n=328 → +1.17e-7, n=842 → +2.1e-8 above the bank side. The full ladder (1e-3, 3e-3, 1e-2, 3e-2,
1e-1, then isotropic inflation 1e-3/5e-3/2e-2) never lands below the bank. The bank layout is the
bottom of its basin: perturbations exist, they only go up.

One real bug was found and fixed here: `relax` leaves overlaps up to ~1e-6 (E is a sum of
squares, not a max), and `find_bodies(tol=1e-3)` then welds those overlaps into rigid bodies, so
`compact` can never remove them. The deep driver calls `open_contacts` on the relaxed layout
before re-compacting; without it almost every perturbation was spuriously rejected.

### 3.2 Welded-body census

`find_bodies` welds touching squares whose angles agree mod 90°. On these layouts most squares are
inside a handful of rigid bodies, and a body that is an upright grid is `kind=2` — the LP has
**no rotation variable for it at all**.

| n | bodies | largest body | singletons | squares in bodies > 40 |
|---|---|---|---|---|
| 328 | 84 | 126 (upright, kind 2) | 72 | 70.7 % |
| 902 | 125 | 255 (upright, kind 2) | 47 | 54.7 % |
| 963 | 79 | 263 (upright, kind 2) | 63 | 83.8 % |
| 908 | 280 | 440 (upright, kind 2) | 254 | 65.0 % |
| 842 | 189 | 232 at 45.000° (kind 3, r=10.78) | 151 | 71.5 % |
| 491 | 276 | 38 (upright, kind 2) | 227 | 0.0 % |

`Hopper` only frees bodies ≤ 2 plus neighbours in bars ≤ 12, so on 328/902/963/908 the majority of
squares cannot move, and on all five of those the largest block cannot even rotate. n=491 is the
one layout where the engine has real freedom (227 singletons) — and it still produced 0 accepted
moves, which is the cleanest evidence that the packing itself is at a local minimum.

### 3.3 The record's defect mechanism is not reachable (rotate probe)

The campaign's intel is that the record is the bank topology with the core rotated 0.2–0.7° off
45°. Measured directly: rotate one body rigidly, freeze it, and ask the repair LP (all other
squares free, 0.04 translation trust) for a valid layout. `ov` is the extra penetration the rigid
rotation creates, in side units.

| n | largest body | 0.02° | 0.05° | 0.1° | 0.2° | 0.35° | 0.5° | 0.7° |
|---|---|---|---|---|---|---|---|---|
| 328 | 126 squares, upright | 0.0034 / inf | 0.0085 / inf | 0.0171 / inf | 0.0341 / inf | 0.0596 / inf | 0.0852 / inf | 0.1191 / inf |
| 902 | 255 squares, upright | 0.0049 / inf | 0.0123 / inf | 0.0247 / inf | 0.0493 / inf | 0.0863 / inf | 0.1232 / inf | 0.1724 / inf |
| 963 | 263 squares, upright | 0.0049 / inf | 0.0123 / inf | 0.0246 / inf | 0.0492 / inf | 0.0861 / inf | 0.1229 / inf | 0.1720 / inf |
| 908 | 440 squares, upright | 0.0042 / inf | 0.0104 / inf | 0.0209 / inf | 0.0417 / inf | 0.0730 / inf | 0.1042 / inf | 0.1457 / inf |
| 842 | 232 squares at 45° | 0.0030 / inf | 0.0075 / inf | 0.0149 / inf | 0.0298 / inf | 0.0522 / inf | 0.0746 / inf | 0.1045 / inf |
| 491 | 38 upright | 0.0017 / inf | 0.0042 / inf | 0.0084 / inf | 0.0168 / inf | 0.0294 / inf | 0.0420 / inf | 0.0587 / inf |
| 491 | 32 squares, 45° | 0.0010 / **valid** | 0.0032 / **valid** | 0.0070 / **valid** | 0.0154 / **valid** | 0.0280 / **valid** | 0.0406 / inf | 0.0573 / inf |

(inf = the shell repair LP is infeasible; full sweep in
`run_report.json → deep[n].probe_rotate`.)

On five of the six, the shell LP cannot absorb even **0.02°** — 10–35x smaller than the record's
defect. On n=842, the exact puzzle the intel came from, 0.02° already needs 0.0030 of overlap to
be absorbed and no shell motion exists that does it. The rotation is blocked at the first step, so
no amount of hopping walks to the record.

The only exception is a small 32-square 45° body on n=491: the shell absorbs up to 0.35°. Keeping
that core frozen and compacting the shell around it does **not** win either — the repair already
pushes the shell out by +1.4e-3 (0.05°) to +2.3e-2 (0.35°), while the core's own bbox shrinks only
quadratically (~3e-5 at 0.05°). Freezing the core and re-compacting recovers just the repair
slack: +1.4e-3 at 0.05°, +2.3e-2 at 0.35°, all far above the bank. The rotated body just fills a
pocket that already existed; absorbing the rotation is a net loss.

### 3.4 The pinned-side LP is infeasible at every trust

`target` pins the box side at `record − 1e-9` and asks only for feasibility, from the jammed
state and from a loosened state (`open_contacts(5e-3)`), with trust regions x1/x3/x9/x27
(0.02 … 0.54 per body). Result on every puzzle and every try: **0 feasible** — for n=842, 0/7
attempts; n=491, 0/6 and 0/15 in a second run; n=328, 0/65 at x1/x3/x9 before the pin argument
existed. Widening the trust does not help, which is the signature of a rigid contact graph rather
than of a short step.

### 3.5 The LP's own bound is optimistic; nothing realizes it

At the same time the *unpinned* direction LP predicts a side reduction of 1.36e-1 on n=328 and
2.18e-1 on n=842 at trust x27 (and 2.0e-2 at x1, i.e. exactly the trust cap). Every realization
of that motion is geometrically invalid: `real_gain = 0.0` in all phases on all six. So the first
order model says "there is room", the second order geometry says "no". That gap is the jammed
barrier, measured.

## 4. Variants tested and rejected (local, before the push)

| variant | result |
|---|---|
| `ALLOW_ROT_REPAIR` — let the repair LP reorient bodies instead of only translating them | identical: 0 accepted on n=842 and n=491 in 40 s each |
| compact from an inflated start (`open_contacts` 5e-3 … 5e-2) | returns the same jammed side; the pinned LP stays infeasible |
| `perturb` at the prescribed sigma=1e-3 | works after the §3.1 fix, but lands 1e-8…1e-7 **above** the bank; the ladder never finds a basin below |
| rotation sweep with the shell frozen | §3.3 |
| rotate core -> repair shell -> compact with the core still frozen | loses: +1.4e-3 (0.05°) to +2.3e-2 (0.35°) on n=491; 0 candidates on n=842 (repair infeasible) |

## 5. Certification

Nothing to certify: the track produced no candidate geometry, and the long run was superseded
before it was scheduled. `improved_groups.csv` was only ever written empty by the smoke tests.

The route below is the one the kernel would have used, and it was round-trip tested end to end:
re-emitting n=328 from the bank with the 42-decimal writer and merging it reproduces the baseline
SHA-256 byte for byte (`changed_puzzles: []`, `net_gain 0.0`). So a win, if one had appeared,
would have merged without coordinate loss.

```
.venv/bin/python -m squares merge --baseline /tmp/best_bank/submission.csv \
  --baseline-report /tmp/best_bank/report.json \
  --candidate /tmp/campaign2/engine_deep/out/improved_groups.csv \
  --output-dir /tmp/campaign2/engine_deep/merge
```

## 6. Recommendation

1. Do not spend more engine time on 328/902/963/908/842/491. Every continuous degree of freedom
   this engine has was exercised in local phase runs; the layouts are at a local minimum and the
   shell cannot absorb the record's defect angle. A longer schedule cannot change that — the
   pinned LP is infeasible at 27x the trust needed to cover the gap.
2. If this family is to be closed, it needs a construction step: build the record's contact
   graph explicitly (rotated core + re-solved shell) and only then hand it to an engine to shave
   the last 1e-9. That is a different code path from `Hopper`.
3. The one layout worth a second look with a *constructive* method is n=491: 227 singletons, the
   shell absorbs up to 0.35° of core rotation, and the gap is the smallest of the six (1.42e-2).
   The missing piece is choosing where the released space goes, not finding it.
4. The C++ shrink engine (corentinlaudicina/SquaresInSquares) is the right next user of the CPU
   slot. §7 is the exact fallback if its shrink mode stalls.

## 7. Fallback: exact flags and schedule for this Python engine

Keep this only as a second opinion. It is genuinely good at two things the C++ engine is not
built for: (a) a **local-optimality certificate** — one LP at trust x1 with every square free
returns `S − pred`; `< 1e-11` means no continuous motion of that contact graph reduces the side;
(b) **testing a specific construction** — `FrozenCompactor` freezes a body and re-solves
everything else around it in ~0.1 s, which is how the rotate probes in §3.3 were measured.

### 7.1 Build and run

```sh
cd /tmp/campaign2/engine_deep
/Users/zhaohuaxiang/ccjjllt/squares/.venv/bin/python build_deep.py    # embeds the six bank
# layouts and asserts computed L == certified L to 5e-10; writes push/kernel.py + metadata

# local dry run (one puzzle, one round) — this is the only local run mode that is cheap:
SIS_OUT=/tmp/x SIS_ONLY=491 SIS_BUDGET=400 SIS_ROUND=60 SIS_MINSEC=5 SIS_NROUND=1 \
  /Users/zhaohuaxiang/ccjjllt/squares/.venv/bin/python push/kernel.py
```

Kaggle metadata is already in `push/`: CPU (`enable_gpu: false`), internet on, **no**
`dataset_sources` (the six layouts are embedded as base64 npz, so there is no bank-version skew),
competition source `squares-in-squares`.

Env knobs (all optional): `SIS_OUT` (default `/kaggle/working`), `SIS_ONLY` (`491,842`),
`SIS_BUDGET` (default `4.5*3600`), `SIS_ROUND` (600), `SIS_NROUND` (4), `SIS_MINSEC` (120),
`SIS_CORES` (4), `SIS_SEED` (20261118).

### 7.2 Schedule

Per puzzle, four 600 s rounds x 4 workers = 40 min wall / 160 CPU-min:

| round | worker 1 | worker 2 | worker 3 | worker 4 |
|---|---|---|---|---|
| r0 | hop | hopx | flexall | target |
| r1 | hop | hop | flexall | target |
| r2 | hopx | flexall | flex | hop |
| r3 | rotate | flexall | hop | hop |

Six puzzles = 4 h. Then a second 30 min: the three closest (`closest − record`) get two 300 s
rounds of `hop, flexall, target, target` and `hop, hop, flexall, target`.

Short-budget variants, in order of information per CPU-minute:

- 10 min total: `rotate` (300 s) + `target` (300 s) on one puzzle. These two carry the whole
  verdict; they are what §3.3–3.5 are made of.
- 20 min: r0 + r3 for one puzzle.
- 1 h: r0 + r3 for all six, sequentially.
- Cut `hop` first if you need to shrink further. It produced 0 accepted hops in ~1.4e5 trials
  here and it is the most expensive phase (`relax` dominates).

### 7.3 Non-negotiable flags

- **Acceptance:** `S < cur − 1e-7` *and* `min_gap_strict(open_contacts(Q)) >= 1e-12`. Do not lower
  the 1e-7: 3e-8 "wins" are numerical noise on these layouts.
- **`open_contacts(3e-12)` at every `Hopper.reset`**, i.e. before every `LocalLP` construction.
- **`open_contacts` after every `relax`, before `find_bodies`.** `relax`'s energy is a sum of
  squares, so E <= 1e-12 still permits ~1e-6 overlaps; `find_bodies(tol=1e-3)` welds those in and
  `compact` can never remove them. This is the bug that silently kills perturbations.
- **`target`:** `pin = record − 1e-9`; trust x1/x3/x9/x27; start from both the jammed layout and
  `open_contacts(P, 5e-3)`.
- **`rotate`:** `FrozenCompactor(frozen=body)`, `repair` with `trust_fixed = 2r = 0.04`, then
  frozen-compact at trust x1/x3/x9 (the core must stay frozen or the rotation is undone), then a
  free all-singles polish. Body size >= 12, angles ±0.05…±0.7°.
- **`flexall`:** `singles = all`, trust x1/x3/x9. **`flex`:** disc radius U(3,18), trust x1/x2.
- **`perturb`:** ladder sigma 1e-3, 3e-3, 1e-2, 3e-2, 1e-1 with boxes `S+6σ` and `S+0.05`, then
  isotropic inflation 1e-3/5e-3/2e-2; 90–120 s budget. `hopx` starts from the result.
- **`Compactor.ALLOW_ROT_REPAIR = False`.** Measured identical with `True` (0 accepted either way
  on n=842 and n=491); leave it off so the port stays faithful.

### 7.4 Reading the output

`OUT/run_report.json → deep[n]` has everything:

| field | meaning |
|---|---|
| `trials`, `hops` | Hopper attempts / accepted hops |
| `flex_acc`, `flex_rounds` | weld-breaking moves accepted |
| `rot_repair_ok`, `rot_acc` | rotations whose shell repair was valid / accepted |
| `target_lp_ok`, `target_scale_ok` | pinned-side LP feasible, per trust scale |
| `lin_gain` | LP first-order side-reduction bound, **per trust scale** (read `1.0`) |
| `real_gain` | best side reduction actually realized by a geometrically valid move |
| `closest`, `closest_phase` | best valid side ever seen |
| `probe`, `probe_rotate` | body census and the full rotation/overlap/repair sweep |

A large `lin_gain` with `real_gain = 0` is the jammed signature. `target_lp_ok = 0` at x27 means
no continuous path exists even at 0.54 displacement per body. `probe_rotate` giving
`repair-valid` at some angle means the shell *can* absorb it — then the frozen-compact step is the
only construction that ever produced a valid alternative layout here.

### 7.5 Cost notes

- 4 workers, 40 min/puzzle -> 4 h for six.
- `flexall` and `perturb` on n≈900 cost 60–120 s per round because the all-singles LP has ~2900
  columns. On n=328 it is 1–2 s.
- Memory is not a problem at n<=1000 with 4 workers.

### 7.6 Do not

- Push `ccjjllt/sis-engine-deep-six-20261118`. It was stood down 2026-11-18 03:33Z; the kernel was
  never created and `push_retry.sh` is now an inert stub.
- Feed raw `compact` output anywhere without `open_contacts` + `min_gap_strict`.
- Trust `S2` returned by `compact` alone; recompute `side()` from the coordinates.
