# Memory Subsystem Health Probe

Full probe recipe for the 6-layer memory landscape. Run in parallel where possible.

## L1/L2 — Redis (ephemeral + session)

```bash
# Connectivity + memory
redis-cli ping
redis-cli info memory | grep -E 'used_memory_human|maxmemory_human|mem_fragmentation_ratio'

# Key inventory by namespace (one-liner)
for p in sess flow cache task aaa:federation:memory:L1 aaa:federation:memory:L4 aaa:federation:memory:L6; do
  n=$(redis-cli KEYS "${p}*" 2>/dev/null | wc -l)
  [ "$n" -gt 0 ] && echo "$p: $n keys"
done
```

**Interpretation:**
- PONG = alive. Anything else = dead.
- `mem_fragmentation_ratio` > 2.0 = high fragmentation (3.0+ is concerning but not critical if used_memory is small).
- `maxmemory_human: 0B` = no eviction limit set (default unlimited — fine for dev, needs review for prod).

## L3 — Qdrant (fuzzy similarity / vector store)

```bash
curl -sf http://127.0.0.1:6333/health
curl -sf http://127.0.0.1:6333/collections | python3 -m json.tool
```

**Expected collections (as of 2026-08):**
`arif_evidence`, `arifos_constitution`, `arifos_memory`, `arifos_precedent`, `arifos_session_memory`, `arifos_vault_canon`, `arifos_vault_ephemeral`, `arifos_vault_quarantine`, `arifos_vault_sacred`

**Interpretation:**
- Empty `collections[]` = service up but no data (possible init failure).
- Missing expected collection = schema drift, not necessarily broken.

## L4 — PostgreSQL / Supabase (structured domain tables)

Postgres runs inside a **Docker container** (`postgres:16-alpine`), not as native systemd. There is no `/var/run/postgresql/` socket. Connection is TCP-only via `127.0.0.1:5432`.

```bash
# Step 0: Confirm container exists (if not, Postgres is genuinely down — not "just slow")
docker ps --filter "name=postgres" --format "{{.Names}} {{.Status}} {{.Ports}}"

# Step 1: Discover which env vars actually hold PG creds (names are NOT what you'd guess)
grep -iE 'postgres|arifos_db|pg_' /root/.secrets/kunci-mas.env | cut -d= -f1

# Step 2: Source + connect using the discovered names
source /root/.secrets/kunci-mas.env
PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB \
  -tAc "SELECT current_database() || ' | tables=' || count(*) FROM information_schema.tables WHERE table_schema='public';"
```

**Pitfalls (verified 2026-08-06):**
- **Docker container, not native process.** `pg_isready -h 127.0.0.1` returns "accepting connections" even when auth is broken — port 5432 is forwarded from the container. No `/var/run/postgresql/` socket exists on the host. No `postgres` user exists (`sudo -u postgres` fails).
- `POSTGRES_USER` may NOT be `arifos` and `POSTGRES_DB` may NOT be `arifos`. Hardcoding "arifos" → "password authentication failed" or "database does not exist". Always discover env var names FIRST via `grep -iE 'postgres' /root/.secrets/kunci-mas.env | cut -d= -f1`.
- If `$POSTGRES_DB` value is a DB you didn't expect → read the actual env values directly from `kunci-mas.env`, do not guess the user/db name from the variable name.
- `LOCALHOST_IS_PASSWORD` doctrine: Postgres binds 127.0.0.1; password auth IS configured for the user → env var is authoritative, no socket peer-auth bypass.
- `docker exec postgres psql` may fail because the container doesn't always have `psql` installed; use host-side `psql` with the correct `$POSTGRES_USER` instead.

**Docker NAT + trust auth (proven 2026-08-06):** Adding a `host all all 127.0.0.1/32 trust` line to `pg_hba.conf` does NOT enable password-less access from the host. Docker port-forwarding (`-p 5432:5432`) rewrites the source IP via iptables DNAT — from inside the container, host connections appear to come from the Docker bridge gateway (`172.17.0.1` or `172.21.0.1`), NOT `127.0.0.1`. The trust rule never matches.

Fix: add a trust line for the bridge subnet, then reload:
```bash
# Discover your bridge subnet
docker network inspect bridge --format '{{range .IPAM.Config}}{{.Subnet}}{{end}}'
# Typical: 172.17.0.0/16 or 172.21.0.0/16

# Append the trust line and reload (no restart required)
docker exec postgres bash -c 'echo "host all all 172.21.0.0/16 trust" >> /var/lib/postgresql/data/pg_hba.conf'
docker exec postgres pg_ctl reload
```

Verify: `psql -h 127.0.0.1 -U postgres -c 'SELECT 1'` should now return without prompting for a password. This is consistent with LOCALHOST_IS_PASSWORD doctrine — the connection IS from a known-trusted Docker-bridge subnet, not from outside the host.

## L4a — Ollama (embedding backend for L3 memory)

Ollama's surviving role in the federation is **embedding generation only** (`bge-m3`), not text generation. Text-gen moved to mimo via LiteLLM (`ilmu_soul.yaml` canonical statement: "Ollama kept only for bge-m3 embeddings").

**Wiring (graphiti-mcp side):**
```
Graphiti MCP (docker container)
  → reads OPENAI_API_KEY="ollama" (sentinel value, not real key)
  → calls http://ollama-engine-prod:11434 inside docker network
  → host Ollama (bare-metal systemd) binds localhost:11434
  → routes to bge-m3 / qwen2.5:3b on /opt/arifos/data/ollama/models
```

**Probe recipe:**
```bash
# Bare-metal systemd
systemctl status ollama | grep -E 'Active|Main PID'
ls -la /opt/arifos/data/ollama/models/ 2>/dev/null | head
curl -sf -m 3 http://127.0.0.1:11434/api/tags | head

# Docker side (graphiti-mcp depends on it)
docker ps -a --filter "name=ollama-engine-prod" --format "{{.Names}} {{.Status}}"
```

**Doctrine conflicts (verified 2026-08-06):**
- `OLLAMA_HOST=0.0.0.0:11434` in the systemd unit WINS over a `bind-localhost.conf` drop-in — systemd `Environment=` lines do NOT yield to drop-in files with the same var. Violation of `LOCALHOST_IS_PASSWORD` doctrine (UFW masks it but the bind is wrong). Fix: remove the `Environment="OLLAMA_HOST=..."` line from the unit file directly.
- **2026-08-06 update:** if the unit file has NO `Environment="OLLAMA_HOST"` line and only drop-ins set the var (both drop-ins agree on `127.0.0.1:11434`), the bind comes up correctly on restart — verified live (`ss -tlnp | grep 11434` shows `127.0.0.1` only). The doctrine-conflict pitfall only fires when the unit itself contains a conflicting `Environment=` line. Audit both before editing.
- `/usr/local/bin/graphiti-start.sh` will FATAL out if it can't reach Ollama at startup — that's the **correct** fail-closed behavior (F2). If graphiti-mcp is down, check Ollama FIRST before debugging the container.
- Hermes agent (the Telegram bridge) does NOT talk to Ollama at all — its model routing goes via LiteLLM → mimo. Don't confuse Ollama's role (embedding infrastructure) with the inference path.

## L5 — Graphiti / FalkorDB (relationship graph)

```bash
# Port check (lightweight)
python3 -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1', 6380)); print('FalkorDB UP'); s.close()"
python3 -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1', 8000)); print('Graphiti MCP UP'); s.close()"
```

**Note:** FalkorDB (`:6380`) is the graph DB; Graphiti MCP (`:8000`) is the MCP interface on top. Both must be UP for relationship queries to work. Graphiti MCP depends on Ollama (see L4a) — if Graphiti is down, check Ollama first.

## L6 — VAULT999 (immutable sealed truth)

```bash
# Append-only flag
lsattr /root/arifOS/VAULT999/outcomes.jsonl | awk '{print $1}'
# Expected: -----a--------e-------  (+a = append-only)

# Size + validity
wc -l /root/arifOS/VAULT999/outcomes.jsonl
tail -3 /root/arifOS/VAULT999/outcomes.jsonl | python3 -c "import sys,json; [json.loads(l) for l in sys.stdin]; print('All valid')"

# Recent activity (last 24h)
python3 -c "
import json
from datetime import datetime, timezone, timedelta
cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
count, last_ts = 0, None
with open('/root/arifOS/VAULT999/outcomes.jsonl') as f:
    for line in f:
        try:
            o = json.loads(line)
            ts = o.get('ts') or o.get('timestamp') or ''
            if ts > cutoff: count += 1
            last_ts = ts
        except: pass
print(f'Last 24h: {count} receipts | Latest: {last_ts}')
"
```

**Interpretation:**
- `+a` absent on lsattr = append-only is NOT enforced (integrity risk — fix: `chattr +a`).
- 0 receipts in 24h = vault ingestion pipeline may be stalled (check `git_to_vault.py` cron).
- Invalid JSON at tail = corruption (serious — check with `make vault999-verify`).

## Supporting services

```bash
# Carry forward state
python3 -c "import json; print(json.dumps(json.load(open('/root/.local/share/arifos/carry_forward.json')), indent=2))" | head -30

# Flow state cache (stale if > 5 min old)
cat /root/AAA/state/flow_state.json | python3 -m json.tool | grep -E '"fq"|"verdict"|"refreshed_at"'

# Live FQ (authoritative — always prefer over cache)
curl -sf http://127.0.0.1:7073/health | python3 -m json.tool
```

**FQ truth rule:** Live `:7073/health` > `flow_state.json` cache. Drift threshold = 0.3. If |live − cache| > 0.3 → `FQ_SIGNAL_DRIFT` → use live.