import json
import re
import subprocess
import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_embedded_bundle(markdown: str) -> dict:
    match = re.search(r"<!-- RLINFRA_CONTEXT_BUNDLE_JSON\s*(.*?)\s*-->", markdown, re.DOTALL)
    assert match, markdown
    return json.loads(match.group(1))


def test_rollout_backend_selection_context_is_target_aware_not_target_only(tmp_path):
    output = tmp_path / "context.md"
    task = "select rollout backend between SGLang and vLLM for RLVR with cache logprob and weight update risks"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/compose_context.py"),
            "--target-framework",
            "verl",
            "--task",
            task,
            "--mode",
            "design",
            "--output",
            str(output),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    validate = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_context_bundle.py"), str(output)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr

    bundle = load_embedded_bundle(output.read_text())
    packs = bundle["packs"]
    assert "framework-verl" in {page["page_id"] for page in packs["target_framework_pack"]}
    assert "capability-rollout-backend-selection" in {page["page_id"] for page in packs["generic_infra_pack"]}
    assert "comparisons-rollout-backends" in {page["page_id"] for page in packs["cross_framework_pack"]}
    assert "validation-logprob-consistency" in {page["page_id"] for page in packs["validation_risk_pack"]}
    all_pages = {page["page_id"] for pack in packs.values() for page in pack}
    assert any(not page.startswith("framework-verl") for page in all_pages)
