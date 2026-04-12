# Biology-Facing Case Study Summaries v1

## Case 1. Clean structural success: BEP / immunomodulatory

`BEP` (`dolphin::33862`) is a clean success case in which the held-out `immunomodulatory` label remains at filtered rank `1` without ontology or disease-aware rescue logic. The local graph evidence is biologically interpretable rather than purely statistical: the polysaccharide is linked to the source organism `Boletus edulis`, carries a mixed monosaccharide profile (`glucose`, `galactose`, `arabinose`, `rhamnose`), and includes several simple residue-level bond signatures. This case is useful because it shows that the KG can support function retrieval through explicit typed evidence even before ontology enters the pipeline. In the paper, this sample can anchor the claim that the clean graph is already predictive when the evidence channels are explicit and structurally coherent.

## Case 2. Clean structural success: Galactofucan / anticoagulant

`Galactofucan(M05 RDP 2H)` (`dolphin::33999`) is a second clean success case with a different functional profile: the held-out `anticoagulant` label is recovered at filtered rank `1`. Unlike the fungal immunomodulatory case, this sample comes from `Laminaria saccharina` and carries a marine polysaccharide signature with a prominent fucose-related bond cue (`伪-Fucp-(4→?)`) together with a richer monosaccharide set. This case is valuable because it broadens the biological scope of the clean benchmark. It shows that the graph is not only retrieving very common antioxidant or immunomodulatory labels, but can also recover a more chemically distinctive functional signal under clean evidence.

## Case 3. Ontology-rescued tail case: APP90-2 / osteogenic

`APP90-2` (`dolphin::34783`) is the strongest ontology-rescued tail candidate currently available. Its held-out `osteogenic` label has training support `2`, and the disease-aware baseline places it at filtered rank `43`, whereas confidence-gated parent/child ontology propagation moves it to filtered rank `3`. The available graph evidence is still substantial: the sample comes from `Alhagi maurorum`, shows a mixed arabinose/xylose-rich bond profile, and is linked to the disease cue `organ injury`. This case is important because it turns the ontology claim into a concrete example: ontology is not globally improving everything, but it can selectively rescue a genuinely under-supported function when parent/child evidence becomes available at retrieval time.

## Case 4. Persistent failure: Amygdalus scoparia Spach / antiinflammatory

The `antiinflammatory` sample from `Amygdalus scoparia Spach` (`dolphin::33382`) is a representative persistent failure. It already contains rich local evidence --- mixed `galactose`, `xylose`, `arabinose`, and `rhamnose` composition, multiple bond types, disease links, and DOI provenance --- yet the clean model still leaves the held-out function at filtered rank `12`, the disease-aware baseline places it at `19`, and the ontology variant does not improve it. This case is useful because it prevents the paper from sounding overconfident. The failure suggests that some function distinctions are not recoverable from the current typed evidence blocks alone and may require motif-level structure, finer ontology granularity, or richer provenance-aware relation semantics.

## Planned Manuscript Use

- Put Case 1 and Case 3 in the main paper.
- Put Case 2 and Case 4 in supplementary material or in a compact Discussion paragraph if space permits.
- Use Case 4 explicitly to support the limitation claim that richer motif-level evidence is still missing from KG v0.
