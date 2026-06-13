---
id: validation-reward-timeout-retry
title: Reward timeout retry validation
type: validation-pattern
page_type: validation-pattern
components:
- reward
summary: Check reward/verifier timeout, retry, and fail-closed behavior.
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

# Reward timeout retry validation

## Purpose
Check reward/verifier timeout, retry, and fail-closed behavior.

## Minimal check
A review-ready task should include a small deterministic or structural command/log that would fail if this invariant is broken.

## Evidence required
Record command, expected result, artifact path, and whether the result is local verification or only source-reported design intent.
