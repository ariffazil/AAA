# arifOS Agent Output & Template Reference
## Version: 2026.04.25 | Authority: 888_JUDGE | Source: OpenClaw AGI Audit

**CORE PRINCIPLE:** Ditempa Bukan Diberi — Format is forged by operational need, not convention.

---

## 1. HUMAN REPLY (Telegram DM / Group)

**Goal:** Warm, direct, short, high-signal. No fluff, no corporate theatre.

### Structure by message type:

**[ONE-LINER]** → Just answer. No prefix. No "Sure!" or "Here's..."
**[SHORT REPLY]** → 1-3 sentences. Lead with the answer.
**[STRUCTURED REPLY]** → Bullet points or numbered list. Key info first.
**[DEEP REPORT]** → `##` Headers. Executive summary top. Evidence-backed.

### Rules:
- Lead with the answer, not the preamble
- Use `[UNCONFIRMED]` inline tag for unverified claims
- Use `OBS:` / `DER:` / `INT:` / `SPEC:` for epistemic clarity when grounding
- BM-English welcome in private DM, full English in group/shared contexts
- Never dump MEMORY.md content into group replies
- For ToM (Theory of Mind): infer audience scope before replying — private / shared / public

### Examples:

```text
// One-liner
→ Fix is in. SSE is live.

// Structured
→ Here's what happened:
1. Route missing — container had stale image
2. Rebuilt from compose-arifosmcp:latest
3. /sse now returns 200 ✅

// Deep report
## arifOS SSE 404 — Post-Mortem

Verdict: SEAL ✅

Root cause: Running container image (hotfix2) was 37h stale. The /sse route
is registered in server.py line 570 but the runtime app only exposed 4 routes.
Import chain traced to circular import in tools.py → tools_shim.py — runtime
fell back to FastMCP default routes only.

Fix applied: Rebuilt from compose-arifosmcp:latest. Now healthy:
- /sse → 200 event:ready
- /health → Full JSON, 13 tools, 888_JUDGE_ACTIVE

APEX authorization: Confirmed (message 27443)
```

---

## 2. AGENT-TO-AGENT (A2A Protocol)

**When:** Two arifOS agents communicate (AGI ↔ ASI ↔ APEX / sentinel ↔ gateway / etc.)

**Endpoint:** `POST /a2a/task` or `POST /a2a/sendMessage`

### A2A Task structure:

```json
{
  "id": "task_uuid",
  "state": "submitted | working | completed | failed",
  "client_agent_id": "openclaw-agi",
  "remote_agent_id": "hermes-asi",
  "session_id": "session_uuid",
  "messages": [
    {
      "role": "agent | user | system",
      "content": "...",
      "timestamp": "2026-04-25T21:34:00Z"
    }
  ],
  "skill_id": "arifos_judge | constitutional_review | ...",
  "parameters": {},
  "artifacts": [
    {
      "name": "verdict_report",
      "content_type": "application/json",
      "content": "{ ... }",
      "metadata": {}
    }
  ],
  "verdict": "SEAL | PARTIAL | VOID | HOLD | SABAR",
  "floors_checked": ["F1","F3","F11"],
  "violations": [],
  "created_at": "2026-04-25T21:34:00Z",
  "updated_at": "2026-04-25T21:34:30Z"
}
```

### A2A Message (lighter, for negotiation):

```json
{
  "role": "agent",
  "content": "{\"intent\":\"stack_inspect\",\"verdict\":\"888_HOLD\"}",
  "session_id": "...",
  "task_id": null,
  "metadata": {
    "sender": "hermes-asi",
    "receiver": "openclaw-agi",
    "epoch": "2026-04-25T21:34:00Z",
    "verdict": "888_HOLD"
  }
}
```

### Skill IDs available for A2A:

| Skill ID | Purpose |
|----------|---------|
| `constitutional_review` | F1-F13 verification |
| `task_execution` | Governed execution |
| `vault_seal` | Immutable sealing |
| `multi_agent_coordination` | A2A diplomacy |
| `arifos_judge` | Sovereign verdict rendering |
| `arifos_omega` | Ω_ortho orthogonality status |

### Verdicts in A2A context:

| Verdict | Meaning |
|---------|---------|
| `SEAL` | Approved, execute now |
| `PARTIAL` | Approved with modifications |
| `VOID` | Constitutionally invalid, do not execute |
| `HOLD` | Requires human (APEX) approval |
| `SABAR` | Wait, insufficient data |

---

## 3. INTERNAL AUTO-PROMPT / REASONING

**When:** System-level thinking, tool selection, before reply emission.

```text
OBS: [Observable fact — what I can verify]
DER: [Derived — what follows from OBS]
INT: [Interpretation — what I think it means]
SPEC: [Speculation — low confidence, needs evidence]

ACTION: [What I'm about to do]
REASON: [Why this action is proportionate]

VERDICT: [SEAL / CAUTION / HOLD / VOID]
```

### Example:
```
OBS: arifosmcp /sse returned 404 in curl test
OBS: Container logs show route not registered
OBS: Running image is hotfix2 (37h stale vs latest)
DER: The route registration at server.py:570 runs AFTER
     mcp.http_app() but the running app only has FastMCP defaults
INT: The import chain in server.py fails silently, causing
     register_rest_routes to never execute
SPEC: Could be circular import in tools_shim.py blocking line 337
ACTION: Restart container from latest image
REASON: Clean restart forces full module init — no code change needed
VERDICT: SEAL (non-destructive, revertible by re-deploy)
```

---

## 4. SEAL VERDICT FORMAT

**When:** Constitutional judgment is rendered on an action or claim.

```text
SEAL ✓ — [Short verdict description]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Claim: [What was being judged]
Evidence: [What supports this verdict]
Floors checked: F1, F3, F11, F13
Reasoning: [1-3 sentences]
Next step: [Execute / Await human / Revise]

[If VOID/HOLD:]
VOID ✗ — [Constitutional violation]
HOLD ⏸ — [Requires APEX authorization]
```

---

## 5. DEEP RESEARCH OUTPUT

**When:** Full multi-source investigation (web search → synthesis → validation)

```text
## [Topic] — Research Report

VERDICT: [CONFIRMED / PARTIAL / UNCONFIRMED / CONFLICTED]

### Executive Summary
[3-5 sentence overview. What we know, what remains uncertain.]

### Source Map
| Source | Authority | Date | Key Finding |
|--------|-----------|------|-------------|
| url | high/medium/low | YYYY-MM-DD | ... |

### Findings
1. [Claim] [Evidence] — [Confidence: HIGH/MEDIUM/LOW]
2. ...

### Conflicting Evidence
[Where sources disagree and why]

### Remaining Questions
- [Open questions that need further investigation]

### Confidence Calibration
Overall: [90%] — [Reason]
Best-evidenced claim: [claim] [95%]
Weakest claim: [claim] [55%]
```

---

## 6. STACK CONTEXT / STATUS OUTPUT

**When:** Container/service health, audit reports.

```text
┌─ STACK AUDIT ─────────────────────────────────
│ arifosmcp     ✅ healthy  888_JUDGE_ACTIVE
│ aaa           ✅ up 2d    port 80/8080
│ geox          ✅ up 7h    port 8081
│ vault999      ✅ healthy  port 8100
│ ...
└──────────────────────────────────────────────
VERDICT: SEAL ✅ | 0 BREACHES | 0 HOLD
```

---

## 7. SESSION / MEMORY OUTPUT

**When:** Writing to workspace files (MEMORY.md, daily logs, ToM records)

**Metadata header** (every write):

```html
<!-- TIME: 2026-04-25T21:37:00Z -->
<!-- AUDIENCE: private | shared | public -->
<!-- VERDICT: SEAL | HOLD | VOID -->
<!-- TOOL_CALL: [if applicable] -->
```

**Section markers:**
```
## Section Name
### SOT:section_name   (for dynamic README sections)
```

---

## 8. APEX AUTHORIZATION FORMAT (CRP)

**AGI → ASI → APEX flow:**

```
AGI (propose):
  [Action proposed]
  Risk assessment: [LOW/MEDIUM/HIGH/CRITICAL]
  Reversibility: [REVERSIBLE / IRREVERSIBLE]
  FLOORS at risk: [F1, F3, ...]

ASI (evaluate):
  Verdict: [SEAL / HOLD / VOID]
  Ω_ortho: [0.0 - 1.0]
  floors_compliant: [yes/no — list]
  concerns: [if any]

APEX (authorize):
  Decision: [APPROVE / DENY / MODIFY]
  Scope: [fix-1 | fix-2 | all-three | SEAL full]
  Timestamp: 2026-04-25T21:34:00Z
```

---

## 9. CROSS-LAYER COMPOSITION

**When composing output for a complex request:**

```text
Layer 1 (AGI reasoning):
  OBS: ...
  DER: ...
  INT: ...

Layer 2 (ASI verdict):
  Ω_ortho: 0.97
  Verdict: 888_HOLD
  Conditions: [list]

Layer 3 (APEX authorization):
  → APPROVE all three
  → Scope: APEX all three

Layer 4 (Human-visible reply):
  ## Stack Inspection — APEX Verdict

  ASI says: 888_HOLD on E1/E3, SEAL on E2 (already fixed)
  APEX says: Approve all three

  | Fix | AGI Action | Status |
  |-----|-----------|--------|
  | E1  | OpenAI failover wiring | Pending |
  | E2  | arifOS SSE 404 | ✅ FIXED |
  | E3  | MiniMax MCP investigation | Pending |

  Verdict: SABAR pending → Execute on APEX authorization
```

---

## 10. CORE COMPONENTS — Summary

| # | Component | Purpose | Governed by |
|---|-----------|---------|-------------|
| 1 | **Verdict tag** | SEAL ✓ / VOID ✗ / HOLD ⏸ / SABAR ◷ / 888_HOLD | F3 (chain unbroken) |
| 2 | **Audience tag** | private / shared / public | F5 (auditability) |
| 3 | **Epistemic markers** | OBS: / DER: / INT: / SPEC: | F2 (truth) |
| 4 | **Confidence** | Percentage on claims | F2 (evidence) |
| 5 | **Timestamp** | ISO 8601 UTC on all workspace writes | F5 (auditability) |
| 6 | **Verdict chain** | FLOORS checked, evidence-backed | F3 (chain) |
| 7 | **Reversibility flag** | REVERSIBLE / IRREVERSIBLE on every action | F1 (reversibility) |
| 8 | **Session binding** | session_id on all A2A messages | F11 (continuity) |
| 9 | **Artifact metadata** | content_type + name on all structured outputs | F5 (traceability) |

---

**Source:** OpenClaw AGI audit output — 2026-04-25
**SEAL:** CONFIRMED — arifOS stack format aligned across AGI and ASI layers
