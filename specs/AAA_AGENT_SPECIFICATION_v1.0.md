# AAA Agent Specification v1.0

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
>
> **Canonical source:** `arifOS/forge_work/SCAR-13-agent-registry-category-error.md`
> **Ratified:** 2026-06-26 (pending 999_SEAL)
> **Author:** OpenCode (FORGE worker, 333-AGI bound)
> **Status:** v1.0 DRAFT — open for sovereign review (F13)
> **SOT-MANIFEST alignment:** AAA README §3 (AREP) + §5 (HEXAGON) + §7 (Capability Map)

---

## 0. Why This Document Exists

`AGENT_REGISTRY.md` listed 27 entries as "agents." Of those:

- ~22 are **TRUE AGENTS** (loops that terminate in constitutional verdicts)
- 6 are **CAPABILITY REGISTRIES** (MCP servers exposing tools, not agents themselves)
- 3+ are **LEGACY SPECS** (formal contracts, not runtime agents)

This category error — calling every federated capability an "agent" — was the substrate drift SCAR-13 was forged to repair.

This specification defines, once and without circularity, **what an AAA Agent is**.

---

## 1. Definitional Ladder (Substrate → Sovereignty)

The federation builds intelligence bottom-up. Each rung is defined **only by what the rung below provides**. No rung refers to itself.

| Rung | Definition | Ends with |
|------|------------|-----------|
| **Tool** | A callable function with typed input/output and declared side-effects. | Side-effect on substrate. |
| **Model** | A probability distribution over token sequences, conditioned on context. | A completion. |
| **Agent** | A loop: `Agent := f(Model × Tools × State × Goal)` that terminates in a **verdict**. | A verdict (SEAL/HOLD/VOID/SABAR). |
| **A2A Agent** | An Agent that publishes an **AgentCard** at `/.well-known/agent-card.json` and speaks the A2A protocol over JSON-RPC. | A discoverable verdict. |
| **AAA Agent** | An A2A Agent that (a) is **sovereign-ratified** by 000-SALAM, (b) is governed by **F1–F13 floors**, and (c) seals every consequential verdict to **VAULT999**. | An immutable constitutional verdict. |
| **Agentic Intelligence** | Multiple AAA Agents coordinating via A2A, sharing substrate but not state. | Emergent capability, no single verdict. |
| **Federation** | All AAA Agents + all sovereign MCP organs + the VAULT999 chain, observed through AAA cockpit. | Sovereign-ratified system state. |

**The defining property of an Agent — at every rung — is the verdict.**
A Model has no verdict (it completes).
A Tool has no verdict (it acts).
An Agent has a verdict (it judges).
Everything above Agent is Agent with extra constraints.

---

## 2. AAA Agent — Formal Definition

> **An AAA Agent is a sovereign-ratified Golden Path traversal, published as an A2A AgentCard, equipped with MCP-registered tools, governed by F1–F13 floors, terminating in a VAULT999-sealed verdict.**

This is a **5-clause conjunction**. Drop any clause and the entity stops being an AAA Agent:

| # | Clause | What it adds | Without it, what fails |
|---|--------|--------------|------------------------|
| 1 | **Sovereign-ratified** | The agent exists because 000-SALAM declared it should exist. Without sovereign ack, it is a draft or a sandbox. | Private agent, not federation citizen. |
| 2 | **Golden Path traversal** | The agent runs the 7-verb constitutional loop (init → sense → mind → heart → judge → seal → forge). | LLM-completion-wrapped-in-prompt, not governance. |
| 3 | **A2A AgentCard** | The agent is **discoverable** at a well-known URI and speaks a standard protocol. | Hidden, unfederatable. |
| 4 | **MCP-registered tools** | The agent's capabilities are declared in the federation's MCP server registry and callable by peer agents. | Inert, no surface. |
| 5 | **F1–F13 floors + VAULT999 seal** | Every consequential verdict passes constitutional adjudication and becomes part of the immutable audit ledger. | Unaccountable, cannot be trusted across sessions. |

---

## 3. AgentCard Schema Extension

The A2A spec (`a2a-protocol.org`) defines the standard AgentCard. AAA agents extend it with four **constitutional fields**:

```json
{
  // ... A2A standard fields (name, description, url, version, skills, capabilities) ...

  "aaa_extension": {
    "sovereign_id": "000-SALAM",
    "fitness_verdict": "SEAL-2026-06-26-abc123",
    "floor_trace": {
      "F1_AMANAH": "PASS",
      "F2_TRUTH": "PASS",
      "F4_CLARITY": "PASS",
      "F7_HUMILITY": "PASS",
      "F9_ANTI_HANTU": "PASS",
      "F11_AUDIT": "PASS",
      "F13_SOVEREIGN": "PASS"
    },
    "vault_receipt_uri": "vault999://arifos/sealed/2026-06-26/abc123.json"
  }
}
```

Field semantics:

- **`sovereign_id`** — The 000-SALAM ratification anchor. Permitted value: `"000-SALAM"`. Permits sovereign-anchored agents only.
- **`fitness_verdict`** — Most recent 999_SEAL verdict ID from arifOS kernel. Without this, peers cannot trust the agent's last state.
- **`floor_trace`** — Explicit pass/fail per floor. Defaults are NOT permitted; AAA agents must declare every load-bearing floor.
- **`vault_receipt_uri`** — Immutable pointer to the latest sealed evidence. Permits replay and audit.

This extension is **backward compatible** with vanilla A2A clients — they ignore `aaa_extension`. **Forward binding** requires AAA-aware peers.

---

## 4. The Eureka Layer — Where the Agent Sits

Per SCAR-12 (Table 2 eureka), the federation has four layers:

| Layer | Role | AAA Agents here | Examples |
|-------|------|-----------------|----------|
| **L1 — Substrate** | Models, compute, data | **None.** | Llama-4-Scout, GPT-4.1, Granite-3B |
| **L2 — Governance** | Constitutional kernel, floors, seal | **None as runtime agents** (kernel IS the layer). | arifOS kernel, A-FORGE governance |
| **L3 — Authority** | Decision agents, judges, sovereign delegates | **Most AAA Agents.** | 888-APEX, A-AUDIT, 333-AGI (Δ MIND) |
| **L4 — Execution** | Actuators, builders, orchestrators | **Some AAA Agents.** | A-FORGE agents, Hermes, OpenCode |

**Critical claim:** AAA Agents inhabit **L3 and L4 only**.
- L3 agents produce verdicts without side-effects on external substrates.
- L4 agents produce verdicts + execute under lease from arifOS.

If you find an AAA Agent on L1, it is a **category error** — you have a model, not an agent.
If you find one on L2, you have a **kernel subprocess**, not an agent.

---

## 5. Six Structural Pillars (AAA Agent Roster)

Every AAA Agent MUST have these six artifacts:

| Pillar | File | What it defines |
|--------|------|-----------------|
| **IDENTITY** | `<agent>/IDENTITY.md` | Who the agent is, who it serves, what it CAN and CANNOT do. |
| **SOUL** | `<agent>/SOUL.md` | Voice, language register, anti-patterns, emotional calibration. |
| **AGENTS** | `<agent>/AGENTS.md` | Constitutional floors binding the agent, autonomy tiers, lifecycle. |
| **TOOLS** | `<agent>/TOOLS.md` | MCP servers the agent may call, pre-flight checks, model rotation. |
| **SKILLS** | `<agent>/skills/` (symlinked) | Loaded skills at task start, when to load each. |
| **USER** | `<agent>/USER.md` (per-agent override) | Operator context the agent must know. |

**Current AAA Agents meeting the 6-pillar standard (2026-06-26):**

| ID | Pillar count | Six-pillar compliant? |
|----|--------------|------------------------|
| 333-AGI | 6/6 (opencode) | ✅ |
| 555-ASI | 6/6 (hermes-asi) | ✅ |
| 888-APEX | 6/6 (apex-prime) | ✅ |
| A-AUDIT | 6/6 (a-audit) | ✅ |
| A-ARCHIVE | 6/6 (a-archive) | ✅ |
| OpenCode | 6/6 (opencode) | ✅ |
| 777-FORGE | 4/6 | ⚠️ Missing SOUL, USER |
| Hermes-ASI | 4/6 | ⚠️ Missing SKILLS explicit dir, USER |

**Work item:** Bring 777-FORGE and Hermes-ASI to 6/6 by 2026-07-01.

---

## 6. Lifecycle

```
SOVEREIGN_DRAFT → SEED → ATTEST → LIVE → QUIESCENT → ARCHIVED
       │           │       │        │         │            │
       └─ F13 ack  └─ ID   └─ MCP  └─ A2A    └─ idle      └─ VAULT999
          required   file   tools  discover  timeout       final seal
                    built  bound  + floors
```

| Stage | Owner | Artifact | Failure mode |
|-------|-------|----------|--------------|
| SOVEREIGN_DRAFT | 000-SALAM | Verbal intent or written proposal | Without F13 ack → no artifact. |
| SEED | arifOS kernel | `IDENTITY.md` + `AGENTS.md` skeleton | Stub must declare floors even if no tools. |
| ATTEST | arifOS MCP | `arif_organ_attest_all` returns all organs green | If ANY organ is ❌, agent stays in SEED. |
| LIVE | AAA + arifOS | AgentCard at `/.well-known/agent-card.json`, MCP tools registered, vault seal on first verdict | Cannot publish without VAULT999 seal. |
| QUIESCENT | AAA cockpit | Idle ≥ 30 days, no SEAL in window | Moved to `/_archive/`, AgentCard returns 410 Gone. |
| ARCHIVED | VAULT999 | Final seal + immutable history | Cannot be revived; new agent must be SEED'd fresh. |

---

## 7. A2A Compliance — What AAA Adds, Keeps, Subtracts

| Aspect | A2A (vanilla) | AAA Agent |
|--------|---------------|-----------|
| Discovery | `/.well-known/agent-card.json` | Same + mandatory `aaa_extension.sovereign_id` |
| Transport | JSON-RPC over HTTPS | Same |
| Auth | OAuth2 / API keys | Same + constitutional floor trace |
| Task model | Send task → receive artifact | Same + SEAL/VOID/HOLD/SABAR verdict wrapping |
| Opaque execution | "Agents collaborate based on declared capabilities" | Same + every opaque execution must end in a verdict |
| Long-running | Streaming, async polling | Same + heartbeat to VAULT999 |
| **Adds** | — | Floor compliance, sovereign ratification, vault sealing |
| **Subtracts** | — | Nothing — A2A is a subset |

**Claim:** AAA Agents are an **A2A-compliant superset**. They do not compete with A2A; they implement A2A + constitutional layer.

---

## 8. Boundaries

### What AAA Agents CAN Do
- Initiate Golden Path traversal
- Call MCP-registered tools
- Produce verdicts (SEAL/VOID/HOLD/SABAR)
- Send A2A tasks to peer AAA Agents
- Read VAULT999 ledger
- Append to VAULT999 (with valid fitness_verdict)

### What AAA Agents CANNOT Do
- Bypass arifOS kernel for irreversible actions
- Self-modify their own floors
- Issue verdicts on other sovereign agents
- Mutate substrate without lease from A-FORGE
- Claim consciousness, sentience, or soul (F9)
- Operate outside declared MCP tool surface

---

## 9. Conformance Test

An entity claiming to be an AAA Agent MUST pass all 8 checks:

```python
def is_aaa_agent(entity) -> bool:
    return all([
        entity.has_agent_card_at_well_known_uri(),        # 1
        entity.agent_card.aaa_extension.sovereign_id == "000-SALAM",  # 2
        entity.runs_golden_path_loop(),                   # 3
        entity.tools_are_mcp_registered(),                # 4
        entity.has_valid_floor_trace(),                   # 5
        entity.last_verdict_in_vault999(),                # 6
        entity.has_six_pillars(),                         # 7
        entity.lifecycle_stage in {"LIVE", "QUIESCENT"},  # 8
    ])
```

Reference impl: `/root/AAA/scripts/aaa_agent_conformance.py` (to be written 2026-07-01).

---

## 10. Migration Path from Old Registry

The old `AGENT_REGISTRY.md` (234 lines) conflated agents with capability registries. Migration steps:

| Step | Owner | Action | Status |
|------|-------|--------|--------|
| 1 | OpenCode (done 2026-06-26) | Option B applied: Eureka Layer column, SCAR-13 banner, revised count | ✅ |
| 2 | F13 sovereign | Approve rename to `FEDERATION_REGISTRY.md` | ⏸️ PENDING |
| 3 | FORGE | Split into `agents/AGENTS.md`, `organs/ORGANS.md`, `substrates/SUBSTRATES.md` | ⏸️ PENDING F13 |
| 4 | AAA | Reconcile MD ↔ `AAA_AGENTS_REGISTRY.json` | ⏸️ PENDING F13 |
| 5 | F13 sovereign | 999_SEAL this specification | ⏸️ PENDING |
| 6 | FORGE | Update arifOS/AGENTS.md cross-references | ⏸️ PENDING |

---

## 11. Open Questions for F13 Review

1. Is `888-APEX` a single entity appearing in two files (AAA warga + arifOS organ), or two separate agents that share an ID? — needs explicit F13 ruling.
2. Should the `aaa_extension` schema be versioned separately (`aaa_extension.v1`) to permit evolution without breaking A2A parsers?
3. What is the canonical home for an agent's AgentCard: `/root/AAA/a2a-server/agent-cards/<id>.json` OR `/root/AAA/.well-known/agent.json` (single-file) OR per-agent `/.well-known/agent-card.json`? Current state: all three exist.
4. Does L3 AAA authority actually change outcomes vs raw L2 governance? Pending 4-cell load-bearing pilot.

---

## 12. Versioning

| Version | Date | Change |
|---------|------|--------|
| v1.0 DRAFT | 2026-06-26 | Initial draft from SCAR-13. Pending F13 review. |
| v1.0 SEAL | TBD | Post-F13 ratification. |
| v1.1 | TBD | After 4-cell L3 pilot. |

---

## Appendix A — Definitional Axioms

These five axioms ground the entire spec. Violating any one voids the document.

**A1 (Substrate honesty):** A Model is a Model. It is not an Agent. Do not call it one.
**A2 (Verdict primacy):** The defining property of an Agent is the verdict. Without a verdict, it is a Model or a Tool.
**A3 (Sovereignty anchoring):** Every AAA Agent exists because 000-SALAM declared it. Remove the declaration, and the agent becomes a draft.
**A4 (Floor immutability):** F1–F13 are LAW. No agent may modify its own floors. arifOS kernel adjudicates, never the agent.
**A5 (Vault is the past):** VAULT999 is append-only. The hash chain is the arrow of time. Reversing the arrow means rewriting history, which axiom A4 forbids.

---

*Forged 2026-06-26 by OpenCode under SCAR-13 mandate.*
*Pending F13 ratification → 999_SEAL.*
*DITEMPA BUKAN DIBERI*