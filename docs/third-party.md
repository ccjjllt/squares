# 来源记录

本文件记录整理后仍保留的第三方代码和坐标来源，版本信息截至 2026-11-07。各材料继续适用原作者的条款，项目未将它们重新授权为统一许可证。

## 运行时代码

| 材料 | 固定来源 | 本地文件与证据 |
| --- | --- | --- |
| 官方评分器 | [Kaggle Competition Metrics，v20](https://www.kaggle.com/code/metric/squares-in-squares) | `src/squares/_vendor/official_metric.py`，版本与 SHA-256 在同目录 `official_metric.metadata.json` |
| Chains + Crossover 几何摘录 | [estopadilla，v1](https://www.kaggle.com/code/estopadilla/beating-124-public-bests-chains-crossover) | `third_party/chains/geometry_original.py`，单元位置和 SHA-256 在 `source.json` |
| CUDA Packing Search 内核 | [Vladislav Lavrentev / lightningv08，v24](https://www.kaggle.com/code/lightningv08/squares-in-squares-cuda-packing-search) | `third_party/cuda_packing/gpu_topology_kernel.cu`，提取位置和 SHA-256 在 `manifest.json` |

官方评分器和 CUDA 内核保留原始源码。结构算子的本地扩展位于 `src/squares/search/structure.py`，GPU 封装位于 `gpu_relax.py`；未复用上游 Notebook 的完整实验流程。Python 依赖与版本由 `pyproject.toml`、`uv.lock` 声明，各依赖保留自己的许可证。

## 固定公开布局

每个目录中的坐标文件名均为 `submission.csv`。公开作者可能更新 Notebook，重建时需获取这里记录的固定输出。

| 来源 | 保存版本 | 本地目录 | 用途 |
| --- | --- | --- | --- |
| [Penguin Certified Research Portfolio](https://www.kaggle.com/code/penguin069/squares-in-squares-certified-research-portfolio) | v2 | `data/public/penguin_v2/` | 历史研究基线、结构供体 |
| [Living Atlas of Tight Packings](https://www.kaggle.com/code/malyshevdanil/squares-in-squares-living-atlas-of-tight-packings) | v79 | `data/public/atlas_v79/` | 交叉供体 |
| [Squares Public Merge Daily](https://www.kaggle.com/code/kmmmvs/squares-public-merge-daily) | v13 | `data/public/daily_v13/` | 迁移链供体 |
| [A Square Deal](https://www.kaggle.com/code/prvsiyan/a-square-deal-research-to-verified-packings) | v33 | `data/public/square_deal_v33/` | 最终合并所用公共基线 |

四份公开布局的固定SHA-256统一见[来源清单](../data/references/sources.json)；Atlas的旧Notebook元数据曾显示v78，使用本地v79布局时应以此坐标哈希核对。最终提交来源及自研两题归因见 `outputs/submissions/merged_research_20261107/provenance.json`。最终布局包含 Square Deal v33 的公共结果及自研 n=459、642，公共更新与自主搜索收益分别统计。

`data/references/leaderboards/perpuzzle_best_20261029.csv` 来自 [lostdecimal27 的 squares-in-squares-bank](https://www.kaggle.com/datasets/lostdecimal27/squares-in-squares-bank)，是 2026-10-29 的边长纪录镜像，不包含领先布局坐标，也不是实时榜单。

未继续采用的 Notebook、论文调研与 Evan 求解器摘录已清理；相关研究结论及停止原因统一保存在[研究概况](research.md)。
