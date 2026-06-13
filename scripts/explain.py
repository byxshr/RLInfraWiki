#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from _rlinfra import find_page, split_frontmatter


def main() -> int:
    parser = argparse.ArgumentParser(description="Explain a term or page with source-traceable pointers")
    parser.add_argument("term")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    page = find_page(args.term)
    if page:
        fm, _ = split_frontmatter(page)
        print(f"{fm.get('id')}: {fm.get('summary')}")
        print(f"path: {page}")
        print(f"sources: {', '.join(fm.get('sources', []))}")
        return 0
    query = Path(__file__).with_name("query.py")
    return subprocess.call([sys.executable, str(query), args.term, "--limit", str(args.limit)])


if __name__ == "__main__":
    raise SystemExit(main())
