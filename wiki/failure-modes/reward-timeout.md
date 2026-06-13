---
id: failure-reward-timeout
title: Reward timeout
type: failure-mode
page_type: failure-mode
components:
- reward
- verifier
summary: Reward or verifier service does not return within bounded time.
sources:
- repo-thudm-slime-readme
- doc-sglang-rl-systems
- repo-verl-readme
- repo-alibaba-roll-readme
- repo-inclusionai-areal-readme
validation_patterns:
- validation-train-infer-schema-match
risks:
- reward-timeout
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

# Reward timeout

## Failure description
Reward or verifier service does not return within bounded time.

## Detection
Require explicit logs, counters, or schema checks that would reveal the failure in a small review scenario.

## Mitigation
Prefer fail-closed behavior, explicit version metadata, bounded retries, and rollback or fallback paths.

## Validation checklist
Tie this failure to a validation-pattern page before promoting a design.
