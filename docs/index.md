# 项目文档

本项目围绕 Kaggle Squares in Squares 开展布局分析、结构搜索和分数优化。文档集中在本目录；输入数据、脚本、第三方代码和实验产物各自存放。

| 文档 | 内容 |
| --- | --- |
| [使用说明](getting-started.md) | 环境准备、生成布局、读取文件和逐题评分 |
| [比赛说明](competition.md) | 问题、评分、提交格式与已有提交 |
| [优化研究](research/optimization.md) | 基线差距、重点题目、开源实现和研究顺序 |
| [目录约定](project-layout.md) | 各类文件的存放位置和迁移规则 |
| [第三方来源](third-party.md) | 官方评分代码、公开 Notebook 和其他材料的出处 |

## 当前研究记录

截至 2026 年 11 月 6 日，已正式提交 Stretching v2，Kaggle 得分 **22.2427257787**，提交编号 **58044087**。Boxed In v16 的本地官方评分为 **22.238211260762**，尚未提交。两者应分别作为正式成绩与本地研究结果记录。

- [正式提交与来源记录](../outputs/submissions/public_stretching_v2/provenance.json)
- [研究数值汇总](../outputs/analysis/baseline/summaries/research_outcome.json)
- [逐题攻关排序](../outputs/analysis/baseline/tables/post_boxed_record_gap_candidates.csv)
- [论文与证据索引](../data/references/literature/source_index.json)

本地输入和评分运行目录可能不包含在新克隆中；数据获取和重建方式见[使用说明](getting-started.md)。
