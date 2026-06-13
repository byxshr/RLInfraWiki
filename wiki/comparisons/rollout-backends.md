---
id: comparisons-rollout-backends
title: Rollout Backends
type: comparison
frameworks:
- vllm
- sglang
backends:
- vllm
- sglang
components:
- rollout
- inference
- router
- weight-sync
- observability
algorithms:
- rlhf
- grpo
- rlvr
deployment_modes:
- external-service
- disaggregated
- colocated
tags:
- comparison
- decision-matrix
- rollout-backend-selection
- code-evidenced
- cache
- logprob
- weight-update
confidence: inferred
reproducibility: source-reading
evidence_level: code-evidenced
sources:
- repo-vllm-readme
- source-vllm-rollout-backend-refs
- repo-sglang-readme
- source-sglang-rollout-backend-refs
- source-sglang-rl-weight-update-refs
- doc-vllm-training-weight-transfer
- doc-sglang-rl-systems
- doc-sglang-faq-determinism
- doc-sglang-pd-disaggregation
version_sensitive: []
created_at: '2026-06-12'
updated_at: '2026-06-13'
summary: Compare vLLM and SGLang for RL rollout serving, caching, refit, deterministic
  evaluation, and PD disaggregation.
risks:
- observability-gap
- stale-kv-cache
- inconsistent-logprob
- version-mismatch
- distributed-rank-mismatch
claim_ids:
- claim-vllm-rl-weight-transfer-backends
- claim-vllm-pause-resume-cache-control
- claim-vllm-async-rl-stale-kv-boundary
- claim-vllm-batch-invariant-rl-determinism
- claim-vllm-disaggregated-prefill-selection
- claim-vllm-multiturn-kv-transfer-cache-ttl
- claim-sglang-refit-strategy-selection
- claim-sglang-sleep-wake-cache-flush
- claim-sglang-pause-continue-generation
- claim-sglang-deterministic-inference-rl-need
- claim-sglang-logprob-request-fields
- claim-sglang-pd-disaggregation-selection
related_pages:
- capability-rollout-backend-selection
- backend-vllm
- backend-sglang
- interface-rollout-backend-adapter
- pattern-colocated-train-rollout
- pattern-disaggregated-train-rollout
- pattern-pd-disaggregation
- failure-stale-kv-cache
- failure-inconsistent-logprob
- validation-logprob-consistency
---

# Rollout Backends

This page is a rollout backend selection dictionary entry. Use it when an RL infra task asks whether to use SGLang, vLLM, or both for rollout generation, RLVR/GRPO logprob capture, weight update, cache control, and colocated or disaggregated serving.

## Evidence Basis

| Backend | Code-evidenced source refs | What the refs prove |
|---|---|---|
| vLLM | `source-vllm-rollout-backend-refs` claims `claim-vllm-rl-weight-transfer-backends`, `claim-vllm-ipc-colocated-weight-transfer`, `claim-vllm-nccl-disaggregated-weight-transfer`, `claim-vllm-pause-resume-cache-control`, `claim-vllm-batch-invariant-rl-determinism`, `claim-vllm-disaggregated-prefill-selection` | vLLM documents RL weight transfer, IPC for colocated transfer, NCCL for separate trainer/inference workers, pause/resume plus cache clearing, batch-invariance controls for RL determinism, and experimental disaggregated prefilling. |
| SGLang | `source-sglang-rollout-backend-refs` claims `claim-sglang-refit-strategy-selection`, `claim-sglang-sleep-wake-cache-flush`, `claim-sglang-pause-continue-generation`, `claim-sglang-deterministic-inference-rl-need`, `claim-sglang-logprob-request-fields`, `claim-sglang-pd-disaggregation-selection` plus `source-sglang-rl-weight-update-refs` | SGLang documents RL lifecycle APIs, memory sleep/wake, disk/tensor/distributed refit, `flush_cache`, `weight_version`, pause/continue generation, logprob request fields, deterministic inference hooks, and PD/router surfaces. |

These are source-reading claims, not local GPU verification.

## Decision Matrix

| Dimension | Prefer SGLang when | Prefer vLLM when | Required validation |
|---|---|---|---|
| Existing stack fit | The target already uses slime/SGLang or needs explicit disk, tensor, or distributed refit APIs with `weight_version` and `flush_cache`. | The target already uses vLLM, verl, or OpenAI-compatible vLLM serving and can integrate the vLLM weight-transfer control plane. | Record target framework page IDs and source IDs. |
| Colocated rollout | Tensor refit or sleep/wake memory handoff is the main optimization, and the rollout engine can be paused cleanly. | IPC weight transfer is selected for same-GPU trainer/inference placement. | Prove a pause/update/resume boundary and cache policy. |
| Disaggregated rollout | A dedicated distributed group and SGLang refit endpoints match the training-to-rollout topology. | NCCL weight transfer and vLLM HTTP/Ray control plane match separate inference workers. | Prove rank/world-size mapping, timeout, rollback, and version monotonicity. |
| RLVR/GRPO logprobs | Native request fields can capture logprob outputs and deterministic mode is part of the design. | Batch invariance and fixed sampling controls are part of the design. | Compare rollout-side old logprobs with trainer recomputation under a fixed sample contract. |
| Multi-turn or agentic rollout | Pause/continue generation and router behavior are central to handling long-tail requests. | Disaggregated prefilling with KV transfer, leases, and multi-turn proxy state are central. | Bound stale cache and conversation/KV namespace reuse. |
| PD disaggregation | SGLang router and PD deployment are selected; prefill/decode health is monitored separately. | vLLM disaggregated prefilling connectors are selected; P/D connector failure policy is explicit. | Track prefill/decode routing, KV transfer errors, and recompute/fail behavior. |

## Selection Contract

A review-ready backend selection must name:

- Primary rollout backend and fallback backend.
- Primary weight update path and full fallback path.
- `weight_version` or equivalent policy version field.
- Cache policy: flush, namespace, TTL, or explicit stale-cache acceptance.
- Logprob contract: prompt/response token IDs, behavior logprobs, reference logprobs when needed, sampling seed/settings, and backend identity.
- Deployment topology: colocated, disaggregated train/rollout, PD disaggregation, or external service.
- Failure modes: stale KV cache, partial weight update, inconsistent logprob, rollout deadlock, rank mismatch, KV transfer failure.
- Validation pages and commands that would prove the selection in a small scenario.

## Known Gaps

- RLInfraWiki has not locally verified vLLM or SGLang GPU performance, NCCL, multi-node, or production behavior.
- vLLM disaggregated prefilling is documented as experimental in the cited source. Treat any production readiness statement as source-reported unless a local artifact proves it.
- SGLang docs contain source-reported production-oriented router language; RLInfraWiki records it as upstream-reported, not locally verified.
