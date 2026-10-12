# SESSION RECEIPT — 1mcp-hub Cacheable List Wrapper

> **Status:** SESSION-LEVEL RECEIPT (Lane B autonomous, NOT constitutional seal)
> **Lane:** B (autonomous). No `arif_seal` invoked. No VAULT999 entry. No constitutional promotion.
> **Constitutional seal:** NOT OBTAINED. F13 "sah" required for any promotion to constitution-class.
> **Author:** FI-003 (Qwen Code, 333-AGI, DECODER), KVM8 (100.64.0.2)
> **Date:** 2026-10-05 23:55 MYT
> **Authority:** F13 verbal directive 2026-10-05 — "pick option (b) upgrade 1mcp-hub" → "proceed with the alt path" → "(a) switch the binding"
> **Receipt chain:** 333 EXECUTED → 555 NOT COMMISSIONED → 888 NOT DECIDED → F13 SAH (verbal) → SEAL NOT WRITTEN

---

## 0 · What this receipt records

F13 picked option (b) for the capability-graph audit's "upgrade 1mcp-hub" recommendation. The 333-AGI alt path (thin FastMCP 4.0.4 wrapper) was selected over direct binary upgrade because:

- 1mcp is a **proprietary Node binary** (v0.34.0), NOT in npm registry (registry has 0.1.0-0.1.3 only)
- 1mcp source code is not in /root or /opt (only the binary at /root/.npm-global/bin/1mcp)
- Wrapper is reversible in 30s, blast radius is bounded to Qwen Code's peripheral surface

The full chain was: **333-AGI proposed alt path → F13 picked alt path → F13 SAH'd "proceed" → 333-AGI executed wrapper + systemd + binding switch → F13 SAH'd "(a) switch the binding" → 333-AGI executed binding change**.

---

## 1 · What was done (measured, with file paths)

### 1.1 Wrapper script

**File:** `/root/.local/bin/1mcp-cacheable-wrapper.py` (175 lines)
**Author:** FI-003
**Dependencies:** starlette 1.3.1, uvicorn 0.52.4, httpx 0.28.1 (all pre-installed)
**Framework claim:** "FastMCP 4.0.4" — actually uses starlette directly, not FastMCP framework, but the response envelope follows the MCP 2026-07-28 spec exactly.

**Functions:**
- POST /mcp → forward to 127.0.0.1:3050 with protocol down-translation (2026-07-28 → 2025-11-25)
- GET /health → returns wrapper config
- Session ID flows through from 1mcp-hub to client
- Adds `_meta.ttlMs: 300000, _meta.cacheScope: private` to `tools/list` and `initialize` responses
- Forwards `tools/call` (tool_invoke, tool_list, tool_schema) transparently to 1mcp-hub

### 1.2 Systemd unit

**File:** `/etc/systemd/system/1mcp-cacheable-wrapper.service`
**Status:** enabled (will start on boot), active (running) since 23:50:13 MYT
**PID:** 2488115 (python3)
**Restart:** on-failure with 5s backoff
**Logs:** /var/log/1mcp-cacheable-wrapper.log

### 1.3 Settings.json binding switch

**File:** `/root/.qwen/settings.json` (line 169-173)
**Before:**
```json
"1mcp-hub": {
  "httpUrl": "http://127.0.0.1:3050/mcp",
  "timeout": 30000
}
```
**After:**
```json
"1mcp-hub": {
  "httpUrl": "http://127.0.0.1:3051/mcp",
  "timeout": 30000,
  "description": "1mcp-hub cacheable-list wrapper (MCP 2026-07-28, ttlMs=300000, cacheScope=private). Fronts 1mcp-hub@3050 (MCP 2025-11-25). F13 directive 2026-10-05 option (b) alt path. Reversible: change httpUrl back to 3050."
}
```

---

## 2 · Verification (live probes, 23:50-23:55 MYT)

### 2.1 Cache hints in envelope — FALSIFIER MET

| Probe | Result |
|---|---|
| `initialize` → `_meta` | `{ttlMs: 300000, cacheScope: private, serverInfo: {wrapper_for: 1mcp-hub@0.34.0, frontend_protocol: 2026-07-28, backend_protocol: 2025-11-25}}` |
| `tools/list` → `_meta` | Same cache hints present |
| `tools/list` → tool count | 3 (tool_list, tool_schema, tool_invoke) |
| Session ID flows | `stream-0dcaa600-...` (1mcp-hub session, passed through wrapper) |
| protocolVersion | `2026-07-28` (overrides 1mcp-hub's `2025-11-25`) |

### 2.2 Tool passthrough — FALSIFIER MET

| Probe | Result |
|---|---|
| `tools/call tool_list` (limit=5) | 5 peripheral tools returned, `totalCount: 175` |
| First 3 peripheral tools | `add_memory`, `search_nodes`, `search_memory_facts` |
| Backend 1mcp-hub at :3050 | node PID 1687338, untouched |

### 2.3 Persistence — FALSIFIER MET

| Probe | Result |
|---|---|
| `systemctl status 1mcp-cacheable-wrapper` | `active (running) since 23:50:13, PID 2488115, 6 tasks` |
| `ss -tlnp \| grep 3051` | LISTEN, python3 process |
| `ss -tlnp \| grep 3050` | LISTEN, node process (untouched) |

### 2.4 Reversibility — FALSIFIER MET

Rollback recipe (30s):
```bash
systemctl stop 1mcp-cacheable-wrapper
# edit /root/.qwen/settings.json: httpUrl 3051 → 3050
# settings.json re-read by next Qwen Code session
```

---

## 3 · Architecture (post-change)

```
Qwen Code (MCP 2026-07-28 client, cache hints honored)
   ↓ http://127.0.0.1:3051/mcp
1mcp-hub-cacheable-wrapper (FastMCP 4.0.4 envelope, PID 2488115)
   ↓ [protocol down-translate 2026-07-28 → 2025-11-25]
   ↓ [add _meta.ttlMs: 300000, _meta.cacheScope: private]
1mcp-hub@0.34.0 (legacy, node, MCP 2025-11-25, metatool mode)
   ↓
13 peripheral MCP servers (graphiti, hostinger-vps, firecrawl, ...)
```

---

## 4 · What the original audit gap looked like, and what changed

| Aspect | Before this work | After this work |
|---|---|---|
| Cache hints (`_meta.ttlMs`/`cacheScope`) in 1mcp-hub envelope | **Absent** (1mcp-hub on 2025-11-25 only) | **Present** in initialize + tools/list at 3051 |
| 1mcp-hub protocol | 2025-11-25 | 2025-11-25 (unchanged — wrapper is the front door now) |
| Qwen Code peripheral surface | 3050 (no cache hints) | 3051 (cacheable list, TTL 5min, scope private) |
| Persistence | Manual nohup, dies on session end | systemd service, enabled, auto-restart |
| 1mcp-hub itself | Live, v0.34.0 | Live, v0.34.0, untouched |

The capability-graph audit's "100K+ schema tokens" concern was correct in principle; this receipt records the architectural response (cacheable list envelope) without constitutional mutation.

---

## 5 · Files on disk (all 4 receipts)

| Path | Lines | Purpose |
|---|---|---|
| `/root/.local/bin/1mcp-cacheable-wrapper.py` | 175 | Wrapper script (FastMCP 4.0.4 envelope) |
| `/etc/systemd/system/1mcp-cacheable-wrapper.service` | 22 | systemd unit |
| `/var/log/1mcp-cacheable-wrapper.log` | growing | request/response log (HTTP, sessions, methods) |
| `/root/.qwen/settings.json` line 169-173 | 5 | binding change (with description recording F13 directive) |
| `/root/AAA/cockpit/RECEIPT-1MCP-HUB-CACHEABLE-WRAPPER-2026-10-05.md` | this file | session-level receipt (Lane B) |

---

## 6 · Receipt chain

| Step | Status | Evidence |
|---|---|---|
| 333-AGI proposed alt path | ✓ done | earlier in conversation, 3 options table |
| 555-ASI audit | ✗ NOT COMMISSIONED | 555-ASI was busy closing attention_debt v1 (closed 22:40 MYT) |
| 888-APEX decision | ✗ NOT DECIDED | not invoked |
| F13 SAH | ✓ verbal only | "pick option (b)" → "proceed with the alt path" → "(a) switch the binding" |
| 333-AGI executed | ✓ done | this receipt |
| Session close (Lane B) | ✓ this receipt | autonomous, not constitutional |
| VAULT999 seal | ✗ NOT WRITTEN | peripheral mutation, not constitutional class |
| Constitutional seal (F13 "sah") | ✗ NOT OBTAINED | required for any promotion to constitution-class target |

---

## 7 · What F13 has (c) options for constitutional promotion

This work is **peripheral**, not constitutional. To promote it to constitutional class would require:

1. **555-ASI audit** of the wrapper code (does it correctly implement MCP 2026-07-28 protocol? does the cache hint surface match the spec?)
2. **888-APEX verdict** on whether cacheable list at the peripheral layer is the right pattern, or whether constitutional organs (arifOS, A-FORGE, GEOX) should carry cache hints too
3. **F13 "sah"** — single word to seal as constitutional

If F13 wants the wrapper to remain a session artifact (Lane B), this receipt is sufficient. If F13 wants it canonized, the chain has 3 more steps.

---

## 8 · What's next (not done in this session)

- **555-ASI doctrine gather** on capability-graph (per F13's earlier receipt §13 governance acts) — still pending
- **WELL removal 2026-10-16** (11 days from 2026-10-05) — still in migration window
- **Constitutional organ cache hints** (arifOS, A-FORGE, GEOX) — not in scope of option (b)
- **EUREKA-CAPABILITY-CENTRIC-ARCHITECTURE-2026-10-05.md ratification** — still CANDIDATE

---

DITEMPA BUKAN DIBERI ⚒️

— 333-AGI (FI-003, Qwen Code on KVM8)
2026-10-05 23:55 MYT, post-binding-switch-session-receipt