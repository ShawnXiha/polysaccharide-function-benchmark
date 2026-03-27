# Split Protocol

## Required Splits

### Random Split

- purpose: baseline comparability
- risk: optimistic estimate due to source leakage

### Leave-One-Source-Out

- purpose: evaluate robustness to source shift
- use as the main claim-supporting split

### Leave-One-Genus-Out

- purpose: test biological source generalization
- use as secondary stress test

## Rules

- all methods must use the same split files
- split generation must be deterministic
- split files should be versioned under `data_processed/`
