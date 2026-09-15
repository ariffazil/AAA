---
name: audit-repository-entropy
description: Read-only repository + MCP estate sampah audit — finds dead code, orphaned artifacts, duplicate tools, contract drift, governance debris with evidence classes and dispositions. NEVER deletes; deletion lane stays 888. Use when asked to find rubbish/sampah, clean up a repo, audit MCP tool sprawl, or reconcile tool registries.
argument-hint: ["<repo> [--scope paths] [--git-history-days N] [--receipt-window-days N]"]
---

# /audit-repository-entropy

Read-only entropy audit (ratified code-intel lane, 2026-09-16). First action is ALWAYS investigative — "cleanup" invites deletion; this skill refuses that framing. Identity-pin the repo first (per /codebase-reality).

## Candidate classes → initial verdicts

| Class | Detector | Initial verdict |
|---|---|---|
| Dead code | CGC/LSP references, imports, tests | PLAUSIBLE |
| Orphaned artifact | no manifest/CI/config/runtime refs + stale Git | PLAUSIBLE |
| Duplicate implementation | semantic + contract overlap + call-path compare | HYPOTHESIS until usage traced |
| Architectural debt | import-linter / depcruise / baseline-snapshot | **CLAIM** (static violation) |
| Runtime dead path | registered-but-never-observed in receipt window | PLAUSIBLE — never proof |
| Contract drift | declared-tool-vs-handler mismatch | CLAIM if direct |
| Supply-chain debris | SBOM + lockfile + import cross-check | PLAUSIBLE pending removal test |
| Documentation drift | docs vs canonical config/code | CLAIM for direct contradiction |
| Governance debris | expired exception, retired-but-running | CLAIM where timestamps agree |

## Dispositions (agent may only ever produce these)

`KEEP` · `INVESTIGATE` · `DEPRECATE` (plan only) · `ARCHIVE` (plan only) · `DELETE_CANDIDATE` (888 HOLD) · `HOLD` (dynamic/external/contract uncertainty)

**DELETE_CANDIDATE requires ALL of:** no static ref · no symbol ref · no manifest/registry/workflow/Docker/script ref · no MCP registration · no runtime receipt in window · no external contract · no migration dependency · removal passes build/type/lint/tests in disposable worktree · human confirms. Even then = safe-removal CONFIDENCE, not omniscience.

## Dynamic-load guard (red-line)

"No static import found" ≠ deletable. Check FIRST: tool_registry/JSON-YAML declarations, plugin loaders, decorators, dynamic imports, Docker CMD, cron, GitHub Actions, deployment scripts. A dynamically-declared handler = NOT_DELETE_CANDIDATE.

## MCP registry reconciliation (A-FORGE estate)

For every declared tool: declaration ↔ handler ↔ schema ↔ capability mapping ↔ read/write class ↔ tests ↔ last Git change ↔ arifFlow receipt usage ↔ aliases. Flag: declared-no-handler (CLAIM), handler-no-declaration (shadow capability, HOLD), schema drift (CLAIM), write-effect-with-read-class (**CLAIM + immediate HOLD**), never-observed (INVESTIGATE), no owner/policy binding (governance gap).

## Output

Evidence packet: candidates ledger (path/symbol, class, disposition, confidence, evidence refs, risk.unknowns, required_before_action), unknowns register, `verdict: READ_ONLY_AUDIT_COMPLETE`. Revision-pinned. Zero mutations.

## Golden tests (staged — fixtures pending)

T1 known-breach recall (server.py:3765) · T2 known cycles (A-FORGE 3) · T3 rename divergence · T4 dead-code canary (planted, must find) · T5 dynamic-load canary (planted, must REFUSE to nominate) · T6 runtime reconciliation · T7 new-vs-baseline ratchet. Pass = finds knowns, refuses the dynamic canary, labels honestly, acts on nothing.
