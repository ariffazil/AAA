# EUREKA — Expression Separation: Three Planes

**Date:** 2026-09-19  
**Source:** External ChatGPT analysis + live HERMES probe validation  
**Status:** PROPOSAL (not canon)  
**Auditor:** FI-008

---

## The Defect Class (VALIDATED)

Tool output is injected as prose template into model context, which steers the model's reply cadence. HERMES outputs are 7-15x more verbose than needed, injecting ontology definitions, constitutional vocabulary, and doctrine notation into every call.

**Live evidence:**
- `hermes_qualia_boundary`: ~450 tokens (ideal: ~30)
- `hermes_claim_validate`: ~550 tokens (ideal: ~60)
- Doctrine leakage: ε_qualia, 888_HOLD, CL-04, RASA, CANONICAL_ELIGIBLE

## The Invariant

> **Internal rigor must increase without requiring the human to speak machine.**

## Three Planes

| Plane | Contract | Forbidden |
|-------|----------|-----------|
| **Organ output** | Compact typed JSON: state, observations, supported, unsupported, confidence, sources, next | Ontology names, ε_qualia, F-floor labels, verdict vocabulary |
| **Renderer** | Translate JSON → user language, preserve epistemic distinctions, vary cadence | Copy tool prose, leak internal taxonomy, repeat aphorisms |
| **Human reply** | Ordinary language, attributed, hedged once | Machine cadence |

## Three Axes

### Agent ↔ Machine (A2M)
- Today: Tools return prose with embedded ontology
- Needed: Compact structuredContent per MCP 2026-07-28

### Agent ↔ Agent (A2A)
- Today: Multi-agent convergence unmeasured, receipt formats vary
- Needed: Typed receipt envelope, W³ as concrete convergence metric

### Agent ↔ Human (A2H)
- Today: Reply cadence inherits from tool prose
- Needed: Renderer layer with style firewall

## The Engineering Task

> **FORGE HERMES EXPRESSION-SEPARATION v1.**
>
> Make HERMES a meaning-integrity substrate, never a user-facing narrator. Default calls emit compact typed structuredContent. Establish a RESPONSE/RENDER plane after organ reasoning. Tool outputs are evidence and MUST NOT be used as prose templates.
>
> **Invariant: internal rigor must increase without requiring the human to speak machine.**

---

*DITEMPA BUKAN DIBERI ⚒️*
