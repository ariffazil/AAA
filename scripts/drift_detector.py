#!/usr/bin/env python3
"""Drift detector — reality <-> cards <-> wiki convergence check.
L4 lever: makes manual trinity passes unnecessary. Exit 1 on drift."""
import json, subprocess, urllib.request, sys, pathlib, re

def http_json(url, timeout=10, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode()

def tool_count(base):
    try:
        raw = http_json(f"{base}/mcp", data=json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}).encode())
        return len(json.loads(raw)["result"]["tools"])
    except Exception:
        pass
    try:
        import urllib.error
        req = urllib.request.Request(f"{base}/mcp", data=json.dumps({"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"drift-detector","version":"1.0"}}}).encode(), headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream"}, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            sid = r.headers.get("mcp-session-id") or r.headers.get("Mcp-Session-Id")
            r.read()
        if not sid:
            return None
        raw = http_json(f"{base}/mcp", data=json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}).encode(), headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream","Mcp-Session-Id":sid})
        return len(json.loads(raw)["result"]["tools"])
    except Exception:
        return None

def health(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status
    except Exception:
        return None

drift = []
# 1. Live tool counts vs wiki api.md claims
WIKI = pathlib.Path("/root/wiki/docs/api.md")
if WIKI.exists():
    wt = WIKI.read_text()
    for host, label in [("https://mcp","arifOS"),("https://geox","GEOX"),("https://wealth","WEALTH"),("https://well","WELL")]:
        m = re.search(rf"### {label}[^()]*\((\d+)[^)]*tools?\)", wt)
        claimed = int(m.group(1)) if m else None
        live = tool_count(host + ".arif-fazil.com")
        if live is not None and claimed is not None and live != claimed:
            drift.append(f"COUNT {label}: wiki={claimed} live={live}")
        if live is None:
            drift.append(f"UNREACHABLE {label} tools/list")
# 2. Kernel health
if health("http://127.0.0.1:8088/health") != 200:
    drift.append("KERNEL :8088 health != 200")
# 3. Fleet: reality.json nodes present
try:
    fleet = json.loads(pathlib.Path("/run/arifos/reality.json").read_text())
    nodes = {n["node_name"] for n in fleet["identity"]["fleet"]}
    need = {"court-core","forge-core","flow-dmz"}
    if not need.issubset(nodes):
        drift.append(f"FLEET missing: {need - nodes}")
except Exception as e:
    drift.append(f"REALITY.JSON unreadable: {e}")
# 4. CCC pool card harness count vs ccc-remote cases
try:
    card = json.loads(pathlib.Path("/root/AAA/a2a-server/agent-cards/harnesses/kvm4-ccc-pool.json").read_text())
    card_h = set(card.get("harnesses", {}))
    remote = pathlib.Path("/usr/local/bin/ccc-remote").read_text()
    for h in card_h:
        if h not in remote:
            drift.append(f"CCC harness {h} in card but not in ccc-remote")
except Exception as e:
    drift.append(f"CCC card check fail: {e}")

print(f"[drift-detector] {len(drift)} drift item(s)")
for d in drift:
    print(f"  DRIFT: {d}")
if not drift:
    print("  ALL CONVERGED (wiki=fleet=cards=kernel)")
sys.exit(1 if drift else 0)
