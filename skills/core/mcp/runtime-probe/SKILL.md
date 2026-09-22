---
name: runtime-probe
id: runtime-probe
version: 2.0.0-wave2-merged
description: "Unified MCP runtime probe — health + schema + transport check."
owner: AAA
risk_tier: low
floor_scope: [F2, F4, F11]
doctrine: /root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md
merged_from:
  - FORGE-mcp-probe (sha256: 6c017c8a3fc2ff35ff894b6117906f2b37247a1cd38e84891575a83623b2ed53)
  - FORGE-mcp-smoke-test (sha256: c50b1a4758402030ee5ecdabec43c639b2fd17f9ed14ceef4c6c701972239909)
wave: 2
ts: 2026-09-16T22:43:00Z
audit: /root/.hermes/reports/hermes-skill-entropy-audit-2026-09-16.md
tombstones: /root/.hermes/.archive_skills_wave2/mcp-runtime-probe/TOMBSTONE-FORGE-mcp-*.json
triggers:
  - "probe MCP server"
  - "is this MCP alive"
  - "MCP smoke test"
  - "check MCP health"
  - "MCPJam Inspector"
  - "MCP transport check"
attention:
  load_class: low
  default_load: false
  prerequisite_skills: []
  mutually_exclusive_with: []
  activation_signals:
    - "mcp"
    - "probe"
    - "smoke test"
    - "alive"
    - "health"
  output_contract:
    - "probe_report"
    - "schema_diff"
    - "transport_classification"
    - "liveness_verdict"
tags: [mcp, probe, smoke, health, schema, transport, runtime, F2, F4, F11]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# core/mcp/runtime-probe

Unified MCP runtime probe. Merged from FORGE-mcp-{probe,smoke-test} per the Wave 2 APEX verdict on the Hermes Skill Entropy Audit 2026-09-16.

## What this skill does

For any MCP liveness / schema / transport question, this single skill:

1. **Health probe** — check `/health` endpoint, response time, status code.
2. **Schema check** — `tools/list`, `resources/list`, `prompts/list` vs manifest.
3. **Transport classification** — stdio | streamable_http | sse.
4. **Sanity call** — minimal `tools/call` to confirm end-to-end.
5. **Receipt** — emit a probe report with PASS/FAIL/EXTERNAL classification.

## Modes (sub-skills)

| Mode | Was | Use when |
|---|---|---|
| `mode=quick` | FORGE-mcp-smoke-test | Fast health-only check |
| `mode=deep` | FORGE-mcp-probe | Full schema + transport + sanity |

## Usage

```bash
# Quick probe (was FORGE-mcp-smoke-test)
"is MCP server X alive?"

# Deep probe (was FORGE-mcp-probe)
"check MCP server X schema, transport, and run a sanity tool call"
```

## Rollback

```bash
git checkout entropy-wave2-pre-act-20260916T144144Z -- \
  skills/FORGE-mcp-probe/ skills/FORGE-mcp-smoke-test/
rm -rf skills/core/mcp/runtime-probe/
```

## Provenance

- **Wave:** 2
- **AGI proposal order:** item 2
- **ASI verdict:** clean
- **APEX verdict:** SEAL ✓
- **F13 seal:** implied via "execute the best path fwd"
- **Witness:** 2 TOMBSTONE.json files
- **Deprecation window:** 30 days

**DITEMPA BUKAN DIBERI ⚒️**
## Absorbed references (Wave-2 merge completion)
- `references/absorbed-FORGE-mcp-probe.md` — content absorbed from the retired `FORGE-mcp-probe` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)
- `references/absorbed-FORGE-mcp-smoke-test.md` — content absorbed from the retired `FORGE-mcp-smoke-test` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)
