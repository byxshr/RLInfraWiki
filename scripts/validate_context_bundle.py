#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from _context import load_bundle, validate_bundle


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate RLInfraWiki context bundle coverage")
    parser.add_argument("bundle")
    args = parser.parse_args()
    errors = validate_bundle(load_bundle(Path(args.bundle)))
    if errors:
        print("Context bundle validation failed")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Context bundle validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
