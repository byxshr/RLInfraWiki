---
id: adapter-add-sglang-rollout-backend
title: Add SGLang rollout backend
type: adapter-recipe
page_type: adapter-recipe
components:
- rollout
- weight-sync
- training
backends:
- sglang
adapter_targets:
- add-sglang-rollout-backend
required_pages:
- interface-rollout-backend-adapter
- interface-weight-sync-adapter
- capability-policy-versioning
summary: Add SGLang rollout backend recipe lists context pages, implementation tasks,
  validation matrix entries, and risk controls.
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
algorithms: []
deployment_modes: []
---

# Add SGLang rollout backend

## Target capability
This recipe targets `add-sglang-rollout-backend` and must be grounded by a context bundle.

## Required interface contracts
- `interface-rollout-backend-adapter`
- `interface-weight-sync-adapter`
- `capability-policy-versioning`

## Implementation tasks
Map target framework lifecycle, define adapter methods, attach version fields, add observability, and write failure-focused validation.

## Validation matrix
Include page/source IDs for all claims and validation/risk pages for every production or performance-adjacent statement.

## Source pages to read
Use `get_page.py --follow-sources` for each required page before drafting a final plan.
