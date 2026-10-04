# Framing Example: Adding FRAME to federation.json

## Correct shape (use this)

```json
{
  "organ": "FRAME",
  "layer": "L1",
  "github": "ariffazil/FRAME",
  "role": "assessment_measurement",
  "port": 18085,
  "posture": "COMPUTE_ONLY",
  "systemd": "frame-organ.service",
  "description": "Federation Reference & Assessment Measurement Engine. Measures (baseline, probe, compare, trend, alert, report, rsi_verify), never judges (F2). Systemd-hardened. Read-only secrets via kunci-mas.flat.env. Registered 2026-08-08.",
  "doctrine": "L1 governance plane. Measures — never judges.",
  "ratified_by": "sovereign"
}
```

## Anti-patterns

- ❌ `{id: "FRAME"}` — wrong key. federation.json uses `organ`/`asset` keys, not `id`.
- ❌ Adding same organ to BOTH `organs[]` and `assets[]` — causes de-duplication chaos. Pick ONE.
- ❌ `layer: "L0"` for organ-level service — L0 is kernel-only (arifOS).
- ❌ Missing `posture:` — required field. Use `COMPUTE_ONLY` for measurement, `REFLECT_ONLY` for read-only, `LIVE` for active gateway, `READ_ONLY` for static assets.
- ❌ Missing `github:` — required. Format: `ariffazil/<repo>` (no .git suffix).
- ❌ Missing `description:` and `doctrine:` — verification tools (verify-surfaces.cjs, federation-json schema) flag these as incomplete.

## How to patch (Python, not edit-by-hand for atomic changes)

```python
import json
path = '/root/web-canon/canon/federation.json'
d = json.load(open(path))
new_entry = {
    "organ": "FRAME",
    "layer": "L1",
    "github": "ariffazil/FRAME",
    "role": "assessment_measurement",
    "port": 18085,
    "posture": "COMPUTE_ONLY",
    "systemd": "frame-organ.service",
    "description": "...",
    "doctrine": "...",
    "ratified_by": "sovereign"
}
# Check if already exists
existing = [o for o in d.get('organs', []) if o.get('organ') == new_entry['organ']]
if existing:
    print(f"Already registered as {new_entry['organ']}, skipping")
else:
    d['organs'].append(new_entry)
    json.dump(d, open(path, 'w'), indent=2)
    print(f"Added {new_entry['organ']} to organs[]")
```

## sites.yaml patching (Class 2: stale entry)

For surfaces, patch existing entries in place (don't add new ones):

```yaml
- path: /earth/hermes
  role: EARTH_EDGE
  description: "HERMES — multi-modal bridge. Live Telegram gateway (port 18089)."
  legacy_path: (TBD)
  port: 18089           # ← was 8644
  posture: LIVE         # ← was REFLECT_ONLY
  deployable: true      # ← was false
```

Comment in commit message should explicitly say "corrected from
[stale values] on [date] from [live evidence]" so future auditors see the
correction trail and don't relitigate it.