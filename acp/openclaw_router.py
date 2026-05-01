"""
OpenClaw ACP Router — integrates ACP into OpenClaw command handling.

When a message comes into OpenClaw via Telegram, it can optionally be
routed via ACP to Hermes or another agent instead of OpenClaw handling
it directly.

Trigger commands:
    /acp <message>     → Route <message> via ACP
    /hermes <message>  → Direct dispatch to Hermes via ACP
    /a2a <agent> <msg> → Explicit agent-to-agent dispatch
    /agents            → List discovered ACP agents
    /route-status <id> → Check ACP run status

Example in Telegram:
    You: /hermes search memory for recent arifOS decisions
    OpenClaw: [ACP] Dispatching to Hermes (skill: memory-recall)
    OpenClaw: [ACP] ✓ Hermes completed → result
"""

import asyncio
import re
from typing import Optional
from AAA.acp.client import ACPClient
from AAA.acp.router import ACPRouter, AGENT_ENDPOINTS


# ─── ACP command parser ─────────────────────────────────────────────────────────

ACP_COMMANDS = [
    ("/acp",    "route_via_acp",   "Route message via ACP to best-matching agent"),
    ("/hermes", "route_to_hermes", "Direct dispatch to Hermes ACP agent"),
    ("/a2a",    "explicit_a2a",    "Explicit agent-to-agent dispatch: /a2a hermes <message>"),
    ("/agents", "list_agents",     "List all discovered ACP agents"),
    ("/route-status", "check_status", "Check status of an ACP run"),
    ("/route-cancel", "cancel_run",  "Cancel a running ACP task"),
]


async def handle_hermes_dispatch(content: str) -> str:
    """Direct dispatch to Hermes via ACP."""
    router = ACPRouter()
    
    # Determine skill from content
    agent_id = "hermes"
    skill_id = _infer_skill(content)
    
    try:
        async with router.client_for(agent_id) as client:
            task = await client.send_message(
                agent_id=agent_id,
                content=content,
                skill_id=skill_id,
            )
            
            # Poll for result
            import asyncio
            for _ in range(30):  # ~60s timeout
                await asyncio.sleep(2)
                status = await client.get_run_status(task.id)
                if status.status == "completed":
                    result = status.result or "(no result)"
                    return (
                        f"🧠 **Hermes ACP Result**\n"
                        f`└ Run ID: \`{task.id}\`\n`
                        f"└ Skill: `{skill_id}`\n"
                        f"└ Status: ✅ completed\n\n"
                        f"{result}"
                    )
                elif status.status == "failed":
                    return (
                        f"🛑 **Hermes ACP Error**\n"
                        f"└ Run ID: `{task.id}`\n"
                        f"└ Error: {status.error}"
                    )
            
            return f"⏳ **Hermes ACP** — Run `{task.id}` still in progress (polling timed out)"
    
    except Exception as e:
        return f"❌ ACP dispatch failed: {str(e)}"


async def handle_generic_acp(content: str) -> str:
    """Route to best-matching agent via ACP."""
    router = ACPRouter()
    agent_id, skill_id = router.classify_intent(content)
    
    if agent_id == "openclaw":
        return "🤖 OpenClaw will handle this directly (no ACP routing needed)."
    
    return await _dispatch_to_agent(router, agent_id, skill_id, content)


async def handle_explicit_a2a(parts: list[str]) -> str:
    """Explicit A2A: /a2a <agent_id> <message>"""
    if len(parts) < 3:
        return "Usage: /a2a <agent_id> <message>\nExample: /a2a hermes search memory for recent decisions"
    
    agent_id = parts[1]
    content = " ".join(parts[2:])
    
    if agent_id not in AGENT_ENDPOINTS:
        return f"Unknown agent: `{agent_id}`\nKnown agents: {', '.join(AGENT_ENDPOINTS.keys())}"
    
    router = ACPRouter()
    skill_id = _infer_skill(content)
    return await _dispatch_to_agent(router, agent_id, skill_id, content)


async def handle_list_agents() -> str:
    """List all discovered ACP agents."""
    router = ACPRouter()
    discovered = []
    missing = []
    
    for agent_id, endpoint in AGENT_ENDPOINTS.items():
        try:
            client = ACPClient(base_url=endpoint, timeout=5.0)
            async with client:
                card = await client.get_agent_card(agent_id)
                discovered.append((agent_id, card.name, card.description[:60]))
        except Exception:
            missing.append(agent_id)
    
    lines = ["🔌 **ACP Agents**\n"]
    for aid, name, desc in discovered:
        lines.append(f"✅ `{aid}` — *{name}*\n   └ {desc}")
    if missing:
        lines.append(f"\n⚠️ Unreachable: {', '.join(missing)}")
    
    return "\n".join(lines)


async def handle_route_status(run_id: str) -> str:
    """Check status of an ACP run."""
    # Try Hermes first
    for agent_id in AGENT_ENDPOINTS:
        try:
            client = ACPClient(base_url=AGENT_ENDPOINTS[agent_id], timeout=5.0)
            async with client:
                task = await client.get_run_status(run_id)
                status_icon = {
                    "pending": "⏳", "in_progress": "🔄",
                    "completed": "✅", "failed": "❌", "cancelled": "🚫",
                }.get(task.status, "❓")
                
                result_text = f"\n└ Result: {task.result[:200]}..." if task.result else ""
                error_text = f"\n└ Error: {task.error}" if task.error else ""
                
                return (
                    f"{status_icon} **Run `{run_id}`**\n"
                    f"└ Agent: `{task.agent_id}`\n"
                    f"└ Status: `{task.status}`\n"
                    f"└ Created: {task.created_at.strftime('%H:%M:%S')}\n"
                    f"{result_text}{error_text}"
                )
        except Exception:
            continue
    
    return f"❌ Run `{run_id}` not found on any known ACP agent."


async def _dispatch_to_agent(
    router: ACPRouter,
    agent_id: str,
    skill_id: Optional[str],
    content: str,
) -> str:
    """Internal dispatch helper."""
    try:
        async with router.client_for(agent_id) as client:
            task = await client.send_message(
                agent_id=agent_id,
                content=content,
                skill_id=skill_id,
            )
            
            import asyncio
            for _ in range(30):
                await asyncio.sleep(2)
                status = await client.get_run_status(task.id)
                if status.status == "completed":
                    result = status.result or "(no result)"
                    icon = {"hermes": "🧠", "opencode": "💻", "maxhermes": "🌍"}.get(agent_id, "🔧")
                    return (
                        f"{icon} **{agent_id.upper()} ACP Result**\n"
                        f"└ Skill: `{skill_id}`\n"
                        f"└ Run: `/{task.id[:8]}`\n"
                        f"└ Status: ✅\n\n"
                        f"{result}"
                    )
                elif status.status == "failed":
                    return f"❌ {agent_id} failed: {status.error}"
            
            return f"⏳ Dispatched to `{agent_id}` (run: `{task.id}`) — still processing"
    
    except Exception as e:
        return f"❌ ACP dispatch to `{agent_id}` failed: {str(e)}"


def _infer_skill(content: str) -> Optional[str]:
    """Infer which ACP skill to use based on message content."""
    content_lower = content.lower()
    
    skill_map = {
        "memory-recall": ["remember", "search memory", "recall", "what did we", "find in", "past"],
        "reasoning-chain": ["analyze", "reason", "logic", "implication", "think through"],
        "memory-curation": ["update memory", "save this", "log this", "remember this"],
    }
    
    for skill_id, keywords in skill_map.items():
        if any(k in content_lower for k in keywords):
            return skill_id
    
    return None


# ─── Telegram message handler ───────────────────────────────────────────────────

async def handle_telegram_message(text: str) -> Optional[str]:
    """
    Parse a Telegram message and handle ACP commands.
    Returns response string, or None if not an ACP command.
    """
    text = text.strip()
    
    if text.startswith("/acp "):
        return await handle_generic_acp(text[5:])
    
    elif text.startswith("/hermes "):
        return await handle_hermes_dispatch(text[8:])
    
    elif text.startswith("/a2a "):
        parts = text.split()
        return await handle_explicit_a2a(parts)
    
    elif text.strip() == "/agents":
        return await handle_list_agents()
    
    elif text.startswith("/route-status "):
        return await handle_route_status(text[14:].strip())
    
    elif text.startswith("/route-cancel "):
        run_id = text[14:].strip()
        return f"Cancel not yet implemented for run: {run_id}"
    
    # Not an ACP command — let OpenClaw handle normally
    return None
