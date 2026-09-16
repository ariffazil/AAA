---
name: agentic-autonomy-loop
version: 1.0.0
author: Hermes (i-ARIF)
license: MIT
description: "Use when building a 24/7 agent that ticks on its own."
tags: [agent, autonomy, loop, deepseek, mcp, federation, tick]
related_skills: [federation-model-routing, arifos-federation-ops, hermes-forge, FORGE-subagent-spawn]
---

# Agentic Autonomy Loop

A class of agent that runs continuously without human prompting: it observes federation state, judges via a reasoning model, gates on FQ entropy, executes bounded maintenance, and seals an audit trail. Not a chatbot. Not a benchmark. A daemon that thinks on its own schedule.

Pattern shipped at `/root/scripts/aaa_autonomy_loop.py` (2026-08-27, DeepSeek V4 Pro reasoning engine, 15-min tick interval, verified live 3 ticks).

## When to use

Use this skill when the request is "how do I make agent X autonomous / continuous / 24/7 / self-deciding" — when the user wants the agent to **act without being asked**, observe state, and run reasoning on its own clock. Use `hermes-forge` or `FORGE-subagent-spawn` for one-off task execution. Use this for the always-on agent. Trigger words: "autonomous agent", "agent loop", "observe judge act seal", "continuous agent", "AAA autonomy", "agent yang berdikari".

## Architecture (5 stages, per tick)

```
TICK (interval) ──► OBSERVE ──► JUDGE ──► GATE ──► ACT(reasoning) ──► SEAL
                    │            │          │         │                │
                    ▼            ▼          ▼         ▼                ▼
               MCP observe   DeepSeek    FQ<0.5    bounded         local tick
               fq_check     v4-pro      → HOLD    maintenance      audit log
               now_state    envelope    Zen       ONLY (drafs)    + transcript
```

**Decision authority stays in CODE, not the model.** The model proposes (tool calls + JSON verdict); the loop disposes (rounds budget, action whitelist, audit). When rounds exhaust without a verdict, code adopts the last executed action as the decision. This is the Gödel lock applied to a daemon: a 24/7 agent that can NEVER act outside its allowed action set, even if its reasoning engine tries.

## Build recipe (verified working order)

1. **Define the tool schema list** — the model gets exactly N tools, no more. Bounded. Tools must be constitutional verbs: read-only observation (arif_observe, now_state), gate queries (fq_check), and bounded write sinks (vault_draft_write to `/root/arifOS/VAULT999/drafts/`, NOT the sealed vault).
2. **Wire arifOS MCP with proper headers** — `Accept: application/json, text/event-stream` AND `Content-Type: application/json` or you get 405. Normalize URL: env may set `ARIFOS_MCP_URL=http://127.0.0.1:8088` without `/mcp` — strip+re-add the path. Without `arif_init` binding the loop runs as `OBSERVE_ONLY` (don't over-privilege daemons; correct authority for observe-only).
3. **Reasoning loop with round budget** — for `MAX_TOOL_ROUNDS` rounds: post messages with `tools` + `tool_choice: "auto"`; if model returns tool_calls, execute them and append tool-role results; on the FINAL round, force `tool_choice: "none"` so the model must emit its JSON verdict instead of burning the round on another tool call. Without the force, models will write the decision INTO vault_draft as another tool call and never produce a final JSON → decision becomes UNKNOWN.
4. **JSON verdict extraction** — try `json.loads(content)`; if that fails, regex-find the largest balanced `{...}` containing `"decision"` inside content. Don't require the model to be perfectly formatted — extract what you can.
5. **Decision adopt-from-code fallback** — if rounds exhaust with no verdict, adopt the last executed action as the decision with `reason: "rounds exhausted; adopted last action"`. This prevents the loop from emitting `decision: null` and breaking downstream audit.
6. **Audit trail** — write the full message transcript (capped ~50KB) to `/var/lib/<loop>/transcript-<ts>.json` and a one-line summary to `ticks.jsonl`. NEVER write to the final vault — that's reserved for human-confirmed decisions (F13 sovereign authority).
7. **Quiet hours** — silence the loop during 00:00-06:00 MYT (or any configurable band) unless verdict == ESCALATE. This is rate-respecting etiquette, not a security feature.

## Critical pitfalls (each bit me during the build)

- **URL normalization hazard.** `ARIFOS_MCP_URL` env may be set without `/mcp` (e.g. `http://127.0.0.1:8088`). Probe directly; don't assume env is canonical.
- **MCP Accept header is mandatory** — `text/event-stream` in Accept or you get HTTP 405 even with correct path.
- **arifflow FQ gate field name is `actor_id`, not `actor`** — `{"actor_id":"...", "risk_class":"T1", "action":"..."}`. Tested probe pattern at :7073.
- **DeepSeek tool calling returns `tool_calls: []` not null** when model decides no tool — handle empty list explicitly.
- **Decision JSON may be embedded inside a longer content string** — always extract via regex if direct parse fails.
- **Final round force** — without `tool_choice: "none"` on the last round, reasoning models prefer to keep "acting" (more tool calls) over producing a verdict. They will literally write the report into vault_draft as a tool call and never JSON-out. Force the answer.
- **Code is the judge, not the model.** Model proposes; code disposes. Action whitelist is enforced in `execute_tool()` — model can't reach outside it even if it tries to call an undeclared tool name (returns `{"source": name, "error": "unknown tool"}`).
- **Path traversal block on vault writes** — reject filenames containing `/` or `..` BEFORE writing. The model can pass `../../etc/passwd` in `filename` and Python's `write_text` would happily follow it.
- **Cost-aware tick interval** — 15-min interval × DeepSeek V4 Pro = ~$0.50/day at 1K tokens/reasoning. Use v4-flash if budget tight; v4-pro only when reasoning quality matters (Gödel-judge-class decisions).

## Live verification (run before declaring the loop operational)

```bash
source /root/.secrets/kunci-root.env
python3 -B -c "
import sys; sys.path.insert(0, '/root/scripts')
from aaa_autonomy_loop import tick
record = tick()
print('DECISION:', record['decision_summary'])
print('TOOLS:', record.get('tools_executed'))
print('REASON:', (record.get('decision') or {}).get('reason','')[:200])
"
```

Expected: 3+ tools called, decision != UNKNOWN, transcript written. If decision == UNKNOWN, the final-round force isn't biting — check `MAX_TOOL_ROUNDS` env and that `tool_choice: "none"` is on the last round.

## Service install (systemd)

Requires Arif's consent via approval gate (systemctl writes are flagged). When approved, `WantedBy=multi-user.target` unit pointing at the script with `EnvironmentFile=/root/.secrets/kunci-root.env` and `Restart=on-failure`/`RestartSec=30` is sufficient. Or fall back to `*/15 * * * *` crontab — simpler, no restart-on-fail, but overlapping ticks possible if a tick takes >15 min.

## Reference files

- `references/aaa-autonomy-loop-build.md` — the full 2026-08-27 build narrative: probe→patch→test sequence, exact error messages, what got fixed and why.