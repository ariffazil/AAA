"""
ACPRouter — Task routing engine for AAA ACP fleet.
Determines which agent should handle a given task and dispatches via ACP.

Arif's ACP routing rules:
    OPENCLAW → handles gateway/routing/dispatch
    HERMES   → handles memory recall, deep reasoning, curation
    OPENCODE → handles coding tasks
    MAXHERMES → handles GEOX/Earth domain
    HERMES-OPS → handles DevOps/scripts

When a message comes into OpenClaw (via Telegram or ACP):
    1. Classify intent
    2. Match to agent capability
    3. Dispatch via ACP client
    4. Log to VAULT999
"""

from __future__ import annotations
from typing import Optional
from AAA.acp.models import AgentCard, ACPSkill
from AAA.acp.client import ACPClient


# ─── Routing registry ──────────────────────────────────────────────────────────

AGENT_ENDPOINTS = {
    "openclaw": "http://localhost:8081",   # OpenClaw ACP endpoint
    "hermes":   "http://localhost:8082",     # Hermes ACP endpoint
    "opencode": "http://localhost:8083",     # OpenCode (future)
    "maxhermes": "http://localhost:8084",    # MaxHermes GEOX (future)
}


class ACPRouter:
    """
    Routes tasks to the appropriate ACP agent based on intent classification.
    """

    def __init__(self):
        self._clients: dict[str, ACPClient] = {}
        self._agent_cards: dict[str, AgentCard] = {}

    def client_for(self, agent_id: str) -> ACPClient:
        """Get or create an ACP client for an agent."""
        if agent_id not in self._clients:
            endpoint = AGENT_ENDPOINTS.get(agent_id)
            if not endpoint:
                raise ValueError(f"No ACP endpoint registered for agent: {agent_id}")
            self._clients[agent_id] = ACPClient(base_url=endpoint)
        return self._clients[agent_id]

    async def dispatch(
        self,
        agent_id: str,
        content: str,
        skill_id: Optional[str] = None,
        session_id: Optional[str] = None,
        timeout: float = 60.0,
    ) -> dict:
        """
        Dispatch a task to the appropriate agent via ACP.
        
        Returns:
            dict with keys: success, agent_id, run_id, result, error
        """
        client = self.client_for(agent_id)
        async with client:
            try:
                task = await client.send_message(
                    agent_id=agent_id,
                    content=content,
                    skill_id=skill_id,
                    session_id=session_id,
                )
                
                # Poll for completion (simple polling for now)
                import asyncio
                for _ in range(int(timeout / 2)):
                    await asyncio.sleep(2)
                    status_task = await client.get_run_status(task.id)
                    if status_task.status == "completed":
                        return {
                            "success": True,
                            "agent_id": agent_id,
                            "run_id": task.id,
                            "result": status_task.result,
                            "error": None,
                        }
                    elif status_task.status == "failed":
                        return {
                            "success": False,
                            "agent_id": agent_id,
                            "run_id": task.id,
                            "result": None,
                            "error": status_task.error,
                        }
                
                return {
                    "success": False,
                    "agent_id": agent_id,
                    "run_id": task.id,
                    "result": None,
                    "error": "Timeout waiting for result",
                }

            except Exception as e:
                return {
                    "success": False,
                    "agent_id": agent_id,
                    "run_id": None,
                    "result": None,
                    "error": str(e),
                }

    # ─── Intent classification ───────────────────────────────────────────────

    INTENT_KEYWORDS = {
        "hermes": {
            "memory-recall": [
                "remember", "what did we", "search memory", "find in memory",
                "recall", "past decision", "what was decided", "who said",
                "context from", "related to", "history of",
            ],
            "reasoning-chain": [
                "reason through", "analyze", "think step", "logic chain",
                "implications", "consequences of", "reasoning for",
                "trace the logic", "what if we",
            ],
            "memory-curation": [
                "update memory", "save to memory", "remember this",
                "log this", "write to memory", "curate", "index",
            ],
        },
        "opencode": {
            "code": ["write code", "implement", "build", "fix bug", "refactor",
                     "function", "class", "python", "typescript", "debug"],
            "review": ["review code", "check code", "lint", "audit code"],
        },
        "maxhermes": {
            "geox": ["geology", "well", "subsurface", "petrophysics", "seismic",
                     "lithology", "porosity", "log", "basin", "earth domain"],
        },
    }

    def classify_intent(self, content: str) -> tuple[str, Optional[str]]:
        """
        Classify user intent → (agent_id, skill_id).
        Returns ("openclaw", None) if no specific agent matches.
        """
        content_lower = content.lower()

        # Check Hermes skills
        hermes_card = self._agent_cards.get("hermes")
        if hermes_card:
            for skill in hermes_card.skills:
                for keyword in self.INTENT_KEYWORDS.get("hermes", {}).get(skill.id, []):
                    if keyword in content_lower:
                        return ("hermes", skill.id)

        # Check other agents
        for agent_id, skills in self.INTENT_KEYWORDS.items():
            for skill_id, keywords in skills.items():
                for keyword in keywords:
                    if keyword in content_lower:
                        return (agent_id, skill_id)

        return ("openclaw", None)  # Default: OpenClaw handles it

    async def load_agent_cards(self):
        """Discover and cache agent cards from all known endpoints."""
        for agent_id, endpoint in AGENT_ENDPOINTS.items():
            try:
                client = ACPClient(base_url=endpoint)
                async with client:
                    card = await client.get_agent_card(agent_id)
                    self._agent_cards[agent_id] = card
                    print(f"[ACPRouter] Discovered agent: {agent_id} ({card.name})")
            except Exception as e:
                print(f"[ACPRouter] Could not reach {agent_id} at {endpoint}: {e}")
