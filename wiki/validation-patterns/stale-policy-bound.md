---
id: validation-stale-policy-bound
title: Stale policy bound
type: validation-pattern
page_type: validation-pattern
components:
- training
- rollout
summary: Check async rollout samples are rejected or downweighted beyond an explicit
  policy lag.
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

# Stale policy bound

## Purpose
Check async rollout samples are rejected or downweighted beyond an explicit policy lag.

## Minimal check
A review-ready task should include a small deterministic or structural command/log that would fail if this invariant is broken.

## Evidence required
Record command, expected result, artifact path, and whether the result is local verification or only source-reported design intent.
