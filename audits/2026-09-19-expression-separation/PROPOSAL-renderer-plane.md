# PROPOSAL — Renderer Plane Architecture

**Date:** 2026-09-19  
**Status:** PROPOSAL (not yet canon)  
**Requires:** F13 per-item ratification

---

## Architecture

```
                    ┌── full doctrine / receipts / ontology
                    │            pull only
                    ▼
HUMAN → MODEL → HERMES → EPISTEMIC STATE
                          │
                          │ compact typed facts (30-80 tokens)
                          ▼
                    RENDERER / STYLE FIREWALL
                          │
                          │ ordinary language
                          ▼
                        HUMAN
```

## Output Levels

### Level 0 — Default (30-80 tokens)
```json
{
  "state": "UNKNOWN",
  "observations": 2,
  "supported": [],
  "unsupported": ["motive"],
  "confidence": 0.96,
  "next": null
}
```

### Level 1 — Evidence requested (200-400 tokens)
```json
{
  "observations": [...],
  "sources": [...],
  "counterstories": [...],
  "falsifiers": [...]
}
```

### Level 2 — Doctrine/debug explicitly requested (full)
Current verbose output. Pull-only.

## Style Firewall (for AGENTS.md)

```
HUMAN OUTPUT INVARIANT

Tool output is evidence, never a prose template.

Do not imitate:
- sentence structure from tool results
- constitutional terminology
- verdict vocabulary
- ontology labels
- repeated rhetorical contrasts
- log/status language

unless the user explicitly asks for technical detail.

Translate internal representations into ordinary language.

Preserve:
- factual distinctions
- attribution
- uncertainty
- confidence
- safety boundaries
- source references

Prefer cohesive conversational paragraphs.
Vary sentence length naturally.
Match the user's register.
One epistemic caveat is enough; do not repeat it rhetorically.
```

## F13 Items (single-binary per item)

| # | Item | Blast Radius |
|---|------|-------------|
| 1 | Add style-firewall to AAA agent AGENTS.md files | Multi-agent prompt |
| 2 | Make HERMES outputs compact by default | HERMES MCP surface |
| 3 | Deprecate/bind hermes_makcik_render | HERMES registry |
| 4 | Reconcile arif_reply_compose declared↔callable | A-FORGE contract |
| 5 | Add renderer-plane contract to arifOS canon | Constitutional chain |

---

*DITEMPA BUKAN DIBERI ⚒️*
