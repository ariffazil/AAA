# MCP Lifecycle Registry v1 — Spec (F13-stage, no build) — AMENDED

**Problem (per Arif audit 2026-10-03)**: connector advertise ≠ runtime accept. Schema/registry split-brain. Earlier "L4 = systemd" was a compile error — systemd is supervisor provenance, not L4 recovery.

**Solution**: 4-plane model. D = R = O = S. Plus 5-level health (L0-L4) + 1 supervisor dimension.

## 4 planes

```
MCP REALITY
  ├── DECLARATION PLANE  (connector schema, AAA registry, tool metadata)
  ├── RUNTIME PLANE      (initialize, tools/list, representative call)
  ├── SUBSTRATE PLANE     (process, supervisor, resource, recovery)
  └── OBSERVABLE PLANE    (5-level health + supervisor provenance)
```

## Per-MCP record (canonical)

```yaml
id: wealth

transport:
  type: streamable_http        # stdio | http | sse | streamable_http
  endpoint: http://127.0.0.1:18082/mcp
  protocol_version: "2024-11-05"  # observed

protocol:
  initialize_required: true      # must call initialize first
  session_header_required: true  # must capture MCP-Session-Id
  notifications_initialized: true # must send notifications/initialized
  probe_method: correct_handshake_v1  # canonical probe pattern

lifecycle:
  class: PERSISTENT_SERVICE       # PERSISTENT_SERVICE | PERSISTENT_CONTAINER | SESSION_STDIO | ON_DEMAND_WRAPPER | BRIDGED_STDIO
  supervisor: systemd            # systemd | docker | harness | wrapper | cron | manual | unknown
  unit: wealth-organ.service     # actual supervisor unit name
  restart_policy: always

authority:
  session_required: true
  actor_required: true
  auth_class: L11_AUTH          # from runtime reject message

surface:
  declared_hash: sha256:...     # canonical tool list at compile time
  registered_hash: sha256:...   # what runtime registers (initialize response)
  callable_hash: sha256:...     # tools/list response
  declared_count: 27
  registered_count: 27
  callable_count: 27

representative_call:
  tool: "geox_organ_status"      # one zero-side-effect call
  expected_schema: "registry_v1"
  observed_response: {...}

health:                          # 5-level + 1 supervisor dim
  l0_process: PASS
  l1_transport: PASS
  l2_initialize: PASS
  l3_representative: PASS|FAIL
  l4_recovery: UNMEASURED
  supervisor_provenance: systemd

truth:                           # Witness Coherence Gate
  status: COHERENT | DRIFT
  drift_class:                     # see table below
    - NONE
    - PHANTOM                  # declared, not callable
    - HIDDEN                   # callable, not declared
    - ABI_DRIFT                # name match, schema diff
    - AUTH_DRIFT               # auth contract diff
    - ALIAS_DRIFT              # alias → dead target
    - SCHEMA_REGISTRY_SPLIT    # like GEOX case

recovery:                       # L4 measurement
  tested_at: 2026-10-03T...
  method: kill_PID+restart+probe
  result: PASS|FAIL
```

## Health probe (canonical MCP handshake)

```python
def probe_mcp(url, timeout=3):
    """One canonical probe, 4 phases. Works for all HTTP-transport MCPs."""
    # Phase 1: initialize
    init_req = {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "fi005-probe", "version": "1.0"}
        }
    }
    init_resp = post(url, init_req, timeout)
    session_id = init_resp.headers.get("MCP-Session-Id") or init_resp.body.get("sessionId")

    # Phase 2: notifications/initialized
    notif_req = {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
    post(url, notif_req, session_id, timeout)

    # Phase 3: tools/list (preserve session)
    tools_resp = post(url, {"jsonrpc":"2.0","id":3,"method":"tools/list"}, session_id, timeout)
    tools = tools_resp.body.get("result",{}).get("tools",[])

    # Phase 4: representative zero-side-effect call (per organ)
    rep_call = choose_representative_call(url)  # per organ
    rep_resp = post(url, rep_call, session_id, timeout)

    return {
        "l0_process": check_pid(url),
        "l1_transport": check_tcp(url),
        "l2_initialize": init_resp.status == 200,
        "l3_representative": rep_resp.status == 200,
        "l4_recovery": kill_restart_verify(url),  # separate probe
        "supervisor": detect_supervisor(url),  # systemctl or docker
        "session_id_obtained": session_id is not None,
        "tools_count": len(tools),
    }
```

## Reversibility

`rm /root/AAA/docs/blueprints/MCP-LIFECYCLE-REGISTRY-SPEC-v1.md` (1 command).

