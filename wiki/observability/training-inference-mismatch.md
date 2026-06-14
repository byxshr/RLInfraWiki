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
- recipe-debug-training-rollout-mismatch
- observability-debug-playbook
- validation-logprob-consistency
- validation-train-infer-schema-match
- failure-inconsistent-logprob
- failure-stale-kv-cache
- failure-sample-schema-drift
- failure-stale-policy-training
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

## Failure Isolation Order

1. Confirm `policy_version`, `weight_version`, trainer step, rollout request ID, backend ID, and route metadata are present on the same sample.
2. Check cache isolation: `flush_cache`, cache namespace, lease, or TTL must explain why stale KV/prefix cache cannot cross a policy update.
3. Compare rollout `old_logprob` with trainer recomputation using the same tokenizer, token IDs, masks, weights, precision policy, and sampling settings.
4. Compare rollout sample schema with trainer batch input: prompt/response token IDs, action/loss mask, stop reason, reward rows, group ID, and data-buffer record ID.
5. Inspect backend/topology only after evidence proves the mismatch is not a missing version, stale cache, logprob, or schema issue.

## Backend Selection Checks

- For SGLang, record deterministic inference flags or known gaps, `return_logprob` request settings, cache flush behavior, and `weight_version`.
- For vLLM, record batch invariance or sampling controls, pause/resume `clear_cache` behavior, and weight transfer protocol.
- For PD or multi-turn rollout, record KV lease/TTL, conversation ID, router/proxy metadata, and whether stale KV can cross a weight update.
- Reject a design that compares trainer and rollout logprobs without naming tokenizer, token IDs, action mask, sampling seed/settings, policy version, and backend identity.

## Stop Conditions

- Missing version identity on samples, logs, or trainer batches blocks promotion.
- Missing cache policy blocks promotion when prefix/KV cache may be reused.
- Missing replay/recompute evidence blocks any claim that rollout and trainer logprobs are compatible.
- Missing source IDs or local artifacts blocks production, performance, and quality claims.

All capability statements on this page are source-reported unless explicitly marked otherwise. Local throughput, quality, GPU, NCCL, multi-node, or production claims require separate evidence.
