# AAA Semantic File Map

> **Purpose:** stop duplication, stop drift, stop "same idea in four files."
> **Rule:** one meaning, one home, many readers.
> **Status:** LIVE

---

## Zen

### Zen of AAA

- AAA is the control plane, not the kernel, not the executor.
- AAA names things, routes things, and makes boundaries visible.
- AAA should prefer indexes, registries, schemas, and contracts over narrative sprawl.
- If two files claim the same authority, one of them is wrong.

### Zen of Python

- Python executes the runtime truth.
- Python owns verification, intake, signing, gating, and mutation logic.
- If behavior is real, eventually it must exist in Python or TypeScript, not just in Markdown.

### Zen of JSON

- JSON is for machine contracts.
- A JSON schema defines shape, invariants, and validation boundaries.
- If another component must parse it, the contract belongs in JSON schema.

### Zen of YAML

- YAML is for human policy.
- YAML chooses routes, tiers, scopes, and triggers.
- If an operator needs to read and change policy safely, YAML is the right home.

---

## Semantic Rule

Use this test before creating a file:

1. Is this **policy**? Put it in YAML.
2. Is this **shape/validation**? Put it in JSON schema.
3. Is this **runtime behavior**? Put it in Python or TypeScript.
4. Is this **discovery/indexing**? Put it in a registry.
5. Is this **explanation only**? Put it in docs, and point to the canonical file.

If a new file fails this test, do not create it.

---

## Canonical Map

| Meaning | Canonical File | Why it lives there |
|---|---|---|
| AAA coding doctrine / Zen of agentic Python | `/root/AAA/skills/AAA_ZEN.md` | Doctrine for coding agents; human-readable rules |
| Event-to-skill routing policy | `/root/AAA/triggers/trigger-map.yaml` | Human-editable trigger policy; Day 1 canonical wire |
| Signed ingress capsule contract | `/root/AAA/core/capsule.py` | Runtime CAPSULE and A2A envelope model live here |
| Capsule schema registry entry | `/root/AAA/schemas/signed-capsule.schema.json` | Machine-validated envelope shape and contract |
| Schema discovery index | `/root/AAA/schemas/SCHEMA_REGISTRY.json` | Registry for schema lookup |
| Sovereign + organ DID provisioning | `/root/AAA/auth/gen_did.py` | Day 1 canonical DID generator and registry writer |
| DID registry | `/root/AAA/auth/did_registry.yaml` | Committed public-key registry for all organs |
| HTTP webhook surface | `/root/arifOS/arifosmcp/runtime/webhook_router.py` | FastAPI ingress route definition |
| Webhook verification + idempotency + intake logic | `/root/arifOS/arifosmcp/runtime/webhook_intake.py` | Runtime truth for source verification |
| Signed capsule append helper | `/root/arifOS/VAULT999/sign_capsule_to_vault.py` | Bridge from signed capsule into VAULT999 sink |
| Human explanation of crypto slice | `/root/AAA/docs/CRYPTO_ATTESTATION_SLICE_0001.md` | Explanation layer, not runtime authority |
| Federation code/infrastructure overview | `/root/AAA/docs/federation-code-map.md` | Broad topology map |
| MCP endpoint source of truth | `/root/AAA/docs/mcp-endpoint-registry.md` | Endpoint registry, not ingress policy |

## Archive Queue

Legacy bootstrap/demo paths are documented once, in:

- `/root/AAA/docs/archive/CRYPTO_ATTESTATION_BOOTSTRAP_ARCHIVE.md`

---

## Boundary Rules

### Do not put routing policy in Python comments

Routing belongs in:
- `/root/AAA/triggers/trigger-map.yaml`

Python may consume it. Python should not become the only place it exists.

### Do not put schema rules in Markdown prose

Validation belongs in:
- `/root/AAA/schemas/*.schema.json`

Docs may explain the schema. Docs are not the validator.

### Do not put runtime truth in YAML

Verification, HMAC, nonce handling, idempotency, and append behavior belong in:
- `/root/arifOS/arifosmcp/runtime/webhook_intake.py`
- `/root/arifOS/VAULT999/sign_capsule_to_vault.py`

YAML declares intent. Python enforces it.

### Do not create a second "canonical" doc for the same surface

If a concept already has:
- a policy file
- a schema
- a runtime implementation

then the next file should be an index or explanation only.

---

## Ingress Stack, By Layer

| Layer | File Type | Canonical File |
|---|---|---|
| Policy | YAML | `/root/AAA/triggers/trigger-map.yaml` |
| Contract | JSON schema | `/root/AAA/schemas/signed-capsule.schema.json` |
| Route | Python | `/root/arifOS/arifosmcp/runtime/webhook_router.py` |
| Verification | Python | `/root/arifOS/arifosmcp/runtime/webhook_intake.py` |
| Audit append | Python | `/root/arifOS/VAULT999/sign_capsule_to_vault.py` |
| Discovery | JSON registry | `/root/AAA/schemas/SCHEMA_REGISTRY.json` |
| Explanation | Markdown | `/root/AAA/docs/CRYPTO_ATTESTATION_SLICE_0001.md` |

Shortest mnemonic:

- `yaml decides`
- `json constrains`
- `python executes`
- `vault remembers`

---

## Anti-Chaos Checks

Before adding a new file, ask:

- Does a file with this meaning already exist?
- Am I adding behavior, or only another explanation?
- Can this be a registry entry instead of a new implementation?
- Can this be one paragraph in this map instead of another doctrine file?

If the answer is "yes, it already exists," update the existing file or this map.
