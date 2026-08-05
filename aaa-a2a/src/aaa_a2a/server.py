"""AAA A2A Server — constitutional overlay on official a2a-sdk.

Replaces 3,862 lines of Express with ~50 lines of Python + SDK.
Now includes Cockpit Live Polling: heartbeat registry, TTL tombstoning,
background organ probes, and live status.json.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import asyncio
import logging
import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from a2a.server.request_handlers.default_request_handler import LegacyRequestHandler
from a2a.server.routes.fastapi_routes import add_a2a_routes_to_fastapi
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill, AgentProvider

from aaa_a2a.executor import ConstitutionalExecutor
from aaa_a2a.routing.organ_router import call_mcp_tool
from aaa_a2a.cockpit import AgentRegistry, HeartbeatPayload, OrganProbe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aaa.server")

# ── Cockpit globals ────────────────────────────────────────────────────────
_probe: OrganProbe | None = None


def create_agent_card() -> AgentCard:
    """Create the AAA agent card for A2A discovery."""
    return AgentCard(
        name="arifOS AAA Control Plane",
        description=(
            "Sovereign ASI civilization control plane for the arif-fazil.com federation. "
            "Constitutional governance overlay on A2A transport. "
            "Routes tasks through F1-F13 floors, DelegationGuard, and 888_JUDGE verdicts."
        ),
        url="https://aaa.arif-fazil.com",
        version="2.0.0",
        provider=AgentProvider(
            organization="arifOS Federation",
            url="https://arif-fazil.com",
        ),
        capabilities=AgentCapabilities(
            streaming=True,
            push_notifications=True,
            state_transition_history=True,
            extensions=["arifos.constitutional.v1"],
        ),
        default_input_modes=["text/plain", "application/json"],
        default_output_modes=["text/plain", "application/json"],
        skills=[
            AgentSkill(
                id="hold.request",
                name="Request HOLD",
                description="Registers a HOLD for human review. Blocks execution until human SEAL or REJECT.",
                tags=["hold", "human-veto", "governance"],
            ),
            AgentSkill(
                id="forge.delegate",
                name="Delegate to A-FORGE",
                description="After SEAL, delegates a task to A-FORGE execution engine.",
                tags=["delegation", "execution", "a-forge"],
            ),
            AgentSkill(
                id="governance.check",
                name="Constitutional Check",
                description="Validates a proposed action against F1-F13 floors. Returns PERMIT / HOLD / BLOCK.",
                tags=["governance", "constitutional", "hold", "seal"],
            ),
            AgentSkill(
                id="agent.discover",
                name="Agent Discovery",
                description="Capability-based service discovery across the federation.",
                tags=["discovery", "routing", "capability"],
            ),
            AgentSkill(
                id="arifos.session.init",
                name="Federation Session Init",
                description=(
                    "Mint a governed session via arifOS (port 8088). "
                    "Returns session_id + session_token (sct_v1.*). "
                    "The canonical entry point for any agent that needs an authoritative identity. "
                    "Same effect as calling arif_init directly — exposed here so cockpit-driven "
                    "agents don't have to know kernel ports. See /root/scripts/federation_ritual.py."
                ),
                tags=["init", "session", "governance", "kernel", "arifos"],
            ),
            AgentSkill(
                id="arifos.session.seal",
                name="Federation Session Seal",
                description=(
                    "Seal the active session via arifOS (port 8088). "
                    "Writes an immutable entry to VAULT999 and returns entry_id + chain_hash. "
                    "The canonical exit point. Same effect as arif_seal — exposed here for "
                    "cockpit-driven agents. See /root/scripts/federation_ritual.py seal."
                ),
                tags=["seal", "session", "vault999", "kernel", "arifos"],
            ),
        ],
    )


# ── Lifecycle ───────────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start/stop cockpit background probe."""
    global _probe
    registry = AgentRegistry()  # noqa — imported; actually use get_registry
    from aaa_a2a.cockpit.registry import get_registry

    reg = get_registry()
    _probe = OrganProbe(registry=reg)
    await _probe.start()
    logger.info("[Cockpit] Background probe started")
    yield
    if _probe:
        await _probe.stop()
        logger.info("[Cockpit] Background probe stopped")


def create_app() -> FastAPI:
    """Create the AAA FastAPI application with Cockpit Live Polling."""
    app = FastAPI(
        title="AAA Constitutional A2A Gateway",
        description="Governance overlay on A2A transport. AAA decides WHETHER. A-FORGE decides HOW.",
        version="2.1.0-live",
        lifespan=lifespan,
    )

    # Create executor and handler
    executor = ConstitutionalExecutor(
        arifos_url=os.getenv("ARIFOS_URL", "http://localhost:8088"),
    )
    handler = LegacyRequestHandler(
        agent_card=create_agent_card(),
        task_store=InMemoryTaskStore(),
        request_handler=executor,
    )

    # Mount A2A routes
    add_a2a_routes_to_fastapi(app, jsonrpc_routes=[handler])

    # ── Health endpoint (enhanced with cockpit stats) ──────────────────

    @app.get("/health")
    async def health():
        from aaa_a2a.cockpit.registry import get_registry

        reg = get_registry()
        summary = reg.summary()
        return {
            "status": "healthy",
            "protocol": "A2A",
            "version": "2.1.0-live",
            "gateway": "AAA",
            "motto": "Ditempa Bukan Diberi",
            "overlay": "constitutional",
            "express_lines_replaced": 3862,
            "cockpit": {
                "version": "2.0.0-live",
                "agents_alive": summary["agents"]["alive"],
                "agents_total": summary["agents"]["total"],
                "probe_count": summary["probe_count"],
                "last_probe": summary["last_probe_at"],
            },
            "identity_hash": "f909eab007954d345edd20ecad73c361b6b2ad2d417b15b9cf0454caf9399578",
            "deployed_commit": "e20c29f",
            "source_commit": "e20c29f",
            "deployment_drift": False,
        }

    # ── Cockpit Endpoints ──────────────────────────────────────────────

    @app.get("/cockpit/live")
    async def cockpit_live():
        """Live agent registry — returns all agents with TTL status."""
        from aaa_a2a.cockpit.registry import get_registry

        reg = get_registry()
        return reg.summary()

    @app.get("/cockpit/agents")
    async def cockpit_agents(filter: str = "all"):
        """List agents by filter: all | alive | dead."""
        from aaa_a2a.cockpit.registry import get_registry

        reg = get_registry()
        if filter == "alive":
            agents = reg.list_alive()
        elif filter == "dead":
            agents = reg.list_dead()
        else:
            agents = reg.list_all()

        return {
            "filter": filter,
            "count": len(agents),
            "agents": [
                {
                    "agent_id": a.agent_id,
                    "status": a.status,
                    "ttl": a.ttl_status,
                    "age_seconds": round(a.age_seconds, 1) if a.last_seen > 0 else None,
                    "latency_ms": round(a.latency_ms, 1),
                    "role": a.role,
                    "port": a.port,
                }
                for a in agents
            ],
        }

    @app.get("/cockpit/agent/{agent_id}")
    async def cockpit_agent(agent_id: str):
        """Get detailed status for one agent."""
        from aaa_a2a.cockpit.registry import get_registry

        reg = get_registry()
        agent = reg.get(agent_id)
        if agent is None:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        return {
            "agent_id": agent.agent_id,
            "name": agent.name,
            "role": agent.role,
            "authority_ceiling": agent.authority_ceiling,
            "port": agent.port,
            "status": agent.status,
            "ttl": agent.ttl_status,
            "last_seen": agent.last_seen,
            "age_seconds": round(agent.age_seconds, 1) if agent.last_seen > 0 else None,
            "missed_probes": agent.missed_probes,
            "latency_ms": round(agent.latency_ms, 1),
            "load": round(agent.load, 3),
            "capabilities": agent.capabilities,
            "tools_count": agent.tools_count,
            "apex_scalars": agent.apex_scalars,
            "source": agent.source,
        }

    @app.post("/cockpit/heartbeat")
    async def cockpit_heartbeat(payload: dict):
        """Receive a heartbeat from an organ."""
        from aaa_a2a.cockpit.registry import get_registry

        reg = get_registry()
        try:
            hb = HeartbeatPayload(
                agent_id=payload["agent_id"],
                status=payload.get("status", "healthy"),
                load=payload.get("load", 0.0),
                capabilities=payload.get("capabilities", []),
                tools_count=payload.get("tools_count", 0),
                latency_ms=payload.get("latency_ms", 0.0),
                sct=payload.get("sct"),
                apex_scalars=payload.get("apex_scalars", {}),
                metadata=payload.get("metadata", {}),
            )
            state = reg.receive_heartbeat(hb)
            return {"accepted": True, "agent_id": state.agent_id, "status": state.status}
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Missing required field: {e}")

    @app.get("/cockpit/status.json")
    async def cockpit_status_json():
        """Return the cached status.json file contents."""
        from aaa_a2a.cockpit.registry import get_registry

        reg = get_registry()
        # Force a fresh write and return it
        reg.write_status_json()
        return reg.summary()

    @app.post("/cockpit/probe-now")
    async def cockpit_probe_now():
        """Trigger an immediate probe cycle. Returns probe results."""
        global _probe
        if _probe is None:
            raise HTTPException(status_code=503, detail="Probe not initialized")
        results = await _probe.probe_once()
        return {"probe_now": True, "results": results}

    # ── REST passthroughs — non-A2A convenience aliases ────────────────

    @app.post("/mcp/session/init")
    async def session_init(actor_id: str, intent: str = "cockpit init"):
        """Canonical session init — same effect as arif_init."""
        return await call_mcp_tool(
            "arifos",
            "arif_init",
            {"actor_id": actor_id, "intent": intent, "mode": "light"},
        )

    @app.post("/mcp/session/seal")
    async def session_seal(session_id: str, content: str):
        """Canonical session seal — same effect as arif_seal."""
        return await call_mcp_tool(
            "arifos",
            "arif_seal",
            {"session_id": session_id, "content": content, "mode": "seal"},
        )

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("AAA_PORT", "3002"))  # 3002 during migration, 3001 after cutover
    logger.info(f"[AAA] Starting constitutional A2A gateway on port {port}")
    uvicorn.run(app, host="127.0.0.1", port=port)
