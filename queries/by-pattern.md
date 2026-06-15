# Query: Pattern

> Auto-generated. Do not edit manually.

| Page | Summary |
|---|---|
| [Async Rollout](../wiki/patterns/async-rollout.md) | Pattern for asynchronous rollout where generation, tools, rewards, and training update do not advance in lockstep. |
| [Colocated Train Rollout](../wiki/patterns/colocated-train-rollout.md) | Pattern for shared GPU pools where trainer and rollout engine sleep, wake, or share memory. |
| [Disaggregated Train Rollout](../wiki/patterns/disaggregated-train-rollout.md) | Pattern for separate training and rollout resources with explicit weight version and transport boundary. |
| [Megatron plus SGLang](../wiki/patterns/megatron-sglang.md) | Pattern for a Megatron trainer and SGLang rollout engines connected by slime weight sync, with explicit conversion, cache, version, fallback, and rollback boundaries. |
| [Prefill Decode Disaggregation](../wiki/patterns/pd-disaggregation.md) | Pattern for separating prefill and decode resources, with router and KV-transfer failure surfaces. |
| [Ray Multi-Role](../wiki/patterns/ray-multirole.md) | Ray orchestration pattern for async agentic RL, multi-turn rollout, tool calling, stale policy control, and explicit actor_train, actor_infer, reference, reward, placement, schedulers, and validation roles. |
