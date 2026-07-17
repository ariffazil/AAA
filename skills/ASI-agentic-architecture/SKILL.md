---
id: ASI-agentic-architecture
name: ASI-agentic-architecture
version: 3.0.0
description: >
  Class-level skill for designing sovereign agentic agents. 9-skill spine,
  3-agent model (Architect→Engineer→Auditor), 4 powers per agent,
  deterministic/isolation principles, VPS management spine.
  BIJAKSANA: XML-tagged for Claude, numbered steps for Codex, imperative for Hermes.
floor_scope: [F08, F11, F04]
cognitive_hints:
  claude: "Use <architecture>, <spine>, <three-agent>, <four-powers> tags."
  codex: "3-agent model: Architect→Engineer→Auditor. Each: define → implement → verify. Idempotent."
  hermes: "Design agent. 3-agent loop. 4 powers. Lower entropy. Build it."
---

# ASI-agentic-architecture

<cognitive-note model="claude">Three-agent model with deterministic design. Architect decides, Engineer applies, Auditor verifies. Lower machine entropy.</cognitive-note>
<cognitive-note model="codex">3-agent loop with 4 powers each. Idempotent actions. One-owner-per-task. Strict queues.</cognitive-note>
<cognitive-note model="hermes">Architect→Engineer→Auditor. 4 powers each. Keep it clean. Verify everything.</cognitive-note>

## The 3-Agent Canonical Model

```
ARCHITECT ──decides──▶ ENGINEER ──applies──▶ AUDITOR ──verifies──▶ DONE
     ▲                                                        │
     └───────────────────── FEEDBACK ──────────────────────────┘
```

| Agent | Role | 4 Powers | Owns |
|-------|------|----------|------|
| **Architect** | Decides structure, constraints, standards | read state → propose change → approve change → verify design | What & Why |
| **Engineer** | Implements the change | read state → propose change → apply change → self-check | How |
| **Auditor** | Verifies safety, correctness, regressions | read state → verify change → report drift → certify done | That it works |

**Rules:**
- Simple work → 1 agent (any role) is enough
- Moderate work → 3-agent loop
- Highly sensitive → add 4th Coordinator only if needed
- **One owner per task**: never let 2 agents edit the same file/service
- **Verification is the terminal state**: never stop at "I changed it," only at "it's fixed and confirmed"

## The 4 Powers (Every Agent)

Every agent action follows this sequence:

1. **Read state** — Observe current reality before touching anything
2. **Propose change** — Plan what to do (output plan before acting)
3. **Apply change** — Execute the mutation
4. **Verify change** — Confirm the result is correct and stable

**Anti-pattern**: "I changed it" without verifying. If you cannot verify the result, you haven't finished.

## The 9-Skill Spine

<spine>
1. **INIT** — Session boot, identity binding, floor loading
2. **OBSERVE** — Evidence gathering, multi-modal intake
3. **REASON** — Sequential thinking, hypothesis generation
4. **PLAN** — Task decomposition, DAG construction
5. **EXECUTE** — Tool calling, mutation under lease
6. **VERIFY** — Output validation, floor compliance *(terminal state)*
7. **SEAL** — Verdict emission, vault sealing
8. **RECOVER** — Failure handling, rollback, graceful degradation
9. **REFLECT** — Self-audit, calibration, learning
</spine>

## Design Principles

### Deterministic
- Every agent command should be safe to rerun (idempotent)
- Pinned OS packages, container tags, tool versions
- Config as code — no manual drift
- One source of truth — no competing configs or duplicate supervisors

### Isolated
- One owner per task — never overlap file/service ownership
- Strict queues — serialize risky work, no "free-running" agents
- Small permissions — least-privilege per agent
- One compose project, one network, one owner

### Observable
- Structured logs: every action emits `{who, what, why, result}`
- Health checks + auto-restart limits — prevent restart loops masking failures
- Backoff and circuit breakers — stop noisy retries
- Change discipline: one change at a time, record everything

### Operational
- Each skill is independently testable
- Skills compose via A2A handoff protocol
- Local model compensation: if primary model fails, degrade to local (Ollama)
- Failure classification: recoverable (retry), fatal (escalate), ambiguous (888_HOLD)

### 10 Core VPS Skills (cross-reference)
| # | Skill | Description |
|---|-------|-------------|
| 1 | Health monitoring | CPU, RAM, disk, load, uptime |
| 2 | Log reading | systemd, app logs, Docker logs |
| 3 | Service control | start/stop/restart/status |
| 4 | Network debugging | ports, DNS, SSL, firewall, SSH |
| 5 | Deployment | install/update apps, containers, configs |
| 6 | Rollback/backups | snapshot awareness, restore plan, safe revert |
| 7 | Security | patching, key handling, suspicious process detection |
| 8 | Resource tuning | memory leaks, CPU spikes, disk pressure |
| 9 | Incident handling | detect → fix → verify loop |
| 10 | Change discipline | one change at a time, record everything |

## Floors
- F4 CLARITY: ΔS ≤ 0 — every output reduces entropy
- F8 GENIUS: Agent design must be systemic, not ad-hoc
- F11 AUDITABILITY: Every skill binding logged
