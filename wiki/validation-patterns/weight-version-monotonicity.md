---
id: validation-weight-version-monotonicity
title: Weight version monotonicity
type: validation-pattern
page_type: validation-pattern
components:
- weight-sync
summary: Check that every rollout-visible update records a nondecreasing weight_version.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- source-slime-weight-sync-code
- source-sglang-rl-weight-update-refs
risks:
- version-mismatch
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

# Weight version monotonicity

## Purpose
Check that every rollout-visible update records a nondecreasing weight_version.

## Minimal check
A review-ready task should include a small deterministic or structural command/log that would fail if this invariant is broken.

## Evidence required
Record command, expected result, artifact path, and whether the result is local verification or only source-reported design intent.
