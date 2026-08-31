# Agent–Governance–Machine Checklist — Federation Audit

> **Reference:** ARIFOS::M365_COPILOT_KERNEL::v1.1 · Phase 2 DOCUMENT_ONLY
> **Authority:** ARIF (F13 SOVEREIGN). **Prepared by:** 333-AGI (FI-001).
> **Date:** 2026-08-31 (UTC). **Status:** REVIEW — not committed, not deployed.
> **Purpose:** Audit taxonomy over existing federation components. This is NOT an
> implementation spec. Governing principle (ARIF, 2026-08-31): *measure only signals
> capable of changing a verdict, intervention, or learning state — everything else is
> telemetry noise.*
> **Terminology note:** the working label "ANC" is VOID. Do not preserve or propagate it.

---

## 1. Status legend

| Status | Meaning |
|---|---|
| PRESENT | Component exists and is live/verifiable, evidence path attached |
| FRAGMENTED | Capability exists but scattered across ≥2 places or with coverage gaps |
| DOCTRINE_ONLY | Stated as rule/skill text, not computed anywhere |
| MISSING | No component exists |
| UNKNOWN | Insufficient evidence to classify |

## 2. The 32-point audit table

### A. Authority and identity

| # | Point | Status | Component + Evidence path |
|---|---|---|---|
| 1 | Sovereign identity | PRESENT | arifOS SCT session tokens with auth band (`arif_init`, kernel :8088); sovereign signal doctrine — `/root/AGENTS.md` ("Sovereign signals, channel-bound"); verified live: SCT in this session carried allowed-verb list |
| 2 | Actor identity | PRESENT | AAA registry `/root/AAA/agents/*/identity.json` + `identity.key` (hermes-asi, openclaw verified live 2026-08-31); FlowReceipt `actor_id` field — `http://127.0.0.1:7073/health` |
| 3 | Delegation scope | PRESENT | SCT auth band (identity_valid ∧ capability ∧ scope ∧ lease); skill `/root/.agents/skills/FORGE-sct-federation-ingress/SKILL.md` (65-case matrix) |
| 4 | Separation of powers | DOCTRINE_ONLY | Trinity 333/555/888 split; doer≠judge in `/root/.agents/skills/domains/apex/arifos-constitutional-judge/SKILL.md`. `power_conflict` NOT computed → deferred (§6.1) |

### B. Intent and reality

| # | Point | Status | Component + Evidence path |
|---|---|---|---|
| 5 | Canonical intent | PRESENT | `arif_init` session binding; `aaa_measure.objective` (required field) |
| 6 | Reality baseline | PRESENT | Pre-mutation baseline practice (M1 report 2026-08-31: unit/port/deps/side-units); `/root/.local/share/arifos/carry_forward.json` |
| 7 | Evidence provenance | PRESENT | OBS/DER/INT/SPEC labels — `/root/AAA/instructions/constitution.md` (F2); skill `/root/.agents/skills/.profile-archive/governance/claim-receipt-discipline/SKILL.md`; FlowReceipt `provenance.formula_hash` |
| 8 | Uncertainty | PRESENT | F7 HUMILITY Ω₀ ∈ [0.03,0.05] cap — `/root/AAA/instructions/constitution.md`; `aaa_measure.failureClass=ambiguous` |
| 9 | Contradiction | FRAGMENTED | `geox_contradiction_scan` exists (GEOX domain only, :8081); failureClass ambiguous elsewhere. No general cross-organ contradiction counter |

### C. Decision and governance

| # | Point | Status | Component + Evidence path |
|---|---|---|---|
| 10 | Risk & reversibility | PRESENT | Autonomy tiers T0–T3 — `/root/AAA/instructions/autonomy.md`, `/root/AAA/agents/opencode/DOCTRINE.md` §2 (ordinal bands, no fake precision) |
| 11 | Policy evaluation | PRESENT | F1–F13 enforced by kernel (live: `floors_active: 13`, verdict SEAL, 2026-08-31 probe :8088); skill `apex-gate-evaluator` |
| 12 | Verdict model | PRESENT (gap) | UNKNOWN/SABAR/HOLD/VOID/SEAL live in kernel judge + response contracts; **PARTIAL absent** from official enum → consolidation C4 |
| 13 | Decision receipt | PRESENT | `aaa_measure` (hypotheses/evidence/action/verification); VAULT999 chain `/root/.local/share/arifos/vault999/seal_chain.jsonl`; FlowReceipt `previous_receipt_hash` chaining |

### D. Agent behaviour

| # | Point | Status | Component + Evidence path |
|---|---|---|---|
| 14 | Trajectory trace | FRAGMENTED | arifFlow per-step receipts (:7073) + Kabarkan observability plane (skill `/root/.agents/skills/.profile-archive/federation/kabarkan-observability/SKILL.md`); not all agents emit Kabarkan spans |
| 15 | Tool use | PRESENT | SCT ingress gates per organ (FORGE-sct-federation-ingress); MCP governance middleware (GEOX AUTH_MW observed live in journal 2026-08-31) |
| 16 | Delegation/handoffs | PRESENT | A2A gateway :3001 (live: 7 agents discovered 2026-08-31, `aaa_dispatch_a2a` taskId/reply); skill `FORGE-cross-agent-handoff` |
| 17 | Loop behaviour | PRESENT | arifFlow per-actor `consecutive_exec_no_verify` + EXECUTION DOMINANCE + throttled/held (observed live 2026-08-31); Calhoun Lock Q10 doctrine |
| 18 | Claim grounding | PRESENT | Skills: `claim-receipt-discipline`, `ASI-fabrication-prevention`, `AUDIT-repo-reality` |
| 19 | Outcome correctness | PRESENT | Verification-as-terminal-state — `/root/.agents/skills/domains/forge/verify-work/SKILL.md`; M1 acceptance 5/5 PASS with independent verifier lane (2026-08-31) |

### E. Machine and execution

| # | Point | Status | Component + Evidence path |
|---|---|---|---|
| 20 | Precondition state | PRESENT | Tool pre-flight — `/root/AAA/agents/opencode/DOMAIN.md` §11; M1 precondition check 5/5 |
| 21 | Exact mutation | PRESENT | A-FORGE governed execution :7071 (EXECUTE_AFTER_SEAL); M1 side-effect diff pattern |
| 22 | Execution result | PRESENT | FlowReceipt `payload.result`/errors; systemd journal evidence |
| 23 | Rollback viability | FRAGMENTED | Rollback documented per action (M1: `systemctl stop` restore path); `rollback_tested` rarely true — doctrine strong, tested-rollback rare |
| 24 | Resource boundary | PRESENT | Token bank `/root/.local/share/arifos/token_bank.db`; FED :7074 `providers[].balance_usd`; paid-API gate — `/root/.config/opencode/rules/arifos-governance.md` |
| 25 | Security boundary | PRESENT | F12 INJECTION floor; localhost-binding doctrine `/root/docs/LOCALHOST_IS_*.md`; skills `FORGE-secret-hygiene`, `FORGE-telegram-audit` |
| 26 | Postcondition verification | PRESENT | Closed loop demonstrated: receipts `0bc705cd` (Execute) + `25fbcbe5` (Verify, independent) + `2ecb7239` (stability re-check) — all 2026-08-31; skill `verify-gate` |

### F. Metabolism and learning

| # | Point | Status | Component + Evidence path |
|---|---|---|---|
| 27 | Receipt completeness | FRAGMENTED | Mechanism live (1000 receipts, :7073) but per_actor = [333-AGI, qwen-code] only — edge agents (hermes-asi, openclaw) do not ingest (verified live 2026-08-31) |
| 28 | FQ equilibrium | PRESENT | Live FQ daemon :7073 (observed 0.517→0.667→0.538, verdict FLOWING, per-actor holds); formula `sha256:arifflow-fq-v2.2` |
| 29 | Decision-changing value | DOCTRINE_ONLY | Principle stated by ARIF 2026-08-31; not encoded → deferred (§6.2) |
| 30 | Memory promotion | PRESENT | Skills: `AGI-dream-engine`, `wisdom-scar-session-audit`, `memory-manage`; `eureka-entries.jsonl`; VAULT999 (LEDGER/SCAR tier) |
| 31 | Entropy receipt | DOCTRINE_ONLY | ΔS ≤ 0 in response contract (per-output claim); `forge entropy sweep` for files exists; per-receipt investment/maintenance/extraction NOT computed → deferred (§6.3) |
| 32 | Owner & corrective action | PRESENT | `carry_forward.json` open_loops with closure state; skills `incident-response`, `RSI-federation-mesh` |

## 3. Tally

**PRESENT 25 · FRAGMENTED 4 (#9, #14, #23, #27) · DOCTRINE_ONLY 3 (#4, #29, #31) · MISSING 0 · UNKNOWN 0.**

Component coverage including fragmented: 29/32. Prior claim "29/32 exist" is hereby evidenced: 25 clean + 4 fragmented.

## 4. Five consolidation proposals (C1–C5)

| ID | Proposal | What merges | What it kills | Rollback boundary |
|---|---|---|---|---|
| C1 | Ledger consolidation | arifFlow :7073 = sole metabolism ledger (every step); VAULT999 = irreversible seals only | HERMES `attestation-ledger.jsonl` writes; OpenClaw `delta-log.jsonl` (1 line since April) | Re-enable old logs; nothing deleted |
| C2 | Canonical identity registry | ONE registry source; AAA discovery + agent-cards render from it (extend existing `render-agents.sh` pattern) | Drift class: GEOX `live:false` vs healthy :8081; hermes-asi/openclaw absent from discovery (verified 2026-08-31) | Restore previous registry file |
| C3 | Scheduler consolidation | All scheduled work → systemd timers; every job ends with one `curl :7073/ingest` | Scattered: root crontab, HERMES jobs.json, dead OpenClaw cron (last run Aug 5) | `systemctl disable --now` per timer |
| C4 | Two-level verdict contract | Step-level floor verdicts (Pass/Caution/Hold/Void) stay; action-level verdicts unify as UNKNOWN/SABAR/HOLD/**PARTIAL**/VOID/SEAL | PARTIAL gap; verdict vocabulary drift | Contract doc revert |
| C5 | Five-measure dashboard | Authority integrity · Reality fidelity · Boundary integrity · Outcome validity · Metabolic health — all derived from existing ledgers | Vanity dashboards | Delete dashboard view only |

## 5. Explicit non-goals (binding until ARIF changes them)

- **No new organ.** Zero new services, ports, registries, or acronyms.
- **No migration yet.** C1–C5 are proposals; no data has moved.
- **No deletion.** Dead channels archived at most, never removed, until separately authorized.
- **M2–M5 remain unauthorized.** (M1 executed+sealed 2026-08-31: receipts `0bc705cd`, `25fbcbe5`, `2ecb7239`.)

## 6. Deferred computations (T1.5 — proposals only, do not build)

1. **power_conflict** — one field in `aaa_measure`: `proposer==authorizer OR verifier==mutator OR judge==executor` → HOLD/VOID. Rationale: only genuinely verdict-changing computation of the three.
2. **measurement_value gate** — rule text: measure only what can change verdict/intervention/causality/policy. Encode as governance rule, not code.
3. **entropy classification** — per-receipt investment/maintenance/extraction. Lowest priority; ΔS currently claim-based.

## 7. Future merge sequence (each step separately authorized, one at a time)

```
S1  M2 (GEOX registry URL fix)          → acceptance: discovery geox live:true
S2  M3 (register hermes-asi + openclaw) → acceptance: discovery count 7→9, both live:true
S3  M5 (hermes-gateway-api decision)    → acceptance: enabled-state matches ARIF choice
S4  C2 identity registry consolidation  → acceptance: discovery == registry, zero drift
S5  C3 scheduler consolidation + M4     → acceptance: timer fires, "openclaw" appears in :7073 per_actor
S6  C1 ledger consolidation             → acceptance: no new writes to attestation/delta logs
S7  C4 verdict contract + C5 dashboard  → acceptance: five measures render from existing ledgers
```

Rollback boundary per step: single command or file restore (§4 column). One SEAL per step. Side-effect diff mandatory after each.

## 8. Provenance

- Audit session receipts: `1c431b67` (audit verify) · `0bc705cd` (M1 execute) · `25fbcbe5` (M1 verify, independent) · `2ecb7239` (stability re-check) — all arifFlow, 2026-08-31.
- Evidence paths marked "verified live" were probed in-session; others are canonical registry paths pending open.
- Uncertainty: #12 verdict-model internals (SABAR/PARTIAL presence in kernel enum) inferred from skill docs + response contracts, not read from kernel source — treat as high-confidence DER, not OBS.
