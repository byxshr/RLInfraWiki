---
id: system-areal
title: AReaL
type: system
frameworks:
- areal
backends:
- sglang
- vllm
- fsdp
- megatron
components:
- training
- rollout
- environment
- reward
- scheduler
algorithms:
- ppo
- grpo
- dapo
- rloo
deployment_modes:
- async
- external-service
tags:
- areal
- agentic
- async
- openai-compatible
- ray
- code-evidenced
confidence: source-reported
reproducibility: source-reading
sources:
- source-areal-agentic-async-refs
- repo-inclusionai-areal-readme
version_sensitive:
- vs-areal-main-2026-06-12
created_at: '2026-06-12'
updated_at: '2026-06-14'
summary: AReaL focuses on fully asynchronous RL and agentic workflows, including OpenAI-compatible
  application integration.
risks:
- stale-policy
- reward-delay
- long-tail-rollout
- proxy-boundary
- scheduler-boundary
capabilities:
- capability-rollout-agentic-multiturn
- capability-rollout-server-async
- capability-policy-versioning
related_pages:
- framework-areal
- pattern-async-rollout
- agentic-openai-compatible-agent-app
- agentic-multi-turn-env
- pattern-ray-multirole
- validation-stale-policy-bound
---

# AReaL

AReaL is a target anchor for fully asynchronous agentic RL, online proxy patterns, and existing agent applications reachable through OpenAI-compatible APIs. Use it as source-reported evidence for design planning, then verify the selected scheduler, proxy, backend, and data contract in target code before implementation.

## Source-Reported Capabilities

- Fully asynchronous RL and agentic RL positioning is recorded in `source-areal-agentic-async-refs` claim `claim-areal-async-agentic-readme`.
- OpenAI-compatible app reuse through base-url style integration is recorded in `claim-areal-openai-compatible-base-url`.
- Multi-turn/tool examples are recorded in `claim-areal-agentic-example-table`, `claim-areal-multiturn-reward-export`, and `claim-areal-agent-service-session-tool-events`.
- Rollout workflow contract includes tensor/logprob/version fields and partial grouped rollout behavior through `claim-areal-rollout-versions-logprobs` and `claim-areal-grouped-rollout-partial`.
- Staleness recovery, pause/continue generation, and staleness metrics are recorded in `claim-areal-staleness-recovery`, `claim-areal-rollout-pause-continue`, and `claim-areal-version-staleness-metrics`.
- Ray scheduler entry is source-reported, while proxy workers are explicitly marked unsupported with `RayScheduler` in the cited trainer path (`claim-areal-ray-scheduler-entry`, `claim-areal-proxy-ray-limit`).

## Design Notes

- Model rollout as asynchronous workflow execution with explicit policy version tracking.
- Separate agent runtime API from trainer API.
- Track delayed rewards, hanging tools, partial trajectories, and stale policy.
- Treat OpenAI-compatible proxy support and Ray scheduler support as separate axes. Do not assume an app proxy design can be moved into Ray mode without source-side support.
- Require target task contracts to define `policy_version`, `old_logprob`, `versions`, `loss_mask`, reward provenance, cache policy, and stale-policy stop conditions.
- When AReaL is target, pair this page with generic pages for environment adapters, async rollout, tool calling, stale-policy bound, and train/infer schema matching.

## Cross-Framework Transfer

- From slime: asynchronous agent trajectory buffer and custom data generation are useful ingestion patterns when agent apps are external.
- From ROLL: Ray multi-role placement and scheduler lifecycle are useful references if AReaL target work needs a Ray-like topology, but source-specific proxy constraints must be checked.
- From SGLang/vLLM: cache, logprob, deterministic replay, and pause/update/resume pages provide backend risk checks for async AReaL designs.

## Failure Modes

- Long-tail tool tasks create stale samples that pass trainer admission without bounded version lag.
- OpenAI-compatible requests are recorded as text only and lose tool/provenance metadata.
- Proxy worker assumptions conflict with Ray scheduler mode.
- Rollout pause/continue hooks are called without matching cache/version validation.

## Validation Ideas

- Compose a context bundle for the target task and require Target, Generic, Cross-Framework, and Validation & Risk packs.
- Static-check a sample schema for `versions`, `old_logprob`, `loss_mask`, reward fields, and trajectory/session ids.
- Inject reward timeout, tool timeout, and stale-policy cases in a fixture before treating the design as implementation-ready.
- Verify scheduler/proxy compatibility in code before claiming an OpenAI-compatible agent app can run under a specific deployment mode.

## Open Gaps

- No local AReaL runtime, GPU, Ray, multi-node, or performance command was executed for this page.
- Backend-specific behavior for SGLang/vLLM/Megatron/FSDP remains source-reported unless tied to separate source ids and local artifacts.
- Production service behavior, reliability, and quality remain unverified.

## Non-Claims

All capability statements on this page are source-reported or inferred from cited source ids. This page does not claim GPU, NCCL, multi-node, throughput, latency, quality, or production validation.
