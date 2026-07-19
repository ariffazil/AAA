# CANONICAL COUNT VOCABULARY — arifOS Federation

> **SOT:** 2026-07-19 · **seal_seq:** TBD
> **Rule:** Live `tools/list` + `/health` beats any static count in prose.
> **DITEMPA BUKAN DIBERI**

## Purpose

Every organ in the arifOS federation exposes tools. But "how many tools?" has no single answer — it depends on which surface you're asking. This document defines the canonical vocabulary so agents, operators, and auditors speak the same language.

## Count Taxonomy

| Surface | Definition | Who sees it |
|---------|-----------|-------------|
| **sovereign_public_wire** | Tools exposed on the public MCP endpoint after all governance filters. This is the count that matters for external agents. | Public internet, ChatGPT, external MCP clients |
| **authenticated_wire** | sovereign_public_wire + tools requiring bearer auth but visible to authenticated clients | Authenticated MCP clients |
| **internal_superset** | All registered tools including internal/diagnostic/admin tools hidden from public facade | Kernel operators, audit |
| **registry_total** | All tools ever registered (including deprecated, quarantined, mode-gated) | Registry audit |
| **diagnostic** | Internal health, debug, and introspection tools | System operators only |

## Per-Organ Canonical Counts (T₁: 2026-07-19)

| Organ | sovereign_public_wire | authenticated_wire | internal_superset | registry_total | Verified source |
|-------|----------------------|-------------------|-------------------|----------------|-----------------|
| **arifOS** | 8 | 8 | 23 | 60 | `/health` surface_consistency CONSISTENT |
| **A-FORGE** | 52 | 52 | 111 | 111 | `/health` on :7072 (52 stateless tools) |
| **AAA** | N/A (A2A gateway) | N/A | N/A | N/A | Cockpit + A2A only |
| **GEOX** | 24 | 24 | 24 | 24 | `/health` tools_loaded=24 canonical_tools=24 |
| **WEALTH** | 20 | 20 | 20 | 20 | `/health` tools_loaded=20 canonical_tools=20 |
| **WELL** | 8 | 8 | 22 | 22 | `/health` tool_count=8, canonical_tools=22 |

## Rules

1. **Never use an unqualified number.** Always specify the surface: "8 public tools" not "8 tools".
2. **The badge shows sovereign_public_wire count.** Update README badges to match live health.
3. **Count drift is a P1 incident.** If `/health` disagrees with a README, the README is wrong.
4. **Live truth always wins.** Run `curl :<port>/health` before quoting any count.
5. **"tools/list" on the public endpoint = sovereign_public_wire.** This is the canonical source.

## Previous Drift (Fixed 2026-07-19)

| Organ | Old claim | New truth | Fix |
|-------|----------|-----------|-----|
| WELL README badge | 27 tools | 8 tools (sovereign_public_wire) | Badge updated |
| GEOX physics | sha256:missing | sha256:9dba3e39... | Symlink created |
| A-FORGE AAA context | "40+" | 52 (sovereign_public_wire) | Documented |

## Verification

```bash
# One-liner to verify all counts against live health
for svc in arifos:8088 aforge-mcp:7072 geox:8081 wealth:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://localhost:$port/health" | python3 -c "
import json,sys; d=json.load(sys.stdin)
tc=d.get('tools_loaded',d.get('tool_count',d.get('stateless_tools','?')))
print(f'{name}: {tc}')
"
done
```

---

*Maintained by AAA Control Plane. Live health beats this document.*
