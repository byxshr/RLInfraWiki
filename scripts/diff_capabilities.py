#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def load_profile(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Diff two framework capability profiles")
    parser.add_argument("left")
    parser.add_argument("right")
    args = parser.parse_args()
    left = load_profile(Path(args.left))
    right = load_profile(Path(args.right))
    left_map = left.get("capability_map", {})
    right_map = right.get("capability_map", {})
    caps = sorted(set(left_map) | set(right_map))
    print("| capability | left | right |")
    print("|---|---|---|")
    for cap in caps:
        print(f"| `{cap}` | {left_map.get(cap, {}).get('status', 'missing')} | {right_map.get(cap, {}).get('status', 'missing')} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
