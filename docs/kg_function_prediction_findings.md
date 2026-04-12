# KG Function Prediction Findings

## Scope

本轮实验的目标不是追求最终最优精度，而是回答三个更关键的问题：

1. DoLPHiN 扩展出的知识图谱是否真的能提供可用监督信号。
2. 这些信号更适合用手工图特征、纯异构 GNN，还是两者结合。
3. 哪些关系可以作为 clean 主线，哪些更适合作为 upper-bound side information。

## Main Findings

### Finding 1. 图谱信息是有价值的

`Meta-Path (Clean)` 在 `66` 标签空间上达到了：

- test macro-F1 = `0.3046`
- test exact match = `0.4144`

这说明即使不使用疾病信息，图谱中的来源、单糖、糖键、文献等关系也已经足以支持一个有竞争力的多标签预测器。

### Finding 2. 当前图上，手工图特征明显强于纯 hetero GNN

`Hetero GNN (Clean)` 只有：

- test macro-F1 = `0.0443`
- test exact match = `0.0256`

这意味着在当前 KG v0 表达下，纯消息传递无法有效提取足够判别性的结构功能规律。主要原因更可能是：

- 节点特征仍然过弱
- 图结构仍然偏稀疏
- 非多糖节点几乎没有语义特征
- 结构信息更多体现在“关系存在与否”，而不是深层可传播表示

### Finding 3. 直接把 meta-path 特征并入 hetero GNN，并没有在 clean 设置下超过纯 meta-path

`Hybrid Hetero GNN (Clean)` 达到：

- test macro-F1 = `0.0347`
- test exact match = `0.0364`

这说明“把 GNN 加在已有强特征上”本身不会自动变强，当前 hybrid 版本仍然没有学会比线性读出更好的组合方式。

### Finding 3b. 即使补充了 richer clean structural features，结论依然没有改变

本轮还将 `polysaccharide` 节点特征扩展到了 `355` 维，纳入了：

- 基础度数统计
- molecular weight 信号
- branching flags
- monosaccharide ratio vector
- glycosidic bond multi-hot vector

但 clean hetero / clean hybrid 仍未超过 clean meta-path。说明短板不是“少几个结构位点特征”，而是当前 KG v0 上：

- 端到端 GNN 的归纳偏置还不适合这类信号
- relation-derived explicit features 依然是更有效的表示方式

### Finding 4. 疾病信息非常强，但不应作为主结果

当加入疾病相关信息后：

- `Meta-Path (With Disease)` test macro-F1 = `0.4560`
- `Hybrid Hetero GNN (Disease Edges + Disease Features)` test macro-F1 = `0.2250`

疾病信息显著提升性能，说明 `disease` 节点和功能标签之间存在强耦合。但这也意味着：

- 它更适合作为 side information / upper bound
- 不适合作为最干净的结构功能主结果

因为从研究叙事上看，这更接近“借助已知疾病语义做辅助预测”，而不是“仅靠多糖结构和来源关系预测功能”。

## Recommended Experimental Story

### Primary result

主结果建议采用：

- `Meta-Path (Clean)`

原因：

- 最强 clean baseline
- 可解释性最好
- 最符合“KG-enhanced function prediction”而不是“疾病辅助预测”

### Secondary result

增强结果建议采用：

- `Meta-Path (With Disease)` 作为 side-information upper bound

原因：

- 性能最强
- 能证明疾病关系确实提供额外语义
- 但不会污染主线结论

### Graph neural result

图神经结果建议定位为：

- 当前 KG v0 上纯 hetero message passing 仍不足
- 图神经模型需要更强的结构编码后才值得与 clean meta-path 竞争

这不是负面结果，而是一个很清晰的研究结论：

`在当前 DoLPHiN KG v0 上，图谱价值首先体现在可解释关系特征，而不是现成异构 GNN 的端到端收益。`

## Implications For Next Iteration

下一轮不建议继续堆更多模型名词，而应该优先增强 clean 图表达：

### Priority 1. 强化多糖节点结构特征

包括：

- monosaccharide 多热向量
- glycosidic bond motif 多热向量
- branching pattern 统计
- molecular weight 标准化数值
- organism taxonomy 层级特征

### Priority 2. 强化 bond / motif 节点语义

当前 bond 节点仍然太像字符串 ID，而不是可学习的结构单元。

### Priority 3. 把 clean meta-path 当作要超越的基线

后续任何 GNN / KGE 模型，都不应该再只和当前 hetero baseline 比，而应该至少达到或接近：

- clean meta-path macro-F1 `0.3046`

## Suggested Paper Framing

如果后续写论文或技术报告，这一段最合理的 framing 是：

1. 我们首先把 DoLPHiN 扩展为可用于图学习的异构知识图谱。
2. 在多标签功能预测上，基于可解释 meta-path 的图谱特征在 clean 设置下优于当前异构 GNN。
3. 疾病信息可显著提升性能，但应视作辅助语义而非主监督来源。
4. 这表明多糖 KG 的短期价值在于结构化关系表示与可解释特征工程，长期价值则在于进一步学习更强的结构节点表示。

## One-Sentence Takeaway

`DoLPHiN KG 已经证明有预测价值，但当前最可靠的收益来自 clean meta-path 特征而不是纯异构 GNN；因此下一阶段应优先增强结构表示，再考虑更强图神经模型。`
