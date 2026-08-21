---
id: FORGE-governance-jsonld
name: FORGE-governance-jsonld
version: 1.0.0-2026.07.17
description: "Governance JSON-LD — constitutional ontology and semantic governance context definitions."
owner: A-FORGE
risk_tier: medium
floor_scope: ['F1', 'F2', 'F4', 'F11']
autonomy_tier: T1
---
# ⚒️ Governance JSON-LD — Constitutional Ontology

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Generate and maintain `/.well-known/governance.jsonld` — machine-readable constitutional ontology expressing the 13 floors (F1–F13), federation organs, action classes, epistemic labels, and authority tiers as linked data.

## When to Use
- Creating or updating `governance.jsonld` for any federation subdomain
- Adding new constitutional terms, floors, or organ definitions to the ontology
- Validating JSON-LD framing and @context resolution
- Integrating with external DID and governance-aware agents

## When NOT to Use
- DID identity — use `did-web-identity`
- Federation topology — use `federation-manifest`
- Human-readable governance docs — write to /root/AAA/governance/

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | Ontology terms are append-only; deprecation replaces deletion |
| F2 TRUTH | Every term has a human-readable definition; no opaque IRIs without explanation |
| F4 CLARITY | One ontology namespace per organ; no overlapping term definitions |
| F11 AUDIT | JSON-LD version history tracked alongside seal chain |
| F13 SOVEREIGN | Floor definitions immutable once sealed in VAULT999 |

## Commands & Patterns

```jsonc
// /.well-known/governance.jsonld — canonical structure
{
  "@context": {
    "@vocab": "https://arifos.arif-fazil.com/ontology/v1#",
    "f1": "https://arifos.arif-fazil.com/ontology/v1#F1_AMANAH",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "did:web:arif-fazil.com",
  "@type": "ConstitutionalFederation",
  "floors": [
    {
      "@id": "f1:amanah",
      "name": "AMANAH",
      "description": "Every mutation reversible or backed up",
      "ordinal": 1,
      "maxConfidence": 0.90,
      "actionClasses": ["MUTATE", "IRREVERSIBLE"]
    },
    // F2–F13 follow same pattern
  ],
  "organs": [
    {
      "@id": "organ:arifos",
      "name": "arifOS",
      "role": "constitutional_kernel",
      "port": 8088
    }
  ],
  "epistemicLabels": ["OBS", "DER", "INT", "SPEC"],
  "authorityTiers": ["T1_AUTO_DO", "T2_ANNOUNCE", "T3_888_HOLD"]
}
```

## Refusal Surface
- ❌ Including runtime state in governance ontology (static by design)
- ❌ Duplicating `did.json` service endpoints here — reference by @id
- ❌ Removing terms that appear in any seal chain entry
- ❌ Non-deterministic `@id` generation (must be reproducible IRIs)
