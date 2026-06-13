#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from _context import bundle_source_summary, load_bundle, write_bundle


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an existing context bundle in another format")
    parser.add_argument("bundle")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json", "yaml", "sources-yaml"])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    bundle = load_bundle(Path(args.bundle))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "sources-yaml":
        output.write_text(
            yaml.safe_dump(bundle_source_summary(bundle), sort_keys=False, allow_unicode=False),
            encoding="utf-8",
        )
    else:
        write_bundle(bundle, output, args.format)
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
