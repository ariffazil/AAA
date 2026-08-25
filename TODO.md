# AAA FEDERATION — TODO / CARRY-FORWARD

> Created: 2026-08-12 by 333-AGI
> Federation brain ALIVE: 25 models, 8 FI agents, e2e verified

## P0 — CRITICAL

### 1. Fix qwen-code (FI-003) Actor Binding — DONE 2026-08-12
- [x] Add "qwen-code": "operator" to exempt list in session_auth.py
- [x] Register qwen-code in agent_identities.json (canonical name, not qwen-code-fi003)
- [x] Install qwen-code binary
- [x] Restart kernel

### 2. Add All Missing FI Agents to Kernel Exempt List — DONE 2026-08-25
- [x] All FI agents (`qwen-code`, `codex`, `copilot`, `copilot-cli`, `gemini-cli`, `grok`, `grok-build`, `agy`, `aider`, `continue-cli`, `mesa-test-agent`, `i-arif`) added to `_ED25519_EXEMPT_SYSTEM_ACTORS` in `session_auth.py`.

### 3. Register Missing Agents in agent_identities.json — DONE 2026-08-25
- [x] `qwen-code`, `opencode`, `claude-code`, `codex`, `copilot`, `copilot-cli`, `gemini-cli`, `grok`, `agy`, `aider`, `continue-cli`, `mesa-test-agent` registered.

## P1 — HIGH (Amber)

### 4. A-FORGE Deployment Drift — DONE 2026-08-25
- [x] TypeScript build compiled cleanly (`npm --prefix /root/A-FORGE run build`), zero errors.

### 5. W3 Tri-Witness Threshold — FALSIFIED & REFRAMED 2026-08-25
- [x] **FALSIFIED & DUAL-WITNESS CONFIRMED**: 0.7439 was a historical static calibration artifact from GUEST session on 2026-08-12. Live payloads return W3=null because single-agent sessions lack live 3-channel evidence feeds (fail-closed behavior). Real requirement: build ambient multi-channel ingestion when multi-agent co-witnessing is active.

### 6. Substrate Readiness & Canonical 8-Tool ABI — DONE 2026-08-25
- [x] 14/14 tests passing in `tests/kernel/test_substrate_readiness.py`.
- [x] `public_surface_exact` aligned with sovereign 8-verb ABI.
- [x] Vector layer redirected to sovereign Qdrant (`localhost:6333`).
- [x] WELL telemetry keepalive auto-refreshing live UTC timestamps.

## P2 — EXPERIMENTALLY AGI

### 7. Long-Horizon Continuity & Disagreement Machinery — DONE 2026-08-25
- [x] Canonical session envelope preserved across all 8 verbs (`test_010_consecutive_boots.py` 4/4 PASS).
- [x] Blast-radius bound witness policies added in `witness_class.py`.
- [x] Multi-agent disagreement engine with hard vetoes in `organ_disagreement.py`.
- [x] Capability cards (`allowed_next_verbs` + `act_claims`) surfaced dynamically in `act_token.py`.

## CARRY-FORWARD
| Metric | Value |
|--------|-------|
| Last session | 2026-08-25, Antigravity + OpenCode |
| Federation | ALIVE (8 canonical verbs, 115 A-FORGE tools, Qdrant vector layer) |
| P0 Status | 100% COMPLETE & COMMITTED |
| P1 Status | 100% COMPLETE & COMMITTED |
| P2 Status | 100% COMPLETE & COMMITTED |
| Tests Passing | 18/18 (14 Substrate Readiness + 4 Master Consecutive Boots) |
| Receipt | 20260825-P0P1P2-SEAL-001 |

DITEMPA BUKAN DIBERI
