#!/usr/bin/env python3
"""SCT autonomous renewal — keeps the federation session envelope fresh.

WHY: SCT capability tokens are short-lived by design (TTL = 1 hour, see
arifosmcp/runtime/sct.py). Without a renewer, the session envelope at
/root/.arifos/federation-session.json goes stale and every SCT-gated call
(forge_vault, arif_seal, arif_judge) fails with SCT_GATE: SCT_EXPIRED.

MECHANISM: re-mint via arif_init (sovereign HMAC-rootkey path, actor
ariffazil). The shared secret ARIFOS_ROOTKEY lives in the KUNCI-MAS vault
(kunci-mas.env `export ARIFOS_ROOTKEY=...`, mirrored to kunci-mas.flat.env
which systemd loads). This script reads it from env or the flat file and
NEVER prints it.

USAGE:
    python3 /root/scripts/sct_renew.py            # renew only if near expiry
    python3 /root/scripts/sct_renew.py --force    # always re-mint
    python3 /root/scripts/sct_renew.py --check    # report only, no renew

CRON (root): */30 * * * * python3 /root/scripts/sct_renew.py >> /root/forge_work/site-audit/sct-renew.log 2>&1
"""
import base64
import datetime
import hashlib
import hmac
import json
import os
import shutil
import sys
import urllib.request

ENVELOPE = "/root/.arifos/federation-session.json"
FLAT_ENV = "/root/.secrets/kunci-mas.flat.env"
KERNEL_URL = "http://127.0.0.1:8088/mcp"
RENEW_BUFFER_S = 1800  # renew when < 30 min left on the token
NONCE_TAG = "sct-autorenew"


def read_rootkey() -> str | None:
    for var in ("ARIFOS_ROOTKEY", "ARIF_ROOTKEY"):
        v = os.environ.get(var)
        if v:
            return v
    if os.path.exists(FLAT_ENV):
        for line in open(FLAT_ENV):
            line = line.strip()
            for var in ("ARIFOS_ROOTKEY=", "ARIF_ROOTKEY="):
                if line.startswith(var):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def parse_sct(token: str) -> dict | None:
    """Decode sct_v1.<b64 payload>.<sig> — returns claims dict or None."""
    if not token or not token.startswith("sct_v1."):
        return None
    try:
        payload = token.split(".")[1]
        pad = payload + "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(pad))
    except Exception:
        return None


def parse_sct_exp(token: str) -> int | None:
    claims = parse_sct(token)
    return claims.get("exp") if claims else None


def mcp_init(args: dict) -> dict:
    body = json.dumps(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
         "params": {"name": "arif_init", "arguments": args}}
    ).encode()
    req = urllib.request.Request(
        KERNEL_URL, data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        resp = json.loads(r.read())
    for c in resp.get("result", {}).get("content", []):
        try:
            return json.loads(c.get("text", ""))
        except Exception:
            continue
    return {"raw_text": " ".join(c.get("text", "") for c in resp.get("result", {}).get("content", []))}


def main() -> int:
    check_only = "--check" in sys.argv
    force = "--force" in sys.argv

    if not os.path.exists(ENVELOPE):
        print(f"SCT_RENEW: NO_ENVELOPE at {ENVELOPE}", flush=True)
        return 1

    env = json.load(open(ENVELOPE))
    tok = env.get("session_token")
    exp = parse_sct_exp(tok)
    now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

    if exp is not None and not force:
        left = exp - now
        if left > RENEW_BUFFER_S:
            print(f"SCT_RENEW: FRESH {left}s left — no renew needed (session={env.get('session_id')})", flush=True)
            return 0
        state = "EXPIRED" if left <= 0 else f"{left}s left (buffer {RENEW_BUFFER_S}s)"
    else:
        state = "NO_VALID_TOKEN" if not force else "FORCED"

    if check_only:
        print(f"SCT_RENEW: CHECK {state} — would renew (session={env.get('session_id')})", flush=True)
        return 0

    rootkey = read_rootkey()
    if not rootkey:
        print("SCT_RENEW: NO_ROOTKEY — ARIFOS_ROOTKEY not in env or flat env. Source kunci-mas.env first.", flush=True)
        return 2

    nonce = f"{now}-{NONCE_TAG}"
    sig = hmac.new(rootkey.encode(), nonce.encode(), hashlib.sha256).hexdigest()
    prev_sid = env.get("session_id")

    res = mcp_init({
        "actor_id": "ariffazil",
        "intent": "autonomous SCT renewal",
        "mode": "init",
        "nonce": nonce,
        "actor_signature": sig,
        "ack_irreversible": False,
        "verbosity": "full",  # full egress required: light/minimal strips re-mint
        "previous_session_hash": prev_sid,
    })

    if res.get("status") not in ("OK", "completed"):
        detail = json.dumps({k: res.get(k) for k in ("status", "verdict", "reason", "message", "error", "raw_text") if k in res})[:500]
        print(f"SCT_RENEW: RENEW_FAIL ({state}) — {detail}", flush=True)
        return 3
    if not res.get("session_id"):
        # kernel nests the mint result under result.result in some releases
        nested = res.get("result")
        if isinstance(nested, dict):
            res.update(nested)
    if not res.get("session_id"):
        detail = json.dumps({k: res.get(k) for k in ("status", "verdict", "reason", "message", "error", "raw_text") if k in res})[:500]
        print(f"SCT_RENEW: RENEW_FAIL ({state}) — {detail}", flush=True)
        return 3

    new_tok = res.get("session_token")
    if not new_tok:
        print("SCT_RENEW: RENEW_FAIL — kernel returned no session_token", flush=True)
        return 3

    # Canonical session id = the sid bound inside the SCT itself
    claims = parse_sct(new_tok)
    sid = (claims or {}).get("sid") or res.get("session_id")
    bridge = (res.get("session_bridge") or {}).get("sct_sid")

    # Atomic envelope update with backup (F1 reversible-first)
    shutil.copy2(ENVELOPE, ENVELOPE + ".bak")
    env["session_id"] = sid
    env["session_token"] = new_tok
    env["actor_id"] = "ariffazil"
    env["previous_session_id"] = prev_sid
    if bridge:
        env["session_bridge_id"] = bridge
    env["renewed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tmp = ENVELOPE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(env, f, indent=2)
    os.chmod(tmp, 0o600)
    os.replace(tmp, ENVELOPE)

    new_exp = parse_sct_exp(new_tok)
    exp_str = datetime.datetime.fromtimestamp(new_exp, datetime.timezone.utc).isoformat() if new_exp else "?"
    print(f"SCT_RENEW: RENEWED session={sid} exp={exp_str} (prev={prev_sid})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
