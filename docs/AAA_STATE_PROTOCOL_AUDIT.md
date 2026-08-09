# AAA State Protocol Audit — MCP · A2A · constitutional stack

> **Forged:** 2026-08-09 · F2 live probe on af-forge  
> **Doctrine:** Protocol = transport + contract over **time**. Governance decides truth.  
> **Rule:** Follow proper protocol **where multi-process / multi-agent / multi-version** applies.  
> Local monolith path (CLI on same VPS) remains valid least-power dial.

## 0. One-line doctrine (from ARIF / 888 reading)

```
Model thinks · Memory remembers · Tool acts · Protocol coordinates · Governance decides · Audit proves.
WHO DECIDES? → arifOS (888), not MCP, not A2A.
```

| Layer | What it is | What it is **not** |
|-------|------------|---------------------|
| **MCP** | AI ↔ tools/data plug standard | Not judgment |
| **A2A** | Agent ↔ agent interoperability | Not seal authority |
| **FastMCP** | Python framework for MCP servers | Not a second constitution |
| **ACT** (`act_v1.*`) | Session capability token | Not SPIFFE/HDP rename |
| **arifOS** | F1–F13 · judge · seal | Not a tool catalog |
| **AAA** | DISPLAY_ONLY catalog + A2A gateway | Not executor, not judge |
| **CALL_MAP** | How to dial | Not who you are (cards) |
| **STATE** | Institution readiness | Not warga passport |

---

## 1. When protocol is **mandatory** vs **optional**

| Situation | Protocol required? | Our path |
|-----------|-------------------|----------|
| One process, one agent, one machine, same owner | Optional (CLI/local) | `opencode run`, `hermes`, `openclaw agent` |
| Cross-organ tools (kernel, forge, earth, capital, well) | **MCP required** | Streamable HTTP `:port/mcp` |
| Cross-agent task routing (mesh) | **A2A required** | AAA `:3001` + agent cards |
| External peer / future version | **A2A + ACT + did:web** | After internal dial proven |
| Constitutional mutation / seal | **Kernel verbs + ACT + VAULT** | Never via AAA alone |
| Identity over time | **did:web + ACT** | Not SPIRE organ |

**Paradox held:** Single-owner today → CLI is enough for many tasks. Success over months → protocols become survival.

---

## 2. Live matrix (OBS 2026-08-09)

### 2.1 Health

| Port | Service | Health |
|------|---------|--------|
| 8088 | arifOS MCP | ✅ |
| 7071/7072 | A-FORGE API/MCP | ✅ |
| 7073 | arifFLOW | ✅ |
| 3001 | AAA A2A | ✅ |
| 8081 | GEOX MCP | ✅ |
| 18082 | WEALTH MCP | ✅ |
| 18083 | WELL MCP | ✅ |
| 18789 | OpenClaw GW | ✅ |
| 18089 | Hermes A2A listener | ✅ (no public agent-card yet) |

### 2.2 MCP (AI ↔ tool)

| Organ | Transport | `initialize` | Negotiated version | Tools (sample) | Verdict |
|-------|-----------|--------------|--------------------|----------------|---------|
| **arifOS** | Streamable HTTP `/mcp` | 200 | **2025-03-26** | 8 Holy verbs: init→seal | ✅ **FOLLOW** |
| **A-FORGE** | Streamable HTTP `/mcp` | 200 | **2025-11-25** | tools+resources+registration | ✅ **FOLLOW** (newer PV) |
| **GEOX** | Streamable HTTP `/mcp` | 200 | **2025-03-26** | tools/resources/prompts | ✅ **FOLLOW** |
| **WEALTH** | Streamable HTTP `/mcp` | 200 | **2025-03-26** | tools/resources/prompts | ✅ **FOLLOW** |
| **WELL** | Streamable HTTP `/mcp` | 200 | **2025-03-26** | tools/resources/prompts | ✅ **FOLLOW** |

**Must follow (MCP clients):**

1. JSON-RPC 2.0 body  
2. `initialize` before tools (session-aware servers)  
3. `Accept: application/json, text/event-stream` for Streamable HTTP  
4. Negotiate `protocolVersion` (do not assume single version)  
5. Tool names stable; ceilings: COMPUTE_ONLY / JUDGE_ONLY / EXECUTE_AFTER_SEAL / REFLECT_ONLY  

**FastMCP:** implementation choice for Python organs — not a separate wire protocol.

**Gap (MCP):** version **skew** arifOS/domain = `2025-03-26` vs A-FORGE = `2025-11-25`. Clients must accept both. Target: document minimum supported PV per organ; prefer streamable-HTTP 2026-07-28 era when all organs upgrade (not emergency).

### 2.3 A2A (agent ↔ agent)

| Check | Live | Spec expectation | Verdict |
|-------|------|------------------|---------|
| `/.well-known/agent-card.json` | 200 AAA | MUST publish Agent Card | ✅ |
| `/.well-known/agent.json` | 200 (alias) | MAY | ✅ |
| `protocolVersion` on card | **1.2** | A2A 1.0 family | ⚠️ label vs binding |
| `A2A-Version` header | **required** `1.0` | Service parameter | ✅ enforced |
| JSON-RPC methods | `tasks/send`, `message/send` | Send Message family | ✅ path present |
| Anonymous external task | **EMD_VALIDATION_BLOCKED** (W3&lt;0.3) | Security / governance | ✅ intentional |
| Hermes `:18089` agent-card | **404** | SHOULD for A2A servers | ❌ gap |
| Streaming / push | declared on card | capabilities | ⚠️ declare ≠ proven E2E |

**Must follow (A2A clients):**

```http
POST /a2a
A2A-Version: 1.0
Content-Type: application/json

{"jsonrpc":"2.0","id":1,"method":"tasks/send","params":{...}}
```

Plus: ACT / session when mutating; never treat AAA as seal authority.

**CALL_MAP example without `A2A-Version` is incomplete** — update callers.

### 2.4 Governance protocols (not MCP/A2A)

| Protocol | Wire / practice | Follow? |
|----------|-----------------|---------|
| **Holy 8 verbs** | MCP tools on :8088 | ✅ always for governed session |
| **ACT** (`act_v1.*`) | capability envelope | ✅ rename registry: ACT only |
| **did:web** | `did:web:arif-fazil.com` | ✅ identity |
| **F1–F13** | arif_judge | ✅ |
| **VAULT999** | append-only seal | ✅ Lane A seals |
| **STATE_READY** | `state-probe.sh` | ✅ institution |
| **CALL_MAP** | dial order | ✅ telephone |
| **3-layer cards** | identity/harness/binding | ✅ directory |
| **EMD / membrane** | gateway gates | ✅ external truth floor |
| **NATS** | event bus | ✅ where wired |
| **OpenTelemetry** | metrics | ⚠️ partial (Prometheus) |
| **CloudEvents** | envelopes | partial / organ-specific |

---

## 3. AAA **state** protocol stack (what AAA must obey)

```
┌─────────────────────────────────────────────────────────┐
│ L6  VAULT999 / OTel          truth & witness              │
│ L5  ACT + did:web            who may act                  │
│ L4  arifOS F1–F13            what is allowed              │
│ L3  A2A (AAA :3001)          agent ↔ agent routing        │
│ L2  MCP (organs)             agent ↔ tools                │
│ L1  CALL_MAP + cards         how + who (directory/phone)  │
│ L0  STATE_READY              institution standing         │
└─────────────────────────────────────────────────────────┘
         AAA owns L1 + L3 DISPLAY_ONLY
         AAA must NOT own L4/L6 decision or seal
```

**AAA state protocol (normative for control plane):**

1. **Probe before act** — `:port/health` + `state-probe`  
2. **Catalog via cards** — 3-layer; agentId + did:web (not SPIFFE primary)  
3. **Dial via CALL_MAP** — priority: local_cli → A2A → MCP → arif_route  
4. **A2A on :3001** — Agent Card well-known; `A2A-Version: 1.0`; JSON-RPC  
5. **MCP consume only for routing** — do not re-implement organ tools on AAA  
6. **DISPLAY_ONLY ceiling** — no execute, no judge, no seal  
7. **External tasks** — EMD / witness gates; no anonymous seal path  
8. **Identity names** — ACT · agentId · warga later (IDENTITY_NAMING_REGISTRY)

---

## 4. Per-surface “must follow” checklist

### Harnesses (OpenCode, Hermes, OpenClaw, Grok, …)

| Must | How |
|------|-----|
| MCP to organs | Official Streamable HTTP / stdio as configured; initialize handshake |
| A2A when mesh | Card discovery + `A2A-Version` + task methods |
| FED for models | OpenAI-compat `:4000` seat = WHICH, not WHO |
| ACT for governed tools | From arif_init / federation ritual |
| No self-seal | 888 path only |

### Organs (GEOX, WEALTH, WELL, A-FORGE, arifOS)

| Must | How |
|------|-----|
| MCP server correctness | tools/list, tools/call, ceiling in description |
| Health | `/health` |
| Authority ceiling | COMPUTE / JUDGE / EXECUTE / REFLECT |
| Optional A2A card | Well-known if they accept remote agent tasks |

### AAA specifically

| Must | Status |
|------|--------|
| Agent Card well-known | ✅ |
| A2A version gate | ✅ |
| Registry 3-layer | ✅ (state-probe) |
| CALL_MAP aligned with live ports | ✅ (refresh if drift) |
| A2A-Version in CALL_MAP examples | ❌ **fix docs** |
| Hermes A2A listener card | ❌ 404 |
| Full A2A task lifecycle E2E proof | ⚠️ blocked by EMD for anonymous — need authenticated dial test |

---

## 5. Gaps ranked (protocol debt only — not Phase E economy)

| P | Gap | Fix class | Tier |
|---|-----|-----------|------|
| **P0** | CALL_MAP A2A examples omit `A2A-Version: 1.0` | Doc + client templates | T1 |
| **P0** | MCP protocolVersion skew (03-26 vs 11-25) | Document + client negotiate | T1 |
| **P1** | Hermes A2A `:18089` missing agent-card well-known | Publish card or pointer to AAA | T1 |
| **P1** | Proven Hermes→OpenCode **internal** A2A dial with ACT | E2E test under auth | T1/T2 |
| **P2** | A2A method naming dual (`tasks/send` vs `message/send`) | Align to binding table | T1 |
| **P2** | PROTOCOL_CONFORMANCE “22 agents” stale vs 38 cards | Re-probe registry | T1 |
| **P3** | OTel full SDK | Observability | later |
| **HOLD** | IBCT/SPIRE/AIMS rename | Rejected (naming registry) | — |

---

## 6. What we **already** follow properly (do not “fix”)

- MCP JSON-RPC initialize + tools on core organs  
- Streamable HTTP on federation MCP doors  
- AAA well-known Agent Card  
- A2A version header enforcement  
- EMD membrane on external A2A (fails closed)  
- Holy 8 kernel tools surface  
- STATE_READY / CALL_MAP / 3-layer separation  
- DISPLAY_ONLY AAA ceiling  

---

## 7. Immediate actions (this audit)

1. Patch **CALL_MAP** A2A examples with `A2A-Version: 1.0`  
2. Keep MCP clients version-tolerant  
3. Next product proof: **authenticated** A2A dial Hermes→OpenCode (not anonymous)  
4. Do **not** invent PEER/HDP organs  

---

## 8. Verdict

| Domain | Conformance | Note |
|--------|-------------|------|
| **MCP (organs)** | **FOLLOWING** | Live initialize + tools; version skew documented |
| **A2A (AAA gateway)** | **PARTIAL → FOLLOWING core** | Card + version + JSON-RPC; external blocked by design; E2E auth dial not proven here |
| **AAA state protocol** | **FOLLOWING** | STATE_READY, DISPLAY_ONLY, catalog/telephone split |
| **Governance** | **FOLLOWING** | Protocol does not replace 888 |
| **Horizon standards (AIMS/HDP)** | **MAP ONLY** | Naming registry |

**PARTIAL-SEAL on “full ecosystem A2A purity”.**  
**SEAL on “use protocol where multi-agent/multi-process; governance owns truth.”**

Evidence: live curls 2026-08-09; MCP initialize results; A2A-Version + EMD behavior; PROTOCOL_MAP inventory.

DITEMPA BUKAN DIBERI.

## Architecture SEAL

See [`AAA_ABOVE_PROTOCOL.md`](./AAA_ABOVE_PROTOCOL.md) — protocol follows AAA state projection; AAA does not become a protocol.
