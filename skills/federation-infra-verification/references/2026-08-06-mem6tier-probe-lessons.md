# 6-Tier Memory Probe — Session Lessons (2026-08-06)

A "is the memory system OK?" probe session turned up two structural lessons worth keeping:

## 1. The "Ollama Fixed ✅" sibling report — performance vs reality

**What happened.** Two sibling reports were pasted about the federation's 6-tier memory landscape. The first sibling report claimed:

| Claim | Report | Live truth |
|---|---|---|
| `bind-localhost.conf` changed to `127.0.0.1:11434` | ✅ Fixed | ✅ TRUE — verified by reading both files |
| `systemctl start ollama` → active | ✅ Active | ❌ **FALSE** — `inactive (dead)`, port 11434 NOT listening |
| `ss -tlnp` confirms 127.0.0.1 only | ✅ | ❌ **FALSE** — nothing on 11434 at all |
| Models loaded: bge-m3, qwen2.5:3b | ✅ | ❌ **UNVERIFIED** — service not up |

**Pattern.** The sibling's *config* claims were true. The sibling's *state* claims (active, listening, models loaded) were false. The report presented "Done. Ollama back online. ΔS=-0.3" as if the state matched the config. It didn't.

**Why this matters.** Sibling reports can be **partial**: the structural intent (edit config, run systemctl) is correct, but the actual state never lands. Re-probing each falsifiable claim — `systemctl is-active`, `ss -tlnp`, `curl /api/tags` — catches the gap.

**Action taken in session:** `sudo systemctl start ollama` → `active`, `127.0.0.1:11434 LISTEN`, models loaded `bge-m3:latest qwen2.5:3b`. Sibling report's **intent** was right; the **report** was overconfident.

**Reusable probe shape:**

```bash
# Don't accept "service X is up" — verify the three live signals
systemctl is-active ollama
ss -tlnp | grep 11434
curl -sf -m 3 http://127.0.0.1:11434/api/tags | jq '.models[].name'
```

All three must succeed for the claim "Ollama is up and serving" to hold. A single check (`curl` alone) misses the case where the binary is dead.

## 2. Postgres trust auth — Docker NAT subnet was the missing piece

**What happened.** Postgres is a Docker container (`postgres`); psql from the host was getting `fe_sendauth: no password supplied` despite the LOCALHOST_IS_PASSWORD doctrine. The pg_hba.conf had trust auth for `127.0.0.1/32` only.

**Root cause.** Docker port-forwarding (`-p 5432:5432`) uses iptables DNAT. From inside the container, connections appear to come from the Docker bridge gateway (`172.21.0.1`), not `127.0.0.1`. The trust rule never matched.

**Fix recipe:**

```bash
# Inside the postgres container's pg_hba.conf, ADD a trust line for the bridge subnet
# (before doing this, confirm the bridge subnet with:)
docker network inspect bridge --format '{{range .IPAM.Config}}{{.Subnet}}{{end}}'
# Typical: 172.17.0.0/16 or 172.21.0.0/16

# Then either:
#   (a) edit pg_hba.conf inside the running container + reload:
docker exec postgres bash -c 'echo "host all all 172.21.0.0/16 trust" >> /var/lib/postgresql/data/pg_hba.conf'
docker exec postgres pg_ctl reload
# or
#   (b) restart the container if the image mounts pg_hba.conf at start
docker restart postgres
```

**Why the doctrine conflict trap fires here.** The instinct on a "trust doesn't work" failure is to conclude "trust isn't safe" or "we need a password". Both are wrong — the doctrine is correct, the **subnet coverage** was incomplete. The fix is an additive trust line, not a re-architecture.

## 3. Kernel probe — judge the probe, not the service

**What happened.** First probe of `:8088/mcp` returned `"Not Acceptable: Client must accept application/json"`. Second probe of `/tools/list` returned `0 tools` (no error — silently rejected because the same header issue). I almost wrote "kernel is broken" in the audit response.

**The fix.** Add `Accept: application/json` (and for FED-style endpoints, also `text/event-stream`) to every probe. Re-probe:

```bash
curl -s -X POST http://127.0.0.1:8088/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}'
# → 8 tools returned: arif_init, arif_observe, arif_think, arif_route, arif_memory, arif_judge, arif_forge, arif_seal
```

**Lesson.** Before declaring "X is broken" from a probe failure, fix the probe ONCE and re-run. If it still fails, then escalate. The same discipline catches sibling reports — their probe may have failed for the same reason, and their "X is broken" conclusion is invalid by construction.

## 4. Atlas333 / EUREKA777 — modes, not tools

A sibling report described these as "kernel concepts accessible to OpenCode". The verified state:

- **atlas333_eureka** Qdrant collection: 74 points, green, 1024-dim Cosine vectors
- **atlas333-cognitive-geometry** skill: v1.0.0, F1/F2/F4/F7-scoped, T1 autonomy, owner=AAA
- **EUREKA777-paradox-resolution** skill: v1.0.0-2026.07.31, F2/F4/F7/F11-scoped, owner=F13 SOVEREIGN, T1 autonomy
- **Kernel tools surface:** 8 canonical tools. NONE named `atlas_*`, `eureka_*`, or `megamemory_*`. ATLAS333/EUREKA777 are accessed via `arif_think(mode='atlas')` — a **mode**, not a tool.

The sibling's architectural description was directionally right (ATLAS333 lives in Qdrant, EUREKA777 is a cooling engine) but the *tool family* claim was fabricated. `megamemory_*` tools don't exist in the kernel `/tools` surface; the only `megamemory` string in the codebase is one regex in a deny-list. Capture this as a sibling-report failure mode in `verify-sibling-ops-reports` §4.3.

## Reusable one-shot probe (memory + kernel)

```bash
# L1/L2 Redis
redis-cli -h 127.0.0.1 -p 6379 ping && redis-cli dbsize

# L3 Qdrant
curl -sf http://127.0.0.1:6333/collections | jq '.result.collections | length'

# L4 Postgres (after trust fix)
docker exec postgres psql -U postgres -tAc 'SELECT count(*) FROM information_schema.tables WHERE table_schema=''public'''

# L5 FalkorDB + Graphiti
docker exec falkordb redis-cli ping
curl -sf http://127.0.0.1:8000/health

# L6 VAULT999
wc -l /root/arifOS/VAULT999/outcomes.jsonl
lsattr /root/arifOS/VAULT999/outcomes.jsonl | grep -o '[a--]'

# Ollama (3-signal check)
systemctl is-active ollama && ss -tlnp | grep 11434 && curl -sf -m 3 http://127.0.0.1:11434/api/tags | jq '.models[].name'

# arifOS kernel (correct headers)
curl -s -X POST http://127.0.0.1:8088/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}' | jq '.result.tools | length'

# FQ
curl -sf http://127.0.0.1:7073/health | jq '.fq'
```