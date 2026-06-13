---
id: failure-stale-kv-cache
title: Stale KV cache
type: failure-mode
page_type: failure-mode
components:
- rollout
- weight-sync
summary: Prefix/KV cache survives across a weight update without namespacing or flush.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- source-slime-weight-sync-code
- source-sglang-rl-weight-update-refs
- source-sglang-rollout-backend-refs
- source-vllm-rollout-backend-refs
validation_patterns:
- validation-weight-version-monotonicity
- validation-pause-update-resume
- validation-logprob-consistency
risks:
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
- claim-vllm-async-rl-stale-kv-boundary
- claim-vllm-pause-resume-cache-control
- claim-vllm-multiturn-kv-transfer-cache-ttl
- claim-sglang-sleep-wake-cache-flush
- claim-sglang-disk-refit-request-fields
- claim-sglang-tensor-refit-request-fields
- claim-sglang-distributed-refit-request-fields
related_pages:
- capability-rollout-backend-selection
- comparisons-rollout-backends
- validation-logprob-consistency
---

# Stale KV cache

## Failure description
Prefix/KV cache survives across a weight update without namespacing or flush.

## Detection
- Compare the sample `policy_version` with the backend `weight_version` and cache namespace.
- Record whether SGLang `flush_cache` or vLLM pause `clear_cache` was enabled for the update.
- In PD/multi-turn flows, record KV lease/TTL and conversation/cache key so stale cache cannot silently cross turns.
- Run a small cached-vs-uncached logprob check when the algorithm consumes old logprobs.

## Mitigation
- Prefer flush or namespace after weight update.
- Fail closed when cache version cannot be proven.
- Fall back to full checkpoint reload when optimized in-memory update leaves cache/version state ambiguous.

## Validation checklist
Tie this failure to a validation-pattern page before promoting a design.
