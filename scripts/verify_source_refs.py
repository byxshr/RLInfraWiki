#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _source_refs import format_issue, validate_source_refs


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SourcePack source_refs metadata and optional local drift")
    parser.add_argument("--check-local", action="store_true", help="Check local clone commits, files, line ranges, and hashes")
    parser.add_argument("--source-root", type=Path, help="Directory containing sibling upstream clones")
    parser.add_argument("--strict-hash", action="store_true", help="Fail on legacy sha256: source-reported placeholders")
    parser.add_argument("--json", action="store_true", help="Print JSON report instead of text")
    args = parser.parse_args()

    report = validate_source_refs(
        check_local=args.check_local,
        source_root=args.source_root,
        strict_hash=args.strict_hash,
    )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for warning in report["warnings"]:
            print(f"WARN: {format_issue(warning)}")
        if report["errors"]:
            print("Source refs validation failed")
            for error in report["errors"]:
                print(f"ERROR: {format_issue(error)}")
        else:
            print(
                "Source refs validation passed "
                f"({report['stats']['source_ref_manifest_count']} source_ref manifests, "
                f"{report['stats']['warning_count']} warning(s))"
            )
    if report["errors"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
