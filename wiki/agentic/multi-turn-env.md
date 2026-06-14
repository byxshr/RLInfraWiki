---
id: agentic-multi-turn-env
title: Multi-Turn Environment
type: agentic
frameworks:
- areal
- slime
- verl
- roll
backends:
- sglang
- vllm
components:
- environment
- rollout
- reward
algorithms:
- rlvr
deployment_modes:
- async
tags:
- agentic
- tool-calling
- multi-turn
- code-evidenced
confidence: inferred
reproducibility: source-reading
sources:
- source-areal-agentic-async-refs
- source-roll-ray-agentic-refs
- source-slime-agentic-buffer
- repo-inclusionai-areal-readme
- repo-thudm-slime-readme
- repo-verl-readme
- repo-alibaba-roll-readme
version_sensitive:
- vs-areal-main-2026-06-12
- vs-slime-main-2026-06-12
- vs-verl-main-2026-06-12
- vs-roll-main-2026-06-12
created_at: '2026-06-12'
updated_at: '2026-06-14'
summary: Multi-turn environments require state, session affinity, cache/version handling,
  and partial trajectory rules.
risks:
- reward-delay
- long-tail-rollout
- stale-policy
- sample-schema-drift
- rollout-deadlock
related_pages:
- agentic-tool-calling
- capability-rollout-agentic-multiturn
- interface-environment-adapter
- interface-algorithm-data-contract
- failure-sample-schema-drift
- validation-train-infer-schema-match
---

# Multi-Turn Environment

Multi-turn environments turn a single prompt into a stateful trajectory. The contract has to preserve session identity, environment state, tool observations, token spans, reward timing, cache/version boundaries, and partial trajectory rules.

## Evidence Basis

- `source-areal-agentic-async-refs` records AReaL's rollout workflow contract, tensor fields including `logprobs` and `versions`, grouped rollout partial handling, high-level agent workflow resolution, and a multi-turn math example that appends messages, attaches rewards, discounts turns, and exports interactions.
- `source-roll-ray-agentic-refs` records ROLL's agentic async config, separate `actor_train`/`actor_infer`/`reference` roles, environment manager trajectory ids, group ids, state hashes, tool metadata, and step/episode scores.
- `source-slime-agentic-buffer` records an asynchronous trajectory buffer pattern that can ingest agent-generated samples through a training-facing interface.

## Design Checks

- Define the identity tuple before training: `env_id`, `session_id`, `trajectory_id`, `group_id`, `turn_id`, `sample_id`, and framework-specific rollout ids.
- Record state transitions: observation hash, action/tool call, tool output hash, reward source, termination reason, timeout/retry/cancellation state, and partial acceptance flag.
- Bind token data to each turn: prompt tokens, response tokens, `loss_mask`, `attention_mask`, `old_logprob`, train/replay logprob policy, and `policy_version` or per-token `versions`.
- State whether cache affinity is per session, per request, or disabled; stale KV cache is a correctness risk when multi-turn state crosses weight updates.
- Specify partial trajectory rules for rejected groups, all-`None` groups, tool timeout, environment reset failure, and reward service failure.

## Failure Modes

- Session affinity breaks and later turns are generated with a different cache namespace or backend state.
- Trainer admits a partial trajectory without the mask, reward, or provenance required to recompute loss.
- Environment reset failure or tool timeout is converted into a normal zero-reward sample without evidence.
- Grouped rollout drops invalid samples, but downstream batching assumes the original group size.
- `policy_version` lag exceeds the accepted stale-policy bound for long-running episodes.

## Validation Checklist

- Round-trip one multi-turn sample through the data buffer and assert identity fields, state hashes, messages, tools, masks, logprobs, reward, and `policy_version`.
- Force one turn to timeout and verify the sample is rejected or marked partial with a terminal reason.
- Recompute a small replay batch and compare train/infer schema, tokenization, masks, old logprobs, and reward fields.
- Validate grouped rollout behavior when one run returns `None` and when all runs return `None`.

## Open Gaps

- Evidence is source reading only; no local AReaL/ROLL/slime multi-turn run was executed.
- Frameworks disagree on transcript shape and turn packing. Adapter code should isolate those differences behind `EnvironmentAdapter` and `AlgorithmDataContract`.
- Long-tail budgeting and stale-policy thresholds remain task-specific design choices.

## Non-Claims

All capability statements on this page are source-reported or inferred from cited source ids. This page does not claim GPU, NCCL, multi-node, throughput, latency, quality, or production validation.
