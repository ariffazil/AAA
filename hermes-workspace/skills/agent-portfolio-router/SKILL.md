---
name: agent-portfolio-router
description: Routes tasks to the right agent or tool stack — MiniMax CLI vs Codex vs Pi vs subagent vs local tools. Activates when: (1) Arif asks to do something complex that might need sub-agents; (2) a task matches multiple tool/skill profiles; (3) when Arif asks "which agent should handle this". Logs routing decision with reasoning trace so the routing logic itself is auditable.
metadata: {"openclaw": {"emoji": "🧭"}}
---

# Agent Portfolio Router — Choose the Right Agent

When a task arrives, route it to the right actor. This skill prevents two failure modes: over-engineering (spawning Codex for a one-liner) and under-engineering (using a weak model for a complex task).

## Routing Decision Tree

```
TASK
  │
  ├─ Simple question / factual lookup?
  │    └─ YES → web_search or mmx search → direct answer
  │
  ├─ Multimodal generation (image/video/music/speech)?
  │    └─ YES → mmx CLI → mmx-quota-guard first
  │
  ├─ Deep research with synthesis?
  │    └─ YES → mmx-text-researcher skill
  │
  ├─ Coding / building / iterating on code?
  │    ├─ Simple edit / one-liner → use exec + write/edit tools
  │    └─ Complex build / new feature / refactor → sessions_spawn Codex
  │         (in temp dir for PR reviews, in project dir for builds)
  │
  ├─ Parallel independent tasks?
  │    └─ YES → sessions_spawn multiple subagents in parallel
  │
  ├─ Task requires different perspective / adversarial check?
  │    └─ YES → sessions_spawn Pi or second model instance
  │
  ├─ Arif's own infrastructure (arifOS MCP, GEOX, configs)?
  │    └─ YES → use exec/tools directly, delta-logger active
  │
  └─ task is undefined / ambiguous?
       └─ → Ask Arif for clarification — do not guess
```

## Routing Priority Table

| Task Type | Primary Actor | Fallback | Notes |
|---|---|---|---|
| Text generation / chat | mmx text (MiniMax-M2.7) | local LLM | Use highspeed for simple |
| Deep research | mmx-text-researcher (MiniMax-Text-01) | mmx search + text | Structured JSON output |
| Image generation | mmx image | image_generate tool | Check quota first |
| Video generation | mmx video (async) | N/A | Job orchestrator supervised |
| Speech synthesis | mmx speech | tts tool | Stream option for live |
| Music | mmx music | N/A | Job orchestrator |
| Vision / image input | mmx vision | image tool | geo-vision-translator if geo |
| Web search | mmx search | web_search | Structured output preferred |
| Code: one-liner fix | exec + edit | N/A | Fastest path |
| Code: new feature | Codex (sessions_spawn) | Claude Code | PTY mode + workdir |
| Code: PR review | Codex in temp dir | N/A | --full-auto, never in ~/openclaw |
| Multi-agent parallel | sessions_spawn × N | N/A | Independent tasks only |
| Geoscience reasoning | geox-ground skill | N/A | Mandatory epistemic labels |
| Constitutional governance | arifOS-sense | N/A | 888_HOLD if triggered |
| Budget check | mmx-quota-guard | N/A | Always before mmx calls |
| Unknown complexity | sessions_spawn Pi | Ask Arif | Err on asking |

## Routing Audit Log

Every routing decision is logged to `memory/vault999-triage.md`:
```
HH:MM UTC | ROUTE | [task brief] → [actor selected] | reason: [why not alternatives] | alternatives: [what else was considered]
```

Example:
```
11:24 UTC | ROUTE | "Build me a dashboard" → Codex | reason: full-stack build, multi-file, iterative | alternatives: [mmx text (cannot write files), exec (too slow for this)]"
```

## Routing Principles

1. **Fastest path that fits** — never over-engineer simple tasks
2. **Correct tool for the job** — Codex for code, mmx for multimodal, not the other way around
3. **Err on asking Arif** — if task is ambiguous, ask before guessing
4. **Budget before generation** — mmx-quota-guard before any mmx call
5. **Governance before execution** — arifOS-sense before any consequential action
6. **Audit the routing** — log why this path and not the alternatives

## Special Cases

### Arif Infrastructure
Never spawn external agents (Codex, Pi) on Arif's own systems. Use exec + tools directly with delta-logger active.

### ~/clawd / OpenClaw state
NEVER spawn Codex or Pi in `~/.openclaw` or any workspace state directory — they'll read soul docs and system files. Use only the local agent.

### Long-Running Tasks
Always spawn as background with `sessions_spawn` background mode + process monitoring. Never hold the session hostage.

### Cost-Critical Tasks
Route through mmx-quota-guard first. Log estimated cost before committing.
