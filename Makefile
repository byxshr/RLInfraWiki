.PHONY: setup validate indices verify-source-refs verify-source-drift refresh-source-report check status demo context test

PYTHON ?= python
CONTEXT ?= /tmp/rlinfra-context-bundle.md
SOURCE_ROOT ?= ..
SOURCE_REFRESH_REPORT ?= /tmp/rlinfrawiki-source-refresh-report.md

setup:
	$(PYTHON) -m pip install -e ".[dev]"

validate:
	$(PYTHON) scripts/validate.py

verify-source-refs:
	$(PYTHON) scripts/verify_source_refs.py

verify-source-drift:
	$(PYTHON) scripts/verify_source_refs.py --check-local --source-root $(SOURCE_ROOT)

refresh-source-report:
	$(PYTHON) scripts/refresh_sources.py --dry-run --source-root $(SOURCE_ROOT) --markdown-output $(SOURCE_REFRESH_REPORT)

indices:
	$(PYTHON) scripts/generate_indices.py

status:
	$(PYTHON) scripts/repo_status.py

context:
	$(PYTHON) scripts/compose_context.py \
	  --target-framework verl \
	  --task "add SGLang rollout backend with weight sync" \
	  --mode design \
	  --output $(CONTEXT)
	$(PYTHON) scripts/validate_context_bundle.py $(CONTEXT)

demo:
	$(PYTHON) scripts/query.py "Megatron SGLang weight sync" --limit 8
	$(PYTHON) scripts/compose_context.py \
	  --target-framework slime \
	  --task "design weight sync between Megatron training and SGLang rollout" \
	  --mode design \
	  --output $(CONTEXT)
	$(PYTHON) scripts/validate_context_bundle.py $(CONTEXT)

test:
	pytest -q

check:
	$(PYTHON) scripts/verify_source_refs.py
	$(PYTHON) scripts/validate.py
	$(PYTHON) scripts/generate_indices.py --check
	$(PYTHON) scripts/repo_status.py
	pytest -q
