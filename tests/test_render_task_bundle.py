import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCAFFOLDED_DOCS = [
    "goal.md",
    "draft.md",
    "plan.md",
    "architecture.md",
    "interfaces.md",
    "validation_matrix.md",
    "risk_register.md",
    "review.md",
    "goal_status.md",
    "codex_tasks.md",
]


def render(out, *extra_args):
    return render_contract(ROOT / "examples/task_contracts/slime-weight-sync.yaml", out, *extra_args)


def render_contract(contract, out, *extra_args):
    return subprocess.run([
        sys.executable, str(ROOT / "scripts/render_task_bundle.py"),
        "--contract", str(contract),
        "--output", str(out),
        *extra_args,
    ], cwd=ROOT, text=True, capture_output=True)


def test_render_task_bundle(tmp_path):
    out = tmp_path / "task"
    result = render(out)
    assert result.returncode == 0, result.stdout + result.stderr
    assert (out / "docs/goal.md").exists()
    assert (out / ".humanize/rlcr_config.yaml").exists()
    assert (out / "review_issues.jsonl").exists()


def test_render_task_bundle_algorithm_data_contract_scaffold(tmp_path):
    out = tmp_path / "algorithm-task"
    contract = ROOT / "examples/task_contracts/slime-grpo-rlvr-data-contract.yaml"
    result = render_contract(contract, out)
    assert result.returncode == 0, result.stdout + result.stderr

    plan = (out / "docs" / "plan.md").read_text()
    draft = (out / "docs" / "draft.md").read_text()
    interfaces = (out / "docs" / "interfaces.md").read_text()
    assert "## Algorithm Data Contract" in plan
    assert "`old_logprob`" in plan
    assert "`group_id`" in interfaces
    assert "sample schema drift" in draft
    assert "## P0 Sync Contract" not in plan

    bundle = json.loads((out / "context" / "context_bundle.json").read_text())
    generic_ids = {
        page["page_id"]
        for page in bundle["packs"]["generic_infra_pack"]
    }
    validation_ids = {
        page["page_id"]
        for page in bundle["packs"]["validation_risk_pack"]
    }
    assert "interface-algorithm-data-contract" in generic_ids
    assert "capability-rollout-logprob-capture" in generic_ids
    assert "validation-logprob-consistency" in validation_ids
    assert "failure-sample-schema-drift" in validation_ids


def test_render_task_bundle_rollout_backend_selection_scaffold(tmp_path):
    out = tmp_path / "rollout-backend-task"
    contract = ROOT / "examples/task_contracts/rollout-backend-selection.yaml"
    result = render_contract(contract, out)
    assert result.returncode == 0, result.stdout + result.stderr

    plan = (out / "docs" / "plan.md").read_text()
    draft = (out / "docs" / "draft.md").read_text()
    architecture = (out / "docs" / "architecture.md").read_text()
    interfaces = (out / "docs" / "interfaces.md").read_text()
    risk_register = (out / "docs" / "risk_register.md").read_text()

    assert "## Rollout Backend Selection" in plan
    assert "`primary_backend`" in plan
    assert "`fallback_backend`" in plan
    assert "`weight_version`" in plan
    assert "flush_cache" in plan
    assert "logprob policy" in plan
    assert "No local GPU, NCCL, multi-node, throughput, latency, or production readiness claim" in plan
    assert "Source-backed evidence" in draft
    assert "Pending RLCR iteration" not in architecture
    assert "Pending RLCR iteration" not in interfaces
    assert "Pending RLCR iteration" not in risk_register
    assert "## Algorithm Data Contract" not in plan

    bundle = json.loads((out / "context" / "context_bundle.json").read_text())
    packs = bundle["packs"]
    generic_ids = {page["page_id"] for page in packs["generic_infra_pack"]}
    cross_ids = {page["page_id"] for page in packs["cross_framework_pack"]}
    validation_ids = {page["page_id"] for page in packs["validation_risk_pack"]}
    assert "capability-rollout-backend-selection" in generic_ids
    assert "backend-sglang" in generic_ids
    assert "backend-vllm" in generic_ids
    assert "comparisons-rollout-backends" in cross_ids
    assert "pattern-colocated-train-rollout" in cross_ids
    assert "pattern-disaggregated-train-rollout" in cross_ids
    assert "pattern-pd-disaggregation" in cross_ids
    assert "validation-logprob-consistency" in validation_ids
    assert "failure-stale-kv-cache" in validation_ids
    assert "failure-inconsistent-logprob" in validation_ids


def test_render_task_bundle_training_rollout_mismatch_debug_scaffold(tmp_path):
    out = tmp_path / "mismatch-debug-task"
    contract = ROOT / "examples/task_contracts/training-rollout-mismatch-debug.yaml"
    result = render_contract(contract, out)
    assert result.returncode == 0, result.stdout + result.stderr

    plan = (out / "docs" / "plan.md").read_text()
    draft = (out / "docs" / "draft.md").read_text()
    architecture = (out / "docs" / "architecture.md").read_text()
    interfaces = (out / "docs" / "interfaces.md").read_text()
    risk_register = (out / "docs" / "risk_register.md").read_text()

    assert "## Debugging Packet" in plan
    assert "### Symptom" in plan
    assert "### Evidence To Collect" in plan
    assert "### Hypothesis Matrix" in plan
    assert "### Replay/Recompute Checklist" in plan
    assert "### Version Cache Logprob Schema Matrix" in plan
    assert "### Failure Isolation Order" in plan
    assert "### Stop Conditions" in plan
    assert "### Non-Claims" in plan
    assert "`policy_version`" in plan
    assert "`weight_version`" in plan
    assert "cache policy" in plan
    assert "schema policy" in plan
    assert "Source-reported backend/framework behavior remains source-reported" in plan
    assert "## P0 Sync Contract" not in plan
    assert "Source-backed evidence" in draft
    assert "Pending RLCR iteration" not in architecture
    assert "Pending RLCR iteration" not in interfaces
    assert "Pending RLCR iteration" not in risk_register

    bundle = json.loads((out / "context" / "context_bundle.json").read_text())
    packs = bundle["packs"]
    assert bundle["mode"] == "debug"
    generic_ids = {page["page_id"] for page in packs["generic_infra_pack"]}
    validation_ids = {page["page_id"] for page in packs["validation_risk_pack"]}
    assert "recipe-debug-training-rollout-mismatch" in generic_ids
    assert "observability-training-inference-mismatch" in generic_ids
    assert "observability-debug-playbook" in generic_ids
    assert "validation-logprob-consistency" in validation_ids
    assert "failure-sample-schema-drift" in validation_ids
    assert "failure-stale-policy-training" in validation_ids


def test_render_task_bundle_refuses_non_empty_workspace(tmp_path):
    out = tmp_path / "task"
    first = render(out)
    assert first.returncode == 0, first.stdout + first.stderr
    sentinel = '{"id":"review-sentinel","round_id":"round-001","severity":"P0","status":"open","summary":"do not delete"}\n'
    (out / "review_issues.jsonl").write_text(sentinel)

    second = render(out)
    assert second.returncode == 1
    assert "refusing to render into non-empty workspace" in second.stdout
    assert (out / "review_issues.jsonl").read_text() == sentinel

    before_goal_versions = (out / "goal_versions.jsonl").read_text()
    before_progress = (out / "progress_log.md").read_text()
    forced = render(out, "--force")
    assert forced.returncode == 0, forced.stdout + forced.stderr
    assert (out / "review_issues.jsonl").read_text() == sentinel
    assert (out / "goal_versions.jsonl").read_text() == before_goal_versions
    assert (out / "progress_log.md").read_text() == before_progress

    reset = render(out, "--force", "--reset-ledgers")
    assert reset.returncode == 0, reset.stdout + reset.stderr
    assert (out / "review_issues.jsonl").read_text() == ""


def test_render_task_bundle_force_flag_guards(tmp_path):
    out = tmp_path / "task"
    result = render(out)
    assert result.returncode == 0, result.stdout + result.stderr
    sentinel = '{"id":"review-sentinel","round_id":"round-001","severity":"P0","status":"open","summary":"do not delete"}\n'
    (out / "review_issues.jsonl").write_text(sentinel)
    (out / "docs" / "goal.md").write_text("custom goal\n")

    reset_without_force = render(out, "--reset-ledgers")
    assert reset_without_force.returncode == 1
    assert "ERROR: --reset-ledgers requires --force" in reset_without_force.stdout
    assert (out / "review_issues.jsonl").read_text() == sentinel

    overwrite_without_force = render(out, "--overwrite-human-docs")
    assert overwrite_without_force.returncode == 1
    assert "ERROR: --overwrite-human-docs requires --force" in overwrite_without_force.stdout
    assert (out / "docs" / "goal.md").read_text() == "custom goal\n"

    overwrite = render(out, "--force", "--overwrite-human-docs")
    assert overwrite.returncode == 0, overwrite.stdout + overwrite.stderr
    assert (out / "docs" / "goal.md").read_text() != "custom goal\n"
    assert (out / "review_issues.jsonl").read_text() == sentinel


def test_render_task_bundle_force_preserves_all_scaffolded_docs(tmp_path):
    out = tmp_path / "task"
    result = render(out)
    assert result.returncode == 0, result.stdout + result.stderr
    custom = {}
    for name in SCAFFOLDED_DOCS:
        text = f"# Custom {name}\n\nSubstantive content for {name}.\n"
        custom[name] = text
        (out / "docs" / name).write_text(text)

    forced = render(out, "--force")
    assert forced.returncode == 0, forced.stdout + forced.stderr
    for name, text in custom.items():
        assert (out / "docs" / name).read_text() == text

    overwritten = render(out, "--force", "--overwrite-human-docs")
    assert overwritten.returncode == 0, overwritten.stdout + overwritten.stderr
    for name, text in custom.items():
        assert (out / "docs" / name).read_text() != text


def test_render_task_bundle_records_contract_amendments_only(tmp_path):
    out = tmp_path / "task"
    result = render(out)
    assert result.returncode == 0, result.stdout + result.stderr
    contract = out / "contract-copy.yaml"
    contract.write_text((ROOT / "examples/task_contracts/slime-weight-sync.yaml").read_text() + "\n# amendment\n")
    amended = subprocess.run([
        sys.executable, str(ROOT / "scripts/render_task_bundle.py"),
        "--contract", str(contract),
        "--output", str(out),
        "--force",
    ], cwd=ROOT, text=True, capture_output=True)
    assert amended.returncode == 0, amended.stdout + amended.stderr
    rows = [json.loads(line) for line in (out / "goal_versions.jsonl").read_text().splitlines()]
    assert len(rows) == 2
    assert rows[0]["contract_hash"] != rows[1]["contract_hash"]
    assert "contract amended -> workspace re-rendered" in (out / "progress_log.md").read_text()


def test_render_task_bundle_empty_goal_versions_is_fresh_history(tmp_path):
    out = tmp_path / "task"
    result = render(out)
    assert result.returncode == 0, result.stdout + result.stderr
    (out / "goal_versions.jsonl").write_text("")
    before_progress = (out / "progress_log.md").read_text()

    forced = render(out, "--force")
    assert forced.returncode == 0, forced.stdout + forced.stderr
    rows = [json.loads(line) for line in (out / "goal_versions.jsonl").read_text().splitlines()]
    assert len(rows) == 1
    progress = (out / "progress_log.md").read_text()
    assert "contract amended -> workspace re-rendered" not in progress
    assert progress.count("workspace rendered from `slime-weight-sync.yaml`") == before_progress.count("workspace rendered from `slime-weight-sync.yaml`") + 1


def test_render_task_bundle_preserves_goal_updates_on_force(tmp_path):
    out = tmp_path / "task"
    result = render(out)
    assert result.returncode == 0, result.stdout + result.stderr
    update = subprocess.run([
        sys.executable, str(ROOT / "scripts/append_goal_update.py"),
        "--workspace", str(out),
        "--status", "needs-amendment",
        "--reason", "scope changed",
        "--approved-by", "human",
    ], cwd=ROOT, text=True, capture_output=True)
    assert update.returncode == 0, update.stdout + update.stderr
    before = [json.loads(line) for line in (out / "goal_versions.jsonl").read_text().splitlines()]
    assert len(before) == 2
    assert before[1]["status"] == "needs-amendment"

    forced = render(out, "--force")
    assert forced.returncode == 0, forced.stdout + forced.stderr
    after = [json.loads(line) for line in (out / "goal_versions.jsonl").read_text().splitlines()]
    assert after == before


def test_render_task_bundle_detects_metrics_header_drift(tmp_path):
    out = tmp_path / "task"
    result = render(out)
    assert result.returncode == 0, result.stdout + result.stderr
    (out / "metrics.csv").write_text("timestamp,metric,value\n")

    forced = render(out, "--force")
    assert forced.returncode == 1
    assert "metrics.csv header mismatch" in forced.stderr
    assert (out / "metrics.csv").read_text() == "timestamp,metric,value\n"
