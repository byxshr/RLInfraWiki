---
id: interface-weight-sync-adapter
title: WeightSyncAdapter
type: interface
page_type: interface
components:
- weight-sync
required_methods:
- prepare_update
- pause_or_drain_rollout
- transfer_weights
- verify_update
- resume_rollout
- rollback_or_fail_closed
required_fields:
- policy_id
- weight_version
- training_step
capabilities:
- capability-weight-sync
failure_modes:
- failure-partial-weight-update
- failure-stale-kv-cache
summary: WeightSyncAdapter is a minimal adapter contract for the weight-sync component
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

# WeightSyncAdapter

## Contract
This page defines fields and lifecycle hooks an adapter plan must name before implementation.

## Required methods
- `prepare_update`
- `pause_or_drain_rollout`
- `transfer_weights`
- `verify_update`
- `resume_rollout`
- `rollback_or_fail_closed`

## Required fields
Carry page-specific fields into task bundles, logs, and validation artifacts.

## Failure modes
Linked failure modes are source-reported or inferred from framework summaries and must be handled in the plan.

## Validation checklist
A review-ready design cites the validation patterns that prove the adapter behavior.
