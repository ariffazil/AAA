# Musyawarah Position: 333-ARCHITECT
## Subject: Federation Stabilization & Cross-Organ Invariants
**Session Date:** 2026-10-18T18:56:00+08:00 (MYT)  
**Role:** 333-AGI (Architect / Intent & Topology)  
**Epistemic Standard:** OBS (Observed) / DER (Derived) / INT (Interpretation) / SPEC (Specification)

---

### 1. Problem Statement
[OBS] The federation recently stabilized key runtimes (WEALTH working_tree clean commit `f4ed354`, WELL runtime upgraded `94539a3`, arifflow-mcp restored on PID 132957 port 7075).
[OBS] However, adversarial sibling audit correctly identified that cross-organ G scalar divergence (AAA 0.875 vs arifOS 0.55) was only "resolved" in prose, not in code.
[OBS] Port 7075 is serving live MCP tools but is absent from federation port registries.
[OBS] Floor F12 `request_trust` remains failed due to unconfigured `ARIFOS_TRUST_AUTO_SIGN`.

---

### 2. Architectural Proposal (333-ARCHITECT)

#### A. Scalar G Single Source of Truth
[SPEC] **Architectural Law:** `arifOS` Kernel is the sole mathematical calculator of APEX scalars ($G$, $C_{\text{dark}}$, $W_3$, $h$, $\text{QDF}$).
[DER] AAA is classified as `DISPLAY_ONLY` (authority ceiling: DISPLAY_ONLY). Therefore, AAA must NOT calculate synthetic scalars independently in TypeScript.
[SPEC] **Target Implementation:**
- In `AAA/src/` or `AAA/a2a-server/server.js`, replace the local synthetic scalar computation with an upstream fetch from `http://127.0.0.1:8088/health`.
- If arifOS is unreachable or degraded, AAA must report `status: "UNKNOWN"` or `value: null` with `source: "arifos.health (unreachable)"`. Under no circumstances should AAA invent a divergent number (e.g. 0.875).

#### B. Port 7075 Formal Registration
[SPEC] **Port Registry Update:**
- Port 7073: `arifFLOW` (Rust Metabolism Daemon - Core FQ & Event Pipeline).
- Port 7075: `arifflow-mcp` (FastMCP Python Service - 8 Tools: `flow_entity_report`, `flow_session_report`, `flow_health`, etc.).
- Update `contracts/mcp_surface.yaml` and related port documentation to register 7075 explicitly, eliminating the "port hantu" class.

#### C. Floor F12 Policy Clarification
[INT] F12 (`request_trust`) fails because `ARIFOS_TRUST_AUTO_SIGN` is unset or 0 in production environment, requiring explicit signature challenge verification.
[SPEC] Recommend F13 ratification of `ARIFOS_TRUST_AUTO_SIGN=observe` during Beta, or keeping fail-closed `HOLD` for unauthorized callers while enabling signed ACT/SCT tokens for registered agents.

#### D. Curated MCP Doorway (P2 Gateway)
[SPEC] The public agent entry point must expose 5 core semantic verbs:
1. `inspect_evidence` (Safe read to GEOX/WEALTH/WELL/CHRON).
2. `get_attention_state` (Read AAA AttentionPackets).
3. `simulate_action` (Dry-run proposal).
4. `submit_for_judgment` (Forward to arifOS 666_JUDGE).
5. `get_receipt` (Retrieve VAULT999 proof).
[DER] This reduces the LLM context surface from 122 implementation tools to 5 governed semantic capabilities.
