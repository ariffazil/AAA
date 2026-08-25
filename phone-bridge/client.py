"""phone_bridge — VPS-side client for Hermes.

Hermes talks to the phone through this skill. It does NOT talk to
Termux directly. The bridge enforces F13 policy on the device edge.
"""

import os
import json
import time
import hmac
import hashlib
import secrets
import requests
from pathlib import Path
from typing import Optional, Literal

# ─── CONFIG ────────────────────────────────────────────────────────────────

BRIDGE_HOST = os.environ.get("BRIDGE_PHONE_HOST", "127.0.0.1")
BRIDGE_PORT = int(os.environ.get("BRIDGE_PORT", "8765"))
BRIDGE_TOKEN = os.environ.get("BRIDGE_TOKEN", "")
SIGNING_SECRET = os.environ.get("BRIDGE_SIGNING_SECRET", "")

# Tunnel URLs (e.g. *.lhr.life) are HTTPS on 443 with no port suffix.
# Plain Tailscale/localhost hosts use http://host:port.
if os.environ.get("BRIDGE_USE_HTTPS") == "1" or BRIDGE_HOST.endswith(".lhr.life"):
    BASE_URL = f"https://{BRIDGE_HOST}"
else:
    BASE_URL = f"http://{BRIDGE_HOST}:{BRIDGE_PORT}"

# Approval TTL window (must match server)
APPROVAL_TTL_SECONDS = 300
NONCE_WINDOW_SECONDS = 60

# ─── SIGNED REQUESTS ───────────────────────────────────────────────────────


def _sign_request(body: str) -> dict:
    """Build signature headers for a POST request."""
    timestamp = str(int(time.time()))
    nonce = secrets.token_hex(16)
    body_hash = hashlib.sha256(body.encode()).hexdigest()
    message = f"{timestamp}:{nonce}:{body_hash}"
    signature = hmac.new(
        SIGNING_SECRET.encode(), message.encode(), hashlib.sha256
    ).hexdigest()

    return {
        "X-Timestamp": timestamp,
        "X-Nonce": nonce,
        "X-Signature": signature,
        "Authorization": f"Bearer {BRIDGE_TOKEN}",
        "Content-Type": "application/json",
    }


def _generate_approval_id(endpoint: str, ttl_seconds: int = APPROVAL_TTL_SECONDS) -> str:
    """Generate one-time approval_id scoped to a specific endpoint."""
    random_part = secrets.token_hex(8)
    expiry = int(time.time()) + ttl_seconds
    return f"f13_{random_part}_{endpoint}_{expiry}"


# ─── HEALTH & STATUS (no approval needed) ─────────────────────────────────


def health() -> dict:
    """Check bridge availability."""
    r = requests.get(f"{BASE_URL}/v1/health", timeout=5)
    r.raise_for_status()
    return r.json()


def get_battery() -> dict:
    """Get phone battery status."""
    r = requests.get(
        f"{BASE_URL}/v1/status/battery",
        headers={"Authorization": f"Bearer {BRIDGE_TOKEN}"},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def get_device_status() -> dict:
    """Get phone device info."""
    r = requests.get(
        f"{BASE_URL}/v1/status/device",
        headers={"Authorization": f"Bearer {BRIDGE_TOKEN}"},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


# ─── SENSITIVE ACTIONS (require approval_id) ────────────────────────────────


def get_location_once(
    mode: Literal["gps", "network", "passive"] = "gps",
    approval_id: Optional[str] = None,
) -> dict:
    """
    One-shot GPS fix. Requires Hermes-generated approval_id.

    Caller MUST generate approval_id via arif_judge → Telegram F13 prompt
    BEFORE calling this function. The phone enforces one-time, scoped,
    expiry-bound approval.
    """
    if not approval_id:
        raise ValueError("approval_id required (F13-gated)")

    body = json.dumps({"mode": mode, "approval_id": approval_id})
    headers = _sign_request(body)

    r = requests.post(
        f"{BASE_URL}/v1/location/once",
        headers=headers,
        data=body,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def capture_camera(
    camera: Literal["rear", "front"] = "rear",
    approval_id: Optional[str] = None,
    delete_local_after_upload: bool = True,
    save_to: Optional[str] = None,
) -> dict:
    """
    Capture photo from rear/front camera. Requires approval_id.

    Returns dict with artifact metadata. Photo downloaded to `save_to` if set.
    """
    if not approval_id:
        raise ValueError("approval_id required (F13-gated)")

    body = json.dumps({
        "camera": camera,
        "approval_id": approval_id,
        "artifact_policy": {
            "upload_to_vps": True,
            "delete_local_after_upload": delete_local_after_upload,
            "delete_vps_after_hours": 24,
        },
    })
    headers = _sign_request(body)

    r = requests.post(
        f"{BASE_URL}/v1/camera/capture",
        headers=headers,
        data=body,
        timeout=30,
    )
    r.raise_for_status()

    artifact_id = r.headers.get("X-Artifact-ID", f"unknown_{int(time.time())}.jpg")

    if save_to:
        Path(save_to).parent.mkdir(parents=True, exist_ok=True)
        with open(save_to, "wb") as f:
            f.write(r.content)
        return {
            "artifact_id": artifact_id,
            "saved_to": save_to,
            "size_bytes": len(r.content),
            "camera": camera,
        }
    else:
        return {
            "artifact_id": artifact_id,
            "size_bytes": len(r.content),
            "camera": camera,
            "raw_bytes": r.content,  # Caller must handle
        }


def get_sensors_snapshot() -> dict:
    """One-shot sensor reading (accelerometer, gyro, light)."""
    r = requests.post(
        f"{BASE_URL}/v1/sensors/snapshot",
        headers={"Authorization": f"Bearer {BRIDGE_TOKEN}"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def vibrate(duration_ms: int = 300) -> dict:
    """Vibrate the phone."""
    r = requests.post(
        f"{BASE_URL}/v1/vibrate",
        headers={"Authorization": f"Bearer {BRIDGE_TOKEN}"},
        timeout=5,
    )
    r.raise_for_status()
    return r.json()


def show_toast(message: str) -> dict:
    """Show toast notification on phone."""
    r = requests.post(
        f"{BASE_URL}/v1/toast",
        headers={
            "Authorization": f"Bearer {BRIDGE_TOKEN}",
            "Content-Type": "application/json",
        },
        json={"message": message[:200]},  # Truncate for safety
        timeout=5,
    )
    r.raise_for_status()
    return r.json()


# ─── APPROVAL HELPER (Hermes calls this after F13 approval) ─────────────────


def issue_approval(endpoint: str, ttl_seconds: int = APPROVAL_TTL_SECONDS) -> str:
    """
    Generate a one-time approval_id. Caller MUST have already received
    F13 approval via Telegram before calling this.

    Returns approval_id string to pass to get_location_once() or capture_camera().
    """
    return _generate_approval_id(endpoint, ttl_seconds)


# ─── EXAMPLE: F13 PROPOSAL ──────────────────────────────────────────────────

PROPOSAL_TEMPLATE = """
🔒 **Hermes requests phone action**

Action: {action}
Purpose: {purpose}
Target: arif-phone (S24)
Tailscale: {host}:{port}
TTL: {ttl_seconds}s

Artifact policy:
• Upload to VPS: {upload}
• Delete from phone after upload: {delete_local}
• Delete from VPS after: {retention_hours}h

Approve? [YES] [NO]
"""


def build_f13_proposal(
    action: str,
    purpose: str,
    ttl_seconds: int = 300,
    upload: bool = True,
    delete_local: bool = True,
    retention_hours: int = 24,
) -> str:
    """Build the F13 Telegram proposal message."""
    return PROPOSAL_TEMPLATE.format(
        action=action,
        purpose=purpose,
        host=BRIDGE_HOST,
        port=BRIDGE_PORT,
        ttl_seconds=ttl_seconds,
        upload=upload,
        delete_local=delete_local,
        retention_hours=retention_hours,
    )