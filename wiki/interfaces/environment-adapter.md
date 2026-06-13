---
id: interface-environment-adapter
title: EnvironmentAdapter
type: interface
page_type: interface
components:
- environment
- rollout
required_methods:
- reset
- step
- call_tool
- close_episode
required_fields:
- request_id
- status
- evidence_ref
capabilities:
- capability-environment
failure_modes:
- failure-sample-schema-drift
summary: EnvironmentAdapter is a minimal adapter contract for the environment, rollout
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

# EnvironmentAdapter

## Contract
This page defines fields and lifecycle hooks an adapter plan must name before implementation.

## Required methods
- `reset`
- `step`
- `call_tool`
- `close_episode`

## Required fields
Carry page-specific fields into task bundles, logs, and validation artifacts.

## Failure modes
Linked failure modes are source-reported or inferred from framework summaries and must be handled in the plan.

## Validation checklist
A review-ready design cites the validation patterns that prove the adapter behavior.
