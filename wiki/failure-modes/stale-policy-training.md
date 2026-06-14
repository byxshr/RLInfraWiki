---
id: failure-stale-policy-training
title: Stale-policy training
type: failure-mode
page_type: failure-mode
components:
- training
- rollout
frameworks:
- slime
- verl
- roll
- areal
backends:
- sglang
- vllm
algorithms:
- grpo
- rlvr
- ppo
summary: Trainer consumes samples beyond the accepted policy lag.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- repo-verl-readme
- repo-alibaba-roll-readme
- repo-inclusionai-areal-readme
validation_patterns:
- validation-train-infer-schema-match
- validation-stale-policy-bound
- validation-weight-version-monotonicity
risks:
- stale-policy-training
- version-mismatch
created_at: '2026-06-13'
updated_at: '2026-06-14'
confidence: inferred
reproducibility: contract
version_sensitive: []
tags:
- debug
- training-rollout-mismatch
related_pages:
- recipe-debug-training-rollout-mismatch
- observability-training-inference-mismatch
- capability-policy-versioning
- validation-stale-policy-bound
deployment_modes: []
---

# Stale-policy training

## Failure description
Trainer consumes samples beyond the accepted policy lag.

## Detection

For each consumed batch, compare sample `policy_version`, optional `weight_version`, trainer step, rollout request time, reward/verifier time, and accepted policy-lag bound. Async or delayed reward paths must record whether a sample was accepted, quarantined, or dropped.

## Mitigation

Fail closed when version identity is missing. Bound accepted policy lag, quarantine stale samples, and record counters for accepted, rejected, and unknown-version samples.

## Validation checklist

- Cite `validation-stale-policy-bound` and `validation-weight-version-monotonicity`.
- Include a small replay or structural check that rejects a sample outside the configured policy lag.
- Do not claim training correctness is verified unless local commands and artifacts prove the bound.
