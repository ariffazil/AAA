# Kimi Code MCP Launchers and Paths (2026-08-07)

Kimi Code's `mcp.json` references shell scripts under `/root/.arifos/agents/kimi/mcp-launchers/`. Each script is a wrapper that sets up env vars / paths then `exec`s the real MCP binary. **If a launcher script's underlying binary is missing or the script is broken, the MCP server silently fails.**

## Launchers present in this federation

| Launcher | Wraps | Verify with |
|---|---|---|
| `/root/.arifos/agents/kimi/mcp-launchers/semgrep.sh` | semgrep MCP server | `bash /root/.arifos/agents/kimi/mcp-launchers/semgrep.sh --version` |
| `/root/.claude/mcp-launchers/serena.sh` | serena MCP (also referenced from opencode.json) | `bash /root/.claude/mcp-launchers/serena.sh --help` |
| `/root/.claude/mcp-launchers/repomapper.sh` | repomapper MCP | `bash /root/.claude/mcp-launchers/repomapper.sh --help` |

## MCP servers in mcp.json (current roster)

```jsonc
{
  "github-official":  { /* github MCP — official */ },
  "serena":           { "command": "sh", "args": ["-lc", "exec /root/.claude/mcp-launchers/serena.sh"] },
  "repomapper":       { "command": "sh", "args": ["-lc", "exec /root/.claude/mcp-launchers/repomapper.sh"] },
  "capability-index": { /* arifOS capability_index MCP */ },
  "context7":         { /* docs lookup MCP */ },
  "playwright":       { /* browser automation MCP */ },
  "postgres-pro":     { /* Postgres MCP */ },
  "semgrep":          { "command": "sh", "args": ["-lc", "exec /root/.arifos/agents/kimi/mcp-launchers/semgrep.sh"] },
  "arifos":           { "url": "http://127.0.0.1:8088/mcp" },   // remote HTTP
  "aforge":           { "url": "http://127.0.0.1:7072/mcp" },
  "arifflow":         { /* local */ },
  "geox":             { "url": "http://127.0.0.1:8081/mcp" },
  "wealth":           { "url": "http://127.0.0.1:18082/mcp" },
  "well":             { "url": "http://127.0.0.1:18083/mcp" },
  "hound":            { /* research MCP */ },
  "brave-search":     { /* search MCP */ },
  "minimax":          { /* minimax tools (non-LLM) */ },
  "minimax-multimodal": { /* minimax multimodal generation */ }
}
```

(18 total MCP servers in this federation's mcp.json — see live file for current list.)

## Diagnostic recipe — "server unavailable" / "MCP failed"

1. **Probe the launcher independently:**
   ```bash
   bash /path/to/launcher.sh --version
   ```
   Fails = launcher broken, fix or replace.

2. **Probe the actual MCP endpoint (HTTP transport):**
   ```bash
   curl -sS -m 5 -X POST "http://127.0.0.1:8088/mcp" \
     -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
     -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}},"id":1}' \
     | jq '.result.serverInfo'
   ```
   JSON-RPC result = server is live. Don't trust Kimi Code's "server unavailable" log line alone.

3. **Check per-server timeout in mcp.json `[mcp]` block:**
   ```bash
   jq '.mcp // {}' /root/.arifos/agents/kimi/mcp.json
   ```
   Default timeouts are short. Federation organs that take longer than ~5s to respond (e.g. WEALTH compute-heavy calls) need a longer per-server timeout.

## Federation vs Kimi Code MCP overlap

Kimi Code's `mcp.json` and OpenCode's `opencode.json` both define MCP servers to the **federation organs** (arifos, aforge, arifflow, geox, wealth, well). They route to the same URLs but are managed independently. **Drift between the two = different MCP health in Kimi Code vs OpenCode.** When debugging "MCP works in OpenCode but not Kimi Code" or vice versa, this is usually the cause.

## Path gotchas

- **Launcher scripts MUST be executable.** `chmod +x /path/to/launcher.sh` if you copy from a backup or fresh git checkout.
- **Launcher scripts use `exec` to replace the shell process** — Kimi Code relies on this for proper signal forwarding. Don't change `exec` to a normal call.
- **Hardcoded absolute paths inside launchers** break if you copy the launcher to a different machine. Audit the launcher before promoting across federation nodes.