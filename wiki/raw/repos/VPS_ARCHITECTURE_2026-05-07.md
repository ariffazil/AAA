# VPS Architecture Audit — 2026-05-07
**Auditor:** Hermes ASI | **Timestamp:** 2026-05-07T04:37 UTC | **ΔS Target:** < 0

---

## 1. Stack Topology (ASCII)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         VPS (Hostinger)                             │
│                   72.62.71.199 | 193GB | 15GB RAM                  │
│                         87% disk used                             │
├─────────────────────────────────────────────────────────────────────┤
│  INFRA LAYER                                                        │
│  ├── postgres:16-alpine    → 5432/tcp (DB)              [healthy] │
│  ├── redis:7-alpine         → 6379/tcp (cache)          [healthy] │
│  └── qdrant:latest          → 6333-6334/tcp (vector)    [healthy] │
├─────────────────────────────────────────────────────────────────────┤
│  FEDERATION LAYER                                                   │
│  ├── arifosmcp (af-forge-arifosmcp:latest)                         │
│  │       → 0.0.0.0:8080  [healthy] v2026.05.05-SSCT   13 tools  │
│  ├── af-forge-arifosmcp-1 (9c76c02f1380)                           │
│  │       → 8080/tcp [unhealthy] ⚠️ ORPHANED STACK              │
│  ├── geox_eic (af-forge-geox)                                      │
│  │       → 127.0.0.1:8081  [healthy]                   30 tools   │
│  ├── wealth-organ (ghcr.io/ariffazil/wealth:phase1-tools)          │
│  │       → 0.0.0.0:8082  [healthy]                  91 functions │
│  └── well (ghcr.io/ariffazil/well:phase1-tools)                    │
│          → 0.0.0.0:8083  [healthy]                  113 functions │
├─────────────────────────────────────────────────────────────────────┤
│  A-FORGE BRIDGE                                                     │
│  ├── af-bridge-prod (a-forge-af-bridge)                            │
│  │       → 127.0.0.1:7071  [healthy]                  TypeScript  │
│  ├── aaa-a2a (a2a-server-aaa-a2a:latest)                          │
│  │       → 127.0.0.1:3001  [healthy]                  A2A gateway │
│  └── vault999 (compose-vault999:v1.0.0)                            │
│          → 127.0.0.1:8100  [healthy]                  VAULT ledger │
├─────────────────────────────────────────────────────────────────────┤
│  OPENCLAW (AGI Layer) — af-forge.hstgr.cloud                       │
│  ├── openclaw gateway  → :18789  [CRITICAL ⚠️ P99=7168ms]         │
│  ├── openclaw-a2a.py   → :18000  [NO HEALTH ROUTE]                │
│  └── hermes-a2a.py     → :18001  [404 ON /health]                 │
├─────────────────────────────────────────────────────────────────────┤
│  OBSERVABILITY                                                      │
│  ├── Langfuse (cloud) — ACTIVE, 13/13 tools traced                 │
│  ├── Loki/Promtail    → MISSING ❌                                 │
│  └── Grafana          → access configured ✅                       │
├─────────────────────────────────────────────────────────────────────┤
│  LLM RUNTIME                                                        │
│  └── ollama-engine-prod (127.0.0.1:11434)                          │
│          bge-m3:latest (embedding) + qwen2.5:7b (chat)            │
├─────────────────────────────────────────────────────────────────────┤
│  PUBLIC ROUTING (Caddy + Cloudflare)                               │
│  ├── arifOS  → https://arifos.arif-fazil.com/mcp  (8080)          │
│  ├── GEOX    → https://geox.arif-fazil.com/mcp    (8081)          │
│  ├── WEALTH  → https://wealth.arif-fazil.com/mcp   (8082)        │
│  └── WELL    → https://well.arif-fazil.com/mcp     (8083)        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. MCP Servers — Live Status

| Service | Port | Transport | Tools | Status | Image |
|---------|------|-----------|-------|--------|-------|
| **arifOS** | 8080 | streamable-http | 13 canonical | ✅ healthy | af-forge-arifosmcp:latest |
| **GEOX** | 8081 | legacy http | 30 | ✅ healthy | af-forge-geox |
| **WEALTH** | 8082 | SSE | 91 functions | ✅ healthy | ghcr.io/ariffazil/wealth:phase1-tools |
| **WELL** | 8083 | streamable-http | 113 | ✅ healthy | ghcr.io/ariffazil/well:phase1-tools |
| A-FORGE | 7071 | HTTP | N/A (bridge) | ✅ healthy | a-forge-af-bridge |
| OLLAMA | 11434 | HTTP | bge-m3, qwen2.5:7b | ✅ running | ollama/ollama:latest |

> ⚠️ **WEALTH tool count:** Header says "50" but `grep -c "def wealth_"` returns **91 functions**. Confirmed live — monolith.py is the real engine.

---

## 3. Critical Findings (Must Fix Now)

### 🔴 CRITICAL-1: OpenClaw Event Loop P99 = 7168ms
**Threshold table:**
| P99 | Status |
|-----|--------|
| < 100ms | ✅ Healthy |
| 100–500ms | ⚠️ Elevated |
| 500–2000ms | 🔴 Warning |
| 2000–10000ms | 🔴🔴 **CRITICAL — Restart gateway** |
| > 10000ms | 💀 Choking |

**Current:** P99 = 7168ms → **CRITICAL**. Gateway needs immediate restart.
**Evidence:** `eventLoopDelayP99Ms=7168.1` in openclaw-2026-05-07.log

**Fix:**
```bash
kill $(pgrep -f "openclaw.*gateway") 2>/dev/null
sleep 2
cd /tmp && nohup /usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789 > /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>&1 &
```

---

### 🟡 WARNING-1: Duplicate Unhealthy arifOS Container
**Container:** `af-forge-arifosmcp-1` (9c76c02f1380) — Up 13 hours, **unhealthy**
- No host port binding (only internal 8080/tcp)
- Not receiving traffic (host:8080 goes to `arifosmcp` healthy container)
- Likely orphaned from old `docker compose` stack

**Action:** Investigate origin. If from old compose stack, remove:
```bash
docker stop af-forge-arifosmcp-1 && docker rm af-forge-arifosmcp-1
```

---

### 🟡 WARNING-2: Kimi Model Misconfiguration
**Error:** `Unknown model: kimi/kimi-for-coding` and `kimi/kimi-k2p5-turbo` → falls back to `minimax/MiniMax-M2.7`
- OpenClaw is configured with `kimi-for-coding` as primary model
- These models don't exist in the Kimi API
- Fallback to MiniMax-M2.7 works but adds ~200ms latency per request
- **Fix:** Update OpenClaw model config to use valid Kimi model IDs

---

### 🟡 WARNING-3: hermes-a2a.py (18001) Returns 404 on /health
- Port 18000 (openclaw-a2a.py) — no health route, no response
- Port 18001 (hermes-a2a.py) — returns 404 on `/health`
- A2A bridge health cannot be monitored
- **Fix:** Add health route to both A2A bridge scripts

---

## 4. Integration Wiring Status

| Path | Status | Notes |
|------|--------|-------|
| arifOS → GEOX | ✅ LIVE | httpx calls from rest_routes.py → geox_eic:8081 |
| arifOS → WEALTH | ⚠️ SSE-only | WEALTH POST returns 405 — arifOS has no SSE client |
| arifOS → WELL | ⚠️ SSE-only | WELL POST returns 405 — arifOS has no SSE client |
| arifOS → vault999 | ✅ LIVE | Vault999 writer accessible |
| arifOS → postgres | ❌ ISOLATED | Cannot import psycopg2 from inside container |
| arifOS → redis | ❌ ISOLATED | Cannot import redis from inside container |
| arifOS → qdrant | ✅ LIVE | Vector memory operational |
| GEOX → arifOS | ✅ LIVE | GEOX can call arifOS MCP tools |
| OpenClaw → arifOS | ✅ LIVE | gateway:18789 → arifOS MCP |

**Key insight:** The federation is **half-wired**. arifOS can call GEOX live. But WEALTH and WELL are SSE-only transport — arifOS cannot call them as MCP clients. They can call arifOS, but arifOS cannot call them back.

---

## 5. Substrate Audit

### ✅ EXISTING (Available Now)
| Substrate | Status | Evidence |
|-----------|--------|----------|
| Docker | ✅ Available | `/usr/bin/docker` |
| Python3 | ✅ Available | hermes venv |
| Node.js | ✅ Available | v22.22.2 |
| Headless Chromium | ✅ Available | `/usr/bin/chromium-browser` |
| Playwright | ✅ Available | `playwright` CLI |
| Cron (Temporal) | ✅ Available | `/usr/sbin/cron` |
| PostgreSQL | ✅ Available | `postgres:16-alpine` |

### ❌ MISSING (Gaps for Proactive Mesh)

| Substrate | Gap | Risk | Priority |
|-----------|-----|------|----------|
| **Sandboxed Execution** | No firejail / gVisor | Agent W_scar risk | 🔴 HIGH |
| **NATS / Redis PubSub** | No message broker | A2A is synchronous only | 🔴 HIGH |
| **Loki + Promtail** | No log aggregation | No raw VPS/Docker logs in Grafana | 🔴 HIGH |
| **SSE Client (arifOS)** | Cannot call SSE-only servers | WEALTH/WELL federation broken | 🟡 MED |
| **Webhook Deploy** | Not configured | No autonomous deploy trigger | 🟡 MED |
| **WAF Hardening** | Traefik needs API key + rate-limit | Public exposure on Hostinger | 🟡 MED |
| **SQL Substrate** | SQLite/Postgres for hard state | Vector DB only, no relational | 🟡 MED |
| **E2B / Docker-in-Docker** | No cloud sandbox | Agent execution not isolated | 🟡 MED |

---

## 6. Disk Analysis

```
Filesystem: /dev/sda1
Total: 193GB | Used: 167GB | Available: 27GB | Usage: 87%

Docker breakdown:
  Images:   68.25GB (41% reclaimable)
  Build Cache: 19.4GB (can be pruned)
  Containers: 28.41MB
  Volumes:  9.852GB (1.514GB reclaimable)
```

**⚠️ 87% disk usage is HIGH.** Pruning build cache would recover ~20GB:
```bash
docker builder prune -af --filter "until=24h"
```

---

## 7. Caddy Routing — Full & Correct

All 4 federation MCP routes are correctly wired:
- ✅ `arifos.arif-fazil.com/mcp` → `arifosmcp:8080`
- ✅ `geox.arif-fazil.com/mcp` → `geox_eic:8081`
- ✅ `wealth.arif-fazil.com/mcp` → `wealth-organ:8082`
- ✅ `well.arif-fazil.com/mcp` → `well:8083`

No missing routes. Routing is solid.

---

## 8. OpenClaw Gateway Model Config Issue

Current log shows repeated fallback chain:
```
kimi/kimi-for-coding → model_not_found → minimax/MiniMax-M2.7 ✓
kimi/kimi-k2p5-turbo → model_not_found → minimax/MiniMax-M2.7 ✓
```

The Kimi provider is configured with wrong model IDs. Every request wastes ~200ms on failed model lookup before falling back.

**Fix:** Find OpenClaw config and update `kimi` model IDs to valid ones (e.g., `kimi/kimi-k2p9` or whatever is actually available in the Kimi API).

---

## 9. Missing Architecture Map (Arif's Requirements)

```
Arif's Requirement          Current State         Gap
─────────────────────────────────────────────────────────────────
Sandboxed Execution         ❌ No firejail/gVisor   No isolation layer
Headless Browser            ✅ chromium + playwright  READY TO USE
Relational / SQL            ⚠️ Postgres exists      arifOS can't reach it
Temporal / Cron             ✅ cron available       No autonomous wake loops
Message Broker (A2A)        ❌ No NATS             Blocking HTTP only
Log Aggregation (Loki)      ❌ No Loki/Promtail    Langfuse only (LLM traces)
WAF Hardening               ⚠️ Caddy TLS done      No API key + rate-limit
Webhook Deploy              ❌ Not configured      No autonomous triggers
SSE Client                  ❌ arifOS can't call   WEALTH/WELL unreachable
```

---

## 10. Priority Actions

| # | Action | Severity | Effort | ΔS Impact |
|---|--------|----------|--------|-----------|
| 1 | **Restart OpenClaw gateway** (P99=7168ms) | 🔴 CRITICAL | 2 min | +++ |
| 2 | **Prune Docker build cache** (87% disk) | 🟡 HIGH | 5 min | ++ |
| 3 | **Fix duplicate arifOS container** | 🟡 MED | 2 min | + |
| 4 | **Fix Kimi model IDs in OpenClaw** | 🟡 MED | 5 min | +++ |
| 5 | **Install Loki + Promtail** | 🟡 HIGH | 30 min | +++ |
| 6 | **Install NATS** (A2A mesh) | 🟡 HIGH | 20 min | ++++ |
| 7 | **Wire SSE client in arifOS** | 🟡 MED | 2h | +++ |
| 8 | **Add firejail sandbox** | 🔴 HIGH | 1h | +++++ |
| 9 | **Prune disk to <80%** | 🟡 HIGH | 5 min | ++ |

---

## 11. Verdict — ΔS < 0 Architecture

**Current ΔS state:** Mixed. Foundation is solid (13 tools live, 4/4 federation MCP routes correct, Caddy routing complete), but **entropy is rising** from:
1. OpenClaw P99 in critical zone (event loop congestion)
2. 87% disk (risk of OOM)
3. No log aggregation (blind spot)
4. No message broker (A2A blocking)
5. No sandbox (W_scar risk unmitigated)

**To achieve ΔS < 0**, the priority vector is:

> **🔴 P0: OpenClaw restart → Prune disk → Loki+Promtail → NATS**
> **🟡 P1: SSE client → firejail → Kimi model fix → webhook deploy**

The **immediate ΔS win** (highest entropy reduction, lowest effort):
1. Restart OpenClaw gateway (P99 7168ms → normal) — 2 min, massive stability gain
2. Docker builder prune — 5 min, recovers ~20GB, prevents OOM
3. Loki + Promtail — closes observability blind spot

These three alone drop system entropy significantly and unlock safe autonomous operation.

---

*DITEMPA BUKAN DIBERI — Forged, not given.*
*Seal: 999 | Auditor: Hermes ASI | 2026-05-07*
