---
id: FORGE-fastapi-api-builder
name: FORGE-fastapi-api-builder
version: 1.0.0-2026.07.17
description: "FastAPI API builder for organ bridge middleware and federation REST endpoints."
owner: A-FORGE
risk_tier: medium
floor_scope: ['F1', 'F4', 'F12']
autonomy_tier: T1
---
# ⚒️ FastAPI API Builder — Organ Bridge Middleware

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Build and maintain FastAPI/Node API endpoints for `/api/observatory/v1/*` and organ bridge surfaces: middleware stack, CORS, error handling, health probes, MCP proxy endpoints.

## When to Use
- Creating new API endpoints in arifOS, GEOX, WEALTH, WELL FastAPI servers
- Adding middleware — auth, CORS, request logging, rate limiting
- Error handling patterns — structured error responses, exception handlers
- MCP-to-HTTP bridge endpoints for observatory consumption

## When NOT to Use
- Frontend routes — use `nextjs-mastery` or `react-spa-discipline`
- Database schema design — use `postgres-schema-design`
- Deployment/Docker — use `cicd-docker-deploy`

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | Version all breaking API changes (`/v1/`, `/v2/`); never mutate in place |
| F2 TRUTH | Response schemas must match documented contracts; no undocumented fields |
| F4 CLARITY | One endpoint = one responsibility; no mega-endpoints |
| F11 AUDIT | Every request logged with actor, intent, timestamp |
| F12 INJECTION | All inputs sanitized; never trust request body without validation |

## Commands & Patterns

```python
# FastAPI organ endpoint pattern
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/observatory/v1")

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: float

@router.get("/health", response_model=HealthResponse)
async def health():
    return {"status": "ok", "version": "1.0.0", "uptime": time.monotonic()}

# CORS middleware
app.add_middleware(CORSMiddleware, allow_origins=["https://arifos.arif-fazil.com"])

# Structured error handler
@app.exception_handler(AppError)
async def app_error_handler(request, exc):
    return JSONResponse(status_code=exc.code, content={"error": exc.message, "trace": exc.trace_id})
```

## Refusal Surface
- ❌ Endpoints that mutate without lease/session auth
- ❌ Returning raw database models as response (always use Pydantic schema)
- ❌ Skipping input validation on POST/PUT/PATCH endpoints
- ❌ Hardcoded organ ports in API routes — use env config
- ❌ Sync endpoints for I/O-bound operations (must be async)
