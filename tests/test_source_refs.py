from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from _source_refs import hash_source_lines, validate_source_refs  # noqa: E402


def init_source_clone(tmp_path: Path, name: str = "demo") -> tuple[Path, str, str]:
    repo = tmp_path / "source-root" / name
    repo.mkdir(parents=True)
    (repo / "src").mkdir()
    source_file = repo / "src" / "file.py"
    source_file.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "init"], check=True, text=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True, text=True, capture_output=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "-c",
            "user.email=test@example.com",
            "-c",
            "user.name=Test",
            "commit",
            "-m",
            "init",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    return repo, head, hash_source_lines(source_file, 1, 2)


def write_wiki_root(
    tmp_path: Path,
    *,
    commit: str,
    sha: str,
    local_path: str = "demo",
    line_range: str = "1-2",
    claim_ids: list[str] | None = None,
    include_claim_ids: bool = True,
    ref_claim_id: str = "claim-demo",
    ref_path: str = "src/file.py",
) -> Path:
    root = tmp_path / "RLInfraWiki"
    (root / "data").mkdir(parents=True, exist_ok=True)
    (root / "wiki").mkdir(exist_ok=True)
    (root / "sources" / "repos").mkdir(parents=True, exist_ok=True)
    (root / "sources" / "source_refs").mkdir(parents=True, exist_ok=True)
    (root / "SKILL.md").write_text("# test\n", encoding="utf-8")
    (root / "data" / "tags.yaml").write_text("frameworks: []\n", encoding="utf-8")
    (root / "data" / "version_claims.yaml").write_text(
        yaml.safe_dump(
            {
                "version_claims": {
                    "vs-demo": {
                        "source_ids": ["repo-demo"],
                        "upstream_commit": commit,
                        "captured_at": "2026-06-15",
                    }
                }
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    (root / "sources" / "repos" / "demo.yaml").write_text(
        yaml.safe_dump(
            {
                "id": "repo-demo",
                "name": "Demo repo",
                "source_category": "upstream-repo",
                "repo": "example/demo",
                "local_path_hint": "demo",
                "captured_at": "2026-06-15",
                "upstream_commit": commit,
                "status": "active",
                "trust_level": "primary",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    manifest = {
        "id": "source-demo",
        "name": "Demo source refs",
        "source_category": "source-code-ref",
        "repo": "example/demo",
        "local_path": local_path,
        "captured_at": "2026-06-15",
        "upstream_commit": commit,
        "status": "included",
        "trust_level": "primary",
        "source_refs": [
            {
                "path": ref_path,
                "line_range": line_range,
                "claim_id": ref_claim_id,
                "sha256": sha,
            }
        ],
    }
    if include_claim_ids:
        manifest["claim_ids"] = claim_ids if claim_ids is not None else ["claim-demo"]
    (root / "sources" / "source_refs" / "demo.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False),
        encoding="utf-8",
    )
    return root


def categories(report: dict) -> set[str]:
    return {item["category"] for item in report["errors"] + report["warnings"]}


def test_source_refs_metadata_and_local_check_pass(tmp_path):
    _, commit, sha = init_source_clone(tmp_path)
    wiki_root = write_wiki_root(tmp_path, commit=commit, sha=sha)

    report = validate_source_refs(skill_root=wiki_root, check_local=True, source_root=tmp_path / "source-root")

    assert report["errors"] == []
    assert report["warnings"] == []


def test_source_refs_support_nested_relative_local_path(tmp_path):
    _, commit, sha = init_source_clone(tmp_path, name="nested/demo")
    wiki_root = write_wiki_root(tmp_path, commit=commit, sha=sha, local_path="nested/demo")

    report = validate_source_refs(skill_root=wiki_root, check_local=True, source_root=tmp_path / "source-root")

    assert report["errors"] == []


def test_source_refs_reject_invalid_line_range(tmp_path):
    _, commit, sha = init_source_clone(tmp_path)
    wiki_root = write_wiki_root(tmp_path, commit=commit, sha=sha, line_range="4-1")

    report = validate_source_refs(skill_root=wiki_root)

    assert "line-range" in categories(report)
    assert report["errors"]


def test_source_refs_missing_line_range_is_not_double_reported(tmp_path):
    _, commit, sha = init_source_clone(tmp_path)
    wiki_root = write_wiki_root(tmp_path, commit=commit, sha=sha, line_range="")

    report = validate_source_refs(skill_root=wiki_root)
    messages = [error["message"] for error in report["errors"]]

    assert "missing line_range" in messages
    assert not any("invalid line_range" in message for message in messages)


def test_source_refs_reject_claim_id_not_listed(tmp_path):
    _, commit, sha = init_source_clone(tmp_path)
    wiki_root = write_wiki_root(tmp_path, commit=commit, sha=sha, claim_ids=["claim-other"])

    report = validate_source_refs(skill_root=wiki_root)

    assert "metadata" in categories(report)
    assert "not listed in manifest claim_ids" in report["errors"][0]["message"]


def test_source_refs_require_manifest_claim_ids(tmp_path):
    _, commit, sha = init_source_clone(tmp_path)
    wiki_root = write_wiki_root(tmp_path, commit=commit, sha=sha, include_claim_ids=False)

    report = validate_source_refs(skill_root=wiki_root)

    assert any(error["message"] == "missing claim_ids" for error in report["errors"])
    assert not any("not listed in manifest claim_ids" in error["message"] for error in report["errors"])


def test_source_refs_detect_missing_clone_and_file(tmp_path):
    _, commit, sha = init_source_clone(tmp_path)
    missing_clone_root = write_wiki_root(tmp_path, commit=commit, sha=sha)
    missing_clone = validate_source_refs(
        skill_root=missing_clone_root,
        check_local=True,
        source_root=tmp_path / "missing-source-root",
    )
    assert "local-clone" in categories(missing_clone)

    missing_file_root = write_wiki_root(tmp_path, commit=commit, sha=sha, ref_path="src/missing.py")
    missing_file = validate_source_refs(
        skill_root=missing_file_root,
        check_local=True,
        source_root=tmp_path / "source-root",
    )
    assert "local-path" in categories(missing_file)


def test_source_refs_detect_commit_and_hash_drift(tmp_path):
    _, commit, sha = init_source_clone(tmp_path)
    commit_drift_root = write_wiki_root(tmp_path, commit="0" * 40, sha=sha)
    commit_drift = validate_source_refs(
        skill_root=commit_drift_root,
        check_local=True,
        source_root=tmp_path / "source-root",
    )
    assert "commit-drift" in categories(commit_drift)

    hash_drift_root = write_wiki_root(tmp_path, commit=commit, sha="1" * 64)
    hash_drift = validate_source_refs(
        skill_root=hash_drift_root,
        check_local=True,
        source_root=tmp_path / "source-root",
    )
    assert "hash-drift" in categories(hash_drift)


def test_source_refs_detect_non_utf8_source_file(tmp_path):
    repo, commit, sha = init_source_clone(tmp_path)
    (repo / "src" / "file.py").write_bytes(b"alpha\n\xff\n")
    wiki_root = write_wiki_root(tmp_path, commit=commit, sha=sha)

    report = validate_source_refs(
        skill_root=wiki_root,
        check_local=True,
        source_root=tmp_path / "source-root",
    )

    assert "encoding" in categories(report)


def test_source_refs_legacy_hash_warns_by_default_and_fails_strict(tmp_path):
    _, commit, _ = init_source_clone(tmp_path)
    wiki_root = write_wiki_root(tmp_path, commit=commit, sha="source-reported")

    default_report = validate_source_refs(skill_root=wiki_root)
    strict_report = validate_source_refs(skill_root=wiki_root, strict_hash=True)

    assert default_report["errors"] == []
    assert "legacy-hash" in categories(default_report)
    assert "legacy-hash" in categories(strict_report)
    assert strict_report["errors"]


def test_verify_source_refs_cli_collapses_warnings_by_default_and_supports_verbose(tmp_path):
    _, commit, _ = init_source_clone(tmp_path)
    wiki_root = write_wiki_root(tmp_path, commit=commit, sha="source-reported")
    env = dict(os.environ)
    env["RLINFRA_WIKI_ROOT"] = str(wiki_root)

    default_result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "verify_source_refs.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    verbose_result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "verify_source_refs.py"), "--verbose"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )

    assert default_result.returncode == 0, default_result.stdout + default_result.stderr
    assert "WARN: legacy-hash: 1 issue(s)" in default_result.stdout
    assert "source_refs[1]" not in default_result.stdout
    assert verbose_result.returncode == 0, verbose_result.stdout + verbose_result.stderr
    assert "WARN: [legacy-hash]" in verbose_result.stdout
    assert "source_refs[1]" in verbose_result.stdout


def test_refresh_sources_dry_run_emits_drift_categories(tmp_path):
    _, commit, sha = init_source_clone(tmp_path)
    wiki_root = write_wiki_root(tmp_path, commit=commit, sha=sha)
    env = dict(os.environ)
    env["RLINFRA_WIKI_ROOT"] = str(wiki_root)

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "refresh_sources.py"),
            "--dry-run",
            "--source-root",
            str(tmp_path / "missing-source-root"),
        ],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Source Refresh Report" in result.stdout
    assert "local-clone" in result.stdout


def test_refresh_sources_can_fail_on_report_errors(tmp_path):
    _, commit, sha = init_source_clone(tmp_path)
    wiki_root = write_wiki_root(tmp_path, commit=commit, sha=sha)
    env = dict(os.environ)
    env["RLINFRA_WIKI_ROOT"] = str(wiki_root)

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "refresh_sources.py"),
            "--dry-run",
            "--source-root",
            str(tmp_path / "missing-source-root"),
            "--fail-on-errors",
        ],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "needs-refresh" in result.stdout


def test_refresh_sources_strict_hash_can_fail_on_report_errors(tmp_path):
    _, commit, _ = init_source_clone(tmp_path)
    wiki_root = write_wiki_root(tmp_path, commit=commit, sha="source-reported")
    env = dict(os.environ)
    env["RLINFRA_WIKI_ROOT"] = str(wiki_root)

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "refresh_sources.py"),
            "--dry-run",
            "--strict-hash",
            "--fail-on-errors",
        ],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "legacy-hash" in result.stdout
