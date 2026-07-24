"""AAA A2A Server — constitutional overlay on official a2a-sdk.

Replaces 3,862 lines of Express with ~50 lines of Python + SDK.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import logging
import os
import uvicorn
from fastapi import FastAPI

from a2a.server.request_handlers.default_request_handler import LegacyRequestHandler
from a2a.server.routes.fastapi_routes import add_a2a_routes_to_fastapi
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill, AgentProvider

from aaa_a2a.executor import ConstitutionalExecutor
from aaa_a2a.routing.organ_router import call_mcp_tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aaa.server")


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


def create_app() -> FastAPI:
    """Create the AAA FastAPI application."""
    app = FastAPI(
        title="AAA Constitutional A2A Gateway",
        description="Governance overlay on A2A transport. AAA decides WHETHER. A-FORGE decides HOW.",
        version="2.0.0",
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

    # Health endpoint
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "protocol": "A2A",
            "version": "2.0.0",
            "gateway": "AAA",
            "motto": "Ditempa Bukan Diberi",
            "overlay": "constitutional",
            "express_lines_replaced": 3862,
        }

    # REST passthroughs — non-A2A convenience aliases so plain HTTP callers
    # (curl, scripts) can hit AAA directly without speaking JSONRPC. These
    # are 1:1 proxies to arifOS at port 8088; no logic added.
    @app.post("/mcp/session/init")
    async def session_init(actor_id: str, intent: str = "cockpit init"):
        """Canonical session init — same effect as arif_init. Returns the
        envelope as the kernel mints it (session_id, session_token, etc.)."""
        return await call_mcp_tool(
            "arifos", "arif_init",
            {"actor_id": actor_id, "intent": intent, "mode": "light"},
        )

    @app.post("/mcp/session/seal")
    async def session_seal(session_id: str, content: str):
        """Canonical session seal — same effect as arif_seal. Returns
        entry_id + chain_hash on success."""
        return await call_mcp_tool(
            "arifos", "arif_seal",
            {"session_id": session_id, "content": content, "mode": "seal"},
        )

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("AAA_PORT", "3002"))  # 3002 during migration, 3001 after cutover
    logger.info(f"[AAA] Starting constitutional A2A gateway on port {port}")
    uvicorn.run(app, host="127.0.0.1", port=port)
