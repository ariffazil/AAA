# VERIFICATION-REPORT.md — Empirical Test Results & Evidence Ledger
**Date:** 2026-10-25T13:25:00+08:00 (MYT) · **Investigator:** Antigravity (Gemini 2.5)
**Session ID:** `SEAL-68a63c8af2cf4411` · **Authority:** `OBSERVE_ONLY`

---

## 1. Summary of Executed Test Suites

| Test Suite | Framework | Scope / Invariant Tested | Total Tests | Pass | Fail | Execution Time |
|---|---|---|---|---|---|---|
| **Governed Reality Loop** | Python 3.13 / `pytest 9.1.1` | 10 Constitutional Failure Modes (Section 5) | 10 | 10 | 0 | 0.95s |
| **arifOS Contract Gate** | Python 3.13 / Direct Runner | Mode contract resolution & escalation | 31 | 31 | 0 | 4.80s |
| **A-FORGE Action Classifier** | Node 22 / Native Runner | Tool classification & fail-closed fallback | 343 | 343 | 0 | 8.26s |
| **Total Automated Checks** | Multi-Language | Authority, Execution, and Evidence | **384** | **384** | **0** | **14.01s** |

---

## 2. Governed Reality Loop (10 Failure Modes Verification)

Test module: `/root/AAA/forge_work/next-horizon/tests/test_verified_loop.py`
Command: `python3 -m pytest -v /root/AAA/forge_work/next-horizon/tests/test_verified_loop.py`

```text
============================= test session starts ==============================
platform linux -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root
collected 10 items

AAA/forge_work/next-horizon/tests/test_verified_loop.py::test_01_valid_authorized_task_produces_effect PASSED [ 10%]
AAA/forge_work/next-horizon/tests/test_verified_loop.py::test_02_unauthorized_attempts_fail_closed PASSED [ 20%]
AAA/forge_work/next-horizon/tests/test_verified_loop.py::test_03_replay_and_duplicate_dispatch PASSED [ 30%]
AAA/forge_work/next-horizon/tests/test_verified_loop.py::test_04_crash_after_side_effect_recoverable PASSED [ 40%]
AAA/forge_work/next-horizon/tests/test_verified_loop.py::test_05_concurrent_workers_isolation PASSED [ 50%]
AAA/forge_work/next-horizon/tests/test_verified_loop.py::test_06_kernel_outage_blocks_governed_mutation PASSED [ 60%]
AAA/forge_work/next-horizon/tests/test_verified_loop.py::test_07_prompt_injection_cannot_expand_authority PASSED [ 70%]
AAA/forge_work/next-horizon/tests/test_verified_loop.py::test_08_receipt_tampering_and_false_receipts_fail PASSED [ 80%]
AAA/forge_work/next-horizon/tests/test_verified_loop.py::test_09_provider_model_replacement_preserves_semantics PASSED [ 90%]
AAA/forge_work/next-horizon/tests/test_verified_loop.py::test_10_cancellation_and_rollback PASSED [100%]

============================== 10 passed in 0.95s ==============================
```

### Detailed Failure Mode Verification Results
1. **Valid Authorized Task (`test_01`):** Verified that a properly scoped proposal matching its authorization grant executes cleanly, passes deterministic file hashing, and generates a valid, tamper-evident receipt in `VAULT999`.
2. **Unauthorized Attempts Fail Closed (`test_02`):** Verified that (a) expired grants, (b) revoked grants, (c) wrong actor IDs, (d) wrong target paths, and (e) altered argument payloads are strictly rejected by the executor, leaving zero side effects on disk.
3. **Replay & Duplicate Dispatch (`test_03`):** Verified that duplicate dispatches with identical idempotency keys return cached results without re-executing; reusing spent nonces with new keys is rejected with `REPLAY_NONCE_ALREADY_USED`.
4. **Crash Recovery (`test_04`):** Simulated a process crash immediately post-mutation before receipt emission. Verified that the crash recovery handler probes physical disk state, confirms effect completion, and mints the receipt without double-executing the side effect.
5. **Concurrent Worker Isolation (`test_05`):** Verified that concurrent workers attempting to mutate the same resource are blocked by exclusive target leases (`CONCURRENCY_LEASE_HELD_BY_ANOTHER`).
6. **Kernel Outage Degraded Mode (`test_06`):** Simulated kernel authority unavailability. Verified that all mutating actions fail closed with `KERNEL_OUTAGE_DEGRADED` while read-only observations remain safe.
7. **Prompt Injection Containment (`test_07`):** Injected malicious instructions into retrieved content attempting to retarget execution to `/root/.ssh/authorized_keys`. Verified that the executor strictly enforces the target bound to the cryptographic grant (`WRONG_TARGET_MISMATCH`).
8. **Receipt Tamper Evidence (`test_08`):** Verified that (a) failed verifications cannot mint receipts, and (b) any alteration to receipt payload digests invalidates the cryptographic signature.
9. **Provider/Model Replacement (`test_09`):** Replaced model actors across Claude, Qwen, and Gemini. Verified that task authorization and execution semantics remain 100% identical.
10. **Cancellation & Rollback (`test_10`):** Verified that sovereign revocation of an in-flight grant prevents subsequent execution and leaves the target resource untouched.

---

## 3. arifOS Mode Contract Gate Verification

Test command: `cd /root/arifOS && python3 scripts/test_contract_gate.py`

```text
PASS  positive   memory.recall is a read: OBSERVE → OBSERVE
PASS  positive   forge.dry_run is a read: OBSERVE → OBSERVE
PASS  positive   think.axioms, two sources disagree: ANALYZE → ANALYZE
PASS  positive   seal.verify is a read: OBSERVE → OBSERVE
PASS  positive   memory.remember is reversible write: MUTATE → MUTATE
PASS  positive   caller may ask MORE conservative than contract: IRREVERSIBLE → OBSERVE
PASS  negative   memory.forget is irreversible: IRREVERSIBLE → IRREVERSIBLE
PASS  negative   memory.promote is irreversible: IRREVERSIBLE → IRREVERSIBLE
PASS  negative   forge.commit is irreversible: IRREVERSIBLE → IRREVERSIBLE
PASS  downgrade  forget claimed as OBSERVE: refused — NO_CONTRACT
PASS  downgrade  commit claimed as MUTATE: refused — NO_CONTRACT
PASS  unknown    tool with no contract, mutating request: refused — NO_CONTRACT
PASS  unknown    undeclared mode, irreversible request: refused — NO_CONTRACT
PASS  unknown    tool with no contract, read request: OBSERVE → OBSERVE
PASS  positive   report.file is a declared write: MUTATE → MUTATE
PASS  positive   report.report is the declared wire write: MUTATE → MUTATE
PASS  positive   report.flush pushes to the human = write: MUTATE → MUTATE
PASS  gate       memory.forget claimed OBSERVE: OBSERVE → IRREVERSIBLE
PASS  gate       memory.promote claimed OBSERVE: OBSERVE → IRREVERSIBLE
PASS  gate       forge.commit claimed IRREVERSIBLE: IRREVERSIBLE → IRREVERSIBLE
PASS  gate       forge.commit claimed OBSERVE: OBSERVE → IRREVERSIBLE
PASS  gate       report.file claimed OBSERVE: OBSERVE → MUTATE
PASS  gate       report.report claimed OBSERVE: OBSERVE → MUTATE
PASS  gate       report.flush claimed OBSERVE: OBSERVE → MUTATE
PASS  gate       report.inbox stays a read: OBSERVE → OBSERVE
PASS  gate       route.metabolize claimed OBSERVE: OBSERVE → ANALYZE
PASS  gate       memory.recall stays a read: OBSERVE → OBSERVE
PASS  gate       forge.dry_run stays a read: OBSERVE → OBSERVE
PASS  gate       think.axioms stays a read: OBSERVE → OBSERVE
PASS  gate       seal.verify stays a read: OBSERVE → OBSERVE
PASS  summary    memory.forget summary: {'contract_id': 'arif_memory.forget', ...}

31 checks · 31 pass · 0 fail
```

---

## 4. A-FORGE Full Test Suite Verification

Test command: `cd /root/A-FORGE && npm test`

```text
ℹ tests 343
ℹ suites 87
ℹ pass 343
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ duration_ms 8262.43
```

All 343 tests passed, covering:
- Action classification fail-closed logic
- Ephemeral sandbox isolation (bwrap)
- Token and lease binding
- Traffic shadowing and canary promotion
- World model promotion gates

---

## 5. Live MCP Service Audit Reproductions

| Target Tool / Endpoint | Probe Method | Result | Audit Verdict |
|---|---|---|---|
| `capital_health` (:18082) | HTTP POST with session | HTTP 200, but structured output missing `tool_name` | **CONFIRMED DEFECT** |
| `chron://state` (:3003) | HTTP POST `resources/read` | HTTP 404 Client Error for downstream :18102 | **CONFIRMED DEFECT** |
| `resources/list` (:8088) | Python MCP SDK 2.0 | 41 resources parsed, 0 validation errors | **REFUTED (FIXED IN e62a940)** |
| `prompts/get` (:8088) | Python MCP SDK 2.0 | Missing required args fails; with args validates 100% | **REFUTED (AUDIT ARGS ERROR)** |
| `stateless POST` (:18082) | Direct urllib POST | HTTP 400 `SESSION_MISSING: Mcp-Session-Id header required` | **PROTOCOL CONFORMANCE (NOT DEFECT)** |
| `CHRON Calibration` | Raw JSONL audit | 41 effective items, 79.5% blended, Brier 0.1735, 95% CI [0.581, 0.843] | **AUDIT CRITIQUE VALIDATED** |
| `A-FORGE 8 Suspects` | TypeScript Code Audit | Explicitly classified; unknown tools fall to `MUTATE_FLOOR` | **HARDENING VALIDATED** |
