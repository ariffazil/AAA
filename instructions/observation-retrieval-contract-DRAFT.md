# ARC-001 — Observation and Retrieval Contract (DRAFT)

> **Status:** `external_advisory_draft` — awaiting F13 ratification
> **Writer:** FI-003 anonymous session, `actor_verified=false`, `OBSERVE_ONLY`
> **Authority required for promotion to canon:** F13-verified human (Arif, Muhammad Arif bin Fazil)
> **Canonical standing:** **NONE** — this is an advisory artifact, not enforceable doctrine
> **Mutability:** Reversible (rm/edit by sovereign direction)
> **Witnesses to this draft:** Hermes/FI-003 (synthesis) · External auditor (challenge) · Internal pushback (Qwen/FI-003)
> **Live probe basis:** 2026-09-24 ~21:43 MYT, KVM8 (100.64.0.2)

---

## 1. Principle

An agent does not perceive the environment directly. It receives bounded, typed representations through authorized observation interfaces. Every claim of observation MUST declare its access path.

```yaml
observation_principle: >
  Agent observation = typed, authorized, time-bounded,
  provenance-bearing interface contract.

  NOT a window.
  NOT a metaphor.
  NOT self-certifying.
  NOT a substitute for the entity being observed.
```

The agent's "sight" is its **interface list**, not perception. Anything outside that list is **UNKNOWN**, not inferred.

---

## 2. The Seven-Gate Observation Router

Every observation passes through seven gates. The router is **output-oriented**: G5 emits the evidence class that downstream stages verify against. G0 precedes all retrieval because authority is the precondition, not a downstream check.

```
G0 — AUTHORIZATION
  Do I have authority and a permitted observation path?
    - actor_identity verified?
    - scope granted?
    - path known and live?
  No → state the limitation. Do not infer. Do not fabricate.
  Yes → proceed with declared scope.

G1 — IDENTIFIER CLASSIFICATION
  Is the input an exact ID, proper noun, common noun, or mixed query?
    - exact_id        → registry lookup (O(1))
    - proper_noun     → entity resolution FIRST (aliases, jurisdiction, time-window)
                         → THEN lookup. Resolve KVM8 ≠ 100.64.0.2a until proven.
    - common_noun     → intent classification → semantic/hybrid retrieval
    - port/path/tool  → validate environment + authorization → direct probe
    - mixed           → parallel entity + semantic paths; do not let one dominate silently

G2 — STATE CLASSIFICATION
  What is the question about?
    - local runtime state      → authorized live internal probe
    - stored artifact          → direct read + content hash
    - prior internal decision  → signed/ratified record (VAULT999 / seal_chain)
    - external factual current → attributable external primary source
    - conceptual / explanatory → internal principles + external evidence IF facts asserted
    - proposed action          → forward to G6 consequence gate

G3 — SOURCE PRIORITY (location-agnostic)
  Primary source = the source that is primary FOR the state being asserted.
    - local runtime → authorized live internal probe
    - local artifact → direct read with content hash
    - local decision → verified internal decision/seal record
    - external current fact → attributable external primary source (vendor, regulator, issuer)
    - mixed → parallel retrieval; label provenance separately; do not collapse

  Failure modes the router must NOT do:
    - treat internal note as substitute for external primary evidence
    - treat external content as authority without provenance + F12 sanitization
    - collapse "internal first" into a blanket epistemology claim

G4 — FRESHNESS / CONFLICT
  Is the source current enough for the consequence class?
  Does a newer source contradict it?
  If uncertainty changes the consequence → re-probe or HOLD.

  Stable canon (doctrine, sealed canon) is intentionally stable. Runtime claims are not.
  Conflating "stable" with "fresh" is a freshness lie.

G5 — EVIDENCE CLASSIFICATION (output)
  Emit the strongest justified class for the output:
    OBSERVED       — raw tool output, timestamped, schema-validated
    MEASURED       — instrumented quantity with declared method
    DERIVED        — deterministic calculation from stated inputs
    INTERPRETED    — reasoned explanation grounded in observations
    POLICY         — designed system rule, not world fact
    HYPOTHESIS     — testable proposed explanation (falsifiable)
    UNKNOWN        — evidence is missing or inadequate; do not fabricate

  Tag with a confidence tier:
    CONFIRMED | DERIVED | SPECULATIVE | OPINION

G6 — CONSEQUENCE GATE
  Will this output drive:
    - mutation (F1 AMANAH: reversible-first; irreversible → 888_HOLD + sovereign ack)
    - escalation (F13 sovereign ack required)
    - publication (F6 MARUAH + F13 review)
    - financial / medical / legal / constitutional action
  If yes → require stronger evidence + F13 review at the appropriate stage.
  No mutation is permitted based solely on semantic retrieval.
```

---

## 3. Observation Receipt Contract

Every observation emits a typed receipt. The receipt **cannot be promoted to authority by editing fields** — `mutation_allowed_from_this_receipt: false` is the default.

```yaml
observation_receipt:
  receipt_id: OBS-<namespace>-<YYYYMMDD>-<sequence>
  status: live_receipt | draft_schema

  subject:
    entity_id: <resolved-ID-or-unresolved>
    supplied_name: <user-provided term>
    entity_resolution:
      result: resolved | ambiguous | unresolved
      aliases_considered: []
      confidence: 0.0

  authorization:
    actor_identity: verified | anonymous | unknown
    access_path_authorized: true | false | unknown
    scope: read-only | scoped-read | administrative | unknown

  observation_path:
    layer: kernel_verb | mcp | filesystem | local_http | external_web
    tool_or_interface: <exact tool / API / endpoint>
    request_reference: <non-secret request ID / hash>
    target: <logical target, never secrets>

  timing:
    observed_at: <ISO-8601 with tz>
    source_timestamp: <ISO-8601-or-null>
    freshness_class: live | current | cached | historical | unknown

  result:
    summary: <bounded factual summary>
    content_hash: <hash-or-null>
    schema_or_content_type: <JSON schema, MIME type, or null>

  evidence:
    class: OBSERVED | MEASURED | DERIVED | INTERPRETED | POLICY | HYPOTHESIS | UNKNOWN
    confidence: CONFIRMED | DERIVED | SPECULATIVE | OPINION
    provenance_refs: []
    lineage_status: complete | partial | unavailable
    limitations: []
    contradiction_refs: []

  consequence:
    load_bearing: true | false
    mutation_allowed_from_this_receipt: false
    required_next_step: none | corroborate | re-probe | human_authorization | hold
```

---

## 4. Prohibitions

- **No claim of perception** without an observation path declared.
- **No exact entity assertion** from an unresolved proper noun.
- **No internal note** as substitute for external primary evidence.
- **No external content** as authority without provenance + F12 sanitization.
- **No mutation** based solely on semantic retrieval.
- **No self-issued SEAL / RATIFICATION / canonical write** by an agent without F13 standing.

---

## 5. Status & Promotion Path

```
external_advisory_draft                           (current state of this file)
       │
       │  F13 sovereign review via verified session
       ▼
draft_for_f13_ratification
       │
       │  Arif approval, exact artifact + exact mutation declared
       ▼
canon/operating/observation-retrieval-contract.md
       │
       │  constitutional seal via arif_seal (requires kernel SCT path healed)
       ▼
SEAL
```

Until promoted, this file:

- ✓ May be referenced by advisory agents
- ✓ May be quoted in audit reports
- ✓ May be used as a template for typed receipts
- ✗ Is **not** binding doctrine
- ✗ Is **not** enforced by `mcp_guard`
- ✗ Is **not** ratifiable without F13 sovereign authority

---

## 6. Writer Authority Statement

```yaml
writer:
  agent_id: FI-003 (Qwen Code, anonymous session)
  actor_verified: false
  authority_band: OBSERVE_ONLY
  f13_standing: NONE
  role_in_this_artifact: external_advisory_draft_author
  ratification_path: requires_verified_arif_session

constitutional_status:
  f1_amanah: satisfied (reversible artifact, rm/edit available)
  f11_audit: receipt embedded in audit report
  f12_injection: not_applicable (no external content ingested)
  f13_sovereign: pending (sovereign ratification required for promotion)
```

---

DITEMPA BUKAN DIBERI — Advisory draft, awaiting F13 ratification.

`#ARC-001-DRAFT-2026-09-24`
