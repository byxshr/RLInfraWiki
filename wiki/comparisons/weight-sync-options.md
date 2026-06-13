---
id: comparison-weight-sync-options
title: Weight sync options
type: comparison
page_type: comparison
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
summary: Compare disk, tensor, distributed, and delta weight synchronization options
  for RL rollout backends.
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

# Weight sync options

## Decision matrix
| option | fit | fallback | key risk |
|---|---|---|---|
| disk | safest full reload | last known-good checkpoint | slow or mutable checkpoint |
| tensor | colocated fast update | disk | IPC/resource cleanup |
| distributed | disaggregated high-throughput update | disk | rank mismatch or partial bucket update |
| delta | sparse update when baseline is trusted | full resync | baseline drift |

## Validation
Always include weight_version, flush_cache/cache policy, update atomicity, and fallback evidence.
