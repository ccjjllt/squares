# 第三方来源说明

本文件记录项目中的第三方来源，不构成对第三方材料的重新授权。本项目没有通过统一许可证覆盖下列代码、坐标或文档。

## Kaggle 官方评分代码

- 来源：[Squares in Squares 官方评分 Notebook](https://www.kaggle.com/code/metric/squares-in-squares)。
- 作者标识：Kaggle Competition Metrics。
- 保存版本：v20；通过 Kaggle MCP 于 2026 年 11 月 6 日读取。
- 原样源码：`src/squares/_vendor/official_metric.py`；重复研究副本已清理。
- 出处、上游运行时间及源码 SHA-256：`src/squares/_vendor/official_metric.metadata.json`。

评分源码保留原样；项目的读写、报告和命令行封装位于 `_vendor` 目录外。使用或再分发该代码应查阅上游页面提供的条款，不应将本地封装的授权推及官方代码。

## 公开 Notebook 与比赛资料

`notebooks/public/` 在本地保存调研时读取的公开 Notebook；下载的 `.ipynb` 不纳入 Git，配套 `.metadata.json` 保留在版本管理中，记录作者、Kaggle 引用和版本。`data/references/kaggle/` 中的小型快照保留比赛页面、讨论和数据集信息的出处。

这些文件用于研究和复现准备。作者对代码、坐标数据、图像及引用材料的许可可能不同；公开可读不代表全部内容都采用同一开源许可证。复制到求解器或对外再分发前，应沿元数据中的原始来源检查各自许可证并保留要求的署名。

官方 `sample_submission.csv` 如存在于本地 `data/competition/`，来源于 [比赛数据页](https://www.kaggle.com/competitions/squares-in-squares/data)，受相应数据使用说明与比赛规则约束。`data/competition/` 与 `data/public/` 默认不纳入 Git；小型参考快照 `data/references/` 可纳入版本管理。

## Python 依赖

Python 依赖通过 `pyproject.toml` 与 `uv.lock` 声明和固定，由包管理器安装，不作为本项目自有源码重新授权。各依赖及其传递依赖继续适用各自发行包中的许可证与声明。

## 开源求解器研究快照

`third_party/evand/` 在本地保留读取时的上游相对目录和原文，包括其 README、DESIGN 与 CLAIMS；下载副本不纳入 Git。它是研究用源码摘录，不是完整可构建的仓库克隆。版本管理保留 `third_party/evand_manifest.json` 与 `third_party/evand_extras_manifest.json`，其中记录文件版本和 blob SHA，仓库版本为 `bb4cc78e5b35103c1f177db55e9cf08974e66563`。这些清单中的 `path` 为上游相对路径。
