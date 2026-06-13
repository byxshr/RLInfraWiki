---
id: failure-stale-policy-training
title: Stale-policy training
type: failure-mode
page_type: failure-mode
components:
- training
- rollout
summary: Trainer consumes samples beyond the accepted policy lag.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- repo-verl-readme
- repo-alibaba-roll-readme
- repo-inclusionai-areal-readme
validation_patterns:
- validation-train-infer-schema-match
risks:
- stale-policy-training
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

# Stale-policy training

## Failure description
Trainer consumes samples beyond the accepted policy lag.

## Detection
Require explicit logs, counters, or schema checks that would reveal the failure in a small review scenario.

## Mitigation
Prefer fail-closed behavior, explicit version metadata, bounded retries, and rollback or fallback paths.

## Validation checklist
Tie this failure to a validation-pattern page before promoting a design.
