---
name: opencode-json-pitfalls
description: Verbatim recipes for the two opencode.json traps that have bitten Arif's wiring sessions — silent round-trip drops (python json.load→json.dump) and schema rejection of unknown root keys (`_last_updated`, `_patch_summary`). Companion to federation-seat-wiring SKILL.md §Layer 3.
---

# opencode.json — two pitfalls, one fix pipeline

`/root/.config/opencode/opencode.json` is the highest-risk file in federation seat wiring. It breaks in two distinct ways that BOTH pass `python3 -m json.tool` and BOTH require different verification probes. This reference has the verbatim recipes.

## Pitfall 1 — python round-trip silent drops (DATA loss)

**Symptom:** After a `json.load → dict mutation → json.dump` round trip via Python, certain keys/arrays vanish without error. Bit 2026-08-07 when 3 entries in `enabled_providers` (`bailian-token-plan-payments`, `qwen-token-plan`, plus one other) silently disappeared.

**Why:** Python's `json.load` parses the file faithfully, but if you mutate the dict via a method that produces a new object (e.g. `dict.update`, list comprehension reassignment) and then `json.dump` without round-tripping the originals, you can drop entries. Most common cause: copying a dict, mutating the copy, and assigning back — but nested structures don't always deep-copy correctly.

**Detection probe (run AFTER any python edit):**
```bash
# Diff against last known-good backup, ignoring the auto-stamped metadata keys
diff <(python3 -m json.tool /root/.config/opencode/opencode.json.bak-<ts> | grep -v _last | grep -v _patch) \
     <(python3 -m json.tool /root/.config/opencode/opencode.json | grep -v _last | grep -v _patch)
```

Lines `<` with no matching `>` partner = silent drop. **Restore from backup immediately.**

**Safer mutation path:** use `jq` for any additive change. It round-trips faithfully.
```bash
jq '.enabled_providers |= . + ["new-provider"]' \
   /root/.config/opencode/opencode.json > /tmp/oc.json && \
mv /tmp/oc.json /root/.config/opencode/opencode.json
```

## Pitfall 2 — schema rejection of unknown root keys (BOOT failure)

**Symptom:** `opencode run` exits with `Error: Configuration is invalid at /root/.config/opencode/opencode.json ↳ Unrecognized keys: _last_updated, _patch_summary`. JSON parses fine — the file is valid JSON. The failure is opencode's runtime schema validator rejecting unknown top-level keys.

**Why:** Some automation (a sibling session, a hand-rolled patch script, or even a careless manual edit) writes metadata keys (`_last_updated`, `_patch_summary`) at the JSON root instead of inside a known block. OpenCode treats these as fatal.

**Bit 2026-08-07:** Two stray keys (`_last_updated`, `_patch_summary`) appeared at the JSON root, broke the agent completely. Fix was a 2-line `python3` strip:
```python
cfg = json.load(open('opencode.json'))
cfg.pop('_last_updated', None); cfg.pop('_patch_summary', None)
json.dump(cfg, open('opencode.json','w'), indent=2, ensure_ascii=False)
```

**Detection probe (run AFTER any opencode.json edit):**
```bash
cd /root/.config/opencode && echo ping | timeout 30 opencode run --log-level DEBUG --print-logs 2>&1 \
  | grep -E "Error|invalid|Configuration" | head -5
```

Empty grep = schema accepts. Non-empty = strip and retest.

**Strip recipe (preserves everything else):**
```bash
cd /root/.config/opencode
cp opencode.json opencode.json.bak-junkkeys-$(date +%Y%m%d-%H%M%S)  # ALWAYS backup first
python3 <<'PY'
import json
cfg = json.load(open('opencode.json'))
removed = [k for k in list(cfg.keys()) if k.startswith('_') and k not in ('$schema',)]
for k in removed: cfg.pop(k, None)
json.dump(cfg, open('opencode.json','w'), indent=2, ensure_ascii=False)
print('Removed:', removed)
PY
# Re-validate
echo ping | timeout 30 opencode run --log-level DEBUG --print-logs 2>&1 | grep -E "Error|invalid" | head -5
```

## Known-good root-key whitelist (opencode.json, 2026-08-07)

17 keys. Anything outside this set is suspect:

| Key | Purpose |
|---|---|
| `$schema` | Schema URL (informational) |
| `model` | Default model |
| `small_model` | Small-model fallback |
| `enabled_providers` | Provider whitelist |
| `default_agent` | Which agent runs by default |
| `instructions` | Prompt stack (list of file paths) |
| `agent` | Per-agent config block |
| `provider` | Per-provider config block |
| `mcp` | MCP server config |
| `references` | Reference docs loaded into context — **tolerated but not in the 17-key whitelist above; if opencode ever rejects it, fold reference paths under `instructions` instead** |
| `permission` | Per-agent permission matrix |
| `compaction` | Context compaction settings |
| `lsp` | LSP server config |
| `formatter` | Code formatter config |
| `autoupdate` | Auto-update settings |
| `plugin` | Plugin list |
| `subagent_depth` | Max subagent recursion depth |

**Anything else at the root → back up + strip + verify.** If the file needs additional top-level config, add it via `jq` and re-test with the schema probe above.

## Mandatory verification pipeline (run after EVERY edit)

```bash
# 1. JSON syntax
python3 -m json.tool /root/.config/opencode/opencode.json > /dev/null && echo "JSON OK"

# 2. Round-trip integrity (vs last known-good backup)
diff <(python3 -m json.tool /root/.config/opencode/opencode.json.bak-<ts>) \
     <(python3 -m json.tool /root/.config/opencode/opencode.json)

# 3. Schema validity (THE one that catches metadata keys)
cd /root/.config/opencode && echo ping | timeout 30 opencode run --log-level DEBUG --print-logs 2>&1 \
  | grep -E "Error|invalid|Configuration"

# 4. Smoke test (only if steps 1-3 all clean)
opencode run "Reply with exactly: OPENCODE_OK"
```

If step 2 surfaces unexpected diffs OR step 3 prints anything, **don't proceed**. Restore from backup, re-read, fix the root cause, retry.

## Backup discipline

Backups live in `/root/.config/opencode/` with date-stamped names. Old pattern (forensic-style):
```bash
opencode.json.bak-junkkeys-20260807-041148
opencode.json.20260806-040947.bak
opencode.json.bak-20260804T042042-pre-mimo-options
```

When restoring, pick the most recent known-good backup (one where steps 1-3 above all passed). After restoring, re-run the pipeline against the restored version before declaring done.

## Reference

This file is paired with `references/qwen-token-plan-diagnostic-2026-08-07.md` (Qwen cascade specifics). For the high-level recipe, see `SKILL.md §Layer 3`.