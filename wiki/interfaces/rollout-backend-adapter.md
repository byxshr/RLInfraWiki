---
id: interface-rollout-backend-adapter
title: RolloutBackendAdapter
type: interface
page_type: interface
components:
- rollout
required_methods:
- generate
- capture_logprobs
- report_weight_version
- pause_or_drain
- resume
required_fields:
- request_id
- prompt_tokens
- response_tokens
- sampling_params
- backend_id
- policy_version
- status
- evidence_ref
capabilities:
- capability-rollout-backend-selection
failure_modes:
- failure-sample-schema-drift
- failure-stale-kv-cache
- failure-inconsistent-logprob
summary: RolloutBackendAdapter is a minimal adapter contract for the rollout component
  boundary.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- source-slime-weight-sync-code
- source-sglang-rl-weight-update-refs
- source-sglang-rollout-backend-refs
- source-vllm-rollout-backend-refs
created_at: '2026-06-13'
updated_at: '2026-06-13'
confidence: inferred
reproducibility: source-reading
evidence_level: code-evidenced
version_sensitive: []
tags:
- rollout-backend-selection
- code-evidenced
risks: []
frameworks:
- slime
- verl
backends:
- sglang
- vllm
algorithms:
- grpo
- rlvr
deployment_modes:
- colocated
- disaggregated
claim_ids:
- claim-vllm-pause-resume-cache-control
- claim-vllm-rl-weight-transfer-backends
- claim-sglang-pause-continue-generation
- claim-sglang-logprob-request-fields
- claim-sglang-refit-strategy-selection
related_pages:
- capability-rollout-backend-selection
- comparisons-rollout-backends
- validation-logprob-consistency
- validation-weight-version-monotonicity
---

# RolloutBackendAdapter

## Contract
This page defines fields and lifecycle hooks an adapter plan must name before implementation.

## Required methods
- `generate`
- `capture_logprobs`
- `report_weight_version`
- `pause_or_drain`
- `resume`

## Required fields
- `request_id`
- `prompt_tokens`
- `response_tokens`
- `sampling_params`
- `backend_id`
- `policy_version`
- `status`
- `evidence_ref`

Carry these fields into task bundles, logs, and validation artifacts. For rollout backend selection, `backend_id` and `policy_version` are required because cache and logprob failures often only become visible after samples cross into the trainer.

## Failure modes
- `failure-stale-kv-cache`: a sample was generated with cache from another policy version or cache namespace.
- `failure-inconsistent-logprob`: rollout behavior logprobs and trainer recomputation do not align.
- `failure-partial-weight-update`: only some workers or shards updated before rollout resumed.

## Validation checklist
- Attach `validation-logprob-consistency` when the algorithm uses old logprobs.
- Attach `validation-weight-version-monotonicity` when rollout weights update during training.
- Attach `validation-pause-update-resume` when the backend supports mid-flight update.
- Record source IDs and claim IDs for the selected backend; do not cite local clone paths in the design.
