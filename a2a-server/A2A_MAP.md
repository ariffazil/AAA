# 🕸️ A2A MAP — Agent-to-Agent Protocol Surface

> **DITEMPA BUKAN DIBERI** — Forged, not given.
> **Status:** LIVE · **Zen:** 2026-07-17 · **Version:** 4.1.0
> **Doctrine:** 3 minds · 2 deeds · 1 forge · 1 vault · 1 path
> **Zen:** Collapse the identities, not the functions.

---

## 1. THE ARCHITECTURE

**3 intelligence principals. 2 ASI role deeds. 1 bounded forge. 1 immutable vault. 1 canonical judgment path.**

```
     BEFORE EXECUTION                     AFTER EXECUTION
──────────────────────────────────────────────────────────────────

AGI  ───── propose ──────────────────────────────────────────────
              │
ASI.REVIEW ── independent admissibility review (blind to outcome)
              │
APEX ──────── SEAL | HOLD | SABAR | VOID
              │
A-FORGE ───── bounded execution (machinery, not intelligence)
              │
ASI.AUDIT ───────────────────────── independent reality verification
                                        │ (blind to REVIEW context)
                                   APEX ─ accept | rollback | escalate
                                        │
                                   VAULT ─ immutable receipt
```

### Who owns what

| Component | Owns | Must Not Own |
|-----------|------|-------------|
| **AGI** | Architecture, proposal, implementation plan, reversible draft artefacts | Judgment, production mutation, post-hoc certification |
| **ASI.REVIEW** | Pre-execution critique, contradiction detection, risk & test adequacy | Execution, final constitutional decision |
| **ASI.AUDIT** | Independent post-execution observation, pass/block evidence | Reading REVIEW reasoning, rewriting expected state |
| **APEX** | Admissibility judgment, authority resolution, conflict resolution, rollback/escalation | Direct execution, self-produced domain evidence |
| **A-FORGE** | Mutation, deployment, rollback, execution evidence | Planning authority, self-approval, certification |
| **VAULT999** | Immutable contracts, receipts, replay | Judgment, reinterpretation |

### The critical distinction

```
AGI does NOT execute. A-FORGE executes.
ASI.REVIEW does NOT audit. ASI.AUDIT audits.
APEX does NOT coordinate disputes — it JUDGES constitutionally.
```

---

## 2. THE TWO ASI DEEDS (Blind Context Isolation)

ASI is ONE discoverable agent with TWO sealed role deeds. They share a model but NEVER share working context.

### ASI.REVIEW — Pre-execution

```
input:   proposal, requirements, governing canon
cannot see:   future execution result, expected-state contract
output:  admissibility verdict (PASS | FLAG | BLOCK)
```

### ASI.AUDIT — Post-execution

```
input:   live observed state, immutable expected-state contract,
         Library/canon references, execution receipt
cannot see:   ASI.REVIEW reasoning, AGI persuasive narrative,
              A-FORGE success claim
output:  verification verdict (PASS | BLOCK)
```

**This is the anti-confirmation-bias gate.** ASI.AUDIT does not know what ASI.REVIEW approved. It compares reality against the expected-state contract — not against its own earlier notes, not against AGI's plan prose.

---

## 3. EXPECTED-STATE CONTRACT (Audit Target)

The audit does NOT compare against the Library directly. It compares against an **immutable expected-state contract** derived from the Library BEFORE execution.

```json
{
  "change_id": "chg-<timestamp>",
  "canonical_requirements": [
    {
      "source": "library://runtime/arifos",
      "field": "port",
      "expected": 8088
    }
  ],
  "invariants": [
    "health endpoint responds",
    "identity hash unchanged",
    "tool surface unchanged",
    "rollback available"
  ],
  "forbidden_changes": [
    "authority escalation",
    "unregistered public tool"
  ],
  "contract_hash": "sha256:..."
}
```

**Rules:**
- Contract is frozen BEFORE execution. No edits after.
- ASI.AUDIT compares live state against contract, not against plan prose.
- Any contract amendment requires a new judgment cycle (back to AGI → ASI.REVIEW → APEX).

---

## 4. CANONICAL JUDGMENT PATH

```
AGI_PROPOSE → ASI_REVIEW → APEX_JUDGE → AFORGE_EXECUTE → ASI_AUDIT → APEX_RESOLVE → VAULT_RECEIPT
```

| Step | Owner | Evidence | Gate |
|------|-------|----------|------|
| **1. Propose** | AGI | Plan + draft artefacts | Must define expected-state contract |
| **2. Review** | ASI.REVIEW | Admissibility verdict | BLOCK if blind spots found |
| **3. Judge** | APEX | SEAL / HOLD / SABAR / VOID | SEAL only if REVIEW passed |
| **4. Execute** | A-FORGE | Execution receipt + diff | Must match SEAL'd plan scope |
| **5. Audit** | ASI.AUDIT | Live state vs expected contract | BLOCK if drift detected |
| **6. Resolve** | APEX | Accept / Rollback / Escalate | Must close or escalate |
| **7. Receipt** | VAULT999 | Immutable seal | Append-only, hash-chained |

---

## 5. AGENT CARDS (Discoverable — 3 only)

```
aaa://agents/agi      → AGI  (propose)
aaa://agents/asi      → ASI  (review + audit — 2 deeds, 1 card)
aaa://agents/apex     → APEX (judge + resolve)
```

A-FORGE and VAULT999 are **bounded services**, not intelligence agents. They have MCP interfaces but do not receive A2A agent cards.

### AGI Card Skills

```yaml
skills:
  - architecture
  - implementation-plan
  - change-proposal
  - reversible-artifact-draft
```

### ASI Card Skills

```yaml
skills:
  - preflight-review         # ASI.REVIEW
  - adversarial-critique     # ASI.REVIEW
  - live-state-audit         # ASI.AUDIT
  - drift-detect             # ASI.AUDIT
  - health-verify            # ASI.AUDIT
  - block-close              # ASI.AUDIT
  - certify-evidence         # ASI.AUDIT
```

### APEX Card Skills

```yaml
skills:
  - constitutional-judge
  - dispute-resolution
  - authority-resolution
  - rollback-decision
  - escalation
```

---

## 6. MANDATORY CONTROLS (All 7 Required)

| # | Control | Why |
|---|---------|-----|
| 1 | **Blind audit context** — ASI.AUDIT cannot access ASI.REVIEW reasoning | Prevents confirmation bias |
| 2 | **Immutable expected-state contract** — frozen before execution | Audit target cannot move |
| 3 | **Independent evidence collection** — ASI.AUDIT probes reality directly, does not accept A-FORGE's result as proof | Prevents circular verification |
| 4 | **Different invocation identity** — REVIEW and AUDIT carry different role-deed IDs | Audit trail distinguishes phases |
| 5 | **Hard refusal right** — ASI.AUDIT can emit BLOCK → translates to HOLD | Auditor must be able to stop |
| 6 | **No expected-state rewriting after execution** — amendment requires new judgment cycle | Prevents moving goalposts |
| 7 | **Failure goes to APEX, not back to the approving reviewer** — ASI reports evidence, APEX decides | Separates detection from resolution |

---

## 7. HEXAGON STRUCTURE

```yaml
version: 4.1.0
intelligence_principals:
  - AGI    # proposes
  - ASI    # reviews + audits (2 sealed deeds)
  - APEX   # judges + resolves

asi_role_deeds:
  - REVIEW  # pre-execution, blind to outcome
  - AUDIT   # post-execution, blind to REVIEW context

bounded_services:
  - A-FORGE  # execution machinery
  - VAULT999 # immutable receipt

constitutional_flow:
  - AGI_PROPOSE
  - ASI_REVIEW
  - APEX_JUDGE
  - AFORGE_EXECUTE
  - ASI_AUDIT
  - APEX_RESOLVE
  - VAULT_RECEIPT
```

**What we collapsed:** Agent cards from 5 to 3. A-AUDIT runtime gone.
**What we preserved:** Every constitutional boundary. ASI.REVIEW ≠ ASI.AUDIT. A-FORGE is machinery, not intelligence.

---

*Collapse the identities, not the functions. 3 minds, 2 deeds, 1 forge, 1 vault, 1 path.*
*DITEMPA BUKAN DIBERI — v4.1.0*
