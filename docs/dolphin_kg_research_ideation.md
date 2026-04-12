# DoLPHiN Knowledge Graph Research Ideation

## Step 1. Long-Term Research Goal

长期目标不是单纯做一个多糖数据库，而是构建一个“结构-来源-证据-功能-疾病”一体化的多糖知识图谱与图学习平台，使其能够：

- 从异构证据中组织可查询知识
- 从图结构中发现新的结构功能规律
- 为多糖功能预测提供可解释推理路径
- 反向提出“值得验证的候选多糖”与“潜在作用疾病”

如果这个方向被完全做成，最终形态应该是：

- 一个可扩展的 polysaccharide KG
- 一个图谱增强的结构功能预测基准
- 一个面向多糖发现的假说生成系统

这条路线比单纯做分类器更有延展性，能持续产出多篇工作。

## Step 2. Literature Tree

这里先基于当前项目与领域常见路线，构造一个工作型 literature tree，用于选题而不是伪装成完整综述。

### 2.1 Novelty Tree

#### Type 1 milestone tasks

1. 多糖数据库与结构资源构建
2. 多糖结构-功能预测
3. 糖类/糖聚合物知识图谱构建与整合
4. 图谱增强的候选发现与机制推断

#### Type 2 paradigm shifts

1. 从人工整理数据库到自动化网页抓取和 ETL
2. 从手工特征分类到序列/图表示学习
3. 从单表监督学习到异构知识图谱建模
4. 从相关性预测到带证据链的可解释发现

#### Type 3 modules

1. 单糖组成解析
2. 糖苷键 motif 规范化
3. 功能标签统一映射
4. 疾病实体对齐
5. 文献 DOI 溯源
6. KG embedding / GNN / link prediction

#### Type 4 incremental work

1. 在现有表格数据上换一个分类器
2. 单纯把 Neo4j 当可视化后端
3. 只做图嵌入而不解决证据与实体规范化问题

### 2.2 Challenge-Insight Tree

#### Challenge A. 多糖结构表达不标准

已知 insight：

- 先抽取可稳定解析的中层结构信号，而不是一步到位追求完整糖链图
- 用 `Monosaccharide + GlycosidicBond + StructuralMotif` 三层表示替代单一字符串

#### Challenge B. 功能和疾病是弱监督、多标签、异构粒度

已知 insight：

- 拆分功能节点与疾病节点，避免直接把标签当最终监督目标
- 用图谱邻域和证据边缓解标签稀疏

#### Challenge C. 多糖研究强调可解释性

已知 insight：

- 图谱路径天生比黑盒分类器更适合解释
- `Polysaccharide -> Motif -> Function -> Disease` 是天然解释链

#### Challenge D. 现有数据证据层不完整

已知 insight：

- 第一阶段先保证 provenance 完整
- 第二阶段再从 DOI 文献补实验上下文，逐步增强证据节点

#### Challenge E. 领域贡献容易落到“又一个预测器”

已知 insight：

- 真正的高价值问题应是“新 failure case + 新数据表示 + 可验证发现”
- 图谱贡献应超越性能，强调可检索、可解释、可迁移

## Step 3. Problem Selection

按照 `research-ideation` 的标准，最关键的问题是：哪类图谱工作真正值得做，而不是只把表导成图库。

### Problem Candidate 1

`DoLPHiN polysaccharide KG construction`

问题定义：
把 DoLPHiN 从监督学习样本集扩展成可追踪异构 KG。

价值：
高，但偏资源型工作，单独成文时 novelty 容易被认为不足。

well-established solution check：

- Level 2 偏强
- 因为“数据库转 KG”本身是常规工程套路

结论：
应该做，但不应作为唯一论文贡献。

### Problem Candidate 2

`KG-enhanced polysaccharide function prediction`

问题定义：
利用图谱中的来源、结构片段、疾病、文献等异构关系，提升多糖多标签功能预测，并提供解释路径。

价值：
很高，且直接继承当前仓库已有的分类 benchmark。

well-established solution check：

- 对一般生物医学 KG 是 Level 2
- 对“DoLPHiN 这一类多糖结构功能数据”更接近 Level 3

结论：
值得做，是最稳的第一篇图谱应用方向。

### Problem Candidate 3

`KG-based candidate discovery for under-studied polysaccharides`

问题定义：
面向标签稀缺或功能未知的多糖，利用图谱链路预测潜在功能或疾病关联，产生待验证假说。

价值：
高，且比常规分类更接近“发现”。

well-established solution check：

- 在一般药物/蛋白 KG 中接近 Level 2
- 在多糖领域更接近 Level 3

结论：
值得做，但要依赖较扎实的 KG v0。

### Problem Candidate 4

`Evidence-aware mechanistic motif discovery`

问题定义：
通过 motif 子图与疾病/功能的局部结构模式，发现可解释的“结构片段-功能”机制规律。

价值：
非常高。

well-established solution check：

- 对多糖领域接近 Level 4

结论：
高风险高回报，适合作为第二阶段研究而不是第一阶段主线。

## Selected Problem

首选问题应是：

`构建 DoLPHiN 多糖知识图谱，并以此实现图谱增强的多标签功能预测与候选发现。`

原因：

1. 和现有 `polysaccharidesdb` benchmark 连续性最强
2. 不会把工作停留在资源工程层面
3. 既能做定量实验，也能做可解释案例
4. 后续很自然扩展到机制 motif 与新候选发现

## Step 4. Solution Design

### Research Direction A

`KG-augmented multi-label function prediction`

#### Core idea

把每条多糖样本从平面特征向量，升级为异构邻域子图：

- 多糖节点
- 来源节点
- 单糖节点
- 糖键节点
- 疾病节点
- 文献节点

模型输入不再只来自原始结构文本，而来自：

- 表格特征
- 结构子图特征
- 邻域聚合表示
- 路径级解释

#### Why it is better than the current baseline

当前仓库里的主线仍偏样本级分类；它能学到“这个样本像什么”，但较难表达：

- 共享来源但不同结构的差异
- 共享结构 motif 但不同疾病定位的关系
- 文献与功能之间的证据链

KG 能把这些中介节点显式化。

#### Proposed modeling stack

1. 先做图谱规则与手工 meta-path 特征
2. 再做 hetero graph neural network
3. 最后做 node classification + link prediction 联合训练

#### First validation

- 与当前 `logistic / random_forest / graph_gcn / evidence-aware` 基线比较
- 任务 1：多标签功能预测
- 任务 2：留来源外泛化
- 任务 3：按 DOI 分组的 harder split

### Research Direction B

`KG link prediction for functional hypothesis generation`

#### Core idea

将已知 `Polysaccharide -> Function` 视为部分可观测边，预测缺失边。

输出不是“最终真理”，而是：

- 高置信新功能候选
- 可解释邻域路径
- 优先实验验证列表

#### Novelty source

不只是用 KGE 做 link prediction，而是把多糖特有结构实体引入图谱，解决领域内“样本少、标签稀、功能多标签”的问题。

#### First validation

- masked edge prediction
- retrospective recovery：隐藏一部分已知功能边，看能否找回
- case studies：找出现阶段标签为 `unknown` 或长尾功能的多糖

### Research Direction C

`Motif-centric subgraph mining for interpretable mechanism discovery`

#### Core idea

从 `Monosaccharide + Bond + Branching` 组合出的结构子图里，挖掘与特定功能显著相关的 motif。

重点不是只报频率，而是报：

- motif 子图
- 对应来源生物群
- 共现疾病语境
- 支持文献 DOI

#### Why it matters

这是最接近领域科学问题的一层，能把“图谱应用”从信息学工作推到可解释生物发现。

#### First validation

- 对 `immunomodulatory`、`antioxidant`、`antidiabetic` 三类高频功能先做
- 与简单频次统计做比较
- 人工检查 top motifs 是否符合领域常识

## Step 5. Validate And Iterate

## Phase 1

先证明 KG 值得存在。

交付：

- KG v0
- 节点/边统计
- 解析质量报告
- 10 个查询案例

## Phase 2

先做最稳的图谱应用。

交付：

- KG-enhanced function prediction benchmark
- 与现有 baselines 的严格比较
- 路径解释案例

## Phase 3

再做发现型任务。

交付：

- link prediction 候选列表
- motif 子图发现
- 候选多糖 case studies

## Three Best Research Directions

如果只保留三个最值得立即推进的方向，我建议是：

### 1. KG-enhanced multi-label function prediction

最稳、最接近当前代码资产、最容易形成可发表主线。

### 2. KG link prediction for under-studied polysaccharides

最像“发现”任务，容易做出高价值案例。

### 3. Motif-centric interpretable subgraph mining

最有科学味道，适合做第二阶段拔高。

## What Not To Do

以下方向现在不值得优先做：

### 1. 只做 Neo4j 可视化

工程上有用，但研究价值太弱。

### 2. 只把现有字段拼成 triples 然后跑通用 KGE

这会落成“通用方法套领域数据”，贡献不够扎实。

### 3. 一上来就追求完整糖链原子级图表示

当前数据噪声和编码问题还没清完，直接冲这一层会拖慢主线。

## Concrete Next Experiments

### Experiment 1. KG v0 build

目标：
把 DoLPHiN 导成标准化图谱。

最小输出：

- nodes CSV
- edges CSV
- graph statistics

### Experiment 2. Meta-path baseline

目标：
不用复杂 GNN，先验证图谱邻域是否有增益。

做法：

- 统计 `Poly-Organism-Poly`
- `Poly-Monosaccharide-Poly`
- `Poly-Bond-Poly`
- `Poly-Disease-Poly`
  邻域特征

然后拼接到现有分类器。

### Experiment 3. Heterogeneous GNN baseline

目标：
验证 hetero message passing 是否优于当前 graph baseline。

### Experiment 4. Functional link prediction

目标：
从隐藏边恢复中检验图谱发现能力。

## Output Artifact

这一轮 ideation 最终收敛为一句话：

`不要把 DoLPHiN 仅仅做成一个多糖分类数据集，而要把它升级成以多糖为中心、连接来源-结构片段-文献-疾病-功能的异构知识图谱，并围绕图谱增强预测、链路发现和 motif 解释三条路线展开研究。`

这条路线既能承接当前项目，也能把后续工作从“样本级预测”抬升到“知识组织 + 可解释发现”。
