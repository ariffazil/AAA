# Detecting `litellm_params: null` Entries in litellm-config.yaml

A specific YAML pitfall that causes litellm-federation to crash-loop with
`AttributeError: 'NoneType' object has no attribute 'items'`. Documented
2026-08-12 during federation health audit.

## The Symptom

```text
litellm-federation.service: Active: activating (auto-restart) (Result: exit-code)
Main process exited, code=exited, status=3/NOTIMPLEMENTED
journalctl: AttributeError: 'NoneType' object has no attribute 'items'
  at proxy_server.py: for k, v in model["litellm_params"].items():
```

The service can ping health, port is held briefly, then dies. systemd
restart-loop every ~30s. No models exposed at `/v1/models` (or only the
escape-config models from a separate :4012 instance, which masks the
real outage).

## The Cause

In `litellm-config.yaml`, a `model_list` entry like this:

```yaml
- model_name: i-arif
  litellm_params:        # ← key present, value parses to None
  model: openai/mimo-v2.5
  api_base: os.environ/MIMO_BASE_URL
  api_key: os.environ/MIMO_API_KEY
```

Note: `model:` is flush-left (column 0), not indented under
`litellm_params:`. YAML parser sees `litellm_params:` with no children
mapped to it → value becomes `null`. litellm iterates
`model["litellm_params"].items()` → crash.

This usually happens during copy-paste edits where the original block had
correct indentation but the new block was reset to column 0 (e.g. when
the editor auto-stripped leading whitespace or the human retyped the
key line without preserving the indent).

## The Diagnostic (Reusable)

```python
import yaml
data = yaml.safe_load(open('/root/A-FORGE/litellm-config.yaml'))
ml = data.get('model_list', [])
print(f'Total models: {len(ml)}')
broken = []
for i, m in enumerate(ml):
    name = m.get('model_name')
    lp = m.get('litellm_params')
    if lp is None:
        actual = '(litellm_params is null)'
        broken.append((i, name, actual))
    else:
        actual = lp.get('model', '?')
    # full list useful for diff
print(f'Broken entries: {len(broken)}')
for idx, name, _ in broken:
    print(f'  [{idx}] {name}')
```

Expected output for a healthy config: `Broken entries: 0`. Anything >0
means litellm-federation will crash on next load.

## How to Spot in Editor

Search the file for the pattern:

```bash
grep -n -B1 "^  model:" /root/A-FORGE/litellm-config.yaml
```

Each hit should be checked: is the line above `- model_name: <X>` with
proper 4-space indent under `litellm_params:`? If `model:` is at column
0 and the line directly above it is `- model_name:`, the entry is
broken.

## The Fix Pattern

For each broken entry, ensure children of `litellm_params:` are
indented 4 spaces (consistent with the rest of the file):

```yaml
- model_name: i-arif
  litellm_params:
    model: openai/mimo-v2.5          # 4-space indent
    api_base: os.environ/MIMO_BASE_URL
    api_key: os.environ/MIMO_API_KEY
    order: 2
```

Validate before restart:

```bash
python3 -c "
import yaml
d = yaml.safe_load(open('/root/A-FORGE/litellm-config.yaml'))
broken = [(i,m.get('model_name')) for i,m in enumerate(d.get('model_list',[]))
          if m.get('litellm_params') is None]
print(f'broken: {len(broken)}')
"
```

Must show `broken: 0` before any `systemctl restart litellm-federation`.

## Why This Class of Bug Slips Through

1. **Editor visual mode hides it** — the block looks structurally
   similar to other entries because all the lines are present.
2. **YAML parses without error** — `yaml.safe_load` returns the dict;
   `null` is a valid YAML value, not a parse error.
3. **Existing reload recipes** (`references/litellm-reload-recipe-2026-08-12.md`)
   Step 2 catches generic yaml syntax errors but does NOT catch
   `litellm_params: null` specifically — the file parses fine.
4. **Only the runtime crash surfaces it** — by which point the service
   has been down for the duration of the audit.

## Session-Specific Findings (2026-08-12)

- 6 broken `i-arif` entries in `/root/A-FORGE/litellm-config.yaml`
  (indices 5, 7, 9, 11, 13, 51, 53 in the model_list at probe time)
- Service had been crash-looping at 10:37–10:38 MYT
- `/v1/models` on :4000 was serving stale `connection refused`
- Only `:4012` (escape-config with 3 models) was up — falsely
  suggested federation was "still working"
- Audit required: probe the canonical port AND any escape ports
  separately, because their health is not transitive

## Verification After Fix

After applying the indent fix and restarting:

```bash
systemctl restart litellm-federation.service
sleep 5
curl -s http://127.0.0.1:4000/v1/models | python3 -c "
import sys, json
d = json.load(sys.stdin)
models = [m.get('id') for m in d.get('data', [])]
print(f'TOTAL: {len(models)}')
# sanity: i-arif must now appear
print(f'i-arif present: {\"i-arif\" in models}')"
```

Must show: `TOTAL: 112` (or current full count) AND
`i-arif present: True`. If false → fix didn't apply; check
`systemctl status litellm-federation` and `journalctl -n 30`.

## Add to Pre-Reload Verification

The pre-restart check in `references/litellm-reload-recipe-2026-08-12.md`
Step 2 should be extended with the broken-entry probe above, BEFORE
generic yaml validity. Pre-existing recipes were missing this check.

## Anti-Pattern

❌ Trusting "yaml loads = yaml good". A file can parse with no errors
yet still have structurally-invalid entries that crash the consumer.

✅ Run the broken-entry probe as a separate gate.