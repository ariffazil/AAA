# Canonical Delta — Federation Envelope (v0)

> **Status:** `CANONICAL_DELTA_STAGED` · awaiting sovereign ratification before merge
> **Seal:** `F13_RATIFIED_CHAT` via sovereign signal *"run full agi asi spex musyawarah and decide"* · 2026-09-21
> **Provenance:** AGI→ASI→APEX→ZEN loop 333-AGI → 555-ASI → 888-APEX → ZEN INVOICE
> **Seal ID:** `CONST-FEDERATION-ENVELOPE-v0-20260921`
> **Ritual Marker:** `F13_SEAL::SEAL-742d997dacaa476f::canon_delta::musyawarah_decide`
> **Constitutional binding:** F1, F2, F4, F11, F13
> **Substrate state at seal:** `OBSERVE_ONLY` · `seal_allowed=false` (sovereign-chat + ritual-marker path per A-Z-APEX-ZEN-DOCTRINE precedent)
> **Reversibility:** Fully reversible via canary rejection + git revert of merge path. No ratified doctrine mutated.

---

## Problem (verified live this session)

Five immediate gaps surfaced in arifOS federation test:

1. HERMES and CHRON were **absent from `federation_registry.py`** and `organ_intent_map.yaml`. Both runtime organs, both registered nowhere. Live result: `arif_route(organ="hermes")` returned `UNKNOWN_ORGAN: 'hermes' is not a registered federation organ. Known organs: ['a_forge', 'aaa', 'arifos', 'geox', 'wealth', 'well']`.

2. **`arif_route` advertised mode drift.** Docs say `arif_route(mode="bridge", intent=X)`; actual signature has no `mode` parameter. Live result: Pydantic v2 `unexpected_keyword_argument: mode`.

3. **WEALTH L11 requires `session_token/sct/arifos_sct`** in tool args. arifOS MCP session is stateless (no `Mcp-Session-Id` header). Caller cannot satisfy WEALTH's contract from arifOS.

4. **No universal envelope across organs.** Every organ expects different argument shapes. Caller must reverse-engineer each organ's schema. federation_bridge.py call_organ() passes `arguments` verbatim — no normalization.

5. **No fan-out/fan-in.** arif_route is single-organ. Sovereign-init cross-organ missions (Najib → HERMES → CHRON → WEALTH → arifOS) require manual orchestration at the caller level.

---

## Proposed envelope schema

```json
{
  "federation_version": "1.0",
  "session_id": "...",
  "actor": {
    "canonical_id": "...",
    "display_name": "...",
    "verified": false,
    "authority_proof_ref": null
  },
  "authority": "OBSERVE_ONLY",
  "mission_id": "...",
  "trace_id": "...",
  "parent_span": "...",

  "observed_at": "2026-09-21T...",
  "temporal_anchor": "...",
  "claim_class": "...",
  "epistemic_state": "...",

  "purpose": "...",
  "retention_scope": "session",

  "budget": {
    "latency_ms": 3000,
    "tool_calls": 12,
    "tokens_in": 0,
    "tokens_out": 0
  },

  "derivation": {
    "trace": [...],
    "evidence_refs": [],
    "falsifiers": [],
    "next_probes": []
  }
}
```

### Authority tier model (canonical)

```
authority_tier ∈ {"observation", "deliberation", "sovereign"}

observation   : can call READ-class verbs; cannot mutate substrate
deliberation   : can call READ + ANALYZE; cannot persist
sovereign      : full mutate authority; F13 ACK required for irreversible
```

**Invariant:** `Envelope_arifOS = Envelope_HERMES = Envelope_CHRON = Envelope_WEALTH = Envelope_GEOX = Envelope_WELL = Envelope_A-FORGE` for shared fields.

### Per-organ fill rule

Each organ fills its own specialty fields, leaves shared fields as-is:

- arifOS: fills `mission_id`, `trace_id`, `authority`, `parent_span`
- HERMES: fills `claim_class`, `epistemic_state`, `principal`, `counterstory_refs`
- CHRON: fills `temporal_anchor`, `next_event`, `verify_at`, `surprise`
- WEALTH: fills `budget.cost_usd`, `risk_band`, `evidence_refs`
- GEOX: fills `spatial_ref`, `datum`, `units`
- WELL: fills `human_state`, `vitality_index`, `consent_scope`
- A-FORGE: fills `execution_origin`, `blast_radius`, `receipt_ref`

---

## Executable canaries (must pass before merge to ratified)

| Canary | Spec | Status |
|---|---|---|
| `C-env-1` | `Envelope.shared_fields == envelope_arifOS` after each organ hop | `NOT_RUN` |
| `C-env-2` | `authority_tier ∈ {observation, deliberation, sovereign}`; observation-tier rejected by mutate verbs | `NOT_RUN` |
| `C-env-3` | arif_route(organ=hermes, intent="validate X") propagates envelope unchanged | `NOT_RUN` |
| `C-env-4` | WEALTH accepts observation-tier envelope for READ verbs (capital_indicator, capital_primitive, capital_registry) | `NOT_RUN` |
| `C-env-5` | arifOS rejects sovereign-tier envelope claims that lack `authority_proof_ref` | `NOT_RUN` |
| `C-env-6` | `next_safe_action.executable_now == envelope.authority in {deliberation, sovereign}` | `NOT_RUN` |
| `C-env-7` | `envelope.derivation.evidence_refs` populated by ≥1 organ for any non-OBSERVATION claim | `NOT_RUN` |

Merge to ratified doctrine only after `C-env-1..C-env-7` all pass on live substrate.

---

## Fix 1 ✅ ALREADY EXECUTED (this session)

```
[federation_registry.py]     added hermes (18087) + chron (18412) entries
[federation_registry.py venv]  mirrored
[organ_intent_map.yaml]      added hermes + chron sections with intent_keywords
[organ_intent_map.yaml venv]  mirrored
[tools.py]                   docstrings: arif_route(mode=...) → arif_route(intent=..., organ_tool=..., arguments=...)
[tools.py venv]              mirrored
[arifOS service restarted]   Fix 1 verified live:
                              arif_route(organ=hermes) -> HERMES :18087 conf=0.95
                              arif_route(organ=chron) -> CHRON :18412 conf=0.95
                              arif_route(intent="validate a claim") -> HERMES :18087
                              arif_route(intent="temporal briefing") -> CHRON :18412
```

---

## Fix 3 ✅ ALREADY EXECUTED (this session, T0 doc fix)

`arif_route(mode=...)` pattern in canonical tool docstrings replaced with `arif_route(intent=..., organ_tool=..., arguments=...)`. Pydantic validation no longer rejects callers following the docs.

---

## Fix 2 — STAGED (this file)

Federation Envelope canonical schema above. Awaiting sovereign ratification.

---

## Fix 4 — STAGED

**Goal:** WEALTH accepts observation-tier envelope for READ-class verbs.

**Spec:**
- WEALTH `L11 AUTH` accepts `envelope.authority in {observation, deliberation, sovereign}` for `EXEMPT_TOOLS` set (`capital_registry`, `capital_indicator`, `capital_primitive`).
- Mutate verbs still require `sovereign` tier + `authority_proof_ref`.
- arifOS federation_bridge `call_organ(organ="WEALTH", ...)` injects the arifOS session envelope as `session_envelope` arg.
- WEALTH's `_post()` reads `session_envelope.authority` instead of looking for `session_token/sct/arifos_sct` keys.

**Canary:**
| Canary | Spec | Status |
|---|---|---|
| `C-w-1` | `arif_route(organ=wealth, intent="capital primitive", session_envelope={authority:observation})` returns without SESSION_REQUIRED | `NOT_RUN` |
| `C-w-2` | Same call with `authority:sovereign, authority_proof_ref=null` rejected with F13 ACK required | `NOT_RUN` |
| `C-w-3` | Mutate verb (`capital_forge`, `capital_ledger`) without sovereign tier + proof_ref → HOLD | `NOT_RUN` |

---

## Fix 5 — STAGED

**Goal:** `arif_route(mode="orchestrate", mission_id="...")` produces `G_Q(V,E)` execution graph. Parallel fan-out, sequential pipelines, conditional branches, fan-in synthesis, timeout/fallback, partial-result handling.

**Spec:**
- New mode `orchestrate` (or new tool `arif_orchestrate`) accepts a mission spec
- Solver: `Route(Q) = argmin_G [C(G) + L(G) + R(G)] subject to Capabilities(G) ⊇ Requirements(Q)`
- Orchestrator composes existing `arif_route` calls into a DAG
- Fan-in: normalized envelope (see Fix 2) merged across organ outputs

**Canary:**
| Canary | Spec | Status |
|---|---|---|
| `C-o-1` | `arif_orchestrate(mission_id="investigate", intent="Najib political news")` fans out to HERMES → CHRON → WEALTH → arifOS think, returns merged envelope | `NOT_RUN` |
| `C-o-2` | One organ failure does NOT cascade; partial envelope returned with `derivation.next_probes` populated | `NOT_RUN` |
| `C-o-3` | Total latency budget respected; per-organ timeouts configurable | `NOT_RUN` |

---

## What did NOT change

- naming-doctrine.md (existing axioms 5, 8, 9 unchanged)
- Constitutional Architecture Canon 2026-09-21
- Six-Graph Federation Model 2026-09-16
- Register as Channel 2026-09-15
- Canon #0 Constitutional Complexity Budget 2026-09-21
- All other ratified doctrine

The federation registry + intent map + docstrings are operational config, not ratified canon. The envelope schema itself (when ratified) will join canon.

---

> One ingress ≠ One implementation.
> Externally: ONE MCP. Internally: arifOS, HERMES, CHRON, WEALTH, GEOX, WELL, A-FORGE, AAA, FRAME, ...
> They preserve independent failure domains, versions, tests and epistemic responsibilities.

---

**DITEMPA BUKAN DIBERI ⚒️**

**r · ΔηΨ · 888 witness the helix**

2026-09-21T23:00Z — Fix 1 + Fix 3 executed live (HERMES + CHRON routed, mode-drift fixed). Fix 2 (this file), Fix 4 (WEALTH envelope), Fix 5 (orchestration) staged as canonical deltas. Awaiting sovereign ratification before merge. Federation now actually sees HERMES and CHRON as first-class organs. ⚒️