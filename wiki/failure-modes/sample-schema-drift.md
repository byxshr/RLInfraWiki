---
id: failure-sample-schema-drift
title: Sample schema drift
type: failure-mode
page_type: failure-mode
components:
- rollout
- data-buffer
- training
frameworks:
- slime
- verl
- roll
- areal
backends:
- sglang
- vllm
algorithms:
- grpo
- rlvr
- ppo
summary: Rollout output and trainer input disagree on required fields.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- repo-verl-readme
- repo-alibaba-roll-readme
- repo-inclusionai-areal-readme
validation_patterns:
- validation-train-infer-schema-match
- validation-logprob-consistency
risks:
- sample-schema-drift
created_at: '2026-06-13'
updated_at: '2026-06-14'
confidence: inferred
reproducibility: contract
version_sensitive: []
tags:
- debug
- training-rollout-mismatch
related_pages:
- recipe-debug-training-rollout-mismatch
- observability-training-inference-mismatch
- interface-algorithm-data-contract
- validation-train-infer-schema-match
deployment_modes: []
---

# Sample schema drift

## Failure description
Rollout output and trainer input disagree on required fields.

## Detection

Record one rollout sample and one trainer batch row with the same `sample_id` or evidence key. Compare required fields: prompt/response token IDs, action/loss mask, attention mask, stop reason, reward/verifier rows, `group_id`, `policy_version`, optional `weight_version`, rollout backend ID, and source IDs for inferred fields.

## Mitigation

Prefer fail-closed behavior when a required field is missing. Add schema validation before data-buffer append and before trainer batch materialization. Quarantine samples whose fields are inferred without provenance.

## Validation checklist

- Cite `interface-algorithm-data-contract` and `validation-train-infer-schema-match`.
- Include a small structural command or log artifact that would fail if a required field is missing.
- Keep local runtime or quality claims out unless the artifact was produced by a local run.
