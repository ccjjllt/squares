# 开发与实验指南

[Kaggle Squares in Squares](https://www.kaggle.com/competitions/squares-in-squares) 的本地实验项目，提供提交文件检查、网格基线生成和官方 v20 逐题评分封装。先建立可复现的评分流程，再逐步接入结构搜索与局部优化。

## 环境准备

项目默认使用 Python 3.12（见 `.python-version`），通过 [uv](https://docs.astral.sh/uv/) 管理虚拟环境和锁文件。在项目根目录运行：

```sh
uv sync --locked
uv run squares --help
```

`uv sync` 会创建本地 `.venv`，缓存放在 `.cache/uv`。核心依赖固定为 `mpmath==1.4.1`、`pandas==2.3.3`，完整版本由 `uv.lock` 固定。官方 v20 使用的 `mpf.man` 和 `mpf.exp` 需要兼容的 mpmath 版本，不应直接降级到 1.3。

## 快速开始

以生成和查看前 10 题的网格布局为例：

```sh
uv run squares baseline --max-n 10 --output outputs/examples/example.csv
uv run squares inspect outputs/examples/example.csv
```

需要分析逐题得分时运行：

```sh
uv run squares score outputs/examples/example.csv --max-n 10 --mode both --workers 2 --output-dir outputs/scores/example
```

`--max-n 10` 表示仅对 `n=1…10` 评分，所得总分不能与全 1,000 题的排行榜比较。省略它时按全部 1,000 题评分，文件中未提供的题目计入网格罚分。

## 完整基线与提交文件

生成全部 1,000 题的网格布局：

```sh
uv run squares baseline --max-n 1000 --output outputs/baselines/grid.csv
uv run squares inspect outputs/baselines/grid.csv
```

完整文件包含 500,500 行，列为：

```text
id,n,square_id,x,y,angle
```

每个 `n` 对应一套完整布局，`square_id` 覆盖 `0…n-1`；`x`、`y` 为单位正方形的中心坐标，`angle` 为弧度。`id` 必须为唯一非负整数。部分提交以整题为单位，不能只提交某个 `n` 的部分方块。

`inspect` 检查列、标识符、题目完整性、数值格式和输入范围，**不检查方块重叠**。已下载官方样例时可运行：

```sh
uv run squares inspect data/competition/sample_submission.csv
```

大文件目录 `data/competition/`、`data/public/` 不纳入 Git；小型参考资料 `data/references/` 保留在版本管理中。新克隆项目可从比赛数据页下载样例，或直接使用 `baseline` 生成本地基线。

## 逐题评分

```sh
uv run squares score outputs/baselines/grid.csv --mode both --max-n 1000 --workers 4 --output-dir outputs/scores/grid
```

评分使用原样保存的官方 v20 单题函数，不替换其几何判定。`--workers` 控制进程数；高精度接触判定可能较慢，调试时优先使用较小的 `--max-n` 和 `--workers 1`。

| 模式 | 输入路径 |
| --- | --- |
| `text` | 保留 CSV 中坐标和角度的原始十进制文本后评分 |
| `float64` | pandas C 引擎以 `float_precision="round_trip"` 读入 double，再导出文本评分 |
| `both` | 分别执行以上两条路径，默认模式 |

`float64` 是固定本地环境下的读写模拟，不能保证与 Kaggle 后台当前解析环境完全相同。保存原文仍有必要，但只验证原文不足以判断提交经过浮点读写后是否有效。导出格式、依赖版本和微小间隙都可能影响接触判定。

每次评分写入：

- `report.json`：各模式汇总，以及输入 SHA-256、官方评分源码 SHA-256、版本和运行依赖信息。
- `per_puzzle.csv`：`mode,n,score,L,status,reason`，保留每题得分、认证边长、状态和原因。

汇总区分有效题目、无效已提交题目与缺失题目。缺失题目允许按网格罚分计入；已提交布局未通过验证时，CLI 返回退出码 `1`。结构检查失败会提前报错。不要只看总分判断合法性：完全平方数题目的网格罚分也是零。

官方目标是最小化 `Σ(L_n / sqrt(n) - 1)`。全网格布局按公式计算的参考总分约为 `28.9376699166`。合法但更差的布局不会自动截断到网格分。`L` 没有被认证时应结合 `status` 与 `reason` 判断，不能把空值或零占位当作改进。

## 目录与分析脚本

文件存放约定见[项目目录](project-layout.md)，研究结论见[优化方向](research/optimization.md)。

在项目根目录重跑现有分析：

```sh
uv run python scripts/analysis/analyze_baseline.py
uv run --with matplotlib python scripts/analysis/plot_baseline_analysis.py
```

分析表格、摘要和图分别写入 `outputs/analysis/baseline/tables/`、`summaries/`、`figures/`。原始纪录表位于 `data/references/leaderboards/`，公开提交文件位于 `data/public/`。

新克隆项目若要重建基线分析，需要准备以下本地输入。下载时选择表中的版本，文件名均为 `submission.csv`：

| 来源 | 版本 | 放置目录 |
| --- | --- | --- |
| [Stretching](https://www.kaggle.com/code/az05192000gmailcom/22-2427-stretching-good-packings-to-nearby-n) | Notebook v2 | `data/public/stretching_v2/` |
| [Living Atlas](https://www.kaggle.com/code/malyshevdanil/squares-in-squares-living-atlas-of-tight-packings) | Notebook v79 | `data/public/atlas_v79/` |
| [Boxed In](https://www.kaggle.com/code/jazivxt/boxed-in-sub) | Notebook v16 | `data/public/boxed_v16/` |

分析脚本必需 Stretching 的本地评分记录；Atlas 输入存在时会额外生成对比表与同族分析。缺少 Stretching 评分记录时，可本地生成，不会提交到 Kaggle：

```sh
uv run squares score data/public/stretching_v2/submission.csv --mode both --output-dir outputs/submissions/public_stretching_v2/validation
```

绘图需要先生成分析摘要；第二张图还需要 Atlas 对比表。Boxed 的研究结果是已归档的独立分析，当前 `analyze_baseline.py` 不会重新生成它。

不要直接修改 `_vendor/official_metric.py`。需要更新官方版本时，重新获取源码、记录出处和校验值，再检查新旧版本的评分行为；本地扩展写在封装层。

后续优先建立逐题候选库，按完整 `n` 组选择已验证的较优布局，并保留来源。再接入 stretching、斜带和 gadget 组合等结构搜索，最后使用 contact polish 精修。当前骨架不包含这些搜索器或自动合并功能，也不会自动向 Kaggle 提交。

第三方代码、数据与研究快照的使用说明见 [第三方来源说明](third-party.md)。
