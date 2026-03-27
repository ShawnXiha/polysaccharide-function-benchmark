# Publishable Evaluation Protocol v1

## Objective

Turn the current engineering-complete pipeline into a scientifically defensible first-paper benchmark.

## Core Decision

Use `DoLPHiN` as the supervised benchmark source for the first paper.

Do **not** use current `CSDB` records as an equal supervised source for function prediction, because the fetched CSDB slice is structure-centric and contributes mostly `unknown` task labels. This makes it useful for engineering stress tests, but weak as evidence for the paper's main supervised claim.

## Dataset Variants

### Supervised Benchmark

- file: `data_processed/dataset_publishable_supervised_v1.jsonl`
- source policy: keep only `DoLPHiN`
- label policy:
  - drop `unknown`
  - keep only labels with global count `>= 20`
- purpose: main benchmark and first-paper baseline table

### Engineering Stress Test

- file: `data_processed/dataset_v0_real.jsonl`
- sources: `DoLPHiN + CSDB`
- purpose: show that random and leave-one-source-out pipelines execute on heterogeneous sources
- limitation: source-shift scores here should not be overclaimed as main scientific evidence

## Recommended Split Usage

### Main Table

- dataset: `dataset_publishable_supervised_v1.jsonl`
- split: random split
- report: majority, logistic, random forest, sequence n-gram, transformer, graph

### Reliability/Shift Analysis

- current recommendation: frame as `engineering stress test`, not the main headline result
- reason: label semantics differ across sources

## Required Paper Language

- say that CSDB was ingested to test pipeline robustness and cross-database interoperability
- do not claim that current CSDB results establish biologically fair cross-source function generalization
- reserve the full source-shift claim for a future label-aligned multi-source benchmark
