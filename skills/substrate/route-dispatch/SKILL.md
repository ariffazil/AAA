---
id: route-dispatch
name: route-dispatch
version: 1.0.0
layer: substrate
description: Right organ for right intent. Classify intent, map to organ, dispatch
  with fallback. Law ≠ execution.
owner: F13 SOVEREIGN
status: active
three_axis: true
axis_version: 1.0.0
---

# route-dispatch

> **Purpose:** Right organ for right intent. Classify intent, map to organ, dispatch with fallback. Law ≠ execution.

## Axis 1: Invariants

- **authority**: arif_route returns organ + tool + confidence
- **evidence_schema**: intent classified with confidence score
- **reversibility**: True
- **lineage**: routing decision logged with intent + organ + timestamp
- **trigger_semantics**: tool_call_ambiguous OR user_intent_unclear OR organ_uncertain
- **failure_contract**: default to read-only observe, never guess execution path
- **resource_budget**: {'cpu': 'minimal', 'time_ms': 2000, 'entropy': 'low'}
- **audit_surface**: ['intent_class', 'organ_selected', 'routing_confidence', 'fallback_used']

## Axis 2: Bridge Connections

- **kernel_verbs**: ['arif_route']
- **skills**: ['kernel-bind']
- **knowledge**: ['know-language']
- **protocol**: synchronous_rpc
- **inputs**: {'intent': 'string', 'context': 'object'}
- **outputs**: {'organ': 'enum[GEOX,WEALTH,WELL,A-FORGE,arifOS,AAA]', 'tool_prefix': 'string', 'confidence': 'float'}

## Axis 3: Contrast

- **Not**: a2a-orchestrator, kernel-trinity, kernel-mcp-governor
- **Distinction**: SINGLE-STEP intent→organ routing. a2a-orchestrator is MULTI-STEP workflow. kernel-trinity is ARCHITECTURAL knowledge. kernel-mcp-governor is MCP transport governance.
- **Trigger conflicts**: fires only when organ is ambiguous; clear calls go direct

## Replaces

- `kernel-mcp-governor`
- `a2a-orchestrator`
- `a2a-explorer`
- `ops-mcp`
- `kernel-trinity`
- `arif-mcp-governor`
- `arifos-mcp-federation`
- `federation-orchestrator`
- `explorer-intelligence-architecture`

---
*Forged: 2026-07-11 under F13 SOVEREIGN.*
*DITEMPA BUKAN DIBERI*
