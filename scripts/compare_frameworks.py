#!/usr/bin/env python3
from __future__ import annotations

import argparse

from _rlinfra import iter_wiki_pages


def capability_status(page: dict, capability: str) -> str:
    cap_map = page.get("capability_map")
    if isinstance(cap_map, dict):
        for key, value in cap_map.items():
            if capability in key:
                if isinstance(value, dict):
                    return str(value.get("status", "source-reported"))
                return str(value)
    text = str(page.get("summary", "")).lower()
    return "source-mentioned" if capability.lower() in text else "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare framework capability support")
    parser.add_argument("frameworks", nargs="+")
    parser.add_argument("--capability", default="weight-sync")
    parser.add_argument("--format", choices=["markdown", "text"], default="text")
    args = parser.parse_args()
    profiles = {
        str(page.get("framework") or (page.get("frameworks") or [""])[0]).lower(): page
        for page in iter_wiki_pages()
        if (page.get("page_type") or page.get("type")) == "framework-profile"
    }
    if args.format == "markdown":
        print("| capability | " + " | ".join(args.frameworks) + " | evidence |")
        print("|---|" + "|".join("---" for _ in args.frameworks) + "|---|")
        values = []
        evidence = []
        for fw in args.frameworks:
            page = profiles.get(fw.lower())
            values.append(capability_status(page or {}, args.capability))
            evidence.extend((page or {}).get("sources", []))
        print(f"| `{args.capability}` | " + " | ".join(values) + f" | {', '.join(sorted(set(evidence)))} |")
        return 0
    for fw in args.frameworks:
        page = profiles.get(fw.lower())
        if not page:
            print(f"{fw}: unknown")
            continue
        print(f"{fw}: {capability_status(page, args.capability)} sources={', '.join(page.get('sources', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
