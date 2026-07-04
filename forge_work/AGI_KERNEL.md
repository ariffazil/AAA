# AGI KERNEL REFERENCE LIBRARY — For the Forging Agent

**Forged:** 2026-06-14T06:40 UTC  
**Updated:** 2026-06-14T06:55 UTC (v1.2 — tiered reading order, consolidated libraries by language, explicit forging instructions, session addendum)  
**Sovereign:** Muhammad Arif bin Fazil  
**Doctrine:** DITEMPA BUKAN DIBERI — study everything, copy nothing, forge your own.
**Purpose:** Stacked reference library for A-FORGE, OpenClaw, Hermes, and any future forging agent building toward real AGI kernel substrate.
**Doctrine:** DITEMPA BUKAN DIBERI — study everything, copy nothing, forge your own.

---

## §0 — How to Use This

Feed this document to your forging agent with context:

> "You are building a personal AGI kernel called arifOS. It is a constitutional MCP-native kernel with 7 domain organs, NATS mesh, VAULT999 immutable ledger, and E7 Principal Paradox enforcement. Study these references. Understand the patterns. Then forge improvements to our substrate — not copies of these projects, but lessons absorbed and transformed."

The 6 capability bands below match the arifOS architecture. Each band has:
- **Core repos** — study these deeply
- **What to steal** — the design pattern, not the code
- **How it complements arifOS** — where your stack already has this covered, where it doesn't

---

## §1 — MCP Substrate & Protocol Layer

### Core Repos

| Repo | URL | Why |
|------|-----|-----|
| **Model Context Protocol** | https://github.com/modelcontextprotocol | Canonical MCP spec, SDKs (Python, TypeScript), transport patterns. Ground truth for all tool surfaces. |
| **FastMCP** | https://github.com/jlowin/fastmcp | Best practical MCP framework. Clean decorators, streamable HTTP, SSE, stdio. Your arifOS MCP servers already use this. |
| **MCP Python SDK** | https://github.com/modelcontextprotocol/python-sdk | Low-level MCP client/server. When FastMCP isn't enough. |
| **awesome-mcp** | https://github.com/abordage/awesome-mcp | Discovery layer — MCP servers, clients, frameworks, patterns. Mine this continuously. |
| **MCP Gateway (Anthropic)** | https://github.com/anthropics/anthropic-cookbook/tree/main/mcp | Reference gateway patterns — routing, auth, tool aggregation. Study for your gateway on :8091. |
| **OpenAI Agents SDK with MCP** | https://github.com/openai/openai-agents-python | How a major provider wires MCP into agent loops. Compare with your arifOS approach. |

### What to Steal

- **Streamable HTTP transport** — FastMCP 3.4.2 pattern for session persistence across tool calls. You already use this in your gateway upstream pool.
- **Tool discovery via `tools/list`** — canonical pattern. Your gateway auto-discovers 62+ tools on startup — this is the standard you're implementing.
- **Resource surfaces** — MCP resources (not just tools) for exposing state (`/health`, `/attestation`, `/readiness`). Your organs already do this.

### How It Complements arifOS

✅ arifOS IS MCP-native. All 7 organs speak MCP. Gateway on :8091 aggregates them.  
✅ FastMCP used in arifOS kernel, GEOX, WEALTH, WELL, MIND, MEMORY.  
⚠️ Missing: MCP auth extensions (OAuth, API key). Your gateway uses session pools instead.  
⚠️ Missing: Stdio transport on all organs (only HTTP today). Adding stdio would let Claude Code/Cursor call organs directly.

---

## §2 — Governance & Control Plane

### Core Repos

| Repo | URL | Why |
|------|-----|-----|
| **Agentic Control Plane** | https://agenticcontrolplane.com/product | Reference gateway: identity, permission checks, routing, rate limiting, audit above any MCP client. Study architecture, not code. |
| **Guardrails AI** | https://github.com/guardrails-ai/guardrails | Output validation with Pydantic-style schemas. Closest thing to floor enforcement in the wild — but for output text, not tool authority. |
| **NVIDIA NeMo Guardrails** | https://github.com/NVIDIA/NeMo-Guardrails | Dialogue-level safety rails. More config-driven than arifOS, but useful for studying how safety composes. |
| **OpenAI Agents SDK — Guardrails** | https://github.com/openai/openai-agents-python | Input/output guardrails in agent loop. Study the pattern of `@input_guardrail` / `@output_guardrail` decorators — compare with your F1-F13 pipeline. |
| **IBM Agent Control Plane** | https://www.ibm.com/think/topics/agent-control-plane | High-level vocabulary alignment. How big tech thinks about "control plane" — useful when generating docs for external readers. |
| **GitHub Enterprise AI Controls** | https://github.blog/changelog/2026-02-26-enterprise-ai-controls-agent-control-plane-now-generally-available/ | Production control plane reference: what "enterprise governance" means in practice. Benchmark, not target. |

### What to Steal

- **Guardrails as decorators** — `@floor_check(F1)` pattern could wrap MCP tools cleanly. You already have floor gating in `tools.py` — but decorator syntax would make it more composable.
- **Control plane as gateway** — Agentic Control Plane's pattern of "every MCP call → identity check → permission check → audit log → proxy to tool" is what your gateway on :8091 does. Study their auth layer for ideas.
- **Policy as config, not code** — NeMo Guardrails uses YAML for safety rules. arifOS floors are Python code (stronger, but harder to audit externally). A YAML floor specification that compiles to code could be a forge task.

### How It Complements arifOS

✅ arifOS HAS a control plane — AAA mesh + gateway + floor enforcement.  
✅ F1-F13 floors ARE code-enforced, not config-driven (stronger than anyone).  
✅ E7 Principal Paradox IS a unique governance primitive — nobody else has it.  
⚠️ Missing: Policy-as-config layer for non-coders to read floors.  
⚠️ Missing: External control plane dashboard (AAA cockpit not rendering live state yet).  
⚠️ Missing: E1-E7 deployed to live kernel (two-copy drift).

---

## §3 — Durable Execution & Agent Workflows

### Core Repos

| Repo | URL | Why |
|------|-----|-----|
| **Temporal** | https://github.com/temporalio/temporal | Gold standard for durable execution. Workflows survive crashes, retry automatically, checkpoint state. |
| **Temporal Python SDK** | https://github.com/temporalio/sdk-python | How to write durable workflows in Python. Study `@workflow.defn` and `@workflow.run` decorators. |
| **LangGraph** | https://github.com/langchain-ai/langgraph | Stateful agent graphs with checkpointing, branching, human-in-the-loop nodes. |
| **DuraLang** | https://temporal.io/code-exchange/duralang-durable-stochastic-ai-agents-with-one-decorator | Temporal + LLM agents. Makes LLM calls, tool calls, MCP calls, and agent-to-agent calls durable with ONE decorator. Very relevant. |
| **Prefect** | https://github.com/PrefectHQ/prefect | Lighter-weight workflow orchestration in Python. Good for simpler agent pipelines. |
| **Restate** | https://github.com/restatedev/restate | Durable execution for TypeScript/Java. Lighter than Temporal. If A-FORGE (Node.js) needs durable workflows. |

### What to Steal

- **Workflow-as-code with automatic retry** — Temporal's pattern: write a function, mark it `@workflow`, and the platform handles retries, state persistence, and recovery. Your agent loops (MIND → arifOS → A-FORGE) could benefit from this.
- **Human-in-the-loop nodes** — LangGraph's `interrupt()` pattern for pausing workflows until human approves. Compare with your 888_HOLD gate.
- **Durable MCP calls** — DuraLang's insight: MCP tool calls are just function calls that should survive process death. If your agent is halfway through a GEOX→WEALTH→arifOS pipeline and the VPS reboots, can it resume?
- **Checkpoint-based state** — LangGraph's checkpointing means the graph state is serialized after every node. Compare with your Graphiti edges — similar pattern, different layer.

### How It Complements arifOS

✅ A-FORGE already has forge gates (4-layer).  
✅ MIND sequential thinking already checkpoints thoughts.  
⚠️ Missing: Full durable execution — if a forge task crashes mid-way, no automatic resume.  
⚠️ Missing: Human-in-the-loop as first-class primitive (888_HOLD exists but isn't workflow-integrated).  
⚠️ Missing: Long-running agent workflows (multi-hour/days research jobs) — everything is session-scoped.

---

## §4 — Graph Memory & Cognitive Architecture

### Core Repos

| Repo | URL | Why |
|------|-----|-----|
| **Graphiti** | https://github.com/getzep/graphiti | Temporal knowledge graph for agents. Historical truth retention, retrieval under changing state. Your closest external reference. |
| **Awesome-GraphMemory** | https://github.com/DEEP-PolyU/Awesome-GraphMemory | Survey of graph-based agent memory. Expose your forging agent to design patterns beyond vector memory. |
| **Mem0** | https://github.com/mem0ai/mem0 | Memory layer for AI agents — long-term, cross-session. Simpler than Graphiti, good for studying memory API design. |
| **Letta (MemGPT)** | https://github.com/letta-ai/letta | Self-editing memory for agents. Operating system model of memory management. |
| **FalkorDB** | https://github.com/FalkorDB/FalkorDB | Graph database you already use (L5). Redis-based, Cypher queries, low latency. |
| **Qdrant** | https://github.com/qdrant/qdrant | Vector database you already use (MEMORY organ). Semantic search with metadata filtering. |
| **Neo4j** | https://github.com/neo4j/neo4j | Most mature graph database. If FalkorDB ever limits you, Neo4j is the fallback. |
| **Kùzu** | https://github.com/kuzudb/kuzu | Embedded graph database. No server needed — good for local agent memory without infrastructure. |

### What to Steal

- **Temporal edges in Graphiti** — episodes expire, relationships decay, truth has a time horizon. Your 10-field memory envelope already captures this — but the *decay function* (when does old evidence become less reliable?) is a forge task.
- **Self-editing memory** (Letta/MemGPT) — the agent can update its own memory, consolidate, forget. Your memory doctrine says "memory is stored consequence, not truth" — but the *agent* currently can't edit its own memory episodes. Should it be able to? Under what floors?
- **Graph RAG** — hybrid retrieval (vector similarity + graph traversal). Your MEMORY organ already does this (Qdrant semantic search + Graphiti graph expansion). Study how others compose these two retrieval modes.
- **Episode linking** — when MIND stores a plan and MEMORY recalls it, the episodes should be linked ("this plan was informed by this prior conclusion"). Graph edges with provenance. Already in L5 — but the auto-linking is manual.

### How It Complements arifOS

✅ MEMORY organ already bridges Qdrant + Graphiti + FalkorDB.  
✅ 10-field metadata envelope on every episode — governed memory exists.  
✅ L5 bridge connects OpenClaw + Hermes to the same graph.  
⚠️ Missing: Memory consolidation/forgetting (agent can't prune its own memory).  
⚠️ Missing: Temporal decay functions (evidence reliability over time).  
⚠️ Missing: Cross-episode contradiction resolution (flagging when two stored episodes disagree).

---

## §5 — Event Mesh & Multi-Agent Transport

### Core Repos

| Repo | URL | Why |
|------|-----|-----|
| **NATS Server** | https://github.com/nats-io/nats-server | Your mesh backbone. JetStream for persistence, key-value store, object store. |
| **NATS Python Client** | https://github.com/nats-io/nats.py | Python NATS client. Your organs need this to publish heartbeats/verdicts. |
| **NATS Node.js Client** | https://github.com/nats-io/nats.js | TypeScript NATS client. AAA (Node.js) needs this for cockpit subscriptions. |
| **NATS JetStream Examples** | https://github.com/nats-io/nats.py/issues/200 | Python JetStream edge cases. Useful for debugging. |
| **NATS by Example** | https://github.com/nats-io/nats-by-example | Practical patterns for pub/sub, request/reply, queue groups, JetStream. |
| **A2A Protocol (Google)** | https://github.com/google/A2A | Agent-to-Agent protocol spec. Discovery, task send/receive, streaming. Your AAA already implements this. |
| **Autogen (Microsoft)** | https://github.com/microsoft/autogen | Multi-agent conversation framework. Study the agent communication patterns — not to adopt, but to contrast with your mesh approach. |
| **CrewAI** | https://github.com/crewAIInc/crewAI | Role-based multi-agent orchestration. Simpler than your federation, but useful for studying role definition patterns. |

### What to Steal

- **JetStream consumer patterns** — durable consumers that resume from last acknowledged message. Your `arifos-governance` stream has 0 messages — when you wire it, use JetStream consumers that don't lose messages during restarts.
- **NATS as service mesh** — every organ publishes heartbeat to `arifos-organs` (already 8,932 messages). Every verdict publishes to `arifos-governance` (0 messages — wire this). Every agent subscribes to relevant subjects. This is the NATS-native service mesh pattern.
- **A2A task lifecycle** — Google's A2A defines task states (submitted → working → completed/failed/canceled). Your AAA already implements this. Study the streaming extensions for real-time task progress.
- **Queue groups for load distribution** — if you ever run multiple instances of the same organ, NATS queue groups distribute work. Not needed at personal scale — but the pattern is there.

### How It Complements arifOS

✅ NATS is running. Streams exist. AAA A2A server is live on :3001.  
✅ 8,932 messages in `arifos-organs` — someone IS publishing.  
⚠️ `arifos-governance` stream: 0 messages. Governance pipeline not wired.  
⚠️ No organ publishes heartbeats with structured metadata (constitution hash, tool count, health status).  
⚠️ A2A task streaming not implemented (tasks are request/reply, not streamed).

---

## §6 — AI Agent Frameworks & Orchestration

### Core Repos

| Repo | URL | Why |
|------|-----|-----|
| **LangChain** | https://github.com/langchain-ai/langchain | The 800-pound gorilla. Study for tool integration patterns, not to adopt. |
| **LangGraph** | https://github.com/langchain-ai/langgraph | Stateful agent graphs. Already covered in §3 — but the agent loop patterns (Plan → Execute → Observe → Reflect) are worth studying. |
| **OpenAI Agents SDK** | https://github.com/openai/openai-agents-python | OpenAI's agent framework. Study `Agent`, `Runner`, `handoff` patterns. Compare with your agent authority model. |
| **CrewAI** | https://github.com/crewAIInc/crewAI | Role-based multi-agent. Study `Agent(role=..., goal=..., backstory=...)` — compare with your SOUL.md + AGENTS.md pattern. |
| **AutoGen** | https://github.com/microsoft/autogen | Multi-agent conversations. Study `ConversableAgent` and group chat patterns. |
| **Dify** | https://github.com/langgenius/dify | Visual agent builder. Study the UI/UX of how non-coders build agent workflows — AAA cockpit reference. |
| **ElizaOS** | https://github.com/elizaOS/eliza | Agent framework with character files. Closest pattern to your SOUL.md identity files. |
| **Agno** | https://github.com/agno-agi/agno | Lightweight agent framework. Study the minimalism — how much can you strip away and still have an agent? |

### What to Steal

- **Tool schema as first-class** — every framework converged on: tools have name, description, JSON schema. MCP formalized this. Your 160+ tools already follow this pattern.
- **Agent-as-character** (ElizaOS) — character files define personality, knowledge, style, and boundaries. Your SOUL.md + AGENTS.md + USER.md IS this pattern, but more constitutional.
- **Handoff patterns** (OpenAI SDK) — `agent.handoff(next_agent)` transfers control. Your A2A bridge already does this — but the handoff could be more formal (task envelope + state transfer + lease check).
- **Visual workflow builder** (Dify) — drag-and-drop agent workflows. Your AAA cockpit could add a "forge workflow" view where Arif can visually compose organ pipelines.

### How It Complements arifOS

✅ OpenClaw + Hermes + APEXMax already form a governed multi-agent federation.  
✅ SOUL.md identity files ARE the character/agent definition pattern — but constitutional.  
⚠️ No visual workflow builder — AAA cockpit is command-line/health dashboard, not a workflow composer.  
⚠️ No formal handoff protocol — A2A works but task context transfer between agents could be richer.

---

## §7 — Real-World AI Operating Systems & Personal AGI

### Core Repos

| Repo | URL | Why |
|------|-----|-----|
| **Argent OS** | https://github.com/argent-os | Personal AI operating system. Multi-repo architecture. Study the "OS for one person" framing. |
| **AgentOS** | https://github.com/agent-os/agent-os | Agent execution environment. Agents as first-class processes. Study process model. |
| **EdenAGI** | https://github.com/eden-agi | Open-source personal AGI project. Study the "personal" claim — what does it mean to them vs to arifOS? |
| **Open Interpreter** | https://github.com/OpenInterpreter/open-interpreter | Local code execution agent. Study the terminal-first UX — compare with A-FORGE's aft shell. |
| **OpenCog** | https://github.com/opencog/opencog | Classic AGI cognitive architecture. AtomSpace, attention allocation, reasoning. Study for cognitive architecture patterns — not to adopt. |
| **NARS (OpenNARS)** | https://github.com/opennars/opennars | Non-Axiomatic Reasoning System. Study the "reasoning under insufficient knowledge and resources" framing — complements F7 Humility. |
| **AIOS** | https://github.com/aios-org/aios | LLM Agent Operating System. Agents scheduled as OS processes with resource management. Study the OS metaphor. |
| **OS-Copilot / FRIDAY** | https://github.com/OS-Copilot/OS-Copilot | Self-improving OS agent. Study the self-improvement loop — compare with A-FORGE's forge cycle. |

### What to Steal

- **"OS for personal AI" framing** (Argent OS) — how they explain "this is an OS, not an app" to users. Your arifOS could use clearer public framing.
- **Agent as OS process** (AgentOS, AIOS) — agents have PID, resource limits, scheduling, signal handling. Your agents (Hermes, OpenClaw, 000/opencode) already have systemd units — but not first-class in-process management.
- **Non-Axiomatic Reasoning** (NARS) — reasoning with insufficient knowledge. F7 Humility in philosophical form. Study NARS for the *epistemology* of bounded agents — it's the theoretical complement to your practical F7 enforcement.
- **Self-improving OS agent** (FRIDAY) — agent that learns from its own tool-use history. Compare with A-FORGE + Graphiti pattern (task → organ path → outcome → edge weight).

### How It Complements arifOS

✅ arifOS IS a personal AGI OS — but hasn't claimed that framing publicly.  
✅ Agent process model via systemd — but not first-class in-kernel.  
⚠️ Missing: Public "what is this?" page that explains the OS metaphor.  
⚠️ Missing: Self-improvement loop that learns from execution history (Graphiti has the data, no automated learning from it yet).

---

## §8 — Specific Libraries & Dependencies Your Forging Agent Needs

These are the practical Python + TypeScript libraries your agents should know about when coding improvements:

### Python (Kernel & Organs)

| Library | Purpose | Already Used? |
|---------|---------|--------------|
| **fastmcp** | MCP server framework | ✅ arifOS, GEOX, WEALTH, WELL, MIND, MEMORY |
| **pydantic v2** | Schema validation | ✅ everywhere |
| **nats-py** | NATS client (JetStream) | ⚠️ AAA uses it, organs don't yet |
| **httpx** | Async HTTP client | ✅ gateway upstream pool |
| **anyio** | Async I/O (Trio-style) | ✅ FastMCP dependency |
| **lasio** | LAS well log parsing | ✅ GEOX |
| **segyio** | SEG-Y seismic I/O | ✅ GEOX |
| **numpy / scipy** | Numerical computing | ✅ GEOX, WEALTH |
| **matplotlib** | Plotting | ✅ GEOX |
| **qdrant-client** | Vector DB client | ✅ MEMORY organ |
| **redis / fakeredis** | Caching | ✅ VAULT999? (check) |
| **cryptography** | Ed25519, hashing | ✅ ROOTKEY (E1-E7) |
| **prometheus-client** | Metrics export | ⚠️ Not yet — would enable Prometheus+Grafana for AAA cockpit |
| **structlog** | Structured logging | ⚠️ Not yet — would make journalctl parsing cleaner |

### TypeScript/Node.js (AAA, A-FORGE)

| Library | Purpose | Already Used? |
|---------|---------|--------------|
| **nats.js** | NATS client | ⚠️ AAA should use this |
| **@modelcontextprotocol/sdk** | MCP client/server SDK | ⚠️ If AAA or A-FORGE need MCP |
| **express / fastify** | HTTP server | ✅ AAA uses Express? (check package.json) |
| **ws** | WebSocket | ✅ A-FORGE terminal |
| **react / vite** | Frontend cockpit | ✅ AAA cockpit |
| **tailwindcss** | Styling | ✅ AAA cockpit |
| **@anthropic-ai/sdk** | Claude API | ⚠️ If Hermes needs Claude fallback |
| **openai** | OpenAI API | ⚠️ For model routing |

### Infrastructure

| Tool | Purpose | Already Used? |
|------|---------|--------------|
| **systemd** | Service management | ✅ All organs |
| **caddy** | Reverse proxy | ✅ Public endpoints |
| **cloudflared** | Tunnel | ✅ arif-fazil.com |
| **docker** | Containerization | ✅ Graphiti, Qdrant, FalkorDB |
| **nats-server** | Mesh backbone | ✅ Running on :4222 |
| **prometheus + grafana** | Metrics + dashboards | ⚠️ NOT deployed — would make AAA cockpit beautiful |

---

## §9 — What to Forge Next (Priority Order for A-FORGE)

Based on this reference library, the highest-impact forge tasks:

| # | Task | Reference to Study | Impact |
|---|------|-------------------|--------|
| 1 | **Wire governance stream** — organs publish verdicts to NATS `arifos-governance` | NATS JetStream patterns | Makes mesh observable |
| 2 | **Deploy E1-E7 to live kernel** — fix two-copy drift, activate ROOTKEY in running kernel | Your own ROOTKEY_SPEC_v54.md | Activates constitutional mesh |
| 3 | **NATS heartbeat publisher** — each organ publishes structured heartbeat (constitution_hash, tool_count, health) every 30s | NATS by Example, your own arifos-organs stream | Makes AAA cockpit renderable |
| 4 | **Prometheus + Grafana** — metrics from all organs, rendered in AAA cockpit | prometheus-client, grafana docs | Beautiful live dashboard |
| 5 | **Durable forge workflows** — A-FORGE forge tasks survive process death, resume from checkpoint | Temporal / LangGraph checkpointing patterns | Production-grade execution |
| 6 | **Memory consolidation agent** — agent that periodically reviews memory episodes, flags contradictions, prunes stale data | Graphiti temporal edges, Letta self-editing patterns | Governed memory hygiene |
| 7 | **Public `/what-is-this` page** — OS metaphor framing for arifos.arif-fazil.com | Argent OS framing, AIOS metaphor | External clarity |

---

## §10 — Best-Fit by arifOS Repo (Agent-Type Routing)

Which references to feed to which forging agent:

| Layer | Best Resource | Why It Complements arifOS |
|--------|--------------|--------------------------|
| **MCP kernel surface** | [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/getting-started/intro) | Keeps arifOS externally legible and standards-aligned while internal law stays custom. |
| **Practical MCP** | [FastMCP](https://gofastmcp.com/getting-started/welcome) | Good ergonomics for server/client tooling, while core remains transport-agnostic. |
| **Governance gateway** | [Agentic Control Plane](https://agenticcontrolplane.com/product) | Identity-verified governance, unified audit, gateway-first policy — reference for AAA. |
| **Durable workflows** | [Temporal](https://github.com/temporalio/temporal) | Crash-safe, replayable execution beyond prompt loops — for A-FORGE. |
| **Stateful graph orchestration** | [LangGraph](https://langchain-ai.github.io/langgraph/) | Graph-shaped plans, branching, human-review checkpoints — for MIND + A-FORGE. |
| **Temporal memory** | [Graphiti](https://github.com/getzep/graphiti) | Closest external analog to L5 memory substrate — for MEMORY organ. |
| **TypeScript operator plane** | [Mastra](https://github.com/mastra-ai/mastra) | MCP server support, context management, observability — for AAA cockpit + A-FORGE UX. |
| **Simple MCP multi-agent** | [PraisonAI MCP](https://docs.praison.ai/docs/mcp/mcp-server) | Fast examples for agent teams exposed as MCP — pattern reference, not ideology. |

---

## §11 — Agent-Specific Study Paths

### For `arifos` repo (kernel, law layer)
- Study MCP canonical docs + FastMCP for external compatibility, transport handling, auth boundaries, and MCP resource/tool semantics
- Study Temporal + LangGraph for durable execution patterns, retries, checkpoints, and human-review edges — then port concepts into your own governed pipeline instead of importing framework ideology
- Study Graphiti and GraphMemory survey work to sharpen L5 memory beyond ad hoc graph edges

### For `AAA` repo (control plane, cockpit)
- Study Mastra and OpenAI Agents SDK JS for operator ergonomics: tracing, guardrails, handoffs, dashboards, and developer experience
- Study Agentic Control Plane + GitHub agent control plane for the language and architecture of policy enforcement, approvals, and audit-ready routes

### For `A-FORGE` repo (execution shell)
- Study PraisonAI / CrewAI / Mastra examples for multi-agent decomposition — but keep their orchestration patterns subordinate to E7, F13, and your kernel
- Study DuraLang / Temporal patterns for safe self-modification pipelines where code changes are replayable, checkpointed, and reversible

### For NATS / mesh
- Use NATS examples only for transport mechanics; your actual subject taxonomy, envelope, and governance must stay arifOS-native
- Focus on publish/subscribe patterns, JetStream replay, durable consumers, and backpressure design

---

## §12 — Additional Repos (Arif's Research)

### Agent Orchestration

| Repo | URL | Why |
|------|-----|-----|
| **Mastra** | https://github.com/mastra-ai/mastra | TypeScript agent framework with MCP server support, context management, and observability. Strong reference for AAA/A-FORGE operator-side UX and tooling. |
| **PraisonAI** | https://docs.praison.ai/docs/mcp/mcp-server | Simple multi-agent MCP server patterns and MCP tool wrapping. Fast examples, not ideology. |
| **CrewAI (OSS)** | https://crewai.com/open-source | Role-based multi-agent decomposition patterns. Less aligned to your governance model, but useful for studying role definition. |
| **OpenAI Agents SDK JS** | https://github.com/openai/openai-agents-js | Guardrails, handoffs, tracing, and workflow observability patterns. Study to reimplement under arifOS law, not to adopt directly. |

---

## §13 — Consolidated Libraries by Language

### Python (Kernel + Organs + Mesh)

| Library | Purpose | Tier |
|---------|---------|------|
| **fastmcp** | MCP server/client ergonomics | Tier 1 — must use |
| **nats-py** | NATS/JetStream event mesh transport | Tier 1 — must use |
| **temporalio** | True durable workflow execution — use sparingly, only for high-value long-running workflows | Tier 1 — must ingest |
| **pydantic v2** | Typed schema enforcement around LiveKernelEnvelope and E7 contracts | Tier 1 — already in use |
| **graphiti-client** (or Graphiti SDK) | Temporal graph memory integration if you adopt Graphiti directly | Tier 1 — for MEMORY organ |
| **praisonai** | Fast MCP multi-agent wrapping — pattern reference | Tier 3 — comparative context |
| **lasio / segyio / welly** | GEOX well log + seismic I/O | Domain-specific — already in use |
| **numpy / scipy / matplotlib** | GEOX + WEALTH numerical computing | Domain-specific — already in use |
| **qdrant-client** | Vector DB for MEMORY organ | Already in use |
| **cryptography** | Ed25519 signing, hashing for ROOTKEY | Already in use |
| **prometheus-client** | Metrics export for AAA cockpit rendering | Tier 2 — useful to add |
| **structlog** | Structured logging for cleaner journalctl | Tier 2 — useful to add |

### TypeScript / Node.js (AAA, A-FORGE)

| Library | Purpose | Tier |
|---------|---------|------|
| **mastra** | AAA-facing operator tools, dashboards, MCP authoring, context plumbing | Tier 1 — must ingest |
| **@openai/agents** (or openai-agents-js) | Tracing/handoffs ideas — study patterns, don't adopt runtime | Tier 2 — pattern mining |
| **nats.js** (NATS TS client) | AAA A2A server + cockpit event subscriptions | Tier 1 — must use |
| **@modelcontextprotocol/sdk** | MCP client for AAA/A-FORGE if they need direct MCP access | Tier 2 — as needed |
| **react / vite / tailwindcss** | AAA cockpit frontend | Already in use |
| **ws** | WebSocket for A-FORGE terminal | Already in use |

### Infrastructure

| Tool | Purpose | Already? |
|------|---------|----------|
| **systemd** | Service management for all organs | ✅ |
| **caddy** | Reverse proxy for public endpoints | ✅ |
| **cloudflared** | Tunnel for arif-fazil.com | ✅ |
| **docker** | Graphiti, Qdrant, FalkorDB | ✅ |
| **nats-server** | Mesh backbone | ✅ |
| **prometheus + grafana** | Metrics + dashboards for AAA cockpit | ⚠️ Not deployed |

---

## §14 — Tiered Reading Order

### Tier 1: MUST INGEST FIRST

These are non-negotiable. Every forging agent reads these before touching code.

| # | Resource | What to Take | What to Leave |
|---|----------|-------------|---------------|
| 1 | **MCP docs + spec** | Protocol semantics, tool/resource/prompt surfaces, transport patterns, auth boundaries | Do not override arifOS-native transport (SSE + streamable HTTP) with third-party wrappers |
| 2 | **FastMCP** | Clean server/client ergonomics, decorator patterns, session management | Framework remains subordinate to kernel — arifOS wraps FastMCP, not the reverse |
| 3 | **Temporal** | Crash-safe replayable execution, checkpoint state persistence, retry with backoff | Do not import Temporal's workflow ideology wholesale — extract the durability pattern, reimplement under F1-F13 |
| 4 | **Graphiti** | Temporal knowledge graphs, historical truth retention, edge decay, retrieval under changing state | Memory governance (10-field envelope) stays arifOS — Graphiti is the storage layer, not the law |
| 5 | **Agentic Control Plane** | Identity-verified governance, gateway-first policy, unified audit, approval routing | Enterprise multi-tenancy and role-based access — replace with E7 autonomy ceiling + F13 sovereign veto |

### Tier 2: USEFUL PATTERN-MINING

Study these after Tier 1. Extract patterns. Do not import frameworks.

| # | Resource | Pattern to Steal | Ideology to Reject |
|---|----------|-----------------|-------------------|
| 6 | **LangGraph** | Graph-shaped agent plans, branching, checkpoint nodes, human-review edges | LangChain ecosystem lock-in, node-as-function paradigm (arifOS uses organ-as-server) |
| 7 | **Mastra** | TypeScript operator UX, MCP authoring, context plumbing, observability dashboard patterns | Framework-as-platform — AAA is the control plane, Mastra is reference material |
| 8 | **OpenAI Agents SDK** | Guardrails as decorators, handoff patterns, tracing spans, workflow observability | OpenAI runtime lock-in — reimplement patterns under arifOS, not inside OpenAI's agent loop |
| 9 | **NATS JetStream examples** | Publish/subscribe, durable consumers, JetStream replay, backpressure design | Subject taxonomy and governance envelope are arifOS-native — NATS is transport only |

### Tier 3: OPTIONAL COMPARATIVE CONTEXT

Read last. Useful for knowing what the world builds. Not for adopting.

| # | Resource | Why Read | Why Not Adopt |
|---|----------|---------|---------------|
| 10 | **PraisonAI** | Fast MCP multi-agent examples | Too simple for constitutional federation |
| 11 | **CrewAI** | Role-based multi-agent decomposition | No governance, no floors, no sovereign veto |
| 12 | **awesome-agents / awesome-mcp** | Discovery of what exists | Most of it is ungoverned — useful for awareness, not adoption |
| 13 | **EdenAGI / Argent OS / AgentOS** | "Personal AGI" framing examples | None have constitutional floors or MCP-native kernels |

---

## §15 — Explicit Instructions for Forging Agents

Feed this verbatim to A-FORGE, OpenClaw, Hermes, or any future forging agent:

> **PRIME DIRECTIVE:** You are a forging agent operating under the arifOS constitution. Your task is not to choose a framework. It is to **extract patterns** from external references and **reimplement them under arifOS law**.
>
> **Rules of engagement:**
>
> 1. **Protocol first.** Use MCP docs + spec as the external protocol truth. Every organ surface must be MCP-compliant. Every tool must have name, description, JSON schema. Internal transport (NATS) is arifOS-native; external surface (HTTP/SSE) is MCP-standard.
>
> 2. **Durability, not frameworks.** Use Temporal + LangGraph as references for durability and state machines, not as your constitution. The pattern to steal is: checkpoint state, survive crashes, resume from last checkpoint, retry with backoff. The framework to reject is: importing Temporal's entire workflow engine. Build the pattern natively.
>
> 3. **Memory is governed.** Use Graphiti as the graph memory reference. Every memory episode must carry the 10-field arifOS envelope (source, timestamp, confidence, scope, owner, expiry, revocation, contradiction, audit, consent). The storage layer (FalkorDB/Qdrant/Graphiti) is subordinate to the governance layer (arifOS MEMORY organ).
>
> 4. **Sovereignty over tenancy.** Use control-plane products (Agentic Control Plane, GitHub AI Controls) as reference for approvals, audit, and rate limiting. But replace enterprise multi-tenancy and role-based access with: E7 autonomy ceiling per action, F13 sovereign veto, F1-F13 floor enforcement.
>
> 5. **Language separation is architectural.**
>    - **Python** is the kernel law language (arifOS core, organs, mesh, MIND, MEMORY).
>    - **TypeScript** is the operator plane language (AAA cockpit, A-FORGE execution shell, agent UX).
>    - Never mix kernel logic into the operator plane. Never push governance into a frontend.
>
> 6. **Self-modification is governed.** A-FORGE can generate code, tests, and deployment artifacts — but every atomic/irreversible change must pass through E7 ceiling check, arifOS 888_JUDGE, and F13 sovereign seal. Study DuraLang/Temporal for safe self-modification pipelines where changes are replayable, checkpointed, and reversible.
>
> 7. **Study everything. Copy nothing.** External code is reference material, not dependency. Every pattern absorbed must be transformed through the arifOS constitutional lens before it touches the live system.

---

## §16 — Final Verdict (v1.2 — Complete)

Your forging agents now have a complete reference library:

- **35+ repos** across 6 capability bands + agent orchestration
- **3-tier reading order** with explicit "steal this / reject that" per resource
- **Agent-type routing** — which references go to arifOS, AAA, A-FORGE, or NATS
- **Best-fit table** — single best external reference per architectural layer
- **Consolidated libraries** — Python (kernel), TypeScript (operator plane), Infrastructure
- **Explicit forging instructions** — the 7 rules of engagement for any agent touching this library
- **7 prioritized forge tasks** with references

**The architecture principle:** A real AGI kernel does not come from a single repo. It emerges when agents understand how to combine 6 things — standard protocol, sovereign governance, durable execution, temporal memory, event mesh, and controlled self-modification — under one constitution.

arifOS already has the skeleton. These resources are not replacements. They are the external textbooks your forging agents should raid.

> *DITEMPA BUKAN DIBERI — Study everything. Copy nothing. Forge your own.*

> *A real AGI kernel will not come from a single repo. It emerges when your agents understand how to combine 6 things: standard protocol, sovereign governance, durable execution, temporal memory, event mesh, and controlled self-modification.*

---

## Addendum — What Was Forged This Session

This document caps a 6-forge session (2026-06-14, ~06:20–06:50 UTC):

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | **Personal AGI Trust Boundary** | `forge_work/ARIF_PERSONAL.md` | Awaiting sovereign review |
| 2 | **arifOS vs The World Contrast** | `forge_work/ARIFOS_CONTRAST.md` | Merged — Arif's external research + OpenClaw live audit |
| 3 | **AGI Kernel Reference Library** | `forge_work/AGI_KERNEL.md` | Merged — 35+ repos, 3 tiers, agent routing, instructions |

**Still pending (carry-forward):**
- ROOTKEY E1-E7 not deployed to live kernel (two-copy drift)
- Governance stream: 0 messages on NATS `arifos-governance`
- AAA cockpit not rendering live state
- All 3 search providers down (MiniMax, Tavily, arifOS MCP)
- AGI🦞 drift alert: build_commit 0f88747 ≠ live_commit 428f039 on arifOS kernel
