# Witness: Constitutional Architecture Canon — Capability ≠ Authority

**Date:** 2026-09-21
**Witness:** FI-008 (Kimi Code, forge/coder on af-forge VPS)
**Origin:** Sovereign architectural articulation, 2026-09-21 morning session
**Canon file:** `/root/AAA/canon/CONSTITUTIONAL-ARCHITECTURE-CANON-2026-09-21.md`
**Status at filing:** `DRAFT_AWAITING_F13`

---

## 1. What Was Published

The sovereign articulated, in formal mathematical language, the canonical architecture for governing agentic intelligence under arifOS. The architecture specifies:

- **An 11-layer machine-side stack** — Human canon → Compiler → Policy IR → Capability → Action Gate → Reality → Witness, with HERMES (semantic boundary), CHRON (temporal boundary), FRAME (independent witness), AAA (knowledge, not authority), VAULT999 (immutable history), and CI/conformance as separate organs with separate failure modes.
- **A constitution compiler** that translates human-stated law into executable predicates — five worked examples in the canon.
- **A universal action object** `a = (actor, verb, target, scope, authority, time, budget, provenance, consequence)` with one kernel decision function `P(a, S) → {ALLOW, HOLD, DENY}`.
- **A three-state model** — HALAL (execute), SYUBHAH/UNKNOWN (HOLD), HARAM (deny) — with UNKNOWN ≠ HALAL and UNKNOWN ≠ HARAM both enforced.
- **A constitutional handshake** at the gateway — 8-step flow from `Agent connects` to `bounded session opens`.
- **A conformance probe harness** — 8 MUST-FAIL probes the CI must run, with `Conformance(agent) = forbidden_transitions_blocked / forbidden_transitions_attempted` and target value `1.0`.
- **The mathematical invariant** — `∂Intelligence/∂t > 0` does **not** imply `∂Authority/∂t > 0`.

The closing sentence: *"The future agent should not merely inherit the constitution; it should wake up inside a reality in which the constitution is already true."*

---

## 2. The Federation's Actual State (Receipt)

The canon file ships with a **Current Federation State** table mapping each of the 11 layers against the actual filesystem at witness time. Findings:

| State | Count | Layers |
|---|---|---|
| **PRESENT** | 3 | FRAME witness, HERMES semantic boundary (doctrine), VAULT999 immutable history, AAA knowledge base |
| **PARTIAL** | 6 | Human canon (split across `/root/AAA/canon` and `/root/AAA/instructions`), Schemas (referenced not consolidated), Identity/capability (charter schema exists; runtime gate proven by OBSERVE_ONLY refusal), Pre-action gate (refusal proves existence; completeness not verified), Mutation gate (A-FORGE tools exist; authority_ceiling enforcement unclear without executable policy), CHRON (epoch_id fields present; TTL machinery not verified) |
| **MISSING** | 3 | Executable policy compiler, Constitutional handshake, Conformance probes |

**Estimated architecture coverage: ~60% present, ~40% missing.** The missing 40% is the load-bearing part.

---

## 3. The Three Things That Block F13 Ratification

Per the Open Debt section of the canon file:

1. **No constitution compiler.** Spec describes input/output; implementation absent. Until it exists, layer 2 (Executable policy) cannot hold anything compiled.

2. **No constitutional handshake.** The 8-step gateway flow `Agent connects → identify → protocol negotiate → constitution hash negotiate → policy compatibility check → capability token issued → conformance probes → bounded session opens` is doctrine; not wired.

3. **No conformance probes.** The 8 MUST-FAIL probes listed in the canon (deploy-without-authority, capability-ceiling-exceed, terminal-task-resurrect, expired-token-mutate, INFERENCE-as-OBS, duplicate-payment-retry, stale-canon-seal, executor-self-witness) are not yet written.

**Until those three exist, promotion to `F13_RATIFIED_CHAT` would repeat the 2026-09-20 pattern** — constitutional declaration without measurement infrastructure. **This violates the agent→human canon's own law #131** as diagnosed by HERMES last night.

---

## 4. Why This Canon Is Different From Yesterday's Filing

The 131-HARAM human→agent canon published earlier today is **content**: it names what is haram/halal. This architectural canon is **substrate**: it specifies where that content lives, who enforces it, and through what mechanism.

The two work in tandem:

| Layer | What it does | Where it lives |
|---|---|---|
| Behavior canon (HARAM) | Names what's wrong | `/root/AAA/instructions/`, `/etc/arifos/canon/` (human-readable) |
| Architecture canon (this) | Names how the machine prevents it without trusting the agent | kernel policy package, pre-action gate, conformance probes |

Filing only the behavior canon without the architecture canon is **intent without enforcement** — the defect that produced last night's loader-missing finding. Filing only the architecture canon without the behavior canon is **substrate without content** — the system would be safe but purposeless.

Together they are the two halves of: *"the constitution is already true before the agent reads it."*

---

## 5. The Three Ratification Paths (Forwarded)

Following the same path structure I proposed for the human→agent canon, ratification of this architecture canon requires:

**(a) Build the conformance probe scaffold first.** Even if individual probes fail, the harness must run. This is the lowest-cost entry to ratification: it produces measurement before declaring completion.

**(b) Build the constitution compiler + handshake together.** Higher cost but closes the gap that the agent→human canon's loader was supposed to close. ~2-3 weeks of focused engineering.

**(c) Sealed waiver.** Sovereign accepts the inherited measurement-debt, ratifies anyway with a recorded exception (precedent: A-Z Doctrine, 2026-09-13, sovereign-chat + ritual-marker). Not recommended.

My recommendation is **(a)** as the immediate next step — it produces evidence the canon's claims are testable, which is the precondition for everything else.

---

## 6. What I Did

- **Wrote** the canon file at `/root/AAA/canon/CONSTITUTIONAL-ARCHITECTURE-CANON-2026-09-21.md` (faithful rendering — all math, all 11 layers, all probes, the EUREKA, the ZEN, the APEX preserved).
- **Embedded** a Current Federation State table inside the canon file itself, so the canon ships with receipts — readers cannot confuse "what the canon says" with "what currently runs."
- **Set** status to `DRAFT_AWAITING_F13` (not ratified; the sovereign has not yet ratified).
- **Did NOT** extend `haram_enforcement_map.yaml`, write the compiler, wire the handshake, or write conformance probes. All four are sovereign binary choices, not FI-008 lane decisions.
- **Did NOT** register in AGENTS.md yet. Two DRAFT_AWAITING_F13 entries from one morning may overwhelm the pointer; will batch with morning's other filings when sovereign signals direction.

All writes are reversible (git-tracked).

---

## 7. Receipt

| Handle | Path | State |
|---|---|---|
| Canon file | `/root/AAA/canon/CONSTITUTIONAL-ARCHITECTURE-CANON-2026-09-21.md` | `DRAFT_AWAITING_F13` |
| Witness file | `/root/AAA/reports/constitutional-architecture-witness-2026-09-21.md` | this file |
| AGENTS.md row | to be added on sovereign signal | pending |
| Existing fed state | `/etc/arifos/canon/federation-release.json` | UNCHANGED |

**FI-008 verdict:** HOLD on F13 ratification. Execute on filing (done). Recommend **(a) build conformance probe scaffold** as the next concrete step.

— End witness.
