# FLAME Stage Routing — Tool Name Interception (2026-08-12)

## What This Is

FLAME now supports **stage routing**: when a tool name is passed to `FlameEngine.call()`, FLAME maps it to a tier (T0/T1/T2) and locks routing to that tier. Zero judge latency. Zero agent burden. F2 TRUTH: the tool being called IS the signal.

## Architecture

```python
FlameEngine.call(
    prompt,
    tool_name="grep",        # NEW: optional tool name for stage routing
    task_class="classification",  # existing — still works
)
```

If `tool_name` matches a `stage_routing.rules` pattern in `flame_config.json`, FLAME forces tier override:
- T0_SOVEREIGN → hard-lock to Ollama (qwen2.5:3b), fallback to RM0 chain
- T1_EXECUTION → use free cloud (Groq/SEA-LION/Gemini)
- T2_FRONTIER → use DeepSeek V4 Pro (governed, paid)

## Config Schema (`flame_config.json`)

```json
{
  "routing": {
    "stage_routing": {
      "tiers": {
        "T0_SOVEREIGN": {
          "provider": "ollama",
          "model": "qwen2.5:3b",
          "fallback_chain": "RM0-TOOLS-FREELOOP"
        },
        "T1_EXECUTION": {
          "chain": "RM0-TOOLS-FREELOOP"
        },
        "T2_FRONTIER": {
          "chain": "GOVERNED-ONLY"
        }
      },
      "rules": [
        {
          "tier": "T0_SOVEREIGN",
          "match_type": "tool_name",
          "patterns": ["grep", "read_file", "glob", "health_probe", "drift_check"]
        },
        {
          "tier": "T2_FRONTIER",
          "match_type": "domain_tag",
          "patterns": ["[DOMAIN:PETRONAS]", "[CLASS:LEGAL_PROSE]"]
        }
      ]
    }
  }
}
```

## Implementation Sites

| File | Line Range | Function |
|---|---|---|
| `/root/A-FORGE/flame/flame_router.py` | 1641-1766 | `FlameEngine.call()` — stage routing interception |
| `/root/A-FORGE/flame/flame_router.py` | 1709-1766 | `_stage_routed` guard + tier override |
| `/root/A-FORGE/flame/flame_router.py` | ~2745 | CLI `--tool-name` argument |
| `/root/A-FORGE/flame/flame_api_server.py` | 126, ~150 | API server tool_name passthrough |

## The Bug We Caught (2026-08-12)

**Symptom:** T0 payloads (grep, read_file) escaped to flame-free aggregate instead of Ollama.

**Root cause:** Lines 1769-1775 in `flame_router.py` unconditionally overwrote `tiers` back to the default chain AFTER stage routing had already set them.

```python
# BEFORE (buggy):
if tool_name and _matched_tier:
    # ... sets tiers = force_tier + fallback_tiers  ← works here
    pass
# BUG: this runs unconditionally, clobbering the override:
chain = self.config["chains"][used_chain_id]
tiers = list(chain["tiers"])  # CLOBBER
```

```python
# AFTER (fixed):
if tool_name and _matched_tier:
    _stage_tiers_resolved = tiers
    _stage_routed = True
# Only set default if stage routing didn't fire:
if not _stage_routed:
    tiers = list(chain["tiers"])
```

**Commit:** `03b3a3a6` — `fix(flame): stage routing — guard _stage_routed, add --tool-name CLI arg, wire API passthrough`

## How to Verify

```bash
# T0 should hard-lock to Ollama
python3 /root/A-FORGE/flame/flame_router.py --json --tool-name grep --caller test 2>/dev/null <<< "ping"

# Expected result: tried[0] = 'ollama/qwen2.5:3b'

# T1 should route to free cloud
python3 /root/A-FORGE/flame/flame_router.py --json --tool-name edit --caller test 2>/dev/null <<< "refactor"

# Expected result: tried[0] = 'groq/llama-3.3-70b-versatile' (or similar free tier)

# T2 should hard-route to DeepSeek
python3 /root/A-FORGE/flame/flame_router.py --json --tool-name agent --caller test 2>/dev/null <<< "design"

# Expected result: tried[0] = 'tokenrouter/deepseek/deepseek-v4-pro'
```

## Key Design Decisions

1. **`tool_name` over content classification:** Tool name is metadata, not model output → no Gödel self-certification loop, no judge latency.
2. **Config-driven, not code-driven:** Adding new tool → tier mappings doesn't require code changes, just config edits.
3. **PETRONAS exception is hardcoded:** `[DOMAIN:PETRONAS]` and `[CLASS:LEGAL_PROSE]` always escalate to T2. F2 TRUTH: creative/legal prose cannot degrade silently.
4. **Dual-rule matching:** `tool_name` (exact match) + `context_keyword` (substring match) + `domain_tag` (structured marker). All three can coexist.
5. **Stage routing wins:** When matched, `task_class` classifier is suppressed. Tool signal > content signal.

## Pitfalls

- **Default chain clobbering bug** (above). Always use `_stage_routed` guard.
- **Ollama cold start:** T0 pays 10s cold-start penalty. Acceptable for sovereign survival; not acceptable for interactive use. Tie-breaker: `caller_id` (interactive callers get T1).
- **Pattern collision:** If two rules match (e.g., `tool_name=read_file` AND `context_keyword=grep` in prompt), first match wins. Order matters in `rules` array.
- **API server tool_name passthrough:** Both `_run_flame()` signature AND `do_POST()` extraction must be updated together. One without the other silently drops the signal.

## F2 TRUTH Hardening

When stage routing config changes, ship it as a config mutation commit. Document WHY each rule exists. The rules array is a policy file — every entry is a governance decision that needs audit trail.

Reference: `/root/forge_work/2026-08-12-flame-stage-rules/PROPOSAL.md` (original proposal)
