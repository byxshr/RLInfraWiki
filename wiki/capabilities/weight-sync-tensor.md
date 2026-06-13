---
id: capability-weight-sync-tensor
title: Tensor in-memory weight sync
type: capability
page_type: capability
components:
- weight-sync
frameworks:
- slime
- verl
- roll
- areal
backends:
- sglang
- vllm
related_interfaces: &id001
- interface-weight-sync-adapter
validation_patterns: &id002
- validation-pause-update-resume
failure_modes:
- failure-partial-weight-update
- failure-stale-kv-cache
known_implementations:
- framework: slime
  support: source-reported
  source_ids:
  - repo-thudm-slime-readme
- framework: verl
  support: source-reported
  source_ids:
  - repo-verl-readme
relations:
  generalizes_to: *id001
  validation_patterns: *id002
  lessons_from:
  - framework-slime
  - framework-roll
  - framework-areal
summary: Tensor in-memory weight sync is an RL infrastructure capability with explicit
  adapter contracts, failure modes, and validation requirements.
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
algorithms: []
deployment_modes: []
---

# Tensor in-memory weight sync

## Definition
Tensor in-memory weight sync describes a reusable RL infrastructure capability rather than a single framework implementation.

## Required semantics
Define ownership, lifecycle boundaries, version fields, failure atomicity, and observability before implementing the capability.

## Minimal adapter contract
Read the related interface pages and carry required fields into plans, task contracts, and review evidence.

## Known implementations
Support status is source-reported from upstream docs/code summaries unless local evidence explicitly proves otherwise.

## Failure modes
Treat linked failure pages as design blockers until mitigations and validation checks are named.

## Validation checklist
Use linked validation pages to make the design reviewable and reproducible.
