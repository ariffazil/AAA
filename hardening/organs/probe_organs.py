#!/usr/bin/env python3
"""
probe_organs.py — READ-ONLY live probe of the arifOS federation TOOLS & ORGANS layer.

Purpose : determine what is actually REACHABLE vs DECLARED-BUT-DEAD on this host.
Method  : (1) enumerate listening TCP sockets + owning cmdline
          (2) HTTP health probe of every organ port (401/403 => UP-AUTH)
          (3) MCP JSON-RPC tools/list probe of every declared /mcp endpoint
          (4) MCP server inventory from Hermes config + registry (read-only)
Writes  : probe_organs_raw.json (next to this file) + human table on stdout
Safety  : opens sockets and sends GET/initialize+tools/list ONLY.
          No mutation, no service restart, no config write, no docker action.
Usage   : python3 /root/AAA/hardening/organs/probe_organs.py
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

TIMEOUT = 6.0
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- organ table
# (label, host, port, [health paths to try in order], declared-by)
ORGANS = [
    ("arifOS kernel (judge)",   "127.0.0.1", 8088, ["/health", "/healthz"],        "registry mcp-servers.yaml organs.kernel"),
    ("A-FORGE exec server",     "127.0.0.1", 7071, ["/health"],                     "MACHINE_MAP §1 A-FORGE :7071"),
    ("A-FORGE MCP",             "127.0.0.1", 7072, ["/health"],                     "registry organs.aforge"),
    ("arifFlow daemon (REST)",  "127.0.0.1", 7073, ["/health"],                     "registry organs.arifflow"),
    ("FED fed-router",          "0.0.0.0",   7074, ["/health", "/healthz"],         "registry organs.fed (MCP http)"),
    ("arifFlow MCP (fastmcp)",  "127.0.0.1", 7075, ["/health"],                     "live ss: arifflow_mcp_fastmcp.py"),
    ("GEOX MCP",                "127.0.0.1", 8081, ["/health"],                     "registry organs.geox"),
    ("WEALTH MCP",              "127.0.0.1", 18082, ["/health"],                    "registry organs.wealth"),
    ("WELL organ",              "127.0.0.1", 18083, ["/health"],                    "registry organs.well"),
    ("SIGNAL organ",            "127.0.0.1", 18084, ["/health"],                    "live ss: signal_organ.main"),
    ("FRAME organ",             "127.0.0.1", 18085, ["/health"],                    "registry organs.frame"),
    ("FRAME MCP (fastmcp)",     "127.0.0.1", 18086, ["/health"],                    "live ss: frame_mcp_fastmcp.py"),
    ("AAA a2a-server",          "127.0.0.1", 3001, ["/health", "/", "/.well-known/agent-card.json"], "registry organs.aaa / MACHINE_MAP AAA :3001"),
    ("AAA MCP (fastmcp)",       "127.0.0.1", 3002, ["/health"],                     "live ss: aaa_mcp_fastmcp.py"),
    ("1mcp aggregator",         "127.0.0.1", 3050, ["/health"],                     "live ss: 1mcp serve"),
    ("playwright-mcp",          "127.0.0.1", 8931, ["/health"],                     "live ss: playwright-mcp"),
    ("FED intake (HAProxy)",    "127.0.0.1", 4000, ["/health/liveliness", "/health"], "MACHINE_MAP §3 trap: /health = 000"),
    ("FED clamp (HAProxy)",     "127.0.0.1", 4012, ["/health/liveliness", "/health"], "MACHINE_MAP §1 :4012"),
    ("litellm (model brain)",   "127.0.0.1", 4013, ["/health", "/health/liveliness"], "live ss: litellm --port 4013"),
    ("fed-aware-middleware",    "127.0.0.1", 4010, ["/health"],                     "MACHINE_MAP §1 :4010"),
    ("i-ARIF (REST claim)",     "127.0.0.1", 18095, ["/health"],                    "registry organs.iarif claims 18095"),
    ("apa-github-bridge",       "127.0.0.1", 18095, ["/health"],                    "MACHINE_MAP §1 corrected :18095 = apa-github-bridge"),
    ("gmail_bridge",            "127.0.0.1", 18097, ["/health"],                    "live ss: gmail_bridge.py"),
    ("gws_bridge",              "127.0.0.1", 18098, ["/health"],                    "live ss: gws_bridge.py"),
    ("drive_bridge",            "127.0.0.1", 18099, ["/health"],                    "live ss: drive_bridge.py"),
    ("gemini_bridge",           "127.0.0.1", 18092, ["/health"],                    "live ss: gemini_bridge.py"),
    ("email_bridge",            "127.0.0.1", 18093, ["/health"],                    "live ss: email_bridge.py"),
    ("calendar_bridge",         "127.0.0.1", 18094, ["/health"],                    "live ss: calendar_bridge.py"),
    ("sheets_bridge",           "127.0.0.1", 18075, ["/health"],                    "live ss: sheets_bridge.py"),
    ("signing_server",          "127.0.0.1", 18900, ["/health"],                    "live ss: AAA/auth/signing_server.py"),
    ("vault999-writer",         "127.0.0.1", 5001,  ["/health"],                    "live ss: vault999-writer/main.py"),
    ("l5_search_api",           "127.0.0.1", 8001,  ["/health"],                    "live ss: arifosmcp.runtime.l5_search_api"),
    ("hermes-prod health",      "127.0.0.1", 18791, ["/health"],                    "live ss: hermes-health.py"),
    ("forge-bot",               "127.0.0.1", 8091,  ["/health"],                    "live ss: /opt/forge-bot/bot.py"),
    ("headscale (mesh)",        "127.0.0.1", 50443, ["/health"],                    "live ss: headscale serve"),
    ("hermes a2a platform",     "127.0.0.1", 9900,  ["/health", "/"],               "~/.hermes/config.yaml platforms.a2a"),
    ("netdata",                 "127.0.0.1", 19999, ["/api/v1/info"],               "live ss: netdata"),
    ("prometheus",              "127.0.0.1", 9090,  ["/-/healthy"],                 "live ss: prometheus"),
    ("grafana",                 "127.0.0.1", 3000,  ["/api/health"],                "live ss: grafana"),
    ("ollama",                  "127.0.0.1", 11434, ["/api/tags"],                  "live ss: ollama serve"),
    ("qwen/llama-server",       "127.0.0.1", 42555, ["/health", "/v1/models"],      "live ss: llama-server"),
]

# MCP JSON-RPC endpoints (declared + discovered HTTP/streamable surfaces)
MCP_ENDPOINTS = [
    ("arifos",     "127.0.0.1", 8088,  "/mcp", "registry organs.kernel + hermes config: url http://127.0.0.1:8088/mcp"),
    ("aforge",     "127.0.0.1", 7072,  "/mcp", "registry organs.aforge (hermes uses stdio, not this http)"),
    ("fed",        "127.0.0.1", 7074,  "/mcp", "registry organs.fed + hermes config: url http://127.0.0.1:7074/mcp"),
    ("geox",       "127.0.0.1", 8081,  "/mcp", "registry organs.geox + hermes config: url http://127.0.0.1:8081/mcp"),
    ("wealth",     "127.0.0.1", 18082, "/mcp", "registry organs.wealth + hermes config 18082"),
    ("well",       "127.0.0.1", 18083, "/mcp", "registry organs.well + hermes config 18083"),
    ("arifflow",   "127.0.0.1", 7075,  "/mcp", "live fastmcp arifflow_mcp_fastmcp.py (hermes uses stdio)"),
    ("frame",      "127.0.0.1", 18086, "/mcp", "live fastmcp frame_mcp_fastmcp.py (NOT in hermes config)"),
    ("aaa",        "127.0.0.1", 3002,  "/mcp", "live fastmcp aaa_mcp_fastmcp.py (NOT in hermes config)"),
    ("1mcp-agg",   "127.0.0.1", 3050,  "/mcp", "live 1mcp aggregator"),
    ("playwright", "127.0.0.1", 8931,  "/mcp", "live playwright-mcp"),
]


# ---------------------------------------------------------------- primitives
def tcp_open(host, port, timeout=2.0):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        return True
    except Exception:
        return False
    finally:
        s.close()


def http_probe(host, port, path, method="GET", body=None, headers=None,
               timeout=TIMEOUT, max_bytes=4000):
    """Return dict with raw evidence: status, error, body excerpt, elapsed_ms."""
    url = "http://%s:%d%s" % (host, port, path)
    req = urllib.request.Request(url, data=body, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    t0 = time.time()
    out = {"url": url, "method": method, "status": None, "error": None,
           "body_excerpt": None, "elapsed_ms": None, "headers": {}}
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(max_bytes)
            out["status"] = resp.status
            out["headers"] = {k.lower(): v for k, v in resp.headers.items()}
            out["body_full"] = raw.decode("utf-8", "replace")
            out["body_excerpt"] = out["body_full"][:400]
    except urllib.error.HTTPError as e:
        raw = b""
        try:
            raw = e.read(max_bytes)
        except Exception:
            pass
        out["status"] = e.code
        out["headers"] = {k.lower(): v for k, v in (e.headers or {}).items()}
        out["body_full"] = raw.decode("utf-8", "replace")
        out["body_excerpt"] = out["body_full"][:400]
    except Exception as e:
        out["error"] = "%s: %s" % (type(e).__name__, e)
    out["elapsed_ms"] = int((time.time() - t0) * 1000)
    return out


def verdict_from(status, error):
    """Doctrine: 401/403 => UP-AUTH. conn-refused/timeout => DOWN."""
    if error:
        if "refused" in error.lower() or "timed out" in error.lower() or "timeout" in error.lower():
            return "DOWN"
        return "ERROR:" + error
    if status is None:
        return "DOWN"
    if status in (401, 403):
        return "UP-AUTH"
    if 200 <= status < 400:
        return "UP-OPEN"
    if status == 404:
        return "UP-OPEN(path-404)"
    if status == 405:
        return "UP-OPEN(405)"
    return "UP-OPEN(HTTP %s)" % status


def mcp_probe(host, port, path="/mcp", retry=True):
    """JSON-RPC initialize + tools/list. Read-only. Returns tool names/count or exact error.

    One retry: some streamable-http servers (GEOX observed) intermittently answer
    tools/list with HTTP 200 + empty body. A second full handshake resolves it.
    """
    payload = {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18",
                   "capabilities": {},
                   "clientInfo": {"name": "probe_organs", "version": "1.0"}},
    }
    hdrs = {"Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"}
    res = http_probe(host, port, path, method="POST",
                     body=json.dumps(payload).encode(), headers=hdrs,
                     max_bytes=4_000_000)
    out = {"endpoint": "http://%s:%d%s" % (host, port, path),
           "initialize_status": res["status"], "initialize_error": res["error"],
           "tool_count": None, "tools": [], "error": None}
    if res["error"] or res["status"] != 200:
        out["error"] = res["error"] or ("initialize HTTP %s: %s" % (res["status"], (res["body_excerpt"] or "")[:160]))
        return out
    # streamable-http may answer as SSE; extract JSON
    sid = res["headers"].get("mcp-session-id")
    txt = res.get("body_full") or ""
    if "data:" in txt:
        txt = "".join(l[5:].strip() for l in txt.splitlines() if l.startswith("data:"))
    try:
        init = json.loads(txt)
    except Exception as e:
        out["error"] = "initialize parse: %s | raw=%s" % (e, txt[:160])
        return out
    proto = init.get("result", {}).get("protocolVersion")
    out["protocol_version"] = proto
    out["server_info"] = init.get("result", {}).get("serverInfo")
    hdrs2 = dict(hdrs)
    if sid:
        hdrs2["mcp-session-id"] = sid
    # streamable-http servers (fastmcp/uvicorn) require the initialized notification
    # before tools/list, else they answer 400 "Server not initialized" or empty body.
    http_probe(host, port, path, method="POST",
               body=json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized",
                                "params": {}}).encode(),
               headers=hdrs2, max_bytes=200_000)
    lst = http_probe(host, port, path, method="POST",
                     body=json.dumps({"jsonrpc": "2.0", "id": 2,
                                      "method": "tools/list", "params": {}}).encode(),
                     headers=hdrs2, max_bytes=6_000_000)
    t2 = lst.get("body_full") or ""
    if "data:" in t2:
        t2 = "".join(l[5:].strip() for l in t2.splitlines() if l.startswith("data:"))
    try:
        d = json.loads(t2)
        tools = d.get("result", {}).get("tools", [])
        out["tool_count"] = len(tools)
        out["tools"] = [t.get("name") for t in tools]
    except Exception as e:
        out["error"] = "tools/list parse: %s | raw=%s (status=%s)" % (e, t2[:160], lst["status"])
    if out.get("tool_count") is None and retry:
        second = mcp_probe(host, port, path, retry=False)
        second["endpoint"] = out.get("endpoint")
        if second.get("tool_count") is not None:
            second["retry_note"] = "first attempt returned no tools/list body; second handshake succeeded"
            return second
        second["retry_note"] = "retried once; first attempt error: %s" % out.get("error")
        return second
    return out


def listening_sockets():
    """ss -ltnp -> [{port, addr, pid, cmdline}]"""
    try:
        raw = subprocess.run(["ss", "-ltnp"], capture_output=True, text=True, timeout=15).stdout
    except Exception as e:
        return [{"error": str(e)}]
    rows = []
    for line in raw.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 4:
            continue
        local = parts[3]
        proc = line.split("users:(", 1)[1] if "users:(" in line else ""
        pid = None
        m = re.search(r"pid=(\d+)", proc)
        if m:
            pid = int(m.group(1))
        cmd = None
        if pid:
            try:
                cmd = open("/proc/%d/cmdline" % pid, "rb").read().replace(b"\x00", b" ").decode("utf-8", "replace").strip()
            except Exception:
                cmd = None
        rows.append({"local": local, "pid": pid, "cmdline": cmd})
    return rows


def mcp_server_inventory():
    """Read-only inventory of configured MCP server names (Hermes config + any mcp*.json)."""
    inv = {"hermes_config_mcp_servers": [], "config_path": "/root/.hermes/config.yaml",
           "other_mcp_json_files": [], "minimax_media_mcp_present": False, "grep_evidence": []}
    cfg = "/root/.hermes/config.yaml"
    try:
        txt = open(cfg).read()
        blk = txt.split("\nmcp_servers:", 1)
        if len(blk) > 1:
            body = blk[1]
            for line in body.splitlines():
                if re.match(r"^  [a-z_][a-z0-9_\-]*:\s*$", line):
                    inv["hermes_config_mcp_servers"].append(line.strip().rstrip(":"))
                elif re.match(r"^\S", line):
                    break
    except Exception as e:
        inv["config_error"] = str(e)
    # search common locations for mcp json configs
    for root in ("/root/.hermes", "/root/AAA", "/root/.config"):
        try:
            out = subprocess.run(["find", root, "-maxdepth", "3", "-name", "mcp*.json",
                                  "-o", "-maxdepth", "3", "-name", "*mcp_servers*.json"],
                                 capture_output=True, text=True, timeout=20).stdout
            for f in [x for x in out.splitlines() if x.strip()]:
                inv["other_mcp_json_files"].append(f)
        except Exception:
            pass
    # does any configured server mention minimax/media as an MCP server?
    try:
        g = subprocess.run(["grep", "-niE", r"minimax|media|image|video|tts",
                            "/root/.hermes/config.yaml"], capture_output=True, text=True, timeout=15).stdout
        inv["grep_evidence"] = [l for l in g.splitlines() if "mcp" in l.lower() or "url:" in l][:20]
        inv["minimax_media_mcp_present"] = any(
            re.search(r"^\s*(minimax|media|image|video|tts)[a-z_\-]*:\s*$", l)
            for l in g.splitlines())
    except Exception:
        pass
    return inv


def main():
    started = datetime.now(timezone.utc).isoformat()
    report = {"probe_started_utc": started, "host": subprocess.run(["hostname"], capture_output=True, text=True).stdout.strip(),
              "host_tailscale_ip": "100.64.0.2 (from ss bind addresses)", "organs": [], "mcp_endpoints": [],
              "listening_sockets": [], "mcp_inventory": {}}

    print("=" * 100)
    print("ORGAN HTTP HEALTH PROBE  @ %s" % started)
    print("=" * 100)
    for label, host, port, paths, declared in ORGANS:
        entry = {"label": label, "host": host, "port": port, "declared_by": declared, "attempts": []}
        chosen = None
        for p in paths:
            r = http_probe(host, port, p)
            entry["attempts"].append({"path": p, "status": r["status"], "error": r["error"],
                                      "elapsed_ms": r["elapsed_ms"], "body_excerpt": r["body_excerpt"]})
            if r["status"] is not None:
                chosen = entry["attempts"][-1]
                break
        if chosen is None:
            chosen = entry["attempts"][-1]
        entry["verdict"] = verdict_from(chosen["status"], chosen["error"])
        entry["evidence"] = "curl %s -> %s" % (chosen.get("path") and ("http://%s:%d%s" % (host, port, chosen["path"])),
                                               chosen["status"] if chosen["status"] is not None else ("ERR " + str(chosen["error"])))
        report["organs"].append(entry)
        print("%-26s :%-6d %-16s %s" % (label, port, entry["verdict"], entry["evidence"]))

    print()
    print("=" * 100)
    print("MCP JSON-RPC PROBE (initialize + tools/list)  — read-only")
    print("=" * 100)
    for name, host, port, path, declared in MCP_ENDPOINTS:
        if not tcp_open(host, port):
            e = {"server": name, "endpoint": "http://%s:%d%s" % (host, port, path),
                 "verdict": "DOWN", "evidence": "tcp connect refused", "tool_count": None}
            report["mcp_endpoints"].append(e)
            print("%-12s %-28s DOWN            tcp connect refused" % (name, e["endpoint"]))
            continue
        r = mcp_probe(host, port, path)
        if r.get("tool_count") is not None:
            r["verdict"] = "UP-MCP"
            r["evidence"] = "initialize HTTP 200 proto=%s; tools/list -> %d tools" % (r.get("protocol_version"), r["tool_count"])
        elif r.get("initialize_status") == 200:
            # Handshake succeeded but tools/list came back unparseable/empty twice.
            # Seen intermittently on GEOX only. Handshake evidence stands; the list is inconclusive.
            r["verdict"] = "UP-MCP-HANDSHAKE-OK/LIST-EMPTY"
            r["evidence"] = ("initialize HTTP 200 proto=%s serverInfo=%s; tools/list EMPTY/UNPARSEABLE on both attempts (%s)"
                             % (r.get("protocol_version"), r.get("server_info"), (r.get("error") or "")[:120]))
        else:
            r["verdict"] = "DOWN"
            r["evidence"] = "initialize HTTP %s err=%s" % (r.get("initialize_status"), r.get("error"))
        r["server"] = name
        r["declared_by"] = declared
        report["mcp_endpoints"].append(r)
        print("%-12s %-28s %-19s %s" % (name, r["endpoint"], r["verdict"], r["evidence"]))
        if r.get("tools"):
            print("             tools: %s" % ", ".join(r["tools"][:40]))

    report["listening_sockets"] = listening_sockets()
    report["mcp_inventory"] = mcp_server_inventory()

    out = os.path.join(HERE, "probe_organs_raw.json")
    with open(out, "w") as f:
        json.dump(report, f, indent=2)
    print()
    print("raw evidence -> %s" % out)
    print("hermes config MCP servers: %s" % ", ".join(report["mcp_inventory"]["hermes_config_mcp_servers"]))
    print("minimax/media MCP server configured? %s" % report["mcp_inventory"]["minimax_media_mcp_present"])


if __name__ == "__main__":
    main()
