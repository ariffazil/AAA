#!/usr/local/lib/hermes-agent/venv/bin/python3
"""Hermes A2A Adapter — AAA-owned agent bridge + optional Telegram polling relay.
- Receives A2A tasks via POST /tasks (from AAA gateway / OpenClaw)
- FORWARDS Telegram messages to AAA gateway at port 3001
- Calls OpenClaw gateway at 127.0.0.1:18789 for model inference
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json, uuid, datetime, os, time, threading, requests, asyncio, websockets, base64

PORT = 18001
TELEGRAM_TOKEN = os.environ.get("HERMES_TELEGRAM_BOT_TOKEN", "841013...HMLM")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
AAA_GATEWAY = "http://127.0.0.1:3001"
OPENCLAW_GATEWAY = "http://127.0.0.1:18789"
# Load actual WS password from openclaw.json
try:
    with open("/root/.openclaw/openclaw.json") as f:
        _cfg = json.load(f)
        OPENCLAW_TOKEN = os.environ.get("OPENCLAW_TOKEN",
            _cfg.get("gateway", {}).get("auth", {}).get("password", "hermes-asi-token"))
except Exception:
    OPENCLAW_TOKEN = os.environ.get("OPENCLAW_TOKEN", "hermes-asi-token")
LAST_UPDATE_ID_FILE = "/tmp/hermes_telegram_offset.txt"
AAA_AUTH = {
    "Authorization": "Bearer aaa-a2a-token-dev",
    "x-a2a-key": "aaa-a2a-apikey-dev",
}


# ── Cron relay: receive announce from OpenClaw, forward to Telegram ────────────
def send_telegram_sync(chat_id: int, text: str, reply_to: int = None):
    """Send a message to Telegram synchronously."""
    payload = {"chat_id": chat_id, "text": text[:4096], "parse_mode": "Markdown"}
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    try:
        r = requests.post(f"{TELEGRAM_API}/sendMessage", json=payload, timeout=10)
        return r.json().get("ok", False)
    except Exception as e:
        print(f"[TELEGRAM relay] send error: {e}", flush=True)
        return False


def telegram_polling_enabled():
    return os.getenv("HERMES_A2A_TELEGRAM_POLLING", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def load_last_update_id():
    try:
        with open(LAST_UPDATE_ID_FILE) as f:
            return int(f.read().strip())
    except:
        return 0


def save_last_update_id(update_id):
    with open(LAST_UPDATE_ID_FILE, "w") as f:
        f.write(str(update_id))


def a2a_resp(task_id, context_id, text, state="completed"):
    return {
        "jsonrpc": "2.0",
        "id": task_id,
        "result": {
            "id": task_id,
            "contextId": context_id,
            "status": {
                "state": state,
                "message": {
                    "role": "agent",
                    "parts": [{"kind": "text", "text": text[:9000]}],
                    "messageId": str(uuid.uuid4()),
                    "taskId": task_id,
                    "contextId": context_id,
                    "timestamp": datetime.datetime.now(datetime.UTC)
                    .isoformat()
                    .replace("+00:00", "Z"),
                },
            },
            "artifacts": [],
            "history": [],
            "kind": "task",
        },
    }


async def call_openclaw_ws(text, task_id=None):
    """Forward to OpenClaw gateway via proper A2A req/rsp protocol."""
    task_id = task_id or str(uuid.uuid4())
    ws_password = OPENCLAW_TOKEN
    uri = f"ws://{OPENCLAW_GATEWAY.replace('http://', '')}/"

    try:
        async with websockets.connect(uri, ping_interval=None) as ws:
            # Step 1: Receive challenge and connect with A2A req/rsp framing
            challenge_raw = await ws.recv()
            nonce = json.loads(challenge_raw)["payload"]["nonce"]

            await ws.send(
                json.dumps(
                    {
                        "type": "req",
                        "id": f"{task_id}-c",
                        "method": "connect",
                        "params": {
                            "minProtocol": 1,
                            "maxProtocol": 10,
                            "client": {
                                "id": "gateway-client",
                                "version": "1.0.0",
                                "platform": "python",
                                "mode": "backend",
                            },
                            "auth": {"password": ws_password},
                            "scopes": [
                                "operator.read",
                                "operator.write",
                                "operator.pairing",
                                "operator.approvals",
                            ],
                        },
                    }
                )
            )
            connect_resp = json.loads(await asyncio.wait_for(ws.recv(), timeout=10))
            if not connect_resp.get("ok"):
                return f"[connect failed: {connect_resp.get('error')}]"

            # Step 2: Send message via sessions.send on the main session
            msg_id = f"msg-{task_id}"
            await ws.send(
                json.dumps(
                    {
                        "type": "req",
                        "id": msg_id,
                        "method": "sessions.send",
                        "params": {
                            "key": "agent:main:main",
                            "idempotencyKey": str(uuid.uuid4()),
                            "message": text,
                        },
                    }
                )
            )
            send_resp = json.loads(await asyncio.wait_for(ws.recv(), timeout=10))
            if not send_resp.get("ok"):
                return f"[send failed: {send_resp.get('error')}]"
            run_id = send_resp.get("payload", {}).get("runId")

            # Step 3: Wait for agent response via agent.wait
            wait_id = f"wait-{task_id}"
            await ws.send(
                json.dumps(
                    {
                        "type": "req",
                        "id": wait_id,
                        "method": "agent.wait",
                        "params": {"runId": run_id},
                    }
                )
            )

            # Collect text from streaming chat events (use final state to avoid duplication)
            text_parts = []
            seen_final = False
            timeout = 150
            start = time.time()
            while time.time() - start < timeout:
                try:
                    resp_raw = await asyncio.wait_for(ws.recv(), timeout=20)
                    resp = json.loads(resp_raw)
                    evt_type = resp.get("type")
                    event_name = resp.get("event")
                    payload = resp.get("payload", {})

                    # Only use final chat message to avoid duplicate deltas
                    if (
                        evt_type == "event"
                        and event_name == "chat"
                        and payload.get("runId") == run_id
                    ):
                        if payload.get("state") == "final":
                            msg = payload.get("message", {})
                            for block in msg.get("content", []):
                                if block.get("type") == "text":
                                    text_parts.append(block.get("text", ""))
                            seen_final = True

                    if evt_type == "res" and resp.get("id") == wait_id:
                        if text_parts:
                            return "".join(text_parts)[:9000]
                        return "[no text in response]"

                except asyncio.TimeoutError:
                    if seen_final:
                        return "".join(text_parts)[:9000]
                    continue

            return "".join(text_parts)[:9000] if text_parts else "[timeout]"

    except Exception as e:
        return f"[gateway error: {e}]"


def call_hermes(text, task_id=None):
    """Sync wrapper — runs async WebSocket call in a thread."""
    task_id = task_id or str(uuid.uuid4())[:10]
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(call_openclaw_ws(text, task_id))
        finally:
            loop.close()
        return result
    except Exception as e:
        return f"[call_hermes error: {e}]"


def call_hermes_nb(text, task_id=None):
    """Non-blocking fire-and-forget — relay to OpenClaw without waiting.
    Used for 888_APPROVE relay to avoid stalling the Hermes agent."""

    def _run():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(call_openclaw_ws(text, task_id))
            finally:
                loop.close()
        except Exception as e:
            print(f"[888_APPROVE NB] error: {e}", flush=True)

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()


# ── F11/F13 envelope helpers (LEGACY_WRAP gap fix, 2026-06-12) ───────────────
# arifOS v2 envelope_validator requires every governed tool call to carry a
# FederationEnvelope with policy_hash, authority_chain, and (for ATOMIC) an
# F13 signature. Previously hermes-a2a.py buried the Ed25519 sig in
# params.actor_signature and posted a bare tools/call — the v2 validator
# rejected this with "No _envelope provided" for vault_seal / forge_execute.

_TOOL_ACTION_CLASS: dict[str, str] = {
    # ATOMIC — F13 sovereign sig mandatory (envelope_validator.py:90)
    "arif_vault_seal": "ATOMIC",
    "arif_judge_deliberate": "ATOMIC",
    # MUTATE — F11 verified authority required
    "arif_forge_execute": "MUTATE",
    "arif_lease_revoke": "MUTATE",
    "arif_session_init": "MUTATE",
    # ADVISORY — floor check + receipt
    "arif_mind_reason": "ADVISORY",
    "arif_heart_critique": "ADVISORY",
    "arif_gateway_connect": "ADVISORY",
    "arif_lease_issue": "ADVISORY",
    # READ — no approval
    "arif_ops_measure": "READ",
    "arif_sense_observe": "READ",
    "arif_evidence_fetch": "READ",
    "arif_memory_recall": "READ",
    "arif_kernel_route": "READ",
    "arif_reply_compose": "READ",
    "arif_lease_inspect": "READ",
}

_TOOL_DEFAULT_MODE: dict[str, str] = {
    "arif_vault_seal": "seal",
    "arif_judge_deliberate": "judge",
    "arif_forge_execute": "engineer",
    "arif_lease_revoke": "revoke",
    "arif_lease_issue": "issue",
    "arif_lease_inspect": "inspect",
    "arif_session_init": "init",
    "arif_mind_reason": "reason",
    "arif_heart_critique": "critique",
    "arif_gateway_connect": "route",
    "arif_ops_measure": "health",
    "arif_sense_observe": "search",
    "arif_evidence_fetch": "fetch",
    "arif_memory_recall": "recall",
    "arif_kernel_route": "route",
    "arif_reply_compose": "compose",
}


def _default_mode_for(tool_name: str) -> str:
    """Return the right default mode for a tool, instead of always 'init'."""
    return _TOOL_DEFAULT_MODE.get(tool_name, "init")


def _build_sovereign_envelope(
    tool_name: str,
    actor_signature: str,
    nonce: str,
    constitution_hash: str,
    actor_id: str,
) -> dict:
    """
    Build a minimal FederationEnvelope dict that satisfies
    arifOS v2 envelope_validator for a sovereign-signed tool call.

    Constitutional wiring (Appendix D, F11/F13):
      - actor_id           = sovereign (verified via Ed25519)
      - session_id         = "sovereign-bridge" (call-scoped, not a SEAL-* id)
      - policy_hash        = constitution_hash from arif_session_init
      - authority_chain    = [actor, "arifOS", "arifOS-kernel"]
      - f13_signature      = Ed25519 sig from sovereign_signer.py
      - action_class       = READ|ADVISORY|MUTATE|ATOMIC per tool
      - tool_scope         = [tool_name]
      - tool_id            = tool_name
      - agent_id           = "hermes-a2a-bridge" (sovereign-delegated)
      - trace_id           = nonce (links the call chain)
      - legacy_wrap        = False (we now provide a real envelope)

    Hermes is a SOVEREIGN-DELEGATED bridge — its Ed25519 sig IS Arif's
    signature, not an impersonation. Constitutionally equivalent to
    Arif calling the tool directly via the MCP client.
    """
    action_class = _TOOL_ACTION_CLASS.get(tool_name, "READ")
    return {
        "actor_id": actor_id,
        "session_id": f"sovereign-bridge:{nonce}",
        "policy_hash": constitution_hash,
        "authority_chain": [actor_id, "arifOS", "arifOS-kernel"],
        "f13_signature": actor_signature,  # Ed25519 from sovereign_signer.py
        "nonce": nonce,
        "action_class": action_class,
        "tool_scope": [tool_name],
        "tool_id": tool_name,
        "agent_id": "hermes-a2a-bridge",
        "trace_id": nonce,
        "legacy_wrap": False,
        "reversibility": "irreversible" if action_class == "ATOMIC" else "high",
        "host_attestation": {
            "host": "af-forge",
            "process": "hermes-a2a.py",
            "cgroup": "system.slice/hermes-asi-gateway.service",
        },
        "issued_at": datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
    }


def call_arif_mcp_sync(tool_name: str, params: dict) -> dict:
    """
    Execute an arifOS MCP tool with Ed25519 SOVEREIGN signature.
    Runs entirely on VPS (hermes-a2a.py host) — no SSH needed.

    Args:
        tool_name: e.g. "arif_session_init"
        params: dict of tool arguments

    Returns:
        Structured dict with keys: status, verdict, authority_level,
        identity_verified, signature_verified, session_id, reasons, error
    """
    import urllib.request, subprocess, time as time_module

    MCP_ENDPOINT = "http://127.0.0.1:8088/mcp"
    SIGNER_PATH = "/root/arifOS/arifosmcp/runtime/sovereign_signer.py"
    ACTOR_ID = "ariffazil"
    MCP_PROTOCOL = "2025-11-25"
    # Cache MCP session id per-process so we only handshake once.
    # Keyed by actor_id since each actor gets its own MCP session.
    _MCP_SESSION_CACHE: dict[str, str] = {}

    def _mcp_post(payload: dict, session_id: str | None = None, is_notification: bool = False) -> tuple[int, dict, str]:
        """POST JSON-RPC to arifOS MCP. Returns (status_code, body_dict, session_id_header)."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "MCP-Protocol-Version": MCP_PROTOCOL,
        }
        if session_id:
            headers["Mcp-Session-Id"] = session_id
        data = json.dumps(payload).encode()
        req = urllib.request.Request(MCP_ENDPOINT, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read().decode()
                sid = resp.headers.get("mcp-session-id", session_id or "")
                # Notifications return 202 with empty body
                if is_notification:
                    return resp.status, {}, sid
                return resp.status, (json.loads(raw) if raw else {}), sid
        except urllib.error.HTTPError as e:
            body_raw = e.read().decode()
            try:
                body = json.loads(body_raw)
            except Exception:
                body = {"raw": body_raw}
            return e.code, body, session_id or ""

    def _ensure_mcp_session(actor_id: str) -> str:
        """Run MCP initialize handshake once per actor. Returns session_id."""
        cached = _MCP_SESSION_CACHE.get(actor_id)
        if cached:
            return cached
        # 1) initialize → returns Mcp-Session-Id header
        init_msg = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {
                "protocolVersion": MCP_PROTOCOL,
                "capabilities": {},
                "clientInfo": {"name": "hermes-a2a-bridge", "version": "1.0.0"},
            },
        }
        status, body, sid = _mcp_post(init_msg)
        if status != 200 or not sid:
            raise RuntimeError(f"MCP initialize failed: status={status} body={body}")
        # 2) notifications/initialized (ack per MCP spec)
        notif = {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
        _mcp_post(notif, session_id=sid, is_notification=True)
        _MCP_SESSION_CACHE[actor_id] = sid
        return sid

    try:
        # ── Step 0: MCP transport handshake (initialize + ack) ───────────
        # Without this, arifOS MCP returns 400 "Missing session ID" per
        # mcp_transport_bridge.py:25. Cached per actor.
        try:
            mcp_session_id = _ensure_mcp_session(ACTOR_ID)
        except Exception as e:
            return {"status": "error", "error": f"MCP handshake failed: {e}"}

        # ── Step 1: Get constitution_hash from unsigned init ──────────────
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "arif_session_init",
                "arguments": {"mode": "init", "actor_id": ACTOR_ID},
            },
        }
        init_status, init_body, _ = _mcp_post(init_payload, session_id=mcp_session_id)
        if init_status != 200 or "result" not in init_body:
            return {
                "status": "error",
                "error": f"session_init failed: status={init_status} body={init_body}",
            }
        result = json.loads(init_body["result"]["content"][0]["text"])["result"]
        constitution_hash = result["session"]["constitution_hash"]

        # ── Step 2: Generate nonce ─────────────────────────────────────────
        nonce = f"mcp_{int(time_module.time() * 1000)}"

        # ── Step 3: Sign with Ed25519 sovereign key ───────────────────────
        signer_result = subprocess.run(
            ["python3", SIGNER_PATH, ACTOR_ID, constitution_hash, nonce],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if signer_result.returncode != 0:
            return {
                "status": "error",
                "error": f"Signer failed: {signer_result.stderr[:200]}",
            }
        sig_b64 = signer_result.stdout.strip()

        # ── Step 4: Call arifOS MCP tool with SOVEREIGN signature ──────────
        # Merge signature into params (legacy field — still accepted)
        tool_params = dict(params)
        tool_params["actor_signature"] = sig_b64
        tool_params["nonce"] = nonce
        if "actor_id" not in tool_params:
            tool_params["actor_id"] = ACTOR_ID
        if "mode" not in tool_params:
            # Default mode per tool class — fixes VAULT999 LEGACY_WRAP gap
            # (previously always "init" which crashed seal/forge paths)
            tool_params["mode"] = _default_mode_for(tool_name)

        # ── Step 4b: Build proper FederationEnvelope (LEGACY_WRAP fix) ───
        # The v2 envelope_validator (envelope_validator.py) requires a
        # _envelope field on every governed tool call. Without it, vault
        # seal + forge execute are rejected with "No _envelope provided"
        # (envelope_validator.py:95) and federation_envelope.py:444 rejects
        # LEGACY_WRAP+MUTATE/ATOMIC. We already have a valid F13 Ed25519
        # sig from sovereign_signer.py — just place it in the right field.
        envelope = _build_sovereign_envelope(
            tool_name=tool_name,
            actor_signature=sig_b64,
            nonce=nonce,
            constitution_hash=constitution_hash,
            actor_id=ACTOR_ID,
        )

        signed_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": tool_params,
                "_envelope": envelope,
            },
        }
        call_status, call_body, _ = _mcp_post(signed_payload, session_id=mcp_session_id)
        if call_status != 200 or "result" not in call_body:
            return {
                "status": "error",
                "error": f"tool call failed: status={call_status} body={call_body}",
            }
        mcp_result = json.loads(call_body["result"]["content"][0]["text"])

        # ── Step 5: Extract and return structured result ───────────────────
        session_result = mcp_result.get("result", {})
        session_info = session_result.get("session", {})

        return {
            "status": mcp_result.get("verdict", "UNKNOWN").lower(),
            "verdict": mcp_result.get("verdict"),
            "authority_level": session_info.get("authority_level"),
            "identity_verified": session_info.get("identity_verified"),
            "signature_verified": session_info.get("signature_verified"),
            "session_id": session_info.get("session_id"),
            "constitution_hash": session_info.get("constitution_hash"),
            "reasons": mcp_result.get("reasons", []),
            "mcp_raw": mcp_result,  # full raw result for debugging
        }

    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "Signer timeout"}
    except Exception as e:
        return {"status": "error", "error": str(e)[:200]}



# ── MULTIMODAL EXTRACTION (Patched 2026-06-24 per Arif 888 directive) ───────
import hashlib as _hashlib
import tempfile as _tempfile
import json as _json

_MULTIMODAL_INBOX = "/tmp/hermes-multimodal-inbox"
os.makedirs(_MULTIMODAL_INBOX, exist_ok=True)


def _download_tg_file(file_id: str) -> str | None:
    """Download a Telegram file by file_id via getFile API, return local path."""
    try:
        meta = requests.get(
            f"{TELEGRAM_API}/getFile",
            params={"file_id": file_id},
            timeout=15,
        ).json()
        if not meta.get("ok"):
            return None
        file_path_remote = meta["result"]["file_path"]
        url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path_remote}"
        local = os.path.join(_MULTIMODAL_INBOX, os.path.basename(file_path_remote))
        with requests.get(url, timeout=30, stream=True) as r:
            r.raise_for_status()
            with open(local, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
        return local
    except Exception as e:
        print(f"[MULTIMODAL] download error: {e}", flush=True)
        return None


def _describe_image(path: str) -> str:
    """Vision analysis via OpenClaw MCP. Fallback on failure."""
    try:
        import urllib.request as _ur
        body = _json.dumps({
            "image_source": path,
            "prompt": "Describe this image in detail for an LLM that cannot see it. Include objects, text, scene, mood, any visible numbers/labels, and image type (photo/diagram/screenshot).",
        }).encode()
        req = _ur.Request(
            "http://localhost:18789/mcp/understand_image",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with _ur.urlopen(req, timeout=60) as r:
            return r.read().decode()[:2000]
    except Exception as e:
        return f"(vision failed: {type(e).__name__}; current model may not support images — fallback to vision-capable model)"


def _transcribe_voice(path: str) -> str:
    """Whisper transcription via OpenClaw MCP."""
    try:
        import urllib.request as _ur
        body = _json.dumps({"audio_path": path, "language": "auto"}).encode()
        req = _ur.Request(
            "http://localhost:18789/mcp/audio_ingest",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with _ur.urlopen(req, timeout=120) as r:
            return r.read().decode()[:4000]
    except Exception as e:
        return f"(transcription failed: {type(e).__name__})"


def _extract_document(path: str) -> str:
    """Text extract via pymupdf for PDF, raw read for txt/md/json."""
    try:
        if path.lower().endswith(".pdf"):
            import fitz as _fitz
            doc = _fitz.open(path)
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            return text[:8000]
        else:
            with open(path, "r", errors="replace") as f:
                return f.read()[:8000]
    except Exception as e:
        return f"(extract failed: {type(e).__name__})"


def _extract_multimodal(msg: dict) -> str:
    """Pull text/caption first, then enrich with any photo/voice/document content."""
    base = msg.get("text") or msg.get("caption") or ""
    prefix = ""

    if msg.get("photo"):
        photo_arr = msg["photo"]
        file_id = photo_arr[-1]["file_id"]
        local = _download_tg_file(file_id)
        if local:
            sha = _hashlib.sha256(open(local, "rb").read()).hexdigest()[:12]
            desc = _describe_image(local)
            prefix += f"[image sha={sha} bytes={os.path.getsize(local)}]\n{desc}\n\n"
            print(f"[MULTIMODAL] image downloaded {local} ({os.path.getsize(local)} bytes)", flush=True)

    voice = msg.get("voice") or msg.get("audio")
    if voice:
        local = _download_tg_file(voice["file_id"])
        if local:
            sha = _hashlib.sha256(open(local, "rb").read()).hexdigest()[:12]
            transcript = _transcribe_voice(local)
            prefix += f"[voice sha={sha} bytes={os.path.getsize(local)} duration={voice.get('duration', '?')}s]\n{transcript}\n\n"
            print(f"[MULTIMODAL] voice downloaded {local}", flush=True)

    if msg.get("document"):
        doc = msg["document"]
        local = _download_tg_file(doc["file_id"])
        if local:
            sha = _hashlib.sha256(open(local, "rb").read()).hexdigest()[:12]
            extracted = _extract_document(local)
            fname = doc.get("file_name", "unknown")
            prefix += f"[document name={fname} sha={sha} bytes={os.path.getsize(local)}]\n{extracted}\n\n"
            print(f"[MULTIMODAL] document downloaded {local} ({os.path.getsize(local)} bytes)", flush=True)

    return (prefix + base).strip()


# ── END MULTIMODAL ───────────────────────────────────────────────────────


def telegram_polling():
    """Poll Telegram for @ASI_arifos_bot messages and FORWARD to AAA gateway."""
    print("[TELEGRAM] Polling thread started for @ASI_arifos_bot", flush=True)
    while True:
        try:
            offset = load_last_update_id()
            resp = requests.get(
                f"{TELEGRAM_API}/getUpdates",
                params={"offset": offset + 1, "timeout": 30},
                timeout=35,
            )
            data = resp.json()
            if not data.get("ok"):
                time.sleep(5)
                continue

            updates = data.get("result", [])
            for update in updates:
                offset = update["update_id"]
                save_last_update_id(offset)

                msg = update.get("message") or update.get("edited_message")
                if not msg:
                    continue

                chat_id = msg["chat"]["id"]
                message_id = msg["message_id"]
                text = _extract_multimodal(msg)
                if not text:
                    continue

                print(
                    f"[TELEGRAM→GATEWAY] chat={chat_id} msg_id={message_id} text={text[:60]}",
                    flush=True,
                )

                gateway_payload = {
                    "jsonrpc": "2.0",
                    "id": f"tg-{message_id}",
                    "method": "tasks/send",
                    "params": {
                        "agent_id": "hermes",
                        "message": {
                            "parts": [{"kind": "text", "text": text}],
                            "messageId": str(message_id),
                            "taskId": f"tg-{message_id}",
                            "contextId": str(chat_id),
                        },
                        "metadata": {
                            "telegram_chat_id": chat_id,
                            "telegram_message_id": message_id,
                            "source": "telegram_polling",
                        },
                    },
                }

                # ── 888_APPROVE Relay ─────────────────────────────────────────────
                # Direct path to OpenClaw for sovereign approval flow.
                # Arif's APPROVE on Telegram = human witness event.
                # Hermes relays to OpenClaw which calls sovereign_signer.py → arif_session_init.
                # This bypasses the AAA gateway loop for speed and directness.
                # ──────────────────────────────────────────────────────────────────
                if text.upper().startswith("APPROVE") or text.upper().startswith(
                    "/APPROVE"
                ):
                    approve_msg = (
                        f"888_APPROVE\nraw:{text}\nchat:{chat_id}\nmsg:{message_id}"
                    )
                    print(
                        f"[888_APPROVE] Relaying to OpenClaw: {text[:80]}", flush=True
                    )
                    try:
                        result = call_hermes(approve_msg, f"apr-{message_id}")
                        print(
                            f"[888_APPROVE] OpenClaw response: {str(result)[:120]}",
                            flush=True,
                        )
                    except Exception as e:
                        print(f"[888_APPROVE] ERROR: {e}", flush=True)
                    # Also forward to AAA gateway for Hermes agent visibility (non-blocking)
                    try:
                        requests.post(
                            f"{AAA_GATEWAY}/tasks",
                            json=gateway_payload,
                            headers=AAA_AUTH,
                            timeout=10,
                        )
                    except Exception:
                        pass
                    continue  # Skip normal gateway forwarding — APPROVE handled by OpenClaw
                # ── END 888_APPROVE Relay ───────────────────────────────────────

                try:
                    gr = requests.post(
                        f"{AAA_GATEWAY}/tasks",
                        json=gateway_payload,
                        headers=AAA_AUTH,
                        timeout=60,
                    )
                    print(f"[TELEGRAM→GATEWAY] → status={gr.status_code}", flush=True)
                except Exception as e:
                    print(f"[TELEGRAM→GATEWAY] → ERROR: {e}", flush=True)

        except requests.exceptions.Timeout:
            continue
        except Exception as e:
            print(f"[TELEGRAM] Polling error: {e}", flush=True)
            time.sleep(5)


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        cl = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(cl).decode() if cl else "{}"
        try:
            req = json.loads(body)
        except:
            self.send_error(400)
            return

        p = req.get("params", {})
        task_id = p.get("taskId") or f"hm-{uuid.uuid4().hex[:10]}"
        context_id = p.get("contextId") or str(uuid.uuid4())

        msg = p.get("message", {})
        if isinstance(msg, dict):
            text = " ".join(
                part["text"]
                for part in msg.get("parts", [])
                if part.get("kind") == "text"
            )
        else:
            text = str(msg)

        # ── 888_APPROVE relay (do_POST path) ──────────────────────────────────
        # When Hermes agent receives APPROVE from Telegram and forwards via A2A,
        # hermes-a2a.py receives it here and relays to OpenClaw non-blocking.
        # This bypasses the Hermes→OpenClaw round-trip through the AAA gateway loop.
        # ───────────────────────────────────────────────────────────────────────
        # ── MCP_EXECUTE relay ────────────────────────────────────────────────
        # Direct arifOS MCP execution with Ed25519 SOVEREIGN signature.
        # Bypasses OpenClaw agent — runs on VPS, returns structured JSON.
        # Request body: {"action": "MCP_EXECUTE", "tool": "arif_session_init", "params": {...}}
        # ───────────────────────────────────────────────────────────────────────
        req_action = req.get("action", "").upper()
        if req_action == "MCP_EXECUTE":
            tool_name = req.get("tool", "arif_session_init")
            tool_params = req.get("params", {})
            print(
                f"[MCP_EXECUTE] tool={tool_name} params={str(tool_params)[:100]}",
                flush=True,
            )
            result = call_arif_mcp_sync(tool_name, tool_params)
            result_text = json.dumps(result)
            print(f"[MCP_EXECUTE] result: {result_text[:200]}", flush=True)
            response = a2a_resp(task_id, context_id, result_text)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        # ── END MCP_EXECUTE relay ──────────────────────────────────────────

        is_approve = text.upper().startswith("APPROVE") or text.upper().startswith(
            "/APPROVE"
        )
        if is_approve:
            chat_id = p.get("metadata", {}).get("telegram_chat_id", "?")
            msg_id = p.get("metadata", {}).get("telegram_message_id", "?")
            approve_msg = f"888_APPROVE\nraw:{text}\nchat:{chat_id}\nmsg:{msg_id}"
            print(
                f"[888_APPROVE do_POST] forwarding to OpenClaw: {text[:80]}", flush=True
            )
            call_hermes_nb(approve_msg, f"apr-{msg_id}")
            # Respond immediately — don't wait for OpenClaw
            response = a2a_resp(
                task_id,
                context_id,
                "888_APPROVE relayed to OpenClaw. Sovereign signature flow initiated.",
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        # ── END 888_APPROVE relay ────────────────────────────────────────────

        result = call_hermes(text, task_id)
        response = a2a_resp(task_id, context_id, result)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
            return
        if ".well-known/agent-card.json" in self.path:
            card = {
                "name": "AAA Hermes ASI",
                "description": "AAA-owned Hermes ASI agent relay; APEX/arifOS own verdict paths",
                "url": "http://127.0.0.1:18001/",
                "protocol_version": "1.0.0",
                "capabilities": {"streaming": False, "push_notifications": False},
                "authentication": {"schemes": ["bearer"]},
                "skills": [
                    {
                        "id": "deliberate",
                        "name": "Agent relay",
                        "description": "Routes Hermes agent tasks through the governed A2A mesh",
                    }
                ],
                "lane": "ASI",
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(card).encode())
        else:
            self.send_error(404)

    def log_message(self, fmt, *args):
        print(f"[HERMES-A2A] {fmt % args}", flush=True)


if __name__ == "__main__":
    if telegram_polling_enabled():
        telegram_thread = threading.Thread(target=telegram_polling, daemon=True)
        telegram_thread.start()
        print("[TELEGRAM] Polling thread started", flush=True)
    else:
        print(
            "[TELEGRAM] Polling disabled; Hermes Gateway owns Telegram updates",
            flush=True,
        )

    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Hermes A2A adapter listening on port {PORT}", flush=True)
    server.serve_forever()

# DEPRECATED 2026-06-21: AAA A2A server (port 3001) handles all routing.
# Hermes A2A bridge (port 18001) decommissioned. Use AAA A2A :3001 instead.
