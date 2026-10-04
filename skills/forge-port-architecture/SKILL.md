---
name: forge-port-architecture
id: forge-port-architecture
version: 1.0.0
description: 'Federation port architecture — single-port vs dual-port patterns, Caddy routing, systemd unit mapping, and the stateless MCP migration. USE WHEN: diagnosing why a port is dead, understanding organ routing, planning MCP upgrades, "why is port X failing", "how does Caddy route to organs".'
owner: A-FORGE
risk_tier: low
floor_scope: [F1, F2, F4, F11]
autonomy_tier: T1
tags: [infrastructure, caddy, mcp, ports, systemd, stateless]
---

# Port Architecture — Federation Routing & MCP Patterns

**Diagnose, understand, and fix port/routing issues across the arifOS federation.**

## When to Use
- "Why is port X failing?"
- "How does traffic reach organ Y from the public internet?"
- "Why does A-FORGE have two ports?"
- Planning stateless MCP migration
- Fixing Caddy reverse proxy misconfiguration
- Diagnosing systemd unit vs binary port conflicts

## The Federation Port Map (2026-08-11 truth)

```
PUBLIC INTERNET
       │
  Cloudflare Tunnel
       │
  Caddy (80/443)
       │
       ├── arifos.arif-fazil.com  ──→ :8088  (arifOS kernel)
       ├── mcp.arif-fazil.com     ──→ :7071  (A-FORGE Sense+MCP)
       ├── geox.arif-fazil.com    ──→ :8081  (GEOX)
       ├── wealth.arif-fazil.com  ──→ :18082 (WEALTH)
       ├── wellness.arif-fazil.com──→ :18083 (WELL)
       ├── aaa.arif-fazil.com     ──→ :3001  (AAA control plane)
       └── /999/flow              ──→ :7073  (arifFlow)
```

## Core Organs (systemd bare-metal)

| Organ | Port | systemd unit | Process | Public subdomain |
|---|---|---|---|---|
| arifOS | 8088 | `arifos.service` | Python (FastMCP) | arifos.arif-fazil.com |
| A-FORGE | 7071 | `a-forge.service` | Node.js (Express+MCP) | mcp.arif-fazil.com |
| GEOX | 8081 | `geox-mcp.service` | Python (FastMCP) | geox.arif-fazil.com |
| WEALTH | 18082 | `wealth-organ.service` | Python (FastMCP) | wealth.arif-fazil.com |
| WELL | 18083 | `well.service` | Python (FastMCP) | wellness.arif-fazil.com |
| AAA | 3001 | `aaa-a2a.service` | Node.js (Vite+React) | aaa.arif-fazil.com |
| arifFlow | 7073 | `arifflow.service` | Node.js | (internal only) |

## The Single-Port Pattern (arifOS — correct)

```
Python process (FastMCP)
  Binds: 127.0.0.1:8088
  Serves: /health + /mcp + /api/* + /gate/check
  ONE process, ONE port, MANY domains
```

This is the target pattern. Simple. Low entropy.

## The Dual-Port Pitfall (A-FORGE — diagnosed 2026-08-11)

**Problem:** A-FORGE `server.js` mounts BOTH Sense API and MCP on the SAME Express app.
But Caddy historically routed `/mcp` to :7072 while the code listens on :7071.
A dead service `a-forge-mcp-test.service` tries to start the same binary on 7072 — always crashes.

```
server.js = SINGLE process, SINGLE listen (AF_FORGE_PORT)
  ├── /health  ✅ on :7071
  ├── /mcp     ✅ CODE EXISTS on :7071
  └── /sense   ✅ on :7071

BUT Caddy said:
  /mcp → :7072    ← WRONG (dead port)
  /health → :7071 ← correct

Fix: Point Caddy mcp.arif-fazil.com/mcp* → 127.0.0.1:7071
Fix: Delete a-forge-mcp-test.service (dead, was never needed)
```

### Why did it break?

Historical baggage. MCP was added to A-FORGE later. Someone assumed it needed a separate
port and created a second systemd service — but the code only reads `AF_FORGE_PORT`, not
`AF_FORGE_MCP_PORT`. The second service was always dead.

## Diagnostic Pattern: "Why is port X failing?"

```bash
# Step 1: Who listens on this port?
ss -tlnp | grep <port>

# Step 2: What systemd unit claims it?
systemctl list-units --type=service | grep -i <organ>

# Step 3: Read the unit file
cat /etc/systemd/system/<unit>.service | grep -E "ExecStart|PORT|Environment"

# Step 4: Does the binary actually support dual-port?
grep -n "listen\|PORT" /path/to/server.js

# Step 5: Does Caddy route to the right port?
grep -A5 "<subdomain>" /etc/caddy/Caddyfile | grep reverse_proxy

# Step 6: Verify the fix
curl -sf http://127.0.0.1:<port>/health | jq .
```

### Common failure mode

Two systemd services start the same binary with different PORT env vars,
but the binary only reads one port variable. Second service always crashes.

**Check:** `ExecStart` in both unit files. If same binary path → merge into one service.

## Stateless MCP Migration (2026-07-28 Spec)

> Full checklist: `references/stateless-mcp-migration.md`

The 2026-07-28 spec removes all protocol-level session state. No handshake, no `Mcp-Session-Id`,
no server-side session DB. Every request is self-contained.

**What to remove from existing servers:**

```javascript
// Session ID injection middleware — DELETE
if (!req.headers["mcp-session-id"]) {
  req.headers["mcp-session-id"] = randomUUID();
}

// Session generator in transport config — DELETE
sessionIdGenerator: () => randomUUID()
```

**What to add:**

```javascript
// Read inline metadata from every request
const meta = req.body?._meta;
const version = meta?.protocolVersion; // "2026-07-28"

// New routing headers (for gateway inspection without JSON parsing)
// Mcp-Method: "tools/call"
// Mcp-Name: "forge_shell"
```

**Infrastructure benefits:**
- No Redis for session storage
- Standard round-robin load balancing (no sticky sessions)
- Scale to zero on serverless platforms

## A-FORGE STATELESS_TOOLS Whitelist Pattern (forged 2026-08-11)

**The actual migration mechanism for Wave A/B on A-FORGE.** Don't rebuild the server — extend the whitelist.

In `/root/A-FORGE/src/interfaces/mcp/serve.ts`:

```typescript
const STATELESS_TOOLS = new Set([
  // ... pre-existing 47 whitelist entries ...
  
  // ── Wave A (2026-08-11) — Pure OBSERVE, audit-only write via recordReceipt ──
  "forge_whoami",
  "forge_netdata_alarms",
  "forge_netdata_metrics",
  "forge_minimax_search",
  "forge_worktree",
  
  // ── Wave B (2026-08-11) — Mutation tools with task_context auth ──────────────
  // Browser tools: each calls a playwright/puppeteer session owned by A-FORGE,
  //   not by the MCP caller. Mutation is on the browser page, not on the caller's session.
  // GitHub tools: accept lease_id for kernel-level authorization (already designed).
  // Postgres/Docker/Git: proxy to local services, task_context provides authority.
  "forge_browser_navigate",
  "forge_browser_click",
  "forge_browser_type",
  "forge_browser_screenshot",
  "forge_browser_extract_text",
  "forge_browser_evaluate_js",
  "forge_github_create_or_update_file",
  "forge_github_create_issue",
  "forge_postgres",
  "forge_docker",
  "forge_git",
  "forge_docsgpt",
  "forge_wealth",
  "forge_well",
  "forge_proxy_call",
]);
```

**The session gate logic (serve.ts:890-895):**
```typescript
if (!STATELESS_TOOLS.has(toolName)) {
  const msg = `Tool "${toolName}" requires session ownership...`;
  return error; // SESSION_MISSING
}
```

**Migration = single edit, no logic change.** Build, restart, done.

**Verifying whitelist extraction** (important gotcha — forged 2026-08-11):

```python
# WRONG — matches commented-out tool names, inflates whitelist
whitelist = set(re.findall(r'"([a-z_][a-z0-9_]+)"', block))

# RIGHT — only active entries (no comments)
for line in src_lines:
    m = re.match(r'\s*"([a-z_][a-z0-9_]+)"\s*,?\s*$', line)
    if m: whitelist.add(m.group(1))
```

**Impact:** The wrong regex catches ~67 entries (including comments), making the diff look like 67 session tools. The correct extraction yields 47 active whitelist entries — revealing only 20 true session-required tools. This 47→67 vs 47→20 distinction is critical for accurate Wave classification.

## Transport ≠ Authorization (5-Layer Auth Model, forged 2026-08-11)

**Critical insight from Wave B patch:** Removing the session gate did NOT remove authorization. The federation has 5 separate authorization layers:

| Layer | Mechanism | Purpose | Removed in stateless migration? |
|-------|-----------|---------|-------------------------------|
| 1. Transport | `Mcp-Session-Id` header | Stateless connection gate | **YES** (for whitelisted tools) |
| 2. Task Context | `task_context` parameter (CONTEXT B) | Trusted agent authority | NO — still required |
| 3. Lease | `lease_id` parameter | Kernel-issued lease for mutations | NO — still required |
| 4. Policy Gate | 5-layer (identity → server → tool → args → verdict) | Authorization decision | NO — still enforced |
| 5. Receipt | `recordReceipt()` per call | F11 audit log | NO — every call logged |

**The whitelist patch ONLY removes Layer 1.** Layers 2-5 still enforce authorization. Mutation tools are callable without session continuity, but each tool still verifies its own auth via `task_context` or `lease_id`.

**F1 AMANAH preserved** — mutation tools cannot be called without explicit authorization parameters.

## Production Isolation Pattern (WELL staging reference, forged 2026-08-11)

For testing Python organ migrations without touching production:

```bash
# 1. F1 AMANAH backup
mv /root/WELL/.venv /root/WELL/.venv.bak.20260811TxxxxxxZ/

# 2. Create staging venv (isolated, separate from prod)
python3.12 -m venv /root/WELL/.venv.staging/

# 3. Install new stack in staging only
.venv.staging/bin/pip install --pre "fastmcp[tasks]==4.0.0b2" "mcp==2.0.0"

# 4. Copy prod server.py, modify for staging port
cp /root/WELL/server.py /root/WELL/server.staging.py
# Add at top: WELL_STAGING_PORT = 28083  (prod stays on 18083)

# 5. Start staging on dedicated port
.venv.staging/bin/python /root/WELL/server.staging.py &

# 6. Run 8-receipt test matrix (see forge-mcp-testing skill)

# 7. Verify production untouched
curl http://127.0.0.1:18083/health  # must still work

# 8. Rollback (kill staging, restore prod venv)
kill <staging_pid>
mv /root/WELL/.venv.staging /root/WELL/.venv.staging.dead
mv /root/WELL/.venv.bak.20260811TxxxxxxZ /root/WELL/.venv
```

**Proven:** WELL 8/8 PASS on FastMCP 4.0.0b2 + mcp SDK 2.0.0 on `:28083`. Production `:18083` unchanged.

> Full staging recipe (10 steps, 5 pitfalls, per-organ timing): `references/well-staging-isolation-2026-08-11.md`
> GRANITE vs WATER annotation doctrine for federation config YAMLs: `references/granite-water-config-yaml.md`

## arifOS Auth Gate Pattern

All domain organs (GEOX, WEALTH, WELL) authenticate through arifOS before serving MCP:

```
Client → mcp.geox.arif-fazil.com/mcp
       ↓
Caddy forward_auth → :8088/gate/check
       ↓ (X-Gate-Verdict: ALLOW)
Caddy reverse_proxy → :8081 (GEOX MCP)
```

arifOS :8088 is both the constitutional kernel AND the auth gateway for all organs.
If :8088 is down, ALL organ MCP doors are locked.

## Python Port Resolution Helpers (federation_ports.py)

When building Python code that needs organ ports, **never hardcode them**. Use the canonical resolver at `/root/HERMES/scripts/federation_ports.py` (or equivalent in your organ).

### Resolution chain (highest priority first)

```
1. os.environ["{ORGAN}_PORT"]        e.g. ARIFOS_PORT=9999
2. os.environ["FED_{ORGAN}_PORT"]    e.g. FED_GEOX_PORT=7777
3. /root/AAA/federation/organs.yaml  (canonical SOT — read via PyYAML)
4. Hardcoded _DEFAULTS fallback table
```

### Key API surface

```python
from scripts.federation_ports import resolve_port, url_for, url_for_organ

# Resolve a single port (env → SOT → fallback)
port = resolve_port("ARIFOS")         # 8088
port = resolve_port("geox")           # 8081 (case-insensitive, hyphens → underscores)

# Build a full URL
url = url_for("GEOX", "/health")      # "http://127.0.0.1:8081/health"
url = url_for("GEOX", "/health", scheme="https", host="geox.arif-fazil.com")

# Lazy module-level constants (re-evaluate per call — env changes propagate)
from scripts.federation_ports import ARIFOS_URL, GEOX_URL
print(ARIFOS_URL())   # "http://127.0.0.1:8088"
print(ARIFOS_URL())   # re-evaluates, so ARIFOS_PORT env override works
```

### Design decisions

| Decision | Rationale |
|---|---|
| Read `organs.yaml` directly (PyYAML), not a JSON registry | Eliminates sync step. SOT is always current. No stale intermediate file. |
| Lazy lambdas for module constants | `_mk("ARIFOS")` returns `lambda: url_for("ARIFOS")`. Constants re-evaluate on each call, so env var changes propagate without `invalidate_cache()`. |
| `invalidate_cache()` for hot-reload | After mutating `organs.yaml` at runtime, call this to clear the PyYAML cache. |
| Case-insensitive organ names | `resolve_port("arifos")` and `resolve_port("ARIFOS")` both work. Hyphens normalized to underscores. |

### Pitfalls

1. **Don't import and cache at module load time for values you want to be overridable.** If you do `ARIFOS_PORT = resolve_port("ARIFOS")` at import, it freezes the value. Use the lazy `_mk()` pattern instead.
2. **`FED_GEOX_PORT` has LOWER priority than `GEOX_PORT`.** The bare `{ORGAN}_PORT` always wins. Only use the `FED_` prefix when you want a federation-level override that doesn't clobber a specific organ's override.
3. **SOT lookup iterates the `components[]` list — O(n).** Fine for ~29 organs. For hot paths, cache the result and use `invalidate_cache()` only when the YAML changes.

## Pitfalls

1. **Don't trust AGENTS.md port tables blindly.** `ss -tlnp` + `systemctl status` is truth.
2. **Same binary, two services = always broken.** Check ExecStart paths before assuming dual-port works.
3. **Caddy routes can point to dead ports.** Always verify the target port has a listener.
4. **Tailscale proxies ports too.** `ss -tlnp` shows `tailscaled` on forwarded ports — don't confuse with actual listeners.
5. **Session injection hacks break with stateless MCP.** Remove `Mcp-Session-Id` middleware entirely when upgrading.
