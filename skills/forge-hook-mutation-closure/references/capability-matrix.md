# Capability Matrix — Hook signal → owner lane

Use this table when deciding whether a new trigger belongs in `hermes-nudges.yaml` (engine) or a plugin (Python). The default: **engine for framework / reloadable / generic; plugin for specific / stateful / testable**.

## Decision criteria

| Criterion | Engine yaml | Plugin Python |
|---|---|---|
| Reload mechanism | file-read on every daemon subprocess | requires daemon restart |
| Test surface | synthetic message list via `process_pre_llm()` | call `plugin.pre_llm_call(...)` directly |
| Trigger complexity | simple: `always`, `any_keyword`, `regex`, `tool_name`, `is_first_turn`, `message_count_min/max` | arbitrary Python — state, history, regex bank |
| Audience | framework-wide nudges | specific persona / role / lane |
| Side effects | none (injects system message) | receipts to JSONL, classification side-effects |
| Owner | federation (`/root/AAA/federation/protocols/`) | profile-specific (`/root/.hermes/profiles/<profile>/plugins/`) |

## Signal classes by hook event

### pre_llm_call

| Signal class | Owner lane | Example |
|---|---|---|
| First turn of conversation | engine yaml (`is_first_turn`) | generic intake reminder |
| Entity-name reference (person / file / system) | plugin | `probe-first-reflex` guard 2 |
| Conversation boundary (forward/paste artifact) | plugin | `probe-first-reflex` guard 1 |
| Question budget (avoid exam-mode) | engine yaml OR firewall script | depends on whether text-shape or trigger-shape |
| LLM classification rubric | plugin | mode selection |

### pre_tool_call

| Signal class | Owner lane | Example |
|---|---|---|
| Consequential action (rm, DROP, payment) | engine yaml regex blocklist | `receipt_citation` nudge |
| Tool-specific gate | engine yaml `tool_name` match | `falsify` nudge for forge_shell etc. |
| Soft guidance only | plugin (`pre_tool_call` returning None) | log-only, no injection |

### post_llm_call

| Signal class | Owner lane | Example |
|---|---|---|
| Strip internal labels `[OBS]`, `[DER]`, etc. | engine yaml transform | `collapse` nudge |
| Strip receipt blocks `[🦾ACT]`, `[EXE]` | engine yaml transform OR plugin | depends on receipt-shape |
| Strip patch-declaration phrases | plugin | `probe-first-reflex` guard 3 |
| Role-boundary gate (CONVERSE / EXPLAIN / INSPECT) | firewall script | `presentation_firewall.py` |

## Anti-patterns

- **Two handlers claiming the same signal class** (e.g. entity-name detection in both yaml and plugin). Token waste + confusing context. Pick one lane.
- **Generic rule in a plugin** (e.g. a plugin guard that fires on `is_first_turn` for ALL profiles). Wrong lane — the daemon restart burden makes generic rules impractical in plugins.
- **Specific persona logic in engine yaml** (e.g. a rule that triggers only on Arif's specific entity names). Wrong lane — engine is profile-agnostic.

## How to detect existing overlap before patching

```bash
# Find every plugin pre_llm_call for the profile
PROFILE=/root/.hermes/profiles/aaa-hermes
grep -rn "def pre_llm_call" $PROFILE/plugins/

# For each plugin, extract condition patterns (entity regex bank, classifier, etc.)
grep -A2 "_needs_probe_first\|_classify_user_message" $PROFILE/plugins/*/__init__.py | head -30

# Compare against engine yaml rules
grep -B1 -A3 "any_keyword:\|regex:" /root/AAA/federation/protocols/hermes-nudges.yaml

# Look for the SAME pattern in both
```

If a regex pattern appears in both yaml and a plugin's `__init__.py`, you have an overlap. Resolve before patching.