"""
telemetry_audit — AAA Telemetry and Audit Spine
Post-tool logging, delegation tracking, approval telemetry, session lifecycle.
DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import json
import os
import time
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class ToolMetrics:
    tool_name: str
    count: int = 0
    success: int = 0
    failure: int = 0
    total_duration_ms: int = 0
    last_called: Optional[str] = None


class TelemetryAuditPlugin:
    def __init__(
        self,
        audit_path: str = "/root/VAULT999/outcomes.jsonl",
        metrics_path: str = "/root/AAA/ops/hermes/telemetry/metrics.jsonl",
        delegation_log_path: str = "/root/AAA/ops/hermes/telemetry/delegation.jsonl",
        approval_log_path: str = "/root/AAA/ops/hermes/telemetry/approvals.jsonl",
        session_log_path: str = "/root/AAA/ops/hermes/telemetry/sessions.jsonl",
        alert_webhook_url: str = "",
    ):
        self.audit_path = Path(audit_path)
        self.metrics_path = Path(metrics_path)
        self.delegation_log_path = Path(delegation_log_path)
        self.approval_log_path = Path(approval_log_path)
        self.session_log_path = Path(session_log_path)
        self.alert_webhook_url = alert_webhook_url
        self._ensure_paths()
        self._metrics: Dict[str, ToolMetrics] = defaultdict(lambda: ToolMetrics(tool_name=""))
        self._session_start: Optional[float] = None
        self._session_tool_count = 0

    def _ensure_paths(self):
        for p in [self.metrics_path, self.delegation_log_path, self.approval_log_path, self.session_log_path]:
            p.parent.mkdir(parents=True, exist_ok=True)

    def log_tool_result(
        self,
        tool_name: str,
        args: Dict[str, Any],
        result: str,
        task_id: str = "",
        duration_ms: int = 0,
        **kwargs,
    ):
        try:
            ok = True
            try:
                parsed = json.loads(result) if isinstance(result, str) else result
                if isinstance(parsed, dict) and "error" in parsed:
                    ok = False
            except (json.JSONDecodeError, TypeError):
                if "error" in str(result).lower():
                    ok = False

            entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "actor": "telemetry",
                "action": "tool_result",
                "tool_name": tool_name,
                "params_sha256": hashlib.sha256(json.dumps(args, sort_keys=True, default=str).encode()).hexdigest()[:16],
                "outcome": "success" if ok else "failure",
                "duration_ms": duration_ms,
                "task_id": task_id,
            }
            self._append(self.audit_path, entry)
            self._update_metrics(tool_name, ok, duration_ms)
        except Exception as e:
            print(f"[telemetry_audit] log_tool_result error: {e}")

    def log_delegation_event(
        self,
        parent_session_id: str,
        child_role: Optional[str],
        child_summary: Optional[str],
        child_status: str,
        duration_ms: int,
        **kwargs,
    ):
        try:
            entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "actor": "telemetry",
                "action": "delegation_event",
                "parent_session_id": parent_session_id,
                "child_role": child_role,
                "child_status": child_status,
                "duration_ms": duration_ms,
                "summary_length": len(child_summary) if child_summary else 0,
            }
            self._append(self.audit_path, entry)
            self._append(self.delegation_log_path, entry)
        except Exception as e:
            print(f"[telemetry_audit] log_delegation_event error: {e}")

    def forward_approval_request(
        self,
        command: str,
        description: str,
        pattern_key: str,
        pattern_keys: List[str],
        session_key: str,
        surface: str,
        **kwargs,
    ):
        try:
            entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "actor": "telemetry",
                "action": "approval_requested",
                "command": command[:200],
                "description": description,
                "pattern_key": pattern_key,
                "pattern_keys": pattern_keys,
                "session_key": session_key,
                "surface": surface,
            }
            self._append(self.audit_path, entry)
            self._append(self.approval_log_path, entry)
            if self.alert_webhook_url:
                self._send_webhook(entry)
        except Exception as e:
            print(f"[telemetry_audit] forward_approval_request error: {e}")

    def log_approval_decision(
        self,
        command: str,
        description: str,
        pattern_key: str,
        pattern_keys: List[str],
        session_key: str,
        surface: str,
        choice: str,
        **kwargs,
    ):
        try:
            entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "actor": "telemetry",
                "action": "approval_decision",
                "command": command[:200],
                "choice": choice,
                "pattern_key": pattern_key,
                "session_key": session_key,
                "surface": surface,
            }
            self._append(self.audit_path, entry)
            self._append(self.approval_log_path, entry)
        except Exception as e:
            print(f"[telemetry_audit] log_approval_decision error: {e}")

    def init_session_telemetry(self, session_id: str, model: str, platform: str, **kwargs):
        try:
            self._session_start = time.time()
            self._session_tool_count = 0
            entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "actor": "telemetry",
                "action": "session_start",
                "session_id": session_id,
                "model": model,
                "platform": platform,
            }
            self._append(self.audit_path, entry)
            self._append(self.session_log_path, entry)
        except Exception as e:
            print(f"[telemetry_audit] init_session_telemetry error: {e}")

    def flush_session_telemetry(
        self,
        session_id: str,
        completed: bool,
        interrupted: bool,
        model: str,
        platform: str,
        **kwargs,
    ):
        try:
            duration_s = time.time() - self._session_start if self._session_start else 0
            entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "actor": "telemetry",
                "action": "session_end",
                "session_id": session_id,
                "completed": completed,
                "interrupted": interrupted,
                "duration_s": round(duration_s, 2),
                "tool_calls": self._session_tool_count,
                "model": model,
                "platform": platform,
            }
            self._append(self.audit_path, entry)
            self._append(self.session_log_path, entry)
        except Exception as e:
            print(f"[telemetry_audit] flush_session_telemetry error: {e}")

    def finalize_session_record(self, session_id: Optional[str], platform: str, **kwargs):
        try:
            self._flush_metrics()
            entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "actor": "telemetry",
                "action": "session_finalize",
                "session_id": session_id,
                "platform": platform,
            }
            self._append(self.audit_path, entry)
        except Exception as e:
            print(f"[telemetry_audit] finalize_session_record error: {e}")

    def _update_metrics(self, tool_name: str, ok: bool, duration_ms: int):
        m = self._metrics[tool_name]
        m.tool_name = tool_name
        m.count += 1
        if ok:
            m.success += 1
        else:
            m.failure += 1
        m.total_duration_ms += duration_ms
        m.last_called = datetime.now(timezone.utc).isoformat()
        self._session_tool_count += 1

    def _flush_metrics(self):
        try:
            with open(self.metrics_path, "a") as f:
                for m in self._metrics.values():
                    f.write(json.dumps({
                        "ts": datetime.now(timezone.utc).isoformat(),
                        "tool_name": m.tool_name,
                        "count": m.count,
                        "success": m.success,
                        "failure": m.failure,
                        "total_duration_ms": m.total_duration_ms,
                        "avg_duration_ms": round(m.total_duration_ms / m.count, 2) if m.count > 0 else 0,
                        "last_called": m.last_called,
                    }) + "\n")
            self._metrics.clear()
        except Exception as e:
            print(f"[telemetry_audit] _flush_metrics error: {e}")

    def _append(self, path: Path, entry: Dict[str, Any]):
        try:
            with open(path, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[telemetry_audit] _append error: {e}")

    def _send_webhook(self, entry: Dict[str, Any]):
        try:
            import httpx
            if self.alert_webhook_url:
                httpx.post(self.alert_webhook_url, json=entry, timeout=5)
        except Exception:
            pass


def register(ctx):
    plugin = TelemetryAuditPlugin(
        audit_path=os.environ.get("AAA_AUDIT_PATH", "/root/VAULT999/outcomes.jsonl"),
        metrics_path=os.environ.get("AAA_METRICS_PATH", "/root/AAA/ops/hermes/telemetry/metrics.jsonl"),
        delegation_log_path=os.environ.get("AAA_DELEGATION_LOG", "/root/AAA/ops/hermes/telemetry/delegation.jsonl"),
        approval_log_path=os.environ.get("AAA_APPROVAL_LOG", "/root/AAA/ops/hermes/telemetry/approvals.jsonl"),
        session_log_path=os.environ.get("AAA_SESSION_LOG", "/root/AAA/ops/hermes/telemetry/sessions.jsonl"),
        alert_webhook_url=os.environ.get("AAA_ALERT_WEBHOOK", ""),
    )
    ctx.register_hook("post_tool_call", _on_post_tool_call)
    ctx.register_hook("subagent_stop", _on_subagent_stop)
    ctx.register_hook("pre_approval_request", _on_pre_approval_request)
    ctx.register_hook("post_approval_response", _on_post_approval_response)
    ctx.register_hook("on_session_start", _on_session_start)
    ctx.register_hook("on_session_end", _on_session_end)
    ctx.register_hook("on_session_finalize", _on_session_finalize)
    print("[telemetry_audit] Loaded — full telemetry spine active")


def _on_post_tool_call(tool_name: str, args: dict, result: str, task_id: str = "",
                        duration_ms: int = 0, **kwargs) -> str:
    try:
        plugin = TelemetryAuditPlugin(
            audit_path=os.environ.get("AAA_AUDIT_PATH", "/root/VAULT999/outcomes.jsonl"),
            metrics_path=os.environ.get("AAA_METRICS_PATH", "/root/AAA/ops/hermes/telemetry/metrics.jsonl"),
            delegation_log_path=os.environ.get("AAA_DELEGATION_LOG", "/root/AAA/ops/hermes/telemetry/delegation.jsonl"),
            approval_log_path=os.environ.get("AAA_APPROVAL_LOG", "/root/AAA/ops/hermes/telemetry/approvals.jsonl"),
            session_log_path=os.environ.get("AAA_SESSION_LOG", "/root/AAA/ops/hermes/telemetry/sessions.jsonl"),
            alert_webhook_url=os.environ.get("AAA_ALERT_WEBHOOK", ""),
        )
        plugin.log_tool_result(tool_name, args, result, task_id, duration_ms, **kwargs)
    except Exception as e:
        print(f"[telemetry_audit] post_tool_call error: {e}")
    return result


def _on_subagent_stop(parent_session_id: str, child_role: Optional[str],
                       child_summary: Optional[str], child_status: str,
                       duration_ms: int = 0, **kwargs):
    try:
        plugin = TelemetryAuditPlugin(
            audit_path=os.environ.get("AAA_AUDIT_PATH", "/root/VAULT999/outcomes.jsonl"),
            metrics_path=os.environ.get("AAA_METRICS_PATH", "/root/AAA/ops/hermes/telemetry/metrics.jsonl"),
            delegation_log_path=os.environ.get("AAA_DELEGATION_LOG", "/root/AAA/ops/hermes/telemetry/delegation.jsonl"),
            approval_log_path=os.environ.get("AAA_APPROVAL_LOG", "/root/AAA/ops/hermes/telemetry/approvals.jsonl"),
            session_log_path=os.environ.get("AAA_SESSION_LOG", "/root/AAA/ops/hermes/telemetry/sessions.jsonl"),
            alert_webhook_url=os.environ.get("AAA_ALERT_WEBHOOK", ""),
        )
        plugin.log_delegation_event(parent_session_id, child_role, child_summary,
                                     child_status, duration_ms, **kwargs)
    except Exception as e:
        print(f"[telemetry_audit] subagent_stop error: {e}")


def _on_pre_approval_request(command: str, description: str, pattern_key: str,
                              pattern_keys: List[str], session_key: str,
                              surface: str, **kwargs):
    try:
        plugin = TelemetryAuditPlugin(
            audit_path=os.environ.get("AAA_AUDIT_PATH", "/root/VAULT999/outcomes.jsonl"),
            metrics_path=os.environ.get("AAA_METRICS_PATH", "/root/AAA/ops/hermes/telemetry/metrics.jsonl"),
            delegation_log_path=os.environ.get("AAA_DELEGATION_LOG", "/root/AAA/ops/hermes/telemetry/delegation.jsonl"),
            approval_log_path=os.environ.get("AAA_APPROVAL_LOG", "/root/AAA/ops/hermes/telemetry/approvals.jsonl"),
            session_log_path=os.environ.get("AAA_SESSION_LOG", "/root/AAA/ops/hermes/telemetry/sessions.jsonl"),
            alert_webhook_url=os.environ.get("AAA_ALERT_WEBHOOK", ""),
        )
        plugin.forward_approval_request(command, description, pattern_key,
                                        pattern_keys, session_key, surface, **kwargs)
    except Exception as e:
        print(f"[telemetry_audit] pre_approval_request error: {e}")


def _on_post_approval_response(command: str, description: str, pattern_key: str,
                                pattern_keys: List[str], session_key: str,
                                surface: str, choice: str, **kwargs):
    try:
        plugin = TelemetryAuditPlugin(
            audit_path=os.environ.get("AAA_AUDIT_PATH", "/root/VAULT999/outcomes.jsonl"),
            metrics_path=os.environ.get("AAA_METRICS_PATH", "/root/AAA/ops/hermes/telemetry/metrics.jsonl"),
            delegation_log_path=os.environ.get("AAA_DELEGATION_LOG", "/root/AAA/ops/hermes/telemetry/delegation.jsonl"),
            approval_log_path=os.environ.get("AAA_APPROVAL_LOG", "/root/AAA/ops/hermes/telemetry/approvals.jsonl"),
            session_log_path=os.environ.get("AAA_SESSION_LOG", "/root/AAA/ops/hermes/telemetry/sessions.jsonl"),
            alert_webhook_url=os.environ.get("AAA_ALERT_WEBHOOK", ""),
        )
        plugin.log_approval_decision(command, description, pattern_key,
                                      pattern_keys, session_key, surface, choice, **kwargs)
    except Exception as e:
        print(f"[telemetry_audit] post_approval_response error: {e}")


def _on_session_start(session_id: str, model: str, platform: str, **kwargs):
    try:
        plugin = TelemetryAuditPlugin(
            audit_path=os.environ.get("AAA_AUDIT_PATH", "/root/VAULT999/outcomes.jsonl"),
            metrics_path=os.environ.get("AAA_METRICS_PATH", "/root/AAA/ops/hermes/telemetry/metrics.jsonl"),
            delegation_log_path=os.environ.get("AAA_DELEGATION_LOG", "/root/AAA/ops/hermes/telemetry/delegation.jsonl"),
            approval_log_path=os.environ.get("AAA_APPROVAL_LOG", "/root/AAA/ops/hermes/telemetry/approvals.jsonl"),
            session_log_path=os.environ.get("AAA_SESSION_LOG", "/root/AAA/ops/hermes/telemetry/sessions.jsonl"),
            alert_webhook_url=os.environ.get("AAA_ALERT_WEBHOOK", ""),
        )
        plugin.init_session_telemetry(session_id, model, platform, **kwargs)
    except Exception as e:
        print(f"[telemetry_audit] on_session_start error: {e}")


def _on_session_end(session_id: str, completed: bool, interrupted: bool,
                    model: str, platform: str, **kwargs):
    try:
        plugin = TelemetryAuditPlugin(
            audit_path=os.environ.get("AAA_AUDIT_PATH", "/root/VAULT999/outcomes.jsonl"),
            metrics_path=os.environ.get("AAA_METRICS_PATH", "/root/AAA/ops/hermes/telemetry/metrics.jsonl"),
            delegation_log_path=os.environ.get("AAA_DELEGATION_LOG", "/root/AAA/ops/hermes/telemetry/delegation.jsonl"),
            approval_log_path=os.environ.get("AAA_APPROVAL_LOG", "/root/AAA/ops/hermes/telemetry/approvals.jsonl"),
            session_log_path=os.environ.get("AAA_SESSION_LOG", "/root/AAA/ops/hermes/telemetry/sessions.jsonl"),
            alert_webhook_url=os.environ.get("AAA_ALERT_WEBHOOK", ""),
        )
        plugin.flush_session_telemetry(session_id, completed, interrupted, model, platform, **kwargs)
    except Exception as e:
        print(f"[telemetry_audit] on_session_end error: {e}")


def _on_session_finalize(session_id: Optional[str], platform: str, **kwargs):
    try:
        plugin = TelemetryAuditPlugin(
            audit_path=os.environ.get("AAA_AUDIT_PATH", "/root/VAULT999/outcomes.jsonl"),
            metrics_path=os.environ.get("AAA_METRICS_PATH", "/root/AAA/ops/hermes/telemetry/metrics.jsonl"),
            delegation_log_path=os.environ.get("AAA_DELEGATION_LOG", "/root/AAA/ops/hermes/telemetry/delegation.jsonl"),
            approval_log_path=os.environ.get("AAA_APPROVAL_LOG", "/root/AAA/ops/hermes/telemetry/approvals.jsonl"),
            session_log_path=os.environ.get("AAA_SESSION_LOG", "/root/AAA/ops/hermes/telemetry/sessions.jsonl"),
            alert_webhook_url=os.environ.get("AAA_ALERT_WEBHOOK", ""),
        )
        plugin.finalize_session_record(session_id, platform, **kwargs)
    except Exception as e:
        print(f"[telemetry_audit] on_session_finalize error: {e}")
