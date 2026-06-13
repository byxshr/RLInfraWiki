---
name: RLInfraWiki
description: Use this skill for RL/RLHF/RLVR/agentic-RL infrastructure design, framework adaptation, rollout/training/reward/data-buffer/weight-sync/orchestration/debug tasks, algorithm-infra fit analysis, or adapting known/unknown RL frameworks to source-backed RL infra capabilities.
---

# RLInfraWiki

RLInfraWiki is a source-traceable RL infrastructure dictionary for agents. The repository root is the skill root.

## Required workflow

1. Normalize the user's problem into canonical terms with `resolve_alias.py` or `query.py`.
2. For design, adaptation, or debug tasks, build a context bundle first:
   ```bash
   python scripts/compose_context.py --target-framework <framework> --task "<problem>" --mode design --output work/context_bundle.md
   ```
3. Validate context coverage:
   ```bash
   python scripts/validate_context_bundle.py work/context_bundle.md
   ```
4. Read pages from all four packs using `get_page.py --follow-sources`.
5. If implementation symbols matter, use `search_symbols.py` or `get_page.py --include-source --source-root <root>`.
6. If the framework is unknown, use `map_framework.py` with a repo root and then `plan_adapter.py`.
7. When producing a design, cite page IDs, paths, source IDs, confidence, version sensitivity, and known gaps.

## No Target-Only Rule

If a target framework is known and exists in RLInfraWiki, do not answer from only the framework profile. Every design answer must include:

- Target Framework Pack
- Generic Infra Pack
- Cross-Framework Pack
- Validation & Risk Pack

## Output Contract

Every answer using RLInfraWiki must include:

- relevant page IDs and paths,
- source IDs,
- confidence level,
- version-sensitive notes,
- verified/source-reported/inferred/experimental status,
- context coverage statement,
- known gaps,
- validation commands or checklist.

Do not make performance or production claims unless the performance claim record has model, hardware, workload, metric, value, unit, source ID, and reproducibility.
