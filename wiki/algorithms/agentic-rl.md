---
id: algorithm-agentic-rl
title: Agentic RL
type: algorithm
page_type: algorithm
components:
- algorithm
- data-buffer
- rollout
algorithms:
- agentic-rl
required_sample_fields:
- episode_id
- tool_calls
- observations
- reward
- weight_version
infra_requirements:
- capability-rollout-agentic-multiturn
- capability-reward-verifier
failure_modes:
- failure-sample-schema-drift
- failure-inconsistent-logprob
- failure-stale-policy-training
validation_patterns:
- validation-train-infer-schema-match
- validation-logprob-consistency
summary: Agentic RL page focuses on infra contracts, required sample fields, rollout
  requirements, and validation rather than only equations.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- repo-verl-readme
- repo-alibaba-roll-readme
- repo-inclusionai-areal-readme
created_at: '2026-06-13'
updated_at: '2026-06-13'
confidence: inferred
reproducibility: contract
version_sensitive: []
tags: []
risks: []
frameworks: []
backends: []
deployment_modes: []
---

# Agentic RL

## Infra-facing definition
Agentic RL requires framework-specific rollout and trainer plumbing to preserve algorithm data semantics.

## Required sample fields
- `episode_id`
- `tool_calls`
- `observations`
- `reward`
- `weight_version`

## Batch/group invariants
Preserve algorithm-specific grouping, masks, rewards, and version metadata across rollout, buffer, and trainer boundaries.

## Failure modes
Schema drift, stale policy samples, and logprob inconsistency are review blockers.

## Validation checklist
Validate required fields, policy/weight version propagation, and any algorithm-specific group invariants.
