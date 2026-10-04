# Federation Ports Resolver — Reference

> Added 2026-08-12 from the Banda Haram Hardcode sweep.

## The Problem

Hermes config.yaml hardcodes the entire federation topology (12 ports) and **NEVER reads** `organs.yaml`. If a port changes in organs.yaml, Hermes breaks silently. The drift monitor watches others' drift while itself drifting — the body that detects disease in others has the same disease in its own spine.

## The Solution

### Files produced

| File | Purpose | SOT |
|------|---------|-----|
| `port-registry.json` | Machine-readable port map (38 entries) | Derived from `organs.yaml` |
| `federation_ports.py` | Runtime resolver with env-first resolution | Reads from `port-registry.json` |
| `cognitive-params.yaml` | Timeout/threshold values (WATER) | Read by `cognitive/config.py` |
| `hermes_timeout_loader.py` | Timeout resolver for Python files | Reads from `cognitive-params.yaml` |

### Resolution chain (highest priority first)

```python
from federation_ports import get_port

# 1. os.environ["ARIFOS_PORT"] → if set, use it
# 2. port-registry.json["env_vars"]["ARIFOS"] → if found, use it
# 3. Default parameter → if provided
# 4. ValueError → port not found in any source
port = get_port("ARIFOS")  # → 8088
```

### Patching hardcoded ports

BEFORE (violation):
```python
# hermes_mcp.py line 351
host="127.0.0.1", port=8088
```

AFTER (compliant):
```python
import os
host = os.environ.get("ARIFOS_HOST", "127.0.0.1")
port = os.environ.get("ARIFOS_PORT", 8088)
```

### Regenerating port-registry.json

After any change to `organs.yaml`:
```bash
python3 -c "
import yaml, json
with open('/root/AAA/federation/organs.yaml') as f:
    data = yaml.safe_load(f)
# ... rebuild env_vars from components ...
# Write to port-registry.json
"
```
