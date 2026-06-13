#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from search_symbols import DEFAULT_TERMS, iter_files


CAPABILITY_PATTERNS = {
    "capability-rollout-batched-sync": ["rollout", "generate"],
    "capability-rollout-logprob-capture": ["old_logprobs", "logprob"],
    "capability-weight-sync-distributed": ["update_weights", "weight_version", "checkpoint"],
    "capability-policy-versioning": ["policy_id", "policy version", "weight_version"],
    "capability-reward-verifier": ["reward", "verifier", "score"],
    "capability-sample-grouping": ["group_id", "group_size"],
}


def scan_repo(root: Path) -> tuple[dict[str, list[dict]], str]:
    evidence: dict[str, list[dict]] = {cap: [] for cap in CAPABILITY_PATTERNS}
    blob = []
    for path in iter_files(root):
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        rel = path.relative_to(root).as_posix()
        for lineno, line in enumerate(lines, 1):
            low = line.lower()
            blob.append(low)
            for cap, terms in CAPABILITY_PATTERNS.items():
                if any(term.lower() in low for term in terms):
                    evidence[cap].append({"path": rel, "line": lineno, "symbols": [term for term in terms if term.lower() in low]})
    return evidence, "\n".join(blob)


def main() -> int:
    parser = argparse.ArgumentParser(description="Map an unknown RL framework to RLInfraWiki capabilities")
    parser.add_argument("--name", required=True)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--context")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path(args.repo_root).expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: repo root does not exist: {root}")
        return 1
    evidence, _ = scan_repo(root)
    capability_map = {}
    missing = []
    for cap, rows in evidence.items():
        status = "likely-supported" if rows else "missing"
        capability_map[cap] = {"status": status, "confidence": "inferred", "evidence": rows[:8]}
        if not rows:
            missing.append(cap)
    profile = {
        "framework": args.name,
        "repo_root": str(root),
        "confidence": "inferred",
        "source_status": "local-scan",
        "capability_map": capability_map,
        "missing_evidence": missing,
        "recommended_tasks": [
            "define RolloutBackendAdapter mapping",
            "propagate weight_version through samples and logs",
            "add grouped rollout validation when using GRPO",
            "define reward/verifier timeout and retry behavior",
        ],
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(profile, sort_keys=False, allow_unicode=False), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
