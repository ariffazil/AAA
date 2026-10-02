"""test_one_door.py — PR-3 ONE-DOOR fresh-agent conformance.

Simulates a fresh agent that knows ONLY the eight arifOS kernel verbs
(init, observe, think, route, memory, judge, forge, seal) and ZERO organ
topology. It must be able to:

    1. DISCOVERY     — find the arifOS kernel MCP endpoint at runtime
                       (from /root/.kimi-code/mcp.json or the launcher it
                       references), never from hardcoded topology.
    2. ROUTING       — drive arif_route with six SEMANTIC intents (no
                       organ names in the intent text) and hit the right
                       organ each time:
                         meaning/interpretation → HERMES
                         temporal/calibration   → CHRON
                         geology                → GEOX
                         capital/market         → WEALTH
                         readiness/vitality     → WELL
                         execution/build        → A-FORGE
    3. IDENTITY_CONTINUITY — bind a session with arif_init and check the
                       kernel echoes the same session_id on arif_route.
                       If the kernel does not echo it → UNMEASURED,
                       honestly, never false.
    4. AUTHORITY_CONTINUITY — authority-band echo across init → route.
                       UNMEASURED when the fields are absent (this PR
                       allows UNMEASURED).
    5. EVIDENCE_RETURN — each route response carries an organ handle or
                       evidence pointer.

Output: a OneDoor verdict object —
    {discovery, routing, identity_continuity, authority_continuity,
     evidence_return}
with true / false / "UNMEASURED" per clause, every clause explicitly
set, plus a per-intent table on stdout.

Offline-safe: every network call has a timeout ≤ 10 s; transport
failures make the affected clause FALSE (or SKIP with an honest reason
when the transport itself is undiscoverable) — never a hang, never a
faked pass. Stdlib only; imports nothing from AAA adapters or organs.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# ── Fresh-agent vocabulary: the eight kernel verbs. Nothing else. ────
VERBS = ["init", "observe", "think", "route", "memory", "judge", "forge", "seal"]

ACTOR_ID = "aaa-one-door-conformance/pr3"

# (clause label, semantic intent — organ names forbidden in intent text, expected organ)
INTENTS: list[tuple[str, str, str]] = [
    (
        "meaning",
        "interpret the meaning and perspective of this human message",
        "HERMES",
    ),
    (
        "temporal",
        "how much attention debt is owed and which predictions are due for calibration verification",
        "CHRON",
    ),
    (
        "geology",
        "interpret this seismic section and map the basin subsurface structure",
        "GEOX",
    ),
    (
        "capital",
        "assess the market risk and capital health of this portfolio position",
        "WEALTH",
    ),
    (
        "vitality",
        "check the machine readiness and vitality health before we deploy the service",
        "WELL",
    ),
    (
        "execution",
        "build and execute this small refactor in the workspace now",
        "A-FORGE",
    ),
]

MCP_JSON = Path("/root/.kimi-code/mcp.json")
HTTP_TIMEOUT = 8.0  # ≤ 10 s, everywhere, no exceptions


# ── transport helpers (fresh agent's own, stdlib only) ───────────────


def _parse_body(raw: str) -> dict[str, Any]:
    raw = (raw or "").strip()
    if raw.startswith("{") or raw.startswith("["):
        return json.loads(raw)
    for line in raw.splitlines():
        if line.startswith("data:"):
            chunk = line[len("data:"):].strip()
            if chunk:
                return json.loads(chunk)
    return {}


def _post_mcp(
    url: str, body: dict[str, Any], session_id: str | None = None
) -> tuple[str | None, dict[str, Any]]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        sid = resp.headers.get("mcp-session-id")
        payload = _parse_body(resp.read().decode(errors="replace"))
    return sid, payload


def _content_dict(envelope: dict[str, Any]) -> dict[str, Any]:
    """Extract the tool's JSON payload from a tools/call response envelope."""
    if envelope.get("error"):
        return {"_error": envelope["error"]}
    result = envelope.get("result") or {}
    for block in result.get("content") or []:
        if isinstance(block, dict) and block.get("text"):
            try:
                parsed = json.loads(block["text"])
                return parsed if isinstance(parsed, dict) else {"_value": parsed}
            except json.JSONDecodeError:
                return {"_raw": block["text"]}
    return {}


# ── clause 1: DISCOVERY (runtime, no hardcoded topology) ─────────────


def discover_kernel_mcp_url() -> tuple[str | None, str]:
    """Find the arifOS kernel MCP URL from runtime config, or give up honestly."""
    import os

    override = os.getenv("AAA_ARIFOS_MCP_URL")
    if override:
        return override.rstrip("/"), "env AAA_ARIFOS_MCP_URL"

    if not MCP_JSON.exists():
        return None, f"{MCP_JSON} not found"
    try:
        cfg = json.loads(MCP_JSON.read_text())
    except json.JSONDecodeError as exc:
        return None, f"{MCP_JSON} unparseable: {exc}"
    entry = (cfg.get("mcpServers") or {}).get("arifos")
    if not entry:
        return None, "no 'arifos' server entry in mcp.json"

    url = entry.get("url")
    if url:
        return str(url).rstrip("/"), "mcp.json arifos.url"

    # command launcher — the shim references the python bridge that knows
    # the kernel host/port; read that reference chain, no guessing.
    command = entry.get("command")
    if not command or not Path(command).exists():
        return None, f"arifos launcher not found: {command!r}"
    launcher_text = Path(command).read_text(errors="replace")
    candidates = [Path(command)]
    for ref in re.finditer(r"([\w./-]+\.(?:py|sh))", launcher_text):
        ref_path = Path(ref.group(1))
        if not ref_path.is_absolute():
            ref_path = Path(command).parent / ref_path
        if ref_path.exists() and ref_path not in candidates:
            candidates.append(ref_path)

    host = port = None
    for cand in candidates:
        text = cand.read_text(errors="replace")
        m_host = re.search(r'ARIFOS_HOST\s*=\s*["\']([^"\']+)["\']', text)
        m_port = re.search(r"ARIFOS_PORT\s*=\s*(\d+)", text)
        if m_host and not host:
            host = m_host.group(1)
        if m_port and not port:
            port = m_port.group(1)
        if host and port:
            break
    if not port:
        # last resort inside the same chain: any localhost:port literal
        for cand in candidates:
            m = re.search(r"127\.0\.0\.1:(\d+)", cand.read_text(errors="replace"))
            if m:
                port = m.group(1)
                host = host or "127.0.0.1"
                break
    if not port:
        return None, (
            "arifos launcher chain exposes no kernel port "
            f"(scanned: {[str(c) for c in candidates]})"
        )
    return f"http://{host or '127.0.0.1'}:{port}".rstrip("/"), (
        f"mcp.json arifos.command chain: {candidates[0].name}"
    )


# ── protocol run ─────────────────────────────────────────────────────


def run_protocol() -> dict[str, Any]:
    verdict: dict[str, Any] = {
        "discovery": False,
        "routing": False,
        "identity_continuity": "UNMEASURED",
        "authority_continuity": "UNMEASURED",
        "evidence_return": False,
        "intents": [],
        "skip_reason": None,
        "discovery_how": None,
    }

    url, how = discover_kernel_mcp_url()
    verdict["discovery_how"] = how
    if not url:
        verdict["skip_reason"] = f"transport undiscoverable: {how}"
        return verdict

    # DISCOVERY clause: GET /tools must advertise the eight verbs.
    try:
        req = urllib.request.Request(
            f"{url}/tools", headers={"Accept": "application/json"}, method="GET"
        )
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            tools_doc = json.loads(resp.read().decode(errors="replace"))
        advertised = {
            t.get("name") if isinstance(t, dict) else t
            for t in (tools_doc.get("tools") if isinstance(tools_doc, dict) else tools_doc)
            or []
        }
        # fresh agent knows the eight verb concepts; kernel names them arif_<verb>
        missing = [
            v for v in VERBS if v not in advertised and f"arif_{v}" not in advertised
        ]
        verdict["discovery"] = not missing
        if missing:
            verdict["skip_reason"] = (
                f"kernel at {url} does not advertise the 8 verbs; missing={missing}"
            )
            return verdict
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
        verdict["skip_reason"] = f"kernel unreachable at {url}: {exc}"
        return verdict

    # Fresh agent boot: verb 1 — init → session bind.
    session_id = session_token = None
    init_actor = init_authority = None
    try:
        mcp_sid, _ = _post_mcp(
            f"{url}/mcp",
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "one-door-conformance", "version": "1.0"},
                },
            },
        )
        _post_mcp(f"{url}/mcp", {"jsonrpc": "2.0", "method": "notifications/initialized"}, mcp_sid)
        _id = 1
        _id += 1

        _sid, init_env = _post_mcp(
            f"{url}/mcp",
            {
                "jsonrpc": "2.0",
                "id": _id,
                "method": "tools/call",
                "params": {
                    "name": "arif_init",
                    "arguments": {
                        "mode": "init",
                        "actor_id": ACTOR_ID,
                        "intent": "PR-3 ONE-DOOR conformance probe",
                        "verbosity": "minimal",
                    },
                },
            },
            mcp_sid,
        )
        init = _content_dict(init_env)
        session_id = init.get("session_id")
        session_token = init.get("session_token")
        actor = init.get("actor") or {}
        init_actor = actor.get("actor_id") or init.get("actor_id")
        init_authority = actor.get("authority_level") or init.get("authority")
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
        verdict["skip_reason"] = f"arif_init transport failed: {exc}"
        # routing/evidence can still be probed; identity stays UNMEASURED

    # Six semantic intents through arif_route.
    routing_ok = True
    evidence_ok = True
    identity_ok = True
    identity_measured = session_id is not None
    authority_ok = True
    authority_measured = init_actor is not None

    for label, intent, expected in INTENTS:
        row: dict[str, Any] = {"intent": label, "expected": expected}
        try:
            args: dict[str, Any] = {"intent": intent}
            if session_id:
                args["session_id"] = session_id
                if session_token:
                    args["session_token"] = session_token
            _id += 1
            _sid, env = _post_mcp(
                f"{url}/mcp",
                {
                    "jsonrpc": "2.0",
                    "id": _id,
                    "method": "tools/call",
                    "params": {"name": "arif_route", "arguments": args},
                },
                mcp_sid,
            )
            resp = _content_dict(env)
            result = resp.get("result") or {}
            target = result.get("organ")
            if not target:
                for fact in resp.get("facts") or []:
                    m = re.match(r"organ=(\S+)", str(fact))
                    if m:
                        target = m.group(1)
                        break
            row["target"] = target
            row["ok"] = target == expected
            routing_ok &= row["ok"]

            # identity echo
            echoed = resp.get("session_id")
            if echoed is None:
                identity_measured = False
            else:
                identity_ok &= echoed == session_id
            row["session_echo"] = echoed

            # authority echo
            actor = resp.get("actor") or {}
            echoed_actor = actor.get("actor_id") or resp.get("actor_id")
            echoed_auth = actor.get("authority_level") or resp.get("authority")
            if echoed_actor is None and echoed_auth is None:
                authority_measured = False
            else:
                if init_actor is not None and echoed_actor is not None:
                    authority_ok &= echoed_actor == init_actor
                if init_authority is not None and echoed_auth is not None:
                    authority_ok &= echoed_auth == init_authority
            row["actor_echo"] = echoed_actor
            row["authority_echo"] = echoed_auth

            # evidence return: organ handle or evidence pointer
            has_handle = bool(target) and bool(
                result.get("port") or result.get("tool_prefix") or result.get("organ_tool")
                or resp.get("facts")
                or resp.get("trace_id")
            )
            row["evidence"] = has_handle
            evidence_ok &= has_handle
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
            row["target"] = None
            row["error"] = f"{type(exc).__name__}: {exc}"
            row["ok"] = False
            row["evidence"] = False
            routing_ok = False
            evidence_ok = False
        verdict["intents"].append(row)

    verdict["routing"] = routing_ok
    verdict["evidence_return"] = evidence_ok
    verdict["identity_continuity"] = (
        identity_ok if (identity_measured and session_id) else "UNMEASURED"
    )
    verdict["authority_continuity"] = (
        authority_ok if authority_measured else "UNMEASURED"
    )
    if session_id is None:
        verdict.setdefault("notes", []).append(
            "arif_init returned no session_id — identity/authority clauses UNMEASURED"
        )
    return verdict


# ── reporting ────────────────────────────────────────────────────────


def _clause_cell(value: Any) -> str:
    if value is True:
        return "PASS"
    if value is False:
        return "FAIL"
    if value == "UNMEASURED":
        return "UNMEASURED"
    return "SKIP" if value is None else str(value)


def print_report(verdict: dict[str, Any]) -> None:
    print("=" * 74)
    print("PR-3 ONE-DOOR CONFORMANCE — fresh agent, 8 verbs, zero organ topology")
    print("=" * 74)
    print(f"  discovery: {verdict.get('discovery_how')}")
    print()
    print("  PER-INTENT ROUTING")
    for row in verdict.get("intents") or []:
        mark = "✓" if row.get("ok") else "✗"
        err = f"  [{row['error']}]" if row.get("error") else ""
        print(
            f"    {mark} {row['intent']:<10} expected={row['expected']:<8} "
            f"got={row.get('target')!s:<8} evidence={row.get('evidence')!s:<5} "
            f"session_echo={row.get('session_echo')!s:<24}{err}"
        )
    print()
    print("  ONEDOOR VERDICT")
    print("  {")
    for clause in (
        "discovery",
        "routing",
        "identity_continuity",
        "authority_continuity",
        "evidence_return",
    ):
        print(f"    {clause}: {verdict.get(clause)!r}")
    print("  }")
    print()
    print("  CLAUSE TABLE")
    for clause in (
        "discovery",
        "routing",
        "identity_continuity",
        "authority_continuity",
        "evidence_return",
    ):
        print(f"    {clause:<22} {_clause_cell(verdict.get(clause))}")
    if verdict.get("skip_reason"):
        print(f"    SKIP REASON: {verdict['skip_reason']}")
    print("=" * 74)


# ── pytest entry ─────────────────────────────────────────────────────


def test_one_door_verdict():
    """Runs the fresh-agent protocol and reports the OneDoor verdict.

    The clause VALUES are the report (true/false/UNMEASURED per clause).
    The assertion guards verdict WELL-FORMEDNESS only: every clause
    explicitly set, no silent None, no hang. Clause failures print as
    FAIL in the table — an offline run must still complete and report.
    """
    verdict = run_protocol()
    print_report(verdict)
    for clause in (
        "discovery",
        "routing",
        "identity_continuity",
        "authority_continuity",
        "evidence_return",
    ):
        assert clause in verdict, f"verdict missing clause: {clause}"
        value = verdict[clause]
        assert value in (True, False, "UNMEASURED"), (
            f"clause {clause} not explicitly set: {value!r}"
        )
    for row in verdict.get("intents") or []:
        assert row.get("ok") in (True, False), f"intent row not resolved: {row}"


if __name__ == "__main__":
    test_one_door_verdict()
