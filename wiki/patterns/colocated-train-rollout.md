---
id: pattern-colocated-train-rollout
title: Colocated Train Rollout
type: pattern
frameworks:
- slime
- verl
backends:
- sglang
- vllm
- megatron
components:
- training
- rollout
- weight-sync
algorithms:
- ppo
- grpo
deployment_modes:
- colocated
tags:
- pattern
- architecture
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
- repo-vllm-readme
- repo-sglang-readme
- source-vllm-rollout-backend-refs
- source-sglang-rollout-backend-refs
version_sensitive:
- vs-slime-main-2026-06-12
- vs-verl-main-2026-06-12
- vs-areal-main-2026-06-12
- vs-roll-main-2026-06-12
- vs-vllm-main-2026-06-12
- vs-sglang-main-2026-06-12
created_at: '2026-06-12'
updated_at: '2026-06-13'
summary: Pattern for shared GPU pools where trainer and rollout engine sleep, wake,
  or share memory.
risks:
- stale-policy
- version-mismatch
- observability-gap
- stale-kv-cache
- inconsistent-logprob
claim_ids:
- claim-vllm-ipc-colocated-weight-transfer
- claim-vllm-pause-resume-cache-control
- claim-sglang-sleep-wake-cache-flush
- claim-sglang-tensor-refit-request-fields
- claim-sglang-pause-continue-generation
related_pages:
- capability-rollout-backend-selection
- comparisons-rollout-backends
- backend-vllm
- backend-sglang
- failure-stale-kv-cache
---

# Colocated Train Rollout

Colocated train rollout means the trainer and rollout engine share a local resource boundary, often the same node or GPU pool. The selection question is whether the backend can pause or drain generation, update weights without losing ownership clarity, handle cache invalidation, and resume with a new policy version.

## Use When

- The target needs low-latency local weight handoff and can keep trainer/rollout lifecycle tightly coordinated.
- vLLM IPC transfer fits same-GPU trainer/inference placement, with serialization risk acknowledged.
- SGLang tensor refit or sleep/wake memory handoff fits the rollout lifecycle, with cache flush and pause semantics explicit.
- The task can tolerate tighter coupling between trainer and rollout process placement.

## Design Requirements

- Define who owns each GPU tensor before, during, and after update.
- Define whether requests are aborted, waited, retracted, or kept across the update.
- Record policy version and backend instance identity in every sample.
- Flush or namespace KV/prefix cache after weight changes unless the design explicitly accepts stale-policy risk.
- Keep disk/checkpoint reload as a full fallback when in-memory transfer fails.

## Validation Ideas

- Version monotonicity test.
- Cache flush or cache namespace test.
- Rollout/train logprob mismatch smoke test.
- Failure injection for sync timeout or partial reward.
- A small update run should show pause/update/resume ordering and cache policy in logs.

All capability statements on this page are source-reported unless explicitly marked otherwise. Local throughput or quality claims require separate evidence.
