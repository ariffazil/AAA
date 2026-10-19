# External Audit Fix — F01 / F02 / F03

**Date:** 19 October 2026 · **Branch:** `fix/external-audit-f01-f03` · **Commit:** `76b568025`
**Source of findings:** Agentic Thinking Ltd, "arifOS Standard Evaluation", 18 Oct 2026, pinned at `8edf8bbd2`
**Executed by:** HERMES (the scheduled Claude Code agent never ran — see §5)

---

## 1. WHAT CHANGED

| Finding | File | Change |
|---|---|---|
| F02 receipts verify over corrupt data | `arifosmcp/runtime/receipt_store.py` | New `all_receipts_strict()` + `ReceiptParseError`; `verify_chain()` rewired to strict; old behaviour preserved as `all_receipts_tolerant()` |
| F01 secrets in lists survive redaction | `arifosmcp/runtime/telemetry.py` | New `_redact_value()` walks lists/tuples; `metadata` redacted at NATS and local sinks |
| F03 refusal claims a bound session | `arifosmcp/runtime/tools.py` | New `_arif_init_refusal_fields()`; the `arif_init` envelope is now derived from the input-contract outcome |

Six files staged: 3 source, 3 tests. 530 insertions, 15 deletions.

## 2. BEFORE / AFTER

### F02 — receipt chain verification

| Case | Before | After |
|---|---|---|
| Valid 3-record chain | `(True, "")` | `(True, "")` |
| Malformed trailing line | **`(True, "")`** | `(False, "malformed_record at line 4: malformed JSON: ...")` |
| File containing only malformed lines | **`(True, "")`** | `(False, "malformed_record at line 1: ...")` |
| Truncated final record | **`(True, "")`, record silently dropped** | `(False, "malformed_record at line 3: ...")` |
| Corrupted middle row | `(False, "chain_broken ...")` | `(False, ...)` — unchanged |
| Altered signature | `(False, "signature_invalid ...")` | unchanged |
| Wrong key | `(False, "signature_invalid ...")` | unchanged |
| Salvage inspection of a damaged file | `all_receipts()` skipped rows silently | `all_receipts_tolerant()` — same behaviour, explicitly named |

`all_receipts()` is kept as a deprecated alias for `all_receipts_tolerant()` so no caller breaks,
but it is no longer on the verification path.

### F01 — telemetry redaction

| Input | Before | After |
|---|---|---|
| `{"api_key": "CANARY"}` | `[REDACTED]` | `[REDACTED]` |
| `{"outer": {"api_key": "CANARY"}}` | `[REDACTED]` | `[REDACTED]` |
| `{"items": [{"api_key": "CANARY"}]}` | **`CANARY` intact** | `[REDACTED]` |
| `{"items": ["CANARY"]}` | **intact** | scanned for SCT tokens |
| tuple of dicts | **intact** | redacted, tuple type preserved |
| list > 100 items | `[list:N items]` | `[list:N items]` — bounded handling kept |

Additionally: the **NATS and local (Postgres) sinks** were passing `metadata` through unredacted.
Only the Langfuse path redacted. Both now call `_redact(metadata)` at the sink.

### F03 — arif_init refusal

Live response before (probed `127.0.0.1:8088`, `tools/call arif_init {}`):

```
status: HOLD · error_code: MISSING_INPUT · session_id: unknown · actor: anonymous
facts: ["Session bound (deterministic identity bind)"]
next_safe_action: "Proceed to arif_observe or arif_think with this session."
```

After (unit-tested at the MCP boundary):

```
facts: ["arif_init REFUSED — missing required input: intent",
        "No session was created. Session id is unknown; no identity was bound."]
next_safe_action: "Supply intent explicitly, then retry arif_init.
                   Do not proceed to arif_observe or arif_think — there is no session."
status: HOLD (unchanged)
```

The control did refuse before and still refuses. What changed is that the text no longer
contradicts the structured verdict. Positive control preserved: a successful init still
reports the deterministic bind.

## 3. TEST OUTPUT (verbatim)

```
$ /root/arifOS/.venv/bin/python -m pytest \
    tests/runtime/test_telemetry_redaction.py \
    tests/runtime/test_receipt_store_strict_verify.py \
    tests/runtime/test_arif_init_refusal_metacognition.py -q
23 passed, 5 warnings in 3.85s
```

Wider regression, `tests/runtime -k "telemetry or receipt or init"`:

```
6 failed, 106 passed, 1 skipped, 2127 deselected in 8.59s
```

**All 6 failures are pre-existing and unrelated to this change.** Verified individually:

| Test | Cause |
|---|---|
| `test_capability_probe::test_run_aborts_loudly_on_init_failure` | DNS resolution failure (`socket.gaierror -3`) — sandbox has no network |
| `test_tools_advanced::test_session_init_returns_binding_governance_and_public_tools` | Expects `result["binding"]`; `_arif_session_init` returns `result["session"]` — shape drift predating this work |
| `test_gate_2d_sensitive_path::test_gate_2d_bare_receipt_string_does_not_exempt` | Gate-2d exemption logic, untouched |
| `test_h2_h3_ratification::test_plan_mode_emits_plan_receipt` | Expects OK, gets HOLD — untouched path |
| `test_mcp_resource_integrity::test_canonical_uri_has_meta` (×2) | MCP resources missing `_meta` — untouched |

## 4. WHAT DID NOT HAPPEN

- **No deploy.** The live process on `:8088` runs from `/opt/arifos/current`, not `/root/arifOS`.
  These fixes are **not live**. Deployment requires a release step and a restart, which was
  outside this task's authority envelope.
- **No push.** The branch is local only. `git push` not run.
- **No PR, no merge.**
- **Live smoke test not performed** — the running kernel predates the change, so probing it would
  have proved nothing. Recorded honestly rather than reported as a pass.

## 5. THE SCHEDULED AGENT NEVER RAN

A Claude Code session was dispatched at ~03:00 to execute this overnight. It **did not run**:
no report, no log, no commit, no process. The three test files it wrote at 02:53 were present
and failing (14 failed / 9 passed) with no source changes.

HERMES executed the work directly at 10:38 the same day. The prompt at
`/root/AAA/prompts/2026-10-19-external-audit-fix.md` remains as the specification of record;
the code was written to match it.

## 6. WHAT WAS REFUSED TO TOUCH

Pre-existing uncommitted work by other agents, left exactly as found:

- `arifosmcp/runtime/fastmcp_ext/transports.py` (modified)
- `arifosmcp/server.py` (modified)
- `arifosmcp/transport/http.py` (modified)
- `docs/agents/laws/LAW_OF_FORGING_CONFIGURATION.md` (modified)
- `arifosmcp/runtime/tailnet_identity.py` (untracked)
- `tests/runtime/test_tailnet_identity.py` (untracked)

Also untouched: `/root/AAA/governance`, `/root/AAA/canon`, `/root/arifOS/GENESIS` (chattr +i).

## 7. STILL OPEN

1. **Deployment.** The fix is committed but not live. Needs a release + restart decision.
2. **F02 callers.** `all_receipts()` is used elsewhere for listing. Every caller should be
   reviewed to decide whether it wants tolerant or strict semantics — the deprecated alias makes
   the wrong choice silent. Grep before the next release.
3. **The other two audit findings are unaddressed** — none were reported beyond F01–F03.
4. **Live smoke** of F03 must be repeated after deploy.

---
