#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import jsonschema

from _context import compose_bundle, write_context_sidecars
from _rlinfra import PROJECT_ROOT, append_jsonl, ensure_workspace_dirs, load_jsonl, now_iso, read_task_contract, sha256_file
from render_goal import render_goal

PLANNED_FILES = [
    "task_contract.yaml",
    "docs/goal.md",
    "docs/draft.md",
    "docs/plan.md",
    "docs/architecture.md",
    "docs/interfaces.md",
    "docs/validation_matrix.md",
    "docs/risk_register.md",
    "docs/review.md",
    "docs/goal_status.md",
    "docs/codex_tasks.md",
    "context/context_bundle.md",
    "context/context_bundle.json",
    "context/context_sources.yaml",
    ".humanize/rlcr_config.yaml",
    ".humanize/loop_state.json",
    ".humanize/codex_invocations.jsonl",
    ".humanize/claude_iterations.jsonl",
    "review_issues.jsonl",
    "review_waivers.jsonl",
    "candidates.jsonl",
    "goal_versions.jsonl",
    "progress_log.md",
    "metrics.csv",
    "review_rounds/README.md",
    "evidence/README.md",
    "runs/README.md",
    "profile/README.md",
]

LEDGER_FILES = [
    ".humanize/codex_invocations.jsonl",
    ".humanize/claude_iterations.jsonl",
    "review_issues.jsonl",
    "review_waivers.jsonl",
    "candidates.jsonl",
]

METRICS_HEADER = "timestamp,metric,value,unit,notes\n"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_if_missing(path: Path, text: str) -> None:
    if path.exists():
        return
    write(path, text)


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(text)


def last_contract_hash(path: Path) -> str | None:
    for row in reversed(load_jsonl(path)):
        value = row.get("contract_hash")
        if value:
            return str(value)
    return None


def validate_metrics_header(path: Path) -> None:
    if not path.exists():
        return
    first_line = path.read_text(encoding="utf-8").splitlines()
    current = first_line[0] + "\n" if first_line else ""
    if current and current != METRICS_HEADER:
        raise SystemExit(
            f"metrics.csv header mismatch: {path}\n"
            f"expected: {METRICS_HEADER.strip()}\n"
            f"found: {current.strip()}"
        )


def validate_contract_schema(contract: dict, contract_path: Path) -> None:
    schema_path = PROJECT_ROOT / "schemas" / "task_contract.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(contract), key=lambda err: list(err.path))
    if errors:
        details = "\n".join(f"- {'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}" for err in errors)
        raise SystemExit(f"task contract failed schema validation: {contract_path}\n{details}")


def first_target_framework(contract: dict) -> str | None:
    frameworks = contract.get("target_frameworks") or []
    if isinstance(frameworks, list) and frameworks:
        return str(frameworks[0])
    return None


def knowledge_basis_table(bundle: dict) -> str:
    rows = []
    labels = {
        "target_framework_pack": "Target Framework Pack",
        "generic_infra_pack": "Generic Infra Pack",
        "cross_framework_pack": "Cross-Framework Pack",
        "validation_risk_pack": "Validation & Risk Pack",
    }
    for key, label in labels.items():
        pages = bundle.get("packs", {}).get(key, [])
        page_ids = ", ".join(f"`{page.get('page_id')}`" for page in pages) or "missing"
        gaps = "; ".join(bundle.get("known_gaps", [])[:2])
        rows.append(f"| {label} | yes | {page_ids} | {gaps} |")
    return "\n".join([
        "## Knowledge Basis",
        "",
        "| pack | required | pages used | gaps |",
        "|---|---:|---|---|",
        *rows,
        "",
        "Context artifacts: `context/context_bundle.md`, `context/context_bundle.json`, `context/context_sources.yaml`.",
        "",
    ])


def context_coverage_section(bundle: dict) -> str:
    lines = ["## Context Coverage", ""]
    for key, title in [
        ("target_framework_pack", "target framework pages"),
        ("generic_infra_pack", "generic infra pages"),
        ("cross_framework_pack", "cross-framework pages"),
        ("validation_risk_pack", "validation/risk pages"),
    ]:
        ids = ", ".join(f"`{page.get('page_id')}`" for page in bundle.get("packs", {}).get(key, []))
        lines.append(f"- {title}: {ids}")
    lines.append("- explicit gaps: " + "; ".join(bundle.get("known_gaps", [])))
    lines.append("")
    return "\n".join(lines)


def task_family(contract: dict) -> str:
    text = " ".join([
        str(contract.get("task_name", "")),
        str(contract.get("objective", "")),
        " ".join(str(item) for item in contract.get("components", []) or []),
    ]).lower()
    mentions_rollout_backend = "rollout-backend-selection" in text or "rollout backend" in text or ("rollout" in text and "backend" in text)
    mentions_backend_pair = "sglang" in text and "vllm" in text
    selection_terms = ["select", "selection", "choose", "compare", "matrix", "tradeoff", "trade-off"]
    if (mentions_rollout_backend or mentions_backend_pair) and any(term in text for term in selection_terms):
        return "rollout-backend-selection"
    if any(term in text for term in ["grpo", "rlvr", "algorithm-data-contract", "algorithm data contract"]):
        return "algorithm-data-contract"
    if "weight-sync" in text or "weight synchronization" in text:
        return "weight-sync"
    return "generic"


def render_draft(contract: dict, bundle: dict) -> str:
    queries = contract.get("required_wiki_queries", [])
    family = task_family(contract)
    sections = [
        "# Draft",
        "",
        "## Task contract summary",
        "",
        contract.get("objective", ""),
        "",
        knowledge_basis_table(bundle).rstrip(),
        "",
        "## RLInfraWiki queries run",
        "",
        "| query | top pages | source IDs | notes |",
        "|---|---|---|---|",
        *[
            f"| {q} | see context bundle | see context sources | run query.py for fresh ranking |"
            for q in queries
        ],
        "",
        "## Candidate directions",
        "",
    ]
    if family == "algorithm-data-contract":
        sections.extend([
            "### Candidate A: minimal slime-compatible GRPO/RLVR data contract",
            "",
            "Define a small `AlgorithmDataContract` between rollout, reward/verifier, data buffer, and trainer. Required fields include `sample_id`, `prompt`, `response`, token IDs, action/attention mask, `old_logprob`, optional `reference_logprob`, reward/verifier outputs, `group_id`, `policy_version`, rollout backend identity, and provenance IDs. Required pages include `interface-algorithm-data-contract`, `capability-rollout-logprob-capture`, `capability-sample-grouping`, and `framework-slime`.",
            "",
            "### Candidate B: staged adapter migration",
            "",
            "Keep existing slime rollout/data-buffer flow intact first, then add schema validation, reward timeout handling, grouped sample invariants, and stale-policy filtering before trainer consumption. Required pages include `interface-data-buffer-adapter`, `interface-reward-service-adapter`, `failure-sample-schema-drift`, and `validation-logprob-consistency`.",
            "",
            "## Failure modes to carry forward",
            "",
            "- Sample schema drift between rollout output and trainer input.",
            "- Missing or semantically inconsistent `old_logprob` / `reference_logprob`.",
            "- Reward/verifier timeout or partial reward rows.",
            "- Grouped GRPO samples with incomplete or mixed-policy groups.",
            "- Stale policy samples accepted beyond the configured lag bound.",
        ])
    elif family == "rollout-backend-selection":
        sections.extend([
            "### Candidate A: SGLang primary with vLLM fallback",
            "",
            "Use SGLang as the primary rollout backend when the target framework values explicit RL lifecycle controls: sleep/wake, pause/continue generation, refit choices, `flush_cache`, `weight_version`, logprob request fields, and PD/router surfaces. Keep vLLM as a full fallback when its documented RL weight-transfer backend, pause/resume and cache control, batch-invariance, and disaggregated prefill surfaces are a better fit for the target deployment. Required pages include `capability-rollout-backend-selection`, `backend-sglang`, `backend-vllm`, and `comparisons-rollout-backends`.",
            "",
            "### Candidate B: vLLM primary with SGLang fallback",
            "",
            "Use vLLM as the primary rollout backend when colocated IPC transfer, NCCL/disaggregated transfer, or vLLM-native inference operations are the strongest target match. Keep SGLang as the fallback when rollout lifecycle controls, deterministic inference hooks, cache flushing, and PD/router controls reduce integration risk. Required source IDs include `source-vllm-rollout-backend-refs` and `source-sglang-rollout-backend-refs`.",
            "",
            "## Source-backed evidence to carry forward",
            "",
            "| topic | page IDs | source IDs | review note |",
            "|---|---|---|---|",
            "| selection capability | `capability-rollout-backend-selection`, `comparisons-rollout-backends` | `source-vllm-rollout-backend-refs`, `source-sglang-rollout-backend-refs` | Compare lifecycle, weight update, cache, logprob, topology, and operational complexity. |",
            "| backend profiles | `backend-sglang`, `backend-vllm` | `source-sglang-rollout-backend-refs`, `source-vllm-rollout-backend-refs` | Treat upstream docs/code refs as source-reported until locally reproduced. |",
            "| topology | `pattern-colocated-train-rollout`, `pattern-disaggregated-train-rollout`, `pattern-pd-disaggregation` | `source-vllm-rollout-backend-refs`, `source-sglang-rollout-backend-refs` | Pick topology before claiming a backend is simpler. |",
            "| correctness risks | `failure-stale-kv-cache`, `failure-inconsistent-logprob`, `validation-logprob-consistency` | `source-vllm-rollout-backend-refs`, `source-sglang-rollout-backend-refs` | Cache and logprob validation are promotion blockers. |",
            "",
            "## Failure modes to carry forward",
            "",
            "- Stale KV/prefix cache after weight update or policy switch.",
            "- Inconsistent rollout `old_logprob` versus trainer recomputation.",
            "- Missing or non-monotonic `weight_version` / policy version on requests, samples, logs, and evidence.",
            "- Partial weight update across rollout workers or disaggregated ranks.",
            "- Target-only design that ignores cross-framework lessons and validation pages.",
            "- Unverified throughput, latency, production, GPU, NCCL, or multi-node claim.",
        ])
    elif family == "weight-sync":
        sections.extend([
            "### Candidate A: distributed primary sync",
            "",
            "Primary sync path: Megatron trainer publishes a new `weight_version`, pauses or drains SGLang rollout, transfers weights through the selected distributed/tensor path, requests `flush_cache`, verifies rollout engines report the new version, then resumes generation. Required pages include `interface-weight-sync-adapter`, `capability-weight-sync-distributed`, and `framework-slime`.",
            "",
            "### Candidate B: full checkpoint fallback",
            "",
            "Full fallback: publish an immutable full checkpoint directory, call the backend disk reload path with the same `weight_version`, request `flush_cache`, and fail closed if any engine cannot confirm the update. Required pages include `capability-weight-sync-disk`, `failure-partial-weight-update`, and `validation-weight-version-monotonicity`.",
            "",
            "## Failure modes to carry forward",
            "",
            "- Partial update across rollout engines or buckets.",
            "- Stale KV/prefix cache after rollout resumes.",
            "- Missing `weight_version` on samples, logs, or trainer batches.",
            "- Distributed rank/world-size mismatch.",
            "- Delta baseline drift requiring full checkpoint resync.",
        ])
    else:
        sections.extend([
            "### Candidate A: target-aware adapter plan",
            "",
            "Anchor the design in the target framework while carrying generic RL infrastructure interfaces, cross-framework analogs, and validation/risk pages from the context bundle.",
            "",
            "### Candidate B: generic-first migration plan",
            "",
            "Start from stable interface contracts and map them into target framework symbols only after source inspection.",
        ])
    return "\n".join(sections) + "\n"


def render_plan(contract: dict, bundle: dict) -> str:
    family = task_family(contract)
    sections = [
        "# Executable Plan",
        "",
        "## Objective",
        "",
        contract.get("objective", ""),
        "",
        "## Non-goals",
        "",
        "- Do not implement a new RL framework.",
        "- Do not make unverified performance claims.",
        "",
        "## Chosen architecture",
        "",
    ]
    if family == "algorithm-data-contract":
        sections.extend([
            "Design a slime-compatible GRPO/RLVR data contract across rollout, reward/verifier, data buffer, and trainer boundaries. The first implementation batch should be schema-first: inspect current slime sample fields, map required algorithm fields, add compatibility adapters, and reject or quarantine samples that fail validation.",
            "",
            "## Algorithm Data Contract",
            "",
            "- rollout identity: `sample_id`, prompt/source ID, rollout backend, `policy_version`, optional `weight_version` when weight sync is involved.",
            "- token payload: prompt/response token IDs, action mask, attention mask, stop reason, and per-token alignment metadata.",
            "- policy statistics: behavior `old_logprob`, optional `reference_logprob`, entropy or mask metadata when required by the algorithm.",
            "- grouping: `group_id`, group size, completion index, and invariant checks for GRPO-style grouped advantages.",
            "- reward/verifier: scalar reward, verifier labels, timeout/retry status, and provenance for reward service versions.",
            "- trainer handoff: advantage inputs, loss mask, stale-policy decision, and source IDs for every inferred field.",
            "",
            "## Slime integration points to inspect",
            "",
            "- rollout worker output and SGLang/vLLM response adapters.",
            "- data-buffer append, storage, and trainer batch materialization paths.",
            "- reward/verifier hooks and timeout behavior.",
            "- policy/version metadata propagation from trainer to rollout and back.",
        ])
    elif family == "rollout-backend-selection":
        sections.extend([
            "Design a target-aware rollout backend selection for RLVR/GRPO. The first pass should choose a primary backend and a full fallback, then make the choice reviewable with source-backed evidence, explicit cache/logprob/version contracts, deployment topology, and validation gates. This plan is a design scaffold; it does not verify GPU/NCCL/multi-node execution, throughput, latency, or production readiness.",
            "",
            "## Rollout Backend Selection",
            "",
            "| decision field | required output | evidence to cite |",
            "|---|---|---|",
            "| `target_framework` | First target framework from the task contract, with source-inspection TODOs. | Target Framework Pack page IDs. |",
            "| `primary_backend` | Choose `sglang` or `vllm`; record why this target prefers it. | `capability-rollout-backend-selection`, `backend-sglang`, `backend-vllm`, `comparisons-rollout-backends`. |",
            "| `fallback_backend` | Choose the other backend as the full fallback or explain why fallback is blocked. | Backend profile pages and source IDs. |",
            "| `primary_weight_update_path` | State disk, tensor, distributed, IPC/NCCL, or target-native path as source-reported design, not verified runtime fact. | `interface-weight-sync-adapter`, backend pages, `source-vllm-rollout-backend-refs`, `source-sglang-rollout-backend-refs`. |",
            "| `full_fallback` | Immutable full checkpoint reload or equivalent fail-closed path with the same version identity. | Weight-sync and backend source IDs. |",
            "| `weight_version` / policy version | Attach to rollout requests, backend state, samples, trainer batches, logs, and evidence. | `capability-policy-versioning`, `validation-weight-version-monotonicity`. |",
            "| cache policy | Require `flush_cache`, cache namespace by version, or documented proof that stale cache cannot cross versions. | `failure-stale-kv-cache`, `validation-logprob-consistency`. |",
            "| logprob policy | Specify whether rollout returns `old_logprob`, trainer recomputes, or both; define mismatch threshold and replay evidence. | `capability-rollout-logprob-capture`, `failure-inconsistent-logprob`, `validation-logprob-consistency`. |",
            "| topology | Choose colocated, disaggregated, or PD disaggregation before backend promotion. | `pattern-colocated-train-rollout`, `pattern-disaggregated-train-rollout`, `pattern-pd-disaggregation`. |",
            "",
            "## Selection Matrix",
            "",
            "| criterion | SGLang evidence | vLLM evidence | design decision |",
            "|---|---|---|---|",
            "| RL lifecycle controls | Cite `backend-sglang` and `source-sglang-rollout-backend-refs`. | Cite `backend-vllm` and `source-vllm-rollout-backend-refs`. | Fill after target repo inspection. |",
            "| weight update and fallback | Cite SGLang refit, `flush_cache`, `weight_version` claims. | Cite vLLM RL weight-transfer, pause/resume, cache-control claims. | Fill with primary/fallback path. |",
            "| cache and logprob correctness | Cite `failure-stale-kv-cache`, `failure-inconsistent-logprob`. | Cite same validation/risk pages. | Promotion blocked without validation evidence. |",
            "| topology fit | Cite colocated/disaggregated/PD pattern pages. | Cite colocated/disaggregated/PD pattern pages. | Pick one topology first. |",
            "",
            "## Non-Claims",
            "",
            "- No local GPU, NCCL, multi-node, throughput, latency, or production readiness claim is made by this scaffold.",
            "- Source-reported backend capabilities remain source-reported until reproduced with local commands, logs, and artifacts.",
            "- A backend is not promoted unless the rendered plan cites page IDs, source IDs, validation/risk pages, and known gaps.",
        ])
    elif family == "weight-sync":
        sections.extend([
            "Primary path: target-aware weight sync from Megatron training to SGLang rollout using explicit `weight_version`, pause/drain, transfer, verify, `flush_cache`, and resume boundaries.",
            "",
            "Fallback path: full checkpoint reload remains available for partial update, delta baseline drift, distributed group failure, or uncertain cache state.",
            "",
            "Every implementation batch must cite the Wiki page IDs and source IDs in `context/context_sources.yaml`.",
        ])
    else:
        sections.append("Use the target framework pack as the anchor, then apply generic infrastructure contracts, cross-framework lessons, and validation/risk pages from the context bundle.")
    sections.extend([
        "",
        "## Alternatives considered",
        "",
        "- Primary framework path.",
        "- Reference framework fallback.",
        "",
        "## Dataflow",
        "",
    ])
    if family == "algorithm-data-contract":
        sections.append("prompt source -> rollout request -> inference backend -> token/logprob output -> reward/verifier -> trajectory/sample schema -> data buffer -> grouped trainer batch -> loss computation -> metrics/traces")
    elif family == "rollout-backend-selection":
        sections.append("target framework requirements -> context bundle -> SGLang/vLLM evidence matrix -> topology choice -> primary backend -> fallback backend -> weight update path -> cache/logprob/version contract -> validation evidence -> review gate")
    else:
        sections.append("prompt source -> rollout request -> inference backend -> tool/env interaction -> reward/verifier -> trajectory object -> data buffer -> trainer batch -> gradient update -> weight sync -> rollout version update -> metrics/traces")
    sections.extend([
        "",
        context_coverage_section(bundle).rstrip(),
        "",
    ])
    if family == "algorithm-data-contract":
        sections.extend([
            "## GRPO/RLVR Contract Checks",
            "",
            "- `old_logprob`: produced by rollout backend or recompute path and attached before trainer consumption.",
            "- `reference_logprob`: either produced, explicitly marked unavailable, or scheduled for reference-model recompute.",
            "- `group_id`: stable across all completions for a prompt and never mixes policy versions.",
            "- `policy_version`: attached to request, sample, reward rows, data-buffer records, trainer batch, and evidence.",
            "- reward/verifier output: records timeout/retry state and never silently defaults failed rewards.",
            "- failure modes: sample schema drift, inconsistent logprob, reward timeout, stale policy training, incomplete groups.",
            "- required Wiki/source IDs: `framework-slime`, `interface-algorithm-data-contract`, `capability-rollout-logprob-capture`, `capability-sample-grouping`, `capability-policy-versioning`, `failure-sample-schema-drift`, `validation-logprob-consistency`.",
        ])
    elif family == "rollout-backend-selection":
        sections.extend([
            "## Rollout Backend Contract Checks",
            "",
            "- `primary_backend`: chosen only after target framework pack, generic capability pages, cross-framework comparisons, and validation/risk pack are present.",
            "- `fallback_backend`: documented with a full fallback route and rollback trigger.",
            "- `primary_weight_update_path`: names the source-reported update mechanism and its fail-closed fallback.",
            "- `full_fallback`: uses immutable checkpoint reload or an equivalent full-state restore with matching `weight_version`.",
            "- `weight_version`: attached to rollout request, backend state, sample, trainer batch, logs, validation output, and artifact provenance.",
            "- cache policy: requires `flush_cache`, cache namespacing, or source-backed proof that stale cache cannot cross policy versions.",
            "- logprob policy: requires rollout `old_logprob` capture or recomputation, tolerance definition, and replay evidence.",
            "- failure modes: stale KV cache, inconsistent logprob, partial weight update, distributed rank mismatch, target-only retrieval, and unverified performance/production claim.",
            "- required Wiki/source IDs: `capability-rollout-backend-selection`, `comparisons-rollout-backends`, `backend-sglang`, `backend-vllm`, `pattern-colocated-train-rollout`, `pattern-disaggregated-train-rollout`, `pattern-pd-disaggregation`, `failure-stale-kv-cache`, `failure-inconsistent-logprob`, `validation-logprob-consistency`, `source-vllm-rollout-backend-refs`, `source-sglang-rollout-backend-refs`.",
        ])
    elif family == "weight-sync":
        sections.extend([
            "## P0 Sync Contract",
            "",
            "- primary sync path: distributed/tensor update when the target lifecycle and backend support it.",
            "- full fallback: immutable full checkpoint reload with the same `weight_version`.",
            "- `weight_version`: attached to update requests, rollout engine state, samples, trainer batches, logs, and evidence.",
            "- `flush_cache`: required unless the design proves cache namespacing or invalidation by version.",
            "- failure modes: partial update, stale KV cache, inconsistent logprob, rollout deadlock, distributed rank mismatch, delta baseline drift.",
            "- required Wiki/source IDs: `framework-slime`, `interface-weight-sync-adapter`, `capability-weight-sync-distributed`, `capability-weight-sync-disk`, `failure-partial-weight-update`, `validation-weight-version-monotonicity`, `source-slime-weight-sync-code`, `source-sglang-rl-weight-update-refs`.",
        ])
    sections.extend([
        "",
        "## APIs and interfaces",
        "",
        "Document trainer, rollout, reward, environment, and evidence interfaces.",
        "",
        "## State and storage",
        "",
        "Track task config, policy version, weight version when applicable, evidence path, and review issue state.",
        "",
        "## Failure modes",
        "",
        "Version mismatch, schema drift, delayed reward, nondeterminism, and rollback gap.",
        "",
        "## Observability",
        "",
        "Metrics, traces, logs, and validation evidence are required before review.",
        "",
        "## Implementation steps",
        "",
        "### Step 1",
        "",
        "- Files: docs/*",
        "- Changes: finalize design and validation matrix",
        "- Tests: run validation commands",
        "- Acceptance: criteria mapped to evidence",
        "",
        "## Validation commands",
        "",
        *[f"- `{cmd}`" for cmd in contract.get("validation_commands", [])],
        "",
        "## Rollback plan",
        "",
        "Revert candidate changes, restore prior plan lock, and mark unresolved review issues open.",
        "",
        "## Promotion criteria",
        "",
        *[f"- {item}" for item in contract.get("promotion_criteria", [])],
        "",
        "## Review checklist",
        "",
        "- Goal alignment",
        "- Source provenance",
        "- Validation evidence",
        "- Failure modes and rollback",
        "- Open review issues and waivers",
    ])
    return "\n".join(sections) + "\n"


def render_architecture(contract: dict, bundle: dict) -> str:
    family = task_family(contract)
    if family == "rollout-backend-selection":
        return """# Architecture

## Target

Design a target-aware rollout backend selection for RLVR/GRPO. The architecture is source-traceable design output, not a verified runtime benchmark or production claim.

## Flow

target framework requirements -> RLInfraWiki context bundle -> SGLang/vLLM evidence matrix -> topology decision -> primary backend -> fallback backend -> weight update path -> cache/logprob/version contract -> validation evidence -> review gate.

## Required boundaries

- Target framework owns trainer/rollout integration points and must be inspected before implementation changes.
- Rollout backend owns generation, backend provenance, cache lifecycle, and any source-reported logprob output.
- Weight update adapter owns primary update path, full fallback, monotonic `weight_version`, `flush_cache` or cache namespacing, and fail-closed behavior.
- Validation layer owns logprob replay checks, train/infer schema matching, stale-policy bounds, and artifact provenance.

## Evidence map

| area | page IDs | source IDs |
|---|---|---|
| backend selection | `capability-rollout-backend-selection`, `comparisons-rollout-backends` | `source-vllm-rollout-backend-refs`, `source-sglang-rollout-backend-refs` |
| backend profiles | `backend-sglang`, `backend-vllm` | `source-sglang-rollout-backend-refs`, `source-vllm-rollout-backend-refs` |
| topology | `pattern-colocated-train-rollout`, `pattern-disaggregated-train-rollout`, `pattern-pd-disaggregation` | `source-vllm-rollout-backend-refs`, `source-sglang-rollout-backend-refs` |
| correctness risks | `failure-stale-kv-cache`, `failure-inconsistent-logprob`, `validation-logprob-consistency` | `source-vllm-rollout-backend-refs`, `source-sglang-rollout-backend-refs` |

## Open gaps

- Source-reported framework behavior has not been locally reproduced with GPU/NCCL/multi-node execution.
- Throughput, latency, and production readiness are not verified by this scaffold.
- Target repository symbols should be inspected before implementation changes.
"""
    if family != "algorithm-data-contract":
        return "# Architecture\n\nPending RLCR iteration.\n"
    return """# Architecture

## Target

Design a slime-compatible GRPO/RLVR data contract. This is a source-traceable design and implementation plan, not a verified runtime implementation.

## Flow

slime trainer config -> rollout request -> rollout backend token/logprob output -> reward/verifier result -> data-buffer record -> grouped trainer batch -> loss inputs -> validation evidence.

## Required boundaries

- Rollout backend owns token generation, behavior logprob capture, stop reason, and backend provenance.
- Reward/verifier owns scalar reward, verifier labels, timeout/retry state, and reward service version.
- Data buffer owns schema validation, group completeness, policy-version checks, and trainer-batch materialization.
- Trainer owns advantage computation, loss masks, stale-policy decision, and update evidence.

## Open gaps

- Source-reported framework behavior has not been locally reproduced with GPU/NCCL/multi-node execution.
- Slime source symbols should be inspected before implementation changes.
"""


def render_interfaces(contract: dict) -> str:
    family = task_family(contract)
    if family == "rollout-backend-selection":
        return """# Interfaces

## RolloutBackendSelection fields

| field | owner | required | notes |
|---|---|---:|---|
| `target_framework` | task owner | yes | Anchor for target-aware design; do not let this become target-only. |
| `primary_backend` | architect | yes | `sglang` or `vllm`, with page IDs and source IDs. |
| `fallback_backend` | architect | yes | The non-primary backend or a documented blocked fallback. |
| `primary_weight_update_path` | weight update adapter | yes | Source-reported path plus fail-closed behavior. |
| `full_fallback` | weight update adapter | yes | Full checkpoint reload or equivalent full-state restore. |
| `weight_version` | trainer/orchestrator | yes | Monotonic identity on requests, samples, backend state, logs, and evidence. |
| `cache_policy` | rollout backend adapter | yes | `flush_cache`, version namespace, or source-backed proof. |
| `logprob_policy` | rollout/trainer adapter | yes | Capture or recompute `old_logprob`; define mismatch threshold. |
| `topology` | architect | yes | colocated, disaggregated, or PD disaggregation. |
| `source_ids` | evidence layer | yes | Include backend and validation/risk source IDs. |

## Adapter contracts

- `interface-rollout-backend-adapter`
- `interface-weight-sync-adapter`
- `capability-rollout-backend-selection`
- `validation-logprob-consistency`
"""
    if family != "algorithm-data-contract":
        return "# Interfaces\n\nPending RLCR iteration.\n"
    return """# Interfaces

## AlgorithmDataContract sample fields

| field | owner | required for GRPO/RLVR | notes |
|---|---|---:|---|
| `sample_id` | rollout/data buffer | yes | Stable evidence key for replay and debugging. |
| `prompt_tokens` / `response_tokens` | rollout backend | yes | Must preserve alignment with masks and logprobs. |
| `action_mask` / `loss_mask` | rollout/backend or trainer adapter | yes | Prevents prompt tokens from entering completion loss. |
| `old_logprob` | rollout backend or recompute path | yes | Behavior-policy logprob consumed by trainer loss. |
| `reference_logprob` | reference model or recompute path | task-dependent | Required when KL/reference-policy control is enabled. |
| `reward` / verifier labels | reward service | yes | Include timeout/retry/provenance state. |
| `group_id` | sampler/data buffer | yes for GRPO | Group completeness and same-policy invariants are mandatory. |
| `policy_version` | trainer/orchestrator | yes | Used to bound stale-policy samples. |

## Adapter contracts

- `interface-algorithm-data-contract`
- `interface-data-buffer-adapter`
- `interface-rollout-backend-adapter`
- `interface-reward-service-adapter`
"""


def render_risk_register(contract: dict) -> str:
    family = task_family(contract)
    if family == "rollout-backend-selection":
        return """# Risk Register

| risk | severity | mitigation | status |
|---|---|---|---|
| target-only backend choice | P1 | Require Target, Generic, Cross-Framework, and Validation & Risk packs before promotion. | open |
| stale KV/prefix cache | P1 | Require `flush_cache`, versioned cache namespace, or source-backed proof that cache cannot cross `weight_version`. | open |
| inconsistent logprob | P1 | Run `validation-logprob-consistency` replay/recompute checks before promoting backend selection. | open |
| partial weight update | P1 | Define primary update path, full fallback, monotonic `weight_version`, and fail-closed rollback. | open |
| topology mismatch | P1 | Pick colocated, disaggregated, or PD topology before backend promotion. | open |
| source-reported treated as verified | P1 | Keep GPU/NCCL/multi-node/performance/production claims out unless local logs/artifacts exist. | open |
| provenance gap | P1 | Cite Wiki page IDs, source IDs, claim IDs, known gaps, and context sidecars. | open |
"""
    if family != "algorithm-data-contract":
        return "# Risk Register\n\n| risk | severity | mitigation | status |\n|---|---|---|---|\n| version mismatch | P1 | add weight_version_id validation | open |\n| provenance gap | P1 | cite RLInfraWiki source IDs | open |\n"
    return """# Risk Register

| risk | severity | mitigation | status |
|---|---|---|---|
| sample schema drift | P1 | Validate every data-buffer record against `interface-algorithm-data-contract`. | open |
| inconsistent logprob | P1 | Add `validation-logprob-consistency` checks and replay evidence. | open |
| incomplete GRPO group | P1 | Enforce `validation-grouped-rollout-invariants` before trainer consumption. | open |
| reward timeout | P1 | Record timeout/retry state and fail closed on missing verifier output. | open |
| stale policy training | P1 | Bound accepted policy lag with `validation-stale-policy-bound`. | open |
| unverified runtime claim | P1 | Keep claims `source-reported` or `inferred` unless local logs/artifacts prove them. | open |
"""


def render_bundle(contract_path: Path, output: Path, preserve_ledgers: bool = False, preserve_human_docs: bool = False) -> None:
    contract = read_task_contract(contract_path)
    validate_contract_schema(contract, contract_path)
    ensure_workspace_dirs(output)
    bundle = compose_bundle(
        task=contract.get("objective", ""),
        target_framework=first_target_framework(contract),
        mode="design",
        max_pages=16,
    )
    write_context_sidecars(bundle, output / "context")
    if preserve_ledgers:
        validate_metrics_header(output / "metrics.csv")
    shutil.copyfile(contract_path, output / "task_contract.yaml")
    doc_writer = write_if_missing if preserve_human_docs else write
    doc_writer(output / "docs" / "goal.md", render_goal(contract))
    doc_writer(output / "docs" / "draft.md", render_draft(contract, bundle))
    doc_writer(output / "docs" / "plan.md", render_plan(contract, bundle))
    doc_writer(output / "docs" / "architecture.md", render_architecture(contract, bundle))
    doc_writer(output / "docs" / "interfaces.md", render_interfaces(contract))
    for name, title in [("review.md", "Review"), ("codex_tasks.md", "Codex Tasks")]:
        doc_writer(output / "docs" / name, f"# {title}\n\nPending RLCR iteration.\n")
    doc_writer(output / "docs" / "validation_matrix.md", "# Validation Matrix\n\n| requirement | validation command | expected result | evidence path | status |\n|---|---|---|---|---|\n" + "".join(f"| contract validation | `{cmd}` | exits 0 | evidence/{i:02d}-validation.log | pending |\n" for i, cmd in enumerate(contract.get("validation_commands", []), 1)))
    doc_writer(output / "docs" / "risk_register.md", render_risk_register(contract))
    doc_writer(output / "docs" / "goal_status.md", f"# Goal Status\n\n- status: active\n- updated_at: {now_iso()}\n")
    write(output / ".humanize" / "rlcr_config.yaml", f"""mode: {contract.get('review_mode', 'humanize-compatible-rlcr')}
builder: {contract.get('builder', 'claude')}
reviewer: {contract.get('reviewer', 'codex')}
human_architect_required_for:
  - goal_amendment
  - P1_waiver
  - promotion_with_unresolved_P2
plan_lock:
  enabled: true
  file: .humanize/plan.lock.md
review:
  blocker_severities: [P0, P1]
  waiver_allowed_for: [P2]
  backlog_allowed_for: [P3]
validation:
  require_before_review: true
  require_after_fix: true
""")
    if not preserve_ledgers:
        write(output / ".humanize" / "loop_state.json", json.dumps({"status": "initialized", "round": 0, "updated_at": now_iso()}, indent=2) + "\n")
    else:
        write_if_missing(output / ".humanize" / "loop_state.json", json.dumps({"status": "initialized", "round": 0, "updated_at": now_iso()}, indent=2) + "\n")
    for rel in LEDGER_FILES:
        target = output / rel
        if preserve_ledgers:
            write_if_missing(target, "")
        else:
            write(target, "")
    rendered_at = now_iso()
    contract_hash = sha256_file(contract_path)
    goal_version = {"goal_id": contract.get("task_name"), "status": "active", "contract_hash": contract_hash, "created_at": rendered_at}
    goal_versions_path = output / "goal_versions.jsonl"
    prior_contract_hash = last_contract_hash(goal_versions_path) if goal_versions_path.exists() else None
    contract_changed = prior_contract_hash is not None and prior_contract_hash != contract_hash
    if preserve_human_docs and contract_changed:
        print(
            "WARN: contract changed; scaffolded docs under docs/ were preserved and may be stale. "
            "Re-run with --overwrite-human-docs to regenerate them, or hand-edit validation_matrix.md "
            "and plan.md to reflect the new contract.",
            file=sys.stderr,
        )
    goal_history_exists = goal_versions_path.exists() and bool(load_jsonl(goal_versions_path))
    if preserve_ledgers and contract_changed:
        append_jsonl(goal_versions_path, [goal_version])
    elif preserve_ledgers and goal_history_exists and prior_contract_hash is None:
        append_jsonl(goal_versions_path, [goal_version])
    elif not preserve_ledgers or not goal_versions_path.exists() or prior_contract_hash is None:
        write(goal_versions_path, json.dumps(goal_version) + "\n")
    progress_path = output / "progress_log.md"
    progress_entry = f"- {rendered_at}: workspace rendered from `{contract_path.name}`.\n"
    amended_progress_entry = f"- {rendered_at}: contract amended -> workspace re-rendered from `{contract_path.name}`.\n"
    if preserve_ledgers and progress_path.exists() and contract_changed:
        append_text(progress_path, amended_progress_entry)
    elif preserve_ledgers and progress_path.exists() and prior_contract_hash is None:
        append_text(progress_path, progress_entry)
    elif preserve_ledgers and progress_path.exists():
        pass
    elif preserve_ledgers and not progress_path.exists():
        write(progress_path, f"# Progress Log\n\n{progress_entry}")
    else:
        write(progress_path, f"# Progress Log\n\n{progress_entry}")
    metrics_path = output / "metrics.csv"
    if preserve_ledgers:
        if not metrics_path.exists() or not metrics_path.read_text(encoding="utf-8"):
            write(metrics_path, METRICS_HEADER)
    else:
        write(metrics_path, METRICS_HEADER)
    write(output / "review_rounds" / "README.md", "# Review Rounds\n\nEach round stores review_packet.md, codex_review.md, parsed_issues.jsonl, claude_response.md, and validation_after_fix.md.\n")
    write(output / "evidence" / "README.md", "# Evidence\n\nStore validation logs, command output, screenshots, traces, and local reproduction evidence here.\n")
    write(output / "runs" / "README.md", "# Runs\n\nTask-specific runs live here when the external workspace permits it.\n")
    write(output / "profile" / "README.md", "# Profile\n\nProfiling notes and summaries live here; large logs should stay outside this repository.\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a complete RL infra task workspace")
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--force", action="store_true", help="Allow refreshing scaffold files in an existing non-empty workspace")
    parser.add_argument("--reset-ledgers", action="store_true", help="With --force, also reset review ledgers, loop state, metrics, and progress logs")
    parser.add_argument("--overwrite-human-docs", action="store_true", help="With --force, also overwrite scaffolded docs under docs/")
    args = parser.parse_args()
    output = Path(args.output)
    existing_nonempty = output.exists() and any(output.iterdir())
    if args.reset_ledgers and not args.force:
        print("ERROR: --reset-ledgers requires --force")
        return 1
    if args.overwrite_human_docs and not args.force:
        print("ERROR: --overwrite-human-docs requires --force")
        return 1
    if existing_nonempty and not args.force:
        print(f"ERROR: refusing to render into non-empty workspace: {output}")
        print("Pass --force to refresh scaffold-managed files. Ledgers and human-edited docs are preserved unless explicit reset flags are used. Planned writes:")
        for rel in PLANNED_FILES:
            print(f"  - {rel}")
        return 1
    output.mkdir(parents=True, exist_ok=True)
    render_bundle(
        Path(args.contract),
        output,
        preserve_ledgers=existing_nonempty and not args.reset_ledgers,
        preserve_human_docs=existing_nonempty and not args.overwrite_human_docs,
    )
    print(f"rendered task workspace at {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
