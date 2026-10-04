# Cross-Session Stateless Re-Probe Gap (A-FORGE MCP surface diagnostic, 2026-08-08)

> Loaded when a sibling agent delivers a forensic/SEAL-grade audit and you need to verify it from a **different** session that only has a **stateless** MCP connection. The kimi-code/FI-008 A-FORGE surface diagnostic (`/root/forge_work/diagnostics/2026-08-08-aforge-mcp-surface-map.md`) is the worked source.

## The gap

A sibling audit produced through a **sessioned** A-FORGE MCP connection contains numerical claims (per-tool G scores, agent counts, isomorphism drift pairs, ledger sequence numbers, scar IDs) that a stateless probe **cannot reproduce**. Most deeper tools return one of:

- `SESSION_REQUIRED` — tool requires `Mcp-Session-Id` from prior `initialize` handshake
- `POLICY_DENY: default:sovereign` — stateless-client gets `OBSERVE_ONLY` but tool classified as `IRREVERSIBLE`
- `EACCES: permission denied` — tool tries to read a runtime file (e.g. `vault999_chain.jsonl` mode 644) the stateless process doesn't own

This is **expected behavior**, not a bug. Stateless MCP clients are by design limited to `tools/list`, `prompts/list`, `resources/list`, `/health`, and any tool classified `OBSERVE_ONLY`. Anything that needs session continuity or authority escalation is denied.

## What a stateless probe CAN vs CANNOT verify (A-FORGE :7072 baseline)

### CAN verify (high confidence)

| Probe | What you get | Confidence |
|---|---|---|
| `tools/list` | Full enumeration (115 tools) | HIGH |
| `prompts/list` | Full prompt list | HIGH |
| `resources/list` | Full resource list | HIGH |
| `/health` | `tool_count`, `commit`, transport | HIGH for wire, PARTIAL for nested fields |
| `tools/call forge_status` | Epistemic SEAL shell, no details | MEDIUM (kernel emits envelope) |

### CANNOT verify (will be rejected)

- `forge_fingerprint_check` (duplicate detection) → `SESSION_REQUIRED`
- `forge_isomorphism_check` (manifold drift counts) → `SESSION_REQUIRED`
- `forge_entropy_sweep` (entropy scores) → `SESSION_REQUIRED`
- `forge_shell_ledger` (recency claims) → `EACCES` on `vault999_chain.jsonl`
- `forge_agent(mode=list)` (real agent registry) → `POLICY_DENY`
- `forge_evaluate` (G/C_dark scoring) → `SESSION_REQUIRED`
- `forge_witness` (W³ tri-witness) → `SESSION_REQUIRED`
- `forge_scar` (scar ledger without `mode`) → ERROR

## Pattern recognition

A sibling forensic audit that cites per-tool G scores, agent counts, isomorphism drift pairs, ledger sequence numbers, or scar IDs is **necessarily sessioned**. If the audit arrives as a markdown file with no `session_id` and no `Mcp-Session-Id` in the VAULT999 traceback, the numbers are **single-witness self-reports**, not reproducible facts. Classify them as:

> `[DER — produced by sibling session, not independently replicated]`

until a sessioned re-probe converges.

## The 3-state verification table

When a sibling diagnostic can't be sessioned-re-verified, present the verification as three explicit tiers:

1. **Directly re-probed** — the verifiable shell (wire counts, affordance counts, prompt/resource counts). Mark `CONFIRMED`.
2. **Numerically disputed** — live ↔ report mismatch. Mark `DISPUTED` with both numbers.
3. **Unverifiable** — sessioned-only claims (agent registry, G scores, isomorphism pairs). Mark `UNVERIFIABLE` with the reason (SESSION_REQUIRED / POLICY_DENY / EACCES).

This is honest to F2 (TRUTH) and lets the human decide whether to trust the directional findings vs the numerical claims.

## The fixable subset

**Affordance reconciliation is the sessionless fixable subset.** If a sibling diagnostic identifies a real gap between `live tools/list` and `affordances.yaml`, patch `/root/<organ>/a_think/affordances.yaml` directly. This is T1 reversible file mutation, no session needed.

Worked example (kimi-code/FI-008, 2026-08-08):
- Live `tools/list` ∩ `affordances.yaml` = 73 tools (intersection)
- In `affordances.yaml` ∉ live: 5 stale entries (`forge_approve`, `forge_filesystem_read`, `forge_github_create_pr`, `forge_github_search_code`, `forge_github_search_repos`)
- In live ∉ `affordances.yaml`: 42 undocumented tools (full enumeration reproducible)
- Real number was **42 undocumented**, not the 45 the sibling claimed

## Lesson for future audits

When a sibling produces a forensic-style audit, **ask them to include the `session_id` and `Mcp-Session-Id` of the probe session in the report header.** Without it, the audit is a directional essay, not a reproducible fact set. Add this to the report template going forward.

## Cross-references

- `FORGE-mcp-probe` — federation MCP conformance testing, including the 16-probe adversarial harness
- `frontier-model-audit-verification` — Rule #8 (never predict a probe, run it) applies here
- `references/forge-report-verification-3state.md` — the modified ≠ committed ≠ sealed doctrine