# A2A Verdict Grammar Extension v1.0

> **Extension ID:** `arifos.verdict-grammar.v1`
> **Ratified:** 2026-07-02
> **Author:** FORGE (000Ω) — metabolized from Copilot A2A analysis
> **DITEMPA BUKAN DIBERI**

## The Mapping

This is the canonical mapping between arifOS constitutional verdicts and A2A protocol `TaskState` values. Any A2A-native peer that reads this extension can understand arifOS sovereign grammar without knowing what arifOS is.

| arifOS Verdict | A2A `TaskState` | Semantics | When |
|---------------|-----------------|-----------|------|
| **UNKNOWN** | `submitted` | Task received, evidence pending | Initial state |
| **(implicit)** | `working` | Judge deliberating, verdict pending | During `arif_think` + `arif_observe` |
| **SABAR** | `input-required` | Task paused, needs more input/time | Safe wait, no violation |
| **HOLD** | `auth-required` | Task blocked pending F11/F13 clearance | Requires sovereign or 888_HOLD |
| **SEAL** | `completed` | Verdict rendered, artifacts sealed | Approved action |
| **PARTIAL** | `completed` with `metadata.partial: true` | Completed with declared gaps | Partial evidence |
| **VOID** | `rejected` | Task refused on principle (F-floor violation) | Constitutional rejection |
| **(exec error)** | `failed` | Non-verdict failure — infra, timeout | System error |
| **(sovereign cancel)** | `canceled` | ARIF explicitly stopped | F13 veto |

## Extension Declaration

Declare in any organ's AgentCard:

```json
{
  "capabilities": {
    "extensions": ["arifos.verdict-grammar.v1"]
  }
}
```

## Task Artifacts

When a task reaches `completed` (SEAL), the following artifacts are emitted:

| Artifact | URI | Description |
|----------|-----|-------------|
| Verdict receipt | `arifos://verdict/{task_id}` | Full verdict with evidence chain |
| Seal receipt | `vault999://seal/{seal_id}` | Immutable VAULT999 record |
| Evidence package | `arifos://evidence/{task_id}` | All evidence used in judgment |

## Human-in-the-Loop (F13 Sovereign Veto)

When any organ emits `auth-required` (HOLD), the AAA gateway:

1. Pauses the task
2. Sends push notification to ARIF's webhook endpoint
3. Waits for sovereign decision (SEAL or VOID)
4. Resumes task with new state

This implements F13 SOVEREIGN at A2A protocol level — any A2A-native peer can participate in the veto flow without knowing arifOS.

## Cross-Organ Example

```
Task: "Evaluate Well Bekantan-1 prospect"
  ├── submitted    → AAA Gateway receives task
  ├── working      → AAA routes to GEOX (basin analysis)
  ├── working      → GEOX returns evidence → AAA routes to arifOS
  ├── working      → arifOS judge deliberates
  ├── auth-required → arifOS emits HOLD (F13: budget > threshold)
  │   └── push notification → ARIF
  │   └── ARIF approves → SEAL
  ├── completed    → arifOS emits SEAL verdict
  └── artifacts    → VAULT999 seal + evidence package
```

## Vocabulary Boundary

| Protocol | Scope | What It Does |
|----------|-------|-------------|
| **MCP** | Within a host | Tool calls (agent → capability) |
| **A2A** | Between hosts | Task lifecycle (agent → agent) |
| **Sampling** | Within a host | Server → LLM callback |
| **Verdict Grammar** | A2A extension | Sovereign semantics on top of TaskState |

**Rule:** MCP for tools, A2A for tasks, Sampling for callbacks, Verdict Grammar for sovereignty.