---
name: audit-verification-protocol
description: Systematic verification of claims made by other agents about system state — containers, MCP servers, databases, deployments. When an agent (Hermes, ASI, etc.) presents audit results, verify each claim directly before accepting.
tags: [audit, verification, containers, MCP, devops, constitutional]
last_updated: 2026-04-29
---

# Audit Verification Protocol

## Trigger
- Another agent presents audit results claiming X is broken/broken/working
- A session summary claims certain verifications passed
- Someone reports container/filesystem state from an external analysis

## Principle
**Agents confabulate. Disks don't lie.** Always verify operational claims with direct shell commands. Do not trust agent summaries of what `docker ps`, `psql`, or file contents show — ask to see the output.

## Systematic Verification Checklist

### 1. Container Health
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>&1
```
Check: uptime, restart count (restart=N means N restarts — high is bad), healthy tag.

### 2. startup.sh Presence (don't trust agent word)
```bash
docker exec <container> sh -c 'ls -la /usr/local/bin/startup.sh /tmp/startup.sh 2>&1'
docker exec <container> sh -c 'find /app/ -name "startup.sh" 2>/dev/null'
```
Check: file exists, size, ownership, timestamp vs container build time.

### 3. MCP Server Port & Transport
```bash
# Check what ports are open inside container
docker exec <container> python3 -c "
import socket
for port in [3000, 8080, 8000, 8083]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('localhost', port))
        print(f'Port {port}: OPEN')
    except:
        print(f'Port {port}: CLOSED')
    s.close()
"

# Check Docker port bindings on host
docker inspect <container> --format '{{json .HostConfig.PortBindings}}' | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin),indent=2))"
```

### 4. MCP HTTP/SSE Transport (arifOS specific)
```bash
curl -s -N http://127.0.0.1:8080/mcp -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}'
```
**Critical:** arifOS MCP requires BOTH `application/json` AND `text/event-stream` in the Accept header. Without `text/event-stream`, returns `406 Not Acceptable`.

### 5. MCP Tools Verification (live JSON-RPC call)
```bash
curl -s -N http://127.0.0.1:8080/mcp -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}' \
  | python3 -c "
import sys, json
# SSE format: 'event: message\ndata: {...}'
for line in sys.stdin:
    line = line.rstrip()
    if line.startswith('data:'):
        d = json.loads(line[5:])
        tools = d.get('result',{}).get('tools',[])
        print(f'Tools: {len(tools)}')
        for t in tools[:5]:
            print(f'  - {t[\"name\"]}')
        break
"
```

### 6. MemoryEngine Import Test (inside container)
```bash
docker exec \
  -e PYTHONPATH=/tmp/pylibs:/app \
  -e DATABASE_URL="postgresql://arifos_admin:ArifPostgresVault2026!@postgres:5432/vault999" \
  -e QDRANT_URL="http://qdrant:6333" \
  -e OLLAMA_URL="http://ollama:11434" \
  <container> python3 -c "
from arifosmcp.memory_engine import MemoryEngine
import asyncio
async def test():
    engine = MemoryEngine()
    result = await engine.retrieve('test', tier='working')
    print(f'Results: {result}')
    print(f'Memories count: {len(result.get(\"memories\", []))}')
asyncio.run(test())
" 2>&1
```

### 7. Postgres Direct Query
```bash
docker exec postgres sh -c 'gosu postgres psql -U arifos_admin -d vault999 -c "SELECT COUNT(*) FROM memory_store;"' 2>&1
docker exec postgres sh -c 'gosu postgres psql -U arifos_admin -d vault999 -c "SELECT COUNT(*) as total, COUNT(DISTINCT text) as unique_texts FROM memory_store;"' 2>&1
```

### 8. Qdrant Collections
```bash
docker exec <container> python3 -c "
from qdrant_client import QdrantClient
c = QdrantClient(url='http://qdrant:6333')
cols = c.get_collections()
for col in cols.collections:
    info = c.get_collection(col.name)
    print(f'{col.name}: {info.points_count} points, vecsize={info.config.params.vectors.size}')
" 2>&1
```

### 9. tools.py asyncio Import Check
```bash
docker exec <container> sh -c 'grep -n "^import asyncio\|^from asyncio" /app/arifosmcp/runtime/tools.py | head -5'
docker exec <container> sh -c 'wc -l /app/arifosmcp/runtime/tools.py'
```

### 10. Git Repo Routing
```bash
# Check remote for any git repo
cd <repo_dir> && git remote -v
cd <repo_dir> && git log --oneline -3

# Check if AF-FORGE is a separate repo or part of arifOS
find /root -name ".git" -exec sh -c 'dir=$(dirname "{}"); cd "$dir" && echo "=== $(pwd) ===" && git remote -v 2>/dev/null | head-1' \; 2>/dev/null
```

## Anti-Pattern: Gmail Credential Retry
If Gmail auth fails and the app password was masked/redacted in logs:
- **Do NOT loop retry** — each attempt fails identically, risks account lockout
- **Do NOT guess the password** — masked values cannot be recovered from logs
- **Report failure** — offer Telegram as fallback delivery method
- **Fix:** User must provide the actual app password again (not in logs)

## Key Files
- arifOS MCP: `/root/arifOS/arifosmcp/`
- VPS deployment: `/srv/arifos/deployments/af-forge/`
- Email credentials: `/root/AAA/secrets/email.env`
- vault999-writer: port 5001, routes: `/health`, `/seal` (POST), `/pending` (GET), `/inspect/{id}`, `/ratify` (POST)
- Cloud vault table: `vault999` (not `vault_events`) in Supabase

## Lessons Learned This Session

### Perplexity cannot audit live MCP tools
Perplexity's fetch tool is GET-only. It cannot POST JSON-RPC to MCP servers, so it cannot call `tools/call`. When it reported "11 tools at 2026.04.07", it was:
- Hitting wrong subdomain: `arifosmcp.arif-fazil.com` (301 redirect) instead of `arifos.arif-fazil.com`
- Repeating old information from prior conversation, not discovering fresh state
- **Cannot** call `arif_vault_seal`, `arif_memory_recall`, or any other tool to verify runtime behavior
- Only way to verify MCP surface: direct curl POST with SSE transport from a capable agent

### Correct arifOS health endpoint
```
GET https://arifos.arif-fazil.com/health   ← canonical, returns 200
GET https://arifosmcp.arif-fazil.com/     ← 301 redirect to old path (avoid)
GET https://mcp.arif-fazil.com/           ← 301 redirect (by design, not an outage)
```

### SSE response parsing for MCP JSON-RPC
MCP SSE responses come as `data: {"jsonrpc":"2.0","result":{"content":[{"type":"text","text":"{...nested JSON...}"]}}`. 
Extract the nested tool result like this:
```bash
curl -s -X POST "https://arifos.arif-fazil.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"arif_session_init","arguments":{"mode":"init","actor_id":"arif"}},"id":1}' \
  | grep '"text"' \
  | python3 -c "
import sys, json, re
for line in sys.stdin:
    m = re.search(r'\"text\":\"(.*?)\"$', line)
    if m:
        inner = json.loads(m.group(1).replace('\\\\n','\n').replace('\\\\\"','\"'))
        print('nine_signal:', inner.get('nine_signal'))
        print('nine_signal_compliant:', inner.get('_nine_signal_compliant'))
        print('_violations:', inner.get('_violations'))
        break
"
```

### vault999-writer /pending 500 bug (known issue)
`GET /pending` returns `UndefinedColumnError: column "action_type" does not exist` — vault999-writer queries column `action_type` but local vault_seals table column is named `action`. Does NOT affect `/seal` (POST). Fix: patch the query or `ALTER TABLE vault_seals ADD COLUMN IF NOT EXISTS action_type TEXT;`.

### VAULT999 dual-write gap (CRITICAL — not wired)
vault999-writer container (`vault999-writer:5001`) has NO Supabase credentials. Inspect:
```bash
docker inspect vault999-writer --format '{{json .Config.Env}}' | python3 -c "
import json,sys
env = json.load(sys.stdin)
supabase = [e for e in env if 'SUPABASE' in e.upper()]
print('SUPABASE env vars in vault999-writer:', supabase if supabase else 'NONE — writes to LOCAL Postgres only')
"
```
Expected: `vault999-writer` should have `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` injected so it can dual-write to both local Postgres and Supabase cloud. Without these, cloud vault_seals table only gets seed data, not live seals.

### Supabase vault tables (correct table names)
- `vault999` — general KV store (seeded 2026-04-17/18, 21 rows)
- `vault_seals` — seal ledger (4 rows, seed data from 2026-04-17)
- `arifosmcp_memory_contract` — does NOT exist in Supabase (Perplexity's RLS claim was wrong)

### Verifying dual-write end-to-end
```bash
# Local seal
docker exec postgres sh -c 'gosu postgres psql -U arifos_admin -d vault999 -c "SELECT id, verdict, sealed_at FROM vault_seals ORDER BY sealed_at DESC LIMIT 3;"'

# Cloud seal (use vault_seals, not vault999)
curl -s "https://utbmmjmbolmuahwixjqc.supabase.co/rest/v1/vault_seals?select=id,verdict,sealed_at&order=sealed_at.desc&limit=3" \
  -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}"
```

## VAULT999 Ledger Audit Protocol

When auditing VAULT999, follow this exact sequence:

### Step 1 — Health endpoints
```bash
curl -s http://localhost:8100/health   # vault999 runtime
curl -s http://localhost:5001/health   # vault999-writer
```
Writer health response includes `vault_seals_count` (e.g., `"vault_seals_count": 6`).

### Step 2 — Read the writer's main.py (source of truth)
```bash
docker exec vault999-writer cat /app/main.py
```
This tells you: what endpoints exist, what DB role it uses, what the schema expects. Do NOT trust documentation — trust the code.

### Step 3 — Probe writer endpoints
```bash
# List pending cooling_queue records
docker exec vault999-writer python3 -c "
import urllib.request
req = urllib.request.Request('http://localhost:5001/pending', method='GET')
with urllib.request.urlopen(req, timeout=10) as r:
    print(r.read().decode())
"

# Inspect a specific seal
docker exec vault999-writer python3 -c "
import urllib.request, json
req = urllib.request.Request('http://localhost:5001/inspect/11', method='GET')
with urllib.request.urlopen(req, timeout=10) as r:
    print(json.dumps(json.loads(r.read()), indent=2))
"
```

### Step 4 — Direct Postgres (definitive)
```bash
# List all seals
docker exec postgres psql -U arifos_admin -d vault999 -c "SELECT id, action, verdict, epoch, witness FROM vault_seals ORDER BY id;"

# Check who has INSERT privilege on vault_seals
docker exec postgres psql -U arifos_admin -d vault999 -c "
SELECT grantor, grantee, privilege_type
FROM information_schema.table_privileges
WHERE table_name = 'vault_seals' AND privilege_type = 'INSERT';
"

# Count seals
docker exec postgres psql -U arifos_admin -d vault999 -c "SELECT COUNT(*) FROM vault_seals;"
```

### Step 5 — Check DB role the writer actually uses
```bash
docker exec vault999-writer env 2>/dev/null | grep VAULT999_DB
```
The writer's `main.py` may claim it uses `vault_writer_svc` in comments — verify actual role from env var.

### Common pitfalls
- **`curl` not in container** — use `python3 -c "import urllib.request..."` instead
- `vault_writer_svc` role mentioned in code comments but **never created** — writer falls back to `arifos_admin`
- "Supabase" in seal comments = Postgres backend, NOT a separate Supabase cloud instance

## Key Lessons From 2026-04-30 Session

### execute_code sandbox has corrupted env vars
The sandbox inherits shell env vars that may be garbled. Always read credentials from the actual file directly:
```bash
# WRONG (may get garbled password):
python3 -c "import os; print(os.environ.get('GMAIL_APP_PASSWORD'))"

# CORRECT:
python3 -c "
with open('/root/AAA/secrets/email.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line: k, v = line.split('=', 1); os.environ[k] = v
"
```

### "Supabase alignment" is just Postgres
VAULT999 uses Postgres as its backend. Seals mentioning "Supabase alignment" mean "we're using Postgres, same as Supabase would." No separate Supabase cloud instance is involved.

### vault_writer_svc role gap
The code intends a least-privilege DB role (`vault_writer_svc`) but it was never created. The writer connects as `arifos_admin` (superuser). This is a hardening item, not an emergency.

### vault999-writer is the only writer (confirmed)
No other container talks to the vault999 Postgres database directly. A-FORGE, arifOS, GEOX, WEALTH do NOT write to VAULT999.

## Rule
**Verify before trusting.** The most confidently wrong audits come from agents summarizing what they believe should be true, not what `psql` actually returns.
Agents with GET-only tools (Perplexity, browser fetch) cannot audit MCP servers that require POST + JSON-RPC.

## Git Repo Audit Protocol (Experiential — 2026-05-01)

### Anti-Pattern: Trusting `git ls-files` or working-directory listings
`git ls-files` shows what's in the **git index** (staged files), not what WOULD be committed from the working directory. If files are modified but not staged, `ls-files` may not show them. Searching the working directory with `find` or `ls` can be confused by symlinks pointing outside the repo.

### Ground-Truth Command: `git ls-tree`
```bash
# What IS in the last commit (definitive — what would be pushed)
git ls-tree -r HEAD --name-only | grep <pattern>

# Compare against working directory
git ls-files | grep <pattern>  # staged/indexed only
find . -name "<pattern>"       # working dir (confused by symlinks)
```

### Git Audit Checklist for Runtime Garbage
When auditing a repo for tracking errors:
1. `git ls-tree -r HEAD --name-only` — establish what commit contains (ground truth)
2. Look for: symlinks to runtime paths (`.openclaw`, `.hermes`), IDE session files (`.claude/sessions/`), backup dirs, large blob files
3. Check `.gitignore` — runtime dirs that ARE listed there but ARE tracked = broken ignore
4. Check `.gitignore` — runtime dirs that are NOT listed but SHOULD be

### Common Tracking Errors Found in arifOS
```
.openclaw          → symlink to /root/.openclaw (runtime, should be gitignored + untracked)
.opencode.json     → OpenClaw runtime state (should be gitignored + untracked)
.claude/sessions/ → session seals from IDE sessions (should be gitignored + untracked)
.gemini/           → Gemini settings (should be gitignored + untracked)
.cursor/           → Cursor settings (should be gitignored + untracked)
```

### To untrack without deleting files
```bash
git rm --cached <path>   # removes from index, file stays on disk
git rm -r --cached <dir> # recursive for directories
```
Then add to `.gitignore` and commit.

## Docker Network Topology Discovery (2026-05-01)

When containers can't reach each other, systematically map the network:

### Step 1 — Find all container network memberships
```bash
for container in $(docker ps --format '{{.Names}}'); do
  aliases=$(docker inspect "$container" --format '{{json .NetworkSettings.Networks}}' 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print([a for n in d.values() for a in n.get('Aliases',[])])" 2>/dev/null)
  if [ -n "$aliases" ]; then echo "$container: aliases=$aliases"; fi
done 2>/dev/null
```

### Step 2 — Get container IP on shared network
```bash
docker inspect <container> --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
# e.g. → 172.19.0.12
```

### Step 3 — Test connectivity from another container
```bash
# Use wget if curl is not available inside container
docker exec <source_container> wget -q -O- --timeout=5 http://<target_ip>:<port>/.well-known/agent-card.json
```

### Step 4 — Test DNS resolution from within container
```bash
docker exec <source_container> nslookup <target_hostname>
# NXDOMAIN = not resolvable in container's DNS
```

### Key lesson from AAA→Hermes bug
- `hermes-agent` is NOT in the filtered `aliases` output because it's on `arifos_core_network` not the default bridge
- AAA and Hermes BOTH on `arifos_core_network` (IPs 172.19.0.12 and 172.19.0.13)
- From host: `localhost:3002` works (Docker port mapping)
- From AAA container: must use `http://hermes-agent:3002` (Docker DNS)
- **Never assume `localhost:X` from host = reachable from inside container at `localhost:X`**

## OpenAI Key Verification Protocol (2026-04-30)
Two distinct errors mean different things — test in order:

```bash
# Step 1: Test auth (listing models — no inference cost)
curl -s -w "\nHTTP_STATUS:%{http_code}" https://api.openai.com/v1/models \
  -H "Authorization: Bearer $KEY"

# Step 2: Test quota (actual inference)
curl -s -w "\nHTTP_STATUS:%{http_code}" https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
```

| Result | Meaning |
|--------|---------|
| 200 on models + 200 on completions | Key fully valid |
| 200 on models + 429 on completions | Key valid, **account quota/grant exhausted** |
| 401 on models | Key is invalid or revoked |

**2026-04-30 finding:** Both `sk-svcacct-*` (service account) and `sk-proj-*` (project key) returned 200 on models but 429 on completions. Arif's $15 promo grant was exhausted. Ollama local models remain available at zero cost.
