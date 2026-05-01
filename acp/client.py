"""
ACP Client — makes ACP calls from OpenClaw to Hermes (or any ACP agent).
Thread-safe, async via httpx.
"""

from __future__ import annotations
import asyncio
import httpx
import json
from typing import AsyncIterator, Optional
from AAA.acp.models import AgentCard, ACPTask, ACPMessage


class ACPClient:
    """
    ACP client for agent-to-agent communication.
    
    Usage:
        client = ACPClient(base_url="http://localhost:8082")
        result = await client.send_message(
            agent_id="hermes",
            content="Search memory for recent arifOS decisions",
            skill_id="memory-recall"
        )
    """

    def __init__(self, base_url: str, timeout: float = 60.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(self.timeout),
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        return self

    async def __aexit__(self, *args):
        if self._client:
            await self._client.aclose()

    # ─── Discovery ──────────────────────────────────────────────────────────

    async def get_agent_card(self, agent_id: str) -> AgentCard:
        """GET /agents/{agent_id} — fetch agent card for discovery."""
        if not self._client:
            raise RuntimeError("Use async context manager: `async with ACPClient(...)`")
        resp = await self._client.get(f"/agents/{agent_id}")
        resp.raise_for_status()
        return AgentCard(**resp.json())

    async def list_agents(self) -> list[AgentCard]:
        """GET /agents — list all registered agents."""
        if not self._client:
            raise RuntimeError("Use async context manager")
        resp = await self._client.get("/agents")
        resp.raise_for_status()
        return [AgentCard(**a) for a in resp.json().get("agents", [])]

    # ─── Messaging ───────────────────────────────────────────────────────────

    async def send_message(
        self,
        agent_id: str,
        content: str,
        skill_id: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> ACPTask:
        """
        POST /runs — create a new ACP run (task) with a message.
        Blocking call — waits for result.
        """
        if not self._client:
            raise RuntimeError("Use async context manager")

        payload = {
            "agent_id": agent_id,
            "message": {
                "content": content,
                "metadata": metadata or {},
            },
        }
        if skill_id:
            payload["skill_id"] = skill_id
        if session_id:
            payload["session_id"] = session_id

        resp = await self._client.post("/runs", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return ACPTask(**data)

    async def send_message_stream(
        self,
        agent_id: str,
        content: str,
        skill_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> AsyncIterator[str]:
        """
        POST /runs/{id}/events — SSE stream of run events.
        Yields text chunks as they arrive.
        """
        if not self._client:
            raise RuntimeError("Use async context manager")

        # Create run
        payload = {
            "agent_id": agent_id,
            "message": {"content": content},
        }
        if skill_id:
            payload["skill_id"] = skill_id
        if session_id:
            payload["session_id"] = session_id

        resp = await self._client.post("/runs", json=payload, timeout=None)
        resp.raise_for_status()
        run_id = resp.json()["id"]

        # Stream events
        async with self._client.stream("GET", f"/runs/{run_id}/events") as stream:
            async for line in stream.aiter_lines():
                if line.startswith("data:"):
                    yield line[5:].strip()

    async def get_run_status(self, run_id: str) -> ACPTask:
        """GET /runs/{id} — check status of a run."""
        if not self._client:
            raise RuntimeError("Use async context manager")
        resp = await self._client.get(f"/runs/{run_id}")
        resp.raise_for_status()
        return ACPTask(**resp.json())

    async def cancel_run(self, run_id: str) -> bool:
        """DELETE /runs/{id} — cancel a running task."""
        if not self._client:
            raise RuntimeError("Use async context manager")
        resp = await self._client.delete(f"/runs/{run_id}")
        return resp.status_code in (200, 204)


# ─── Sync wrapper for non-async contexts ──────────────────────────────────────

def run_async(coro):
    """Run an async ACP call from sync context."""
    import asyncio
    try:
        loop = asyncio.get_running_loop()
        # Already in async context — schedule task
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result(timeout=120)
    except RuntimeError:
        # No running loop
        return asyncio.run(coro)
