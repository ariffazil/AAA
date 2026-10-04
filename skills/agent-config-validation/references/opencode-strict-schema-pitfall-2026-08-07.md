# OpenCode Strict-Schema Pitfall (2026-08-07)

## The failure mode

`opencode.json` has `additionalProperties: false` enforced at the top level. Any unknown key (audit metadata, sidecar tags, even `_last_updated` or `_patch_summary` appended by a sibling agent) causes a fatal startup error:

```
Error: Configuration is invalid at /root/.config/opencode/opencode.json
↳ Unrecognized keys: _last_updated, _patch_summary
```

The TUI refuses to launch. `opencode models` returns the same error. The fix requires editing the file and removing the offending keys.

## The validation recipe

Two commands that confirm the file is valid:

```bash
opencode models              # returns 1600+ provider/model entries if valid
opencode debug config | head -5  # returns resolved config JSON if valid
```

Both print the error and exit non-zero when invalid. Run BEFORE declaring the fix done.

## Two distinct pitfalls

### Pitfall 1: Top-level underscore keys (audit metadata)

Sibling agents append metadata like `_last_updated` or `_patch_summary` to the JSON root for bookkeeping. This breaks strict schema. **Fix:** store audit metadata in a sibling `.meta.json` sidecar file. Never at JSON root.

### Pitfall 2: Python `json.load` → `json.dump` round-trip drops `enabled_providers`

A different class of bug. Round-tripping `opencode.json` through Python can silently drop entries from the `enabled_providers` array. Always diff `enabled_providers` and `agent` keys after any Python edit:

```python
import json
b = json.loads(open('opencode.json.pre.bak').read())
c = json.loads(open('opencode.json').read())
assert c.get('enabled_providers') == b.get('enabled_providers'), "lost providers"
assert set(c.get('agent', {}).keys()) == set(b.get('agent', {}).keys()), "lost agents"
```

## Pre-edit backup recipe

Before any surgical edit:

```bash
SNAP=/root/.local/share/arifos/snapshots/2026-08-07-opencode-fix
mkdir -p $SNAP
cp /root/.config/opencode/opencode.json $SNAP/opencode.json.pre-fix.bak
```

Snapshot path: `/root/.local/share/arifos/snapshots/<date>-<fix-name>/`. Probe the snapshot dir FIRST — `/root/.local/share/arifos/` is the canonical state dir (see arifos-federation-ops §5).

## Live provenance for this session

- Snapshot: `/root/.local/share/arifos/snapshots/2026-08-07-opencode-fix/opencode.json.pre-fix.bak` (60,959 bytes)
- Live file: `/root/.config/opencode/opencode.json` (60,960 bytes, 1-byte diff = trailing newline)
- Validation: 5/5 plugins PASS smoke test, all 6 agents + 14 providers preserved

## Cross-reference

- `arifos-federation-ops` §3: "live :port/health + AAA/docs/ORGAN.md win." Same principle — live `opencode models` output beats the file on disk.
- `federation-model-routing`: how to probe proxy chains when the file shows one model but runtime resolves to another.
