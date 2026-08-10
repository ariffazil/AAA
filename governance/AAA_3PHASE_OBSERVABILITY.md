# AAA 3-Phase Observability Contract

> **Forged:** 2026-08-10 · Agent-ratified Lane B (SESSION_RECEIPT)
> **Source:** Adapted from external General Directive Specification
> **Binding:** arifOS / arifFLOW / AAA Multi-Agent Protocol
> **Status:** CANON — adoption under "minimal gap" mode (F4 ΔS ≤ 0)
> **DITEMPA BUKAN DIBERI** — Forged, not given.

---

## 1. The Contract

Every autonomous agent action — every tool execution, every model call, every system mutation — MUST execute the **3-Phase Observability Contract**:

### Phase 1 · PRE_FLIGHT
Verify before acting. No action without:
- **File dependencies** present and ≥ minimum size (no truncated models, no missing configs)
- **Daemon health** — all required services responding 200 on `/health`
- **Resource availability** — VRAM (if CUDA), disk, RAM above thresholds
- **Session identity** — `arif_init` minted, lease held, sovereign confirmed

### Phase 2 · RUNTIME
Telemetry during execution:
- **Latency** measurement (wall-clock ns)
- **Peak resource** (VRAM, memory, CPU)
- **Step type** labeled (`Execute` | `Route` | `Merge`)
- **Epistemic label** on the action (`OBS` | `DER` | `INT` | `SPEC`)
- **Floor verdict** (`Pass` | `Caution` | `Hold` | `Void`)

### Phase 3 · POST_FLIGHT
Evaluate before concluding:
- **Verify** — independent witness of the output (W³ tri-witness when stakes warrant)
- **Visual/perception scoring** — VLM evaluator for image/structured outputs
- **Cool** — drift detection if behavior diverged from prediction
- **Receipt** — sealed to VAULT999 with hash-chained lineage

---

## 2. Integration Rule — F4 CLARITY (ΔS ≤ 0)

**DO NOT create parallel ledgers.** The federation already has:

| Substrate | Path / Service | Role |
|---|---|---|
| `arifflow_receipts.jsonl` | `/root/.local/share/arifos/` | Flow Quotient (FQ) ledger |
| `flow_ingest` MCP | `:7073/mcp` | Receipt emission — `arifFlow` |
| `flow_health` MCP | `:7073/health` | FQ pulse + verdict |
| `forge_*` primitives | `:7071/mcp` (A-FORGE) | Pre-flight, runtime, post-flight gates |
| `arif_seal` | `:8088/mcp` (arifOS) | Constitutional Lane A seal |

**Adoption rule:** the 3-phase contract is the **mental model**. arifFlow + forge_* primitives are the **execution**. No new file at `/workspace/`. No new ledger schema. Align to canonical paths.

---

## 3. Stage Mapping to Existing Substrate

| Spec Stage | Federation Surface | Tool |
|---|---|---|
| PRE_FLIGHT file integrity | `forge_scan` / `forge_runtime_verify` | A-FORGE |
| PRE_FLIGHT daemon health | `forge_health_check` / `:port/health` | A-FORGE + direct |
| PRE_FLIGHT resource | `well_machine_diagnose` + `netdata` | WELL |
| PRE_FLIGHT session | `arif_init` → `forge_lease` | arifOS |
| RUNTIME telemetry | `flow_ingest(step_type=Execute)` | arifFlow |
| RUNTIME shell | `forge_shell(expected_output=...)` | A-FORGE |
| POST_FLIGHT verify | `flow_ingest(step_type=Verify)` | arifFlow |
| POST_FLIGHT witness | `forge_witness` (W³) | A-FORGE |
| POST_FLIGHT evaluation | `forge_evaluate` (G = APEX) | A-FORGE |
| POST_FLIGHT drift | `forge_cool_drift` | A-FORGE |
| POST_FLIGHT VLM perception | `mcp__minimax__understand_image` | minimax MCP |
| POST_FLIGHT seal | `arif_seal(mode=seal)` Lane A | arifOS |
| POST_FLIGHT receipt | `forge_vault(mode=receipt)` Lane B | A-FORGE |

---

## 4. Genuine Gap — Python Wrapper for Non-MCP Code

MCP-tool calls are already receipted via `flow_ingest`. **The gap is Python code that bypasses MCP** — raw `subprocess`, `urllib`, torch inference, image generation, anything that touches the federation without going through the MCP surface.

For that code path, AAA provides `arifosmcp.observability`:

```python
from arifosmcp.observability import AAAFlowEngine

engine = AAAFlowEngine()
engine.execute_sovereign_task(
    model_path="/opt/models/foo.safetensors",
    api_url="http://127.0.0.1:8188",   # ComfyUI
    prompt_payload={"prompt": "..."},
)
```

The engine:
1. **PRE_FLIGHT** — runs `AAAExecutionGuard.verify_file_integrity`, `check_service_health`, `check_vram_capacity`. On failure, aborts + emits Barrier receipt via `flow_ingest`.
2. **RUNTIME** — executes the payload, measures latency + peak VRAM, emits Execute receipt.
3. **POST_FLIGHT** — if image output, calls VLM perception scorer (minimax `understand_image`). Emits Verify receipt with fidelity score ≥ 0.7.

**All receipts route to arifFlow :7073 → arifflow_receipts.jsonl. No parallel ledger.**

---

## 5. Floor Compliance

| Floor | 3-Phase Mapping |
|---|---|
| **F1 AMANAH** (reversible-first) | PRE_FLIGHT abort path; snapshot before mutation |
| **F2 TRUTH** (epistemic labels) | RUNTIME `epistemic_label` field; W³ at POST_FLIGHT |
| **F4 CLARITY** (ΔS ≤ 0) | No parallel ledgers; align to canonical paths |
| **F11 AUDITABILITY** | Every phase emits a hash-chained receipt |
| **F12 RESILIENCE** | PRE_FLIGHT guards prevent OOM + zombie processes |
| **F13 SOVEREIGN** | Agent self-ratifies via Lane B (no F13 ACK needed for SESSION_RECEIPT) |

---

## 6. Authority

- **Binding for:** all arifOS / arifFLOW / AAA agents
- **Ratification:** Lane B SESSION_RECEIPT (this document)
- **Override:** Lane A CONSTITUTIONAL_SEAL via arif_seal (F13 ACK required)
- **Scope creep guard:** any extension must pass ΔS ≤ 0 + F11 reconciliation with existing ledgers

---

## 7. Anti-Patterns

- ❌ Writing new telemetry ledger at `/workspace/telemetry.jsonl` (parallel source of truth)
- ❌ Bypassing `flow_ingest` with a new JSONL format (F4 violation)
- ❌ Importing `torch` in arifOS kernel code path (kernel is torch-free; GEOX keeps torch)
- ❌ Auto-promoting 3-phase contract to Lane A without F13 ACK
- ❌ Wrapping MCP tool calls with custom telemetry (already receipted — double-wrap = audit duplicate)

---

*Forged 2026-08-10 by 333-AGI Δ MIND under "Adopt + minimal gap" F13 ratification (Arif, 2026-08-10T07:15Z).*
*Sealed to VAULT999 via Lane B SESSION_RECEIPT.*
*DITEMPA BUKAN DIBERI — Adopted, not imported.*