---
id: framework-areal
title: AReaL framework profile
type: framework-profile
page_type: framework-profile
framework: areal
frameworks:
- areal
components:
- training
- rollout
- environment
- reward
- scheduler
training_backends:
- fsdp
- megatron
rollout_backends:
- vllm
- sglang
backends:
- fsdp
- megatron
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
    - source-areal-agentic-async-refs
    - repo-inclusionai-areal-readme
  pattern-async-rollout:
    status: source-reported
    source_ids:
    - source-areal-agentic-async-refs
    - repo-inclusionai-areal-readme
  async-rollout:
    status: source-reported
    source_ids:
    - source-areal-agentic-async-refs
    - repo-inclusionai-areal-readme
  capability-rollout-agentic-multiturn:
    status: source-reported
    source_ids:
    - source-areal-agentic-async-refs
    - repo-inclusionai-areal-readme
  capability-weight-sync-distributed:
    status: backend-specific
    source_ids: &id001
    - source-areal-agentic-async-refs
    - repo-inclusionai-areal-readme
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
- framework-roll
relations:
  lessons_from: *id002
  compare_with:
  - comparison-rl-frameworks
  - comparisons-rollout-backends
summary: AReaL framework profile maps source-reported async agentic framework capabilities
  to generic RLInfraWiki contracts and cross-framework lessons.
confidence: source-reported
reproducibility: source-reading
sources: *id001
created_at: '2026-06-13'
updated_at: '2026-06-14'
version_sensitive: []
tags: []
risks: []
---

# AReaL framework profile

## Capability map
Use this page as an entry point only; a design must still read generic contracts, cross-framework lessons, and validation/risk pages. The `async-rollout` entries are source-reported from AReaL source ids and must not be treated as runtime verification.

## Transferable lessons
Transfer lessons only after checking backend assumptions, orchestration model, policy lag, and validation coverage.

## Negative transfer risks
Do not copy backend-specific weight update or worker lifecycle assumptions without target-side evidence.

## Non-Claims
This profile does not claim GPU, NCCL, multi-node, throughput, latency, quality, or production validation.

## Related pages
Read interface-weight-sync-adapter, interface-rollout-backend-adapter, capability-policy-versioning, and validation pages.
