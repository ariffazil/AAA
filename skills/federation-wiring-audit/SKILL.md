---
name: federation-wiring-audit
description: "Audit whether a Hermes installation is actually wired to the arifOS federation (MCP connections, plugin stubs, agent-card vs runtime gaps). Lightweight 5-step sequence — not the full 6-phase constitutional audit. Use when: 'is hermes wired to arifOS', 'check MCP connections', 'are the slash commands real', 'agent-card audit', or after any Hermes config change."
tags: [hermes, arifos, mcp, wiring, audit, federation, plugins]
version: 1.0.0
triggers:
  - "is hermes wired to arifOS"
  - "check MCP connections"
  - "are the slash commands real"
  - "federation wiring"
  - "agent-card audit"
  - "plugin stub check"
related_skills:
  - hermes-audit
  - federation-constitutional-audit
  - hermes-agent
---

# Federation Wiring Audit — Hermes ↔ arifOS

> **Forged:** 2026-08-10 from Arif's sovereign directive.
> **Scope:** Lightweight wiring check (not the full 6-phase constitutional audit).
> **DITEMPA BUKAN DIBERI**

## When to Use

- After adding/changing MCP servers in Hermes config
- After plugin changes (new /init, /seal, etc.)
- When investigating "why can't Hermes call arif_init?"
- Post-upgrade verification (did MCP wiring survive the update?)
- Periodic drift check (is documentation still matching runtime?)

## When NOT to Use

- Full organ audit → `federation-constitutional-audit` (6-phase, adversarial)
- Quick health check → `forge-federation-probe` (7 probes)
- Single MCP server test → `forge-mcp-testing` (MCPJam Inspector)

## The 5 Steps

### Step 1: MCP Connection Matrix

```bash
# What config.yaml declares
grep -A20 "mcp_servers:" ~/.hermes/profiles/aaa-hermes/config.yaml

# What hermes sees (NOTE: only shows `hermes mcp add` servers, not config.yaml entries)
hermes mcp list --profile aaa-hermes

# What agent-card.json declares (may be aspirational)
python3 -c "
import json
d = json.load(open('/root/AAA/agents/hermes/agent-card.json'))
for name, url in d.get('mcp_servers', {}).items():
    print(f'  {name}: {url}')
"
```

Build the matrix:

| Server | agent-card | config.yaml | hermes mcp list | Live probe |
|--------|-----------|-------------|----------------|------------|
| arifOS | ? | ? | ? | `curl -sf :8088/mcp` |
| A-FORGE | ? | ? | ? | `curl -sf :7072/mcp` |
| notebooklm | N/A | ? | ? | check status |

**Red flag:** agent-card says YES but config.yaml says NO → documentation-reality gap.

### Step 2: Plugin Stub Detection

Check whether plugins that claim federation work actually call federation APIs:

```bash
# Count federation API calls in each plugin
for plugin in init-command seal-command; do
  dir="/usr/local/lib/hermes-agent/profiles/aaa-hermes/plugins/$plugin"
  if [ -d "$dir" ]; then
    echo "=== $plugin ==="
    grep -c "arif_init\|arif_seal\|arif_route\|arif_judge\|mcp__arifos\|forge_vault" \
      "$dir/__init__.py" 2>/dev/null || echo "  (no federation calls found)"
    wc -l "$dir/__init__.py" 2>/dev/null
  fi
done
```

**If all counts are 0:** plugins are stubs — they do local file ops masquerading as federation work.

**What a stub looks like:**
- `/init` → `curl :8088/health` → "✅ arifOS" (health check, not session binding)
- `/seal` → `json.dump(receipt, file)` → "saved locally" (file write, not VAULT999 seal)

**What wired looks like:**
- `/init` → `mcp_arifos__arif_init()` → session_id + lease + SCT token
- `/seal` → `mcp_arifos__arif_seal()` or `mcp_aforge__forge_vault()` → sealed receipt

### Step 3: Hook Verification

Hooks are shell scripts (stdin JSON), not MCP — they work independently:

```bash
grep "pre_tool_call\|post_tool_call" ~/.hermes/profiles/aaa-hermes/config.yaml
ls -la /root/AAA/federation/protocols/arifos-*-hook.py 2>/dev/null
```

**Key insight:** Hooks can work even when MCP is unwired. Don't conflate "hooks work" with "federation is wired."

### Step 4: What Each Component Actually Does

| Component | Type | Federation dependency | Works without MCP? |
|-----------|------|----------------------|-------------------|
| lane_switch plugin | Plugin | None (reads YAML) | ✅ Yes |
| pre_tool_call hook | Shell hook | None (reads stdin) | ✅ Yes |
| /init plugin | Plugin | SHOULD call arif_init | ⚠️ Works as stub |
| /seal plugin | Plugin | SHOULD call arif_seal | ⚠️ Works as stub |
| MCP tools | Native MCP | Full MCP required | ❌ No |

### Step 5: Verdict

Classify the installation:

| Status | Meaning | Action |
|--------|---------|--------|
| **WIRED** | config.yaml has MCP servers, plugins call them, tools available | Verify with `hermes mcp list` |
| **PARTIAL** | Some MCP wired, some stubs | Complete the wiring |
| **UNWIRED** | Zero federation MCP connections | Add MCP servers to config.yaml |
| **ASPIRATIONAL** | agent-card declares capabilities that don't exist at runtime | Fix documentation OR wire the MCP |

## Common Fixes

### Add federation MCP servers

```yaml
# In config.yaml under mcp_servers:
mcp_servers:
  arifos:
    url: "http://127.0.0.1:8088/mcp"
    timeout: 30
  aforge:
    url: "http://127.0.0.1:7072/mcp"
    timeout: 30
  arifflow:
    url: "http://127.0.0.1:7073/mcp"
    timeout: 10
```

After restart, tools appear as `mcp_arifos__arif_init`, `mcp_arifos__arif_seal`, etc.

### Rewrite stub plugins to use MCP

Replace `subprocess.run(["curl", ...])` with `mcp_arifos__arif_init()` calls.

## Pitfalls

1. **`hermes mcp list` is incomplete.** It only shows servers added via `hermes mcp add`, NOT servers defined directly in config.yaml. Always parse config.yaml directly for the full picture.

2. **Agent-card is aspirational documentation, not runtime truth.** `/root/AAA/agents/hermes/agent-card.json` declares MCP endpoints and tool access — but it's a static JSON file, not a live capability manifest.

3. **Hooks ≠ MCP wiring.** The `arifos-hermes-gate-hook.py` works because it reads stdin JSON, not because MCP is connected. Don't assume federation integration from hook functionality.

4. **Plugins can be enabled without being wired.** `plugins.enabled: [init-command, seal-command]` in config.yaml means the plugin code loads — it does NOT mean the plugin calls arifOS. Check the plugin source code.

## Session-Specific Detail

See `references/federation-wiring-audit-2026-08-10.md` for the full audit findings from 2026-08-10 including the agent-card vs runtime mismatch matrix and specific file paths.
