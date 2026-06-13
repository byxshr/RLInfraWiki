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
required_fields:
- request_id
- status
- evidence_ref
capabilities:
- capability-rollout-backend
failure_modes:
- failure-sample-schema-drift
summary: RolloutBackendAdapter is a minimal adapter contract for the rollout component
  boundary.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- source-slime-weight-sync-code
- source-sglang-rl-weight-update-refs
created_at: '2026-06-13'
updated_at: '2026-06-13'
confidence: inferred
reproducibility: contract
version_sensitive: []
tags: []
risks: []
frameworks: []
backends: []
algorithms: []
deployment_modes: []
---

# RolloutBackendAdapter

## Contract
This page defines fields and lifecycle hooks an adapter plan must name before implementation.

## Required methods
- `generate`
- `capture_logprobs`
- `report_weight_version`

## Required fields
Carry page-specific fields into task bundles, logs, and validation artifacts.

## Failure modes
Linked failure modes are source-reported or inferred from framework summaries and must be handled in the plan.

## Validation checklist
A review-ready design cites the validation patterns that prove the adapter behavior.
