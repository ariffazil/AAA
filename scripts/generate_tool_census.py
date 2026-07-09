import json
import os
import sys
import time
import urllib.request
import urllib.error
import yaml

BEARER_PATH = "/root/.secrets/aaa-identity/agentmesh.token"
MCP_PROTOCOL = "2025-11-25"
INIT_TIMEOUT = 5.0

PORTS = {
    "arifOS": 8088,
    "A-FORGE": 7072,
    "GEOX": 8081,
    "WEALTH": 18082,
    "WELL": 18083,
}

def load_bearer_token():
    if os.path.exists(BEARER_PATH):
        with open(BEARER_PATH, "r") as f:
            return f.read().strip()
    return ""

def http_post_with_headers(url, payload, token="", extra_headers=None):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Mcp-Protocol-Version": MCP_PROTOCOL,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if extra_headers:
        headers.update(extra_headers)
        
    req = urllib.request.Request(url, headers=headers, data=json.dumps(payload).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=INIT_TIMEOUT) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            resp_headers = resp.headers
            return resp_data, resp_headers
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} for {url} - {e.read().decode('utf-8', errors='ignore')}")
        raise e

def query_tools(organ, port, token):
    url = f"http://localhost:{port}/mcp"
    print(f"Querying tools for {organ} on port {port}...")
    
    # 1. Initialize Handshake
    init_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": MCP_PROTOCOL,
            "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
            "clientInfo": {"name": "tool_census_generator", "version": "1.0.0"},
        }
    }
    init_res, resp_headers = http_post_with_headers(url, init_payload, token)
    if "error" in init_res:
        raise ValueError(f"Init error: {init_res['error']}")
        
    # Get session ID from headers or result
    session_id = resp_headers.get("Mcp-Session-Id") or resp_headers.get("mcp-session-id")
    if not session_id and "result" in init_res:
        # Check if session ID is inside the result meta or serverInfo
        session_id = init_res["result"].get("meta", {}).get("sessionId")
        
    extra_headers = {}
    if session_id:
        extra_headers["Mcp-Session-Id"] = session_id
        print(f"  Bound session ID: {session_id[:8]}...")
    else:
        # Fallback: if no session ID header returned, try using a dummy or let it slide
        print("  Warning: No session ID returned in initialize response headers.")
        
    # 2. tools/list Request
    list_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    list_res, _ = http_post_with_headers(url, list_payload, token, extra_headers)
    if "error" in list_res:
        raise ValueError(f"List error: {list_res['error']}")
        
    return list_res.get("result", {}).get("tools", [])

def classify_tool(name):
    name_lower = name.lower()
    if any(x in name_lower for x in ["seal", "record", "archive", "ledger", "vault_write"]):
        return "RECORD"
    if any(x in name_lower for x in ["shell", "execute", "sandbox_run", "systemctl", "docker", "filesystem", "lock", "pipeline_run", "git", "github", "postgres"]):
        if "dryrun" in name_lower or "preview" in name_lower or "check" in name_lower:
            return "PREPARE"
        return "EXECUTE"
    if any(x in name_lower for x in ["dryrun", "preview", "plan", "docket_prep", "prepare"]):
        return "PREPARE"
    if any(x in name_lower for x in ["evaluate", "audit", "scan", "check", "assess", "verify", "compare", "reason", "interpret", "predict", "compute", "calculate", "asymmetry", "confluence"]):
        return "ASSESS"
    return "READ"

def danger_class_tool(name, lane):
    name_lower = name.lower()
    if any(x in name_lower for x in ["shell", "execute", "systemctl", "docker", "postgres", "sandbox_run", "pipeline_run"]):
        return "BLACK"
    if any(x in name_lower for x in ["filesystem", "lock", "git", "github", "vault_write"]):
        return "RED"
    if any(x in name_lower for x in ["boundary", "survival", "collapse", "dignity", "judge_handoff"]):
        return "ORANGE"
    if lane == "ASSESS" or any(x in name_lower for x in ["compute", "evaluate", "analyse", "parse"]):
        return "YELLOW"
    return "GREEN"

def main():
    token = load_bearer_token()
    census = {
        "census_metadata": {
            "version": "1.0.0",
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "owner": "arifOS Federation Control Plane / AAA",
        },
        "tools": []
    }
    
    for organ, port in PORTS.items():
        try:
            tools = query_tools(organ, port, token)
            print(f"Retrieved {len(tools)} tools for {organ}.")
            for t in tools:
                name = t.get("name")
                desc = t.get("description", "")
                lane = classify_tool(name)
                danger = danger_class_tool(name, lane)
                
                census["tools"].append({
                    "name": name,
                    "organ": organ,
                    "lane": lane,
                    "mutation": lane == "EXECUTE" or lane == "RECORD",
                    "authority_required": "F13_REQUIRED" if danger in ["RED", "BLACK"] else "OBSERVE_ONLY" if lane == "READ" else "PREPARE_ONLY",
                    "evidence_layer": "VERIFIED_STATE" if lane == "RECORD" else "CACHED_STATE",
                    "ttl_seconds": 300 if lane == "READ" else None,
                    "runtime_callable": True,
                    "deprecated": False,
                    "replacement": None,
                    "danger_class": danger,
                    "description": desc,
                })
        except Exception as e:
            print(f"Error querying {organ}: {e}")
            
    output_path = "/root/AAA/docs/tool_census.yaml"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(census, f, sort_keys=False, indent=2)
    print(f"Successfully generated tool census at {output_path}")

if __name__ == "__main__":
    main()
