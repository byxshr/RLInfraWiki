#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from _context import load_bundle


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan an adapter from a mapped framework profile and context bundle")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--context")
    parser.add_argument("--target", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    profile = yaml.safe_load(Path(args.profile).read_text(encoding="utf-8")) or {}
    context = load_bundle(Path(args.context)) if args.context else None
    capability_map = profile.get("capability_map", {})
    missing = [cap for cap, data in capability_map.items() if data.get("status") in {"missing", "unknown"}]
    lines = [
        f"# Adapter Plan: {args.target}",
        "",
        f"- framework: `{profile.get('framework')}`",
        "- confidence: `inferred`",
        "- verification status: source-reported context plus local symbol scan; no GPU/NCCL/performance validation.",
        "",
        "## Target Capability",
        "",
        f"`{args.target}`",
        "",
        "## Required Interface Contracts",
        "",
        "- `interface-rollout-backend-adapter`",
        "- `interface-weight-sync-adapter`",
        "- `interface-algorithm-data-contract`",
        "",
        "## Missing Evidence",
        "",
    ]
    lines.extend(f"- `{cap}`" for cap in missing) if missing else lines.append("- No missing capability buckets from the shallow scan.")
    lines.extend([
        "",
        "## Implementation Tasks",
        "",
        "1. Map target framework rollout lifecycle to `RolloutBackendAdapter`.",
        "2. Add explicit `weight_version` and policy/version metadata to samples and logs.",
        "3. Define SGLang update path, cache flush policy, and full checkpoint fallback.",
        "4. Add schema, logprob, grouped rollout, and failure injection checks.",
        "",
        "## Validation Matrix",
        "",
        "| requirement | validation page | expected evidence |",
        "|---|---|---|",
        "| weight version propagation | `validation-weight-version-monotonicity` | local command/log artifact |",
        "| pause/drain before update | `validation-pause-update-resume` | lifecycle trace or unit test |",
        "| train/infer schema match | `validation-train-infer-schema-match` | schema/unit test |",
        "",
        "## Risk Register",
        "",
        "- `failure-partial-weight-update`: fail closed or fall back to full checkpoint sync.",
        "- `failure-stale-kv-cache`: flush or namespace cache by weight version.",
        "- `failure-sample-schema-drift`: reject batches missing required algorithm fields.",
    ])
    if context:
        lines.extend(["", "## Context Pages", ""])
        for pack, pages in context.get("packs", {}).items():
            ids = ", ".join(f"`{page.get('page_id')}`" for page in pages)
            lines.append(f"- {pack}: {ids}")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
