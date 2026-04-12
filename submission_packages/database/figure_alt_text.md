# Figure Alt Text for Database Submission

## Figure 1

Workflow diagram showing conversion of DoLPHiN records into a typed polysaccharide knowledge graph with nodes for polysaccharides, organisms, monosaccharides, glycosidic bonds, functions, diseases, and publications, followed by clean retrieval, disease-aware retrieval, and ontology-enhanced tail retrieval evaluation paths.

## Figure 2

Three-panel benchmark figure. Panel A compares clean baselines and shows that the strongest performance comes from a shallow linear model on explicit graph features rather than hetero GNNs. Panel B compares the disease-aware retrieval baseline with the ontology-enhanced variant on filtered ranking metrics. Panel C shows GNN failure ablations where no-message models remain close to the full hetero models.

## Figure 3

Three-panel stability figure for ontology-enhanced tail retrieval. One panel shows paired seed-wise tail Hits@3 for baseline and ontology variants, another shows per-seed deltas, and the third summarizes paired statistical tests supporting a stable tail-sensitive gain without observed tail regression.

## Figure 4

Two local subgraph panels illustrating biology-facing case studies. The first shows the ontology-rescued tail case APP90-2 with the held-out osteogenic label and a narrow parent-child ontology path that improves ranking. The second shows the persistent failure case CZGS-1 with antiinflammatory as the held-out label, where rich local graph evidence is present but ranking does not improve.
