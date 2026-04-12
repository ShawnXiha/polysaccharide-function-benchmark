# Revision Improvement Plan v1

## Goal

将当前稿件从“有发表潜力但实验与写法尚未完全收口的中后期版本”，推进到“可针对 `Database` / `BMC Bioinformatics` / `Bioinformatics Advances` 做定向投稿”的稳定投稿稿。

当前稿件最合理的定位不是“提出了一个全面领先的新模型”，而是：

1. 基于 DoLPHiN 构建了一个可检索、可评测、可追溯的多糖知识图谱资源。
2. 证明在当前图上，`interpretable meta-path retrieval` 是 strongest clean baseline。
3. 证明 ontology 不是普适增益，而是在 `disease-aware upper-bound` 设定里对长尾标签提供稳定补益。

本提高计划围绕这个真实贡献展开，目标是：

- 强化实验协议与可复现性
- 消除数值与统计解释歧义
- 增加方法和生物学层面的说服力
- 让标题、摘要、引言和结果组织与真实贡献完全对齐

---

## Revision Strategy

采用“先补硬伤，再补亮点，最后重写叙事”的顺序：

1. 先补方法细节、数据构建细节、实验协议、数值一致性。
2. 再补 baseline、ablation、case study。
3. 最后根据目标期刊改标题、摘要、引言、投稿定位。

这样做的原因是：当前稿件最大的风险不是缺故事，而是审稿人会先质疑实验协议、数值口径和可复现性。

---

## Work Package 1: 方法与数据构建细节补全

### Objective

让审稿人能够明确理解：

- DoLPHiN 原始记录如何转成 KG
- 哪些字段是自动规范化，哪些带人工规则
- 图中的节点、边、缺失值、重复记录如何处理
- ontology hierarchy 如何构建

### Required Additions

1. 在 `Methods` 中新增 `KG Construction and Normalization` 小节。
2. 明确写出：
   - source fields
   - normalization targets
   - entity merge rules
   - missing-value policy
   - provenance retention strategy
3. 单独描述 function hierarchy 的来源、人工规则、parent/child 定义原则。
4. 在 supplementary 或 appendix 中补 schema 表和 normalization examples。

### Expected Artifacts

- 主稿新增一节方法细化文本
- 结构化 schema 表
- 2--3 个 normalization case examples
- ontology hierarchy 构建说明

### Acceptance Criteria

- 读者可复原 KG 构建逻辑
- baseline 不会因“图构造不透明”被质疑
- hierarchy 不会被认为是 ad hoc trick

---

## Work Package 2: 实验协议标准化与可复现性补强

### Objective

让实验部分达到“协议完整、泄漏控制明确、统计单元清楚”的标准。

### Required Additions

1. 明确 train/validation/test 切分规则。
2. 明确 filtered ranking 的计算对象和 multi-label 处理方式。
3. 明确 head/mid/tail 阈值定义及其依据。
4. 检查并写清：
   - 是否存在同一 polysaccharide 的跨集合信息泄漏
   - publication / organism / disease 辅助信息是否可能形成过强泄漏
5. 对 paired significance：
   - 写清 seed-level paired setup
   - 写清 edge-level paired unit
   - 写清 one-sided 与 two-sided test 的使用原因

### Expected Artifacts

- 主稿实验协议补全文本
- supplementary 中的 evaluation protocol subsection
- 统计检验说明表

### Acceptance Criteria

- 审稿人能回答“你的统计单位是什么”
- 能清楚解释为什么使用 filtered ranking
- 能解释 clean 与 disease-aware 为何是两种不同 scientific question

---

## Work Package 3: 数值口径统一与统计解释修正

### Objective

清除当前稿件中最容易被抓的“数字不一致”和“统计表述不精确”问题。

### Known Issues To Resolve

1. tail micro filtered Hits@3：
   - tuned split: `0.1667 -> 0.3333`
   - paired pooled evaluation: `0.0552 -> 0.1021`
   必须明确分别对应什么协议。
2. Hits@5：
   - Table 2: `0.938 / 0.939`
   - Table 3: `0.9366 / 0.9366`
   必须明确 split-level vs pooled-seed statistics。
3. filtered MRR：
   - global delta 很小，但 paired test 显著
   - 不能再写成笼统的 “globally neutral” 而不解释 effect size vs significance。

### Required Changes

1. 所有表格标题中明确：
   - single tuned split
   - pooled paired seed evaluation
2. 在正文增加一句解释：
   - “single-split result” 与 “paired pooled significance result” 不应直接横向比较。
3. 改写统计结果语言：
   - 把 “neutral” 改成 “negligible in effect size, though statistically detectable under paired testing”

### Expected Artifacts

- 修订版 Table 2 / Table 3
- 正文统计解释更新
- figure caption 中标注 metric source

### Acceptance Criteria

- 不再出现“看起来矛盾”的数字
- 统计解释与效应量解释一致

---

## Work Package 4: Baseline 与 Ablation 增强

### Objective

让“meta-path retrieval > current GNN”这个结论更可信，而不是像“GNN 没调好”。

### Priority Additions

1. 补更标准的非神经检索/分类 baseline：
   - logistic regression or linear classifier on explicit graph features
   - shallow MLP on the same handcrafted features
2. 对 hetero GNN 的失败进行更可验证的 ablation：
   - stronger node features vs weak node features
   - disease edges on/off
   - meta-path features injected vs not injected
3. 如果算力允许，补一个更标准的 graph baseline：
   - GraphSAGE-style or RGCN-style simplified variant

### Expected Artifacts

- 新 baseline 结果表
- 失败原因 ablation 表
- 一段“why retrieval wins” 的更强实证说明

### Acceptance Criteria

- 审稿人不容易再说 “you did not give GNNs a fair chance”
- retrieval 更强的结论由多组对照支撑

---

## Work Package 5: 生物学案例分析

### Objective

让文章不只是一篇 bioinformatics benchmark 稿，而是能让 glycobiology / polysaccharide 读者看到实际解释价值。

### Required Additions

选择 2--4 个 case studies，分别覆盖：

1. ontology propagation 成功救回 tail label 的例子
2. clean retrieval 成功但 ontology 无增益的例子
3. ontology 失败或误导的反例

### Each Case Should Explain

- query polysaccharide 的核心结构/来源特征
- baseline top candidates vs ontology-adjusted top candidates
- parent/child hierarchy 如何改变排序
- 对应 organism / monosaccharide / bond / disease 证据
- biological plausibility or uncertainty

### Expected Artifacts

- 主稿或 supplementary 中的 case study figure/table
- 失败案例分析段落

### Acceptance Criteria

- ontology gain 不再只是一个抽象统计数字
- 读者能看到 tail gain 的局部机制

---

## Work Package 6: 叙事收束与标题摘要重写

### Objective

让标题、摘要和引言与真实贡献一致，避免“题目像方法主打，正文其实是资源 + benchmark + tail supplement”的错位。

### Current Problem

当前稿件容易让人第一眼以为：

- 主角是 ontology-aware retrieval 方法本身

但实际上更准确的主角是：

- DoLPHiN-derived typed evidence KG
- interpretable retrieval benchmark
- ontology as tail-sensitive supplementary mechanism

### Recommended Narrative

推荐将主叙事固定为：

> We contribute a DoLPHiN-derived typed evidence KG and a controlled benchmark.  
> On the current graph, interpretable retrieval is the strongest clean baseline.  
> Ontology is not a universal gain, but provides stable tail-sensitive improvement in the disease-aware upper-bound setting.

### Title Revision Direction

避免把 ontology 放成唯一主语。

更合适的标题方向：

1. `A DoLPHiN-Derived Polysaccharide Knowledge Graph for Interpretable Function Retrieval and Tail-Sensitive Ontology Support`
2. `Interpretable Function Retrieval on a DoLPHiN-Derived Polysaccharide Knowledge Graph with Tail-Sensitive Ontology Propagation`
3. `From DoLPHiN to a Typed Evidence Graph: Function Retrieval and Ontology-Aware Tail Enhancement for Natural Polysaccharides`

### Expected Artifacts

- 新标题候选 3--5 个
- 新摘要
- 新引言首段和贡献段

### Acceptance Criteria

- 标题不再夸大 ontology 主角地位
- 摘要不再给人“overall SOTA method paper”的预期

---

## Work Package 7: 期刊定向版本化

### Objective

根据不同期刊口味，提前准备两个版本。

### Version A: Database / Resource-Oriented

适用目标：

- `Database`

强调：

- resource value
- schema
- provenance
- reusability
- query / benchmark utility

### Version B: Bioinformatics Method-Oriented

适用目标：

- `BMC Bioinformatics`
- `Bioinformatics Advances`

强调：

- benchmark design
- retrieval vs GNN insight
- tail-sensitive ontology effect
- reproducible evaluation protocol

### Acceptance Criteria

- 可以按目标期刊快速切换摘要、标题、引言开头和 discussion emphasis

---

## Priority Order

### Tier 1: 必须先做

1. Work Package 1
2. Work Package 2
3. Work Package 3

### Tier 2: 决定稿件说服力

4. Work Package 4
5. Work Package 5

### Tier 3: 投前定向

6. Work Package 6
7. Work Package 7

---

## Recommended 2-Week Execution Plan

### Days 1--3

- 补方法细节
- 补实验协议
- 统一数值口径

### Days 4--7

- 跑新增 baseline / ablation
- 重做主结果表

### Days 8--10

- 写 case studies
- 做 case figure/table

### Days 11--12

- 重写标题、摘要、引言和结果叙事

### Days 13--14

- 分叉出 `Database` 版和 `Bioinformatics` 版
- 最终 self-review

---

## Final Success Criteria

当以下条件满足时，稿件进入较稳妥投稿状态：

1. 数据构建与 ontology 构建过程可复现。
2. 所有统计数字口径一致且解释无歧义。
3. retrieval 胜过 GNN 的结论有足够对照支撑。
4. ontology tail gain 有局部案例支持，不只是全局统计。
5. 标题、摘要、引言与真实贡献完全一致。
6. 能明确区分 resource-led submission 与 method-led submission 两条投稿路线。

---

## Suggested Immediate Next Step

从 `Work Package 1 + Work Package 2 + Work Package 3` 联合开始，因为它们直接决定这篇稿子是否会在审稿第一轮被“实验不完整 / 数字不一致 / 协议不清楚”卡住。
