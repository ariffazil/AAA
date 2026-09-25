#!/usr/bin/env python3
"""
federation_hook_engine.py — Universal Agentic Hook Engine for AAA Citizens
Canonical Path: /root/AAA/hooks/lib/federation_hook_engine.py

Governs all 7 AAA agent harnesses (OpenCode, Claude Code, Hermes, OpenClaw, Antigravity, Kimi, Qwen).
Implements the Unified 5-Phase Hook Spine:
  - 000_BOOT: Session ignition, kernel init, active scar priming
  - 100_GATE: Pre-tool monotonic ladder, ignition pass-through, ACT auto-minting, rollback journal
  - 200_HEAL: Post-tool telemetry, HTTP 406 / zombie / git auto-healing reflex
  - 300_METABOLIZE: Turn-level epistemic metabolism, anti-tangguh sentry, scar crystallization
  - 999_SEAL: Generational carry-forward append, vault sealing, journal flush

Zero external dependencies — standard library only.
"""

from __future__ import annotations

import argparse
import enum
import fcntl
import hashlib
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# --- Canonical Constants & Paths ---
KERNEL_URL = os.environ.get("ARIFOS_KERNEL_URL", "http://127.0.0.1:8088")
CARRY_PATH = Path("/root/.local/share/arifos/carry_forward.json")
SCARS_DIR = Path("/root/AAA/scars")
ROLLBACK_JOURNAL_PATH = Path("/root/.local/share/arifos/rollback_journal.jsonl")
SEALS_LEDGER_PATH = Path("/root/.local/share/arifos/seal_receipts.jsonl")
TURN_MEMORY_PATH = Path("/root/.local/share/arifos/turn_memory.json")

# Unconditional pass-through tools for 100_GATE (read/probe/bootstrap)
UNCONDITIONAL_PASS_TOOLS = {
    "arif_init",
    "read",
    "view_file",
    "glob",
    "grep",
    "grep_search",
    "find_by_name",
    "list_dir",
    "duckdb_describe",
    "duckdb_list_approved_datasets",
    "forge_probe",
    "forge_scan",
    "forge_status",
    "forge_registry_status",
    "read_url_content",
    "search_web",
    "list_resources",
    "read_resource",
    "manage_task",
}

# Forbidden / extreme-risk mutation targets (escalates to HOLD / VOID)
FORBIDDEN_MUTATION_TARGETS = [
    "/etc/shadow",
    "/etc/sudoers",
    "/root/.ssh/authorized_keys",
    "/root/.secrets/kunci-root.env",
]

# Anti-Tangguh permission seeking patterns (Digital = MUBAH / HITL OFF)
ANTI_TANGGUH_PATTERNS = [
    re.compile(r"\bshall i proceed\b", re.IGNORECASE),
    re.compile(r"\bwould you like me to\b", re.IGNORECASE),
    re.compile(r"\bdo you want me to\b", re.IGNORECASE),
    re.compile(r"\bshould i continue\b", re.IGNORECASE),
    re.compile(r"\bjalan\?", re.IGNORECASE),
    re.compile(r"\bready to proceed\?", re.IGNORECASE),
    re.compile(r"\bcan i run\b", re.IGNORECASE),
    re.compile(r"\bdo la\b", re.IGNORECASE),
]


class HookPhase(str, enum.Enum):
    BOOT = "000_BOOT"
    GATE = "100_GATE"
    HEAL = "200_HEAL"
    METABOLIZE = "300_METABOLIZE"
    SEAL = "999_SEAL"


class RestrictionLevel(enum.IntEnum):
    """Monotonic Restriction Ladder: A restriction can never be degraded downstream."""
    ALLOW = 0
    OBSERVE_ONLY = 1
    SABAR = 2
    HOLD = 3
    VOID = 4
    REVOKED = 5

    @classmethod
    def from_string(cls, val: str) -> "RestrictionLevel":
        name = val.strip().upper()
        if name in cls.__members__:
            return cls.__members__[name]
        return cls.ALLOW


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _kernel_tool_result(kernel_resp: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Unwrap a JSON-RPC tools/call response to the tool's own dict.

    MCP wraps tool output as result.content[0].text (a JSON string); some
    surfaces return the bare object. Returns None on error / no-verdict
    shapes so callers fall to the local failsafe.
    """
    if not isinstance(kernel_resp, dict):
        return None
    result = kernel_resp.get("result")
    if not isinstance(result, dict) or result.get("isError"):
        return None
    content = result.get("content")
    if isinstance(content, list) and content and isinstance(content[0], dict):
        text = content[0].get("text")
        if isinstance(text, str):
            try:
                parsed = json.loads(text)
                return parsed if isinstance(parsed, dict) else None
            except json.JSONDecodeError:
                return None
    if isinstance(result.get("verdict"), str):  # bare-object surfaces
        return result
    return None


def _ensure_dir(path: Path) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass


class FederationHookEngine:
    """Canonical Federation Hook Engine coordinating all 7 AAA harnesses."""

    def __init__(self, actor_id: str = "333-AGI", session_id: Optional[str] = None):
        self.actor_id = actor_id
        self.session_id = session_id or f"sess-{int(time.time())}-{uuid.uuid4().hex[:6]}"
        self.session_token: Optional[str] = None
        self.current_restriction: RestrictionLevel = RestrictionLevel.ALLOW
        self.turn_errors: List[Dict[str, Any]] = []
        self.active_scars: Dict[str, Dict[str, Any]] = {}
        self.rollback_entries: List[Dict[str, Any]] = []

    # =========================================================================
    # Phase 0: Session Ignition & Active Scar Priming (000_BOOT)
    # =========================================================================
    def boot(self, context_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Ignition hook:
        1. Calls arif_init on kernel (with strict Accept: application/json) or falls back.
        2. Binds session token.
        3. Extracts top scars and open loops.
        4. Generates Active Constraint Brief for agent context priming.
        """
        # Step 1: Kernel arif_init contact
        init_payload = {
            "action": "arif_init",
            "actor_id": self.actor_id,
            "session_id": self.session_id,
            "timestamp": _utc_iso(),
        }
        kernel_resp = self._call_kernel("/kernel/call", init_payload)
        if kernel_resp and "token" in kernel_resp:
            self.session_token = kernel_resp["token"]
            init_mode = "KERNEL_AUTHENTICATED"
        else:
            self.session_token = f"degraded-local-{self.actor_id}-{uuid.uuid4().hex[:8]}"
            init_mode = "DEGRADED_LOCAL_FALLBACK"
            self.is_degraded = True

        # Step 2: Query active scars & carry forward
        active_scars = self._load_recent_scars(limit=5)
        open_loops = self._load_open_loops(limit=5)

        # Step 3: Build Active Constraint Brief
        brief = [
            f"=== arifOS Active Constraint Brief [{self.session_id}] ===",
            f"Actor: {self.actor_id} | Init Mode: {init_mode}",
            "Core Law: F1 Amanah (Reversibility) | F2 Truth | F13 Sovereign Attention Preservation.",
            "Directive: Digital work is MUBAH / HITL OFF. Never ask Arif to run/paste terminal commands.",
            "Active Scars Loaded:",
        ]
        for s in active_scars:
            brief.append(f"  - [{s['name']}] {s['summary']}")
        if open_loops:
            brief.append("Prior Session Open Loops:")
            for op in open_loops:
                brief.append(f"  - ({op.get('id', 'LOOP')}) {op.get('description', '')}")
        brief.append("==========================================================")
        brief_text = "\n".join(brief)

        return {
            "phase": HookPhase.BOOT.value,
            "status": "OK",
            "session_id": self.session_id,
            "session_token": self.session_token,
            "session_identity": {
                "session_id": self.session_id,
                "source": "kernel" if init_mode == "KERNEL_AUTHENTICATED" else "local_hook_fallback",
                "authority_scope": "authenticated" if init_mode == "KERNEL_AUTHENTICATED" else "local_correlation_only",
            },
            "execution_authority": {
                "source": "aaa_kernel" if init_mode == "KERNEL_AUTHENTICATED" else "degraded_local_policy",
                "verdict": "kernel_authorized" if init_mode == "KERNEL_AUTHENTICATED" else "degraded_local_only",
                "allows_irreversible": init_mode == "KERNEL_AUTHENTICATED",
            },
            "init_mode": init_mode,
            "scars_count": len(active_scars),
            "open_loops_count": len(open_loops),
            "brief": brief_text,
        }

    # =========================================================================
    # Phase 1: Pre-Tool Advisory Enrichment (100_GATE)
    # =========================================================================
    def gate(
        self,
        tool_name: str,
        tool_args: Optional[Dict[str, Any]] = None,
        provided_token: Optional[str] = None,
        incoming_restriction: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Pre-tool ADVISORY enrichment (NOT a gate or BOP).
        Hooks enrich context — the kernel (arif_judge) is the judge.

        1. Detects forbidden targets → ADVISORY signal (not blocking verdict)
        2. Tracks monotonic restriction state → context for kernel
        3. Auto-mints ACT token if mutating tool lacks one
        4. Logs to rollback journal for audit trail
        5. Returns ALLOW always — harness/kernel decides whether to proceed
        """
        tool_args = tool_args or {}
        incoming_level = (
            RestrictionLevel.from_string(incoming_restriction)
            if incoming_restriction
            else self.current_restriction
        )
        # Track monotonicity (context only — hook doesn't block)
        if incoming_level > self.current_restriction:
            self.current_restriction = incoming_level

        # APEX ZEN: Restriction state is context, enforced if at VOID
        if self.current_restriction >= RestrictionLevel.VOID:
            return {
                "phase": HookPhase.GATE.value,
                "verdict": "VOID",
                "kernel_verdict": self.current_restriction.name,
                "verdict_source": "kernel_monotonicity",
                "hook_role": "sensor_and_transport",
                "execution_status": "NOT_EXECUTED",
                "consequence": f"ACTIVE_RESTRICTION_{self.current_restriction.name}_RECORDED",
                "restriction_level": self.current_restriction.name,
                "tool_name": tool_name,
                "reason": f"Active restriction {self.current_restriction.name} enforced.",
                "session_token": provided_token or self.session_token,
            }

        # 1. Detect forbidden targets (advisory enrichment, not blocking)
        normalized_paths = []
        for k, v in tool_args.items():
            if isinstance(v, str) and ("/" in v or ".." in v):
                try:
                    normalized_paths.append(os.path.normpath(v).lower())
                except Exception:
                    pass
        arg_str = json.dumps(tool_args).lower()

        security_warnings = []
        for forbidden in FORBIDDEN_MUTATION_TARGETS:
            f_lower = forbidden.lower()
            matched = False
            if f_lower in arg_str:
                matched = True
            for np in normalized_paths:
                if f_lower in np or np.startswith(f_lower) or np.endswith(f_lower.lstrip("/")):
                    matched = True
                    break
            if matched:
                security_warnings.append({
                    "target": forbidden,
                    "severity": "CRITICAL",
                    "advisory": f"Target matches forbidden pattern: {forbidden}. Kernel arif_judge must evaluate.",
                })

        if security_warnings:
            # SENSOR: Forward target to kernel arif_judge for adjudication.
            # (Bridge fix FI-008 2026-09-25: valid arif_judge kwargs only —
            #  target_path was rejected by pydantic validation; the target
            #  rides inside the candidate string.)
            kernel_resp = self._call_kernel("tools/call", {
                "name": "arif_judge",
                "arguments": {
                    "mode": "judge",
                    "candidate": f"SENSITIVE_PATH_TARGET: {security_warnings[0]['target']} in {tool_name} with args: {json.dumps(tool_args)}",
                    "session_id": self.session_id,
                    "session_token": provided_token or self.session_token,
                    "actor_id": self.actor_id,
                    "action_tier": "critical",
                    "reversibility_level": "R5",
                    "blast_radius": "critical",
                }
            })
            kernel_result = _kernel_tool_result(kernel_resp)
            kernel_verdict = (kernel_result or {}).get("verdict")
            if not kernel_verdict:
                # ENGINE-VERDICT-OVERREACH fix (FI-008, 2026-09-25): a hook may
                # never SPELL a kernel-only verdict. Kernel unreachable on an
                # enumerated fail-safe target => refuse fail-safe under a
                # hook-lawful HOLD + escalation receipt (separation_of_powers
                # hook_permitted_outcomes), never a synthesized VOID.
                self.current_restriction = max(self.current_restriction, RestrictionLevel.HOLD)
                return {
                    "phase": HookPhase.GATE.value,
                    "verdict": "HOLD",
                    "kernel_verdict": None,
                    "verdict_source": "local_hook_failsafe",
                    "hook_role": "sensor_and_transport",
                    "execution_status": "NOT_EXECUTED",
                    "consequence": "FAILSAFE_KERNEL_UNREACHABLE",
                    "restriction_level": self.current_restriction.name,
                    "tool_name": tool_name,
                    "security_warnings": security_warnings,
                    "reason": (
                        f"Enumerated fail-safe target {security_warnings[0]['target']} matched "
                        "and kernel arif_judge returned no verdict (unreachable or error) — "
                        "refused fail-safe, deferred to kernel."
                    ),
                    "escalation_required": True,
                    "escalation_target": "kernel_arif_judge",
                    "escalation_floor": "F1",
                    "escalation_route": "arif_judge_requeue_on_reachable",
                    "kernel_reachable": False,
                    "session_token": provided_token or self.session_token,
                }
            self.current_restriction = max(self.current_restriction, RestrictionLevel.VOID)
            return {
                "phase": HookPhase.GATE.value,
                "verdict": kernel_verdict,
                "kernel_verdict": kernel_verdict,
                "verdict_source": "kernel_arif_judge",
                "hook_role": "sensor_and_transport",
                "execution_status": "NOT_EXECUTED",
                "consequence": "PREVENTED_BY_KERNEL_VOID",
                "restriction_level": self.current_restriction.name,
                "tool_name": tool_name,
                "security_warnings": security_warnings,
                "reason": f"Access to forbidden target detected: {security_warnings[0]['target']}",
                "session_token": provided_token or self.session_token,
            }

        # 2. Auto-Mint Reflex: ensure token exists for mutating tools
        active_token = provided_token or self.session_token
        auto_minted = False
        if not active_token:
            active_token = f"act-minted-{self.actor_id}-{uuid.uuid4().hex[:8]}"
            self.session_token = active_token
            auto_minted = True

        # 3. Rollback Journaling
        journal_id = self._record_rollback_entry(tool_name, tool_args)

        # Digital work is MUBAH: hook enriches context, passes to execution membrane
        return {
            "phase": HookPhase.GATE.value,
            "verdict": "ALLOW",
            "verdict_source": "kernel_policy_mubah",
            "hook_role": "sensor_and_transport",
            "execution_status": "PROCEEDED",
            "consequence": "DISPATCHED_TO_RUNTIME",
            "restriction_level": self.current_restriction.name,
            "tool_name": tool_name,
            "session_token": active_token,
            "auto_minted": auto_minted,
            "journal_id": journal_id,
            "security_warnings": security_warnings,
            "reason": "CLEAR: action permitted under autonomous digital policy (MUBAH)",
        }

    # =========================================================================
    # Phase 2: Post-Execution Telemetry & Auto-Healing Reflex (200_HEAL)
    # =========================================================================
    def heal(
        self,
        tool_name: str,
        tool_args: Optional[Dict[str, Any]] = None,
        exit_code: int = 0,
        stdout: str = "",
        stderr: str = "",
        http_status: Optional[int] = None,
        error_message: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Post-tool outcome analyzer and auto-healing reflex:
        - HTTP 406: Content negotiation repair (inject Accept: application/json)
        - ModuleNotFound / Command not found: dependency diagnosis
        - Swap/Zombie exhaustion: diagnosis and cleanup recipe
        - Git detached HEAD / conflict: rebase/stash recipe
        """
        combined_err = f"{stderr} {error_message or ''} {stdout}".strip()
        healing_action = None
        auto_retry = False
        remediated = False

        # Pattern A: HTTP 406 Not Acceptable (Accept header missing)
        if http_status == 406 or "406" in combined_err or "not acceptable" in combined_err.lower():
            healing_action = {
                "type": "HTTP_406_CONTENT_NEGOTIATION",
                "diagnosis": "Endpoint rejected request because Accept header was missing or invalid.",
                "fix": "Enforce 'Accept: application/json' and 'Content-Type: application/json' on request headers.",
            }
            auto_retry = True
            remediated = True

        # Pattern B: ModuleNotFound / Command not found
        elif "command not found" in combined_err.lower() or "modulenotfounderror" in combined_err.lower():
            pkg_match = re.search(r"No module named ['\"]([^'\"]+)['\"]", combined_err)
            cmd_match = re.search(r"([a-zA-Z0-9_\-]+): command not found", combined_err)
            missing = pkg_match.group(1) if pkg_match else (cmd_match.group(1) if cmd_match else "unknown")
            healing_action = {
                "type": "DEPENDENCY_MISSING",
                "target": missing,
                "diagnosis": f"Required binary/module '{missing}' is missing from runtime path.",
                "fix": f"Auto-provision '{missing}' in isolated venv or fallback to sibling tool.",
            }
            remediated = True

        # Pattern C: Stale / Zombie Process Lock / Swap Starvation
        elif "out of memory" in combined_err.lower() or "no space left on device" in combined_err.lower() or "resource temporarily unavailable" in combined_err.lower():
            healing_action = {
                "type": "RESOURCE_EXHAUSTION",
                "diagnosis": "Host memory, swap, or PID limits exceeded due to stale background workers.",
                "fix": "Scan PID table for stale test/worker processes >24h and reclaim resources.",
            }
            remediated = True

        # Pattern D: Git detached / merge conflict
        elif "detached head" in combined_err.lower() or "non-fast-forward" in combined_err.lower() or "merge conflict" in combined_err.lower():
            healing_action = {
                "type": "GIT_BRANCH_DESYNC",
                "diagnosis": "Git worktree in detached state or remote rejected non-fast-forward update.",
                "fix": "Execute 'git stash && git pull --rebase origin main && git stash pop'.",
            }
            remediated = True

        # Calculate Delta Entropy (F4 clarity)
        delta_s = -0.1 if exit_code == 0 else 0.2

        receipt = {
            "phase": HookPhase.HEAL.value,
            "tool_name": tool_name,
            "exit_code": exit_code,
            "http_status": http_status,
            "delta_s": delta_s,
            "remediated": remediated,
            "auto_retry": auto_retry,
            "healing_action": healing_action,
            "timestamp": _utc_iso(),
        }

        # Track error in turn memory for scar formation
        if exit_code != 0 or http_status in (406, 500, 502, 503):
            self._record_turn_error(tool_name, combined_err[:200])

        return receipt

    # =========================================================================
    # Phase 3: Turn-Level Epistemic Metabolism (300_METABOLIZE)
    # =========================================================================
    def metabolize(self, assistant_text: str, turn_index: int = 1) -> Dict[str, Any]:
        """
        Turn-level reasoning and learning hook:
        1. Anti-Tangguh Sentry: flags permission-seeking questions on digital tasks.
        2. Autonomous Scar Forging: creates a scar artifact if identical error repeats >= 2 times.
        3. Updates turn telemetry.
        """
        # 1. Anti-Tangguh Sentry
        anti_tangguh_flagged = False
        matched_phrase = ""
        for pattern in ANTI_TANGGUH_PATTERNS:
            m = pattern.search(assistant_text)
            if m:
                anti_tangguh_flagged = True
                matched_phrase = m.group(0)
                break

        # 2. Autonomous Scar Crystallization check
        created_scar = self._check_and_crystallize_scar()

        result = {
            "phase": HookPhase.METABOLIZE.value,
            "turn_index": turn_index,
            "anti_tangguh_tripwire": anti_tangguh_flagged,
            "matched_phrase": matched_phrase,
            "new_scar_created": created_scar is not None,
            "created_scar": created_scar,
            "instruction": (
                "TRIPWIRE: Digital work is MUBAH / HITL OFF. Do not ask Arif for permission ('Shall I', 'Jalan?'). Execute silently and report verified receipts."
                if anti_tangguh_flagged
                else "CLEAR"
            ),
        }
        return result

    # =========================================================================
    # Phase 4: Session Closure & Mesh Propagation (999_SEAL)
    # =========================================================================
    def seal(
        self,
        verdict: str,
        completed_tasks: Optional[List[str]] = None,
        open_loops: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Closure hook:
        1. Appends record to carry_forward.json with flock.
        2. Logs seal receipt to ledger.
        3. Flushes verified entries in rollback journal.
        """
        completed_tasks = completed_tasks or []
        open_loops = open_loops or []

        # Step 1: Append to carry_forward.json
        carry_entry = {
            "session_id": self.session_id,
            "agent_id": self.actor_id,
            "closed_at": _utc_iso(),
            "verdict": verdict,
            "completed": completed_tasks,
            "open_loops": [{"id": f"loop-{uuid.uuid4().hex[:6]}", "desc": ol} for ol in open_loops],
        }
        self._append_carry_forward(carry_entry)

        # Step 2: Write seal receipt
        seal_record = {
            "seal_id": f"seal-{int(time.time())}-{uuid.uuid4().hex[:6]}",
            "session_id": self.session_id,
            "actor_id": self.actor_id,
            "verdict": verdict,
            "timestamp": _utc_iso(),
        }
        self._record_seal(seal_record)

        return {
            "phase": HookPhase.SEAL.value,
            "status": "SEALED",
            "session_id": self.session_id,
            "seal_id": seal_record["seal_id"],
            "completed_count": len(completed_tasks),
            "open_loops_count": len(open_loops),
        }

    # =========================================================================
    # Internal Helpers
    # =========================================================================
    def _call_kernel(self, endpoint: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """JSON-RPC call over the kernel MCP endpoint.

        Transport fix (FI-008, 2026-09-25): the kernel MCP surface lives at
        {base}/mcp and speaks JSON-RPC (method=tools/call, params={name,
        arguments}). The previous plain-POST to /tools/call never reached a
        route (404 -> None), so enumerated adjudication ALWAYS fell to the
        local failsafe — the kernel never actually judged. Envelope + 5s
        timeout (real arif_judge runs >1.5s) + isError passthrough.
        """
        base = KERNEL_URL.rstrip("/")
        url = base if base.endswith("/mcp") else f"{base}/mcp"
        envelope = {
            "jsonrpc": "2.0",
            "id": uuid.uuid4().hex[:8],
            "method": endpoint.lstrip("/"),
            "params": payload,
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(envelope).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",  # Mandatory to prevent HTTP 406
                "X-Actor-ID": self.actor_id,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                if resp.status in (200, 201):
                    return json.loads(resp.read().decode("utf-8"))
        except Exception:
            pass
        return None

    def _load_recent_scars(self, limit: int = 5) -> List[Dict[str, str]]:
        scars = []
        if not SCARS_DIR.exists():
            return scars
        try:
            files = sorted(SCARS_DIR.glob("*.md"), key=os.path.getmtime, reverse=True)
            for f in files[:limit]:
                content = f.read_text(encoding="utf-8", errors="ignore")
                first_line = content.splitlines()[0] if content.splitlines() else f.stem
                scars.append({"name": f.stem, "summary": first_line.lstrip("# \t")[:100]})
        except Exception:
            pass
        return scars

    def _load_open_loops(self, limit: int = 5) -> List[Dict[str, Any]]:
        if not CARRY_PATH.exists():
            return []
        try:
            with open(CARRY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                loops = data.get("open_loops", [])
                open_only = [l for l in loops if l.get("status") == "OPEN"]
                return open_only[:limit]
        except Exception:
            return []

    def _record_rollback_entry(self, tool_name: str, tool_args: Dict[str, Any]) -> str:
        _ensure_dir(ROLLBACK_JOURNAL_PATH)
        entry_id = f"rb-{uuid.uuid4().hex[:8]}"
        entry = {
            "id": entry_id,
            "session_id": self.session_id,
            "tool_name": tool_name,
            "args_hash": hashlib.sha256(json.dumps(tool_args, sort_keys=True).encode("utf-8")).hexdigest()[:16],
            "timestamp": _utc_iso(),
        }
        try:
            with open(ROLLBACK_JOURNAL_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass
        return entry_id

    def _record_turn_error(self, tool_name: str, error_snippet: str) -> None:
        err_entry = {
            "session_id": self.session_id,
            "tool": tool_name,
            "snippet": error_snippet,
            "time": time.time(),
        }
        self.turn_errors.append(err_entry)
        self.turn_errors = self.turn_errors[-20:]

        _ensure_dir(TURN_MEMORY_PATH)
        data = {"errors": []}
        try:
            if TURN_MEMORY_PATH.exists():
                with open(TURN_MEMORY_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
        except Exception:
            data = {"errors": []}

        data["errors"].append(err_entry)
        data["errors"] = data["errors"][-20:]
        try:
            with open(TURN_MEMORY_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            pass

    def _check_and_crystallize_scar(self) -> Optional[str]:
        """If same tool error repeats >= 2 times in turn memory, crystallize a scar."""
        errors = list(self.turn_errors)
        seen_keys = {(e.get("tool"), e.get("snippet"), int(e.get("time", 0))) for e in errors}
        if TURN_MEMORY_PATH.exists():
            try:
                with open(TURN_MEMORY_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for e in data.get("errors", []):
                        if self.session_id and e.get("session_id") == self.session_id:
                            k = (e.get("tool"), e.get("snippet"), int(e.get("time", 0)))
                            if k not in seen_keys:
                                seen_keys.add(k)
                                errors.append(e)
            except Exception:
                pass

        if len(errors) < 2:
            return None

        # Count frequencies of normalized snippets
        freq: Dict[str, List[Dict[str, Any]]] = {}
        for err in errors:
            norm = err.get("snippet", "")[:80].strip()
            if norm:
                freq.setdefault(norm, []).append(err)

        for snippet, occurrences in freq.items():
            if len(occurrences) >= 2:
                # Crystallize new scar
                tool = occurrences[0].get("tool", "tool")
                scar_id = f"SCAR-AUTO-{hashlib.md5(snippet.encode('utf-8')).hexdigest()[:8]}"
                if scar_id in self.active_scars:
                    return scar_id

                candidate_file = SCARS_DIR / "candidates" / f"{scar_id}.md"
                scar_content = f"""# {scar_id} — Recurring Tool Failure Candidate: {tool}

> **Autonomous Crystallization:** Forged turn-level by FederationHookEngine  
> **Candidate Status:** QUARANTINED (Requires canary verification before constitutional promotion)  
> **First Witnessed:** {_utc_iso()}  
> **Repeated Occurrences:** {len(occurrences)} within recent turn window

## 1. Witnessed Pattern
Tool `{tool}` triggered recurring errors:
```
{snippet}
```

## 2. Invariant & Remediation
- **F1 Amanah:** Do not retry identical failing arguments without parameter mutation.
- **F2 Truth:** Verify preconditions before invocation.
- **Remediation Reflex:** Apply auto-healing membrane before escalating to sovereign.
"""
                self.active_scars[scar_id] = {
                    "tool": tool,
                    "snippet": snippet,
                    "occurrences": len(occurrences),
                    "status": "CANDIDATE_QUARANTINE",
                }
                try:
                    _ensure_dir(candidate_file)
                    candidate_file.write_text(scar_content, encoding="utf-8")
                    return scar_id
                except Exception:
                    return f"VIRTUAL-{scar_id}"
        return None

    def _append_carry_forward(self, entry: Dict[str, Any]) -> None:
        _ensure_dir(CARRY_PATH)
        try:
            # Safe flock-protected write
            with open(CARRY_PATH, "a+", encoding="utf-8") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                try:
                    f.seek(0)
                    content = f.read().strip()
                    doc = json.loads(content) if content else {"schema": "arifos.carry_forward.v2", "sessions": []}
                    doc.setdefault("sessions", []).append(entry)
                    f.seek(0)
                    f.truncate()
                    json.dump(doc, f, indent=2)
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)
        except Exception:
            pass

    def _record_seal(self, seal_record: Dict[str, Any]) -> None:
        _ensure_dir(SEALS_LEDGER_PATH)
        try:
            with open(SEALS_LEDGER_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(seal_record) + "\n")
        except Exception:
            pass


# =============================================================================
# CLI Dispatcher Interface
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="Federation Hook Engine CLI")
    parser.add_argument("command", choices=["dispatch", "boot", "gate", "heal", "metabolize", "seal"])
    parser.add_argument("--actor", default="333-AGI", help="Actor ID (e.g. 333-AGI, FI-001)")
    parser.add_argument("--session-id", default=None, help="Session ID")
    parser.add_argument("--payload", default="{}", help="JSON payload for event")
    args = parser.parse_args()

    try:
        payload = json.loads(args.payload)
    except Exception:
        payload = {}

    engine = FederationHookEngine(actor_id=args.actor, session_id=args.session_id)

    if args.command in ("boot", "dispatch") and payload.get("event") in (None, "boot", "session_start"):
        res = engine.boot(payload)
    elif args.command == "gate" or payload.get("event") == "pre_tool":
        res = engine.gate(
            tool_name=payload.get("tool_name", "unknown"),
            tool_args=payload.get("tool_args", {}),
            provided_token=payload.get("session_token"),
            incoming_restriction=payload.get("restriction_level"),
        )
    elif args.command == "heal" or payload.get("event") == "post_tool":
        res = engine.heal(
            tool_name=payload.get("tool_name", "unknown"),
            tool_args=payload.get("tool_args", {}),
            exit_code=payload.get("exit_code", 0),
            stdout=payload.get("stdout", ""),
            stderr=payload.get("stderr", ""),
            http_status=payload.get("http_status"),
            error_message=payload.get("error_message"),
        )
    elif args.command == "metabolize" or payload.get("event") == "turn_end":
        res = engine.metabolize(
            assistant_text=payload.get("assistant_text", ""),
            turn_index=payload.get("turn_index", 1),
        )
    elif args.command == "seal" or payload.get("event") == "session_close":
        res = engine.seal(
            verdict=payload.get("verdict", "COMPLETED"),
            completed_tasks=payload.get("completed", []),
            open_loops=payload.get("open_loops", []),
        )
    else:
        res = {"error": f"Unknown command {args.command} or event {payload.get('event')}"}

    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
