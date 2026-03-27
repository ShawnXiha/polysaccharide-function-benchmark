# 多糖论文规划：Story Design、Comparisons、Ablations、Demo Scenarios

## 0. 论文定位

### 工作标题

`Polysaccharide Structure-Function Benchmark and Evidence-Aware Modeling`

### 论文类型

- 资源 + 方法混合型论文
- 第一优先目标不是宣称“多糖基础模型”，而是建立一个可复现、可评测、可解释的多糖结构-功能预测任务

### 最小可辩护 claim

我们首次把 `长链多糖` 的结构-功能预测系统化为一个可复现 benchmark，并证明：

1. 直接迁移 glycan-centric 表示和模型到 polysaccharide 任务时，跨来源泛化明显不足
2. 显式建模多糖特有结构因素与证据权重后，可以显著提升鲁棒性、可解释性和跨来源泛化

### 不要宣称的内容

- 不要宣称“解决了多糖功能预测”
- 不要宣称“建立了完整多糖知识图谱”
- 不要宣称“提出了通用多糖基础模型”

## 1. Mock Rejection Letter

先写潜在拒稿意见，再反推实验设计。

### 可能的拒稿意见

- `R1 limited novelty`: 只是把现有 glycan 模型迁移到多糖数据，没有真正方法创新
- `R2 dataset issue`: 数据噪声大、标签标准不统一，结论可能不可靠
- `R3 missing baselines`: 没有和合理的序列模型、图模型、手工特征模型充分比较
- `R4 weak generalization`: 只在随机划分上有效，跨来源/跨物种泛化不成立
- `R5 interpretability is shallow`: 所谓可解释只是 feature importance，没有和真实化学规律建立联系

### 对应预防动作

- 对 R1：把贡献定位成 `benchmark + evidence-aware modeling + polysaccharide-specific representation`
- 对 R2：做证据分级、标签清洗协议、数据卡、来源追溯
- 对 R3：至少做手工特征、序列模型、图模型三类 baseline
- 对 R4：必须加入 `leave-one-source-out` 和 `leave-one-genus-out`
- 对 R5：做 motif/linkage/modification/molecular-weight 四类误差与解释分析

## 2. Story Design

### 2.1 Task

建立面向长链多糖的结构-功能预测 benchmark，并设计一个证据感知的预测框架。

### 2.2 Challenge

现有糖科学机器学习多数围绕 glycan，而不是 polysaccharide。多糖任务有四个额外难点：

- 结构表示不完整且标准不统一
- 功能标签来自异构实验体系，噪声高
- 长链多糖存在重复单元、分支、修饰和分子量分布等特有因素
- 随机划分容易高估性能，跨来源外推更接近真实应用

### 2.3 Insight

问题的核心不只是“模型不够强”，而是 `任务定义和数据表示不对`。如果：

- 把多糖统一到一个可训练的表示
- 明确保留证据等级和来源追踪
- 用更符合实际的跨来源评测

那么即使不是很复杂的模型，也能得到更可信、更可解释的结果。

### 2.4 Contribution

#### Contribution 1

定义第一个面向长链多糖结构-功能预测的可复现 benchmark。

#### Contribution 2

提出一个 `evidence-aware` 建模框架，把实验证据等级、来源数据库和结构缺失情况纳入训练和评测。

#### Contribution 3

系统比较 glycan-centric baseline 在 polysaccharide 任务上的迁移表现，并识别其失败模式。

#### Contribution 4

构建最小知识图谱支撑证据追踪和误差解释，形成可复核的构效分析流程。

### 2.5 Advantage

- 比现有工作更贴近多糖真实任务，而不是继续沿用寡糖任务设定
- 结果更可信，因为不只看随机 split
- 更容易复用，因为数据、schema、split、证据链都可以公开
- 即使方法增量有限，资源价值和任务定义价值仍然成立

## 3. Story Flow

### Introduction 逻辑链

1. 多糖功能研究重要，但机器学习落地慢
2. 根因不是缺少模型，而是缺少任务定义、标准化数据和可信评测
3. glycan 领域已有 SweetNet/glyBERT/GlycanML 等进展，但不能直接覆盖长链多糖
4. 长链多糖与 glycan 的关键差别在重复单元、统计结构、修饰、分子量和标签异质性
5. 因此本文不先追求更大模型，而是先建立 benchmark 和 evidence-aware modeling
6. 在此基础上证明：合适的数据建模和评测协议本身就能带来更可靠的性能与解释

### 一句话摘要骨架

We present the first reproducible benchmark for polysaccharide structure-function prediction and show that evidence-aware modeling with polysaccharide-specific representations yields more reliable cross-source generalization than direct transfer of glycan-centric baselines.

## 4. Module Motivation Mapping

| 模块 | 为什么必须有 | 如果没有会怎样 |
| :--- | :--- | :--- |
| 统一结构 schema | 解决跨库字段和表示不一致 | 数据不可复现，模型输入混乱 |
| 证据分级 | 处理 in vitro/animal/clinical 标签异质性 | 模型把噪声当真值 |
| 多糖特有表示 | 捕获重复单元、分支、修饰、分子量 | baseline 只学到浅层相关性 |
| 跨来源 split | 测真实泛化 | 随机 split 虚高 |
| 最小 KG | 提供来源追踪与错误分析 | 结果难以解释、难以审稿说服 |

## 5. Claim-to-Experiment Mapping

| Claim | 必须证明什么 | 对应实验 |
| :--- | :--- | :--- |
| 我们定义了有效 benchmark | 数据可复现、任务清晰、split 合理 | 数据统计表、schema、data card、split 说明 |
| glycan baseline 直接迁移不足 | 跨来源泛化差，不只是分数低 | 随机 split vs source split 对比 |
| evidence-aware modeling 有效 | 加入证据后性能或校准更好 | 证据权重 ablation、校准分析 |
| 多糖特有表示有效 | 重复单元/修饰/分子量信息有贡献 | 表示 ablation、特征重要性 |
| 方法更可信 | 预测可追溯、有可解释模式 | KG-driven case study、误差分析 |

## 6. Comparison Plan

### 6.1 Comparison Checklist

- [ ] 至少覆盖手工特征、序列模型、图模型三类 baseline
- [ ] 至少覆盖一个 glycan 领域代表模型改造版
- [ ] 所有方法使用同一数据版本和同一 split
- [ ] 报告平均值和方差，不只报最好一次
- [ ] 同时报随机 split 和跨来源 split

### 6.2 建议 baselines

#### Classical baselines

- `Majority / stratified baseline`
- `Logistic Regression / Linear SVM`
- `XGBoost or LightGBM` with handcrafted features

#### Sequence baselines

- `Bag-of-substructure / n-gram`
- `Transformer on canonical IUPAC`
- `Transformer on WURCS` if conversion稳定

#### Graph baselines

- `GCN / GIN`
- `SweetNet-style graph model`
- `Hierarchical graph model` for repeating units if实现可控

#### Evidence-related baselines

- 不加证据权重的标准训练
- 加 source token 但不加 evidence weight
- 加 evidence weight 但不加 source token

### 6.3 Comparison Table Checklist

- [ ] 主表 1：随机 split 上的多方法比较
- [ ] 主表 2：cross-source / cross-genus split 上的多方法比较
- [ ] 主表 3：校准、AUPRC、宏平均 F1 等鲁棒指标
- [ ] 附表：计算开销、参数量、训练时间

## 7. Ablation Plan

### 7.1 Core Ablation Checklist

- [ ] 去掉证据权重
- [ ] 去掉来源/source 信息
- [ ] 去掉分子量相关特征
- [ ] 去掉修饰特征
- [ ] 去掉重复单元或层次结构编码
- [ ] 用随机 split 替代 cross-source split 观察结论变化

### 7.2 核心 ablation 表

| Ablation | 目的 | 预期现象 |
| :--- | :--- | :--- |
| Full model | 作为参考 | 最稳 |
| w/o evidence weighting | 证明证据建模有效 | 校准和泛化下降 |
| w/o source encoding | 证明来源偏移存在 | cross-source 明显变差 |
| w/o MW feature | 证明分子量信息有贡献 | 某些功能任务下降 |
| w/o modification feature | 证明修饰信息重要 | 与抗病毒/免疫相关任务可能下降 |
| w/o repeating-unit encoding | 证明多糖特有表示重要 | 跨任务整体下降 |

### 7.3 Design-choice ablations

- [ ] IUPAC vs WURCS
- [ ] 单任务 vs 多任务学习
- [ ] 证据权重策略：hard weighting vs soft weighting
- [ ] label cleaning 前后
- [ ] 是否加入 KG-derived features

### 7.4 Error Analysis Checklist

- [ ] 错误按来源数据库分组
- [ ] 错误按物种分组
- [ ] 错误按分子量范围分组
- [ ] 错误按修饰类型分组
- [ ] 错误按标签证据等级分组

## 8. Demo Scenarios

这篇论文的 demo 不该是“炫技 UI”，而应该是能直接服务审稿判断的场景。

### Demo Scenario 1：Cross-source generalization stress test

目标：

- 展示随机 split 很乐观，但真实外推困难

Checklist：

- [ ] 选一个功能任务
- [ ] 报告 random split 结果
- [ ] 报告 leave-one-source-out 结果
- [ ] 可视化性能落差
- [ ] 展示 evidence-aware 方法相对更稳

### Demo Scenario 2：Evidence traceability case study

目标：

- 展示任意一个预测结果都能追溯到结构、来源、功能标签和 DOI

Checklist：

- [ ] 选 3-5 个高置信预测样本
- [ ] 展示其结构表示
- [ ] 展示对应 evidence type
- [ ] 展示原始来源数据库和 DOI
- [ ] 解释模型认为重要的 motif/linkage/modification

### Demo Scenario 3：Failure mode showcase

目标：

- 展示模型不是“全都能做”，而是在哪些条件下失败

Checklist：

- [ ] 选跨来源失败样本
- [ ] 标注失败原因
- [ ] 区分表示缺失、标签冲突、物种偏移、实验偏移
- [ ] 给出最小 KG 中的证据链截图或结构化输出

### Demo Scenario 4：Ranking use-case for candidate prioritization

目标：

- 展示该方法可以作为候选筛选器，而不是最终功能判定器

Checklist：

- [ ] 给定某一功能目标
- [ ] 输出 top-k 候选
- [ ] 标出高证据与低证据样本
- [ ] 展示为何这些样本被排前
- [ ] 强调这是 hypothesis generation，不是 biological proof

## 9. Figure Plan

### Figure 1: Teaser

- 左：glycan-centric setting 与 polysaccharide setting 的差别
- 中：random split vs cross-source split 的性能落差
- 右：我们的 evidence-aware 方法缩小该落差

### Figure 2: Pipeline

- 多源数据输入：DoLPHiN / CSDB / GlyTouCan
- 统一表示与 evidence schema
- 预测模型
- 最小 KG 追踪与解释层

### Figure 3: Benchmark statistics

- 标签分布
- 证据等级分布
- 来源数据库分布
- 物种/功能任务分布

### Figure 4: Main results

- 不同模型在 random split 和 cross-source split 上的对比

### Figure 5: Ablation + explanation

- 模块 ablation
- motif/linkage/modification importance

### Figure 6: Case studies

- 正例、反例、失败例
- 证据链追踪

## 10. Structured Checklists

### Story Checklist

- [ ] 任务定义足够窄
- [ ] 明确区分 glycan 与 polysaccharide
- [ ] 核心 claim 不超过 2 个
- [ ] 每个 claim 都有实验支撑
- [ ] fallback narrative 已定义

### Comparison Checklist

- [ ] baseline 覆盖 classical / sequence / graph
- [ ] 有 random split
- [ ] 有 cross-source split
- [ ] 有 cross-genus split
- [ ] 有 calibration 或 uncertainty 指标

### Ablation Checklist

- [ ] 每个核心模块可单独拿掉
- [ ] 每个 ablation 对应一个 claim
- [ ] 有 design-choice ablation
- [ ] 有 error analysis

### Demo Checklist

- [ ] 至少一个 stress test
- [ ] 至少一个 traceability demo
- [ ] 至少一个 failure case demo
- [ ] demo 和主 claim 直接相关

## 11. Fallback Narrative

如果最终 SOTA 提升不大，备选叙事不要改成“我们模型也很强”，而应改成：

- 我们提出了第一个可信的多糖结构-功能 benchmark
- 我们证明随机 split 会系统性高估性能
- 我们提供了 evidence-aware 和 traceable 的评测框架
- 我们识别了 glycan-to-polysaccharide transfer 的主要失败模式

这条 fallback 仍然是可发表的。

## 12. 下一步执行顺序

1. 先把 Figure 2 的 pipeline 草图画出来
2. 用 claim-to-experiment mapping 反推最少实验集
3. 先设计 ablation 表，再决定模型复杂度
4. 最后再写 introduction 和 method
