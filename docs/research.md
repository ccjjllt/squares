# 研究概况与取舍

整理日期：2026-11-16（北京时间）；实验与正式成绩截至 2026-11-16 06:20 UTC。本页是唯一研究状态入口，取代历史计划、公开前沿快照和逐轮长文。这里的“停止”是当前资源取舍，不是数学不可行或算法无效的证明。已放弃路线只留本页简述，不保留文档、脚本与中间产物；清理范围见[2026-11-13 清理记录](../data/references/cleanup_20261113.json)与[2026-11-16 清理记录](../data/references/cleanup_20261116.json)。

## 2026-11-16 当前状态

| 项目 | 值 |
| --- | --- |
| 官方最好 | **22.1327829081**（ref 58418244，COMPLETE，2026-11-16 05:50Z 提交） |
| 本地 bank | 同分 22.132782908131748；SHA-256 `3465e359…`；500,500 行；text/float64 均 1000/1000 有效 |
| 排名 / 差距 | rank 78；距榜首 22.0399511 约 `0.0928`；距 per-puzzle 纪录合计约 `0.0853`（389 题落后） |
| 今日/本段累计 | 自 2026-11-13 的 22.1730995210 累计下降 `0.0403` |
| 当前主线 | 公开前沿逐题合并（三个哨兵 240/300 s + `auto_pipeline` 300 s + 9 个收口点）＋ Kaggle GPU 静态分区 GA（`NPROC=12`，已实测 24/24 覆盖） |
| 算力状态 | ccjjllt / qingyu1232 / zhuating 的 GPU 周配额耗尽，2026-11-21 00:00Z 刷新；刷新前只靠公开 donor |
| 已停止 | CPU LP 抛光、block-LNS、CPU wave、TPU、旧 CPU/GPU pilot 管线、外部证书/文献库、全量 SLS/LP（详见文末清理） |

2026-11-15/16 官方链：58368557 `22.1411505741` → 58383648 `22.1404429508` → 58392028 `22.1400698371` → 58395980 `22.1400693231` → 58401147 `22.1342325793` → 58405258 `22.1338204867` → 58409967 `22.1333334050` → 58412458 `22.1333332097` → 58417748 `22.1332782582` → **58418244 `22.1327829081`**。当前主线的有效贡献来自公开 donor（`boxed_v56` +5.378e-3、jazivxt +3.731e-4、alexchilton +4.954e-4）与自研静态分区 GA（gpu-a/b/f 合计约 +1.2e-3）；逐轮证据见 `data/references/run_reports_20261116/`。

说明：下文 2026-11-16 之前各节提到的 `outputs/submissions/<name>/` 归档，除当前 `gpu_f_20261116/` 外均已在文末清理中删除；对应 ref、官方分与 SHA-256 见[历史提交身份表](../data/references/official_submissions_20261116.json)。

## 当前结果（已与官方对齐）

项目研究将 n=1…1000 个单位正方形分别装入尽量小的正方形容器。当前基线为 v124 公共合并 + 自研 n=642 链，再逐题吸收 Atlas 新版与 Daily v44。

| 项目 | 分数（越低越好） |
| --- | ---: |
| 旧正式提交 Stretching v2 | 22.2427257787 |
| 仓库旧归档 58068296（Square Deal v33 + 自研 n=459、642） | 22.2322230038 |
| 中间提交 58153974（Atlas v107 + 自研 n=642） | 22.2161912103，COMPLETE |
| 中间提交 58156456（Atlas v107 + 抛光 + Daily v35 + kirill + pilot08 n=642） | 22.2160143492，COMPLETE |
| 中间提交 58165370（Atlas v108 合并） | 22.2157802829，COMPLETE |
| 58226707（v108 + pilot09 n=642） | 22.2157801596，COMPLETE |
| 58227413（Atlas v124 + sqd v39 + daily v43，212 题，净约 `0.01641`） | 22.1993688316，COMPLETE |
| 58232975（v124 + Atlas 新版，28 题，净 `0.00304`） | 22.1963280817，COMPLETE |
| 58236174（v124+atlasnew2 + Daily v44，51 题，净 `5.0e-10`） | 22.1959256252，COMPLETE（本地 22.195925625258） |
| 58237691（v124+daily44 + public2：nilanjan seam-dp + busyaprime FQ，34 题，净 `0.001375594`） | 22.1945500311，COMPLETE（本地 22.1945500312） |
| 58239472（public2 + penguin 认证联合，25 题，净 `0.000398183`） | 22.194152，COMPLETE（本地 22.1941518482，排名 103/1942） |
| **58241961（public2+penguin + grennwolf GA，5 题，净 `0.000646850`）** | **22.193505，COMPLETE（本地 22.1935049984，排名 100/1942）** |
| **58242719（GA 合并 + nilanjan/atlas 15:15，10 题，净 `0.000451864`）** | **22.193053，COMPLETE（本地 22.1930531344，排名 97/1942）** |
| 58243251（+ evand n=910，净 `7.5e-8`） | 本地 22.1930530593，双路径 1000 有效（低于六位显示精度） |
| **58256528（公开更新：atlas 22:50 + prvsiyan 22:05 + GA 20:23，75+4 题，净 `0.0007196`）** | **22.1923334334，COMPLETE（排名 129/1958）** |
| **58258750（自研 GA 3 题 + jazivxt boxed-in-sub 11 题，净 `0.0006170`）** | **22.1917164423，COMPLETE（本地精确一致）** |
| **58260286（jlevy 认证 132/157/180 + prvsiyan 03:31 + jazivxt，净 `0.0017373`）** | **22.1899791624，COMPLETE（排名 101/1961）** |
| **58260715（JoeGun 22.1793 公开输出，136 题，净 `0.0128686`）** | **22.1771105280，COMPLETE（排名 52/1961）** |
| **58271587（GA A/B 恢复 11 题 + prvsiyan 09:51 39 题，净 `0.0013376`）** | **22.1757729367，COMPLETE（排名 77/1971）** |
| **58290129（koboshchan 公开产物 + contact polish round1–4，净 `0.0026734`）** | **22.1730995210，COMPLETE（排名 74/1999）** |

2026-11-12 归档文件：`outputs/submissions/public_update_1112_20261112/submission.csv`，SHA-256 `0cde0d2b3f575e8dd88531060d5678f4a152ece692f60c25a9ea87a2e435d079`，500,500 行、1,000 题，文本 / float64 双路径同分且全部有效；对应官方 22.1899791624（提交 58260286）。当前官方/本地最佳已更新为 **22.1730995210 / 22.17309952100155**（提交 58290129，`outputs/submissions/official_58290129_20261113/`，SHA-256 `13efc5fd…`，排名 74/1999）。相对 58239472 的官方 22.194152 累计下降 `0.0018187`（GA 5 题 + nilanjan/atlas 10 题 + evand n=910 + 11-12 公开更新 79 题）；相对旧归档累计下降约 `0.03989`。2026-11-12 凌晨公开源继续更新（atlas 22:50、prvsiyan 22:05、grennwolf GA 20:23），较上一官方提交下降 `0.0026734`。

2026-11-12 12:00 UTC 后公开前沿继续更新：jazivxt `boxed-in-sub` 11:16 版逐题 20 胜、净 `0.0005758`，已合入本地候选（中间合并 `jaz2_1112` 已于 2026-11-13 清理，最终结果进入 candidate h/j 与 official 58290129 归档；本地 **22.1751971838**，双路径 1000 有效）。随后两条新收益：

1. **CPU contact polish（Kaggle，非 GPU）**：`sis-polish-cpu-a/b` 两个 kernel 对 160 个 gap 最大题各跑 80 题（4 worker × 240 s），共 kept 27 题、净 `5.21e-5`；收益集中在 640（`4.35e-4`）、587（`2.21e-4`）、747（`3.83e-4`）、800（`3.33e-4`）。triage 显示 1000 题中只有 **69 题存在一阶可行方向**，其余 931 题接触图已卡死——这也解释了 polish 的低产出。
2. **koboshchan 公开产物**（新源）：`pell_corrugation/.../merged.csv`、`contact_slp_submission189`、`dual-pocket`，逐题认证 **25 胜**、净 `0.001855758936`，最大 n=269（`+6.87e-4`）、237（`+5.72e-4`）、971（`+3.41e-4`）、687（`+1.09e-4`）。

当前本地最佳 **22.1732892775**（`outputs/submissions/candidate_1112f_20261112/`，双路径 1000 有效），待 2026-11-13 00:00 UTC 额度重置后提交。当日 5 次提交额度已用尽（58256528/58258750/58260286/58260715/58271587）。Kaggle 周 GPU 配额 30h 已用尽，GA 需等配额重置。2026-11-12 新增主办方逐题榜快照 `data/references/leaderboards/perpuzzle_best_20261111.csv`。

### 2026-11-12 状态

- 主办方逐题榜最新快照（2026-11-11 13:54 UTC 抓取，`data/references/leaderboards/perpuzzle_best_20261111.csv`）：411 题落后，合计 `0.140833`；全部追平对应总分 `22.050884`。其中 337 题的逐题纪录由 “Cats and boxes” 持有。
- 刚性族诊断：把每题 `f = L - floor(sqrt(n))` 按 1e-6 聚类，20 个“重复 f 族”覆盖了 279 个实质差距中的 96 个、合计 `0.05195`。这些题的当前布局是共享同一刚性构件（如 `f=0.535534`、`0.707107`、`0.727922`），而对手在同一族内用了更优构件。优先攻族而不是逐题。
- 自研 GA（grennwolf Santa-2025 岛式 GA，2×T4）已于 2026-11-11 13:54–14:58 跑到 3 题（453/549/640，`1.143e-4`）；2026-11-12 03:00 UTC 起再开两个 7 小时定向 run（A：主办方榜动态排序；B：新榜前 100 题固定表），预计 09:30 UTC 完成。
- 公开前沿：atlas 02:28 新版、jazivxt 02:10、alexchilton 数据集 22:34 与 lucifer19/uneon/mzishran/keshigami 输出均已逐题比较，仅 jazivxt 胜出 11 题（`5.027e-4`）。

- 当前基线来源与官方回执、合并报告、完整独立评分（历史路径 `outputs/submissions/v124_plus_daily44_public2_penguin_ga_nilan_20261111/`；文件已于 2026-11-16 删除，ref/官方分/SHA-256 见[历史提交身份表](../data/references/official_submissions_20261116.json)）。
- 上一步 GA 基线：58241961 归档（历史路径 `outputs/submissions/v124_plus_daily44_public2_penguin_ga_20261111/`，同上）。
- 上一官方基线：58239472 归档（历史路径 `outputs/submissions/v124_plus_daily44_public2_penguin_20261111/`，同上）。

注意：`outputs/merged/` 曾在 2026-11-13 只保留四个血缘目录；这些目录也在 2026-11-16 清理中删除（结论保留在本页，身份见表末记录）。仓库以本页、当前最佳归档与身份表为准。2026-11-11 已删除零赢家 pilot06/07 本地副本、已超前中间合并、抛光重复完整 CSV 与 atlas_v107 本地下载，仅保留结论；2026-11-13 的删除范围见[清理记录](../data/references/cleanup_20261113.json)。

截至 2026-11-11 晚间的公开对照：**nilanjansaha123 的 seam-dp/soft-rigid 输出（09:58，`01cb16d8…`）与 busyaprime 的 FQ packings（12:05）合并后为 22.194550031**，与 busyaprime 标题中的 LB 22.1945500 一致；其中 34 题已合入。**penguin069 的 boxed 认证联合（12:39，`f86cb7d8…`）进一步在 25 题上优于该前沿，逐题合并后本地 22.1941518482**。**grennwolf/inspector gadget 的 Santa-2025 岛式 GA 输出（`submission_improved.csv`，SHA `0d1350e5…`）在 n=335/462/497/643/690 上更优，逐题合并后本地 22.1935049984（净 `0.00064685`）**；这是本轮首次由全局进化搜索拿到的实质收益。Daily v44（`48c51d2b…`，22.1959256255）、Atlas v127 certified（`0199ae…`，22.1959256349）、Square Deal v39（`396aa573…`，22.1995203）均已被超过。排行榜第一为非公开的 22.0544215；上一官方 22.194152 排名 103/1942，与榜首仍有约 `0.13973` 差距。相对 2026-10-29 逐题纪录仍有 **401 题实质差距、合计约 `0.12556`**（547 个原始正值中 146 个小于 1e-12），头部仍为 971/911/910/791/972/793/908/634/861/803（`8e-4–1.3e-3`）。

## 2026-11-13 研究主线（历史；脚本已于 2026-11-16 删除）

**多样结构生成 → 可靠可行性恢复 → 保留不同结构的近优供体 → 自动跨代搜索 → 赢家续压 → 双路径验证 → 逐题合并。** CPU 生成离散候选，GPU 按同 n 批量松弛；正式收益只计算最终选中的合法完整 n 组。升级点：续压只由新官方赢家触发；每个 n 保留 4–8 个结构不同的供体；约 20% 探索预算，不只复用旧赢家家族；谱系绑定题组坐标哈希，被替换题组以新来源为根。

| 有效结果 | 来源与贡献（相对已确认基线） |
| --- | --- |
| n=642 系列 | Penguin 与 Atlas 的 n=591 交叉中间态迁移到 642，再继续压缩；相对 Atlas v107 约 `1.21e-5`，pilot08 续压再约 `3.2e-6` |
| Daily v35 合并 | 164 题更优，净约 `2.46e-5`（相对抛光基线） |
| kirilltym 22-2160 部分解 | 8 题更优，净约 `1.49e-4` |
| 抛光 n=553、696 | CPU 接触抛光，净约 `4.5e-9`；738、652 对照零收益，路线冻结 |

代码入口当时保留 `prepare_candidates.py`、`run_gpu_pilot.py`，搜索模块保留 `structure.py`、`gpu_relax.py`、按需调用的 `local_repair.py` 与新增 `archive.py`（接触拓扑供体档案，P0）；这些脚本与模块已在 2026-11-16 清理中删除。`squares merge` 保留完整题组、原始坐标文本、双路径评分和来源追踪。

在线跨代循环仍需手动触发候选生成；`archive.py` 已提供按拓扑去重与每 n 4–8 供体配额，`run_gpu_pilot.py` 赢家自动续压待接。具体命令见[使用指南](getting-started.md)。

## 已完成实验与停止原因

| 路线 / 实验 | 已观察到的结果 | 当前决定及原因 |
| --- | --- | --- |
| Pilot01 | 96 候选×2轮，CUDA 约79.4秒；零直接赢家 | 清除运行副本，仅留进入后续赢家血缘的近优供体；零即时收益不等于中间态没有价值 |
| Pilot02、Pilot04 | Pilot02 改善642；Pilot04 24候选、30续压批次，约494.6秒，改善459与642 | 保留有效主线、赢家、谱系和小型复现材料，删除重复完整CSV |
| 独立固定角度 LP 续压 | 21次尝试、8次接受，约21.1秒；相对Pilot02累计额外改善约`1.364892361e-7`，随后被Pilot04覆盖 | 停止独立路线，删除专用脚本及产物；收益小且不再贡献最终结果。GPU主线的可选修复模块仍保留 |
| 小核心 / 薄带编辑与有限 refill | 29候选，固定角CPU和Pilot05自由角GPU均无净收益 | 停止当前编辑器，删除实现、候选及运行结果；有限编辑未显示效果，不将其扩大为完整FTMC工程 |
| 有限两列矩形构件组合 | 128 / 512构件，各检查1000题，合计约14.3秒；容量改善为0，没有候选进入官方评分 | 停止当前组合器，删除实现及构件库；它没有独立优化矩形，也不是完整递归DP |
| Pilot06、Pilot07 | 96 批次、约 95 秒 CUDA，零赢家；诊断：warm 200×1 带不动 dry_excess ~0.05，结构臂全灭或触及修复上限 | 保留诊断结论；pilot08 已改用深 warm（1500×2）+ 细化 + local-repair + 紧 dry 上限；2026-11-11 已删本地副本 |
| Pilot08 | n=642 续压赢家，增益约 `3.2e-6`，238 次 local-repair；其余 23 候选零赢家 | 已合入当前基线；同参数模板用于 pilot09；赢家产物本地保留 |
| Pilot09 | 12 候选、n=642 赢家 1，增益约 `1.23e-7`，334 次 local-repair | 待评，已合入 v108_plus_p09 并作为 v124 前基；非放弃路线，本地保留 |
| 抛光 n=696、553 | 固定角/自由角各 +2.8e-09、+1.7e-09，双路径验证通过；738、652 四组 <1.1e-10 | 只收过 1e-10 门限的题；已合入基线；2026-11-11 已删重复完整 CSV，仅留 90K 候选 |
| 已超前中间合并与下载 | atlas_v107_plus_self、atlas_v107_plus_self_polish、daily35_kirill 及 atlas_v107 本地下载均已被 v108/v124 链取代 | 2026-11-11 已删本地副本；链路以保留的 merge_report/provenance 与最终提交 CSV 为准 |
| Daily v35、kirilltym 22-2160 合并 | Daily 164 题 +2.46e-05；kirill 8 题 +1.49e-04；均双路径 1000 有效 | 已合入当前基线并提交 58156456 |
| Atlas v108、kirilltym v22 | v108 本地 22.21579565，v22 部分解；合并净约 `2.34e-04` | 已合入当前基线并提交 58165370；下一轮先刷新对照，避免重复研究已被超过的题目 |
| 大规模局部 LP 修复 | Pilot04 173次约207秒，仅5次通过浮点修复；Pilot05 83次约115秒，无新赢家 | 不作为普遍优化路线；只在主线中按较小穿透量筛选使用。求解失败不证明几何不可行 |
| 专用 GPU 吞吐研究 | n642、600步、三次重复，batch8/32/64约26.17/105.94/130.36条轨迹/秒 | 测量任务已结束，保留结论、删除专用脚本与原始输出；吞吐提升不是分数收益，也不保证跨题通用 |
| 旧 Stretching / Boxed 基线分析 | 原分析定位了大n及106题历史候选，但依据旧基线与2026-10-29纪录 | 删除旧分析脚本、表图、公共旧CSV及重复规划；不把旧约0.06463差距当当前可获收益 |
| Atlas v124 / atlasnew2 / Daily v44 合并 | v124 官方 22.1993688316；+Atlas 新版 22.1963280817；+Daily v44 后官方 22.1959256252（51 题，净 5.0e-10），1000/1000 有效 | 已提交 58236174；Daily v44 为当前公开最佳，Atlas v127 相对其 0 题增益，公开源刷新到此饱和 |
| fault-line gadget DP（公开实现） | 以当前前沿为供体提取 1166 donors、14.8K 非支配 gadget；对 325–1000 的 DP 最小 f 与当前 L−K 持平（约 2e-9 安全缝），零 n 进入认证 | 公开合并前沿已吸收全部 fault-line 组合；仅在新供体家族出现后重跑 |
| 精确刚性插入 / 空位扫描 | 对 20 个高空隙父布局、12 个角度做精确 SAT 自由域搜索，0 个可放点；最高 slack 父布局也只有亚单位缝隙 | 插入不是独立增益路线；若使用必须先扩张再压缩（成本更高） |
| 固定角压缩 LP（全 999 题） | 从 dL=1e-6 起单调试探，全部 `solver_rejected`；每方块 3–6 个零间隙接触且四壁贴边，接触图超静定 | 这是“局部无下降方向”的硬证书；不再对成熟布局做全量 SLP/局部 LP |
| evand Rust fq quench + bandflip | 用公开 `square-packing` 的 `fq`（PHR 增广拉格朗日）与 strip band-flip 在 971/910/911/908/791/972/687/328/642 上多 seed、loosen 1.02/1.05：L 不变或回弹，零赢家 | 实际 fq 引擎也无法突破合并前沿；JoeGun 的 92 次 polish 收益来自更松的公开起点，不是前沿本身 |
| 长尾 55 题结构搜索 | 目标 gap 1e-4–6e-4；冷 polish 55 次、插入 110 次、删除 55 次、镜像/带翻转 21 次、压缩+soft 6 次；全部零接受 | 记录布局是不同的最优解，不是当前布局的松弛；长尾同样需要新构型 |
| evand atlas / exact / tilings 外部布局 | 公开 atlas n≤324、exact register 324 份、n=964/1092/1228 证书逐题比较：0 题优于当前（n=964 当前 31.5355 < 证书 31.8595） | 外部精确研究库也被当前公开合并前沿支配；不再重复下载比对 |
| penguin 认证联合（12:39 UTC） | 249 个新几何组、117 个钉住的公开源；逐题合并后 25 题更优，净 `0.000398183`，本地 22.1941518482，双路径 1000 有效 | 已提交 58239472；来源与哈希见归档 provenance。公开合并仍在日内更新，需持续逐题吸收 |
| evand packer 目标 campaign | 0.74 CPU-h、348 次应用；仅 n=910 认证赢家 `7.517e-8`，band/chainshift/reinsert/add/drop/kick/melt 等结构移动全部 0 赢家 | 该引擎在当前前沿只能做同盆地微调；若继续需为大 n 移植 band/bulb/fault 生成器并给单题 10+ CPU-h |
| grennwolf Santa-2025 岛式 GA | 公共 notebook 的 `submission_improved.csv`（session 368440075，SHA `0d1350e5…`）逐题比较：5 题更优（335/462/497/643/690），净 `0.00064685`，本地 22.1935049984，双路径 1000 有效 | 已合并并准备提交；这是首次由全局进化搜索拿到的实质收益，证明头部多角度族内仍有可搜索空间 |
| 从零 K²+D 模板（T1 行带、T4 角块、全局） | T1 冻结 (K−t)×K 格后，f<1 的带容量比目标恰好少 `D` 个方块；T4 受面积排除；从零全局收敛到 `L=K+1` | 任何“保持直立子格刚性、把 D 个方块塞进 f<1 边界带”的构造都不可行；上界由容量给出，不需要再试同类模板 |
| 记录族反推（CDB / 中心对角块） | 精确复现 Friedman 的 n=26/65/85/89（`7/2+3/√2`、`5+5/√2` 等，1e-15）；f(D) 表在 K=31 平滑上升 0.5066→0.9988；该族在 K=31 的容量平台为 966，无法到达 971 的 31.6368；n=687 的当前解与该族预测 1e-6 内一致 | 当前合并前沿已使用该族；它不是新收益来源。f(D) 是数值最优接触构型而非闭式，H 的 SPEC 保留为供体/诊断资料 |
| 冻结网格 / 楔形再压缩（2026-11-12，40 题） | 5 族重启 × 11 次松弛；40 题全部 `ΔL=0`，δ=0.001 即出现真实重叠（官方判 n=971 的 730/733 重叠）；吸收率随 δ 线性（0.62–0.92），无阈值 | 停止该路线：当前布局在 1e-6–1e-2 内零间隙，差距是离散参数（带宽角度、行数、接缝）而非连续松弛；需要改变接触图的搜索（GA 已在跑） |
| 自研 GA 双 run 收尾（2026-11-12 02:15–09:15） | 两个 kernel 均在 7 小时末尾因**周 GPU 配额 30h 用尽**被杀（ERROR）；从 1469 个输出文件里恢复 `runs/improvements.csv` + `runs/starts/index.json`，下载 11 组 `.npy` 后逐题认证，净 `0.0004830`（497 最大 +2.16e-4） | 已合入 58271587；本周 GPU 配额已尽，后续只做公开合并与 CPU 实验 |
| JoeGun 22.1793 公开输出（2026-11-12 03:51） | 逐题比较 136 题更优，净 `0.0128686`；双路径认证通过；本地 22.1771105280 | 已提交 58260715；说明公开 Code 输出仍会阶段性跳变，必须持续扫描（此前其 22.2004 版本已吸收） |
| franciscouzo 精确证书库（2026-11-12） | 解析 720 个 n≤1000 的有理证书并逐题比较；0 题优于当前前沿（其 416 题低于主办方榜，但全部高于我们） | 不再重复；外部证书库（de Winter 40、griffcass 39、jlevy web 2000）同样 0 胜 |
| jlevy/squares 见证证书（2026-11-12） | 从 `github.com/jlevy/squares` 的 witness YAML 取到精确坐标；n=132/157/180 三题官方双路径认证通过，L 分别降 7.64e-3 / 6.70e-3 / 1.38e-3，合计 `0.00147534` | 已合入 58260286；同源的 2000 份证书里其余均不优于当前前沿；n>324 的外部库（franciscouzo、de Winter、griffcass）逐题比较后 0 胜 |
| 去尖角 / 两块分割（2026-11-12，10 尖角题 + 30 高 gap 题） | 精确复现 8/10 尖角题的刚性模板（`L=K+1/√2`），证明该族容量在 `s<1/√2` 时骤降回 `K²`；矩形块 CDB 需 `L=25.79`（比现有差 0.083）；两块分割全部差 0.11–0.23 | 两个家族都被现有布局支配，停止；尖角题的 0.005–0.025 只能来自离格接触图搜索（GPU GA） |
| Cats and boxes 公开方法（n=299/260/232） | 其“破纪录”布局不是单角刚性带：倾斜区更大、含 14–21 个略不同角度，或拆成对角两个独立块；这三个坐标已被我们当前前沿超过 | 结构原则是新线索：对 971/911/910/791/972 做“加厚多角度倾斜区”实验（subagent I 进行中），不再做刚性带镜像 |

主要瓶颈是可行性修复：Pilot02 中80条结构轨迹的原始包围盒更小，其中76条修复后失去收益。原始边长或碰撞损失的下降不能替代官方有效分数。2026-11-11 的补充结论更具体：当前合并前沿的接触图是**超静定**的，连续局部方法（LP、fq、soft、polish）没有无穷小下降方向；要再提高必须换构型（新的全局布局族），而不是继续压已有布局。记录族反推进一步表明：大 n 的纪录来自 CDB 类“平移半格 + 中心 45° 块”以及 Cats 的“加厚多角度倾斜区”两条路线；前者已被现有前沿吸收，后者是当前唯一有公开证据的新结构方向。

2026-11-11 晚间的角度谱分析给出一个关键校准：当前前沿的头部题**已经**是 Cats 所描述的多角度倾斜结构，而不是待改造的刚性单角带。n=971 有 270 个倾斜方块、中位角 24.46°、28 个不同角度；n=910 有 269 个、中位 24.66°、34 个不同角度；n=908 有 206 个、中位 24.26°、17 个不同角度；连 n=299 的 86 个倾斜方块也与 Cats 的 90 个/26.6° 结构同族，且我们更小。因此头部 0.001–0.0013 的逐题差距不是“缺结构”，而是**同一多角度族内的优化质量差距**；合适的工具是能跨盆地搜索的 GA/进化算法（grennwolf 的 Santa-2025 1st-place 方法正在 Kaggle GPU 上跑 971/911/910 等目标，起点 atlas 与当前前沿在这些题上仅差 3e-10），而不是再做刚性带镜像或从零模板。

## 当前不实施的方向

- **完整 FTMC / Rust、递归 fault-line DP、矩形独立优化**：公开 fault-line DP 已用当前前沿供体实测，1166 donors / 14.8K gadgets 零 n 进入认证；继续投入的边际收益低。仅在新供体家族或新 n 赢家出现后重跑。
- **fq 圆角压力硬化、Soft-to-Rigid、渐近构造、pinwheel / 全局非线性探索**：已用 evand 的实际 Rust `fq` 和 bandflip 实测，当前前沿零增益；fq 的公开收益来自更松起点。该方向冻结，除非出现新起点或新构型。
- **成熟布局全量 SLP、无结构随机重启、统一延长松弛、复杂多 GPU / FP32 工程**：全 999 题固定角压缩 LP 在 dL=1e-6 即不可行，说明没有局部无穷小运动；当前不投入。真正的下一步是全局/模板族搜索，需先给出目标题和小规模可验证实验。

这些方向只有在出现新构型、可复用实现或明确的小规模收益证据后才重新评估；不会因为旧计划里列过就自动继续。

## 2026-11-13 停止方向清理（已删除 5.41 GiB）

按“停止的研究只留本页简述，不保留文档、脚本和中间产物”的约定，本次清理删除了以下已停止路线。删除前 `outputs/` 为 6.1 GiB，清理后 682 MiB；仓库总计从约 7.5 GiB 降到 1.4 GiB。完整路径、大小和保留证据见[清理记录](../data/references/cleanup_20261113.json)。

| 已停止路线 | 最后结论（停止原因） | 已删除 |
| --- | --- | ---: |
| 2026-11-11 五路并行：fault-line gadget DP、evand fq/bandflip、精确插入、长尾 55 题、模板/CDB/记录族、全 999 题固定角 LP、公开 notebook 拆解 | 除 evand packer 的 n=910（`7.517e-8`，已合入当时基线）外全部 0 认证赢家；固定角 LP 在 dL=1e-6 即不可行，接触图超静定；fault-line DP 1166 donors/14.8K gadgets 零进入认证；外部布局与长尾均被当前前沿支配 | `research_20261111/` + 11 个专用脚本 + `free_polish.py`/`soft_quench.py`（123 MiB） |
| 2026-11-12 CDB、冻结网格/楔形、去尖角/两块分割、外部证书 hunt | CDB 901 题 0 胜；冻结网格 40 题 ΔL=0；去尖角为容量硬台阶；两块分割差 0.117–0.233；jlevy 3 胜已合入官方 58260286 | `research_20261112/`（196 MiB） |
| 2026-11-12b 近平方族 S2 | 626/842/902/963 全部 ΔL=0；626 精确坐在容量台阶（s 降 1e-3 容量 626→602），15 个多起点回到同一 L | `research_20261112b/s2/`（28 MiB） |
| 2026-11-13 d=9–12 两带+两轴块 | 244 次 swap + 34 次 transfer 全 0 改进；接触数 1.34–1.49× 等静定，整体收缩上界 ΔL≤9.8e-11 | `research_20261112b/bands/`（1.3 MiB） |
| 2026-11-12b 文献反推 + 外部坐标源 | 闭式族 1075 个父布局 0 胜；Karimi 两斜条差 0.08–0.11；31 类外部源只有 koboshchan 25 题胜出且已合入当前候选 | `literature/` + `external/`（2.87 GiB） |
| 2026-11-12b 逐题差距分析 | 目标表已过时，当前判断以 `data/references/leaderboards/perpuzzle_best_20261111.csv` 为准 | `research_20261112b/gaps/`（256 KiB） |
| 2026-11-12b 公开前沿原始下载 | 已完成扫描的临时 submission 与合并副本；kobosh pr45 9 胜、其余 0 胜、终检 0 胜已记录 | `frontier/downloads` 等 9 个目录（1.22 GiB） |
| 旧 GPU 结构 pilot 轮次 `next_*` | 9 轮全部 completed 且 improved_count=0 / winners=0，未进入当前血缘 | 9 个 `next_*` 目录（163 MiB） |
| 已被取代的中间合并链 | 最终坐标已固化在正式提交/当前候选与 provenance；逐轮 26 MB CSV 不再承担复现作用 | `outputs/merged/` 33 个目录（839 MiB） |
| 2026-11-12 日记 | 关键经验与基础设施结论已并入本页 | `docs/daily-2026-11-12.md` |

保留（2026-11-13 时点）：官方 58290129 / 当前候选 j / 暂存文件（同一 SHA-256 `13efc5fd…`）、其余 git 跟踪的正式提交归档、pilot01/02/04/08/09、`polish_n696_n553/candidate.csv`、四个血缘 merged 目录、`outputs/scores/`、`data/public/`、逐题榜快照，以及仍在使用的前沿监控报告和 `witness_to_submission.py`。**2026-11-16 清理后，上述提交 CSV、pilot 产物、merged 目录与 `data/public/` 已删除；仅保留当前最佳 `gpu_f_20261116/`、`outputs/scores/` 与 `data/references/`，身份见[历史提交表](../data/references/official_submissions_20261116.json)。**

2026-11-12 日记要点（删除前已并入）：公开 Code 输出会阶段性跳变，必须逐题扫描；jlevy witness 是有效的精确坐标来源；自研 GA 受周 GPU 30h 配额限制；公开 kernel/证书库扫描已饱和；重计算一律在 Kaggle，本机只做编排与 `squares merge/score` 认证。

## 下一步与证据保留

深度研究（2026-11-11，五并行）：v124 相对 v108 的 212 改进中 179 题实质提分（均值 `9.2e-5`，中位 `2.6e-5`，最大 n=593 `7.2e-4`），53% 相邻成串，证实相邻迁移。以 v124_plus_daily44_public2 为当前前沿，相对 2026-10-29 逐题纪录仍有 401 题实质差距、合计约 `0.12706`（547 个原始正值中 146 个小于 1e-12；早期 401/0.1319 口径已过时）；头部为 971/911/910/791/972/793/908/634/861/803（`8e-4–1.3e-3`）。本轮把公开代码与外部研究库真正跑了一遍：fault-line gadget DP（1166 donors / 14.8K gadgets）、evand Rust `fq` + bandflip、精确插入、全 999 题固定角压缩 LP、长尾 55 题结构搜索、evand atlas/exact/tilings 外部布局比对——**全部零赢家**；固定角 LP 在 dL=1e-6 即不可行，给出接触图超静定的硬证书。确认的增量来自公开合并：Atlas v124 → 新版 → Daily v44 → nilanjan/busyaprime public2；官方从 22.1993688316 降到 22.1959256252，再降到官方 22.1945500311（提交 58237691，本地 22.1945500312）。结论：公开前沿与成熟布局的局部空间都已饱和，下一步必须做**新全局构型/模板族搜索**，而不是继续压已有布局；任何新路线先给出目标 n、可验证小实验和 1e-10 门限。

下一轮先刷新公共对照和逐题差距，再围绕459、642及可迁移的相邻题开展有预算的跨轮搜索，保留不同接缝的近优状态。当前仍保留2026-10-29的逐题纪录CSV作为可选历史排序参考，不作为实时目标或收益预测。

以下为 2026-11-13 的保留清单；**2026-11-16 清理后，本清单中的 pilot 产物、merged 血缘目录与 `data/public/` 均已删除，仅保留文末“2026-11-16 停止方向清理”所列内容**：

产物只保留以下用途（2026-11-13 已按停止方向清理，删除范围见[清理记录](../data/references/cleanup_20261113.json)）：

- 2026-11-13 的产物清单已不再适用：其中的提交归档、pilot 产物、merged 血缘目录与 `data/public/` 已在 2026-11-16 清理中删除；仅保留 `outputs/scores/` 的历史评分对照。当前保留范围与验证方式见文末“2026-11-16 停止方向清理”。

原始回执、谱系和运行清单中的历史路径保持其记录语义，其中部分临时文件已删除；它们不是当前运行入口。清理前的实验摘要、删除清单和文件哈希集中记录在[2026-11-09 清理记录](../data/references/cleanup_20261109.json)和[2026-11-13 清理记录](../data/references/cleanup_20261113.json)。没有将废弃产物搬进新的归档目录。

### 2026-11-13 本机误跑与 Kaggle 执行纪律（重要）

- 2026-11-12 深夜 `near_square_s2.py` 在本机 Mac 误跑，峰值内存 **103 GB**；已 kill PID 90859/91262 及父 shell，并在脚本头部加硬保护：非 `/kaggle/input` 环境且未显式 `S2_ALLOW_LOCAL=1` 时直接退出。后续所有优化/搜索/批量验证一律在 Kaggle 运行，本机只做编排、下载、`squares merge/score` 认证。
- Kaggle CLI 当前 `~/.kaggle/access_token` 属于 **qingyu1232**（团队账号）；`ccjjllt` 的提交走 MCP。实测：
  - `qingyu1232` 的 dataset/kernel 创建、push、status、output 均正常（用 `KAGGLE_CONFIG_DIR=/tmp/kg_qingyu1232`）。
  - `ccjjllt` 的 private dataset 不能被 qingyu1232 kernel 挂载；跨账号用“把输入内嵌进 kernel”或改用 qingyu1232 自己的 dataset。
  - MCP 的 kernel 读接口对 ccjjllt 私有 kernel 一直 `Permission 'kernels.get' denied`，不要再依赖它取输出。
- 已在 qingyu1232 下验证 dataset 创建可用（`qingyu1232/sis-qytest-20261113`）；后续重计算 campaign 统一用 qingyu1232 dataset + kernel，结果下载后本机认证合并。

### 2026-11-13 近平方族结构化重优化：0 胜（停止方向）

- Kaggle CPU 独立双跑（`qingyu1232/sis-nearsquare-s2-20261112` v4 与 `qingyu1232/sis-ns2-20261113`，708 s / 1337 s）对 n=626/842/902/963 做三臂搜索（生成族精确枚举 + 5 刚体 SE(2) soft-to-rigid 多起点 + contact polish），**全部 ΔL=0**，`squares merge` 净收益 0。
- 关键证书：n=626 的当前布局恰好坐在其生成族的**容量台阶**上——精确计数 `s_min_feasible=0.520815` 与当前 L 完全相同；`s` 降 1e-3，容量从 626 掉到 602（−24 格）。15 个独立多起点（含 θ 偏离 45°、±1 换拓扑）全部收敛回同一 L，给出 5 刚体不可压证据。
- 结论：榜首的 0.502153 属于**另一个族**；连续松弛（LP/SLP/fq/soft/polish）在这一族上必然为 0。不要再对 k²+1/k²+2 做局部/小参数优化，除非找到新的分块+矩形孔+边界 filler 族。
- 产物已于 2026-11-13 清理（`s2/` 目录删除，本机误跑 103GB 与硬门禁结论保留在本页）；删除清单见[清理记录](../data/references/cleanup_20261113.json)。

### 2026-11-12 18:25 UTC 候选更新（koboshchan PR union）

- 前线监控从 koboshchan 新 commit/PR union 逐题认证 **126 题微缩**，净 `7.9189e-5`。
- 合并后本地 **22.17320935237965**（`outputs/submissions/candidate_1112h_20261112/`），独立 `squares score --mode both` 复核：text/float64 同分、1000 有效、0 invalid、0 missing（147 s）。
- 官方 22.1757729367 → 候选 22.1732093524，提升 `2.5636e-3`；对照公开榜约从 89 名升到 66 名。待 00:00 UTC 提交。
- 同轮 polish3（Kaggle CPU，64 个 open 题 × 600 s）仍在跑，预计 21:00 UTC 前出结果。

### 提交自动化（2026-11-13 00:01 UTC）

- 暂存路径：`outputs/submissions/staged_latest/submission.csv`（当前 = candidate h，sha `6dcabf79…`，22.1732093524）。
- 已启动后台脚本 `/tmp/auto_submit.sh`：等待到 2026-11-13 00:01:30 UTC，用 qingyu1232 团队账号 `kaggle competitions submit` 提交暂存文件，失败重试 3 次，日志 `/tmp/auto_submit.log`。00:00 前的任何新收益只需覆盖暂存文件即可被自动提交。
- 当前官方 22.1757729367（89 名）；候选 h 对照公开榜约 67 名。

### 2026-11-13 d=9–12 “两带 + 两轴块”结构化重优化：0 胜（停止方向）

- 4 个 Kaggle CPU kernel（`qingyu1232/sis-bands-d912-20261113` v1–v4，共 244 次 swap + 34 次 transfer，860/780/420 s 预算）对 971/910/972/908/911 做参数化重优化，**全部 0 改进**，无候选、净收益 0。
- 分解证据：每题 = 2 个轴对齐晶格块 + 2 个旋转带块（旋转晶格 + 阶梯剖面 + 逐行剪切；971 每条带 141 个方块）。L 由轴块 4 个外角决定；带角 ±2°、fan ±3°、shear ±0.6、平移 ±1、全局压缩 ±1%、带↔轴块单方块互换，全部回到同一 L。
- 卡死证据：971/910/908 接触数 2400–2880 = 1.34–1.49× 等静定 `2n−3`，中位自由位移 1e-11…1e-14，>2/3 方块完全卡死；整体收缩上界对应 ΔL：971 9.8e-11、910 1.9e-13、972 2.3e-13、908 2.1e-13、911 0。
- 结论：剩余 0.028–0.035（合计 score ≈0.0051）不是同一参数化的局部变形；要追需换块划分/换构造（非对称主块 + L 形左下块 + 不同缺口切法）。优先级低于公开前沿合并与 GPU GA。
- 产物已于 2026-11-13 清理（`bands/` 目录删除）；结论保留在本页，删除清单见[清理记录](../data/references/cleanup_20261113.json)。

### 自动任务队列（2026-11-13）

| 时间（UTC） | 脚本 | 动作 |
| --- | --- | --- |
| 00:01:30 | `/tmp/auto_submit.sh` | 提交 `staged_latest`（当前 candidate h，22.1732093524），失败重试 3 次 |
| kernel 完成后 | `/tmp/watch_polish3.sh` | 下载 `sis-polish3` 输出，逐文件 `squares merge`，只在新分更低时覆盖 `staged_latest` |
| 23:45（11-12） | `/tmp/final_check.sh` | 终检 JoeGun/jazivxt 新 run，只 merge 更新 `staged_latest`，不提交（给 00:01 用） |
| 04:10 | `/tmp/auto_frontier.py` | 扫 JoeGun/jazivxt 新 run；有 wins 则 merge + 提交（用当日剩余额度） |
| 11:30 / 15:30 | 同上 | 同上 |

- 所有 merge 都走 `squares merge` 的 text/float64 双路径认证；自动提交只提交认证后的 1000 题完整文件。
- 每日额度 5 次：00:01 用 1 次，frontier 自动最多 3 次，留 1 次手动余量。

### 2026-11-12 20:42 UTC contact polish round3（fresh triage，显著）

- `qingyu1232/sis-polish3-20261113`（fresh triage 全 1000 题 → top-64 open × 600 s，4 workers）完成：**57 题改进、净 `1.0792e-4`**，远高于 round1 的 `5.21e-5`。
- 最大收益：543（`3.35e-5`）、549（`2.12e-5`）、497（`1.70e-5`）、453（`1.58e-5`）、645（`9.9e-6`）、747（`4.3e-6`）、651（`4.0e-6`）。
- 合并后本地 **22.173101430589412**（`outputs/submissions/candidate_1112i_20261112/`），独立 `squares score --mode both` 复核：text/float64 同分、1000 有效；已更新 `staged_latest`，00:01 UTC 自动提交将使用该文件。
- 立即启动 round4：`qingyu1232/sis-polish4-20261113`（以 candidate i 为基座，fresh triage top-64 open × 420 s），watcher 自动下载、逐文件 merge、只在新分更低时覆盖暂存；预计 23:00 UTC 前完成，可赶上 00:01 提交。

### 2026-11-12 22:28 UTC contact polish round4：饱和

- `qingyu1232/sis-polish4-20261113`（以 candidate i 为基座，fresh triage top-64 open × 420 s）完成：47 题仅净 `1.9096e-6`；round3 是 `1.0792e-4`，边际下降两个数量级。
- 当前本地最佳 **22.17309952100155**（`outputs/submissions/candidate_1112j_20261112/`，独立双路径 1000 有效），已更新 `staged_latest`，00:01 UTC 自动提交使用该文件。
- 结论：contact polish 在当前前沿上已饱和，后续不再重复短周期 polish；除非公开前沿出现新供体改变接触图。

### 2026-11-12 23:34 UTC 提交前终检：0 胜，暂存不变

- 扫描 18:45 UTC 后 7 个新 kernel run + 数据集 + kobosh/jlevy HEAD：5 个可比较输出都是同一公开 union（总 L≈21461.6620），对暂存 **21461.5874** 逐题 0 胜；penguin069 20:10 与 grennwolf 22:08 ERROR 无输出。
- kobosh 18:47–19:51 三个 commit 只加日志/负结果（`free_band_ga`、`setpack367`、`setpack_lns`），`border-scan/merged.csv` blob 未变；jlevy HEAD 仍 `0ee1e762`。
- 暂存保持 `13efc5fd…` = **22.17309952100155**。
- 追加安全网：05:00 UTC 检查当日是否已有提交；若仍无，则提交暂存文件（`/tmp/fallback_submit.py`）。

### 2026-11-12 23:45 UTC DNS 故障与提交加固

- 23:45 终检时系统 DNS（223.5.5.5）无法解析 `api.kaggle.com`，而 8.8.8.8/1.1.1.1 正常（解析为 34.54.168.202）；storage.googleapis.com / www.kaggle.com 系统解析正常。
- 解决：新增 `/tmp/kaggle_resolve.py`，运行时用 8.8.8.8 解析 Kaggle 三个主机并在进程内 patch `socket.getaddrinfo`，再调用 Kaggle CLI；`/tmp/kaggle_r` 为包装器。已实测 `competitions submissions` 正常。
- 00:01 提交改用 `/tmp/auto_submit2.sh`：用包装器、从 00:00:40 开始每 60 s 重试最多 20 次；auto_frontier 与 fallback 也已切到包装器。旧脚本已 kill（PID 4141）。

### 2026-11-13 04:10 / 05:00 UTC 自动检查

- 04:10 自动前沿检查：JoeGun 仍是 2026-11-12 09:12 版本（未更新）；jazivxt 01:56 新输出逐题 **0 胜**。未提交。
- 05:00 fallback：检测到今日已有提交（58290129），按设计跳过。
- 下一次自动检查：11:30 / 15:30 UTC；JoeGun 若在上午更新，会自动 merge + 提交。

## 2026-11-15 公开前沿大合并（官方 22.1475078728）

11-14 晚间到 11-15，公开前沿整体前移（tomkodaj 22.1636、penguin atlas153/public152/boxed50、lucifer19 v50、oceanwang 研究仓库、jlevy/JoostdeWinter 新精确 witness）。本机只做下载、逐题 merge 与官方双路径认证，所有重计算在 Kaggle。

### 官方提交链（团队 ccjjllt）

| ref | 本地分 | 增量来源 |
| --- | ---: | --- |
| 58351261 | 22.1541906360 | tomkodaj 22.1636 逐题 + penguin atlas153/public152 + lucifer/kmmmvs/jazivxt/atlas |
| 58351930 | 22.1489959402 | + oceanwang 公开 packing（pell border-scan、lift_polish 等）+ jlevy n297 |
| 58352321 | 22.1476727305 | + 合法备选 442/447/485/530/577/743/798/997 |
| 58353688 | 22.1475723289 | + JoostdeWinter n332/n409 精确 witness + penguin boxed50 n918 |
| **58354659** | **22.1475078728** | + penguin GPU-glide n684/n916 + glide checkpoint n684/n918 |

净提升相对 58290129 的 22.1730995210：**0.0255916482**。全部提交在 text/float64 双路径 1000/1000 有效，官方分与本地逐位一致。

### 本轮公开源消化

- **oceanwang525-creator/squares-in-squares**（main `5cea61470b`、merge 分支 `0a1b187509`、codex/* 分支）：仓库内 217 个坐标 CSV + 1220 个 JSON 全量扫描，官方逐题认证后仅 8 题合法胜出（442/447/485/530/577/743/798/997，净 `1.3232e-3`）；merge 分支 `merged-22.15074317621.csv` 与 main 的候选对其时基线 0 胜；`mixed_irregular_seam`（367/791）为负结果。
- **penguin069 公开 union 资产**（1.19 GB、46 275 个 checkpoint + 3 层嵌套 zip + `.cert` 46 万行有理数证书）：全量流式扫描后仅 n=757 有 1.86e-10 的可认证改进；大 dL 候选都是搜索过程里的 `proposal`（不可行构造，穿透深度 0.44–1.00），999/1011 被官方 checker 判 overlap。
- **penguin069 GPU-glide 新 run**（18:22 UTC）：逐题合并得 n=684/916 两题（净 `6.4456e-5`），其 checkpoint zip 再补 n=684/918 各约 1.6e-9。
- **davidwarshawsky 研究归档**（766 MB、540 个含坐标 CSV）：对当前前沿 0 胜（多为 11-03 旧银行与 coordinate diff）。
- **CacinieP/sis-cloud-artifacts `sub_best.csv`**：0 胜。
- **22 个 11-11～11-14 公开 notebook 输出批量复扫**：0 胜（早已并入）。
- **16 个 penguin 新数据集输入（npz/zip）**：0 胜（4271 个数组全是 proposal）。
- **jlevy/squares**：main 仍 `fa980f8e70`，known-best 只新增 n297（已并入）；**JoostdeWinter/square-packing** 新增 n332/n409 精确 witness（已并入），n227/229/260 旧记录都劣于当前基线。

### 结论与下一步

公开可得坐标已被本轮基本吃干；剩余差距是逐题 2e-4 量级的精密修形（per-puzzle leaderboard 上 396 题落后，合计约 0.0988 分，其中约 90% 由 “Cats and boxes” 保持）。因此后续只在 Kaggle 跑计算：

- `ccjjllt/sis-ocean-melt-20261115`、`ccjjllt/sis-ocean-breadth-20261115`（ocean `swarm_masked_melt_breadth` / `swarm_inflation` 路线）已完成，输出逐题认证中。
- `ccjjllt/sis-ga-full-20261115`（2×T4，8 h，10 进程，top-50 gap + 127 个 ocean 备选种子）运行中。
- 新增 `ccjjllt/sis-glide-smoke/full`（GPU whole-packing glide：压缩到记录边长后用可微 SAT 罚函数 Adam+L-BFGS 松弛，shrunk-model + 缩放保证严格可行）——smoke 通过后跑满 7.4 h。

### 2026-11-15 00:01 UTC 公开前沿再前移：官方 22.1434306495（ref 58360040）

- `jazivxt/boxed-in-sub`（22:17 UTC 新输出）与 `penguin069/squares-boxed51-certified-current-union`（21:38 UTC）逐题合并得 **41 题**，净 `4.074217e-3`，本地 22.1434306496（双路径 1000/1000，merge 0 非法）。
- 最大单题：n=366 `+5.78e-4`、n=147 `+4.79e-4`、n=329 `+4.22e-4`、n=447 `+3.81e-4`、n=735 `+2.92e-4`、n=790 `+2.82e-4`、n=534 `+2.51e-4`、n=228 `+2.52e-4`、n=581 `+2.41e-4`。
- 官方回执：58360040 = **22.1434306495**，与本地逐位一致。相对 22.1730995210 累计 **0.0296688715**。
- 与 per-puzzle 纪录的差距降到 392 题 / 0.0947 分。
- CPU `swarm_new159` / `masked_melt` / `sametilt` / `mechwalk` 第二轮 9 个 kernel 共 2.52 h 全部 0 胜（365 差 5.8e-6、328 差 1.1e-5、491 差 1.2e-5），该 CPU 路线确认饱和。
- 新增自动化：`/tmp/frontier_watch.py` 每 10 min 扫 `kernels list --competition squares-in-squares` 的 lastRunTime，只下载变化的公开输出并逐题比对当前最佳，发现胜题即写 `/tmp/frontier_watch/wins.csv` 并退出。

### 2026-11-15 05:00 UTC 自研算力结果：GA 拿下 n=367，glide 全线 0 胜

- **GA run1**（`ccjjllt/sis-ga-full-20261115`，2×T4，8.04 h，10 worker）：n=367 `19.6923881554 → 19.6839313510`，单题 `+4.414e-4`，是当日自有算力最大收益；已并入最新公开 union 后提交 **ref 58368557**，本地 **22.141150574120026**（双路径 1000/1000）。
  - 该轮 10 个 worker 共用一个 claim 文件、全挤在 3 题上（visits 269 / finds 46，只有 1 题真正严格改进）；run2 已改为 per-worker claim tag。
- **glide**（`ccjjllt/sis-glide-full-20261115`，2×L4，4 worker，7.4 h）：对 396 道落后题做了 3 轮完整扫描（压缩 0→2e-3、含记录边长目标，Adam+L-BFGS 可微 SAT 罚函数，shrunk-model + 1/(1-2ε) 缩放保证严格可行），**0 胜**。结论：该可微松弛在当前 hyperstatic 前沿上无法把 1e-6～1e-3 的压缩量重新排成合法解，此方法停用。
- GPU 配额：04:59Z 已用 17.24 h / 剩 12.76 h（周配额，11-21 刷新）。GA run2 约需 6.5 h；余下额度用于 **GA run3**：10 worker 集中在 top-12 gap（367/803/328/908/791/365/902/861/969/963/842/491），硬预算 5 h，输出周期性落盘。
- 公开前沿哨兵持续运行（60×10 min，基线 22.1411505741）；今日提交额度剩 1 次，留给最终合并版。

### 2026-11-15 09:45 UTC GA run3：12 道最大 gap 集中攻坚，5 题胜出

- **GA run3**（`ccjjllt/sis-ga-full3-20261115`，2×T4，10 worker，4.69 GPU·h，12 题 × 95 min）：
  n=365 `+7.87e-5`、n=367 `+4.89e-5`、n=791 `+6.10e-5`、n=861 `+1.64e-4`、n=969 `+8.42e-5`，净 `4.3707e-4`，5/12 命中。
- 与公开前沿（alexchilton fault-line n=340）合并后本地 **22.140442950835556**，`squares score --mode both` 双路径 1000/1000 有效、同分（`/tmp/merge_g3`、`/tmp/merge_g3.score/report.json`）。
- 关键配置对比（同样 2×T4）：run1（50 题 × 18 min）1 胜 / 16 GPU·h；run3（12 题 × 95 min）5 胜 / 4.69 GPU·h。**集中预算到最大 gap 的题目，命中率高一个数量级**，后续 GPU 轮次沿用「top-12 gap × 95 min」。
- 检查了「把单题改进按 family 抬升」的可行性：GA3 的改进是全局重排（n=365 全部 365 个方块都移动，中位位移 1e-2），不是可平移的局部 gadget，family 抬升不成立。

### 2026-11-15 10:10 UTC 公开源消化自动化扩容

- 新增 `/tmp/frontier_watch_ds.py`：扫 datasets（`--sort-by updated`），只下载变更且 < 400 MB 的包，逐个 CSV 比当前最佳。首轮 6 个变更数据集（cshara current-best 22.2556、alexchilton starter-kit、prvsiyan/romywicaksono/mzishran 等）**0 胜**（仅 1e-10 噪声）。
- 新增 `/tmp/sweep_kernels.py`：一次性遍历全部 100 个公开 notebook（不只是 top-40 dateRun），补扫历史上从未下载过的输出。
- 新增 `/tmp/auto_pipeline.py`：新候选 → 逐题比较 → `squares merge` + 双路径 `squares score` 认证 → 更新 `/tmp/best_bank` → 按当日剩余额度自动提交（默认每天最多 4 次，最后 1 次留给 23:00Z 收口）。任何一次合并后若双路径不一致或出现非法题，会拒绝更新 bank。
- Kaggle 配额：GPU 27.4 h 已用、`isFrozen=True`（11-21 才刷新），本周剩余算力只能走 CPU/TPU（TPU 20 h 未用）。
- 逐题记录 gap 已降到 **392 题 / 0.0900**（top gap：803/328/908/791/902/861/969/963/367/842/491，8e-4 量级）。

### 2026-11-15 12:10 UTC GA run2 收口：0 胜，问题定位在 claim/cooldown

- **GA run2**（`ccjjllt/sis-ga-full2-20261115`，2×T4，7.54 h）：239 次 visit 全部落在 ns.txt 前 12 题，0 find、0 胜。`improved_groups.csv` 只有表头（sha256 `aaaf164b…`）。
- 根因：`VIS` 冷却表是 per-process 的，题目一旦结束就立刻重新可领，worker 反复吃列表头部；per-worker claim tag 只解决了并发抢占，没解决跨进程冷却。run3 同样只有 11/12 题被真正访问。
- 下一轮（GPU 配额 11-21 刷新后）改为**静态分区**：10 worker × `--part k/10`，每个 worker 独占 ns 切片（top-50 gap 每 worker 5 题），不再用动态 claim。
- 本周 GPU 配额用尽（剩余 0.93 h），11-21 前不再排 GPU 任务；期间只做公开前沿合并 + CPU/TPU 探测。

### 2026-11-15 12:10 UTC 官方提交 58383648 = 22.1404429508（rank 68）

- 提交文件 `/tmp/best_bank/submission.csv`（sha256 `4940bb43d3933fd8…`，26 578 910 B），官方回执 **22.1404429508**，与本地 text/float64 双路径逐位一致，1000/1000 有效。
- 相对上一官方最好 22.1411505741 提升 **7.0762e-4**；相对当日基准 22.1730995210 累计 **0.0326565702**。
- 排行榜：提交前 69 → 提交后 68（同期其他队伍也在推进：12:00Z 时榜上高于 22.14044 的有 60 队，12:25Z 增到 67 队）。
- 归档：`outputs/submissions/ga3_20261115/`（submission.csv、validation/report.json+per_puzzle.csv、merge_report、provenance.json，含三次 GA 运行时长与逐题来源）。

### 2026-11-15 12:30 UTC 夜间/次日自动化

- `/tmp/auto_pipeline.py`（每 10 min）：扫 kernel / dataset / 全量 kernel 输出三个下载池的新 CSV 与 NPZ，逐题比对 → 只把严格更快的完整组送进 `squares merge`（带 baseline report）→ 双路径 `squares score` 复核 → 通过才更新 `/tmp/best_bank`。
- `/tmp/final_slot.py --at 23:00 --at 00:05`：每日两个收口点，用 Kaggle submissions 列表里的最好 publicScore 做门槛，只有严格更好才提交；今天 23:00Z 若 bank 未变会自动跳过。
- `/tmp/frontier_watch.py`（kernel submission.csv）、`/tmp/frontier_watch_all.py`（kernel 全产物 csv/npz/zip）、`/tmp/frontier_watch_ds.py`（dataset 全量）三个哨兵并行；全部用 `daemonize.py` 双 fork + setsid 脱离进程组，避免被父 shell 回收。
- 全量历史 kernel 补扫（`/tmp/sweep_kernels.py`）：100 个公开 notebook 全部扫完，**0 胜**。
- TPU 探测（`ccjjllt/sis-tpu-probe`，TpuV5E8）：排队中。GPU 配额 11-21 前不可用，若 TPU 可用则作为本周唯一自研算力来源。

### 2026-11-15 12:55 UTC run4（静态分区）已在 Kaggle 上跑通 dry-run 验证

- 新 kernel `ccjjllt/sis-ga-full4-20261121`（2×L4，10 worker，top-24 gap × 90 min，硬预算 4.5 h）。
- 关键修复（针对 run2/run3 的 claim 饥饿）：`--part {k}/{NPROC}` 静态分区 + `--ns-file runs/ns_fixed.txt`；并把 top-24 目标**内嵌在 kernel 源码**（seed 数据集无法再 version，`datasets version/create` 均挂起）。
- 在 Kaggle 上用同一份代码跑 `ccjjllt/sis-ga-full4-dryrun`（CPU，dryrun 短路在 spawn GA 之前），输出证据：
  - baseline（seed 数据集）1000 组，score **22.141150574120047**；
  - 10 个 worker 分区互不重叠且覆盖全部 24 题：w0[803,901,974] w1[328,333,585] w2[908,747,982] w3[902,804,262] w4[791,962] w5[963,843] w6[842,748] w7[491,456] w8[367,795] w9[969,965]；
  - `disjoint: true`，`minutes_per_puzzle: 90.0`，`run_seconds: 16200`（=4.5 h 墙钟，10 worker 摊到 2 卡 ≈ 9 GPU·h）。
- 顺带发现并修掉：dry-run 首版只切出 3 个分区 —— `NPROC` 的 profile 分支没包含 `full4`，实跑会退化成 4 worker × 6 题（9 h）超预算；已改为 `if PROFILE == "full4": NPROC = 10` 并重新验证到 10 分区。
- CPU kernel 可用性已验证：`ccjjllt/sis-cpu-probe` COMPLETE，`/kaggle/input/datasets/ccjjllt/sis-ga-seed-20261115/pkg/ga.py` 可导入，`sq.core`/`sq.lp` 正常，submission.csv 500 501 行。GPU/TPU 仍 `isFrozen`（GPU 29.07/30 h，TPU 0/20 h 但冻结），11-21 00:00Z 刷新。
- 尝试把当前 bank 直接内嵌进 kernel 源码（zlib+base85 9.5 MB）以摆脱 seed 数据集：push 返回 400/BrokenPipe，说明源码体积超限；后续 GPU 轮次继续用 seed 数据集（只落后 bank 7.1e-4，逐题合并时会被严格比较挡住）。

### 2026-11-15 13:05 UTC CPU 算力试跑：随机 tie 的 contact-LP 还能再挤

- 新增 `ccjjllt/sis-cpu-lp-search`（CPU，11.5 h，top-24 gap，reclose(rounds=4, time_limit=3s, 随机 tie∈{0,1e-6..3e-3}) + 每 4 次一次“角度抖动 + grow=0.02 修复”）。
- 第 1 次尝试即命中 **n=333 `18.771335676 → 18.771333979`（+9.3e-8）**，说明在 LP 局部最优之间用 tie 随机化仍可缓慢下降；该结果远小于分数分辨率，但验证了 CPU 路径可用。
- 首版崩在 `emit()` 里引用局部 `STATS`（NameError），已改为全局并重推 v3；`/tmp/poll_cpu_lp.py` 会在完成时把 `improved_groups.csv` 放进 harvest 池，由 `auto_pipeline` 自动并入。
- 结论：CPU contact-LP 只能给出 1e-7 量级的抛光，无法替代 GPU 的结构搜索；本周主收益仍是公开前沿合并，11-21 后按 run4 静态分区跑 top-24。

### 2026-11-15 13:55 UTC 公开源已彻底吃干（全 100 个 notebook 的**全部**产物 0 胜）

- 新脚本 `/tmp/frontier_sweep_all.py`：不分 lastRunTime，遍历全部 100 个公开 notebook，按 `(pack|merge|best|current|union|submission|solution|final|donor|record|atlas|bank|portfolio|candidate).*\.(csv|npz|zip)` 下载并扫描（单文件 ≤150 MB、单 kernel ≤500 MB），zip 递归到 60 MB 内的 csv/npz。
- 结果：`iter 0: kernels=100 changed=100`，`wins.csv` 只有表头 —— **0 胜**。加上此前的 submission.csv 全量补扫（100/100，0 胜）与 dataset 全量（0 胜），可判定：当前 bank（22.1404429508）已严格支配所有公开可见坐标。
- 由此确认后续只有两条路：①公开前沿的新更新（哨兵每 10 min 捕获）；②自研算力（GPU 11-21 刷新；CPU 两条线在跑）。

### 2026-11-15 13:30 UTC 第二条 CPU 搜索线：block-LNS（换接触图，而不是只抛光）

- `ccjjllt/sis-cpu-block-lns`（CPU，11.4 h）：对 top-8 最大 gap（328/491/842/791/902/908/803/963）做「取随机中心最近 25–60 个方块 → 整块旋转 θ~N(0,1.6°) + 位置抖动 → `reclose(grow=0.03, L_ref=bank_L, rounds=4)` 修复并压缩」，每 3 次中插 1 次纯 LP 抛光；只导出严格优于 bank 的组。
- 与第一条线（`sis-cpu-lp-search`，top-24，随机 tie 抛光 + 角度抖动）并行运行，两条线各自跑满 11.5 h，poller 会在完成时把 `improved_groups.csv` 放进 harvest 池由 `auto_pipeline` 自动并入。
- 提交收口点从 3 个扩到 5 个（00:05 / 01:15 / 12:00 / 23:00 / 23:45 UTC），正好覆盖每日 5 次额度，且每次都要求严格优于榜上最好成绩才会提交。

### 2026-11-15 14:05 UTC CPU 算力波次化：把 392 道落后题全部排进队列

- 新增 `/tmp/cpu_wave/template.py` + `scheduler.py`：按 per-puzzle gap 排序的 392 题列表，每 24 题一个 wave（`ccjjllt/sis-cpu-wave-<idx>`），每个 wave 跑 11.3 h 的「随机 tie 的 contact-LP 抛光 + 每 5 次一次 2% 方块角度抖动 + grow=0.02 修复」，只导出严格优于 bank 的组。
- 调度器保持 2 个自有 wave 在跑，完成即取回 `improved_groups.csv` 到 harvest 池（`auto_pipeline` 会自动 merge + 双路径认证），然后推下一个 wave；按 16 个 wave 计算约 90 CPU·h，可在 11-21 GPU 刷新前覆盖全部 368 道未覆盖的落后题。
- 实测 Kaggle 允许 **4 个 CPU kernel 并发**（当前同时 RUNNING：`sis-cpu-lp-search`、`sis-cpu-block-lns`、`sis-cpu-wave-024`、`sis-cpu-wave-048`），所以 wave 不必等前两条线结束。
- 覆盖映射：top-8（block-LNS）、top-24（LP）、idx 24–47（wave-024）、idx 48–71（wave-048）；后续 wave 从 idx 72 起自动滚动。

### 2026-11-15 15:00 UTC 关键解锁：备用账号 GPU 配额 + dataset 上传修复

- 用户授权可用 `qingyu1232`、`zhuating` 的 GPU 配额（提交仍只用 ccjjllt）。实测配额：**qingyu1232 15.09/30 h 已用（14.9 h 可用）**，**zhuating 4.68/30 h 已用（25.3 h 可用）**，二者 `isFrozen=True` 但**仍可起 GPU 会话**（与 ccjjllt 相同现象）；ccjjllt 本轮已用 29.1 h。
- 发现 `datasets create/version` 挂起的真正原因：数据上传同样走 `www.googleapis.com`，与本机不可达的提交上传是同一个问题。用 `/tmp/kaggle_dataset_create.py`（把 `upload_complete` 的 URL 改写到 `storage.googleapis.com`）后，**27 MB 数据集 3 秒内创建成功**：
  - `qingyu1232/sis-ga-seed-qy-20261115`（首版只上了根文件）
  - `qingyu1232/sis-ga-bundle-qingyu1232`、`zhuating/sis-ga-bundle-zhuating`（bank 22.1404429508 + pkg/data/seeds 打包成 `bundle.zip`，Kaggle 自动解包为 `bundle/pkg/...`）
- 由此解决了一直卡住的「GPU kernel 拿不到当前 bank」问题：任何账号的 kernel 都能用 `submission.csv + bundle/` 的组合；kernel 里新增了 merged-view 兜底（pkg/data/seeds 软链 + 根目录 submission.csv）。
- 已按静态分区配置提交三个 GPU 轮次：
  - `ccjjllt/sis-ga-sprint-1`（本意 42 min / 4 题，因 profile 默认值未生效实际按 full3 跑：12 题 × 95 min，RUNNING）
  - `qingyu1232/sis-ga-run4-top24`（QUEUED）
  - `zhuating/sis-ga-run5-next24`（v2，24 题 × 90 min，QUEUED）
- 教训：改 profile 默认值时 `PROFILE = os.environ.get("SIS_PROFILE", "full3")` 这行在 full4 里**没有**被改成 "full4"，导致 sprint 跑成 full3；后续 push 前必须 grep 确认 profile 与 targets 分支。

### 2026-11-15 15:20 UTC jazivxt 大更新：bank 22.140442951 → **22.140069837**（+3.731e-4）

- 15:03Z 下载到 jazivxt/boxed-in-sub 的新 `submission.csv`（43.6 MB），`auto_pipeline` 逐题合并：**59 题**改进，净 **3.731137e-4**，双路径 `squares score` 复核 1000/1000 合法、text=float64。
- 收益集中在两题：**n=228 `15.600801735 → 15.596043117`（+3.151e-4）**、**n=803 `28.817265876 → 28.815696680`（+5.538e-5）**，其余 57 题各 1e-7～1e-6。
- 顺手修掉两类管线问题：
  - `avazaku/squares-contact-lp-cusp-bounds-465-998` 的 `frontier_v18_packings.csv` 缺少 `id` 列，`squares merge` 直接报错拒收；`auto_pipeline` 新增 `_normalize_candidate()`（自动补 `id` 后再 merge）。手工补列后该文件另贡献 4 题 **+1.106e-7**（bank 22.140069837 → 22.140069837，见 report）。
  - 哨兵基线改为每次从 `/tmp/best_bank` 重新加载，避免用旧基线反复报“已合并过的胜题”。
- 当前 bank：**22.140069837165804**（text/float64 一致，1000/1000）→ 今日 00:05Z 收口点提交，预期官方 ~22.14007。

### 2026-11-15 16:27 UTC 官方回执 58392028 = **22.1400698371**（rank 71）

- 提交 `/tmp/best_bank/submission.csv`（jazivxt 15:03Z 合并 59 题 +3.731e-4，avazaku 4 题 +1.106e-7），官方分 **22.1400698371**，与本地 22.140069837165804 前 10 位一致；归档 `outputs/submissions/public_merge_20261115_b/`。
- 排名从 68 掉到 **71**：同期约 10 支队伍在 4 小时内推进超过 3.7e-4，说明竞争在加速（不是我们退步）。
- 另一个实测结论：**每日提交上限不是 5**——今天第 6 次提交（58392028）成功。已把收口点从 5 个扩到 9 个（00:05/03/06/09/12/15/18/21/23:45Z），以提高捕获前沿更新的频率。

### 2026-11-15 16:45 UTC 双 GPU 槽调度 + 一个会让作业必挂的 bug

- `gpu_wave/scheduler.py` 重写为「每个账号 2 个 GPU 会话」的调度器（qingyu1232/zhuating 各 2 槽，共 4 个并发 campaign），队列按 gap 段 48–192 + top-10 深度 180 min 排序。
- 实测账号槽位：`zhuating` 可同时挂 `sis-ga-run5-next24` + `sis-gpu-a`；`qingyu1232` 的第二槽被该账号另一个 kernel（`qcc-assemble-28059`）占用，push 会报 `Maximum batch GPU session count of 2 reached`，调度器每 10 min 重试。
- 关键 bug：调度器从 `/tmp/ga_kernel_full4` 造作业，而该目录**没有** bundle 版 `find_input()` 补丁，导致 `zhuating/sis-gpu-a` 直接 `FileNotFoundError: .../bundle/submission.csv`。已把 merged-view 逻辑写回 BASE kernel 并重推；教训：任何新作业模板必须先跑一次 dry-run 或看 logs。
- 当前 GPU：`ccjjllt/sis-ga-sprint-1`(RUNNING)、`qingyu1232/sis-ga-run4-top24`(RUNNING)、`zhuating/sis-ga-run5-next24`(RUNNING)、`zhuating/sis-gpu-a`(QUEUED)。

### 2026-11-15 18:20 UTC 官方 58395980 = **22.1400693231**；修掉一个会挡住所有后续提交的网关 bug

- penguin `multicloud401` n=401/550（+5.127e-7）与 n=868 抛光（+1.334e-9）合并后 bank 22.14006932313377，提交回执 **22.1400693231**（本地/官方前 10 位一致）。
- 关键 bug：`final_slot.py` 的额度闸门写死 `used < 5`，但实测每日上限 >5（今天已提交 6 次），18:00Z 收口点因此判定 "nothing to do" 而跳过提交。已改为 `used < 9` 并重推；同时手工补交了这版。
- GPU 账期实测：ccjjllt 31.54 h（已超 30 h 上限仍在跑）、qingyu1232 15.80 h、zhuating 5.57 h —— 三个账号的 RUNNING 会话确实在消耗配额，GPU 作业没有卡死。
- 新增 `/tmp/verify_gpu_run.py`：从 `run_report.json` 打印 profile / nproc / targets / 分区覆盖 / visit_count / win_count / net_gain_score / 缺失目标；对 run1 的报告回放确认它能正确暴露「50 题只访问了 3 题」的旧 claim bug。
- 逐题 gap 分布（相对 per-puzzle 纪录，合计 0.0892 / 391 题）：≤1e-6 仅 10 题（4.1e-6）、≤1e-5 26 题（8.2e-5）、≤1e-4 103 题（4.4e-3）；**0.085 的差距集中在 288 道 gap >1e-4 的题上**，只能靠 GPU 结构搜索，抛光无济于事。

### 2026-11-15 19:17 UTC 静态分区修复**验证通过**（sprint 报告）

`ccjjllt/sis-ga-sprint-1` COMPLETE（实跑 full3 profile：12 题 × 95 min，4.69 h，10 worker）。`/tmp/verify_gpu_run.py` 读 `run_report.json` 的输出：

```
targets (12): [367, 803, 328, 908, 791, 365, 902, 861, 969, 963, 842, 491]
partitions seen: 10   {'0/10': [367, 842], '1/10': [491, 803], '2/10': [328], '3/10': [908],
                       '4/10': [791], '5/10': [365], '6/10': [902], '7/10': [861],
                       '8/10': [969], '9/10': [963]}
visit_count 30  visit_finds 22  win_count 4  net_gain_score 3.141256e-04
targets covered: 12/12  missing []
```

对照旧 claim 逻辑的 run1（50 题只访问 3 题、1 胜），**静态分区确实把 12 道目标全部覆盖到了**。

4 个胜题（相对 seed 22.1411505741）：n=365 +7.86e-5、n=791 +6.78e-5、n=861 +8.40e-5、n=969 +8.38e-5。其中 3 题已被 GA3 的更好结果覆盖，只有 **n=791** 对当前 bank 有效（`28.625920780 → 28.625730292`）。

`auto_pipeline` 在 19:01Z 自动合并：

```
candidate improved_groups.csv (ccjjllt_sprint): 1 faster groups
merged 2 puzzles [401, 791] gain 6.800841e-06
new bank score 22.140062522049
```

bank 现为 **22.140062522048712**（text/float64 一致、1000/1000），21:00Z 收口点提交。

### 2026-11-15 21:19 UTC 大跳：官方 **58401147 = 22.1342325793**（rank 71 → 61，+5.837e-3）

- 21:00Z 收口点自动提交，官方分与本地 22.134232579354094 逐位一致；归档 `outputs/submissions/boxed_v56_20261115/`（sha `ae25e4283ea3fd9b…`，500 500 行，双路径 1000/1000）。
- 主要来源不是自研 GA，而是此前漏掉的公开 donor：`avazaku/squares-contact-lp-cusp-bounds-465-998` 里的 **`boxed_v56_submission.csv`（43.7 MB）**，逐题合并 **112 题、净 +5.377971e-3**（19:55Z 由 `auto_pipeline` 自动合并）。同目录的 `boxed_v55`、`contact_v19`、`frontier_v19` 等 20+ 个文件均已扫描，只有它和 `squarecraft_n868.csv` 有胜题。
- 三个静态分区 GPU 轮次全部完成并验证：

| 轮次 | targets | 覆盖 | partitions | visits | win_count | net_gain |
|---|---:|---:|---:|---:|---:|---:|
| `ccjjllt/sis-ga-sprint-1`（full3 12 题） | 12 | **12/12** | 10 | 30 | 4 | 3.141e-4 |
| `qingyu1232/sis-ga-run4-top24`（top-24） | 24 | 20/24 | 10 | 30 | 2 | 1.007e-5 |
| `zhuating/sis-ga-run5-next24`（gap 24–47） | 24 | 20/24 | 10 | 30 | 5 | 3.749e-4 |

  - **静态分区修复确认有效**：三份 `run_report.json` 都出现 10 个不同 `--part k/10` 分区，sprint 更是把 12 道目标全部覆盖（旧 claim 逻辑下 50 题只访问 3 题）。
  - run4/run5 各缺 4 题（262/585/974/982 与 860/919/975/981）：24 题 / 10 worker / 90 min 时，两个分到 3 题的 worker 会把第 3 题留到超时之后。下一轮把 `--part` 的分母改成 12（或把每题预算降到 75 min）即可全覆盖。
- 对 bank 的实际贡献：run5 的 492/861/862/921（+3.438e-4）、run4 的 969（+1.007e-5）、sprint 的 791（+6.8e-6），合计约 3.6e-4；其余胜题被更强的公开 donor 覆盖。

### 2026-11-15 21:30 UTC 分区数 10 → 12：24 题全覆盖修复（Kaggle dry-run 验证）

- 根因：24 题 / 10 worker 时有两个 worker 分到 3 题，90 min/题 × 3 = 270 min 正好撞上 4.5 h 硬预算，第三题拿不到时间（run4/run5 各缺 4 题）。
- 改法：`if PROFILE == "full4": NPROC = 12`（24 题 → 每 worker 恰好 2 题 × 90 min = 3 h，留 1.5 h 余量；10 题深度轮 → 每 worker 1 题 × 180 min）。
- Kaggle 真机 dry-run（`zhuating/sis-ga-part12-dryrun`，COMPLETE）：
  ```
  nproc 12 | targets 24 | disjoint+coverage True | minutes/puzzle 90.0 | run_seconds 16200
  part 0 [803,747] 1 [328,804] 2 [908,962] 3 [902,843] 4 [791,748] 5 [963,456]
  part 6 [842,795] 7 [491,965] 8 [367,974] 9 [969,585] 10 [901,982] 11 [333,262]
  ```
- 注意：已在跑的 `sis-gpu-a/b/c/e` 仍是 NPROC=10（推送早于补丁），队列里剩余 6 个 campaign 会用 NPROC=12。
- 顺带发现 Kaggle 每个账号还有 **5 个并发 CPU kernel** 的限制（ccjjllt 的 5 条 CPU 线正好占满，导致 dry-run 只能换 zhuating 账号跑）。

### 2026-11-15 23:47 UTC 官方 58405258 = **22.1338204867**（静态分区首个真实胜题轮次）

- `zhuating/sis-gpu-a`（gap 48–71，full4，NPROC=10，4.52 h）验证：24 题、20 访问、10 分区、visit 30、**win_count 4、net 4.2157e-4**；胜题 n=591 +1.278e-4、n=749 +6.63e-5、n=924 +2.63e-5、n=984 +2.012e-4。合并 3 题 +3.952e-4 进 bank。
- `qingyu1232/sis-gpu-c`（top-10 深度 180 min，5.53 h）：10/10 全覆盖、10 分区、visit 20、win 2（791 +3.74e-6、969 +6.44e-6），但被公开 donor 的更好值覆盖，对 bank 无贡献。
- 官方 **22.1338204867**，与本地 22.133820486730905 逐位一致；归档 `outputs/submissions/gpu_a_20261115/`。
- 排名反而 61 → 73：2.5 小时内 12 支队伍超过我们（公开前沿在这一小时里连续放出大 donor，`avazaku`/`alexchilton` 都在更新），说明**捕获速度**比单次收益更决定名次。
- 修掉调度器两个 bug：①每账号 GPU 余额 <3 h 时不再派活（qingyu1232 只剩 2.76 h 时仍在排 4.5 h 作业）；②收口点 fire 后 `sleep(3600)` 会把 45 分钟后的下一个 slot（23:00→23:45）整段跳过，已改为 120 s。
- `frontier_watch_ds.py` 也修了一个隐蔽 bug：baseline 只在启动时加载一次，导致 alexchilton 22:41Z 的更新被误报为「110 胜 / 5.385e-3」（实际那些改进早已并入），现在每轮重新加载。

### 2026-11-16 00:55 UTC CPU 两条线的最终结论：都是死路

- `ccjjllt/sis-cpu-lp-search`（11.5 h，top-24，8404 次尝试/题）：只拿到 n=333 +9.59e-8、n=747 +2.16e-8，合并后 bank 仅 **+2.16e-8**（n=333 已被公开 donor 覆盖）。
- `ccjjllt/sis-cpu-block-lns`（11.4 h，top-8，「整块旋转 + LP 修复」）：`improved_groups.csv` 只有表头，**0 胜**。
- 结论：在当前 hyperstatic 前沿上，CPU 端无论纯 LP 抛光还是块级结构扰动都无法产出 1e-6 以上改进；后续 CPU 不再投入（ccjjllt 的 5 个 CPU 槽位可留给别用）。
- 公开前沿此刻也安静：malyshev atlas 00:03Z 的新版只发代码/图表（无 submission.csv），`asteriospanoras`、`areebbb` 同样只有代码产物；当前公开 union 最好 22.1367，仍落后我们 22.1338。
- GPU 队列：qingyu1232 余额仅 0.72 h（`sis-gpu-e` 将被配额终止），zhuating 剩 10.5 h；已给 zhuating 追加 6 个 campaign（gap 192–240 段、top-24 复跑、48–71 复跑）。

### 2026-11-16 01:00 UTC 队列重心从 top 段移到中段（有数据支撑）

对各轮对 bank 的**实际**净贡献（不是对各自 seed 的贡献）：

| 轮次 | 目标段 | 对 bank 净贡献 |
|---|---|---:|
| `zhuating/sis-gpu-a` | gap 48–71 | **+3.952e-4**（591/749/984） |
| `qingyu1232/sis-gpu-c` | top-10 深度 180 min | ~0（791/969 被 avazaku donor 覆盖） |
| `qingyu1232/sis-ga-run4-top24` | top-24 | ~0（同上） |
| `ccjjllt/sis-ga-sprint-1` | top-12 | +6.8e-6（仅 791） |

原因很清楚：top 段的题同时被所有队伍和公开 donor 反复打磨，我们的 GA 很难再挤出东西；而 48–240 名的题仍是「有 gap 但少人碰」的区域。因此把队列里的 `sis-gpu-m`（top-24 复跑）换成 gap 240–264，并追加 264–288；zhuating 剩余 10.5 h 的 7 个 campaign 全部落在 144–288 段与 48–71 复跑。

### 2026-11-16 01:05 UTC 官方 22.1338204867 之后的小额抛光

- CPU LP 的 n=747 +2.16e-8 已并入，bank 22.133820465110077；这个量级对排名无意义，只为记录。
- `qingyu1232` GPU 余额 0.72 h，`sis-gpu-e` 仍在跑，预计被配额终止；其 partial 输出会在状态变 ERROR 后尝试取回。

### 2026-11-16 01:52 UTC 官方 58409967 = **22.1333334050**（gpu-b 复跑拿到 +4.87e-4）

- `zhuating/sis-gpu-b`（gap 24–47 **复跑**，4.52 h，静态分区）：visit 30、**win_count 5、net 9.3359e-4**：
  n=492 +1.227e-4、**n=545 +4.862e-4**、n=861 +6.90e-6、n=862 +1.549e-4、n=911 +1.628e-4。
  合并时 492/862 已被公开 donor 覆盖，最终计入 **545 + 911 = +4.8706e-4**。
- `qingyu1232/sis-gpu-e`（gap 72–95，4.52 h）：1 胜 n=587 +6.22e-5，但 bank 已有更好值，未计入。
- 官方 **22.1333334050**（本地 22.133333405072793 逐位一致），归档 `outputs/submissions/gpu_b_20261116/`（含两份 run_report）。
- 重要经验：**同一段复跑仍有价值**——gpu-b 是 run5 的完全重复目标段，却把 n=545 从 23.8252 打到 23.8138（+4.86e-4），因为 GA 每次随机重启落在不同的局部盆地里。后续队列保留 48–71 复跑（gpu-n）就是这个道理。

### 2026-11-16 03:10 UTC 官方 58412458 = 22.1333332097；按「band 产出率」重排 GPU 队列

逐 band 的 gap 存量（相对 per-puzzle 纪录，总计 0.0853 / 389 题）：

| 名次段 | 题数 | gap 合计 |
|---|---:|---:|
| 0–23 | 24 | 0.01481 |
| 24–47 | 24 | 0.01117 |
| 48–71 | 24 | 0.00929 |
| 72–95 | 24 | 0.00805 |
| 96–143 | 48 | 0.01323 |
| 144–191 | 48 | 0.01062 |
| 192–239 | 48 | 0.00819 |
| 240–287 | 48 | 0.00573 |
| 288–335 | 48 | 0.00333 |
| 336–391 | 53 | 0.00085 |

结合实测产出率（24–47 复跑 +4.87e-4、48–71 首跑 +3.95e-4、top-10 深度 ~0），队列重排为 **24–47 → 72–95 → 96–119 → 144–191 → 192–239 → 48–71 复跑 → 240–287**，把「gap 大且被反复验证可挖」的段落排到最前。zhuating 剩余配额只够再跑约 3 个 campaign，所以顺序即优先级。

- 03:00Z 收口点自动提交 **58412458 = 22.1333332097**（比 22.1333334050 再好 1.95e-7，来自一笔小额公开合并）。
- `sis-gpu-d`（10 题深度 180 min，NPROC=12）与 `sis-gpu-f`（gap 144–167，24 题，NPROC=12）仍在跑；后者是第一个能验证 **24/24 覆盖** 的真实轮次，预计 06:00Z 落盘。

### 2026-11-16 05:50 UTC **NPROC=12 真人验证 24/24**；官方 58418244 = 22.1327829081

`zhuating/sis-gpu-f`（gap 144–167，24 题，NPROC=12，4.52 h）的 `run_report.json`：

```
nproc 12 | partitions seen: 12  ('0/12' … '11/12')
distinct visited: 24        | targets covered: 24/24   missing []
visit_count 36  visit_finds 40  win_count 6  net_gain_score 3.500132e-04
  WIN n=547 +4.555e-05  n=644 +4.267e-05  n=645 +8.287e-05
      n=812 +1.253e-04  n=815 +1.095e-05  n=968 +4.269e-05
```

**这是第一次在真实 GPU 轮次里确认 12 分区 = 24/24 全覆盖**（此前 gpu-a/b/e 都是 NPROC=10 → 20/24）。同批 `sis-gpu-d`（10 题深度，NPROC=12）也是 **10/10** 覆盖、2 胜（n=333 +3.094e-5、n=795 +2.402e-5）。

- 官方回执：`58417748 = 22.1332782582`（gpu-d 两题），随后 `58418244 = 22.1327829081`（alexchilton `best_current.csv` 05:38Z 更新：92 题 +4.9535e-4，叠加 gpu-f 的胜题）。
- 归档：`outputs/submissions/gpu_d_20261116/`、`outputs/submissions/gpu_f_20261116/`。
- **排名压力**：分数一路降（22.1731 → 22.1328，累计 +0.0403），名次却 69 → 61 → 73 → 78。6 小时里 17 支队伍超过我们——公开前沿的 donor 让所有人同时跳。对策已落地：三个哨兵的轮询从 600/900 s 压到 **240/300 s**，`auto_pipeline` 从 600 s 压到 **300 s**，把「发现→合并→提交」的延迟减半。

## 2026-11-16 停止方向清理（已删除约 18.3 GiB）

按“停止的研究只留本页简述与停止原因，不保留文档、脚本和中间产物”的约定，本轮清理了 2026-11-13 之后新判死的研究线、旧 pilot 管线、被取代的提交归档，以及 `/tmp` 中一次性扫描与中间合并。完整路径、大小和保留证据见[清理记录](../data/references/cleanup_20261116.json)；正式提交身份表见[official_submissions_20261116.json](../data/references/official_submissions_20261116.json)；GPU 轮次证据见[run_reports_20261116](../data/references/run_reports_20261116/)。

| 已停止路线 | 最后结论（停止原因） | 已删除 |
| --- | --- | --- |
| CPU contact-LP 抛光（`sis-cpu-lp-search`） | 11.5 h、8404 次尝试/题；仅 n=333 `+9.59e-8`、n=747 `+2.16e-8`，合并后 `+2.16e-8`；成熟布局接触图超静定 | `/tmp/cpu_lp_search/`、`poll_cpu_lp.py`、Kaggle kernel |
| CPU block-LNS（`sis-cpu-block-lns`） | 11.4 h、top-8 整块旋转 + LP 修复；`improved_groups.csv` 只有表头，**0 胜** | `/tmp/cpu_lns/`、Kaggle kernel |
| CPU wave 轮转（`sis-cpu-wave-024/048/072`） | 392 道落后题分段轮转，产出 1e-7 量级；不改变任何名次 | `/tmp/cpu_wave/` 调度器与模板、3 个 Kaggle kernel、dl 目录 |
| TPU 探测 | 用户明确不使用 TPU（排队过慢）；probe 长期 QUEUED，无结果 | `ccjjllt/sis-tpu-probe`、`/tmp/tpu_probe/` 与 probe 目录 |
| 2026-11-07~13 旧 CPU 生成 + GPU 松弛 pilot 主线 | 已被 2026-11-15 起的 Kaggle 静态分区 GA 与公开前沿合并取代；n=642 链、pilot08/09 等结论已并入本页 | `scripts/experiments/`、`scripts/kaggle/`、`src/squares/search/`、`third_party/`、`outputs/experiments/`、`outputs/merged/`、`data/public/`（0.94 GiB） |
| 公开源一次性扫描与外部库下载 | 结论为 0 胜或已并入 bank；原始下载与解包不再承担复现作用 | `/tmp` 下 40 个扫描目录 + 10 个大文件（11.4 GiB）；三份候选池中已处理文件 1263 个（4.57 GiB） |
| 被取代的正式/候选提交归档 | 只保留当前最佳 `gpu_f_20261116`；其余 ref 的官方分、SHA-256、行数已写入身份表 | `outputs/submissions/` 下 27 个目录（690.86 MiB） |
| 中间合并与陈旧运行目录 | bank 是唯一权威；run_report 已抽存；seed bundle 将在 2026-11-21 按当前 bank 重建 | `/tmp/merge_*`（保留 `best_merge`）、`cpu_merge_*`、`qy_run4`、`zh_run5`、`ga_sprint`、`ga_full_out`、`ga_prev_out`、`seed_bundle*`、`bank_test`、`launch_run4.py` 等（1.21 GiB） |

保留：当前官方最佳归档 `outputs/submissions/gpu_f_20261116/`（ref 58418244，22.1327829081，SHA-256 `3465e359…`，text/float64 1000/1000）；`src/squares/` 的评分、合并、提交校验与官方 v20 评分器；`data/references/` 的来源、榜单快照、历史提交身份表和 GPU run_report；`outputs/scores/` 的历史公共对照；以及正在运行的公开前沿合并管线（`/tmp/best_bank`、三个哨兵、`auto_pipeline.py`、`final_slot.py`）和 2026-11-21 恢复 GPU 所需的 `ga_kernel_full4`/`ga_dataset`/`gpu_wave`。

验证：`uv run squares inspect` 对当前 bank 报 500,500 行 / 1000 题 / 0 缺失；`squares score --max-n 10 --mode both` 两条路径均 10/10 有效；`squares merge` 全量复核 bank 仍为 `22.132782908131748`（未因删除搜索模块而改变）。磁盘：仓库 1.6 GiB → 671 MiB，`outputs/` 878 MiB → 29 MiB，`/tmp` 约 20 GiB → 2.2 GiB，可用空间 505 GiB → 523 GiB。Kaggle 侧同时删除 6 个已停止研究的 kernel。

## 2026-11-17 CPU 研究战役（当前状态，覆盖上节）

上节之后公开前沿继续前移，但自研算力仍受 GPU 配额限制。2026-11-17 按“Kaggle CPU only、本机不做优化”的约束重开一轮，目标是近平方 `n=K²+D` 族和公开 donor 收割。

### 官方提交链

| ref | 官方分（public LB） | 来源 |
| --- | ---: | --- |
| 58418244 | 22.1327829081 | 上节基线（alexchilton best_current + gpu-f） |
| 58458362 | 22.1315964706 | 06:00Z 收口；含 jazivxt boxed-in-sub 等公开合并 |
| 58463326 | 22.1312621382 | 09:00Z 收口；60 s fault-DP gadget quench 5 题 |
| 58467863 | 22.1310140483 | 12:00Z 收口；penguin n=448 + hop 333/747/803 + n=367 |
| 58472778 | 22.1308572457 | 15:00Z 收口；asteriospanoras n=330/448/643 +1.568e-4 |
| **58473557** | **22.1296844959（PENDING，本地）** | 16:05Z 额外收口；rosswade jammed-squares donor 72 题 +1.17275e-3 |

本地 bank：**22.12968449588547**，SHA-256 `e9ca9ee5…`，text/float64 均 1000/1000 有效；归档 `outputs/submissions/bank_20261117/`。相对 58418244 累计下降 **3.09841e-3**；公开榜约 **82 / 2184**。

### 已验证的增量（全部 dual-route 认证）

| 来源 | 题数 | 净收益 | 关键题 |
| --- | ---: | ---: | --- |
| alexchilton 60 s gadget quench（fault-DP keys） | 5 | **2.9198e-4** | 641 +1.227e-4、803 +9.92e-5、789 +4.67e-5、861 +1.55e-5、693 +7.85e-6 |
| penguin069 public neural recovery union | 2 | **2.2806e-4** | n=448 ΔL=4.827e-3 |
| evand `packer hop` 2–10 min 链 | 4 | 2.00e-5 | 367 +1.04e-5；333 +5.98e-6；803 +3.59e-6；747 +2.6e-8 |
| jazivxt boxed-in-sub 06:32Z | 38 | 4.235e-5 | 已进入 58458362 基线 |
| asteriospanoras public best 13:11Z | 3 | 1.5680e-4 | n=330/448/643 |
| **rosswade jammed-squares + fast LP 15:01Z** | **72** | **1.17275e-3** | 330/448/643/971/910/911/... 大批题 |

### 关键结构发现

- 从 bank 的 fault-DP 提取出 D=1 族的绑定 gadget 为 **(w,h,dm)=(24,25,1)**、f=0.520815（覆盖 n=626/677/730/785/842/901/962）；D=2 族为 **(9,9,1)**、f=0.535534（覆盖 902/963/843/786/...）。记录族的 f 分别低到 0.502153 / 0.514079。
- 但目标侧可行性搜索失败：61 个 record-side `packer hop` 单元全部无可行解（0/61）；n=82 的 9×9+1 目标侧 246 条链 0 胜；n=842 的 82 条 5–12 min 链 0 胜。结论：记录族的 f 不是 bank 邻近盆地的局部压缩，需要新构型/新 gadget，而不是更长的 hop。
- 24×25+1 与邻近 (23,25)/(24,24)/(25,25)/(24,26) 的 target-f gadget 搜索、以及硬约束 fault-DP 复算仍在 Kaggle CPU 上运行；这是当前唯一有潜力一次性带来 1e-3 量级的方向。
- 公开前沿仍是最稳定的增量来源；penguin 的 n=448 说明单题大 donor 仍会出现，哨兵不能停。

### 当前负面结果（避免重复）

- X3 record-side `packer hop`：0/61 单元可行；`harden` momentum 首版未跑通（jobs 秒退，需修 CLI/格式）。
- n=82 9×9+1 target hop：0/246；n=842 target hop：0/82。
- 第二波 12 min hop（20 题×2 seeds）全部无新胜（kernel `sis-hop-wave2-20261117`）。
- 公开源本轮：kmmmvs 08:27Z、nilanjan 07:50Z、alexchilton 09:10Z、amir 最新 run 均 0 胜或仍在跑；penguin 07:32Z 仅 n=448。

### 下一步

- 收割 24×25+1 / 邻近 key 的 target-f gadget 结果；若有 f<0.52 的 gadget，立刻用 fault-DP 复算 D=1 列，并在 15:00/18:00Z 提交。
- 继续公开前沿哨兵；2026-11-21 00:00Z GPU 配额刷新后，按静态分区 GA 队列（NPROC=12）继续中段 band，但不再对 top-10 做深度 hop。
- 记录身份与新提交证据：`data/references/official_submissions_20261117.json`；当前 bank 归档 `outputs/submissions/bank_20261117/`。

## 2026-11-18 00:15Z 前沿合并与五路并行研究

上节之后公开前沿又前移一步：rosswade `jammed-squares-engine-packings` 的
`engine_improvements.csv` 一次性改进 **52 题、净收益 +1.82137e-4**（76 个几何组复核，
其中 52 组严格更优；最大 n=542 +2.90e-5、n=548 +2.09e-5、n=812 +1.96e-5）。
该 donor 的 77 题已全部吸收，复查对当前 bank 剩余收益为 0。

bank 更新为 **22.129502357094957**，SHA-256
`6f6e9da8e3c795914d89f1e79d777233e256cce4a5600ab32d0e70e8f55e0c40`，
text/float64 均 1000/1000 有效；归档 `outputs/submissions/bank_20261117/`（provenance 8 条合并记录）。
官方最佳仍为 58473557（22.1296844958，COMPLETE），下一档 18:00Z 提交将带上这 1.82e-4。

### 本轮五路并行 subagent（全部 Kaggle CPU，`enable_gpu: false`）

| 轨道 | 目标 | 关键事实 |
| --- | --- | --- |
| harvest | Kaggle notebook 输出 + 数据集 + discussion + GitHub | 前几次单 donor 最大 +1.17e-3，故设为常驻收割 |
| gadget | `n=K²+D` 角 gadget（D=1..12） | D=1 差 4.9e-3、D=2 差 3.6e-3；bank 绑定 (24,25,1) f=0.520815，记录 0.502153 |
| templates | grid+bands 精确模板族 | 占剩余差距 79.3%；闭式几何构造，不做局部搜索 |
| cdb | 45° 中心菱形块族 | 占 12.6%；`n(u,v,L)=uv+4·N(T)`，`T=L−(u+v)/(2√2)` |
| engine | 移植 rosswade 公开 notebook 的 contact-force + fast-LP 引擎 | 其公开输出只覆盖 77 题；我们把它跑遍 389 道落后题 |

### 结构结论（本轮新增，已验证）

- `lostdecimal27/squares-in-squares-bank`（2026-10-29，含 1000 题坐标的 submission.csv）
  对当前 bank **0 胜**，历史记录源已被完全吸收；per-puzzle 记录表只有 L 没有坐标，
  因此记录族布局无法直接取得，只能重建。
- 单角 gadget 组合对 bank 已封闭（全量 K×K' × w×h × dm≤80 扫描仅 2.6e-12 量级）。
  剩余增益必须来自**新的 packings**，而非重组合。
- `D=1` 列的记录 f 在 k=29,30,31 完全相同，说明记录侧存在一个 `max(w,h)≤29`
  的 gadget；等价于存在 842 个单位正方形、边长 < 29.5021527 的 packing。

### 官方提交链更新（2026-11-17 17:31Z）

`58477184` **22.1294951718 COMPLETE**，与本地 dual-route 预测逐位一致
（预测 22.1294951718），说明本地 v20 评分器与实际榜单完全等价。至今链条：

| ref | 官方分 |
| --- | ---: |
| 58418244 | 22.1327829081 |
| 58458362 | 22.1315964706 |
| 58463326 | 22.1312621382 |
| 58467863 | 22.1310140483 |
| 58472778 | 22.1308572457 |
| 58473557 | 22.1296844958 |
| **58477184** | **22.1294951718** |

相对 58418244 累计 **−3.28774e-3**；相对本轮 03:00Z 起点 22.1318435850 累计 **−2.34841e-3**。

### 本轮新增结构结论（供后续轮次直接使用）

- **单角 gadget 组合只在 D=1,2,3,5,6 列成立**（平台起点 k0=25,17,25,30,30）；
  D≥7 的银行布局 `f(D,k)` 随 k 严格下降，说明那些列是**按 k 缩放的带状构型**，
  不是固定 gadget。要对 D≥7 的列做增益，必须找到 k-缩放的族，而不是更大的 gadget。
- 拟合 `f(D,k) = a(D) + b/k`：记录侧的渐近截距 a 系统性低于银行侧，
  最大差在 D=2（0.5355 vs 0.4859）、D=1（0.4956 vs 0.4509）、D=20（0.5103 vs 0.4763）、
  D=19（0.5058 vs 0.4729）。这指向记录侧的带构型在 k→∞ 时更紧，
  即**角度/分带参数随 k 连续变化**，而非离散换 gadget。
- 记录布局的角度缺陷 44.79°–45.33°（我方 n=328 为 44.16°–44.52°）说明
  双方都是**数值抛光位置**；纯闭式模板扫描只能复现银行现状，不能超越。

### 2026-11-18 公开源穷尽核验（全部 0 胜）

| 源 | 状态 | 结果 |
| --- | --- | --- |
| `asteriospanoras/squares-in-squares-best` 17:59Z | 44 MB，1000 题坐标 | 对 bank **0 胜** |
| `rosswade/jammed-squares-engine-packings` 16:11Z | 77 题 engine_improvements | 对 bank **0 胜**（8 小时前那版已全吸收） |
| `avazaku/squares-contact-lp-cusp-bounds-465-998` | N465/N998/335/498/591 整包坐标 | **全部比 bank 差**（N465 −5.3e-5、N998 −1.0e-3、591 −7.8e-3） |
| `lostdecimal27/squares-in-squares-bank` | 10-29 全量坐标 | 0 胜（会话早期已核验） |
| `alexchilton` starter kit `best_current.csv` 17:06Z | 4 题 | 已被 auto-pipeline 于 17:18Z 先行吸收 |

结论：**公开前沿已穷尽**。唯一仍在出量的是 `areebbb/squares-in-squares-the-last-1e-9`
的周期性重跑（17:48Z 版本 +1.1011e-5，24 题，已并入 bank），其收益量级已降到 1e-5。

### 2026-11-18 构造族封闭性（三条独立证明）

1. **精确 45° 中心菱形族封闭**：3.64M 三元组穷举，对 47 题与 bank 相符到 2e-13，
   其余 35 题 bank 严格更好，**0 胜**。
2. **旋转核心族封闭且可证**：核心旋转 φ 的精确 LP 化（约束对 (s,X,Y) 线性），
   φ∈[43°,47°] 以 0.02° 步长 + [40°,50°] 粗扫，**0 胜**；并给出支配性证明
   `s(φ) ≥ (TR+BL+2)/2 + a/√2 = s(45°)`，等号仅在 45°，即核心旋转**严格更差**。
   记录侧的 0.21–0.67° 缺陷角不是核心旋转，而是个别方块扰动。
3. **闭式 grid+band 模板族封闭**：5 个族（ELL/DIAG/CROSS/EDGE/FLOOR）穷举，
   仅 n=683（+2.18e-6）与 n=751（平局）两处，其余 bank 已最优或更好。

同时发现一个重要**数值陷阱**：45° 闭式公式在退化形状上不成立（公式边长 2.914214，
实际 L=3.371320），基于公式的筛选会产生 10 个假胜（n=6,17,29,55,68,83,153,175,446,637）。
必须用 LP 复算 + SAT 验证，这也是 cdb2 轨的 `rotcore.py` 现在的做法。

### 2026-11-18 连续抛光假设的证否（engine 轨硬证据）

移植 rosswade 公开 notebook 的 contact-force + fast-LP 引擎后，对 n=842 直接做了
"记录侧缺陷角 = 刚性核心旋转" 的检验：

| 实验 | 结果 |
| --- | --- |
| 核心刚体（232 方块）旋转 0.1° | 角部位移 0.025，局部重叠达 0.045 |
| `relax(free=核心附近 r+2)` 400 步 L-BFGS | E=15.9，min_gap −1.19，无解 |
| `relax(free=全部 842 方块, 盒 S+0.08)` | E→0 但两个方块重合，gap −1.207，`compact` 判 ov=1.2 拒绝 |
| 从旋转态 `compact` | ov=1.2，被正确拒绝 |

原因（389 个目标布局实测）：焊接刚体尺寸分布 **≤2 方块 27%、3–12 棒 16%、
13–40 6.6%、>40 51%**；`Hopper` 只能自由 bodies≤2 与棒≤12 内的相邻方块，
**一半方块永远动不了**，且 n=605/762/877/937/1000/730/677/626 的整个布局是单一刚体。

结论：记录侧位置**不是从我们的布局连续滑过去的**，它需要不同的接触图，
即构型/gadget 的改变；这与"固定角接触 LP 在目标侧全被拒"的历史结论一致。

另外两条组合封闭性（本轮修正后重算）：
- 单角 gadget 组合：**0 胜**（与之前一致）
- 双角 gadget 组合：**0 胜**——对立角的悬垂量是相加的（L = k + t₁ + t₂），
  不是取最大；先前一次错误实现曾给出 n=842→29.0 的假胜（842 方块 > 29²=841 面积），
  该错误已定位并修正。

### 2026-11-18 过盈律与两晶格错位构型（theory 轨，本轮最重要结构结果）

**核心变量不是 f 而是废面积 W。** 定义 `W = L² − n = 2kf + f² − D`，则

    L(k²+D) = sqrt(k² + D + W)

在 k=31 上：记录侧 `W = 31.15 − 0.121·D`，银行侧 `W = 31.87 − 0.131·D`。
每多一个方块只花 **0.87** 个面积单位（不是 1），这才是斜率 0.0138 的来源；
`f = a(D) + b(D)/k` 只是平滑假象（k=18..31 中有 98/468 个相邻步长恰好为 0，
1/k 律无法产生平台，说明 f 是"逐渐变大的 gadget 查找表"上的 min）。

**构造实测（从 bank 自身坐标量出）：两晶格断层。**
轴向格子在 x、y 上只取相位 `{0, f}`；`(f,f)` 偏移等价于沿 `U = x+y` 平移 `2f`；
一个格子占 `U` 长度 2，因此 **`f = 1/2` 就是完美的半格互锁**。

| | 2f |
| --- | ---: |
| 记录侧 | **1.00431** |
| 银行侧 | 1.04163 |

**整个 D=1 列的差距就是 `f = 1/2 + 0.00215` vs `1/2 + 0.02082`。**

**通道定理**：垂直宽度 `Δ(f+Δ)/√(1+Δ²)` 给出 `f ≥ √2−1 = 0.414214`
（Δ=1 阶梯时有效，Δ≥1.5 时为真空约束）；容量 `k√(1+1/Δ²) ≈ 34.7`（k=31, Δ=2）
正好解释观测到的 `D ≤ 36` 包络，而 `atan(Δ)` 复现 57.4°/66.2°/67.2°/71.75° 的带角。

**硬否定**：在记录侧 `L = 29.502152708` 上，单 45° 核心 + 全部晶格格子只能到 **823**，
两个互锁晶格到 **833**，而记录需要 **842**。即**单核心 gadget 可证短 9 个方块**，
记录用的是 **4 块 / 4 相位** 形式——这也解释了为什么 gadget 穷举只得到 2.6e-12。

**下一步实验**：对 4 个相位赋值做整数穷举（~10³ 组，用 `d_U + d_V ≥ 1` 判据），
而不是继续连续抛光。该实验已交给 theory 轨执行。

### 2026-11-18 重要更正：缺陷角来自我们自己的 bank，不是记录侧

polish 轨与 cdb2 轨各自独立发现：本战役多次引用的"记录布局缺陷角 44.79°–45.33°"
**实际测自 `/tmp/best_bank/submission.csv` 的 n=842 布局**，那是我们自己的 8 个接缝方块
（44.7921/44.8353/44.9154/44.9447/44.9852/45.0014/45.0026/45.3328），
不是记录持有者布局的特征。记录侧我们**只有 L 值，没有坐标**。

因此以下结论建立在一个循环推断上，应予撤回：
- "记录 = 我们拓扑的数值抛光位置"
- "刚性核心旋转 0.2–0.7° 可以复现记录侧"

证据链现状：
- 旋转核心族已在 `φ∈[43°,47°]`（0.02° 步长）穷举，**0 胜**，且有支配性证明
  `s(φ) ≥ s(45°)`，等号仅 45°——即核心旋转严格更差。
- 刚性组位移在 n=842 上是**精确卡死**：四个角簇朝收缩方向全部被核心以
  1/√2=0.7071 的面接触系数硬阻，9 约束 9 自由度超静定；34 自由度（放开 9 个接缝方块）
  同样卡死。18 个优先目标全部同类卡死。
- 还有一条几何事实：1.97 "waste units" 是**面积**预算，不是位移预算；
  缝隙是厚度 1/(2√2)=0.354 的锯齿带，宽度小于 1.0 放不下单位方块，
  所以那片面积不可能靠平移收回。

**净结论**：记录侧优势必须来自**我们没有的构型族**，而不是对我们布局的连续变形。
本轮唯一仍然有效的结构线索是 theory 轨的"两晶格/4 相位"计数论证
（记记录侧 L=29.502152708 时，单核心+全晶格=823，双晶格=833，而需要 842）。

### 2026-11-18 刚性组位移的定量证否（polish 轨最终证书）

把侧长钉在记录值、求"最小重叠"的刚性组排布（罚权 1e7，等价于硬约束）：

| n | 记录侧 L | 达到的 s | 总重叠 | 单对最大穿透 |
| --- | ---: | ---: | ---: | ---: |
| 842 | 29.502152708 | 29.501988 | **1.3346** | **0.05315** |
| 328 | 18.599535465 | 18.599533 | **0.6973** | **0.05173** |

即刚体必须互相穿透 **0.053 个格子**才能到达记录侧——这是 0.0187 差距本身的 **2.9 倍**。
全 bank 扫描：**396/396 道落后题零松弛**（`max |s₁−s₀| = 0.000e+00`，最终穿透 0.000e+00）。

**方法学副产品**：控制实验（把某刚体向外推 0.02 再让搜索恢复）显示 Nelder–Mead 只能
恢复到最优值上方 1.4e-4，DE 与 basin-hopping **完全无法恢复**。这解释了本战役
"所有局部搜索都返回 0 或 1e-7" 的一致现象：在 1e-2 尺度上罚函数墙太陡。

**结论**：剩余 0.0786 需要"格子跨组移动"（block-LNS 已 0 胜）或
**每道题跑数小时的全局 n 体退火**，不是刚体摆放。

## 2026-11-18 战役日志（第二轮）：gadget 平台、免费胜利点、已封闭族

### 1. 关键结构发现：近方题是“主 gadget 的提升”

对每个 D=k²+D 族，bank 的 f=L-k 在很多 k 上是**常数**（精确到 1e-12），说明它是
一个主 gadget 的角部提升（corner-gadget lift）。已确认的主 gadget：

| D | 主 gadget n=k0²+D | bank f | k 范围 | 平局题目数 |
|---|---|---:|---|---:|
| 1 | **65 = 8²+1** | 0.535533906 | 8..19 | **12** |
| 2 | **291 = 17²+2** | 0.535533906 | 17..23 | **7** |
| 3 | 628 = 25²+3 | 0.535533906 | 25..28 | 4 |
| 1 | 626 = 25²+1 | 0.520815280 | 25..31 | 0（但 7 题全部落后） |

“平局”= bank 与公开记录完全相同；因此**任何**对 65 / 291 / 628 主 gadget 的改进都会
立即变成 12 / 7 / 4 道题的同时胜利。65 每改进 dL，分数收益约 0.77·dL
（dL=0.0055 → 4.2e-3）。这是全竞赛最大的“免费胜利”杠杆。
626 不是免费：记录在 k=25..31 每一项都更好，首胜阈值是
f<0.511048764（k=25），全胜需要 f<0.502152708。

### 2. n=65 的 solid-core 族被精确封闭

用角度感知 SAT 精确计数（锚点：5×5 core、45°、gap=0.535533906 → covered=24,
kept=40, n=65，完全复现 bank 的 L=8.535533905932745）：

- 矩形 core (5,5),(5,6),(6,5),(4,7),(7,4),(4,8),(8,4),(6,6),(3,9),(9,3)：在
  g<0.5355 时全部 ≤62；g=0.5355 时只有 5×5 达到 65。g≤0.53 时 5×5 跌到 57（悬崖，
  因为 diamond 尖端跨过整行象限格）。
- 角度 36.87°,53.13°,22.62°,67.38° 的最佳值全部 ≤60。
- 结论：8×8 四象限 split-grid + 实心 core 族在 n=65 上**精确封闭于 bank 侧**。
  剩余的 12 题杠杆需要非实心 core（staircase polyomino）、多角度 fan 或全局退火。

### 3. n=401 是“多角度 core”的在手证据

bank 的 n=401（k=20）不是 45° core：183 个轴对齐 + **211 个非 45° 方块**，角度
均值 68.06°，模式 69.32(45), 69.66(23), 69.33(21), 68.74(14), 69.34(14), 69.65(12),
69.18(8), 68.04(7)…，散布约 ±1.5°。其 f=0.5330，已经优于 45° 族的 0.5355；
公开记录 k=20 的 f=0.5261。这直接验证了记录持有者的“many slightly different angles”
方法，并给出一个可反向工程的在手模板。

### 4. 数据源状态

- `udishiken/square-in-square-22-26`：perpuzzle 表总和 22.0677，比 11-11 快照
  22.0509 **更差**（279 题更差，0 题更好）；其 submission.csv 实测 22.2155，不可用。
- 11-11 快照本身相对 rank-1 的 22.03995 也已过时（每题最佳之和应 ≤ 任何单队分数，
  故真实前沿至少低 0.011）。但**我们的分数只取决于自己的提交**，快照只是可行性参考，
  落后题的“首胜阈值”不变。
- 11-11 快照仍是目前最好的公开逐题参考；`lostdecimal27` 的 10-29 副本更旧。

### 5. 方法学教训（本轮新增）

- bandphase 的 4 类晶格 MILP 在 n=328 的**自身锚点**上只得 261/262，差 1 格；
  在锚点精确复现之前，任何“记录侧不可行”的结论都不可信。已要求先补 loose
  squares / 第三相位 / 边界接触格，再搜索 block 角度与相位。
- “提升”工具 `/tmp/campaign2/lift.py` 已泛化到矩形 gadget（w≠h），并用 bank 的
  626→677..962 验证：复现 L 到 1e-13，merge 认证为 0 增益（几何正确）。
- 任何候选必须：n==行数、n≤L²+1e-9、逐对 SAT、merge 双路由 1000/1000。


## 2026-11-18 第三轮：切触界、全族封闭、外部枯竭

### 1. D=1 切触界（精确到 10^-15）

对“K×K 轴网格 + m×m 45° 实心核”的角部 gadget 族，精确计数给出唯一最优间隙

    f = m/√2 − (K/2 − 1)

- n=65（m=5, K=8）：f = 5/√2 − 3 = 0.5355339059327，与 bank 逐位相同；
- n=626（m=17, K=25）：f = 17/√2 − 11.5 = 0.5208152801713，与 bank 逐位相同。

覆盖格数在 g ≥ g* 时恒为 m²−1（24 / 288），在 g*−ε 时跳变为整环 24–48 / 48 格。
C++ GA 的 8.5338“近失”残余代价 4.6e-6，是**不可行**而非未完成。
n=65 的 4,261 个 staircase polyomino × 100 偏移精确扫描：最小值就是 bank 本身，
第二好 8.8184，**0 个形状低于 bank**。扇形（row fan）全部 ≥311 覆盖格（预算 288）。
结论：65 / 626 的实心核族在 bank 侧**严格封闭**；记录侧的 0.5022 必须来自
“倾斜晶格 patch + 第三相位”的不同架构。

### 2. 两晶格断层族的整数封闭

对两条相互垂直偏移 (f,−f) 的晶格，A–B 冲突图存在完美匹配，König 给出
MIS = k² **恰好**（完美匹配 + Hopcroft–Karp + 暴力 + HiGHS MILP 四重验证）。
每个目标 n=k²+D 且 D≥1，故该无 sliver 族**不可达**；每多一个方块都必须是
单独调角的 sliver。

### 3. 全库卡死（退火/刚体）

- 396/396 道落后题：`max |s₁−s₀| = 0`，一阶零松弛；
- 精确接触 LP（仅平移，可证）最大连续收缩：804 为 1.0e-7，970 为 3.9e-8，
  491/328/842/902/908/963 ≈0；而需要 0.0075–0.0215，差 10^5–10^6；
- 全库无一个可插入空单元格（n→n+1 通道关闭）；
- 退火最优严格增益仅 7.1e-9（n=804/970），已认证但无显示意义。

### 4. 外部源彻底枯竭

60,000+ puzzle 组、25 个公开数据集（含 408MB `kmmmvs` 私有包、50 份完整提交）、
972 个 jlevy issue、27 个 GitHub 证书仓、Packomania/Trump/OEIS/Zenodo/arXiv：
**0 胜**。最好的独立声明落后 bank 2.45e-12。386 道落后题的坐标是 Kaggle 私有的。

### 5. 记录持有者的真实架构（新线索）

我们自己的 n=401（k=20）不是 45° 核，而是**倾斜晶格 patch**：18×13 槽位、
69.3°、188 占用，配 191 个轴对齐格 + sliver。两纯晶格在该侧最多 400 < 401
（n=626 为 613 < 626），所以记录侧必须用**第三相位**或 patch 的 MIS/LP。
这是下一步 `mis401` 轨的实验：对 ~1000 个候选格做精确最大独立集/ILP。

### 6. 新算力载体：C++20 引擎

`corentinlaudicina/SquaresInSquares`（shrink / cycle / GA、深度²罚函数、
capped L-BFGS、LNM、独立精确验证器）已打包成 600KB 自包含 payload，
在 Kaggle CPU 上跑 top-16（排除已封闭的 65/626）+ 291 + band。两条关键教训：
- `start.mirror = true` 会先把非对称 bank 布局镜像破坏（n=328 立刻 +0.26），
  必须关；
- `prepare` 在紧布局上要 13–40 秒，`--time` 必须 ≥600 秒，否则 `kicks=0`。

### 7. 方法学：假阳性拦截

bandphase 的 n=491 候选 bbox 小 0.00318，但直接 SAT 查出 **120,283 对重叠**
（最差 −27.4），merge 正确拒绝。任何候选必须：n==行数、n≤L²、逐对 SAT、
双路由 1000/1000，缺一不可。


### 8. band 区间的精确天花板（第四轮）

把 n=328 等九题的“轴梳 + 倾斜块 + sliver”分解成 4 相位带框模型，精确计数：
- 锚点：n=328 复现 261 fill + 66 block + 1 loose = 328；n=965 复现 845+120=965；
  其余七题差 −2…−7（bank 的亚晶格缺陷，最大 5.8e-4）。
- 记录侧的最优（块平移 + 精确填充 + loose）：328 313/328（缺 15），908 870/906（缺 38），
  970 936/965（缺 34），804 768/799（缺 36），748 711/741（缺 37），491 472/489（缺 19），
  367 343/363（缺 24）；965/991 内容 bbox 已超过记录侧（不可行）。
- 加第三晶格相位最多 +1 格；独立全自由度 LP（2n 平移）给出九题**最大均匀收缩 0.000000**。
- 结论：记录不是被测块的再定相；唯一有希望的是**全倾斜 patch 模型**
  （w 行 × m 列、逐行角度、逐格相位），已交给 band 轨继续。

另：`/tmp/campaign2/band/contacts.py` 的 `sat_gap` 初始化 `best=-1e18` 且取 min，
**永远返回 -1e18**（此前“0 touch edges / 328 components”的报告作废）；修正后每题为
一个 295–969 方块的连通分量、258–3089 个接触对。

### 9. n=291 的精确封闭（D=2 主 gadget）

n=291 = 17²+2 的 bank 布局被精确分解为：两个 5×5 实心块（u0=5/√2、23/√2，块心相距 (9,9)）
+ 241 个四相位轴格；`repro.py` 逐格复现（241+50，最小间距 −3.6e-15，0 重叠），
L = 14 + 5√2/2 = **17.535533905932738**，即 f = 5√2/2 − 3。
- 轴填充 241 由 clique-cover set-packing MILP（HiGHS）证明**恰好最优**；
- 20 种核排列（两 5×5 不同间距、合并 5×10、单 5×5、三 4×4、6×5/4×6、6×6−角…）
  **全部需要 L ≥ 18.0**（差 0.464，不是近失）；
- 悬崖正好在 f：L=17+f 时 241；f−1e-5 时 ≤217；
- 插格扫描（90 方向 × 0.02 网格）**0 个可放位置**；
- SA 的残余满足 minsep ≈ −0.12·ΔL（卡死平衡，不是暂态）。
结论：291 在其族内封闭。**下一杠杆是 D=2 的 k=24..31 列**（578…963）：
bank 仍为 0.535533906，而记录已降到 0.5348/0.5311/0.5239/0.5216/0.5182/0.5141，
总差 ~3.59e-3，且记录本身证明**可达**。

### 10. n=401 的三相位 MIS（记录架构的精确上界）

bank 的 n=401 精确分解：180 精确轴 + 17 近轴 sliver + 197 倾斜带 + 6 倾斜 sliver
+ 1 个 (+3.52°) = 401（不是 220+191）。倾斜带是 69.32° 框架下的 26 行阶梯
（18 行 × 13 列的 ~1.0035 v 间距 + 16 个界面方块），每块有自己的角度。
- 两纯晶格 / 3-4 相位 HiGHS 在 L=20.533…20.526 的最大值**都是 400**；
- 固定 bank 带的精确轴填充只有 385；另外 16 格来自 **24 个手工 sliver**；
- bank-seeded 2258 顶点 MILP 在 L=20.532 **证明**最优恰为 400（status 0）。
结论：记录侧的 20.526135333 是**松弛后的非晶格布局**，不是又一个相位；
刚性族在 401 上封顶 400。

### 11. 2026-11-18 晚：公开工件再收获 +1.1e-4

公开渠道并未枯竭——新的每日工件仍在出现。两笔已安装（双路由 1000/1000）：

| 来源 | 题数 | 增益 | 最大单项 |
|---|---:|---:|---|
| `romywicaksono/squares-pipeline` 数据集（04:47Z） | 10 | **4.514e-5** | n=870 ΔL=1.061e-3（+3.597e-5） |
| `nilanjansaha123/s-in-s-certified-portfolio-merge-proj-quench`（20:20Z） | 50 | **6.460e-5** | n=991 5.98e-4、876 3.26e-4、421 2.73e-4 |

银行：`55090172…` / **22.128332087771835**（旧 `bb6d5f2a…` / 22.1283966845 由
`romywicaksono` 在 20:52Z 安装；更旧 `9c981e6e…` / 22.1284418248 已是提交值）。
累计对本轮基线 58418244 的增益 **4.4508e-3**。

**公开索引已再次被银行支配**：`nevska/squares-in-squares-explorer-files` 的
`credit_table.json`（556 题公开逐题最好侧 + 出处）对当前银行 **0 胜**；
此后检查的 `sigmaborov`（22.1335）、`penguin069` ga-contact（22.1352）、
`seshurajup`（22.1462）、`aqibrazadev`（22.1959）、`areebbb` frontier（22.1320）、
`jazivxt` 14:13Z（26.72）、`avazaku` cusp 全套（0 胜）均无胜。
`grennwolf/squares-in-squares-top-1-santa-2025` 是 GPU-only notebook，在 CPU 环境
直接 `SystemExit: No GPU driver`，无输出。

**提交配额**：2026-11-17 已用 9/9。已排定 **00:05Z 2026-11-18** 自动提交槽
（`final_slot.py --at 00:05 --at 09:00`），届时提交当前银行 + 夜间 C++ 引擎战果。

**夜间 CPU 管线**（全部 Kaggle CPU，无 GPU）：
- `sis-cpp-engine-self-polish`（shrink，3h，~23:06Z）
- `sis-cpp-engine-self-ga`（GA，2h，~23:20Z）
- `sis-d2-ladder`（D=2 k=24..31，1.5h，~23:05Z）
- `sis-d1-2224`（D=1 k=22..24，1.5h，~23:35Z）
- `sis-band-polish`（最后的带区抛光，已超时）
自动收割器 `cpp_harvest/auto_harvest.sh` 每 5 分钟轮询，完成即 JSON→CSV→merge→install。

### 12. 带区连续抛光最终证否 + 夜间全 C++ 管线

`sis-band-polish-20261118` 完成（3.5h，九题 328/367/491/748/804/965/908/970/991）：
`wins.json = {}`，九题 `results=[]`，每题跑到 2979–6335 秒仍无严格改进。
与 bandphase 的精确天花板（记录侧缺 15–38 格）、退火的 396/396 零松弛一致——
带区连续抛光轨道**彻底关闭**。

随后释放的槽位全部转入 C++20 引擎（Kaggle CPU，无 GPU），当前五路并行：
| kernel | 模式 | 目标 | 预算/结束 |
|---|---|---|---|
| `sis-cpp-engine-self-polish` | shrink | PRIO15 + BAND4 + 842 + 291 | 3h / ~23:06Z |
| `sis-cpp-engine-self-ga` | GA | 同上 | 2h / ~23:20Z |
| `sis-cpp-engine-self-cycle` | cycle（wall-free + full compression + Metropolis） | 同上 | 1.5h / ~23:35Z |
| `sis-d2-ladder` | GA | D=2 k=24..31（578…963） | 1.5h / ~23:05Z |
| `sis-d1-2224` | GA | D=1 k=22..24（485/530/577） | 1.5h / ~23:35Z |

收割：`auto_harvest.sh`（前三者）与 `auto_cycle.sh`（后两者）每 5 分钟轮询，
完成即 `out/best/*.json` → `sqpack_to_csv.py` → `squares merge` → `install_candidate.py --install`。
`final_slot.py --at 00:05 --at 09:00` 已排定：11-17 配额 9/9 用尽，UTC 零点重置后
自动提交当前银行（22.128332087771835）+ 夜间战果。

### 13. 头号发现：top-1 notebook 是 Santa 2025 冠军方法的移植

`grennwolf/squares-in-squares-top-1-santa-2025`（21:09Z 运行，24 票）的源码已拉取
（`/tmp/campaign2/newpub/grennwolf_src/`，278KB ipynb，45 个 cell）：
- **方法**：Jeroen Cottaar 的 **Santa 2025 第 1 名**方案——island genetic algorithm
  + GPU relaxation（`github.com/jcottaar/packing`），移植到本题；
- **输入**：`malyshevdanil/squares-in-squares-living-atlas-of-tight-packings` 的
  `submission.csv` 作为起始 packing，`inversion/squares-in-squares-per-puzzle-leaderboard`
  的逐题最好侧作为目标；
- **组件**：`ga.py`（78KB，8 islands × 64、14 种 move、crossover、diversity）、
  `rank.py`（按 gap×size 排序）、`polish.py` + `sq/lp.py`（**CPU 精确接触 LP**，
  scipy HiGHS，固定角度收缩）、`sqga/relax2f.cu`/`relax64f.cu`（CUDA L-BFGS，
  FP32 搜索 + FP64 legalize）、`sq/core.py`（numba SAT）；
- **要求**：2×T4（`machine_shape: NvidiaTeslaT4`, `enable_gpu: true`）。在 CPU 环境
  直接 `SystemExit: No GPU driver`，所以公开输出只有日志；ipynb 的 cell 无保存输出，
  没有 top-1 坐标泄漏。

**结论**：这是唯一已知的、能复现 22.04 量级的前沿方法；它需要 GPU。
用户已授权“先传 Google Drive，再用 Colab 挂载数据跑 T4”。当前唯一阻塞是
Colab OAuth 的一次人工 consent 点击（`/tmp/campaign2/colab/REPORT.md` §3 的 20 秒命令）。
一量 token 落地，就可以把我们的银行（比 Living Atlas 更强）作为起始、跑该 GA。

### 14. Colab T4 bundle 已上传 Drive 并本地验证

`我的云端硬盘/sis_campaign/`（27MB）：
- `submission.csv`（银行 55090172 / 22.128332087771835）、`report.json`；
- `perpuzzle_best.csv`（11-11 逐题记录）；
- `colab_pkg/`：top-1 GA 的全部 13 个源码文件（ga.py/rank.py/polish.py/sq/*/sqga/*.cu）；
- `prepare_colab.py`、`make_submission.py`、`run_colab.sh`、`COLAB_RUN.md`。

本地验证：
- `prepare_colab.py` → 1000 个 `runs/starts/nNNNN.npy` + `index.json` + 1000 条
  `data/leaders.csv` + 80 题 `sweep_ns.txt`；top gaps =
  `328,902,963,908,842,491,367,901,803,969,747,804,962,843,333,456,748,965,982,263,...`
- `make_submission.py` → 0 wins / 0 rows（起始就是银行本身，符合预期）。

唯一阻塞仍是 Colab OAuth 的一次人工 consent 点击；token 落地后
`colabx new -s sis --gpu T4` → 挂载 Drive → `NPROC=4 MAX_MIN=600 bash run_colab.sh`
即可跑 top-1 方法。

### 15. D=2 ladder（C++ GA，1.5h）结果：0 胜，近失 1e-10

`sis-d2-ladder`（GA，1.5h，280s/job，902/963/843/786/731/678/627/578 × ga-explore/ga-seeded）
16 jobs 完成、8 queued。每题 `start -> best -> legal` 全部等于 bank 侧：
578=24.535533906, 627=25.535533906, …, 902=30.535533906, 963=31.535533906。
`near_miss`（FP32 GA 在盒侧 h 上的最小残余代价）：
- 902: cost **1.03e-10** at h=30.535511（bank−2.3e-5）
- 843: 6.29e-10 at 29.535490（−4.4e-5）
- 786: 1.47e-10 at 28.535…（−4e-5）
- 963: 3.16e-9 at 31.535487（−4.7e-5）
即从 bank 出发的 GA 已在 bank 下方 **2–5e-5** 处达到卡死平衡；而记录 D=2 的
f=0.514079 需要 **0.0215** 的不同构造。1.5h 的 GA 不能跨过；D=2 杠杆需要
记录私有的新构造族（或 GPU 规模搜索），不是更多同族搜索。

### 16. 夜间管线最终配置（2026-11-18 00:00Z 前）

| kernel | 目标 | 预算 | 结束/收割 |
|---|---|---|---|
| `sis-cpp-engine-broad-seeded` | 389 题按当前 gap 降序（328 +8.19e-4, 902 +7.14e-4, 963 +6.91e-4, 908, 842, 491…） | 9.5h，08:20Z 硬截止 | ~08:35Z；`watch_broad.sh` |
| `sis-cpp-engine-self-polish` | top-16 + band4 + 291 + 842，4 shrink workers | 3h（或 10h） | auto_night |
| `sis-cpp-engine-self-cycle` | 同上，4 cycle workers（kick→wall-free relax→compress→Metropolis） | 1.5h | auto_cycle |
| `sis-d1-2224` | 485/530/577 + N±1 | 1.5h | auto_cycle |
| `sis-mis401-3phase` | n=401 的 3-phase MIS（本地已封顶 400） | 1–2h | mis401 watcher |
| `sis-d2master`（准备中） | 678/902 两个 D=2 master（记录 f=0.523860/0.514079，值 2.28e-3） | — | 下一个空位 |

已收割：`self-ga` 0 胜（10/88 jobs 完成，328/908/902/963/491×2 全部 = bank；其余 78 被
`--until` 截断）；`d2-ladder` 0 胜（17/17 valid，近失 3.9e-6–5.6e-5，cost 1.5e-11–3.2e-9）。
`sqpack_to_csv.py` 修复了 macOS `._*` 元数据文件导致的崩溃（此前的 self-ga 收割被它误报为
0 胜；修复后重跑确认确实 0 胜）。
提交：00:05Z（配额重置后，银行 22.128332087771835 + 已收割战果）；09:00Z（夜间全部战果）。

## 2026-11-18 停止方向清理（已删除约 20 GiB）

按“停止的研究只留本页简述与停止原因，不保留文档、脚本和中间产物”的约定，本轮清理了
2026-11-17/18 已判死的研究线、已吸收的公开源原始下载、旧前沿 watcher/agent 目录、被取代的
中间合并，以及本机缓存。完整路径、大小与保留证据见
[cleanup_20261118.json](../data/references/cleanup_20261118.json)；停止线的最终 REPORT 抽存于
[closed_20261118/reports](../data/references/closed_20261118/reports/)（29 份，1.2 MiB），
一次性族扫描表抽存于 `closed_20261118/evidence/`。

| 已停止路线 | 最后结论（停止原因） | 已删除 |
| --- | --- | ---: |
| 外部文献/代码/目录挖掘（`external`/`external2`/`external3`） | Mishapolk 6 题 +1.0402e-3 已入 bank；round2 仅 +5.8137e-11 且未安装；round3 解析 60,000+ 组 **0 胜**；来源枯竭 | 6.3 GiB |
| 定向 16 题外部搜索（`targeted`） | 16 个高价值题没有公开坐标；per-puzzle leaderboard 只有边长；0 候选 | 298 MiB |
| 公开前沿原始收割（`harvest`/`newpub`） | `harvest` 最好 +1.1011e-5；今日 romywicaksono +4.514e-5、nilanjansaha +6.460e-5 均已吸收；其余 0 胜 | 1.5 GiB |
| 旧前沿 watcher/agent 与中间合并（`/tmp`） | 旧 merge 最高 22.1296845，已被 22.1283321 取代；packer hop、penguin n=448 等胜题均已并入 | 10.5 GiB |
| 近方族实心核（`master65`/`master626`/`multiangle`/`staircase65`） | 切触界与 bank 逐位相同；45° 5×5 核是唯一可行核；所有 θ/offset/split/fan 更差；族精确封闭 | 2 MiB |
| n=291 双核、CDB、格点、带区相位（`master291`/`cdb`/`cdb2`/`lattice`/`bandphase`） | n=291 精确最优 17.5355339，20 种核排列全部 ≥18.0；CDB 47/82 恰为族最优、35 题 bank 更好、0 胜；两晶格容量恰为 k² | 173 MiB |
| n=401 三相位 MIS（`mis401`） | 纯晶格族封顶 **400**；记录的 401 是含 24 个手工 sliver 的松弛布局 | 1.4 MiB |
| 带区 9 题（`band`） | 12,536 s 连续抛光 **0 胜**；接触卡死；精确天花板差 15–38 格；±0.82° 缺陷承重 | 31 MiB |
| D=1/D=2 近方族（`d1_2224`/`d2ladder`/`d2master`） | 21/21、17/17 valid 全 **0 胜**；近失 3.9e-6–5.6e-5；记录 D=2 差 0.0215 = 不同构造；刚性族差 2–16 格 | 131 MiB |
| 刚性组/退火/连续抛光/旧 engine | 396/396 零松弛；连续收缩 ≤1e-7，而需要 0.0075–0.0215；engine 0 胜、半库焊死；deep 0 feasible | 257 MiB |
| 模板/多角度/理论构造族（`templates`/`theory`/`theory2`/`cpsat`） | 5 个闭式族全部被 bank 追平或击败；0 胜；证明结论已写入本页 | 98 MiB |
| C++ 引擎一次性测试输出 | 仅清 `out_fake`/`merge_test`/`out_ga`/`payload_test` 等；夜间 self-polish/broad/nearmiss/polish2 的 kernel、best、bankds、payload_broad 全部保留 | 142 MiB |
| Colab Chrome 配置副本 | 复制 profile 无法复用 Google cookie，OAuth 必须在真实浏览器点一次；保留 REPORT/OAuth 脚本/Drive bundle | 96 MiB |
| 本地 Drive 暂存重复 | 完整 bundle 已在 Drive `sis_campaign`；本地只留脚本与 `colab_pkg` | 40 MiB |
| 仓库 uv 缓存与根目录一次性表 | `.cache/uv` 与 `family_table*.json`/`phase_sweep.json`；表已抽存到证据目录 | 242 MiB |

保留：`/tmp/best_bank`（权威 bank、backup）；正在运行的 C++ 夜间链 `/tmp/campaign2/cpp_engine`
（115 MiB：kernel/best/bankds/stage/payload_broad/sqpack_to_csv.py）、`cpp_harvest`（脚本与日志）、
`watch`（watcher 状态）；`newpub/merge_nilan`（bank report 的 input，SHA 与 bank 相同）；
`colab` 精简脚本与 Drive 上的 T4 bundle；`docs/`、`data/references/`、`src/squares/`、
`outputs/submissions/bank_20261117/` 与 `gpu_f_20261116/`。

验证：删除前后 bank 的 SHA-256 均为 `55090172…`，`report.json` 仍报 **22.128332087771835**，
text/float64 均 1000/1000；`squares inspect` 报 500,500 行 / 1000 题 / 0 缺失；
`squares score --max-n 10 --mode both` 两条路径均 10/10（1.3711576158）；`squares merge`
用 bank 对自身跑完整收割路径得到 `changed_puzzles=[]`、`net_gain=0.0`、两路径
22.128332087771835；四个收割脚本 `bash -n` 全部通过；`newpub/merge_nilan/submission.csv`
与 bank 逐字节相同。磁盘：仓库
879 MiB → 638 MiB，`/tmp/campaign2` 9.4 GiB → 196 MiB，旧 `/tmp` 树 10.5 GiB 删除，
可用空间 526 GiB → 546 GiB（清理结束时实测）。

## 2026-11-18 02:27Z 公开 starter-kit v83 小胜（+1.724e-7）

公开源 subagent 用 Kaggle MCP 扫到 `alexchilton/squares-in-squares-starter-kit` **v83**
（dataset，2026-11-18 01:53Z 更新）。完整 merge 改 12 题、净 **+1.7379e-7**
（score 22.128331913985928），但其中 11 题只是 1e-12–1e-16 的格式级差异。按
“不引入脆弱近 tie”的原则，只取主胜题 **n=865** 做外科式 merge：
`changed_puzzles=[865]`，净 **+1.724244e-7**，text/float64 均
**22.12833191534741**，1000/1000。已安装为 bank `9b93a936…`；其余 11 题不安装。

本次对 58418244（22.1327829081）的累计增益为 **4.4509928e-3**。官方 ref 58487857
已 COMPLETE（22.1283320877）；09:00Z 槽提交新 bank + 夜间 kernel 战果。

证据：`/tmp/pubscan_20261118/merge_n865/`、`/tmp/pubscan_20261118/cand_n865.csv`；
合并记录已写入 `outputs/submissions/bank_20261117/provenance.json`（15 条 merge）。

## 2026-11-18 02:30Z Colab T4 GA 首个胜题 n=448（+1.3179e-5）

Colab T4 上跑的 Santa 2025 冠军 GA（`grennwolf` 移植）在第 50 代找到 n=448 的合法改进：
L `21.687501911686 → 21.687222964826`，score 增益 **1.317900e-5**。`make_submission.py`
输出候选，本地 `squares merge` 认证 `changed_puzzles=[448]`，text/float64 均
**22.12831873634704**，1000/1000。已安装为 bank `f4e8425d…`。

这是本轮第一条不是公开 donor、而是自研 GPU 搜索产生的胜题。对 58418244 的累计增益
更新为 **4.4641718e-3**。09:00Z 槽提交该 bank + 夜间 kernel 战果。
证据：`/tmp/campaign2/colab_merge/`、`/tmp/campaign2/colab_candidate.csv`。

## 2026-11-18 04:02Z Colab n=376 四连改进（+1.6337e-4）

同一 T4 GA 随后在 n=376 上连续四次合法改进：

| 阶段 | L |
|---|---:|
| bank | 19.876005938679 |
| 第 1 次 polish | 19.875391479495 |
| 第 2 次 polish | 19.874818651469 |
| 第 3 次 polish | 19.873850496145 |
| 第 4 次 polish | **19.872838100383** |

本地 `squares merge` 认证 `changed_puzzles=[376]`，text/float64 均
**22.12815536756089**，1000/1000，净增益 **1.6336879e-4**。已安装为 bank
`4a03e224…`。这是本轮最大的自研单题收益，超过今天两笔公开 donor 之和。

对 58418244 的累计增益更新为 **4.6275405e-3**；相对官方 58487857
（22.1283320877）已低 **1.7672e-4**。09:00Z 槽提交该 bank + 夜间 kernel 战果。
证据：`/tmp/campaign2/colab_merge/`、`/tmp/campaign2/colab_candidate.csv`。

## 2026-11-18 05:27Z Colab n=376 第二阶段（+1.2215e-4）

同一 T4 GA 在 n=376 上继续累积到 **17 条**合法改进，第二阶段把 L 从
`19.872838100383` 推到 `19.870469467981`。本地认证 `changed_puzzles=[376]`，
text/float64 均 **22.12803321467166**，1000/1000，净增益 **1.2215289e-4**。
已安装为 bank `3adf4d68…`。

n=376 单题两阶段合计 **2.8552e-4**，是目前自研 GA 的最大收益。对 58418244 的
累计增益更新为 **4.7496934e-3**；相对官方 58487857（22.1283320877）低
**2.9887e-4**。09:00Z 槽提交该 bank + 夜间 kernel 战果。
证据：`/tmp/campaign2/colab_merge/`、`/tmp/campaign2/colab_candidate.csv`。

## 2026-11-18 08:16Z Colab n=264（+7.710e-5）

T4 GA 继续在 n=264 上累积 4 条合法改进：L `16.773807597984 → 16.772554834668`。
本地认证 `changed_puzzles=[264]`，text/float64 均 **22.127956112419483**，
1000/1000，净增益 **7.7102252e-5**。已安装为 bank `5d8d79fa…`。

至此 Colab 自研 GA 已贡献三道题：n=448 +1.3179e-5、n=376 +2.8552e-4、
n=264 +7.7102e-5，合计 **3.7590e-4**。对 58418244 的累计增益更新为
**4.8267957e-3**；相对官方 58487857 低 **3.7598e-4**。09:00Z 槽提交。
证据：`/tmp/campaign2/colab_merge/`、`/tmp/campaign2/colab_candidate.csv`。

## 2026-11-18 08:48Z broad-seeded n=545 与 Colab 会话丢失

`sis-cpp-engine-broad-seeded` 在 08:20Z 截止后完成。CLI 逐文件下载被
`kaggleusercontent` 的 SSL EOF 卡在 70/389；改用 Kaggle API 列文件 + 独立
session 重试，**389/389 全部下载成功**。`sqpack_to_csv.py` 找到 1 个胜题：
n=545，L `23.813821288 → 23.813722828`（ΔL −9.846e-5）。merge 认证
`changed_puzzles=[545]`，净 **+4.2175989e-6**，双路由 **22.127951894820566**，
1000/1000，已安装为 bank `68dc750e…`。

`sis-cpp-engine-polish2` 随后完成：23 个 best 文件，**0 胜**。

Colab T4 会话在 08:37:42Z 被回收（404/401），运行 7h22m。最后一条未收割的
n=264 尾改进（L 16.772474136323，约 **4.97e-6**）随 VM 丢失；当前 bank 保留的是
16.772554834668。尝试 `colab new -s sis2 --gpu T4` 返回 **503 Service Unavailable**，
暂时无法重新分配 T4。

对 58418244 的累计增益更新为 **4.8310133e-3**；相对官方 58487857 低
**3.8019e-4**。09:00Z 槽提交该 bank。
证据：`/tmp/broad_full/out/best/`（389 JSON）、`/tmp/campaign2/cpp_harvest/broad-full/merge/`。

## 2026-11-18 09:00Z 提交与新 Colab 账号恢复

09:00Z 槽由 `final_slot.py` 正常触发：ref **58502763**，官方分
**22.1279518948**，`COMPLETE`，与本地 bank `68dc750e…` 一致。

老账号 `smshiliangyao` 的 T4 仍返回 **503**；新账号 `ccjjllt0` 的 T4 可用。
根因不是账号额度，而是 `colabx` 默认代理 `127.0.0.1:7900` 在
`POST /tun/m/assign` 上稳定 `SSLEOF`；换 `COLAB_PROXY=http://127.0.0.1:7897`
后 `new -s gpu1 --gpu T4` 一次成功。该结论已写入 `README.md` 的
“Colab T4 运行（colabx）”一节，并新增 `scripts/colab_bootstrap_remote.py`。

数据不再依赖 Drive 挂载：GA bundle（`colab_pkg/` + 当前 bank + prepare/run/harvest
脚本）打成 `sis_bundle.tar.gz`，作为私有数据集
**`ccjjllt/sis-ga-bundle-20261118`**（7.9 MiB）发布。会话内用 Kaggle token 下载、
解包到 `/content/sis`、`prepare_colab.py` 建 1000 个 starts；随后
`NPROC=4 MAX_MIN=600 bash run_colab.sh` 起 4 个 GA worker + 1 个 polish。
13:04Z 状态：GPU 100%、6 进程、0 改进（刚开始）；13:07Z 首个 worker 进入
n=367（f 0.68279）。

rank.py 的目标表按当前 bank 与 11-11 逐题记录计算，前 15 大 gap 中
**6 题（902/963/842/901/962/843）因 45° 边缘被自动跳过**；这 74 题合计
0.0053 分，是 GA 覆盖不到的剩余空间。主流 gap（328/908/491/367/803/747/…）
仍在列表内。

证据：`README.md`、`scripts/colab_bootstrap_remote.py`、
`/tmp/sis_bundle_build/`、Kaggle dataset `ccjjllt/sis-ga-bundle-20261118`。

### 13:09Z 逐题榜刷新：22.0310070197

11-11 快照已过时。`inversion/squares-in-squares-per-puzzle-leaderboard`
（定时刷新，12:02:43Z 运行）把完整表以 `const DATA` 嵌在 `__results__.html` 里，
13:09Z 抓取后与 11-11 的 502 条 baseline 行合并为
`data/references/leaderboards/perpuzzle_best_20261118.csv`（SHA `9cae7620…`）。

- 逐题最佳合计 **22.0310070197**，低于榜首单次提交 22.0399510810（混合收益 0.0089）；
- 对 bank 的总正差距 **0.096944875120**，399 题落后 ≥1e-6，437 题并列，**0 题严格领先**；
- 差距集中：top-10 9.3%、top-60 36.1%、top-100 51.3%；
- 持有者：Cats and boxes 262 题 / 0.066394（68.5%）、VitalyR 7.8%、
  Sunstone 7.0%、Chris Deotte 4.9%。

| 家族 | 题数 | 落后≥1e-6 | 差距合计 | 占比 |
|---|---:|---:|---:|---:|
| D9–16 | 163 | 114 | 0.027646 | 28.5% |
| mid17–24 | 114 | 68 | 0.020188 | 20.8% |
| D5–8 | 94 | 53 | 0.013187 | 13.6% |
| D1 | 31 | 31 | 0.006703 | 6.9% |
| D2 | 8 | 8 | 0.003904 | 4.0% |

Top 10 目标：234（0.001198）、491、962、901、842、730、328、785、367、738。

**D1/D2 是系统性 k 缩放构造，不是抛光**：D1 记录 `L−k` 从 k=25 的 0.51105
降到 k=31 的 0.48951（bank 恒为 0.520815），k=31 的 31.489513775 已**低于 k+0.5**，
与 `√(k²+k)=31.4960` 只差 6.5e-3；D2 同样从 0.53298 降到 0.51177（bank 0.535534）。
这否定了“记录侧存在固定 `max(w,h)≤29` gadget”的旧结论（§ 结构结论），
指向随 k 变化的互锁/环扩展构造。

Colab 会话已把 `leaders.csv` 换成本表并重启 ranker；新 ns 首位为 n=234。
rank.py 的 45° 规则会跳过 D1/D2 的 7 道旗舰题（962/901/842/785/730/963/902），
因此单独起了一个 `--ns` 固定列表的 worker（tag `_d12`）专攻这 7 题。

证据：`data/references/leaderboards/perpuzzle_best_20261118.csv` 与
`.provenance.json`、`/tmp/campaign2/GAP_REPORT_20261118.md`、
`/tmp/campaign2/gap_targets_20261118.json`、`/tmp/campaign2/top100_gap_20261118.csv`。

## 2026-11-18 13:50Z 公开收割 +8.138e-4（bank 22.1271380476）

公开哨兵（`/tmp/pubscan2`）扫了 191 个 notebook、45 份输出、67 个候选 CSV、
20 个 squares/packing 数据集、17 个 GitHub 仓库后发现两笔真实增量：

| donor | 发布时间 | 胜题 | 净收益 |
|---|---|---:|---:|
| `alexchilton/squares-in-squares-starter-kit` → `best_current.csv`（sha `3b60ade8…`） | **2026-11-18T10:54:40Z** | 160 | **+7.8687537e-4** |
| `AHFE0924/Squares-Feeder` → `latest_public.csv`（sha `da479cab…`） | 2026-11-16 | 21 | **+2.6971826e-5** |

两步 merge 各自双路由 1000/1000：hop1 `22.127951894820566 → 22.127165019452693`
（`changed_puzzles=160`），hop2 `→ 22.12713804762674`（`changed_puzzles=21`，
n=378/464/465/495/499/501/502/503/543/546/632/683/686/694/707/736/758/761/809/817/875）。
最终 union SHA-256 `430bb155…`，500,500 行、1000 题、0 missing，已安装进 bank 并
提交 **ref 58512171**（13:50:09Z）。

注意 `best_current.csv` 单独评分只有 22.129578（比 bank 差），价值全在**逐题**：
160 题上它更好。这与“公开源要逐题合并、不能看整表分数”的既有结论一致。

其余公开源全部 0 胜或只是 hop1 的严格子集（jazivxt 7.8577e-4/107 题、nilanjansaha
GPU 7.8688e-4/107 题、kmmms 2.0440e-4/80、kazuhiroyogo 2.0434e-4/90、
lianlian99 2.0207e-4/22）。`udishiken/square-in-square-22-26`、`lostdecimal27`
均无新版本；Nevska 11-18 的 explorer 只有边长/哈希，无坐标。

对 58418244 的累计增益更新为 **5.6448605e-3**。已设置 30 分钟哨兵
（alex 数据集 + AHFE GitHub），只做只读 merge、不安装、不提交。

证据：`/tmp/pubscan2/REPORT.md`、`/tmp/pubscan2/merge_alex_bestcur/`、
`/tmp/pubscan2/merge_alex_feeder/`（`submission.csv` SHA `430bb155…`）。

### 14:00Z 官方确认、Colab 首胜与新证据

- ref **58512171 COMPLETE = 22.1271380476**，与本地逐位一致（14:05Z 排名 **102**，
  09:00Z 时是 107）。
- Colab T4 用**刷新后的逐题目标表**跑出第一胜：n=264
  `16.772554834668 → 16.772430426879`（**+7.6567701e-6**），merge
  `changed_puzzles=[264]`，双路由 1000/1000，bank 更新为
  **22.127130390856603**（SHA `f599393a…`）。15:00Z 槽提交。
- 新增 `scripts/colab_harvest_safe.sh`：探测 kernel（卡死就 `restart-kernel`，
  detached GA worker 不会死）→ 远端 `make_submission.py` → 下载 → 只读 merge →
  **仅在 ≥1e-10 且双路由 1000/1000 时自动安装**。当前以 1800s 循环常驻，
  避免再次出现“改进随 VM 丢失”。

**S4 前沿结论（硬否定）**：把记录族形式化为 lattice+defect 后证明
“任何插入的单位正方形都需要一个含 1×1 空腔的 void”，因此刚性平移 defect 至少
`f ≥ 1/√2 = 0.70711`（45° 菱形）或 `f = 1`（轴对齐）。记录侧 D1 的 f 从 k=19 的
0.532894 降到 k=31 的 **0.489514**，低于 1/√2 屏障，所以记录族**不可能**是
lattice+刚性 defect；必须是 fractional-offset 的重新铺砌/fanning。该结论解释了
fault-line、two-lattice、frozen-grid、rigid/anneal、contact-LP 全部 0 胜的原因。
证据：`/tmp/campaign2/FRONTIER_REPORT.md`、kernel
`ccjjllt/sis-frontier-fanprobe-20261118`（COMPLETE，1272s）。

**S2 环扩展分析**：586 个极大环组，但只有 7 组携带差距（4.46% 的 0.0969），
95.5% 的差距没有精确环孪生；bank 本身是环扩展的（D1 f 恒 0.520815），
而记录每一步都降 f——继续拉长环只会保持差距，必须在每个 k 上单独找构型。
基实例 392 个（只比 399 少 1.8%）。

**S3 CPU kernel**：`ccjjllt/sis-cpp-engine-gap2-20261118` v2 于 13:38Z 起跑，
57 题（占差距 3.02e-2）、4 workers、203 jobs、~8.15h，预计 22:10–22:40Z commit；
已排除 45° D1/D2（交给 Colab 专用 worker）。

**S5 alex 方法加宽**：`ccjjllt/sis-alexkit-wide-20261118` v4 于 14:40Z 起跑。
公开 starter kit 只带 driver，引擎是 `github.com/evand/square-packing` 的
`packer hop`（basin hopping + L-BFGS，MIT，pin `c801ab47`）。104 题、216 jobs、
2160 process-min ≈ 9h，预计 23:46Z；首个认证胜 **n=915**
`30.740316604 → 30.739963633`（−1.17e-5，600s）。

**15:00Z 槽故障与修复**：老 `final_slot.py` 用一次 `time.sleep(357min)`，实际
15:07:41Z 才醒（macOS 定时器合并/App Nap），结果手动 15:05Z 的 58514784 与它的
58514816 重复提交了同一个 bank。已换成 `scripts/submit_slots.py`：30 秒轮询、
按日状态文件去重、CLI 调用带 7897 代理，槽后 10 分钟内触发。当前 bank
**22.127130390856603** 已由 58514784/58514816 提交，官方 **22.1271303908**。

**Colab 会话 15:20Z 被回收并自动恢复**：第一段 T4 只跑了约 2h20m（13:00–15:20），
比昨天的 7h22m 短。新增 `scripts/colab_keeper.sh`：每 5 分钟只查 session 列表
（不碰 kernel），发现丢失就 `colabx new -s gpu1 --gpu T4` → 用最新私有数据集
bootstrap → 起 4 个 GA worker。15:21Z 已自动完成：新 VM 从 **当前 bank
22.1271304** 和 **2026-11-18 逐题记录**出发（数据集 v2，15:09Z 上传），
GPU 100%，worker 正在跑 234/328/367。旧 VM 的唯一改进 n=264 已在丢失前入 bank。

为避免 kernel 再次被过多进程拖死，新会话维持 4 个常规 worker，不再额外挂
D1/D2 专用 worker；45° 家族交给 S4 的 free-offset 可行性与 Kaggle CPU 侧。

## 2026-11-18 15:50Z Joost n=299 精确证书（+4.2607e-4）

第二轮公开扫描找到 `github.com/JoostdeWinter/square-packing`（HEAD `7232328`，
2026-11-18T07:31Z）的 `n299/n299_exact.json`：有理数精确证书，边长
**17.793636991743039**，比 bank 的 17.801004434251865 低 0.00737。证书本身是
零间隙接触，float64 下不合法；按 1e-12 中心膨胀后通过官方 v20 双路由：
`changed_puzzles=[299]`，净 **+4.2607020e-4**，score **22.126704172180595**
（与 AHFE 15:20Z 版本 union 后同分），1000/1000。已安装为 bank `e50d51e2…`，
提交 **ref 58516336**。

同一轮扫描的其他结论：

- **残余差距 100% 由没有公开坐标的队伍持有**。top-4 占 0.0848186（88.2%）：
  Cats and boxes 0.0658310（266 题）、VitalyR 0.0075195、Sunstone 0.0067601、
  Chris Deotte 0.0047080。Deotte 的 14 条记录在其公开 notebook 中复现 0/14；
  Nevska 的 52 条只有边长。
- `jlevy/squares` register（HEAD `1015fc17`）解析出 315 条已知最优见证，**0 胜**；
  9 条代数域见证被跳过，待用同样的 1e-12 膨胀复核。
- Joost 仓库另有 55 题候选，17 个精确接触组“invalid”，其余都弱于 bank；
  需要用 n=299 同款膨胀再复核一次，可能还有漏网。
- alexchilton 仍是 v85（10:54:40Z）；AHFE 15:20Z 版本再贡献 6.08e-9，已并入。

**S4 自由偏移模板最终结论**：T3（45° 块 + 四角楼梯，精确闭式）对 6 个 D1 目标的
容量只有 601/653/725/820/880/921（需要 626/677/730/842/901/962），**6/6 不可行**；
T1/T2 因 v1 的 `max_nfev` 参数 bug 未真正迭代，v2 预算被 gadget 压缩耗尽，
无判决；gadget 压缩在 f=0.520815 上 0/3 可行（n=65 残差 4.18e-3 最接近）。
CPU 可测的固定模板到此全部封死，剩余可能只有 GPU 上的 fan/multi-angle 自由搜索。

**会话抖动**：15:21 新建的 T4 在 15:37 又消失，keeper 再次重建。已给 keeper 加
“空列表需二次确认 + runtime ID 记录”，避免把健康会话误判为丢失而重建；
harvest 也改成连续两次探测失败才 `restart-kernel`。

### 精确证书类已穷尽

对 Joost 55 组 + jlevy 324 组（9 组代数数用 80 位精度求值）逐一做 1e-12 中心膨胀
并跑官方 v20：**379 组中 138 组原始边长低于 bank，138/138 膨胀后合法，但可用 0 组**。
原因是膨胀代价约 1.0–1.7e-11，除 n=299（原始余量 1.679e-11）外全部翻负：

- Joost n=268/270 余量 6.68e-13；jlevy n=295 1.037e-12；n=272/262/260 约 6.5e-13；
- 9 条代数见证的余量只有 3.1e-15…3.72e-14，膨胀代价是余量的 300–3000 倍；
- 17 个 Joost “invalid” 组在 1e-12/1e-11 下全部合法，纯属零间隙接触退化，
  其中 n=413/543/547/590/851/910 的边长反而比 bank 差 6.97e-3…4.26e-2。

整类 union（363 题、81,547 行，SHA `2cf2ebbc…`）merge 增益 **0.0**。
独立 `squares score` 复核 bank：**22.126704172180595** text / 22.1267041721806
float64，1000 有效、0 invalid、0 missing，输入 SHA `e50d51e2…`。
证据：`/tmp/pubscan2/rescan2/audit_groups_below_bank.tsv`（138 行）、
`/tmp/pubscan2/rescan2/merge_audit_all_dilated/`。

**n>324 的精确证书也已穷尽**（第二轮 GitHub 定向搜索）：Joost 55 组、
jlevy/Couzo 253 组（325–994）、`franciscouzo/square-packing` 396 组（325–998）、
`TheSnakeFang/squarepack-certs` 17 组、`Mishapolk` 18 组、`evand` 25 组、
`sosudo` 130 个坐标候选，以及 1zuki/Belloblaze/nayan268/Ujjwal/amin076/
NNGeetha/RAH333/JohnKimaiyo/wand125/chelokot/HyukdongKim/mohsensbu/anopheles/
JonathanGun 等仓库，**全部 0 胜**（原始边长就不低于 bank，膨胀无从谈起）。
唯一“看起来能赢”的 `oceanwang/poc/lift_polish/data/shrunk_frontier.csv` 在
n=442/485/530/577/743/798 上标称 +1.029e-3，但固定配对的方块重叠约 5e-4，
1e-10 膨胀后仍非法，是**造假/错误数据**，不采用。

同日 16:27Z 又从 AHFE commit `216698d2` 拿到 n=342/683/736 的
**+1.8179437e-7**（max n=736 是 2.75e-15 的并列，不算实质胜利），
bank 更新为 **22.12670399038623**（SHA `1d2c7665…`）。

### 16:00Z Colab 免费 GPU 额度耗尽

15:42 的 T4 只活了 15 分钟，15:57 新建的会话 **4 分钟内又消失**（16:01Z
`No active sessions found on server`）。这是账号级免费 GPU 额度用完的典型形态，
不是脚本问题：同一天该账号已累计跑了两段（2h20m + 15m），老账号上午已用 7h22m
且一直 503。两个账号的免费 T4 目前都不可用。

处理：
- keeper 加 **backoff**：如果上一个 runtime 存活 <25 分钟，就暂停 90 分钟再试，
  避免把额度浪费在只能跑几分钟的会话上；
- harvest 先查 session 列表，没有会话就不再发 exec，也不再 `restart-kernel`；
- 夜间搜索改由 **Kaggle CPU** 承担（gap2 / alexkit-wide / alexkit-d1d2 三个
  kernel，约 6 小时）；公开哨兵继续。

Colab 额度恢复后 keeper 会自动重建会话并从数据集 v3
（bank `e50d51e2…`）bootstrap。
