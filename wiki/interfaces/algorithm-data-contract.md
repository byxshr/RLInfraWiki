---
id: interface-algorithm-data-contract
title: AlgorithmDataContract
type: interface
page_type: interface
components:
- algorithm
- data-buffer
required_methods:
- required_fields
- batch_invariants
- loss_masks
required_fields:
- request_id
- status
- evidence_ref
capabilities:
- capability-sample-grouping
failure_modes:
- failure-sample-schema-drift
summary: AlgorithmDataContract is a minimal adapter contract for the algorithm, data-buffer
  component boundary.
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

# AlgorithmDataContract

## Contract
This page defines fields and lifecycle hooks an adapter plan must name before implementation.

## Required methods
- `required_fields`
- `batch_invariants`
- `loss_masks`

## Required fields
Carry page-specific fields into task bundles, logs, and validation artifacts.

## Failure modes
Linked failure modes are source-reported or inferred from framework summaries and must be handled in the plan.

## Validation checklist
A review-ready design cites the validation patterns that prove the adapter behavior.
