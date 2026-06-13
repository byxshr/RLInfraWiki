# RLInfraWiki Agent Instructions

RLInfraWiki is a standalone source-traceable RL infrastructure dictionary. The repository root is the skill root.

For design, adaptation, or debug tasks:

1. Generate a context bundle before drafting a solution.
2. Validate the bundle.
3. Read pages from all four packs with `get_page.py --follow-sources`.
4. Cite page IDs, source IDs, confidence, version sensitivity, and known gaps.

Never produce target-framework-only designs for known frameworks. Do not mark source-reported upstream behavior as locally verified unless this repository contains command, hardware/context, log/artifact, and result evidence.

Local clones are ingestion backends only. Long-lived wiki evidence must use source IDs, repo IDs, commit IDs, paths, line ranges, hashes, claim IDs, and provenance metadata.
