# Case Study Shortlist

## Selection Logic

The shortlist is designed to support four manuscript needs:

1. show that clean graph-based retrieval can work without disease-aware ontology support
2. show a second clean case with a different biological function profile
3. show one ontology-rescued tail case where the hierarchy materially changes the rank
4. show one representative failure that remains unresolved despite rich local graph evidence

## Selected Cases

### Case 1. Clean structural success: BEP / immunomodulatory

- **Poly ID**: `dolphin::33862`
- **Name**: `BEP`
- **Held-out function**: `immunomodulatory`
- **Type**: clean success
- **Reason for selection**:
  - clean filtered rank is `1`
  - evidence is dense across organism, monosaccharide, bond, disease, and DOI
  - the function is biologically central and easy for readers to understand
- **Evidence preview**:
  - organism: `Boletus edulis`
  - monosaccharides: `glucose; galactose; arabinose; rhamnose`
  - bonds: `尾-Glcp-(1→?); 尾-Galp-(1→?); 尾-Rhap-(1→?)`
  - DOI: `10.1016/j.carbpol.2013.12.085`

### Case 2. Clean structural success: Galactofucan / anticoagulant

- **Poly ID**: `dolphin::33999`
- **Name**: `Galactofucan(M05 RDP 2H)`
- **Held-out function**: `anticoagulant`
- **Type**: clean success
- **Reason for selection**:
  - clean filtered rank is `1`
  - function type differs clearly from immunomodulatory and antioxidant head labels
  - the case highlights marine-source sulfated/fucose-rich style evidence that is distinct from the fungal cases
- **Evidence preview**:
  - organism: `Laminaria saccharina`
  - monosaccharides: `glucose; mannose; galactose; xylose; ...`
  - bond cue: `伪-Fucp-(4→?)`
  - DOI: `10.1016/j.phytochem.2010.05.021`

### Case 3. Ontology-rescued tail case: APP90-2 / osteogenic

- **Poly ID**: `dolphin::34783`
- **Name**: `APP90-2`
- **Held-out function**: `osteogenic`
- **Type**: ontology rescue
- **Reason for selection**:
  - only stable ontology rescue discovered in the current paired pool
  - tail label with support `2`
  - baseline filtered rank `43` improves to ontology filtered rank `3`
  - rescue observed in `5` of the `16` paired seeds
- **Evidence preview**:
  - organism: `Alhagi maurorum`
  - monosaccharides: `glucose; mannose; galactose; xylose; ...`
  - bonds: multiple arabinose/xylose-rich motifs
  - disease cue: `organ injury`
  - DOI: `10.1016/j.ijbiomac.2020.12.189`

### Case 4. Persistent failure: Amygdalus scoparia Spach / antiinflammatory

- **Poly ID**: `dolphin::33382`
- **Name**: unavailable in current node table
- **Held-out function**: `antiinflammatory`
- **Type**: clean failure + ontology failure
- **Reason for selection**:
  - clean filtered rank `12`
  - disease-aware baseline filtered rank `19`
  - ontology filtered rank `19`
  - rich local evidence is present, so failure is informative rather than trivial
- **Evidence preview**:
  - organism: `Amygdalus scoparia Spach`
  - monosaccharides: `galactose; xylose; arabinose; rhamnose`
  - bonds: mixed galactose/arabinose/xylose/rhamnose motifs
  - disease cues: `Malignant neoplasms; 04-Diseases of the immune system`
  - DOI: `10.1016/j.carbpol.2017.10.099`

## Planned Use In The Paper

- **Main text**:
  - Case 1 for clean interpretable retrieval
  - Case 3 for ontology-rescued tail behavior
- **Discussion or supplementary**:
  - Case 2 as a second clean success with a different functional profile
  - Case 4 as the representative failure case linked to current graph limitations
