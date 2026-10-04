# GEOX Tool Development — Editable Install Path Pitfall

## The Problem

GEOX is installed in **editable mode** (`pip install -e .`). Python resolves the import path to `/root/GEOX/geox/` (via the editable .pth file), NOT to `/root/GEOX/src/geox/`.

When you create a new tool file in `src/geox/egs/tools/temporal.py`, Python **cannot import it** because the runtime path is `geox/egs/tools/`.

## The Fix

After creating a new file in `src/`, **also copy it to the non-src path**:

```bash
# Create in source
vim /root/GEOX/src/geox/egs/tools/mytool.py

# Copy to runtime path
cp /root/GEOX/src/geox/egs/tools/mytool.py /root/GEOX/geox/egs/tools/mytool.py

# Verify import works
python3 -c "from geox.egs.tools.mytool import *; print('OK')"
```

Or use the symlink-based install which should handle this:
```bash
cd /root/GEOX && pip install -e .
```

## Why This Happens

- `pyproject.toml` has `[tool.setuptools.packages.find] where = ["src"]`
- But the editable install creates a `.pth` file pointing to `/root/GEOX/`
- So Python sees `/root/GEOX/geox/` as the package root
- The `src/geox/` and `geox/` directories are **both** present but only `geox/` is on the import path

## Registration

After creating the tool file, register it in `src/geox_mcp/tools_manifest.yaml`:
- Add tool entry with `name: geox_<tool_name>`, `domain: earth.<domain>`, `visibility: public`
- Update `public_count_target` (increment by number of new tools)
- Restart the service: `systemctl restart geox-mcp`

## Verification

```bash
# Check tool count increased
curl -sf http://127.0.0.1:8081/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'tools={d[\"tools_loaded\"]}')"

# Run import test
python3 -c "from geox.egs.tools.<new_tool> import <function>; print('OK')"
```

## Proven: 2026-08-09

Opencode created `src/geox/egs/tools/temporal.py` but import failed until we also placed the file in `geox/egs/tools/temporal.py`. Service restart picked up both the new file and the updated manifest.
