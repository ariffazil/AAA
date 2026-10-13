# LLM Wiki Pattern — Federation Memory Convention

> **Verdict:** ADOPT AS INSTITUTIONAL MEMORY CONVENTION
> **Source:** gist.github.com/karpathy/442a6bf555914893e9891c11519de94f (49,227★, Apr 2026) — Level 5 DATA
> **Staged raw:** /root/forge_work/gist-ingest-2026-10-08/PROVENANCE-llm-wiki.md
> **Compiled:** 2026-10-08 · 333-AGI · session SEAL-b117b112a28d411d

## The pattern (Karpathy)

Three layers, three operations:

| Layer | Who writes | What |
|---|---|---|
| raw/ | Human | Immutable sources (papers, notes, receipts) |
| wiki/ | Agent | Compiled, revisable synthesis, cross-linked |
| schema | Co-evolved | AGENTS.md-style conventions for the wiki itself |

Operations: **ingest** (source → summary + entity pages + index + log entry), **query** (index-first, then drill), **lint** (contradictions, stale claims, orphans).

## arifOS mapping (already half-built)

| Karpathy layer | Federation SOT |
|---|---|
| raw/ (immutable) | **VAULT999** append-only + /root/forge_work staging |
| wiki/ (agent-maintained) | **/root/AAA/knowledge** (this tree) |
| schema | /root/AGENTS.md + rendered instruction fragments |
| index.md | /root/AAA/knowledge/index.md (navigation-first query) |
| log.md | /root/AAA/knowledge/log.md (append-only chronology, grep-parseable) |
| query-time RAG re-derivation | arif_memory recall — used only when index is insufficient |

## Governance guards (hardening deltas)

1. **No silent class promotion** — a wiki page (DER/INT) never becomes evidence (OBS). Provenance back-link mandatory: every wiki page cites its raw/ or VAULT999 receipt id.
2. **Lint = existing verbs, no new tools:** `arif_memory(mode="audit")` + seal-ceremony drift flag generalize the wiki lint. No new cron (event-driven law).
3. **Human memory lane stays untouched** — /root/memory (H1-H6) is sovereign-owned; this convention applies to the institutional tree only.
4. Write-back: query results that are reusable get filed back as pages — exploration compounds.
