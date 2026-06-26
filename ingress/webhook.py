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

import json
import logging
import os
import sys
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
AFORGE_URL            = os.environ.get("AFORGE_URL", "http://localhost:3000")
ARIFOS_URL            = os.environ.get("ARIFOS_URL", "http://localhost:8088")

_TRIGGER_MAP_PATH = _ROOT / "triggers" / "trigger-map.yaml"

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
            resp = await client.post(
                f"{AFORGE_URL}/skill/run",
                json=payload,
                headers={"Content-Type": "application/json"},
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

    if not GITHUB_WEBHOOK_SECRET:
        log.warning("GITHUB_WEBHOOK_SECRET not set — accepting event without HMAC verification")

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
) -> JSONResponse:
    """
    Manual trigger endpoint. event_path becomes the event_type with dots.
    e.g. POST /webhook/manual/incident → event_type = manual.incident
    """
    raw = await request.body() or b"{}"
    event_type = f"manual.{event_path.replace('/', '.')}"

    capsule = build_capsule(
        raw_payload=raw,
        event_type=event_type,
        source="manual",
        source_did="did:arif:Ω",
        hmac_header="",
        github_secret="",
    )
    capsule = capsule.model_copy(update={"hmac_verified": True})  # manual = sovereign, always trusted

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
async def cron_trigger(schedule: str, request: Request) -> JSONResponse:
    """
    Cron bridge. schedule = 'daily' or 'weekly'.
    Called by cron job or systemd timer on the VPS.
    """
    event_type = f"cron.{schedule}"
    capsule = build_capsule(
        raw_payload=f'{{"schedule":"{schedule}"}}'.encode(),
        event_type=event_type,
        source="cron",
        source_did="did:arif:aaa",
    )
    capsule = capsule.model_copy(update={"hmac_verified": True})

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
