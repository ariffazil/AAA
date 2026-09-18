# 05 — session_enforcement falsification probe — diagnosis witness

> Status: READ-ONLY diagnostic. No kernel mutation executed.
> Date: 2026-09-17 14:40 UTC
> Author: 333-AGI (this session)

## Probe attempts in this session

```
curl -sS --max-time 5 http://127.0.0.1:8088/kernel/readiness
   → curl: (28) Operation timed out after 5002 milliseconds with 0 bytes received

curl -X POST :8088/mcp
  -H 'content-type: application/json'
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"arif_kernel_readiness","arguments":{}}}'
   → "Unknown tool: 'arif_kernel_readiness'"

curl -X POST :8088/mcp
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"arif_observe","arguments":{"surface":"kernel","topic":"readiness"}}}'
   → "Unexpected keyword argument [type=unexpected_keyword_argument,
       input_value='kernel', input_type=str]"  (pydantic)

curl -X POST :8088/mcp
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"arif_forge","arguments":{"topic":"kernel_readiness"}}}'
   → "Unexpected keyword argument [type=unexpected_keyword_argument,
       input_value='kernel_readiness', input_type=str]"  (pydantic)
```

## Code witness (read-only)

`/opt/arifos/current/venv/lib/python3.13/site-packages/arifosmcp/runtime/reality_scoring.py`

```python
def probe_mcp_session_enforcement() -> tuple[bool, str]:
    try:
        import http.client
        conn = http.client.HTTPConnection("127.0.0.1", 8088, timeout=5)   # line 187
        body = '{"jsonrpc":"2.0","id":99,"method":"tools/list"}'
        conn.request("POST", "/mcp", body=body,
                     headers={"Content-Type": "application/json",
                              "Accept": "application/json"})                # line 193 (NO text/event-stream)
        resp = conn.getresponse()
        status = resp.status
        data = json.loads(resp.read().decode())                             # line 197
        conn.close()
        if status == 400:
            return True, "session_enforcement_400"
        err = data.get("error", {}).get("message", "")
        if "session" in err.lower():
            return True, "session_enforcement_active"
        return False, f"bypassed: HTTP_{status}_{err[:50]}"
    except Exception as e:
        return False, f"probe_timeout: {str(e)[:60]}"                      # line 208 — broad except
```

## Diagnosis (F2 anti-shadow)

The probe is **broken by design** in three ways:

1. **No SSE accept header** — kernel MCP wants `application/json, text/event-stream` per the 2026-07-28 conformance matrix; sending only `application/json` can stall.
2. **No `initialize` handshake** — `tools/list` raw against a strict MCP server hangs or 400s. Probe expects 400; server may return something else.
3. **Broad `except Exception` masks real failure modes** as `"probe_timeout"`. The kernel calls this routine during readiness scoring; every failing variant looks identical to the readiness consumer.

## Why no patch this turn

`/opt/arifos/venv/lib/python3.13/site-packages/arifosmcp/runtime/reality_scoring.py` is **production kernel** (release `v2026.08.01`). A behavior change to a constitutional probe is F13-gated. The manifest P2-002 marks `f13_sovereignty: AUTHORED` — but where doctrine says AUTHORED and the artifact targets production, I record HOLD pending sovereign sign on the patch in `/root/FORGE-musyawawah-gotong/proposals/T-017-session-enforcement-probe-fix.md`.

## What can run today with no risk

```
cd /opt/arifos/current/venv
python -c "from arifosmcp.runtime.reality_scoring import probe_mcp_session_enforcement; print(probe_mcp_session_enforcement())"
```

This re-runs the current probe — predictably `(False, 'probe_timeout: ...')` until the patch lands. Reversible, no production effect.

## Shadow

- `/opt/arifos/venv/bin/python3` (different venv) reported broken in earlier session per manifest shadow — not re-probed this session.
- `kernel/readiness` handler at `server.py:2988` does not itself timeout-bounded per probe — the 5 s observed may come entirely from the inner `timeout=5` argument.
- Probe interaction with `Accept: text/event-stream` not tested against the live kernel — would require kernel-side restart.
