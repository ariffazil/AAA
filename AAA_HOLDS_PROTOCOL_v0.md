<!--
SOT-MANIFEST
owner: Arif
last_verified: 2026-05-19
valid_from: 2026-05-19
valid_until: 2026-06-19
confidence: high
scope: /root/.openclaw/workspace
epistemic_status: CLAIM
-->

# AAA_HOLDS Protocol v0 — Closed-Loop Mechanics

**Status:** `SI v0 ACTIVE` | **File:** `AAA_HOLDS.md` | **Sovereign:** Arif

This document defines the **operational protocol** for the 888_HOLD queue that lives in `/root/.openclaw/workspace/AAA_HOLDS.md`.

---

## 1. The Problem (Now Solved)

**Before v0:**
1. Agent encounters something that requires 888_HOLD
2. Agent writes hold to `AAA_HOLDS.md`
3. Agent sends Telegram message to Arif: "Please check /holds"
4. Arif opens `AAA_HOLDS.md`, makes decision
5. Arif sends Telegram: "/approve 1" or "/reject 1"
6. **Agent never reads the decision back** — hold stays in Active table forever

**This was a broken loop.** The hold was a black hole.

---

## 2. The Closed Loop (v0 — BUILT 2026-05-19)

```
┌────────────┐    write    ┌─────────────┐    notify    ┌────────┐
│   Agent    │────────────▶│ AAA_HOLDS.md│─────────────▶│  Arif  │
│  (hold)    │             │  Active     │   Telegram   │(human) │
└────────────┘             └─────────────┘              └───┬────┘
                                                            │
                                               /approve N  │ /reject N
                                                            │
                                                            ▼
                                                    ┌──────────────┐
                                                    │ Move to      │
                                                    │ Completed    │
                                                    │ (Decision)   │
                                                    └──────┬───────┘
                                                           │
                                                           ▼
                                                    ┌──────────────┐
                                                    │ aaa-holds-   │
                                                    │ trigger.sh   │
                                                    │ (every 5min) │
                                                    └──────┬───────┘
                                                           │
                                                           ▼
                                                    ┌──────────────┐
                                                    │ OpenClaw     │
                                                    │ agent turn   │
                                                    │ executes     │
                                                    └──────┬───────┘
                                                           │
                                                           ▼
                                                    ┌──────────────┐
                                                    │ Mark executed│
                                                    │ State file + │
                                                    │ VAULT999 log │
                                                    └──────────────┘
```

### 2.1 Write Path (Agent)

When an agent encounters an 888_HOLD situation:

1. **Write** to `AAA_HOLDS.md` Active table:
   ```markdown
   | HOLD-2026.05.19.005 | 2026-05-19 12:34 | Deploy FalkorDB | Needs Arif's infra approval | PENDING |
   ```
2. **Notify** Arif via Telegram with the hold ID and summary.
3. **Set internal state** `awaiting_hold_resolution = True`.

### 2.2 Read Path (Automation)

Every 5 minutes, `aaa-holds-trigger.sh` runs via system cron:

1. **Parse** `AAA_HOLDS.md` Completed table.
2. **Filter** APPROVED holds not yet in `.aaa-holds-state.json`.
3. **If work found:** trigger `openclaw agent` turn with hold details.
4. **Agent executes** using available tools.
5. **Agent marks** hold as executed via `aaa-holds-mark-executed.py <id>`.
6. **Agent logs** to VAULT999 and notifies Arif via Telegram.

### 2.3 Human Override

Arif retains absolute veto:
- Edit `AAA_HOLDS.md` directly — change Decision to `HOLD` or `VOID`
- Stop the cron job: `sudo systemctl stop aaa-holds-trigger` (if systemd-wrapped)
- Or simply: send Telegram `/holds stop` (future command)

---

## 3. Components

| Component | Path | Purpose |
|-----------|------|---------|
| `AAA_HOLDS.md` | `/root/.openclaw/workspace/` | Canonical hold queue (human-readable) |
| `.aaa-holds-state.json` | `/root/.openclaw/workspace/` | Machine state (executed + pending IDs) |
| `aaa-holds-parser.py` | `/root/.openclaw/workspace/scripts/` | Deterministic parser — no LLM |
| `aaa-holds-trigger.sh` | `/root/.openclaw/workspace/scripts/` | Cron wrapper — triggers agent only when needed |
| `aaa-holds-mark-executed.py` | `/root/.openclaw/workspace/scripts/` | Agent calls this after execution |

---

## 4. Schema

### Active Holds
```
| ID | When | Request | Held because | Status |
```

### Completed Holds
```
| ID | When | Request | Decision | Decided by |
```
- `Decision`: `APPROVED` | `REJECTED` | `HOLD` | `VOID`

### Executed Holds
```
| ID | When | Request | Decision | Decided by | Executed at | Executed by |
```
- Optional human-visible audit trail
- Primary audit is `.aaa-holds-state.json` + VAULT999

---

## 5. Known Limitations

1. **File-based queue is not concurrent-safe.** If both agents write simultaneously, last-write wins. Mitigation: append-only rows, never edit in-place.
2. **Agent execution requires LLM reasoning.** Natural language hold requests are interpreted by the agent. Mitigation: keep requests specific, one-line, actionable.
3. **No auto-retry on failure.** If agent fails to execute, hold stays in pending state until manual cleanup. Mitigation: agent logs failure reason, Arif reviews.
4. **Cron is polling, not event-driven.** 5-minute latency max. Mitigation: acceptable for 888_HOLD (not real-time).

---

## 6. Build Log

| Date | Action | By |
|------|--------|-----|
| 2026-05-19 | Parser + trigger + state file created | Kimi Code CLI |
| 2026-05-19 | Cron entry added | Kimi Code CLI |
| 2026-05-19 | First live test | pending |

---

*DITEMPA BUKAN DIBERI — The loop is forged, not given.*
