---
id: validation-grouped-rollout-invariants
title: Grouped rollout invariants
type: validation-pattern
page_type: validation-pattern
components:
- algorithm
- data-buffer
summary: Check group_id, group_size, prompt grouping, and reward normalization boundaries.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- repo-verl-readme
- repo-alibaba-roll-readme
- repo-inclusionai-areal-readme
risks:
- sample-schema-drift
created_at: '2026-06-13'
updated_at: '2026-06-13'
confidence: inferred
reproducibility: contract
version_sensitive: []
tags: []
frameworks: []
backends: []
algorithms: []
deployment_modes: []
---

# Grouped rollout invariants

## Purpose
Check group_id, group_size, prompt grouping, and reward normalization boundaries.

## Minimal check
A review-ready task should include a small deterministic or structural command/log that would fail if this invariant is broken.

## Evidence required
Record command, expected result, artifact path, and whether the result is local verification or only source-reported design intent.
