---
id: comparisons-orchestration-options
title: Orchestration Options
type: comparison
frameworks:
- slime
- verl
- areal
- roll
backends:
- ray
- openai-compatible
components:
- scheduler
- training
- rollout
- reward
algorithms:
- rlvr
deployment_modes:
- ray-multirole
- async
- external-service
tags:
- comparison
- decision-matrix
- orchestration
- ray
- async
- code-evidenced
confidence: inferred
reproducibility: source-reading
sources:
- source-roll-ray-agentic-refs
- source-areal-agentic-async-refs
- source-slime-agentic-buffer
- repo-alibaba-roll-readme
- repo-inclusionai-areal-readme
- repo-thudm-slime-readme
version_sensitive:
- vs-roll-main-2026-06-12
- vs-areal-main-2026-06-12
- vs-slime-main-2026-06-12
created_at: '2026-06-12'
updated_at: '2026-06-14'
summary: Compare controller-worker, Ray multi-role, fully async, and external service
  orchestration.
risks:
- provenance-gap
- observability-gap
- stale-policy
- resource-placement-gap
related_pages:
- pattern-ray-multirole
- pattern-async-rollout
- system-areal
- system-roll
- agentic-openai-compatible-agent-app
- interface-orchestrator-adapter
---

# Orchestration Options

Use this page to compare controller-worker, Ray multi-role, fully async, and OpenAI-compatible external-service orchestration. The right answer is task-specific: known target frameworks should shape the Target pack, but design review still needs Generic, Cross-Framework, and Validation & Risk evidence.

## Evidence Basis

- `source-roll-ray-agentic-refs` provides code-level source ids for Ray multi-role worker config, placement/resource manager, role clusters, reward scheduler, rollout schedulers, async agentic config, and trajectory ids.
- `source-areal-agentic-async-refs` provides source ids for fully async agentic RL, OpenAI-compatible app boundary, rollout workflow fields, staleness metrics, pause/continue hooks, Ray scheduler entry, and proxy/Ray limitation.
- `source-slime-agentic-buffer` provides an async agent trajectory buffer reference that is useful for controller-worker or external data generation designs.

## Decision Matrix

| Option | Fits When | Evidence Anchors | Main Risks | Required Validation |
|---|---|---|---|---|
| Controller-worker/data-buffer | Agent generation can be external but trainer ingestion should stay simple. | slime buffer source ids, generic data-buffer and algorithm-data-contract pages. | Hidden partial trajectories, delayed reward, schema drift. | Schema round trip, group ids, reward provenance, replay/recompute. |
| Ray multi-role | Roles need explicit resource placement and heterogeneous scheduling. | ROLL `claim-roll-worker-role-config`, `claim-roll-agentic-cluster-roles`, `claim-roll-rollout-scheduler-lifecycle`. | Device overlap, scheduler lifecycle gaps, actor failure isolation. | Static role topology, placement/overlap check, named actor startup order, failure injection. |
| Fully async rollout | Tool/reward/generation latency makes synchronous rollout inefficient or brittle. | AReaL staleness/version claims, ROLL async config, vLLM/SGLang cache/logprob risk pages. | Stale policy, stale KV cache, long-tail queue drain, mismatch between rollout/train logprobs. | Stale-policy bound, cache namespace/flush, logprob replay, delayed reward timeout. |
| OpenAI-compatible app proxy | Existing agent app should be reused behind a chat-compatible endpoint. | AReaL OpenAI-compatible base-url and agent service claims. | Transcript truncation, missing tool provenance, scheduler/proxy incompatibility. | Request lifecycle trace, session affinity, tool event export, proxy/scheduler compatibility check. |

## Design Questions

- Target: Which framework is the implementation target, and which source ids prove the target supports the intended boundary?
- Generic: Which adapter contracts are required for trainer, rollout backend, environment, reward service, data buffer, and orchestrator?
- Cross-framework: Which lessons transfer from AReaL, ROLL, slime, verl, SGLang, and vLLM without copying target-incompatible assumptions?
- Validation & Risk: Which failure modes are in scope: stale policy, stale cache, missing provenance, tool hang, reward timeout, sample schema drift, or distributed rank/resource mismatch?

## Failure Isolation Order

1. Validate sample identity and provenance: `trajectory_id`, `group_id`, `session_id`, source ids, claim ids.
2. Validate schema and masks: tokens, `loss_mask`, `attention_mask`, tool transcript, reward fields.
3. Validate version/cache: `policy_version`, `weight_version`, cache namespace/flush, stale-policy bound.
4. Validate orchestration lifecycle: actor startup, scheduler startup, queue drain, cancellation, shutdown.
5. Validate replay/recompute: rollout logprobs, trainer logprobs, reward/verifier replay, stop conditions.

## Open Gaps

- This comparison is source-reading based; it does not verify any framework runtime locally.
- It intentionally avoids throughput, latency, quality, and production claims.
- Target implementation must add code-specific artifacts before review gate should accept performance or production claims.

## Non-Claims

All capability statements on this page are source-reported or inferred from cited source ids. This page does not claim GPU, NCCL, multi-node, throughput, latency, quality, or production validation.
