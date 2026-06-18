"""
mcp_client.py — Async MCP client for the federation 4-organ surface.
Owner: arif
Scope: opencode-bot (000♎️)

Provides direct, persistent streamable-http MCP sessions to:
  arifOS (:8088), WEALTH (:18082), WELL (:18083), A-FORGE (:7071), GEOX (:8081)
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Optional

import aiohttp

log = logging.getLogger("opencode-bot.mcp")

DEFAULT_ORGANS = {
    "arifos": "http://127.0.0.1:8088/mcp",
    "wealth": "http://127.0.0.1:18082/mcp",
    "well": "http://127.0.0.1:18083/mcp",
    "aforge": "http://127.0.0.1:7071/mcp",
    "geox": "http://127.0.0.1:8081/mcp",
}

MCP_SESSIONS_PATH = Path(__file__).resolve().parent / ".mcp_sessions.json"
MCP_TIMEOUT_S = float(os.environ.get("MCP_TIMEOUT_S", "15"))


class FederationMCPClient:
    """Persistent async MCP client for federation organs."""

    def __init__(
        self,
        organs: Optional[dict[str, str]] = None,
        sessions_path: Path = MCP_SESSIONS_PATH,
        timeout: float = MCP_TIMEOUT_S,
    ):
        self.organs = {**DEFAULT_ORGANS, **(organs or {})}
        self._sessions: dict[str, Optional[str]] = {}
        self._sessions_path = sessions_path
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None
        self._load_sessions()

    async def _session_obj(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self._session

    def _load_sessions(self) -> None:
        try:
            if self._sessions_path.exists():
                data = json.loads(self._sessions_path.read_text())
                self._sessions = {k: v for k, v in data.items() if isinstance(v, str)}
        except Exception as exc:
            log.warning(f"MCP session load failed: {exc}")
            self._sessions = {}

    def _save_sessions(self) -> None:
        try:
            self._sessions_path.write_text(json.dumps(self._sessions, indent=2))
            self._sessions_path.chmod(0o600)
        except Exception as exc:
            log.warning(f"MCP session save failed: {exc}")

    async def initialize(self, organ: str) -> Optional[str]:
        """Initialize an MCP session for an organ. Returns mcp-session-id."""
        url = self.organs.get(organ)
        if not url:
            log.warning(f"MCP: unknown organ '{organ}'")
            return None
        body = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "opencode-bot", "version": "1.17.8"},
            },
        }
        session = await self._session_obj()
        try:
            async with session.post(
                url,
                json=body,
                headers={"Accept": "application/json"},
            ) as resp:
                sid = resp.headers.get("mcp-session-id")
                await resp.read()
                if sid:
                    self._sessions[organ] = sid
                    self._save_sessions()
                    log.info(f"MCP initialized {organ}: session_id={sid[:16]}...")
                else:
                    log.warning(f"MCP initialize {organ} returned no session id")
                return sid
        except Exception as exc:
            log.warning(f"MCP initialize {organ} failed: {type(exc).__name__}: {exc}")
            return None

    async def call_tool(
        self,
        organ: str,
        tool_name: str,
        arguments: dict[str, Any],
        session_id: Optional[str] = None,
        auto_init: bool = True,
    ) -> Optional[dict[str, Any]]:
        """Call a tool on a federation organ."""
        url = self.organs.get(organ)
        if not url:
            log.warning(f"MCP: unknown organ '{organ}'")
            return None

        sid = session_id or self._sessions.get(organ)
        if not sid and auto_init:
            sid = await self.initialize(organ)
        if not sid:
            log.warning(f"MCP: no session for {organ}; cannot call {tool_name}")
            return None

        body = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        }
        session = await self._session_obj()
        try:
            async with session.post(
                url,
                json=body,
                headers={"Accept": "application/json", "mcp-session-id": sid},
            ) as resp:
                data = await resp.json()
                return data
        except aiohttp.ClientResponseError as exc:
            if exc.status == 401 and auto_init:
                # Session expired; re-init once.
                new_sid = await self.initialize(organ)
                if new_sid and new_sid != sid:
                    return await self.call_tool(
                        organ, tool_name, arguments, session_id=new_sid, auto_init=False
                    )
            log.warning(f"MCP {organ}/{tool_name} HTTP {exc.status}: {exc.message}")
            return None
        except Exception as exc:
            log.warning(f"MCP {organ}/{tool_name} failed: {type(exc).__name__}: {exc}")
            return None

    async def health(self, organ: str) -> Optional[dict[str, Any]]:
        """GET /health on an organ (not all organs expose this)."""
        url = self.organs.get(organ)
        if not url:
            return None
        health_url = url.replace("/mcp", "/health")
        session = await self._session_obj()
        try:
            async with session.get(health_url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                return await resp.json()
        except Exception as exc:
            log.debug(f"MCP health {organ} failed: {type(exc).__name__}: {exc}")
            return None

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    def session_id(self, organ: str) -> Optional[str]:
        return self._sessions.get(organ)
