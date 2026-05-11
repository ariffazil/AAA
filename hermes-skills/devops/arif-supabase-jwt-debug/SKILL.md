---
name: arif-supabase-jwt-debug
description: Debug and configure Supabase JWT/JWKS for arifOS token verification
triggers:
  - Supabase JWT configuration for arifOS
  - JWKS endpoint returning empty keys
  - Management API 401 Unauthorized
  - JWT enforcement not working
---

# arifOS + Supabase JWT Debugging

## Trigger
Any task involving Supabase JWT/JWKS configuration for arifOS, or debugging JWT verification failures.

## Context

arifOS uses Supabase only as a **JWT/JWKS provider** for auth token verification — NOT as a database. Vault999 uses Postgres directly.

**Key fact:** Supabase's hosted projects return `{"keys":[]}` from their JWKS endpoint by default. JWT signing keys must be configured in the Supabase dashboard before JWKS returns any keys.

## Non-Obvious Findings (learned the hard way)

### 1. Supabase CLI tokens ≠ Management API tokens
- `sbp_...` tokens from `~/.supabase/access-token` are CLI auth tokens
- They work for: `supabase inspect *`, `supabase db *`, `supabase projects list`
- They do NOT work for direct Management API calls to `api.supabase.com/v1/projects/{ref}/...`
- Management API requires a **personal access token** from https://app.supabase.com/account/tokens

### 2. `supabase inspect` uses a different API path
```
CLI → api.supabase.com/v1/inspector/...  ✓ (sbp_ token works)
API → api.supabase.com/v1/projects/{ref}/config/...  ✗ (401 Unauthorized)
```

### 3. DOTENV: disabled in docker-compose.yml
arifOS containers have `DOTENV: disabled` in their docker-compose entry. This means:
- `.env` files inside the container are NOT loaded
- Environment variables MUST be set in the `environment:` section of docker-compose.yml
- `docker compose up` (recreates containers) loads new env vars
- `docker restart` does NOT reload env vars from compose file

### 4. JWT enforcement is asymmetric
`extract_token_from_header` returns `None` if no `Authorization` header is present. When the calling client doesn't send a Bearer token:
- `enforce=log` → logs nothing (no token to check)
- `enforce=block` → blocks nothing (no token to check)
- `enforce=off` → verifies nothing

So in practice, the calling client must consistently send Bearer tokens for JWT enforcement to actually trigger. This means arifOS's JWT enforcement primarily protects against *malformed tokens*, not *absent tokens*.

### 5. arifOS git branch is `main`, compose is `master`
- arifOS: `origin/main`
- compose: `origin/master`

## JWKS URL
```
https://utbmmjmbolmuahwixjqc.supabase.co/.well-known/jwks.json
```

## Two Configuration Paths

### Option A: Supabase Dashboard (proper JWT)
1. Go to https://app.supabase.com/account/tokens
2. Create personal access token → use as management token
3. Or configure JWT settings manually at:
   `https://supabase.com/dashboard/project/utbmmjmbolmuahwixjqc/auth/providers?panel=jwks`

### Option B: Self-hosted JWKS (zero external dependency)
1. Generate RSA key pair
2. Host public JWKS at a VPS endpoint
3. Set `SUPABASE_JWKS_URL=https://your-vps/jwks.json` in compose environment
4. Supabase tokens signed with the matching private key will verify

## Docker Compose Env Var Pattern (arifOS)
```yaml
environment:
  - JWT_ENFORCE_MODE=enforce-block  # was absent due to DOTENV: disabled
  - SUPABASE_JWKS_URL=https://utbmmjmbolmuahwixjqc.supabase.co/.well-known/jwks.json
  # ... other vars
```

## Verification Commands
```bash
# Check JWKS content
curl -s https://utbmmjmbolmuahwixjqc.supabase.co/.well-known/jwks.json | python3 -m json.tool

# Check if container has env vars (after docker compose up)
docker exec arifosmcp env | grep -E "JWT|SUPABASE"

# Check arifOS logs for JWT errors
docker logs arifosmcp --tail 50 | grep -i "jwt\|jwks\|unauthorized"

# Health check
curl -s http://localhost:8080/health | python3 -m json.tool
```

## Related
- `arifos-vault999-audit`: Vault999 audit methodology (ground-truth approach)
- `arif-os-readiness-debugging`: General arifOS container debugging
