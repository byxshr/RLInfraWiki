---
id: backend-sglang
title: SGLang
type: backend
frameworks:
- sglang
backends:
- sglang
components:
- rollout
- inference
- router
- weight-sync
algorithms:
- rlhf
- grpo
deployment_modes:
- external-service
- disaggregated
tags:
- sglang
- radixattention
- prefix-caching
- pd-disaggregation
- rollout-backend-selection
- code-evidenced
confidence: source-reported
reproducibility: source-reading
evidence_level: code-evidenced
sources:
- repo-sglang-readme
- doc-sglang-rl-systems
- doc-sglang-faq-determinism
- doc-sglang-pd-disaggregation
- source-sglang-rollout-backend-refs
- source-sglang-rl-weight-update-refs
version_sensitive:
- vs-sglang-main-2026-06-12
created_at: '2026-06-12'
updated_at: '2026-06-13'
summary: SGLang is the rollout/refit backend for the P0 slime + Megatron path, with
  documented disk, tensor, and distributed weight update APIs plus cache flush,
  sleep/wake, deterministic inference, PD, and router surfaces.
risks:
- nondeterminism
- cache-staleness
- partial-weight-update
claim_ids:
- claim-sglang-rl-lifecycle-surfaces
- claim-sglang-sleep-wake-cache-flush
- claim-sglang-refit-strategy-selection
- claim-sglang-disk-refit-request-fields
- claim-sglang-tensor-refit-request-fields
- claim-sglang-distributed-refit-request-fields
- claim-sglang-pause-continue-generation
- claim-sglang-deterministic-inference-rl-need
- claim-sglang-logprob-request-fields
- claim-sglang-pd-disaggregation-selection
- claim-sglang-pd-router
related_pages:
- comparisons-rollout-backends
- capability-rollout-backend-selection
- pattern-colocated-train-rollout
- pattern-disaggregated-train-rollout
- pattern-pd-disaggregation
- validation-logprob-consistency
---

# SGLang

SGLang is the rollout/refit backend for the P0 slime + Megatron weight sync path. Treat it as an inference engine with explicit lifecycle APIs, not as a passive model loader: the design must say when generation pauses, which weight update API is used, whether KV/prefix cache is flushed, and how `weight_version` is observed.

## Evidence Basis

- `source-sglang-rollout-backend-refs` claim `claim-sglang-rl-lifecycle-surfaces` records SGLang's RL lifecycle surfaces: sleep/wake, refit, postponed generation, deterministic inference, and router.
- Claim `claim-sglang-sleep-wake-cache-flush` records memory-aware sleep/wake and the cache flush behavior after releasing KV cache.
- Claim `claim-sglang-refit-strategy-selection` records disk, tensor, and distributed refit strategy selection.
- Claims `claim-sglang-disk-refit-request-fields`, `claim-sglang-tensor-refit-request-fields`, and `claim-sglang-distributed-refit-request-fields` record endpoint fields including `flush_cache` and `weight_version`.
- Claim `claim-sglang-pause-continue-generation` records the pause-generation/update/continue-generation boundary and pause modes.
- Claims `claim-sglang-deterministic-inference-rl-need`, `claim-sglang-deterministic-inference-backends`, and `claim-sglang-deterministic-test-hooks` record deterministic inference rationale, backend compatibility, and test hooks.
- Claim `claim-sglang-logprob-request-fields` records native request fields for returning log probabilities.
- Claims `claim-sglang-pd-disaggregation-selection` and `claim-sglang-pd-router` record prefill/decode separation and router integration.

## Design Implications

- Disk refit is the safest fallback because the checkpoint directory is an external source of truth and can bootstrap newly added rollout engines.
- Tensor refit is a colocated optimization and should only be selected when tensor ownership, GPU residency, and IPC/serialization boundaries are explicit.
- Distributed refit is the natural match for disaggregated slime rollout because training workers and rollout engines can join a dedicated NCCL group, but the design must include group creation and teardown.
- Cache policy is part of correctness. If updated weights change token probabilities, stale KV/prefix cache can invalidate rollout/train logprob comparison.
- PD disaggregation and Model Gateway routing add separate failure domains; prefill, decode, router health, and cache transfer should be monitored independently.
- SGLang is a strong first choice for this repository's P0 slime + Megatron path because existing code evidence already covers SGLang refit, `weight_version`, `flush_cache`, and full fallback semantics.

## Failure Modes

- Updating while requests are still running can create partial-version generations unless the scheduler is paused or requests are aborted.
- `flush_cache=false` can preserve throughput but risks stale-policy behavior after weight changes.
- A distributed group with mismatched rank offsets, world size, or backend can deadlock or leave engines waiting for tensors.
- Tensor updates can silently fail at the design level if dtype/shape/name lists do not match the engine loader expectation.
- Deterministic evaluation claims can be invalidated by dynamic batching, cache reuse, or non-deterministic sampling settings.

## Validation Ideas

- Exercise one disk update with `weight_version="smoke-v1"` and verify every rollout engine reports or logs the new version before accepting rollout data.
- For distributed refit, validate `init_weights_update_group` -> `update_weights_from_distributed` -> `destroy_weights_update_group` in one smoke run and fail closed on any Ray/NCCL timeout.
- Run a small cached-vs-uncached logprob check with deterministic inference settings when the design depends on reward or policy logprob equality.
- Record whether `flush_cache` was true for each weight update in the rollout metrics/log bundle.

## Open Gaps

- No local GPU run has verified SGLang latency, memory, or quality behavior for this project.
- RLInfraWiki does not yet index SGLang implementation symbols behind each HTTP endpoint; current evidence is official local docs plus slime caller code.

All capability statements on this page are source-reported unless explicitly marked otherwise. Local throughput or quality claims require separate evidence.
