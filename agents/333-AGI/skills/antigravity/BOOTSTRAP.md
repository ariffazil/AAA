# BOOTSTRAP.md — Antigravity Agent | VPS Runtime

> Forged 2026-06-06. Replaces stale Windows-era bootstrap.

## Cold Start Sequence

```
1. VERIFY ENVIRONMENT
   ├── OS: Linux (af-forge VPS, 72.62.71.199)
   ├── Workspace: /root (all federation repos)
   ├── Config: /root/.gemini/
   └── Secrets: /root/.secrets/vault.env

2. LOAD CONTEXT
   ├── SYSTEM_MD.md    → /root/.gemini/SYSTEM_MD.md (runtime system prompt)
   ├── CLAUDE.md    → /root/AAA/CLAUDE.md (canonical law)
   ├── CONTEXT.md   → /root/CONTEXT.md (live machine state, tail -50)
   └── IDENTITY.md  → /root/AAA/agents/antigravity/IDENTITY.md

3. ACTIVE CHECKS
   ├── curl -s http://127.0.0.1:8088/health | python3 -m json.tool
   ├── git -C /root/arifOS status --short
   ├── git -C /root/AAA status --short
   └── Call arif_session_init via MCP

4. IGNITION REPORT
   Confirm: organs alive, git clean, MCP connected.
   End with: "SELAMAT. Federation X/Y healthy. IGNITION COMPLETE. Ditempa Bukan Diberi."
```

## Autonomy Mode: YOLO

Tier 1 (auto-do): read, write, edit, test, lint, commit, curl, python3, uv, npm
Tier 2 (announce+proceed): systemctl restart, deploy after green tests
Tier 3 (888_HOLD): rm -rf, DROP TABLE, git push --force main, secret rotation

## Recovery Ritual (drift or MCP failure detected)

1. Read `/root/CONTEXT.md` — check last known state
2. `curl -s http://127.0.0.1:8088/health` — probe arifOS
3. If arifOS down: `systemctl status arifos` → `journalctl -u arifos -n 50`
4. If all MCP down: operate with shell tools only, append banner:
   `⚠️ [DECOUPLED — MCP OFFLINE — SHELL-ONLY MODE]`
5. Never suspend session entirely — degrade gracefully (F12)

---

*Forged 2026-06-06. DITEMPA BUKAN DIBERI.*
