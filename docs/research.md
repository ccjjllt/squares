# 研究概况与放弃原因

本页为研究状态入口。历史清理范围见[清理记录](../data/references/cleanup_history.json)，官方提交身份链见[提交记录](../data/references/official_submissions.json)。

## 11 月 20 日深度研究战役

官方最好 **22.1060264871**（ref `58592523`，fq/harden 增量）← `58589527` = 22.1063144462（公开 malyshev Living Atlas v169 合并）← 22.1267039903。本轮多 subagent 并行深度研究 + Kaggle CPU（zhuating）/ Colab GPU（rainer，80 units，5 账号中唯一有额度）远端算力，本机零搜索。

**关键研究结论**（详见 [CPU 引擎笔记](../outputs/research_20261120/notes_cpu_engines.md)、[斜带拼接笔记](../outputs/research_20261120/notes_bands.md)）：
- 过去**只用 evand `packer hop`（3.3e-7 score/CPU-h）**，同 repo（pin==HEAD）的 `fq`/`harden`/`hhop` 从未用；alexchilton 实测 fq 系 **0.004 score/CPU-h（30-50×）**，gadget quench + fault DP 代码 CC0 公开。**重叠起点必须 `--round-r0 0.15 --round-compress`，否则塌回 k+1 网格**（解释旧 GPU 滑行 396 题 0 胜）。Sparrow 否决（产不出单位正方形精确接触解）。
- GeiserX 代码 Apache-2.0 公开（`k123_join`/`k123_tartan`/`k123_step57`，须署名 Sergio Fernández Rubio）。**803（747 join，641/747 可继承）/969（chains-of-9）**可得；730/785、786/843 是「锁」（记录 f 差 ~4e-12=加行设计，条件收益 ~2.9e-3）。
- **730 家族（730/785/842/901/962）= 289=17² 个 45° 实心核 + 轴向圈**，frac 恒 0.520815；GA rank.py 排除 ≥5 个 45° 方块的题，故 GA 不碰它。突破需 tartan 滑移（17 宽 phi=2.385°），是 GeiserX **尚未建成的开放项**（价值 ~0.005）。

**算力部署与收益**：
| 战役 | 平台 | 状态/收益 |
| --- | --- | --- |
| fq/harden 高产扫掠 | zhuating CPU | COMPLETE，**+0.000288**（333/759/793/805/849/924/977），已提交 58592523 |
| gadget quench + fault DP（换供体换排序，3 轮自迭代） | zhuating CPU | RUNNING，预期 +0.0003~0.002 |
| 跨题拼接 + fq 修缝（join/tartan/803 surgery/234 reduce/step57 五 lane） | zhuating CPU | RUNNING，预期 229 族 2.35e-4 / 969 4.3e-4 / 803 7.7e-5 / 730 tartan ≤1.6e-3 |
| plain-hop 对照 | zhuating CPU | RUNNING |
| 岛式 GA plain-start | rainer Colab T4 | 0 改善（jammed，预期内），会话已回收；待拼接起点注入 B 组 |

## 11 月 19 日晚间复核

正式提交仍为 **22.1267039903**，北京时间 21:36 观察排名 225 / 2254。公开 v26 坐标与两份已完成的 CPU 搜索产物逐题合并后，独立全量复分为 **22.106322870827146**，两种解析各 1,000 题有效。候选单独保存，较正式提交改善了 255 个不同的题。距榜首仍差 0.066371790，下一轮优先研究跨题斜带拼接及其在大题上的传播。[研究结论、公开实现及实验设计](research_20261119.md) · [候选 CSV](../outputs/research_20261119/candidate.csv)

## 11 月 19 日上午 10:50 快照（北京时间）

| 项目 | 当前值 |
| --- | --- |
| 官方最好提交 | **`58520513`** = **`22.1267039903`**（`2026-11-18T18:00:29Z`，COMPLETE，排名 **122 / 2240**） |
| 本地权威 bank | `22.12670399038623`（`outputs/submissions/bank_20261117/submission.csv`，SHA `1d2c7665…`，500,500 行，双路径 1000/1000 有效） |
| 逐题差距 | 对照 [`perpuzzle_best_20261118.csv`](../data/references/leaderboards/perpuzzle_best_20261118.csv)（逐题合计 `22.0310070197`，单队榜首 `22.039951081`），落后约 `0.0957`（~399 题）；100% 差距由未公开坐标队伍持有（Cats and boxes 占 ~68%） |
| 隔夜 Kaggle CPU 实测 | `sis-cpp-engine-gap2-20261118`（8.24h, 57 题）**0 胜**；`sis-alexkit-d1d2-20261118`（8.35h, 13 题）**0 胜**；`sis-d1-freeoffset2-20261118` **0 胜**；`sis-alexkit-wide-20261118`（9.03h）**21 胜 `+2.615e-5`**、`sis-alexkit-wide2-20261118`（8.82h）**12 胜 `+2.259e-5`**（`hop_best.csv` 已 COMPLETE 待收割） |
| 算力状态 | Colab 免费 T4 于 11-18 16:00Z 耗尽额度（`colab_keeper.sh` 90min backoff 待恢复）；Kaggle GPU 周配额（ccjjllt/qingyu1232/zhuating）于 **2026-11-21 00:00Z** 刷新 |

## 当前有效主线（继续）

1. **公开前沿逐题合并**：持续扫描 Kaggle 公开输出/数据集与 GitHub 精确证书，经 `squares merge` 双路径严格认证。本轮主力降幅来自此路线（`boxed_v56` +5.378e-3、`rosswade` +1.355e-3、`alexchilton` +1.282e-3、`Mishapolk` 精确证书 +1.040e-3、`Joost` n=299 经 `1e-12` 中心膨胀 +4.261e-4、`jazivxt` 等）。
2. **Santa 2025 岛式 GPU GA**（`grennwolf` 移植，Colab T4 / Kaggle GPU `NPROC=12` 静态分区）：唯一能产生大额自研收益的跨盆地搜索。Colab T4 已在 n=448/376/264 拿到 `+3.836e-4`；11-15/16 Kaggle GPU（gpu-a/b/d/f 等）合计贡献约 `+1.2e-3`。额度恢复后继续主攻中段 gap（24–288）及未饱和题。
3. **`evand packer hop` 宽范围盆地跳跃**（Kaggle CPU）：隔夜两批分别报告 21 和 12 题改善。换用晚间公开合并基线逐题认证后，547、644、862、915 四题仍有净贡献，已计入晚间研究候选。

## 已放弃研究方向与停止原因

| 停止路线 | 关键实验结果 | 放弃原因 |
| --- | --- | --- |
| 旧本机生成 + GPU 松弛 pilot 管线（`pilot01–09`, `free_polish`, `soft_quench`） | 仅早期的 n=642/459 有微小改善，大批轨迹局部修复后丢失收益 | 已被静态分区 Santa-2025 GPU GA 与公开前沿合并完全取代 |
| GPU 可微 SAT 滑行（`sis-glide-full`，L4 7.4 h） | 396 题 3 轮全扫，0 胜 | 可微罚函数无法把压缩后的重叠推回超静定合法布局 |
| CPU 接触抛光 / LP / LNS / 波次 / 退火 / 刚体引擎（`cpu-lp`/`block-lns`/`cpu-wave`/`anneal`/`polish`/`band`/`engine`/`engine_deep`） | 全 999 题固定角 LP 在 `dL=1e-6` 即不可行；396/396 落后题 `max\|s1−s0\|=0`；连续平移上界 `≤1e-7`（差 `10⁵–10⁶` 倍）；`anneal` 仅 LP 得 `7.1e-9`（`E≈k·δ²`）；`band` 9 题 3.48 h 0 胜；刚体目标边长最小重叠 `0.052–0.053`（gap 的 2.9×）；`rosswade` 移植中 51% 布局存在 >40 格大刚体被 Hopper 锁死，全放开产生 `1.2` 重叠 | 当前 bank 接触图超静定、完全卡死（jammed），无连续下降方向；必须跨盆地改变接触图 |
| C++20 引擎 Kaggle CPU 战役（`corentinlaudicina`，`self-polish`/`self-ga`/`self-cycle`/`polish2`/`d1-2224`/`d2-ladder`/`d2-gadget`/`gap2`） | 仅 `broad-seeded` 产出 1 题（n=545 `+4.22e-6`）；其余及隔夜 `gap2`（8.24 h, 57 题）、`d1-2224`（21/21 valid）、`d2-ladder`（17/17 valid，近失 `2–5e-5`）全 **0 胜** | 单位算力难以跨过 `0.007–0.021` 的构型壁垒；停止继续部署及监控脚本 |
| 实心核主 gadget / 阶梯多联骨牌 / 多角度核（`master65`/`master626`/`master291`/`staircase65`/`multiangle`） | 切触界 `f=m/√2−(K/2−1)` 精确复现 bank（65: `0.535534`、626: `0.520815`、291: `14+5√2/2`）；4,261 个 staircase polyomino、多种旋转/扇形核及 20 种双核排列全劣 | 家族在 bank 侧数学精确封闭；记录侧优势来自非实心核与多角度松弛布局 |
| 闭式模板 / 中心菱形 / 旋转核 / 格点 / 带区相位 / 三相位 MIS / 自由偏移（`cdb`/`cdb2`/`templates`/`gadget`/`lattice`/`cpsat`/`theory`/`theory2`/`bandphase`/`mis401`/`d1-freeoffset`） | CDB 3.64M 三元组 0 胜（47 平 35 劣），证明旋转核 `s(φ)≥s(45°)`；5 套闭式模板（30,089 参数）0 胜；双晶格断层 König 证明 MIS=`k²`；`L_rec(842)` 下任意轴格封顶 `841=29²`；4 相位仅达 `836<842`；带区相位在记录侧缺 15–38 格；`mis401` 纯晶格封顶 `400<401`；`T3` 自由偏移 6/6 不可行、`d1-freeoffset2` 0 胜；`alexkit-d1d2`（8.35 h）0 胜 | 刚性晶格/闭式构造容量严格不足或被 edge-lock 锁死；记录侧 D1 `f=0.4895 < 1/√2` 证明其突破了晶格+刚性 void 屏障，属自由角度重铺砌 |
| 外部文献与精确证书深度挖掘（`external 1–3`/`targeted`/`frontier_agent`/`harvest`） | 扫遍 60,000+ 组、25+ 数据集、27+ GitHub 仓：除已并入的 Mishapolk / Joost n=299 / jlevy 等外 **0 胜**；11-18 复审 379 组 Joost/jlevy（138 组原边长低于 bank，但余量 `3e-15..1e-12 < 1e-11` 膨胀代价）0 组可用 | 公开外部证书库已被完全吃干；仅保留常规哨兵捕获日内新增 |
| TPU 路线（`sis-tpu-probe`） | 长期 QUEUED，无输出 | 排队过慢，用户明确不采用 TPU |

## 关键方法论与结构结论

1. **废面积律与两晶格互锁**：`W = L² − n` 呈近似线性，`(f,f)` 两晶格互锁完美中心在 `f=1/2`；D1 记录 `f` 从 0.533 降至 0.4895（低于 `1/√2` 刚性空腔下界），说明记录侧非固定 gadget 或刚性 defect，而是随 `k` 变化的重铺砌/fan 构型。
2. **严格双路由门禁**：任何候选必须同时满足 `n == 行数`、`n ≤ L²`、逐对 SAT 无重叠与 `squares merge/score` 在 `text`/`float64` 双路径 1000/1000 有效；零间隙精确证书需经 `1e-12` 膨胀验证后才可入库。
3. **算力纪律**：禁止在本机跑搜索/批量优化（此前 `near_square_s2.py` 误跑峰值内存达 103 GB）；重计算一律在 Colab / Kaggle 运行，本机只负责认证与提交。
