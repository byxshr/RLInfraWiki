---
id: pattern-disaggregated-train-rollout
title: Disaggregated Train Rollout
type: pattern
frameworks:
- slime
- roll
- areal
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
- repo-thudm-slime-readme
- repo-verl-readme
- repo-inclusionai-areal-readme
- repo-alibaba-roll-readme
- repo-vllm-readme
- repo-sglang-readme
- source-vllm-rollout-backend-refs
- source-sglang-rollout-backend-refs
- source-sglang-rl-weight-update-refs
version_sensitive:
- vs-slime-main-2026-06-12
- vs-verl-main-2026-06-12
- vs-areal-main-2026-06-12
- vs-roll-main-2026-06-12
- vs-vllm-main-2026-06-12
- vs-sglang-main-2026-06-12
created_at: '2026-06-12'
updated_at: '2026-06-13'
summary: Pattern for separate training and rollout resources with explicit weight
  version and transport boundary.
risks:
- stale-policy
- version-mismatch
- observability-gap
- distributed-rank-mismatch
- stale-kv-cache
claim_ids:
- claim-vllm-nccl-disaggregated-weight-transfer
- claim-vllm-nccl-four-phase-weight-update
- claim-sglang-distributed-refit-request-fields
- claim-sglang-disk-refit-request-fields
- claim-sglang-pd-timeouts-health
related_pages:
- capability-rollout-backend-selection
- comparisons-rollout-backends
- backend-vllm
- backend-sglang
- failure-distributed-rank-mismatch
- failure-partial-weight-update
---

# Disaggregated Train Rollout

Disaggregated train rollout separates trainer resources from rollout serving resources. It makes backend selection mostly about the weight transport contract, rank/world-size mapping, cache policy, and how rollout samples carry policy version back to the trainer.

## Use When

- The trainer and rollout engine run on separate GPUs, nodes, or process groups.
- vLLM NCCL weight transfer or SGLang distributed refit matches the desired trainer-to-rollout data plane.
- Rollout scaling, elastic serving, or failure isolation matters more than local handoff simplicity.
- A full disk/checkpoint reload fallback can recover from partial distributed updates.

## Design Requirements

- Record process group name, master address/port, rank offset, world size, backend, and teardown behavior when distributed update is selected.
- Specify whether rollout engines are paused, drained, aborted, or blocked during update.
- Require every rollout sample to include `weight_version` or equivalent policy version.
- Require cache flush, cache namespace, or bounded stale-cache policy after update.
- Add timeout and rollback behavior for communication group creation, weight transfer, and resume.

## Validation Ideas

- Version monotonicity test.
- Cache flush or cache namespace test.
- Rollout/train logprob mismatch smoke test.
- Failure injection for sync timeout or partial reward.
- A rank-mismatch smoke test should fail closed before training consumes rollout samples.

All capability statements on this page are source-reported unless explicitly marked otherwise. Local throughput or quality claims require separate evidence.
