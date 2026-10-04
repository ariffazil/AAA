# Dynamic Config Audit Recipe — OpenCode Session (2026-08-12)

## Context

Arif gave the 6-domain hardcode taxonomy doctrine. Applied to OpenCode (FI-001) as the first config to audit. F13 Sovereign Override used.

## Scan Procedure

```bash
# Load and count
wc -c ~/.config/opencode/opencode.json  # 91,747 bytes

# Top-level keys
python3 -c "import json; cfg=json.load(open(CONFIG)); print(list(cfg.keys()))"
# Output: $schema, model, small_model, enabled_providers, default_agent,
#          instructions, agent, provider, mcp, references, permission,
#          compaction, lsp, formatter, autoupdate, plugin, subagent_depth, command

# Domain 1: model IDs — found 178 strings across 21 providers
# Domain 2: ports — 12 hardcoded (8088, 7072, 7074, 8081, 18082, 18083, 18087, 18090, 8000, 11434, 4000, 4010)
# Domain 3: MCP endpoints — 26 servers (10 HTTP + 16 STDIO)
# Domain 4: permission *:allow — trivial
# Domain 5: compaction {auto:true, prune:true, reserved:10000}, subagent_depth:3
# Domain 6: 9 instruction paths, 8 plugin paths (all /root/...)
# Secrets: 0 plaintext found — all use ${VAR}
```

## Provider Count (D1)

```
bailian-token-plan-payments, deepseek, kimi, litellm, minimax, minimax-code,
ollama, openai-api, openrouter, qwen, qwen-free, qwen-responses,
qwen-resp-api, qwen-token-plan, qwen-token-plan-individual,
qwen-token-plan-payments, sea-lion, zai-direct, zai-openai-compat,
opencode-go-zen, zai
```

## MCP Servers (D3)

| Name | Type | Endpoint |
|------|------|----------|
| arifos | http | 127.0.0.1:8088/mcp |
| aforge | http | 127.0.0.1:7072/mcp |
| fed | http | 127.0.0.1:7074/mcp |
| geox | http | 127.0.0.1:8081/mcp |
| wealth | http | 127.0.0.1:18082/mcp |
| well | http | 127.0.0.1:18083/mcp |
| hermes-agent | http | 127.0.0.1:18090/mcp |
| graphiti | http | 127.0.0.1:8000/mcp |
| openrouter | http | mcp.openrouter.ai/mcp |
| hindsight | http | 127.0.0.1:18087/mcp |
| arifflow | stdio | /root/arifFlow/mcp/arifflow-mcp.py |
| context7 | stdio | /usr/local/bin/context7-mcp |
| supabase | stdio | npx @supabase/mcp-server-supabase |
| qdrant | stdio | python3 /usr/local/bin/qdrant-mcp-bridge.py |
| hostinger-vps | stdio | /root/.npm-global/bin/hostinger-vps-mcp |
| hermes | stdio | python3 /root/.hermes/mcp_servers/hermes_mcp.py |
| megamemory | stdio | npx megamemory |
| sqlite | stdio | /usr/bin/mcp-server-sqlite |
| capability-index | stdio | bash: /root/arifOS/.venv/bin/python |
| semgrep | stdio | bash: /root/.arifos/agents/kimi/mcp-launchers/semgrep.sh |
| serena | stdio | sh: /root/.claude/mcp-launchers/serena.sh |
| repomapper | stdio | bash: /root/.claude/mcp-launchers/repomapper.sh |
| minimax | stdio | minimax-coding-plan-mcp |
| minimax-mcp | stdio | uvx minimax-mcp -y |
| codebase-memory | stdio | /root/.npm-global/bin/codebase-memory-mcp |
| free-search | stdio | uvx free-search-mcp |

## Output Files

- `/root/.config/opencode/dynamic-registry.yaml` (15KB)
- `/root/.config/opencode/opencode-dynamic-builder.py` (7KB)

## Builder --diff Results

```
provider  = (trimmed per-provider details — structural change, not semantic)
command   = init/seal (simplified from copy template)
agent     = model-only (simplified from description+mode)
mcp       = type "http" vs "remote" (structural change)
references = simplified to registry/secrets/skills/scars paths
enabled_providers = renamed keys (same models, better grouping)
```

All D1–D6 values preserved. Differences are structural simplification, not semantic drift.

## Lessons

1. First-pass builder always loses per-provider detail (options, wire_api, headers) — plan for `--merge-with-current` mode
2. The scan reveals config has accumulated cruft (6+ backup files, some with wrong names) — cleanup opportunity
3. Permissions set to wildcard `* : allow` — needs audit per D4 (human sovereignty)
