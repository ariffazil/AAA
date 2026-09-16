---
name: federation-mcp-drift-audit
id: federation-mcp-drift-audit
version: 1.0.0
owner: HERMES
risk_tier: low
description: Use when auditing arifOS MCP federation drift or bypass, or inventorying which MCP tools exist versus which are actually used.
when_to_use: After a deploy, when Arif brings an external audit/contrast report, before any "is the federation governed or just running?" question, or before answering "what should we upgrade / cut / add" about the MCP tool surface.
floor_scope:
- F2
- F4
- F11
autonomy_tier: T0
---
# Federation MCP Drift Audit

Run this when asked to inspect or "apex-zen" the federation's MCP tools. The deliverable is a diagnosis grounded in what actually executed, plus a fix plan split by substrate (safe, reversible) vs authority (F13 architectural seal).

## Baseline: run the inspector, then distrust it

`python3 /root/scripts/mcp_federation_inspector.py` (tests arifOS, GEOX, WEALTH, WELL). Two traps:

- Its TOTAL row hardcodes "GREEN" and it `exit 0` even when organs report ERROR. Read the per-organ `Status:` lines and the JSON at `/root/AAA/registries/MCP_INSPECTOR_AUDIT.json` — never trust the aggregate scorecard or exit code.
- It imports each organ's SOURCE module (`from geox_mcp.server import mcp`), not the live HTTP surface, so its tool counts reflect source, not what is deployed. Cross-check live `tools/list` (MCP probe) for source→runtime drift.

## Surface ≠ usage: measure the ledger before proposing a cut or an upgrade

A tool list is a claim about capability; the invocation record is evidence about work. Never answer "which tools need upgrading / which are dead" from the surface alone — enumerate both sides.

1. **Enumerate the live surface across organs, not the source tree.** The baseline inspector imports source modules and over-reports. Run `scripts/mcp_surface_usage_audit.py` from this skill: it does `initialize` → `notifications/initialized` → `tools/list` against each HTTP organ, drives the A-FORGE stdio server through its own CLI, then cross-references the usage ledger.
2. **Measure real usage from the session store, not from history files.**
   ```bash
   sqlite3 /root/.hermes/state.db "select tool_name, count(*) from messages \
     where tool_name is not null and tool_name<>'' group by tool_name order by 2 desc"
   ```
   MCP tools are recorded **prefixed** as `mcp__<server>__<toolname>` — match on that prefix or every MCP tool reads as zero-call. `.hermes_history` records typed text and transcripts, not invocations; scoring against it produces a false "nothing is used" reading.
3. **Report zero-call share per organ as a measurement, not a verdict.** "Unexercised" is the finding; "useless" is a conclusion F13 draws. A zero-call tool may be a rare-but-critical fallback — say which reading you mean.
4. **Protocol era is a separate axis from the tool list.** Test stateless `2026-07-28` with a `server/discover` POST carrying `MCP-Protocol-Version: 2026-07-28`, `Mcp-Method: server/discover`, and the `_meta.io.modelcontextprotocol/*` envelope. A 400 there means the organ is still on the legacy stateful handshake even while its tool list looks healthy.
5. **Hygiene findings outrank tool counts.** Report these first — a tool inventory never shows them, and they silently corrupt downstream output: freshness expiry in an organ's `/health`, cached snapshot files that a cron prompt tells agents to read instead of probing live, and cron prompts naming tools, ports, or versions that no longer exist.

## Many tools failing at once = dependency-pin drift, not per-organ breakage

Import errors like `cannot import name 'McpError'` or `StreamableHTTPServerTransport has no attribute '_check_accept_headers'` across several organs mean a package version drifted off the pin. mcp 2.0.0 renamed `McpError`→`MCPError` and dropped `_check_accept_headers`, silently breaking every transport built against 1.x.

**Never quote a pin from memory, a doc, or this skill — read both sides.** The declared pin and the installed version drift independently, per organ, and the mismatch is itself the finding:

```bash
grep -E '^(mcp|fastmcp)==' /root/arifOS/requirements.txt        # declared intent
/root/<organ>/.venv/bin/python -c 'import importlib.metadata as m; print(m.version("mcp"), m.version("fastmcp"))'   # installed reality
```

Compare organ to organ too — each organ runs its own venv, so a partial upgrade leaves one on a different mcp than the rest. When declared and installed disagree, align one to the other as a single conscious step (raise the install to the pin, or correct the pin if the upgrade was intended and verified); never assume the higher number is the right one, and do not patch each broken organ's transport code.

## Authority failures are silent (feedback asymmetry)

Broken substrate screams (timeout, EROFS, load). Broken authority seals quietly — a bypassed ACT scope token or an advisory 888_HOLD still returns `status: SEAL` and increments the sequence number, looking like success in the ledger. Re-run the probe and read what actually executed (`action_class`, `allowed[]`, `exit_code`), never what the verdict claims.

## The three authority surfaces are disconnected

Declarative capability graph, `gate_action` judgment, and the tool execution path are separate surfaces with no hard interceptor between judgment and execution — that gap IS the scope bypass. `gate_action` lives in `arifOS/arifosmcp/boot/internal_rasa.py`; `scripts/constitutional_guard.py` imports a `core.constitutional_gate` module that does not exist (dead CLI). To close the bypass, wire the gate into the execution path (`forge_shell`, `forge_seal_lane_a`), not beside it.
