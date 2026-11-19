# 来源记录

本文件记录第三方代码和坐标来源及其保留状态（截至 2026-11-16）。各材料继续适用原作者的条款，项目未将它们重新授权为统一许可证。

## 运行时保留

| 材料 | 固定来源 | 本地文件与证据 |
| --- | --- | --- |
| 官方评分器 | [Kaggle Competition Metrics，v20](https://www.kaggle.com/code/metric/squares-in-squares) | `src/squares/_vendor/official_metric.py`，版本与 SHA-256 在同目录 `official_metric.metadata.json` |

Python 依赖与版本由 `pyproject.toml`、`uv.lock` 声明，各依赖保留自己的许可证。

## 已删除的第三方摘录（2026-11-16）

旧 CPU 生成 + GPU 松弛 pilot 管线及其第三方摘录已停止并删除（见[清理记录](../data/references/cleanup_20261116.json)）。来源与哈希保留如下，源码副本不再位于工作区：

| 材料 | 固定来源 | 已删除的本地文件 | 身份 |
| --- | --- | --- | --- |
| Chains + Crossover 几何摘录 | [estopadilla，v1](https://www.kaggle.com/code/estopadilla/beating-124-public-bests-chains-crossover) | `third_party/chains/geometry_original.py`、`source.json` | notebook SHA-256 `213af870…`；几何摘录 SHA-256 `40b3e735…` |
| CUDA Packing Search 内核 | [Vladislav Lavrentev / lightningv08，v24](https://www.kaggle.com/code/lightningv08/squares-in-squares-cuda-packing-search) | `third_party/cuda_packing/gpu_topology_kernel.cu`、`manifest.json` | 内核 SHA-256 `c1452753…`；notebook SHA-256 `389de724…` |

## 固定公开布局（身份保留，坐标副本已删除）

公开作者可能更新 Notebook；下表保存的是项目曾使用的固定版本。坐标文件 `data/public/*/submission.csv` 已随旧 pilot 管线于 2026-11-16 删除，SHA-256 仍保留在[来源清单](../data/references/sources.json)，可据此重新获取同一版本。

| 来源 | 保存版本 | 原本地目录 | 用途 |
| --- | --- | --- | --- |
| [Penguin Certified Research Portfolio](https://www.kaggle.com/code/penguin069/squares-in-squares-certified-research-portfolio) | v2 | `data/public/penguin_v2/` | 历史研究基线、结构供体 |
| [Living Atlas of Tight Packings](https://www.kaggle.com/code/malyshevdanil/squares-in-squares-living-atlas-of-tight-packings) | v79 | `data/public/atlas_v79/` | 交叉供体 |
| [Squares Public Merge Daily](https://www.kaggle.com/code/kmmmvs/squares-public-merge-daily) | v13 | `data/public/daily_v13/` | 迁移链供体 |
| [A Square Deal](https://www.kaggle.com/code/prvsiyan/a-square-deal-research-to-verified-packings) | v33 | `data/public/square_deal_v33/` | 最终合并所用公共基线 |

`data/references/leaderboards/perpuzzle_best_20261029.csv` 来自 [lostdecimal27 的 squares-in-squares-bank](https://www.kaggle.com/datasets/lostdecimal27/squares-in-squares-bank)，是 2026-10-29 的边长纪录镜像，仅作历史排序参考，不是实时榜单。

## 2026-11-18 公开 donor（当日收割）

| 材料 | 固定来源 | 版本 / SHA-256 | 收益 |
| --- | --- | --- | --- |
| `alexchilton/squares-in-squares-starter-kit` → `best_current.csv` | [Kaggle dataset](https://www.kaggle.com/datasets/alexchilton/squares-in-squares-starter-kit) | v85，2026-11-18T10:54:40Z，`3b60ade8…` | **+7.8687537e-4**，160 题 |
| `AHFE0924/Squares-Feeder` → `latest_public.csv` | [GitHub](https://github.com/AHFE0924/Squares-Feeder) | commit `d2293a82`，2026-11-18T13:50:43Z，`e9925e49…` | +2.6971826e-5，21 题（后续版本再 +1.85e-8） |
| 逐题纪录表 | [inversion/squares-in-squares-per-puzzle-leaderboard](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | 2026-11-18T12:02:43Z 运行，`__results__.html` 内嵌 `const DATA` | 只含边长，无坐标；合并后见 `data/references/leaderboards/perpuzzle_best_20261118.csv`（`9cae7620…`） |

`best_current.csv` 单独整表只有 22.129578（弱于 bank），价值在逐题：160 题更优。
哨兵 `scripts/watch_public.sh`（即 `/tmp/pubscan2/watch_public.sh`）每 30 分钟重下
这两个 donor，只做只读 merge，不安装、不提交。

## 正式提交身份

2026-11-16 清理删除了除当前最佳外的正式/候选提交 CSV。每个 ref 的官方分、SHA-256、行数与本地复核结果保存在[历史提交身份表](../data/references/official_submissions_20261116.json)与[2026-11-18 提交链](../data/references/official_submissions_20261118.json)；当前官方最佳为 `outputs/submissions/gpu_f_20261116/`（ref 58418244，22.1327829081，SHA-256 `3465e359…`），最新为 ref 58512171（22.1271380476，SHA-256 `430bb155…`）。

未继续采用的 Notebook、论文调研与外部求解器摘录已清理；相关研究结论及停止原因统一保存在[研究概况](research.md)。
