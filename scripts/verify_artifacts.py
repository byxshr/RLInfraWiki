#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from _rlinfra import SKILL_ROOT


def main() -> int:
    errors = []
    artifacts = SKILL_ROOT / "artifacts"
    for path in artifacts.rglob("PROVENANCE.yaml"):
        manifest = path.parent / "MANIFEST.yaml"
        if not manifest.exists():
            errors.append(f"{path.parent}: missing MANIFEST.yaml")
    if errors:
        print("Artifact validation failed")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Artifact validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
