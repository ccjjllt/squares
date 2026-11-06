# 第三方来源说明

本文件记录项目中的第三方来源，不构成对第三方材料的重新授权。本项目没有通过统一许可证覆盖下列代码、坐标或文档。

## Kaggle 官方评分代码

- 来源：[Squares in Squares 官方评分 Notebook](https://www.kaggle.com/code/metric/squares-in-squares)。
- 作者标识：Kaggle Competition Metrics。
- 保存版本：v20；通过 Kaggle MCP 于 2026 年 11 月 6 日读取。
- 原样源码：`src/squares/_vendor/official_metric.py`，研究归档副本为 `research/official_metric.py`。
- 出处、上游运行时间及源码 SHA-256：`src/squares/_vendor/official_metric.metadata.json`。

评分源码保留原样；项目的读写、报告和命令行封装位于 `_vendor` 目录外。使用或再分发该代码应查阅上游页面提供的条款，不应将本地封装的授权推及官方代码。

## 公开 Notebook 与比赛资料

`research/notebooks/` 保存调研时读取的公开 Notebook 及其元数据。每份配套 `.metadata.json` 记录对应作者、Kaggle 引用和版本；其他 `research/` 快照保留比赛页面、讨论和数据集信息的出处。

这些文件用于研究和复现准备。作者对代码、坐标数据、图像及引用材料的许可可能不同；公开可读不代表全部内容都采用同一开源许可证。复制到求解器或对外再分发前，应沿元数据中的原始来源检查各自许可证并保留要求的署名。

官方 `sample_submission.csv` 如存在于本地 `data/`，来源于 [比赛数据页](https://www.kaggle.com/competitions/squares-in-squares/data)，受相应数据使用说明与比赛规则约束。该目录默认不纳入 Git。

## Python 依赖

Python 依赖通过 `pyproject.toml` 与 `uv.lock` 声明和固定，由包管理器安装，不作为本项目自有源码重新授权。各依赖及其传递依赖继续适用各自发行包中的许可证与声明。
