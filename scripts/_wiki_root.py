"""Root resolution for RLInfraWiki scripts.

The standalone repository root is also the skill root:

    <RLInfraWiki>/scripts/_wiki_root.py -> <RLInfraWiki>

RLINFRA_WIKI_ROOT may point at an alternate checkout. Invalid overrides or
ambiguous script locations fail with a non-zero exit instead of falling back to
the wrong knowledge base.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _looks_like_wiki_root(path: Path) -> bool:
    return (
        (path / "SKILL.md").is_file()
        and (path / "data" / "tags.yaml").is_file()
        and (path / "wiki").is_dir()
        and (path / "sources").is_dir()
    )


def _error(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def resolve_wiki_root() -> Path:
    env_value = os.environ.get("RLINFRA_WIKI_ROOT")
    if env_value:
        root = Path(env_value).expanduser().resolve()
        if _looks_like_wiki_root(root):
            return root
        _error(
            "RLINFRA_WIKI_ROOT={!r} does not point at an RLInfraWiki root "
            "(expected SKILL.md, data/tags.yaml, wiki/, and sources/).".format(env_value)
        )

    default_root = Path(__file__).resolve().parent.parent
    if _looks_like_wiki_root(default_root):
        return default_root

    seen: set[Path] = set()
    for start in (Path(__file__).resolve().parent, Path.cwd().resolve()):
        for candidate in [start, *start.parents]:
            if candidate in seen:
                continue
            seen.add(candidate)
            if _looks_like_wiki_root(candidate):
                return candidate

    _error(
        "Could not locate RLInfraWiki root. Run scripts from the cloned skill "
        "directory or set RLINFRA_WIKI_ROOT to its absolute path."
    )


WIKI_ROOT = resolve_wiki_root()
