#!/usr/bin/env python3
from __future__ import annotations

import argparse

from _rlinfra import WIKI_DIR

PATTERNS = ["../slime", "../sglang", "../verl", "../ROLL", "../AReaL"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check for legacy local relative evidence paths")
    parser.add_argument("--rewrite-local-paths", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    hits = []
    for path in WIKI_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for pattern in PATTERNS:
            if pattern in text:
                hits.append((path, pattern))
    if hits:
        print("Legacy local path references remain:")
        for path, pattern in hits:
            print(f"- {path}: {pattern}")
        if args.rewrite_local_paths and args.dry_run:
            print("dry-run only; use SourcePack source_refs and edit pages explicitly.")
        return 1
    print("No legacy local relative evidence paths found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
