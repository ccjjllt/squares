# 比赛说明

[Squares in Squares](https://www.kaggle.com/competitions/squares-in-squares/overview) 是几何优化比赛：对每个 `n=1…1000`，将 n 个边长为 1 的正方形放入尽可能小的轴对齐正方形容器。小正方形可以旋转，内部不能重叠。

以下信息来自 2026 年 11 月 6 日保存的[比赛快照](../data/references/kaggle/competition_snapshot.json)；后续日期或规则变化以比赛页面为准。

## 评分与提交

每题的分数为 `max(0, L / sqrt(n) - 1)`，1,000 题相加，**越低越好**。L 由所有方块角点的轴对齐包围盒计算，不直接提交。各题独立，完整布局可以按 n 组组合。

官方只提供提交样例，没有传统训练集。完整文件共 **500,500 行**：

| 列 | 含义 |
| --- | --- |
| `id` | 唯一整数行标识 |
| `n` | 题目规模，1 到 1,000 |
| `square_id` | 该题方块编号，0 到 n−1 |
| `x`, `y` | 方块中心坐标 |
| `angle` | 旋转角度，单位为弧度 |

部分提交以整题为单位；缺失题目使用 `ceil(sqrt(n))` 网格边长计分。全网格参考总分为 **28.9376699166**。本地样例位于 `data/competition/sample_submission.csv`。

官方 v20 对重叠使用高精度区间判定；代码中的 `1e-8` 不是允许穿透量。评分入口接收 DataFrame，因此坐标的原始文本和 float64 读写路径可能有差异。项目提供两种评分模式，详见[使用说明](getting-started.md)。缺失或无效题目通常计网格罚分，合法但比网格更差的布局不会自动截断。完整实现见[官方评分 Notebook](https://www.kaggle.com/code/metric/squares-in-squares)。

## 时间与限制

| 项目 | 保存的官方信息 |
| --- | --- |
| 奖金 | 共 50,000 美元，含两次各 5,000 美元阶段奖 |
| 提交次数 | 每天最多 10 次，最终选择 1 次提交 |
| 队伍人数 | 最多 5 人 |
| 最终截止 | 2027 年 7 月 19 日 07:59，北京时间 |
| 阶段奖截止 | 2027 年 1 月 18 日、4 月 19 日 07:59，北京时间 |

[官方规则](https://www.kaggle.com/competitions/squares-in-squares/rules)规定外部材料的使用和获奖交付要求；公开代码、坐标和图像的来源分别保留在[第三方来源说明](third-party.md)中。

## 项目已有成绩

| 方案 | 得分 | 状态 |
| --- | ---: | --- |
| Stretching v2 | **22.2427257787** | Kaggle 正式提交 58044087，评分完成 |
| Living Atlas v79 | 22.238567040753 | 本地官方 float64 路径，1,000 题有效 |
| Boxed In v16 | 22.238211260762 | 本地官方 float64 路径，1,000 题有效，尚未提交 |

正式回执保存在 [Kaggle 状态记录](../outputs/submissions/public_stretching_v2/kaggle_status.json)，本地分数分别见 [Atlas 报告](../outputs/scores/atlas_v79/report.json)和 [Boxed 报告](../outputs/scores/boxed_v16/report.json)。
