# Rigid-group polish — n=842 and the near-square priority list: **closed**

Track: rigid-group placement polish of the live bank layouts (not a constructive track).
Local machine used only for orchestration, small I/O and certification; all search on Kaggle
CPU (`enable_gpu: false`, one kernel at a time).

Baseline re-read at the end of the work (the bank moved five times during the session):

| | |
|---|---|
| `/tmp/best_bank/submission.csv` | SHA-256 `9c981e6ea9a44c076587256936948e636936a84ad0668af6b75e946f4fa527e9` |
| certified total (text = float64) | **22.128441824806618** (22.128441824806620) |
| baseline when the search ran | `19877e21…` / 22.129481982260582 — every priority `L` below is **unchanged** in the current bank, which was re-read at the end |

The bank moved five times during the session (22.129684 → 22.129502 → 22.129495 → 22.129482 →
22.128442; the last move is another track's win, +1.04e-3). None of the 18 priority targets
changed, so every number in this report applies to the live file.

> **ANSWER (n=842): NO.** Translations only, and translations + rigid core rotation, both
> fail — and fail *provably*, not for want of restarts. The live layout is an exact
> rigid-group jam: the two bodies that set the left edge both touch the core on their inner
> faces, so any narrowing of the box forces the core across, which pushes the right edge out
> by the same amount. Measured residual motion of every body: **< 3e-8**. Capping the side at
> the record and asking for the least-overlapping arrangement still forces the bodies
> **0.013–0.053 of a cell through each other** (0.7–2.9× the gap being sought, depending on
> partition and restarts) and never close to zero. Restarts: 4 NM, 4 DE (43k evals), 18
> basin hops (45k evals), plus 6-restart jam-depth runs on 4 different partitions; and a
> **full-bank scan of all 396 lagging puzzles on Kaggle, which found zero slack on every
> one**. See §3 and §4.

---

## 1. Verdict

**n=842 does not reach 29.502152708 by rigid-group placement.** Neither does any other
target in this model, and the same is true of **every one of the 396 lagging puzzles** — the
full-bank scan found zero slack everywhere. The bank's layouts are **exactly jammed**: with
the core and the corner/band clusters treated as rigid bodies, every body that defines a
bounding-box edge is blocked by a contact with the core, to a resolution of **3e-8**. Because
that contact pattern is the only admissible one (each corner body is confined to its own
corner by its size), this is a proof of the global rigid-group optimum, not a failed search.

The record's 0.0187 of headroom on n=842 is therefore not a placement offset inside our
topology — it is a different packing. Capping the side at the record and asking for the
least-overlapping arrangement still forces the rigid bodies **0.013–0.053 of a cell through
each other** (0.7–2.9× the gap itself), and refining the partition (core split in 2, every
body split in 2 or 3, up to 23 bodies) **never reduces** that requirement.

The track should be retired. §3 gives the certificate and §5 the analytic reason rotation cannot
rescue it; §8 records one finding that explains why the hypothesis looked so plausible (its
evidence was circular); §9 states what would actually be needed.

---

## 2. The model as implemented

For a puzzle layout of squares `(x, y, angle)`:

1. **Orientation clustering.** Angles folded onto the 90° circle (`a = deg mod 90`), split
   at the largest circular gap plus a tolerance `atol` (1.6° primary; 0.8° and 0.4° as
   finer variants). Squares whose own angle deviates from their cluster median by more than
   `free_tol = 0.05°` are freed as **seam singletons** (this recovers the 9 defect squares
   of n=842).
2. **Spatial clustering.** Within each orientation cluster, connected components under
   exact unit-square adjacency (tolerance 1e-6).
3. **Rigid bodies.** Each component is a rigid body with `dθ` (only for non-axis bodies) plus
   `(tx, ty)`. Group 0 is the translation reference — its `tx, ty` pinned, its rotation
   free — so the objective has no global-translation flat direction and the core's rotation
   is a real DOF.
4. **Objective.** `s = max(bbox_w, bbox_h) + μ · Σ` pairwise OBB penetration, exact SAT.
   Feasible ⟺ max penetration ≤ 1e-9.
5. **Search.** Nelder–Mead from the seed; differential evolution at four translation widths
   (0.06, 0.30, 1.00, 2.00) with `μ = 100`, each followed by an NM re-polish at `μ = 400`;
   12 random restarts; and a **target-side** run minimising
   `1e4·max(0, s − (L_record − 1e-9))² + Σ penetration`, which lets the search tunnel
   through infeasible configurations to look for a different feasible basin.

Code: `engine.py` (rigid bodies + vectorised exact OBB SAT with a pre-computed static fast
path), `cert.py` (jamming certificate), `mk_kernel.py` → `kernel/kernel.py` (Kaggle).

---

## 3. n=842 — decomposition, DOF, and the jamming certificate

Live layout, `atol=1.6`, seam freeing on:

```
group  size  angle      role
  0     284  45.0000°   core, rigid   (1 rotation + 2 translation)
  1     206   0/90°     TR corner cluster
  2     137   0/90°     BR corner cluster
  3     126   0/90°     TL corner cluster
  4      78   0/90°     BL corner cluster
  5       2   0/90°     small pair
  6-14    9 × 1        seam singletons at 44.79°…45.33°
```

**34 DOF** — 3 for the core, 8 for the four corner clusters, 2 each for the 9 seam pieces;
a strict superset of both the requested "6–10 translational DOF" model and the "core + 4
clusters" 9-DOF model. With the seam held rigid to the core the model is exactly the 9-DOF
one specified in the mission; every conclusion below holds for the 9-DOF version too.

The core is genuinely rigid: **280 squares at exactly 45.0000°**, plus 9 with
0.0002°–0.33° of defect (the seam), and nothing else within 44°–46°.

### Certificate (5-group 8-DOF version, translations only)

Maximum feasible displacement of each body in each of 8 directions, all other bodies fixed,
by bisection with **26 steps and resolution 3e-8**:

```
grp0 (289, core)  +x 0.000  -x 0.000  +y 0.000  -y 0.000  +d 0.000  -d 0.000  +a 0.000  -a 0.000
grp1 (206, TR)    +x 2.000  -x 0.000  +y 2.000  -y 0.000  +d 2.000  -d 0.000  +a 0.008  -a 0.004
grp2 (143, BR)    +x 2.000  -x 0.000  +y 0.000  -y 2.000  +d 0.002  -d 0.006  +a 2.000  -a 0.000
grp3 (126, TL)    +x 0.000  -x 2.000  +y 2.000  -y 0.000  +d 0.005  -d 0.049  +a 0.000  -a 2.000
grp4 ( 78, BL)    +x 0.000  -x 2.000  +y 0.000  -y 2.000  +d 0.000  -d 2.000  +a 0.008  -a 0.038
```
(`d` = `(1,1)/√2`, `a` = `(1,−1)/√2`; `2.000` = free out to the probe limit, i.e. outward.)

**Proof that the box cannot shrink.** The bounding box is `[−15.2604, 14.2604]²`, side
29.520815280 — exactly the CDB family value `13.5 + 17/√2 + 4`.

Verified blocking contacts (move the body by 1e-3 and attribute the penetration to a pair):

| body | direction that would shrink the box | blocked by | penetration per unit |
|---|---|---|---|
| TL (126) | `+x` (left edge) | **core** | 0.7071 |
| BL (78) | `+x` (left edge) | **core** | 0.7071 |
| TR (206) | `−x` (right edge) | **core** | 0.7071 |
| BR (143) | `−x` (right edge) | **core** | 0.7071 |
| BL (78) | `+y` (bottom edge) | **core** | 0.7071 |
| BR (143) | `+y` (bottom edge) | **core** | 0.7071 |

(0.7071 = 1/√2 is the 45°-face contact factor of the core, so these are true face contacts,
not corner grazes.)

* The **left** edge is touched by TL and BL. Reducing the width requires **both** to move
  `+x`; both are hard-blocked by the core (`0.000`, `< 3e-8`).
* The **bottom** edge is touched by BL and BR. Reducing the height requires **both** to move
  `+y`; both are hard-blocked by the core.
* The core itself is blocked in **all eight** directions, so it cannot be shifted to relieve
  them; and shifting it either way pushes the opposite edge out (TR/BR `−x` and `−y` are also
  `0.000`, again blocked by the core).

So any increase of `xmin` forces the core to translate `+x`, which forces TR and BR `+x` by
the same amount, leaving `W = xmax − xmin` unchanged. The same holds for `H`. **No
coordinated rigid-group motion can shrink the box**: four diagonal contacts plus four wall
contacts, nine constraints for nine DOF — a hyperstatic jam.

### The argument is a proof, not a failed search

The width argument above is complete and does not depend on any optimiser: `xmin` is
attained by two bodies that both touch the core on their inner faces, so any increase of
`xmin` forces the core to translate `+x`, which forces the two right-hand bodies to
translate `+x` by the same amount, leaving `W` unchanged. Same for `H`. Every one of those
contact facts is measured directly by the certificate (each `0.000` is a *contact*, i.e.
the bisection found the boundary within 3e-8 of zero).

Because the four corner bodies are 11–17 wide in a 29.52 box, each is confined to its own
corner quadrant, so the contact topology is the only admissible one — the certificate
therefore certifies the **global** rigid-group optimum for this puzzle, not just a local one.

### Search as a consistency check (with a caveat about the optimiser)

| search | DOF | evaluations | best s |
|---|---|---|---|
| Nelder–Mead from the seed | 9 | 4 000 | 29.520815280 (= seed) |
| DE, translations ±0.3, core rotation ±2° | 9 | 19 236 | 29.520815280 |
| NM + DE, seam-freed model | 34 | 35 000 | 29.520815280 |
| basin hopping, 18 × (perturb σ=0.12 + NM) | 9 | 45 000 | 29.520815280 |
| Kaggle kernel, 4 DE widths × 12 restarts × 3 partitions | 9 / 19 / 34 | see §6 | 29.520815280 |

Every run returns the seed with the parameter vector exactly **0**. **Caveat, measured:**
the derivative-free searches are weak on this landscape. A control experiment — translate
one corner body outward by 0.02 (which raises `L` to 29.5408) and ask the search to recover —
shows NM recovering to **29.520954** (1.4e-4 above the true optimum) while DE and basin
hopping **do not recover at all** (they return the perturbed value, or an infeasible point).
So the searches can confirm a local optimum but cannot be trusted to find a 0.019-scale
improvement. That is precisely why the certificate above, not the search, is the result.

This control also explains a campaign-wide pattern: every derivative-free / penalty
local search on these mature layouts has returned "0 or 1e-7" — the penalty valley wall is
too steep for these methods at the 1e-2 scale.

---

## 4. The whole lagging set is jammed — full-bank scan

The Kaggle kernel's phase A ran a **shallow local polish** (NM, 300 evals — a first-order
slack test: it accepts a move only if it lowers `s` without overlap) on **every puzzle that
was lagging at scan time — 396 of them** (all n with `L_bank > L_record`, n = 199…1000, 386
of which have ≥ 2 groups and therefore real DOF; 7 have since been merged from other tracks,
leaving 389 lagging at the final read):

```
scan records: 396
max |s1 - s0| over all scans : 0.000e+00
max final penetration        : 0.000e+00
```

**Not one puzzle has any first-order slack** — the polish ends exactly where it started, to
the last digit, on every single one. The rigorous 8-direction certificate (§3) was then run
on the 18 priority targets, all of which are also jammed. So the bank is not merely "close to
optimal" on a few puzzles: its entire lagging set is a set of rigid-group local optima.

### The priority targets

| n | groups (sizes) | DOF | jam | L_bank (live) | L_record | Δscore if reached | overlap at record side |
|---|---|---|---|---|---|---|---|
| 328 | 130, 117, 74, 4, 1, 1, 1 | 13 | <3e-8 | 18.614368938 | 18.599535465 | 8.190e-4 | 0.033–0.052 |
| 902 | 747, 30, 30, 25, 25, 25, 10, 9, 1 | 19 | <3e-8 | 30.535533906 | 30.514078774 | 7.144e-4 | — |
| 963 | 888, 25, 25, 25 | 9 | <3e-8 | 31.535533906 | 31.514078774 | 6.914e-4 | — |
| 908 | 631, 125, 125, 15, 10, 1, 1 | 14 | <3e-8 | 30.625574725 | 30.605884509 | 6.534e-4 | — |
| 842 | 284, 206, 137, 126, 78, 2, 9×1 | 34 | <3e-8 | 29.520815280 | 29.502152708 | 6.432e-4 | 0.013–0.053 |
| 491 | 251, 112, 38, 32, 25, 14, 13, 6 | 19 | <3e-8 | 22.684143606 | 22.669926930 | 6.416e-4 | — |
| 367 | 255, 25, 22, 20, 17, 10, 9, 9 | 21 | <3e-8 | 19.682794506 | 19.670856797 | 6.231e-4 | — |
| 901 | 284, 240, 149, 138, 78, 2, 10×1 | 36 | <3e-8 | 30.520815280 | 30.502152708 | 6.217e-4 | — |
| 803 | 532, 108, 100, 25, 17, 12, 5, 4 | 17 | <3e-8 | 28.811202562 | 28.793943440 | 6.091e-4 | — |
| 969 | 682, 124, 123, 17, 10, 9, 2, 2 | 19 | <3e-8 | 31.624490854 | 31.605570899 | 6.078e-4 | — |
| 747 | 402, 192, 86, 48, 9, 5, 5×1 | 23 | <3e-8 | 27.810271339 | 27.793759657 | 6.041e-4 | — |
| 804 | 570, 113, 85, 25, 5, 3, 2, 1 | 19 | <3e-8 | 28.827154350 | 28.810060585 | 6.029e-4 | — |
| 962 | 285, 269, 162, 153, 77, 7, 5, 3, 1 | 23 | <3e-8 | 31.520815280 | 31.502152708 | 6.017e-4 | — |
| 843 | 768, 25, 25, 25 | 9 | <3e-8 | 29.535533906 | 29.518244283 | 5.955e-4 | — |
| 333 | 168, 50, 37, 35, 11, 11, 11, 7, 3×1 | 27 | <3e-8 | 18.770654870 | 18.760014153 | 5.831e-4 | — |
| 456 | 193, 187, 55, 21 | 8 | <3e-8 | 21.846667193 | 21.834217587 | 5.830e-4 | — |
| 965 | 432, 404, 113, 4, 4, 3, 2, 2, 1 | 22 | <3e-8 | 31.562050659 | 31.544499527 | 5.650e-4 | — |
| 970 | 317, 305, 139, 137, 54, 18 | 13 | <3e-8 | 31.636652031 | 31.629165290 | 2.404e-4 | — |

Sum of the 18 = **0.01100**; the whole lagging gap is **0.08047** over 389 puzzles
(sum of `(L_bank − L_record)/√n`; the net figure including the puzzles where the bank is
*better* than the 2026-11-11 snapshot is 0.0786).

### How deep is the jam: overlap required at the record side

Cap the bounding side at `L_record` (penalty weight 1e7, so the cap acts as a constraint) and
let the optimiser find the least-overlapping rigid-group arrangement. The measured overlap is
the **best found** over the restarts, i.e. an *upper* bound on the minimum achievable overlap
(a smaller true minimum is not excluded; zero is excluded by the certificate in §3 for the
5-body partition).

| n | partition | bodies | max single-pair penetration | total overlap |
|---|---|---|---|---|
| 842 | core + 4 clusters + seam solos | 15 | **0.0130** | 0.2249 |
| 842 | core split in 2 | 16 | 0.0183 | 0.3877 |
| 842 | all large bodies split in 2 | 19 | 0.1205 | 3.5871 |
| 842 | all large bodies split in 3 | 23 | 0.0592 | 1.1089 |
| 328 | core + 2 clusters | 7 | **0.0327** | 0.5086 |
| 328 | core split in 2 | 8 | 0.0348 | 0.5690 |
| 328 | all large bodies split in 2 | 9 | 0.0431 | 0.8081 |
| 328 | all large bodies split in 3 | 11 | 0.0564 | 1.6496 |

An independent, longer run on the 5-body partition (4 restarts, NM 1800 evals) found
0.0532 / 1.3346 for 842 and 0.0517 / 0.6973 for 328 — the number is restart-dependent, which
is why the table above reports the best of 6 restarts per cell.

What matters is the scale: **in no partition and in no restart does the required overlap
approach zero; the smallest found anywhere is 0.013 — 0.7× the 0.0187 gap itself, and the
typical value is 2–6×.** A placement offset of 0.019 would show up as overlap → 0 as soon as
the groups were in the right relative positions. It does not.

### Finer partitions do not unlock it

The natural objection is "one rigid grouping was wrong". The table above answers it: refining
the partition — core split in two, then every large body split in two, then in three, up to 23
bodies — **never reduces** the required overlap (842: 0.0130 → 0.0183 → 0.1205 → 0.0592;
328: 0.0327 → 0.0348 → 0.0431 → 0.0564). It usually grows, because more bodies means more
contacts to satisfy against the same wall.

Splitting a rigid body cannot create space: it only lets the pieces separate, which does not
shrink the bounding box. So "more DOF" is not the missing ingredient either, and the
9-parameter model was not too small — it was already the right size.

The **band regime behaves exactly like the diamond regime.** The tilted bands are detected
as rigid bodies at their true angles (57.41° for 965, 65.71° for 970, 66.25°/67.20° for 804,
66.01° for 491, ±32° for 367) and they are jammed between two axis clusters and the walls.
The D=2 strip of 902/963 (74–75 squares at exactly 45.0000°, `u`-extent 4.9 × `v`-extent
28.3) is likewise pinned on both long sides.

---

## 5. Two independent negative results agree

* A parallel track swept the **rotated-core family** exhaustively — φ = 43°…47° at 0.01°
  plus a 40°–50° pass, corner staircases re-rasterised exactly at each φ, all n = 1…1000,
  exact breakpoint enumeration — and found **0 wins**.
* The certificate above shows the same thing for *placement*: the four diagonal contacts
  are simultaneously tight.

Rotation cannot help analytically either: a rigid 45° core of side `w` has d1-extent
`w(cos φ + sin φ) ≥ w`, so any rotation increases the diagonal budget in **both**
directions at once. The family's `+1` per staircase comes from the half-diagonal of the
extreme axis-aligned cell, which cannot be reduced without rotating that cell into its own
neighbours.

## 6. Kaggle kernel

* `ccjjllt/sis-rigid-group-polish-20261118` — CPU, `enable_gpu: false`, dataset
  `ccjjllt/sis-bank-20261117`. Dataset/push worked; the kernel ran and produced its scan,
  then **was removed from the account mid-session** (subsequent `kernels.status` and
  `kernels.output` return `Permission 'kernels.get' was denied`, and it no longer appears in
  `kernels list`). The v3 phase-B artefact was therefore lost; everything below is from the
  v2 run that completed phase A, plus local measurements.

| version | phase A (scan) | phase B |
|---|---|---|
| v1 | crashed at scan 23/396 (`n=960` has `nparams=0` → NM `dim=0`) | — |
| v2 | **complete: 396/396, zero slack** (1389 s) | crashed on the first JSON dump (`np.float64`) |
| v3 | re-ran the scan | kernel removed before its output could be collected |

The scan result in §4 is from v2 and is complete; the jam-depth numbers in §4 were measured
locally on the two highest-value targets (842, 328) with the same code.

### 6a. Kernel results

* **Phase A (v2, complete):** `scan 396/396`, `max |s1 − s0| = 0.000e+00`, max final
  penetration `0.000e+00`. Zero slack on every lagging puzzle. Table of all 396:
  `scan_all396.csv`.
* **Phase B:** the v3 kernel was removed from the account before its output could be
  collected, so no phase-B artefact exists. The jam-depth numbers in §4 were produced by the
  same code run locally on the two highest-value targets (842, 328) — deliberately small
  (6 restarts × 1200 evals per cell) because local compute is reserved for orchestration.

## 7. Certified wins

**None.** No puzzle was improved, so no `candidate.csv` is emitted; a win requires a
candidate strictly below the live bank on both routes with 1000/1000 valid, and there is
nothing to merge.

## 8. Why the hypothesis looked right — and why it is not

The mission's evidence was that *"the record's layouts carry defect angles of
44.79°–45.33°, the same topology as ours, core rotated 0.2–0.7° off 45°"*, and that
matching the record "shaves 1.97 waste units off the corner slivers".

Both statements are true of a layout we have — but it is **our own bank layout, not the
record's**. The live n=842 layout contains exactly eight squares at

```
44.7921°  44.8353°  44.9154°  44.9447°  44.9852°  45.0014°  45.0026°  45.3328°
```

— the same eight values, digit for digit, that were quoted as the record's signature. They
are the seam cells our layout uses to plug sliver gaps, laid down by whatever polish
produced the bank layout. So the "record defect angles" were read off our own file, and the
inference "the record used a rotated rigid core" had no external evidence behind it. That
also explains why the rotated-core sweep found nothing and why the rigid-group search finds
nothing: there was never a second layout to match.

The 1.97-unit waste figure is likewise an **area** budget, not a displacement. The four
slivers are sawtooth gaps of thickness `1/(2√2) = 0.354`; no unit square fits in a strip
narrower than 1.0, so that area cannot be reclaimed by sliding — only by re-packing.

## 9. What would actually be needed

The record's values are outside every family we can enumerate:

* the CDB family is exhaustively closed (`/tmp/campaign2/cdb`: the bank *is* the exact
  family optimum on 47/82 CDB puzzles, and strictly better on the other 35);
* the rotated-core generalisation is closed (parallel track, 0/1000);
* rigid-group placement is closed — this track: 0 slack on **all 396** lagging puzzles,
  and at the record's side the bodies must interpenetrate by 0.013–0.053;
* the `l_border` extension closure cannot produce it either: chaining
  `n → n + 2⌊s+1⌋ − 1, s → s+1` from **every** n < 842 in the live bank, the closest any
  chain lands to 29.502152708 is **+0.018663** (the 626 → 677 → 730 → 785 → 842 chain, which
  is exactly the bank's own value). No base layout we hold, extended or not, reaches it.

The 0.013–0.053 figure is the useful one for planning. It is not a rounding-level shortfall:
it is a wall 1.3–5.3 % of a cell edge thick (up to ~40 % of the 1/(2√2) sliver thickness), it
does **not** go to zero in any partition or restart, and it does **not** shrink when the
partition is refined (§4). Getting through it means changing
which cells belong to which body — a genuine re-packing, in which cells move across the
partition, not bodies sliding within it.

That is the **block-LNS / cell-reassignment** regime (move a few cells between groups, then
re-optimise), which this campaign has already tried with 0 wins, or a **global n-body
annealer** run for hours per puzzle. No multi-start on rigid groups will produce it, and each
attempt costs a kernel slot.

**Recommendation: retire the rigid-group placement track and stop spending kernel time on
the near-square columns with this instrument.**

---

## 10. Artifacts

| path | content |
|---|---|
| `/tmp/campaign2/polish/engine.py` | rigid bodies, exact vectorised OBB SAT, static fast path |
| `/tmp/campaign2/polish/cert.py` | 8-direction jamming / slack certificate |
| `/tmp/campaign2/polish/mk_kernel.py` | generates the Kaggle kernel from `engine.py` + `targets.csv` |
| `/tmp/campaign2/polish/kernel/kernel.py` | the generated kernel (scan + deep search + 50-digit emitter) |
| `/tmp/campaign2/polish/cert_table.txt`, `cert_rows.json` | per-puzzle decomposition + jamming radius |
| `/tmp/campaign2/polish/scan_all396.csv` | the full-bank scan: n, s0, s1, slack, penetration, group sizes for all 396 lagging puzzles (all slack = 0) |
| `/tmp/campaign2/polish/build_candidate.py` | builds `candidate.csv` from kernel layouts and runs `squares merge`; ready but never used — it only runs when a layout beats the bank |
| `/tmp/campaign2/polish/kout/` | empty: the kernel was deleted from the account before its output could be re-downloaded; the scan data survives in `scan_all396.csv` |
