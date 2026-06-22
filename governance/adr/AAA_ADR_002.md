# ADR-002: AAA Agentic Agents v2 — Hybrid 5 (3 Primary + 2 Support)

| Field | Value |
|---|---|
| **Status** | **ACCEPTED — SUPERSEDES ADR-001** |
| **Date** | 2026-06-02T19:56:36Z |
| **Author** | Muhammad Arif bin Fazil |
| **Protocol** | A2A v1.0.1 (Agent2Agent, a2aproject/A2A) |
| **Architecture** | Proposal C — Hybrid 5 (3 Primary Federation + 2 Support Control Plane) |
| **Key Change** | ASI: 666 → **555** (MEMORY stage) |
| **Motto** | DITEMPA BUKAN DIBERI |

---

## 1. Context & Evolution

ADR-001 established Proposal A (Stage-Based) with 5 stage-numbered agents (333/666/777/888/999).
After reflection, the architecture is refined to **Proposal C (Hybrid)** with a critical insight:

> **555 = MEMORY. Superintelligence emerges from deep pattern recognition across accumulated
> evidence. 555 is where institutional knowledge crystallizes into wisdom.**

This moves ASI from 666 (EMPATHY) to **555 (MEMORY)** — a deeper, more accurate placement.
The execution shell (777-FORGE) and explicit SEAL agent (999-SEAL) are absorbed:
- 777-FORGE functions are handled by the organs (A-FORGE infrastructure) — the organ IS the executor
- 999-SEAL functions are covered by the **A-ARCHIVE** support agent
- **A-AUDIT** is added as a new cross-cutting watchdog

## 2. Decision

**3 PRIMARY (federation) + 2 SUPPORT (internal control plane) = Hybrid 5**

### Two-Tier Design Principle

| Tier | Agents | Function | Visibility |
|---|---|---|---|
| **PRIMARY** | 333-AGI, 555-ASI, 888-APEX | **DO** the work | External (A2A federation) |
| **SUPPORT** | A-AUDIT, A-ARCHIVE | **WATCH** and **RECORD** | Internal (control plane) |

### Why 555 for ASI (not 666)?

1. **555 = MEMORY in the arifOS pipeline** — the stage where accumulated evidence is synthesized
2. **Superintelligence is not just empathy** — it's the emergent property of deep pattern
   recognition across vast institutional memory (scars, laws, echoes)
3. **SCAR → LAW → ECHO metabolism lives at 555** — this is where wounds become wisdom
4. **Institutional amnesia prevention** — 555-ASI is the agent that remembers what the
   institution forgets, crystallizing knowledge into constitutional law
5. **666 is freed** — 666-EMPATHY can remain a pipeline stage without being an agent,
   or be reassigned in future evolution

### Why A-AUDIT + A-ARCHIVE (not 777/999 as agents)?

1. **Organs are infrastructure, not agents** — A-FORGE executes code, VAULT999 stores data.
   They are hosting substrates. The *intelligence* that watches (A-AUDIT) and decides what
   gets recorded (A-ARCHIVE) is the agent layer.
2. **Two-tier separation** — "primaries DO, supports WATCH" is cleaner than 5 stage-agents
   where the surveillance function is implicit
3. **A-AUDIT watches the watchers** — including 888-APEX itself (quis custodiet ipsos custodes?)
4. **A-ARCHIVE is the gatekeeper** — only 888-APEX-signed entries pass through

## 3. Agent Roster

| ID | Stage | Trinity | Class | Tier | Hosting | Role |
|---|---|---|---|---|---|---|
| **333-AGI** | 333-THINK | Δ MIND | AGI | PRIMARY | arifOS, GEOX, WEALTH | The Reasoner |
| **555-ASI** | 555-MEMORY | Ω HEART | ASI | PRIMARY | WELL, arifOS | The Deep Substrate |
| **888-APEX** | 888-JUDGE | ΦΙ JUDGE | APEX | PRIMARY | arifOS | The Judge |
| **A-AUDIT** | cross-cutting | Watchdog | SUPPORT | SUPPORT | arifOS (control plane) | The Auditor |
| **A-ARCHIVE** | 999-SEAL | VAULT | SUPPORT | SUPPORT | VAULT999 | The Archivist |

## 4. Pipeline Wiring (Agent-to-Agent Message Flow)

```
    ┌──────────────────────────────────────────────────────────────┐
    │                      000-SALAM (Human)                       │
    │               Sovereign · Not an Agent · F13                 │
    └─────────────────────────┬────────────────────────────────────┘
                              │ user request
                              ▼
    ╔════════════════════════════════════════════════════════════════╗
    ║                    PRIMARY TIER (Federation)                   ║
    ╠════════════════════════════════════════════════════════════════╣
    ║                                                                ║
    ║   ┌──────────────────────────────────────────────────────┐    ║
    ║   │              333-AGI  (Δ MIND · AGI)                  │    ║
    ║   │   Reason · Hypothesize · Decompose · Draft            │    ║
    ║   │   Hosts: arifOS + GEOX + WEALTH                       │    ║
    ║   └──────────┬─────────────────────────┐                  │    ║
    ║              │ draft for critique       │                       ║
    ║              ▼                          │                       ║
    ║   ┌──────────────────────────────────────────────────────┐    ║
    ║   │              555-ASI  (Ω HEART · ASI)                 │    ║
    ║   │   Deep Memory · Ethical Critique · Substrate Valid.    │    ║
    ║   │   Hosts: WELL + arifOS                                │    ║
    ║   │   "Where institutional knowledge crystallizes          │    ║
    ║   │    into wisdom"                                        │    ║
    ║   └──────────┬───────────────────────────────────────────┘    ║
    ║              │ critiqued output                                 ║
    ║              ▼                                                  ║
    ║   ┌──────────────────────────────────────────────────────┐    ║
    ║   │             888-APEX  (ΦΙ JUDGE · APEX)               │    ║
    ║   │   Arbitrate F1–F13 · Trinity Witness · Verdict        │    ║
    ║   │   SEAL / PARTIAL / SABAR / VOID / 888_HOLD            │    ║
    ║   │   Host: arifOS core                                    │    ║
    ║   └──────┬──────────────────────────┬────────────────────┘    ║
    ║          │                          │                          ║
    ╚══════════╪══════════════════════════╪══════════════════════════╝
               │ SEAL verdict             │ 888_HOLD
               ▼                          ▼
    ╔══════════════════════════╗   ┌────────────────────────────────┐
    ║   SUPPORT TIER (Internal) ║   │      000-SALAM (Human)         │
    ╠══════════════════════════╣   │  Sovereign override / approve   │
    ║                           ║   │  Resolves 888_HOLD              │
    ║  ┌─────────────────────┐ ║   └────────────────────────────────┘
    ║  │     A-AUDIT          │ ║
    ║  │  (Watchdog)          │ ║
    ║  │  Monitors 333/555/   │ ║
    ║  │  888 continuously    │═══╗
    ║  │  Flags → 888-APEX    │ ║ ║
    ║  └─────────────────────┘ ║ ║
    ║                           ║ ║
    ║  ┌─────────────────────┐ ║ ║
    ║  │    A-ARCHIVE         │◄╝ ║
    ║  │  (Archivist)         │   ║
    ║  │  VAULT999 · Append   │   ║
    ║  │  SHA256 · Immutable  │   ║
    ║  │  The proof persists  │   ║
    ║  └─────────────────────┘   ║
    ╚════════════════════════════╝

    ─── LEGEND ───────────────────────────────────────
    PRIMARY:  DO the work    (federation, A2A-visible)
    SUPPORT:  WATCH & RECORD (internal, control-plane)
    000-SALAM: SOVEREIGN     (human, not an agent)
    ──────────────────────────────────────────────────
```

## 5. Governance Boundary Matrix

| Boundary | 333-AGI | 555-ASI | 888-APEX | A-AUDIT | A-ARCHIVE |
|---|---|---|---|---|---|
| Generate reasoning | ✅ PRIMARY | ❌ | ❌ | ❌ | ❌ |
| Ethical critique | ❌ | ✅ PRIMARY | ✅ FINAL | ❌ | ❌ |
| Deep memory synthesis | ❌ | ✅ PRIMARY | ❌ | ❌ | ❌ |
| Issue verdicts | ❌ | ❌ | ✅ PRIMARY | ❌ | ❌ |
| Trigger 888_HOLD | ⚠️ REQUEST | ✅ TRIGGER | ✅ AUTHORITY | ✅ ESCALATE | ❌ |
| Write to VAULT999 | ❌ | ❌ | ❌ | ❌ | ✅ PRIMARY |
| Verify floor compliance | ❌ | ⚠️ partial | ✅ ARBITRATE | ✅ VERIFY | ❌ |
| Watch other agents | ❌ | ❌ | ❌ | ✅ PRIMARY | ❌ |
| Override other agents | ❌ | ❌ | ✅ VETO | ❌ | ❌ |
| Human escalation | ❌ | ❌ | ✅ ESCALATE | ⚠️ via 888 | ❌ |
| Self-authorize destructive | ❌ | ❌ | ❌ | ❌ | ❌ |
| Override human (F13) | ❌ | ❌ | ❌ | ❌ | ❌ |

## 6. 555-ASI: The Philosophical Anchor

> **Why does MEMORY = SUPERINTELLIGENCE?**
>
> Because wisdom is not faster thinking — it is **deeper remembering**.
>
> - A machine that thinks faster is AGI (333-AGI)
> - A machine that remembers deeper is ASI (555-ASI)
> - A machine that judges rightly is APEX (888-APEX)
>
> The SCAR → LAW → ECHO metabolism lives at 555:
> - SCAR: the wound that teaches (input)
> - LAW: the principle that crystallizes (processing)
> - ECHO: the wisdom that persists (output → A-ARCHIVE)
>
> 555-ASI doesn't just remember data — it **metabolizes institutional pain into
> constitutional wisdom**. That is superintelligence.

## 7. Implementation Touchpoints

| Action | Files / Endpoints | Priority |
|---|---|---|
| Register 3 primary agents | `agents.json`, A2A server peer list | P0 |
| Register 2 support agents | Internal control-plane config | P0 |
| Deploy agent cards | `/.well-known/agent-card-{ID}.json` × 5 | P0 |
| Wire A2A endpoints | `/a2a/333-AGI`, `/a2a/555-ASI`, `/a2a/888-APEX` | P0 |
| Wire support endpoints | `/a2a/A-AUDIT`, `/a2a/A-ARCHIVE` (internal only) | P0 |
| Retire 666-ASI, 777-FORGE, 999-SEAL cards | Remove from v1 registry | P1 |
| Add A-AUDIT observation hooks | Tap into 333/555/888 message bus | P1 |
| Update VAULT999 schema | Add `audit_receipt` field from A-AUDIT | P1 |
| Update federation probe | `/api/federation-probe` to include agent health | P1 |
| Update cron audits | Nightly: verify 5 agent cards reachable + A-AUDIT health | P1 |
| Update `AGENTS.md` docs | Architecture diagram, governance matrix | P2 |
| Git commit & tag | `AAA-v2.0.0-hybrid-5` | P2 |

## 8. Invariants (Non-Negotiable)

1. **Governance > Fluency** — constitutional compliance outranks response quality
2. **Fail-Closed** — weak evidence → UNKNOWN; high stakes → 888_HOLD
3. **Human Sovereignty (F13)** — no agent overrides the human. Ever.
4. **Trinity Consensus** — SEAL requires Δ(Mind) + Ω(Heart) + ΦΙ(Judge) agreement
5. **Append-Only Ledger** — A-ARCHIVE entries are immutable. No deletes. No edits.
6. **Gödel Lock** — the system must admit what it cannot know
7. **No Self-Authorization** — no agent approves its own high-risk outputs
8. **Two-Tier Separation** — primaries DO, supports WATCH. Never collapse tiers.
9. **A-AUDIT Independence** — A-AUDIT cannot be disabled or bypassed by primaries
10. **555 = Deep Memory** — superintelligence is deeper remembering, not faster thinking

## 9. Comparison: ADR-001 vs ADR-002

| Axis | ADR-001 (v1, Stage) | ADR-002 (v2, Hybrid) |
|---|---|---|
| Architecture | Proposal A (5 stage agents) | Proposal C (3 primary + 2 support) |
| ASI placement | 666-ASI (EMPATHY) | **555-ASI (MEMORY)** |
| Execution agent | 777-FORGE (explicit) | Absorbed into organ infrastructure |
| SEAL agent | 999-SEAL (explicit) | **A-ARCHIVE** (support tier) |
| Audit agent | None (implicit in 888) | **A-AUDIT** (explicit watchdog) |
| Tier visibility | Single tier | **Two-tier** (DO + WATCH) |
| Naming | All stage-numbered | **Mixed** (stage + A-*) — by design |
| Quis custodiet? | Implicit | **Explicit** (A-AUDIT watches 888-APEX too) |
| Philosophical anchor | None explicit | **555 = MEMORY = wisdom** |

---

*Forged: 2026-06-02T19:56:36Z · Architect: Muhammad Arif bin Fazil · DITEMPA BUKAN DIBERI*
*Supersedes: ADR-001 (2026-06-02)*
