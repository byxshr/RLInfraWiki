import json
import re
import subprocess
import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from _context import is_async_agentic_ray_task  # noqa: E402


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


def test_training_rollout_mismatch_debug_context_uses_debug_packs(tmp_path):
    output = tmp_path / "mismatch-context.md"
    task = "debug training rollout mismatch old_logprob trainer recompute policy_version weight_version stale KV cache sample schema drift"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/compose_context.py"),
            "--target-framework",
            "slime",
            "--task",
            task,
            "--mode",
            "debug",
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
    assert bundle["mode"] == "debug"
    assert "framework-slime" in {page["page_id"] for page in packs["target_framework_pack"]}
    generic_ids = {page["page_id"] for page in packs["generic_infra_pack"]}
    validation_ids = {page["page_id"] for page in packs["validation_risk_pack"]}
    cross_ids = {page["page_id"] for page in packs["cross_framework_pack"]}
    assert "recipe-debug-training-rollout-mismatch" in generic_ids
    assert "observability-training-inference-mismatch" in generic_ids
    assert "observability-debug-playbook" in generic_ids
    assert "validation-logprob-consistency" in validation_ids
    assert "failure-sample-schema-drift" in validation_ids
    assert "failure-stale-policy-training" in validation_ids
    assert "framework-verl" in cross_ids
    all_pages = {page["page_id"] for pack in packs.values() for page in pack}
    assert any(not page.startswith("framework-slime") for page in all_pages)


def test_async_agentic_ray_context_uses_agentic_orchestration_packs(tmp_path):
    output = tmp_path / "async-agentic-context.md"
    task = "design async agentic RL pipeline with Ray orchestration multi-turn tool calling reward timeout stale policy bound"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/compose_context.py"),
            "--target-framework",
            "areal",
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
    assert "framework-areal" in {page["page_id"] for page in packs["target_framework_pack"]}
    generic_ids = {page["page_id"] for page in packs["generic_infra_pack"]}
    cross_ids = {page["page_id"] for page in packs["cross_framework_pack"]}
    validation_ids = {page["page_id"] for page in packs["validation_risk_pack"]}
    assert "agentic-tool-calling" in generic_ids
    assert "agentic-multi-turn-env" in generic_ids
    assert "pattern-async-rollout" in generic_ids
    assert "interface-orchestrator-adapter" in generic_ids
    assert "capability-rollout-server-async" in generic_ids
    assert "pattern-ray-multirole" in cross_ids
    assert "comparisons-orchestration-options" in cross_ids
    assert "system-roll" in cross_ids
    assert "validation-stale-policy-bound" in validation_ids
    assert "failure-tool-hang" in validation_ids
    assert "failure-reward-timeout" in validation_ids
    all_pages = {page["page_id"] for pack in packs.values() for page in pack}
    assert any(not page.startswith("framework-areal") for page in all_pages)


def test_compound_algorithm_data_contract_keeps_async_agentic_ray_packs(tmp_path):
    output = tmp_path / "compound-async-agentic-contract.md"
    task = "design GRPO algorithm data contract for async agentic Ray multi-turn rollout with logprob trace"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/compose_context.py"),
            "--target-framework",
            "areal",
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

    bundle = load_embedded_bundle(output.read_text())
    packs = bundle["packs"]
    generic_ids = {page["page_id"] for page in packs["generic_infra_pack"]}
    cross_ids = {page["page_id"] for page in packs["cross_framework_pack"]}
    validation_ids = {page["page_id"] for page in packs["validation_risk_pack"]}
    assert "interface-algorithm-data-contract" in generic_ids
    assert "capability-rollout-logprob-capture" in generic_ids
    assert "agentic-tool-calling" in generic_ids
    assert "agentic-multi-turn-env" in generic_ids
    assert "pattern-async-rollout" in generic_ids
    assert "pattern-ray-multirole" in cross_ids
    assert "comparisons-orchestration-options" in cross_ids
    assert "validation-logprob-consistency" in validation_ids
    assert "validation-stale-policy-bound" in validation_ids


def test_compound_rollout_backend_selection_keeps_async_agentic_ray_packs(tmp_path):
    output = tmp_path / "compound-rollout-backend-async-agentic.md"
    task = "design rollout backend selection between SGLang and vLLM for async agentic Ray multi-turn"
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

    bundle = load_embedded_bundle(output.read_text())
    packs = bundle["packs"]
    generic_ids = {page["page_id"] for page in packs["generic_infra_pack"]}
    cross_ids = {page["page_id"] for page in packs["cross_framework_pack"]}
    validation_ids = {page["page_id"] for page in packs["validation_risk_pack"]}
    assert "capability-rollout-backend-selection" in generic_ids
    assert "backend-sglang" in generic_ids
    assert "backend-vllm" in generic_ids
    assert "agentic-tool-calling" in generic_ids
    assert "pattern-async-rollout" in generic_ids
    assert "pattern-ray-multirole" in cross_ids
    assert "comparisons-orchestration-options" in cross_ids
    assert "validation-logprob-consistency" in validation_ids
    assert "validation-stale-policy-bound" in validation_ids


def test_async_agentic_ray_detection_rejects_non_rl_agent_substrings():
    assert is_async_agentic_ray_task(
        "design async agentic RL pipeline with Ray orchestration multi-turn tool calling reward timeout stale policy bound"
    )
    assert is_async_agentic_ray_task(
        "design async agent service rollout pipeline with Ray and reward delays"
    )
    assert is_async_agentic_ray_task(
        "design async agent app proxy with Ray orchestrator and reward timeout"
    )
    assert is_async_agentic_ray_task(
        "design async agent tool snapshot with Ray queue rollback"
    )
    assert not is_async_agentic_ray_task("design async user-agent rollout pipeline with Ray orchestrator")
    assert not is_async_agentic_ray_task("design async chatbot agent rollout with Ray and reward delays")
    assert not is_async_agentic_ray_task("plan async management-agent rollout pipeline with Ray")
    assert not is_async_agentic_ray_task("design async agentless rollout pipeline with Ray")
    assert not is_async_agentic_ray_task("design async event loop agent rollout pipeline with Ray")
    assert not is_async_agentic_ray_task("design async user-agent step rollout pipeline with Ray")
    assert not is_async_agentic_ray_task("design async user-agent app rollout with Ray orchestrator")
