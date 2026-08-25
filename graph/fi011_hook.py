#!/usr/bin/env python3
"""
fi011_hook.py — FI-011 hook for arifOS delegation_envelope.

What this is
------------
A thin import shim that, when called from arifOS's `delegation_envelope.py`,
runs FI-011's context-prune pipeline against the parent context before
sealing a child envelope.

arifOS-side patch (T3 territory — Arif gates apply):
    # In arifOS/arifosmcp/runtime/delegation_envelope.py, near top:
    try:
        import sys
        sys.path.insert(0, "/root/AAA/graph")
        from fi011_hook import prune_parent_context
        HAS_FI011 = True
    except ImportError:
        HAS_FI011 = False

    # Inside DelegationEnvelope.sign() (or before signing), if
    # HAS_FI011 and parent_session_id has a known context payload:
        if HAS_FI011 and self.parent_context_files:
            pruned = prune_parent_context(
                self.parent_session_id,
                self.parent_context_files,
                task_hint=self.task_hint or "",
            )
            self.parent_context_files = pruned["kept"]
            self.context_prune_receipt = pruned   # attached for audit

If FI-011 graph_bridge is unreachable, `prune_parent_context` returns
the unchanged file list with `graceful: True` and `warning` set —
delegation_envelope stays safe-fall-back.

DITEMPA BUKAN DIBERI ⚒️ — graph says, we obey, but never punish.
"""
from __future__ import annotations
import hashlib
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from typing import Optional

# Re-use prune_context module
sys.path.insert(0, "/root/AAA/graph")
from prune_context import prune_for_task, BRIDGE_URL  # noqa: E402

DEFAULT_MAX_TOKENS = int(os.environ.get("FI011_MAX_TOKENS", "8000"))
DEFAULT_DEPTH = int(os.environ.get("FI011_DEPTH", "1"))


def prune_parent_context(
    parent_session_id: str,
    parent_context_files: list[str],
    *,
    task_hint: str = "",
    bridge_url: Optional[str] = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    depth: int = DEFAULT_DEPTH,
) -> dict:
    """FI-011 entry point for delegation_envelope.

    Wraps prune_for_task() with an F11-shaped receipt suitable for
    attaching to a DelegationEnvelope as audit metadata.
    """
    started = time.time()

    if not parent_context_files:
        return {
            "tool": "fi011_prune",
            "version": "0.1",
            "kept": [],
            "dropped": [],
            "graceful": True,
            "bridge_ok": True,
            "input_files_count": 0,
            "estimated_tokens_saved": 0,
            "duration_ms": int((time.time() - started) * 1000),
            "receipt_id": f"pr-{uuid.uuid4().hex[:12]}",
            "parent_session_id": parent_session_id,
            "task_hint": task_hint[:200] if task_hint else None,
        }

    raw = prune_for_task(
        task_hint or f"delegation from session {parent_session_id}",
        parent_context_files,
        bridge_url=bridge_url or BRIDGE_URL,
        max_tokens=max_tokens,
        depth=depth,
    )

    # Convert prune_context receipt → FI-011 receipt
    return {
        "tool": "fi011_prune",
        "version": "0.1",
        "parent_session_id": parent_session_id,
        "task_hint": task_hint[:200] if task_hint else None,
        "kept": raw.get("kept", []),
        "dropped": raw.get("dropped", []),
        "graceful": raw.get("graceful", True),
        "bridge_ok": raw.get("bridge_ok", False),
        "input_files_count": len(raw.get("input_files", [])),
        "estimated_tokens_saved": raw.get("estimated_tokens_saved", 0),
        "duration_ms": int((time.time() - started) * 1000),
        "task_hash": raw.get("task_hash"),
        "graph_queries_count": len(raw.get("graph_queries", [])),
        "warning": raw.get("warning"),
        "safety_override": raw.get("safety_override", False),
        "receipt_id": f"pr-{uuid.uuid4().hex[:12]}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ─── optional integration ──────────────────────────────────────────────────


def attach_prune_to_envelope(envelope: object) -> dict:
    """If envelope has parent_context_files attribute, prune in-place.

    Returns the FI-011 receipt. Mutates envelope.parent_context_files.
    """
    files = getattr(envelope, "parent_context_files", None)
    if not files:
        return {"tool": "fi011_prune", "skipped": "no parent_context_files",
                "graceful": True}
    receipt = prune_parent_context(
        getattr(envelope, "parent_session_id", "unknown"),
        list(files),
        task_hint=getattr(envelope, "task_hint", "") or "",
    )
    if receipt.get("graceful") and receipt.get("kept") is not None:
        envelope.parent_context_files = receipt["kept"]
    envelope.context_prune_receipt = receipt
    return receipt


# ─── CLI ──────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    import json
    if len(sys.argv) < 3:
        print("usage: fi011_hook.py <parent_session_id> <file1> [<file2> ...]\n"
              "  example: fi011_hook.py session-abc arifOS/judge.py arifOS/server.py")
        sys.exit(0)
    sess = sys.argv[1]
    files = sys.argv[2:]
    print(json.dumps(prune_parent_context(sess, files), indent=2))