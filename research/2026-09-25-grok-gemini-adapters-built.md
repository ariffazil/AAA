# grok + gemini adapters — BUILD receipt (2026-09-25)

> Order: F13 "buat adapter grok/gemini" · Executor: FI-003 (BUILD lane)
> SOT hash chain: build_receipt.json `sot_sha256` now covers codex+grok+gemini adapter.py

## What was verified BEFORE building (no ghost capability)

- **Grok CLI** (bundled README, /root/.grok/metadata 2026-09-23): hooks run on
  "tool and session lifecycle events (pre/post-tool-use, session start/end)" —
  JSON files in `.grok/hooks/` OR `[[hooks.<Event>]]` TOML in config layers;
  matcher example `Bash|Write|Edit`; MCP `[mcp_servers.<id>]` with `url =`
  (HTTP) PROVEN by live `/root/.grok/config.toml` (5 organs already hand-wired
  that way); skills = SKILL.md dirs.
- **Gemini CLI**: NO hook mechanism documented/configured on-host
  (`/root/.gemini/hooks/` empty since 2026-08-13; settings.json = mcpServers
  only, 12 servers hand-wired incl. all 6 arif-core organs).

## Built

| Artifact | Path | Shape |
|---|---|---|
| Grok adapter | `hooks/adapters/grok/adapter.py` | 4-event map (SessionStart/PreToolUse/PostToolUse/SessionEnd) — documented surface only |
| Grok shim | `hooks/adapters/grok/shim.py` | sensor → spool `grok.jsonl`, advisory JSON out, never blocks |
| Gemini adapter | `hooks/adapters/gemini/adapter.py` | **declared-absent** event map (honest FP-04) |
| Gemini shim | `hooks/adapters/gemini/shim.py` | unmapped-class capture (void guard) if a surface ever fires |
| compile.py | `plugins/adapters/compile.py` | + emit_grok, emit_gemini, 6-column coverage matrix |
| dist views | `plugins/dist/grok/arif-core/` (config.arif-core.toml + hooks.json + SKILL.md), `plugins/dist/gemini/arif-core/` (settings-mcpServers.fragment.json + GEMINI.md) | build artifacts, not committed (FP-01) |

## Smoke test (live, 2026-09-25 ~13:58 MYT)

```
echo '{"tool_name":"Bash","session_id":"smoke-grok"}' | shim.py PreToolUse
→ supplemental: canonical_event=aaa.action.proposed, validated=true, unmapped=false
→ spool grok.jsonl: event_type=aaa.action.proposed, action.kind=execute,
  tool_id=Bash, risk_class=R3, harness envelope schema-valid

echo '{"session_id":"smoke-gemini"}' | gemini/shim.py SessionStart
→ canonical_event=aaa.turn.received, validated=true, absent_surface=true
```

TOML validated (tomllib): 6 organs resolved from organs.yaml (a-forge, arifos,
chron, hermes, minimax-media, signal), url-form + headers matching the live
grok config style; hooks = 4 events, PreToolUse matcher `Bash|Write|Edit`.

## Honest limits (FP-04)

- Grok coverage = PARTIAL by design: only the 4 documented events; UserPromptSubmit/
  Stop/Compact/Subagent are NOT documented for grok — absent, not faked.
- Gemini hooks = ABSENT (verified); the view's value = compiled MCP parity fragment.
- Install = F13 pen (FP-05): grok = merge `config.arif-core.toml` into
  `~/.grok/config.toml` OR drop `hooks.json` into `.grok/hooks/` (ONE form);
  gemini = merge fragment into `~/.gemini/settings.json`.
- Grok hook response schema undocumented → shim stays advisory (same posture as codex).
