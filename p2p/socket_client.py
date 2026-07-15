"""Asyncio Unix-domain-socket client for P2P messages.

Stdlib only. One connection per message — keeps back-pressure and ack
semantics trivial, and matches the ≤10ms target on loopback.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any


SOCKET_CONNECT_TIMEOUT_S = 2.0
SOCKET_READ_TIMEOUT_S = 5.0


class P2PClient:
    """Outbound client. Connect, write one JSON line, read one ack line."""

    def __init__(self, socket_dir: str | Path = "/tmp/aaa-p2p") -> None:
        self.socket_dir = Path(socket_dir)

    def _path_for(self, recipient: str) -> Path:
        """Resolve recipient → socket file."""
        if recipient == "all":
            return self.socket_dir / "888-to-all.sock"
        return self.socket_dir / f"{_short(recipient)}-to-all.sock"

    async def send(
        self,
        recipient: str,
        message: dict[str, Any],
        *,
        timeout_s: float = SOCKET_READ_TIMEOUT_S,
    ) -> dict[str, Any]:
        """Send one message, return parsed ack (or raise on protocol error)."""
        path = self._path_for(recipient)
        if not path.exists():
            raise FileNotFoundError(f"recipient_socket_missing:{path}")

        body = (json.dumps(message, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")

        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_unix_connection(str(path)),
                timeout=SOCKET_CONNECT_TIMEOUT_S,
            )
        except (FileNotFoundError, ConnectionRefusedError) as exc:
            raise ConnectionError(f"connect_failed:{path}:{exc}") from exc
        except asyncio.TimeoutError as exc:
            raise TimeoutError(f"connect_timeout:{path}") from exc

        try:
            writer.write(body)
            await writer.drain()
            raw = await asyncio.wait_for(reader.readline(), timeout=timeout_s)
        except asyncio.TimeoutError as exc:
            raise TimeoutError(f"ack_timeout:{path}") from exc
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:  # noqa: BLE001 — best-effort cleanup
                pass

        if not raw:
            raise EOFError(f"empty_ack_from:{path}")
        try:
            ack = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"bad_ack_json:{exc.msg}") from exc
        return ack


def _short(agent: str) -> str:
    """333-AGI → 333 ; 555-ASI → 555 ; 888-APEX → 888."""
    return agent.split("-", 1)[0]