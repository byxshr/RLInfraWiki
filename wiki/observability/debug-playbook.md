---
id: observability-debug-playbook
title: Debug Playbook
type: observability
frameworks:
- slime
- verl
- areal
- roll
backends:
- sglang
- vllm
- megatron
components:
- observability
- reward
- rollout
algorithms:
- rlvr
- grpo
deployment_modes:
- async
- disaggregated
tags:
- observability
- debug
- training-rollout-mismatch
confidence: inferred
reproducibility: source-reading
evidence_level: code-evidenced
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- repo-verl-readme
- repo-inclusionai-areal-readme
- repo-alibaba-roll-readme
- source-slime-weight-sync-code
- source-sglang-rollout-backend-refs
- source-vllm-rollout-backend-refs
- source-sglang-rl-weight-update-refs
version_sensitive:
- vs-slime-main-2026-06-12
- vs-verl-main-2026-06-12
- vs-areal-main-2026-06-12
- vs-roll-main-2026-06-12
created_at: '2026-06-12'
updated_at: '2026-06-14'
summary: Debugging RL infra needs small repros, replayable trajectories, versioned
  weights, metrics, traces, and evidence logs.
risks:
- observability-gap
- version-mismatch
- nondeterminism
- inconsistent-logprob
- sample-schema-drift
claim_ids:
- claim-sglang-logprob-request-fields
- claim-sglang-sleep-wake-cache-flush
- claim-vllm-pause-resume-cache-control
- claim-vllm-batch-invariant-rl-determinism
related_pages:
- recipe-debug-training-rollout-mismatch
- observability-training-inference-mismatch
- validation-logprob-consistency
- validation-train-infer-schema-match
- failure-inconsistent-logprob
- failure-sample-schema-drift
---

# Debug Playbook

Debugging RL infra needs small repros, replayable trajectories, versioned weights, metrics, traces, and evidence logs.

## Evidence To Collect

- Exact command and config.
- Source and target weight version.
- Prompt, response, token IDs, logprobs, reward, and route metadata.
- Rollout backend flags affecting cache, batching, and determinism.
- Failure logs and rollback action.

## Failure Isolation Order

1. Reduce to one replayable sample before comparing aggregate metrics.
2. Confirm version identity and cache policy before logprob comparison.
3. Recompute or replay logprobs with the same tokenizer, masks, weights, precision, and sampling settings.
4. Validate sample schema and trainer batch fields before blaming the backend.
5. Record the first boundary where evidence diverges and stop promotion until it is fixed or explicitly scoped out.

## Non-Claims

Debug packets are evidence-routing artifacts. They do not verify GPU, NCCL, multi-node execution, throughput, latency, quality, or production readiness unless local commands, logs, and artifacts are attached.

All capability statements on this page are source-reported unless explicitly marked otherwise. Local throughput or quality claims require separate evidence.
