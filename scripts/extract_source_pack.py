#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a metadata-only SourcePack manifest")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    manifest = {
        "repo": args.repo,
        "commit": args.commit,
        "capture_mode": "metadata-only",
        "paths": args.path,
        "notes": "No upstream source is vendored by this command.",
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=False), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
