import json, urllib.request, urllib.error
URL = "http://127.0.0.1:8088/mcp"
SID = "SEAL-P2-PROBE-2026-10-06"
META = {"io.modelcontextprotocol/protocolVersion": "2026-07-28", "io.modelcontextprotocol/clientCapabilities": {}}
def call(tool, arguments):
    body = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": tool, "arguments": arguments, "_meta": META}}
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream", "MCP-Protocol-Version": "2026-07-28", "Mcp-Method": "tools/call", "X-ArifOS-Actor": "arif", "mcp-session-id": SID, "Mcp-Name": tool}
    req = urllib.request.Request(URL, json.dumps(body).encode(), headers)
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return {"ok": True, "data": json.loads(resp.read())}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "body": e.read().decode()[:200]}
    except Exception as e:
        return {"ok": False, "exc": str(e)}

results = {}
for tool, args_list in [
    ("arif_critique", [{}, {"candidate": "test"}, {"candidate": "test", "target": "test"}]),
    ("arif_compose", [{}, {"message": "test"}, {"message": "test", "style": "plain"}]),
    ("arif_kernel_intercept", [{}, {"constitutional_chain_id": "test"}]),
    ("arif_measure", [{}, {"mode": "health"}]),
    ("arif_ops_measure", [{}, {"mode": "health"}]),
    ("arif_triage", [{}, {"intent": "test"}]),
    ("arif_bridge_connect", [{}, {"intent": "test"}]),
    ("wealth_dscr_leverage", [{}]),
    ("wealth_emv_downside", [{}]),
    ("wealth_irr_yield", [{}]),
    ("wealth_npv_reward", [{}]),
]:
    results[tool] = [call(tool, args) for args in args_list]

print(f'{"tool":30s} {"#ok":5s} {"#err":5s} verdict')
for tool, calls in results.items():
    ok = sum(1 for c in calls if c.get('ok') and not c.get('data',{}).get('result',{}).get('isError'))
    err = len(calls) - ok
    verdicts = []
    for c in calls:
        if c.get('ok'):
            r = c.get('data',{}).get('result',{})
            if r.get('isError'):
                content = r.get('content',[])
                for ct in content:
                    if isinstance(ct, dict):
                        t = ct.get('text','')
                        if 'Unknown tool' in t: verdicts.append('UNKNOWN')
                        elif 'missing' in t.lower(): verdicts.append('missing-arg')
                        else: verdicts.append(t[:40])
                        break
                else: verdicts.append('isError')
            else: verdicts.append('OK')
        else: verdicts.append('EXC')
    print(f'{tool:30s} {ok:5d} {err:5d} {verdicts}')