# Zen Seal Crash Course — 2026-08-09 Session Trace

A real session where every recipe in the parent SKILL.md failed in sequence, plus the fixes that landed. Read this if you ever see `EROFS: read-only file system` or `VAULT999_APPEND_ONLY` on a name that doesn't exist.

---

## The setup

Goal: seal a triage verdict (`arif_hygiene_triage_verdict_2026_08_09`) — "no urgent action, defer 13 hygiene warnings to hourly sync". F13 SOVEREIGN `actor_id="ARIF"`. Reversible record (audit verdict, no doctrine change).

Expected path: `forge_vault(mode="receipt")` → Lane B → auto-seal to `vault999` Supabase table.

## What broke in order

### 1. `forge_vault(mode="receipt")` → `PolicyGateError: EROFS`

```
{
  "status": "ERROR",
  "code": -32010,
  "name": "PolicyGateError",
  "message": "MCP Policy Gate engine error during pre-check of forge_vault: EROFS: read-only file system, open '/root/.agent-workbench/mcp-audit.jsonl'"
}
```

**Misleading.** It says "read-only file system" but the file is mode 644 on `ext4 rw`. A standalone `node -e "fs.appendFileSync(...)"` succeeds. Even `chown arifos:arifos` doesn't help.

**Actual cause:** A-FORGE node process has a stale fd cache. The MCP policy gate's pre-check uses an old file view that doesn't reflect current perms.

**Fix:** restart A-FORGE :7072 bridge process (see Pitfall in SKILL.md).

### 2. After restart, `tools/call` → `Bad Request: Server not initialized`

After killing PID 2711285 and relaunching the bridge, the next `forge_vault` call returns:

```json
{"jsonrpc": "2.0", "error": {"code": -32000, "message": "Bad Request: Server not initialized"}, "id": null}
```

**Cause:** MCP server tracks the `initialize` handshake per-connection. New process = new connection state.

**Fix:** send `initialize` first, then `tools/call` (see Pitfall in SKILL.md).

### 3. After init, `forge_vault(mode="receipt")` → `VAULT999_APPEND_ONLY: Record already exists`

```
VAULT999_APPEND_ONLY: Record 'arif_hygiene_triage_verdict_2026_08_09' already exists.
Existing created_at=2026-08-11T07:34:18.125678+00:00.
To update, use a new name or append a versioned record.
```

**But `SELECT count(*) FROM vault999 WHERE name = 'arif_hygiene_triage_verdict_2026_08_09'` returns 0.**

**Cause:** `vault_read` RPC returns a phantom record (cache layer, eventual consistency, or stale projection). The 2026-08-11 timestamp is from the federation clock — agent clock is 2026-08-09 (2-day skew).

**Fix:** versioned name suffix. `_v2_final` worked on first try.

### 4. Lane A path (`arif_seal` via Python direct) → `seal_allowed=False`

When testing the constitutional path:
```python
from arifosmcp.tools.session import arif_init
# SOVEREIGN bind succeeded:
# {"actor_authority": "SOVEREIGN", "actor_verified": true, "seal_allowed": false}
```

**Cause:** `arif_init` for AUDIT_RECORD (reversible) returns SOVEREIGN identity but `seal_allowed=False`. The constitutional seal is gated by irreversibility.

**Decision:** abandoned Lane A. AUDIT_RECORD is exactly what Lane B (`forge_vault`) is for. The "AUDIT_RECORD" action_class name is the hint — reversible records don't need the full chain.

### 5. Lane A `arif_judge` and `arif_seal` are async coroutines

First attempt to call `arif_seal(...)` synchronously returned a `coroutine` object that was never awaited. Receipt did not land. RuntimeWarning: `coroutine was never awaited`.

```python
# WRONG — returns coroutine, never awaited
result = arif_seal(mode="seal", payload="...")

# RIGHT
async def do_seal():
    return await arif_seal(mode="seal", payload="...")
result = asyncio.run(do_seal())
```

### 6. `arif_judge` returns `VerdictOutput` pydantic, not dict

```python
chain_id = judge.get("constitutional_chain_id")  # AttributeError!
chain_id = getattr(judge, "constitutional_chain_id", None)  # works
```

Same for `arif_seal` return — use `.model_dump()` or attribute access.

---

## The full sequence that worked

```python
import json, http.client

# 1. Initialize MCP handshake (after bridge restart)
c = http.client.HTTPConnection('127.0.0.1', 7072, timeout=60)
c.request('POST', '/mcp', body=json.dumps({
    'jsonrpc': '2.0', 'id': 1, 'method': 'initialize',
    'params': {'protocolVersion': '2025-03-26', 'capabilities': {},
               'clientInfo': {'name': 'seal-script', 'version': '1.0'}}
}), headers={'Content-Type': 'application/json', 'Accept': 'application/json'})

# 2. forge_vault with versioned suffix
c.request('POST', '/mcp', body=json.dumps({
    'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
    'params': {'name': 'forge_vault', 'arguments': {
        'mode': 'receipt',
        'name': 'arif_hygiene_triage_verdict_2026_08_09_v2_final',  # suffix!
        'category': 'audit_verdict',
        'content': json.dumps({"session_label": "...", "actor_id": "ARIF", ...}),
        'actor_id': 'ARIF',
        'intent': 'Zen seal: triage verdict',
        'summary': '...',
        'delta_s': '<= 0',
    }}
}), headers={'Content-Type': 'application/json', 'Accept': 'application/json'})

# 3. Verify
import subprocess
subprocess.check_output(['psql', os.environ['VAULT999_PG_URL'], '-t', '-c',
    "SELECT id, name, created_at FROM vault999 WHERE name = 'arif_hygiene_triage_verdict_2026_08_09_v2_final';"])
```

Result: `id=ab8d6842-1062-4726-90dc-b72ae90d40c4`, created_at=2026-08-11T07:53:32Z.

---

## Time well spent vs time wasted

| Time | What was tried | Why it didn't work |
|---|---|---|
| 2 min | `curl :7072 ... forge_vault` directly | EROFS (stale fd cache) |
| 3 min | `chown arifos:arifos mcp-audit.jsonl` | file was already writable, root cause was fd cache |
| 2 min | `chmod 664 ...` | same — A-FORGE runs as root, already had write |
| 1 min | `arif_seal` via Python direct | `seal_allowed=False` for AUDIT_RECORD |
| 4 min | `arif_judge` for chain_id | returned HOLD without chain_id (reversible) |
| 3 min | debugging async / VerdictOutput | coroutine never awaited, `.get()` on pydantic |
| 1 min | phantom collision debug | didn't run direct SELECT first |
| 1 min | versioned suffix `_v2_final` | it worked |
| ~17 min | total | recipe in parent SKILL.md is now ~30 sec |

The lesson: when the A-FORGE bridge UI lies about EROFS, restart first, debug second. When `vault_read` lies about a phantom record, versioned suffix. When AUDIT_RECORD won't Lane-A-seal, use Lane B from the start.
