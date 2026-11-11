# 深度研究报告 — 2026-11-11 晚场

本报告汇总 2026-11-11 下午至晚间围绕“新全局构型 / 模板族搜索”的并行研究。
所有收益均以官方 v20 指标、文本 / float64 双路径、1000 题有效为准。

## 1. 正式成绩进展

| 提交 | 内容 | 本地双路径 | 官方 | 排名 |
|---|---|---:|---:|---:|
| 58237691 | public2：nilanjan seam-dp + busyaprime FQ，34 题 | 22.194550031155 | 22.1945500311 | 104/1942 |
| **58239472** | **public2 + penguin069 boxed 认证联合，25 题，净 `0.000398183`** | **22.194151848166** | **22.194152** | **103/1942** |

- 当前归档：`outputs/submissions/v124_plus_daily44_public2_penguin_20261111/`
- 当前文件 SHA-256：`11b5e39c840182b905450505e5800ce0b033c776107c5b751baea8551be39075`
- 来源：`penguin069/squares-boxed-public-certified-union`（2026-11-11 12:39 UTC，输出 SHA `f86cb7d8…`，249 个新几何组、117 个钉住的公开源）
- 官方榜快照 2026-11-11T13:45:48Z 确认：Score 22.194152、SubmissionCount 11、Rank 103/1942。

## 2. 新路线一：从零 K²+D 模板（负结果，硬容量界）

子代理 F 实现并测试了四类模板：T1 行带（冻结 (K−t)×K 直立格，t=1..4）、T2 阶梯断层、T3 直斜接缝、T4 角块。

关键测量（n=971，L_record=31.636789）：

| t | 冻结格 | 带内需放 | 带容量 | 缺口 |
|---:|---:|---:|---:|---:|
| 1 | 930 | 41 | 31 | **10 = D** |
| 2 | 899 | 72 | 62 | **10 = D** |
| 3 | 868 | 103 | 93 | **10 = D** |

T4 由面积直接排除；从零全局优化收敛到 `L=K+1`。结论：**任何“保持直立子格刚性、把 D 个方块塞进 f<1 边界带”的构造都恰好少 D 个方块**；这类模板不再尝试。产物：`outputs/experiments/research_20261111/templates/`。

## 3. 新路线二：记录族反推（CDB / 中心对角块）

子代理 H 从 evand atlas 与 Friedman/Ellsworth 目录反推出 **centered diagonal block（CDB）** 族：

- 几何：K×K 格沿反对角切成四块阶梯，两个半格在 x/y 各拉开 s，中心放 b×b 的 45° 块；`L=K+s`，`f=s`。
- 精确复现：n=26（`7/2+3/√2`）、n=65（`5+5/√2`）、n=85（`3√2−7/2`）、n=89（`7/√2−4`），误差 1e-15。
- `f(D)` 表（K=31，D=1..39）从 0.506591 平滑升到 0.998785；重复常数包括 `5/√2−3`（27 题）、`4√2−5`（8 题）、`1/√2`（18 题）。
- 容量反演：K=31 时该族在 f≤0.70 的平台只有 **966 题**，无法到达 n=971 的 31.636789；对 911/910/791/972/793/908/969/862 同样不足。
- 校准：n=687 的当前解与该族预测在 1e-6 内一致，说明现有前沿已经使用该族。

结论：CDB 是记录族的“骨架”，但不是新收益来源；详细公式、f(D) 表和复现脚本见 `outputs/experiments/research_20261111/literature/SPEC.md`。

## 4. 新路线三：evand packer 目标 campaign

子代理 G 在公开 `evand/square-packing` 引擎上跑了 0.74 CPU-h、348 次应用，目标是 971/911/910/791/972/793/908/969/862/687/328。

- 结构移动（band、chainshift、reinsert、add、drop、kick、melt）全部 0 赢家。
- 唯一认证赢家：**n=910，L 30.679153253763 → 30.679150986160**，总增益 `7.517e-8`。
- 合并后本地 22.194151772995，双路径 1000/1000 有效；产物 `outputs/merged/v124_plus_daily44_public2_penguin_n910/`。
- 结论：该引擎在当前前沿只能做同盆地微调；若要继续，需为大 n 移植 band/bulb/fault 生成器并给单题 10+ CPU-h。

## 5. 关键校准：头部题已经是“多角度倾斜族”

对当前前沿做角度谱分析（倾斜角折到 0–45°，>1° 计入）：

| n | 倾斜方块 | 中位角 | 不同角（1° 分箱） |
|---:|---:|---:|---:|
| 299 | 86 | 26.87° | 16 |
| 971 | 270 | 24.46° | 28 |
| 911 | 350 | 24.47° | 18 |
| 910 | 269 | 24.66° | 34 |
| 908 | 206 | 24.26° | 17 |
| 969 | 208 | 24.51° | 17 |

Cats and boxes 的公开 notebook（`pjmathematician/three-square-packings-that-beat-the-records`）说明他们的破纪录方法正是“更大的倾斜区 + 14–21 个略不同角度 / 对角两个独立块”。上表显示**我们的头部题已经是同族结构**，且 n=299/260/232 的当前解比 Cats 公开的三个新布局更小。

因此头部 0.001–0.0013 的逐题差距不是“缺结构”，而是**同一多角度族内的优化质量差距**；正确的工具是能跨盆地搜索的 GA/进化算法，而不是刚性带镜像或从零模板。

## 6. 外部全局搜索

- `grennwolf/squares-in-squares-top-1-santa-2025`（排行榜第 3 的 inspector gadget 队）正在 Kaggle GPU 上运行 Santa-2025 1st-place 的岛式 GA；其 `rank.py` 以“距逐题 leader 的 gap”排序，天然优先 971/911/910。该 notebook 的 atlas 起点与当前前沿在这些题上仅差约 3e-10，因此其输出可直接作为新候选来源。
- 截至本报告，该 notebook 仍为 RUNNING，尚无公开输出；若完成，应按逐题完整 n 组认证后合并。

## 7. 继续方向（按期望收益排序）

1. **GPU/CPU 进化搜索**：以当前前沿为种子，跑岛式 GA（大规模变异 + 交叉 + 固定 L 松弛 + LP polish），目标 971/911/910/791/972。头部题已在多角度族内，GA 是唯一有公开证据能继续改善该族的工具。
2. **逐题吸收公开更新**：penguin/busyaprime/nilanjan/atlas 仍在日内更新；每次新输出用 `squares merge` 逐题筛选，只有完整 n 组且官方 L 严格更小才收。
3. **停止**：刚性带镜像、单方块插入、删除+polish、固定角 LP、从零 K²+D 模板、CDB 模板、evand 引擎的结构移动——均已有硬负结果或容量证书。

## 8. 产物索引

- 正式归档：`outputs/submissions/v124_plus_daily44_public2_penguin_20261111/`
- n=910 候选：`outputs/merged/v124_plus_daily44_public2_penguin_n910/`
- 模板负结果：`outputs/experiments/research_20261111/templates/`
- CDB/记录族：`outputs/experiments/research_20261111/literature/`
- evand campaign：`outputs/experiments/research_20261111/packercampaign/`
- 公开前沿 gap：`outputs/experiments/research_20261111/public_frontier/`
