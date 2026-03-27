# 多糖论文规划：Pipeline Figure Sketch、Section Outline、Experiment Matrix

## 1. Pipeline Figure Sketch

目标不是解释全部细节，而是让审稿人一眼看到“这不是普通 glycan 预测流水线”。

## 1.1 Figure 2 总体布局

建议用 4-column 横向布局：

1. `Multi-source polysaccharide data`
2. `Canonicalization + evidence schema`
3. `Evidence-aware prediction model`
4. `Traceability + interpretation layer`

核心视觉原则：

- 左侧数据源多而杂
- 中间是本文第一个 novelty：统一表示与证据感知 schema
- 右中是第二个 novelty：evidence-aware modeling
- 最右是第三个 novelty：traceability / minimal KG / interpretable cases

## 1.2 Figure 2 草图

```text
+--------------------------------------------------------------------------------------+
|                             Figure 2. Overview Pipeline                              |
+--------------------------------------------------------------------------------------+

  [DoLPHiN]        [CSDB]         [GlyTouCan]
      |               |                |
      +---------------+----------------+
                      |
                      v
          +-----------------------------+
          | Raw polysaccharide records  |
          | structure / source / label  |
          | DOI / evidence / metadata   |
          +-----------------------------+
                      |
                      v
      +----------------------------------------------+
      | Canonicalization and evidence schema         |
      | - canonical IUPAC / optional WURCS           |
      | - repeating-unit / branching / modification  |
      | - molecular-weight features                  |
      | - evidence level: in vitro / animal / clinical |
      | - source id / provenance fields              |
      +----------------------------------------------+
                      |
          +-----------+------------+
          |                        |
          v                        v
  +------------------+     +----------------------+
  | Sequence branch  |     | Graph branch         |
  | Transformer      |     | GNN / SweetNet-style |
  +------------------+     +----------------------+
          |                        |
          +-----------+------------+
                      |
                      v
      +----------------------------------------------+
      | Evidence-aware predictor                     |
      | - task heads                                 |
      | - evidence weighting                         |
      | - source-aware training                      |
      | - calibrated outputs                         |
      +----------------------------------------------+
                      |
          +-----------+------------+
          |                        |
          v                        v
  +------------------+     +----------------------+
  | Benchmark eval   |     | Minimal polysaccharide KG |
  | random / source  |     | structure-label-DOI trace |
  | / genus splits   |     | error analysis            |
  +------------------+     +----------------------+
```

## 1.3 Figure 2 每块要强调什么

### Block A: Multi-source input

强调：

- 不是单一数据库任务
- 多糖数据来自异构来源
- 数据问题本身就是研究问题的一部分

不要画得太复杂：

- 只保留 3 个源：DoLPHiN、CSDB、GlyTouCan
- 不要把全部数据库都塞进去

### Block B: Canonicalization + evidence schema

这是 Figure 2 最该突出的模块。

必须显式出现的关键词：

- `canonical representation`
- `repeating unit`
- `modification`
- `molecular weight`
- `evidence level`
- `provenance`

### Block C: Predictor

强调：

- 不是单纯一个模型
- 是“多糖特有表示 + evidence-aware training”的组合

建议画成双分支：

- sequence branch
- graph branch

这样可以自然支撑后文 comparisons。

### Block D: Traceability layer

这是区别于普通 benchmark 论文的重要视觉点。

必须画出来：

- prediction
- evidence chain
- error analysis
- case review

因为这会直接支撑“可信”这个叙事。

## 1.4 Figure 1 Teaser 草图

Figure 1 不讲方法，直接讲问题和结果。

建议三联图：

```text
[Panel A] glycan vs polysaccharide task mismatch
[Panel B] random split inflates performance
[Panel C] our evidence-aware setting is more robust under source shift
```

### Panel A

- 左：常规 glycan 数据，结构较短、标签较规则
- 右：polysaccharide，重复单元、修饰、分子量和证据异质

### Panel B

- 一个柱状图或折线图
- random split 结果高
- leave-one-source-out 显著下降

### Panel C

- 我们的方法 vs naive transfer
- 在 cross-source split 上相对更稳

## 2. Section Outline

这部分按能直接写成 paper 的顺序组织。

## 2.1 Title

`Polysaccharide Structure-Function Benchmark and Evidence-Aware Modeling`

备选：

- `Beyond Glycan Transfer: A Benchmark and Evidence-Aware Framework for Polysaccharide Structure-Function Prediction`
- `Toward Reliable Polysaccharide Structure-Function Prediction with Evidence-Aware Benchmarking`

## 2.2 Abstract Outline

### Sentence 1: problem importance

多糖结构-功能关系重要，但机器学习研究滞后。

### Sentence 2: gap

现有糖科学方法主要围绕 glycan，缺少面向长链多糖的统一 benchmark、可信标签建模与跨来源评测。

### Sentence 3: what we do

本文构建一个可复现的多糖结构-功能 benchmark，并提出 evidence-aware modeling framework。

### Sentence 4: technical components

我们统一多源结构表示、编码多糖特有结构因素，并将证据等级与来源信息纳入训练和评测。

### Sentence 5: key results

实验表明 random split 会系统性高估性能，而 evidence-aware 建模在 cross-source 泛化、校准和解释性上更可靠。

### Sentence 6: significance

该工作为多糖机器学习提供了更可信的评测基线、数据资源和可追溯分析框架。

## 2.3 Introduction Outline

### Paragraph 1

多糖在食品、免疫调节、材料和药用中重要，但结构复杂、表征难、数据碎片化。

### Paragraph 2

糖科学机器学习已有进展，但大多数针对 glycan，不适用于长链多糖真实任务。

### Paragraph 3

直接迁移这些方法的问题：

- 表示缺失
- 标签异质
- 来源偏移
- 随机划分乐观偏差

### Paragraph 4

本文核心观点：当前瓶颈不只是模型，而是 benchmark 和 evidence modeling 缺失。

### Paragraph 5

本文贡献列表：

1. benchmark
2. evidence-aware modeling
3. systematic transfer study
4. minimal KG for traceability

## 2.4 Related Work Outline

分 4 小节：

### RW1. Glycan machine learning

- SweetNet
- glyBERT
- GlycanML / GlycoGym

### RW2. Polysaccharide data resources

- DoLPHiN
- CSDB
- GlyTouCan
- PolySac3DB

### RW3. Evidence-aware / noisy-label learning

- 强调本文不是纯噪声学习论文，但借鉴其思想

### RW4. Scientific knowledge graphs / provenance-aware data integration

- 说明本文 KG 是最小 traceability layer，不是 full biomedical KG

## 2.5 Method Outline

### 4.1 Task Definition

- 输入
- 输出
- 任务形式
- split 定义

### 4.2 Data Construction

- data sources
- schema
- canonicalization
- evidence levels

### 4.3 Representations

- sequence representation
- graph representation
- polysaccharide-specific attributes

### 4.4 Evidence-Aware Modeling

- sample weighting
- source-aware features
- multi-task heads
- calibration

### 4.5 Minimal KG and Traceability

- node types
- edge types
- provenance chain
- case review usage

## 2.6 Experiments Outline

### 5.1 Experimental Setup

- datasets
- splits
- metrics
- training details

### 5.2 Main Comparison

- random split
- cross-source split
- cross-genus split

### 5.3 Ablation Study

- core module ablations
- representation ablations
- evidence strategy ablations

### 5.4 Calibration and Reliability

- ECE / Brier / calibration curves

### 5.5 Case Studies

- traceability
- failure mode
- ranking scenario

## 2.7 Discussion Outline

### Discussion 1

为什么 random split 在这个问题上误导性很强。

### Discussion 2

glycan 到 polysaccharide transfer 的边界在哪里。

### Discussion 3

当前 benchmark 仍然有什么限制：

- 标签噪声
- 结构缺失
- 功能定义粗糙
- 数据源规模有限

## 3. Experiment Matrix

## 3.1 Paper Information

- Paper title: `Polysaccharide Structure-Function Benchmark and Evidence-Aware Modeling`
- Core contributions:
  - benchmark
  - evidence-aware modeling
  - transfer failure analysis
  - minimal KG traceability
- Target venue:
  - 首选：bioinformatics / Briefings in Bioinformatics / Database / Journal of Cheminformatics 风格期刊
  - 若偏方法短文：MLSB / AI for Science workshop
- Submission mode:
  - 先按期刊长文组织，更稳

## 3.2 Datasets

| # | Dataset | Role | Why Include |
|---|---------|------|-------------|
| 1 | DoLPHiN-derived dataset | main supervised dataset | 最直接的多糖结构-功能标签来源 |
| 2 | CSDB-linked subset | metadata / structure enrichment | 补结构细节、NMR、来源信息 |
| 3 | GlyTouCan-linked subset | ID anchor / representation normalization | 做跨库锚点和 canonical mapping |

## 3.3 Tasks

| # | Task | Type | Priority |
|---|------|------|----------|
| 1 | 功能多标签分类 | classification | P0 |
| 2 | 单一高质量功能子任务分类 | classification | P0 |
| 3 | 证据等级感知预测 | classification / calibration | P1 |
| 4 | 候选排序任务 | ranking | P1 |

说明：

- P0 任务必须能支撑主稿
- P1 任务可用于增强可信度和 demo

## 3.4 Metrics

| # | Metric | Direction | Why Needed |
|---|--------|-----------|------------|
| 1 | AUROC | up | 标准分类指标 |
| 2 | AUPRC | up | 处理标签不平衡 |
| 3 | Macro-F1 | up | 评估多类别平衡性能 |
| 4 | ECE | down | 衡量校准 |
| 5 | Brier Score | down | 衡量概率质量 |
| 6 | Hits@k / Recall@k | up | 支撑 ranking scenario |

## 3.5 Baselines

| # | Method | Category | Why Include |
|---|--------|----------|-------------|
| 1 | Majority baseline | naive | lower bound |
| 2 | Logistic Regression | classical | 简单强 baseline |
| 3 | XGBoost / LightGBM | classical | 手工特征强基线 |
| 4 | n-gram sequence model | sequence | 低成本序列表达 |
| 5 | Transformer-IUPAC | sequence | 主序列 baseline |
| 6 | Transformer-WURCS | sequence | 测表示差异 |
| 7 | GCN / GIN | graph | 标准图模型 |
| 8 | SweetNet-style model | graph | glycan 迁移代表方法 |

## 3.6 Splits

| # | Split | Purpose | Priority |
|---|-------|---------|----------|
| 1 | Random split | 与既有习惯对齐 | P0 |
| 2 | Leave-one-source-out | 测来源偏移 | P0 |
| 3 | Leave-one-genus-out | 测生物来源泛化 | P0 |
| 4 | Time-aware / DOI-aware split | 如果数据允许，测信息泄漏 | P2 |

## 3.7 Core Comparisons

| Exp ID | Experiment | Output |
|--------|------------|--------|
| C1 | all baselines on random split | Main Table 1 |
| C2 | all baselines on source split | Main Table 2 |
| C3 | best methods on genus split | Main Table 2 or appendix |
| C4 | calibration comparison | Reliability Table |

## 3.8 Core Ablations

| Abl ID | Configuration | Supports Which Claim |
|--------|---------------|----------------------|
| A1 | full model | reference |
| A2 | w/o evidence weighting | evidence-aware claim |
| A3 | w/o source encoding | source-shift claim |
| A4 | w/o MW feature | polysaccharide-specific feature claim |
| A5 | w/o modification feature | polysaccharide-specific feature claim |
| A6 | w/o repeating-unit encoding | polysaccharide-specific representation claim |
| A7 | single-task instead of multi-task | training design claim |
| A8 | no KG-derived traceability layer | traceability claim |

## 3.9 Design-choice Tables

### Table D1: Representation choice

| Variant | Goal |
|---------|------|
| canonical IUPAC | default |
| WURCS | check robustness |
| concatenated feature string | simple baseline |

### Table D2: Evidence weighting strategy

| Variant | Goal |
|---------|------|
| no weighting | lower bound |
| hard weighting | simple |
| soft weighting | default candidate |

### Table D3: Multi-task strategy

| Variant | Goal |
|---------|------|
| single-task | compare |
| shared trunk + task heads | default |
| task-specific towers | optional |

## 3.10 Demo / Case Studies

| Demo ID | Scenario | Figure / Output |
|---------|----------|-----------------|
| D1 | random vs source shift | Figure 1 / Figure 4 |
| D2 | traceable positive case | Figure 6 |
| D3 | failure mode case | Figure 6 |
| D4 | candidate ranking scenario | Figure 6 or appendix |

## 3.11 Claim-to-Experiment Matrix

| Claim ID | Claim Sentence | Evidence | Priority |
|----------|---------------|----------|----------|
| CL1 | 我们构建了第一个可复现的多糖结构-功能 benchmark | dataset stats + schema + data card | Must |
| CL2 | glycan-centric baselines 在 polysaccharide cross-source generalization 上不足 | C1 + C2 + C3 | Must |
| CL3 | evidence-aware modeling 提升可靠性和校准 | C4 + A2 | Must |
| CL4 | 多糖特有结构特征对预测有实质贡献 | A4 + A5 + A6 | Must |
| CL5 | 最小 KG 提供可追溯和可复核案例分析 | D2 + D3 | Should |

## 4. 最小可执行实验集

如果时间紧，只保留以下组合，也足以支撑主稿：

### Must-have

- dataset statistics
- random split vs leave-one-source-out
- 3 类 baseline：classical / sequence / graph
- evidence weighting ablation
- repeating-unit / modification / MW ablation
- 2 个 case studies：一个正例，一个失败例

### Good-to-have

- leave-one-genus-out
- calibration curves
- ranking demo
- KG-derived feature comparison

### Can drop first

- WURCS 全面实验
- 时间切分
- 大规模多任务扩展
- 复杂 hierarchical graph architecture

## 5. 写作顺序

按 `paper-planning` 的原则，这篇论文最稳的顺序不是从 abstract 开始，而是：

1. Figure 2 pipeline 定稿
2. Main Table 1 / 2 结构先定
3. Ablation Table 结构先定
4. Introduction outline
5. Method
6. Experiments
7. Abstract

## 6. 当前最优下一步

直接进入实现时，优先顺序应为：

1. 固化 schema 和 split 定义
2. 实现 classical / sequence / graph 三类 baseline
3. 预留 evidence weighting 接口
4. 预留 traceability 输出格式
