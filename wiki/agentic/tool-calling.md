---
id: agentic-tool-calling
title: Tool Calling
type: agentic
frameworks:
- areal
- slime
- verl
- roll
backends:
- openai-compatible
- sglang
- vllm
components:
- environment
- reward
- rollout
algorithms:
- rlvr
- grpo
deployment_modes:
- async
- external-service
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
summary: Tool-calling RL needs transcript capture, token/logprob attribution, timeout
  handling, and reward provenance.
risks:
- reward-delay
- long-tail-rollout
- stale-policy
- tool-hang
- provenance-gap
related_pages:
- agentic-multi-turn-env
- agentic-openai-compatible-agent-app
- interface-environment-adapter
- capability-reward-verifier
- validation-reward-timeout-retry
- failure-tool-hang
---

# Tool Calling

Tool-calling RL is an adapter boundary between the agent runtime and the trainer. A design should preserve the tool transcript, token/logprob attribution, reward provenance, and policy version for each trainable segment instead of treating a tool call as plain text.

## Evidence Basis

- `source-areal-agentic-async-refs` records AReaL's agent service session handling, tool-call event emission, multi-turn reward attachment, rollout workflow return contract, logprob fields, and per-token `versions` fields. Relevant claim ids include `claim-areal-agent-service-session-tool-events`, `claim-areal-multiturn-reward-export`, and `claim-areal-rollout-versions-logprobs`.
- `source-roll-ray-agentic-refs` records ROLL's agentic environment manager trajectory identifiers, tool metadata, state hash, step scores, and Ray handoff to an output queue. Relevant claim ids include `claim-roll-agentic-env-trajectory-ids` and `claim-roll-agentic-role-config`.
- `source-slime-agentic-buffer` records slime's asynchronous agent trajectory buffer references, which are useful as a cross-framework ingestion pattern for externally generated tool trajectories.

These sources support a source-reported/inferred design contract. They do not verify model quality, runtime speed, or production reliability.

## Design Checks

- Define a stable tool-call record: `call_id`, `tool_name`, structured arguments, observation payload hash, tool status, timeout status, retry count, and exception class.
- Keep transcript provenance separate from trainable token spans. Tool observations may become prompt context, while tool-call arguments, sampled tokens, logprobs, `loss_mask`, and `attention_mask` need explicit attribution.
- Store reward provenance: reward source, verifier version, reward timeout/retry/cancellation result, delayed reward state, and whether a partial trajectory is accepted or rejected.
- Track `policy_version` or per-token `versions` for every generated segment, then bound stale-policy consumption before the trainer computes loss.
- Preserve cross-framework portability by mapping the generic environment adapter contract before copying AReaL proxy or ROLL Ray role assumptions.

## Failure Modes

- Tool runtime hangs or returns after the trainer has already admitted newer samples.
- Tool-call serialization differs between rollout runtime and tokenizer/template used by training.
- Tool observations are present in text but missing from provenance records, making replay impossible.
- Reward/verifier output is delayed or missing, causing hidden partial trajectories.
- `policy_version`, `old_logprob`, and `loss_mask` are missing for segments produced through tool branches.

## Validation Checklist

- Replay a stored transcript and confirm tool-call records, observations, token spans, masks, rewards, and `policy_version` survive serialization.
- Inject a tool timeout and verify cancellation/retry state is recorded and the trajectory is either marked partial or rejected.
- Recompute logprobs for at least one tool branch and compare masks/schema against the rollout record.
- Run schema checks for `call_id`, `trajectory_id`, `group_id`, `policy_version`, `old_logprob`, reward source, and verifier status.

## Open Gaps

- The current evidence is line-level source reading, not a local end-to-end run of AReaL, ROLL, slime, verl, SGLang, or vLLM.
- Tool schemas and transcript exporters differ by framework; adapter recipes still need target-specific code review before implementation.
- Long-tail handling requires workload-specific stop conditions and stale-policy budgets.

## Non-Claims

All capability statements on this page are source-reported or inferred from cited source ids. This page does not claim GPU, NCCL, multi-node, throughput, latency, quality, or production validation.
