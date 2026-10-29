#!/usr/bin/python3
"""FED typed-contract pilot — calls the 6 read/compute-safe FED tools, captures raw evidence.

fed_report_latency is NOT called: its own description says it writes to the route_latency
table ("populate route_latency table with live telemetry") -> OBSERVATION_NOT_EXECUTED.

Output: /tmp/opencode/mission/fed-pilot-raw.json
"""

import json
import urllib.request

URL = "http://127.0.0.1:7074/mcp"
H = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}
INIT = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "333-AGI-fed-pilot", "version": "1.0-candidate"},
    },
}
NOTIF = {"jsonrpc": "2.0", "method": "notifications/initialized"}

CALLS = {
    "fed_health": {},
    "fed_status": {},
    "fed_probe": {},
    "fed_classify": {"task": "propose a constitutional verdict for a vault seal"},
    "fed_contrast": {"route_a": "deepseek-v4-pro", "route_b": "MiniMax-M3"},
    "fed_route": {
        "task": "summarize a legal filing",
        "constitutional_tier": "advisory",
    },
}


def post(payload, sid=None, timeout=30):
    h = dict(H)
    if sid:
        h["mcp-session-id"] = sid
    r = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers=h)
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        return resp.headers.get("mcp-session-id"), resp.read().decode()


def env(body):
    for line in reversed(body.strip().split("\n")):
        line = line[5:].strip() if line.startswith("data:") else line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return {}


sid, body = post(INIT)
init_env = env(body)
try:
    post(NOTIF, sid)
except Exception:
    pass

# also re-list tools here so the pilot evidence is self-contained
_, body = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, sid)
tools = env(body).get("result", {}).get("tools", [])

out = {
    "probed_at": None,
    "server": init_env.get("result", {}).get("serverInfo"),
    "tools_list": tools,
    "calls": {},
}
for name, args in CALLS.items():
    try:
        _, body = post(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": name, "arguments": args},
            },
            sid,
        )
        e = env(body)
        res = e.get("result", e)
        out["calls"][name] = {
            "arguments": args,
            "raw_result": res,
            "isError": res.get("isError"),
            "structuredContent": res.get("structuredContent"),
            "content_text": (res.get("content") or [{}])[0].get("text", "")[:4000]
            if isinstance(res.get("content"), list)
            else None,
        }
        print(f"called {name}: isError={res.get('isError')} keys={list(res)[:8]}")
    except Exception as ex:
        out["calls"][name] = {
            "arguments": args,
            "error": f"{type(ex).__name__}: {ex}"[:300],
        }
        print(f"called {name}: EXCEPTION {type(ex).__name__}")

json.dump(
    out,
    open("/tmp/opencode/mission/fed-pilot-raw.json", "w"),
    indent=1,
    ensure_ascii=False,
)
print("wrote /tmp/opencode/mission/fed-pilot-raw.json")
