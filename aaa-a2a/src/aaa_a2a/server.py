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

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("AAA_PORT", "3002"))  # 3002 during migration, 3001 after cutover
    logger.info(f"[AAA] Starting constitutional A2A gateway on port {port}")
    uvicorn.run(app, host="127.0.0.1", port=port)
