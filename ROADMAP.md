# AAA — Roadmap H1–H4

**Version:** v2026.05.06  
**Organ:** AAA (Arif Autonomous Agent — Control Plane)  
**Maturity:** STAGING (233 commits) — **56 open issues**  
**Role:** Operator cockpit / A2A gateway / session anchoring  
**Status:** SEALED — pending APEX ratification

---

## Executive Summary

AAA is the control plane of the arifOS federation — the operator cockpit and A2A gateway. It is currently the **highest-risk organ** due to 56 open issues including unknown failure modes in the A2A federation handshake.

**AAA responsibilities by horizon:**

| Horizon | Theme | AAA Milestones |
|---------|-------|----------------|
| **H1** (Q2–Q3 2026) | Substrate Hardening | A2A mTLS + cap attenuation, session continuity, issue triage |
| **H2** (Q4 2026–Q1 2027) | Recursive Governance | Session persistence across kernel restart, operator panel |
| **H3** (Q2–Q3 2027) | AGI-Scale Runtime | 10k+ session management, resource isolation |
| **H4** (Q4 2027+) | Foundational Substrate | Third-party organ conformance testing |

---

## H1: Substrate Hardening (Q2–Q3 2026)

### ⚠️ CRITICAL: 56 Open Issues Triage

56 open issues must be triaged to <10 critical within 30 days. This is the highest-priority action in the entire federation.

**Triage protocol:**

```
Step 1: Categorize by type
  - P0 (HALT): Blocks federation operation
  - P1 (CRITICAL): Degrades governance, no workaround
  - P2 (HIGH): Significant impact, workaround exists
  - P3 (MEDIUM): Minor impact
  - P4 (LOW): Backlog, nice-to-have

Step 2: Identify unknown failure modes
  - A2A federation handshake failures
  - Session state loss on restart
  - Token refresh race conditions
  - MCP discovery inconsistency

Step 3: Create concrete reproduction steps for each P0/P1
  - No reproduction = not a P0
  - Reproduction without fix = P0 with fix tracked separately

Step 4: Assign owners and SLAs
  - P0: Fix within 48 hours or escalate to Arif
  - P1: Fix within 7 days
  - P2: Fix within 30 days
  - P3/P4: Add to backlog, revisit at H2

Step 5: Close or consolidate duplicates
```

**Target:** 56 → <10 critical within 30 days  
**Owner:** AAA control plane team  
**Deadline:** June 2026

### H1.1 A2A Mutual Authentication v1.1

Extend `AAA_MUTUALITY_LOCK_PROTOCOL v1.0` (GOLD SEAL) with mTLS + capability attenuation.

**Current state:** Token-based auth with `AAA_MUTUALITY_LOCK_PROTOCOL v1.0`

**Required upgrades:**

```yaml
# a2a_mutual_auth_v1.1
upgrades:
  - name: mTLS Transport
    description: All A2A connections use mutual TLS
    implementation:
      - Each organ gets a client certificate signed by AAA CA
      - AAA validates both client cert AND bearer token
      - Certificate rotation every 24 hours
    
  - name: Capability Attenuation
    description: Each A2A session token is scoped to exactly the tools requested
    implementation:
      - Token includes `allowed_tools: string[]` claim
      - A-FORGE validates tool call against token scope before execution
      - arifOS 888_JUDGE issues scoped tokens
```

**Current token (v1.0):**
```json
{
  "bearer": "aaa-a2a-token-dev",
  "x-a2a-key": "aaa-a2a-apikey-dev"
}
```

**v1.1 token:**
```json
{
  "bearer": "<JWT>",
  "mtls_cert": "<client_cert>",
  "scope": {
    "allowed_tools": ["arif_session_init", "arif_vault_seal"],
    "max_duration_seconds": 3600,
    "organ_id": "hermes"
  }
}
```

**Owner:** AAA protocol team  
**Target:** July 2026  
**Dependency:** AAA issue triage (unknown failure modes must be identified first)

### H1.2 Session Continuity Across Reboot

AAA must persist in-flight session state to VAULT999 so federation sessions survive kernel restart without loss of governance context.

**Session state to persist:**

```typescript
interface PersistedSessionState {
  session_id: string;
  user_id: string;
  organ_id: string;
  
  // Governance state
  current_stage: number;           // 000–999
  verdict_so_far: string;          // Partial verdict chain
  floor_scores: Record<string, number>;  // F1–F13 current scores
  
  // A2A state
  pending_messages: A2AMessage[];
  capability_token_scope: string[];
  
  // Timestamps
  created_at: Date;
  last_active: Date;
  checkpoint_count: number;
}
```

**Implementation:**
1. Add `session_state_persist()` call to VAULT999 before every significant stage transition
2. On AAA restart, read VAULT999 for active sessions and reconstruct state
3. On arifOS restart, AAA re-initializes session context from persisted state

**Owner:** AAA session team  
**Target:** August 2026

### H1.3 Operator Override Latency

F13 veto path must complete in <2 seconds from human trigger to A-FORGE kill signal.

**Path:**
```
Arif (telegram @AGI_ASI_bot) 
  → OpenClaw (A2A)
  → arifOS (888_JUDGE)
  → A-FORGE (kill signal)
  → Execution halted
```

**Latency budget:**
| Segment | Budget |
|---------|--------|
| Telegram → OpenClaw | 200ms |
| OpenClaw → arifOS (A2A) | 300ms |
| arifOS F13 veto evaluation | 500ms |
| arifOS → A-FORGE kill signal | 200ms |
| A-FORGE halt | 300ms |
| **Total** | **< 1500ms** (200ms headroom) |

**Owner:** AAA infra team + A-FORGE  
**Target:** August 2026

---

## H2: Recursive Governance (Q4 2026 – Q1 2027)

### H2.1 Operator Panel Governance

For AGI-weighted decisions, WELL must be able to aggregate readiness across a panel of operators, not just a single human.

**AAA responsibilities:**
- Maintain operator registry (who is in the panel)
- Route strategic decisions to all panel members
- Aggregate responses (unanimous / majority / consensus)
- Handle operator unavailability gracefully

### H2.2 Session Persistence Full Stack

Full session state (including memory, reasoning trace, VAULT999 chain) persisted and resumable across any organ restart.

---

## H3: AGI-Scale Runtime (Q2–Q3 2027)

### H3.1 10,000+ Concurrent Session Management

Resource isolation per session using cgroups. Session state management at scale.

### H3.2 Unified MCP Namespace Registry

AAA publishes `MCP_ENDPOINT_REGISTRY` v2.0 with namespace enforcement.

```
Registry v2.0 requirements:
- Single source of truth for all MCP tool names
- Namespace convention: <organ>_<noun>_<verb>
  - arifOS: arif_session_init, arif_judge_deliberate, etc.
  - GEOX: geox_lithos_interpret, geox_well_log_analyze, etc.
  - WEALTH: wealth_npv_reward, wealth_emv_risk, etc.
  - WELL: well_hrv_fetch, well_cognitive_load_predict, etc.
- Collision detection in CI
- Deprecation path for tool renames
```

---

## H4: Foundational Substrate (Q4 2027+)

### H4.1 Third-Party Organ Conformance Tests

Standardized A2A + MCP conformance tests for third-party organs joining the federation.

---

## Immediate Actions (This Week)

- [ ] **Issue triage session** — Schedule 4-hour session to categorize 56 issues
- [ ] **A2A failure mode audit** — Document all known A2A handshake failure modes
- [ ] **Session state inventory** — What state needs persisting? (H1.2 prerequisite)

---

## Risk Register

| Risk | Probability | Impact | Owner |
|------|------------|--------|-------|
| A2A handshake unknown failure modes | Medium | Critical | AAA |
| 56 issues blocks federation hardening | High | High | AAA |
| Session continuity fails on arifOS reboot | Medium | High | AAA |
| F13 override latency > 2s | Low | Critical | AAA + A-FORGE |

---

**DITEMPA BUKAN DIBERI — Control plane sovereignty is forged, not given.**

*SEALED: 2026-05-06 | AAA Control Plane*
