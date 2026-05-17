---
title: "SKILL: Cloudflare Agents SDK"
type: skill
version: 1.0.0
category: cloud
risk_band: MEDIUM
floors: []
evidence_required: false
sources: [/root/.agents/skills/agents-sdk/SKILL.md]
confidence: high
---

# SKILL: Cloudflare Agents SDK

> **Build AI agents on Cloudflare Workers using the Agents SDK.**
> **Source:** `/root/.agents/skills/agents-sdk/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Creating stateful agents, durable workflows
- Real-time WebSocket apps, scheduled tasks
- MCP servers, chat applications, voice agents
- Browser automation
- Keywords: agents-sdk, cloudflare agents, durable agents, websocket, chat

---

## Retrieval Directive

**Prefer retrieval over pre-training.** Fetch `https://developers.cloudflare.com/agents/` for latest docs.

---

## Key Capabilities

| Capability | API |
|-----------|-----|
| Persistent state | `setState`, `validateStateChange` |
| Callable RPC | `@callable()` methods over WebSocket |
| Scheduling | `schedule()`, `scheduleEvery()`, cron |
| Workflows | `AgentWorkflow`, durable multi-step |
| Durable execution | `runFiber()`, `stash()` |
| Queue | `queue()` with FIFO retries |
| MCP integration | `McpAgent`, MCP client |
| Email handling | `onEmail()`, `replyToEmail()` |
| Streaming chat | `AIChatAgent` with resumable streams |
| React hooks | `useAgent`, `useAgentChat` |

---

## Agent Class Pattern

```typescript
import { Agent, routeAgentRequest, callable } from "agents";

type State = { count: number };

export class Counter extends Agent<Env, State> {
  initialState = { count: 0 };

  validateStateChange(nextState: State, source: Connection | "server") {
    if (nextState.count < 0) throw new Error("Count cannot be negative");
  }

  @callable()
  increment() {
    this.setState({ count: this.state.count + 1 });
    return this.state.count;
  }
}

export default {
  fetch: (req, env) => routeAgentRequest(req, env) ?? new Response("Not found", { status: 404 })
};
```

---

## Routing

| Class | URL |
|-------|-----|
| `Counter` | `/agents/counter/user-123` |
| `ChatRoom` | `/agents/chat-room/lobby` |

---

## Core APIs

| Task | API |
|------|-----|
| Read state | `this.state.count` |
| Write state | `this.setState({ count: 1 })` |
| Schedule (delay) | `await this.schedule(60, "task", payload)` |
| Schedule (cron) | `await this.schedule("0 * * * *", "task", payload)` |
| RPC method | `@callable() myMethod() { ... }` |
| Workflow | `await this.runWorkflow("ProcessingWorkflow", params)` |
| Enqueue | `this.queue("handler", payload)` |
| Retry | `await this.retry(fn, { maxAttempts: 5 })` |

---

## React Client

```tsx
import { useAgent } from "agents/react";

function App() {
  const [state, setLocalState] = useState({ count: 0 });
  const agent = useAgent({
    agent: "Counter",
    name: "my-instance",
    onStateUpdate: (newState) => setLocalState(newState),
  });
  return <button onClick={() => agent.setState({ count: state.count + 1 })}>Count: {state.count}</button>;
}
```

---

## Reference Files

- `references/state-scheduling.md` — State persistence, scheduling, SQL
- `references/callable.md` — RPC methods, streaming, timeouts
- `references/routing.md` — URL patterns, custom routing
- `references/streaming-chat.md` — AIChatAgent, resumable streams
- `references/workflows.md` — Durable Workflows
- `references/mcp.md` — MCP client and server

---

## Related Pages

- [[skill-durable-objects]] — Durable Objects background
- [[skill-mcp-builder]] — MCP server building
- [[skill-workers-best-practices]] — Workers production practices
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Agents SDK mastered. Stateful agents forged.*
