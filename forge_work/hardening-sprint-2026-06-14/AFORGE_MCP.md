# 04 — A-FORGE Direct MCP Surface

**Hardening Item:** #4 of 8
**Status:** SPEC (design phase)
**Author:** OPENCLAW
**Session:** hardening-sprint-2026-06-14
**Reversibility:** READ-ONLY design doc. No live system touched.
**Epoch:** 2026-06-14T12:50Z

---

## §0 — Current State

### What exists (source, not compiled)

A-FORGE has a full MCP server in TypeScript at `/root/A-FORGE/src/interfaces/mcp/`:

```
src/interfaces/mcp/
├── core.ts          — MCP server + FloorEnforcer wrapper
├── server.ts        — Streamable HTTP transport
├── client.ts        — MCP client for cross-organ calls
├── proxyTools.ts    — 12 proxy tools (filesystem, git, docker, postgres, memory, github)
├── forgeTools.ts    — 11 forge tools (identity, lease, registry, shell, log, job)
├── resources.ts     — MCP resources
├── telemetry.ts     — Telemetry hooks
├── serve.ts         — Entry point
├── cli.ts           — CLI interface
└── stdio.ts         — Stdio transport
```

### Defined tools (48 total in source)

**Forge identity/lease tools (11):**
```
forge_agent_register    — Register agent identity
forge_agent_status      — Check agent identity
forge_agent_list        — List all agents
forge_lease_request     — Request bounded authority lease
forge_lease_status      — Check lease state
forge_lease_revoke      — Revoke a lease
forge_registry_status   — Tool registry
forge_shell_dryrun      — Preview shell command
forge_log_tail          — Tail system logs
forge_job_submit        — Submit background job
forge_job_status        — Check job status
```

**Proxy filesystem tools (6):**
```
forge_filesystem_read   — Read file
forge_filesystem_write  — Write file
forge_filesystem_glob   — Glob files
forge_filesystem_grep   — Grep files
forge_filesystem_stat   — File stat
```

**Proxy git tools (4):**
```
forge_git_status        — Git status
forge_git_diff          — Git diff
forge_git_log           — Git log
forge_git_commit        — Git commit
```

**Proxy docker tools (4):**
```
forge_docker_ps         — Docker ps
forge_docker_logs       — Docker logs
forge_docker_exec       — Docker exec
forge_docker_images     — Docker images
```

**Cross-organ tools (3):**
```
arif_session_init       — arifOS session
arif_health_check       — arifOS health
arif_sense_observe      — arifOS sense
arif_mind_reason        — arifOS mind
arif_heart_critique     — arifOS heart
arif_judge_deliberate   — arifOS judge
forge_pipeline          — A-FORGE pipeline
```

### Live state (compiled, running)

```
Endpoint: http://127.0.0.1:7071/mcp
Status:   SINGLE-SESSION (pre-initialized by main server at startup)
Issue:    External agents cannot get fresh MCP session
          "Server already initialized" error
          Mcp-Session-Id header required but no session issuance endpoint

Available HTTP endpoints:
  /health        → 200  (service health)
  /mcp           → 400  (needs session, single-session mode)
  /contract      → 200  (capability manifest)
  /api/federation-probe → 200  (all 9 organs up, GREEN)
  /api/repo-steward/* → 200  (code hygiene)
```

### The build gap

```
Source:  /root/A-FORGE/src/interfaces/mcp/  →  48 tools defined
Dist:    /root/A-FORGE/dist/src/mcp/       →  EMPTY (not compiled)
```

The MCP transport is wired in server.js directly (line 93-114), not from the mcp/ build directory. Tools register at server startup through the monolithic server.js, but the MCP session management is single-session.

---

## §1 — The Gap

### What's missing

1. **Multi-session MCP**: Current transport is single-session (main server pre-initializes)
2. **Dedicated MCP endpoint**: No separate MCP process/port for external agents
3. **Tool discovery**: `tools/list` returns 0 tools (session mismatch)
4. **Compiled dist**: `dist/src/mcp/` is empty — tools defined but not separately buildable

### Desired state

```
External agent (OPENCLAW)
    │
    ├── arifOS MCP (port 8088) ← 13 tools, currently broken (identity gap)
    ├── A-FORGE MCP (port 7071) ← 48 tools SHOULD be callable here
    ├── GEOX MCP (port 18081) ← 37 tools, working
    ├── WEALTH MCP (port 18082) ← 20 tools, working
    └── WELL MCP (port 18083) ← 18 tools, working
```

---

## §2 — Fix Options

### Option A: Enable multi-session on existing /mcp (FASTEST)

1. Modify `server.ts` to use `StreamableHTTPServerTransport` with session management
2. Allow external clients to initialize fresh MCP sessions
3. Each session gets its own tool surface
4. FloorEnforcer still gates every call

**Risk:** Low (config change, no new process)
**Time:** ~2 hours

### Option B: Dedicated MCP process on separate port (CLEANEST)

1. Build `dist/src/mcp/cli.js` (`npm run build`)
2. Run `node dist/src/mcp/cli.js serve --transport http --port 7072`
3. Expose as separate systemd service `a-forge-mcp.service`
4. All 48 forge tools available at `http://127.0.0.1:7072/mcp`

**Risk:** Medium (new service, new port, needs firewall/nginx/caddy)
**Time:** ~1 day

### Option C: Add A-FORGE as OpenClaw MCP connector (INTEGRATED)

1. Add A-FORGE MCP as a connected MCP server in OpenClaw gateway config
2. Tools surface through existing `arifos__` namespace or new `forge__` namespace
3. Single unified tool surface for OPENCLAW

**Risk:** Low (config change only)
**Time:** ~2 hours
**Prerequisite:** Option A or B must be done first (A-FORGE must accept multi-session)

---

## §3 — Recommended: Option B + Option C

1. **Build and deploy** A-FORGE MCP on dedicated port 7072
2. **Connect** to OpenClaw gateway as `forge__*` namespace
3. **Result:** OPENCLAW can call all 48 forge tools directly

```yaml
# OpenClaw gateway config addition
mcp:
  - name: "forge"
    url: "http://127.0.0.1:7072/mcp"
    namespace: "forge__"
```

---

## §4 — Verified Live State (2026-06-14)

| Check | Result |
|-------|--------|
| A-FORGE process | ✅ Running (PID 2286585, 47MB RSS, 25min uptime) |
| /health | ✅ 200, healthy, authority_ceiling: 777_FORGE |
| /contract | ✅ 200, capabilities enumerated |
| /api/federation-probe | ✅ 200, all 9 organs GREEN |
| /api/repo-steward | ✅ 200, 6 repos dirty, 47 uncommitted changes total |
| /mcp | ⚠️ Single-session, tools inaccessible to external agents |
| dist/build | ❌ dist/src/mcp/ empty, needs `npm run build` |

---

**Signed:** OPENCLAW · 2026-06-14T12:50Z
**Next:** Submit for Arif review. After seal → Option B (build + deploy dedicated MCP process).
