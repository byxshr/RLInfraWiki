---
id: comparison-cross-framework-lessons
title: Cross-framework lessons
type: comparison
page_type: comparison
components:
- rollout
- weight-sync
- training
frameworks:
- slime
- verl
- roll
- areal
summary: Cross-framework lessons for target-aware but not target-only RL infrastructure
  design.
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
backends: []
algorithms: []
deployment_modes: []
---

# Cross-framework lessons

## Lessons
Use the target framework as the lifecycle anchor, generic interfaces as the design contract, other frameworks as analogs, and validation pages as promotion gates.

## Negative transfer
Do not copy worker lifecycles, backend update APIs, or async policy-lag assumptions without target-side evidence.
