# AAA Federation Implementation Charter — Phases 0–4
# Status: DRAFT — awaiting sovereign ratification of doctrine (Phase 0)
# Authored: 2026-08-07 | Source: sovereign directive (this session)
# Path: /root/AAA/federation/implementation/IMPLEMENTATION_CHARTER_2026-08-07.md

This charter operationalizes the 24 EUREKAs into 9 specific actions across 5 phases. Each action maps to one or more EUREKAs and is owned by a specific agent. Order respects **E-21**: doctrine → protocol → implementation → tool. Phase 0 is the gate; no protocol work without ratified doctrine.

---

## Phase 0 — Ratify Doctrine (E-21)

**Action 0**: Ratify + seal doctrine  
**Owner**: F13 (sovereign) + 888-APEX (judge)  
**EUREKA**: E-21 (Constitution → Protocol → Implementation)  
**Reversible**: — (constitutional act)  
**Deliverable**: `AAA_EUREKA_DOCTRINE_v1.md` ratified via 888 verdict, sealed to VAULT999. Each EUREKA becomes a permanent reference number (E-01…E-24) so future receipts can cite "violates E-03" rather than "feels wrong."  
**Outcome**: Doctrine becomes canonical; protocols may derive.

**Why Phase 0 is the gate**: Implementation-before-constitution violates E-21 itself. No protocol work without ratified doctrine.

---

## Phase 1 — Enforcement (E-11, E-12, E-22)

### Action 1a: Audit `arifos-judge-gate.ts`

**Owner**: Hermes (delegation — no vested interest in OpenCode runtime)  
**EUREKA**: E-11 (runtime > memory), E-22 (final AAA test)  
**Reversible**: yes (audit is observational)  
**Scope**:
- Coverage test of irreversible actions
- Fail-closed when the hook itself fails
- Who can disable it and how the disablement is recorded

**Deliverable**: Verdict + gap list.

### Action 1b: E-22 test × 3 harnesses

**Owner**: All 3 primaries (333-AGI, af-forge, Hermes)  
**EUREKA**: E-22  
**Reversible**: yes (test)  
**Deliverable**: 3-row scorecard — one row per harness: *"Can the runtime violate the constitution without leaving a receipt? YES/NO + evidence."*  
**Outcome**: Real federation state, not theory. Any YES becomes Phase 1c work.

---

## Phase 2 — Protocol (E-01, E-03, E-05, E-06, E-07)

### Action 2a: No-nesting contract (federation rule, written)

**Owner**: 333-AGI (OpenCode primary — most nesting-risk-exposed)  
**EUREKA**: E-05, E-06  
**Reversible**: yes  
**Deliverable**: Contract paragraph at `/root/AAA/contracts/no_nesting_protocol_v0.1.yaml`:

> *spawn depth ≤ 1; tujuan: preserve verification capacity (E-06), bukan anti-loop.*

### Action 2b: Spawn-cost logging instrument

**Owner**: 3 primaries  
**EUREKA**: E-03, E-04  
**Reversible**: yes  
**Deliverable**: Log `expected_entropy_reduction` vs `expected_debt` per spawn. Witness fields in observation schema.  
**Outcome**: After 2 sessions → threshold can be derived. **No rule until data.** Paper law prohibited.

### Action 2c: Chain-length metric

**Owner**: Kimi Code  
**EUREKA**: E-07 (real Dunbar boundary)  
**Reversible**: yes  
**Deliverable**: `max_receipt_chain_length` per session as observable metric.  
**Outcome**: Answers "how long can the chain be and still be verified end-to-end?" with data, not theory.

---

## Phase 3 — Capability (E-12, E-18)

### Action 3a: Don't → Cannot × 3 critical cases

**Owner**: af-forge (Kimi) + 333-AGI (OpenCode)  
**EUREKA**: E-01, E-12  
**Reversible**: yes (verification)  
**Cases**:
1. Subagent cannot spawn (already: `max_spawn_depth=1`; verify enforced in all 3, not config-only)
2. Subagent cannot seal directly to VAULT without primary witness (E-01: authority stays; seal = authority act)
3. Subagent cannot mutate observation schema (instrument integrity)

**Deliverable**: YES/NO + evidence per capability per harness.

---

## Phase 4 — Identity & Records (E-17, E-18, E-19, E-20)

### Action 4a: FEDERATION_STATE registry

**Owner**: AAA  
**EUREKA**: E-18, E-20  
**Reversible**: yes (mutable only via receipt)  
**Deliverable**: `/root/AAA/FEDERATION_STATE.md` — per organ: identity, capability surface (MCP), routing, enforcement, E-01–E-24 checklist status. Updates only via receipt, not free edit.  
**Outcome**: "AAA federation state level" becomes an **object**, not an idea.

### Action 4b: Failure class tagging

**Owner**: All agents  
**EUREKA**: E-19 (infra ≠ governance)  
**Reversible**: yes  
**Deliverable**: Every failure receipt tagged `class: infrastructure | governance`. Vault-down no longer reads as constitutional breach — and vice versa.

---

## What NOT to do now

- **E-15 / E-16 (productive disagreement)**: sifat, bukan mechanism. Emerges from E-01 enforcement. Don't codify; observe in notes field.
- **Spawn pricing as rule**: wait for Phase 2b data. **Paper law prohibited.**
- **Aggregate dashboards (E-08)**: last. After per-spawn audit stable.

---

## Summary Table

| Phase | Action | Owner | EUREKA | Reversible |
|---|---|---|---|---|
| 0 | Ratify + seal doctrine | F13 + 888 | E-21 | — |
| 1a | Audit `judge-gate.ts` | Hermes | E-11, E-22 | ✅ |
| 1b | E-22 test × 3 harnesses | All primaries | E-22 | ✅ |
| 2a | No-nesting contract | 333-AGI | E-05, E-06 | ✅ |
| 2b | Spawn-cost logging | 3 primaries | E-03, E-04 | ✅ |
| 2c | Chain-length metric | Kimi Code | E-07 | ✅ |
| 3a | Don't → Cannot × 3 | af-forge, 333 | E-01, E-12 | ✅ |
| 4a | FEDERATION_STATE registry | AAA | E-18, E-20 | ✅ |
| 4b | Failure class tagging | All | E-19 | ✅ |

**9 actions. 8 reversible. 1 ratification. Order respects E-21.**

---

DITEMPA BUKAN DIBERI. Charter forged; awaiting sovereign ratification to seal.