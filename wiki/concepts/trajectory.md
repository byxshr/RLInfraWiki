---
id: concept-trajectory
title: Trajectory
type: concept
page_type: concept
components:
- rollout
- data-buffer
summary: Ordered sample record from prompt/environment state through response, reward,
  and metadata.
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

# Trajectory

## Definition
Ordered sample record from prompt/environment state through response, reward, and metadata.

## Infra contract
Track the term explicitly in task contracts, samples, logs, and validation evidence when it affects rollout/training correctness.

## Related pages
Use related capability, interface, failure-mode, and validation-pattern pages before making design decisions.
