# Squares in Squares

Kaggle 几何优化项目。对每个 `n = 1…1000`，把 `n` 个允许旋转的单位正方形无重叠地装进最小正方形。若其边长为 `L_n`，总分为 `Σ max(0, L_n / √n − 1)`，越低越好。[比赛页面](https://www.kaggle.com/competitions/squares-in-squares)

## 当前成绩

| 记录 | 得分 | 提交编号 | 本地文件 |
| --- | ---: | ---: | --- |
| 11 月 26 日公开最好，jazivxt 的 Boxed In Sub v77 原文件 | 官方 **22.0905523976** | 58920662 | [提交 CSV](outputs/public_best_20261126/boxed_in_v77.csv) |
| 11 月 23 日已提交研究基线，逐题合并公开布局与自研结果 | 官方 **22.1034314474** | 58768971 | [研究基线 CSV](outputs/research_20261120/merged_quench_20261123/submission.csv) |
| 11 月 25 日最新自研快照，Colab GA B 组再改善 3 题 | 本地 **22.10339658009354** | 未单独提交 | [GA 快照 CSV](outputs/retained_research/ga_20261125/submission.csv) |

北京时间 2026 年 11 月 26 日 10:03，公开最好提交排名 **156 / 2490**，距榜首 **0.0506013166**，距第 50 名 **0.0041593443**。[公开文件、哈希与复分记录](data/references/public_best_20261126.json) · [官方提交账本](data/references/official_submissions.json)

已恢复的 5 题 CPU 增量及其认证结果、停止方向和开放问题见[研究概况](docs/research.md)。第三方实现、数据和署名见[来源记录](data/references/sources.json)。

## 本地验证

完整 CSV 含 500,500 行，坐标为方块中心，角度单位为弧度。官方 v20 评分器分别读取原始十进制文本和 float64 往返值，两条路径都应有 1,000 题有效。

```sh
BANK=outputs/research_20261120/merged_quench_20261123
.venv/bin/python -m squares inspect "$BANK/submission.csv"
.venv/bin/python -m squares score "$BANK/submission.csv" \
  --mode both --workers 4 --output-dir /tmp/squares-score
```

本地 CLI 支持逐题合并，参数见 `.venv/bin/python -m squares merge --help`。搜索在 Kaggle 或 Colab 执行。Kaggle CPU 任务完成后可用[手动收割合并脚本](scripts/harvest_merge.py)下载并复分。Colab GA 会话可用[监控脚本](scripts/watch_colab.sh)查看。
