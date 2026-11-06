# 项目目录与存放约定

项目文档集中在 `docs/`，根目录 README 只保留入口与启动方式。自有脚本、原始资料和分析产物分开存放。

## 目录职责

| 目录 | 内容 | Git 默认行为 |
| --- | --- | --- |
| `docs/` | 比赛说明、使用指南、优化研究、来源说明 | 保留 |
| `src/squares/` | 自有工具包；`_vendor/` 是运行时官方评分源码 | 保留 |
| `scripts/analysis/` | 自有分析和绘图脚本 | 保留 |
| `notebooks/public/` | 下载的公开 Notebook 与版本元数据 | `.ipynb` 忽略，元数据保留 |
| `third_party/evand/` | 下载的上游源码摘录 | 本地保留，Git 忽略 |
| `third_party/*manifest.json` | 第三方来源、固定版本和文件 SHA | 保留 |
| `data/competition/` | 官方样例及后续比赛输入 | 忽略大文件 |
| `data/public/<来源版本>/` | 下载的公开布局 CSV | 忽略大文件 |
| `data/references/` | 小型参考表、Kaggle 快照、论文索引 | 保留 |
| `outputs/analysis/<研究名>/` | 研究表格、摘要和图表 | 保留，日志忽略 |
| `outputs/baselines/` | 本地生成的基线 CSV | 忽略 |
| `outputs/scores/<布局名>/` | 官方评分器产生的逐题记录和汇总 | 忽略 |
| `outputs/submissions/<提交名>/` | Kaggle 回执、来源与评分记录 | 忽略 |
| `outputs/examples/` | 旧示例或临时演示产物 | 忽略 |
| `.venv/` | 当前 Python 开发环境 | 本地保留，Git 忽略 |
| `.cache/`、`__pycache__/`、`.ruff_cache/` | 可重新生成的缓存 | 忽略，可清理 |

`outputs/analysis/` 只保留可阅读和复用的研究成果；大规模中间搜索结果应放在其他 `outputs/` 子目录。原始下载暂存目录 `data/references/downloads/`、日志和编辑器临时文件也被忽略。Git 忽略与磁盘删除是两回事：公开布局和第三方源码仍可留在本地使用。

所有命令中的相对路径均以项目根目录为起点；分析脚本通过自身位置定位项目根目录，因此可从其他工作目录调用。

## 分析结果的内部组织

```text
outputs/analysis/baseline/
├── tables/       逐题 CSV、差距排序、同族候选
├── summaries/    研究结论、计划、数据审计 JSON
├── figures/      静态研究图
└── logs/         控制台输出
```

输入数据放 `data/`，不要写回分析输出目录。Python 脚本放 `scripts/`；面向阅读的解释、结论和实验记录放 `docs/`。CSV 表与生成的 JSON 汇总放对应研究的 `tables/`、`summaries/`。

## 常用文件

- [逐题分析脚本](../scripts/analysis/analyze_baseline.py)
- [绘图脚本](../scripts/analysis/plot_baseline_analysis.py)
- [原始纪录参考表](../data/references/leaderboards/perpuzzle_best_20261029.csv)
- [研究结果摘要](../outputs/analysis/baseline/summaries/research_outcome.json)
- [优化计划](../outputs/analysis/baseline/summaries/research_plan.json)
- [Boxed 更新后的攻关排序](../outputs/analysis/baseline/tables/post_boxed_record_gap_candidates.csv)
- [论文来源索引](../data/references/literature/source_index.json)

## 原始资料与历史记录

第三方源码树中的 README、DESIGN、CLAIMS 属于上游内容，随源码在本地原样保留，不搬散到项目文档中。`third_party/evand/` 是已阅读文件的摘录，并非完整可构建仓库；新克隆需要根据其 manifest 从对应上游版本重新获取。公开 Notebook 同样根据配套 `.metadata.json` 中的引用与版本获取。

已提交布局 `data/public/stretching_v2/submission.csv` 及 `outputs/submissions/public_stretching_v2/` 保持原位。历史评分报告、Notebook 和 MCP 原始快照中的旧路径属于当时的记录，不做全局替换。

旧 `research/` 已按上述职责迁移。需要定位旧文件时，查阅[目录迁移清单](../data/references/directory_migration.json)；它记录旧路径、新路径和搬迁时的 SHA-256。该校验值表示搬迁时字节内容，后续主动更新的自有脚本与文档可能不同。

2026 年 11 月 6 日的[清理记录](../data/references/cleanup_20261106.json)列出已移除的缓存、旧示例、空下载和重复文件。迁移清单中的历史路径不代表这些临时文件仍被保留。官方评分代码以 `src/squares/_vendor/` 为唯一源码副本；完整网格基线可用 `make baseline` 重新生成。
