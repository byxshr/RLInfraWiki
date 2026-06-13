---
id: validation-logprob-consistency
title: Logprob consistency
type: validation-pattern
page_type: validation-pattern
components:
- rollout
- training
summary: Check behavior logprobs are attached and semantically compatible with trainer
  loss.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- repo-verl-readme
- repo-alibaba-roll-readme
- repo-inclusionai-areal-readme
- source-sglang-rollout-backend-refs
- source-vllm-rollout-backend-refs
risks:
- sample-schema-drift
- inconsistent-logprob
- stale-kv-cache
created_at: '2026-06-13'
updated_at: '2026-06-13'
confidence: inferred
reproducibility: source-reading
evidence_level: code-evidenced
version_sensitive: []
tags:
- rollout-backend-selection
- code-evidenced
frameworks: []
backends:
- sglang
- vllm
algorithms:
- grpo
- rlvr
deployment_modes:
- colocated
- disaggregated
claim_ids:
- claim-vllm-batch-invariant-rl-determinism
- claim-vllm-async-rl-stale-kv-boundary
- claim-sglang-deterministic-inference-rl-need
- claim-sglang-deterministic-test-hooks
- claim-sglang-logprob-request-fields
related_pages:
- failure-inconsistent-logprob
- failure-stale-kv-cache
- observability-training-inference-mismatch
- capability-rollout-backend-selection
---

# Logprob consistency

## Purpose
Check behavior logprobs are attached and semantically compatible with trainer loss.

## Minimal check
A review-ready task should include a small deterministic or structural command/log that would fail if this invariant is broken.

Required fields:

- prompt token IDs and response token IDs
- action or response mask
- rollout backend ID and backend version
- policy or weight version
- sampling seed/settings
- rollout-side old logprobs
- trainer-side recomputed logprobs or explicit reason recomputation is out of scope
- cache policy for the request

## Evidence required
Record command, expected result, artifact path, and whether the result is local verification or only source-reported design intent.
