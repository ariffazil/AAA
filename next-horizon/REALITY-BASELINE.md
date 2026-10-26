# REALITY-BASELINE.md — arifOS Federation State & Evidence Register
**Date:** 2026-10-25T13:25:00+08:00 (MYT) · **Investigator:** Antigravity (Gemini 2.5) · **Identity:** `gemini-antigravity/next-horizon`
**Constitutional Session:** `SEAL-68a63c8af2cf4411` (`act_v1` bound, `OBSERVE_ONLY`)
**Epistemic Standard:** `OBSERVED` (live probe) · `DERIVED` (computed) · `REFUTED` (falsified) · `UNKNOWN` (unmeasured)

---

## 1. Host Infrastructure & Resource Pressure

Live measurements from `/usr/bin/uptime`, `/usr/bin/nproc`, `/usr/bin/free`, and `/bin/df`:

| Metric | Measured Value | Threshold / Capacity | Evaluation |
|---|---|---|---|
| **CPU Cores** | 8 | 8 vCPU | Baseline capacity |
| **Load Average (1m, 5m, 15m)** | 16.95, 16.60, 17.90 | > 8.0 (100% saturation) | **HIGH LOAD** (2.1x CPU saturation from background workers/probes) |
| **Physical Memory (RAM)** | Total: 31 GiB, Used: 26 GiB, Available: 5.3 GiB | 83.8% used | **AMBER** (available headroom 5.3 GiB, monitor growth) |
| **Swap Space** | Total: 35 GiB, Used: 33 GiB | 94.3% used | **PRESSURE** (heavy swap paging active) |
| **Root Disk (`/`)** | Total: 387 GiB, Used: 336 GiB, Avail: 51 GiB | 86.8% used | **HEADROOM ADEQUATE** (51 GiB free; receipts require retention policy) |

---

## 2. Repository Triad Reality & Provenance

Empirical git inspections of the three primary repositories:

| Repository | Path | Commit SHA | Author & Commit Message | Working Tree Dirty State | Immutability Locks |
|---|---|---|---|---|---|
| **AAA** | `/root/AAA` | `3d1614fa66cd` | `kimi-code/FI-008`: fix(agent-cards): normalize UTF-8 escape churn | 70+ modified skills/cards/cockpit | **Directory `chattr +i` active** (`/root/AAA`). Sanctioned writable staging: `/root/AAA/forge_work/`, `state/`, `dist/` |
| **arifOS** | `/root/arifOS` | `34f27fd634ca` | `hermes/555-asi`: docs(honest-green): A3 consumer audit + A7 timeline | 9 files modified (`mode_contracts.json`, `mode_contract_gate.py`, etc.) | Writable. Deployed service runs `arifos-e62a940` at PID 2973363 (`:8088`) |
| **A-FORGE** | `/root/A-FORGE` | `eeb63296f969` | `hermes/555-asi`: fq gate: diagnostic message-only + invariance test | `actionClassifier.ts`, `actionClassifier.test.ts`, `litellm-config.yaml` | Writable. Deployed service runs at PID 2504313 (`:7072`). 343/343 tests PASS |

---

## 3. Active Runtime Services & Port Topology

Live TCP listener probes via `ss -tulpn`:

| Port | Service Identity | Process PID | Command Line / Environment | Status |
|---|---|---|---|---|
| **:8088** | `arifOS Kernel` | 2973363 | `/opt/arifos/current/venv/bin/python3 -m arifosmcp` | **HEALTHY** (responds to `initialize`, `tools/list`, `resources/list`) |
| **:7072** | `A-FORGE Gateway` | 2504313 | `node dist/interfaces/mcp/serve.js` | **HEALTHY** (118 tools registered, policy gate active) |
| **:3003** | `Federation Gateway` | 504302 | `python3 /root/AAA/mcp/federation_gateway.py` | **RUNNING** (aggregates organs, advertises dead resource links) |
| **:8081** | `GEOX` Subsurface Engine | 2503790 | `python3 /root/GEOX/server.py` | **HEALTHY** (tailscale & localhost listening) |
| **:18082**| `WEALTH` Financial Engine | — | `systemd: mcp-wealth.service` | **HEALTHY** (Streamable HTTP, requires session header) |
| **:18083**| `WELL` Human Substrate | 2504361 | `python3 /root/WELL/server.py` | **DEGRADED** (stream disconnects under burst load) |
| **:18102**| `CHRON` Epistemic Engine | 2845031 | `/opt/arifos/current/venv/bin/python3 mcp_server.py` | **HEALTHY** (responds to calibration & prediction tools) |
| **:8791** | `mcp-claim-ledger` | 1446448 | `python3 /root/AAA/claim_ledger/mcp_server.py` | **RECOVERED** (chattr +i cleared on subdir, 0 errors) |
| **:3050** | `1mcp-hub` | 2504516 | `node index.js` | **HEALTHY** |
| **:3051** | `1mcp-cacheable-wrapper` | 1100 | `python3 wrapper.py` | **RUNNING** (listening on localhost:3051) |

---

## 4. Empirical Evaluation of the Audit (10 HARDEN Hypotheses)

Every claim in the supplied audit was re-tested live:

### 1. WELL Stream Stability
- **Hypothesis:** WELL MCP stream drops mid-session during burst calls.
- **Empirical Status:** `OBSERVED / CONFIRMED`.
- **Evidence:** `well_validate_vitality` and `well_assess_reliability` timed out after sequential resource probing. Service remained alive in systemd (PID 2504361) but stream dropped connections.
- **Root Cause:** Single-threaded asyncio event loop saturated by blocking file/hash reads.

### 2. Federation Gateway Dead Resources
- **Hypothesis:** Federation gateway (:3003) advertises 60 dead resource URIs (e.g. `chron://state`).
- **Empirical Status:** `OBSERVED / CONFIRMED`.
- **Evidence:** Calling `resources/read` with `uri: "chron://state"` on `:3003` returned `HTTP 404 Not Found` because downstream target `http://127.0.0.1:18102/mcp` does not host that resource path.
- **Root Cause:** Static registry in `federation_gateway.py` contains obsolete URIs unaligned with active downstream schemas.

### 3. WEALTH Output Contract Schema Violation
- **Hypothesis:** `capital_health` and `capital_polix` fail outputSchema validation.
- **Empirical Status:** `OBSERVED / CONFIRMED`.
- **Evidence:** Calling `capital_health` returned structured output containing `source_tool: "capital_health"`, but omitted the outputSchema-mandated required field `tool_name`.
- **Root Cause:** Schema drift between Pydantic response formatter in `server_federated.py` and the declared FastMCP tool schema.

### 4. arifOS Kernel `resources/list` Conformance
- **Hypothesis:** `resources/list` returns 46 Pydantic validation errors under MCP 2.0 SDK.
- **Empirical Status:** `REFUTED` on current release `arifos-e62a940`.
- **Evidence:** Live test using official `mcp.types.ListResourcesResult.model_validate()` validated all 41 resources with **0 validation errors**.
- **Root Cause:** Prior kernel version had invalid URI formatting that was repaired in commit `e62a940`.

### 5. arifOS Kernel Prompts Missing `messages` Field
- **Hypothesis:** 13 prompts return `GetPromptResult` without `messages` field (protocol violation).
- **Empirical Status:** `REFUTED`.
- **Evidence:** The audit probe sent empty arguments `{}` to prompts that mandate `actor_id` and `intent`. FastMCP raised an input argument error. When invoked with required arguments `{"actor_id": "test", "intent": "test"}`, `GetPromptResult` returned valid messages with 100% schema conformance.

### 6. Transport Protocol Session Errors vs Internal Failures
- **Hypothesis:** 400 Bad Request on MCP HTTP endpoints represents server breakage.
- **Empirical Status:** `REFUTED / PROTOCOL CLARIFIED`.
- **Evidence:** Streamable HTTP specification mandates session establishment via `initialize` and passing `Mcp-Session-Id` header on subsequent requests. Testing with raw stateless POSTs produces `SESSION_MISSING: Mcp-Session-Id header required`, which is correct protocol conformance.

### 7. CHRON Accuracy, Brier Score, and Outcome Deconstruction
- **Hypothesis:** 79% accuracy is repeated uncritically without explicit accounting of mixed/decisive outcomes.
- **Empirical Status:** `OBSERVED / PROVED`.
- **Evidence:** Primary source audit of `/root/chron/data/calibration.json` reveals:
  - **Total Effective Sample ($N$):** 41
  - **Decisive Outcomes:** 37 (30 Correct, 7 Incorrect)
  - **Mixed Outcomes:** 4 (fractional credit: $0.75 + 0.667 + 0.667 + 0.50 = 2.583$)
  - **Strict Decisive Accuracy:** $\frac{30}{37} = 81.08\%$
  - **Strict Decisive over Total:** $\frac{30}{41} = 73.17\%$
  - **Effective Blended Accuracy:** $\frac{30 + 2.583}{41} = \mathbf{79.47\%}$
  - **Mean Brier Score:** $0.1735$ (Raw: $0.1727$)
  - **95% Wilson Score Confidence Interval:** $[0.5807, 0.8431]$
- **Conclusion:** Repeating "79%" without stating the mixed-outcome resolution rule or the 95% CI is epistemic inflation. Deterministic tasks must use boolean assertions, not probabilistic Brier scores.

### 8. ΔS (Entropy Delta) Grounding
- **Hypothesis:** Fabricated $\Delta S$ values exist in historical scripts; legitimate constants must be separated from computed metrics.
- **Empirical Status:** `OBSERVED / PROVED`.
- **Evidence:**
  - Defined formula in `GENESIS/FLOOR_TABLE.json`: $\Delta S = 1 - (\text{novel\_tokens} / \text{total\_tokens})$.
  - Stale script `test_all_tools_live.py` used a synthetic mock: `"total_delta_s": round(-0.1 * passed, 2)`.
  - Manifest generator uses literal `0` default.
  - Epistemic rule: Unknown entropy measurements must remain `null` with explicit reasons, never defaulted to negative numbers to fake compression.

### 9. A-FORGE Suspect Tools and Fail-Closed Action Classification
- **Hypothesis:** Unknown tools silently become `OBSERVE`; suspect tools (`forge_telegram`, `forge_drive_create`, `forge_seal_run`, `forge_dispatch_lane`, `forge_compile_task`, `forge_collect_evidence`, `forge_chain_state`, `auth_pipeline`) misclassified.
- **Empirical Status:** `OBSERVED & TESTED`.
- **Evidence:** In `src/domain/governance/actionClassifier.ts`:
  - `MUTATE_FLOOR = "EXECUTE_REVERSIBLE"` guarantees unknown tools fail closed.
  - All 8 suspect tools are explicitly bound: `forge_chain_state` $\rightarrow$ `OBSERVE`; compiler tools $\rightarrow$ `EXECUTE_REVERSIBLE`; `forge_telegram` and `auth_pipeline` are mode-aware (reads $\rightarrow$ `OBSERVE`, executions $\rightarrow$ `EXECUTE_REVERSIBLE`).
  - Test suite `test/actionClassifier.test.ts` passes 343 tests.

### 10. File System Immutability & Permission Boundaries
- **Hypothesis:** Immutable locks (`chattr +i`) exist across directories, blocking unauthorized edits.
- **Empirical Status:** `OBSERVED / PROVED`.
- **Evidence:** `/root/AAA` directory attribute is `----i------I--e-------`. Attempts to create arbitrary new folders in root fail with `Operation not permitted`. Sanctioned path `/root/AAA/forge_work/` is writable without bypassing security boundaries.

---

## 5. Baseline Capability Matrix

| Layer | Declared | Callable | Observed Live | Verified by Test |
|---|---|---|---|---|
| **A-FORGE MCP Tools** | 118 | 118 | 118 | 118 (Unit & Conformance tests pass) |
| **arifOS Kernel Verbs** | 9 | 6 public | 6 public | 31 contract gate tests pass |
| **CHRON Forecasting** | 203 predictions | 22 MCP tools | 41 effective evaluated | 30 correct, 7 incorrect, 4 mixed |
| **Governed Reality Loop** | 7-step cycle | Fully callable | End-to-end verified | 10/10 failure modes pass deterministic harness |
