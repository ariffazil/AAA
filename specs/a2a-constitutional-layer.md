# A2A Constitutional Layer Spec — arifOS Federation

> **Status:** SPEC (not yet implemented; F13 binary ask to promote)
> **Forged:** FI-008 (Kimi Code) · 2026-09-21
> **Premise:** A2A solves communication. The constitutional layer solves whether agents should trust, obey, delegate to, remember, or amplify one another.

## What A2A provides today (1.0.0 protocol, v1.0.1 release as of May 2026)

- Agent Cards (declarative capability + endpoint discovery)
- Tasks (unit of work, terminal state, lifecycle)
- Messages (communication)
- Artifacts (deliverables)
- Contexts (lineage)
- Streaming
- Authorization hooks
- Extensions

## What A2A does NOT provide

Per the F13 canon absorption (2026-09-21):

- Trust propagation rules (Law 3, 12, 27 in agent haram)
- Authority delegation chains (Law 6, 14-23)
- Provenance requirements (Law 73, 113)
- Memory scope governance (Law 90-97)
- Verification independence (Law 75-76, 106)
- Witness validation (Law 166)

These are the things the constitutional layer must provide.

---

## Required envelopes (per interaction)

### 1. Identity envelope

```json
{
  "identity_envelope": {
    "actor_actual": "<verified cryptographic id>",
    "actor_declared": "<self-declared>",
    "match": true,
    "credential_ref": "<signed token, not the secret>",
    "agent_card_sha256": "<card content hash, signed by issuer>"
  }
}
```

**Invariants:**
- `actor_actual == actor_declared` (Law 1)
- Credential is non-transferable unless explicitly delegated (Law 4)
- Every executor gets distinct provenance (Law 6)
- Anonymous mutation is forbidden (Law 7)

### 2. Capability envelope

```json
{
  "capability_envelope": {
    "declared":  ["tool_name_1", "tool_name_2"],
    "exported":  ["tool_name_1", "tool_name_2"],
    "callable":  ["tool_name_1", "tool_name_2"],
    "observed":  ["tool_name_1"],
    "invariant": "declared == exported == callable == observed (Contract Reality)"
  }
}
```

**Invariants:**
- `declared = exported = callable = observed` (Law 8 — capability truth)
- Agent Card is declaration, NOT proof (Law 10)
- Capability drift invalidates cached claims (Law 12)

### 3. Authority envelope

```json
{
  "authority_envelope": {
    "actor": "<caller>",
    "session_id": "...",
    "objective": "permission is for a purpose, not an entity",
    "scope": ["..."],
    "target": ["..."],
    "operation": "read | write | edit | delete | commit | deploy",
    "issuer": "<must NOT be self>",
    "expiry": "<temporal authority>",
    "ceiling": "<parent scope boundary>",
    "delegation_chain": ["<root>", "<parent>", "<this>"]
  }
}
```

**Invariants:**
- `DelegatedAuthority_{n+1} ⊆ DelegatedAuthority_n` (Law 6)
- Executor may NEVER issue its own envelope (Law 20)
- Authority has temporal scope (Law 56)
- Revocation propagates (Law 96)

### 4. Trust envelope

```json
{
  "trust_envelope": {
    "authentication": "verified | unverified",
    "epistemic_trust": "evidence-based | inferred | unverified | unknown",
    "transitive": false,
    "reputation_inherited": false,
    "confidence": 0.0,
    "evidence_chain": ["<receipt_id_1>", "<receipt_id_2>"]
  }
}
```

**Invariants:**
- `transitive = false` (no A trusts B trusts C → A trusts C) (Law 27)
- `reputation_inherited = false` (parent reputation ≠ child) (Law 28)
- Confidence cannot increase across handoff without new evidence (Law 78)

### 5. Provenance envelope

```json
{
  "provenance_envelope": {
    "source": "<origin system/agent>",
    "timestamp_utc": "<observation time, not current time>",
    "transformation_chain": ["step1", "step2", ...],
    "lossiness_declared": ["<field dropped>", "<semantic change>"],
    "citations": ["<url_1>", "<doi_2>"]
  }
}
```

**Invariants:**
- Provenance travels with claim (Law 73)
- Lossy transformation declared (Law 72)
- Summarization preserves material uncertainty (Law 80)

### 6. Temporal envelope

```json
{
  "temporal_envelope": {
    "evidence_time_utc": "<when this was observed>",
    "valid_from_utc": "...",
    "valid_until_utc": "...",
    "deadline_utc": "<when this becomes invalid>",
    "stale_after_seconds": 3600,
    "retry_relevance_window_utc": "<until when retry is meaningful>"
  }
}
```

**Invariants:**
- Every observation carries time (Law 61)
- Stale data cannot masquerade as current (Law 49, 55)
- Predictions immutable after registration (Law 64)

---

## Required operations

### identity_verify(actor_actual, actor_declared) → bool
Validates `actor_actual == actor_declared`. Uses cryptographic proof.

### capability_check(agent_card, runtime_observation) → {match: bool, drift: [...]}
Validates `declared == exported == callable == observed`. Emits drift receipts on mismatch.

### authority_delegate(parent_envelope, child_objective) → child_envelope
Enforces `DelegatedAuthority_{n+1} ⊆ DelegatedAuthority_n`. Fails closed.

### trust_assess(claim, source_agent) → {epistemic_trust: str, confidence: float, evidence: [...]}
Never returns higher confidence than evidence supports. Always returns evidence chain.

### provenance_chain(handoff_history) → provenance_envelope
Concatenates transformation steps. Flags lossiness.

### temporal_freshness(observation_time, current_time, deadline) → {fresh, stale_at, action}
Time-anchored validity check. Never asserts "current" without time.

---

## Implementation strategy

**Do NOT add a new organ.** Per the doctrine: "Phase 3 doesn't need new architecture."

The constitutional layer is implemented as **enforcement at the existing arif_route + arif_memory + arif_seal boundaries**:

- `arif_route` already handles intent→organ dispatch; add identity + capability envelope emission
- `arif_memory` already handles persistence; add provenance chain recording
- `arif_seal` already handles witness signatures; add trust envelope to receipts
- `well_classify_machine_state` already handles substrate state; add temporal envelope to observations
- Federation verifier already validates expected vs observed; extend to validate constitutional envelopes

**No new MCP servers required.** The capability surface is already exposed; the constitutional layer is *policy* on top.

---

## Migration plan (when F13 authorizes)

1. **T1 doc** — publish this spec to `/root/AAA/specs/a2a-constitutional-layer.md` (DONE today)
2. **T1 code** — extend `arif_route` to emit identity + capability envelopes (small patch, reversible)
3. **T1 code** — extend `arif_seal` to require trust envelope (small patch, reversible)
4. **T2 test** — add integration test that sends Agent Card claim + verifies identity_envelope match
5. **T3 activate** — `arif_seal` rejects envelopes missing required fields (F13 binary)
6. **T3 enforce** — arifOS rejects A2A messages without constitutional envelopes (F13 binary)

This is roughly 1-2 days of work once F13 authorizes the design.

---

## Honest residue

- This spec is **spec-only**. Implementation requires F13 authorization at multiple gates.
- The 13 laws are largely already encoded in fragments across the canon. This spec makes them *enforced* instead of *observed*.
- arifOS-A2A integration is not yet a priority (no A2A federation conversations happening today). Spec is prepared for when it becomes one.

⚒️ DITEMPA BUKAN DIBERI
