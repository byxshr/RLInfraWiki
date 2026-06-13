#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from _rlinfra import QUERIES_DIR, iter_wiki_pages

INDEX_FIELDS = {
    "by-framework.md": ("frameworks", "Framework"),
    "by-algorithm.md": ("algorithms", "Algorithm"),
    "by-component.md": ("components", "Component"),
    "by-backend.md": ("backends", "Backend"),
    "by-deployment-mode.md": ("deployment_modes", "Deployment Mode"),
    "by-source.md": ("sources", "Source"),
    "by-risk.md": ("risks", "Risk"),
    "by-capability.md": ("capabilities", "Capability"),
    "by-interface.md": ("related_interfaces", "Interface"),
    "by-failure-mode.md": ("failure_modes", "Failure Mode"),
    "by-validation.md": ("validation_patterns", "Validation"),
    "by-adapter-task.md": ("adapter_targets", "Adapter Task"),
}


def link(page):
    return f"[{page.get('title')}]({ '../' + page.get('_path') })"


def render_grouped(filename, field, label, pages):
    groups = defaultdict(list)
    for page in pages:
        for value in page.get(field, []) or []:
            groups[str(value)].append(page)
    lines = [f"# Query: {label}", "", "> Auto-generated. Do not edit manually.", ""]
    lines.append(f"| {label} | Pages |")
    lines.append("|---|---|")
    for value in sorted(groups):
        page_links = ", ".join(link(p) for p in sorted(groups[value], key=lambda x: x.get("title", "")))
        lines.append(f"| `{value}` | {page_links} |")
    return "\n".join(lines) + "\n"


def render_by_problem(pages):
    lines = ["# Query: By Problem", "", "> Auto-generated. Do not edit manually.", "", "| Problem / Risk | Pages |", "|---|---|"]
    groups = defaultdict(list)
    for page in pages:
        for value in page.get("risks", []) or []:
            groups[str(value)].append(page)
    for value in sorted(groups):
        lines.append(f"| `{value}` | {', '.join(link(p) for p in groups[value])} |")
    return "\n".join(lines) + "\n"


def render_topic_map(pages):
    lines = ["# Topic Map", "", "> Auto-generated. Do not edit manually.", ""]
    for page in sorted(pages, key=lambda p: (p.get("page_type") or p.get("type", ""), p.get("title", ""))):
        lines.append(f"- `{page.get('id')}`: {link(page)} - {page.get('summary', '')}")
    return "\n".join(lines) + "\n"


def render_by_page_type(filename, pages, wanted_type, label):
    lines = [f"# Query: {label}", "", "> Auto-generated. Do not edit manually.", "", "| Page | Summary |", "|---|---|"]
    for page in sorted(pages, key=lambda p: p.get("title", "")):
        if (page.get("page_type") or page.get("type")) != wanted_type:
            continue
        lines.append(f"| {link(page)} | {page.get('summary', '')} |")
    return "\n".join(lines) + "\n"


def render_relations(pages):
    lines = ["# Query: By Relation", "", "> Auto-generated. Do not edit manually.", "", "| page | relation | targets |", "|---|---|---|"]
    for page in sorted(pages, key=lambda p: p.get("id", "")):
        relations = page.get("relations") if isinstance(page.get("relations"), dict) else {}
        for rel, targets in relations.items():
            if isinstance(targets, str):
                targets = [targets]
            lines.append(f"| `{page.get('id')}` | `{rel}` | {', '.join(f'`{t}`' for t in targets or [])} |")
    return "\n".join(lines) + "\n"


def render_generic_to_framework(pages):
    lines = ["# Query: Generic To Framework", "", "> Auto-generated. Do not edit manually.", "", "| generic page | frameworks | sources |", "|---|---|---|"]
    for page in sorted(pages, key=lambda p: p.get("id", "")):
        if (page.get("page_type") or page.get("type")) not in {"capability", "interface", "algorithm", "validation-pattern", "failure-mode"}:
            continue
        lines.append(f"| `{page.get('id')}` | {', '.join(f'`{v}`' for v in page.get('frameworks', []) or [])} | {', '.join(f'`{v}`' for v in page.get('sources', []) or [])} |")
    return "\n".join(lines) + "\n"


def render_cross_framework_lessons(pages):
    lines = ["# Query: Cross Framework Lessons", "", "> Auto-generated. Do not edit manually.", "", "| page | frameworks | lesson summary |", "|---|---|---|"]
    for page in sorted(pages, key=lambda p: p.get("id", "")):
        if (page.get("page_type") or page.get("type")) not in {"framework-profile", "comparison", "pattern"}:
            continue
        lines.append(f"| `{page.get('id')}` | {', '.join(f'`{v}`' for v in page.get('frameworks', []) or [])} | {page.get('summary', '')} |")
    return "\n".join(lines) + "\n"


def build_outputs():
    pages = iter_wiki_pages()
    outputs = {name: render_grouped(name, field, label, pages) for name, (field, label) in INDEX_FIELDS.items()}
    outputs["by-problem.md"] = render_by_problem(pages)
    outputs["by-pattern.md"] = render_by_page_type("by-pattern.md", pages, "pattern", "Pattern")
    outputs["by-relation.md"] = render_relations(pages)
    outputs["generic-to-framework.md"] = render_generic_to_framework(pages)
    outputs["cross-framework-lessons.md"] = render_cross_framework_lessons(pages)
    outputs["topic-map.md"] = render_topic_map(pages)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate RLInfraWiki query indices")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs()
    QUERIES_DIR.mkdir(parents=True, exist_ok=True)
    drift = []
    unexpected = []
    for name, content in outputs.items():
        path = QUERIES_DIR / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                drift.append(name)
        else:
            path.write_text(content, encoding="utf-8")
            print(f"wrote {path.relative_to(QUERIES_DIR.parent)}")
    if args.check:
        expected = set(outputs)
        unexpected = sorted(path.name for path in QUERIES_DIR.glob("*.md") if path.name not in expected and path.name != "README.md")
    if drift:
        print("ERROR: generated query indices are stale:")
        for name in drift:
            print(f"  {name}")
    if unexpected:
        print("ERROR: unexpected generated query index file(s):")
        for name in unexpected:
            print(f"  {name}")
    if drift or unexpected:
        print("Run python scripts/generate_indices.py and remove unexpected files")
        return 1
    if args.check:
        print("generated query indices are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
