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
IDENTITY_KEYS_DIR = Path(os.environ.get("ARIFOS_IDENTITY_KEYS", "/root/AAA/IDENTITY/keys"))
CARRY_PATH = Path("/root/.local/share/arifos/carry_forward.json")
SCARS_DIR = Path("/root/AAA/scars")
ROLLBACK_JOURNAL_PATH = Path("/root/.local/share/arifos/rollback_journal.jsonl")
SEALS_LEDGER_PATH = Path("/root/.local/share/arifos/seal_receipts.jsonl")
TURN_MEMORY_PATH = Path("/root/.local/share/arifos/turn_memory.json")

# ── Reality Link (2026-10-23, 333-AGI) ──────────────────────────────────────
# Every non-R0 action leaves an Execute receipt; a file mutation leaves a
# Verify receipt with pre/post sha256. Delivery is outbox-based (never block
# the tool on flow transport). Disable with ARIFOS_FLOW_LINK=0.
FLOW_URL = os.environ.get("ARIFOS_FLOW_URL", "http://127.0.0.1:7073")
FLOW_LINK_ENABLED = os.environ.get("ARIFOS_FLOW_LINK", "1") != "0"
FLOW_OUTBOX = Path(os.environ.get("ARIFOS_FLOW_OUTBOX", "/root/.local/share/arifos/flow_outbox.jsonl"))
FLOW_SENT = Path(os.environ.get("ARIFOS_FLOW_SENT", "/root/.local/share/arifos/flow_outbox.sent"))
HOOK_ACTIONS_DIR = Path(os.environ.get("ARIFOS_HOOK_ACTIONS_DIR", "/root/.local/share/arifos/hook_actions"))

# Mutating tool names (native + common adapter aliases). Everything not in
# UNCONDITIONAL_PASS_TOOLS and not a read-only prefix is treated conservatively.
MUTATE_TOOL_HINTS = {
    "bash", "shell", "write", "edit", "patch", "multi_edit", "multiedit",
    "replace_file_content", "create_file", "delete_file", "apply_patch",
    "write_to_file", "run_command", "execute_command", "terminal",
}
READONLY_PREFIXES = (
    "read", "get_", "list", "grep", "glob", "find", "search", "view",
    "probe", "status", "health", "describe",
)
R4_COMMAND_PATTERNS = (
    r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f?\s+/(?:\s|$)",
    r"\bmkfs(\.[a-z0-9]+)?\b",
    r"\bdd\s+[^\n]*of=/dev/",
    r"\b(shutdown|reboot|poweroff|halt)\b",
    r"\bdrop\s+(table|database|schema)\b",
    r"\btruncate\s+table\b",
    r"git\s+push\s+[^\n]*--force",
    r"\bchmod\s+777\s+/",
    r"\b(userdel|passwd|visudo)\b",
)
R3_COMMAND_PATTERNS = (
    r"\bsystemctl\s+(restart|stop|start|disable|enable|mask|unmask)\b",
    r"\bdocker\s+(rm|rmi|restart|stop|kill|prune)\b",
    r"\bcaddy\s+reload\b",
    r"\b(apt|apt-get|dnf|yum|apk)\s+(install|remove|purge|upgrade)\b",
    r"\bpip3?\s+install\b",
    r"\b(npm|pnpm|yarn)\s+install\s+-g\b",
    r"\bcrontab\b",
    r"(/etc/|/root/\.ssh/|/root/\.secrets/|/root/VAULT999|/root/arifOS/VAULT999)",
)

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
        self.is_degraded = False

    # =========================================================================
    # Phase 0: Session Ignition & Active Scar Priming (000_BOOT)
    # =========================================================================
    def _ed25519_bind(self) -> Optional[Tuple[str, str]]:
        """Challenge → sign → init. Returns (session_token, authority) or None.

        2026-10-18 (root-cause fix): boot previously called arif_init without a
        signature, so the kernel always returned an unverified session and the
        harness stayed DEGRADED_LOCAL_FALLBACK. The kernel supports a real
        Ed25519 bind: mode=challenge → sign result.signature_payload → mode=init
        with actor_signature + nonce. Fail-open: any error returns None and the
        caller falls back to the old plain-init path.
        """
        try:
            import base64

            from cryptography.hazmat.primitives import serialization

            key_path = IDENTITY_KEYS_DIR / f"{self.actor_id}_private.pem"
            if not key_path.is_file():
                return None

            ch_resp = self._call_kernel(
                "tools/call",
                {
                    "name": "arif_init",
                    "arguments": {
                        "mode": "challenge",
                        "actor_id": self.actor_id,
                        "intent": "hook boot identity bind",
                        "verbosity": "minimal",
                    },
                },
            )
            ch = _kernel_tool_result(ch_resp)
            inner = ch.get("result") if isinstance(ch, dict) else None
            if not isinstance(inner, dict):
                return None
            nonce = inner.get("nonce")
            payload = inner.get("signature_payload") or (f"{self.actor_id}:{nonce}" if nonce else None)
            if not nonce or not payload:
                return None

            private_key = serialization.load_pem_private_key(key_path.read_bytes(), password=None)
            signature = base64.b64encode(private_key.sign(str(payload).encode())).decode()

            init_resp = self._call_kernel(
                "tools/call",
                {
                    "name": "arif_init",
                    "arguments": {
                        "mode": "init",
                        "actor_id": self.actor_id,
                        "intent": "hook boot identity bind",
                        "actor_signature": signature,
                        "nonce": nonce,
                        "verbosity": "minimal",
                    },
                },
            )
            res = _kernel_tool_result(init_resp)
            if not isinstance(res, dict):
                return None
            actor = res.get("actor") or {}
            if actor.get("actor_verified") is not True:
                return None
            token = res.get("session_token") or res.get("sct")
            if not token:
                return None
            authority = str(
                res.get("authority_band") or actor.get("authority_level") or res.get("autonomy_band") or "UNKNOWN"
            )
            self.is_degraded = False
            return str(token), authority
        except Exception:
            return None

    def boot(
        self, context_info: Optional[Dict[str, Any]] = None, provided_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ignition hook:
        1. Binds a kernel session — three honest modes (patch 2026-10-15, F13 sah):
             HARNESS_TOKEN          — harness already did the Ed25519 challenge/init
                                      bind and passed its SCT (crypto-verified actor).
             KERNEL_INIT            — engine binds a real kernel session via plain
                                      arif_init over the working tools/call envelope
                                      (actor unverified; session real).
             DEGRADED_LOCAL_FALLBACK — kernel unreachable; local correlation only.
           (Old bug: boot POSTed method "/kernel/call", which the kernel MCP
           surface never had — every boot was permanently degraded even while
           the judge path worked. Live-proven 2026-10-15 audit.)
        2. Extracts top scars and open loops.
        3. Generates Active Constraint Brief for agent context priming.
        """
        # Step 1: Kernel bind
        if provided_token:
            self.session_token = provided_token
            init_mode = "HARNESS_TOKEN"
        else:
            bound = self._ed25519_bind()
            if bound:
                self.session_token, _authority = bound
                init_mode = "ED25519_BIND"
                kernel_resp = None
                kernel_result = None
            else:
                kernel_resp = self._call_kernel(
                    "tools/call",
                    {
                        "name": "arif_init",
                        "arguments": {
                            "mode": "init",
                            "actor_id": self.actor_id,
                            "session_id": self.session_id,
                            "verbosity": "minimal",
                        },
                    },
                )
                kernel_result = _kernel_tool_result(kernel_resp)
            tok = None
            if isinstance(kernel_result, dict):
                tok = kernel_result.get("session_token") or kernel_result.get("sct")
            if bound:
                pass
            elif tok:
                self.session_token = str(tok)
                init_mode = "KERNEL_INIT"
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
                "source": "kernel"
                if init_mode in ("HARNESS_TOKEN", "KERNEL_INIT", "ED25519_BIND")
                else "local_hook_fallback",
                "authority_scope": (
                    "authenticated"
                    if init_mode in ("HARNESS_TOKEN", "ED25519_BIND")
                    else "kernel_session_unverified"
                    if init_mode == "KERNEL_INIT"
                    else "local_correlation_only"
                ),
            },
            "execution_authority": {
                "source": "aaa_kernel"
                if init_mode in ("HARNESS_TOKEN", "KERNEL_INIT", "ED25519_BIND")
                else "degraded_local_policy",
                "verdict": (
                    "kernel_authorized"
                    if init_mode in ("HARNESS_TOKEN", "ED25519_BIND")
                    else "kernel_session_only"
                    if init_mode == "KERNEL_INIT"
                    else "degraded_local_only"
                ),
                # Irreversibility is decided by kernel/judge per action — never
                # declared wholesale at boot (honest authority envelope).
                "allows_irreversible": False,
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
            RestrictionLevel.from_string(incoming_restriction) if incoming_restriction else self.current_restriction
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

        # AT-002 (F13 sah 2026-10-15): scar consultation is mandatory and
        # PROVABLE before selection. Every gate receipt carries the consulted
        # set; candidate-signature matches change the enrichment (the AT-001
        # selection-delta seed: same signature, different guidance).
        scar_consult = self._consult_scars(tool_name, tool_args)

        # 1. Detect forbidden targets — EXACT path-target match (patch 4, F13
        #    sah 2026-10-15). The old substring scan over the whole args dump
        #    self-blocked any agent that so much as MENTIONED a forbidden path
        #    in prose (live-proven twice on 2026-10-15: an audit command and
        #    then the very patch fixing it were VOIDed by their own gate).
        #    Now only real targets adjudicate:
        #      a) argument values that ARE absolute paths (exact or child-of)
        #      b) write-redirect targets inside command strings (> >> tee)
        #    Known limit, documented: reads of forbidden files and exotic
        #    redirection are not matched here — kernel arif_judge remains the
        #    constitutional backstop for those classes.
        def _candidate_targets(args: Dict[str, Any]) -> List[str]:
            out: List[str] = []
            for v in args.values():
                if not isinstance(v, str):
                    continue
                if v.startswith("/"):
                    out.append(v)
                out.extend(m.strip("\"'") for m in re.findall(r"(?:>{1,2}\s*|tee\s+)(/\S+)", v))
            return out

        normalized_paths = []
        for p in _candidate_targets(tool_args):
            try:
                normalized_paths.append(os.path.normpath(p).lower())
            except Exception:
                pass

        security_warnings = []
        for forbidden in FORBIDDEN_MUTATION_TARGETS:
            f_lower = forbidden.lower()
            # A fail-safe class covers the exact path, its children, AND its
            # sibling dotted family. `/etc/sudoers.d/*` is a sibling of
            # `/etc/sudoers`, not a child — the old `f + "/"` test returned
            # False for `echo pwned >> /etc/sudoers.d/evil` (live-proven
            # 2026-10-20 by hook_mesh_check C9: ALLOW/PROCEEDED). Same family
            # logic covers shadow.bak, authorized_keys.old, kunci-root.env.bak.
            matched = any(
                np == f_lower or np.startswith(f_lower + "/") or np.startswith(f_lower + ".") for np in normalized_paths
            )
            if matched:
                security_warnings.append(
                    {
                        "target": forbidden,
                        "severity": "CRITICAL",
                        "advisory": f"Target matches forbidden pattern: {forbidden}. Kernel arif_judge must evaluate.",
                    }
                )

        if security_warnings:
            # SENSOR: Forward target to kernel arif_judge for adjudication.
            # (Bridge fix FI-008 2026-09-25: valid arif_judge kwargs only —
            #  target_path was rejected by pydantic validation; the target
            #  rides inside the candidate string.)
            kernel_resp = self._call_kernel(
                "tools/call",
                {
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
                    },
                },
            )
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
                    # AT-004 (F13 sah 2026-10-15): a constitutional HOLD carries
                    # owner / next_action / evidence_gap / expiry — no orphan
                    # HOLDs, no fossil HOLDs.
                    "owner": "arifos-kernel (arif_judge requeue)",
                    "next_action": "re-queue arif_judge adjudication for the matched target once kernel is reachable; do not retry the tool meanwhile",
                    "evidence_gap": f"kernel verdict for {security_warnings[0]['target']} (kernel returned no verdict)",
                    "expiry": datetime.fromtimestamp(time.time() + 900, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
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

        # 2. Auto-Mint Reflex: ensure a CORRELATION token exists for mutating tools.
        #    NOTE (333-AGI 2026-10-20): this string is NOT a kernel-issued ACT.
        #    It is minted by THIS process for correlation only and grants no
        #    authority — the previous `act-minted-` prefix read as a real
        #    credential and was an authority-envelope lookalike. Renamed so the
        #    name shows what it is (F12 authority smuggling / ACAH2 LAW 1).
        active_token = provided_token or self.session_token
        auto_minted = False
        if not active_token:
            active_token = f"local-corr-{self.actor_id}-{uuid.uuid4().hex[:8]}"
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
            "scar_consulted": scar_consult["scar_consulted"],
            "scars_in_context": scar_consult["scars_in_context"],
            "scar_matches": scar_consult["scar_matches"],
            "scar_guidance": scar_consult["scar_guidance"],
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
        elif (
            "out of memory" in combined_err.lower()
            or "no space left on device" in combined_err.lower()
            or "resource temporarily unavailable" in combined_err.lower()
        ):
            healing_action = {
                "type": "RESOURCE_EXHAUSTION",
                "diagnosis": "Host memory, swap, or PID limits exceeded due to stale background workers.",
                "fix": "Scan PID table for stale test/worker processes >24h and reclaim resources.",
            }
            remediated = True

        # Pattern D: Git detached / merge conflict
        elif (
            "detached head" in combined_err.lower()
            or "non-fast-forward" in combined_err.lower()
            or "merge conflict" in combined_err.lower()
        ):
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
    # =========================================================================
    # Reality Link — flow receipts + consequence witness (2026-10-23)
    # =========================================================================
    # Doctrine: the hook NEVER blocks. It labels risk, records pre-state, and
    # transmits evidence to arifFlow. Enforcement stays with the kernel and the
    # harness boundary (F13 2026-09-14: "a hook is not a stopper gate").

    def _flow_enabled(self) -> bool:
        return FLOW_LINK_ENABLED

    def _action_id(self, payload: Dict[str, Any], tool_name: str, target: str) -> str:
        cid = payload.get("call_id") or payload.get("action_id") or payload.get("tool_call_id")
        if isinstance(cid, str) and cid.strip():
            return cid.strip()
        seed = f"{self.actor_id}|{self.session_id}|{tool_name}|{target}|{int(time.time() // 60)}"
        return "act-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20]

    def _risk_class(self, tool_name: str, tool_args: Dict[str, Any]) -> str:
        """R0..R4 label. Advisory only — do not use to block here."""
        name = (tool_name or "").lower()
        if name in UNCONDITIONAL_PASS_TOOLS or name.startswith(READONLY_PREFIXES):
            return "R0"
        # Match raw string arg values (JSON encoding wraps commands in quotes,
        # which breaks end-anchored patterns like "/(?:\s|$)").
        _texts = [v for v in (tool_args or {}).values() if isinstance(v, str)]
        blob = "\n".join(_texts) if _texts else json.dumps(tool_args or {}, ensure_ascii=False, sort_keys=True)
        if re.search("|".join(R4_COMMAND_PATTERNS), blob, re.IGNORECASE):
            return "R4"
        if re.search("|".join(R3_COMMAND_PATTERNS), blob, re.IGNORECASE):
            return "R3"
        if name in MUTATE_TOOL_HINTS or any(k in blob for k in ("command", "cmd")):
            return "R2" if name in ("bash", "shell", "run_command", "execute_command", "terminal") else "R1"
        return "R2"

    def _file_target(self, tool_name: str, tool_args: Dict[str, Any]) -> Optional[str]:
        name = (tool_name or "").lower()
        if name not in MUTATE_TOOL_HINTS and name not in ("write", "edit", "patch", "multi_edit", "replace_file_content", "create_file", "write_to_file"):
            return None
        for key in ("path", "filePath", "file_path", "TargetFile", "target_file", "filename"):
            val = (tool_args or {}).get(key)
            if isinstance(val, str) and val.startswith("/"):
                return val
        return None

    @staticmethod
    def _file_state(path: Optional[str]) -> Dict[str, Any]:
        if not path:
            return {"exists": False, "sha256": None, "size": None}
        try:
            with open(path, "rb") as f:
                data = f.read()
            return {"exists": True, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
        except FileNotFoundError:
            return {"exists": False, "sha256": None, "size": None}
        except Exception:
            return {"exists": None, "sha256": None, "size": None}

    def _pending_path(self, action_id: str) -> Path:
        return HOOK_ACTIONS_DIR / f"{action_id}.json"

    def _record_pending(self, action_id: str, record: Dict[str, Any]) -> None:
        try:
            _ensure_dir(self._pending_path(action_id))
            with open(self._pending_path(action_id), "w", encoding="utf-8") as f:
                json.dump(record, f, ensure_ascii=False)
        except Exception:
            pass

    def _load_pending(self, payload: Dict[str, Any], tool_name: str) -> Optional[Dict[str, Any]]:
        try:
            aid = payload.get("call_id") or payload.get("action_id")
            if aid:
                p = self._pending_path(str(aid))
                if p.exists():
                    return json.loads(p.read_text(encoding="utf-8"))
            # Fallback: newest pending for this actor/session/tool within 10 min.
            if not HOOK_ACTIONS_DIR.exists():
                return None
            best = None
            best_m = 0.0
            auto_sess = not self.session_id or self.session_id.startswith("sess-")
            for f in HOOK_ACTIONS_DIR.glob("*.json"):
                m = f.stat().st_mtime
                if time.time() - m > 600 or m < best_m:
                    continue
                try:
                    rec = json.loads(f.read_text(encoding="utf-8"))
                except Exception:
                    continue
                if rec.get("actor") == self.actor_id and rec.get("tool") == tool_name:
                    if rec.get("session") == self.session_id or auto_sess:
                        best, best_m = rec, m
            return best
        except Exception:
            return None

    def _flow_post(self, route: str, body: Dict[str, Any], timeout: float = 0.4) -> Optional[Dict[str, Any]]:
        try:
            req = urllib.request.Request(
                FLOW_URL.rstrip("/") + route,
                data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status in (200, 201, 202):
                    raw = resp.read().decode("utf-8", errors="replace")
                    return json.loads(raw) if raw.strip() else {}
        except Exception:
            return None
        return None

    def _flow_emit(self, receipt: Dict[str, Any]) -> Optional[str]:
        """Append to the outbox. Returns receipt_id. Never raises."""
        if not self._flow_enabled():
            return None
        try:
            _ensure_dir(FLOW_OUTBOX)
            with open(FLOW_OUTBOX, "a", encoding="utf-8") as f:
                f.write(json.dumps(receipt, ensure_ascii=False) + "\n")
            return receipt.get("receipt_id")
        except Exception:
            return None

    def _flow_drain(self, max_items: int = 5) -> None:
        """Best-effort outbox → /ingest. Serialized by flock, deduped by sent ledger.

        Concurrency defect observed 2026-10-23: 8 parallel tool calls started 8
        drains; each read the sent ledger before the others wrote, delivering 6
        receipts twice. LOCK_NB + re-read under lock closes that race.
        """
        if not self._flow_enabled() or not FLOW_OUTBOX.exists():
            return
        lock_fd = None
        try:
            _ensure_dir(FLOW_SENT)
            lock_fd = open(str(FLOW_SENT) + ".lock", "a+")
            try:
                fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                return  # another drain owns the outbox
            sent: set[str] = set()
            if FLOW_SENT.exists():
                sent = {ln.strip() for ln in FLOW_SENT.read_text(encoding="utf-8").splitlines() if ln.strip()}
            lines = FLOW_OUTBOX.read_text(encoding="utf-8", errors="replace").splitlines()
            delivered = 0
            for line in lines:
                if delivered >= max_items:
                    break
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                rid = rec.get("receipt_id")
                if not rid or rid in sent:
                    continue
                if self._flow_post("/ingest", rec) is not None:
                    with open(FLOW_SENT, "a", encoding="utf-8") as f:
                        f.write(rid + "\n")
                    sent.add(rid)
                    delivered += 1
        except Exception:
            pass
        finally:
            if lock_fd is not None:
                try:
                    fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)
                    lock_fd.close()
                except Exception:
                    pass

    def _flow_receipt(
        self,
        step_type: str,
        risk_class: str,
        summary: str,
        payload: Dict[str, Any],
        floor_verdict: str = "Pass",
        epistemic: str = "Observation",
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        risk_map = {"R0": "T0Observe", "R1": "T1Mutate", "R2": "T1Mutate", "R3": "T2Deploy", "R4": "T3Irreversible"}
        return {
            "receipt_id": str(uuid.uuid4()),
            "previous_receipt_hash": None,
            "created_at": _utc_iso(),
            # Attribution: the harness passes its bound crypto actor in identity.
            # Using the harness label ("opencode") would shard FQ away from 333-AGI.
            "actor_id": (
                (payload.get("identity") or {}).get("crypto_actor")
                if isinstance(payload.get("identity"), dict)
                else None
            ) or self.actor_id,
            "session_id": self.session_id or "session-unattributed",
            "session_token": None,
            "step_type": step_type,
            "risk_class": risk_map.get(risk_class, "T1Mutate"),
            "topology_id": None,
            "lane_id": None,
            "step_number": 0,
            "cost_ns": 0,
            "preceding_verify_cost_ns": None,
            "epistemic_label": epistemic,
            "floor_verdict": floor_verdict,
            "cooling_decision": "None",
            "tri_witness_votes": None,
            "merkle_root": None,
            "merkle_inclusion_proof": None,
            "payload": {
                "engine": "federation_hook_engine",
                "source": "arif-core/reality-link",
                **(details or {}),
            },
            "summary": summary[:500],
        }

    def flow_after_gate(self, res: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        """Attach action identity, risk label, pre-state and Execute receipt."""
        if not self._flow_enabled():
            return res
        try:
            tool_name = payload.get("tool_name", "unknown")
            tool_args = payload.get("tool_args") or {}
            target = self._file_target(tool_name, tool_args) or payload.get("target") or ""
            risk = self._risk_class(tool_name, tool_args)
            action_id = self._action_id(payload, tool_name, target)
            pre = self._file_state(target) if target else {"exists": None, "sha256": None, "size": None}

            if risk != "R0" and res.get("verdict") not in ("VOID", "HOLD") and res.get("execution_status") != "NOT_EXECUTED":
                self._record_pending(action_id, {
                    "action_id": action_id, "actor": self.actor_id, "session": self.session_id,
                    "tool": tool_name, "target": target, "risk": risk,
                    "pre": pre, "ts": _utc_iso(),
                })
                receipt = self._flow_receipt(
                    "Execute", risk, f"{tool_name} {('-> ' + target) if target else ''}".strip(),
                    payload,
                    floor_verdict="Pass",
                    details={
                        "action_id": action_id, "tool": tool_name, "target": target,
                        "pre_exists": pre.get("exists"), "pre_sha256": pre.get("sha256"),
                        "hook_verdict": res.get("verdict"), "verdict_source": res.get("verdict_source"),
                    },
                )
                rid = self._flow_emit(receipt)
                res["action_id"] = action_id
                res["risk_class"] = risk
                res["flow_receipt_id"] = rid
                # Advisory FQ context for elevated risk (never blocking).
                if risk in ("R3", "R4"):
                    chk = self._flow_post("/check", {"actor_id": self.actor_id})
                    res["flow_actor_allowed"] = (chk or {}).get("allowed")
                    res["flow_check_note"] = "advisory context only — hook does not block"
                self._flow_drain(max_items=2)
            elif risk != "R0":
                res["action_id"] = action_id
                res["risk_class"] = risk
        except Exception as exc:
            res["flow_link_error"] = str(exc)[:200]
        return res

    def flow_after_heal(self, res: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        """Post-state witness → Verify receipt (VERIFIED_CHANGE / NO_CHANGE / FAILED)."""
        if not self._flow_enabled():
            return res
        try:
            tool_name = payload.get("tool_name", "unknown")
            tool_args = payload.get("tool_args") or {}
            pending = self._load_pending(payload, tool_name)
            if pending and pending.get("session") and (not self.session_id or self.session_id.startswith("sess-")):
                self.session_id = str(pending["session"])
            target = (pending or {}).get("target") or self._file_target(tool_name, tool_args) or ""
            pre = (pending or {}).get("pre") or {"exists": None, "sha256": None}
            post = self._file_state(target) if target else {"exists": None, "sha256": None}
            exit_code = int(payload.get("exit_code", 0) or 0)

            consequence = "NO_TARGET"
            floor = "Pass"
            if target and pre.get("sha256") is not None or (target and pre.get("exists") is False):
                if exit_code != 0:
                    consequence, floor = "FAILED", "Caution"
                elif post.get("sha256") != pre.get("sha256") or (post.get("exists") and not pre.get("exists")):
                    consequence, floor = "VERIFIED_CHANGE", "Pass"
                else:
                    consequence, floor = "NO_CHANGE", "Caution"
            elif exit_code != 0:
                consequence, floor = "FAILED", "Caution"
            elif target and pre.get("sha256") is None and pre.get("exists") is None:
                # Heal-only harness (no gate pending): pre-state is unknown, but
                # the postcondition (target exists + hash) is still observed.
                consequence = "POST_STATE_OBSERVED" if post.get("exists") else "TARGET_MISSING"
                floor = "Pass" if post.get("exists") else "Caution"
            elif not target:
                # No file target, but the exit code is a mechanical postcondition.
                consequence, floor = "VERIFIED_EXIT", "Pass"

            risk = (pending or {}).get("risk") or self._risk_class(tool_name, tool_args)
            action_id = (pending or {}).get("action_id") or self._action_id(payload, tool_name, target)
            receipt = self._flow_receipt(
                "Verify", risk, f"verify {tool_name} {consequence}",
                payload, floor_verdict=floor, epistemic="Observation",
                details={
                    "action_id": action_id, "tool": tool_name, "target": target,
                    "pre_exists": pre.get("exists"), "pre_sha256": pre.get("sha256"),
                    "post_exists": post.get("exists"), "post_sha256": post.get("sha256"),
                    "consequence": consequence, "exit_code": exit_code,
                    "witness": "host_file_probe" if target else "exit_code",
                },
            )
            rid = self._flow_emit(receipt)
            if pending and pending.get("action_id"):
                try:
                    self._pending_path(str(pending["action_id"])).unlink(missing_ok=True)
                except Exception:
                    pass
            res["consequence"] = consequence
            res["action_id"] = action_id
            res["flow_verify_receipt_id"] = rid
            self._flow_drain(max_items=5)
        except Exception as exc:
            res["flow_link_error"] = str(exc)[:200]
        return res

    def flow_after_seal(self, res: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self._flow_enabled():
            return res
        try:
            receipt = self._flow_receipt(
                "Seal", "R1", f"session seal {res.get('seal_id', '')}",
                payload, floor_verdict="Pass", epistemic="Seal",
                details={"seal_id": res.get("seal_id"), "verdict": payload.get("verdict", "COMPLETED")},
            )
            rid = self._flow_emit(receipt)
            res["flow_seal_receipt_id"] = rid
            self._flow_drain(max_items=10)
        except Exception as exc:
            res["flow_link_error"] = str(exc)[:200]
        return res

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

    def _load_scar_candidates(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Autonomous crystallization queue (300_METABOLIZE output).

        Patch 2026-10-15 (F13 sah): candidates were written but NEVER read
        back — the quarantine had no visibility to selection. They are now
        consulted at gate time (still quarantined: they enrich guidance,
        they never block; promotion to canonical scar stays a human/kernel
        ritual).
        """
        out: List[Dict[str, Any]] = []
        cdir = SCARS_DIR / "candidates"
        if not cdir.exists():
            return out
        try:
            files = sorted(cdir.glob("*.md"), key=os.path.getmtime, reverse=True)
            for f in files[:limit]:
                content = f.read_text(encoding="utf-8", errors="ignore")
                tool_m = re.search(r"^Tool `([^`]+)`", content, re.M)
                rem_m = re.search(r"\*\*Remediation Reflex:\*\*\s*(.+)", content)
                out.append(
                    {
                        "scar_id": f.stem,
                        "tool": tool_m.group(1) if tool_m else None,
                        "remediation": rem_m.group(1).strip()[:200] if rem_m else None,
                        "first_seen": None,
                    }
                )
        except Exception:
            pass
        return out

    def _consult_scars(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """AT-002: prove scars were consulted before selection (receipt field),
        and let matching candidate signatures change the enrichment (AT-001
        seed: same signature -> different guidance -> observable delta)."""
        names: List[str] = []
        matches: List[Dict[str, Any]] = []
        for s in self._load_recent_scars(limit=5):
            names.append(s["name"])
        for c in self._load_scar_candidates(limit=10):
            names.append(c["scar_id"])
            if c.get("tool") and c["tool"] == tool_name:
                matches.append(
                    {
                        "scar_id": c["scar_id"],
                        "tool": c["tool"],
                        "remediation": c.get("remediation"),
                        "binding": "enrichment_only_quarantined",
                    }
                )
        guidance = None
        if matches:
            guidance = (
                f"SCAR MATCH on tool '{tool_name}': prior failure signature present "
                f"({len(matches)} candidate scar(s)). Apply known remediation before/instead of "
                f"the identical failing invocation: "
                + "; ".join(m.get("remediation") or "consult scar file" for m in matches)
            )
        return {
            "scar_consulted": True,
            "scars_in_context": names,
            "scar_matches": matches,
            "scar_guidance": guidance,
        }

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
        res = engine.boot(payload, provided_token=payload.get("session_token"))
    elif args.command == "gate" or payload.get("event") == "pre_tool":
        res = engine.gate(
            tool_name=payload.get("tool_name", "unknown"),
            tool_args=payload.get("tool_args", {}),
            provided_token=payload.get("session_token"),
            incoming_restriction=payload.get("restriction_level"),
        )
        res = engine.flow_after_gate(res, payload)
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
        res = engine.flow_after_heal(res, payload)
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
        res = engine.flow_after_seal(res, payload)
    else:
        res = {"error": f"Unknown command {args.command} or event {payload.get('event')}"}

    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
