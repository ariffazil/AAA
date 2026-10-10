# Infra Live State — arifOS Human-Reality Architecture Storage

**Probe date:** 2026-10-09 23:57 +08 (Asia/Kuala_Lumpur) · host `forge` · user `root`
**Mode:** READ-ONLY probe. No service started/stopped/restarted. No writes except this file.

## Verdicts (one line per target)

| Target | Verdict | One-liner |
|---|---|---|
| (a) Graphiti/FalkorDB link graph `:18412` | **DOWN** (MCP front) / **LIVE** (FalkorDB backend `:6380`, all 7 graphs intact) | `graphiti-mcp.service` disabled & stopped 2026-10-09 18:46 after 36 crash-loop restarts (`falkordb:6379` DNS unresolvable — falkordb container is on `bridge`, not `arifos_core_network`); FalkorDB itself is healthy on 6380 with all 7 group graphs incl. the 7th = `searah_2026q3` |
| (b) Postgres `127.0.0.1:5432` | **LIVE** | docker `postgres:16-alpine`, 4 user DBs (`vault999`, `litellm`, +templates); `vault999` = 422,752 observability rows; **pgvector NOT installed**; **no people/human/memory tables** (only `LiteLLM_MemoryTable` in the litellm DB, which is LiteLLM proxy bookkeeping) |
| (c) Redis `6379` | **LIVE (auth-protected)** | host `redis-server` (systemd `redis.service`), requirepass set; 640 keys in db0 (389 volatile); usage = **LiteLLM-fed router rate-limit/cache + `federation:organ:*` organ registry keys**; dir `/var/lib/redis`, dump.rdb |
| (d) arifflow `:7073` | **LIVE** | `GET /health` → `status:"ok-v3-vector"`, verdict `HEURISTIC_ADVISORY`, uptime ≈ 2.9 h, 1039 cycles, 1000 receipts |

---

## (a) Graphiti / FalkorDB link graph — MCP front DOWN, backend LIVE

### Consumer expectation
`/root/AAA/scripts/linkgraph_sync.py` (line 44): `GRAPHITI_URL = "http://127.0.0.1:18412/mcp/"`, 7 group_ids (docstring lines 7–9): `arif_l5_knowledge, sado_knowledge, atlas333_graph, af_forge, arifos, arifos_federation, searah_2026q3` — **the 7th group_id is `searah_2026q3`**.

### Port probe
```
$ curl -sS -m 5 -o /dev/null -w "http_code=%{http_code}\n" http://127.0.0.1:18412/
curl: (7) Failed to connect to 127.0.0.1 port 18412 after 0 ms: Could not connect to server
http_code=000
$ curl ... http://127.0.0.1:18412/mcp/
http_code=000
$ ss -tlnp | grep 18412        # (no output — nothing listens on 18412)
```

### Service discovery
```
$ systemctl list-unit-files | grep -iE 'falkor|graphiti'
graphiti-mcp.service    disabled  enabled
falkordb.service        enabled   enabled

$ systemctl status graphiti-mcp
○ graphiti-mcp.service - Graphiti MCP Knowledge Graph (ILMU-native)
     Loaded: loaded (/etc/systemd/system/graphiti-mcp.service; disabled; preset: enabled)
     Active: inactive (dead)

$ systemctl status falkordb
● falkordb.service - FalkorDB Graph Database (Docker) — L5 substrate, port 6380
     Active: active (running) since Fri 2026-10-09 21:11:54 +08; 2h 45min ago
     └─10819 /usr/bin/docker run --rm --name falkordb -p 127.0.0.1:6380:6379 -v falkordb_data:/var/lib/falkordb/data ... falkordb/falkordb:latest
```
Docker: `falkordb` container `Up 3 hours (healthy)` at `127.0.0.1:6380->6379/tcp`. Image `zepai/knowledge-graph-mcp:latest` (the Graphiti MCP image) is still present locally; `graphiti_data` docker volume intact (created 2026-09-20).

### Last error (journalctl -u graphiti-mcp)
Crash-loop, restart counter reached 36; root cause in the last failure:
```
redis.exceptions.ConnectionError: Error -3 connecting to falkordb:6379.
Temporary failure in name resolution.
Oct 09 18:36:37 systemd[1]: Main process exited, code=exited, status=1/FAILURE
...restart counter is at 36...
Oct 09 18:46:43 systemd[1]: Stopping graphiti-mcp.service ...   ← manual stop
Oct 09 18:47:09 systemd[1]: Stopped graphiti-mcp.service.
```
**Why DNS fails:** graphiti-mcp runs on docker network `arifos_core_network` and dials `redis://falkordb:6379` (see `/usr/local/bin/graphiti-start.sh`), but the falkordb container is on the **default `bridge`** network:
```
$ docker network inspect arifos_core_network --format '{{range .Containers}}{{.Name}} {{end}}'
qdrant postgres minio                      # ← no falkordb
$ docker inspect falkordb --format '{{.HostConfig.NetworkMode}}'
bridge
```

### Backend liveness — all 7 graphs present
```
$ redis-cli -h 127.0.0.1 -p 6380 ping
PONG
$ redis-cli -h 127.0.0.1 -p 6380 info keyspace
db0:keys=15,expires=0,avg_ttl=0
$ redis-cli -h 127.0.0.1 -p 6380 GRAPH.LIST
atlas333_graph  arifos_federation  searah_2026q3  sado_knowledge
arif_l5_knowledge  af_forge  arifos        # ← all 7 group_ids match the script
```
FalkorDB boot log (via falkordb.service): "Done decoding graph arifos … keys loaded: 15 … Ready to accept connections" (2026-10-09 21:13:02).

### Governance context (not an accident)
`/root/AAA/instructions/L5-Graphiti-Deprecation-2026-10-07.md` — **F13_RATIFIED_CANON, 2026-10-07**: L5 (Graphiti) write path deprecated; memory writes are 2-leg (L3 Qdrant + L4 Supabase); "port 18412 is no longer load-bearing for memory writes". FalkorDB kept running as a read-only historical graph. So the link-graph write path consumed by `linkgraph_sync.py` is down **by ratified policy**, not by unnoticed failure.

### Recovery (minimal, in dependency order — NOT executed)
The unit that WOULD start the 18412 front:
```
systemctl start graphiti-mcp        # launches /usr/local/bin/graphiti-start.sh
```
…but it will crash-loop again until the network split is fixed. True minimal recovery:
```
docker network connect arifos_core_network falkordb   # make 'falkordb' DNS-resolvable
systemctl start graphiti-mcp
```
(falkordb runs `--rm`, so re-attach is needed after each falkordb restart — durable fix is adding `--network arifos_core_network` to `falkordb.service` ExecStart, plus an alias. Preconditions already met: Ollama up on 11434, `qwen2.5:3b` present.) Per canon, re-enabling L5 writes additionally requires an F13 re-enable ratification file (`L5-RE-ENABLE-<date>.md`) superseding the deprecation doc.

---

## (b) Postgres 127.0.0.1:5432 — LIVE

```
$ ss -tlnp | grep 5432
LISTEN 127.0.0.1:5432 users:(("docker-proxy",pid=8965,fd=8))
$ docker ps --filter name=postgres
postgres:16-alpine  Up 3 hours (healthy)  127.0.0.1:5432->5432/tcp
```
Credentials surfaced read-only from the container env (`POSTGRES_USER=arifos_admin`, `POSTGRES_DB=vault999`) — used only for probing via `docker exec psql`; not needed from the network side.

### Databases
```
$ psql -U arifos_admin -d vault999 -c '\l'
 litellm | arifos_admin | UTF8 ...
 postgres | arifos_admin | UTF8 ...
 template0 / template1
 vault999 | arifos_admin | UTF8 ...
```

### Schemas & tables (vault999)
```
$ psql -c '\dn'
 observability | arifos_admin
 public        | pg_database_owner

$ psql -c "SELECT table_schema, table_name FROM information_schema.tables
           WHERE table_schema NOT IN ('pg_catalog','information_schema');"
 observability | observations     ← 422,752 rows (tool-invoke telemetry; latest 2026-09-29+)
 public        | trust_history    ← 0 rows
 public        | trust_scores     ← 0 rows
 public        | vault_seals      ← 0 rows
```
`observations` columns: id/trace_id/span_id/session_id/actor_id/tool_name/organ_id/verdict_class/…/input_hash/output_hash/created_at (indexed on actor, session, tool, trace, verdict, created_at DESC).

### pgvector
```
$ psql -c '\dx'
 plpgsql | 1.0 | pg_catalog        ← only extension installed
$ psql -c "SELECT extname FROM pg_extension WHERE extname LIKE '%vector%';"
 (0 rows)                            ← pgvector NOT installed
```

### people/human/memory tables
```
$ psql -c "SELECT table_schema, table_name FROM information_schema.tables
           WHERE table_name ~* 'people|human|memory|person';"
 (only pg_catalog.pg_backend_memory_contexts — system)
```
**No people/human/person tables exist.** `litellm` DB holds ~100 `LiteLLM_*` proxy tables (budgets, spend, keys — including `LiteLLM_MemoryTable`, which is LLM-proxy session memory, not human-reality storage). **The human-reality v2 storage layer has no Postgres footprint yet** — vault999 is currently telemetry (observations) + empty trust/seal scaffolding.

Recovery step: none needed (LIVE). For v2: `CREATE EXTENSION vector;` would be required first if pgvector-backed memory is planned (image `postgres:16-alpine` ships the contrib files).

---

## (c) Redis 6379 — LIVE (auth required)

```
$ ss -tlnp | grep 6379
LISTEN 127.0.0.1:6379 + 100.64.0.2:6379 + ::1  users:(("redis-server",pid=3450))
$ redis-cli -h 127.0.0.1 -p 6379 ping
NOAUTH Authentication required.           ← requirepass set
```
Password lives in `/etc/redis/redis.conf:2349` (`requirepass …`; also `bind 127.0.0.1 100.64.0.2 -::1`, `port 6379`). This is the **host** redis-server (systemd `redis.service`), *not* the searxng container redis (that one is `redis:7-alpine`, port unexposed).

With auth (read-only commands):
```
PING → PONG
DBSIZE → 640
INFO keyspace → db0:keys=640,expires=389,avg_ttl≈68.6M ms
CONFIG GET dir → /var/lib/redis ; dbfilename → dump.rdb
```
Sample keys (SCAN, 30):
```
litellm-fed:global_router:<hash>:openai/qwen3.7-plus:rpm:07-27   (rate-limit windows)
litellm-fed:<hash>…                                             (router/session cache)
litellm-fed:global_router:<hash>:openai/deepseek-v4-pro-0813:rpm:…
federation:organ:geox                                           (organ registry keys)
```
**Verdict on usage:** Redis 6379 = LiteLLM-federation LLM-router cache & RPM rate-limit windows + a small set of `federation:organ:*` registry keys. It is *not* used for human-reality memory; ~61% of keys are volatile (389/640 with TTL).

Recovery step: none (LIVE). Note: password is in world-readable-to-root config only (`-rw-r----- redis:redis`) — good.

---

## (d) arifflow 7073 — LIVE

```
$ ss -tlnp | grep 7073
LISTEN 127.0.0.1:7073 users:(("arifflow",pid=3021))   (/opt/arifflow/bin/arifflow --daemon)
$ curl -sS -m 5 http://127.0.0.1:7073/
http_code=404                                        (expected — routes are explicit)
$ curl http://127.0.0.1:7073/health
{"diagnosis":"HEURISTIC_ADVISORY", ... "status":"ok-v3-vector","uptime_ms":10585652, ...}
```
Health detail: `status ok-v3-vector`, uptime ≈ 10,585,652 ms (~2.94 h, started with the 21:00 boot cohort), `invariants.cycle_count 1039`, `receipts 1000`, `hold_count 13`, `throttle_count 0`, 7 actors tracked, top-level verdict `HEURISTIC_ADVISORY` (g dimension PATHOLOGICAL/uncalibrated — phase-1 heuristic, by design). Companion `arifflow.service`, `arifflow-mcp.service` (7075) both `active/running` per systemctl.

Recovery step: none (LIVE).

---

## Summary matrix

| # | Probe | Verdict | Minimal recovery |
|---|---|---|---|
| a1 | FalkorDB 6380 | LIVE | — |
| a2 | Graphiti MCP 18412 | DOWN (disabled 2026-10-09; canon-deprecated 2026-10-07) | `docker network connect arifos_core_network falkordb && systemctl start graphiti-mcp` (+F13 re-enable ratification if writes resume) |
| b | Postgres 5432 | LIVE | — (no pgvector, no human tables — v2 must create them) |
| c | Redis 6379 | LIVE | — |
| d | arifflow 7073 | LIVE | — |

No BLOCKED probes. Secrets (redis requirepass, POSTGRES_PASSWORD) were read from local root-owned configs for probing only and are intentionally not reproduced in full here beyond their source locations.
