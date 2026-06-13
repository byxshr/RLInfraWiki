---
id: pattern-pd-disaggregation
title: Prefill Decode Disaggregation
type: pattern
frameworks:
- vllm
- sglang
backends:
- vllm
- sglang
components:
- inference
- router
algorithms:
- rlhf
- grpo
- rlvr
deployment_modes:
- disaggregated
tags:
- pattern
- architecture
- rollout-backend-selection
- code-evidenced
confidence: inferred
reproducibility: source-reading
evidence_level: code-evidenced
sources:
- repo-vllm-readme
- repo-sglang-readme
- source-vllm-rollout-backend-refs
- source-sglang-rollout-backend-refs
- doc-sglang-pd-disaggregation
version_sensitive:
- vs-slime-main-2026-06-12
- vs-verl-main-2026-06-12
- vs-areal-main-2026-06-12
- vs-roll-main-2026-06-12
- vs-vllm-main-2026-06-12
- vs-sglang-main-2026-06-12
created_at: '2026-06-12'
updated_at: '2026-06-13'
summary: Pattern for separating prefill and decode resources, with router and KV-transfer
  failure surfaces.
risks:
- stale-policy
- version-mismatch
- observability-gap
- stale-kv-cache
- rollout-deadlock
claim_ids:
- claim-vllm-disaggregated-prefill-selection
- claim-vllm-disaggregated-prefill-kv-transfer
- claim-vllm-multiturn-kv-transfer-cache-ttl
- claim-vllm-kv-load-failure-policy
- claim-sglang-pd-disaggregation-selection
- claim-sglang-pd-router
- claim-sglang-pd-timeouts-health
related_pages:
- capability-rollout-backend-selection
- comparisons-rollout-backends
- backend-vllm
- backend-sglang
- failure-stale-kv-cache
---

# Prefill Decode Disaggregation

PD disaggregation separates prefill and decode serving phases. For RL rollout backend selection, treat it as a cache transfer and routing contract rather than a generic serving optimization.

## Use When

- Long prompts, multi-turn conversations, or agentic traces make prefill and decode scaling requirements diverge.
- vLLM disaggregated prefilling connectors or SGLang PD/router surfaces match the target serving topology.
- The design can track KV transfer params, lease/TTL, prefill/decode health, and fail vs recompute behavior.

## Design Requirements

- Name the router/proxy and the request metadata it carries between prefill and decode.
- Define cache ownership: producer, consumer, lease duration, decoder TTL, and release/cleanup behavior.
- Define behavior when KV transfer fails: fail closed, recompute, or retry with explicit stale-policy risk.
- Record whether prefill and decode instances share weight version, sampling settings, tokenizer, and logprob behavior.
- Monitor prefill, decode, router, KV transfer, and cache release separately.

## Validation Ideas

- Version monotonicity test.
- Cache flush or cache namespace test.
- Rollout/train logprob mismatch smoke test.
- Failure injection for sync timeout or partial reward.
- A PD smoke design should include one forced KV transfer failure and the expected fail/recompute branch.

All capability statements on this page are source-reported unless explicitly marked otherwise. Local throughput or quality claims require separate evidence.
