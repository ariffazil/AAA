---
name: apex_tool_approval_gate
description: Gate and route tool use across federation MCP servers according to authority, risk, and fallback policy
agent: 888-APEX
namespace: apex_*
cluster: GATE
---

# APEX-mcp-federation (O_Omega Orchestration Layer)

<cognitive-note model="claude">
This skill uses XML-tagged sections for native Claude parsing. Process each section independently.
Use extended context recall to maintain cross-organ state across the full procedure.
</cognitive-note>

<cognitive-note model="codex">
This skill uses numbered steps with explicit input/output schemas. Follow each step in order.
Validate schema conformance before proceeding to next step. Log chain-of-thought at each gate.
</cognitive-note>

<cognitive-note model="hermes">
Direct imperative format. No fluff. Route tasks. Execute sequence. Verify outputs. Report results.
If server fails: fallback. If governance fails: 888_HOLD. If all fails: escalate.
</cognitive-note>

## arifOS-ACT Embedding

<act-protocol>
Before using this skill on any mutating, irreversible, or high-blast-radius task:

**Step 1 — ART (Codex: validate each sub-step)**
- Attune: What is the real task?
- Recognize: What class of power? (Observer/Maker/Messenger/Mutator/Destroyer/Sovereign)
- Test: fit · authority · evidence · blast · reversible

**Step 2 — Kernel Route (Claude: <kernel-gate>)**
- If action class is Maker/Mutter/Destroyer/Sovereign → route to arifOS for F1-F13 judgment
- Governance path must reach arifOS tools, never A-FORGE directly

**Step 3 — ACT (Hermes: do it)**
- Apply narrow scope
- Constrain blast radius
- Trace witness
- STOP before corruption

**Step 4 — Receipt**
- Leave evidence: what changed, why, under whose authority
</act-protocol>

## Purpose
Route tasks across MCP servers, coordinate server/tool sequences, and define fallbacks when one substrate fails.

## Use When
1. A complex task spans multiple distinct organ environments (GEOX, WEALTH, WELL, A-FORGE)
2. Coordinating sequential multi-tool calls across different MCP servers
3. Defining fallback routes when an MCP server goes offline
4. Auditing active FastMCP server registries
5. Verifying cross-organ constitutional floors during A2A communication

## Do Not Use When
1. Task is entirely within a single local directory
2. Writing standard localized components
3. Task requires structural changes to a specific tool's internal code

## Inputs
<schema codex="strict">
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| intent | string | yes | High-level pipeline task |
| server_registry | object | yes | Active MCP endpoints |
| client_connections | array | yes | Active SSE/stdio channels |
| fallback_policy | string | no | "graceful" or "fail-fast" |
</schema>

## Procedure

<procedure claude="xml-tagged" codex="numbered" hermes="imperative">

### Step 1: Intent Mapping + Brain/Hands Classification
<step id="1" input="user_intent" output="routing_plan">
- **Codex:** Parse intent → identify required tools → classify each as governance or execution → build routing graph
- **Claude:** Use <intent-analysis> to decompose multi-organ requirements. Recall prior routing state from extended context.
- **Hermes:** What does the user need? Which organ has it? Route.

**Routing Rules:**
- Governance, judgment, floors, memory mutation, sealing → **arifOS MCP (8088) FIRST**
- Execution, build, shell, browser, jobs → **A-FORGE MCP (7072)** only after lease
- Domain intelligence → **GEOX (8081) / WEALTH (18082) / WELL (18083)** as needed
</step>

### Step 2: Tool Sequence Plan
<step id="2" input="routing_plan" output="tool_sequence">
- **Codex:** Build ordered tool list. For each: input_schema, output_schema, dependency, fallback. Validate all schemas chain.
- **Claude:** Use <sequence-planning> to construct graph. Identify parallel branches. Insert governance gates.
- **Hermes:** List tools in order. Add arif_judge before any high-risk A-FORGE call. Done.

**Schema (each tool call):**
```json
{
  "tool": "tool_name",
  "server": "arifos|aforge|geox|wealth|well",
  "input": {},
  "output_schema": {},
  "depends_on": ["step_id"],
  "fallback": "alternative_tool or null",
  "governance_gate": true|false
}
```
</step>

### Step 3: F8 Cross-Organ Gating + Lease/Judge Handoff
<step id="3" input="tool_sequence" output="gated_sequence">
- Enforce Floor F8 (Genius/Systemic Health)
- Any mutate/atomic forge_* requires valid lease_id
- Governance paths must reach arifOS canonical tools
- **Codex:** Validate lease_id exists before any A-FORGE call. Log gate decision.
- **Claude:** Use <governance-gate> to verify floor compliance. Recall floor state from context.
- **Hermes:** Need lease? Get lease. No lease? 888_HOLD. Simple.
</step>

### Step 4: Sequential Execution & Verification
<step id="4" input="gated_sequence" output="execution_results">
- Execute step-by-step
- Verify output of each tool before piping to next
- Reject any pipe that lets A-FORGE issue or bypass 888/999 verdicts
- **Codex:** After each step, validate output matches expected schema. Log chain-of-thought.
- **Claude:** Use <verification> after each step. Cross-reference with extended context for anomalies.
- **Hermes:** Run tool. Check output. If bad: stop. If good: next tool.
</step>

### Step 5: Fallback Routing
<step id="5" input="failure_event" output="fallback_result">
- If server fails or times out:
  1. Identify equivalent alternative tools
  2. Gracefully degrade execution loop
  3. Log failure trace
  4. Notify ASI-observability
  5. On governance substrate failure: escalate to 888_HOLD; NEVER fall back to execution-only path
- **Codex:** Check fallback list in order. First viable alternative wins. Log decision.
- **Claude:** Use <fallback-reasoning> to select best alternative considering full context.
- **Hermes:** Server down? Try backup. Backup down? 888_HOLD. All down? Escalate.
</step>

### Step 6: Telemetry Serialization
<step id="6" input="execution_results" output="telemetry_log">
- Record cross-organ connection path
- Record which MCP surface was used for judgment vs execution
- Record lease_id (if any)
- Record tool success counts
- Emit to AAA for lease-compliance and seal-latency metrics
</step>

</procedure>

## Postconditions
1. All sequential tool outputs verified and validated
2. Alternative backup routes executed automatically if primary fails
3. Complete cross-server trace recorded for F11 auditability

## Failure Modes & Escalation
- **Substrate Collapse:** All MCP servers unreachable → degrade, log ERR_MCP_SUBSTRATE_COLLAPSE, halt high-stakes, prompt user
- **Data Pipeline Mismatch:** Output A ≠ Input B schema → invoke hold protocol, refuse to pipe, alert developer

## Floors
- F2 TRUTH: Tool outputs verified before piping. No silent corruption.
- F3 TRI-WITNESS: Cross-organ consensus required for high-stakes routing.
- F4 CLARITY: Routing plan must be more structured than raw intent.
- F8 GENIUS: Systemic health maintained across organ boundaries.
- F11 AUDITABILITY: Full routing trace logged.
