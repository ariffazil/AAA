"""
Pre-Forge Constitutional Gate HTTP Service.
============================================

Thin HTTP wrapper around pre_forge_gate.py — exposes the unified
constitutional gate as a local HTTP endpoint for A-FORGE and AAA.

Endpoint:
  POST /check      — Run full pre-forge gate
  POST /quick      — Quick boolean check
  GET  /health     — Liveness probe
  GET  /witness/:id — Get witness state for a session

Port: 18990 (internal, localhost only)

Usage from A-FORGE:
  const res = await fetch('http://127.0.0.1:18990/check', {
    method: 'POST',
    body: JSON.stringify({ text, action_class, session_id }),
  });
  const gate = await res.json();
  if (!gate.allowed) throw new Error(`GATE_BLOCKED: ${gate.verdict}`);

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import json
import sys
import os
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone
from typing import Optional

# Add AAA root to path
_AAA_ROOT = Path("/root/AAA")
sys.path.insert(0, str(_AAA_ROOT))

from core.pre_forge_gate import PreForgeGate, PreForgeGateResult
from core.witness_diversity import (
    SessionWitnessState,
    WitnessType,
    compute_witness_score,
    pre_forge_witness_gate,
)
from core.citation_provenance import CitationProvenance, CitationProvenanceAuditor
from core.shadow_audit import ShadowAuditor, ShadowAuditResult

# ── Session State Store ──────────────────────────────────────────────────────

SESSIONS: dict[str, SessionWitnessState] = {}
SESSION_STORE_PATH = Path("/tmp/aaa_preforge_sessions.json")


def _load_sessions():
    """Restore session states from disk."""
    global SESSIONS
    if SESSION_STORE_PATH.exists():
        try:
            data = json.loads(SESSION_STORE_PATH.read_text())
            for sid, sdata in data.items():
                state = SessionWitnessState(sid)
                for wt, wdata in sdata.get("witnesses", {}).items():
                    if wdata.get("active"):
                        state.register(wt, wdata.get("evidence_ref", ""))
                SESSIONS[sid] = state
        except Exception:
            pass


def _save_sessions():
    """Persist session states to disk."""
    try:
        data = {}
        for sid, state in SESSIONS.items():
            data[sid] = state.to_dict()
        SESSION_STORE_PATH.write_text(json.dumps(data, indent=2))
    except Exception:
        pass


def get_or_create_session(session_id: str) -> SessionWitnessState:
    """Get existing session or create new one."""
    if session_id not in SESSIONS:
        SESSIONS[session_id] = SessionWitnessState(session_id)
        SESSIONS[session_id].register_human()  # Human sovereign always present
        _save_sessions()
    return SESSIONS[session_id]


def register_witness(session_id: str, witness_type: str, evidence_ref: str = "") -> dict:
    """Register a witness in a session."""
    state = get_or_create_session(session_id)
    state.register(witness_type, evidence_ref)
    _save_sessions()
    return {"ok": True, "session_id": session_id, "witness_summary": state.summary()}


def register_earth_measurement(session_id: str, tool_name: str, evidence_ref: str = "") -> dict:
    """Register an Earth measurement witness."""
    state = get_or_create_session(session_id)
    state.register_earth_measurement(tool_name, evidence_ref)
    _save_sessions()
    return {"ok": True, "session_id": session_id, "witness_summary": state.summary()}


def register_model_output(session_id: str, model_id: str, is_primary: bool = True) -> dict:
    """Register a model output witness."""
    state = get_or_create_session(session_id)
    state.register_model_output(model_id, is_primary)
    _save_sessions()
    return {"ok": True, "session_id": session_id, "witness_summary": state.summary()}


# ── HTTP Handler ─────────────────────────────────────────────────────────────

class PreForgeHandler(BaseHTTPRequestHandler):
    """HTTP handler for the pre-forge gate service."""

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self._send_json({
                "status": "ok",
                "service": "pre-forge-gate",
                "version": "v1.0.0",
                "active_sessions": len(SESSIONS),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        elif self.path.startswith("/witness/"):
            session_id = self.path.split("/witness/", 1)[1]
            state = get_or_create_session(session_id)
            self._send_json(state.to_dict())
        elif self.path == "/sessions":
            self._send_json({
                "count": len(SESSIONS),
                "sessions": {sid: s.summary() for sid, s in SESSIONS.items()},
            })
        else:
            self._send_json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path == "/check":
            self._handle_check()
        elif self.path == "/quick":
            self._handle_quick()
        elif self.path == "/witness":
            self._handle_witness_register()
        elif self.path == "/earth":
            self._handle_earth_register()
        elif self.path == "/model":
            self._handle_model_register()
        else:
            self._send_json({"error": "not found"}, 404)

    def _handle_check(self):
        """POST /check — Run full pre-forge constitutional gate."""
        try:
            body = self._read_body()
            text = body.get("text", "")
            action_class = body.get("action_class", "mutate")
            session_id = body.get("session_id", "default")
            claimed_evidence_tier = body.get("claimed_evidence_tier", "INTERPRETATION")
            model_id = body.get("model_id", "unknown")
            known_provenances_raw = body.get("known_provenances", {})

            # Reconstruct CitationProvenance objects from raw dicts
            known_provenances = {}
            for marker, prov_data in known_provenances_raw.items():
                if isinstance(prov_data, dict):
                    known_provenances[marker] = CitationProvenance(
                        citation_text=prov_data.get("citation_text", marker),
                        source_model_id=prov_data.get("source_model_id", ""),
                        tool_name=prov_data.get("tool_name", ""),
                        query_id=prov_data.get("query_id", ""),
                        retrieval_timestamp=prov_data.get("retrieval_timestamp", ""),
                        result_position=prov_data.get("result_position", -1),
                        source_url=prov_data.get("source_url", ""),
                    )

            # Get or create session witness state
            witness_state = get_or_create_session(session_id)

            # Register this model output as a witness
            if model_id and model_id != "unknown":
                witness_state.register_model_output(model_id, is_primary=True)

            gate = PreForgeGate(witness_state)
            result = gate.check(
                text=text,
                action_class=action_class,
                claimed_evidence_tier=claimed_evidence_tier,
                known_provenances=known_provenances,
                model_id=model_id,
            )

            response = {
                "allowed": result.allowed,
                "verdict": result.verdict,
                "all_clear": result.all_clear,
                "violations": result.violations,
                "required_actions": result.required_actions,
                "citation_summary": {
                    "total": result.citation_audit.get("total_citations", 0) if result.citation_audit else 0,
                    "provenanced": result.citation_audit.get("provenanced_count", 0) if result.citation_audit else 0,
                    "decorative": result.citation_audit.get("decorative_count", 0) if result.citation_audit else 0,
                    "recommendation": result.citation_audit.get("recommendation", "N/A") if result.citation_audit else "N/A",
                } if result.citation_audit else None,
                "witness_summary": witness_state.summary(),
                "shadow_summary": {
                    "classification": result.shadow_audit.shadow_classification,
                    "score": round(result.shadow_audit.shadow_score, 3),
                } if result.shadow_audit else None,
                "gated_at": result.gated_at,
            }
            self._send_json(response)
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 500)

    def _handle_quick(self):
        """POST /quick — Quick boolean check."""
        try:
            body = self._read_body()
            text = body.get("text", "")
            action_class = body.get("action_class", "mutate")
            session_id = body.get("session_id", "default")

            witness_state = get_or_create_session(session_id)
            gate = PreForgeGate(witness_state)
            result = gate.check(text=text, action_class=action_class)
            self._send_json({
                "allowed": result.allowed,
                "verdict": result.verdict,
                "violations": [v.get("step", "unknown") for v in result.violations],
            })
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 500)

    def _handle_witness_register(self):
        """POST /witness — Register a witness."""
        try:
            body = self._read_body()
            session_id = body.get("session_id", "default")
            witness_type = body.get("witness_type", "")
            evidence_ref = body.get("evidence_ref", "")
            result = register_witness(session_id, witness_type, evidence_ref)
            self._send_json(result)
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 500)

    def _handle_earth_register(self):
        """POST /earth — Register an Earth measurement."""
        try:
            body = self._read_body()
            session_id = body.get("session_id", "default")
            tool_name = body.get("tool_name", "unknown")
            evidence_ref = body.get("evidence_ref", "")
            result = register_earth_measurement(session_id, tool_name, evidence_ref)
            self._send_json(result)
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 500)

    def _handle_model_register(self):
        """POST /model — Register a model output witness."""
        try:
            body = self._read_body()
            session_id = body.get("session_id", "default")
            model_id = body.get("model_id", "unknown")
            is_primary = body.get("is_primary", True)
            result = register_model_output(session_id, model_id, is_primary)
            self._send_json(result)
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 500)

    def log_message(self, format, *args):
        """Suppress default HTTP request logging (use arifOS event log instead)."""
        pass


# ── Service Runner ───────────────────────────────────────────────────────────

def start_service(port: int = 18990):
    """Start the pre-forge gate HTTP service."""
    _load_sessions()
    server = HTTPServer(("127.0.0.1", port), PreForgeHandler)
    print(f"[pre-forge-gate] Constitutional gate live on http://127.0.0.1:{port}")
    print(f"[pre-forge-gate] Endpoints: /check /quick /witness /earth /model /health")
    print(f"[pre-forge-gate] Loaded {len(SESSIONS)} existing sessions")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[pre-forge-gate] Shutting down...")
        _save_sessions()
        server.shutdown()


if __name__ == "__main__":
    port = int(os.environ.get("PRE_FORGE_PORT", 18990))
    start_service(port)
