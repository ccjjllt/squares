# Squares in Squares

[Kaggle Squares in Squares](https://www.kaggle.com/competitions/squares-in-squares) 几何优化研究项目：通过公开前沿逐题合并与 Kaggle GPU 静态分区 GA，寻找更紧的正方形布局。

截至 2026-11-16，官方成绩 **22.1327829081**（提交 58418244，排名 78），1,000 题全部有效；本地最佳与官方一致。收益主要来自公开 donor（`boxed_v56`、jazivxt、alexchilton）与自研静态分区 GA（`NPROC=12`，已实测 24/24 覆盖）。研究结论、停止方向与两轮清理（2026-11-13、2026-11-16）统一记录在研究概况中。

- [研究概况](docs/research.md)：当前结果、有效主线、停止方向及原因、清理记录。
- [使用指南](docs/getting-started.md)：问题定义、环境、评分、逐题合并与保留约定。
- [来源记录](docs/third-party.md)：第三方代码与公开布局的来源、版本与保留状态。

```sh
uv sync --locked
uv run squares --help
```

当前最佳布局及完整验证保存在 `outputs/submissions/gpu_f_20261116/`（`submission.csv`、`validation/report.json`、`provenance.json`、`run_report.json`）。本仓库只保留评分、合并、提交校验与本机编排的接口；结构搜索/GA 全部在 Kaggle 运行，不在本机重计算。历史提交的 ref、官方分与 SHA-256 见 `data/references/official_submissions_20261116.json`；2026-11-16 清理删除约 18.3 GiB 的停止研究脚本、原始下载、中间合并与旧提交 CSV，范围见 `data/references/cleanup_20261116.json`。
