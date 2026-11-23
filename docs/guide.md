# 使用指南与来源记录

本文件合并原使用指南与第三方来源记录。所有命令从项目根目录运行；研究结论与停止方向见[研究概况](research.md)。

## 问题格式与本地工具

对 `n=1…1000`，将 `n` 个单位正方形装入最小轴对齐正方形容器，评分为 `sum(max(0, L_n / sqrt(n) - 1))`（越低越好）。完整提交含 500,500 行（列：`id,n,square_id,x,y,angle`，角度单位为弧度），候选文件可只含部分 `n`，但每个 `n` 必须完整。

项目使用 Python 3.12（`uv.lock` 固定核心依赖 `mpmath==1.4.1`、`pandas==2.3.3`；`.venv` 另保留提交/抓取所需的 `kaggle` CLI）。运行局部检查与合并：

```sh
BANK=outputs/research_20261120/merged_jaz_20261123
.venv/bin/python -m squares inspect "$BANK/submission.csv"
.venv/bin/python -m squares score "$BANK/submission.csv" \
  --mode both --workers 4 --output-dir /tmp/bank_score
.venv/bin/python -m squares merge \
  --baseline "$BANK/submission.csv" \
  --baseline-report "$BANK/report.json" \
  --candidate /path/to/candidate.csv --output-dir /tmp/merged_next --workers 4
```

- 评分采用原样保存的官方 v20（`src/squares/_vendor/official_metric.py`），`both` 模式同时检验原始文本 `text` 与 `pandas` 浮点往返 `float64` 两条路径；仅在双路径均 1000/1000 有效且严格优于基线时才更新 bank。
- **执行纪律**：搜索、GA 与批量松弛一律在 Colab T4 或 Kaggle 执行，禁止在本机跑重计算。

## 目录结构

| 路径 | 用途 |
| --- | --- |
| `src/squares/` | 官方 v20 评分封装、逐题合并（`merge`）、格式检查（`inspect`）与基线生成 |
| `scripts/` | Colab T4 GA 生命周期管理（`colab_*.py`/`*.sh`、`watch_colab.sh`）与定时提交（`submit_slots.py`） |
| `outputs/research_20261120/merged_jaz_20261123/` | 当前最佳权威 bank（`submission.csv`、`report.json`；22.103438695324，双路径 1000/1000） |
| `data/references/` | `official_submissions.json`、`cleanup_history.json`、`sources.json`、`leaderboards/perpuzzle_best_20261118.csv`、`perpuzzle_best_20261119.csv` |
| `docs/` | `research.md`（研究概况）、`research_20261120.md`（11-20→22 战役）、`guide.md`（本指南） |

## 第三方来源与许可证

各第三方材料继续适用原作者许可证：

| 材料 | 来源与版本 | 用途与保留状态 |
| --- | --- | --- |
| 官方评分器 v20 | [Kaggle Competition Metrics](https://www.kaggle.com/code/metric/squares-in-squares) | 运行时保留于 `src/squares/_vendor/`（SHA-256 `abce6231…`） |
| Santa 2025 岛式 GPU GA | `grennwolf/squares-in-squares-top-1-santa-2025`（移植自 `jcottaar/packing`） | 运行于 Colab T4 私有数据集 `ccjjllt/sis-ga-bundle-20261118` |
| `packer hop` 引擎 | [`evand/square-packing`](https://github.com/evand/square-packing)（MIT，pin `c801ab47`） | 运行于 Kaggle CPU（`alexkit-wide` 系列） |
| 逐题纪录快照 | [`inversion/squares-in-squares-per-puzzle-leaderboard`](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard)（11-18/11-19） | 保留于 `data/references/leaderboards/perpuzzle_best_20261118.csv` 与 `..._20261119.csv` |
| 跨题斜带/arm 算子 | [`GeiserX/squares-in-squares`](https://github.com/GeiserX/squares-in-squares)（代码 Apache-2.0；布局/文档 CC BY 4.0） | `family_step`/`k123` splice 用于 fq r5–r9 与跨题拼接；保留 NOTICE 并署名 Sergio Fernández Rubio |
| 逐日公开 best-of | [`prvsiyan/squares-verified-best-of-1105`](https://www.kaggle.com/datasets/prvsiyan/squares-verified-best-of-1105) v26→v1121（CC BY-SA 4.0） | 每日哨兵逐题认证合并；按原表保留逐题署名 |
| union-register packings | `goodpjw2008`（Kaggle 公开输出，许可随原 notebook） | 11 题独特胜场，已并入 58682330 |
| 公开 donor 与精确证书 | `alexchilton`（v85）、`AHFE0924/Squares-Feeder`、`rosswade`、`Mishapolk`、`JoostdeWinter`、`jlevy`、`jazivxt` 等 | 坐标已逐题认证并入 bank；历史基线哈希见 `data/references/sources.json` |
