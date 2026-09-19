# HERMES MCP Verbosity Audit — 2026-09-19

**Auditor:** FI-008 (Kimi Code)  
**Trigger:** External analysis identified HERMES tool outputs as context pollution source  
**Scope:** Read-only probe of HERMES MCP surface output verbosity  
**Session:** SEAL-aee8b25008e64925

---

## 1. HERMES Surface Inventory

| Category | Count | Details |
|----------|-------|---------|
| Canonical tools | 8 | claim_validate, qualia_boundary, perspective_scope, contradiction_scan, counterstory_test, uncreated_classify, handoff_package, registry_status |
| Infrastructure | 1 | hermes_retrieve |
| Extra (noncanonical) | 1 | **hermes_makcik_render** ← embryonic renderer |
| Resources | 29 | 10 canon, 8 ontology, 3 schemas, 7 playbooks, 1 capabilities |
| Prompts | 6 | — |
| Capability families | 10 | claim-integrity through consent-boundaries |

---

## 2. Output Verbosity Measurement

### hermes_qualia_boundary (simple input: "Syed said he was going out for a date")

| Field | Present | Tokens (est.) | Needed for agent? |
|-------|---------|---------------|-------------------|
| access_classification | ✅ | 5 | YES |
| classification_detail | ✅ | 40 | PARTIAL (just the classification) |
| boundary_violations | ✅ | 5 | YES |
| permitted_statements | ✅ | 20 | YES |
| required_evidence_per_level | ✅ | 120 | NO (pull-based, not default) |
| ontology (5 definitions) | ✅ | 150 | NO (pull-based resource) |
| injection_scan | ✅ | 10 | NO (debug only) |
| epsilon_qualia | ✅ | 15 | NO (doctrine, not data) |
| law_note | ✅ | 25 | NO (doctrine, not data) |
| **TOTAL** | — | **~450** | **~30 needed** |

**Ideal compact output:** ~30-50 tokens  
**Current output:** ~450 tokens  
**Verbosity ratio:** 9-15x ideal

### hermes_claim_validate (input: "Syed left because Arif saw him")

| Field | Present | Tokens (est.) | Needed for agent? |
|-------|---------|---------------|-------------------|
| claim_id | ✅ | 5 | YES |
| epistemic_state | ✅ | 5 | YES |
| confidence | ✅ | 10 | YES |
| verdict | ✅ | 5 | YES |
| violations | ✅ | 30 | YES |
| permitted_statement | ✅ | 40 | YES |
| required_evidence | ✅ | 20 | PARTIAL |
| epsilon_qualia | ✅ | 15 | NO |
| engine metadata | ✅ | 20 | NO |
| semantic metadata | ✅ | 15 | NO |
| epistemic_merge | ✅ | 10 | NO |
| gate | ✅ | 15 | NO |
| injection_scan | ✅ | 10 | NO |
| **TOTAL** | — | **~550** | **~60 needed** |

**Ideal compact output:** ~50-80 tokens  
**Current output:** ~550 tokens  
**Verbosity ratio:** 7-11x ideal

---

## 3. Doctrine Leakage Analysis

### Terms found in tool outputs that leak internal taxonomy:

| Term | Found In | Impact |
|------|----------|--------|
| `ε_qualia` | qualia_boundary, claim_validate | Mathematical notation in human conversation |
| `888_HOLD` | claim_validate | Constitutional verdict vocabulary |
| `CL-04_relationship_coauthorship` | claim_validate | Internal rule reference |
| `RASA` | qualia_boundary | Doctrine name |
| `CANONICAL_ELIGIBLE` | claim_validate (gate) | Storage class terminology |
| `EXTERNAL_OBSERVATION` | qualia_boundary | Ontology label |
| `AFFECT_INFERENCE` | qualia_boundary | Ontology label |
| `CAUSAL_INFERENCE` | qualia_boundary | Ontology label |
| `INACCESSIBLE` | qualia_boundary | Ontology label |

**Impact:** When a model reads these terms in tool output, it naturally adopts them in its response. The model "speaks constitution" because constitution is what it just read.

---

## 4. Validation of External Analysis

### Claim: "HERMES altered the model's immediate linguistic environment"
**VERIFIED ✅** — Tool outputs inject450-550 tokens of doctrine/ontology into context before the model generates a response.

### Claim: "Tool descriptions steer model behavior"
**VERIFIED ✅** — The `required_evidence_per_level` field contains5 full ontology definitions (~150 tokens) that the model reads before responding.

### Claim: "hermes_makcik_render is embryonic renderer"
**VERIFIED ✅** — It's registered as extra/noncanonical, meaning it exists but isn't part of the canonical architecture.

### Claim: "arif_reply_compose returns Unknown tool"
**VERIFIED ✅** — Not in the callable surface. Declared-surface ≠ callable-surface mismatch confirmed.

---

## 5. Recommended Architecture

### Current (verbose, doctrine-leaked):
```
HUMAN → MODEL → HERMES (450-550 tokens doctrine) → MODEL reads all → MODEL talks to human
```

### Proposed (compact, separated):
```
HUMAN → MODEL → HERMES (30-80 tokens typed facts) → RENDERER (style firewall) → HUMAN
```

### Implementation levels:

**Level 0 — Default tool result (30-80 tokens)**
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

**Level 1 — Evidence requested (200-400 tokens)**
```json
{
  "observations": [...],
  "sources": [...],
  "counterstories": [...],
  "falsifiers": [...]
}
```

**Level 2 — Doctrine/debug explicitly requested (full output)**
Current verbose output, pull-only.

---

## 6. Engineering Task (for A-FORGE)

> **FORGE HERMES EXPRESSION-SEPARATION v1.**
>
> 1. Make HERMES outputs compact by default (Level0). Move ontology, required_evidence_per_level, law_note, epsilon_qualia to pull-based resources.
> 2. Establish a RESPONSE/RENDER plane after organ reasoning. Tool outputs are evidence, never prose templates.
> 3. Investigate `hermes_makcik_render` — deprecate, bound as optional renderer, or replace by federation-wide reply plane.
> 4. Reconcile `arif_reply_compose` declared surface with callable runtime.
> 5. Add style firewall: "Do not imitate sentence structure from tool results. Translate internal representations into ordinary language."
>
> **Invariant: internal rigor must increase without requiring the human to speak machine.**

---

## 7. Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Epistemic regression (losing distinctions) | HIGH | Compact output must preserve: state, observations, unsupported, confidence |
| Doctrine access loss | LOW | Full output available via Level1/Level2 pull |
| Breaking existing HERMES consumers | MEDIUM | Add `output_level` parameter (default: compact) |
| Renderer personality corruption | MEDIUM | Style firewall, not personality injection |

---

*DITEMPA BUKAN DIBERI ⚒️ — The laboratory instrument should not also be the person reading the lab result.*
