# 使用指南

所有命令从项目根目录运行。研究状态、停止原因与清理记录见[研究概况](research.md)，第三方来源见[来源记录](third-party.md)。

## 问题与文件格式

对每个 `n=1…1000`，把 n 个边长为 1 的正方形放入尽可能小的轴对齐正方形容器。方块可以旋转，内部不能重叠。评分为 `sum(max(0, L_n / sqrt(n) - 1))`，越低越好；`L_n` 由方块角点的包围盒计算。

完整提交包含 500,500 行，列为 `id,n,square_id,x,y,angle`。`id` 为唯一非负整数，`square_id` 在每题覆盖 `0…n-1`，`x/y` 是中心坐标，`angle` 单位为弧度。候选文件可只包含部分题目，但每个 n 必须完整。缺失或无效题目按网格罚分处理；合法但更差的布局不会自动截断到网格分。

## 环境与检查

项目默认 Python 3.12，依赖由 `uv.lock` 固定：

```sh
uv sync --locked
uv run squares --help
```

`inspect` 检查格式、标识符和题目完整性，不检查重叠。当前最佳布局在 `outputs/submissions/gpu_f_20261116/submission.csv`（官方 ref 58418244，22.1327829081）：

```sh
uv run squares inspect outputs/submissions/gpu_f_20261116/submission.csv
```

新环境没有布局文件时，可生成小型网格验证安装：

```sh
uv run squares baseline --max-n 10 --output outputs/examples/grid10.csv
uv run squares score outputs/examples/grid10.csv --max-n 10 --mode both --workers 1 --output-dir outputs/examples/grid10_score
```

仅对前 10 题计算的分数不能与完整比赛成绩比较。

## 官方评分与跨轮合并

评分使用原样保存的官方 v20。`text` 模式保留原始十进制文本；`float64` 模式经 pandas 的 round-trip 浮点读写后评分；默认 `both` 执行两条路径。高精度接触判定对微小重叠和读写精度敏感，浮点残差小并不等于有效布局。

每次输出 `report.json` 和 `per_puzzle.csv`，包含文件/评分器哈希、环境版本、有效性及逐题分数。已提交题目无效时命令返回非零状态；总分不能代替有效性检查。

从下一轮实验或公开 donor 中选择每题最佳布局：

```sh
uv run squares merge \
  --baseline outputs/submissions/gpu_f_20261116/submission.csv \
  --baseline-report outputs/submissions/gpu_f_20261116/validation/report.json \
  --candidate /tmp/harvest/improved_groups.csv \
  --output-dir outputs/merged/next --workers 4
```

`--candidate` 可重复。示例中的 `/tmp/harvest/improved_groups.csv` 需替换为实际路径。合并按完整 n 组选择；两条评分路径都不得比基线退步，保留原始数值文本并记录来源。同题的多次改善只按最终赢家计算一次。

`--baseline-report` 仅复用与基线哈希、评分器和环境一致的完整报告；环境改变时省略该参数重新评分。最终序列化文件在提交前仍需完整独立复评：

```sh
uv run squares score outputs/merged/next/submission.csv \
  --mode both --workers 4 --output-dir outputs/merged/next/validation
```

这些命令只生成和验证本地文件，不提交比赛。官方评分源码位于 `src/squares/_vendor/`；更新版本时应重新记录来源和哈希。

## 搜索与重计算的执行位置

结构搜索、GA 与批量松弛**不在本仓库、也不在本机运行**：全部通过 Kaggle kernel/dataset 执行，结果以 `improved_groups.csv` 或公开 `submission.csv` 回到本地，由 `squares merge` 逐题认证。2026-11-16 已删除旧的 `scripts/experiments/`、`scripts/kaggle/`、`src/squares/search/` 与 `third_party/`，因为该 CPU 生成 + GPU 松弛 pilot 管线已被 Kaggle 静态分区 GA 取代。

本机只做四件事：下载候选、`squares merge`、`squares score` 双路径复核、提交。不要在本机跑优化或批量搜索——2026-11-12 的近平方族脚本在本机峰值内存 103 GB，已明确禁止。

当前在用的编排脚本放在 `/tmp`（不在仓库）：`frontier_watch*.py` 扫描公开前沿，`auto_pipeline.py` 每 300 s 合并新候选，`final_slot.py` 在 9 个 UTC 收口点提交，GPU 模板在 `/tmp/ga_kernel_full4`、调度器在 `/tmp/gpu_wave/scheduler.py`。

## 目录与保留约定

| 目录 | 保留内容 |
| --- | --- |
| `docs/` | 本指南、研究概况、来源记录 |
| `src/squares/` | 官方评分封装、逐题合并、提交校验与官方 v20 |
| `data/references/` | 来源清单、逐题榜快照、历史提交身份表、GPU run_report、清理记录 |
| `outputs/submissions/` | 仅当前官方最佳 `gpu_f_20261116/`（提交 CSV、完整评分、provenance、run_report） |
| `outputs/scores/` | 历史公共收益对照的小型完整评分 |

正式提交的原始字节以保存的完整 CSV 为准。历史提交（000 级 ref）的 CSV 已在 2026-11-16 清理中删除，但 ref、官方分、SHA-256 与行数保留在 `data/references/official_submissions_20261116.json`，可据以核对任何旧结论。公开 donor 的固定版本与 SHA-256 保留在 `data/references/sources.json`，本地坐标副本已随旧 pilot 管线删除。

后续实验先将结论与停止原因更新到 `docs/research.md`，再清理被替代或无用途的中间产物。有效坐标、来源谱系和最终验证需一起保留，不再为每轮实验新建独立说明。2026-11-16 按此约定删除停止方向的脚本、原始下载、中间合并与旧提交归档，释放约 18.3 GiB；具体路径与保留证据见[清理记录](../data/references/cleanup_20261116.json)。
