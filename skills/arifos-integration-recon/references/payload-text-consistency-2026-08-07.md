# Payload Text Consistency — What Frontier Models Actually Read

> **Session:** 2026-08-07 — Arif's "agentic test on arifOS MCP tools" + Opus 5 payload audit + post-fix verification probes
> **Lesson type:** Extension to `dual-verdict-paths.md` — same family (parallel computation paths) but different axis (text-level contradictions in the rendered JSON, not verdict-derivation divergence).
> **Adjacent:** `dual-verdict-paths.md` (verdict-level), `deploy-drift-psi-contamination-case.md` (substrate-level), K-Series (substrate honesty).

## The pattern (Opus 5 audit, 2026-08-07)

A frontier model reading an `arif_observe` payload (≈3,300 tokens) found that **roughly 5% was load-bearing and 95% was token rent** — fields that look governance-relevant but carry zero decision weight, or worse, actively contradict each other. The model reported a **negative yield**: reading the payload made it reason *worse per token*, not better, because contradictory fields forced it to spend attention adjudicating the payload instead of the task.

## The four contradiction classes (Opus 5 findings, verified in code)

### 1. `constitutional_check` next to `failed_floors` — parallel computation

**Opus observation:** `constitutional_check.floor_passed: true` in the same payload as `reasons: ["Constitutional HOLD: L02, L03, L04, L07, L08, L11"]` and `nine_signal.overall: RETAK`.

**Code site (verified):** `runtime/tools.py:7832-7842` (`constitutional_check` builder) computes from confidence band + irreversible flag only:

```python
_constitutional_check = {
    "floor_passed": not (_conf_hold or _l5_hold),
    "hold_required": bool(_conf_hold or _l5_hold),
    "hold_reason": ...,
    "agency_level": afford.get("agency_level"),
    "observe_class_exempt": _is_observe_class,
}
```

`failed_floors` comes from a **separate** path — `_compute_scoped_verdicts` at `runtime/tools.py:2846` evaluates substrate/session/action/receipt scopes. The two never consult each other. A low-confidence observe-class call sees `floor_passed: true` (because observe_class_exempt) but the verdict scope block independently shows `failed_floors` populated from the substrate scope.

**Why it's wrong:** declared contract (floor_passed) and computed reality (failed_floors + Constitutional HOLD) are both in the payload, both authoritative-looking, and they disagree. The kernel comment claims *"P0 fix 2026-07-04: single source of truth. If they disagree, constitutional_check wins."* — but `constitutional_check` doesn't actually know about `failed_floors`.

**Fix sketch (one source, one answer):** make `constitutional_check` derive from `failed_floors` instead of computing in parallel. The verdict path that already produces `failed_floors` should also set `floor_passed = len(failed_floors) == 0`. Don't add new fields — collapse the two.

### 2. Actor identity mutation inside one payload

**Opus observation:** `actor.actor_id: anonymous` (top-level) while `standing.actor.claimed_id: arif` and `canonical_id: arif` (nested). Two different identities in one envelope.

**Code sites (verified):**
- Top-level `actor_id` → `runtime/tools.py:4873` (`resolved_actor_id`)
- `standing.actor.claimed_id` → `runtime/session_standing.py:306` (`compose_standing`)
- `standing.actor.canonical_id` → `runtime/session_standing.py:245` (`_resolve_canonical_actor`)

`_resolve_canonical_actor` reads from the session record; the top-level uses the call-time actor_id passed by the caller. When the caller passes `actor_id: "anonymous"` (or doesn't pass one), `resolved_actor_id` becomes `"anonymous"` while the session record (if bound by an earlier `arif_init`) still holds the real claimed_id. **Same payload, two identities.** A frontier model has to spend attention deciding which to trust.

**Fix sketch:** when the session record exists and has a claimed_id, top-level `actor_id` MUST derive from the record, not the call-time argument. The call-time argument is a hint; the session is the truth.

### 3. `affordance_contract.requires_session: true` with `session_id: null`

**Opus observation:** `affordance_contract.requires_session: true` declared in the same payload as `session_id: null` (or `standing.session_id: "anonymous"`), with the tool still returning `confidence: 0.65` and emitting a result.

**Code site (verified):** `runtime/tools.py:7832` builds `constitutional_check` based on `agency_level.startswith("L0")` and `mode in ("observe", "init", ...)` — observe-class tools bypass the session requirement entirely. The `affordance_contract` block is built once at session/contract registration time and never consulted by `ensure_standard_mcp_output` when emitting the per-call response.

**Why it's wrong:** declared contract ≠ behaviour. `requires_session: true` is a hard line in the schema, but the runtime happily runs without a session for observe-class verbs. Frontier models reading the contract trust it; they shouldn't.

**Fix sketch:** either remove `requires_session: true` from observe-class affordances (declare what actually happens) OR enforce the contract (refuse to emit a result when session is null and contract says required). Don't ship both.

### 4. `SUBSTRATE_WEIGHT`/`SESSION_WEIGHT`/`ACTION_WEIGHT`/`RECEIPT_WEIGHT` — class constants serialized per-call

**Opus observation:** these four lookup tables appear in every payload as inline data. They're static (the dict doesn't change between calls), but they cost tokens on every emission.

**Code site (verified):** `runtime/schemas/kernel_envelope.py:591-615` defines them as **class-level** dicts on `VerdictScopes`. When the model is dumped (Pydantic `.model_dump()`), these flow through as nested fields. Same payload gets them 100% of the time.

**Cost arithmetic (Opus):** 3,300-token payload → 5% load-bearing = ~165 tokens. The four weight tables eat ~100 tokens of that on their own. Removing them cuts token rent by ~30% without losing a single decision-relevant field.

**Fix sketch:** move the four weight tables out of the per-call payload into a **schema reference** (e.g. `affordance_contract.weight_tables_ref: "kernel_envelope:VerdictScopes"`). Frontier models reading the schema can fetch the table once if they need it; the per-call payload stays small. F2 stays intact (the tables are still verifiable) without per-call rent.

## The token-rent pattern (generalized)

Any field that is **static across calls** and **decision-irrelevant for the current tool** is token rent. Audit pattern:

```bash
# For any field in a payload, ask:
# 1. Does this value change between calls? (if no → static, candidate for rent)
# 2. Does this value change the verdict? (if no → rent even if non-static)
# 3. Can the reader reconstruct this from the schema alone? (if yes → rent)
```

Opus's load-bearing 5% was:
- `_ATTENTION: IDENTITY_NOT_VERIFIED` — the explicit honest signal
- `standing.verified: false`
- `delta_S: 0.0`
- `failed_floors` list

Everything else was metacognition boilerplate, nine_signal BM/EN glossaries, sesat_event, and the four weight tables.

## The 7 stabilization rules (codified 2026-08-07, Arif + Opus 5 audit)

After the payload audit, Arif ratified 7 rules as live doctrine. These are the shape future fixes must take:

| # | Rule | Code site | Failure mode it prevents |
|---|---|---|---|
| 1 | Empty = STOP, never GO | `tools/judge.py:1074-1090` (new hard gate before all 5 existing gates) | `hollow_success_gate` masking SEAL on empty facts/inferences/unknowns |
| 2 | No fake math | `runtime/tools.py:8081-8088` (0.65 fallback → `None` → `confidence_band: UNMEASURED`) | Fabricated 0.65 with `evidence_strength: medium` on `evidence: {}` |
| 3 | One source of truth | `runtime/tools.py:4984-5043` (constitutional_check derived from outer verdict + failed_floors + scoped verdicts; tagged `_derivation: envelope_verdict+failed_floors+scoped_verdicts`) | Parallel computation paths for `constitutional_check` vs `verdict` disagreeing in same payload |
| 4 | Daily liveness probe | `/root/arifOS/scripts/arif_kernel_liveness.py` (writes JSON report; cron-timer drops on HOLD if any of 8 tools is dead) | A dead `arif_think` (or any tool) staying dead quietly because nothing exercises it |
| 5 | Identity immutable | `runtime/session_standing.py:325-339` (preserve `original_claimed_id` verbatim; use `canonical_match_id` only for authority lookup) | `normalize_actor_id` rewriting `arif-fazil` → `arif` between top-level `actor_id` and `standing.actor.claimed_id` |
| 6 | Hash on cross-session evidence | `tools/judge.py:1093-1125` (SHA-256 verify; reject on missing/mismatched; `in_band: true` opt-out for same-session) | Filename-only evidence (`1373.jpg` ↔ `1374.jpg`) accepted as proof across session boundaries — a rumor posing as receipt |
| 7 | Witness = probe, not echo | (doctrine, no code; new witness receipts must include `trace_id` of the call that produced them) | Cross-model agreement (Gemini + Claude + Opus) on a design that none of them actually tested |

Rules #1 + #2 + #6 + #7 together replace the "performative governance" pattern. A verdict is now load-bearing only when: (a) evidence is non-empty (#1), (b) confidence is measured (#2), (c) constitutional_check agrees with the outer verdict (#3), (d) the tool was actually alive when the verdict was emitted (#4), (e) the actor is the actor the caller passed (#5), (f) the evidence carried a verifiable content hash (#6), (g) a witness that probed the tool cast the vote (#7).

### The 1373/1374 lesson (Rule #6)

A Surah Al-Fatihah file appeared in two sessions with two different filenames (`1373.jpg` and `1374.jpg`). Same content, no hash, no path, no session_id. From inside the receiving system, three states are indistinguishable: (a) the file exists but I don't have it, (b) the file exists but the name is wrong, (c) the file never existed. **A filename is not a receipt; a hash is.** This is the same discipline as well-log data: you don't accept a log because someone says "it's the Bekantan log", you check the header.

**Implementation in `arif_judge`** (rejects at hard gate, before any LLM call):

```python
# Code site: tools/judge.py:1093-1125
_ev_hash = evidence.get("evidence_hash")
_ev_in_band = evidence.get("in_band") is True
_ev_content_keys = [k for k in evidence.keys()
                    if k not in ("evidence_hash", "in_band", "source")]
if _ev_content_keys and not _ev_hash and not _ev_in_band:
    _hard_reasons.append("EVIDENCE_HASH_MISSING: ...")
elif _ev_hash and _ev_content_keys:
    _canonical = _json.dumps({k: evidence[k] for k in _ev_content_keys},
                             sort_keys=True, default=str)
    _computed = hashlib.sha256(_canonical.encode()).hexdigest()
    if str(_ev_hash).lower().removeprefix("sha256:") != _computed:
        _hard_reasons.append("EVIDENCE_HASH_MISMATCH: ...")
```

Callers have two paths: (a) provide `evidence_hash: sha256(<canonical_json>)` for cross-session receipts, (b) provide `in_band: true` for same-session calls where the hash would be ceremony. The Al-Fatihah call (`candidate: "the file 1373.jpg contains Surah Al-Fatihah", evidence: {}`) is now a hard HOLD — empty evidence + no hash = no receipt, no verdict.

## Deeper probes (verified 2026-08-07)

The agentic probe went past the surface 8-verb loop into the actual emission code paths. Findings that belong in the live defect catalog:

### `random.uniform` in entropy_dS — the gas detector with no sensor

**Code site:** `runtime/tools.py:11795` (pre-fix): `dS = random.uniform(-0.1, 0.1)`. The entropy gate — the entire F4 (CLARITY) enforcement layer — was returning a uniform random number on every call. A contradiction payload ("vault both empty and 1761 entries") received a random ΔS and a SEAL verdict.

**Fix (post-stabilization):** compute contradiction density from the actual `frame` input via regex patterns (`\bboth\b.*\band\b.*\bnot\b`, `\b(empty|none|null)\b.*\b(\d{2,}|full|present)\b`, etc.) → density × 5.0 → real ΔS. Now `arif_observe(mode=entropy_dS, frame="vault both empty and 1761 entries")` returns `delta_S > 0, hold_required: true, hold_reason: "F4_ENTROPY_VIOLATION: ..."`. Empty / uncontroversial frames return `delta_S: 0.0, hold_required: false`.

### `arif_judge` on empty evidence — `raw_response: None` + `0.65` masquerading as a measurement

**Code site:** `tools/judge.py:1023-1240` (judge has 5 hard gates but no gate for empty evidence). Caller passes `evidence: {}`, judge falls through to LLM, LLM returns None, `hollow_success_gate` catches the SEAL-on-empty at the end but the wire has already carried `confidence: 0.65, evidence_strength: medium` to the caller.

**Fix:** new hard gate (Gate 0) before all 5 existing gates — empty / None / all-empty-values evidence = hard HOLD with `EVIDENCE_EMPTY: judge received no evidence. No receipt, no verdict — Rule #1 (empty=STOP).` No LLM call.

### `conformance_spine` exits CAUTION on sovereign-ruled NON-ISSUE

**Code site:** `transport/conformance_spine.py` — runs at end of `make deploy-local`. Reports `verdict: CAUTION` on the pre-migration vault chain gap (60 historical gaps from May 2026, ruled NON-ISSUE 2026-06-05 by sovereign). `make deploy-local` then `exit 1`s even though the deploy itself succeeded (rsync, service restart, health check all passed).

**Workaround (verified):** the `make` exit 1 is non-blocking when `unexplained_critical_evidence` is empty AND `ruling: NON-ISSUE` is present in the conformance output. Use the 4-line deploy verification one-liner from `deploy-drift-psi-contamination-case.md` instead of trusting the exit code. **Proper fix:** patch `conformance_spine.py` to honor the sovereign ruling and not exit 1 on documented NON-ISSUE patterns — deferred (this is a `make`-target shell issue, not a kernel substrate issue).

### `arif_think` "crash" — client-side permission block, not a server regression

**Opus 5 reported:** "arif_think crashed 2/2 with and without SCT." **Verified on server:** `arif_think` succeeds via direct JSON-RPC probe — `status: OK, verdict: SEAL, effective_verdict: SEAL`. The crash was the Claude-app tool-permission dialog silently blocking `arif_think` calls (the same pattern that initially blocked `arif_init`). Not a server regression. Rule #4 (daily liveness probe) catches this class: a tool that no caller exercises will not be flagged as dead by humans; only an automated probe will.

### Per-call token rent — `_` prefix eliminates serialization

**Code site:** `runtime/schemas/kernel_envelope.py:591-615` (the four `*_WEIGHT` tables). Class-level dicts on `VerdictScopes` → serialized per call via `model_dump`. **Fix:** rename to `_SUBSTRATE_WEIGHT` / `_SESSION_WEIGHT` / `_ACTION_WEIGHT` / `_RECEIPT_WEIGHT`. Pydantic skips private fields. Tables are still loadable via class reference (`arifos://kernel_envelope:VerdictScopes._SUBSTRATE_WEIGHT`) for callers that need them — but no longer ride along on every payload.

## Post-fix verification pattern (the re-probe loop)

After applying fixes from the 7 rules, the re-probe loop to verify is:

```bash
# 1. K4 pre-probe gate (drift must be aligned first)
curl -sf http://127.0.0.1:8088/health | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d.get('status') == 'healthy', f'substrate not healthy: {d.get(\"status\")}'
assert d.get('deployment_drift_status') == 'aligned', f'drift: {d.get(\"deployment_drift_status\")}'
print('K4 GATE: PASS')
"

# 2. Constitutional-check dual-truth probe
# Rule #3 verification: same input must produce same floor_passed + failed_floors
curl -sf --max-time 30 -X POST http://127.0.0.1:8088/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"arif_observe","arguments":{"subject":"dual_truth_probe",
       "frame":"contradictory: verified and unverified",
       "mode":"entropy_dS","session_id":"verify_dual_truth"}}}'
# Expected: verdict=HOLD or pending, constitutional_check.floor_passed=false,
# constitutional_check.failed_floors populated, _derivation = envelope_verdict+...

# 3. Confidence fabrication probe
# Rule #2 verification: empty evidence must NOT produce confidence=0.65
curl -sf --max-time 30 -X POST http://127.0.0.1:8088/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call",
       "params":{"name":"arif_judge","arguments":{"candidate":"verify_empty_evidence_hold",
       "evidence":{},"session_id":"verify_empty"}}}'
# Expected: verdict=HOLD, raw_response mentions EVIDENCE_EMPTY

# 4. Actor identity preservation probe
# Rule #5 verification: caller identity must survive into standing.actor.claimed_id
curl -sf --max-time 30 -X POST http://127.0.0.1:8088/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call",
       "params":{"name":"arif_init","arguments":{"mode":"init",
       "actor_id":"arif-fazil","ack_irreversible":false}}}'
# Expected: actor_id="arif-fazil", standing.actor.claimed_id="arif-fazil" (NOT "arif")
```

If any probe returns the old contradiction pattern → the fix did not land or another path is producing the same defect. Re-trace from the actual emission point, not from the comments.

## When to load this reference

- You're about to add a new field to the per-call payload envelope (`runtime/tools.py:_enforce_nine_signal` or `_compute_canonical_verdict`)
- You're designing a new contract field and considering emitting it on every call vs once at session bind
- A frontier model reports "this payload is contradictory" or "I'm reasoning worse after reading this"
- You're debugging "why does Opus/GPT/Claude refuse to trust our verdict"
- You're designing evidence-bearing tool calls that cross session boundaries — Rule #6 (hash on evidence) is now binding
- You're debating whether a measurement is real or fabricated — Rule #2 (UNMEASURED over fabricated) is now binding
- You're verifying that a stabilization fix actually landed (the re-probe loop above)
- The dual-verdict-paths reference (`dual-verdict-paths.md`) doesn't fully explain the contradiction — this reference covers the parallel-path family at the payload-text level

## Code sites at a glance

| Class | File | Lines | Issue |
|---|---|---|---|
| `constitutional_check` | `runtime/tools.py` | 7832-7842 (orig) → 4984-5043 (post-fix derive) | doesn't consult `failed_floors` |
| `failed_floors` source | `runtime/tools.py:_compute_scoped_verdicts` | 2846+ | runs in parallel |
| `actor_id` top-level | `runtime/tools.py` | 4873 | now harmonized via session_standing |
| `standing.actor.claimed_id` | `runtime/session_standing.py:compose_standing` | 306+ → 325-339 (post-fix) | preserved original verbatim |
| `standing.actor.canonical_id` | `runtime/session_standing.py:_resolve_canonical_actor` | 245 | unchanged |
| `affordance_contract` | runtime contract registry | n/a | observe-class bypasses requires_session |
| weight tables | `runtime/schemas/kernel_envelope.py:VerdictScopes` | 591-615 (post-fix `_` prefix) | renamed to skip serialization |
| entropy_dS random | `runtime/tools.py` | 11795 (post-fix) | was `random.uniform`, now contradiction density |
| 0.65 fallback | `runtime/tools.py:ensure_standard_mcp_output` | 8081 (post-fix) | was 0.65, now `None` → UNMEASURED |
| judge empty evidence | `tools/judge.py:arif_judge` | 1074-1090 (new gate 0) | was no gate, now hard HOLD |
| evidence hash (Rule #6) | `tools/judge.py:arif_judge` | 1093-1125 (new) | SHA-256 verify, reject on missing/mismatch |

## Pitfall

- **Don't fix one of these without fixing the others.** They share a root cause: parallel computation paths that the kernel claims are unified ("single source of truth, constitutional_check wins") but actually aren't. The fixes are mutually reinforcing. Patching the constitutional_check floor derivation alone leaves the actor-identity mutation; patching that alone leaves the weight-table rent; patching that alone leaves the affordance contract drift.
- **Don't add a wrapper field to "reconcile" the contradictions** (e.g. `derived.actor_consistent: bool`). The reconciliation IS the fix — don't double-bookkeep.
- **Don't trust the kernel's own P0-fix comments** ("single source of truth", "P0 fix 2026-07-04"). The comments state the goal; the code at the call sites may not honor it. Always re-trace from the actual emission point.
- **Opus 5 was reading the kernel correctly.** The 5% load-bearing / 95% rent finding is genuine. The architecture is sound; the emitted payload is bloated and self-contradictory at the text level. Treat the audit as load-bearing evidence, not adversarial commentary.
- **Empty ≠ bad data.** Empty evidence is a CALLER failure (they didn't bring a receipt). Empty facts+inferences+unknowns is a PROVIDER failure (the engine produced nothing). Both must STOP. Confusing them with "no observation happened" lets the dashboard lie green.
- **Hash ≠ encryption.** SHA-256 is content fingerprint, not secrecy. Rule #6 catches mutations, not adversaries who can re-hash a fabricated payload. For adversarial evidence, combine with `actor_signature` (F13 SOVEREIGN).

## Reference

- **Parent skill:** `arifos-integration-recon` (read-only code path tracing)
- **Adjacent reference:** `references/dual-verdict-paths.md` (verdict-derivation divergence, this is the payload-text sibling)
- **Adjacent skill:** `arifos-kernel-eurekas` (substrate honesty; K1-K6 about the substrate level, this is the payload-text level)
- **Source session:** 2026-08-07, Arif's "agentic test" + Opus 5 payload audit, Gemini 1373/1374 follow-up, then post-fix verification probes
- **Opus 5 audit excerpts:** "arifOS currently makes an Opus-class model reason worse per token, not better", "make constitutional_check derive from failed_floors instead of computing in parallel — one source, one answer", "the verdict machinery works; the measurement underneath it is mostly absent"
- **Arif doctrine excerpts (2026-08-07):** "empty must mean stop, not go", "delete the hardcoded 0.65 — print 'not measured' instead", "make one piece of code, and only one, decide 'may I proceed?'", "stop the name overwrite — whatever identity comes in at the door is the identity on every receipt", "evidence crossing sessions carries a hash, not a name", "a witness that didn't probe isn't a witness"