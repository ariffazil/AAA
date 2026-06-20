"""
client.py — arifOS MCP client.

Talks to the live arifOS MCP endpoint. Used by all 4 guards to issue
kernel calls. Implements the F2 epistemic auto-stamp (the F2 wire we
just shipped — see commit bd1b6b63c) so the kernel responses we receive
are properly F2-stamped.

The client is intentionally thin. The kernel is the source of truth;
this is just the transport.
"""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.parse import urljoin

import httpx


class ArifOSMCPClient:
    """
    Thin client for the arifOS MCP server.

    Default base URL points at the public production endpoint. Override
    for local development or testing.

    Uses streamable HTTP transport per MCP spec 2025-11-25.
    """

    def __init__(
        self,
        base_url: str = "https://arifos.arif-fazil.com",
        actor_id: str = "arif",
        session_id: str | None = None,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.mcp_url = f"{self.base_url}/mcp"
        self.actor_id = actor_id
        self.session_id = session_id or f"sess_{os.urandom(8).hex()}"
        self.timeout = timeout
        self._request_id = 0

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Call an arifOS MCP tool. Returns the result envelope.

        The envelope includes the F2 epistemic stamp (when applicable)
        and a seal_pointer for audit-trail completion.
        """
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {},
                "_meta": {
                    "actor_id": self.actor_id,
                    "session_id": self.session_id,
                },
            },
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.mcp_url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                },
            )
            response.raise_for_status()

            # MCP streamable HTTP returns either JSON or SSE.
            content_type = response.headers.get("content-type", "")
            if "text/event-stream" in content_type:
                # Parse SSE — last event is the result
                result = None
                for line in response.text.splitlines():
                    if line.startswith("data: "):
                        result = json.loads(line[6:])
                if result is None:
                    raise RuntimeError("Empty SSE response from arifOS MCP")
                return result
            else:
                return response.json()

    async def kernel_check_call(
        self,
        intent: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Issue a kernel.check_call against the arifOS kernel.

        This is the Band 1 cognition firewall endpoint. The kernel
        classifies the intent, applies F1-F13 floors, and returns a
        Decision envelope.
        """
        return await self.call_tool(
            "arif_kernel_route",
            {
                "mode": "check_call",
                "intent": intent,
                "actor_id": self.actor_id,
                "session_id": self.session_id,
            },
        )

    async def kernel_seal(
        self,
        decision: dict[str, Any],
        output: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Seal a decision + output to VAULT999.

        Returns the seal_pointer (VAULT999 entry id). The result is
        trusted only if the seal_pointer is present.
        """
        return await self.call_tool(
            "arif_vault_seal",
            {
                "decision": decision,
                "output": output,
                "actor_id": self.actor_id,
                "session_id": self.session_id,
            },
        )
