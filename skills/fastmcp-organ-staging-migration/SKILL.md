---
name: "fastmcp-organ-staging-migration"
description: "Migrate a Python MCP organ from FastMCP 3.x to FastMCP 4.x + mcp SDK v2 without touching production. The T1-tier staging pattern: isolated venv, parallel staging server on alternate port, 8-receipt test suite, rollback verification. Covers the WELL migration (2026-08-11, 8/8 PASS) and applies to WEALTH, GEOX, arifOS in Phase 1. Trigger: user asks to upgrade an organ to FastMCP 4, migrate to mcp SDK v2, or verify MCP 2026-07-28 stateless support on a Python organ."
tags: [mcp, fastmcp, migration, staging, python, fastmcp4, mcp-sdk-v2]
---

# FastMCP Organ Staging Migration

The T1-tier pattern for upgrading a Python MCP organ from FastMCP 3.x to FastMCP 4.x + mcp SDK v2 in complete isolation from production. Verified pattern from the WELL migration (2026-08-11, 8/8 PASS, 3.25 hours end-to-end).

## Why Staging, Not Direct Production Upgrade

1. **FastMCP 4 is beta** (4.0.0b2 as of 2026-08-11). GA ETA ~Sep 2026. Beta bugs reach staging first.
2. **mcp SDK v2 has breaking changes** — method renames (`_check_accept_headers` → `_validate_accept_header`), signature changes (async `(self, request, scope, send)`).
3. **Organ-specific session middleware** — each Python organ implements its own F1 AMANAH session validation. FastMCP 4 doesn't replace this; you have to audit and adjust per organ.
4. **Production MUST stay untouched** until 8/8 receipts are green.

## The 10-Step Pattern

### Step 1: Production venv backup (F1 AMANAH)

```bash
# Backup production venv with timestamp
mv /root/<ORGAN>/.venv /root/<ORGAN>/.venv.bak.$(date +%Y%m%d)
# This creates: /root/WELL/.venv.bak.20260811 (example)
```

**Critical:** Keep the backup until staging is proven green AND promoted to production (or rolled back entirely).

### Step 2: Isolated staging venv

```bash
# Clone to a NEW staging venv name (don't reuse .venv)
ln -s /root/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 \
      /root/<ORGAN>/.venv.staging/bin/python  # if venv existed

# Or create fresh
python3.12 -m venv /root/<ORGAN>/.venv.staging
```

**Pattern:** `.venv.staging/` next to `.venv` (or `.venv.bak.<ts>/`). Never overwrite production venv.

### Step 3: Install FastMCP 4 + mcp SDK v2

```bash
/root/<ORGAN>/.venv.staging/bin/pip install --pre "fastmcp[tasks]>=4.0.0b2,<5.0.0"
/root/<ORGAN>/.venv.staging/bin/pip install "mcp>=2.0.0,<3.0.0"
# Plus all the organ's other deps from pyproject.toml
```

**Verify:**
```bash
.venv.staging/bin/pip show fastmcp | grep Version   # should show 4.0.0b2
.venv.staging/bin/pip show mcp | grep Version      # should show 2.0.0
```

**Pitfall:** `pip index versions fastmcp` hides pre-releases. Use `--pre` flag or query PyPI directly:
```bash
pip index versions fastmcp --pre
# or
curl -s https://pypi.org/pypi/fastmcp/json | python3 -c "
import json,sys
d = json.load(sys.stdin)
print(sorted([v for v in d['releases'] if 'b' in v or 'rc' in v])[-5:])
"
```

### Step 4: Create staging server file

```bash
# Copy production server.py to server.staging.py
cp /root/<ORGAN>/server.py /root/<ORGAN>/server.staging.py
```

**Three patches typically needed in server.staging.py:**

#### Patch A: TasksExtension registration (FastMCP 4 requires explicit)

```python
# server.staging.py — near top, after FastMCP import
try:
    from fastmcp_tasks import TasksExtension
    mcp.add_extension(TasksExtension())
except ImportError:
    pass
```

Tasks were in FastMCP core in 3.x. In 4.x, they're a separate `fastmcp-tasks` package.

#### Patch B: Accept header async signature change

In 3.x:
```python
def _check_accept_headers(self, request): ...  # sync
```

In 4.x:
```python
async def _validate_accept_header(self, request, scope, send): ...  # async, 3 args
```

Any monkey-patch of the old method must update to the new async signature or it raises `TypeError: takes 2 positional arguments but 4 given`.

#### Patch C: Session middleware _EXEMPT_TOOLS expansion

For organs with application-level session middleware (WELL has `WellSessionValidationMiddleware`, GEOX has `_kernel_mcp_session_id` variable, A-FORGE has STATELESS_TOOLS whitelist):

```python
# Before:
_EXEMPT_TOOLS: frozenset[str] = frozenset({"well_health_check"})

# After (staging only):
_EXEMPT_TOOLS: frozenset[str] = frozenset({
    "well_health_check",
    "well_validate_vitality",       # NEW — read-only, stateless-safe
    "well_assess_homeostasis",      # NEW — read-only, stateless-safe
})
```

**Critical:** This patch is in server.staging.py ONLY. Never merge into server.py until FastMCP 4 GA + production trial.

### Step 5: Port isolation

```bash
# Production: :18083 (WELL)
# Staging:   :28083 (port + 10000 — easy to remember, no collision)

# If server.py hardcodes port, override via env var
export WELL_STAGING_PORT=28083
export HOST=127.0.0.1
```

If the production server.py doesn't already have an env override, add it to server.staging.py:
```python
port = int(os.environ.get(f"{ORGAN.upper()}_STAGING_PORT", 28083))
mcp.run(transport="http", host="127.0.0.1", port=port)
```

### Step 6: Start staging server (background)

```bash
# Use venv.staging + server.staging.py
cd /root/<ORGAN>
.venv.staging/bin/python server.staging.py > /tmp/<organ>-staging.log 2>&1 &

# Verify it's listening
sleep 5
ss -tlnp 2>/dev/null | grep <STAGING_PORT>
```

**Pitfall:** server.staging.py may exit silently due to import errors. Check the log:
```bash
tail -20 /tmp/<organ>-staging.log
# Common: "[transport] module 'well_mcp.transport' has no attribute 'register_transport'"
# This is non-fatal — server still starts, but some compat stubs are missing.
```

### Step 7: Run the 8-receipt test suite

| # | Test | What to verify | PASS criteria |
|---|------|----------------|---------------|
| 1 | server/discover (2026-07-28) | Initialize with modern protocol header | protocolVersion returned (any era acceptable; FastMCP 4 negotiates back to 2025-11-25 if 2026-07-28 not supported) |
| 2 | tools/list | List tools without session | Tool count > 0, tool names returned |
| 3 | tools/call stateless | Call a known-exempt tool without session_id | Result returned, no SESSION_MISSING error |
| 4 | read-only tool 1 | First core read-only tool | Real data returned |
| 5 | read-only tool 2 | Second core read-only tool | Real data returned |
| 6 | ACT-gated tool | Try mutation without session/ACT | SESSION_MISSING or unauthorized error (must be rejected) |
| 7 | trace_id propagation | Send W3C traceparent header | Header accepted (no 400 error), optionally logged |
| 8 | rollback | Kill staging process, verify prod survives | Prod health unchanged before/after kill |

**Sample test command:**
```bash
curl -s -X POST http://127.0.0.1:28083/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'tools: {len(d.get(\"result\",{}).get(\"tools\",[]))}')"
```

### Step 8: Verify production untouched

```bash
# BEFORE staging tests:
curl -sf http://127.0.0.1:18083/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'PROD: tool_count={d[\"tool_count\"]} status={d[\"status\"]}')"

# AFTER staging tests (must match):
curl -sf http://127.0.0.1:18083/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'PROD: tool_count={d[\"tool_count\"]} status={d[\"status\"]}')"
```

If values differ: STOP. Something went wrong. Do not promote.

### Step 9: Rollback verification (Test 8)

```bash
STAGING_PID=$(pgrep -f "server.staging.py")
kill $STAGING_PID
sleep 2

# Verify prod still works
curl -sf http://127.0.0.1:18083/health | python3 -c "..."

# Verify staging is dead
curl -sf --max-time 2 http://127.0.0.1:28083/health  # should fail
```

### Step 10: Document the receipt

Save to `/root/forge_work/<date>-<organ>-staging/<ORGAN>-STAGING-RECEIPT.md` with:
- Date, sovereign, curator
- Stack versions (FastMCP 4.0.0b2, mcp 2.0.0, Python 3.12)
- 8/8 test results table
- Critical findings (dual-era negotiation, session middleware origin, etc.)
- Patches applied (TasksExtension, accept header, _EXEMPT_TOOLS)
- F13 sovereign decision pending

## Constitutional Compliance

| Floor | Compliance |
|-------|------------|
| F1 AMANAH | ✅ Production venv backed up before any mutation |
| F2 TRUTH | ✅ Live probe receipts, not assumptions |
| F4 CLARITY | ✅ Single staging instance, alternate port, no ambiguity |
| F7 HUMILITY | ✅ Organs may have known-degraded status — investigate, don't ignore |
| F11 AUDITABILITY | ✅ Full receipt trail, 8 tests, rollback verified |
| F13 SOVEREIGN | ✅ Production untouched, F13 ratification before promotion |

## Pitfalls

### Pitfall 1: Wrong pip index for pre-releases

`pip index versions fastmcp` returns stable versions only. Use `--pre`:
```bash
pip index versions fastmcp --pre  # shows 4.0.0b2, 4.0.0b1, etc.
```

### Pitfall 2: Server exits silently

Import errors during startup may not fail the process. Always check the log:
```bash
tail -20 /tmp/<organ>-staging.log
# Look for: "Failed to register ...", "AttributeError", "ImportError"
```

Non-fatal errors (like `well_mcp.transport.register_transport` missing) still allow server start but indicate incompatibility.

### Pitfall 3: SESSION_MISSING from application middleware, not framework

WELL returns SESSION_MISSING because of its own `WellSessionValidationMiddleware`, NOT because FastMCP 4 requires sessions. Test 6 (ACT-gated tool) confirms the gate works. Tests 4-5 confirm stateless works for exempt tools.

**Pattern:** when session errors appear, read the source. Most session middleware is application-level (organ-specific), not framework-level.

### Pitfall 4: Opencode CLI `-p` is `--password`, not `--prompt`

If spawning opencode/kimi code via CLI:
```bash
# WRONG — -p interpreted as password, prompt ignored
opencode run -p "mission text" ...

# RIGHT — pipe via stdin
cat /tmp/mission.md | opencode run --auto --dir /root --title "..."
```

### Pitfall 5: Test 3 may report "Unknown tool"

If `_EXEMPT_TOOLS` doesn't include a tool, the middleware still blocks. But if the tool name itself doesn't exist in the staging server (e.g., `well_health_check` was renamed), Test 3 returns "Unknown tool" — NOT a session error.

**Rule:** always check that the tool you test with is in `tools/list` (Test 2) before testing call (Test 3).

### Pitfall 6: Session ID extraction from curl -i headers is fragile

When extracting `Mcp-Session-Id` from curl -i output:
```bash
# WRONG — grep matches Content-Type header substring too:
SID=$(curl -s -i ... | grep -i "mcp-session-id" | head -1 | cut -d: -f2)
# Result: "Content-Type,Mcp-Session-Id,MCP-Protocol..." (wrong)

# RIGHT — match only the session header line:
SID=$(curl -s -i ... | grep -i "^mcp-session-id:" | head -1 | cut -d: -f2 | tr -d ' \r\n')
```
The first pattern also matches attribute values in other headers. Always anchor with `^` and clean whitespace with `tr`.

### Pitfall 7: MCP "Server not initialized" means missing handshake

When tools/call returns "Server not initialized" or "Bad Request", the MCP protocol requires `initialize` first. Even for stateless tools:
```bash
# 1. Initialize (creates session context)
curl -s -i ... -d '{"method":"initialize","params":{...}}'
# 2. Extract session ID
# 3. Call tool with header: mcp-session-id: <SID>
```

### Pitfall 8: Tailscale still advertises dead ports

When port 7072 was retired on A-FORGE, Tailscale kept listening on `100.64.0.2:7072` forwarding to nothing. Same can happen for staging ports. Verify with:
```bash
ss -tlnp | grep <STAGING_PORT>  # should show your python process
```

If only `tailscaled` shows, the local service isn't actually listening.

## Migration Order (Verified 2026-08-11)

Per F13 sovereign directive (Arif):

```
WELL ✅ 8/8 PASS (first Python organ verified)
  → WEALTH (3-4 days, similar pattern)
  → GEOX (3-4 days, may have different session middleware)
  → arifOS (1 day, already FastMCP 3.4.6, closest to target state)
```

Each organ: copy the 10-step pattern. Estimate per organ: 3-4 hours end-to-end.

### Pitfall 9: Reality-first audit — probe live before diagnosing from config

When investigating port/service health, config files can be stale. A-FORGE's `mcp.arif-fazil.com` was diagnosed as "routing to dead :7072" from Caddyfile grep — but live probes showed it correctly routes to :8088 (arifOS kernel). The Caddyfile had old redirect references but the actual `reverse_proxy` block was correct.

**Rule:** Always verify with live curl BEFORE proposing fixes. The triad:
1. `ss -tlnp | grep <PORT>` — what's actually listening
2. `curl <URL>/health` — does it respond
3. `systemctl status <SERVICE>` — is the service active

Config files are evidence, not truth. Live probes are truth.

### Pitfall 10: A-FORGE has a different (lighter) migration pattern than WELL

For A-FORGE (Node.js, MCP SDK v2 already), Wave migration is simpler than Python organ migration:

**A-FORGE Wave pattern (different from WELL staging):**
1. Audit tool handler bodies for mutations and session reads
2. Classify: Wave A (stateless-ready, audit-only writes), Wave B (mutations with task_context/lease_id auth), Wave C (stateful), Wave D (long-running)
3. For Wave A/B: add tool names to `STATELESS_TOOLS` set in `src/interfaces/mcp/serve.ts`
4. Build: `npm run build && node scripts/copy-handwritten-js.mjs`
5. Restart: `systemctl restart a-forge`
6. Verify: `tools/list` shows the tool is reachable; call without session_id returns non-SESSION_MISSING result

**Key insight:** A-FORGE tools that accept `task_context` (CONTEXT B - trusted agent authority) or `lease_id` (kernel-issued lease) DON'T NEED session continuity. The session gate is a transport-layer check, not an authorization check. Removing the session gate preserves authorization.

**Wave discovery:** Many "session-required" tools in A-FORGE were never actually session-dependent. The whitelist expansion (47 → 67 tools) was a transport-layer change that increased stateless surface by ~40%.

## When NOT to Use
- **Non-Python MCP organs** — A-FORGE is Node.js, already on MCP SDK v2. No migration needed.
- **FastMCP 4.0.0 GA** — when it ships, this pattern becomes simpler (no pre-release, no _EXEMPT_TOOLS expansion needed since GA fixes the dual-era negotiation).

## Reference Receipts

- `references/well-staging-receipt-2026-08-11.md` — full WELL migration receipt (8/8 PASS, 3.25 hours, all patches documented)
- ``references/`` — A-FORGE Wave A+B migration methodology (lighter pattern, 20 tools moved to stateless, transport-layer insight)

## Reference Pattern Comparison

| Aspect | WELL (Python) | A-FORGE (Node) |
|--------|---------------|----------------|
| Stack upgrade | FastMCP 3.x → 4.0.0b2 | Already on MCP SDK v2 |
| Effort | 3.25 hours | ~15 minutes |
| Patch location | `server.staging.py` (staging only) | `src/interfaces/mcp/serve.ts` (production) |
| Whitelist mechanism | `_EXEMPT_TOOLS` (middleware-level) | `STATELESS_TOOLS` (transport-level) |
| Risk | MEDIUM (beta framework) | MEDIUM (auth duplication removal) |
| Auth preserved | ✅ task_context unchanged | ✅ task_context + lease_id + policy_gate unchanged |


<!-- dead-pointer sweep 2026-10-23: artifacts that could not be located were replaced with the references/ directory; see audit JSON for the missing basenames. -->
