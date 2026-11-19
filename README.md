# Squares in Squares

[Kaggle Squares in Squares](https://www.kaggle.com/competitions/squares-in-squares) 几何优化研究项目：通过公开前沿逐题合并与 Kaggle GPU 静态分区 GA，寻找更紧的正方形布局。

截至 2026-11-18，本地 bank **22.126704172180595**（SHA-256 `e50d51e2…`），1,000 题全部有效，官方 **58516336 = 22.1267041721**（15:50Z，排名 **96**；当日公开收割合计 −1.248e-3）。上一笔官方分 22.1271303908（58514784 / 58514816）。收益主要来自公开 donor（`boxed_v56`、jazivxt、alexchilton v83）、Colab T4 上的 Santa 2025 冠军 GA，以及 Kaggle CPU 上的 C++20 引擎。研究结论、停止方向与清理统一记录在研究概况中。

- [研究概况](docs/research.md)：当前结果、有效主线、停止方向及原因、清理记录。
- [使用指南](docs/getting-started.md)：问题定义、环境、评分、逐题合并与保留约定。
- [来源记录](docs/third-party.md)：第三方代码与公开布局的来源、版本与保留状态。

```sh
uv sync --locked
uv run squares --help
```

当前最佳布局及完整验证保存在 `outputs/submissions/bank_20261117/`（`submission.csv`、`report.json`、`provenance.json`）。本仓库只保留评分、合并、提交校验与本机编排的接口；结构搜索/GA 全部在 Kaggle 或 Colab 运行，不在本机重计算。历史提交的 ref、官方分与 SHA-256 见 `data/references/official_submissions_20261116.json`；2026-11-16 / 11-18 两轮清理的范围见 `data/references/cleanup_20261116.json` 与 `data/references/cleanup_20261118.json`。

## Colab T4 运行（colabx）

本机的 `colab-cli` 用 `colabx` 包装，支持多 Google 账号、独立 token 与独立 session 列表。

```sh
colab-accounts                    # 列出账号，* 是当前默认
colab-use ccjjllt0                # 切换默认账号
COLAB_ACCOUNT=ccjjllt0 colabx …   # 只对单条命令临时指定账号
colab-rename old new              # 改名（新名不能已存在）
```

**网络注意**：本机直连 `colab.research.google.com` 的 TLS 会被重置，必须走本地代理；`colabx` 默认用 7900，但实测 7900 在 `POST /tun/m/assign` 上会 `SSLEOF`，**用 7897**：

```sh
export COLAB_PROXY=http://127.0.0.1:7897
```

**起一个 T4 会话并验证 GPU：**

```sh
colabx new -s gpu1 --gpu T4
colabx exec -s gpu1 <<'PY'
import torch; print(torch.cuda.get_device_name(0), torch.cuda.is_available())
PY
```

**准备数据（不依赖 Drive 挂载）**：GA bundle 已作为私有数据集发布
`ccjjllt/sis-ga-bundle-20261118`（`sis_bundle.tar.gz` = `colab_pkg/` + 当前 bank
`submission.csv`/`report.json` + `prepare_colab.py` / `run_colab.sh` / `make_submission.py`）。
会话内用 Kaggle token 直接下载并解包到 `/content/sis`，然后：

```sh
colabx exec -s gpu1 -f scripts/colab_bootstrap_remote.py --timeout 1800 \
  --env KAGGLE_API_TOKEN="$(cat ~/.kaggle/access_token_ccjjllt_check)"
```

（`scripts/colab_bootstrap_remote.py` 只负责下载/解包/装依赖/`prepare_colab.py`；已有
`work/` 时幂等跳过。）

**跑 GA：**

```sh
colabx exec -s gpu1 <<'PY'
import subprocess
print(subprocess.run(["bash","-lc",
  "cd /content/sis && NPROC=4 MAX_MIN=600 setsid nohup bash run_colab.sh > run.out 2>&1 < /dev/null & sleep 8; tail -5 run.out"],
  capture_output=True, text=True).stdout)
PY
```

**看状态 / 收割 / 停止：**

```sh
colabx exec -s gpu1 -f scripts/colab_status_remote.py --timeout 120   # GPU、进程、改进数
colabx exec -s gpu1 -f scripts/colab_harvest_remote.py --timeout 600  # 生成 candidate_colab.csv
colabx download -s gpu1 /content/sis/candidate_colab.csv /tmp/campaign2/colab_candidate.csv
colabx stop -s gpu1                                                   # 跑完必须停，别空转
```

**自动收割（推荐）**：kernel 偶发卡死时 `restart-kernel` 能恢复，而 detached 的 GA
worker 不受影响。`scripts/colab_harvest_safe.sh` 会先探测、必要时重启 kernel，再
远端 `make_submission.py` → 下载 → 只读 merge，**只在增益 ≥1e-10 且双路由
1000/1000 时自动安装**（从不提交 Kaggle）：

```sh
nohup ./scripts/colab_harvest_safe.sh --loop 1800 \
  >> /tmp/campaign2/colab_harvest.out 2>&1 &
```

**会话保活**：免费 T4 会被提前回收（本次只跑了约 2h20m）。`scripts/colab_keeper.sh`
每 5 分钟只查 session 列表（不碰 kernel），丢失时自动 `new -s gpu1 --gpu T4`、
从最新私有数据集 bootstrap、再起 4 个 worker；已有会话绝不重启。

```sh
nohup ./scripts/colab_keeper.sh --loop 300 >> /tmp/campaign2/colab_keeper.log 2>&1 &
```

本地只做只读认证，不安装：

```sh
.venv/bin/python -m squares merge --baseline /tmp/best_bank/submission.csv \
  --baseline-report /tmp/best_bank/report.json \
  --candidate /tmp/campaign2/colab_candidate.csv \
  --output-dir /tmp/campaign2/colab_merge --workers 2
```

免费 T4 会被回收（本次约 7h20m）；GA 每题有 checkpoint（`work/runs/ga_state`），重连后从当前
bank 重新 `prepare_colab.py` + `run_colab.sh` 即可续跑。
