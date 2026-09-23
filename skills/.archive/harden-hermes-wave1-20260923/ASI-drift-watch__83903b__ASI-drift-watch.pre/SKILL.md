---
name: ASI-drift-watch
id: asi-drift-watch
version: 1.1.0
owner: 555-ASI
risk_tier: low
description: Detect drift between federation source and runtime. Reads organ topology
  from /root/AAA/federation/organs.yaml (canonical SOT), probes live health endpoints,
  and compares git SHAs. No hardcoded paths or ports — everything derived from live registry.
when_to_use: After deploy, when organ behavior surprises you, weekly health audit,
  before any "is it running what I think?" question.
disable-model-invocation: false
allowed_tools:
- Bash
- Read
- Grep
floor_scope:
- F1
- F2
- F4
- F7
- F11
autonomy_tier: T0
capability_tier: fed-agent-subagent
ecology_state: WARM
---
# Drift Watch — Probe-Based (v1.1.0)

A service running is not the same as a service running what you think. This skill surfaces that gap using LIVE organ registry data — zero hardcoded paths or ports.

## Canonical SOT

The organ registry at `/root/AAA/federation/organs.yaml` is the single source of truth for organ names, source paths, runtime locations, ports, and health endpoints. Read it FIRST.

```bash
# Discover all organs
python3 -c "
import yaml, json
with open('/root/AAA/federation/organs.yaml') as f:
    reg = yaml.safe_load(f)
for o in reg.get('organs', []):
    print(f'{o[\"id\"]} src={o.get(\"source_path\",\"?\")} runtime={o.get(\"runtime_path\",\"?\")} port={o.get(\"port\",\"?\")}')
"
```

## Steps

1. **Read organ registry** — `cat /root/AAA/federation/organs.yaml` or use the python snippet above. This gives you source_path, runtime_path, and port for every organ.

2. **For each organ** with a source_path:
   - `git -C <source_path> rev-parse HEAD` → source SHA
   - `cat <runtime_path>/.git_commit 2>/dev/null` → runtime SHA (if file exists)
   - Compare → if mismatch → DRIFT

3. **For each organ** with a port:
   - `curl -sf --max-time 2 http://localhost:<port>/health` → probe live health
   - Parse the software_release block for deployed_commit
   - Cross-reference with source SHA

4. **If DRIFT detected:**
   - Source newer than runtime → `make deploy-local` candidate (per-organ)
   - Runtime newer than source → runtime patch not in source → 888 HOLD
   - Runtime `.git_commit` missing → warn, treat source as truth

5. **Also check (from registry, not hardcoded):**
   - Caddy port map: `/etc/caddy/Caddyfile` (sovereign-locked)
   - systemd units: `systemctl list-units --type=service | grep -E 'arifos|aforge|geox|wealth|well|aaa|arifflow'`
   - env file presence: `/root/.secrets/kunci-mas.env` (mode 600)

## Organ topology (derived live from registry — this table is a CACHED EXAMPLE, probe for truth)

| Organ | Source discovery | Runtime discovery | Health probe |
|-------|-----------------|-------------------|-------------|
| arifOS | registry `source_path` | registry `runtime_path` | `curl :8088/health` |
| A-FORGE | registry `source_path` | registry `runtime_path` | `curl :7071/health` |
| GEOX | registry `source_path` | registry `runtime_path` | `curl :8081/health` |
| WEALTH | registry `source_path` | registry `runtime_path` | `curl :18082/health` |
| WELL | registry `source_path` | registry `runtime_path` | `curl :18083/health` |
| AAA | registry `source_path` | registry `runtime_path` | `curl :3001/health` |
| arifFlow | registry `source_path` | registry `runtime_path` | `curl :7073/health` |

**Rule:** The table above is illustrative. The organ registry is authoritative. If they differ, the registry wins. Fix this SKILL.md.

## Verification loop
- Match → no action
- Mismatch → log + 888 HOLD with both SHAs + recommended action
- `.git_commit` missing on runtime → log warning, treat source as truth
- Organ DOWN → skip SHA comparison for that organ, flag in report

## Failure modes
- Runtime file missing → assume source is truth, surface to operator
- Mismatch in `.git_commit` only (cosmetic) → warn, don't HOLD
- Source repo not on `main` → flag, ask if intentional
- Registry unreachable → fall back to filesystem inspection of known paths

## De-hardcoding log (v1.1.0)
- Replaced hardcoded organ paths with registry-derived values
- Port numbers read from `/root/AAA/federation/organs.yaml` live
- Health endpoints probed dynamically rather than assumed
- Added graceful degradation: if registry unavailable, fall back to filesystem scan
