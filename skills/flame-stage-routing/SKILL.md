---
name: flame-stage-routing
description: >
  FLAME stage routing — tool_name interception that routes payloads to the right tier
  (T0=Ollama local, T1=Groq cloud, T2=governed frontier). Covers the full pipeline:
  config rules → router interception → API passthrough → cascade fallback.
  Also covers the critical two-source drift pitfall and dead provider cleanup patterns.
version: "2026.08.12"
owner: AAA
risk_tier: medium
autonomy_tier: T1
floor_scope:
  - F1
  - F2
  - F4
  - F9
---

# FLAME Stage Routing — tool_name → tier interception

> **Skill ID:** FLAME-stage-routing · **Version:** 1.0.0 · **Forged:** 2026-08-12
> **Load when:** Configuring FLAME routing, fixing stage routing, debugging tool_name interception, syncing FLAME between /root/FLAME and /root/A-FORGE.
> **Do NOT load for:** Constitutional judgment, SEAL decisions, paid model routing.

## Architecture

Stage routing intercepts `tool_name` from the request payload and overrides the chain
before the main dispatch engine runs. It's a **zero-latency judge** — reads metadata
(tool name), not model output. Gödel Lock Rule 2 preserved (no self-certification).

```
Request → ZeroFlyZone check → STAGE ROUTING (tool_name → tier) → task_class classifier → dispatch cascade
                                        ↓
                          T0_SOVEREIGN: grep/read_file/curl/git → Ollama first
                          T1_EXECUTION: edit/write_file/pytest → Groq free cloud
                          T2_FRONTIER: PETRONAS/constitutional/SEAL → governed frontier
```

Stage routing runs BEFORE `classify_payload()` — it takes precedence.

## Three-Part Pipeline

### 1. Config (flame_config.json → routing.stage_routing.rules)

Rules are stored in `config['routing']['stage_routing']['rules']` — an array of tier
rules with `match_type` (tool_name | domain_tag | context_keyword) and `patterns`.

```json
{
  "tier": "T0_SOVEREIGN",
  "match_type": "tool_name",
  "patterns": ["grep", "grep_search", "glob", "read_file", "list_directory",
               "run_shell_command:curl", "run_shell_command:git status", ...]
}
```

See `references/stage-routing-config.md` for the full ruleset.

### 2. Router (flame_router.py → FlameEngine.call())

```python
# In FlameEngine.call(), BEFORE task_class classifier:
if tool_name:
    stage_rules = self.config.get("routing", {}).get("stage_routing", {}).get("rules", [])
    for rule in stage_rules:
        if rule.get("match_type") == "tool_name" and tool_name in rule.get("patterns", []):
            # Override chain_id and reorder tiers
            ...
```

`tool_name` is a new parameter added to `FlameEngine.call()` (line ~1631).

### 3. API Server (flame_api_server.py → /v1/chat/completions handler)

```python
tool_name = query.get("tool_name", "")
engine.call(prompt, ..., tool_name=tool_name)
```

**Critical:** Without this passthrough, `tool_name` never reaches the router.

## Verification

```bash
# Trigger probe and check logs
curl -s http://127.0.0.1:18901/probe
sleep 12

# Test stage routing (T0 → Ollama first)
curl -s http://127.0.0.1:18901/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"flame","messages":[{"role":"user","content":"List files"}],"tool_name":"grep","max_tokens":50}'
# → tried: ["ollama/qwen2.5:3b", "groq/qwen/qwen3.6-27b"]

# Check logs for STAGE_ROUTE
journalctl -u flame-api.service --since "30 sec ago" | grep STAGE_ROUTE
# → FLAME STAGE_ROUTE: tool=grep → tier=T0_SOVEREIGN target=ollama/qwen2.5:3b
```

## ⚠️ CRITICAL PITFALL: Two-Source Drift

**The #1 cause of "changes not taking effect" in FLAME.**

```
LIVE SERVICE:  /root/FLAME/     ← systemd ExecStart points here
GIT REPO:      /root/A-FORGE/flame/  ← git commits happen here
```

The systemd unit (`flame-api.service`) runs `ExecStart=/usr/bin/python3 /root/FLAME/flame_api_server.py`.
Editing `/root/A-FORGE/flame/flame_router.py` does NOT affect the running service.

**Rule:** After editing A-FORGE, always `cp /root/A-FORGE/flame/*.py /root/FLAME/` then restart.
Or: edit `/root/FLAME/` directly, then `cp` to A-FORGE for git.

```bash
# Correct sync pattern
cp /root/A-FORGE/flame/flame_router.py /root/FLAME/flame_router.py
cp /root/A-FORGE/flame/flame_api_server.py /root/FLAME/flame_api_server.py
cp /root/A-FORGE/flame/flame_config.json /root/FLAME/flame_config.json
sudo systemctl restart flame-api.service
```

## ⚠️ PITFALL: Ollama Cold-Start Timeout

Ollama `qwen2.5:3b` takes 10+ seconds to respond on first request (cold start).
FLAME probe timeout is also ~10s. Result: Ollama always shows `health=down` in the
routing table after restart, even though it IS available (just slow).

**Behavior:** Stage routing puts Ollama first (T0), Ollama times out → cascade to Groq.
This is correct — Ollama serves T0 when warm (subsequent requests <2s). On cold start
it gracefully falls through.

**If Ollama needs to be forced out of the chain:** Remove the `"tier": "T0_SOVEREIGN"`
rule from `flame_config.json` → `routing.stage_routing.rules`.

## ⚠️ PITFALL: Dead Provider Stale Refs

After providers are retired (removed from `flame_config.json` tiers), references to them
can persist in `TASK_CLASS_CHAINS` in `flame_router.py`. These cause silent cascade failures
— every routing attempt tries the dead provider first, fails, then cascades.

**Detection:**
```python
import json
chains = json.dumps(TASK_CLASS_CHAINS)
for dead in ['mistral/', 'sambanova/', 'cerebras/']:
    count = chains.count(dead)
    if count > 0:
        print(f"⚠️ {dead} still referenced {count} times")
```

**Fix:** Remove all dead provider refs from `TASK_CLASS_CHAINS`. Live providers only:
groq, gemini, sea-lion, qwen, openrouter, ollama.

## Related Skills

- `FLAME-router` (bundled) — tool lane vs agent lane classification
- `FLAME-operator` (bundled) — health probe, hit-rate, tier management

## References

- `references/stage-routing-config.md` — full config ruleset and tier definitions
