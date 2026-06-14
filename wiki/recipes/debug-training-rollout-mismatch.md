---
id: recipe-debug-training-rollout-mismatch
title: Debug Training Rollout Mismatch
type: recipe
frameworks:
- slime
- verl
- roll
- areal
backends:
- sglang
- vllm
- megatron
components:
- training
- rollout
- data-buffer
- observability
- weight-sync
algorithms:
- grpo
- rlvr
- ppo
deployment_modes:
- colocated
- disaggregated
- async
tags:
- recipe
- playbook
- debug
- training-rollout-mismatch
- code-evidenced
confidence: inferred
reproducibility: source-reading
evidence_level: code-evidenced
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- repo-verl-readme
- repo-alibaba-roll-readme
- repo-inclusionai-areal-readme
- source-slime-weight-sync-code
- source-sglang-rollout-backend-refs
- source-vllm-rollout-backend-refs
- source-sglang-rl-weight-update-refs
version_sensitive:
- vs-slime-main-2026-06-12
- vs-verl-main-2026-06-12
- vs-roll-main-2026-06-12
- vs-areal-main-2026-06-12
- vs-sglang-main-2026-06-12
- vs-vllm-main-2026-06-12
created_at: '2026-06-14'
updated_at: '2026-06-14'
summary: Debugging recipe for isolating training/rollout mismatch across version
  identity, cache, logprob replay, schema, reward/data-buffer, backend, and topology
  boundaries.
risks:
- inconsistent-logprob
- stale-kv-cache
- sample-schema-drift
- stale-policy-training
- version-mismatch
- observability-gap
claim_ids:
- claim-sglang-logprob-request-fields
- claim-sglang-sleep-wake-cache-flush
- claim-vllm-pause-resume-cache-control
- claim-vllm-batch-invariant-rl-determinism
- claim-vllm-async-rl-stale-kv-boundary
related_pages:
- observability-training-inference-mismatch
- observability-debug-playbook
- validation-logprob-consistency
- validation-train-infer-schema-match
- validation-weight-version-monotonicity
- validation-stale-policy-bound
- failure-inconsistent-logprob
- failure-stale-kv-cache
- failure-sample-schema-drift
- failure-stale-policy-training
---

# Debug Training Rollout Mismatch

Use this recipe when trainer-side loss inputs diverge from rollout-side generation evidence. The goal is to isolate the first broken boundary, not to tune throughput or choose a faster backend.

## Failure Isolation Order

1. Version identity: record `policy_version`, `weight_version`, trainer step, rollout request ID, backend ID, and checkpoint or refit source.
2. Cache boundary: prove `flush_cache`, cache namespace, lease, or TTL prevents stale KV/prefix cache from crossing a weight update.
3. Logprob replay/recompute: compare rollout `old_logprob` with trainer recomputation under the same tokenizer, weights, precision policy, sampling settings, and masks.
4. Schema, mask, and tokenization: compare prompt/response token IDs, action mask, loss mask, stop reason, chat template, padding side, and truncation rules.
5. Reward and data-buffer handoff: verify reward/verifier rows, timeout/retry state, group IDs, sample IDs, and trainer batch materialization.
6. Backend and topology: only after the above, inspect SGLang/vLLM lifecycle controls, colocated/disaggregated topology, PD routing, and async stale-policy bounds.

## Evidence Checklist

- Exact command, config, framework commit, backend version, and source IDs.
- One replayable sample with prompt text, prompt token IDs, response token IDs, masks, sampling settings, and stop reason.
- Rollout-side `old_logprob`, trainer recomputed logprob or explicit recompute gap, and mismatch tolerance.
- `policy_version`, `weight_version`, cache policy, rollout backend ID, route metadata, and data-buffer record ID.
- Validation artifacts that distinguish local verification from source-reported design intent.

## Debug Packet Output

A review-ready packet must include a symptom statement, hypothesis matrix, evidence-to-collect table, replay/recompute checklist, version/cache/logprob/schema matrix, stop conditions, and risk register.

## Stop Conditions

- Stop promotion if version identity is missing from samples, logs, or trainer batches.
- Stop promotion if cache policy cannot prove stale KV isolation.
- Stop promotion if `old_logprob` and trainer recomputation cannot be compared or explicitly scoped out.
- Stop promotion if sample schema fields are inferred without source IDs or replay evidence.

## Non-Claims

All backend and framework behavior here is source-reported or inferred unless local commands, logs, hardware context, commits, and artifacts are attached. This recipe does not verify GPU, NCCL, multi-node execution, throughput, latency, quality, or production readiness.
