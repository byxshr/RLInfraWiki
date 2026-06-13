#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
import yaml
from _context import load_bundle, validate_bundle
from _rlinfra import (
    DEFERRED_STATUSES,
    TERMINAL_STATUSES,
    VALID_ISSUE_STATUSES,
    VALID_SEVERITIES,
    issue_blocks_promotion,
    load_jsonl,
    load_review_waivers,
    load_yaml,
    normalize_review_issue,
    schema_validation_errors,
    sha256_file,
)

LOCKED_HASHES = {
    "plan_sha256": "docs/plan.md",
    "task_contract_sha256": "task_contract.yaml",
    "goal_sha256": "docs/goal.md",
}


def plan_lock_hashes(lock_path: Path) -> dict[str, str]:
    hashes = {}
    for line in lock_path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if text == "---":
            break
        if not text.startswith("- ") or ":" not in text:
            continue
        key, value = text[2:].split(":", 1)
        key = key.strip()
        if key in LOCKED_HASHES:
            hashes[key] = value.strip()
    return hashes


def validate_plan_lock(ws: Path, errors: list[str]) -> None:
    lock_path = ws / ".humanize" / "plan.lock.md"
    if not lock_path.exists():
        errors.append("missing .humanize/plan.lock.md")
        return
    hashes = plan_lock_hashes(lock_path)
    for key, rel in LOCKED_HASHES.items():
        expected = hashes.get(key)
        if not expected:
            errors.append(f"plan.lock.md missing {key}; rerun lock_plan.py")
            continue
        actual = sha256_file(ws / rel)
        if expected != actual:
            errors.append(f"plan.lock.md {key} does not match {rel}; rerun lock_plan.py")


def validate_contract_validation_matrix(ws: Path, errors: list[str]) -> None:
    contract_path = ws / "task_contract.yaml"
    matrix_path = ws / "docs" / "validation_matrix.md"
    contract = load_yaml(contract_path, {}) or {}
    if not isinstance(contract, dict):
        errors.append("task_contract.yaml must be a YAML mapping")
        return
    if not matrix_path.exists():
        errors.append("missing docs/validation_matrix.md")
        return
    matrix = matrix_path.read_text(encoding="utf-8")
    # render_task_bundle.py writes validation commands as markdown code spans.
    matrix_commands = set(re.findall(r"`([^`]+)`", matrix))
    for command in contract.get("validation_commands", []) or []:
        if str(command) not in matrix_commands:
            errors.append(f"validation_matrix.md missing validation command from task_contract.yaml: {command}")


def validate_context_bundle_files(ws: Path, errors: list[str]) -> None:
    context_dir = ws / "context"
    bundle_md = context_dir / "context_bundle.md"
    bundle_json = context_dir / "context_bundle.json"
    sources_yaml = context_dir / "context_sources.yaml"
    for path in [bundle_md, bundle_json, sources_yaml]:
        if not path.exists():
            errors.append(f"missing {path.relative_to(ws)}")
    if not bundle_md.exists():
        return
    try:
        bundle = load_bundle(bundle_md)
    except SystemExit as exc:
        errors.append(f"context/context_bundle.md cannot be parsed: {exc}")
        return
    for issue in validate_bundle(bundle):
        errors.append(f"context bundle invalid: {issue}")
    if bundle_json.exists():
        try:
            json_bundle = load_bundle(bundle_json)
            if json_bundle.get("id") != bundle.get("id"):
                errors.append("context/context_bundle.json does not match context_bundle.md id")
        except SystemExit as exc:
            errors.append(f"context/context_bundle.json cannot be parsed: {exc}")
    if sources_yaml.exists():
        sources = yaml.safe_load(sources_yaml.read_text(encoding="utf-8")) or {}
        required = [
            "target_framework_pages",
            "generic_pages",
            "cross_framework_pages",
            "validation_risk_pages",
        ]
        for key in required:
            if not sources.get(key):
                errors.append(f"context_sources.yaml missing {key}")
        source_map = sources.get("sources")
        if not isinstance(source_map, dict) or not source_map:
            errors.append("context_sources.yaml missing page/source id map")


def validate_design_claims_have_context(ws: Path, errors: list[str]) -> None:
    bundle_md = ws / "context" / "context_bundle.md"
    if not bundle_md.exists():
        return
    combined = ""
    for rel in ["docs/draft.md", "docs/plan.md", "docs/architecture.md"]:
        path = ws / rel
        if path.exists():
            combined += "\n" + path.read_text(encoding="utf-8")
    lower = combined.lower()
    risky_terms = ["throughput", "latency", "performance", "production"]
    if any(term in lower for term in risky_terms):
        required_terms = ["source", "context", "validation", "risk"]
        missing = [term for term in required_terms if term not in lower]
        if missing:
            errors.append("performance/production claim lacks complete context: missing " + ", ".join(missing))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate RLCR review gate")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--require-review", action="store_true", help="Fail if latest review round lacks codex_review.md")
    args = parser.parse_args()
    ws = Path(args.workspace)
    errors = []
    warnings = []
    if not (ws / "docs" / "goal.md").exists():
        errors.append("missing docs/goal.md")
    validate_plan_lock(ws, errors)
    validate_contract_validation_matrix(ws, errors)
    validate_context_bundle_files(ws, errors)
    validate_design_claims_have_context(ws, errors)
    issues = []
    for idx, issue in enumerate(load_jsonl(ws / "review_issues.jsonl"), 1):
        normalized = normalize_review_issue(issue)
        errors.extend(schema_validation_errors(normalized, "review_issue.schema.json", f"review_issues.jsonl:{idx}"))
        issues.append(normalized)
    _, waivers, waiver_errors = load_review_waivers(ws)
    errors.extend(waiver_errors)
    for issue in issues:
        issue_id = issue.get("id")
        status = str(issue.get("status", "open")).lower()
        severity = str(issue.get("severity", "")).upper()
        if severity not in VALID_SEVERITIES:
            errors.append(f"unknown issue severity blocks promotion: {issue_id} {issue.get('severity')!r}")
            continue
        if status not in VALID_ISSUE_STATUSES:
            errors.append(f"unknown issue status blocks promotion: {issue_id} {status!r}")
            continue
        if status in TERMINAL_STATUSES:
            continue
        if not issue_blocks_promotion(issue, waivers):
            if severity == "P3" and status not in DEFERRED_STATUSES:
                warnings.append(f"unresolved P3 remains open: {issue_id} {issue.get('summary')}")
            continue
        if severity in {"P0", "P1"}:
            errors.append(f"unresolved {severity} issue blocks promotion: {issue_id} {issue.get('summary')}")
        elif severity == "P2":
            errors.append(f"unresolved P2 without approved waiver blocks promotion: {issue_id} {issue.get('summary')}")
    rounds = sorted((ws / "review_rounds").glob("round-*")) if (ws / "review_rounds").exists() else []
    if args.require_review:
        if not rounds:
            errors.append("no review round exists")
        elif not (rounds[-1] / "codex_review.md").exists():
            errors.append(f"missing {rounds[-1] / 'codex_review.md'}")
    elif rounds and not (rounds[-1] / "codex_review.md").exists():
        warnings.append(f"latest review round has no codex_review.md yet: {rounds[-1].name}")
    if errors:
        print("Review gate failed")
        for err in errors:
            print(f"ERROR: {err}")
        for warn in warnings:
            print(f"WARN: {warn}")
        return 1
    print("Review gate passed")
    for warn in warnings:
        print(f"WARN: {warn}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
