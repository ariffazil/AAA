"""AAA Cockpit — Background Organ Probe.

Async background task that probes all federation organs via /health
at a fixed interval (default 15s). Updates the live registry with
probe results. Implements the TTL tombstoning logic: 3 missed probes
= DEAD.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any

import httpx

from aaa_a2a.cockpit.registry import (
    PROBE_INTERVAL_SECONDS,
    PROBED_ORGANS,
    PROBED_SERVICES,
    AgentRegistry,
    get_registry,
)

logger = logging.getLogger("aaa.cockpit.probe")


class OrganProbe:
    """Async background prober for federation organs."""

    def __init__(
        self, registry: AgentRegistry | None = None, interval: int = PROBE_INTERVAL_SECONDS
    ):
        self.registry = registry or get_registry()
        self.interval = interval
        self._task: asyncio.Task[None] | None = None
        self._running = False
        self._probe_count = 0
        self._client: httpx.AsyncClient | None = None

    async def start(self) -> None:
        """Start the background probe loop."""
        if self._running:
            return
        self._running = True
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(5.0))
        self._task = asyncio.create_task(self._probe_loop())
        logger.info(f"Organ probe started (interval={self.interval}s)")

    async def stop(self) -> None:
        """Stop the background probe loop."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self._client:
            await self._client.aclose()
        logger.info("Organ probe stopped")

    async def probe_once(self) -> dict[str, Any]:
        """Run a single probe cycle across all organs. Returns summary."""
        results: dict[str, Any] = {"timestamp": time.time(), "organs": {}, "services": {}}
        start = time.monotonic()

        for organ in PROBED_ORGANS:
            result = await self._probe_organ(organ)
            results["organs"][organ["id"]] = result

        for svc in PROBED_SERVICES:
            result = await self._probe_organ(svc)
            results["services"][svc["id"]] = result

        self._probe_count += 1
        self.registry._probe_count = self._probe_count
        self.registry._last_probe = time.time()

        # Write status.json after each probe cycle
        self.registry.write_status_json()

        elapsed = time.monotonic() - start
        alive = sum(1 for r in results["organs"].values() if r["healthy"])
        dead = len(results["organs"]) - alive
        logger.info(
            f"Probe #{self._probe_count}: {alive}/{len(PROBED_ORGANS)} organs alive "
            f"({dead} down) in {elapsed:.2f}s"
        )
        return results

    async def _probe_loop(self) -> None:
        """Main probe loop — runs until stopped."""
        # Initial probe immediately
        await self.probe_once()

        while self._running:
            await asyncio.sleep(self.interval)
            if not self._running:
                break
            try:
                await self.probe_once()
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Probe cycle failed")

    async def _probe_organ(self, organ: dict[str, Any]) -> dict[str, Any]:
        """Probe a single organ via GET /health."""
        agent_id = organ["id"]
        port = organ["port"]
        url = f"http://127.0.0.1:{port}/health"
        result: dict[str, Any] = {
            "agent_id": agent_id,
            "url": url,
            "healthy": False,
            "status_code": 0,
            "latency_ms": 0.0,
            "error": None,
            "apex_scalars": {},
            "tools_count": 0,
        }

        if self._client is None:
            result["error"] = "client not initialized"
            self.registry.mark_unreachable(agent_id, "probe client not ready")
            return result

        t0 = time.monotonic()
        try:
            resp = await self._client.get(url)
            result["status_code"] = resp.status_code
            result["latency_ms"] = round((time.monotonic() - t0) * 1000, 1)

            if resp.status_code == 200:
                result["healthy"] = True
                try:
                    body = resp.json()
                    # Extract apex scalars if present
                    apex = body.get("apex_scalars", {})
                    if apex:
                        result["apex_scalars"] = {
                            "G": apex.get("G", {}).get("value")
                            if isinstance(apex.get("G"), dict)
                            else apex.get("G"),
                            "C_dark": apex.get("C_dark", {}).get("value")
                            if isinstance(apex.get("C_dark"), dict)
                            else apex.get("C_dark"),
                            "W3": apex.get("W3", {}).get("value")
                            if isinstance(apex.get("W3"), dict)
                            else apex.get("W3"),
                        }
                    # Extract tools count
                    tc = body.get("tools_count") or body.get("tools_loaded") or body.get("tools")
                    if isinstance(tc, (int, float)):
                        result["tools_count"] = int(tc)
                    elif isinstance(tc, list):
                        result["tools_count"] = len(tc)
                except (json.JSONDecodeError, TypeError, AttributeError):
                    pass

                self.registry.update_from_probe(
                    agent_id,
                    healthy=True,
                    latency_ms=result["latency_ms"],
                    apex_scalars=result["apex_scalars"],
                    tools_count=result["tools_count"],
                )
            else:
                result["error"] = f"HTTP {resp.status_code}"
                self.registry.mark_unreachable(agent_id, f"HTTP {resp.status_code}")

        except httpx.TimeoutException:
            result["latency_ms"] = round((time.monotonic() - t0) * 1000, 1)
            result["error"] = "timeout"
            self.registry.mark_unreachable(agent_id, "timeout")
        except httpx.ConnectError:
            result["latency_ms"] = round((time.monotonic() - t0) * 1000, 1)
            result["error"] = "connection refused"
            self.registry.mark_unreachable(agent_id, "connection refused")
        except Exception as exc:
            result["latency_ms"] = round((time.monotonic() - t0) * 1000, 1)
            result["error"] = str(exc)[:200]
            self.registry.mark_unreachable(agent_id, str(exc)[:200])

        return result
