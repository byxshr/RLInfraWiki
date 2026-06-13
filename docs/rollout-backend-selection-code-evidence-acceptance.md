# Rollout Backend Selection Code Evidence Acceptance

Date: 2026-06-13

This document is the command checklist for the P1 rollout backend selection content upgrade. It is intentionally limited to code-evidenced/source-reading content and does not claim local GPU, NCCL, multi-node, production, or performance verification.

## Scope

Promoted rollout backend selection from framework-summary content into RL infra dictionary entries backed by SourcePack-style refs:

- page ids: `capability-rollout-backend-selection`, `comparisons-rollout-backends`, `backend-vllm`, `backend-sglang`, `pattern-colocated-train-rollout`, `pattern-disaggregated-train-rollout`, `pattern-pd-disaggregation`, `observability-training-inference-mismatch`, `interface-rollout-backend-adapter`, `failure-stale-kv-cache`, `failure-inconsistent-logprob`, `validation-logprob-consistency`
- source ids: `source-vllm-rollout-backend-refs`, `source-sglang-rollout-backend-refs`, `source-sglang-rl-weight-update-refs`
- evidence level: `code-evidenced` via local-clone ingestion and stable source refs
- confidence: source-reported or inferred, not locally verified

## Commands

Run from `RLInfraWiki/`:

```bash
python scripts/validate.py
python scripts/generate_indices.py --check
python scripts/repo_status.py
python scripts/query.py "rollout backend selection SGLang vLLM cache logprob weight update" --limit 10
python scripts/query.py "colocated disaggregated rollout backend RLVR" --limit 10
python scripts/compose_context.py --target-framework verl --task "select rollout backend between SGLang and vLLM for RLVR with cache logprob and weight update risks" --mode design --output /tmp/rollout-backend-context.md
python scripts/validate_context_bundle.py /tmp/rollout-backend-context.md
conda run -n rl-infra-design-agents pytest -q
```

Optional source-policy checks:

```bash
python scripts/verify_source_refs.py
python scripts/get_page.py capability-rollout-backend-selection --follow-sources
python scripts/get_page.py comparisons-rollout-backends --follow-sources
```

If the main repository submodule pointer or status docs are updated, run from `rl-infra-design-agents/` the affected checks and record the result in the final implementation summary.

## Non-Claims

- No local GPU rollout was executed.
- No local NCCL or multi-node run was executed.
- No production deployment was verified.
- No throughput, latency, memory, quality, or stability number is promoted to locally verified.
- Upstream performance or production wording remains source-reported unless a local artifact is added.
