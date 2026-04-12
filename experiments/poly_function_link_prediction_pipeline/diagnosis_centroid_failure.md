# Experiment-Craft Diagnosis: Why Centroid Scoring Failed

## Step 1. Collect Failure Cases

Observed in the first masked link prediction runs:

- clean centroid baseline had `MRR=0.0538`, `Hits@3=0.014`
- top predictions were often irrelevant high-frequency or semantically noisy functions
- example failures included `immunomodulatory` edges being ranked behind unrelated functions such as `moisture_absorption` or `emulsifying`

This failure was systematic, not random.

## Step 2. Find a Working Version

Two working references were available:

- `popularity` baseline worked as a sanity floor
- the underlying meta-path feature extraction was executable and stable

So the problem was not the masking pipeline or feature construction. It was the scoring function.

## Step 3. Bridge the Gap

Starting from the same feature space:

- global function centroids failed badly
- local kNN voting over nearby polysaccharides immediately improved retrieval

The single factor causing failure was therefore:

`global prototype scoring erased local neighborhood structure in a sparse, multimodal multi-label space`

## Step 4. Hypothesize and Verify

Ranked hypotheses:

1. Function classes are too heterogeneous for a single centroid
2. Frequent labels dominate centroid geometry
3. Multi-label overlap makes global prototypes especially unstable

Verification:

- kNN over the same features beat centroid strongly without changing the representation
- therefore the dominant issue was the scorer, not the features

## Step 5. Proposed Fix

Replace global centroid scoring with local neighbor voting:

- compute meta-path features per polysaccharide
- find nearest labeled polysaccharides
- aggregate function votes locally

Verification:

- clean `meta_path_knn` improved `Hits@3` from `0.014` to `0.639` in the first successful attempt

## Prescription

- keep the graph-derived features
- discard centroid scoring for this task
- use local kNN voting as the default clean masked-edge recovery baseline
- treat any future prototype-based method as requiring explicit multimodal class modeling, not a single centroid
