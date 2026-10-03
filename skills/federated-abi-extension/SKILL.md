---
name: federated-abi-extension
description: Extend federated typed ABI without semantic duplication.
---

# Federated Typed-ABI Extension

How to add a new schema, packet type, or contract to a federated typed-ABI directory (e.g. `/root/AAA/schemas/ir/`) **without manufacturing semantic duplication, parallel enums, or contested provenance**. The destination is one machine-enforced ABI; the discipline is reconcile-before-extend.

## When this skill applies

- Adding a new JSON Schema / Protobuf / typed contract to a registry that already has N contracts (schemas/ir/, a2a-v1.0, peer-federation-contract, etc.)
- Proposing a new enum or classification that could overlap with an existing one (epistemic_class, status, comparability, relation, probe_state)
- Discovering that the new contract will be touched by concurrent workers / parallel agents / sibling sessions
- Routing a doctrine that wants its own ontology (e.g. "we need a ClaimRecord") when existing canon already has the field under a different name (RealityAssertion)

## Hard rules (each is a lesson, not procedural nicety)

### Reconcile before extending

Before writing a new schema file, run a **reconciliation matrix**:

```
existing canon → new schema → conflict → decision
```

Three outcomes:
1. **No overlap** → proceed (but still CANDIDATE_ABI status until promotion).
3. **Equivalent term, different name** → projection / extension, not parallel ontology.
3. **Different terms, same referent** → DRAFT_LOCAL/CANDIDATE_ABI + reconciliation note in registry; do not silently fork the vocabulary.

A schema that creates a new enum for OBS/DER/INT/SPEC/SEAL when the canonical Reality Graph already uses those classes is the canonical failure mode. Symptom: one system writes SPEC, another writes GENERATED, another writes HYPOTHESIS — your membrane becomes the next translation bug.

**Comparability is wider than the strict equality check.** A naive `Type(A) = Type(B)` guard fires false-positive DRIFT for legitimate bridge candidates: `git_sha ↔ pep440` (build manifest provenance), `DOI ↔ paper URL` (openurl resolution), `App Store ID ↔ canonical URL` (tools/list transport), `tool alias ↔ canonical name` (registrar mapping). The correct invariant is:

```
Comparable(A,B) = SameType(A,B) ∨ WitnessedBridge(A,B)
```

The bridge function is itself a claim that must be backed by evidence (BUILDINFO, SBOM, transport response, registrar artifact). Encode this in the schema with an optional `type_mismatch_resolution` block carrying `bridge_name` + `bridge_artifact_ref` + `normalized_a/b` + `comparable_after_resolution: bool`. Without it, the type-equality gate manufactures drift that does not exist.

### Capability proof cannot create consequences while measuring truth

A `CapabilityGraph` whose `observed_callable` set is produced by invoking every declared tool will execute mutating tools (MUTASI / DEPLOY consequence_class) merely to prove they exist. That makes the capability probe the source of the consequence it is trying to measure — the worst kind of side-effect-on-observation.

Required pattern:

```
declared → registered → exported → reachable → contract_valid
                                                         ↓
                                                  safely_probeable
                                                  (consequence_class
                                                   ∈ {AKSES, HANTAR})
                                                         ↓
                                                  observed_callable
```

Tools with `consequence_class ∈ {MUTASI, DEPLOY}` must be carried in a separate `mutating_tools[]` array and excluded from `observed_callable` via JSON Schema `allOf` + `if/then` invariant. Their callability evidence comes from schema presence, transport response, or dry-run synthetic probe — not execution. Otherwise your truth compiler manufactures consequences.

### Use multiple axes, not single enums

When a primitive carries two or more orthogonal concerns, split them into separate required fields. Conflating them manufactures false equivalences and false divergences.

Example: a BridgeProof must NOT be a single `relation` enum that contains both "what ontological claim" AND "whether comparison is meaningful" AND "what witness concluded" AND "whether probe succeeded". Four concerns, four axes:

| Axis | Distinct question | Forbidden cross-axis value |
|------|-------------------|---------------------------|
| `relation` | What is being claimed? | TYPE_MISMATCH (belongs to comparability) |
| `comparability` | Can these even be compared? | UNRESOLVED (belongs to verification) |
| `verification_state` | What did witness conclude? | UNREACHABLE (belongs to probe) |
| `probe_state` | Did the probe actually run? | REFUTED (probe failure ≠ refutation) |

Enforce the partition with JSON Schema `allOf` + `if/then` so an EQUIVALENT_TO cannot be released without `comparability=COMPARABLE ∧ verification_state=WITNESSED ∧ non-empty evidence_refs`.

### Status: DRAFT_LOCAL / CANDIDATE_ABI, not "frozen"

A registry whose root claims `frozen: <date>` before its contracts have been reconciled, validated, and round-tripped is manufacturing maturity. The seal preserves a record; it does not make the contract canonical. Required promotion gate:

1. All schemas validate against the meta-schema (JSON Schema 2020-12, etc.)
2. All `$ref` cross-schema dependencies resolve
3. Reconciliation matrix produced against existing canon
4. Validator + fixture suite passes
5. A2A / round-trip test passes (if A2A-relevant)
6. No semantic duplicate exists in federation vocabulary
7. GitHub / upstream diff independently reviewed

Until 7-of-7: status `CANDIDATE_ABI`. Frozen implies "this is what every organ now emits", which is a federation-wide commitment that needs every layer checked.

### Hard invariants via JSON Schema `allOf` + `if/then`

The "multiple axes" rule is enforceable at the schema layer, not just prose. JSON Schema draft 2020-12 `allOf` + `if/then` is the canonical enforcement surface — codify each cross-axis guard directly:

```json
{
  "allOf": [
    {
      "description": "EQUIVALENT_TO requires COMPARABLE ∧ WITNESSED",
      "if": { "properties": { "relation": { "const": "EQUIVALENT_TO" } }, "required": ["relation"] },
      "then": {
        "properties": {
          "comparability": { "const": "COMPARABLE" },
          "verification_state": { "const": "WITNESSED" }
        }
      }
    },
    {
      "description": "Probe failure cannot masquerade as REFUTED",
      "if": { "properties": { "probe_state": { "enum": ["ERROR", "UNREACHABLE", "NOT_RUN"] } }, "required": ["probe_state"] },
      "then": { "properties": { "verification_state": { "enum": ["UNRESOLVED"] } } }
    }
  ]
}
```

Three rules for using this idiom:

- **`if` requires the trigger field in `required`**, otherwise the `then` branch is skipped when the trigger is absent and the guard silently becomes a no-op.
- **`then` is additive**, not replaceable — multiple `if/then` blocks compose; do not nest.
- **Comments inside `description` are the audit trail** for human readers; the schema validator ignores them but they are how a future agent understands why the invariant exists.

Prose laws in a `MIGRATION.md` table are good for humans. JSON Schema `if/then` is what actually fires. Always pair both.

### Concurrent-worker hazard

The federation runs parallel agents on the same canonical paths. Before any mutation:

1. Read the file FULLY with `read_file` (every page if it spans offset).
2. Check `git log -1` on the file — does its recent commit belong to a different lane / session / agent?
3. Use `patch` (targeted find-and-replace) for surgical edits. Avoid mass `write_file` overwrites that may discard concurrent provenance.

The `stale_write_blocked` error from `write_file` ("this task has not seen its full current content") is the system telling you the file is being touched by another lane — not a bug. Reload, merge, retry. Reading a snippet earlier in the conversation does NOT satisfy the guard.

**Doctrinal corollary — `NarratedState ≠ ObservedState`.** When you re-read a file you previously authored and find it has been replaced with a minimal placeholder (missing `$schema`, `$id`, description, ratified-tuple fields), that is not drift in your output — it is federation-wide evidence that schemas are NOT living artifacts between sessions unless the registry locks them. Treat the discovery as a CI signal: a validator that compares every registry entry against the byte-on-disk schema file would have surfaced the substitution. The C.3 reconciliation matrix should include a per-schema byte-comparison row.

### Provenance attribution discipline

- Cite provenances by ID (`#qa-AB12cd`, `added_by: session-<date>-<id>`) not by author names unless the name is canonical to the federation.
- Remove any attribution that does not resolve to a real federation entity. ("Karim et al, 02 Oct 2026" in a schema description, with no retrievable Karim in the federation, is unexplained attribution — strip it.)
- Preserve concurrent-worker provenance: when you patch a registry another agent created, KEEP its `frozen_by` / `created_by` provenance and ADD your own `added_by` for the entries you introduce. Do not overwrite the root provenance.

### Wraps rather than parallel transports

Before writing a new A2A / message / transport envelope, check whether existing transport contracts already cover the use case:
- `a2a-v1.0.schema.json`
- `peer-federation-contract.schema.json`
- `task-envelope.schema.json`
- `specs/HHMM/INIT-SPEC-v0.1.md` E12

The right move is to extend these by reference, not to create a parallel transport that other agents will then have to translate between. A second A2A contract is the federation's translation debt forever.

### Schema extension discipline

When a new schema must extend an existing one, model it as a **wire-format projection** of the existing object:

```
NewClaimRecord := projection of existing RealityAssertion
NewA2AEnvelope := projection of existing peer-federation-contract
```

A projection declares its source. A parallel ontology silently assumes its referent is the same — and breaks when the projection drifts from the source.

## Procedure (5 steps, in order)

1. **Reconnaissance** — Read the registry, the existing schemas that touch the new shape, and the doctrine files that justify the extension. Identify overlap.

2. **Reconciliation matrix** — Produce a table: existing term → new term → overlap class → decision (use / extend / wrap / reject). If overlap > 0, decide the wire-format relationship before writing.

3. **Schema file** — Write the new JSON Schema with:
   - Required axes split per fact, not collapsed into one enum.
   - Hard invariants encoded as `allOf` / `if/then`.
   - `additionalProperties: false` (no silent extension surface).
   - `$id` at canonical URL space (e.g. `https://aaa.arif-fazil.com/schemas/ir/<name>.v<N>.schema.json`).

4. **Registry update** — Patch the registry: `status: CANDIDATE_ABI`, `added_by: session-<...>`, `note: ...`. **Preserve** any concurrent-worker provenance.

5. **Migration doc** — One row per invariant the schema locks. Cross-reference the MIGRATION.md law index.

## Anti-patterns (each kills the work)

- **Adding a new enum without checking existing enums** — the membrane becomes the next translation bug.
- **Mass `write_file` of a file concurrent writers also touch** — discards sibling provenance and triggers merge conflict on the next render.
- **`status: "frozen"` on first commit** — manufactures maturity, blocks honest promotion work later.
- **Adding a parallel A2A / transport schema** — translation debt forever, agents disagree on message shape.
- **Schema `additionalProperties: true`** — silent extension surface that hides downstream incompatibilities.
- **Provenance by author name with no federation resolution** — unexplained attribution; remove.
- **No `$id` or wrong `$id`** — schema loads but `lookup` cannot find it; A2A round-trips fail.

## Companion skills

- `forge-project-context-update` — surgical merge of AGENTS.md (related: surgical-edit discipline).
- `forge-repo-intelligence` modes `manifest_reconcile` and `cross_repo_impact` — read-only lanes that surface the overlaps before you write.
- `forge-lsp-pre-edit-gate` — pre-mutation LSP grounding for code changes; pair with this skill for schema contracts.
- `governance-ops` / row 5 `aaa-doctrine-sealing` — when the new schema embodies ratified doctrine, sealing is downstream of this skill's reconciliation matrix.
- `path-hallucination-guard` — narrower: filesystem paths; this skill is the schema-registry equivalent.