# OpenCode Hardcode Audit — Session Reference (2026-08-12)

## Scan Results Summary

| Domain | Findings | Severity |
|--------|----------|----------|
| D1: Model IDs | 178 (21 providers) | LOW — accepted DRY debt |
| D2: Ports | 12 hardcoded across ×3 profiles + Python | HIGH — CRITICAL |
| D3: Tool Paths | 10 HTTP URLs + 16 STDIO | MEDIUM |
| D4: Human | permission "allow" only | NONE |
| D5: Math Thresholds | compaction + subagent_depth | LOW — already YAML-loaded |
| D6: Timeouts | 7 magic numbers across 4 files | HIGH |

## Files Produced

- `/root/.config/opencode/dynamic-registry.yaml` — 15KB, all dynamic values
- `/root/.config/opencode/opencode-dynamic-builder.py` — builds opencode.json from registry

## Usage

```bash
# Edit registry values:
vim ~/.config/opencode/dynamic-registry.yaml

# Rebuild opencode.json:
python3 ~/.config/opencode/opencode-dynamic-builder.py --apply

# Show diff vs current:
python3 ~/.config/opencode/opencode-dynamic-builder.py --diff
```

## Hermes Port Topology (from organs.yaml)

| Organ | Port | env_var |
|-------|------|---------|
| arifOS | 8088 | ARIFOS_PORT |
| A-FORGE | 7071 | AFORGE_PORT |
| FED | 7074 | FED_PORT |
| GEOX | 8081 | GEOX_PORT |
| WEALTH | 18082 | WEALTH_PORT |
| WELL | 18083 | WELL_PORT |
| arifFlow | 7073 | ARIFFLOW_PORT |
| LiteLLM | 4000 | LITELLM_PORT |
| Graphiti | 8000 | GRAPHITI_PORT |
| Hermes MCP | 18086 | HERMES_MCP_PORT |
| Hermes Agent | 18089 | HERMES_AGENT_PORT |
| Hermes A2A | 18090 | HERMES_A2A_PORT |

## Python Patches Applied

| File | Change |
|------|--------|
| hermes_mcp.py | `/root/VAULT999` → `os.environ.get("VAULT999_PATH", "/root/VAULT999")` |
| hermes_agent_mcp.py | `http://127.0.0.1:18089` → env-first |
| hermes_real_bridge.py | `host="127.0.0.1"` → env-first |

## The Drift Irony

Hermes has `drift_monitor` that detects semantic drift in memory — yet Hermes itself has topology drift (hardcoded ports that silently diverge from organs.yaml). The body that detects disease in others has the same disease in its own spine.
