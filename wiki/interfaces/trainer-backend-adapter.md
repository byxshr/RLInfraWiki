---
id: interface-trainer-backend-adapter
title: TrainerBackendAdapter
type: interface
page_type: interface
components:
- training
required_methods:
- prepare_step
- export_checkpoint
- report_policy_version
required_fields:
- request_id
- status
- evidence_ref
capabilities:
- capability-trainer-backend
failure_modes:
- failure-sample-schema-drift
summary: TrainerBackendAdapter is a minimal adapter contract for the training component
  boundary.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- repo-verl-readme
- repo-alibaba-roll-readme
- repo-inclusionai-areal-readme
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

# TrainerBackendAdapter

## Contract
This page defines fields and lifecycle hooks an adapter plan must name before implementation.

## Required methods
- `prepare_step`
- `export_checkpoint`
- `report_policy_version`

## Required fields
Carry page-specific fields into task bundles, logs, and validation artifacts.

## Failure modes
Linked failure modes are source-reported or inferred from framework summaries and must be handled in the plan.

## Validation checklist
A review-ready design cites the validation patterns that prove the adapter behavior.
