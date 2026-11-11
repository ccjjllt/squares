# Squares in Squares

[Kaggle Squares in Squares](https://www.kaggle.com/competitions/squares-in-squares) 几何优化研究项目：通过结构迁移、接缝交叉和连续松弛寻找更紧的正方形布局。

截至 2026-11-11，正式成绩为 **22.1959256252**（提交 58236174），1,000 题全部有效；相对上一正式提交 22.1963280817 的收益主要来自 Atlas/Daily 公共更新与逐题合并。研究结论和停止方向统一记录在研究概况中。

- [研究概况](docs/research.md)：当前结果、有效主线、停止方向及原因。
- [使用指南](docs/getting-started.md)：问题定义、环境、候选生成、评分与合并。
- [来源记录](docs/third-party.md)：保留代码与公开布局的出处。

```sh
uv sync --locked --extra experiments
uv run squares --help
```

当前最佳布局及完整验证保存在 `outputs/submissions/v124_plus_daily44_20261111/`。代码在 `src/`，实验入口在 `scripts/`；数据和实验产物的保留约定见使用指南。
