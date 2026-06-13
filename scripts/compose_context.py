#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from _context import compose_bundle, validate_bundle, write_bundle


def main() -> int:
    parser = argparse.ArgumentParser(description="Compose a target-aware RLInfraWiki context bundle")
    parser.add_argument("--target-framework")
    parser.add_argument("--repo-root")
    parser.add_argument("--task", required=True)
    parser.add_argument("--mode", default="design", choices=["design", "adapter", "debug", "explain"])
    parser.add_argument("--max-pages", type=int, default=16)
    parser.add_argument("--format", default="auto", choices=["auto", "markdown", "json", "yaml"])
    parser.add_argument("--output", required=True)
    parser.add_argument("--allow-invalid", action="store_true")
    args = parser.parse_args()

    bundle = compose_bundle(
        task=args.task,
        target_framework=args.target_framework,
        mode=args.mode,
        max_pages=args.max_pages,
        repo_root=args.repo_root,
    )
    errors = validate_bundle(bundle)
    if errors and not args.allow_invalid:
        print("ERROR: composed context bundle failed validation")
        for error in errors:
            print(f"  - {error}")
        return 1
    write_bundle(bundle, Path(args.output), args.format)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
