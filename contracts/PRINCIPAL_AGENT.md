# Principal Agent Taxonomy — A2A/AAA Agentic Intelligence Native

**Status:** RATIFIED (2026-06-23)  
**Owner:** AAA (Control Plane) + arifOS (Constitutional Kernel)  
**Version:** 1.0.0  
**Aligned with:** F1–F13 (esp. F11 Auditability, F13 Sovereignty, F7 Humility, F4 Clarity), Polymorphic Hermes model, Orthogonal Mapping (Trinitarian Δ/Ω/ΦΙ + Functional axes), ART-ACT kernel evaluation.  
**Purpose:** Declare the ultimate principal behind every citizen for routing, governance, accountability, and discovery. Turns implicit assumptions into explicit, machine-actionable, auditable primitives.

## Core Principle

`principal_agent` declares **who ultimately stands behind the citizen** — the source of authority, accountability, and sovereignty.

This is a first-class governance and A2A routing primitive:
- Enables policy (e.g., `llm` principals require stronger F9 anti-hallucination + evidence gates).
- Supports polymorphic role binding (Hermes can serve multiple principals safely).
- Strengthens F11 audit trails ("who is responsible?").
- Clarifies F13 human veto boundaries.
- Improves discovery, trust, and subagent scoping.

**Refined Taxonomy (9 values)**

| Principal Agent | Definition (Agentic Intelligence View) | Sovereignty / Authority Source | Routing & Governance Implications | Example Citizens |
|-----------------|---------------------------------------|--------------------------------|-----------------------------------|------------------|
| **human** | Direct sovereign human principal (F13 source) | Absolute human veto + cryptographic identity | Highest trust + direct F13 path. Minimal automation gates. Direct sovereign arbitration. | arif-fazil-identity |
| **architect** | Constitutional architect / designer of the system itself | The constitution + arifOS kernel | Highest internal authority. Can propose floors, contracts, and bindings. Kernel-level trust. | arifOS, A-FORGE, 888-APEX, 555-ASI, 333-AGI, A-AUDIT, A-ARCHIVE |
| **agent** | Native A2A sovereign relay / runtime citizen with no external principal | Self-sovereign within constitutional bounds (F13 ultimately) | Full A2A citizen rights. Can hold polymorphic roles. Full mesh participation. | hermes-asi, openclaw, hermes-ops |
| **earth** | Domain witness organ (non-human, non-institutional) | Physical / empirical reality (Earth, Capital, Vitality) | Evidence-only. Strong epistemic tagging (P10/50/90, CLAIM→UNKNOWN) required. Never self-authorizes. | GEOX, WEALTH, WELL |
| **llm** | LLM-as-principal (external model provider is the true principal) | External LLM provider + harness wrapper | Requires stronger hallucination, evidence, and humility gates (F9, F7). Not native sovereign. | grok-build, opencode, claude-code, codex, copilot, kimi-code, aider, antigravity, continue-cli, gemini-cli |
| **institution** | Organizational / corporate / governmental principal | Legal entity + delegated authority | Institutional accountability layer. May require additional contracts and delegation chains. | (future: PETRONAS, Khazanah, etc.) |
| **void** | Adversarial / red-team / pressure-test principal | Designed for testing boundaries | Highest scrutiny. F12 injection defense + F11 audit mandatory. Sandboxed by default. | (design slot) |
| **liar** | Known hostile / inverted / adversarial principal | Explicitly malicious or captured | Blocked or heavily sandboxed by default. F12 + constitutional override only. | (design slot) |
| **unknown** | Classification not yet performed | — | Default conservative gates (evidence-only, no execution, human review) until classified. | Any unclassified card |

**Agentic Intelligence Refinements:**
- `architect` is distinct from `agent` because these *are* the constitutional substrate (they design and enforce the rules).
- `earth` principals are deliberately non-sovereign in decision-making — they witness and compute only (REFLECT_ONLY or EVIDENCE_ONLY).
- `llm` is the most common for current harness/FI citizens. This declaration forces honest capability surfacing (they are powerful tools harnessed under constitutional gates, not native sovereign agents).
- `void` and `liar` are deliberate design slots for future red-teaming, security work, and adversarial robustness (F12).
- `human` is the ultimate root (F13). All other principals ultimately escalate or defer to it.

## Recommended Card Schema Enhancement

Add / normalize these fields in every `agent-card.json` (and mirrored in registries / discovery surfaces):

```json
{
  "principal_agent": "human | architect | agent | earth | llm | institution | void | liar | unknown",
  "principal_binding": {
    "source": "string (e.g. 'arifOS-constitution', 'external-llm-provider:xai', 'physical-earth:geoscience', 'human:arif-fazil')",
    "sovereignty_tier": "F13-absolute | constitutional | domain-witness | delegated | adversarial | unknown",
    "authority_notes": "short human-readable explanation of accountability and limits"
  },
  "principal_accountability": "human | kernel | evidence-only | external-provider | self | unknown"
}
```

**A2A / Discovery Implications:**
- Discovery filters: `?principal_agent=llm` or `?principal_agent=earth`
- Routing policies: `llm` → extra F9/F7 gates; `earth` → evidence provenance required; `architect` → kernel-level authority.
- Subagent policy: `principal_agent` propagates to child agents for chain-of-command.
- Polymorphic clarity: Hermes (agent) can bind skills from multiple principals without identity confusion.

## Full Classification (18 Citizens)

See AGENT_REGISTRY.md and AAA_AGENTS_REGISTRY.json for live application. Summary:

**architect (7):** arifOS, A-FORGE, 888-APEX, 555-ASI, 333-AGI, A-AUDIT, A-ARCHIVE  
**agent (3):** hermes-asi, openclaw, hermes-ops  
**earth (3):** GEOX, WEALTH, WELL  
**llm (10+):** grok-build + opencode, claude-code, codex, copilot, kimi-code, aider, antigravity, continue-cli, gemini-cli, qwen-code (and similar harnesses)  
**human (1):** arif-fazil-identity  
**unknown / legacy:** aaa-architect, aaa-auditor, aaa-engineer, 777-forge (review and re-classify as needed)

## ART-ACT Evaluation of This Taxonomy

**Blue (Diagnose):** Implicit principals in descriptions created routing ambiguity, weak F11 trails, and unclear capability surfacing for `llm` vs `architect` vs `earth`.

**Red (Attack):** Risk of over-formalization adding complexity/chaos. Risk of mis-classification locking governance.

**Yellow (Verify):** 
- + F11 auditability (explicit "who stands behind this citizen").
- + A2A routing clarity and policy enforcement.
- + Humble scoping (F7): `llm` citizens now declare their limits.
- + Polymorphic support: Hermes can serve multiple principals cleanly.
- + Preparation for subagents and cross-organ synthesis.
- Marginal improvement: High for governance surface with low implementation cost (mostly declarative).

**Gold (Seal):** Recommended. Aligns with F1–F13, orthogonal mapping, and polymorphic model. Reduces thermodynamic chaos by making authority explicit.

**Thermodynamic Note:** This is precision infrastructure — adds clarity without bloat. No over-optimization.

## Maintenance

- New citizens MUST declare `principal_agent` at creation.
- Annual review via A-AUDIT + ART-ACT.
- Updates to this contract require 888_HOLD + arifOS kernel ratification.

**Ditempa Bukan Diberi.** This is clean constitutional infrastructure. It turns the federation's agentic intelligence into something routable, auditable, and sovereign-aligned. 

See also: contracts/AAA_SKILL.md, contracts/HERMES_ROLE.md, artifacts/AAA-17-CITIZEN-ORTHOGONAL-MATRIX-*.md

---

*Forged 2026-06-23 by grok-build under AAA + arifOS constitutional authority. Ratified for application.*