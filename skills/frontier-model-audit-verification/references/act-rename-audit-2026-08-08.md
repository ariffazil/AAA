# ACT Rename Audit — 2026-08-08 Session

**Trigger:** Arif publishes a self-authored article ("I'm Not a Programmer...") about the SCT→ACT rename journey.
**Load skill:** `frontier-model-audit-verification` + `verify-nested-sibling-reports`
**When:** Arif pastes any article/essay about his own system. Treat as self-authored analysis requiring independent verification.

## Session findings (verified OBS)

### Writer/Reader fracture (Bug 1)

**Writer** (`act_token.py:516`): emits claim key `"act_v": ACT_VERSION` under ACT_PREFIX `act_v1`.
**Readers** using old key name `"sct_v"` → returns `None`:

| File:line | Field read | Actual key | Result |
|---|---|---|---|
| `session_standing.py:950` | `claims.get("sct_v")` | `"act_v"` | **None** |
| `session.py:886` | `_claims.get("sct_v")` | `"act_v"` | **None** |
| `session.py:879` | `out["standing_source"] = "sct"` | hardcoded | **stale label** |
| `session.py:904` | `"sct_sid": _sct_sid` | old key name | **stale** |
| `authority_context.py:29` | `ProofMethod = Literal["ed25519", "session_token", "sct_v1", "anon"]` | `sct_v1` in union | **stale** |

**Note:** `verify_sct` at line 628 does dual-read (`claims.get("act_v") or claims.get("sct_v")`) — validation works. Break is downstream.

**Lesson (Rule 10):** A rename is not done until the reader is renamed. Ship writer and reader together.

### Schema drift on consent (Bug 2)

`arif_forge` tool signature (`forge.py:138-163`) accepts `ack_irreversible` but does NOT include `seal_verdict_id` or `approved_action_hash`.
`forge_preflight.py:270-271` accepts both as function parameters and verifies Ed25519 integrity.
**Gap:** schema exposes fields in MCP inputSchema, but Python rejects them as `unexpected_keyword_argument`.

### Pre-existing test failure

`test_forge_preflight_irreversible_action_requires_ack` fails on clean HEAD `22146b9d9`:
- Test calls `forge_preflight(session_id="sess_irrev", ...)` → `session_valid=False`
- `human_ack_required` is set in `stage_09` (line 682+) but early gates short-circuit before reaching it
- Test asserts on a field set by a stage the inputs never reach
- **Pre-existing, verified by git stash + re-run on clean HEAD**

### Uncommitted code in working tree

`pre_execution_gate.py` has 188 lines added vs HEAD. Includes:
- `ForgedClassificationError` class (structural hardening, self-contained)
- Gate 2.55 (classification contradiction guard)
- Calls to undefined `_resolve_independent_evidence()` and `_resolve_previous_stage_verified()` → NameError on first MUTATE call

**This code must be split:** commit the safe structural parts, revert or stub the undefined-function calls.

## Arif's contribution claims (review)

| Claim | Verdict | Evidence |
|---|---|---|
| "I accidentally invented a new question for AI" | **INT (overclaim)** | Governance-beats-capability is an established literature; what's genuine is the working receipt |
| "The PTW analogy" | **OBS** | Genuinely from oilfield experience, no AI contribution |
| "authority should not be self-generated" | **OBS receipt** | His own red-team test returned `OBSERVE_ONLY` for self-authorised agent — live receipt, not hope |
| "Most Python was written by AI agents" | **OBS** | Confirmed by codebase history; Arif's contribution is the naming/judgment layer |

**Rule for reviewing Arif's self-authored essays:** Claim the receipt, not the invention. The receipt (kernel refuses self-authorisation) survives contact with the field. The invention claim (I invented governance-for-AI) does not.

## Follow-up work items

1. Fix Bug 1: rename `sct_v` → `act_v` in `session_standing.py:950`, `session.py:886,879,904`, `authority_context.py:29`, `capability_token.py:83` docstring
2. Fix Bug 2: add `seal_verdict_id` and `approved_action_hash` to `arif_forge` tool signature in `forge.py:138-163`
3. Split `pre_execution_gate.py` working tree: commit `ForgedClassificationError` + Gate 2.55, revert/stub undefined helper calls
4. Fix pre-existing test: update `test_forge_preflight_irreversible_action_requires_ack` inputs to pass early gates

## Key file locations

| What | Where |
|---|---|
| Token minting | `/root/arifOS/arifosmcp/runtime/act_token.py:465` (writer: `act_v`) |
| Token verification | `/root/arifOS/arifosmcp/runtime/act_token.py:548` (dual-read: `act_v` or `sct_v`) |
| Session claims reader | `/root/arifOS/arifosmcp/runtime/session_standing.py:950` (old: `sct_v`) |
| Session bridge reader | `/root/arifOS/arifosmcp/tools/session.py:886` (old: `sct_v`) |
| Standing source label | `/root/arifOS/arifosmcp/tools/session.py:879` (hardcoded `"sct"`) |
| Forge tool signature | `/root/arifOS/arifosmcp/tools/forge.py:138` (missing `seal_verdict_id`) |
| Forge preflight | `/root/arifOS/arifosmcp/runtime/forge_preflight.py:270` (accepts both params) |
| ACT spec doc | `/root/A-FORGE/docs/ACT_CANONICAL_SPEC.md` (still titled "SCT") |
| Pre-existing failing test | `/root/arifOS/tests/adversarial/test_forge_preflight_chain.py:79` |
| Pre-execution gate (uncommitted) | `/root/arifOS/arifosmcp/runtime/pre_execution_gate.py:427+` (Gate 2.55) |
