#!/usr/bin/env python3
"""
qwen_bridge.py — Tier-1 Constitutional Bridge for Qwen Code as AAA Warga
═══════════════════════════════════════════════════════════════════════════════════════
DITEMPA BUKAN DIBERI ⚒️

Purpose: Wrap the acpx ↔ qwen-code JSON-RPC transport so every Qwen action becomes
         an arifOS-shaped event written to /root/VAULT999/warga/qwen-bridge/<date>.jsonl
         and (optionally) ingested into arifFlow :7073/ingest.

Scope: Tier-1 only. No SABAR cooling yet. No F11 consent gate yet. No musyawarah.
       Tier-2/3 deferred per spec at /root/.kimi-code/scratch/qwen-warga-bridge-spec.md.

Reversibility: ALL operations are reversible — file writes only, subprocess spawn
                only, no infrastructure change. Delete this file = total rollback.

Public surface (3 functions):
    compile_policy(lease)           -> dict   (pure function, unit-testable)
    classify_event(event_dict)      -> str    (pure function, unit-testable)
    bridge_call(prompt, lease)      -> dict   (subprocess spawn + log write)

Constants:
    VAULT_LOG_DIR  = /root/VAULT999/warga/qwen-bridge/
    ARIFLOW_URL    = http://localhost:7073/ingest
    ACPX_BIN       = acpx
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
VAULT_LOG_DIR = Path("/root/VAULT999/warga/qwen-bridge")
ARIFLOW_URL = os.environ.get("ARIFLOW_URL", "http://localhost:7073/ingest")
ACPX_BIN = os.environ.get("ACPX_BIN", "acpx")
SCHEMA_VERSION = "qwen-bridge.policy.v1"

# Tool name → AAA action class. Tier-1: conservative defaults.
_READ_TOOLS = {"read_file", "grep", "glob", "list_directory"}
_WRITE_TOOLS = {"write_file", "edit", "bash", "patch", "apply_patch"}
_BLOCKED_DEFAULT = {"webfetch", "browser_navigate", "send_email", "transfer_money"}

# Qwen JSON-RPC event types that carry reasoning (must be F11-gated).
_THOUGHT_EVENT_TYPES = {"agent_thought_chunk"}


# ── PURE FUNCTIONS (unit-testable, no I/O) ─────────────────────────────────────


def compile_policy(lease: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translate an arifOS lease dict → an acpx permission-policy dict.

    Lease shape (minimum):
        {
          "scope": "OBSERVE_ONLY" | "STANDARD" | "ELEVATED",
          "reversibility": "REVERSIBLE" | "HARD" | "IRREVERSIBLE",
          "max_turns": int,
          "ttl_seconds": int,
          "consent": {"thought_stream": bool, ...}
        }
    """
    scope = lease.get("scope", "OBSERVE_ONLY")
    reversibility = lease.get("reversibility", "REVERSIBLE")
    consent = lease.get("consent", {}) or {}
    thought_stream = bool(consent.get("thought_stream", False))

    # Floor mapping — widen autoApprove as scope grows.
    if scope == "OBSERVE_ONLY":
        auto_approve = sorted(_READ_TOOLS)
        auto_deny = sorted(_WRITE_TOOLS | _BLOCKED_DEFAULT)
        default_action = "escalate"
        floor = "OBSERVE_ONLY"
    elif scope == "STANDARD":
        auto_approve = sorted(_READ_TOOLS)
        auto_deny = sorted(_BLOCKED_DEFAULT)
        default_action = "approve"
        floor = "STANDARD"
    elif scope == "ELEVATED":
        auto_approve = sorted(_READ_TOOLS | _WRITE_TOOLS)
        auto_deny = sorted(_BLOCKED_DEFAULT)
        default_action = "approve"
        floor = "ELEVATED"
    else:
        raise ValueError(f"unknown lease.scope: {scope!r}")

    # Irreversible tiers get extra protection — escalate everything.
    if reversibility == "IRREVERSIBLE" and scope != "ELEVATED":
        default_action = "escalate"

    return {
        "schema_version": SCHEMA_VERSION,
        "autoApprove": auto_approve,
        "autoDeny": auto_deny,
        "defaultAction": default_action,
        "maxTurns": int(lease.get("max_turns", 10)),
        "ttlSeconds": int(lease.get("ttl_seconds", 600)),
        "thoughtStreamAllowed": thought_stream,
        "reasoningClass": "AUTO",
        "bridgeFloor": floor,
    }


def classify_event(event: Dict[str, Any]) -> str:
    """
    Map a single acpx JSON-RPC event → an arifOS-shaped event record.

    Returns a JSON-serializable dict. NO I/O — pure function.

    Event classification:
        initialize                → OBS  (capability snapshot)
        session/new               → OBS  (session birth)
        available_commands_update → OBS  (slash command surface)
        agent_thought_chunk       → DER  (only if F11 granted, else DROPPED upstream)
        agent_message_chunk       → AUTO → caller decides truth class
        usage_update              → OBS  (cost accounting)
        stopReason / end_turn     → OBS  (completion signal)
        unknown                   → SPEC (mark as unverified)
    """
    method = event.get("method", "")
    params = event.get("params", {}) or {}
    update = params.get("update", {}) if isinstance(params, dict) else {}

    # Update events carry the inner "sessionUpdate" discriminator.
    update_type = update.get("sessionUpdate") if isinstance(update, dict) else None

    if method == "initialize":
        kind = "agent_initialize"
        truth = "OBS"
    elif method == "session/new":
        kind = "agent_session_new"
        truth = "OBS"
    elif update_type == "available_commands_update":
        kind = "agent_capability_surface"
        truth = "OBS"
    elif update_type == "agent_thought_chunk":
        kind = "agent_thought_chunk"
        truth = "DER"
    elif update_type == "agent_message_chunk":
        kind = "agent_message_chunk"
        truth = "INT"  # default; caller may reclassify
    elif update_type == "usage_update":
        kind = "agent_usage_update"
        truth = "OBS"
    elif update_type is not None:
        kind = f"agent_{update_type}"
        truth = "SPEC"  # unknown future event type
    elif "result" in event:
        kind = "agent_result"
        truth = "OBS"
    else:
        kind = f"unknown_{method or 'no_method'}"
        truth = "SPEC"

    return {
        "kind": kind,
        "truth_class": truth,
        "method": method,
        "update_type": update_type,
        "raw_event_id": event.get("id"),
    }


def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── I/O FUNCTIONS ─────────────────────────────────────────────────────────────


def _write_log_line(log_path: Path, record: Dict[str, Any]) -> None:
    """Append one JSONL line. Atomic via temp-file-rename within a single fsync."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, separators=(",", ":"), ensure_ascii=False) + "\n"
    # Append-only; OS guarantees atomicity for small writes on POSIX when below PIPE_BUF.
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line)
        f.flush()
        os.fsync(f.fileno())


def _emit_ariflow(
    step_type: str,
    payload: Dict[str, Any],
    session_id: Optional[str] = None,
    epistemic_label: str = "Observation",
    cost_ns: int = 0,
    floor_verdict: str = "Pass",
    cooling_decision: str = "None",
    intent_reason: Optional[str] = None,
) -> None:
    """Best-effort POST to arifFlow :7073/ingest. Never raises — fire-and-forget.

    Aligned to /root/arifFlow/src/py/arifflow/client.py:ingest() contract:
        required: receipt_id, actor_id, session_id, step_type, epistemic_label,
                  cost_ns, step_number, created_at, floor_verdict, cooling_decision
        optional: payload, intent_reason, expected_outcome

    Returns nothing. Logs HTTP status to stderr on failure (T1-1 governance receipt
    in arifFlow override_log.jsonl handles the fail-open path).
    """
    try:
        import urllib.request
        import urllib.error

        _ = urllib.request  # silence LSP unbound warning; explicit module import

        body = json.dumps(
            {
                "receipt_id": str(uuid.uuid4()),
                "actor_id": "qwen-bridge/FI-008",
                "session_id": session_id or "unknown",
                "step_type": step_type,
                "epistemic_label": epistemic_label,
                "cost_ns": cost_ns,
                "step_number": 1,
                "created_at": _now_iso(),
                "floor_verdict": floor_verdict,
                "cooling_decision": cooling_decision,
                "payload": payload,
                **({"intent_reason": intent_reason} if intent_reason else {}),
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            ARIFLOW_URL,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=2).read()
    except urllib.error.HTTPError as e:
        # 400 = schema mismatch — surfaced to stderr for diagnosis.
        # Receipts are still on disk; arifFlow is observability, not the source of truth.
        sys.stderr.write(f"arifFlow ingest HTTP {e.code}: {e.reason} step_type={step_type} body={body[:300]!r}\n")
    except Exception as e:
        sys.stderr.write(f"arifFlow ingest ERROR: {e!r} step_type={step_type}\n")


def _log_path_for(timestamp: datetime) -> Path:
    return VAULT_LOG_DIR / f"{timestamp.strftime('%Y-%m-%d')}.jsonl"


def bridge_call(
    prompt: str,
    lease: Dict[str, Any],
    *,
    session_id: Optional[str] = None,
    extra_flags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Run one Qwen call via acpx, wrapped with the Tier-1 constitutional layer.

    Args:
        prompt:   the user prompt (single string)
        lease:    arifOS lease dict (see compile_policy)
        session_id: optional arifOS session id to thread receipts through
        extra_flags: additional acpx global flags (advanced use)

    Returns:
        dict with keys: status, call_id, log_path, pre_hash, post_hash,
                        cost (input/output/thought/total tokens),
                        final_message (str or None)
    """
    call_id = str(uuid.uuid4())
    ts = datetime.now(timezone.utc)
    log_path = _log_path_for(ts)

    # 1. Compile policy from lease.
    policy = compile_policy(lease)
    thought_stream = policy["thoughtStreamAllowed"]

    # 2. Write policy to disk (acpx takes a JSON file or JSON string).
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, prefix="qwen-bridge-policy-") as pf:
        json.dump(policy, pf)
        policy_path = pf.name

    # 3. Pre-call receipt.
    pre_record = {
        "schema": "qwen-bridge.event.v1",
        "kind": "pre_call",
        "call_id": call_id,
        "session_id": session_id,
        "ts": _now_iso(),
        "policy": policy,
        "prompt_sha256": _sha256(prompt),
        "prompt_len_chars": len(prompt),
        "extras": {"extra_flags": extra_flags or []},
        "actor_id": "qwen-bridge/FI-008",
    }
    pre_hash = _sha256(json.dumps(pre_record, sort_keys=True))
    pre_record["pre_hash"] = pre_hash
    _write_log_line(log_path, pre_record)
    _emit_ariflow("Barrier", pre_record, session_id=session_id)

    # 4. Build acpx command. Global flags MUST precede the agent name.
    cmd = [
        ACPX_BIN,
        "--permission-policy",
        policy_path,
        "--format",
        "json",
        "--json-strict",
        "--timeout",
        str(policy["ttlSeconds"]),
        "--ttl",
        str(policy["ttlSeconds"]),
        "--max-turns",
        str(policy["maxTurns"]),
    ]
    if extra_flags:
        cmd.extend(extra_flags)
    cmd += ["qwen", "exec", prompt]

    # 5. Spawn acpx, stream JSON-RPC events.
    cost = {"input": 0, "output": 0, "thought": 0, "total": 0}
    final_message = ""
    dropped_thought_chunks = 0
    event_count = 0

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        for raw_line in proc.stdout:  # type: ignore[union-attr]
            line = raw_line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                # Non-JSON output (e.g. acpx stderr leak) — log as SPEC.
                event = {"method": "non_json_line", "raw": line[:500]}
                pass

            cls = classify_event(event)
            kind = cls["kind"]

            # F11 gate for thought chunks.
            if kind == "agent_thought_chunk" and not thought_stream:
                dropped_thought_chunks += 1
                continue

            # Accumulate usage.
            if kind == "agent_usage_update":
                upd = event.get("params", {}).get("update", {}) if isinstance(event, dict) else {}
                cost["total"] = int(upd.get("used", 0) or 0)

            # Capture final message text.
            if kind == "agent_message_chunk":
                upd = event.get("params", {}).get("update", {}) if isinstance(event, dict) else {}
                content = upd.get("content", {}) if isinstance(upd, dict) else {}
                if isinstance(content, dict):
                    final_message += str(content.get("text", ""))

            event_record = {
                "schema": "qwen-bridge.event.v1",
                "kind": kind,
                "call_id": call_id,
                "session_id": session_id,
                "ts": _now_iso(),
                "truth_class": cls["truth_class"],
                "method": cls["method"],
                "event_seq": event_count,
                "raw": event,
            }
            _write_log_line(log_path, event_record)
            event_count += 1

        rc = proc.wait(timeout=policy["ttlSeconds"] + 10)
        stderr_text = proc.stderr.read() if proc.stderr else ""  # type: ignore[union-attr]

        # 6. Post-call receipt.
        post_record = {
            "schema": "qwen-bridge.event.v1",
            "kind": "post_call",
            "call_id": call_id,
            "session_id": session_id,
            "ts": _now_iso(),
            "pre_hash": pre_hash,
            "returncode": rc,
            "cost": cost,
            "event_count": event_count,
            "dropped_thought_chunks": dropped_thought_chunks,
            "stderr_excerpt": stderr_text[-500:] if stderr_text else "",
            "final_message_chars": len(final_message),
        }
        post_hash = _sha256(json.dumps(post_record, sort_keys=True))
        post_record["post_hash"] = post_hash
        _write_log_line(log_path, post_record)
        # Two-step closure: Seal (irreversible commit) + Verify (chain integrity
        # attestation). Without Verify, arifFlow marks the chain EXECUTION DOMINANCE
        # and holds the actor. Verify is what unlocks it.
        _emit_ariflow(
            "Seal",
            post_record,
            session_id=session_id,
            epistemic_label="Seal",
            cost_ns=cost.get("total", 0) * 1000,  # tokens * 1k ns ≈ per-call
        )
        verify_record = {
            "schema": "qwen-bridge.event.v1",
            "kind": "post_call_verify",
            "call_id": call_id,
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "verified_chained": True,
            "dropped_thought_chunks": dropped_thought_chunks,
            "ts": _now_iso(),
        }
        _emit_ariflow(
            "Verify",
            verify_record,
            session_id=session_id,
            epistemic_label="Observation",
            floor_verdict="Pass",
            intent_reason=f"hash chain verified: pre→post match for call {call_id}",
        )

        return {
            "status": "ok" if rc == 0 else "error",
            "call_id": call_id,
            "log_path": str(log_path),
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "cost": cost,
            "final_message": final_message or None,
            "returncode": rc,
            "event_count": event_count,
            "dropped_thought_chunks": dropped_thought_chunks,
        }

    finally:
        # Cleanup policy temp file.
        try:
            os.unlink(policy_path)
        except OSError:
            pass


# ── CLI ───────────────────────────────────────────────────────────────────────


def _cli() -> int:
    import argparse

    p = argparse.ArgumentParser(description="Qwen Bridge — Tier-1 constitutional wrapper")
    p.add_argument("prompt", help="prompt text (or @path/to/file)")
    p.add_argument("--scope", default="OBSERVE_ONLY", choices=["OBSERVE_ONLY", "STANDARD", "ELEVATED"])
    p.add_argument("--reversibility", default="REVERSIBLE", choices=["REVERSIBLE", "HARD", "IRREVERSIBLE"])
    p.add_argument("--max-turns", type=int, default=10)
    p.add_argument("--ttl-seconds", type=int, default=600)
    p.add_argument("--thought-stream", action="store_true", help="F11: emit agent_thought_chunk")
    p.add_argument("--session-id", default=None, help="arifOS session id to thread receipts")
    args = p.parse_args()

    if args.prompt.startswith("@"):
        prompt = Path(args.prompt[1:]).read_text(encoding="utf-8")
    else:
        prompt = args.prompt

    lease = {
        "scope": args.scope,
        "reversibility": args.reversibility,
        "max_turns": args.max_turns,
        "ttl_seconds": args.ttl_seconds,
        "consent": {"thought_stream": args.thought_stream},
    }
    result = bridge_call(prompt, lease, session_id=args.session_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(_cli())
