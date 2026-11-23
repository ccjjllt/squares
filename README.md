# Squares in Squares

[Kaggle Squares in Squares](https://www.kaggle.com/competitions/squares-in-squares) 几何优化研究项目：通过公开 donor 逐题合并、GPU 岛式 GA（Colab T4 / Kaggle GPU）与宽范围 basin-hopping，压缩 `n=1…1000` 单位正方形最小外接正方形总分。

- **当前官方最好**：ref **`58709491`** = **`22.1039649341`**（COMPLETE；2026-11-23 02:14Z 排名 **100 / 2397**）
- **距榜首**：Cats and boxes 😼 `22.0399510810`，差 `0.0640139`；距前 50（`22.0989656913`）差 `0.0049992`
- **本地权威 bank**：[`outputs/research_20261120/ga_b_20261120b/merge/submission.csv`](outputs/research_20261120/ga_b_20261120b/merge/submission.csv)（SHA-256 `c19b8bf9…`，`22.103964934115`，text/float64 双路径 1000/1000）
- **文档入口**：[研究概况与放弃原因](docs/research.md) ｜ [使用指南与来源](docs/guide.md) ｜ [11-20 → 11-22 深度研究战役](docs/research_20261120.md)

## 快速验证

本仓库只做评分、合并、提交校验与远端编排；重计算全部在 Colab / Kaggle 执行。

```sh
BANK=outputs/research_20261120/ga_b_20261120b/merge
.venv/bin/python -m squares --help
.venv/bin/python -m squares inspect "$BANK/submission.csv"
.venv/bin/python -m squares merge \
  --baseline "$BANK/submission.csv" \
  --baseline-report "$BANK/report.json" \
  --candidate /path/to/candidate.csv \
  --output-dir /tmp/merge_check --workers 2
```

## Colab T4 GA 与提交编排（`scripts/`）

- **代理与账号**：本机直连 Colab TLS 会被重置，必须走 `export COLAB_PROXY=http://127.0.0.1:7897`（`7900` 会 `SSLEOF`）。使用 `colabx` 管理多账号（`colab-accounts` / `colab-use ccjjllt0`）。
- **数据 bundle**：私有数据集 `ccjjllt/sis-ga-bundle-20261118`（含 `colab_pkg/`、bank、启动脚本）。

```sh
# 1. 启动并部署 T4 会话
colabx new -s gpu1 --gpu T4
colabx exec -s gpu1 -f scripts/colab_bootstrap_remote.py --timeout 1800 \
  --env KAGGLE_API_TOKEN="$(cat ~/.kaggle/access_token_ccjjllt_check)"

# 2. 后台保活与安全收割（仅当 >=1e-10 且双路径 1000/1000 才安装，不自动提交）
nohup ./scripts/colab_keeper.sh --loop 300 >> /tmp/campaign2/colab_keeper.log 2>&1 &
nohup ./scripts/colab_harvest_safe.sh --loop 1800 >> /tmp/campaign2/colab_harvest.out 2>&1 &

# 3. 手动查看状态 / 停机
colabx exec -s gpu1 -f scripts/colab_status_remote.py --timeout 120
./scripts/watch_colab.sh -s gpu1 --once
colabx stop -s gpu1

# 4. 固定 UTC 槽位提交（严格优于榜上最好才提交）
.venv/bin/python scripts/submit_slots.py --slots 09:00,15:00,21:00 --check
```

免费 T4 会话回收周期约 2–7 小时，GA 每题自带 `work/runs/ga_state` 断点，重连后可继续。
