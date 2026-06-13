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
- source-sglang-rollout-backend-refs
- source-vllm-rollout-backend-refs
validation_patterns:
- validation-train-infer-schema-match
- validation-logprob-consistency
risks:
- inconsistent-logprob
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
deployment_modes: []
claim_ids:
- claim-vllm-batch-invariant-rl-determinism
- claim-sglang-deterministic-inference-rl-need
- claim-sglang-logprob-request-fields
related_pages:
- capability-rollout-backend-selection
- observability-training-inference-mismatch
- validation-logprob-consistency
---

# Inconsistent logprob

## Failure description
Rollout-side old_logprobs and trainer-side recomputation are not semantically aligned.

## Detection
- Log prompt token IDs, response token IDs, action mask, sampling settings, backend ID, policy version, and rollout-side logprobs.
- Recompute trainer-side logprobs under the same tokenizer, weights, precision policy, and deterministic/batch-invariant settings when available.
- Compare cached vs uncached paths if prefix/KV cache is enabled.

## Mitigation
- Treat missing logprob provenance as a schema error.
- Freeze or explicitly record sampling seed/settings for GRPO/RLVR grouped samples.
- Fail closed when trainer recomputation cannot be aligned with rollout samples.

## Validation checklist
Tie this failure to a validation-pattern page before promoting a design.
