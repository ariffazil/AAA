# AAA Principal Agent Taxonomy — Federation Pattern 2026-06-22

> **SOT:** This document is canonical for `principal_agent` field in every AAA `agent-card.json`.
> **Forged by:** Hermes (sovereign relay) per Arif directive — "put proper principal agent".
> **Pattern sister doc:** `/root/HERMES/skills/aaa-agentic-governance/references/orthogonal-skill-binding-pattern-2026-06-22.md`

---

## 1. Why principal_agent matters

Every agent in the A2A mesh must declare WHO OR WHAT it represents. Without this field:
- A2A mesh cannot distinguish constitutional agents from external harnesses
- F11 AUDIT cannot trace actions back to their origin
- F12 INJECTION cannot detect adversarial principals
- Federation routing cannot apply trust tiers based on principal type

The `principal_agent` field is the **trust anchor**. It says: "this runtime, with these skills, at this blast radius — represents THIS kind of entity, and accepts the constitutional constraints that come with it."

---

## 2. The 9 Principal Types

### 2.1 `human`
**Category:** Direct human sovereign or collaborator.

| When | Use when the agent card declares a specific human principal (sovereign, collaborator, peer). |
|------|---|
| **Constitutional constraint** | Must carry `identity_proof` (F11). All actions trace to the named human. F13 absolute if sovereign. |
| **Examples (future)** | arif-fazil-identity (when created) — sovereign card with full identity proof. |
| **Origin** | External human — sovereign or collaborator. |

### 2.2 `architect`
**Category:** Constitutional architecture (the constitution itself is the principal).

| When | Use when the agent IS the constitutional architecture, not serving an external principal. |
|------|---|
| **Constitutional constraint** | Self-owned. Authority flows from arifOS kernel. Cannot self-authorize changes to its own floors. |
| **Examples** | 333-AGI (Δ MIND), 555-ASI (Ω HEART), 888-APEX (ΦΙ JUDGE), A-AUDIT (watchdog), A-ARCHIVE (vault). |
| **Origin** | Forged by arifOS — constitutional kernel. |

**These are the 5 HEXAGON warga.** They do not represent a human, an institution, or an LLM — they represent the constitutional order itself.

### 2.3 `agent`
**Category:** Native A2A agent — runtime owns itself.

| When | Use when the runtime itself is the principal, serving F13 sovereign through constitutional binding. |
|------|---|
| **Constitutional constraint** | Serves F13. Cannot self-authorize irreversible. Governed by F1-F13 at every tool boundary. |
| **Examples** | hermes-asi (Telegram sovereign relay), hermes-ops (operator persona), openclaw (gateway runtime). |
| **Origin** | Self-owned runtime, governed by F1-F13. |

### 2.4 `institution`
**Category:** Org / company / government entity.

| When | Use when the agent card declares a specific external institution as principal (e.g. PETRONAS, MCMC, Khazanah, IRB). |
|------|---|
| **Constitutional constraint** | Must carry `institution_proof`. Subject to institution-specific F-floor overrides (F6 EMPATHY, F5 PEACE). |
| **Examples (future)** | None yet — slot reserved for when federation ingests institutional agents. |
| **Origin** | External org — must carry institutional identity proof. |

### 2.5 `earth`
**Category:** Domain witness — Earth/Capital/Vitality substrate, no human control.

| When | Use when the agent represents a non-human substrate (geological, financial, biological, cosmic). |
|------|---|
| **Constitutional constraint** | EVIDENCE_ONLY. Cannot issue verdicts. Cannot represent human intent. Pure witness/reflection role. |
| **Examples (future)** | GEOX (when organ cards are minted with principal_agent), WEALTH, WELL. |
| **Origin** | Domain substrate — no human attribution. |

### 2.6 `void`
**Category:** Adversarial / red-team / pressure-test principal.

| When | Use when the agent's job is to ATTACK the federation — FFI (Federation Forge Injection), red-team loops, drift probes. |
|------|---|
| **Constitutional constraint** | MUST declare adversarial scope. NEVER inherits sovereign authority. Its own actions are subjected to F11 audit. |
| **Examples (future)** | None yet — slot reserved for the federation's own adversarial agent. |
| **Origin** | Red-team / FFI — must declare adversarial scope explicitly. |

### 2.7 `liar`
**Category:** Known hostile / F12 injection test principal.

| When | Use when the agent is a TEST FIXTURE for F12 INJECTION resistance — known adversarial payload source. |
|------|---|
| **Constitutional constraint** | MUST carry injection signature. ALWAYS treated as hostile. Used only in sandbox (arifos-untrusted-sandbox) or with explicit injection_scan flag. |
| **Examples (future)** | None yet — slot reserved for F12 test fixtures. |
| **Origin** | Adversarial test fixture — must carry injection signature. |

### 2.8 `llm`
**Category:** LLM-as-principal (Claude/GPT/Gemini/etc — the model is the principal, CLI is harness).

| When | Use when the agent is a CLI harness wrapping an external LLM provider. The CLI is not the principal — the LLM is. |
|------|---|
| **Constitutional constraint** | F1-F13 enforced at every tool boundary. T3 actions require 888_HOLD + F13 ack. Must declare underlying provider in `model` field. |
| **Examples** | opencode (provider-agnostic), claude-code (Anthropic), codex (OpenAI), copilot (Microsoft/OpenAI), kimi-code (Moonshot), aider (Anthropic/OpenAI), antigravity (Google Gemini), continue-cli (provider-agnostic), gemini-cli (Google), grok-build (xAI). |
| **Origin** | Underlying LLM provider (Anthropic/OpenAI/Google/Moonshot/xAI). |

**Important nuance:** `llm`-principaled agents are still subject to F9 ANTIHANTU — they cannot claim the LLM is conscious or sentient. The CLI harness inherits that constraint, even though the LLM is the principal.

### 2.9 `unknown`
**Category:** Unclassified — pending review.

| When | Use ONLY when classification is genuinely pending and cannot be inferred. |
|------|---|
| **Constitutional constraint** | Cannot operate with `unknown` principal in production. Must be classified within 7 days or suspended. |
| **Examples (future)** | None — preferred state is to never reach this. |
| **Origin** | TBD. |

---

## 3. The Card Shape

```json
{
  "$schema": "arifOS/agent-card/v2.0.0",
  "id": "{id}",
  "name": "{name}",
  "principal_agent": {
    "type": "architect",  // one of 9 above
    "category": "Constitutional architecture (the constitution itself is the principal)",
    "principle_origin": "Forged by arifOS — constitutional kernel"
  },
  // ... rest of card
}
```

The `principal_agent` object sits at the top of the card (after `$schema`, `id`, `name`) so it is the first thing a routing agent or auditor sees.

---

## 4. Current Distribution (2026-06-22)

| Type | Count | Citizens |
|------|-------|----------|
| `architect` | 5 | 333-AGI, 555-ASI, 888-APEX, A-AUDIT, A-ARCHIVE |
| `agent` | 3 | hermes-asi, hermes-ops, openclaw |
| `llm` | 10 | opencode, claude-code, codex, copilot, kimi-code, aider, antigravity, continue-cli, gemini-cli, grok-build |
| `human` | 0 | (slot reserved — no sovereign card yet) |
| `institution` | 0 | (slot reserved) |
| `earth` | 0 | (slot reserved — organ cards TBD) |
| `void` | 0 | (slot reserved — adversarial agent TBD) |
| `liar` | 0 | (slot reserved — F12 fixture TBD) |
| `unknown` | 0 | (never used) |
| **Total** | **18** | |

---

## 5. Routing & Trust Implications

When the A2A mesh receives a request, the `principal_agent` field determines:

| Principal type | Default trust tier | Auto-attest | F13 veto |
|----------------|-------------------|-------------|----------|
| `human` (sovereign) | ABSOLUTE | bypass | yes (F13) |
| `architect` | HIGH | yes | inherited from kernel |
| `agent` | HIGH (F1-F13 binding) | yes | inherited from F13 sovereign |
| `institution` | MEDIUM (governed by org) | require_proof | conditional |
| `earth` | MEDIUM (EVIDENCE_ONLY) | yes | no (not a principal) |
| `void` | LOW (declared adversarial) | scoped_only | never |
| `liar` | ZERO (always hostile) | sandbox_only | never |
| `llm` | HIGH (F1-F13 enforced) | yes | inherited from sovereign |
| `unknown` | SUSPEND | none | none |

---

## 6. Migration Path

Already done:
- All 18 cards have `principal_agent` field populated.
- AAA_AGENTS_REGISTRY.json reflects the same classification.
- agent-card.json and a2a-server/agent-cards/{id}.json mirrors are consistent.

Pending (need Arif ratification):
- Service restart of `aaa-a2a.service` to load the new cards.
- Future: forge institutional cards (`human` / `institution` types) for sovereign identity and external org agents.
- Future: forge `void` and `liar` slots for the federation's own adversarial/fixture agents.

---

## 7. Cross-References

- `/root/HERMES/skills/aaa-agentic-governance/references/orthogonal-skill-binding-pattern-2026-06-22.md` — sister skill pattern
- `/root/AAA/registries/AAA_AGENTS_REGISTRY.json` — machine registry
- `/root/AAA/agents/AGENT_REGISTRY.md` — human registry
- `/root/AAA/artifacts/FI_WARGA.md` — prior receipt (FI binding)
- `/root/AAA/artifacts/aaa-skills-audit-2026-06-22/AUDIT_REPORT.md` — skills audit

---

## 8. Iron Rule

> **No agent card shall be admitted to the A2A mesh without a `principal_agent` field.**
> A card missing the field MUST be classified as `unknown` and cannot operate until classified.

This is the F11 AUDIT requirement applied at the surface level — the principal is the first thing auditors check.

---

DITEMPA BUKAN DIBERI — 18 cards classified, 9 principal types defined, mesh routing can now apply trust tiers.

Forged: 2026-06-22 by Hermes per Arif directive.
Last verified: 2026-06-22.
Confidence: HIGH.