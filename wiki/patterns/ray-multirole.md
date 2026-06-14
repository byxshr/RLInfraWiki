---
id: pattern-ray-multirole
title: Ray Multi-Role
type: pattern
frameworks:
- roll
- verl
backends:
- ray
- vllm
- sglang
components:
- scheduler
- training
- rollout
- reward
algorithms:
- rlvr
deployment_modes:
- ray-multirole
tags:
- pattern
- architecture
- ray
- multirole
- async
- code-evidenced
confidence: inferred
reproducibility: source-reading
sources:
- source-roll-ray-agentic-refs
- source-areal-agentic-async-refs
- repo-thudm-slime-readme
- repo-verl-readme
- repo-inclusionai-areal-readme
- repo-alibaba-roll-readme
- repo-vllm-readme
- repo-sglang-readme
version_sensitive:
- vs-slime-main-2026-06-12
- vs-verl-main-2026-06-12
- vs-areal-main-2026-06-12
- vs-roll-main-2026-06-12
- vs-vllm-main-2026-06-12
- vs-sglang-main-2026-06-12
created_at: '2026-06-12'
updated_at: '2026-06-14'
summary: Ray orchestration pattern for explicit roles such as actor_train, actor_infer,
  reference, reward, placement, schedulers, and validation.
risks:
- stale-policy
- version-mismatch
- observability-gap
- resource-placement-gap
- lifecycle-gap
related_pages:
- system-roll
- system-areal
- pattern-async-rollout
- interface-orchestrator-adapter
- comparisons-orchestration-options
- failure-distributed-rank-mismatch
---

# Ray Multi-Role

Ray multi-role orchestration makes training, inference, reference, reward, validation, schedulers, and resource placement explicit architecture components. It is most useful when a task needs heterogeneous engines or role-specific scaling, and most risky when role lifecycle and placement are implicit.

## Evidence Basis

- `source-roll-ray-agentic-refs` records ROLL's Ray-based multi-role README claim, `WorkerConfig` role/device/resource fields, device-overlap helper, base resource manager, placement-group model download, agentic clusters for `actor_train`, `actor_infer`, optional `reference`/`critic`/`reward`, Ray reward scheduler, and train/val rollout scheduler initialization.
- `source-areal-agentic-async-refs` records AReaL's Ray scheduler entry point and an explicit proxy-worker limitation under `RayScheduler`. This provides a useful contrast: Ray support must be checked per integration boundary, not assumed from a framework label.

## Use When

- The task objective names these frameworks or components.
- The acceptance criteria require explicit failure modes, rollback, and observability.
- The rollout and training surfaces have different latency, memory, or scaling needs.

## Design Checks

- List roles and lifecycle separately: `actor_train`, `actor_infer`, `reference`, `critic`, `reward`, train rollout scheduler, validation rollout scheduler, data manager, and model update path.
- Declare resource placement: node count, GPUs per node, role `device_mapping`, colocated/disaggregated pairs, placement groups, and overlap policy.
- Define startup/shutdown ordering: model download, cluster initialization, scheduler creation, model update pair setup, checkpoint/resume, and failure cleanup.
- Define cross-role data contracts: prompt batch, trajectory ids, group ids, state hashes, rewards, logprobs, policy versions, weight versions, and model update metadata.
- Decide how observability hands off between Ray actor logs, tracker metrics, context bundle source ids, and review-gate artifacts.

## Failure Modes

- Role device mappings overlap unintentionally, causing hidden colocation or resource starvation.
- Schedulers start before referenced clusters are initialized.
- Reward or rollout scheduler failure leaves queued trajectories without terminal state.
- Proxy/OpenAI-compatible integration is assumed to work under Ray even when source code marks it unsupported for a scheduler path.
- Actor lifecycle logs are not tied to Wiki source ids, making design review untraceable.

## Validation Ideas

- Version monotonicity test.
- Cache flush or cache namespace test.
- Rollout/train logprob mismatch smoke test.
- Failure injection for sync timeout or partial reward.
- Static config test for role presence, device mapping, and actor-infer overlap.
- Lifecycle smoke test that verifies scheduler initialization order and named actor creation.
- Context bundle check that includes target, generic, cross-framework, validation, and risk evidence.

## Open Gaps

- Evidence is source reading only; no local Ray cluster or multi-node run was executed.
- ROLL and AReaL expose different Ray boundaries. Adapter planning must verify the exact target scheduler path.
- Placement and lifecycle checks need target task contracts before they can become executable tests.

## Non-Claims

All capability statements on this page are source-reported or inferred from cited source ids. This page does not claim GPU, NCCL, multi-node, throughput, latency, quality, or production validation.
