#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Read a small local source snippet with explicit source root")
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    args = parser.parse_args()
    root = Path(args.source_root).expanduser().resolve()
    target = (root / args.path).resolve()
    if not str(target).startswith(str(root)) or not target.is_file():
        print(f"ERROR: source path not found under source root: {target}")
        return 1
    lines = target.read_text(encoding="utf-8", errors="ignore").splitlines()
    for lineno in range(args.start, min(args.end, len(lines)) + 1):
        print(f"{lineno}: {lines[lineno - 1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
