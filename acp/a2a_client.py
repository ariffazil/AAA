"""
AAA A2A Client — talks to the AAA A2A Gateway at localhost:3001.

The gateway implements the real A2A protocol (agentcommunicationprotocol.dev).
Auth: Bearer token + x-a2a-key header (dev fallback: aaa-a2a-token-dev / aaa-a2a-apikey-dev)

API base: http://localhost:3001/a2a/
Endpoints:
    POST /a2a/message/send  → send a task, await result
    GET  /a2a/tasks/{id}    → get task status
    GET  /a2a/tasks/{id}/subscribe → SSE stream
"""

from __future__ import annotations
import httpx
import asyncio
import json
from typing import AsyncIterator, Optional
from pydantic import BaseModel


A2A_BASE_URL = "http://localhost:3001"
A2A_TOKEN = "aaa-a2a-token-dev"
A2A_API_KEY = "aaa-a2a-apikey-dev"


class A2AMessage(BaseModel):
    role: str = "user"
    parts: list[dict]  # [{"kind": "text", "text": "..."}]


class A2ATaskResponse(BaseModel):
    id: str
    contextId: str
    status: dict
    artifacts: list = []
    history: list = []
    kind: str = "task"
    metadata: dict = {}


class A2AClient:
    """
    A2A client that talks JSON-RPC 2.0 to the AAA A2A Gateway.

    Usage:
        client = A2AClient()
        result = await client.send(
            content="Search memory for recent arifOS decisions",
            agent_id="hermes",
            skill_id="memory-recall",
        )
    """

    def __init__(
        self,
        base_url: str = A2A_BASE_URL,
        token: str = A2A_TOKEN,
        api_key: str = A2A_API_KEY,
        timeout: float = 60.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.api_key = api_key
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(self.timeout),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
                "x-a2a-key": self.api_key,
            }
        )
        return self

    async def __aexit__(self, *args):
        if self._client:
            await self._client.aclose()

    def _rpc(self, method: str, params: dict) -> dict:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }

    async def send(
        self,
        content: str,
        agent_id: str = "hermes",
        skill_id: Optional[str] = None,
    ) -> A2ATaskResponse:
        """
        POST /a2a/message/send — send a task and await completion.
        """
        if not self._client:
            raise RuntimeError("Use `async with A2AClient() as client:`")

        payload = self._rpc("message/send", {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": content}],
            },
            "agent_id": agent_id,
            **({"skill_id": skill_id} if skill_id else {}),
        })

        resp = await self._client.post("/a2a/message/send", json=payload)
        resp.raise_for_status()
        data = resp.json()

        if "error" in data:
            raise RuntimeError(f"A2A error: {data['error']}")

        return A2ATaskResponse(**data["result"])

    async def send_stream(
        self,
        content: str,
        agent_id: str = "hermes",
    ) -> AsyncIterator[dict]:
        """
        GET /a2a/tasks/{id}/subscribe — SSE stream of task events.
        """
        if not self._client:
            raise RuntimeError("Use `async with A2AClient() as client:`")

        # Send first
        task = await self.send(content, agent_id)

        # Subscribe to SSE stream
        async with self._client.stream(
            "GET",
            f"/a2a/tasks/{task.id}/subscribe",
        ) as stream:
            async for line in stream.aiter_lines():
                if line.startswith("data:"):
                    yield json.loads(line[5:].strip())

    async def get_task(self, task_id: str) -> A2ATaskResponse:
        """GET /a2a/tasks/{id} — get task status."""
        if not self._client:
            raise RuntimeError("Use async context manager")

        payload = self._rpc("tasks/get", {"taskId": task_id})
        resp = await self._client.post("/a2a/tasks/" + task_id, json=payload)
        resp.raise_for_status()
        data = resp.json()

        if "error" in data:
            raise RuntimeError(f"A2A error: {data['error']}")

        return A2ATaskResponse(**data["result"])


# ─── Synchronous helper ─────────────────────────────────────────────────────────

def send_sync(content: str, agent_id: str = "hermes", skill_id: Optional[str] = None) -> A2ATaskResponse:
    """Blocking send from non-async context."""
    return asyncio.run(
        A2AClient().__aenter__().send(content, agent_id, skill_id)
    )
