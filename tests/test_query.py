import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_query_finds_sglang_rollout():
    result = subprocess.run([sys.executable, str(ROOT / "scripts/query.py"), "SGLang rollout", "--limit", "3"], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert "sglang" in result.stdout.lower()


def test_query_finds_rollout_backend_selection_dictionary_pages():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/query.py"),
            "rollout backend selection SGLang vLLM cache logprob weight update",
            "--limit",
            "8",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert "capability-rollout-backend-selection" in result.stdout
    assert "comparisons-rollout-backends" in result.stdout


def test_query_finds_training_rollout_mismatch_debug_pages():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/query.py"),
            "training rollout mismatch logprob policy_version cache schema drift",
            "--limit",
            "8",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert "recipe-debug-training-rollout-mismatch" in result.stdout
    assert "observability-training-inference-mismatch" in result.stdout
