from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from _rlinfra import SKILL_ROOT, load_yaml

SOURCE_BASES = ["repos", "docs", "papers", "blogs", "issues", "source_refs"]
REQUIRED_MANIFEST_FIELDS = ["id", "repo", "upstream_commit", "source_refs", "captured_at", "claim_ids"]
REQUIRED_REF_FIELDS = ["path", "line_range", "claim_id", "sha256"]
LINE_RANGE_RE = re.compile(r"^(\d+)-(\d+)$")
HEX_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
LEGACY_HASH_PLACEHOLDER = "source-reported"
GIT_TIMEOUT_SECONDS = 10


@dataclass(frozen=True)
class SourceRefIssue:
    severity: str
    category: str
    label: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "category": self.category,
            "label": self.label,
            "message": self.message,
        }


def issue(severity: str, category: str, label: str, message: str) -> SourceRefIssue:
    return SourceRefIssue(severity=severity, category=category, label=label, message=message)


def scan_source_manifests(skill_root: Path = SKILL_ROOT) -> list[dict[str, Any]]:
    manifests: list[dict[str, Any]] = []
    sources_dir = skill_root / "sources"
    for base_name in SOURCE_BASES:
        base = sources_dir / base_name
        if not base.exists():
            continue
        for path in sorted(base.glob("*.yaml")):
            data = load_yaml(path, {}) or {}
            if not isinstance(data, dict):
                data = {}
            data = dict(data)
            data["_abs_path"] = path
            data["_path"] = path.relative_to(skill_root).as_posix()
            data["_source_base"] = base_name
            manifests.append(data)
    return manifests


def load_version_claims_from(skill_root: Path = SKILL_ROOT) -> dict[str, dict[str, Any]]:
    raw = load_yaml(skill_root / "data" / "version_claims.yaml", {}) or {}
    claims = raw.get("version_claims", raw)
    if isinstance(claims, list):
        return {str(claim.get("id")): claim for claim in claims if isinstance(claim, dict) and claim.get("id")}
    return claims if isinstance(claims, dict) else {}


def version_commits_by_repo(
    manifests: list[dict[str, Any]], version_claims: dict[str, dict[str, Any]]
) -> dict[str, set[str]]:
    manifests_by_id = {str(manifest.get("id")): manifest for manifest in manifests if manifest.get("id")}
    commits: dict[str, set[str]] = {}
    for claim in version_claims.values():
        if not isinstance(claim, dict):
            continue
        for source_id in claim.get("source_ids", []) or []:
            manifest = manifests_by_id.get(str(source_id))
            if not manifest:
                continue
            repo = manifest.get("repo")
            commit = claim.get("upstream_commit") or manifest.get("upstream_commit")
            if repo and commit:
                commits.setdefault(str(repo), set()).add(str(commit))
    return commits


def parse_line_range(value: Any) -> tuple[int, int] | None:
    match = LINE_RANGE_RE.fullmatch(str(value or ""))
    if not match:
        return None
    start, end = int(match.group(1)), int(match.group(2))
    if start < 1 or end < start:
        return None
    return start, end


def is_hex_sha(value: Any) -> bool:
    return bool(HEX_SHA_RE.fullmatch(str(value or "")))


def read_source_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def hash_lines(lines: list[str], start: int, end: int) -> str:
    snippet = "\n".join(lines[start - 1 : end]) + "\n"
    return hashlib.sha256(snippet.encode("utf-8")).hexdigest()


def hash_source_lines(path: Path, start: int, end: int) -> str:
    return hash_lines(read_source_lines(path), start, end)


def source_ref_manifests(skill_root: Path = SKILL_ROOT) -> list[dict[str, Any]]:
    return [manifest for manifest in scan_source_manifests(skill_root) if manifest.get("_source_base") == "source_refs"]


def clone_rel_path(manifest: dict[str, Any]) -> Path | None:
    value = manifest.get("local_path") or manifest.get("local_path_hint")
    if not value:
        return None
    rel = Path(str(value))
    if rel.is_absolute() or ".." in rel.parts:
        return None
    return rel


def resolve_clone_root(manifest: dict[str, Any], source_root: Path) -> Path | None:
    rel = clone_rel_path(manifest)
    if not rel:
        return None
    return (source_root / rel).expanduser().resolve()


def is_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def git_head(repo_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            text=True,
            capture_output=True,
            check=False,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def validate_source_refs(
    *,
    skill_root: Path = SKILL_ROOT,
    check_local: bool = False,
    source_root: Path | None = None,
    strict_hash: bool = False,
) -> dict[str, Any]:
    skill_root = skill_root.resolve()
    resolved_source_root = source_root.expanduser().resolve() if source_root else None
    manifests = scan_source_manifests(skill_root)
    version_claims = load_version_claims_from(skill_root)
    repo_version_commits = version_commits_by_repo(manifests, version_claims)
    issues: list[SourceRefIssue] = []

    seen_ids: dict[str, str] = {}
    for manifest in manifests:
        sid = manifest.get("id")
        label = str(manifest.get("_path"))
        if not sid:
            issues.append(issue("error", "metadata", label, "missing source id"))
            continue
        sid = str(sid)
        if sid in seen_ids:
            issues.append(issue("error", "metadata", label, f"duplicate source id {sid!r}; first seen in {seen_ids[sid]}"))
        else:
            seen_ids[sid] = label

    ref_manifests = [manifest for manifest in manifests if manifest.get("_source_base") == "source_refs"]
    for manifest in ref_manifests:
        label = str(manifest.get("_path"))
        for field in REQUIRED_MANIFEST_FIELDS:
            if not manifest.get(field):
                issues.append(issue("error", "metadata", label, f"missing {field}"))

        repo = str(manifest.get("repo") or "")
        upstream_commit = str(manifest.get("upstream_commit") or "")
        expected_commits = repo_version_commits.get(repo)
        if expected_commits and upstream_commit and upstream_commit not in expected_commits:
            issues.append(
                issue(
                    "error",
                    "version-claim",
                    label,
                    f"upstream_commit {upstream_commit} does not match version claims for {repo}: {sorted(expected_commits)}",
                )
            )
        elif repo and upstream_commit and not expected_commits:
            issues.append(issue("warning", "version-claim", label, f"no version claim found for repo {repo}"))

        raw_claim_ids = manifest.get("claim_ids", []) or []
        claim_ids_valid = bool(raw_claim_ids) and isinstance(raw_claim_ids, list)
        if raw_claim_ids and not isinstance(raw_claim_ids, list):
            issues.append(issue("error", "metadata", label, "claim_ids must be a non-empty list"))
            raw_claim_ids = []
        claim_ids = {str(claim_id) for claim_id in raw_claim_ids}
        refs = manifest.get("source_refs", []) or []
        if not isinstance(refs, list) or not refs:
            issues.append(issue("error", "metadata", label, "source_refs must be a non-empty list"))
            continue

        clone_root = resolve_clone_root(manifest, resolved_source_root) if check_local and resolved_source_root else None
        head: str | None = None
        if check_local:
            local_path_value = manifest.get("local_path") or manifest.get("local_path_hint")
            if not resolved_source_root:
                issues.append(issue("error", "local-clone", label, "--source-root is required with --check-local"))
            elif not clone_root:
                if local_path_value:
                    issues.append(
                        issue("error", "local-clone", label, "local_path/local_path_hint must be relative and stay under source root")
                    )
                else:
                    issues.append(issue("error", "local-clone", label, "missing local_path/local_path_hint"))
            elif not is_under(clone_root, resolved_source_root):
                issues.append(issue("error", "local-clone", label, f"clone root escapes source root: {clone_root}"))
            elif not clone_root.exists():
                issues.append(issue("error", "local-clone", label, f"missing clone root: {clone_root}"))
            elif not (clone_root / ".git").exists():
                issues.append(issue("error", "local-clone", label, f"not a git clone: {clone_root}"))
            else:
                head = git_head(clone_root)
                if not head:
                    issues.append(issue("error", "local-clone", label, f"cannot read git HEAD: {clone_root}"))
                elif upstream_commit and head != upstream_commit:
                    issues.append(
                        issue(
                            "error",
                            "commit-drift",
                            label,
                            f"git HEAD {head} does not match upstream_commit {upstream_commit} in {clone_root}",
                        )
                    )

        for idx, ref in enumerate(refs, 1):
            ref_label = f"{label}:source_refs[{idx}]"
            if not isinstance(ref, dict):
                issues.append(issue("error", "metadata", ref_label, "source ref must be a mapping"))
                continue
            missing_fields = set()
            for field in REQUIRED_REF_FIELDS:
                if not ref.get(field):
                    missing_fields.add(field)
                    issues.append(issue("error", "metadata", ref_label, f"missing {field}"))
            line_range = None
            if "line_range" not in missing_fields:
                line_range = parse_line_range(ref.get("line_range"))
            if "line_range" not in missing_fields and not line_range:
                issues.append(issue("error", "line-range", ref_label, f"invalid line_range {ref.get('line_range')!r}"))
            claim_id = str(ref.get("claim_id") or "")
            if claim_id and claim_ids_valid and claim_id not in claim_ids:
                issues.append(issue("error", "metadata", ref_label, f"claim_id {claim_id!r} not listed in manifest claim_ids"))

            sha = str(ref.get("sha256") or "")
            if sha == LEGACY_HASH_PLACEHOLDER:
                severity = "error" if strict_hash else "warning"
                issues.append(issue(severity, "legacy-hash", ref_label, "sha256 uses legacy source-reported placeholder"))
            elif "sha256" not in missing_fields and sha and not is_hex_sha(sha):
                issues.append(issue("error", "metadata", ref_label, f"sha256 must be 64 hex chars or {LEGACY_HASH_PLACEHOLDER!r}"))

            if not check_local or not clone_root or not clone_root.exists() or not line_range or "path" in missing_fields:
                continue
            source_path = (clone_root / str(ref.get("path") or "")).resolve()
            if not is_under(source_path, clone_root):
                issues.append(issue("error", "local-path", ref_label, f"path escapes clone root: {ref.get('path')}"))
                continue
            if not source_path.is_file():
                issues.append(issue("error", "local-path", ref_label, f"missing source file: {source_path}"))
                continue
            try:
                lines = read_source_lines(source_path)
            except UnicodeDecodeError as exc:
                issues.append(issue("error", "encoding", ref_label, f"source file is not valid UTF-8: {exc}"))
                continue
            start, end = line_range
            if end > len(lines):
                issues.append(
                    issue(
                        "error",
                        "line-range",
                        ref_label,
                        f"line_range {start}-{end} exceeds file length {len(lines)} for {source_path}",
                    )
                )
                continue
            if is_hex_sha(sha):
                actual = hash_lines(lines, start, end)
                if actual != sha:
                    issues.append(issue("error", "hash-drift", ref_label, f"sha256 mismatch: expected {sha}, actual {actual}"))

    errors = [item.as_dict() for item in issues if item.severity == "error"]
    warnings = [item.as_dict() for item in issues if item.severity == "warning"]
    return {
        "check_local": check_local,
        "source_root": str(resolved_source_root) if resolved_source_root else None,
        "stats": {
            "source_manifest_count": len(manifests),
            "source_ref_manifest_count": len(ref_manifests),
            "error_count": len(errors),
            "warning_count": len(warnings),
        },
        "errors": errors,
        "warnings": warnings,
    }


def format_issue(item: dict[str, str]) -> str:
    return f"[{item['category']}] {item['label']}: {item['message']}"


def render_markdown_report(report: dict[str, Any]) -> str:
    status = "needs-refresh" if report["errors"] else "clean"
    lines = [
        "# Source Refresh Report",
        "",
        f"- status: {status}",
        f"- check_local: {str(report['check_local']).lower()}",
        f"- source_root: {report.get('source_root') or 'not provided'}",
        f"- source_manifests: {report['stats']['source_manifest_count']}",
        f"- source_ref_manifests: {report['stats']['source_ref_manifest_count']}",
        f"- errors: {report['stats']['error_count']}",
        f"- warnings: {report['stats']['warning_count']}",
        "",
    ]
    if report["errors"]:
        lines.extend(["## Errors", ""])
        lines.extend(f"- {format_issue(item)}" for item in report["errors"])
        lines.append("")
    if report["warnings"]:
        lines.extend(["## Warnings", ""])
        lines.extend(f"- {format_issue(item)}" for item in report["warnings"])
        lines.append("")
    if not report["errors"] and not report["warnings"]:
        lines.extend(["No source refresh drift detected.", ""])
    return "\n".join(lines)


def write_json_report(report: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
