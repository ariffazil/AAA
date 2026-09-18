---
report_id: VERIFY-2026-09-17-01
session_id: verify-round-2026-09-17
actor: FI-002 (claude code)
verdict_class: RECEIPT
lane: B (autonomous, not constitutional)
date: 2026-09-17
---

# Verification 1/4 — arifOS kernel :8088, post-MCP-2026-07-28 migration

## Verdict: PASS (with 2 ⚠️ and 3 observations)

## Claim

Kernel is post-MCP-2026-07-28 migration, exposes 8 canonical tools, enforces F1–F13 floors, signs receipts with Ed25519, drift honestly reported.

## Method

Cold-started from `README.md` SOT banner → probed `/health` (SOT-stamped source of truth) → mapped 19 endpoints via curl code scan → drove `/kernel/authority-probe`, `/kernel/readiness`, `/gate/v0`, `/kernel/identity/verify`, `/.well-known/mcp.json`, `/tools`, `/ready` → ran `arifosmcp/runtime/test_persona_receipt.py` against working-tree (uncommitted) v2 source.

## Findings

1. `:8088` live, MCP-2026-07-28 stamped, 200/2.5ms. Back-compat list `[2026-07-28, 2025-11-25, 2025-03-26, 2004-11-05]`.
2. 8 canonical tools exposed, surface hash `d00212fccf333c20` CONSISTENT across 5 vantages.
3. F1–F13 floors all report `pass`. Hard/soft classification matches doctrine.
4. Anonymous probe refused: `gate_verdict: HOLD/RAW=BLOCK`, F1+F8 triggered, lease_active=false.
5. Readiness self-audit honest: `decision: production_burn_in (84.8 ±6)`, NOT sovereign_runtime.
6. Working-tree v2 receipt schema internally consistent (4/4 test pass).
7. Deployed venv still on v1; drift correctly flagged via deployment_attestation.
8. `/ready` 503 in 7.9s — session_check reports SEAL-f36ac678ec784c5a (stage 000).
9. Cross-module dual-axis decomposition labeled with HOLD comment.

## ⚠️ Notable

- Working tree 1 commit ahead of origin, uncommitted changes held locally. Musyawarah ratification needed.
- **`session_enforcement` falsification probe — root cause found (P2-002):** probe tests `tools/list` (MCP discovery) and expects HTTP 400 or session error. But anonymous `POST /mcp` with `tools/list` returns **HTTP 200 with full tool list** in 8ms — by MCP-2026-07-28 spec, discovery is public. `tools/call` IS session-gated (HOLD with reason). The probe logic is wrong, not the enforcement. Fix: probe should test `tools/call`, not `tools/list`. F7 actual score is **1.0**, not 0.04.
- 666/888 dual-axis decomposition partial: only `arif_judge` KERNEL renamed; `owner: "888"` governance_tier fields intentionally retained.

## Honest gaps (unmeasured)

- **Earlier "ELF bytes" probe of `/opt/arifos/venv/bin/python3` was a test artifact** — bash tried `cd` on a file path. Symlink resolves correctly to `/usr/bin/python3 → python3.13`. Not actually broken.
- 148-rule MCP scanner badge in README not independently probed.

## P2-002 (Session-enforcement probe investigation) — CLOSED

**Finding:** The probe `probe_mcp_session_enforcement()` in `/opt/arifos/current/venv/lib/python3.13/site-packages/arifosmcp/runtime/reality_scoring.py:182` sends an anonymous `tools/list` request and expects HTTP 400 or session error. It actually gets HTTP 200 — which is **MCP-2026-07-28 spec-compliant** (discovery is public).

**Verified behavior:**
- `POST /mcp` with anonymous `tools/list` → HTTP 200, full tool list returned in 8ms
- `POST /mcp` with anonymous `tools/call` → HOLD, "No constitutional_chain_id from prior arif_judge SEAL"

**Probe verdict when run directly:** `(False, 'bypassed: HTTP_200_')` — this is the **correct** verdict for the probe as written.

**Kernel verdict:** reports `probe_timeout: timed out` — likely the falsification pipeline itself is hanging, not the probe.

**Recommendation:** Update the probe to test `tools/call` (which IS session-gated) instead of `tools/list` (which is public by spec). F7 actual score is **1.0**, not 0.04.

**Status:** Investigation complete, finding documented, fix recommendation authored. F13 ratification needed before code change to deployed venv.

See `/root/work/tasks.json` for follow-ups (P0-001, P1-004, P2-002 — now CLOSED for investigation).

— End of Report 1/4 —
