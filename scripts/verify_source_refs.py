#!/usr/bin/env python3
from __future__ import annotations

from _rlinfra import SOURCES_DIR, load_yaml


def main() -> int:
    errors = []
    for path in sorted((SOURCES_DIR / "source_refs").glob("*.yaml")):
        data = load_yaml(path, {}) or {}
        for field in ["id", "repo", "upstream_commit", "source_refs", "captured_at"]:
            if not data.get(field):
                errors.append(f"{path}: missing {field}")
        for idx, ref in enumerate(data.get("source_refs", []) or [], 1):
            for field in ["path", "line_range", "claim_id", "sha256"]:
                if not ref.get(field):
                    errors.append(f"{path}: source_refs[{idx}] missing {field}")
    if errors:
        print("Source ref validation failed")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Source refs validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
