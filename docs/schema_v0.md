# Schema v0

## Required Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `poly_id` | string | stable internal identifier |
| `source_db` | string | source database name |
| `source_record_id` | string | original source identifier |
| `raw_representation` | string | source representation |
| `canonical_representation` | string | normalized representation |
| `function_label` | string or list | target label(s) |
| `evidence_type` | string | `in_vitro`, `animal`, `clinical` |
| `doi` | string | source paper DOI |
| `license` | string | reuse status |

## Recommended Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `monomer_composition` | string or json | monosaccharide composition |
| `linkage` | string | linkage summary |
| `branching` | string | branching information |
| `modification` | string | modification annotations |
| `mw_or_range` | string or number | molecular weight signal |
| `organism_source` | string | biological source |

## Notes

- keep the original source fields even if normalization fails
- never overwrite the raw representation
- store evidence level separately from function label
