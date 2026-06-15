# RLInfraWiki

RLInfraWiki is a standalone, source-traceable RL infrastructure dictionary and Codex/Claude skill. The repository root is the skill root: `SKILL.md`, `data/`, `sources/`, `wiki/`, `queries/`, `references/`, and `scripts/` live together.

It is designed for RL/RLHF/RLVR/agentic-RL infrastructure design, framework adaptation, rollout/training/reward/data-buffer/weight-sync/orchestration/debug tasks, and unknown framework mapping.

## Quick Start

```bash
python scripts/query.py "Megatron SGLang weight sync" --limit 8
python scripts/compose_context.py \
  --target-framework verl \
  --task "add SGLang rollout backend with weight sync" \
  --mode design \
  --output /tmp/context_bundle.md
python scripts/validate_context_bundle.py /tmp/context_bundle.md
python scripts/get_page.py interface-weight-sync-adapter --follow-sources
python scripts/validate.py
python scripts/generate_indices.py --check
```

For rollout backend selection:

```bash
python scripts/query.py "rollout backend selection SGLang vLLM cache logprob weight update" --limit 10
python scripts/compose_context.py \
  --target-framework verl \
  --task "select rollout backend between SGLang and vLLM for RLVR with cache logprob and weight update risks" \
  --mode design \
  --output /tmp/rollout-backend-context.md
python scripts/validate_context_bundle.py /tmp/rollout-backend-context.md
python scripts/get_page.py capability-rollout-backend-selection --follow-sources
```

For unknown frameworks:

```bash
python scripts/compose_context.py \
  --target-framework smoke \
  --repo-root tests/fixtures/minimal_rl_framework \
  --task "add SGLang rollout backend" \
  --mode adapter \
  --output /tmp/smoke-context.md
python scripts/map_framework.py --name smoke --repo-root tests/fixtures/minimal_rl_framework --output /tmp/smoke-profile.yaml
python scripts/plan_adapter.py --profile /tmp/smoke-profile.yaml --context /tmp/smoke-context.md --target add-sglang-rollout-backend --output /tmp/smoke-plan.md
```

## Source Policy

Local clones are ingestion backends only. Wiki pages cite stable source IDs, source refs, upstream commits, paths, line ranges, claim IDs, hashes, confidence, and known gaps. Do not vendor full upstream RL framework repositories, and do not mark source-reported claims as locally verified without command, hardware/context, log/artifact, and result evidence.

Source ref validation has two layers:

```bash
python scripts/verify_source_refs.py
python scripts/verify_source_refs.py --check-local --source-root ..
python scripts/refresh_sources.py --dry-run --source-root .. --markdown-output /tmp/rlinfrawiki-source-refresh-report.md
```

The default checker is CI-safe and validates SourcePack metadata without requiring upstream clones. The local checker expects sibling clones under `--source-root`, verifies recorded commits, paths, line ranges, and real hashes, and reports legacy `sha256: source-reported` refs as warnings unless `--strict-hash` is used.

## Content Status

- Rollout backend selection P1 is code-evidenced/source-reading as of 2026-06-13 through `source-vllm-rollout-backend-refs`, `source-sglang-rollout-backend-refs`, and `source-sglang-rl-weight-update-refs`.
- Primary page ids are `capability-rollout-backend-selection`, `comparisons-rollout-backends`, `backend-vllm`, and `backend-sglang`.
- Unverified boundaries remain GPU execution, NCCL, multi-node, production deployment, and performance numbers.

## Main-Repo Integration

`rl-infra-design-agents` can consume this repository as a submodule or equivalent pinned local dependency at `.agents/skills/RLInfraWiki`. If the remote `https://github.com/byxshr/RLInfraWiki` is unavailable, use local `../RLInfraWiki` and later switch `.gitmodules` to the remote URL.
