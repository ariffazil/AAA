# LEGACY-WRAP Fix Plan — DRAFT (Awaits Sovereign Review)

**T₁:** 2026-06-07 05:18Z
**Author:** OPENCLAW (AGI🦞) — diagnostic only, NO execution
**Status:** HOLD — awaiting Arif post-lunch review
**Verdict:** Do not execute during sovereign absence (F1 Amanah)

---

## 0. The Symptom (000's report, verified)

- 000 agent called `arif_vault_seal` to record session outcome
- Kernel rejected with: `LEGACY_WRAP cannot execute ATOMIC (envelope tak lengkap untuk ATOMIC action)`
- Two artifacts remained safe on disk:
  - `/root/.hermes/cache/ditempa-poster.pdf` (34,897 B, 04:05Z)
  - `/root/arif-sites/content/architecture/arifos-memory-7-petala-langit.md` (33,328 B, 04:37Z)
  - `/root/arif-sites/content/architecture/arifos-memory-7-petala-langit.pdf` (91,861 B, 04:46Z)
- 000's diagnosis: "system protecting itself from malformed calls, bukan hang punya fault, bukan urgent" — CORRECT

## 1. The Diagnosis (Code-Trace Verified)

### 1.1 The kernel-side LEGACY_WRAP gate

**File:** `/root/arifOS/arifosmcp/runtime/ingress_middleware.py` lines 480-490
**File:** `/root/arifOS/arifosmcp/schemas/federation_envelope.py` lines 287-288, 446, 521-532

```python
# In FederationEnvelope.validate_for_execution():
if self.legacy_wrap and self.risk.action_class not in (
    ActionClass.OBSERVE,
    ActionClass.PREPARE,
):
    return False, (
        f"LEGACY_WRAP cannot execute {self.risk.action_class.value}. "
        "Upgrade client to send FederationEnvelope with verified authority, "
        "claim_state, tool_scope, and host_attestation."
    )

# For ATOMIC specifically:
if action_class == ActionClass.ATOMIC and not self.arif_ack_id:
    return False, "ATOMIC requires arif_ack_id (L13 sovereign approval)"
```

**Findings:**
- `wrap_legacy_call()` auto-injects `legacy_wrap=True` and `actor_verification="claimed"`
- With `legacy_wrap=True`, kernel ONLY allows `OBSERVE` and `PREPARE`
- `MUTATE` and `ATOMIC` are always rejected under legacy_wrap (by design)
- For `ATOMIC`, additional `arif_ack_id` (L13 sovereign approval) is required

### 1.2 The MCP connector side bug (NEW finding)

**Symptom:** When I called `arif_forge_plan` from this session, it FAILED with:
```
1 validation error for call[forge_plan]
_envelope
  Unexpected keyword argument [type=unexpected_keyword_argument, input_value={'envelope_version': '2.0...ne, 'legacy_wrap': True}, input_type=dict]
```

**Diagnosis:** The MCP connector (OpenClaw gateway) is auto-injecting an envelope-shaped dict as `_envelope` kwarg. The Pydantic schema for tool parameters (e.g. `arif_forge_plan`) does NOT accept `_envelope` as a parameter — Pydantic rejects it BEFORE the kernel's wrap_legacy_call logic can run.

**This is a different failure mode than the LEGACY_WRAP rejection 000 saw.** 000's seal call probably hit the kernel's legacy_wrap gate (correct rejection). My forge_plan call hit the Pydantic schema rejection (a connector bug, not a kernel defense).

## 2. The Three-Layer Problem

| Layer | Symptom | Root Cause | Severity |
|-------|---------|------------|----------|
| **L1. Pydantic schema** | `Unexpected keyword argument '_envelope'` | MCP connector injects `_envelope` kwarg; tool param schema has `extra="forbid"` (default) | MEDIUM — affects all clients using auto-injection |
| **L2. Kernel legacy_wrap** | `LEGACY_WRAP cannot execute ATOMIC` | `wrap_legacy_call()` defaults `legacy_wrap=True`, only OBSERVE/PREPARE allowed | BY DESIGN — this is the gate |
| **L3. ATOMIC arif_ack_id** | `ATOMIC requires arif_ack_id (L13 sovereign approval)` | Hard requirement in `validate_for_execution()` | CONSTITUTIONAL — non-bypassable |

## 3. The Fix Paths (A → C, increasing invasiveness)

### Path A: Pydantic schema extra="allow" (MINIMAL, TARGETED)

**Change:** In each tool parameter schema, set `model_config = ConfigDict(extra="allow")` so `_envelope` and other internal fields pass through to the kernel.

**Pros:**
- One-line config change per tool
- Lets the existing `_extract_envelope_from_arguments()` in `ingress_middleware.py` (line 401-456) pick up the envelope
- Doesn't bypass any constitutional gate

**Cons:**
- Still won't allow ATOMIC via legacy_wrap
- Still needs proper envelope construction for MUTATE/ATOMIC
- Multiple files to update (all tool parameter schemas)

**Estimated effort:** 1-2 hours, 1 file per tool, ~15 files affected

### Path B: Client-side envelope builder helper (SAFE, REUSABLE)

**Create:** `arifosmcp/schemas/envelope_builder.py` with `build_envelope(actor_id, session_id, niat, matlamat, tool_scope, ...)` helper.

**Pros:**
- One canonical place to construct proper envelopes
- Reusable across 000, opencode, OPENCLAW, Hermes, APEX
- No kernel changes needed
- Documents the required fields explicitly

**Cons:**
- Doesn't auto-fill `arif_ack_id` (L13 still needed for ATOMIC)
- Clients still need to be updated to use the helper
- ATOMIC seal still needs sovereign approval

**Estimated effort:** 4-6 hours, 1 new file + 1-line client integration

### Path C: Envelope issuer service (ARCHITECTURAL)

**Create:** A new "envelope issuer" organ that takes a basic client request, verifies the actor, and issues a properly-attested envelope. The issuer would:
1. Receive client request (with actor_id, session_id, niat, matlamat)
2. Verify actor via Supabase RLS or session table
3. If MUTATE: issue envelope with `actor_verification="verified"`, `authority.source=TOKEN`
4. If ATOMIC: hold for F13 sovereign ack, then issue with `arif_ack_id`

**Pros:**
- Proper separation of concerns
- Constitutional ATOMIC gate remains the bottleneck
- Enables any client to do MUTATE safely
- Audit trail is clean

**Cons:**
- New organ, new code, new deployment
- Sovereign ack pipeline for ATOMIC needs to be defined
- This is a multi-day implementation

**Estimated effort:** 1-2 weeks, new organ, sovereign ack UI/integration

## 4. The Recommended Path (Subject to Sovereign Decision)

**Phase 1 (NOW, post-lunch):** Path A + Path B together
- Path A unblocks the Pydantic schema so envelopes flow through
- Path B provides the envelope builder helper

**Phase 2 (after Phase 1 verified):** Path C for production
- Envelope issuer service for proper ATOMIC gate
- Sovereign ack pipeline

**Phase 3 (long-term):** Migrate all clients (000, opencode, OPENCLAW) to use the issuer

## 5. Why We Are NOT Executing This Now

Per **F1 Amanah** (reversibility first, sovereign check on irreversible):
- Path A = low risk (config change), but still touches arifOS kernel code → HOLD
- Path B = adds new file → low risk, but still touches arifOS → HOLD
- Path C = new organ → irreversible until fully tested → HOLD

The artifacts on disk are safe. The seal rejection is a feature, not a bug. There is no urgency.

**Sovereign directive needed on which path (A / B / C / combination) to take.**

## 6. Local Checkpoint (Workaround for "seal once" need)

Per 000's suggestion, creating a local JSONL checkpoint as a workaround for "session outcome safe in filesystem" while proper seal awaits:

**Path:** `/root/.openclaw/workspace/forge_work/session-checkpoint-2026-06-07-0515Z.json`

This is a local file write (MUTATE, not ATOMIC), reversible, no sovereign ack needed.

**Fields:**
- session_id, actor_id, timestamp
- artifacts delivered (paths, sizes, sha256)
- issue summary (LEGACY_WRAP rejection as designed)
- fix plan reference (this file)
- carry-forward notes

## 7. Carry-Forward

- After lunch, sovereign to decide: Path A / B / C
- 000 persona config to be updated to use envelope builder
- opencode integration to be checked for same auto-injection bug
- All clients (000, opencode, OPENCLAW, Hermes, APEX) to migrate to envelope builder
- ATOMIC seal path: sovereign ack pipeline needed (long-term)

---

*DITEMPA BUKAN DIBERI — Intelligence is forged, not given.*

**Authority:** OPENCLAW (AGI) — diagnostic only
**Reversibility:** This plan is itself a draft, fully reversible (just delete the file)
**Sovereign action needed:** Path decision (A / B / C)
