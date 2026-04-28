---
name: arifos-agent-output-templates
description: arifOS agent output formats, A2A protocol, verdict system, and forensic replay schema — for Hermes ASI and OpenClaw AGI
tags: [arifOS, A2A, output-format, verdict, SEAL, VOID, forensic-replay, CRP]
created: 2026-04-25
authority: 888_JUDGE
---

# arifOS Agent Output & Template System

## Verdict System — Every Output Carries One

| Verdict | Meaning | Who Can Issue | Effect |
|---------|---------|---------------|--------|
| `SEAL` | Proceed — safe, constitutional | A-VALIDATOR only | Execution authorized |
| `VOID` | Halt — unconstitutional or dangerous | A-AUDITOR, A-VALIDATOR | Execution blocked |
| `888_HOLD` / `SABAR` | Pause — needs human review | Any agent | Sovereign must approve |
| `PARTIAL` | Proceed with conditions | ASI only | Conditions must be met |

**Epistemic labels** (on claims within any output):
- `OBS` — Direct observation
- `DER` — Derived from OBS  
- `INT` — Interpretation
- `SPEC` — Specification/plan

---

## Human → Agent Output (Arif Fazil / Telegram)

Per USER.md rules — **verdicts only, no option lists**:

```
✅ Done: [what happened]
⚠️ SABAR: [risk, safe default chosen, approval needed only if Arif disagrees]
🛑 VOID: [stopped, why]
```

No bullet lists of 3 possible approaches. No "would you prefer A or B?" Pick the best one, defend it.

---

## A2A Protocol — Agent-to-Agent Communication

**Standard:** Google A2A Protocol v0.3.0

**AAA Gateway A2A skills:**
- `agent-dispatch` — non-blocking task dispatch (HOLD required)
- `agent-handoff` — governed delegation (HOLD required)  
- `status-query` — read-only task/run status (on-demand)

**Transports:**
- SSE: `/a2a/events` — server-push to subscribed agents
- streamable-http: streaming JSON-RPC
- JSON-RPC HTTPS: cross-network request/response

**A2A Agent Card schema:**
```json
{
  "protocol_version": "0.3.0",
  "id": "agent-id",
  "name": "Agent Name",
  "url": "https://example.com/a2a",
  "preferred_transport": "sse",
  "capabilities": { "streaming": true, "push_notifications": false },
  "skills": [{ "id": "skill-id", "approval_policy": "hold|on-demand" }]
}
```

---

## Trinity Agent Output Formats

### A-ARCHITECT (Δ — Design Authority)
```
1. Design Proposal — clear, specific recommendation
2. Rationale — why this approach (with evidence cited)
3. Trade-offs — what was considered and rejected
4. Integration Points — how it fits existing system
5. F1 Reversibility Check — how to undo if wrong
6. Constitutional Compliance — F1-F13 check results
```

### A-ENGINEER (Ω — Execution Authority)
```
1. Implementation — the code
2. Test Coverage — tests written
3. Constitutional Check — floor validation
4. Diff Summary — what changed
5. Receipt — execution log reference for VAULT999
```

### A-AUDITOR (Ψ — Judgment Authority)
```
1. Review Summary — Pass/Fail per file
2. Constitutional Audit — F1-F13 check results
3. Issues Found — severity: CRITICAL, HIGH, MEDIUM, LOW
4. Verdict — SEAL, VOID, or 888_HOLD
5. Recommendations — specific fixes required
6. Evidence — citations for all findings
```

### A-VALIDATOR (Ψ — Deployment Gate)
```
1. Validation Report — all checks passed
2. Deployment Plan — strategy (canary/blue-green)
3. Constitutional SEAL — F1-F13 compliance
4. Approval Chain — Human + Auditor + Validator signatures
5. VAULT999 Receipt — immutable deployment record
```

---

## Execution Receipt Schema

Every action generates this audit record:

```json
{
  "receipt_id": "uuid",
  "timestamp": "iso8601",
  "agent_id": "agent://arifos/{role}",
  "session_id": "uuid",
  "request": {
    "intent": "string",
    "tools_requested": ["tool_name"],
    "files_accessed": ["path"]
  },
  "policy_check": {
    "agent_authorized": true,
    "tools_allowed": true,
    "within_boundaries": true,
    "constitutional_passed": true
  },
  "execution": {
    "tools_executed": ["tool_name"],
    "files_modified": ["path"],
    "files_created": ["path"],
    "files_deleted": ["path"]
  },
  "verdict": {
    "status": "SEAL|VOID|888_HOLD",
    "floors_triggered": ["F1", "F2"],
    "human_approval": "APPROVED|PENDING|REQUIRED"
  },
  "vault": {
    "sealed_to_vault999": true,
    "merkle_hash": "sha256"
  }
}
```

---

## Forensic Replay Artifact

Complete decision record for every significant action:

```
replay_artifact:
├── prompt_input (original_prompt, constitutional_context, agent_state)
├── tool_call_chain[] (step, timestamp, reasoning, constitutional_check, result)
├── file_diffs[] (before/after hash, diff_stats, constitutional_review)
├── command_outputs[] (command, exit_code, stdout, agent_interpretation)
├── final_decision
│   ├── verdict: SEAL|VOID|888_HOLD|PARTIAL|SABAR
│   ├── constitutional_basis (per floor)
│   ├── tri_witness: {human, ai, system, W₃}
│   ├── confidence: {G_Genius, Omega_Uncertainty, overall}
│   ├── floors_violated[] (if VOID)
│   └── required_approvals[] (if HOLD)
└── reflection_metadata (trainable_insights[], review_status)
```

Schema source: `/root/arifOS/docs/agents/forensic-replay.yaml`

---

## CRP v1.0 — Conflict Resolution Protocol

```
AGI proposes → CandidateAction + CapabilityClaim
ASI evaluates → VerdictCode + Ω_ortho + Floor compliance
APEX authorizes → ActorBinding + CapabilityToken
Vault persists → 999_SEAL
```

---

## Context Injection Per Situation

| Context | Injected |
|---------|---------|
| New session | SOUL.md + USER.md + MEMORY.md + daily memory |
| Earth/subsurface task | GEOX context before speaking confidently |
| A2A dispatch | Agent card + skill ID + approval_policy |
| Cron/auto-prompt | HEARTBEAT.md + last heartbeat state |
| AGI → ASI handoff | CandidateAction + CapabilityClaim + risk_tier |
| ASI → APEX | VerdictCode + Ω_ortho + Floor compliance |
| Forge execution | ActorBinding + CapabilityToken + arifos://forge manifest |

---

## Event Bus Triggers

Agents listen for:
- **A-ARCHITECT:** git.pull_request, provider.outage, health.critical
- **A-ENGINEER:** git.push, container.health_check_failed, resource.disk_critical
- **A-AUDITOR:** git.push, health.warning, deploy.completed
- **A-VALIDATOR:** deploy.canary_unhealthy, container.health_check_failed, telegram.command:/deploy

---

## Source Files

- Verdict system: `/root/arifOS/docs/agents/system-prompts.yaml`
- Agent identity/policy: `/root/arifOS/docs/agents/agent-identity.yaml`
- Capability manifest: `/root/arifOS/docs/agents/capability-manifest.yaml`
- Event bus: `/root/arifOS/docs/agents/event-bus.yaml`
- Forensic replay: `/root/arifOS/docs/agents/forensic-replay.yaml`
- A2A agent card: `/root/sites/aaa/a2a/agent-card.json`
