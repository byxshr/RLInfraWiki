#!/usr/bin/env python3
from __future__ import annotations

import argparse

from _rlinfra import load_aliases, load_yaml, DATA_DIR


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve RLInfraWiki aliases")
    parser.add_argument("term")
    args = parser.parse_args()
    term = args.term.lower()
    raw = load_yaml(DATA_DIR / "aliases.yaml", {}) or {}
    for canonical, aliases in raw.items():
        candidates = {str(canonical).lower(), *(str(v).lower() for v in aliases or [])}
        if term in candidates:
            print(canonical)
            print("aliases: " + ", ".join(str(v) for v in aliases or []))
            return 0
    expanded = load_aliases().get(term)
    if expanded:
        print(sorted(expanded)[0])
        print("aliases: " + ", ".join(sorted(expanded)))
        return 0
    print(args.term)
    print("aliases: <none>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
