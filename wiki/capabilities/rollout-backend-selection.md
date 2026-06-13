---
id: capability-rollout-backend-selection
title: Rollout Backend Selection
type: capability
page_type: capability
frameworks:
- slime
- verl
backends:
- sglang
- vllm
components:
- rollout
- inference
- weight-sync
- observability
algorithms:
- grpo
- rlvr
deployment_modes:
- colocated
- disaggregated
- external-service
tags:
- rollout-backend-selection
- code-evidenced
- cache
- logprob
- weight-update
confidence: inferred
reproducibility: source-reading
evidence_level: code-evidenced
sources:
- source-vllm-rollout-backend-refs
- source-sglang-rollout-backend-refs
- source-sglang-rl-weight-update-refs
version_sensitive:
- vs-vllm-main-2026-06-12
- vs-sglang-main-2026-06-12
created_at: '2026-06-13'
updated_at: '2026-06-13'
summary: Capability for selecting a rollout backend by matching rollout semantics,
  weight-update path, cache policy, logprob contract, topology, and validation risk.
risks:
- stale-kv-cache
- inconsistent-logprob
- version-mismatch
- distributed-rank-mismatch
claim_ids:
- claim-vllm-rl-weight-transfer-backends
- claim-vllm-pause-resume-cache-control
- claim-vllm-batch-invariant-rl-determinism
- claim-vllm-disaggregated-prefill-selection
- claim-sglang-refit-strategy-selection
- claim-sglang-sleep-wake-cache-flush
- claim-sglang-deterministic-inference-rl-need
- claim-sglang-logprob-request-fields
- claim-sglang-pd-disaggregation-selection
related_interfaces:
- interface-rollout-backend-adapter
- interface-weight-sync-adapter
failure_modes:
- failure-stale-kv-cache
- failure-inconsistent-logprob
- failure-partial-weight-update
- failure-distributed-rank-mismatch
validation_patterns:
- validation-logprob-consistency
- validation-train-infer-schema-match
- validation-weight-version-monotonicity
- validation-pause-update-resume
---

# Rollout Backend Selection

Rollout backend selection is the capability of choosing and adapting an inference engine for RL rollout generation while preserving training correctness. It is not only a throughput choice: the backend must expose enough lifecycle, weight update, cache, and logprob semantics for the algorithm and trainer.

## Required Semantics

- Generate batches of prompts or multi-turn interactions with request IDs and backend identity.
- Capture rollout-side behavior logprobs or enough inputs to recompute them under a controlled trainer contract.
- Report a policy or weight version for every sample handed to the trainer.
- Define a weight update path and full fallback path.
- Define whether KV/prefix cache is flushed, namespaced, leased, or intentionally retained.
- Define how colocated and disaggregated topologies pause, drain, update, and resume rollout.

## Code-Evidenced Backend Surfaces

- vLLM evidence includes RL weight transfer, IPC same-GPU transfer, NCCL separate-worker transfer, pause/resume with cache clearing, batch invariance for RL reproducibility, and experimental disaggregated prefilling.
- SGLang evidence includes sleep/wake, disk/tensor/distributed refit, `flush_cache`, `weight_version`, pause/continue generation, deterministic inference, logprob request fields, and PD/router integration.

## Selection Checklist

1. Name the target framework and existing rollout backend, if any.
2. Pick primary and fallback backend.
3. Pick weight update path: disk/checkpoint, tensor/IPC, NCCL/distributed group, or full reload.
4. Pick cache policy and record the stale-cache failure mode.
5. Pick logprob policy and attach `validation-logprob-consistency`.
6. Pick topology: colocated, disaggregated train/rollout, PD disaggregation, or external service.
7. Declare non-claims: no GPU, NCCL, multi-node, production, or performance verification without local artifacts.

## Known Gaps

- This capability is code-evidenced by source refs, not locally verified with GPUs.
- Production and performance statements are not promoted beyond source-reported without local command output, logs, and artifacts.
