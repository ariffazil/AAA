# ARIFOS_CONTEXT_MCP_V1 — Context Engine MCP Contract

> **Status:** SEALED-BY-DOCTRINE (F13, Arif #74569, 2026-06-12 02:59:59 UTC)
> **Runner:** SEAL (pass/fail test PASS, 217/217 green)
> **Forge scope:** F8 for in-process; F13 for MCP tool surface
> **Reversibility:** `rm forge_work/ARIFOS_CONTEXT_MCP_V1.md`
> **DITEMPA BUKAN DIBERI** — the contract is forged, not given.

---

## 0. Final architecture sentence

> In arifOS MCP, context management is a governed service: tools compute it, resources expose it, prompts standardize it, and the runner enforces it.

## 1. The 4-surface mental model

MCP is a governed port system with **four** surfaces, not one:

| Surface | Question it answers | Example |
|---|---|---|
| **Tool** | "What can the agent *do*?" | `prepare_context`, `record_context_usage` |
| **Resource** | "What can the agent *read*?" | `arifos://context/policy/v1`, `arifos://context/session/{sid}/status` |
| **Prompt** | "What *procedure* should the agent follow?" | `prompt://arifos/context/preflight_report` |
| **Runner** | "What must the agent do *before* the model call?" | `before_model_context_guard`, `after_model_usage_recorder`, `context_run_receipt_emitter` |

**Without the runner:** agents *may* call MCP tools.
**With the runner:** agents *must* call MCP tools. That is the difference.

## 2. The 11-step enforced flow

The runner forces the flow:

```
 1. Arif gives task
 2. Agent receives task
 3. Runner gets session_id
 4. Runner calls arif_context_status
 5. If HOLD, stop
 6. Runner calls prepare_context
 7. Runner gives curated packet to model
 8. Model answers
 9. Runner records usage
10. Runner emits ContextRunReceipt
11. Optional verifier checks packet/action
```

This is the bridge from **paper constitution** to **executable intelligence OS**.

## 3. Authority classes (F10 ONTOLOGY)

| Class | Authority | Compressible? | Source |
|---|---|---|---|
| USER_INSTRUCTION | 90 | NO | user_direct |
| TASK_STATE | 80 | NO | runtime |
| VERIFIED_MEMORY | 70 | yes | L4/L5 stores |
| RECENT_CONVERSATION | 50 | yes | L2 |
| DERIVED_SUMMARY | 40 | yes (working) | LLM |
| LOW_CONFIDENCE | 20 | yes | inference |
| UNTRUSTED | 0 | N/A (quarantined) | tool_output |

The allocator must protect the non-compressible classes. **F10.**

## 4. Pressure bands (5-band law)

| Band | Range | Action |
|---|---|---|
| LOW | 0.00–0.50 | proceed, log only |
| WATCH | 0.50–0.75 | log only, no action |
| WARN | 0.75–0.85 | surface advisory, **no** auto-compact |
| COMPACT | 0.85–0.95 | surface advisory, auto-compact **F13-gated** |
| HOLD | 0.95+ | refuse non-reversible |

`auto_compact_enabled = false` in v1. F8 + F13 required to enable.

## 5. Tools (5 in v1)

| Tool | Computes | Floor to expose as MCP |
|---|---|---|
| `arif_context_status(session_id)` | pressure report | F13 |
| `prepare_context(task, query, session_id, model_key)` | context packet | F13 |
| `record_context_usage(session_id, packet_id, model_usage)` | usage receipt | F13 |
| `verify_context_packet(packet_id)` | truth check | F13 |
| `compact_context_dry_run(session_id, target_pressure)` | manifest only, no execution | F13 |

`compact_context_execute` is **NOT** in v1. F13 territory.

## 6. Resources (6 in v1)

Resources are for **inspection, not mutation**.

| URI | Returns |
|---|---|
| `arifos://context/policy/v1` | the canonical policy doc |
| `arifos://context/session/{session_id}/status` | live session meter |
| `arifos://context/packet/{packet_id}` | frozen packet read |
| `arifos://context/audit/{run_id}` | runner audit trail |
| `arifos://context/pressure-bands` | 5-band table |
| `arifos://context/authority-classes` | authority table |

Pattern: **create thing → tool, inspect thing → resource.**

## 7. Prompts (4 in v1)

Prompts are templates, not the engine. They keep all agents speaking the same operational language.

| Prompt | Use |
|---|---|
| `arifos://context/preflight_report` | standard preflight wording |
| `arifos://context/compact_summary` | compaction candidate summary |
| `arifos://context/verification_report` | claim verification format |
| `arifos://context/failure_explanation` | HOLD / SABAR / VOID format |

Example preflight_report:
> Report current context status using: session_id, pressure_band, tokens_used, tokens_remaining, selected_segments, dropped_segments, protected_user_instructions, audit_mode, verdict. Do not claim completion unless verifier passes.

## 8. Runner guards (3)

| Guard | Steps | Purpose |
|---|---|---|
| `before_model_context_guard` | 1–7 | status → prepare → HOLD gate → curated packet |
| `after_model_usage_recorder` | 9 | post-call accounting |
| `context_run_receipt_emitter` | 10 | audit emission |

## 9. Pass/fail contract (F2 truth, F7 humility)

The runner must satisfy this or it is theatre:

```
GIVEN  critical instruction: "ARIF_RETAINS_FINAL_AUTHORITY_999"
       bloated candidate set: 30+ long segments
EXPECT phrase preserved verbatim
       classified USER_INSTRUCTION
       non-compressible (F10)
       visible in protected list
FAIL   if phrase missing, vaguely summarized, "probably", no list
```

**Locked as pytest:** `tests/runtime/test_pass_fail_runner_001.py` (15 tests, all green).

## 10. Inside MCP vs Outside MCP

**Inside MCP (F8):**
- status, prepare, verify, record usage
- read policy, read packet, read audit
- dry-run compaction

**Outside MCP / F13-gated:**
- real VAULT999 seal
- canonical memory deletion
- policy threshold changes
- auto-compact enable
- LLM summarizer activation
- deploy/restart

**MCP gives the agent access. It does not automatically give permission.**

## 11. The 18-item v1 contract

```
TOOLS (5)
  arif_context_status              [F13 to expose, F8 in-process]
  prepare_context                  [F13 to expose, F8 in-process]
  record_context_usage             [F13 to expose, F8 to build fn]
  verify_context_packet            [F13 to expose, F8 to build fn]
  compact_context_dry_run          [F13 to expose, F8 to build fn]

RESOURCES (6)
  arifos://context/policy/v1                  [F8]
  arifos://context/session/{session_id}/status [F8]
  arifos://context/packet/{packet_id}         [F8]
  arifos://context/audit/{run_id}             [F8]
  arifos://context/pressure-bands             [F8]
  arifos://context/authority-classes          [F8]

PROMPTS (4)
  arifos://context/preflight_report           [F8]
  arifos://context/compact_summary            [F8]
  arifos://context/verification_report        [F8]
  arifos://context/failure_explanation        [F8]

RUNNER (3)
  before_model_context_guard                  [F8 to wire, fn built]
  after_model_usage_recorder                  [F8 to wire, fn built]
  context_run_receipt_emitter                 [F8 to wire, fn built]
```

## 12. The agent fleet

| FI | Agent | Status |
|---|---|---|
| FI-001 | opencode | Phase 1.3 wire target |
| FI-002 | claude-code | Phase 4 spread |
| FI-003 | qwen-code | Phase 4 spread |
| FI-004 | gemini-cli | Phase 4 spread |
| FI-005 | codex-cli | Phase 4 spread |
| FI-006 | copilot-cli | Phase 4 spread |

**Different minds. Same operating law.**

## 13. Doability

**Yes. Not theoretically. Practically.**

The hard conceptual pieces already exist in `/root/arifOS/`:
- token pressure meter (token_pressure.py, Phase 1 forged)
- authority classes (this doc §3)
- audit modes (TRACE / DIGEST / FULL)
- memory store (L4 Supabase, L3 Qdrant, L1/L2 Redis)
- compression primitives (Eureka)
- policy docs (EUREKA_TOKEN_MANAGEMENT.md, context_policy_v1.md)
- context packet direction (prepare_context.py)

What remains is wiring — and the runner is the bridge.

## 14. The no-bullshit answer

```
Tool:    prepare_context()       builds the context
Resource: context_packet         shows what was built
Prompt:  preflight_report        tells the agent how to report it
Runner:  before_model_context_guard  forces the agent to use it
```

That is the whole thing. **No more theory. Forge it.**

---

## Phase ledger

| Phase | Status | Receipt |
|---|---|---|
| 1.1 Seal contract | ✅ | `forge_work/ARIFOS_CONTEXT_MCP_V1.md` (this file) |
| 1.2 Forge 12 of 18 in-process | ⏳ | next session |
| 1.3 Wire FI-001 opencode | ⏳ | after 1.2 |
| 2 7-day burn-in | ⏳ | after 1.3 |
| 3 Expose 5 tools + spread FI-002..FI-006 | ⏳ F13 | after 7 days |

**Runner state:**
- `arifosmcp/runtime/runner/runner_001.py` (24,844 B)
- `arifosmcp/runtime/runner/dryrun_runner_001.py` (4,162 B)
- `arifosmcp/runtime/runner/pass_fail_runner_001.py` (8,293 B)
- `tests/runtime/test_runner_001.py` (19 tests, green)
- `tests/runtime/test_pass_fail_runner_001.py` (15 tests, green)
- `arifosmcp/runtime/context_engine/prepare_context.py` (5 named tests, green after parallel substrate fix)

**Total test count:** 217 passed, 0 failed across 8 test files.

**Memory:** `/root/.openclaw/workspace/memory/2026-06-12-0318-v1-contract-sealed.md` (next)
