# AAA Federation — Global Agent Config Hub

**Canonical location for all agent configurations** — extracted from scattered per-machine and per-repo locations.

## Structure

```
federation/
├── BACKUP/                    # Timestamped backups before extraction
├── kimi/                      # Kimi Code MCP configs
│   ├── mcp.json             # Primary MCP config
│   ├── kimi.json            # Kimi settings
│   ├── mcp-arifos.json      # arifos-specific override
│   ├── mcp-full.json        # Full MCP config
│   └── mcp-lite.json       # Lite MCP config
├── gemini/                   # Gemini CLI & Antigravity configs
│   ├── gemini-cli-mcp.json  # Gemini CLI MCP config
│   ├── gemini-antigravity-mcp.json
│   ├── settings.json
│   └── plugins/arifos/     # arifos Gemini plugin
├── antigravity/              # Antigravity VSCode configs
│   ├── mcp.json            # VSCode MCP servers
│   └── vscode-settings.json
├── claude/                   # Claude Code & Claude Desktop configs
│   ├── claude-desktop-mcp.json
│   └── rules/CONTEXT_MANAGEMENT.md
├── codex/                    # Codex rules
│   └── default.rules
├── copilot/                  # Copilot configs (future)
├── mcp-catalog.yaml          # UNIFIED MCP server registry
└── README.md                 # This file
```

## Agent → Config Mapping

| Agent | Home Config | AAA Federation |
|-------|-------------|-----------------|
| Kimi | `C:\Users\User\.kimi\` | `AAA/federation/kimi/` |
| Gemini CLI | `C:\Users\User\.gemini\config\` | `AAA/federation/gemini/` |
| Antigravity | `AppData\Roaming\Antigravity\User\` | `AAA/federation/antigravity/` |
| Claude Code | `C:\Users\User\.claude\` | `AAA/federation/claude/` |
| Claude Desktop | `AppData\Roaming\Claude\` | `AAA/federation/claude/` |
| Codex | `C:\Users\User\.codex\` | `AAA/federation/codex/` |

## Backward Compatibility

After extraction, **symlinks** were created from user home dirs → AAA federation.

To verify:
```powershell
# Check symlink
Get-Item C:\Users\User\.kimi\mcp.json | Select-Object LinkType, Target
```

## MCP Catalog Usage

All agents should reference `AAA/federation/mcp-catalog.yaml` as the **single source of truth** for MCP server definitions.

Individual agent configs (`mcp.json`, `mcp_config.json`) should use `extends: aaa-federation` or inline only agent-specific overrides.

## Historical

- Backup timestamp: `2026-05-24_04-52-53`
- Extraction performed under AAA governance (888_HOLD confirmed)
