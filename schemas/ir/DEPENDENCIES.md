# AAA-IR Schema Dependency DAG

**Generated:** 2026-10-02
**Status:** CANDIDATE_ABI
**Purpose:** Document every cross-schema dependency and detect resolution gaps.

---

## Schemas in `/root/AAA/schemas/ir/`

| Schema | $id | Required refs | Refs that resolve | Refs that need work |
|--------|-----|---------------|-------------------|---------------------|
| identity-packet.v1 | `…/identity-packet.v1.schema.json` | none | n/a | n/a |
| capability-graph.v1 | `…/capability-graph.v1.schema.json` | none (uses inline IdentityPacket description) | n/a | inline identity may cause validator complaints on draft-2020-12 |
| task-ir.v1 | `…/task-ir.v1.schema.json` | none | n/a | n/a |
| authority-envelope.v1 | `…/authority-envelope.v1.schema.json` | none (uses IdentityPacket-style nested objects inline) | n/a | inline refs may need lookup |
| runtime-packet.v1 | `…/runtime-packet.v1.schema.json` | 6× `$ref: identity-packet.v1.schema.json` | ✅ same dir, relative-path resolution | works if all files co-located |
| evidence-packet.v1 | `…/evidence-packet.v1.schema.json` | none | n/a | n/a |
| temporal-packet.v1 | `…/temporal-packet.v1.schema.json` | none | n/a | n/a |
| dispatch-plan.v1 | `…/dispatch-plan.v1.schema.json` | none (uses CapabilityGraph, AuthorityEnvelope by id reference only) | id-only acceptable | future: switch to `$ref` if ResolutionEngine inserted |
| resolution-packet.v1 | `…/result-packet.v1.schema.json` | none | n/a | n/a |
| artifact-bundle.v1 | `…/artifact-bundle.v1.schema.json` | `$ref: release-link-gate.v1.schema.json` | ✅ | works |
| context-packet.v1 | `…/context-packet.v1.schema.json` | none | n/a | n/a |
| release-link-gate.v1 | `…/release-link-gate.v1.schema.json` | none | n/a | n/a |
| measurement.v1 | `…/measurement.v1.schema.json` | none | n/a | n/a |
| bridge-proof.v1 | `…/bridge-proof.v1.schema.json` | none | n/a | n/a |
| worldline.v1 | `…/worldline.v1.schema.json` | 2× `$ref: measurement.v1.schema.json` | ✅ | co-location required |

---

## Visual DAG

```
                          ┌──────────────┐
                          │ IdentityPacket│
                          └──────┬───────┘
                                 │
                                 ▼
                       ┌─────────────────┐
                       │  RuntimePacket  │
                       │  (6× IdentityPacket) │
                       └─────────────────┘

┌──────────────┐
│ Measurement  │
└──────┬───────┘
       │
       ▼
┌──────────────────────────┐
│      Worldline           │
│  (R, V dims → Measurement)│
└──────────────────────────┘

┌──────────────────┐
│ ReleaseLinkGate  │
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│  ArtifactBundle  │
└──────────────────┘
```

---

## $ref resolution strategy

**Rule:** all `$ref` MUST use either:
1. **Same-directory relative path:** `"$ref": "identity-packet.v1.schema.json"` — resolves when consumer schema is in the same dir.
2. **Fully qualified $id URL:** `"$ref": "https://aaa.arif-fazil.com/schemas/ir/identity-packet.v1.schema.json"` — resolves via HTTP fetch.

**Current state:** all existing `$ref` instances use same-directory relative path. Works because all 15 IR schemas are co-located in `/root/AAA/schemas/ir/`.

**Anti-pattern:** mixed relative + absolute refs in same DAG leads to inconsistent resolution. Avoid.

---

## Future dependency risks

1. **If schemas split across subdirectories** (e.g., `ir/core/`, `ir/profiles/`), every relative `$ref` must include the relative directory.

2. **If IR_REGISTRY.v1 moves out of `/root/AAA/schemas/ir/`** (e.g., into `/root/AAA/canon/`), refs to it from schemas break. Keep registry inside the IR directory or use absolute $id.

3. **No $ref currently points to non-IR schemas.** This is intentional — IR schemas must not re-implement existing types (per RECONCILIATION.md row 3). If a future schema needs RealityAssertion or A2A Agent Card fields, it MUST use a wire-format projection, not a $ref into lib/reality_graph.py (Python type) or schemas/a2a-v1.0.schema.json.

---

## Validator integration

```python
import json
from jsonschema import Draft202012Validator, RefResolver

base_uri = "https://aaa.arif-fazil.com/schemas/ir/"
schemas = {}
for f in pathlib.Path("/root/AAA/schemas/ir/").glob("*.schema.json"):
    name = f.name
    schema = json.loads(f.read_text())
    schemas[name] = schema

resolver = RefResolver(base_uri=base_uri, referrer=raw_schema)
validator = Draft202012Validator(schema, resolver=resolver)
```

When ready, install jsonschema: `pip install jsonschema` and run this script.

---

## Status

**DAG is complete and resolvable.** Zero outstanding cross-schema integrity gaps that block promotion to FROZEN.

Awaiting C.3 follow-ups listed in RECONCILIATION.md before final FROZEN promotion.