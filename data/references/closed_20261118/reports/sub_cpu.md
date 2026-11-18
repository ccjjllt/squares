# CPU hop / fixed-side (X3) / scaled hop experiments — report

Date: 2026-11-17.  Scope: Kaggle CPU only, no local optimization, no submission.  The
bank (`/tmp/best_bank/submission.csv`) was not written by this subagent; it was
updated by the main pipeline (see §6.4).

## TL;DR

- **The packer runs on Kaggle CPU.** The kit is a prebuilt x86_64 static binary
  (`x86_64-unknown-linux-musl`, no `PT_INTERP`) shipped as a Kaggle dataset; the
  Kaggle CPU image has **no cargo and no rustc**, so a prebuilt binary is the clean
  route. Dataset v4 `ccjjllt/sis-cpu-hop-kit-20261117` is `ready`; the binary round
  trip was checked byte-for-byte.
- **Smoke kernel v3 `COMPLETE`**: 12 puzzles, 2 min each, 4 workers; n=367 improved
  by 1.043392e-05 in L (score +5.45e-7), certified; the other 11 no change. The main
  session merged n=367 into the bank.
- **Scaled hop kernel v1 `COMPLETE`**: 20 targets × 2 seeds, 600 s per chain, 4
  workers; **3 certified wins** — n=333 (+5.980179e-06), n=803 (+3.592685e-06),
  n=747 (+2.574905e-08), total **9.598613e-06**. The merge output scores
  **22.13101404834979** (text and float64, 1000 valid, 0 invalid/missing) and is now
  byte-identical to the bank (`eab2f56c…`), which the main pipeline updated at 19:19;
  this subagent did not write the bank.
- **X3 fixed-side kernel `COMPLETE`, negative**: 61 cells at the record sides
  (0.0176–0.0215 below the bank) found **0 feasible** packings in 240 s per cell.
  The `packer hop` fixed-side route is not enough at this distance; the `harden`
  momentum route is the untested alternative.
- Two environment workarounds were necessary and are documented below: pinning
  `www.googleapis.com` for uploads, and cross-compiling for x86_64 (Docker on this
  Apple-silicon Mac builds arm64 by default).

## 1. What was checked

### 1.1 Kaggle CPU image

From the completed smoke `run_report.json` (kernel v3, `COMPLETE`):

```
python      3.13.18 (main, Oct 26 2026) [GCC 13.3.0]
platform    Linux-6.18.55+-x86_64-with-glibc2.39
machine     x86_64
cpu_count   4
memory_gb   33.7
which       cargo=null  rustc=null  cc=/usr/bin/cc  gcc=/usr/bin/gcc  file=/usr/bin/file
fq          /tmp/kit/packer/packer/target/release/fq, 6,276,096 bytes,
            sha256 e6cf6ab5c274804199f4bf3e9bfaa5d43f49171ce9e6bf4fbeb071419ddd9c0d
preflight   returncode 0, {"s": 2.000000000000766, "min_gap": 2.75e-13, "min_wall": 1.01e-13}
```

**The Kaggle CPU image has no cargo and no rustc** (`which` returns null), so
building the packer inside the kernel is not the clean route; a prebuilt static
binary is. No internet is needed by the experiment, and the kernel was pushed with
`enable_internet: true` successfully, but the run does not depend on it.

### 1.2 Upload path (important)

`www.googleapis.com` (the GCS resumable-upload endpoint used by the Kaggle CLI) is
blackholed from this network: every `172.217.x` address, IPv4 and IPv6, stalls in
`SYN_SENT`, while `storage.googleapis.com` (`34.x`) is reachable. The CLI therefore
hung at `0%` for 15+ minutes. Workaround: `/tmp/sub_cpu/kaggle4.py`, a wrapper that

1. filters `getaddrinfo` to IPv4,
2. pins `www.googleapis.com` to a reachable Google front end
   (`KAGGLE_PIN=www.googleapis.com=34.153.3.27`),
3. sets a 20 s socket timeout.

Every Kaggle command in this report is run through that wrapper:

```sh
export KAGGLE_API_TOKEN=$(cat ~/.kaggle/access_token_ccjjllt_check)
export KAGGLE_PIN=www.googleapis.com=34.153.3.27
PY=/Users/zhaohuaxiang/ccjjllt/squares/.venv/bin/python
$PY /tmp/sub_cpu/kaggle4.py datasets status  ccjjllt/sis-cpu-hop-kit-20261117
$PY /tmp/sub_cpu/kaggle4.py kernels  status  ccjjllt/sis-cpu-hop-smoke-20261117
$PY /tmp/sub_cpu/kaggle4.py kernels  logs    ccjjllt/sis-cpu-hop-smoke-20261117
```

### 1.3 Architecture trap

Docker Desktop on this Apple-silicon Mac builds `linux/arm64` by default. The first
kit therefore shipped an AArch64 `fq`, and Kaggle (x86_64) failed with:

```
OSError: [Errno 8] Exec format error: '/kaggle/working/kit/packer/packer/target/release/fq'
```

Evidence: `/tmp/sub_cpu/smoke_v1_log.json`, kernel version 1 of
`ccjjllt/sis-cpu-hop-smoke-20261117`.

The `--platform linux/amd64` Docker route could not be used reliably (the emulated
container lost DNS), so the binaries were cross-compiled on the host with the musl
self-contained toolchain and `rust-lld`:

```sh
cd /tmp/sub_cpu/build/packer-src        # evand/square-packing search/packer, no .cargo/ (target-cpu=native removed)
rustup target add x86_64-unknown-linux-musl
SYS=$(rustc --print sysroot); HOST=$(rustc -vV | sed -n 's/^host: //p')
RUSTFLAGS="-C linker=$SYS/lib/rustlib/$HOST/bin/rust-lld" \
  cargo build --release --offline --target x86_64-unknown-linux-musl \
  --bin fq --bin packer --bin harden
```

Result: ELF `e_machine=62` (x86-64), no `PT_INTERP` (fully static), sizes 6.3/2.8/2.6 MB.
The crates came from the host `~/.cargo` cache (`--offline`) because `index.crates.io`
was also failing DNS at that moment.

## 2. Artifacts

| artifact | ref | state |
|---|---|---|
| dataset | `ccjjllt/sis-cpu-hop-kit-20261117` | v4, `ready` |
| dataset contents | `packer.zip` (source + `fq`, `packer`, `harden`), `official_metric.py`, `targets.csv` (12-n smoke rows), `targets20.csv` (current bank rows for the 20 scaled-hop targets), `targets_gap.csv` | |
| smoke kernel | `ccjjllt/sis-cpu-hop-smoke-20261117` | v1 ERROR (arm64), v2 ERROR (string→float bug), **v3 COMPLETE** (n=367 win) |
| X3 kernel | `ccjjllt/sis-x3-fixedside-20261117` | v1 ERROR (mount path), **v2 COMPLETE** (0 feasible) |
| scaled hop kernel | `ccjjllt/sis-hop-scaled-20261117` | **v1 COMPLETE** (3 wins) |
| local kit | `/tmp/sub_cpu/dataset`, `/tmp/sub_cpu/kit_upload` | |
| local kernels | `/tmp/sub_cpu/kernel`, `/tmp/sub_cpu/x3_kernel`, `/tmp/sub_cpu/hop_scaled` | |

The dataset zip is auto-extracted by Kaggle into `packer/packer/...`; both kernels
locate the real packer root by searching for `hop.py` next to `target/release/fq`
(or `packer` for X3), so the extra nesting is harmless.

Verified by round trip (`kaggle datasets download ... --unzip`, `/tmp/sub_cpu/dl_ds`):
`packer/packer/target/release/{fq,packer,harden}` are present, ELF `e_machine=62`
(x86-64), and `fq` is byte-identical to the local x86_64 build
(sha256 `e6cf6ab5c274804199f4bf3e9bfaa5d43f49171ce9e6bf4fbeb071419ddd9c0d`).

## 3. Smoke kernel (fq quench + `hop.search`)

`/tmp/sub_cpu/kernel/main.py` is the public `33_hop.py` pipeline adapted to a
self-contained script kernel:

- 12 target n from the top-gap list (`328, 367, 491, 803, 842, 901, 902, 908, 962,
  963, 965, 969`), bank rows embedded in the dataset (`targets.csv`, exact decimal
  strings from `/tmp/best_bank/submission.csv`);
- 4 workers, 1 seed, `SIS_MINUTES` (default 2.0) per puzzle, `T=1e-5`;
- initial `fq quench` then `hop.search` (Metropolis over global/local kicks), exactly
  the 33_hop logic, including the `hop.quench` failure wrapper;
- only certified improvements are written to `improved_groups.csv`; certification is
  the host metric (`official_metric.verify_puzzle` + `measure_side_mp`, mpmath
  60 dps, interval SAT with escalation);
- `run_report.json` carries per-puzzle `L0_mp`, `L0_float`, `L1_quench`, `L1_mp`,
  gain, seconds, seed, fq quench stats, binary sha256, `platform.machine()`, and
  `which(cargo/rustc/cc/gcc)`.

Exact commands used:

```sh
$PY /tmp/sub_cpu/kaggle4.py kernels push -p /tmp/sub_cpu/kernel
$PY /tmp/sub_cpu/kaggle4.py kernels status ccjjllt/sis-cpu-hop-smoke-20261117
$PY /tmp/sub_cpu/kaggle4.py kernels output ccjjllt/sis-cpu-hop-smoke-20261117 \
    -p /tmp/sub_cpu/dl_smoke2 --file-pattern '(^|/)(run_report\.json|improved_groups\.csv|.*\.jsonl)$'
```

## 4. X3 fixed-side feasibility (`packer hop`)

Implemented in `/tmp/sub_cpu/x3_kernel/main.py`; targets are the near-square records
from `data/references/leaderboards/perpuzzle_best_20261111.csv`.

Per cell:

```sh
packer hop --in seeds/n<N>_<seed>.txt --s <L_record + delta> --seed 7 \
           --iters 1000000000 --descend 1e-4 --out cells/<tag>.txt --quiet
packer relax --in cells/<tag>.txt --s <s_out> --squeeze --out cells/<tag>.txt.relax
```

The process is killed after `X3_CELL_SECONDS` (default 240); `packer hop` writes its
`--out` only when the side is feasible, atomically, so a killed run keeps its best
feasible packing. The parent certifies both the raw and the relaxed file with
`official_metric` and keeps the smaller certified side.

Certification detail: `packer` writes angles in degrees with 15 decimals, so a
degree→radian round trip can leave a ~1e-15 overlap on a touching layout. The
certifier therefore retries the layout scaled about its bbox centre by
`1+{1e-12,1e-11,1e-10,1e-9,1e-8,1e-7}` and keeps the first scale that the host
metric certifies (the side grows by ~L·eps ≤ 3e-6, negligible against the 0.019–0.021
deficits). The mock drill at `/tmp/sub_cpu/x3_test` exercises the full 16-cell path
with a fake packer and confirmed the scale ladder repairs a 1e-15 overlap and writes
a valid `run_report.json`/`improved_groups.csv`. No target optimization was run
locally.

Ladder: `delta ∈ {0, 2e-4, 5e-4, 1e-3, 2e-3}` with the `asis` seed; `delta ∈
{5e-4, 2e-3}` with a pre-scaled seed (`f=(L-1)/(L0-1)` on centres); a per-square
angle-jitter seed (±0.3°) for D=1/2. 61 cells × 240 s / 4 workers ≈ 60 min, highest-payoff targets
(D=1 → D=2 → D=4 → D=8) first.

`--descend 1e-4` also walks the rungs downward from a looser start when it reaches
feasibility, so the five explicit rungs are starts, not the only sides tried.

## 5. Target table (bank vs record)

Bank sides measured with the host metric at 60 dps from the exact bank strings.

| n | D | bank L0 (mp) | record L | deficit | potential gain if record |
|---|---|---|---|---|---|
| 842 | 1 | 29.520815280171 | 29.502152707903 | 0.018663 | 0.000643 |
| 901 | 1 | 30.520815280171 | 30.502152707908 | 0.018663 | 0.000622 |
| 962 | 1 | 31.520815280171 | 31.502152707911 | 0.018663 | 0.000602 |
| 902 | 2 | 30.535533905933 | 30.514078774139 | 0.021455 | 0.000714 |
| 963 | 2 | 31.535533905933 | 31.514078774129 | 0.021455 | 0.000691 |
| 965 | 4 | 31.562050658717 | 31.544499526788 | 0.017551 | 0.000565 |
| 908 | 8 | 30.625574725146 | 30.605884508570 | 0.019690 | 0.000653 |
| 969 | 8 | 31.624490853785 | 31.605570898559 | 0.018920 | 0.000608 |

Total if all eight reach the record: **0.005099**.

## 6. Results

### 6.1 Smoke kernel v3 — COMPLETE

Kernel: `ccjjllt/sis-cpu-hop-smoke-20261117` version 3, status
`KernelWorkerStatus.COMPLETE`, wall 1464.7 s, 12 puzzles, 2 min search each, 1 seed,
4 workers. Outputs downloaded to `/tmp/sub_cpu/dl_smoke2/` (`run_report.json`,
`logs/hop_n*_s0.jsonl`, kernel log).

| n | L0 (bank, mp) | L1 (best, mp) | gain | certified |
|---|---|---|---|---|
| 367 | 19.682994390728600 | 19.682794505625298 | **1.043392e-05** | yes |
| 328 | 18.614368938490987 | 18.614368938508600 | -9.7e-13 | yes |
| 491 | 22.684143606359193 | 22.684143606359192 | ~0 | yes |
| 803 | 28.814116436573623 | 28.814116436573623 | ~0 | yes |
| 842 | 29.520815280171445 | 29.520815280171445 | 0 | yes |
| 901 | 30.520815280171451 | 30.520815280171451 | 0 | yes |
| 902 | 30.535533905932952 | 30.535533905932952 | ~0 | yes |
| 908 | 30.625574725145633 | 30.625574725145633 | ~0 | yes |
| 962 | 31.520815280171474 | 31.520815280172000 | -9.8e-13 | yes |
| 963 | 31.535533905932983 | 31.535533905963524 | -9.8e-13 | yes |
| 965 | 31.562050658716569 | 31.562050658716569 | ~0 | yes |
| 969 | 31.624490853784550 | 31.624490853784551 | ~0 | yes |

`improved_groups.csv` contained exactly the n=367 group. The main session merged it
into the bank (SHA `9b0bcce13ddc7879c4e395ea72e28149b96f92e8552915300929bfb54a2181ce`
at 17:11); the scaled-hop merge later used that bank as its baseline
(score 22.131023646963278 by the merge arithmetic, see §6.4). This subagent did
not modify the bank.

### 6.2 X3 fixed-side kernel

- Run 1: `ERROR` — `find_kit` only looked one level under `/kaggle/input`, but the
  dataset was mounted at `/kaggle/input/datasets/...`; fixed with a recursive search.
- Run 2 (`ccjjllt/sis-x3-fixedside-20261117` v2): `COMPLETE`, wall 3863.6 s, 61
  cells (8 targets × 5 asis rungs + 2 scaled rungs + 5 angle-jitter cells).
  **0 certified feasible outputs, 0 wins**: all 61 cells ran the full 240 s without
  `packer hop` reaching an overlap-free packing at the fixed record side; 58 cells
  left only a best-energy `*.inf` file. This is the expected negative in the
  near-record regime: the record sides are 0.0176–0.0215 (0.06–0.07 %) below the
  bank, and a fixed-side basin hop from the bank/scaled/jitter seeds did not close
  that gap in 4 minutes. Outputs: `/tmp/sub_cpu/dl_x3b/` (`run_report.json` 11.8 kB,
  `improved_groups.csv` header-only).

### 6.3 Scaled hop kernel — COMPLETE, 3 wins

Kernel: `ccjjllt/sis-hop-scaled-20261117` version 1, status
`KernelWorkerStatus.COMPLETE`, wall 6401.2 s, 20 targets × 2 seeds, `packer hop`
descending from the current bank side, 600 s hard timeout per chain, 4 workers.
All 40 chains hit the full 600 s timeout (that is the protocol, not an error).
Outputs: `/tmp/sub_cpu/dl_hop_scaled/{run_report.json (15.9 kB),
improved_groups.csv (130 kB)}`.

Independent re-certification of the downloaded CSV (host metric at 60 dps, from
the exact written strings):

| n | D | bank L0 | hop L1 | L gain | score gain | seed |
|---|---|---|---|---|---|---|
| 333 | 9 | 18.770763998141440 | 18.770654870107466 | 1.091280e-04 | **5.980179e-06** | jitter |
| 803 | 19 | 28.811304369188422 | 28.811202562358366 | 1.018068e-04 | **3.592685e-06** | asis |
| 747 | 18 | 27.810272042933633 | 27.810271339178615 | 7.037550e-07 | **2.574905e-08** | asis |

The other 17 targets have no certified strict improvement; their chains end at the
bank side (or ~1e-12 above it after the certification dilation). n=367, the earlier
smoke win, is unchanged by this run (−1.5e-16).
`run_report.json` has per-target `L0_mp`, `D`, both chain results (`seed`, `s_out`,
`L1_mp`, `gain`, `seconds`, `certified`, `improved`); no chain dumps.  Kernel log
evidence (`/tmp/sub_cpu/dl_hop_scaled/sis-hop-scaled-20261117.log`):

```
CHAIN 803 asis s 28.81120256233061 L1 28.811202562358365665 gain 4e-06 cert True sec 600.1
CHAIN 803 jitter s 28.811250815365636 L1 28.811250815393278069 gain 2e-06 cert True sec 600.1
SUMMARY {"targets": 20, "improved": 3, "total_gain": 9.598613487860334e-06, "wall_seconds": 6401.2}
```

### 6.4 Merge against the bank

Separate output dir, bank not written by this subagent:

```sh
.venv/bin/squares merge \
  --baseline /tmp/best_bank/submission.csv \
  --baseline-report /tmp/best_bank/report.json \
  --candidate /tmp/sub_cpu/dl_hop_scaled/improved_groups.csv \
  --output-dir /tmp/sub_cpu/merge_hop_scaled --workers 4
```

Result (both scoring paths):

```
changed_puzzles  [333, 747, 803]
net_gain         text 9.598613487815655e-06   float64 9.598613487815655e-06
score            text 22.13101404834979        float64 22.13101404834979
competition_submitted false
```

Independent full re-score of the serialized merge file:

```
squares score /tmp/sub_cpu/merge_hop_scaled/submission.csv --mode both --workers 4 \
  --output-dir /tmp/sub_cpu/merge_hop_scaled/validation
score 22.13101404834979 (text and float64), valid 1000 / invalid 0 / missing 0
```

The bank changed while this merge ran: at 19:19 it became byte-identical to the
merge output (`SHA-256 eab2f56c38ce4f36858b388ca237bbd47039da2cfe302f7659aa24c49ac24622`,
same as the merge report's `submission_sha256`), and its bound report scores
22.13101404834979. The merge's baseline was the pre-merge bank `9b0bcc…`, baseline score
22.131023646963278, so the certified net gain is **9.5986e-06**. The number
22.131251704293867 quoted in the task does not match the local report bound to
`9b0bcc…`; it is most likely the official submitted score (which is not what the
local merge certifies). This subagent did not write the bank.

## 7. Session-slot contention (resolved)

For ~25 minutes all five batch-CPU sessions were held by sibling agents, and both
pushes were rejected with `Maximum batch CPU session count of 5 reached`. A retry
loop (`/tmp/sub_cpu/run_queue.sh`) got the smoke into a slot as soon as one freed;
the X3 and scaled-hop kernels were pushed once the smoke completed. No sibling
kernel was touched.

## 8. Merge (when there is a win)

Never touches the bank.  Separate output dir:

```sh
cd /Users/zhaohuaxiang/ccjjllt/squares
uv run squares merge \
  --baseline /tmp/best_bank/submission.csv \
  --baseline-report /tmp/best_bank/report.json \
  --candidate /tmp/sub_cpu/dl_hop_scaled/improved_groups.csv \
  --output-dir /tmp/sub_cpu/merge_hop_scaled --workers 4
uv run squares score /tmp/sub_cpu/merge_hop_scaled/submission.csv \
  --mode both --workers 4 --output-dir /tmp/sub_cpu/merge_hop_scaled/validation
```

At the time of the run the bank report was bound to
SHA `9b0bcce13ddc7879c4e395ea72e28149b96f92e8552915300929bfb54a2181ce`, so the
cached path was valid. The bank is now `eab2f56c…` (the merge output itself), and
`/tmp/best_bank/report.json` was regenerated to match it. The bank is never written
by this code path.
