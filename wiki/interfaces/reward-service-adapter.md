---
id: interface-reward-service-adapter
title: RewardServiceAdapter
type: interface
page_type: interface
components:
- reward
- verifier
required_methods:
- score
- timeout
- retry_or_fail_closed
required_fields:
- request_id
- status
- evidence_ref
capabilities:
- capability-reward-service
failure_modes:
- failure-sample-schema-drift
summary: RewardServiceAdapter is a minimal adapter contract for the reward, verifier
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

# RewardServiceAdapter

## Contract
This page defines fields and lifecycle hooks an adapter plan must name before implementation.

## Required methods
- `score`
- `timeout`
- `retry_or_fail_closed`

## Required fields
Carry page-specific fields into task bundles, logs, and validation artifacts.

## Failure modes
Linked failure modes are source-reported or inferred from framework summaries and must be handled in the plan.

## Validation checklist
A review-ready design cites the validation patterns that prove the adapter behavior.
