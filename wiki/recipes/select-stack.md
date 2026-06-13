---
id: recipe-select-stack
title: Select Stack
type: recipe
frameworks:
- slime
- verl
- areal
- roll
backends:
- sglang
- vllm
- megatron
- fsdp
components:
- training
- rollout
- scheduler
algorithms:
- ppo
- grpo
- rlvr
deployment_modes:
- colocated
- disaggregated
- async
tags:
- recipe
- playbook
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
- repo-nvidia-megatron-lm-readme
- source-vllm-rollout-backend-refs
- source-sglang-rollout-backend-refs
version_sensitive:
- vs-slime-main-2026-06-12
- vs-verl-main-2026-06-12
- vs-areal-main-2026-06-12
- vs-roll-main-2026-06-12
- vs-vllm-main-2026-06-12
- vs-sglang-main-2026-06-12
- vs-megatron-main-2026-06-12
created_at: '2026-06-12'
updated_at: '2026-06-13'
summary: Recipe for selecting framework, trainer, rollout backend, orchestration,
  and validation strategy.
risks:
- provenance-gap
- rollback-gap
- observability-gap
claim_ids:
- claim-vllm-rl-weight-transfer-backends
- claim-sglang-refit-strategy-selection
- claim-vllm-batch-invariant-rl-determinism
- claim-sglang-deterministic-inference-rl-need
related_pages:
- capability-rollout-backend-selection
- comparisons-rollout-backends
- pattern-colocated-train-rollout
- pattern-disaggregated-train-rollout
- pattern-pd-disaggregation
---

# Select Stack

Recipe for selecting framework, trainer, rollout backend, orchestration, and validation strategy.

## Steps

1. State objective, non-goals, and acceptance criteria.
2. Query RLInfraWiki and list page IDs plus source IDs.
3. Draw sample lifecycle from prompt source to metrics/traces.
4. Choose primary path and fallback path.
5. Add validation commands and evidence paths.
6. Prepare the Codex review packet.

## Rollout Backend Selection Addendum

For rollout backend selection tasks, include these fields in the stack decision:

- `target_framework`: existing framework and current rollout backend, if known.
- `primary_backend` and `fallback_backend`: for example SGLang primary with disk reload fallback, or vLLM primary with checkpoint/full reload fallback.
- `weight_update_path`: disk/checkpoint, tensor/IPC, NCCL/distributed group, or full reload.
- `cache_policy`: flush, namespace, TTL, lease, or explicit stale-cache acceptance.
- `logprob_policy`: behavior logprobs captured by rollout, recomputed by trainer, or both with consistency validation.
- `topology`: colocated train/rollout, disaggregated train/rollout, PD disaggregation, or external service.
- `non_claims`: GPU, NCCL, multi-node, production, and performance are unverified unless local artifacts are cited.

All capability statements on this page are source-reported unless explicitly marked otherwise. Local throughput or quality claims require separate evidence.
