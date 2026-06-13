#!/usr/bin/env python3
from __future__ import annotations

import argparse

from _rlinfra import iter_wiki_pages


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest cross-framework analogs")
    parser.add_argument("--capability", default="")
    parser.add_argument("--backend", default="")
    parser.add_argument("--algorithm", default="")
    parser.add_argument("--target-framework")
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    excluded = {str(v).lower() for v in args.exclude}
    if args.target_framework:
        excluded.add(args.target_framework.lower())

    rows = []
    for page in iter_wiki_pages():
        if (page.get("page_type") or page.get("type")) != "framework-profile":
            continue
        framework = str(page.get("framework") or (page.get("frameworks") or [""])[0]).lower()
        if framework in excluded:
            continue
        score = 1
        text = " ".join(str(v) for v in [page.get("summary", ""), page.get("capability_map", ""), page.get("backends", ""), page.get("algorithms", "")]).lower()
        for needle in [args.capability, args.backend, args.algorithm]:
            if needle and needle.lower() in text:
                score += 3
        rows.append((score, page))
    rows.sort(key=lambda item: (-item[0], item[1].get("id", "")))
    for idx, (_, page) in enumerate(rows[: args.limit], 1):
        print(f"{idx}. {page.get('id')}")
        print(f"   reason: {page.get('summary')}")
        print(f"   sources: {', '.join(page.get('sources', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
