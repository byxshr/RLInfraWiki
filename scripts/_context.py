from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from _rlinfra import SKILL_ROOT, find_page, iter_wiki_pages, load_source_manifests, split_frontmatter

PACK_KEYS = [
    "target_framework_pack",
    "generic_infra_pack",
    "cross_framework_pack",
    "validation_risk_pack",
]

PACK_TITLES = {
    "target_framework_pack": "Target Framework Pack",
    "generic_infra_pack": "Generic Infra Pack",
    "cross_framework_pack": "Cross-Framework Pack",
    "validation_risk_pack": "Validation & Risk Pack",
}

DEFAULT_GENERIC_IDS = [
    "interface-rollout-backend-adapter",
    "interface-weight-sync-adapter",
    "capability-weight-sync-distributed",
    "capability-policy-versioning",
    "capability-sample-grouping",
    "algorithm-grpo",
]

DEFAULT_CROSS_IDS = [
    "framework-slime",
    "framework-roll",
    "framework-areal",
    "framework-verl",
    "comparison-weight-sync-options",
    "comparison-cross-framework-lessons",
    "pattern-megatron-sglang",
    "comparisons-rollout-backends",
]

DEFAULT_VALIDATION_IDS = [
    "failure-partial-weight-update",
    "failure-stale-kv-cache",
    "failure-inconsistent-logprob",
    "validation-weight-version-monotonicity",
    "validation-pause-update-resume",
    "validation-train-infer-schema-match",
    "validation-grouped-rollout-invariants",
]

ROLLOUT_BACKEND_SELECTION_GENERIC_IDS = [
    "capability-rollout-backend-selection",
    "interface-rollout-backend-adapter",
    "interface-weight-sync-adapter",
    "capability-rollout-logprob-capture",
    "capability-policy-versioning",
    "algorithm-rlvr",
    "algorithm-grpo",
    "backend-sglang",
    "backend-vllm",
]

ROLLOUT_BACKEND_SELECTION_CROSS_IDS = [
    "framework-slime",
    "framework-roll",
    "framework-areal",
    "framework-verl",
    "comparisons-rollout-backends",
    "pattern-colocated-train-rollout",
    "pattern-disaggregated-train-rollout",
    "pattern-pd-disaggregation",
    "comparison-cross-framework-lessons",
]

ROLLOUT_BACKEND_SELECTION_VALIDATION_IDS = [
    "failure-stale-kv-cache",
    "failure-inconsistent-logprob",
    "failure-partial-weight-update",
    "failure-distributed-rank-mismatch",
    "validation-logprob-consistency",
    "validation-train-infer-schema-match",
    "validation-weight-version-monotonicity",
    "validation-pause-update-resume",
    "validation-stale-policy-bound",
]

ALGORITHM_DATA_CONTRACT_GENERIC_IDS = [
    "algorithm-grpo",
    "algorithm-rlvr",
    "interface-algorithm-data-contract",
    "interface-data-buffer-adapter",
    "interface-rollout-backend-adapter",
    "interface-reward-service-adapter",
    "capability-rollout-logprob-capture",
    "capability-sample-grouping",
    "capability-policy-versioning",
    "capability-reward-verifier",
    "capability-data-buffer-trajectory",
]

ALGORITHM_DATA_CONTRACT_VALIDATION_IDS = [
    "failure-sample-schema-drift",
    "failure-inconsistent-logprob",
    "failure-reward-timeout",
    "failure-stale-policy-training",
    "validation-logprob-consistency",
    "validation-grouped-rollout-invariants",
    "validation-train-infer-schema-match",
    "validation-stale-policy-bound",
    "validation-reward-timeout-retry",
]

TRAINING_ROLLOUT_MISMATCH_GENERIC_IDS = [
    "recipe-debug-training-rollout-mismatch",
    "observability-training-inference-mismatch",
    "observability-debug-playbook",
    "interface-algorithm-data-contract",
    "interface-rollout-backend-adapter",
    "capability-rollout-logprob-capture",
    "capability-policy-versioning",
    "capability-sample-grouping",
    "algorithm-grpo",
]

TRAINING_ROLLOUT_MISMATCH_CROSS_IDS = [
    "framework-slime",
    "framework-verl",
    "framework-roll",
    "framework-areal",
    "comparisons-rollout-backends",
    "pattern-colocated-train-rollout",
    "pattern-disaggregated-train-rollout",
    "comparison-cross-framework-lessons",
]

TRAINING_ROLLOUT_MISMATCH_VALIDATION_IDS = [
    "validation-logprob-consistency",
    "validation-train-infer-schema-match",
    "validation-weight-version-monotonicity",
    "validation-stale-policy-bound",
    "failure-inconsistent-logprob",
    "failure-stale-kv-cache",
    "failure-sample-schema-drift",
    "failure-stale-policy-training",
]

ASYNC_AGENTIC_RAY_GENERIC_IDS = [
    "recipe-design-agentic-rl-pipeline",
    "algorithm-agentic-rl",
    "agentic-tool-calling",
    "agentic-multi-turn-env",
    "agentic-openai-compatible-agent-app",
    "pattern-async-rollout",
    "interface-environment-adapter",
    "interface-orchestrator-adapter",
    "interface-reward-service-adapter",
    "interface-data-buffer-adapter",
    "capability-rollout-agentic-multiturn",
    "capability-rollout-server-async",
    "capability-policy-versioning",
    "capability-reward-verifier",
]

ASYNC_AGENTIC_RAY_CROSS_IDS = [
    "framework-slime",
    "framework-roll",
    "framework-verl",
    "framework-areal",
    "system-roll",
    "system-areal",
    "pattern-ray-multirole",
    "comparisons-orchestration-options",
    "comparison-cross-framework-lessons",
    "comparisons-rollout-backends",
    "pattern-colocated-train-rollout",
    "pattern-disaggregated-train-rollout",
]

ASYNC_AGENTIC_RAY_VALIDATION_IDS = [
    "failure-reward-timeout",
    "failure-tool-hang",
    "failure-stale-policy-training",
    "failure-stale-kv-cache",
    "failure-sample-schema-drift",
    "failure-inconsistent-logprob",
    "validation-stale-policy-bound",
    "validation-reward-timeout-retry",
    "validation-train-infer-schema-match",
    "validation-logprob-consistency",
    "validation-grouped-rollout-invariants",
]


def normalized_task_text(task: str) -> str:
    return task.lower().replace("_", " ").replace("-", " ")


def is_algorithm_data_contract_task(task: str) -> bool:
    text = normalized_task_text(task)
    has_algorithm = any(term in text for term in ["grpo", "rlvr", "ppo", "dapo", "algorithm"])
    has_contract = any(term in text for term in ["data contract", "algorithm data", "sample schema", "logprob"])
    return has_algorithm and has_contract


def is_rollout_backend_selection_task(task: str) -> bool:
    text = normalized_task_text(task)
    mentions_rollout_backend = "rollout backend" in text or ("rollout" in text and "backend" in text)
    mentions_backend_pair = "sglang" in text and "vllm" in text
    selection_words = ["select", "selection", "choose", "compare", "between", "matrix", "tradeoff", "trade-off"]
    risk_words = ["cache", "logprob", "weight update", "weight sync", "pd", "colocated", "disaggregated"]
    return (mentions_rollout_backend or mentions_backend_pair) and (
        any(word in text for word in selection_words) or any(word in text for word in risk_words)
    )


def is_training_rollout_mismatch_debug_task(task: str, mode: str = "design") -> bool:
    text = normalized_task_text(task)
    mentions_boundary = ("training" in text or "trainer" in text) and ("rollout" in text or "inference" in text)
    mentions_debug = any(term in text for term in ["debug", "mismatch", "drift", "replay", "recompute"])
    mentions_signal = any(
        term in text
        for term in [
            "logprob",
            "old logprob",
            "policy version",
            "weight version",
            "cache",
            "kv",
            "schema",
            "token",
            "mask",
            "stale policy",
        ]
    )
    return (mode == "debug" and mentions_boundary and mentions_signal) or (
        mentions_boundary and mentions_debug and mentions_signal
    )


def is_async_agentic_ray_task(task: str, mode: str = "design") -> bool:
    text = normalized_task_text(task)
    mentions_agentic = any(term in text for term in ["agentic", "agent", "tool calling", "multi turn", "multiturn"])
    mentions_async = any(term in text for term in ["async", "asynchronous", "stale policy", "long tail"])
    mentions_orchestration = any(term in text for term in ["ray", "orchestration", "orchestrator", "scheduler", "multi role", "multirole"])
    mentions_rollout_context = any(term in text for term in ["rollout", "generation", "pipeline", "reward", "environment", "tool"])
    return mode in {"design", "adapter", "explain"} and mentions_agentic and mentions_async and mentions_orchestration and mentions_rollout_context


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def page_index() -> dict[str, dict[str, Any]]:
    return {str(page.get("id")): page for page in iter_wiki_pages()}


def page_type(page: dict[str, Any]) -> str:
    return str(page.get("page_type") or page.get("type") or "")


def framework_id(name: str | None) -> str | None:
    if not name:
        return None
    normalized = name.lower().replace("_", "-")
    aliases = {
        "roll": "roll",
        "roll-framework": "roll",
        "areal": "areal",
        "real": "areal",
        "verl": "verl",
        "ve-rl": "verl",
        "slime": "slime",
    }
    return aliases.get(normalized, normalized)


def make_entry(page: dict[str, Any], why: str) -> dict[str, Any]:
    return {
        "page_id": str(page.get("id")),
        "title": str(page.get("title", "")),
        "path": str(page.get("_path", "")),
        "page_type": page_type(page),
        "why_included": why,
        "source_ids": [str(sid) for sid in page.get("sources", [])],
        "confidence": str(page.get("confidence", "inferred")),
        "summary": str(page.get("summary", "")),
    }


def add_existing(pages: dict[str, dict[str, Any]], ids: list[str], why: str) -> list[dict[str, Any]]:
    out = []
    seen = set()
    for pid in ids:
        page = pages.get(pid)
        if not page or pid in seen:
            continue
        seen.add(pid)
        out.append(make_entry(page, why))
    return out


def infer_facets(task: str) -> dict[str, list[str]]:
    text = task.lower()
    facets = {"components": [], "algorithms": [], "backends": [], "deployment_modes": []}
    for component in ["rollout", "weight-sync", "training", "data-buffer", "reward", "scheduler", "environment", "observability"]:
        if component.replace("-", " ") in text or component in text:
            facets["components"].append(component)
    for algorithm in ["grpo", "ppo", "rlvr", "agentic-rl", "dapo", "gspo", "rloo"]:
        if algorithm in text:
            facets["algorithms"].append(algorithm)
    for backend in ["sglang", "vllm", "megatron", "fsdp", "ray"]:
        if backend in text:
            facets["backends"].append(backend)
    for mode in ["async", "disaggregated", "colocated"]:
        if mode in text:
            facets["deployment_modes"].append(mode)
    if "rollout" not in facets["components"]:
        facets["components"].append("rollout")
    if "weight" in text and "weight-sync" not in facets["components"]:
        facets["components"].append("weight-sync")
    if not facets["algorithms"]:
        facets["algorithms"].append("grpo")
    return facets


def compose_bundle(
    task: str,
    target_framework: str | None = None,
    mode: str = "design",
    max_pages: int = 16,
    repo_root: str | None = None,
) -> dict[str, Any]:
    pages = page_index()
    target = framework_id(target_framework)
    target_pid = f"framework-{target}" if target else None
    target_known = bool(target_pid and target_pid in pages)

    target_ids: list[str] = []
    if target_known and target_pid:
        target_ids.append(target_pid)
        legacy_pid = f"system-{target}"
        if legacy_pid in pages:
            target_ids.append(legacy_pid)
    elif target:
        target_ids.append("adapter-adapt-new-framework")

    if is_training_rollout_mismatch_debug_task(task, mode):
        generic_ids = list(TRAINING_ROLLOUT_MISMATCH_GENERIC_IDS)
        validation_ids = list(TRAINING_ROLLOUT_MISMATCH_VALIDATION_IDS)
        base_cross_ids = list(TRAINING_ROLLOUT_MISMATCH_CROSS_IDS)
    elif is_rollout_backend_selection_task(task):
        generic_ids = list(ROLLOUT_BACKEND_SELECTION_GENERIC_IDS)
        validation_ids = list(ROLLOUT_BACKEND_SELECTION_VALIDATION_IDS)
        base_cross_ids = list(ROLLOUT_BACKEND_SELECTION_CROSS_IDS)
    elif is_algorithm_data_contract_task(task):
        generic_ids = list(ALGORITHM_DATA_CONTRACT_GENERIC_IDS)
        validation_ids = list(ALGORITHM_DATA_CONTRACT_VALIDATION_IDS)
        base_cross_ids = list(DEFAULT_CROSS_IDS)
    elif is_async_agentic_ray_task(task, mode):
        generic_ids = list(ASYNC_AGENTIC_RAY_GENERIC_IDS)
        validation_ids = list(ASYNC_AGENTIC_RAY_VALIDATION_IDS)
        base_cross_ids = list(ASYNC_AGENTIC_RAY_CROSS_IDS)
    else:
        generic_ids = list(DEFAULT_GENERIC_IDS)
        validation_ids = list(DEFAULT_VALIDATION_IDS)
        base_cross_ids = list(DEFAULT_CROSS_IDS)
    if "sglang" in task.lower() and "adapter-add-sglang-rollout-backend" in pages:
        generic_ids.append("adapter-add-sglang-rollout-backend")
    if "vllm" in task.lower() and "adapter-add-vllm-rollout-backend" in pages:
        generic_ids.append("adapter-add-vllm-rollout-backend")

    cross_ids = []
    for pid in base_cross_ids:
        if target and pid == f"framework-{target}":
            continue
        cross_ids.append(pid)

    bundle = {
        "id": f"context-{target or 'unknown'}-{now_stamp()}",
        "mode": mode,
        "user_task": task,
        "target_framework": target,
        "target_framework_known": target_known,
        "repo_root": repo_root,
        "retrieval_policy": "target-aware-balanced" if target_known else "generic-first-balanced",
        "problem_facets": infer_facets(task),
        "packs": {
            "target_framework_pack": add_existing(
                pages,
                target_ids,
                "Target framework entry point; target-aware anchor, not the full context.",
            ),
            "generic_infra_pack": add_existing(
                pages,
                generic_ids,
                "Generic RL infrastructure contract relevant to the task.",
            ),
            "cross_framework_pack": add_existing(
                pages,
                cross_ids,
                "Cross-framework analog or comparison to avoid target-only design.",
            ),
            "validation_risk_pack": add_existing(
                pages,
                validation_ids,
                "Failure or validation page required by the review gate.",
            ),
        },
        "known_gaps": [
            "Source-reported framework behavior has not been locally reproduced with GPU/NCCL/multi-node execution.",
            "Target repository symbols should be inspected before implementation changes.",
        ],
        "rejected_pages": [
            {
                "id": "framework-openrlhf",
                "reason": "Not included in the current source-backed corpus for this P0 context.",
            }
        ],
    }
    # max_pages is a soft retrieval hint. The four-pack coverage rule is more
    # important than a global cap, so composition keeps required packs intact.
    return bundle


def bundle_source_summary(bundle: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "target_framework_pages": [],
        "generic_pages": [],
        "cross_framework_pages": [],
        "validation_risk_pages": [],
        "sources": {},
        "rejected_pages": bundle.get("rejected_pages", []),
        "known_gaps": bundle.get("known_gaps", []),
    }
    key_map = {
        "target_framework_pack": "target_framework_pages",
        "generic_infra_pack": "generic_pages",
        "cross_framework_pack": "cross_framework_pages",
        "validation_risk_pack": "validation_risk_pages",
    }
    for pack_key, out_key in key_map.items():
        for page in bundle.get("packs", {}).get(pack_key, []):
            summary[out_key].append(page["page_id"])
            summary["sources"][page["page_id"]] = page.get("source_ids", [])
    return summary


def render_markdown(bundle: dict[str, Any]) -> str:
    lines = ["# RLInfraWiki Context Bundle", ""]
    lines.append(f"- id: `{bundle.get('id')}`")
    lines.append(f"- mode: `{bundle.get('mode')}`")
    lines.append(f"- target_framework: `{bundle.get('target_framework')}`")
    lines.append(f"- retrieval_policy: `{bundle.get('retrieval_policy')}`")
    lines.append("")
    for idx, key in enumerate(PACK_KEYS, 1):
        lines.append(f"## {idx}. {PACK_TITLES[key]}")
        lines.append("")
        lines.append("| page_id | path | why included | source_ids | confidence |")
        lines.append("|---|---|---|---|---|")
        for page in bundle.get("packs", {}).get(key, []):
            lines.append(
                "| `{}` | `{}` | {} | {} | `{}` |".format(
                    page["page_id"],
                    page["path"],
                    page["why_included"],
                    ", ".join(f"`{sid}`" for sid in page.get("source_ids", [])),
                    page.get("confidence", ""),
                )
            )
        lines.append("")
    lines.append("## Known Gaps")
    lines.append("")
    for gap in bundle.get("known_gaps", []):
        lines.append(f"- {gap}")
    lines.append("")
    lines.append("## Rejected Pages")
    lines.append("")
    for page in bundle.get("rejected_pages", []):
        lines.append(f"- `{page.get('id')}`: {page.get('reason')}")
    lines.append("")
    lines.append("## Required Citations for Design Output")
    lines.append("")
    lines.append("Cite page IDs, paths, source IDs, confidence, version-sensitive notes, known gaps, and validation/risk pages.")
    lines.append("")
    lines.append("## Recommended Next Queries")
    lines.append("")
    backends = set(bundle.get("problem_facets", {}).get("backends", []))
    deployment_modes = set(bundle.get("problem_facets", {}).get("deployment_modes", []))
    components = set(bundle.get("problem_facets", {}).get("components", []))
    if "async" in deployment_modes and ("ray" in backends or "scheduler" in components):
        lines.append("- `python scripts/get_page.py pattern-async-rollout --follow-sources`")
        lines.append("- `python scripts/get_page.py pattern-ray-multirole --follow-sources`")
        lines.append("- `python scripts/get_page.py comparisons-orchestration-options --follow-sources`")
    elif {"sglang", "vllm"} <= backends:
        lines.append("- `python scripts/get_page.py capability-rollout-backend-selection --follow-sources`")
        lines.append("- `python scripts/get_page.py comparisons-rollout-backends --follow-sources`")
        lines.append("- `python scripts/get_page.py validation-logprob-consistency --follow-sources`")
    else:
        lines.append("- `python scripts/get_page.py interface-weight-sync-adapter --follow-sources`")
        lines.append("- `python scripts/get_page.py algorithm-grpo --follow-sources`")
        lines.append("- `python scripts/suggest_cross_framework.py --capability weight-sync-distributed --exclude {}`".format(bundle.get("target_framework") or "none"))
    lines.append("")
    lines.append("<!-- RLINFRA_CONTEXT_BUNDLE_JSON")
    lines.append(json.dumps(bundle, indent=2, sort_keys=False))
    lines.append("-->")
    return "\n".join(lines) + "\n"


def write_bundle(bundle: dict[str, Any], output: Path, output_format: str = "auto") -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fmt = output_format
    if fmt == "auto":
        fmt = "json" if output.suffix == ".json" else "yaml" if output.suffix in {".yaml", ".yml"} else "markdown"
    if fmt == "json":
        output.write_text(json.dumps(bundle, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    elif fmt == "yaml":
        output.write_text(yaml.safe_dump(bundle, sort_keys=False, allow_unicode=False), encoding="utf-8")
    else:
        output.write_text(render_markdown(bundle), encoding="utf-8")


def write_context_sidecars(bundle: dict[str, Any], context_dir: Path) -> None:
    context_dir.mkdir(parents=True, exist_ok=True)
    write_bundle(bundle, context_dir / "context_bundle.md", "markdown")
    write_bundle(bundle, context_dir / "context_bundle.json", "json")
    (context_dir / "context_sources.yaml").write_text(
        yaml.safe_dump(bundle_source_summary(bundle), sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def load_bundle(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    if path.suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(text)
        if isinstance(data, dict):
            return data
    match = re.search(r"<!-- RLINFRA_CONTEXT_BUNDLE_JSON\s*(.*?)\s*-->", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    raise SystemExit(f"could not parse context bundle: {path}")


def page_frontmatter(page_id: str) -> dict[str, Any] | None:
    path = find_page(page_id)
    if not path:
        return None
    fm, _ = split_frontmatter(path)
    if not fm:
        return None
    if "page_type" not in fm and "type" in fm:
        fm["page_type"] = fm["type"]
    if "_path" not in fm:
        fm["_path"] = path.relative_to(SKILL_ROOT).as_posix()
    return fm


def validate_bundle(bundle: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    sources = load_source_manifests()
    packs = bundle.get("packs")
    if not isinstance(packs, dict):
        return ["context bundle missing packs"]
    for key in PACK_KEYS:
        pages = packs.get(key)
        if not isinstance(pages, list) or not pages:
            errors.append(f"missing or empty {key}")
    target = bundle.get("target_framework")
    target_known = bool(bundle.get("target_framework_known"))
    if target_known:
        target_pages = {page.get("page_id") for page in packs.get("target_framework_pack", [])}
        if f"framework-{target}" not in target_pages:
            errors.append("target framework pack does not contain target framework profile")
    all_pages = [page for key in PACK_KEYS for page in packs.get(key, [])]
    if all(page.get("page_id", "").startswith(f"framework-{target}") for page in all_pages) and target:
        errors.append("target-only context is not allowed")
    seen_types: set[str] = set()
    seen_frameworks: set[str] = set()
    for entry in all_pages:
        pid = str(entry.get("page_id", ""))
        fm = page_frontmatter(pid)
        if not fm:
            errors.append(f"page id does not resolve: {pid}")
            continue
        seen_types.add(str(fm.get("page_type") or fm.get("type")))
        for framework in fm.get("frameworks", []) or []:
            seen_frameworks.add(str(framework))
        if not entry.get("source_ids"):
            errors.append(f"{pid}: missing source_ids")
        for sid in entry.get("source_ids", []) or []:
            if sid not in sources:
                errors.append(f"{pid}: source id does not resolve: {sid}")
    generic_types = {
        str(page_frontmatter(p.get("page_id", "")) or {}).lower()
        for p in packs.get("generic_infra_pack", [])
    }
    generic_page_types = {
        page_type
        for p in packs.get("generic_infra_pack", [])
        for page_type in [str((page_frontmatter(p.get("page_id", "")) or {}).get("page_type") or (page_frontmatter(p.get("page_id", "")) or {}).get("type"))]
    }
    if "interface" not in generic_page_types:
        errors.append("generic infra pack must contain at least one interface page")
    if "capability" not in generic_page_types:
        errors.append("generic infra pack must contain at least one capability page")
    cross_framework_pages = [
        page_frontmatter(p.get("page_id", ""))
        for p in packs.get("cross_framework_pack", [])
    ]
    non_target_frameworks = {
        fw
        for fm in cross_framework_pages
        if fm
        for fw in fm.get("frameworks", []) or []
        if fw != target
    }
    if target_known and len(non_target_frameworks) < 2:
        errors.append("cross-framework pack must include at least two non-target frameworks")
    validation_types = {
        str((page_frontmatter(p.get("page_id", "")) or {}).get("page_type") or (page_frontmatter(p.get("page_id", "")) or {}).get("type"))
        for p in packs.get("validation_risk_pack", [])
    }
    if "failure-mode" not in validation_types:
        errors.append("validation/risk pack must contain a failure-mode page")
    if "validation-pattern" not in validation_types:
        errors.append("validation/risk pack must contain a validation-pattern page")
    if not bundle.get("known_gaps"):
        errors.append("known_gaps must be recorded")
    if not bundle.get("rejected_pages"):
        errors.append("rejected_pages must be recorded")
    if {"framework-profile", "capability", "interface", "algorithm", "failure-mode"} - seen_types:
        errors.append("bundle lacks required page type diversity")
    if target_known and len(seen_frameworks) < 3:
        errors.append("bundle lacks required framework diversity")
    return errors
