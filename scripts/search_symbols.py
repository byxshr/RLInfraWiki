#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_TERMS = [
    "trainer",
    "rollout",
    "reward",
    "actor",
    "critic",
    "ref",
    "worker",
    "ray",
    "fsdp",
    "megatron",
    "vllm",
    "sglang",
    "checkpoint",
    "weight_version",
    "old_logprobs",
    "action_mask",
    "group_id",
]


def iter_files(root: Path):
    for path in root.rglob("*"):
        if path.is_dir():
            if path.name in {".git", "__pycache__", ".pytest_cache"}:
                continue
        elif path.suffix.lower() in {".py", ".md", ".rst", ".yaml", ".yml", ".toml", ".json", ".txt"}:
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description="Search framework repo symbols for RL infra mapping")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--terms", nargs="*", default=DEFAULT_TERMS)
    parser.add_argument("--limit", type=int, default=80)
    args = parser.parse_args()
    root = Path(args.repo_root).expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: repo root does not exist: {root}")
        return 1
    count = 0
    for path in iter_files(root):
        rel = path.relative_to(root)
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for lineno, line in enumerate(lines, 1):
            low = line.lower()
            hits = [term for term in args.terms if term.lower() in low]
            if hits:
                print(f"{rel}:{lineno}: {', '.join(hits)}: {line.strip()[:180]}")
                count += 1
                if count >= args.limit:
                    return 0
    if count == 0:
        print("No matching symbols found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
