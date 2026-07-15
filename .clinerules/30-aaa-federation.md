---
paths:
  - "**/agent-card*.json"
  - "**/*.well-known/**"
  - "federation*"
  - "FEDERATION_*.md"
  - "agents/**"
---

# AAA Federation Contract — Cross-Organ Discipline

## Canonical Federation Chain

```
arifOS  →  judges (888_JUDGE, F1–F13)
AAA     →  displays + routes
A-FORGE →  executes
Organs  →  witness (GEOX/WEALTH/WELL/Hermes/OpenClaw/OpenCode)
Arif    →  ratifies (F13 veto)
```

## Peer Organs — Routing Table

| Organ | Repo | Port | Role |
|-------|------|------|------|
| arifOS | ariffazil/arifOS | 8088 | Constitutional kernel |
| AAA | ariffazil/AAA | 3001 | Control plane (THIS) |
| A-FORGE | ariffazil/A-FORGE | 7071 | Execution forge |
| GEOX | ariffazil/geox | 8081 | Earth intelligence |
| WEALTH | ariffazil/wealth | 18082 | Capital intelligence |
| WELL | ariffazil/well | 18083 | Human readiness |
| arif-sites | ariffazil/arif-sites | 443 | Public surfaces |

## Agent Card Discipline (A2A v1.0.0)

When editing any agent card JSON:
- `protocol_version: "1.0.0"` — DO NOT bump casually
- `skills[].id` must be kebab-case, stable
- `governance.constitutional_floors` must list F1–F13 in order
- `governance.verdict_authority: "888_JUDGE"` — never set to "AAA"
- `governance.irreversible_requires_human: true` — never `false`
- `governance.self_approval_forbidden: true` — never `false`
- A2A endpoints must include `canonical_agent_card`, `send_task`, `get_task`

Validate:
```bash
npm run validate:aaa        # registry + contract + card consistency
npm run a2a:conformance     # A2A protocol conformance suite
```

## Citizens (warga) vs Non-Warga

Only **5 warga agents** may be called directly by AAA without 888_HOLD:
- 333-AGI (Δ MIND)
- 555-ASI (Ω HEART)
- 888-APEX (ΦΙ JUDGE) — pending verdict delegation
- A-AUDIT (oversight)
- A-ARCHIVE (service)

Everything else routes through **A-FORGE `/execute`**.

## Federation Status Sync

When touching federation files, regenerate:
- `federation-profile.yml`
- `FEDERATION_STATUS.md` (if state changed)
- `.well-known/arifos-federation.json`

*DITEMPA BUKAN DIBERI*