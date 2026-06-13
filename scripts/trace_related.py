#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import deque

from _rlinfra import iter_wiki_pages


def related_ids(page: dict, relation: str | None) -> list[str]:
    out = []
    relations = page.get("relations") if isinstance(page.get("relations"), dict) else {}
    fields = [relation] if relation else list(relations)
    for field in fields:
        value = relations.get(field, [])
        if isinstance(value, str):
            out.append(value)
        elif isinstance(value, list):
            out.extend(str(v) for v in value)
    for field in ["related_interfaces", "validation_patterns", "failure_modes", "infra_requirements", "required_pages", "comparable_frameworks"]:
        if relation and field != relation:
            continue
        value = page.get(field, [])
        if isinstance(value, list):
            out.extend(str(v) for v in value)
    return list(dict.fromkeys(out))


def main() -> int:
    parser = argparse.ArgumentParser(description="Trace typed RLInfraWiki relations")
    parser.add_argument("page_id")
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--relation")
    args = parser.parse_args()
    pages = {str(page.get("id")): page for page in iter_wiki_pages()}
    if args.page_id not in pages:
        print(f"ERROR: page not found: {args.page_id}")
        return 1
    queue = deque([(args.page_id, 0)])
    seen = {args.page_id}
    while queue:
        pid, depth = queue.popleft()
        page = pages[pid]
        indent = "  " * depth
        print(f"{indent}- {pid} ({page.get('page_type') or page.get('type')})")
        if depth >= args.depth:
            continue
        for rid in related_ids(page, args.relation):
            if rid in pages and rid not in seen:
                seen.add(rid)
                queue.append((rid, depth + 1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
