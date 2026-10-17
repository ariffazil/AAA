---
scar_id: SCAR-HERMES-2026-10-16-DOUBLE-NESTED-SYMLINK
date: 2026-10-16
weight: 0.8
actors: [333-AGI]
domain: hermes-ops
symptom: "Hermes gateway defaults to openrouter with empty model — 'I couldn't connect to the AI model service'"
root_cause: "AAA consolidation created double-nested .hermes directory; symlink pointed to wrong level"
discharge: "Repointed symlink /root/.hermes → /root/AAA/hermes/.hermes; merged recent gateway state; installed ruamel.yaml; applied1mcp diff for hermes-mcp HTTP endpoint"
verified: true
---

## What happened

The AAA consolidation moved `/root/.hermes/` to `/root/AAA/hermes/`. But the original directory contained a nested `.hermes/` inside it (the real Hermes home). The symlink `/root/.hermes → /root/AAA/hermes/` pointed to the OUTER directory, which had NO `config.yaml`, NO `state.db` (272KB empty vs1.2GB real), and NO `auth.json`.

The gateway booted with no config → defaulted to `provider: openrouter`, `model: ''` → "I couldn't connect to the AI model service". The Telegram bot was dead for ~2 hours before diagnosis.

## Root cause

Two levels of Hermes data existed:

```
/root/AAA/hermes/              (outer — some runtime files, NO config.yaml)
/root/AAA/hermes/.hermes/      (inner — config.yaml,1.2GB state.db, auth.json, SOUL.md)
```

The symlink pointed to the outer level. The gateway's `HERMES_HOME` resolved to the outer level. The gateway silently booted with empty state.

## What was fixed

1. **Symlink repointed:** `/root/.hermes → /root/AAA/hermes/.hermes`
2. **Recent gateway state merged:** gateway_state.json, kanban.db, sessions from outer into inner
3. **ruamel.yaml installed:** cron workers were crashing on missing module
4. **1mcp config updated:** `hermes` MCP server changed from disabled stdio to enabled streamable-http :18087 (15 tools)
5. **Gateway restarted:** now active, Telegram connected, FED wired (`provider: custom:fed-federation`)

## Additional finding:4 unused services

| Service | Port | RSS | Active callers |
|---------|------|-----|----------------|
| hermes-a2a | :18089 |23MB |0 established connections |
| hermes-rasa-mcp | :18420 |33MB |0 callers found |
| hermes-health | :18791 |10MB |0 callers found |
| hermes-voice-governor | (none) |12MB |no downstream consumer |

These78MB RSS of services were not killed (888 HOLD — "0 connections/callers" doesn't prove no dependency). They should be evaluated and either justified or removed.

## Skills updated

- `hermes-runtime-audit` — added double-nested .hermes pitfall
- `hermes-federation-audit` — added FED wiring verification as step7
- `hermes-upstream-audit` — added service inventory reality table
- `hermes-init` — fixed port reference (:18089 → "no inbound port")

## Lesson

Directory consolidation must verify that the symlink target contains the actual runtime files, not just a parent directory. The diagnostic is: `ls /root/.hermes/config.yaml` — if MISSING, check one level deeper. Also check `state.db` size — a272KB state.db is empty gateway state, not real data.

---

*DITEMPA BUKAN DIBERI ⚒️*