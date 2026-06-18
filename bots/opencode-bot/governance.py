"""
governance.py — Constitutional governance manager for opencode-bot.
Owner: arif

Orchestrates:
  - 4-organ federation MCP surface (via mcp_client)
  - 12 constitutional hooks (via HookRunner)
  - 8-class action taxonomy + 333 FORGE cycle
  - WELL substrate gate
  - 888_JUDGE deliberation
  - VAULT999 stop-seal
  - NATS federation memory events
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import socket
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from substrate_gate import GateHandler, probe_well_substrate
from mcp_client import FederationMCPClient
from action_taxonomy import ActionVerdict, classify, ActionClass
import sovereign_auth

log = logging.getLogger("opencode-bot.governance")

WORKSPACE = Path(__file__).resolve().parent
HOOKS_DIR = WORKSPACE / "hooks"


class HookRunner:
    """Run a constitutional hook script with JSON input via stdin."""

    def __init__(self, hooks_dir: Path = HOOKS_DIR):
        self.hooks_dir = hooks_dir

    async def run(self, name: str, event: dict[str, Any]) -> dict[str, Any]:
        script = self.hooks_dir / f"opencode-{name}.py"
        if not script.exists():
            log.warning(f"Hook script missing: {script}")
            return {"_missing": True, "permissionDecision": "allow"}
        try:
            proc = await asyncio.create_subprocess_exec(
                "python3",
                str(script),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate(json.dumps(event).encode("utf-8"))
            # Human-guard / backup / format emit plain text on stderr/stdout
            if stderr:
                for line in stderr.decode("utf-8", errors="replace").strip().splitlines():
                    if line.strip():
                        log.info(f"[{name}] {line.strip()}")
            if proc.returncode == 2:
                try:
                    return json.loads(stdout.decode("utf-8", errors="replace"))
                except Exception:
                    return {
                        "hookSpecificOutput": {
                            "hookEventName": event.get("hook_event_name", "PreToolUse"),
                            "permissionDecision": "deny",
                            "permissionDecisionReason": stdout.decode("utf-8", errors="replace").strip()
                            or f"{name} denied",
                        }
                    }
            try:
                return json.loads(stdout.decode("utf-8", errors="replace"))
            except Exception:
                return {
                    "hookSpecificOutput": {
                        "hookEventName": event.get("hook_event_name", "PreToolUse"),
                        "permissionDecision": "allow",
                        "permissionDecisionReason": f"[{name}] no-json stdout: {stdout.decode('utf-8', errors='replace')[:200]}",
                    }
                }
        except Exception as exc:
            log.warning(f"Hook {name} failed: {exc}")
            return {
                "hookSpecificOutput": {
                    "hookEventName": event.get("hook_event_name", "PreToolUse"),
                    "permissionDecision": "allow",
                    "permissionDecisionReason": f"[{name}] hook runtime error: {exc}",
                }
            }


class Governor:
    """High-level governance facade for the bot."""

    def __init__(
        self,
        mcp_client: Optional[FederationMCPClient] = None,
        gate_handler: Optional[GateHandler] = None,
        hook_runner: Optional[HookRunner] = None,
        workspace: Path = WORKSPACE,
    ):
        self.mcp = mcp_client or FederationMCPClient()
        self.gate = gate_handler or GateHandler()
        self.hooks = hook_runner or HookRunner()
        self.workspace = workspace
        self._verified_arifos_session: Optional[str] = None

    # ──────────────────────────────────────────────────────────────────────
    # Session lifecycle
    # ──────────────────────────────────────────────────────────────────────

    async def session_start(self, session_id: str, source: str = "startup") -> dict[str, Any]:
        return await self.hooks.run(
            "session-start",
            {
                "session_id": session_id,
                "source": source,
                "cwd": str(self.workspace),
                "hook_event_name": "SessionStart",
            },
        )

    # ──────────────────────────────────────────────────────────────────────
    # Tool-use governance (PRE/POST)
    # ──────────────────────────────────────────────────────────────────────

    async def pre_govern(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
        session_id: str,
        cwd: str = "/root",
    ) -> tuple[bool, str, dict[str, Any]]:
        """
        Run the full PRE gate on a tool invocation.
        Returns (allowed, reason, metadata).
        """
        base_event = {
            "tool_name": tool_name,
            "tool_input": tool_input,
            "cwd": cwd,
            "session_id": session_id,
            "hook_event_name": "PreToolUse",
        }

        # Hard human guard first
        guard = await self.hooks.run("human-guard-hard", base_event)
        guard_out = guard.get("hookSpecificOutput", {})
        if guard_out.get("permissionDecision") == "deny":
            return False, guard_out.get("permissionDecisionReason", "Human guard denied"), guard_out.get("metadata", {})

        # Pre-govern risk gate
        pre = await self.hooks.run("pre-govern", base_event)
        pre_out = pre.get("hookSpecificOutput", {})
        if pre_out.get("permissionDecision") == "deny":
            return False, pre_out.get("permissionDecisionReason", "Pre-govern denied"), pre_out.get("metadata", {})

        # Backup before file edits
        if tool_name in ("WriteFile", "StrReplaceFile"):
            await self.hooks.run("human-backup", base_event)

        # Thermodynamic pre-check (advisory)
        thermo = await self.hooks.run("thermo-pre", base_event)
        thermo_out = thermo.get("hookSpecificOutput", {})
        meta = {
            "pre_govern": pre_out.get("metadata", {}),
            "thermo_pre": thermo_out.get("metadata", {}),
        }
        reason = f"PRE gates passed. {thermo_out.get('permissionDecisionReason', '')}"
        return True, reason, meta

    async def post_witness(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
        tool_output: dict[str, Any],
        session_id: str,
        cwd: str = "/root",
    ) -> dict[str, Any]:
        base_event = {
            "tool_name": tool_name,
            "tool_input": tool_input,
            "tool_output": tool_output,
            "cwd": cwd,
            "session_id": session_id,
            "hook_event_name": "PostToolUse",
        }
        witness = await self.hooks.run("post-witness", base_event)
        thermo = await self.hooks.run("thermo-post", base_event)
        if tool_name in ("WriteFile", "StrReplaceFile"):
            await self.hooks.run("human-format", base_event)
        return {
            "witness": witness.get("hookSpecificOutput", {}),
            "thermo_post": thermo.get("hookSpecificOutput", {}),
        }

    # ──────────────────────────────────────────────────────────────────────
    # Federation organ helpers
    # ──────────────────────────────────────────────────────────────────────

    async def well_substrate(self) -> dict[str, Any]:
        """Probe WELL for current substrate state."""
        resp = await self.mcp.call_tool(
            "well",
            "well_assess_homeostasis",
            {"mode": "fatigue"},
        )
        if not resp or "result" not in resp:
            return {"source": "no_probe"}
        try:
            content = json.loads(resp["result"].get("content", [{}])[0].get("text", "{}"))
        except Exception:
            return {"source": "no_probe_parse"}
        return content

    async def ensure_arifos_verified_session(self) -> Optional[str]:
        """Mint or reuse a verified arifOS session (Ed25519 challenge-response)."""
        if self._verified_arifos_session:
            return self._verified_arifos_session
        sid = await self.mcp.initialize("arifos")
        if not sid:
            return None
        actor_id = "arif"
        challenge_resp = await self.mcp.call_tool(
            "arifos",
            "arif_session_init",
            {"mode": "challenge", "actor_id": actor_id},
            session_id=sid,
            auto_init=False,
        )
        if not challenge_resp or "result" not in challenge_resp:
            return None
        nonce = challenge_resp["result"].get("nonce")
        if not nonce:
            return None
        sig = sovereign_auth.sign_actor_challenge(actor_id, nonce)
        if not sig:
            log.warning("ensure_arifos_verified_session: cannot sign challenge")
            return None
        init_resp = await self.mcp.call_tool(
            "arifos",
            "arif_session_init",
            {"mode": "init", "actor_id": actor_id, "nonce": nonce, "signature": sig},
            session_id=sid,
            auto_init=False,
        )
        if not init_resp or "result" not in init_resp:
            return None
        result = init_resp["result"]
        actor = result.get("actor", {})
        if not actor.get("identity_verified"):
            log.warning("ensure_arifos_verified_session: identity not verified")
            return None
        forge_session_id = result.get("session_id") or result.get("session", {}).get("session_id")
        if not forge_session_id and isinstance(result.get("session_state"), dict):
            forge_session_id = result["session_state"].get("session_id")
        self._verified_arifos_session = forge_session_id
        log.info(f"Verified arifOS session: {forge_session_id}")
        return forge_session_id

    async def judge(self, prompt: str) -> tuple[str, str, Optional[dict[str, Any]]]:
        """
        Call 888_JUDGE on a prompt.
        Returns (verdict, reason, raw_result_or_none).
        """
        session_id = await self.ensure_arifos_verified_session()
        if not session_id:
            return "JUDGE_UNAVAILABLE", "Cannot mint verified arifOS session", None
        resp = await self.mcp.call_tool(
            "arifos",
            "arif_judge_deliberate",
            {
                "mode": "judge",
                "candidate": prompt,
                "session_id": session_id,
                "actor_id": "arif",
                "claimed_evidence_level": "verified",
            },
            auto_init=False,
        )
        if not resp or "result" not in resp:
            return "JUDGE_UNAVAILABLE", "arif_judge_deliberate returned no result", resp
        if "error" in resp:
            err = resp["error"]
            return "JUDGE_UNAVAILABLE", f"{err.get('code', '?')} {err.get('message', '?')}", resp
        result = resp["result"]
        structured = result.get("structuredContent") or {}
        verdict = structured.get("verdict") or result.get("verdict") or "UNKNOWN"
        inner = structured.get("result") or {}
        reason = (
            inner.get("reason")
            or structured.get("reason")
            or result.get("reason")
            or result.get("reasons")
            or ""
        )
        if isinstance(reason, list):
            reason = "; ".join(str(r) for r in reason)
        if not reason:
            for part in result.get("content", []):
                if isinstance(part, dict) and part.get("type") == "text" and part.get("text"):
                    reason = part["text"]
                    break
        return str(verdict), str(reason), resp

    # ──────────────────────────────────────────────────────────────────────
    # Action classification + substrate gate for /forge
    # ──────────────────────────────────────────────────────────────────────

    def classify_prompt(self, prompt: str) -> ActionVerdict:
        return classify(prompt)

    async def substrate_gate_decision(
        self, action_type: str, decision_class: str
    ) -> tuple[bool, str, Optional[dict[str, Any]]]:
        """Run the WELL substrate gate. Returns (hold, reason, decision)."""
        substrate = await probe_well_substrate()
        decision = await self.gate.evaluate(action_type, decision_class, substrate=substrate)
        if decision.hold:
            return True, decision.message or decision.reason, decision
        return False, decision.reason, decision

    # ──────────────────────────────────────────────────────────────────────
    # VAULT999 + NATS + stop seal
    # ──────────────────────────────────────────────────────────────────────

    async def stop_seal(self, session_id: str) -> dict[str, Any]:
        """Run stop-seal hook, write to VAULT999, publish NATS, write summary."""
        event = {
            "session_id": session_id,
            "cwd": str(self.workspace),
            "hook_event_name": "Stop",
            "stop_hook_active": False,
        }
        seal = await self.hooks.run("stop-seal", event)
        seal_out = seal.get("hookSpecificOutput", {})
        meta = seal_out.get("metadata", {})

        # Attempt VAULT999 seal via arifOS MCP
        vault_ok = False
        vault_error = None
        try:
            verified = await self.ensure_arifos_verified_session()
            if verified:
                payload = {
                    "mode": "seal",
                    "payload": json.dumps(meta),
                    "ack_irreversible": True,
                    "session_id": verified,
                    "actor_id": "arif",
                }
                vault_resp = await self.mcp.call_tool(
                    "arifos",
                    "arif_vault_seal",
                    payload,
                    auto_init=False,
                )
                vault_ok = bool(vault_resp and "result" in vault_resp)
                if not vault_ok:
                    vault_error = str(vault_resp)
            else:
                vault_error = "No verified arifOS session"
        except Exception as exc:
            vault_error = str(exc)

        # Queue local retry if failed
        if not vault_ok:
            self._queue_vault_retry(session_id, meta)

        # NATS publish
        await self.hooks.run("nats-publish", event)

        # Human-readable summary
        await self.hooks.run("human-session-summary", event)

        return {
            "seal": seal_out,
            "vault_ok": vault_ok,
            "vault_error": vault_error,
        }

    def _queue_vault_retry(self, session_id: str, meta: dict[str, Any]) -> None:
        queue_path = self.workspace / ".vault_retry_queue.jsonl"
        try:
            with queue_path.open("a") as f:
                f.write(json.dumps({"session_id": session_id, "meta": meta, "ts": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}) + "\n")
        except Exception as exc:
            log.warning(f"vault retry queue failed: {exc}")

    async def notify(
        self,
        session_id: str,
        sink: str,
        notification_type: str,
        title: str,
        body: str,
        severity: str = "info",
    ) -> dict[str, Any]:
        return await self.hooks.run(
            "notify",
            {
                "session_id": session_id,
                "sink": sink,
                "notification_type": notification_type,
                "title": title,
                "body": body,
                "severity": severity,
                "hook_event_name": "Notification",
            },
        )

    async def close(self) -> None:
        await self.mcp.close()
