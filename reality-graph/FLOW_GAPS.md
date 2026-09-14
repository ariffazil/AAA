# FLOW_GAPS — Phase D Flow Integrity Register

**Program:** Entropy Reduction (Phases C+D) · arifOS Federation
**Canonical flow audited:** `Intent → Proposal → Verification → Judgment → Execution → Receipt → Witness`
**Date:** 2026-09-14 · KVM8 forge
**Companion:** `FLOW_MAP.md` (the map) · `SEMANTIC_ALIGNMENT_AUDIT.md` (Phase C)

**Total gaps: 18** — classified as DEAD_END · DEAD_GATE · BYPASS · SHADOW_EXECUTION · RECEIPTLESS · PHANTOM_RECEIPT · LOOP_BREAK.

---

## A. Execution stage

### G-01 · DEAD_END — kernel Execution stage is closed
`/root/arifOS/arifosmcp/tools/forge.py:382`
`arif_forge` (one of 8 exposed kernel tools) allows **only** `mode="query"`. Every `MUTATE`/`ATOMIC` mode returns `HOLD` (P0 boundary closed, `arif_falsification_audit_2026-07-25`).
**Consequence:** the canonical flow cannot reach *Execution* inside the kernel. Execution exists only if the caller crosses to A-FORGE :7072. The documented chain `888 JUDGE → signed permit → 777 FORGE verify+consume → 999 receipt` is not implemented at the kernel.

### G-02 · DEAD_GATE — kernel stage-progression gate is off
`/root/arifOS/arifosmcp/runtime/executor.py:23` — `ARIFOS_STATE_MACHINE_ENFORCE` defaults to `"false"`.
`/root/arifOS/arifosmcp/runtime/state_machine_guard.py` (STAGE_ORDER 000→999, IRON LAW 4 `SEAL_BEFORE_ACT`) is **imported nowhere** in the live runtime.
**Consequence:** stage order, "no act without judge SEAL", and "no seal without compose" are doctrine, not enforcement.

### G-03 · DEAD_GATE — A-FORGE metabolic stages are decorative
`/root/A-FORGE/src/infrastructure/metrics/prometheus.ts:79` — `runStage()` is a Prometheus timer only.
**Consequence:** the 9-stage metabolic loop `000→999` in A-FORGE is a label on a span. Relevant call sites: `core.ts:1264,1516,1560,1628`.

### G-04 · SHADOW_EXECUTION — no execution path is sandboxed
`/root/A-FORGE/src/interfaces/mcp/forge8Verbs.ts`
- `:382` `forge_sandbox_run` — comment says *"Execute staged artifact in isolated sandbox"*; body is raw `execAsync("bash artifact.code", { cwd: staging_path })`.
- `:780` `forge_execute` (legacy path) — same raw `execAsync("bash artifact.code")` after seal verification.
Both run on the host with the A-FORGE service user's privileges. The containment engine (`ContainmentEngine.ts` — `bwrap`/`firejail`/`docker`; `ExecutionSandbox.ts` — `runInSandbox`, `createSandbox`) is **imported at `:43–52` and never called**.
The `trust_tier` (`local_only` … `full_access`) is metadata passed to the same `bash` call regardless of tier.
**Consequence:** 120 A-FORGE tools reach a code-execution surface where isolation is declared, imported, and absent.

### G-05 · PHANTOM_RECEIPT — receipt without execution
`/root/A-FORGE/src/interfaces/mcp/forge8Verbs.ts:670–706`
The `stage_id + human_seal_token` branch returns `success: true`, `execution_id`, `executed_at`, `receipt_uri` and `authorization_path: "governance_stage"` **with no process spawned**. A downstream witness reading the receipt cannot distinguish it from real execution. (Phase C: M-02.)

---

## B. Approval / human branch

### G-06 · DEAD_END — human escalation never fires
`/root/A-FORGE/src/application/approval/index.ts:145–150` — `escalate()` is `{}`, inherited by `WebhookHumanEscalationClient` and `NoOpHumanEscalationClient`.
**Consequence:** `AWAIT_APPROVAL` in the execution state machine has no reachable human terminal. The `A2H` branch of the Universal Triangle terminates in a no-op.

### G-07 · BYPASS — orphaned parallel approval doctrine
`ApprovalBoundary.ts:1` / `HumanEscalationClient.ts:1` declare *"⚠️ REPLACED by constitutional governance"* while `PersonalOS.ts:77–88` still constructs `new ApprovalBoundary()`, and `HumanEscalationClient` is still imported at `AgentEngine.ts:82` and `PipelineCoordinator.ts:82`.
**Consequence:** two approval authorities coexist; whichever runs first wins. (Phase C: M-05.)

---

## C. Verification stage

### G-08 · DEAD_END — verification lane always INCONCLUSIVE
`/root/A-FORGE/src/infrastructure/tools/forge_verify.ts:123,139` — every check is `passed: false`; result is always `INCONCLUSIVE`.
**Consequence:** the `Verification → Judgment` edge carries no signal. Judgment runs on unverified claims.

---

## D. Authorization / token path

### G-09 · BYPASS — forged token accepted as SOVEREIGN (proven)
`/root/AAA/governance/federation_act.py:389–417` — fail-OPEN branch decodes the payload and trusts `auth` without HMAC verification.
Empirical, 2026-09-14: 4 of 6 attempts **ALLOWED** a token with a garbage signature (`act_v1.<b64({"auth":"SOVEREIGN"})>.deadbeefdeadbeef`); the 2 rejections were `ARIFOS_UNREACHABLE` (kernel timeout), not structural.
**Live ingress consumers:** `GEOX/src/geox_mcp/geox_middleware.py:593`, `WELL/server.py:13382`, `WEALTH/wealth_mcp/server.py:573`.
**Consequence:** a shadow authorization path into three organs. (Phase C: F-01, F-02.)

### G-10 · LOOP_BREAK — three token parsers, three answers
| Parser | Pattern | Accepts |
|---|---|---|
| `federation_act.py:37` `SCT_RE` | `^sct_v1\.[…]$` | `sct_v1` only |
| `federation_act.py:296` (verify prefix check) | `act_v1.\|arifos.v1.` | NOT `sct_v1` |
| `A-FORGE/src/infrastructure/governance/actIngress.ts:25` | `^(sct_v1\|act_v1)\.` | both |

`SCT_RE` is defined but never used on the verification path, so the module simultaneously declares and ignores a shape. The federation has no single token grammar.

### G-11 · BYPASS — `forge_seal_lane_a` explicitly bypasses the canonical HOLD
`/root/A-FORGE/src/interfaces/mcp/sealLaneA.ts:4` — *"bypasses chat-MCP `arif_seal` HOLD (vault_sovereign lease)"*, spawning `/root/scripts/forge_seal_lane_a.py`.
**Consequence:** a second, in-process seal path that does not pass the `arif_seal` HOLD gate. Two ways to reach VAULT999 with different gate coverage.

---

## E. Receipt / witness stage

### G-12 · DEAD_END — `audit_seal` buffer has no drain
`/root/arifOS/arifosmcp/runtime/context_audit.py:219,379` — `_SEAL_BUFFER` is appended to and never flushed.
**Consequence:** every audit "SEAL" is lost at process exit. (Phase C: F-05.)

### G-13 · RECEIPTLESS — arifFLOW fallback has no sweeper
`/root/A-FORGE/src/infrastructure/receipts/flowEmit.ts:8–9` — *"A sweeper (future P1-7) can replay the fallback when the plane returns."* No P1-7 sweeper exists in the tree.
**Consequence:** when arifFLOW (:7073) is unreachable, receipts land in `~/.agent-workbench/aforge-flow-fallback.jsonl` and are never replayed to the canonical plane. The doctrine "no silent drop" holds locally but not federated.

### G-14 · DEAD_END — self-attestation is indistinguishable from external witness
`/root/arifOS/arifosmcp/runtime/witness_class.py:5` — positional witness taxonomy is *"STAGED — NOT DEPLOYED"*.
The live kernel reports `tri_witness: [true, true, true]` on substantive witnesses only. A receipt that is `substantive=ai, position=SELF` is displayed exactly like one from outside the loop.
**Consequence:** the `Witness` terminal of the canonical flow cannot distinguish a closed loop from an open one. (Phase C: P-03.)

### G-15 · LOOP_BREAK — verdict semantics flattened at interception
`/root/A-FORGE/src/domain/governance/verdict-interceptor.ts:53–63` — `HOLD` and `VOID` both map to `"ERROR"`.
**Consequence:** downstream consumers cannot tell a constitutional refusal from a crash. The `Judgment → Receipt` edge loses the verdict. (Phase C: M-04.)

---

## F. Surface / organ integrity

### G-16 · LOOP_BREAK — GEOX surface drift
Live `geox-mcp` log, 2026-09-14:
```
WARNING:geox.governance.middleware:SURFACE_DRIFT
raw_live=100 raw_drift=74 canonical=26 removed=['geox_abstraction_guard', … +64]
```
74 of 100 live tools are absent from the canonical surface.
**Consequence:** the MCP Surface Guard's tool fingerprint cannot validate calls to tools it does not know; surface drift is reported but not resolved.

### G-17 · DEAD_END — WELL organ degraded
Live `/health` :18083 → `{"status":"degraded", "authority":"REFLECT_ONLY"}`; `/metrics` → 404.
**Consequence:** the WELL (human-substrate) lane is present but not carrying state. `well_heartbeat` runs; the organ does not.

### G-18 · DEAD_GATE — FED is advisory by construction
`:7074` `/health` → `"role":"ADVISORY_ONLY", "ceiling":"never judges, never hard-blocks"`.
**Consequence:** the FED node cannot terminate a bad flow. Correct by doctrine — recorded here so the flow map does not imply a hard gate at :7074.

---

## Remediation order

1. **G-09** — close the fail-open branch. Highest consequence: live authority bypass into three organs.
2. **G-05, G-13** — stop emitting receipts for work not done; build or remove the sweeper.
3. **G-06, G-08** — the human terminal and the verification lane are both non-functional; either wire them or remove them from the flow story.
4. **G-02, G-03, G-18** — label the decorative gates as decorative (or turn them on).
5. **G-10, G-11** — one token grammar; one seal path.
6. **G-16, G-17** — organ-level: reconcile GEOX surface, restore WELL state.
