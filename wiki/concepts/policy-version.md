---
id: concept-policy-version
title: Policy version
type: concept
page_type: concept
components:
- training
- rollout
summary: Identifier for the behavior policy that produced samples or serves rollout
  requests.
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

# Policy version

## Definition
Identifier for the behavior policy that produced samples or serves rollout requests.

## Infra contract
Track the term explicitly in task contracts, samples, logs, and validation evidence when it affects rollout/training correctness.

## Related pages
Use related capability, interface, failure-mode, and validation-pattern pages before making design decisions.
