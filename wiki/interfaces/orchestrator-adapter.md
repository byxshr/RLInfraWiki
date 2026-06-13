---
id: interface-orchestrator-adapter
title: OrchestratorAdapter
type: interface
page_type: interface
components:
- scheduler
- orchestration
required_methods:
- allocate
- start_role
- stop_role
- health_check
required_fields:
- request_id
- status
- evidence_ref
capabilities:
- capability-orchestrator
failure_modes:
- failure-sample-schema-drift
summary: OrchestratorAdapter is a minimal adapter contract for the scheduler, orchestration
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

# OrchestratorAdapter

## Contract
This page defines fields and lifecycle hooks an adapter plan must name before implementation.

## Required methods
- `allocate`
- `start_role`
- `stop_role`
- `health_check`

## Required fields
Carry page-specific fields into task bundles, logs, and validation artifacts.

## Failure modes
Linked failure modes are source-reported or inferred from framework summaries and must be handled in the plan.

## Validation checklist
A review-ready design cites the validation patterns that prove the adapter behavior.
