# Query: Cross Framework Lessons

> Auto-generated. Do not edit manually.

| page | frameworks | lesson summary |
|---|---|---|
| `comparison-cross-framework-lessons` | `slime`, `verl`, `roll`, `areal` | Cross-framework lessons for target-aware but not target-only RL infrastructure design. |
| `comparison-weight-sync-options` | `slime`, `verl`, `roll`, `areal` | Compare disk, tensor, distributed, and delta weight synchronization options for RL rollout backends. |
| `comparisons-orchestration-options` | `slime`, `verl`, `areal`, `roll` | Compare controller-worker, Ray multi-role, fully async, and external service orchestration. |
| `comparisons-rl-frameworks` | `slime`, `verl`, `areal`, `roll` | Compare slime, verl, AReaL, and ROLL by backend choices, orchestration style, async support, and agentic workflow fit. |
| `comparisons-rollout-backends` | `vllm`, `sglang` | Compare vLLM and SGLang for RL rollout serving, caching, refit, deterministic evaluation, and PD disaggregation. |
| `comparisons-training-backends` | `verl`, `areal`, `roll`, `megatron-lm` | Compare Megatron, Megatron-FSDP, FSDP/FSDP2, and framework-specific training backends. |
| `framework-areal` | `areal` | AReaL framework profile maps source-reported framework capabilities to generic RLInfraWiki contracts and cross-framework lessons. |
| `framework-roll` | `roll` | ROLL framework profile maps source-reported framework capabilities to generic RLInfraWiki contracts and cross-framework lessons. |
| `framework-slime` | `slime` | slime framework profile maps source-reported framework capabilities to generic RLInfraWiki contracts and cross-framework lessons. |
| `framework-verl` | `verl` | verl framework profile maps source-reported framework capabilities to generic RLInfraWiki contracts and cross-framework lessons. |
| `pattern-async-rollout` | `areal`, `roll`, `slime` | Pattern for asynchronous rollout where generation, tools, rewards, and training update do not advance in lockstep. |
| `pattern-colocated-train-rollout` | `slime`, `verl` | Pattern for shared GPU pools where trainer and rollout engine sleep, wake, or share memory. |
| `pattern-disaggregated-train-rollout` | `slime`, `roll`, `areal` | Pattern for separate training and rollout resources with explicit weight version and transport boundary. |
| `pattern-megatron-sglang` | `slime` | Pattern for a Megatron trainer and SGLang rollout engines connected by slime weight sync, with explicit conversion, cache, version, fallback, and rollback boundaries. |
| `pattern-pd-disaggregation` | `vllm`, `sglang` | Pattern for separating prefill and decode resources, with router and KV-transfer failure surfaces. |
| `pattern-ray-multirole` | `roll`, `verl` | Pattern for explicit Ray roles such as actor_train, actor_infer, reference, reward, and validation. |
