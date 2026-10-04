# Federation Wiring Audit — Detailed Findings (2026-08-10)

## Context

Arif: "Is Hermes even wired to arifOS and part of the warga AGENTIC AAA state? Do deep audit."
Ran 2026-08-10 12:48 MYT, after temporal correction (stale reply chain injected 4:48 AM).

## Config.yaml Audit Path

```
/usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml
```

### MCP Servers in Config

```yaml
mcp_servers:
  notebooklm:
    command: /root/.local/share/uv/tools/notebooklm-skill/bin/notebooklm-mcp
    enabled: true
```

**Result:** Only notebooklm. Zero federation MCP connections.

### Plugins Enabled

```yaml
plugins:
  enabled:
    - lane_switch
    - seal-command
    - init-command
```

**Result:** All three enabled, but init-command and seal-command are stubs.

### Hooks Configured

```yaml
hooks:
  pre_tool_call: '[{"matcher":"*","command":"/root/AAA/federation/protocols/arifos-hermes-gate-hook.py","accept_hooks":true},{"matcher":"*","command":"/root/AAA/federation/protocols/arifos-output-gate-hook.py","accept_hooks":true}]'
```

**Result:** Both hooks configured and functional (shell-based, no MCP dependency).

## Agent-Card Declaration

Path: `/root/AAA/agents/hermes/agent-card.json`

### Declared MCP Servers

```json
"mcp_servers": {
    "arifos": "http://127.0.0.1:8088/mcp",
    "aforge": "http://127.0.0.1:7072/mcp",
    "geox": "http://127.0.0.1:8081/mcp",
    "wealth": "http://127.0.0.1:18082/mcp",
    "well": "http://127.0.0.1:18083/mcp",
    "arifflow": "http://127.0.0.1:7073",
    "flame": "http://127.0.0.1:18901"
}
```

### Declared Organ Capabilities

```json
"organs": {
    "arifos": {
        "port": 8088,
        "tools": ["arif_route", "arif_init", "arif_judge"]
    }
}
```

**Reality:** These tools are NOT available. No MCP connection exists.

## Plugin Source Analysis

### init-command (/usr/local/lib/hermes-agent/profiles/aaa-hermes/plugins/init-command/__init__.py)

```python
# What it does:
ENDPOINTS = [
    ("arifOS", "http://127.0.0.1:8088/health"),
    ("A-FORGE", "http://127.0.0.1:7072/health"),
    ("arifFlow", "http://127.0.0.1:7073/health"),
]

def _probe(url, timeout=5):
    result = subprocess.run(["curl", "-sf", "--max-time", str(timeout), url], ...)
    return result.returncode == 0

# Verdict: STUB — health check, not session binding
```

### seal-command (/usr/local/lib/hermes-agent/profiles/aaa-hermes/plugins/seal-command/__init__.py)

```python
# What it does:
def _build_receipt(note=""):
    receipt = {"mode": "receipt", "name": f"session-seal-{now[:10]}", ...}
    return receipt

def _save_local_receipt(receipt):
    path = RECEIPT_DIR / f"receipt-{ts}.json"
    path.write_text(json.dumps(receipt, indent=2))
    return path

# Verdict: STUB — local file save, not VAULT999 seal
```

### Hook: arifos-hermes-gate-hook.py

```python
# What it does:
T3_PATTERNS = [r"secrets?[/\\]", r"kunci-mas", r"VAULT999/outcomes\\.jsonl", ...]
T2_TOOLS = {"write_file", "patch", "terminal", "cronjob", "delegate_task", ...}

def classify(tool_name, tool_input):
    # Returns 'OBSERVE', 'T1', 'T2', or 'T3'
    ...

def main():
    event = json.loads(sys.stdin.read())
    classification = classify(event["tool_name"], event["tool_input"])
    # Block T3, allow OBSERVE/T1, gate T2
    ...

# Verdict: WORKING — shell hook, reads stdin, no MCP dependency
```

## Organs.yaml Entry

```yaml
- id: hermes
  class: EDGE
  display_name: HERMES
  role: multimodal_telegram_bridge
  authority_ceiling: RELAY_ONLY
  forbidden_domains:
    - constitutional_judgment
    - engineering_execution
    - sealing
```

**Note:** authority_ceiling is RELAY_ONLY in organs.yaml but agent-card says DISPLAY_ONLY — minor inconsistency.

## The Gap

The gap is between what the documentation declares (agent-card.json) and what the runtime actually does (config.yaml + plugin source). This is the same pattern found in the arifFlow audit: "the daemon worked enough for most cases, so the full architecture was never activated."

Hermes works as a Telegram bot with notebooklm and local file tools. The federation integration (arifOS MCP, constitutional session binding, VAULT999 sealing) was designed and documented but never wired.
