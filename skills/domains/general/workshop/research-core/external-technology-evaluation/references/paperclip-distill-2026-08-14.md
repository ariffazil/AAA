# Paperclip Distill — Mode 5 Repo Evaluation (2026-08-14)

> **PURPOSE:** Canonical record of the Paperclip (AI company OS) evaluation — what it is, where it sits in the agent-ecosystem taxonomy, and the 5 protocols to ingest into arifOS organs. Future sessions: do NOT re-clone; the distill decisions live here.

## Source & Live Data (OBS, 2026-08-14)

- Repo: `paperclipai/paperclip` — MIT, TypeScript (Node server + React UI), 106MB shallow clone
- **78,114 ★ · 14,326 forks · created 2026-03-02 · velocity ≈ 14,500 ★/month**
- Self-description: "The app people use to manage AI agents for work" — *"If OpenClaw is an employee, Paperclip is the company."*
- Structure: `server/src/services/` = 235 services (budgets, approvals, heartbeats, watchdogs, tool-access-policy, sandbox-provider-runtime…), `packages/adapters/` (claude, codex, cursor, gemini, grok, **hermes**, openclaw, opencode, pi), skills-catalog + teams-catalog with provenance, external-task-protocol spec (Linear/Jira/GitHub Issues sync, idempotent link store).

## Agent-Ecosystem Taxonomy (validated this session)

| Tier | Systems | Signal |
|---|---|---|
| Constitution | arifOS (ours) | bounds institutions; nobody else occupies this layer |
| Institution | Paperclip | org chart, budgets, governance, mission — agent-as-employee |
| Personal runtime | Hermes (230K★), OpenClaw (386K★) | agent-you-live-with |
| Specialist worker | OpenCode (sst, 197K★), Claude Code, Codex | delegate-one-domain |
| Framework | MetaGPT 69.8K★ (dormant since 2026-01), AutoGen 60.4K★, CrewAI 57K★, LangGraph 39.7K★ | build-agents-for-others; ossifying |
| Vendor SDK | OpenAI Agents, Google ADK | lock-in disguised as framework |

**Fork ratio (forks/stars) = deployment signal**: runtimes/platforms 18–21% vs frameworks 12–17%. Star velocity: OpenClaw 42.9K/mo > Hermes 18.4K/mo > OpenCode 12.6K/mo >> frameworks ~1.1–1.9K/mo. Market says: people want agents and institutions, not frameworks.

## Constitutional Contrast (why not institution-ledger envy)

Paperclip governance = **managerial**: approve hires, override strategy, pause agents, RBAC, budgets. Human is a NODE in the org chart. arifOS = human is the AUTHOR outside the system; F13 is constitutive, not top-of-chart. Their only HARD alignment floor is **budget** (money as circuit breaker); mission alignment is propagation, not falsification. "Internal trace collection, compounding data value" — they are collecting org-level behavioral data at multi-tenant scale; overlaps the I-ARIF moat data class but not the sovereign failure-grammar pairs.

## Distill Decisions

### INGEST (5, by priority)
1. **P1 — Budget hard-stop → FLAME**: `observedAmount >= amount → "hard_stop"` → scope `paused` + `pauseReason: "budget"` + guidance ("raise budget and resume, or keep paused"). This is W_scar HOLD-not-DROP in production code. Copy the **state machine + machine-readable reason + human-decidable guidance**, not just the number check.
2. **P2 — Heartbeat wake-request queue → arifFLOW**: agents wake on state change (assignment, comment, upstream-done, watchdog-detected-stopped-subtree), not on clock. Details worth stealing: 15s first-run grace window (avoids false-positive stopped detection racing the assignment run), stop-fingerprint prefix dedup, wake statuses queued/deferred.
3. **P3 — Atomic checkout → A-FORGE/CCC**: single-assignee claim semantics + idempotent external link store (survives webhook replays/restarts, fingerprint per sync state). Kills the double-fire/duplicate-worker bug class in delegate_task retries.
4. **Adapter contract → FED**: one package two transports (local child process / gateway HTTP+SSE), typed `TranscriptEntry` for all harnesses, benign-stderr reclassification (MCP init noise ≠ error). Fixes dirty-transcript problem with OpenCode/Claude Code spawns.
5. **Catalog provenance → skill substrate**: `catalog/bundled|optional` + `generated/` + provenance service + company-skill-policy. Anti-drift structure for our 700+ overlapping skills (feeds AUDIT-skill-atlas).

### AVOID
- React manager dashboard (manager-first worldview ≠ sovereign)
- Multi-company SaaS multi-tenancy (we are single-tenant sovereign)
- 235-service sprawl (their disease, not ours)
- Org-chart layer (institution modeling belongs to arifOS, which bounds institutions)

### BIND (leverage, don't build)
Paperclip already ships `hermes_local` + `hermes_gateway` adapters (skills sync from `~/.hermes/skills/`, config detection, transcript parsing, session codec). Integration door is open on their side. If Arif ever runs a commercial AI company: one Paperclip instance = one institution under the constitution; their heartbeat protocol is the arifOS→institution binding interface. We sit above; we don't maintain a fork.

## Protocol-stack foresight
```
MCP        = agent talks to tools       (standardized)
Heartbeat  = institution talks to agents (Paperclip de facto)
(arifOS)   = constitution bounds institutions (empty layer, ours)
```

## Tooling lessons (session)
- `gh api repos/<repo> --jq` — authenticated, no rate limit hit; raw curl api.github.com died mid-batch at ~10 calls.
- SearXNG web_search returned empty `{"web": []}` repeatedly → pivot transport (gh api + shallow clone), don't rephrase forever.
- Shallow-clone reading order: README → AGENTS.md/DESIGN.md → packages/docs tree → `ls server/src/services/` → specs. Directory names carry the architecture; don't read source line-by-line.

## Status
P1–P5 proposed, awaiting Arif's GO/HOLD (2026-08-14). Clone at /tmp/paperclip-study (ephemeral).
