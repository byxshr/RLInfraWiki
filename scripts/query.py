#!/usr/bin/env python3
from __future__ import annotations

import argparse
from _rlinfra import expand_terms, iter_wiki_pages, tokenize


def contains_any(values, wanted):
    actual = {str(v).lower() for v in (values or [])}
    return bool(actual & {str(v).lower() for v in wanted})


def page_type(page):
    return str(page.get("page_type") or page.get("type") or "")


def field_values(page, *fields):
    values = []
    for field in fields:
        raw = page.get(field, [])
        if isinstance(raw, dict):
            values.extend(raw)
        elif isinstance(raw, list):
            values.extend(raw)
        elif raw:
            values.append(raw)
    return values


def score_page(page, terms):
    hay_title = str(page.get("title", "")).lower()
    hay_summary = str(page.get("summary", "")).lower()
    hay_id = str(page.get("id", "")).lower()
    hay_type = page_type(page).lower()
    hay_tags = " ".join(
        str(v)
        for key in [
            "tags",
            "frameworks",
            "backends",
            "components",
            "algorithms",
            "deployment_modes",
            "risks",
            "failure_modes",
            "validation_patterns",
            "capabilities",
            "related_interfaces",
            "implements_interfaces",
        ]
        for v in field_values(page, key)
    ).lower()
    hay_body = str(page.get("_body", "")).lower()
    score = 0
    for term in terms:
        if term in hay_id:
            score += 10
        if term in hay_title:
            score += 10
        if term in hay_type:
            score += 8
        if term in hay_tags:
            score += 6
        if term in hay_summary:
            score += 4
        score += min(hay_body.count(term), 3)
    if page.get("sources"):
        score += 2
    return score


def main() -> int:
    parser = argparse.ArgumentParser(description="Query RLInfraWiki pages")
    parser.add_argument("query", nargs="?", default="", help="Keyword query")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--framework")
    parser.add_argument("--backend")
    parser.add_argument("--component")
    parser.add_argument("--algorithm")
    parser.add_argument("--deployment-mode")
    parser.add_argument("--capability")
    parser.add_argument("--interface")
    parser.add_argument("--failure")
    parser.add_argument("--adapter-task")
    parser.add_argument("--confidence")
    parser.add_argument("--type")
    parser.add_argument("--page-type")
    parser.add_argument("--source")
    parser.add_argument("--risk")
    args = parser.parse_args()

    query_text = " ".join(
        value
        for value in [
            args.query,
            args.capability,
            args.interface,
            args.failure,
            args.adapter_task,
        ]
        if value
    )
    terms = expand_terms(tokenize(query_text)) if query_text else []
    rows = []
    for page in iter_wiki_pages():
        if args.framework and not contains_any(page.get("frameworks"), [args.framework]):
            continue
        if args.backend and not contains_any(page.get("backends"), [args.backend]):
            continue
        if args.component and not contains_any(page.get("components"), [args.component]):
            continue
        if args.algorithm and not contains_any(page.get("algorithms"), [args.algorithm]):
            continue
        if args.deployment_mode and not contains_any(page.get("deployment_modes"), [args.deployment_mode]):
            continue
        if args.capability and args.capability.lower() not in str(page.get("id", "")).lower() and not contains_any(field_values(page, "capabilities", "related_capabilities", "required_capabilities"), [args.capability]):
            continue
        if args.interface and args.interface.lower() not in str(page.get("id", "")).lower() and not contains_any(field_values(page, "interfaces", "related_interfaces", "implements_interfaces"), [args.interface]):
            continue
        if args.failure and args.failure.lower() not in str(page.get("id", "")).lower() and not contains_any(field_values(page, "failure_modes", "risks"), [args.failure]):
            continue
        if args.adapter_task and args.adapter_task.lower() not in str(page.get("id", "")).lower() and not contains_any(field_values(page, "adapter_targets", "tags"), [args.adapter_task]):
            continue
        if args.confidence and str(page.get("confidence")) != args.confidence:
            continue
        requested_type = args.page_type or args.type
        if requested_type and page_type(page) != requested_type:
            continue
        if args.source and args.source not in (page.get("sources") or []):
            continue
        if args.risk and not contains_any(page.get("risks"), [args.risk]):
            continue
        score = score_page(page, terms) if terms else 1
        if score > 0:
            rows.append((score, page))

    rows.sort(key=lambda item: (-item[0], item[1].get("title", "")))
    for idx, (score, page) in enumerate(rows[: args.limit], 1):
        print(f"{idx}. {page.get('id')} | {page.get('title')} | {page.get('_path')} | score={score}")
        print(f"   summary: {page.get('summary', '')}")
        print(f"   sources: {', '.join(page.get('sources', []))}")
    if not rows:
        print("No matching RLInfraWiki pages found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
