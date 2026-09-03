# vault999-writer Audit Findings — 2026-05-17

## Service Profile

- **Location:** `/root/A-FORGE/deploy/arifOS/vault999-writer/`
- **Type:** Python 3.12-alpine FastAPI service, custom Dockerfile
- **Role:** Sole service allowed to INSERT into `vault_seals` table
- **Auth:** `X-Writer-Token` header via mounted Docker secret
- **Port:** 5001

## Issues Found & Fixed

### Issue 1: `blake3` not in requirements.txt

**Severity:** High — silent hash algorithm fallback on every restart

**Root Cause:** `blake3` was manually installed inside the container or inherited from a parent image layer, but was NOT in `requirements.txt`. Every `docker compose build --no-cache` or fresh deploy would reinstall from requirements.txt only, missing `blake3`. Code has an `ImportError` guard that falls back to `hashlib.sha256`, producing different hashes than `blake3`.

**Impact:** Hash mismatch in vault999 chain — all seals after a restart would have SHA256 hashes instead of blake3, breaking chain integrity verification.

**File:** `vault999-writer/requirements.txt`
**Fix:** Added `blake3>=1.0.8`

```
fastapi>=0.109.0
uvicorn[standard]>=0.23.0
asyncpg>=0.29.0
pydantic>=2.0.0
python-dotenv>=1.0.0
httpx>=0.27.0
blake3>=1.0.8   ← ADDED
```

---

### Issue 2: Duplicate code in `compute_chain_hash`

**Severity:** Low — code smell, no functional impact

**File:** `vault999-writer/main.py`, lines 143-145
**Problem:** Exact duplicate of lines 140-142. Dead code.

```python
# Lines 140-142 (real code):
if _HAS_BLAKE3:
    return blake3.blake3(chain_input.encode("utf-8")).hexdigest(32)
return hashlib.sha256(chain_input.encode("utf-8")).hexdigest()

# Lines 143-145 (duplicate — REMOVED):
if _HAS_BLAKE3:
    return blake3.blake3(chain_input.encode("utf-8")).hexdigest(32)
return hashlib.sha256(chain_input.encode("utf-8")).hexdigest()
```

**Fix:** Deleted duplicate block.

---

### Issue 3: `from datetime import datetime` inside function

**Severity:** Low — works but poor style

**File:** `vault999-writer/main.py`, line 180 (inside `VaultDB.write_seal`)
**Problem:** `datetime` was already imported at module level (line 18), but a second import appeared inside the function body.

**Fix:** Removed the inline import.

---

## Audit Commands Used

```bash
# Locate the service files
ls /root/A-FORGE/deploy/arifOS/vault999-writer/

# Check requirements.txt (before fix)
cat /root/A-FORGE/deploy/arifOS/vault999-writer/requirements.txt

# Check Dockerfile
cat /root/A-FORGE/deploy/arifOS/vault999-writer/Dockerfile

# Rebuild container
cd /root/A-FORGE/deploy/arifOS && docker compose build vault999-writer

# Restart
docker compose up -d vault999-writer

# Verify blake3 available inside container
docker exec vault999-writer python -c "import blake3; print(blake3.blake3(b'test').hexdigest(32))"

# Health check
curl -s http://localhost:5001/health
```

## Verification Results

- blake3 loads: ✅ `4878ca0425c739fa427f7eda20fe845f6b2e46ba5fe2a14df5b1e32f50603215`
- Health: ✅ `{"status":"healthy","vault_seals_count":4,"pending_holds":0}`
- Container restarted cleanly: ✅

## Pattern to Watch

For any Python service in a custom Dockerfile:
- Check `requirements.txt` completeness — not just imports that work in dev
- Python C-extension packages (`blake3`, `uvloop`, `asyncpg`) need special wheels — `alpine` linux needs `musllinux` variants
- Import-guarded fallbacks (`try blake3; except ImportError: hashlib.sha256`) are a code smell: they hide incomplete installs
- Verify the preferred implementation actually loads: `docker exec <container> python -c "import <package>"`