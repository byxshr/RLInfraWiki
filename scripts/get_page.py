#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from _rlinfra import find_page, load_source_manifests, split_frontmatter, dump_yaml, SKILL_ROOT


def main() -> int:
    parser = argparse.ArgumentParser(description="Get an RLInfraWiki page by id or path")
    parser.add_argument("lookup")
    parser.add_argument("--body-only", action="store_true")
    parser.add_argument("--frontmatter-only", action="store_true")
    parser.add_argument("--follow-sources", action="store_true")
    parser.add_argument("--include-source", action="store_true", help="Include source snippets when --source-root is provided")
    parser.add_argument("--source-root", help="Local clone root used only for explicit snippet expansion")
    args = parser.parse_args()

    path = find_page(args.lookup)
    if not path:
        print(f"ERROR: no page found for {args.lookup}")
        return 1
    fm, body = split_frontmatter(path)
    if args.frontmatter_only:
        print(dump_yaml(fm or {}), end="")
        return 0
    if args.body_only:
        print(body)
        return 0
    print(f"# {path.relative_to(SKILL_ROOT)}\n")
    print(path.read_text(encoding="utf-8"))
    if args.follow_sources and fm:
        manifests = load_source_manifests()
        print("\n---\n## Cited Sources\n")
        for sid in fm.get("sources", []):
            source = manifests.get(sid)
            if not source:
                print(f"### {sid}\nMissing source manifest.\n")
                continue
            print(f"### {sid}")
            print(f"- manifest: `{source.get('_path')}`")
            print(f"- name: {source.get('name')}")
            print(f"- repo: {source.get('repo')}")
            print(f"- commit: {source.get('upstream_commit')}")
            print(f"- local path hint: {source.get('local_path_hint') or source.get('local_path')}")
            print(f"- confidence: source-reported unless local evidence says otherwise\n")
            if source.get("source_refs"):
                print("Source refs:")
                for ref in source.get("source_refs", []):
                    print(f"- `{ref.get('path')}:{ref.get('line_range')}` claim `{ref.get('claim_id')}` hash `{ref.get('sha256')}`")
                print("")
            summary_path = source.get("summary_path")
            if summary_path:
                candidate = SKILL_ROOT / summary_path
                if candidate.exists():
                    print(candidate.read_text(encoding="utf-8"))
                    print("")
            if args.include_source:
                if not args.source_root:
                    print("include-source requested without --source-root; refusing to infer local clone paths.\n")
                    continue
                root = Path(args.source_root).expanduser().resolve()
                local_hint = source.get("local_path_hint") or source.get("local_path") or ""
                local = (root / local_hint).resolve()
                if not local.exists():
                    print(f"local source root missing for {sid}: {local}\n")
                    continue
                print(f"local source root available for explicit snippet lookup: {local}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
