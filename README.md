# Squares in Squares

[Kaggle Squares in Squares](https://www.kaggle.com/competitions/squares-in-squares) 几何优化研究项目。围绕公开布局、逐题差距和结构搜索开展实验。

## 文档入口

- [文档目录](docs/index.md)
- [开发与实验指南](docs/getting-started.md)
- [比赛与提交记录](docs/competition.md)
- [优化研究与优先方向](docs/research/optimization.md)
- [项目目录与文件存放约定](docs/project-layout.md)
- [第三方来源说明](docs/third-party.md)

## 开始使用

在项目根目录运行：

```sh
uv sync --locked
uv run squares --help
make analyze
```

`make analyze` 使用本地公开布局和已有评分记录，输出逐题分析。新克隆项目需要先准备对应本地数据，详见开发指南。

## 目录

```text
docs/          项目文档与研究结论
src/           自有 Python 包及运行时评分器
scripts/       分析与绘图脚本
notebooks/     公开 Notebook 及元数据
third_party/   原样保留的第三方代码摘录
data/          比赛输入、公开布局、参考资料
outputs/       分析结果、评分报告、候选布局与提交归档
```
