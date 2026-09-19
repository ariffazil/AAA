# Composio CLI Dual-Key Discovery

*Discovered 2026-08-25 — root cause of OAuth connection mismatch*

> **STATE (verified 2026-09-19): Key 2 below, and every command that reads it, are UNBUILT on
> this host.** `/root/.composio/` does not exist — no `composio` binary, no `user_data.json`,
> nothing named `composio` on PATH. What would have to exist: the binary from
> `curl -fsSL https://composio.dev/install | sh`, plus the `user_data.json` that
> `composio login` writes. Key 1 (the `ak_` key consumed by
> `/root/.config/mcp/composio-proxy.mjs`) is the only live half of this document today.

## The Problem

Social-mcp gateway returns "No connected account" for all Composio tool calls, even though OAuth connections exist in dashboard.composio.dev.

## Root Cause: Two API Keys

### Key 1: MCP Proxy Key (`ak_` prefix)
- **Location**: `/root/.secrets/kunci-root.env` as `COMPOSIO_API_KEY`
- **Used by**: `/root/.config/mcp/composio-proxy.mjs` (MCP stdio proxy)
- **Endpoint**: `https://backend.composio.dev/v3/mcp/{server_id}/mcp?user_id=arif-federation`
- **Problem**: Hardcoded `user_id=arif-federation` doesn't match actual OAuth connections
- **Symptom**: All tool calls return "No connected account found for user ID arif-federation"

### Key 2: CLI Key (`uak_` prefix)
- **Location**: `/root/.composio/user_data.json` as `api_key`
- **Used by**: `/root/.composio/composio` (CLI binary, 102MB)
- **Endpoint**: `https://backend.composio.dev/api/v1/` (v1 API)
- **Works**: Can list connections, execute tools, see OAuth accounts
- **Context**: Inherits logged-in user context from CLI session

## Discovery Commands

```bash
# 1. Check MCP proxy key
grep COMPOSIO_API_KEY /root/.secrets/kunci-root.env
# Output: export COMPOSIO_API_KEY="ak_..."

# 2. Check CLI key
cat /root/.composio/user_data.json | jq '.api_key'
# Output: "uak_..."

# 3. List connections via CLI (works)
/root/.composio/composio dev connected-accounts list

# 4. List toolkits via CLI (works)
/root/.composio/composio dev toolkits list
# Shows: Gmail (61 tools), Reddit (21 tools), etc.

# 5. Test MCP proxy (fails)
curl -s https://backend.composio.dev/v3/mcp/6e892839-a047-4611-8b1e-eea39b81a1c6/mcp?user_id=arif-federation \
  -H "x-api-key: $COMPOSIO_API_KEY"
# Returns: "No connected account"
```

## Why This Happens

1. OAuth connections are created via dashboard.composio.dev using the `uak_` key
2. Connections are bound to user IDs like `arifbfazil@gmail.com`
3. MCP proxy uses hardcoded `user_id=arif-federation` (doesn't exist in OAuth connections)
4. Proxy queries v3 API with wrong user_id → no connections found

## Fix Options

### Option A: Update MCP Proxy user_id
Edit `/root/.config/mcp/composio-proxy.mjs`:
```javascript
// Change from:
const USER_ID = "arif-federation";
// To:
const USER_ID = "arifbfazil@gmail.com";  // or whatever user_id owns the OAuth connections
```

**Pros**: Minimal change, keeps MCP architecture
**Cons**: Hardcoded user_id still fragile; need to verify which user_id owns connections

### Option B: Switch to CLI Subprocess
Change `ComposioClient.call_tool()` in `/root/social-mcp/src/server.py`:
```python
async def call_tool(self, tool_name: str, arguments: dict) -> dict:
    cmd = ["/root/.composio/composio", "execute", tool_name, "-d", json.dumps(arguments)]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={**os.environ, "COMPOSIO_API_KEY": os.environ.get("COMPOSIO_CLI_KEY", "")}
    )
    # Parse CLI output...
```

**Pros**: Inherits CLI session context, sees all connections
**Cons**: CLI subprocess slower than MCP; need to parse CLI output format

### Option C: Unify API Keys
Ensure both keys point to same user context. Requires:
1. Find which user_id owns OAuth connections: `/root/.composio/composio dev connected-accounts list --json`
2. Update MCP proxy to use that user_id
3. Or update dashboard to create connections under `arif-federation`

**Pros**: Clean architecture, single source of truth
**Cons**: Requires dashboard access, may need to re-authorize OAuth

## Verification After Fix

```bash
# 1. Test MCP proxy directly
node /root/.config/mcp/composio-proxy.mjs
# Should return: {"jsonrpc":"2.0","result":{"tools":[...]}}

# 2. Test social-mcp tool call
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"gmail_fetch_emails","arguments":{"query":"test"}}}'
# Should return: {"result":{"content":[{"type":"text","text":"..."}]}}

# 3. Check audit ledger
tail -1 /root/social-mcp/audit/ledger.jsonl | jq .
# Should show: "result_status":"success" (not "error")
```

## Lessons Learned

1. **Always verify which API key is in use** — Composio has multiple key formats (`ak_`, `uak_`) with different scopes
2. **MCP proxy user_id is hardcoded** — check `/root/.config/mcp/composio-proxy.mjs` for `USER_ID` constant
3. **CLI binary sees different context than MCP proxy** — they use different keys and user contexts
4. **OAuth connections are user-scoped** — connections created under one user_id are invisible to another
5. **Test both read and write paths** — "No connected account" can mask deeper auth issues

## Related Files

- `/root/.config/mcp/composio-proxy.mjs` — MCP stdio proxy (uses `ak_` key)
- `/root/.composio/composio` — CLI binary (uses `uak_` key)
- `/root/.composio/user_data.json` — CLI config with API key
- `/root/social-mcp/src/server.py` — social-mcp gateway (uses MCP proxy)
- `/root/social-mcp/audit/ledger.jsonl` — audit trail showing failures

## Next Steps

1. Determine which user_id owns OAuth connections
2. Choose fix option (A/B/C above)
3. Update code and test
4. Verify audit ledger shows successful tool calls
5. Document final architecture in main SKILL.md
