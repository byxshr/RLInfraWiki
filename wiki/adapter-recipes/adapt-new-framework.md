---
id: adapter-adapt-new-framework
title: Adapt a new RL framework
type: adapter-recipe
page_type: adapter-recipe
components:
- rollout
- weight-sync
- training
backends: []
adapter_targets:
- adapt-new-framework
required_pages:
- interface-rollout-backend-adapter
- interface-weight-sync-adapter
- interface-algorithm-data-contract
summary: Adapt a new RL framework recipe lists context pages, implementation tasks,
  validation matrix entries, and risk controls.
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
algorithms: []
deployment_modes: []
---

# Adapt a new RL framework

## Target capability
This recipe targets `adapt-new-framework` and must be grounded by a context bundle.

## Required interface contracts
- `interface-rollout-backend-adapter`
- `interface-weight-sync-adapter`
- `interface-algorithm-data-contract`

## Implementation tasks
Map target framework lifecycle, define adapter methods, attach version fields, add observability, and write failure-focused validation.

## Validation matrix
Include page/source IDs for all claims and validation/risk pages for every production or performance-adjacent statement.

## Source pages to read
Use `get_page.py --follow-sources` for each required page before drafting a final plan.
