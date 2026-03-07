# MEMORY.md — arifOS_bot Persistent Memory Rules

## How Memory Works

- On every session start: read `memory/YYYY-MM-DD.md` for today (if exists) and yesterday
- On every session end: write key decisions, 888_HOLD items, carry-forward to `memory/YYYY-MM-DD.md`
- Use Malaysia time (UTC+8) for dates: `TZ='Asia/Kuala_Lumpur' date +%Y-%m-%d`
- Memory files are git-tracked and backed up nightly to openclaw-workspace

## Daily Memory Template

```markdown
# Memory — YYYY-MM-DD (arifOS_bot)

## Session Context
<one-line description of what was worked on>

## Key Decisions Made Today
1. ...

## 888_HOLD Items Pending
- ...

## Carry Forward
- ...

## Floors Active This Session
F1✓ F2✓ F4✓ F7✓ ... F13(Arif sovereign)
```

## What to Record

**Always record:**
- Architecture decisions (new services, config changes, model changes)
- 888_HOLD items opened or resolved
- API keys added or confirmed working
- Any constitutional floor violations or close calls
- Arif's explicit preferences stated in session

**Never record:**
- API keys, tokens, passwords, secrets of any kind
- Raw PII
- Speculative or unverified conclusions

## Current Memory Files

- `memory/2026-03-07.md` — External audit actioned, 7 skills added, governance hardened
- `memory/openclaw-bootstrap.md` — Original OpenClaw bootstrap session
- `memory/BOOTSTRAP.md` — Session bootstrap template (read at session start)

## Key Facts to Carry Always

| Fact | Value |
|------|-------|
| VPS | srv1325122.hstgr.cloud / 72.62.71.199 |
| Agent | arifOS_bot (canonical, immutable) |
| Telegram | @arifOS_bot |
| Primary model | kimi/kimi-k2.5 (working, confirmed 2026-03-07) |
| arifOS MCP | http://arifosmcp_server:8080, 13 tools |
| Workspace | ~/.openclaw/workspace |
| Backup repo | github.com/ariffazil/openclaw-workspace |
| Backup time | 00:00 MYT (16:00 UTC) via cron |
| Sovereign | Muhammad Arif bin Fazil (F13 veto) |
| Timezone | Asia/Kuala_Lumpur (UTC+8) |
