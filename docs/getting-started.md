# 使用指南

所有命令从项目根目录运行。研究状态与停止原因见[研究概况](research.md)，第三方版本见[来源记录](third-party.md)。

## 问题与文件格式

对每个 `n=1…1000`，把 n 个边长为 1 的正方形放入尽可能小的轴对齐正方形容器。方块可以旋转，内部不能重叠。评分为 `sum(max(0, L_n / sqrt(n) - 1))`，越低越好；`L_n` 由方块角点的包围盒计算。

完整提交包含 500,500 行，列为 `id,n,square_id,x,y,angle`。`id` 为唯一非负整数，`square_id` 在每题覆盖 `0…n-1`，`x/y` 是中心坐标，`angle` 单位为弧度。候选文件可只包含部分题目，但每个 n 必须完整。缺失或无效题目按网格罚分处理；合法但更差的布局不会自动截断到网格分。

## 环境与检查

项目默认 Python 3.12，依赖由 `uv.lock` 固定。结构搜索和局部修复需要 `experiments` 依赖组中的 SciPy：

```sh
uv sync --locked --extra experiments
uv run squares --help
uv run squares inspect outputs/submissions/v124_plus_daily44_public2_penguin_ga_nilan_20261111/submission.csv
```

`inspect` 检查格式、标识符和题目完整性，不检查重叠。新环境没有布局文件时，可生成小型网格验证安装：

```sh
uv run squares baseline --max-n 10 --output outputs/examples/grid10.csv
uv run squares score outputs/examples/grid10.csv --max-n 10 --mode both --workers 1 --output-dir outputs/examples/grid10_score
```

仅对前 10 题计算的分数不能与完整比赛成绩比较。

## 官方评分与跨轮合并

评分使用原样保存的官方 v20。`text` 模式保留原始十进制文本；`float64` 模式经 pandas 的 round-trip 浮点读写后评分；默认 `both` 执行两条路径。高精度接触判定对微小重叠和读写精度敏感，浮点残差小并不等于有效布局。

每次输出 `report.json` 和 `per_puzzle.csv`，包含文件/评分器哈希、环境版本、有效性及逐题分数。已提交题目无效时命令返回非零状态；总分不能代替有效性检查。

从下一轮实验中选择每题最佳布局：

```sh
uv run squares merge \
  --baseline outputs/submissions/v124_plus_daily44_public2_penguin_ga_nilan_20261111/submission.csv \
  --baseline-report outputs/submissions/v124_plus_daily44_public2_penguin_ga_nilan_20261111/validation/report.json \
  --candidate outputs/experiments/next/remote/improved_groups.csv \
  --output-dir outputs/merged/next --workers 4
```

`--candidate` 可重复。示例中的 `next/remote/improved_groups.csv` 是待生成的新实验结果，需替换为实际路径。合并按完整 n 组选择；两条评分路径都不得比基线退步，保留原始数值文本并记录来源。同题的多次改善只按最终赢家计算一次。

`--baseline-report` 仅复用与基线哈希、评分器和环境一致的完整报告；环境改变时省略该参数重新评分。最终序列化文件在提交前仍需完整独立复评：

```sh
uv run squares score outputs/merged/next/submission.csv \
  --mode both --workers 4 --output-dir outputs/merged/next/validation
```

这些命令只生成和验证本地文件，不提交比赛。官方评分源码位于 `src/squares/_vendor/`；更新版本时应重新记录来源和哈希。

## 保留的结构搜索流程

CPU 生成迁移链与接缝交叉候选，GPU 批量连续松弛，官方评分接受有效赢家。新赢家和近优布局可导出为下一轮供体；目前跨轮结构生成仍需重新调用脚本。

生成一轮有界候选：

```sh
uv run python scripts/experiments/prepare_candidates.py \
  --baseline outputs/submissions/v124_plus_daily44_public2_penguin_ga_nilan_20261111/submission.csv \
  --baseline-lineage-json outputs/submissions/v124_plus_daily44_public2_penguin_ga_nilan_20261111/baseline_lineage.json \
  --donor data/public/penguin_v2/submission.csv \
  --donor data/public/atlas_v79/submission.csv \
  --donor data/public/daily_v13/submission.csv \
  --max-candidates 48 --max-seconds 120 \
  --output-dir outputs/experiments/next/candidates
```

可用 `--parent-n` 聚焦指定父题，用 `--max-parents-per-n`、`--slab-beam-width` 和 `--crossover-children` 控制多样性。默认纪录表 `data/references/leaderboards/perpuzzle_best_20261029.csv` 是历史排序线索，不能作为当前可获得收益。

继续已有迁移链时，成对传入 `--donor-pool-npz` 和 `--donor-pool-json`，指向同一次运行导出的 `donors.npz/json`。Pilot04 的供体保存在 `outputs/experiments/pilot04/remote/pilot04/`。上例的 `baseline_lineage.json` 对应最终基线中的459、642，保留已有链深度；更换基线时也应提供相应谱系，不要用旧基线的谱系文件描述新坐标。

GPU 环境需要安装本项目、NVIDIA CUDA 与匹配的 CuPy；普通本地环境安装不包含 GPU 运行时。在该环境中运行：

```sh
python scripts/experiments/run_gpu_pilot.py \
  --baseline outputs/submissions/v124_plus_daily44_public2_penguin_ga_nilan_20261111/submission.csv \
  --candidates outputs/experiments/next/candidates/candidates.npz \
  --manifest outputs/experiments/next/candidates/manifest.json \
  --output-dir outputs/experiments/next/remote \
  --seconds 900 --batch 32 --staged-warm --incumbent-passes 10
```

`--local-repair` 可启用固定角度修复，默认关闭；已有实验显示它成本较高。评价以官方验证后的净收益为准。运行产物包括 `improved_groups.csv`、赢家/供体数组、`per_n_gains.json` 和 `summary.json`。

使用 Kaggle GPU 时，`scripts/kaggle/build_pilot_bundle.py` 将代码和候选打包，不包含凭据，也不启动远程运行。用 `--candidates-dir`、`--output-dir` 指定目录，并显式指定 `--account`、`--slug`、`--run-name` 以及至少一个 `--kernel-source` 或 `--dataset-source`。输入源必须实际包含与候选 manifest 中 SHA-256 一致的 `submission.csv`；最终合并基线需单独作为输入提供，公共 Penguin 输出不能代替它。打包命令的完整参数可用 `--help` 查看。

`scripts/kaggle/account_api.py` 提供显式账号的 quota/push/status/logs/output 操作，需要另行安装 Kaggle 官方 Python 包及配置本地凭据；`push` 会启动计算。计算账号与比赛提交账号分别指定，不因打包而自动更换提交身份。

## 目录与保留约定

| 目录 | 保留内容 |
| --- | --- |
| `docs/` | 本指南、研究概况、来源记录 |
| `src/squares/` | 官方评分封装、逐题合并、结构搜索与松弛 |
| `scripts/experiments/` | 候选生成与 GPU 搜索入口 |
| `scripts/kaggle/` | 运行打包和账号操作 |
| `third_party/` | 正在使用的 chains 原始摘录、CUDA 内核及来源清单 |
| `data/public/` | Penguin v2、Atlas v79、Daily v13、Square Deal v33 固定布局 |
| `data/references/` | 保留的来源、历史纪录及清理记录 |
| `outputs/submissions/` | 正式提交、完整评分、来源和回执 |
| `outputs/experiments/` | 有效主线的候选、供体、赢家及必要谱系证据 |

固定公开布局和最终完整CSV在本地保存，Git克隆不会自动携带；来源、评分、有效赢家和供体等小型证据列入保留范围，新实验产物默认忽略。恢复公开布局时按[来源清单](../data/references/sources.json)核对版本与哈希。最终几何与成绩可用Square Deal v33和Pilot04的`improved_groups.csv`逐题合并重建；Pilot04的旧输入可用Penguin v2和Pilot02的`improved_groups.csv`重建。

正式提交的原始字节仍以保存的完整CSV为准。以v33为基线重建时，n=1的angle文本为`0`，原提交为`0.0`；其余字段一致，几何和成绩相同，但文件哈希不同。逐字节恢复需保留该原始文本并核对研究概况中的SHA-256。

后续实验先将结论与停止原因更新到 `docs/research.md`，再清理被替代或无用途的中间产物。有效坐标、来源谱系和最终验证需一起保留，不再为每轮实验新建一篇独立说明。
