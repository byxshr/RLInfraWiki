---
id: observability-training-inference-mismatch
title: Training Inference Mismatch
type: observability
frameworks:
- slime
- verl
backends:
- sglang
- vllm
- megatron
components:
- observability
- training
- rollout
algorithms:
- ppo
- grpo
deployment_modes:
- colocated
- disaggregated
tags:
- observability
- debug
- rollout-backend-selection
- code-evidenced
confidence: inferred
reproducibility: source-reading
evidence_level: code-evidenced
sources:
- repo-thudm-slime-readme
- repo-verl-readme
- repo-inclusionai-areal-readme
- repo-alibaba-roll-readme
- source-vllm-rollout-backend-refs
- source-sglang-rollout-backend-refs
- source-sglang-rl-weight-update-refs
version_sensitive:
- vs-slime-main-2026-06-12
- vs-verl-main-2026-06-12
- vs-areal-main-2026-06-12
- vs-roll-main-2026-06-12
created_at: '2026-06-12'
updated_at: '2026-06-13'
summary: Mismatch debugging compares rollout logprobs, trainer logprobs, tokenization,
  routing, precision, and policy versions.
risks:
- observability-gap
- version-mismatch
- nondeterminism
claim_ids:
- claim-vllm-batch-invariant-rl-determinism
- claim-vllm-async-rl-stale-kv-boundary
- claim-sglang-deterministic-inference-rl-need
- claim-sglang-deterministic-test-hooks
- claim-sglang-logprob-request-fields
related_pages:
- validation-logprob-consistency
- validation-train-infer-schema-match
- failure-inconsistent-logprob
- failure-stale-kv-cache
- capability-rollout-backend-selection
---

# Training Inference Mismatch

Mismatch debugging compares rollout logprobs, trainer logprobs, tokenization, routing, precision, and policy versions.

## Evidence To Collect

- Exact command and config.
- Source and target weight version.
- Prompt, response, token IDs, logprobs, reward, and route metadata.
- Rollout backend flags affecting cache, batching, and determinism.
- Failure logs and rollback action.

## Backend Selection Checks

- For SGLang, record deterministic inference flags or known gaps, `return_logprob` request settings, cache flush behavior, and `weight_version`.
- For vLLM, record batch invariance or sampling controls, pause/resume `clear_cache` behavior, and weight transfer protocol.
- For PD or multi-turn rollout, record KV lease/TTL, conversation ID, router/proxy metadata, and whether stale KV can cross a weight update.
- Reject a design that compares trainer and rollout logprobs without naming tokenizer, token IDs, action mask, sampling seed/settings, policy version, and backend identity.

All capability statements on this page are source-reported unless explicitly marked otherwise. Local throughput or quality claims require separate evidence.
