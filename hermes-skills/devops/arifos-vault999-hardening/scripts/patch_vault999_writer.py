#!/usr/bin/env python3
"""Hot-patch vault999-writer with X-Writer-Token auth.
Run inside the container: docker cp patch_vault999_writer.py vault999-writer:/tmp/p.py && docker exec vault999-writer python3 /tmp/p.py
"""
import re

target = '/app/main.py'
with open(target) as f:
    content = f.read()

if 'verify_writer_token' in content:
    print("Already patched")
    exit(0)

# 1. Add token config after LOG_LEVEL
old_cfg = 'LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()'
new_cfg = '''LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
VAULT_WRITER_TOKEN_FILE = os.getenv("VAULT_WRITER_TOKEN_FILE", "/run/secrets/vault_writer_token")

def _load_writer_token() -> str:
    try:
        with open(VAULT_WRITER_TOKEN_FILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""
    except Exception:
        return ""

_WRITER_TOKEN = _load_writer_token()

def verify_writer_token(x_writer_token: str = Header(None)) -> str:
    """Reject requests without a valid X-Writer-Token."""
    if not _WRITER_TOKEN:
        return "unauthenticated"
    if not x_writer_token:
        raise HTTPException(401, "Missing X-Writer-Token")
    if x_writer_token != _WRITER_TOKEN:
        raise HTTPException(401, "Invalid X-Writer-Token")
    return x_writer_token'''

if old_cfg in content and 'verify_writer_token' not in content:
    content = content.replace(old_cfg, new_cfg, 1)
    print("Added token config + verify function")
else:
    print("Config already present or pattern not found")

# 2. Add Depends to /seal
old_seal = '@app.post("/seal")\nasync def create_seal(req: SealRequest):'
new_seal = '@app.post("/seal")\nasync def create_seal(req: SealRequest, _auth = Depends(verify_writer_token)):'

if old_seal in content and 'Depends(verify_writer_token)' not in content:
    content = content.replace(old_seal, new_seal, 1)
    print("Added Depends to /seal")

# 3. Add Depends to /ratify
old_ratify = '@app.post("/ratify")\nasync def ratify_seal(req: RatifyRequest):'
new_ratify = '@app.post("/ratify")\nasync def ratify_seal(req: RatifyRequest, _auth = Depends(verify_writer_token)):'

if old_ratify in content and content.count('Depends(verify_writer_token)') < 2:
    content = content.replace(old_ratify, new_ratify, 1)
    print("Added Depends to /ratify")

with open(target, 'w') as f:
    f.write(content)

print("Patched OK")
