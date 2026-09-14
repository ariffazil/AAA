# SEMANTIC ALIGNMENT AUDIT — Phase C

**Program:** Entropy Reduction (Phases C+D) · arifOS Federation
**Node:** KVM8 forge (100.64.0.2 / 72.62.71.199)
**Audit:** 2026-09-14 · Asia/Kuala_Lumpur
**Method:** Read source + live probe. Every finding is falsifiable and cites `file:line`.
**Scope:** `/root/arifOS/arifosmcp`, `/root/A-FORGE/src`, `/root/AAA/governance`, plus live surfaces.

> **Question:** does the *name* match the *behaviour*?

---

## 0. Live ground truth (observed, not inferred)

| Surface | Port | Observed state |
|---|---|---|
| arifOS kernel | :8088 | `healthy` · floors 13/13 · registry_size 62 · declared 48 · **exposed 8** |
| Kernel exposed tools | :8088 | `arif_init arif_observe arif_think arif_route arif_memory arif_judge arif_forge arif_seal` |
| A-FORGE | :7072 | `healthy` · 120 tools |
| FED | :7074 | `healthy` · role `ADVISORY_ONLY` |
| VAULT999 writer | :5001 | `healthy` · `vault_seals_count: 12` |
| WELL | :18083 | **`degraded`** · authority `REFLECT_ONLY` · `/metrics` 404 |
| WEALTH | :18082 | `healthy` |
| GEOX | :8081 | `healthy` · **SURFACE_DRIFT** raw_live=100 raw_drift=74 canonical=26 |
| AAA A2A | :3001 | `degraded` |
| FRAME | :18085 | `ok` (independent observer) |

---

## 1. Classification summary

| Class | Count |
|---|---|
| TRUE_NAME | 6 (controls) |
| PARTIAL_NAME | 3 |
| MISLEADING_NAME | 6 |
| **FALSE_NAME** | **8** |

---

## 2. FALSE_NAME findings (name states something the code does not do)

### F-01 — `verify_federation_sct()` verifies nothing on the live path
**File:** `/root/AAA/governance/federation_act.py:265`, fail-open branch `:389–417`
**Claimed:** cryptographically verifies a federation token. Module header (`:13`) states *"Tokens are forged, not assumed."*
**Actual:** when the kernel answers `valid=false` (which the code's own comment `:391` says is the *normal* live result — `status=pending`), execution falls into a **fail-OPEN** branch that base64-decodes the token payload and trusts the plaintext `auth` claim **without verifying the HMAC**:

```python
payload_auth = payload.get("auth") or payload.get("authority")
if payload_auth in ("FULL", "SOVEREIGN", "LIMITED_MUTATE", "OPERATOR"):
    return SCTVerification(ok=True, ...)   # no signature check
```

**Falsified empirically** (2026-09-14):
```
FORGED TOKEN RESULT: ok= True  authority= SOVEREIGN  actor= arif
VERDICT: *** BYPASS CONFIRMED — forged token accepted ***
```
Token used: `act_v1.<b64({"actor":"arif","auth":"SOVEREIGN"})>.deadbeefdeadbeef` — garbage HMAC.
**Verdict:** FALSE_NAME. The name promises verification; the code performs claim-trust.

### F-02 — `gate_tool_ingress()` admits forged SOVEREIGN tokens
**File:** `/root/AAA/governance/federation_act.py:577` → delegates to F-01
**Wired into:** `GEOX/src/geox_mcp/geox_middleware.py:593`, `WELL/server.py:13382`, `WEALTH/wealth_mcp/server.py:573`
**Empirical result** (6 attempts, 2026-09-14):
```
ALLOWED=4  REJECTED=2   (rejections were ARIFOS_UNREACHABLE timeouts, not structure)
```
The gate rejects only when the kernel is *slow*. When the kernel answers within the 2 s window, the forged token is **allowed** as SOVEREIGN into GEOX/WELL/WEALTH.
**Verdict:** FALSE_NAME. Named an ingress gate; functions as a conditional pass-through for unauthenticated callers.

### F-03 — `forge_verify` never verifies
**File:** `/root/A-FORGE/src/infrastructure/tools/forge_verify.ts:107–142`
**Claimed:** *"WAJIB 2 — Independent verification lane … Returns VERIFIED, MISMATCH, INCONCLUSIVE, or STALE"*.
**Actual:** every criterion check is hardcoded `passed: false` (`:123` — *"Requires actual verification implementation"*) and the result is always `state: "INCONCLUSIVE"` (`:139`). It never calls `permitted_observation_tools`.
**Verdict:** FALSE_NAME. Verification lane that cannot return VERIFIED.

### F-04 — `HumanEscalationClient.escalate()` is an empty method
**File:** `/root/A-FORGE/src/application/approval/index.ts:145–150`
```ts
export class HumanEscalationClient {
  async escalate(_event: Record<string, unknown>): Promise<void> {}   // no-op
}
export class WebhookHumanEscalationClient extends HumanEscalationClient {}
export class NoOpHumanEscalationClient    extends HumanEscalationClient {}
```
Both subclasses inherit the empty body — including `WebhookHumanEscalationClient`, whose name promises a webhook POST.
**Verdict:** FALSE_NAME. Human escalation never reaches a human.

### F-05 — `audit_seal()` seals into a buffer that is never flushed
**File:** `/root/arifOS/arifosmcp/runtime/context_audit.py:339` (append at `:379`), buffer `:219`
**Actual:** appends to the module-global `_SEAL_BUFFER: list = []` and returns `vault999_status: "queued_for_phase2_flush"`. No flush, drain, or sweeper exists anywhere in the module (grep: only `.append` and the read-back helper).
**Verdict:** FALSE_NAME. A "seal" writes to in-process memory that dies with the process.

### F-06 — `_wrap_call()` backs an action-named alias surface that performs no action
**File:** `/root/arifOS/arifosmcp/runtime/tools.py:3305`
```python
async def _wrap_call(name: str, **kwargs: Any) -> dict[str, Any]:
    return {"ok": True, "tool": name, "kwargs": kwargs}
```
Bound to `VAULT_SEAL`, `APEX_JUDGE`, `INIT_ANCHOR`, `AGI_REASON`, `ASI_CRITIQUE`, `verify_vault_ledger`, `audit_rules`, `check_vital`, `search_reality`, `ingest_evidence`, `reality_atlas` and the lowercase aliases (`vault_seal = VAULT_SEAL`, `apex_judge = APEX_JUDGE`, …).
Each returns `{"ok": True}` **without executing anything** — `VAULT_SEAL` never writes VAULT999; `verify_vault_ledger` never reads the chain.
**Latent, not live:** verified against the running kernel — `/tools` and `tools/list` expose exactly the 8 canonical tools; none of the above appear on the public wire (`exposed_tools: 8`).
**Verdict:** FALSE_NAME (source-level, latent). Not a live breach today; a breach the moment any of these names is re-registered.

### F-07 — `forge_health_check` returns a hardcoded "healthy"
**File:** `/root/A-FORGE/src/interfaces/mcp/core.ts:1510–1530`
**Actual:** returns a static literal `{ status: "healthy", version: "2.0.0-genome-stable", genome: {…} }`. It probes no dependency, reads no ledger, checks no organ.
**Verdict:** FALSE_NAME. A banner, not a health check.

### F-08 — `forge_sandbox_run` does not sandbox
**File:** `/root/A-FORGE/src/interfaces/mcp/forge8Verbs.ts:361–383`
**Claimed:** verb description and inline comment (`:377`) — *"Execute staged artifact in isolated sandbox."*
**Actual:** the handler calls raw `execAsync("bash artifact.code", { cwd: staging_path, timeout })`. No `bwrap`, `firejail`, `docker`, or namespace is invoked.
The file **imports** the containment engine (`:43–52` — `runInSandbox`, `createSandbox`, `SandboxStorage`, …) and then **uses none of it**: grep across the file finds those symbols only on the import lines.
**Verdict:** FALSE_NAME. The sandbox was imported, not installed.

---

## 3. MISLEADING_NAME findings (name over-claims scope)

### M-01 — `arif_forge` (010_FORGE) cannot forge
**File:** `/root/arifOS/arifosmcp/tools/forge.py:382`, module docstring `forge_execute.py:1` ("010_FORGE Stub")
The P0 execution boundary is **CLOSED** (audit ref `arif_falsification_audit_2026-07-25`):
```python
_P0_ALLOWED_MODES = {"query"}
if mode not in _P0_ALLOWED_MODES:
    return ForgeOutput(status="HOLD", ...)   # all MUTATE/ATOMIC halted
```
One of the 8 exposed kernel tools is an execution verb that executes nothing but read-only queries.
**Verdict:** MISLEADING_NAME.

### M-02 — `forge_execute` (governance path) issues a receipt without executing
**File:** `/root/A-FORGE/src/interfaces/mcp/forge8Verbs.ts:670–706`
After validating the human seal token it sets `stageMeta.status = "sealed"`, `executed_at = now`, generates `execution_id` and `receipt_uri`, then returns `success: true, authorization_path: "governance_stage"`. **No process is spawned.** The name and the receipt say "executed"; only authorization happened.
**Verdict:** MISLEADING_NAME (phantom receipt).

### M-03 — `runStage()` does not run a stage
**File:** `/root/A-FORGE/src/infrastructure/metrics/prometheus.ts:79`
```ts
export async function runStage<T>(stage: MetabolicStage, fn: () => Promise<T>) {
  const end = metabolicStageDuration.startTimer({ stage });
  try { return await fn(); } finally { end(); }
}
```
Wraps the call in a Prometheus timer and nothing else. No order check, no precondition, no `MetabolicStage` state transition. Call sites (`core.ts:1264,1516,1560,1628`) label themselves as `"000_INIT"`, `"555_HEART"`, `"777_FORGE"` with no enforcement behind the label.
**Verdict:** MISLEADING_NAME.

### M-04 — `verdict-interceptor` flattens constitutional verdicts to "ERROR"
**File:** `/root/A-FORGE/src/domain/governance/verdict-interceptor.ts:53–63`
`determineStatus()` maps `HOLD` and `VOID` — deliberate constitutional states — into `"ERROR"`, losing the distinction between *refusal* and *failure* at the interception boundary.
**Verdict:** MISLEADING_NAME.

### M-05 — `ApprovalBoundary` / `ApprovalRouter` are marked replaced but still live
**Files:** `application/approval/ApprovalBoundary.ts:1` (*"⚠️ REPLACED by constitutional governance"*), `HumanEscalationClient.ts:1` (same), yet `application/personal-v2/PersonalOS.ts:77–88` still constructs and uses `new ApprovalBoundary()`.
**Verdict:** MISLEADING_NAME (orphaned-but-referenced; two approval doctrines coexist).

### M-06 — `state_machine_guard` / `execution_state_machine` enforce nothing by default
**File:** `/root/arifOS/arifosmcp/runtime/executor.py:23`
```python
_STATE_MACHINE_ENFORCE = os.getenv("ARIFOS_STATE_MACHINE_ENFORCE", "false")...
```
`state_machine_guard.py` (STAGE_ORDER 000→999, IRON LAW 4 SEAL_BEFORE_ACT) is **imported nowhere** in the live runtime (grep: only its own module). The documented IRON LAWS are not gate law.
**Verdict:** MISLEADING_NAME.

---

## 4. PARTIAL_NAME findings (honest in the docstring, misleading in the name)

### P-01 — `vault_sealer.write_audit_receipt()`
**File:** `/root/arifOS/arifosmcp/runtime/vault_sealer.py:1–11`
Module named *sealer*; docstring is candid — *"a clerk-level audit receipt, not a sovereign SEAL … Sovereign SEAL (arif_seal / 888_JUDGE) remains the only binding verdict."* Callers reading only the import name will believe they sealed.
**Verdict:** PARTIAL_NAME.

### P-02 — `SealService.validateDag()`
**File:** `/root/A-FORGE/src/domain/governance/SealService.ts:49,68`
Class named `SealService`; the entry method validates a DAG and returns a `SealVerdict` — it never appends to VAULT999. (The class does compute a `sealId`, which is what makes the name only *partially* wrong.)
**Verdict:** PARTIAL_NAME.

### P-03 — `witness_class.py` (positional witness taxonomy)
**File:** `/root/arifOS/arifosmcp/runtime/witness_class.py:5`
Header: *"Status: STAGED — NOT DEPLOYED … Not wired into the live runtime."* The file itself documents the gap precisely: the live kernel reports `tri_witness: [true, true, true]` on **substantive** witnesses while never recording **position**, so `substantive=ai, position=SELF` (self-attestation) is displayed identically to an external witness.
**Verdict:** PARTIAL_NAME — the name is honest; the *live witness* it names is not what is actually running.

---

## 5. TRUE_NAME controls (behaviour matches name)

| Symbol | File | Evidence |
|---|---|---|
| `gate_tool_ingress` | `AAA/governance/federation_act.py:577` | strips caller `action_class`, resolves authority from registry (structure is correct; F-02 is a *token-trust* defect, not a name defect) |
| `verify_or_reject` | `federation_act.py:483` | returns `None` on pass, error dict on fail |
| `ForgeSealService.seal()` | `A-FORGE/src/domain/governance/ForgeSealService.ts:74` | writes `skill.scars_referencing.push(sealId)`, `trust_tier = "TRUSTED"`, builds receipt |
| `resolve_tool_authority` | `AAA/governance/tool_authority_registry.py:265` | resolves from `tools.yaml` + organ defaults |
| `isIndependentVerifier` | `A-FORGE/src/infrastructure/tools/forge_verify.ts:43` | compares identity hashes |
| `_emit_gate_decision` | `federation_act.py:516` | emits a decision event; never raises into the gate path |

---

## 6. Remediation priority

| # | Finding | Action |
|---|---|---|
| 1 | F-01/F-02 | Delete the fail-open branch (`federation_act.py:389–417`) or gate it behind signature verification. This is an authority bypass into three organs. |
| 2 | F-04 | Implement `escalate()` or delete the class and its callers. |
| 3 | F-03 | Implement the observation-tool loop or remove `forge_verify` from the WAJIB 2 story. |
| 3b | F-08 | Call `runInSandbox` in `forge_sandbox_run`/`forge_execute`, or delete the "isolated sandbox" claim from both the description and the comment. |
| 4 | F-05, F-06 | Delete the dead buffer and the `_wrap_call` alias surface; add a registry assertion that no wire-exposed tool resolves to `_wrap_call`. |
| 5 | M-01 | Rename `arif_forge` → `arif_forge_query` (or re-open the boundary). Remove the `forge_execute.py` "Stub" docstring contradiction. |
| 6 | M-02, F-07 | Stop emitting `executed_at`/`status:"healthy"` for work not done. |
| 7 | M-03, M-06, P-03 | Either wire the guards (state machine, stage enforcement, positional witness) or mark them explicitly `DECORATIVE` in the surface so no agent treats them as gates. |
