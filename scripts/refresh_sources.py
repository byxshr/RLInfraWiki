#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from _source_refs import render_markdown_report, validate_source_refs, write_json_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a non-mutating SourcePack refresh/drift report.")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--source-root", type=Path, help="Directory containing sibling upstream clones")
    parser.add_argument("--dry-run", action="store_true", help="Compatibility flag; this command is always non-mutating")
    parser.add_argument("--strict-hash", action="store_true", help="Treat legacy sha256 placeholders as errors in the report")
    parser.add_argument("--fail-on-errors", action="store_true", help="Exit non-zero when the report contains drift errors")
    parser.add_argument("--markdown-output", type=Path, help="Write a markdown report")
    parser.add_argument("--json-output", type=Path, help="Write a JSON report")
    args = parser.parse_args()

    report = validate_source_refs(
        check_local=bool(args.source_root),
        source_root=args.source_root,
        strict_hash=args.strict_hash,
    )
    markdown = render_markdown_report(report)
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(markdown, encoding="utf-8")
        print(f"wrote {args.markdown_output}")
    if args.json_output:
        write_json_report(report, args.json_output)
        print(f"wrote {args.json_output}")
    if not args.markdown_output and not args.json_output:
        print(markdown)
    if args.fail_on_errors and report["errors"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
