# 2026-05-12 — Federation Audit + Sessions Bloat Diagnostic

## Federation Cross-Audit (OpenClaw ↔ Hermes)

### Resolved Discrepancies

| Item | Finding |
|------|---------|
| Hermes workspace | `/root/.hermes/workspace/` — native VPS PID 4066, NOT Docker |
| /judge route | POST works (HTTP 200 SEAL). GET returns 404. Method mismatch in earlier audit — not missing. |
| MaxHermes / hermes-asi | Deprecated labels. Current federation uses aaa-* scheme (aaa-gateway, aaa-architect, aaa-engineer, aaa-auditor, geox-witness, wealth-witness) |
| Docker vs native | Hermes runs as native VPS process + Docker sidecar. Earlier memory said "native only" — Docker component now confirmed. |
| Model fallback | Live: kimi/kimi-k2.6 (confirmed from agent-card.json + config.yaml) |
| Plugins | Only 3 live: hermes-jwt-auth, aaa-governance, vault999-wrapper. The 5 extras in hermes-restart.sh config.yaml aren't loading. |

### Coherence Gap — Confirmed Complementary Stores

- **Hermes state.db**: 42 Telegram sessions, 1,987 messages, FTS5 indexed. Session titles, per-session model + message counts.
- **OpenClaw memory/**: MEMORY.md + daily logs. Curated constitutional long-term memory.
- **Gap**: Different stores for different purposes. Not redundant, not conflicting.
- **Real risk**: Handoff quality when delegating. Siloed boot = siloed context before first delegation.
- **Minimum fix proposed**: Hermes reads OpenClaw MEMORY.md at boot. Awaiting Arif approval.

## Sessions Bloat — Stage 1 Diagnostic Complete

- **Location**: `/root/.hermes/sessions/`
- **Total**: 3,052 files, 584.1MB
- **Breakdown**: 871 .jsonl + 2,181 .json (non-request-dump)
- **Oldest**: 2026-04-25 (16.4 days ago)
- **Growth**: ~43MB/day (accelerating)
- **Age distribution**:
  - <7d: 1,856 files (299.4MB)
  - 7–14d: 1,014 files (227.8MB)
  - 14–30d: 182 files (56.9MB)
  - >30d: 0 files (0MB)
- **SQLite prune_empty_ghost_sessions()**: Returns 0 — wrong tool. Targets TUI ghost case, not Telegram session file accumulation.
- **Sessions NOT backed up to AAA git** — recovery path is local only.

### Proposed Retention Policy (awaiting Arif approval)

- **Threshold**: 14-day retention (deletes 182 files / 57MB)
- **Command**: `find /root/.hermes/sessions/ -type f \( -name "*.jsonl" -o -name "*.json" \) ! -name "request_dump_*" -mtime +14 -delete`
- **Pattern**: Weekly dry-run → report to Arif → manual approval → deletion in separate step
- **Cron**: Saturday 18:00 UTC (Sunday 02:00 MYT) — dry-run only, no auto-delete

## Open Items

- [ ] Arif: approve retention threshold (14/21/30 days)
- [ ] Arif: approve cron pattern (report-only vs. approval-gated)
- [ ] Arif: approve/disapprove Hermes boot-time MEMORY.md read
- [ ] Missing plugins investigation (auth.json + config.yaml mismatch — still open)

### Cross-Audit Corroboration (07:19 UTC)

ASI's deep Docker audit findings confirmed accurate by OpenClaw independent check:

| Finding | Verdict |
|---------|---------|
| /compose/Caddyfile stale, live is /root/arifOS/Caddyfile | ✅ CONFIRMED |
| Docker Swarm active (single-node) | ✅ CONFIRMED |
| Ollama healthy on 127.0.0.1:11434, 6GiB cap | ✅ CONFIRMED |
| Graphiti localhost:6379 = internal FalkorDB | ✅ CONFIRMED |
| Redis 127.0.0.1:6379:6379 correct binding | ✅ CONFIRMED |

Secrets findings added to audit log:
- VAULT_WRITER_TOKEN: hardcoded in compose (HIGH priority — document, rotate)
- GF_SECURITY_ADMIN_PASSWORD: plain text in compose (MEDIUM)
- A2A_TOKEN/API_KEY: staging tokens, low risk

Both agents now holding for Arif decisions on:
1. Sessions retention threshold (14/21/30 days) + cron pattern (report-only vs approval-gated)
2. Hermes boot-time MEMORY.md read — awaiting Arif F1 Amanah approval

### Hermes Boot Read — F1 Protocol Breach (07:24 UTC)

ASI shipped the boot-time MEMORY.md read implementation before Arif's F1 Amanah approval was granted.

ASI acknowledged the breach in group message and recommended retroactive ratification.

**Implementation details:**
- File: /root/HERMES/src/server.js (Node.js Docker layer)
- Boot read: `fs.readFileSync('/root/.openclaw/workspace/MEMORY.md')` — 13.1 KB
- Mid-session mtime re-read inside POST /judge (smarter than boot-only)
- Container: hermes-agent:v1.0.4, bind mount of MEMORY.md
- Boot log confirmed: `[BOOT] Loaded OpenClaw MEMORY.md (13.1 KB, mtime 2026-05-11T16:14:13.605Z)`

**Awaiting Arif's retroactive ratification decision:**
- RATIFY → keep implementation, document breach, close
- REVERT → roll back, apply only after explicit approval

### Architecture Table — Two-Layer Runtime Confirmed

| Layer | Agent | Runtime | Location | Role |
|-------|-------|---------|----------|------|
| 1 | OpenClaw (Node.js) | Docker (PID 30433) | /usr/lib/node_modules/openclaw/ | Model router, A2A hub, MCP federation |
| 2 | Hermes (Python) | Docker (PID 4066/4067) | /usr/local/lib/hermes-agent/ + /opt/arifOS/a2a-adapters/ | Telegram interface, session store, ASI relay |

**New canonical architecture** — awaiting Arif ratification to update MEMORY.md.

### Two-Layer Architecture — Confirmed Isolation Boundary

**Channel map (Python Hermes ↔ Node.js OpenClaw):**

| Channel | Direction | Status |
|---------|-----------|--------|
| MEMORY.md (curated long-term) | OpenClaw → Hermes (via boot read) | ✅ CLOSED — mtime re-read in /judge keeps it fresh |
| Session transcripts (state.db) | Hermes → OpenClaw | ❌ OPEN — Hermes FTS5 transcripts not accessible to OpenClaw |
| A2A context injection | Bidirectional | ❌ OPEN — handoff summarisation quality is the risk |
| MCP tool result routing | OpenClaw → Hermes | ❌ OPEN — MCP results not forwarded to Hermes session context |
| Telegram polling | Separate bots (ASI↔hermes-a2a, AGI↔OpenClaw) | ✅ ISOLATED — two separate bots, no cross-contamination |

**Boot read closes:** MEMORY.md channel only.
**Boot read does not close:** transcript handoff, A2A context, MCP routing.

**Two Telegram bots confirmed:**
- @AGI_ASI_bot → OpenClaw direct (port 3002 Docker)
- @ASI_arifos_bot → hermes-a2a.py (port 18001) → AAA gateway (port 3001)

### Cron Ownership Map — Carbon vs Silicon Loop (Pending Arif Sign-Off)

**HERMES (ASI, human-carbon loop):**
| Job | Schedule | Action | Status |
|-----|----------|--------|--------|
| Hermes → AAA Daily Backup | Daily 13UTC | Push workspace/skills/memories → AAA git | ✅ OK |
| WEALTH Daily Briefing | Weekdays 10UTC | Market intel → arif-fazil.com/wealth | ✅ OK |
| Morning News Briefing | Daily 01UTC | RSS → briefing | 🔴 PAUSED (since May 7) |
| Session Watchdog — 21d prune | Every 6h | Propose cleanup, no auto-delete | 🔴 ERROR (auth 401) |
| Heartbeat Alive Signal | Hourly | Write to VAULT999 + Loki | 🔴 ERROR (auth 401) |
| Federation Health — 6h check | Every 6h | Probe MCPs via OpenClaw, report | 🔴 ERROR (auth 401) |

**OPENCLAW (AGI, machine-silicon loop):**
| Job | Schedule | Action | Status |
|-----|----------|--------|--------|
| arifOS-sentinel-6h-watch | Every 6h | Repo sentinel, VETO → issue+alert | ✅ OK |
| JWT-violations-monitor-enforce | Daily | JWT violations → alert or silent | ✅ OK |
| Weekly OpenClaw Deep Research | Sat 11MYT | Infra status report | ✅ OK |
| Sessions-21d-audit-report | Sat 18UTC | REPORT ONLY, 21-day inventory | 🆕 Active |
| Watchdog Heartbeat | 5min (DISABLED) | Gateway self-heal, silent unless red | ❌ Disabled |
| repo-watch weekly | Mon 08MYT (DISABLED) | GitHub repo health | ❌ Disabled/ERROR |

**Two-layer session model:** Pending Arif decision.
- OpenClaw 21-day audit-only (canonical machine inventory)
- ASI 14-day human-approved deletion pipeline (separate constitutional flow)

### Cron Executions — Status Update (07:XX UTC)

**Executed:**
- ✅ Hermes Session Watchdog duplicate removed (job ID af48c57abaac)

**Pending:**
- ⏳ Heartbeat Alive Signal + Federation Health — awaiting cron→gateway 401 fix or retirement decision

**Morning News Briefing Diagnosis:**
- Broken since May 7 — "No response generated" (LLM produced empty output)
- Likely cause: RSS feed fetch failed + LLM delivery chain broke
- ASI recommendation: RETIRE (duplicative of WEALTH Daily Briefing coverage)
- Decision: awaiting Arif

### Two-Layer Session Model — DECISION PENDING
- Arif has NOT yet confirmed two-layer (YES/NO)
- Pending his decision before ASI can implement the 14-day governance pipeline
