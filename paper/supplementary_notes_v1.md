## Supplementary Notes v1

### Table S1. Biology-facing case-study evidence summary

| Case | Poly ID | Name | Held-out function | Setting / behavior | Rank change | Supporting evidence |
|---|---|---|---|---|---|---|
| Clean success 1 | `dolphin::33862` | `BEP` | `immunomodulatory` | clean success | rank `1` in clean retrieval | organism `Boletus edulis`; monosaccharides `glucose, galactose, arabinose, rhamnose`; simple residue-level bond signatures; DOI `10.1016/j.carbpol.2013.12.085` |
| Clean success 2 | `dolphin::33999` | `Galactofucan(M05 RDP 2H)` | `anticoagulant` | clean success | rank `1` in clean retrieval | organism `Laminaria saccharina`; marine fucose-rich cue; mixed monosaccharide composition; DOI `10.1016/j.phytochem.2010.05.021` |
| Ontology rescue | `dolphin::34783` | `APP90-2` | `osteogenic` | disease-aware baseline miss, ontology hit | rank `43 -> 3` | organism `Alhagi maurorum`; arabinose/xylose-rich bond profile; disease cue `organ injury`; DOI `10.1016/j.ijbiomac.2020.12.189` |
| Persistent failure | `dolphin::33382` | `Amygdalus scoparia Spach` | `antiinflammatory` | clean and ontology failure | clean rank `12`; disease-aware rank `19`; ontology rank `19` | mixed `galactose, xylose, arabinose, rhamnose`; multiple bond motifs; disease cues; DOI `10.1016/j.carbpol.2017.10.099` |

### Table S2. Additional note on GNN ablation interpretation

| Setting | Model | Test macro-F1 | Test exact match | Interpretation |
|---|---|---:|---:|---|
| Base graph | Hetero GNN | 0.0443 | 0.0256 | full message passing remains weak |
| Base graph | No-message ablation | 0.0423 | 0.0276 | almost unchanged from full GNN |
| Hybrid graph | Hetero GNN | 0.0347 | 0.0364 | message passing still weak after adding sparse meta-path inputs |
| Hybrid graph | No-message ablation | 0.0386 | 0.1132 | higher exact match does not indicate better multi-label ranking quality |

Exact match is intentionally not used as a primary conclusion for the GNN ablation because it is brittle in this multi-label setting. A model can obtain a superficially larger exact-match ratio by predicting very sparse label sets while still failing to recover the label distribution well enough to improve macro-F1. The core diagnostic evidence therefore remains the macro-F1 comparison between full message passing and no-message controls.
