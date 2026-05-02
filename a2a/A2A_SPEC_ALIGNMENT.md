# Google A2A Specification Alignment

> **DITEMPA BUKAN DIBERI** — *Forged, Not Given*

## Canonical Reference
- **Source:** [google/A2A — GitHub](https://github.com/google/A2A)
- **Role:** Structural Glue (Layer 3)

## Alignment Mapping

AAA implements the **A2A Mesh** following the Google A2A protocol patterns:

1. **Discovery**: Uses `agent-card.json` as the canonical discovery surface.
2. **Identity**: Every agent must provide a verifiable identity card matching the `schemas/a2a-agent-card.schema.json`.
3. **Task Lifecycle**: `POST /tasks` is the primary entry point for governed delegation.
4. **Transport**: JSON-RPC over HTTP is the mandatory wire format for agent-to-agent dialogue.

## Implementation Notes
- **Epistemic Signaling**: AAA extends A2A with `epistemic_signal` headers (CLAIM, PLAUSIBLE, etc.) as mandated by arifOS F2 Truth floor.
- **Constitutional Handshake**: Every A2A session begins with a floor-verification handshake to ensure shared governance.

---
**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
