---
id: interface-data-buffer-adapter
title: DataBufferAdapter
type: interface
page_type: interface
components:
- data-buffer
required_methods:
- append_trajectory
- sample_batch
- validate_schema
required_fields:
- request_id
- status
- evidence_ref
capabilities:
- capability-data-buffer
failure_modes:
- failure-sample-schema-drift
summary: DataBufferAdapter is a minimal adapter contract for the data-buffer component
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

# DataBufferAdapter

## Contract
This page defines fields and lifecycle hooks an adapter plan must name before implementation.

## Required methods
- `append_trajectory`
- `sample_batch`
- `validate_schema`

## Required fields
Carry page-specific fields into task bundles, logs, and validation artifacts.

## Failure modes
Linked failure modes are source-reported or inferred from framework summaries and must be handled in the plan.

## Validation checklist
A review-ready design cites the validation patterns that prove the adapter behavior.
