# EXECUTION-BACKLOG.md — Federation Hardening & Next Horizon Backlog
**Target:** Sovereign Federation (AAA / arifOS / A-FORGE) · **Updated:** 2026-10-25T13:25:00+08:00
**Governance State:** Bounded Execution Mandate · **Tracking System:** Single Task/Claim ID

---

## 1. Backlog Summary Matrix

| Tier | Total Tasks | DONE / PATCHED | IN PROGRESS | BLOCKED (Needs Grant) | PLANNED |
|---|---|---|---|---|---|
| **P0: Authority & Evidence Integrity** | 5 | 3 | 1 | 1 | 0 |
| **P1: Operational Correctness** | 6 | 4 | 1 | 1 | 0 |
| **P2: Bounded Autonomous Coordination**| 4 | 2 | 1 | 0 | 1 |
| **P3: Evidence-Gated Learning** | 3 | 0 | 0 | 0 | 3 |
| **Total** | **18** | **9** | **3** | **2** | **4** |

---

## 2. P0: Authority & Evidence Integrity (Immediate / Critical)

### [P0-01] ActionClassifier Fail-Closed Default & 8 Suspect Tools
- **Status:** **PATCHED & TESTED**
- **Owner:** `A-FORGE` (Hands)
- **Path:** `/root/A-FORGE/src/domain/governance/actionClassifier.ts`
- **Verification Evidence:**
  - `MUTATE_FLOOR = "EXECUTE_REVERSIBLE"` installed. Unknown tools fail closed.
  - Suspect tools resolved: `forge_chain_state` $\rightarrow$ `OBSERVE`; compiler tools (`forge_compile_task`, `forge_dispatch_lane`, `forge_collect_evidence`, `forge_seal_run`) $\rightarrow$ `EXECUTE_REVERSIBLE`; `forge_telegram`, `forge_drive_create`, `auth_pipeline` explicitly classified with mode awareness.
  - Test suite `test/actionClassifier.test.ts` passes 343/343 tests.
- **Remaining Action:** Commit and push to repo origin when sovereign grant is given.

### [P0-02] arif_report Mode Contract Escalation in Kernel
- **Status:** **PATCHED & TESTED**
- **Owner:** `arifOS` (Kernel)
- **Path:** `/root/arifOS/arifosmcp/abi/mode_contracts.json`, `mode_contract_gate.py`
- **Verification Evidence:**
  - Wire write mode `report` and external side-effect mode `flush` escalate from `OBSERVE` to `MUTATE` / `MATERIAL`.
  - Test `scripts/test_contract_gate.py` passes 31/31 checks.
- **Remaining Action:** Restart `arifos.service` to reload Python bytecode into active process PID 2973363.

### [P0-03] Verified Loop Failure Mode Test Harness
- **Status:** **DONE & VERIFIED**
- **Owner:** `AAA` Architecture Group
- **Path:** `/root/AAA/forge_work/next-horizon/tests/test_verified_loop.py`
- **Verification Evidence:**
  - 10/10 deterministic tests pass in pytest (`test_01` to `test_10`).
  - Proves: point-of-mutation auth check, replay rejection, lease locking, crash recovery, prompt injection containment, tamper detection, and rollback.

### [P0-04] Cryptographic Session Token Binding (Ed25519)
- **Status:** **IN PROGRESS**
- **Owner:** `arifOS` (Kernel)
- **Path:** `/root/arifOS/arifosmcp/runtime/session.py`
- **Current Reality:** Unsigned `arif_init` calls receive `OBSERVE_ONLY` session token with `actor_verified=false`.
- **Target State:** Require Ed25519 signature over challenge nonce for any tool requesting mutation authority.

### [P0-05] Thaw and Purge Frozen Stale Debris in A-FORGE
- **Status:** **BLOCKED**
- **Owner:** Sovereign (Arif)
- **Target Paths:** `tools_sot.yaml`, `package.json`, `.registry/fingerprints.json`, `*.bak`
- **Blocker:** File immutability lock (`chattr +i`) set on 2026-10-23 00:19.
- **Required Action:** Arif to issue explicit `chattr -i` authority to allow SOT regeneration (115 $\rightarrow$ 118 tools) and safe debris cleanup.

---

## 3. P1: Operational Correctness (Reliability & Clean Metrics)

### [P1-01] WEALTH OutputSchema `tool_name` Restoration
- **Status:** **PATCHED & READY FOR REVIEW**
- **Owner:** `WEALTH` Organ
- **Path:** `/root/WEALTH/server_federated.py`
- **Reproduction:** Calling `capital_health` omitted `tool_name` in root, violating outputSchema.
- **Fix:** Ensure structured output wrapper injects `"tool_name": "capital_health"` and `"domain": "wealth"`.
- **Verification:** FastMCP schema validator returns 0 errors on live call.

### [P1-02] Prune 60 Dead Resources in Federation Gateway
- **Status:** **PATCHED & READY FOR REVIEW**
- **Owner:** `AAA`
- **Path:** `/root/AAA/mcp/federation_gateway.py`
- **Reproduction:** Probing `chron://state` returns HTTP 404 from downstream `:18102`.
- **Fix:** Remove stale route mappings from gateway registry or point to valid `/episodes` endpoints.

### [P1-03] WELL MCP Stream Resilience Under Burst Load
- **Status:** **IN PROGRESS**
- **Owner:** `WELL` Organ
- **Path:** `/root/WELL/server.py`
- **Reproduction:** Rapid sequential calls drop SSE connection mid-session.
- **Fix:** Move blocking disk I/O to background executor thread; increase client keep-alive timeout to 60s.

### [P1-04] CHRON Epistemic Accuracy Publication
- **Status:** **DONE**
- **Owner:** `CHRON` Organ
- **Path:** `/root/chron/data/calibration.json`
- **Output:** Published 4-metric honest breakdown (81.1% decisive, 73.2% raw, 79.5% blended, Brier 0.1735, 95% CI [0.581, 0.843]).

### [P1-05] ΔS Grounding & Mock Formula Deprecation
- **Status:** **DONE**
- **Owner:** `arifOS`
- **Path:** Stale scripts archived; literal 0 / null preserved in manifest.

### [P1-06] System Resource Retention & Swap Pressure Mitigation
- **Status:** **BLOCKED** (Needs Policy Decision)
- **Owner:** Host Infrastructure
- **Observation:** Swap at 94.3% (33 GiB used); root disk at 86.8% (51 GiB free).
- **Proposed Action:** Safe rotation of old `/root/reports/` and `.cache/` directories over 30 days old; zero deletion of canonical VAULT999 receipts.

---

## 4. P2: Bounded Autonomous Coordination

### [P2-01] Peer Report Lane Adoption
- **Status:** **IN PROGRESS**
- **Owner:** `AAA` Coordinator
- **Action:** Configure agent harnesses (Gemini, Claude, Kimi, Opencode) to emit inter-agent progress reports to `/var/lib/arifos/reports/inbox.jsonl`.

### [P2-02] Exclusive Resource Lease Enforcement
- **Status:** **DONE (Harness Tested)**
- **Owner:** `A-FORGE`
- **Action:** Tested in `verified_loop_harness.py`; ready for integration into `A-FORGE/src/interfaces/mcp/serve.ts`.

### [P2-03] Automated Crash-Effect Reconciler
- **Status:** **DONE (Harness Tested)**
- **Owner:** `A-FORGE`
- **Action:** Tested in `test_04_crash_after_side_effect_recoverable`; reconciles target state before attempting retry.

### [P2-04] Retiring Alt-Harness Dead Launchers
- **Status:** **PLANNED**
- **Owner:** Infrastructure
- **Action:** Remove 5 unreachable launcher definitions (`postgres-pro`, `hound`, `repomapper`, `semgrep`, `minimax-multimodal`) from `.claude.json`.

---

## 5. P3: Evidence-Gated Learning (Research Track)

### [P3-01] Deterministic Task Benchmark Dataset Curation (500 Tasks)
- **Status:** **PLANNED**
- **Owner:** Research Group

### [P3-02] Bitemporal Memory Integration for RAG
- **Status:** **PLANNED**
- **Owner:** `CHRON` + `Qdrant`

### [P3-03] Local Small Model GRPO Training on Isolated Test Verifiers
- **Status:** **PLANNED (Gated by P3-01)**
- **Owner:** Research Group
