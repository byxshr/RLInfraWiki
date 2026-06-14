---
id: system-roll
title: ROLL
type: system
frameworks:
- roll
backends:
- ray
- vllm
- sglang
- megatron-lm
components:
- training
- rollout
- reward
- scheduler
algorithms:
- ppo
- grpo
- rlvr
deployment_modes:
- ray-multirole
- async
tags:
- roll
- ray
- agentic
- rlvr
- async
- code-evidenced
confidence: source-reported
reproducibility: source-reading
sources:
- source-roll-ray-agentic-refs
- repo-alibaba-roll-readme
version_sensitive:
- vs-roll-main-2026-06-12
created_at: '2026-06-12'
updated_at: '2026-06-14'
summary: ROLL is a Ray orchestration system for async agentic RL, multi-turn rollout,
  RLVR, and multi-role pipelines with Megatron-Core, SGLang, and vLLM integration.
risks:
- observability-gap
- long-tail-rollout
- rollback-gap
- resource-placement-gap
- stale-policy
capabilities:
- capability-rollout-agentic-multiturn
- capability-rollout-server-async
- capability-policy-versioning
related_pages:
- framework-roll
- pattern-ray-multirole
- pattern-async-rollout
- comparisons-orchestration-options
- interface-orchestrator-adapter
- validation-stale-policy-bound
---

# ROLL

ROLL is a source-reported reference for Ray multi-role worker placement, RLVR reward roles, and agentic asynchronous rollout. It is especially useful as cross-framework evidence when a design needs explicit role topology rather than an opaque training loop.

## Source-Reported Capabilities

- ROLL README records a Ray-based multi-role distributed architecture and heterogeneous task scheduling in `source-roll-ray-agentic-refs` claim `claim-roll-ray-multirole-readme`.
- Agentic async rollout/training support is source-reported through `claim-roll-agentic-async-feature` and the async example config `claim-roll-agentic-async-config`.
- Worker role config captures role name, worker class, model/training/data/generation/strategy args, device mapping, model update frequency, and Ray actor concurrency (`claim-roll-worker-role-config`).
- Device overlap detection and placement/resource manager paths are recorded in `claim-roll-device-overlap-detection`, `claim-roll-base-resource-manager`, and `claim-roll-placement-group-download`.
- Agentic pipeline code creates `actor_train`, `actor_infer`, optional `reference`/`critic`, optional reward cluster, Ray reward scheduler, train rollout scheduler, and validation rollout scheduler (`claim-roll-agentic-cluster-roles`, `claim-roll-reward-scheduler`, `claim-roll-rollout-scheduler-lifecycle`).
- Agentic environment manager records trajectory ids, group ids, tools, state history, step scores, and output queue handoff (`claim-roll-agentic-env-trajectory-ids`).

## Design Notes

- Keep actor_train, actor_infer, reference, reward, and validation roles explicit.
- Ray scheduling and resource placement are part of the architecture, not deployment afterthoughts.
- RLVR reward functions should have local debugging and evidence paths.
- Treat `device_mapping`, `num_gpus_per_worker`, `world_size`, actor concurrency, and overlap rules as reviewable contract fields.
- Separate lifecycle checks for model download, cluster initialization, reward scheduler, rollout schedulers, model update pair, checkpoint/resume, and failure cleanup.
- For agentic tasks, require trajectory ids, group ids, state hashes, tool metadata, step scores, reward fields, and stale-policy/version fields before trainer admission.

## Cross-Framework Transfer

- To AReaL: ROLL's Ray role topology can inform orchestration planning, but AReaL proxy/Ray boundaries must be checked separately.
- To slime/verl: ROLL's explicit role config can inspire adapter contracts for data-buffer or Ray trainer integration without copying framework-specific worker classes.
- To SGLang/vLLM: backend selection and cache/logprob risk pages should still validate rollout backend behavior independently from Ray scheduler topology.

## Failure Modes

- Role `device_mapping` overlaps are accidental rather than deliberate colocation.
- Scheduler named actors initialize without corresponding cluster health checks.
- Async generation drains trajectories without preserving group ids or state hashes.
- Reward scheduler failures return missing or delayed rewards that are treated as valid zero rewards.
- Source-reported observability is mistaken for locally verified performance.

## Validation Ideas

- Static-check role config for actor_train, actor_infer, reference, reward, validation, device mapping, and overlap policy.
- Render a Ray topology artifact listing named actors, placement groups, resource owner, startup order, and shutdown/failure hooks.
- Validate that every trajectory has `traj_group_id`, `traj_id`, state hash, reward, tool metadata, policy/version fields, and terminal status.
- Fault-inject reward scheduler failure and long-tail rollout timeout in a fixture before accepting a production design.

## Open Gaps

- No local ROLL runtime, Ray cluster, GPU, multi-node, or performance command was executed for this page.
- Worker lifecycle and model update behavior need target-task code review before implementation.
- Production reliability, quality, and scaling claims remain unverified.

## Non-Claims

All capability statements on this page are source-reported or inferred from cited source ids. This page does not claim GPU, NCCL, multi-node, throughput, latency, quality, or production validation.
