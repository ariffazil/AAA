#!/usr/bin/env python3
"""
webhook.py — AAA Webhook Ingress Server

Receives external events (GitHub, cron, manual), wraps each in a signed
CAPSULE, looks up the trigger-map, and dispatches to the A-FORGE agent pool.

Run:
    python ingress/webhook.py
    uvicorn ingress.webhook:app --host 0.0.0.0 --port 3010 --reload

Endpoints:
    POST /webhook/github          — GitHub webhook (HMAC-SHA256 verified)
    POST /webhook/manual/{event}  — Manual trigger (Arif CLI or curl)
    POST /webhook/cron/{schedule} — Cron bridge (daily, weekly)
    GET  /health                  — Liveness probe

Environment:
    GITHUB_WEBHOOK_SECRET   — GitHub webhook shared secret (required for GitHub)
    AFORGE_URL              — A-FORGE agent pool base URL (default: http://localhost:3000)
    ARIFOS_URL              — arifOS kernel URL for floor pre-gate (default: http://localhost:8088)
    AAA_INGRESS_PORT        — Port to bind (default: 3010)
"""
from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional

import httpx
import yaml
from fastapi import FastAPI, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse

# Ensure AAA root on sys.path when run as script
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from core.capsule import CAPSULE, build_capsule  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(name)s  %(message)s")
log = logging.getLogger("aaa.ingress")

# ── Config ────────────────────────────────────────────────────────────────────

GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "")
# fix 2026-10-28: default was :3000 which is Grafana on this host (302 redirect spam).
# A-FORGE lives at :7071 (Sense API, single-port collapse 2026-08-11).
AFORGE_URL            = os.environ.get("AFORGE_URL", "http://127.0.0.1:7071")
AFORGE_OPERATOR_TOKEN = os.environ.get("AFORGE_OPERATOR_TOKEN", os.environ.get("OPERATOR_API_TOKEN", ""))
ARIFOS_URL            = os.environ.get("ARIFOS_URL", "http://localhost:8088")

# fix 2026-10-28: file lives at topology/, not triggers/ - old path made every
# trigger lookup crash FileNotFoundError after auth passed (dead router bug)
_TRIGGER_MAP_PATH = _ROOT / "topology" / "trigger-map.yaml"


def _make_dpop_proof(bearer_token: str, method: str, url: str) -> str:
    """Generate a DPoP proof (ES256 dpop+jwt) for an A-FORGE /peer request.

    A-FORGE runs AFORGE_DPOP_MODE=enforce (deliberate security posture, systemd
    drop-in). Proof claims htm/htu/iat/jti/ath per RFC 9449 as enforced by
    A-FORGE dpop.ts. Key persisted at AAA_DPOP_KEY (default
    /root/.secrets/aaa-dpop-key.pem), chmod 600.
    """
    import base64 as _b64
    import uuid as _uuid
    from jwcrypto import jwk as _jwk
    from jwcrypto import jws as _jws

    key_path = Path(os.environ.get("AAA_DPOP_KEY", "/root/.secrets/aaa-dpop-key.pem"))
    if not key_path.exists():
        key = _jwk.JWK.generate(kty="EC", crv="P-256")
        key_path.write_text(key.export_to_pem(private_key=True, password=None).decode(), encoding="utf-8")
        os.chmod(key_path, 0o600)
    key = _jwk.JWK.from_pem(key_path.read_bytes())

    def _b64u(raw: bytes) -> str:
        return _b64.urlsafe_b64encode(raw).rstrip(b"=").decode()

    pub = json.loads(key.export_public())
    pub = {k: pub[k] for k in sorted(pub) if k in ("crv", "kty", "x", "y")}

    ath = _b64u(hashlib.sha256(bearer_token.encode()).digest())
    header = {"typ": "dpop+jwt", "alg": "ES256", "jwk": pub}
    payload = {
        "htm": method.upper(),
        "htu": url,
        "iat": int(time.time()),
        "jti": str(_uuid.uuid4()),
        "ath": ath,
    }
    signed = _jws.JWS(json.dumps(payload, separators=(",", ":")))
    signed.add_signature(key, alg="ES256", protected=json.dumps(header, separators=(",", ":")))
    return signed.serialize(compact=True)

# ── Trigger map loader ────────────────────────────────────────────────────────

def _load_trigger_map() -> list[dict]:
    data = yaml.safe_load(_TRIGGER_MAP_PATH.read_text(encoding="utf-8")) or {}
    return data.get("triggers", [])


def _match_trigger(event_type: str) -> list[dict]:
    """Return all trigger entries matching event_type. Excludes catch-all."""
    triggers = _load_trigger_map()
    matches = [t for t in triggers if t.get("event") == event_type and t.get("skill")]
    if not matches:
        # Check catch-all
        catch = next((t for t in triggers if t.get("event") == "*"), None)
        if catch:
            return [catch]
    return matches


# ── Dispatch ──────────────────────────────────────────────────────────────────

async def _dispatch(capsule: CAPSULE, trigger: dict) -> dict:
    """
    Send a signed capsule + trigger config to the A-FORGE skill runner.
    Returns the dispatch response or an error dict.
    """
    skill = trigger.get("skill")
    agent_pool = trigger.get("agent_pool", "a-forge")
    authority_tier = trigger.get("authority_tier", "Tier0")
    action = trigger.get("action")

    if action == "HOLD" or not skill:
        log.warning("HOLD: event %s matched catch-all or null skill", capsule.event_type)
        return {"status": "HOLD", "reason": "no matching skill", "event_type": capsule.event_type}

    # Update routing fields on capsule
    routed = capsule.model_copy(update={
        "skill_routed_to": skill,
        "agent_pool": agent_pool,
        "authority_tier": authority_tier,
    })

    payload = {
        "capsule": routed.model_dump(),
        "skill_id": skill,
        "agent_pool": agent_pool,
        "authority_tier": authority_tier,
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # A-FORGE contract: POST /peer/execute (peer-contract gated, arifOS-judged).
            # Old target /skill/run never existed on A-FORGE (discovered live 2026-10-28).
            _headers = {"Content-Type": "application/json"}
            if AFORGE_OPERATOR_TOKEN:
                _headers["Authorization"] = f"Bearer {AFORGE_OPERATOR_TOKEN}"
                _url = f"{AFORGE_URL.rstrip('/').rstrip('/')}/peer/execute"
                _headers["DPoP"] = await asyncio.to_thread(
                    _make_dpop_proof, AFORGE_OPERATOR_TOKEN, "POST", _url
                )
            resp = await client.post(
                f"{AFORGE_URL}/peer/execute",
                json=payload,
                headers=_headers,
            )
            if resp.status_code == 200:
                return {"status": "DISPATCHED", "skill": skill, "response": resp.json()}
            log.error("A-FORGE returned %s for skill %s", resp.status_code, skill)
            return {"status": "DISPATCH_ERROR", "code": resp.status_code, "skill": skill}
    except httpx.ConnectError:
        log.warning("A-FORGE unreachable at %s — capsule logged, dispatch queued", AFORGE_URL)
        return {"status": "QUEUED", "skill": skill, "note": "A-FORGE offline — capsule sealed, retry needed"}


# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="AAA Webhook Ingress",
    description="Receives, verifies, signs, and routes inbound federation events.",
    version="1.0.0",
)


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "ingress": "aaa-webhook-v1",
        "trigger_map": str(_TRIGGER_MAP_PATH),
        "aforge_url": AFORGE_URL,
    }


@app.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(default=None),
    x_github_event: Optional[str] = Header(default=None),
    x_github_delivery: Optional[str] = Header(default=None),
) -> JSONResponse:
    """
    GitHub webhook endpoint.
    GitHub sends: POST with X-Hub-Signature-256, X-GitHub-Event, X-GitHub-Delivery headers.
    """
    raw = await request.body()

    # FAIL-CLOSED: no configured secret means no verification is possible.
    # Reject rather than accept unverified external events.
    if not GITHUB_WEBHOOK_SECRET:
        log.error("GITHUB_WEBHOOK_SECRET not configured — rejecting event (fail-closed)")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="GITHUB_WEBHOOK_SECRET not configured — endpoint fail-closed, delivery rejected",
        )

    capsule = build_capsule(
        raw_payload=raw,
        event_type=_github_event_type(x_github_event, raw),
        source="github",
        source_did="did:github:webhook",
        hmac_header=x_hub_signature_256 or "",
        github_secret=GITHUB_WEBHOOK_SECRET,
    )

    if GITHUB_WEBHOOK_SECRET and not capsule.hmac_verified:
        log.error("HMAC verification failed — delivery %s rejected", x_github_delivery)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="HMAC verification failed — signature mismatch",
        )

    log.info("GitHub event %s → capsule %s (hmac=%s)", capsule.event_type, capsule.event_id[:8], capsule.hmac_verified)

    triggers = _match_trigger(capsule.event_type)
    results = []
    for trigger in triggers:
        result = await _dispatch(capsule, trigger)
        results.append(result)

    return JSONResponse(content={
        "event_id": capsule.event_id,
        "event_type": capsule.event_type,
        "hmac_verified": capsule.hmac_verified,
        "dispatched": len([r for r in results if r.get("status") == "DISPATCHED"]),
        "results": results,
    })


@app.post("/webhook/manual/{event_path:path}")
async def manual_trigger(
    event_path: str,
    request: Request,
    x_hub_signature_256: Optional[str] = Header(default=None),
) -> JSONResponse:
    """
    Manual trigger endpoint. event_path becomes the event_type with dots.
    e.g. POST /webhook/manual/incident → event_type = manual.incident
    """
    raw = await request.body() or b"{}"
    event_type = f"manual.{event_path.replace('/', '.')}"

    # FAIL-CLOSED: manual triggers must present a valid HMAC signature
    # (same shared secret as GitHub) — no signature, no capsule, no dispatch.
    if not GITHUB_WEBHOOK_SECRET:
        log.error("GITHUB_WEBHOOK_SECRET not configured — manual trigger %s rejected (fail-closed)", event_type)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="GITHUB_WEBHOOK_SECRET not configured — endpoint fail-closed, trigger rejected",
        )
    if not x_hub_signature_256:
        log.error("Manual trigger %s rejected — missing X-Hub-Signature-256", event_type)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Hub-Signature-256 — signature required",
        )
    expected = "sha256=" + hmac.new(GITHUB_WEBHOOK_SECRET.encode(), raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, x_hub_signature_256.strip()):
        log.error("Manual trigger %s rejected — HMAC mismatch", event_type)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="HMAC verification failed — signature mismatch",
        )

    capsule = build_capsule(
        raw_payload=raw,
        event_type=event_type,
        source="manual",
        source_did="did:arif:Ω",
        hmac_header=x_hub_signature_256,
        github_secret=GITHUB_WEBHOOK_SECRET,
    )
    # hmac_verified now reflects the real signature check above.

    log.info("Manual trigger %s → capsule %s", event_type, capsule.event_id[:8])

    triggers = _match_trigger(event_type)
    results = []
    for trigger in triggers:
        result = await _dispatch(capsule, trigger)
        results.append(result)

    return JSONResponse(content={
        "event_id": capsule.event_id,
        "event_type": capsule.event_type,
        "results": results,
    })


@app.post("/webhook/cron/{schedule}")
async def cron_trigger(
    schedule: str,
    request: Request,
    x_hub_signature_256: Optional[str] = Header(default=None),
) -> JSONResponse:
    """
    Cron bridge. schedule = 'daily' or 'weekly'.
    Called by cron job or systemd timer on the VPS.
    Callers must present HMAC-SHA256 over the body using GITHUB_WEBHOOK_SECRET.
    """
    event_type = f"cron.{schedule}"

    # FAIL-CLOSED: same signature requirement as the manual endpoint.
    if not GITHUB_WEBHOOK_SECRET:
        log.error("GITHUB_WEBHOOK_SECRET not configured — cron trigger %s rejected (fail-closed)", event_type)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="GITHUB_WEBHOOK_SECRET not configured — endpoint fail-closed, trigger rejected",
        )
    if not x_hub_signature_256:
        log.error("Cron trigger %s rejected — missing X-Hub-Signature-256", event_type)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Hub-Signature-256 — signature required",
        )
    raw = await request.body()
    expected = "sha256=" + hmac.new(GITHUB_WEBHOOK_SECRET.encode(), raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, x_hub_signature_256.strip()):
        log.error("Cron trigger %s rejected — HMAC mismatch", event_type)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="HMAC verification failed — signature mismatch",
        )

    capsule = build_capsule(
        raw_payload=raw or f'{{"schedule":"{schedule}"}}'.encode(),
        event_type=event_type,
        source="cron",
        source_did="did:arif:aaa",
        hmac_header=x_hub_signature_256,
        github_secret=GITHUB_WEBHOOK_SECRET,
    )
    # hmac_verified now reflects the real signature check above.

    log.info("Cron %s → capsule %s", schedule, capsule.event_id[:8])

    triggers = _match_trigger(event_type)
    results = []
    for trigger in triggers:
        result = await _dispatch(capsule, trigger)
        results.append(result)

    return JSONResponse(content={
        "event_id": capsule.event_id,
        "event_type": event_type,
        "results": results,
    })


# ── GitHub event-type normaliser ──────────────────────────────────────────────

def _github_event_type(event_header: Optional[str], raw: bytes) -> str:
    """
    Convert GitHub's X-GitHub-Event + action field to dot-path event_type.
    e.g. event=pull_request, action=opened → github.pull_request.opened
    """
    if not event_header:
        return "github.unknown"
    try:
        body = json.loads(raw)
        action = body.get("action", "")
        if action:
            return f"github.{event_header}.{action}"
        return f"github.{event_header}"
    except (json.JSONDecodeError, Exception):
        return f"github.{event_header}"


# ── Entrypoint ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("AAA_INGRESS_PORT", "3010"))
    log.info("AAA Webhook Ingress starting on port %d", port)
    uvicorn.run("ingress.webhook:app", host="0.0.0.0", port=port, reload=False)
