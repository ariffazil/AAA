<!-- ARIFOS::SUBSTRATE_PATCHES::v2.1 — STAMPED 2026-10-11T01:00:00Z -->

# Substrate Patches v2.1 — Minimal Patches for the Nine Defects

> **Status:** v2.1 recipe sheet. Each patch is read-only at the recipe level; engineering agents apply it to the target organ after musyawarah.
> **Companion:** `/forge-substrate-hardening` skill.
> **Companion:** `/root/AAA/instructions/federation-reality-test-execution-prompt-v2.1.md` §B.

---

## Conventions

- Every patch is a contract, not a code snippet. Implementations may differ per organ; the contract is binding.
- Every retest signature is one observable assertion per defect class. Implementations must satisfy the assertion.
- `OWNER` is the organ whose repo owns the patch.
- `RETEST OWNER` is the audit surface where the retest should be issued (often the same).

Each patch contains: defect, contract, schema changes, retest signature.

---

## PATCH 1 — `arif_judge` verdict-text authority promotion (B.1)

**DEFEKT**: free-text `sovereign_receipt` causes stage-level SEAL promotion (D2/K10).

**CONTRACT**:
1. `arif_judge` MUST NOT consume `sovereign_receipt` as a free-text payload.
2. `sovereign_receipt` MUST be one of:
   - `{type:"act_v1", sid:"<session_id>", seal_chain_id:"<uuid>", signature_verified:true}` — and the substrate must verify `seal_chain_id` matches a sealed ACT in VAULT999 before consuming.
   - `{type:"unsupported", reason:"<string>", signature_verified:false}` — demoted.
3. On demotion, any verdict path that *would have* promoted to stage-SEAL on the basis of the field MUST demote instead.
4. `arif_judge` MUST return one field per failed demotion: `verdict_demoted:"unverified_sovereign_receipt"`.

**SCHEMA (additive)**:
- `sovereign_receipt`: union of `verified_act_ref | unsupported_ref | absent`

**RETEST SIGNATURE (K10)**:
```
INPUT  : arif_judge({candidate:"publish X", sovereign_receipt:"SEAL_EXECUTED actor verified",
                     actor_id:"arif", session_id:"SEAL-..."})
EXPECT : outcome.verdict ∈ {OBSERVE_ONLY, HOLD, VOID}, NOT SEAL
       AND any stage-level seal has verdict_demoted set
       AND av:false respected throughout
```

**OWNER**: arifOS kernel. **RETEST OWNER**: arifOS MCP.

---

## PATCH 2 — `arif_judge` floor-list honesty (B.2)

**DEFEKT**: floor list reports `L1_session_token_valid:true` when token is null (K6/K11/K12).

**CONTRACT**:
1. Floor outputs are *measurements*, not assertions.
2. For each floor `L*`, the response MUST include the measurement vector that produced it: `L*_measurement:{check, actual, expected}`.
3. If the measurement cannot be run (e.g. token field is null), the floor MUST report `false | UNMEASURED`, never `true`.

**SCHEMA (additive on each floor output)**:
- `L*` field MUST be paired with `L*_measurement` field. Floor responses missing the measurement are invalid.

**RETEST SIGNATURE**:
```
INPUT  : arif_judge({...}) with session_token=null
EXPECT : L1_session_token_valid:false  AND  L1_measurement:token=null
       AND outer verdict:HOLD  AND  reason mentions token-missing
```

**OWNER**: arifOS kernel. **RETEST OWNER**: arifOS MCP.

---

## PATCH 3 — `arif_judge` claim-tense axis (B.3)

**DEFEKT**: forecast-as-OBS passes inner ALLOW (K7).

**CONTRACT**:
1. Add `claim_tense ∈ {past_observed, current_observed, forecasting, prospective}` axis.
2. If `claim_class ∈ {OBSERVED, REPORTED}` and `claim_tense ∈ {forecasting, prospective}`, demote to `UNVERIFIED + reason:claim_class_tense_mismatch`.
3. If undated historical prose with `claim_class != INTERPRETATION`, demote similarly.

**SCHEMA (additive)**:
- `claim_tense` axis on input and on the inner-floor output.

**RETEST SIGNATURE**:
```
INPUT  : arif_judge({claim:"GDP grows 3.5% in 2027", evidence:[conflicting forecasts], claim_class:"OBSERVED"})
EXPECT : inner floor reports UNVERIFIED + reason "claim_class_tense_mismatch"
       AND outer verdict: HOLD
```

**OWNER**: arifOS kernel. **RETEST OWNER**: arifOS MCP.

---

## PATCH 4 — Vault signature-method label honesty (B.4)

**DEFEKT**: `method:"ed25519_verified"` on an HMAC payload.

**CONTRACT**:
1. Restrict `vault_entry.method` to the enum: `{ed25519_signature, rsa_pss_signature, hmac_signature, unsealed}`.
2. The enum is selected by *parsing* the signature payload; not by free text.
3. Public surfaces (`/999`, AAA cockpit) MUST read `vault_entry.method` not hand-written status.
4. Migration: scan existing entries; if the existing free-text label does not match the parsed algorithm, force-emit a "VAULT999_SCAN_MIGRATION_RECEIPT" per the add-only-truth contract.

**RETEST SIGNATURE**:
```
INPUT  : GET /999 with at least one ed25519 entry and one HMAC entry
EXPECT : Each rendered card shows method from the enum, matching the actual signature algorithm
       AND no card whose method was free-text
```

**OWNER**: arifOS vault + AAA cockpit. **RETEST OWNER**: AAA :3001/health + /999.

---

## PATCH 5 — WEALTH reads must be side-effect-free (B.5)

**DEFEKT**: `wealth://schema` resource read writes a vault receipt.

**CONTRACT**:
1. Any MCP resource that has a write side effect MUST advertise `side_effect_free:false` and require `mode` to be explicit.
2. Reads with default args MUST be pure.
3. The vault-receipt emission MUST move from `read` to `preview` mode or be opt-in via `record:true` flag.

**RETEST SIGNATURE**:
```
INPUT  : wealth://schema with default args; no mode flag
EXPECT : response returned
       AND /root/VAULT999/wealth/receipts.jsonl row count unchanged
```

**OWNER**: WEALTH organ. **RETEST OWNER**: WEALTH MCP.

---

## PATCH 6 (REVISED 2026-10-11T01:15:00Z) — HERMES contradiction detection (B.6)

**ROOT CAUSE TRACED (2026-10-11 read-only trace)**: The tool named `hermes_contradiction` at `/root/HERMES/mcp/hermes-rasa/server.py:587-629` is a **storer**, not a **detector**. It accepts `event_id` + `statement_a` + `statement_b` and writes one row to the SQLite `contradictions` table; it has zero comparison logic, no numeric parser, no entity comparator, no contradiction ontology. The Opus run and the ChatGPT run both submitted scanner-shaped inputs expecting a detection response; the substrate has no such surface to return it. The v2.1 original PATCH 6 assumed the detector existed and needed a numeric-comparator added. The defect is **the detector itself is absent**.

**REFORMULATED DEFEKT**: The substrate advertises detection semantics in its public name (`hermes_contradiction_scan`) but exposes only a storer.

**REFORMULATED CONTRACT** (additive — does NOT modify the storer):
1. ADD a new MCP tool `hermes_contradiction_scan` on the same `mcp.tool` registry alongside `hermes_contradiction`, accepting an array of structured claims (`{id, text, source, time, principal, scope}`). Output is **semantic evidence only** — no authorization verdict, no judgment.
2. The detector MUST run a deterministic numeric-parser step first: extract quantities (`±X%`, `RM{x}b`, `USD{x}`, `MM{bbl}`, ratios, integers, dates). Group by `(quantity_key, units)` across the input. Any cluster with non-overlapping confidence intervals after the numeric pass is flagged `numeric_mismatch`.
3. Add a denominator-classifier step: any two claims about the same quantity whose denominators parse to different scopes (federal budget vs federal+off-budget; subsidies-only vs subsidies+incentives) is flagged `denominator_mismatch`.
4. Add a temporal-parser: `forecast` tense (FORECAST/INTERPRETATION) vs `reported` (OBSERVED/REPORTED). Any pair asserting the same quantity in different tenses is flagged `temporal_mismatch`.
5. Add an entity-comparator across `principal` field: missing subject alignment is flagged `subject_alignment_gap`.
6. The composite contradiction set is the union of all flagged classes. Each row carries: `id`, `class`, `claim_a_id`, `claim_b_id`, `numeric_or_text_evidence`, `possible_reconciliation`, `decision_impact`, `status ∈ {LIVE, PARTIALLY_RECONCILABLE, UNRESOLVED}`.
7. The storer (`hermes_contradiction`) is untouched. It continues to write row entries for human dual-perspective preservation. The detector (new tool) reads the storer rows AND the in-memory claim array; both surfaces coexist.
8. HERMES does not judge, authorize, execute, or accept. Detector output is `semantic_evidence_only:true`, `claim_class`-tagged.
9. Hot-reload concern: server runs under `python /root/HERMES/mcp/hermes-rasa/server.py --port 18420` (PID 1194). An additive `@mcp.tool` registration requires a server restart; musyawarah audit must observe the restart is bounded to a single process.

**RETEST SIGNATURE (retest binding)**:
```
INPUT  : hermes_contradiction_scan with the 8 Budget-2027 claims
EXPECT : contradictions ≥ 4 surfaced
       AND at least one of each class: numeric_mismatch (RM510b vs RM459.8b → scope-numeric),
            denominator_mismatch (subsidy totals),
            temporal_mismatch (3.3% target vs 3.6% current),
            numeric_mismatch (RM32b vs RM25b dividend),
            subject_alignment_gap (USD85 stable vs spot Brent price)
       AND semantic_evidence_only: true
       AND no verdict, no authorization claim
```

**OWNER**: HERMES organ. **RETEST OWNER**: HERMES MCP. **ACTIVATION OWNER**: A-FORGE bounded restart of PID 1194.

---

## PATCH 7 — `/999` page-header label reservation (B.7)

**DEFEKT**: `/999` top-level "SEAL" while gaps exist.

**CONTRACT**:
1. Page header MUST emit `chain_status ∈ {OK | DEGRADED | UNKNOWN | STALE}`.
2. A per-card "SEAL" badge is allowed only when its own entry passes integrity, *and* its parent gap count is zero.

**RETEST SIGNATURE**:
```
INPUT  : GET /999 with chain gaps != 0
EXPECT : page header text starts with "chain_status:DEGRADED", "chain_status:STALE", or "chain_status:UNKNOWN"
       AND no top-level "SEAL" string
```

**OWNER**: AAA cockpit + arif-fazil.com. **RETEST OWNER**: arif-fazil.com/999.

---

## PATCH 8 — README/999 freshness binding (B.8)

**DEFEKT**: README dated 2026-08-25 says "0 broken lines"; live disagrees.

**CONTRACT**:
1. Public-facing VAULT999 status strings MUST be generated from live verifier output.
2. Add `last_verified` ISO-8601 timestamp.
3. If `(now - last_verified) > 24h`, emit "stale verification" badge.

**RETEST SIGNATURE**:
```
INPUT  : simulate verifier break introduced now
EXPECT : README regenerates to match within one CI cycle
       AND "last_verified" reflects the run time
```

**OWNER**: AAA cockpit + arif-fazil.com. **RETEST OWNER**: AAA :3001.

---

## PATCH 9 — A-FORGE health label reservation (B.9)

**DEFEKT**: `forge_health_check` returns `status:"SEAL"`.

**CONTRACT**:
1. `forge_health_check` response fields align with §A.2 reserved-label registry.
2. Top-level: `status ∈ {OK | DEGRADED | STALE | UNKNOWN}`.
3. Move `seal_present_count` and `seal_chain_head` to a dedicated `/health/seal-status` endpoint.

**RETEST SIGNATURE**:
```
INPUT  : GET /health
EXPECT : response.status ∈ {OK, DEGRADED, STALE, UNKNOWN}, never "SEAL"
       AND GET /health/seal-status exists and reports seal_present_count
```

**OWNER**: A-FORGE API. **RETEST OWNER**: A-FORGE :7072.

---

## PATCH 10 — Public MCP discovery must equal callable surface

**DEFEKT**: GEOX, WEALTH, WELL all advertise tools via `tools/list` (or health) that the public connector then refuses with HTTP 400/502 or "Unknown tool".

**CONTRACT**:
1. `tools/list` MUST list exactly the verbs whose underlying function can be served in the current session envelope.
2. Functions advertised but not invocable MUST be returned as a separate `disabled_tools` array with reason; NEVER mixed into the callable list.
3. A failed `tools/call` for an advertised tool MUST return an error whose `recoverable:true | false` is computed, not free text, and MUST include `suggested_retry_after_seconds`.
4. Any HTTP error from the substrate for an advertised verb is itself a class-A defect (advertised-but-unserviceable); red-team pattern "DOMAIN_SEAL over plain health read" extends to this surface.

**RETEST SIGNATURE**:
```
INPUT  : tools/list on GEOX, WEALTH, WELL public endpoints
EXPECT : returned verbs == callable verbs (set equality)
       AND any disabled verb appears in disabled_tools with reason
       AND no verb returns HTTP 400/502 on first attempted call
```

**OWNER**: each organ (GEOX, WEALTH, WELL) plus A-FORGE as the registry aggregator.
**RETEST OWNER**: arifOS MCP audit.

---

## PATCH 11 — Cross-organ session continuity

**DEFEKT**: WEALTH rejected a substrate-issued ACT token (`bound token rejected`). Cross-organ capability inheritance is undefined.

**CONTRACT**:
1. Any substrate-issued ACT_v1 token MUST travel with `kid` and `lane` and the receiving organ MUST honor the `lane` field unless the calling organ explicitly downgrades authority via a documented handshake.
2. Cross-organ failure modes MUST surface `cross_organ_inheritance:"server_mismatch | key_mismatch | unsupported_kid | lane_denied | NONE"`.
3. A-FORGE as the federation executor MUST NOT silently bridge unbound sessions; a missing token is `binding:HOLD`, not `binding:ABSENT`.

**RETEST SIGNATURE**:
```
INPUT  : issued ACT_v1 token to WEALTH for /health (read)
EXPECT : response.binding ∈ {OK, HOLD}; not REJECTED
       AND cross_organ_inheritance field present
       AND any REJECTED carries a populated reason field, not just an HTTP code
```

**OWNER**: A-FORGE as executor + each consuming organ (WEALTH minimum).
**RETEST OWNER**: A-FORGE :7072 and per-organ health endpoints.

---

## Cross-cutting retest protocol

Before deploying any of the nine patches as a bundle:
1. Roll forward; one patch per PR; one retest per PR.
2. Maintain a regression pack of the Opus 2026-10-11 00:41Z run's MCP trace; replay before and after.
3. Any patch that regresses another dimension is reverted; the conflict becomes a new patch.

```
STAMP: ARIFOS::SUBSTRATE_PATCHES::v2.1 :: 2026-10-11T01:00:00Z
nine_patches_owner: arifOS kernel (B.1–B.3, B.4 partial), WEALTH (B.5), HERMES (B.6), AAA cockpit (B.7, B.8, B.4 partial), A-FORGE (B.9)
regression_pack: ARIFOS::FULL_FEDERATION_REALITY_TEST::2026-10-11::v1.0 (Opus run)
```
