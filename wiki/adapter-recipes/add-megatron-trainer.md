---
id: adapter-add-megatron-trainer
title: Add Megatron trainer backend
type: adapter-recipe
page_type: adapter-recipe
components:
- rollout
- weight-sync
- training
backends: []
adapter_targets:
- add-megatron-trainer
required_pages:
- interface-trainer-backend-adapter
- interface-weight-sync-adapter
summary: Add Megatron trainer backend recipe lists context pages, implementation tasks,
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

# Add Megatron trainer backend

## Target capability
This recipe targets `add-megatron-trainer` and must be grounded by a context bundle.

## Required interface contracts
- `interface-trainer-backend-adapter`
- `interface-weight-sync-adapter`

## Implementation tasks
Map target framework lifecycle, define adapter methods, attach version fields, add observability, and write failure-focused validation.

## Validation matrix
Include page/source IDs for all claims and validation/risk pages for every production or performance-adjacent statement.

## Source pages to read
Use `get_page.py --follow-sources` for each required page before drafting a final plan.
