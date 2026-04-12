# DoLPHiN Knowledge Graph Design v0

## Goal

将 `D:\projects\paper_writing\polysaccharidesdb` 中抓取的 DoLPHiN 数据，从“监督学习样本表”扩展为“可追踪、可查询、可推理”的多糖知识图谱，用于：

- 多糖结构-功能-来源-疾病的可解释检索
- 图谱增强的结构功能预测
- 假说生成与候选多糖发现
- 文献证据追踪与跨来源数据对齐

## What The Current Data Already Supports

基于 `dataset_dolphin_only.jsonl` 与 `dolphin_raw_records.jsonl` 的抽样统计：

- 记录数约 `5078`
- 功能标签约 `66`
- 来源生物约 `1499`
- 单糖类型约 `23`
- 糖苷键模式约 `323`
- 疾病字符串约 `107`
- DOI 覆盖约 `5071 / 5078`
- `related_diseases` 非空约 `2690 / 5078`

这意味着第一版图谱不需要等待新增数据，已经可以构建以下核心子图：

- `Polysaccharide -> Function`
- `Polysaccharide -> Disease`
- `Polysaccharide -> Organism`
- `Polysaccharide -> Monosaccharide`
- `Polysaccharide -> GlycosidicBond`
- `Polysaccharide -> Publication`

## Core Design Principle

现有表中的很多字段还是自由文本。图谱扩展的关键不是把 JSONL 原样导入图库，而是把文本拆成规范实体，同时保留原始证据字符串。

所以每条关系都建议有两层：

1. `normalized layer`
   标准化后的实体与关系，用于查询、学习和推理。
2. `traceability layer`
   原始字符串、来源页面、DOI、解析规则、置信度，用于审计和回溯。

## Proposed Node Types

### 1. `Polysaccharide`

主实体，来自 DoLPHiN 记录。

关键属性：

- `poly_id`
- `source_record_id`
- `name`
- `raw_representation`
- `canonical_representation`
- `mw_or_range_raw`
- `mw_kda_min`
- `mw_kda_max`
- `branching_raw`
- `main_chain_raw`
- `side_chain_raw`
- `source_db`

### 2. `Organism`

来源生物实体。

关键属性：

- `organism_name_raw`
- `organism_name_norm`
- `taxon_rank_guess`
- `taxonomy_id`
- `kingdom`

### 3. `Monosaccharide`

单糖实体。

关键属性：

- `mono_name_raw`
- `mono_name_norm`
- `mono_family`

### 4. `GlycosidicBond`

糖苷键或结构 motif 实体。

关键属性：

- `bond_text_raw`
- `anomericity`
- `donor_residue`
- `acceptor_position`
- `bond_signature`

### 5. `StructuralMotif`

比单个键更高层的结构单元，如 `beta-glucan backbone`、`RG-I-like`、`arabinogalactan-like`。

关键属性：

- `motif_name`
- `motif_rule`
- `motif_source`

### 6. `Function`

功能标签实体。

关键属性：

- `function_name_norm`
- `function_group`
- `is_dolphin_native_label`

### 7. `Disease`

疾病或 ICD-11 相关条目。

关键属性：

- `disease_name_raw`
- `disease_name_norm`
- `icd11_code`
- `disease_group`

### 8. `Publication`

文献实体。

关键属性：

- `doi`
- `title`
- `year`
- `journal`

第一版至少保留 `doi`，后续再补元数据抓取。

### 9. `Evidence`

证据节点，用来连接功能、疾病、实验层级。

关键属性：

- `evidence_type`
- `evidence_level`
- `assay_text`
- `raw_support_text`
- `confidence`

DoLPHiN 目前 `evidence_type` 基本是 `unknown`，所以这类节点在 v0 可以先弱化，但 schema 应该先留。

### 10. `DatabaseRecord`

来源记录节点，用于跨数据库对齐。

关键属性：

- `source_db`
- `source_record_id`
- `detail_url`
- `license`

## Proposed Edge Types

### Identity / provenance

- `(:Polysaccharide)-[:HAS_RECORD]->(:DatabaseRecord)`
- `(:DatabaseRecord)-[:SUPPORTED_BY]->(:Publication)`

### Source biology

- `(:Polysaccharide)-[:ISOLATED_FROM]->(:Organism)`

### Structure

- `(:Polysaccharide)-[:HAS_MONOSACCHARIDE {ratio_percent}]->(:Monosaccharide)`
- `(:Polysaccharide)-[:HAS_GLYCOSIDIC_BOND]->(:GlycosidicBond)`
- `(:Polysaccharide)-[:HAS_MOTIF]->(:StructuralMotif)`
- `(:Polysaccharide)-[:HAS_BRANCHING_PATTERN]->(:StructuralMotif)`

### Function / disease

- `(:Polysaccharide)-[:ASSOCIATED_WITH_FUNCTION]->(:Function)`
- `(:Polysaccharide)-[:ASSOCIATED_WITH_DISEASE]->(:Disease)`
- `(:Function)-[:RELEVANT_TO_DISEASE]->(:Disease)`

### Evidence

- `(:Polysaccharide)-[:SUPPORTED_BY_EVIDENCE]->(:Evidence)`
- `(:Evidence)-[:CLAIMS_FUNCTION]->(:Function)`
- `(:Evidence)-[:TARGETS_DISEASE]->(:Disease)`
- `(:Evidence)-[:REPORTED_IN]->(:Publication)`

## Minimal V0 Graph Schema

如果目标是尽快构出第一版图谱，建议先做最小闭环：

- Nodes:
  - `Polysaccharide`
  - `Organism`
  - `Monosaccharide`
  - `GlycosidicBond`
  - `Function`
  - `Disease`
  - `Publication`
- Edges:
  - `ISOLATED_FROM`
  - `HAS_MONOSACCHARIDE`
  - `HAS_GLYCOSIDIC_BOND`
  - `ASSOCIATED_WITH_FUNCTION`
  - `ASSOCIATED_WITH_DISEASE`
  - `SUPPORTED_BY`

这是最适合先跑通 ETL、Neo4j 导入和图算法基线的版本。

## ETL Expansion Plan

### Stage A. Parse and normalize

新增解析器，把现有自由文本字段拆解为结构化表：

- `organism_source` -> organism dictionary
- `monomer_composition` -> composition table
- `linkage` -> bond table
- `related_diseases` -> disease table
- `function_label` -> function table
- `mw_or_range` -> numeric range

建议生成以下中间文件：

- `kg_nodes_polysaccharide.parquet`
- `kg_nodes_organism.parquet`
- `kg_nodes_monosaccharide.parquet`
- `kg_nodes_bond.parquet`
- `kg_nodes_function.parquet`
- `kg_nodes_disease.parquet`
- `kg_nodes_publication.parquet`
- `kg_edges_*.parquet`

### Stage B. Canonicalization

建立标准化词表：

- 单糖同义词表
- 功能标签映射表
- 疾病字符串拆分与 ICD-11 对齐表
- 来源生物别名表

### Stage C. Graph build

将实体与边导出为：

- `CSV` for Neo4j bulk import
- `NetworkX` / `PyG` object for modeling
- `triples.tsv` for KG embedding

## Recommended Repository Structure

建议在 `polysaccharidesgraph` 中建立如下骨架：

```text
docs/
  dolphin_kg_design.md
  dolphin_kg_research_ideation.md
configs/
  kg_schema_v0.yaml
src/
  polysaccharidesgraph/
    kg/
      schema.py
      normalize.py
      build_graph.py
      export_neo4j.py
      export_pyg.py
data/
  interim/
  processed/
```

## Immediate Implementation Priorities

优先级按性价比排序：

1. 先把 `function_label`、`related_diseases`、`organism_source`、`doi` 抽成实体
2. 再把 `monomer_composition` 和 `linkage` 解析成结构节点
3. 最后补 `StructuralMotif` 和 `Evidence` 两层高阶语义

原因：

- 前两步就足够支持查询、可视化、链路分析和图学习
- 后一步更偏研究创新，需要额外规则或模型

## Example Queries

### Query 1

找“来自真菌、富含 glucose/mannose、与 immunomodulatory 相关”的多糖。

### Query 2

找“与糖尿病相关疾病相连，但结构上接近已知免疫调节多糖”的候选。

### Query 3

找“共享单糖组成但功能不同”的多糖对，作为机制研究负样本。

## Main Data Risks

### Risk 1. Disease strings are mixed-granularity

同一字段里既有 ICD-11 样式，也有宽泛短语，如 `organ injury`、`Aging-related disorders`。

### Risk 2. Bond strings have encoding noise

目前抓取结果里糖键文本存在编码符号异常，必须在标准化前做字符修复。

### Risk 3. Evidence is weakly structured

DoLPHiN 当前对实验层级的表达不充分，图谱中的证据边在 v0 只能先弱监督。

### Risk 4. Function labels are semi-controlled

标签命名存在别名，如 `immunoregulation` 与 `immunomodulatory`。

## Deliverable Definition For KG v0

如果你要把这项工作定义成“第一阶段完成”，建议验收标准是：

- 从 DoLPHiN 全量记录构建出一版实体-关系图
- 每条图谱边都能回溯到 `source_record_id` 与 `doi`
- 支持至少 10 条高价值查询模板
- 导出一份可用于 GNN / KGE 的训练图
- 给出一份图谱质量报告：节点数、边数、解析成功率、标准化覆盖率
