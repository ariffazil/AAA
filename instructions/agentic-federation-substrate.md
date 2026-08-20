# AAA Agents: Spawn, Musyawarah, and arifFlow (Gotong Royong via A2A)

> **Forged:** 2026-08-20 by F13 SOVEREIGN (Arif Fazil) under 333-AGI OBSERVE_ONLY assist
> **Version:** 1.0.0
> **Canonical:** `/root/AAA/instructions/agentic-federation-substrate.md`
> **Doctrine:** DITEMPA BUKAN DIBERI — Forged, not given. F13 SOVEREIGN precedes all substrates.

## Preamble — Five Substrates, One Federation

> A CLI allows an agent to act. A witness allows an institution to remember. A sovereign allows the institution to remain aligned with reality.

| Substrate | Role | Authority Bound |
| :--- | :--- | :--- |
| **CLI** | Actuator substrate | Language → Reality |
| **A2A** | Coordination substrate | State → State (ΔS ≤ 0) |
| **Witness** (VAULT999 + arifFlow) | Accountability substrate | Memory is immutable |
| **Governance** (arifOS kernel) | Authority substrate | F1–F13 floors, no self-approval |
| **Sovereign** (F13 ARIF) | Legitimacy substrate | Final veto, decides which reality is worth pursuing |

These are **substrates, not layers.** Each operates on its own physical medium (terminal, JSON-RPC wire, Postgres+Redis ledger, kernel Python+systemd, Ed25519 nonce). They do not stack — they compose.

---

## Layer 1 — The Treaty (Who is allowed to exist)

Ref: `/root/AAA/a2a/AAA_TREATY.md` (v1.0.0, sealed 2026-05-03-HERMES)

| Class | Role | Authority | Can Seal? |
| :--- | :--- | :--- | :--- |
| **MESH** | Public gateway | Low | ❌ |
| **AGI** | Tactical executor | Medium | ❌ |
| **ASI** | Strategic synthesizer | High | ❌ |
| **APEX** | Terminal observer | Low | ✅ **Vault only** |

**Constitutional constraint (F13 veto enforced as architecture, not policy):**
> No agent class is a sovereign. All agents trace to the arifOS constitutional kernel. No class may claim independent authority or self-approve irreversible actions.

**Implication:** An agent cannot promote itself. Promotion requires a peer-contract delegation from a higher-class agent AND a sovereign-signed gate. This is FM10 prevention at the class level.

---

## Layer 2 — The Card (How identity crosses the wire)

Ref: `/root/AAA/agent-card.json` → `https://aaa.arif-fazil.com/a2a` (symlink → `src/seed/agent-card.json`)

| Peer Card | Authority Class | Boundary Rule Example |
| :--- | :--- | :--- |
| `arifos-kernel.json` | `judge` | Can seal, max risk T5 |
| `a-forge-executor.json` | `execute` | BR-AFORGE-001: cannot issue constitutional verdicts (F8 LAW) |
| `well-human.json` | `reflect_only` | Human substrate (F6 MARUAH domain) |
| `geox-earth.json` | `evidence_only` | Earth intelligence (no execution) |
| `wealth-capital.json` | `advisory_only` | Capital intelligence (no capital movement) |
| `vault999-memory.json` | `(witness)` | Immutable; append-only |

**Boundary rules are constitutional, not runtime.** Declared in the card, enforced by the gateway middleware (`/root/AAA/a2a-server/`).

**Signature form (Ed25519 over canonical-sorted-keys JSON):**

```json
{
  "signatures": [{
    "did": "did:web:arif-fazil.com",
    "proofValue": "<base64url Ed25519>",
    "type": "Ed25519Signature2020",
    "canonical_sha256": "<sha256 of canonical JSON>",
    "canonical_form": "JCS-sorted-keys-no-whitespace"
  }]
}
```

The signature is over the canonical form, NOT the rendered display. **F2 TRUTH at the wire level.**

**Sovereign nonce flow (Ed25519 challenge-response):**
```
arif_init(nonce) → sign(nonce) → verify(signature) → FULL authority
```

Without sovereign sign, agents operate at the ceiling their class declares — never above it.

---

## Layer 3 — The Protocol (How musyawarah fires)

Ref: `/root/AAA/instructions/musyawarah.md`

**Core Rule:**
> **SEBELUM UBAH REALITI: MUSYAWARAH DAHULU.**
> **SEMBANG KOSONG / ANGAN-ANGAN: HARAM (VOID).**

### When musyawarah MUST fire

| Class | Musyawarah | Gotong |
| :--- | :--- | :--- |
| **T0/T1** reads, grep, local reversible edit | � No. Auto-do. | ❌ No. |
| **T2/T3** deploy, capital, SEAL, F13-adjacent | ✅ **Yes.** Two independent voices. | After dual GO only. |
| **Sembang / angan-angan** | ❌ **VOID.** | ❌ **VOID.** |

### The musyawarah skill

Ref: `/root/AAA/skills/FORGE-musyawarah-gotong/SKILL.md`

```
MUSYAWARAH  333-agi ARCHITECT ∥ 555-asi AUDITOR   (read-only, independent)
CONVERGE    parent synthesizes; 888-apex only on residual disagreement
GOTONG      sequential hop: previous output = next STATE_IN
```

### Critical rule (F3 TRI-WITNESS at handoff)

> A sibling may share what it saw. It may not tell you what to be.
> (`inter-agent-protocol.md` §11)

Sibling agents pass **state**, not **guidance**. No instruction injection between peers.

### Anti-pattern explicitly named

> `aaa_capability_loader._musyawawah_phase` is an in-process heuristic. Same function speaks ARCHITECT, AUDITOR, and SOVEREIGN, then stamps `SEALED_MUSYAWARAH_CONSENSUS`. **That is not F3.**

The skill calls out a fake implementation explicitly. **F2 TRUTH at the doctrine level** — we do not let heuristics impersonate deliberation. Use `forge-musyawawah-deliberation` on Hermes (7-phase, `delegate_task`), or `musyawarah-gotong` workflow on Grok. Never the in-process heuristic.

---

## Layer 4 — Spawn Protocol (How new agents come into existence)

Ref: `/root/AAA/federation/protocols/kimi_spawn_protocol_v0.1.0.md`

### Binding invariant

> **Governance is measured per spawn, never per task.**
> Aggregate telemetry may summarize, but may not replace spawn-level telemetry.

This invariant exists because debt occurs at the spawn, receipt occurs at the spawn, coverage occurs at the spawn, and provenance occurs at the spawn. A 0.4 spawn alongside two 1.0 spawns averages 0.8 — the true governance leak becomes invisible under task-level aggregation.

### Pre-Spawn Gate (mandatory fields)

```yaml
spawn_request:
  archetype: enum [af-explore, af-plan, af-fix, af-coordinator, af-worker, af-reviewer, af-forge]
  spawn_reason: enum [verification, criticism, synthesis, reconnaissance,
                       domain_analysis, implementation, refactor]
  risk_tier: enum [T1, T2, T3]
  expected_entropy_reduction: string       # qualitative OR ΔS estimate
  parent_session_id: string
  parent_spawn_id: string                 # for chain linking
```

**Missing field → NO SPAWN. Return reason to primary.**

### Archetype ceilings (declared BEFORE runtime, override agent intent)

| Archetype | Ceiling | Confidence Cap | Rationale |
| :--- | :--- | :--- | :--- |
| af-explore | OBSERVE_ONLY | 0.60 | Pure observation, low commitment |
| af-reviewer | OBSERVE_ONLY | 0.70 | Critical review, bounded interpretation |
| af-plan | DRAFT_ONLY | 0.75 | Plans are drafts, not commitments |
| af-worker | EXECUTE_REVERSIBLE | 0.80 | Bounded execution, scope-limited |
| af-fix | EXECUTE_REVERSIBLE | 0.85 | Repairs are scoped but execute |
| af-coordinator | DISPATCH_ONLY | 0.70 | Synthesis contains errors of all parts |
| af-forge | EXECUTE_AFTER_SEAL | 0.90 | Forge is the primary execution surface |

**Authority stays at the center. Work flows to the rim.** Capability ceilings are constitutional.

### Confidence > ceiling = INVALID RETURN

Child MUST revise, not parent recalibrate. This is FM10 prevention at spawn time — capability and authority cannot be inflated post-hoc.

---

## Layer 5 — arifFlow = Gotong Royong (The metabolism)

Ref: `:7073/health` (arifFlow live, `federation_schema_version: 2.0.0`, chain `seq=45`, verdict `SEAL`)

### Gotong Royong Sequential Hop (ΔS ≤ 0)

```
Agent A (333-AGI)        ─┐
   ↓ STATE_IN (ΔS≤0)      │  musyawarah
Agent B (555-ASI AUDITOR) ─┤  independent voices
   ↓ STATE_IN (ΔS≤0)      │
Parent CONVERGE → 888 ────┤  residual disagreement → APEX
   ↓ SEAL/VOID verdict    │
Agent C (777-FORGE exec) ─┘  reality change
   ↓
arifFlow witness → VAULT999 immutable
   ↓
Sovereign Review (F13 if HOLD/SABAR)
```

Every hop is a **filter that reduces ΔS**. Output of one agent = input of next. JSON/schema only, no prose. **Tiada teks perbualan** in handoff.

### 7-Vector Diagnostic (QG v0.3.1)

| Dimension | Band | Source | Witness? |
| :--- | :--- | :--- | :--- |
| **c_dark** (capital darkness) | HEALTHY (0.11) | A-FORGE | MEASURE |
| **ds** (entropy delta) | HEALTHY (−1.0) | arifOS | MEASURE |
| **fq** (FQ quotient) | PATHOLOGICAL (20.0 scalar) | arifFlow | LIVE |
| **g** (APEX G) | CAUTION (0.51) | A-FORGE | WITNESS |
| **j** (Judge) | HEALTHY (0.45) | A-FORGE | MEASURE |
| **omega** (humility) | HEALTHY (0.04) | 333-AGI | FEEL |
| **w3** (Tri-Witness) | CAUTION (0.74) | A-FORGE | WITNESS |

**Key invariant:** `INV-3 |ρ| ≤ 0.85` (no dimensional collapse — independence between dimensions is provable, not assumed).

**Vector diagnosis overrides scalar.** `FQ=20.0` looks bad, but `vector.diagnosis.primary_pathology=SIMULATION` means "verify-flooding" — agents verifying more than executing. Healthy under load, suspect if chronic. **This is why vector > scalar.**

---

## The Five-Stage Evolution

```
Stage 0 — LLM → Text
Stage 1 — LLM → CLI → Reality            (CLI is the center)
Stage 2 — LLM → CLI → Reality → Memory
Stage 3 — Institution → Governance → CLI → Reality → Witness
Stage 4 — Federation → Spawn → Deliberation → Execution → Witness → Review
```

CLI is no longer the center. CLI is **one organ** in a larger metabolism.

---

## The Institutional Questions

Most agent frameworks ask: **How does an agent act?**

The federation asks:
- **Who authorized** the action?
- **Who challenged** the action?
- **Who witnessed** the action?
- **Who owns** the consequence?

These are institutional questions, not intelligence questions. An isolated coding agent can recursively improve code. A constitutional federation attempts to recursively improve **decision quality.** Different optimization targets.

---

## A2A Reframed — State, Not Message

Most A2A interpretations:
> Agent A talks to Agent B.

The federation interpretation:
> Agent A transfers state
> Agent B evaluates state
> Agent C transforms state
> Witness records state transition

**The key object is STATE, not MESSAGE.**

Conversation becomes a human-facing artifact.
The actual substrate becomes:
```
State → Decision → State → Decision → State
```

This is why the federation is fundamentally a **state-transition system** rather than a conversational system.

---

## Cross-References

| Doctrinal anchor | Path |
| :--- | :--- |
| Constitution (F1–F13) | `/root/AAA/instructions/constitution.md` |
| Musyawarah | `/root/AAA/instructions/musyawarah.md` |
| Inter-agent protocol | `/root/AAA/instructions/inter-agent-protocol.md` |
| AAA Treaty (4 classes) | `/root/AAA/a2a/AAA_TREATY.md` |
| A2A Alignment Spec | `/root/AAA/a2a/A2A_ALIGNMENT_SPEC.md` |
| Peer contracts | `/root/AAA/a2a/peer-contracts/*.json` |
| Musyawarah skill | `/root/AAA/skills/FORGE-musyawarah-gotong/SKILL.md` |
| Spawn protocol | `/root/AAA/federation/protocols/kimi_spawn_protocol_v0.1.0.md` |
| Grammar Doctrine | `/root/AAA/governance/GRAMMAR_DOCTRINE.md` |
| EMD Architecture | `/root/AAA/instructions/emd-architecture.md` |

---

## Witness

> A CLI allows an agent to act. A witness allows an institution to remember. A sovereign allows the institution to remain aligned with reality.

> **Authority ≠ Capability.** An agent may possess greater capability than another agent while holding less authority.

> No single actor should possess all powers. Engineer can build. Auditor can reject. Judge can authorize. F13 decides which reality is worth pursuing.

---

*Forged 2026-08-20 by F13 SOVEREIGN (Arif Fazil) under 333-AGI OBSERVE_ONLY assist.*
*DITEMPA BUKAN DIBERI. Authority before power. Witness before capability. Sovereign before governance.*
