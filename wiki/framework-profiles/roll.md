---
id: framework-roll
title: ROLL framework profile
type: framework-profile
page_type: framework-profile
framework: roll
frameworks:
- roll
components:
- training
- rollout
- reward
- scheduler
training_backends:
- megatron-lm
rollout_backends:
- vllm
- sglang
backends:
- megatron-lm
- vllm
- sglang
algorithms:
- ppo
- grpo
- rlvr
- agentic-rl
deployment_modes:
- colocated
- disaggregated
- async
capability_map:
  capability-rollout-server-async:
    status: source-reported
    source_ids:
    - source-roll-ray-agentic-refs
    - repo-alibaba-roll-readme
  pattern-async-rollout:
    status: source-reported
    source_ids:
    - source-roll-ray-agentic-refs
    - repo-alibaba-roll-readme
  pattern-ray-multirole:
    status: source-reported
    source_ids:
    - source-roll-ray-agentic-refs
    - repo-alibaba-roll-readme
  capability-rollout-agentic-multiturn:
    status: source-reported
    source_ids:
    - source-roll-ray-agentic-refs
    - repo-alibaba-roll-readme
  capability-weight-sync-distributed:
    status: backend-specific
    source_ids: &id001
    - source-roll-ray-agentic-refs
    - repo-alibaba-roll-readme
  capability-rollout-logprob-capture:
    status: source-reported
    source_ids: *id001
  capability-policy-versioning:
    status: required-contract
    source_ids: *id001
implements_interfaces:
- interface-trainer-backend-adapter
- interface-rollout-backend-adapter
- interface-weight-sync-adapter
- interface-data-buffer-adapter
comparable_frameworks: &id002
- framework-slime
- framework-verl
- framework-areal
relations:
  lessons_from: *id002
  compare_with:
  - comparison-rl-frameworks
  - comparisons-rollout-backends
summary: ROLL framework profile maps source-reported Ray multi-role and async agentic
  capabilities to generic RLInfraWiki contracts and cross-framework lessons.
confidence: source-reported
reproducibility: source-reading
sources: *id001
created_at: '2026-06-13'
updated_at: '2026-06-14'
version_sensitive: []
tags: []
risks: []
---

# ROLL framework profile

## Capability map
Use this page as an entry point only; a design must still read generic contracts, cross-framework lessons, and validation/risk pages. The async rollout and `pattern-ray-multirole` entries are source-reported from ROLL source ids and must not be treated as runtime verification.

## Transferable lessons
Transfer lessons only after checking backend assumptions, orchestration model, policy lag, and validation coverage.

## Negative transfer risks
Do not copy backend-specific weight update or worker lifecycle assumptions without target-side evidence.

## Non-Claims
This profile does not claim GPU, NCCL, multi-node, throughput, latency, quality, or production validation.

## Related pages
Read interface-weight-sync-adapter, interface-rollout-backend-adapter, capability-policy-versioning, and validation pages.
