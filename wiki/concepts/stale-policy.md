---
id: concept-stale-policy
title: Stale policy
type: concept
page_type: concept
components:
- rollout
- training
summary: A policy lag condition where samples are trained under a newer policy than
  the one that generated them.
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

# Stale policy

## Definition
A policy lag condition where samples are trained under a newer policy than the one that generated them.

## Infra contract
Track the term explicitly in task contracts, samples, logs, and validation evidence when it affects rollout/training correctness.

## Related pages
Use related capability, interface, failure-mode, and validation-pattern pages before making design decisions.
