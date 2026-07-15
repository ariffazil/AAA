"""Asyncio Unix-domain-socket server for the P2P inner loop.

Each agent runs one server bound to `/tmp/aaa-p2p/<short>-to-all.sock`.
Inbound messages are validated (F12 INJECTION), appended to the audit log
(F11 AUDIT), and either:
  - forwarded to the recipient's socket, or
  - broadcast to every other agent when `to == "all"`.

The server then writes a JSON-line ack back to the sender.
Stdlib only.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any, Awaitable, Callable

from .audit import AuditLog
from .protocol import (
    ALLOWED_AGENTS,
    SchemaError,
    canonical_json,
    new_message,
    validate_message,
)
from .socket_client import P2PClient


log = logging.getLogger("aaa.p2p.server")


# Callback signature: (message_dict) -> None. Called after audit + forward.
OnMessageHandler = Callable[[dict[str, Any]], Awaitable[None]]


class P2PServer:
    """Bind to one Unix socket, route inbound messages, audit everything."""

    def __init__(
        self,
        agent: str,
        socket_dir: str | Path = "/tmp/aaa-p2p",
        audit_path: str | Path = "/root/AAA/p2p/audit.jsonl",
        on_message: OnMessageHandler | None = None,
    ) -> None:
        if agent not in ALLOWED_AGENTS:
            raise ValueError(f"unknown_agent:{agent}")
        self.agent = agent
        self.short = agent.split("-", 1)[0]  # 333-AGI → 333
        self.socket_dir = Path(socket_dir)
        self.socket_dir.mkdir(parents=True, exist_ok=True)
        self.socket_path = self.socket_dir / f"{self.short}-to-all.sock"
        self.audit = AuditLog(audit_path)
        self.client = P2PClient(socket_dir=self.socket_dir)
        self._on_message = on_message
        self._server: asyncio.base_events.Server | None = None
        self._stop = asyncio.Event()

    # ── Lifecycle ─────────────────────────────────────────────────────────

    async def start(self) -> None:
        # Stale socket? Remove it. We are the only owner on this VPS.
        if self.socket_path.exists():
            try:
                self.socket_path.unlink()
            except FileNotFoundError:
                pass
        # Bind with restrictive perms (0o660) — owner+group only.
        self._server = await asyncio.start_unix_server(
            self._handle_connection,
            path=str(self.socket_path),
        )
        try:
            os.chmod(self.socket_path, 0o660)
        except OSError:  # some FS don't support chmod
            pass
        log.info(
            "p2p_server_up agent=%s socket=%s audit_seq=%d",
            self.agent,
            self.socket_path,
            self.audit.seq,
        )
        await self._stop.wait()
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
        if self.socket_path.exists():
            try:
                self.socket_path.unlink()
            except FileNotFoundError:
                pass
        log.info("p2p_server_down agent=%s", self.agent)

    def stop(self) -> None:
        self._stop.set()

    # ── Connection handling ──────────────────────────────────────────────

    async def _handle_connection(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        try:
            raw = await asyncio.wait_for(reader.readline(), timeout=10.0)
        except asyncio.TimeoutError:
            writer.close()
            await _safe_wait_closed(writer)
            return

        if not raw:
            writer.close()
            await _safe_wait_closed(writer)
            return

        ack: dict[str, Any]
        try:
            msg = json.loads(raw.decode("utf-8"))
            validate_message(msg)  # F12 INJECTION
        except (json.JSONDecodeError, SchemaError, UnicodeDecodeError) as exc:
            log.warning("reject schema agent=%s err=%s", self.agent, exc)
            ack = _reject_ack(reason=str(exc), code=_classify_code(exc))
            await _write_ack(writer, ack)
            return

        # Audit BEFORE delivery — F11 AMANAH.
        try:
            self.audit.append(
                sender=msg["from"],
                recipient=msg["to"],
                verb=msg["verb"],
                blast_radius=msg["blast_radius"],
                message=msg,
                session_id=msg.get("session_id"),
                outcome="received",
            )
        except OSError as exc:
            log.error("audit_blocked agent=%s err=%s", self.agent, exc)
            ack = _reject_ack(reason=f"F11_AUDIT_BLOCKED:{exc}", code="F11_AUDIT_BLOCKED")
            await _write_ack(writer, ack)
            return

        # Route to recipient.
        if msg["to"] == "all":
            recipients = [a for a in ALLOWED_AGENTS if a != msg["from"]]
            ok_all = True
            for r in recipients:
                try:
                    # Per-recipient copy with `to` rewritten so the receiver
                    # handles it as a direct message, NOT another broadcast
                    # (otherwise we get infinite fan-out loops).
                    fanout = dict(msg)
                    fanout["to"] = r
                    await self.client.send(r, fanout)
                except (FileNotFoundError, ConnectionError, TimeoutError) as exc:
                    log.warning("broadcast_drop agent=%s to=%s err=%s", self.agent, r, exc)
                    ok_all = False
            ack = _ack_ok(msg) if ok_all else _reject_ack(
                msg, "partial_broadcast", "PARTIAL_DELIVERY"
            )
        elif msg["to"] == self.agent:
            # Local — invoke handler if any, then ack.
            if self._on_message is not None:
                try:
                    await self._on_message(msg)
                except Exception as exc:  # noqa: BLE001
                    log.exception("handler_error agent=%s err=%s", self.agent, exc)
                    ack = _reject_ack(msg, f"handler_error:{exc}", "HANDLER_ERROR")
                    await _write_ack(writer, ack)
                    return
            ack = _ack_ok(msg)
        else:
            # Forward to another agent's socket.
            try:
                await self.client.send(msg["to"], msg)
                ack = _ack_ok(msg)
            except (FileNotFoundError, ConnectionError, TimeoutError) as exc:
                log.warning("forward_failed from=%s to=%s err=%s", msg["from"], msg["to"], exc)
                ack = _reject_ack(msg, f"forward_failed:{exc}", "FORWARD_FAILED")

        await _write_ack(writer, ack)


# ── Helpers ─────────────────────────────────────────────────────────────────


async def _safe_wait_closed(writer: asyncio.StreamWriter) -> None:
    try:
        await writer.wait_closed()
    except Exception:  # noqa: BLE001
        pass


async def _write_ack(writer: asyncio.StreamWriter, ack: dict[str, Any]) -> None:
    body = (json.dumps(ack, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    writer.write(body)
    try:
        await writer.drain()
    except ConnectionResetError:
        pass
    writer.close()
    await _safe_wait_closed(writer)


def _ack_ok(msg: dict[str, Any]) -> dict[str, Any]:
    return new_message(
        sender=msg["to"],
        recipient=msg["from"],
        verb="ack",
        payload={"ref_timestamp": msg.get("timestamp"), "received": True},
        blast_radius="LOW",
        requires_judgment=False,
        session_id=msg.get("session_id"),
    )


def _reject_ack(
    msg_or_reason: dict[str, Any] | str,
    reason: str | None = None,
    code: str = "REJECT",
) -> dict[str, Any]:
    if isinstance(msg_or_reason, dict):
        ref = msg_or_reason.get("timestamp")
        sender = msg_or_reason.get("from", "unknown")
        actual_reason = reason or "rejected"
    else:
        ref = None
        sender = "unknown"
        actual_reason = str(msg_or_reason)
    return new_message(
        sender="888-APEX",  # rejection authority — 888 arbitrates
        recipient=sender,
        verb="reject",
        payload={"ref_timestamp": ref, "reason": actual_reason, "code": code},
        blast_radius="LOW",
        requires_judgment=False,
    )


def _classify_code(exc: Exception) -> str:
    if isinstance(exc, SchemaError):
        return "F12_SCHEMA"
    if isinstance(exc, json.JSONDecodeError):
        return "F12_JSON"
    if isinstance(exc, UnicodeDecodeError):
        return "F12_ENCODING"
    return "REJECT"