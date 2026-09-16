#!/usr/bin/env python3
"""federation_capability_audit — what can each AAA agent ACTUALLY do, proven live.

WHY
  "Hermes has capability X" and "all AAA agents can use X" are claims, and claims
  drift. Each agent has its own skills tree and its own MCP config, so a capability
  added once is silently visible to nobody but its author. This script answers the
  only question that matters — *proven vs assumed* — for every agent at once.

WHAT IT CHECKS (all live, no cached narrative)
  skills  : does the agent's skill dir (or the AAA mesh it links to) contain the skill
  mcp     : does the agent's MCP config carry the server, and is the backend UP
  bin     : is the CLI/wrapper the capability depends on present and executable

TRUTH STATES — no "we have that"
  LIVE     artifact present AND backend verified reachable
  PRESENT  artifact present, backend not verified (no probe defined)
  PARTIAL  listed in config but the backend did not answer
  ABSENT   not found
  N/A      this agent does not use this substrate

USAGE
  python3 /root/AAA/registry/federation_capability_audit.py            # human table
  python3 /root/AAA/registry/federation_capability_audit.py --json     # machine
  python3 /root/AAA/registry/federation_capability_audit.py --drift    # only gaps, exit 1 if any

Exit code: 0 when nothing is ABSENT/PARTIAL outside expected gaps, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import socket
import sys
import time
from pathlib import Path

AAA_MESH = Path("/root/AAA/skills")

# ── the capabilities this audit tracks ───────────────────────────────────────
# Each: skill name on disk + optional backend (tcp port or http path) to prove live.
CAPABILITIES = {
    "media-ingest-lane": {
        "skill": "media-ingest-lane",
        "mcp_server": "media-ingest",
        "backend": ("http", "http://127.0.0.1:18411/mcp"),
        "why": "read any shared link (YouTube/IG/TikTok/X/web) instead of guessing",
    },
    "mcp-context-compression": {
        "skill": "mcp-context-compression",
        "mcp_server": None,
        "backend": ("bin", "/root/.local/bin/mcp-compressor"),
        "why": "stop tool schemas from eating the context window",
    },
    "youtube-extraction-datacenter-ip": {
        "skill": "youtube-extraction-datacenter-ip",
        "mcp_server": None,
        "backend": None,
        "why": "which YouTube lanes actually work from this IP",
    },
    "graphiti-temporal-memory-ops": {
        "skill": "graphiti-temporal-memory-ops",
        "mcp_server": None,
        "backend": ("http", "http://127.0.0.1:18412/mcp/"),
        "why": "temporal memory ops; the wrong-graph trap that faked a FAIL",
    },
    # --- ORGANS: the ability to OBSERVE and METABOLIZE the federation itself ---
    "frame-observer": {
        "skill": None,
        "mcp_server": "frame",
        "backend": ("http", "http://127.0.0.1:18086/mcp"),
        "why": "independent observer — baseline/drift/trend; evidence, never a verdict",
    },
    "arifflow-metabolism": {
        "skill": None,
        "mcp_server": "arifflow",
        "backend": ("http", "http://127.0.0.1:7073/health"),
        "why": "FQ gate + flow receipts; agents must POST /check before execute",
    },
}

# ── the agents ───────────────────────────────────────────────────────────────
def _home() -> Path:
    return Path(os.environ.get("HOME") or "/root")

AGENTS = {
    "hermes": {
        "skills": [_home() / ".hermes" / "skills"],
        "mcp": _home() / ".hermes" / "config.yaml",
        "mcp_format": "yaml",
    },
    "codex": {
        "skills": [Path("/root/.codex/skills")],
        "mcp": Path("/root/.codex/config.toml"),
        "mcp_format": "toml",
    },
    "kimi": {
        "skills": [Path("/root/.kimi-code/skills"), AAA_MESH],
        "mcp": Path("/root/.kimi-code/mcp.json"),
        "mcp_format": "json-mcpServers",
    },
    "claude": {
        "skills": [Path("/root/.claude/skills")],
        "mcp": Path("/root/.claude/mcp.json"),
        "mcp_format": "json-mcpServers",
    },
    "grok": {
        "skills": [Path("/root/.grok/skills")],
        "mcp": None,  # grok configures organs in AGENTS.md, not a json/toml file
        "mcp_format": "none",
    },
    "opencode": {
        "skills": [Path("/root/.opencode/skills"), Path("/root/.config/opencode/skills")],
        "mcp": Path("/root/.config/opencode/opencode.json"),
        "mcp_format": "json-mcp",
    },
    "agents-mesh": {
        "skills": [Path("/root/.agents/skills")],
        "mcp": None,
        "mcp_format": "none",
    },
}


def probe_backend(spec) -> tuple[bool | None, str]:
    if not spec:
        return None, "no probe defined"
    kind, target = spec
    if kind == "http":
        try:
            r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                                "--max-time", "6", target],
                               capture_output=True, text=True, timeout=20)
            code = (r.stdout or "").strip()
            # An MCP streamable-HTTP endpoint answers variously depending on what it
            # expects: 200/400/406 on a bare probe, and 307 when the path needs a
            # trailing slash. ALL of those mean "something is listening and speaking
            # HTTP" — only conn-refused/timeout (000) means DOWN. Treating 307 as DOWN
            # produced a false PARTIAL across all 7 agents (caught 2026-09-16).
            if code in ("200", "307", "308", "400", "401", "403", "406"):
                return True, f"HTTP {code}"
            return False, f"HTTP {code or 'no answer'}"
        except Exception as exc:  # noqa: BLE001
            return False, f"probe error: {exc}"
    if kind == "bin":
        p = Path(target)
        return (p.exists() and os.access(p, os.X_OK)), ("executable" if p.exists() else "missing")
    if kind == "port":
        try:
            with socket.create_connection(("127.0.0.1", int(target)), timeout=4):
                return True, f"port {target} open"
        except OSError:
            return False, f"port {target} closed"
    return None, "unknown probe kind"


def read_mcp_servers(agent: dict) -> set[str] | None:
    """Server names for this agent, or None when the agent has NO MCP surface at all.

    None ("no MCP config exists") is meaningfully different from set() ("config exists
    but configures nothing") — the first should score N/A, the second ABSENT. Conflating
    them marked a pure skills tree as an agent with missing wiring (caught 2026-09-16).
    """
    path, fmt = agent.get("mcp"), agent.get("mcp_format")
    if not path or fmt in (None, "none") or not Path(path).exists():
        return None
    try:
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    if fmt == "yaml":
        import yaml
        d = yaml.safe_load(text) or {}
        return set((d.get("mcp_servers") or {}).keys())
    if fmt == "toml":
        return set(re.findall(r"^\[mcp_servers\.([A-Za-z0-9_.-]+)\]", text, re.M))
    if fmt == "json-mcpServers":
        try:
            d = json.loads(text)
            return set((d.get("mcpServers") or d).keys())
        except Exception:  # noqa: BLE001
            return set()
    if fmt == "json-mcp":
        try:
            d = json.loads(text)
            return set((d.get("mcp") or {}).keys())
        except Exception:  # noqa: BLE001
            return set()
    return set()


def mcp_has(servers: set[str] | None, name: str) -> bool | None:
    """Case-insensitive membership.

    Server names are not cased consistently across agents: Kimi configures
    `arifFlow` while Hermes uses `arifflow`. An exact-match check reported a false
    ABSENT for every agent that spelled it differently (caught 2026-09-16).
    """
    if servers is None:
        return None
    low = {s.lower() for s in servers}
    return name.lower() in low


def has_skill(agent: dict, skill: str | None) -> tuple[bool, str]:
    # Organ capabilities (frame, arifflow) are MCP-only — no skill artifact. Treat
    # them as "present" so the audit scores them on MCP wiring + live backend,
    # not on a skill file that was never supposed to exist.
    if not skill:
        return True, "organ(mcp-only)"
    for base in agent["skills"]:
        if not base.exists():
            continue
        d = base / skill
        if (d / "SKILL.md").exists():
            resolved = base.resolve()
            return True, ("mesh" if resolved == AAA_MESH.resolve() else "local")
    return False, ""


def audit() -> dict:
    out: dict = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                 "capabilities": {}, "backends": {}, "agents": {}}

    for cap, meta in CAPABILITIES.items():
        ok, detail = probe_backend(meta.get("backend"))
        out["backends"][cap] = {"ok": ok, "detail": detail, "why": meta["why"]}

    for name, agent in AGENTS.items():
        rows = {}
        for cap, meta in CAPABILITIES.items():
            present, where = has_skill(agent, meta["skill"])
            servers = read_mcp_servers(agent) if meta.get("mcp_server") else None
            srv = mcp_has(servers, meta["mcp_server"]) if meta.get("mcp_server") else None
            backend_ok = out["backends"][cap]["ok"]
            mcp_only = not meta.get("skill")

            # An MCP-only organ capability is only usable if the agent actually
            # CONFIGURES that server. Scoring it "present" just because the daemon is
            # up would mark an agent with no MCP config at all as LIVE — a false green
            # (caught 2026-09-16). For those, wiring is the gate.
            if mcp_only:
                if servers is None:
                    state = "N/A"              # agent has no MCP surface
                elif srv and backend_ok is True:
                    state = "LIVE"
                elif srv and backend_ok is False:
                    state = "PARTIAL"
                elif srv:
                    state = "PRESENT"
                else:
                    state = "ABSENT"           # daemon up, but this agent can't reach it
            elif not present and not srv:
                state = "ABSENT"
            elif present and backend_ok is True:
                state = "LIVE"
            elif present and backend_ok is False:
                state = "PARTIAL"
            elif present:
                state = "PRESENT"       # no probe defined -> honest about it
            elif srv:
                state = "ONLY_MCP_CONFIG"
            else:
                state = "ABSENT"
            rows[cap] = {"state": state, "skill": where or None, "mcp": srv}
        out["agents"][name] = rows
    return out


def print_table(rep: dict) -> None:
    caps = list(CAPABILITIES)
    print(f"FEDERATION CAPABILITY AUDIT · {rep['ts']}\n")
    print("BACKENDS (live probes)")
    for cap, b in rep["backends"].items():
        mark = {True: "LIVE   ", False: "DOWN   ", None: "n/a    "}[b["ok"]]
        print(f"  {mark} {cap:34s} {b['detail']}")
    print()
    hdr = f"  {'agent':14s}" + "".join(f"{c[:22]:24s}" for c in caps)
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    for name, rows in rep["agents"].items():
        line = f"  {name:14s}"
        for c in caps:
            st = rows[c]["state"]
            mark = {"LIVE": "LIVE", "PRESENT": "present", "PARTIAL": "PARTIAL",
                    "ABSENT": "-", "ONLY_MCP_CONFIG": "cfg-only", "N/A": "n/a"}[st]
            line += f"{mark:24s}"
        print(line)
    print("\n  LIVE=artifact+backend verified · present=no probe defined · "
          "PARTIAL=backend down · cfg-only=in config, no skill · -=absent")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--drift", action="store_true")
    a = ap.parse_args()
    rep = audit()

    if a.json:
        print(json.dumps(rep, indent=1))
    elif a.drift:
        gaps = []
        for agent, rows in rep["agents"].items():
            for cap, r in rows.items():
                if r["state"] in ("ABSENT", "PARTIAL", "ONLY_MCP_CONFIG"):
                    gaps.append(f"{agent:14s} {cap:34s} {r['state']}")
        print("\n".join(gaps) if gaps else "no drift")
    else:
        print_table(rep)

    gaps = sum(1 for rows in rep["agents"].values() for r in rows.values()
               if r["state"] in ("ABSENT", "PARTIAL", "ONLY_MCP_CONFIG"))
    return 1 if gaps else 0


if __name__ == "__main__":
    sys.exit(main())
