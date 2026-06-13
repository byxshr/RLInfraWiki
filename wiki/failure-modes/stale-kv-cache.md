---
id: failure-stale-kv-cache
title: Stale KV cache
type: failure-mode
page_type: failure-mode
components:
- rollout
- weight-sync
summary: Prefix/KV cache survives across a weight update without namespacing or flush.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- source-slime-weight-sync-code
- source-sglang-rl-weight-update-refs
validation_patterns:
- validation-weight-version-monotonicity
- validation-pause-update-resume
risks:
- stale-kv-cache
created_at: '2026-06-13'
updated_at: '2026-06-13'
confidence: inferred
reproducibility: contract
version_sensitive: []
tags: []
frameworks: []
backends: []
algorithms: []
deployment_modes: []
---

# Stale KV cache

## Failure description
Prefix/KV cache survives across a weight update without namespacing or flush.

## Detection
Require explicit logs, counters, or schema checks that would reveal the failure in a small review scenario.

## Mitigation
Prefer fail-closed behavior, explicit version metadata, bounded retries, and rollback or fallback paths.

## Validation checklist
Tie this failure to a validation-pattern page before promoting a design.
