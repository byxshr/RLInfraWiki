---
id: backend-vllm
title: vLLM
type: backend
frameworks:
- vllm
backends:
- vllm
components:
- rollout
- inference
- weight-sync
- router
algorithms:
- rlhf
- grpo
deployment_modes:
- external-service
- disaggregated
tags:
- vllm
- pagedattention
- prefix-caching
- openai-compatible
- rollout-backend-selection
- code-evidenced
- batch-invariance
confidence: source-reported
reproducibility: source-reading
evidence_level: code-evidenced
sources:
- repo-vllm-readme
- doc-vllm-training-weight-transfer
- source-vllm-rollout-backend-refs
version_sensitive:
- vs-vllm-main-2026-06-12
created_at: '2026-06-12'
updated_at: '2026-06-13'
summary: vLLM provides LLM serving features including PagedAttention, continuous batching,
  chunked prefill, prefix caching, OpenAI-compatible serving, and RL weight transfer
  docs.
risks:
- nondeterminism
- cache-staleness
- version-mismatch
claim_ids:
- claim-vllm-rl-weight-transfer-backends
- claim-vllm-http-weight-transfer-control-plane
- claim-vllm-ipc-colocated-weight-transfer
- claim-vllm-nccl-disaggregated-weight-transfer
- claim-vllm-pause-resume-cache-control
- claim-vllm-async-rl-stale-kv-boundary
- claim-vllm-batch-invariant-rl-determinism
- claim-vllm-disaggregated-prefill-selection
- claim-vllm-multiturn-kv-transfer-cache-ttl
- claim-vllm-kv-load-failure-policy
related_pages:
- comparisons-rollout-backends
- capability-rollout-backend-selection
- pattern-colocated-train-rollout
- pattern-disaggregated-train-rollout
- pattern-pd-disaggregation
- validation-logprob-consistency
---

# vLLM

vLLM is a strong rollout backend candidate when the design needs general serving, OpenAI-compatible APIs, prefix caching, chunked prefill, or pluggable weight transfer for RL workflows.

## Evidence Basis

- `source-vllm-rollout-backend-refs` claim `claim-vllm-rl-weight-transfer-backends` records vLLM's documented RL weight-transfer system and its IPC/NCCL backend split.
- Claim `claim-vllm-http-weight-transfer-control-plane` records HTTP endpoints for init/start/update/finish plus pause/resume and the `VLLM_SERVER_DEV_MODE=1` requirement.
- Claim `claim-vllm-ipc-colocated-weight-transfer` records CUDA IPC as the colocated same-GPU path and its serialization risk.
- Claims `claim-vllm-nccl-disaggregated-weight-transfer` and `claim-vllm-nccl-four-phase-weight-update` record the NCCL process group and update protocol for separate trainer/inference workers.
- Claims `claim-vllm-pause-resume-cache-control` and `claim-vllm-async-rl-stale-kv-boundary` record the pause/resume cache boundary and stale KV risk when cache is not cleared.
- Claim `claim-vllm-batch-invariant-rl-determinism` records vLLM's source-reported batch invariance motivation for RL reproducibility.
- Claims `claim-vllm-disaggregated-prefill-selection`, `claim-vllm-multiturn-kv-transfer-cache-ttl`, and `claim-vllm-kv-load-failure-policy` record experimental disaggregated prefilling, multi-turn KV cache TTL/lease concerns, and fail vs recompute behavior.

## RL Backend Selection Notes

- Use vLLM when the target framework already relies on vLLM, when OpenAI-compatible rollout serving is a hard requirement, or when IPC/NCCL weight transfer matches the trainer placement.
- For colocated training/rollout, evaluate IPC transfer, serialization boundaries, and whether the same-GPU placement actually holds for every rank.
- For disaggregated training/rollout, evaluate NCCL world size, rank offset, trainer/inference worker lifecycle, and whether pause/start/update/finish/ resume can be made atomic enough for the task.
- For RLVR/GRPO, pair batch invariance or fixed sampling controls with a sample contract that records prompt tokens, response tokens, behavior logprobs, policy version, and backend identity.
- For multi-turn or agentic rollout, treat KV lease/TTL, conversation ID, and KV load failure policy as correctness fields, not only serving tuning.

## Design Checks

- Identify whether the task uses offline generation, online HTTP serving, or a colocated trainer/engine.
- Specify weight transfer backend, control plane, data plane, pause/resume behavior, cache clearing, rollback, and policy version semantics.
- Do not treat disaggregated prefilling as a throughput improvement unless a local workload artifact proves it; the cited source explicitly describes it as a latency-control feature and experimental.
- Treat all production, performance, and multi-node/NCCL statements as source-reported unless local logs and artifacts are attached.

All capability statements on this page are source-reported unless explicitly marked otherwise. Local throughput or quality claims require separate evidence.
