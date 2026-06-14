---
id: agentic-openai-compatible-agent-app
title: OpenAI-Compatible Agent App
type: agentic
frameworks:
- areal
backends:
- openai-compatible
components:
- environment
- rollout
- reward
algorithms:
- rlvr
deployment_modes:
- external-service
- async
tags:
- agentic
- tool-calling
- multi-turn
- openai-compatible
- code-evidenced
confidence: inferred
reproducibility: source-reading
sources:
- source-areal-agentic-async-refs
- source-roll-ray-agentic-refs
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
summary: OpenAI-compatible agent apps let existing agent runtimes connect through
  base_url style proxy patterns.
risks:
- reward-delay
- long-tail-rollout
- stale-policy
- proxy-boundary
- observability-gap
related_pages:
- agentic-tool-calling
- agentic-multi-turn-env
- system-areal
- pattern-async-rollout
- validation-stale-policy-bound
---

# OpenAI-Compatible Agent App

OpenAI-compatible agent apps let an existing agent runtime call an RL-controlled model endpoint through a `base_url` style boundary. That boundary is useful for reuse, but it must be treated as a traceable control plane: request ids, session keys, tool events, rewards, and version state must flow back into the trainer.

## Evidence Basis

- `source-areal-agentic-async-refs` records AReaL README claims for black-box agent applications via OpenAI-compatible endpoint replacement, agent service session management, tool-call emission, multi-turn reward export, and the proxy worker boundary in the trainer.
- The same AReaL source ref records an explicit limitation: proxy workers are not supported with the Ray scheduler in the cited trainer code path. This is a design constraint, not a negative claim about the whole project.
- `source-roll-ray-agentic-refs` provides the complementary Ray-oriented orchestration evidence for cases where the app is integrated as a ROLL agentic pipeline rather than as an OpenAI-compatible proxy.

## Design Checks

- Separate the external app API from the training adapter. The app may speak OpenAI-compatible chat, but the trainer needs typed records for tokens, masks, logprobs, rewards, and versions.
- Require `session_key` or equivalent affinity for multi-turn apps; close sessions on hard failures and record whether a retry created a new session.
- Capture streamed deltas and tool-call events before summary truncation so reward/verifier replay can inspect the full transcript.
- Define request lifecycle states: accepted, generation started, tool pending, tool completed, reward pending, exported, rejected, cancelled, timed out.
- Declare scheduler constraints before implementation. For AReaL, cited source code marks proxy workers unsupported with `RayScheduler`; ROLL covers a different Ray-native integration path.

## Failure Modes

- The app returns only a final answer and drops tool-call provenance needed for reward attribution.
- A proxy retry creates a second session, making transcript replay disagree with training data.
- The trainer consumes a sample without knowing which `policy_version` served the OpenAI-compatible request.
- Ray-native orchestration assumptions are copied into an OpenAI-compatible proxy design without checking scheduler support.

## Validation Checklist

- Run a request lifecycle smoke test with one successful tool call, one timeout, and one cancelled request; assert session id, request id, tool events, reward status, and version fields.
- Export a transcript and verify `old_logprob`, masks, reward source, and tokenization can be recomputed or explicitly marked unavailable.
- Check adapter startup under the intended scheduler mode and fail fast if proxy/Ray support is absent.

## Open Gaps

- Evidence is source reading only; no local proxy worker, Ray scheduler, or external agent app was run.
- OpenAI-compatible request schemas vary across agent SDKs. A production adapter needs target SDK-specific schema tests.
- Streaming and tool-event truncation policies need implementation-specific review.

## Non-Claims

All capability statements on this page are source-reported or inferred from cited source ids. This page does not claim GPU, NCCL, multi-node, throughput, latency, quality, or production validation.
