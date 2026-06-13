---
id: failure-inconsistent-logprob
title: Inconsistent logprob
type: failure-mode
page_type: failure-mode
components:
- rollout
- training
summary: Rollout-side old_logprobs and trainer-side recomputation are not semantically
  aligned.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- repo-verl-readme
- repo-alibaba-roll-readme
- repo-inclusionai-areal-readme
validation_patterns:
- validation-train-infer-schema-match
risks:
- inconsistent-logprob
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

# Inconsistent logprob

## Failure description
Rollout-side old_logprobs and trainer-side recomputation are not semantically aligned.

## Detection
Require explicit logs, counters, or schema checks that would reveal the failure in a small review scenario.

## Mitigation
Prefer fail-closed behavior, explicit version metadata, bounded retries, and rollback or fallback paths.

## Validation checklist
Tie this failure to a validation-pattern page before promoting a design.
