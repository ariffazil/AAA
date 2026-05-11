---
name: arifos-vault999-hardening
description: Hardening VAULT999 write path with token auth — ABC steps (token creation, arifOS header injection, vault999-writer verification). Covers Docker secret pitfalls, image rebuild workflow, and bind-mount token injection for non-swarm Docker Compose.
triggers:
  - "VAULT999 token auth"
  - "vault999-writer X-Writer-Token"
  - "harden vault write path"
  - "Docker secret compose"
  - "token auth vault"
---

# VAULT999 Token Auth Hardening — ABC Steps

## Overview

Hardening VAULT999 so agents act autonomously within governed lanes, with arifOS kernel attaching the writer token at runtime. Arif holds veto; arifOS holds the credential; agents hold authorization claims.

## Token Model

```
agent → arifOS: "I want to seal X"
arifOS: [judges X through F1-F13]
       ↓ policy approved
arifOS kernel: [attaches X-Writer-Token at runtime]
              [calls vault999-writer:5001/seal]
vault999-writer: [verifies token] → [writes to DB]
```

- Agents hold authorization claims, NOT credentials
- arifOS kernel holds the X-Writer-Token
- Token stored as bind-mounted secret, not env var in chat

## Three-Step Implementation (ABC)

### Step A — Create and store token

**Token generation:**
```bash
openssl rand -hex 32
# Fresh token: ade8242fcd8882cfd6b22b489b6c66d21c2234f9f4f35b187d84d9e814e1a56e
```

**Storage — Docker bind-mount (NOT Docker secret):**
```bash
# Docker secrets require swarm mode — use bind-mount instead for compose v2
mkdir -p /root/compose/secrets
echo "TOKEN_VALUE" > /root/compose/secrets/vault_writer_token
chmod 600 /root/compose/secrets/vault_writer_token

# Mount in compose:
volumes:
  - /root/compose/secrets/vault_writer_token:/run/secrets/vault_writer_token:ro
```

**NEVER** type the token in Telegram chat after generation. If exposed, rotate immediately.

### Step B — arifOS: inject X-Writer-Token header

**File:** `arifOS/arifosmcp/runtime/tools_internal.py`

```python
import os

# Near the vault writer call (line ~856):
writer_url = os.environ.get("VAULT999_WRITER_URL", "http://vault999-writer:5001")
writer_token = os.environ.get("VAULT_WRITER_TOKEN", "")
headers = {"Content-Type": "application/json"}
if writer_token:
    headers["X-Writer-Token"] = writer_token

verdict = payload.get("verdict", "SABAR")
if verdict == "SEAL":
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{writer_url}/seal",
            json=payload,
            headers=headers,  # ← token injected here
        )
```

**Set token in compose .env:**
```bash
# /root/compose/.env (NOT in Telegram chat)
echo "VAULT_WRITER_TOKEN=TOKEN_VALUE" >> /root/compose/.env
```

**Hot-patch running container (before permanent fix):**
```bash
# 1. Write patch script to host
cat > /root/patch_arifos_writer.py << 'PYEOF'
import re
target = '/app/arifosmcp/runtime/tools_internal.py'
with open(target) as f: c = f.read()
old = 'response = await client.post(\n            f"{writer_url}/seal",\n            json=payload,\n        )'
new = 'response = await client.post(\n            f"{writer_url}/seal",\n            json=payload,\n            headers=headers,\n        )'
if old in c and "headers=headers" not in c:
    c = c.replace(old, new, 1)
    with open(target, 'w') as f: f.write(c)
    print("Patched OK")
else:
    print("Already patched or pattern not found")
PYEOF

# 2. Copy into container and run
docker cp /root/patch_arifos_writer.py arifosmcp:/tmp/patch.py
docker exec arifosmcp python3 /tmp/patch.py

# 3. Verify
docker exec arifosmcp grep "X-Writer-Token" /app/arifosmcp/runtime/tools_internal.py
```

**For permanent fix:** Commit to git, rebuild image, update compose with volume mount:
```yaml
volumes:
  - /root/arifOS/arifosmcp/runtime/tools_internal.py:/app/arifosmcp/runtime/tools_internal.py:ro
```

### Step C — vault999-writer: verify X-Writer-Token

**Extract source from running container if not in repo:**
```bash
docker exec vault999-writer cat /app/main.py > /root/compose/vault999-writer/main.py
docker exec vault999-writer cat /app/requirements.txt > /root/compose/vault999-writer/requirements.txt
```

**Patch main.py — add token loading and verification:**

```python
import os

VAULT_WRITER_TOKEN_FILE = os.getenv("VAULT_WRITER_TOKEN_FILE", "/run/secrets/vault_writer_token")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Load token from mounted secret file (no logging at module level — causes NameError)
def _load_writer_token() -> str:
    try:
        with open(VAULT_WRITER_TOKEN_FILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""  # Bootstrap: allow unauth until token mounted
    except Exception:
        return ""

_WRITER_TOKEN = _load_writer_token()

def verify_writer_token(x_writer_token: str = Header(None)) -> str:
    """Reject requests without a valid X-Writer-Token."""
    if not _WRITER_TOKEN:
        return "unauthenticated"  # Graceful degradation during bootstrap
    if not x_writer_token:
        raise HTTPException(401, "Missing X-Writer-Token")
    if x_writer_token != _WRITER_TOKEN:
        raise HTTPException(401, "Invalid X-Writer-Token")
    return x_writer_token

# Apply to endpoints:
@app.post("/seal")
async def create_seal(req: SealRequest, _auth = Depends(verify_writer_token)):
    ...

@app.post("/ratify")
async def ratify_seal(req: RatifyRequest, _auth = Depends(verify_writer_token)):
    ...
```

**PITFALL: No logging at module level** — `log` is undefined until `logging.basicConfig()` runs. Use `print()` or defer to after `basicConfig`.

**Build and deploy:**
```bash
# 1. Build new image
docker build -f /root/compose/vault999-writer/Dockerfile \
  -t compose-vault999-writer:v1.0.0 /root/compose/vault999-writer/

# 2. Recreate container (NOT docker start — must use compose for env_file)
cd /root/compose && docker compose up -d --force-recreate vault999-writer

# 3. Verify token loaded
docker exec vault999-writer python3 -c "import os; print(len(os.environ.get('VAULT_WRITER_TOKEN','')))"

# 4. Test auth
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:5001/seal \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"test","action":"TEST","verdict":"SEAL","epoch":"2026-04-30T00:00:00Z","human_ratifier":"arif","human_signature":"SIG","ratified_at":"2026-04-30T00:00:00Z","payload":{}}'
# Expected: 401

curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:5001/seal \
  -H "Content-Type: application/json" \
  -H "X-Writer-Token: YOUR_TOKEN" \
  -d '...'
# Expected: 200
```

## Verification Tests

| Test | Expected |
|------|----------|
| No token | `401 Missing X-Writer-Token` |
| Wrong token | `401 Invalid X-Writer-Token` |
| Correct token | `200` + seal created |

## Key Gotchas Discovered

1. **Docker secrets require swarm mode** — `deploy.secrets` in compose v2 is not valid. Use bind-mount instead.

2. **`docker update` can't set env vars** — use `env_file` or recreate container. `docker update --env VAR=val` does not work for env injection.

3. **Container recreate resets to baked image** — `docker compose up --force-recreate` uses the CURRENT image, not rebuild. If source changed, must `docker build` first.

4. **Token filename mismatch** — code reads `/run/secrets/vault_writer_token` but bind-mount may create `vault_writer_token.txt`. Verify exact filename inside container.

5. **arifOS image is GHCR, not local build** — cannot hot-patch image layer. Must use volume bind mount or rebuild GHCR image.

6. **`docker rm -f <name>` then `docker compose up -d <name>`** — needed when compose can't rename a running container.

7. **NameError from module-level log calls** — if `logging.basicConfig()` is called later in `main()`, any `log.warning()` or `log.error()` at module level before it runs will raise `NameError: name 'log' is not defined`.

## Compose Service Definition (vault999-writer)

```yaml
vault999-writer:
  image: compose-vault999-writer:v1.0.0
  container_name: vault999-writer
  restart: unless-stopped
  env_file: [.env]
  environment:
    VAULT999_DB: postgresql://arifos_admin:${POSTGRES_PASSWORD}@postgres:5432/vault999
    VAULT_WRITER_TOKEN_FILE: /run/secrets/vault_writer_token
    VAULT_WRITER_TOKEN: ${VAULT_WRITER_TOKEN}  # from .env
    LOG_LEVEL: INFO
  volumes:
    - /root/compose/secrets/vault_writer_token:/run/secrets/vault_writer_token:ro
  ports:
    - "127.0.0.1:5001:5001"
  networks: [arifos_core]
  depends_on:
    postgres:
      condition: service_healthy
  healthcheck:
    test: ["CMD-SHELL", "python3 -c \"import urllib.request; urllib.request.urlopen('http://localhost:5001/health')\""]
    interval: 10s
    timeout: 5s
    retries: 3
    start_period: 5s
```

## D/E (Future Sprint — NOT implemented)

- **Step D:** DB least privilege — create `vault_writer_svc` role with INSERT+SELECT only; revoke from arifos_admin
- **Step E:** Lineage check — `/seal` verifies `cooling_queue` exists and is not yet sealed before writing

## Source Artifacts

After implementation, source saved to:
- `/root/compose/vault999-writer/main.py` — patched FastAPI server
- `/root/compose/vault999-writer/Dockerfile`
- `/root/compose/vault999-writer/requirements.txt`
