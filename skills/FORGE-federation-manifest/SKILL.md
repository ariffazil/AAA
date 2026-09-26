---
id: FORGE-federation-manifest
name: FORGE-federation-manifest
version: 2.0.0-2026.09.17
description: "Inspect organ topology, MCP contracts, and attestation."
owner: A-FORGE
risk_tier: high
floor_scope: ['F1', 'F2', 'F4', 'F8', 'F11', 'F13']
autonomy_tier: T2
triggers:
  - "federation topology"
  - "organ registry"
  - "what organs exist"
  - "federation manifest"
  - "organ ports"
  - "which protocol version"
  - "federation drift"
  - "MCP conformance"
  - "protocol version check"
  - "deployment attestation"
  - "source deployed drift"
tags: [federation, topology, manifest, mcp, protocol, deployment, attestation]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Federation Manifest — arifOS Topology (v2.0)

The authoritative source of truth for federation organ identity, ports, capabilities, MCP protocol conformance, and deployment attestation state. Updated 2026-09-17 based on live federation probe.

**Architectural Equation (locked, empirically proven 2026-09-17):**
Stateless MCP transport + explicit stateful arifOS governance = stateless API + constitutional state machine. MCP forgets connections. arifOS remembers accountable constitutional chains.

---

## The Federation (Live State, 2026-09-17)

### Organ Registry

| Organ | Port | MCP Endpoint | Protocol Version | Tasks Cap | Status |
|---|---|---|---|---|---|
| **arifOS** | 8088 | /mcp | **2026-07-28** | yes | ✅ honest drift report |
| **WEALTH** | 18082 | /mcp | **2026-07-28** | yes | ✅ |
| **WELL** | 18083 | /mcp | **2025-11-25** ⚠️ | — | LAGGARD (manifest bumped, runtime pending) |
| **A-FORGE sense** | 7071 | /health | (A2A, not MCP) | n/a | ✅ source_commit: cbc25cb |
| **A-FORGE MCP** | 7072 | /mcp | (MCP gateway) | declared | ✅ 121 tools, 87 stateless |
| **arifFlow FQ** | 7073 | /health | (observation, not MCP) | n/a | ✅ formula qg.v0.3.1-vector |
| **AAA** | 3001 | /health | (A2A cockpit, not MCP) | n/a | ⚠️ stale drift strings (fixed upstream) |
| **HERMES** | 9900 | (dashboard) | (queue, not MCP) | n/a | ✅ |
| **otelcol** | 8888 | — | OpenTelemetry | — | ✅ |

### Seven-Layer Separation of Powers

| Stage | Tool | Constitutional Boundary |
|---|---|---|
| 000 | `arif_init` | Identity, actor binding, authority context |
| 111 | `arif_observe` | Evidence acquisition, reality registration |
| 333 | `arif_think` | Reasoning, hypotheses, plan formation |
| 444 | `arif_route` | Delegation to the appropriate organ |
| 555 | `arif_memory` | Governed recall, correction, persistence |
| 666 | `arif_judge` | Constitutional arbitration (HOLD/SEAL/VOID) |
| 777 | `arif_forge` | Controlled, bounded real-world change |
| 999 | `arif_seal` | Durable provenance, receipt issuance |

### Two-Lock Authority Model

| Layer | What it proves | Lifespan |
|---|---|---|
| OAuth access token | Client may access MCP resource under scopes | Short-lived |
| MCP `_meta` + headers | Request protocol semantics + client declaration | Single request |
| **ACT/SCT** | Which arifOS actor is bound, what constitutional authority applies | Explicit, renewable |
| **Constitutional chain** | Accountable sequence: observe → judge → execute | Mission lifetime |
| **Forge permit** | Specific mutation authorized within constraints | Single action/lease |
| **Seal receipt** | What verifiably occurred | Durable, append-only |

```
P_effective = P_oauth ∩ P_actor ∩ P_verdict ∩ P_constraint ∩ P_runtime
```

### Deployment Attestation State (2026-09-17)

| Source | Commit | Verified How |
|---|---|---|
| Working tree HEAD | `93526c15f` | `git rev-parse HEAD` |
| Deployed marker | `24f1a4f9c` | `cat /opt/arifos/releases/deployed-commit` |
| Kernel `source_commit` | `93526c15f` | Live MCP probe `arif_judge` |
| Kernel `deployed_commit` | `24f1a4f9c` | Live MCP probe `arif_judge` |
| Kernel `drift` | `true` | Live probe — **honest** |
| AAA `:3001/health` | `cc7e64f` / `44188e8` | **Stale** — different handler, needs fix |

**Verdict:** The membrane (:8088) is honest. AAA (:3001) lies with stale strings. AAA is the A2A cockpit facade, NOT on the kernel's critical path.

### MCP 2026-07-28 Conformance Matrix

| Feature | Spec | arifOS | Gap |
|---|---|---|---|
| Advertise 2026-07-28 in initialize | YES | YES | — |
| Capabilities.tasks | optional | YES | — |
| Capabilities.extensions.ui | optional | YES | — |
| Stateless HTTP transport | allowed | YES | — |
| `resultType` injection | required | YES | — |
| **`input_required` resultType** | required for MRTR | **MISSING** | kernel HOLD via JSON, not MCP wire |
| **Public discovery `server.json`** | recommended | **STALE** (says 2025-11-25) | needs bump |
| **OAuth PRM** | recommended | **MISSING** | F13 HOLD HARD |
| **RFC 9207 audience** | recommended | **MISSING** | F13 HOLD HARD |
| **MRTR bridge** | native fit | **MISSING** | F13 HOLD HARD |
| **MCP Tasks for arif_forge** | optional | **PARTIAL** | capability declared, handler not wrapped |
| Bearer + DPoP | allowed | YES | — |
| JSON Schema 2020-12 | allowed | YES | — |

### F13 HOLD Gates (from MCP migration musyawarah 2026-09-17)

| Gate | Phase | What | Why deferred |
|---|---|---|---|
| **G1** | Phase 0 | Deployment attestation — source/build/runtime provenance chain + CI verifier | CI activation is R0 irreversible; first forge canary needed |
| **G2** | Phase 2+3 | Auth surface — OAuth PRM, RFC 9207, MRTR bridge, MCP Tasks | Wire-visible to clients; OIDC rotation cost; F11 identity change |
| **G3** | Phase 3 | First forge post-remediation — reversible canary with full 000→999 audit | Past G1+G2 only; sovereign approval required |

---

## When to Use

- Initializing or updating federation topology for a new organ
- Checking MCP protocol conformance across federation members
- Diagnosing deployment drift (source vs deployed commit)
- Planning migration phases (must know current conformance state)
- Federated agent discovering which organs exist and their capabilities

## When NOT to Use

- Individual organ identity (DID) — use `did-web-identity`
- Runtime health probes — use organ `/health` endpoints
- MCP testing/validation — use `mcp-testing` (canonical, merged 2026-09-19) with MCPJam Inspector
- Model routing/fallback — use `litellm-proxy-triage`

## Constitutional Floor Alignment

| Floor | Application |
|---|---|
| F1 AMANAH | Manifest versioned; old manifests archived, never deleted |
| F2 TRUTH | Every declared tool must match live `tools/list` — drift = F2 violation |
| F4 CLARITY | One manifest, one topology — no stale copies |
| F8 GENIUS | Measure drift, don't narrate it. Live probes > hardcoded strings |
| F11 AUDIT | Manifest changes logged to VAULT999 with diff receipt |
| F13 SOVEREIGN | New organ registration requires F13 approval; auth surface changes are F13 HOLD HARD |

## Commands

```bash
# Live federation probe
curl -sS -X POST http://localhost:8088/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_judge","arguments":{"query":"federation status"}}}'

# Check protocol version across federation
for port in 8088 18082 18083 7072; do
  echo -n "Port $port: "
  curl -sS -X POST "http://localhost:$port/mcp" \
    -H 'Content-Type: application/json' \
    -H 'MCP-Protocol-Version: 2026-07-28' \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2026-07-28","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}' \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result',{}).get('protocolVersion','UNKNOWN'))" 2>/dev/null || echo "FAILED"
done

# Deployment drift check
echo "Source: $(git -C /root/arifOS rev-parse HEAD)"
echo "Deployed: $(cat /opt/arifos/releases/deployed-commit)"
echo "Kernel reports: $(curl -sS -X POST http://localhost:8088/mcp -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_judge","arguments":{"query":"software_release"}}}' | python3 -c "import sys,json; print(json.load(sys.stdin).get('result',{}).get('content',[{}])[0].get('text','')[:200])" 2>/dev/null)"
```

## Refusal Surface

- ❌ Declaring capabilities not verified by live probe
- ❌ Outdated port/transport info — must match systemd config
- ❌ Trusting hardcoded commit strings (use live probes, not `git log` alone)
- ❌ Publishing auth surface changes without F13 HOLD HARD approval
- ❌ Normalizing drift to "healthy" when it isn't

## Source of Truth

- Live probe beats hardcoded strings
- Deployed marker (`/opt/arifos/releases/deployed-commit`) beats git HEAD
- Kernel's own `software_release` block beats AAA facade
- This manifest beats any prior version — check `version` field
