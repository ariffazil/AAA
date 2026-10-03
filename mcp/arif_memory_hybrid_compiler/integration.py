"""
Integration shim for arif_memory hybrid recall.

Per Arif 2026-10-03: this is a PIPE, not a new DOOR.
The arif_memory canonical handler is the door.
This module is a thin wrapper that allows arif_memory recall to invoke
the compiler without changing the public surface.

Usage in arif_memory recall handler (tool_13_arif_memory.py):
  if payload.get("hybrid"):
      from arifosmcp.mcp.arif_memory_hybrid_compiler.integration import hybrid_recall
      result = await hybrid_recall(query=..., peer=..., budget=..., peer_id=...)
      return _wrap_in_envelope(result)
  else:
      # existing v4 baseline (engineering_memory_dispatch_impl)
      ...
"""
from __future__ import annotations

import asyncio
import logging
import sys
from typing import Any

logger = logging.getLogger("arif_memory.hybrid_compiler.integration")

# Path to the compiler. In production this is /opt/arifos/arifosmcp/mcp/...
# We import as a module to share code.
COMPILER_PATH = "/root/AAA/mcp/arif_memory_hybrid_compiler"

def _load_compiler():
    """Lazy-load the compiler module. Avoids hard import at module level."""
    if COMPILER_PATH not in sys.path:
        sys.path.insert(0, COMPILER_PATH)
    import server  # type: ignore
    return server

async def hybrid_recall(
    query: str,
    peer: str = "arif",
    budget: int = 2000,
    graph_hops: int = 1,
    peer_id: str | None = None,
) -> dict:
    """
    Call the Hybrid Context Compiler.
    Returns the evidence bundle from server.compile().
    
    peer_id: optional session/actor context (for VAULT999 audit if ever wired).
    """
    server = _load_compiler()
    payload = {
        "peer": peer,
        "budget": budget,
        "graph_expand": graph_hops,
    }
    if peer_id:
        payload["peer_id"] = peer_id
    return await asyncio.to_thread(server.HybridContextCompiler().compile, query, payload)


def hybrid_recall_sync(
    query: str,
    peer: str = "arif",
    budget: int = 2000,
    graph_hops: int = 1,
) -> dict:
    """Sync version for non-async callers (e.g. test scripts)."""
    server = _load_compiler()
    payload = {
        "peer": peer,
        "budget": budget,
        "graph_expand": graph_hops,
    }
    return server.HybridContextCompiler().compile(query, payload)
