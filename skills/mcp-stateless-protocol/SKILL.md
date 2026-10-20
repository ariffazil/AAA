---
name: mcp-stateless-protocol
description: "Probe and connect MCP servers on the 2026-07-28 stateless wire format (MCP 2.0). Covers the exact header+envelope handshake (MCP-Protocol-Version, Mcp-Method, Mcp-Name, _meta io.modelcontextprotocol/* keys), the error taxonomy (-32020 HeaderMismatch, -32022 UnsupportedProtocolVersion, -32602 missing envelope keys), using stateless.mcpjam.com/mcp as a conformance test rig (13 fixture tools), and verifying whether any coding agent/client supports the latest MCP (SDK version + trial calls). Trigger: user asks which agents support the latest MCP, wants to connect an https MCP server, or an MCP endpoint rejects initialize with UnsupportedProtocolVersion."
---

# MCP Stateless Protocol (2026-07-28 wire format)

The MCP 2026-07-28 spec (RC May 21 2026, final July 28 2026) replaced sessionful Streamable-HTTP with a **stateless core**: no initialize round-trip, no session ID, no sticky sessions, routable on ordinary HTTP. Every request is self-contained. This skill covers probing such endpoints and testing client support. Verified live 2026-08-08 against stateless.mcpjam.com/mcp.

## 1. The handshake (exact recipe)

```bash
curl -sS -m 15 -X POST 'https://<host>/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -H 'Mcp-Method: tools/list' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'
```

- `tools/call` additionally requires `-H 'Mcp-Name: <tool>'` matching `params.name` (e.g. `-H 'Mcp-Name: echo'` with `"params":{"name":"echo","arguments":{...},"_meta":{...}}`).
- Required `_meta` envelope keys: `io.modelcontextprotocol/protocolVersion` + `io.modelcontextprotocol/clientCapabilities`. Optional: `io.modelcontextprotocol/clientInfo`.
- **NO `initialize` method.** Sending the legacy handshake (body `protocolVersion`) — or mixing it with a modern header — returns `-32020 HeaderMismatch`.
- Success responses carry `resultType: "complete"` and `_meta.io.modelcontextprotocol/serverInfo`.

## 2. Error taxonomy (the server tells you what it wants)

| Code | Name | Meaning |
|---|---|---|
| -32020 | HeaderMismatch | Headers and body disagree (legacy initialize body + modern header; missing Mcp-Name on tools/call) |
| -32021 | MissingRequiredClientCapability | Client didn't advertise a required capability |
| -32022 | UnsupportedProtocolVersion | Wrong/absent version — **read `data.supported`**, it lists exactly what the server accepts |
| -32602 | Invalid params | Missing required envelope keys — **read `data.envelope.missing`**, it names them |
| -32600 | Invalid Request | Body not a valid JSON-RPC message per this server's strict schema |

**Meta-rule: read `error.data` before retrying.** The first probe error usually contains `"supported":["2026-07-28"]` and later errors name the missing `_meta` keys. Do not guess shapes.

## 3. Reference test rig: stateless.mcpjam.com/mcp

MCPJam's stateless conformance server (`mcpjam-stateless` v0.3.1), Cloudflare-hosted, no auth. 13 fixture tools, one per protocol feature:

| Tool | Exercises |
|---|---|
| echo, get-weather, execute-sql, fail | basic calls, outputSchema validation, error paths |
| long-task | progress notifications (`_meta.progressToken`) |
| ask-name, confirm-launch, open-dashboard, summarize, list-client-roots, never-satisfied | MRTR: form mode, 2-round confirm, URL elicitation, sampling, roots/list, round-limit |
| trigger-notifications | list_changed / resources/updated subscriptions |
| run-task | Tasks extension (CreateTaskResult + tasks/get polling) |

Use it as the known-good target when testing whether any client/agent speaks the stateless wire format.

## 4. Verifying an agent's MCP support

1. Check the agent's MCP SDK: `pip show mcp` (Python — 1.x speaks ≤ 2025-11-25; 2026-07-28 needs ≥ 2.0), `npm ls -g @modelcontextprotocol/sdk`, or the app's package.json deps.
2. **SDK version is not the whole story** — an agent can implement the stateless transport itself (OpenClaw 2026.7.1-2 with SDK 1.29.0 works via custom code). A trial call beats version inference.
3. Trial: point the agent at `https://stateless.mcpjam.com/mcp`, run `echo` / `get-weather`, watch for `resultType:"complete"`. Failure = the agent's client speaks an older protocol revision.
4. Status on this box (2026-08-08 — re-probe, versions go stale): OpenClaw ✅ verified; Hermes (Python mcp 1.27.2) ❌; Claude Code 2.1.218, Codex 0.146.0, OpenCode 1.18.11, Kimi Code — installed, unverified.

   ORGAN STATUS UPDATE (2026-10-15, 333-AGI — live-probed):
   - **GEOX :8081 ✅ VERIFIED** — stateless era fully working. `resultType:'complete'`
     enforced at the era-bridge choke point for EVERY method (JSON + SSE) since
     commit 1c624842; deploy gate `make deploy-gate` live; contract
     tests/test_stateless_resulttype_contract.py 11/11. Public URL
     https://geox.arif-fazil.com/mcp strict-client ALL PASS (tools 27, resources 52, prompts 16).
   - **WEALTH :18082 ❌ STATEFUL-ONLY** — stateless envelope returns
     `-32000 SESSION_MISSING: Mcp-Session-Id header required`; no era bridge.
     Works via legacy initialize→session flow (Claude Code OK). Porting the GEOX
     era-bridge pattern is the known fix (backlog).
   - Federation organ index reconciliation: AAA CAPABILITY_INDEX.json + AGENT_SURFACE_MAP.yaml
     were advertising retired tool names against live surfaces — reconciled to live
     probes 2026-10-15. See eureka-2026-10-15-frozen-registry-stale-truth.

## 5. Pitfalls

- **`curl -sf` swallows error bodies.** Stateless servers answer 400 with a JSON-RPC error that IS the diagnosis. Use `-sS` / `-si` and read `error.data`.
- **Don't conclude "useless/demo" before trying the current-spec envelope.** 2026-08-08 case: 6 failed probes with legacy shapes produced a wrong "empty demo endpoint" verdict; the server was a fully functional 13-tool conformance rig reachable with the correct 2-header + envelope shape. The `data.supported` list was in the very first error — read it.
- Protocol versions `2025-03-26` / `2025-06-18` / `2025-11-25` are all legacy; only `2026-07-28` (and future) speak stateless. Older clients get -32022.
- Legacy-era servers sometimes dual-accept prefixes (e.g. `sct_v1|act_v1`); check each server's own `data.supported` rather than assuming.
- **FastMCP `stateless_http=True` is necessary but not sufficient.** The transport flag enables stateless mode, but you must also: (1) declare protocol "2026-07-28" in health/discovery endpoints, (2) append "2026-07-28" to the mcp SDK's `SUPPORTED_PROTOCOL_VERSIONS` list (it's not included by default in mcp 1.27.x), (3) remove any session-validation middleware that enforces `Mcp-Session-Id` headers. See `references/federation-sdk-readiness-audit-2026-08-11.md` for the exact per-organ checklist.
- **Session middleware removal is not just code deletion.** WELL had TWO session middlewares (parameter-level + header-level), GEOX has a global `_kernel_mcp_session_id` variable, A-FORGE has an active `sessionIdGenerator`. Each organ's session dependencies are different — grep for `session_id`, `Mcp-Session`, `SessionEnforcement`, `SessionValidation` before declaring stateless readiness.
- **Enforce era obligations at the choke point, never by method-name matching.** The 2026-10-15 GEOX defect: only tools/list carried resultType (outer middleware matched that one method); every other modern-era reply relayed verbatim by the era bridge → strict clients rejected ALL calls. Fix belongs inside the bridge where every era reply crosses. Regression-proofing = per-method contract test (both transports, both eras, legacy negative tests) + a live deploy gate that fails the deploy when the contract breaks. Law: eureka-2026-10-15-choke-point-protocol-law.
- **`'Unknown tool'` from a catalog/connector: probe the LIVE organ first.** The advertisement side (AAA CAPABILITY_INDEX, agent cards, DeepWiki) is often the stale side — an immutable registry protects integrity of record, not correctness of content. Reconcile from live probes, then re-freeze. Law: eureka-2026-10-15-frozen-registry-stale-truth.
- **Don't mistake dual-era negotiation for migration failure.** FastMCP 4.x correctly negotiates 2026-07-28 requests DOWN to 2025-11-25. See "Dual-Era MCP Negotiation" below.

## 6. Dual-Era MCP Negotiation (forged 2026-08-11)

**FastMCP 4.x correctly negotiates protocol version.** When a client requests `protocolVersion=2026-07-28` against a server that supports both eras, FastMCP 4 responds with `protocolVersion=2025-11-25` (the older supported version).

```bash
# Client requests 2026-07-28
curl -X POST http://server/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2026-07-28",...}}'

# Server responds with 2025-11-25 (negotiated down)
{"result":{"protocolVersion":"2025-11-25", ...}}
```

**This is correct behavior, NOT a failure.** The server is exercising dual-era support — accepting the modern client but serving via the legacy path. To force a 2026-07-28 response, the server must be upgraded to FastMCP 4 with explicit 2026-07-28 capability.

**Pitfall:** Don't treat the negotiated-down response as a migration failure. Verify by:
1. Server's `data.supported` array (if using stateless envelope) includes "2026-07-28"
2. `initialize` returns successfully with 2025-11-25 OR 2026-07-28
3. `tools/list` enumerates tools (works either way)

If all three pass, dual-era is working. If only 2025-11-25 is supported and you need 2026-07-28, that's a separate migration (see federation-sdk-readiness-audit).

## 7. Transport ≠ Authorization — 5-Layer Auth Model (forged 2026-08-11)

**Critical insight:** The session gate (`Mcp-Session-Id` header check) is Layer 1 of a 5-layer authorization model. Removing it for whitelisted tools does NOT compromise security:

| Layer | Mechanism | Stateless migration? |
|-------|-----------|---------------------|
| 1. Transport | `Mcp-Session-Id` header | **Removed** for whitelisted tools |
| 2. Task Context | `task_context` parameter (CONTEXT B) | Required, unchanged |
| 3. Lease | `lease_id` parameter (kernel-issued) | Required for mutations, unchanged |
| 4. Policy Gate | 5-layer (identity → server → tool → args → verdict) | Always enforced |
| 5. Receipt | `recordReceipt()` per call → VAULT999 | Always logged (F11) |

**Implication:** A-FORGE's STATELESS_TOOLS whitelist patch removes ONLY Layer 1. Mutation tools (forge_browser_*, forge_github_create_*, forge_postgres) remain callable without session continuity but still require `task_context` or `lease_id` for authorization.

**F1 AMANAH preserved** — session removal ≠ authorization removal.

**Verification:** After whitelist patch, mutation tools should:
- Accept calls without `Mcp-Session-Id` header ✅
- Still require `task_context` or `lease_id` argument ✅
- Produce `recordReceipt()` audit log entry ✅

If a mutation tool can be called WITHOUT `task_context` AND WITHOUT `lease_id`, the patch is **broken** — Layer 2/3 bypassed.

**Practical pattern** (A-FORGE `serve.ts`):

```typescript
const STATELESS_TOOLS = new Set([
  // ... pre-existing whitelist entries ...
  
  // Wave A: pure read-only tools, no auth params needed
  "forge_whoami",
  "forge_netdata_alarms",
  "forge_netdata_metrics",
  "forge_worktree",
  
  // Wave B: mutation tools — still require task_context or lease_id in handler
  "forge_browser_navigate",  // handler enforces task_context
  "forge_github_create_issue", // handler enforces lease_id
  // ...
]);

// Session gate (Layer 1)
if (!STATELESS_TOOLS.has(toolName)) {
  return error("SESSION_MISSING");  // Layer 1 enforcement
}

// For whitelisted tools, Layers 2-5 still enforce:
// - Layer 2: handler checks args.task_context
// - Layer 3: handler checks args.lease_id (mutations)
// - Layer 4: Policy Gate validates every call
// - Layer 5: recordReceipt() logs to VAULT999
```

## 6. Support files

| Path | Purpose |
|---|---|
| `references/mcp-stateless-probe-failure-2026-08-08.md` | Verbatim transcript of 6 failed probes + correct envelope shape |
| `references/gemini-docs-mcp-probe-2026-08-09.md` | Google's public Gemini Docs MCP server (gemini-api-docs-mcp.dev) — live probe results, install recipe for opencode/claude-code/codex, skills-vs-MCP comparison, pitfalls. Use when wiring Gemini documentation access into coding agents. |
| `references/federation-stateless-migration-2026-08-11.md` | **Federation migration state:** all 6 organs probed live, SDK versions, A-FORGE dual-port architecture, 4-phase migration plan. Reference for any "which organs are stateless?" question. |
| `references/federation-sdk-readiness-audit-2026-08-11.md` | **Per-organ SDK readiness audit:** exact FastMCP/SDK versions, `stateless_http` flag status, session-dependent code inventory, fix checklist per organ. Use when planning migration or answering "what needs to change?" |
| `../fastmcp-organ-staging-migration/SKILL.md` | **Staging migration pattern:** T1-tier sandbox workflow for upgrading Python MCP organs to FastMCP 4 + mcp SDK v2 without touching production. The 10-step pattern, 8-receipt suite, and rollback verification — verified against WELL (2026-08-11, 8/8 PASS). |

## 7. Federation architecture insight (2026-08-11)

**Transport ≠ Governance. Stateless MCP only solves transport, not identity/authority/governance/audit.**

This is like HTTP vs Constitution. The protocol becoming stateless is orthogonal to whether governance is centralized or federated.

### The 5 deployment options (evaluated 2026-08-11)

| Option | Pattern | Effort | Risk | Alignment | Score |
|--------|---------|--------|------|-----------|-------|
| 1. Multi-Door | Each organ has its own subdomain | 2/10 | 2/10 | 5/10 | 60 |
| 2. Single Door | Everything through arifOS | 8/10 | 6/10 | 9/10 | 60 |
| 3. Hybrid Federation | arifOS=governance, organs=execution | 4/10 | 3/10 | 8/10 | 76 |
| 4. Service Mesh | Envoy/Istio/mTLS | 10/10 | 8/10 | 6/10 | 20 |
| 5. APEX Registry | Discovery + direct routing | 5/10 | 2/10 | 10/10 | 80 |

**F13 Verdict (2026-08-11):** Option 3 now, evolve toward Option 5.

- **Hybrid Federation** (Option 3): arifOS provides identity/policy, organs execute directly. No bottleneck, constitutional control maintained.
- **APEX Registry** (Option 5): arifOS maintains canonical registry (tool→organ map), clients discover then connect directly. Closest to `Kernel governs, organs execute` doctrine.

### Migration phases (approved by F13)

```
Phase 0 (common prerequisite — all options need this):
  1. Verify Python SDK stateless support per organ
  2. Collapse A-FORGE dual-port (:7071 + :7072 → single port)
  3. Create canonical registry manifest (tool→organ map)

Phase 1 (~30 days): Stateless enable all organs
Phase 2 (~60 days): Hybrid Federation (arifOS=governance hub)
Phase 3 (~90 days): Registry-first discovery
```

### Registry as SOT first, automation later (F13 insight)

The registry does NOT need to be a platform. It can start as a simple YAML mapping:
```yaml
tool:
  geox.search:
    owner: GEOX
  wealth.portfolio:
    owner: WEALTH
```
Constitutional SOT appears in Phase 0. Registry automation appears in Phase 3. Doctrine before tooling.

### Current federation state (updated 2026-08-11)

**arifOS IS on 2026-07-28 spec.** Reference file was written before arifOS upgrade completed.

See `references/federation-stateless-migration-2026-08-11.md` for full live inventory.

<!-- SKILL-WITNESS-NOTE (auto, additive-only) -->
Witnessed reality moved this skill's selection to **ROUTE or MERGE**.
Scar signatures: 2026-09-30-f13-ask-h3-polarity-version-drift, SCAR-2026-09-12-phantom-cron-category-error
Do not treat this skill as neutral until the signatures are resolved.
<!-- /SKILL-WITNESS-NOTE -->
