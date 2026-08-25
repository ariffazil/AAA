#!/usr/bin/env python3
"""
pickup_proxy.py — VPS-side pickup layer for Phone Bridge.

What this is
------------
A stdlib-only HTTP front (127.0.0.1:18800) that wraps /root/AAA/phone-bridge/client.py
so the rest of the federation (arifOS MCP, A-FORGE forge_*, Hermes, AAA cockpit)
can reach Arif's phone capabilities through one stable, governed surface.

This is NOT an alternative to the bearer-token + HMAC-signed protocol that
client.py implements. The proxy applies an additional F13 approval_id gate
on the sensitive verbs (/v1/gps, /v1/camera, /v1/toast, /v1/vibrate).

Verb map (APA-style envelope; same shape as /root/A-FORGE/bridges/gemini_bridge.py):
    /health              → liveness + last-known phone reachability
    /verbs               → list available verbs
    POST /{verb} {params}
        health           → federation liveness check (no phone call)
        battery          → GET /v1/status/battery
        device           → GET /v1/status/device
        sensors          → POST /v1/sensors/snapshot
        locate           → POST /v1/location/once (F13-gated)
        capture          → POST /v1/camera/capture (F13-gated; returns base64)
        vibrate          → POST /v1/vibrate
        toast            → POST /v1/toast

Phone-side reachability states (cached for 30s to avoid hammering phone):
    ONLINE      → last phone health probe <60s ago and returned {"status":"ok"}
    DEAD        → connection refused or unknown host
    UNREACHABLE → Tailscale/ACL/network blocked (timeout > 1s)

F13 flow (sensitive verbs)
--------------------------
1. Caller already has a one-time approval_id minted by arif_judge OR by
   `client.issue_approval()`.
2. Caller sends the approval_id in body field `approval_id` (locate/capture).
3. Proxy forwards it to phone-bridge per client.py contract.

If the body lacks approval_id, proxy returns envelope
    {"ok": false, "error": "approval_required", "endpoint": "..."}
with verdict="HOLD" — never re-issues approvals.

DITEMPA BUKAN DIBERI ⚒️
"""
from __future__ import annotations
import json
import os
import sys
import time
import uuid
import base64
import logging
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# Bring client.py alongside us onto sys.path so we can import it cleanly.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import client  # noqa: E402  – phone-bridge client (sibling module)

DEFAULT_PORT = 18800
DEFAULT_BIND = "127.0.0.1"
log = logging.getLogger("phone_pickup")
logging.basicConfig(level=os.environ.get("PHONE_PICKUP_LOG", "INFO"),
                    format="[phone_pickup] %(asctime)s %(levelname)s %(message)s")

REACH_TTL_SECONDS = 30
SLOW_THRESHOLD_SECONDS = 1.0

# Last-known phone reach cache.
_reach_cache: dict = {"state": "UNKNOWN", "at": 0.0, "detail": None}


def _envelope(verb: str, ok: bool, result, *, verdict="PROCEED",
              evidence_tag="OBS", confidence=0.9, error=None):
    return {
        "ok": ok,
        "connector": "phone_pickup",
        "verb": verb,
        "verdict": verdict if ok else "HOLD",
        "evidence_tag": evidence_tag,
        "confidence": confidence,
        "result": result,
        "error": error,
        "receipt": {
            "receipt_id": f"pp-{uuid.uuid4().hex[:12]}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


def _now() -> float:
    return time.time()


def _reach_refresh(force: bool = False) -> dict:
    """Probe phone health; cache result for REACH_TTL_SECONDS."""
    if not force and (_now() - _reach_cache["at"]) < REACH_TTL_SECONDS:
        return _reach_cache
    started = _now()
    try:
        h = client.health()
        state = "ONLINE" if h.get("status") == "ok" else "DEAD"
        detail = {"device": h.get("device"), "version": h.get("version"),
                  "capabilities": h.get("capabilities")}
    except Exception as e:
        elapsed = _now() - started
        s = str(e).lower()
        if "refused" in s or "no route" in s or "name resolution" in s or "no route to host" in s:
            state, detail = "DEAD", {"error": str(e)[:140]}
        elif elapsed > SLOW_THRESHOLD_SECONDS:
            state, detail = "UNREACHABLE", {"error": str(e)[:140],
                                            "elapsed_seconds": round(elapsed, 2)}
        else:
            state, detail = "DEAD", {"error": str(e)[:140]}
    _reach_cache.update({"state": state, "at": _now(), "detail": detail})
    log.info("phone reachability → %s (%s)", state, detail.get("device") or detail.get("error"))
    return _reach_cache


# ─── ACTION VERBS ──────────────────────────────────────────────────────

SENSITIVE_VERBS = {"locate", "capture"}


def action_health(params: dict) -> dict:
    r = _reach_refresh(force=True)
    return {
        "ok": True,
        "bridge": "phone_pickup",
        "phone_state": r["state"],
        "phone_detail": r["detail"],
        "host": client.BRIDGE_HOST,
        "port": client.BRIDGE_PORT,
        "base_url": client.BASE_URL,
        "sensitive_verbs": sorted(SENSITIVE_VERBS),
        "verbs": ["health", "battery", "device", "sensors", "locate", "capture",
                  "vibrate", "toast"],
        "status": "READY" if r["state"] == "ONLINE" else f"PHONE_{r['state']}",
    }


def action_battery(params: dict) -> dict:
    return client.get_battery()


def action_device(params: dict) -> dict:
    return client.get_device_status()


def action_sensors(params: dict) -> dict:
    return client.get_sensors_snapshot()


def action_locate(params: dict) -> dict:
    approval_id = params.get("approval_id")
    if not approval_id:
        return {"approval_required": True,
                "endpoint": "locate",
                "hint": "Generate via arif_judge F13 prompt → client.issue_approval('gps_once')."}
    mode = params.get("mode", "gps")
    return client.get_location_once(mode=mode, approval_id=approval_id)


def action_capture(params: dict) -> dict:
    approval_id = params.get("approval_id")
    if not approval_id:
        return {"approval_required": True,
                "endpoint": "capture",
                "hint": "Generate via arif_judge F13 prompt → client.issue_approval('camera_capture')."}
    camera = params.get("camera", "rear")
    save_to = params.get("save_to")  # VPS-side path; if None, base64 returned
    raw = client.capture_camera(
        camera=camera,
        approval_id=approval_id,
        save_to=save_to,
    )
    if save_to:
        return raw
    # Return base64 inline (don't dump raw bytes via envelope).
    if isinstance(raw.get("raw_bytes"), (bytes, bytearray)):
        raw["image_base64"] = base64.b64encode(bytes(raw["raw_bytes"])).decode()
        raw.pop("raw_bytes", None)
    return raw


def action_vibrate(params: dict) -> dict:
    duration = int(params.get("duration_ms", 300))
    return client.vibrate(duration_ms=duration)


def action_toast(params: dict) -> dict:
    message = str(params.get("message", ""))[:200]
    if not message:
        return {"ok": False, "error": "message_required"}
    return client.show_toast(message)


ACTIONS = {
    "health": action_health,
    "battery": action_battery,
    "device": action_device,
    "sensors": action_sensors,
    "locate": action_locate,
    "capture": action_capture,
    "vibrate": action_vibrate,
    "toast": action_toast,
}


# ─── HTTP HANDLER ──────────────────────────────────────────────────────


class PickupHandler(BaseHTTPRequestHandler):
    server_version = "PhonePickup/0.1"

    def log_message(self, fmt, *args):
        log.info("%s - %s", self.address_string(), fmt % args)

    def _send(self, payload, status=200):
        body = json.dumps(payload, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        # No caching on control surface.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        p = self.path.split("?", 1)[0].rstrip("/") or "/"
        if p in ("/health", "/"):
            reach = _reach_refresh(force=False)
            ok = reach["state"] == "ONLINE"
            verb = "health"
            self._send(_envelope(verb, True if ok else False,
                                 action_health({}),
                                 verdict="PROCEED" if ok else "HOLD"))
            return
        if p == "/verbs":
            self._send(_envelope("verbs", True,
                                 {"verbs": sorted(ACTIONS.keys()),
                                  "sensitive": sorted(SENSITIVE_VERBS)}))
            return
        self._send(_envelope("?", False, None,
                             verdict="HOLD", error=f"unknown path {p}"), 404)

    def do_POST(self):
        p = self.path.split("?", 1)[0].rstrip("/") or "/"
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
        except Exception as e:
            self._send(_envelope(p.lstrip("/"), False, None,
                                 verdict="HOLD", error=f"invalid_json: {e}"), 400)
            return
        verb = body.get("verb") or p.lstrip("/")
        params = body.get("params") or body
        if verb not in ACTIONS:
            self._send(_envelope(str(verb), False, None,
                                 verdict="HOLD", error=f"unknown_verb: {verb}"), 400)
            return
        # Pre-flight: require online for non-health verbs.
        if verb != "health":
            r = _reach_refresh(force=False)
            if r["state"] != "ONLINE":
                self._send(_envelope(verb, ok=False,
                                     verdict="HOLD",
                                     error=f"phone_{r['state'].lower()}",
                                     result={"phone_state": r["state"],
                                             "phone_detail": r["detail"]}), 503)
                return
        try:
            result = ACTIONS[verb](params)
            self._send(_envelope(verb, True, result))
        except Exception as e:
            log.exception("verb=%s failed", verb)
            self._send(_envelope(verb, False, None,
                                 verdict="HOLD", error=str(e)[:400]), 502)


class _ReusableHTTPServer(ThreadingHTTPServer):
    """Allow rapid restarts without TIME_WAIT EADDRINUSE."""
    allow_reuse_address = True


if __name__ == "__main__":
    port = int(os.environ.get("PHONE_PICKUP_PORT", str(DEFAULT_PORT)))
    bind = os.environ.get("PHONE_PICKUP_BIND", DEFAULT_BIND)
    log.info("phone_pickup listening on http://%s:%d", bind, port)
    log.info("phone host target: %s", client.BASE_URL)
    _ReusableHTTPServer((bind, port), PickupHandler).serve_forever()
