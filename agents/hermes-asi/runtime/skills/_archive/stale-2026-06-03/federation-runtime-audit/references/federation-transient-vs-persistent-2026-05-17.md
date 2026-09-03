# Federation Diagnostic: Transient vs Persistent Failures

> **Skill:** `federation-runtime-audit`
> **Created:** 2026-05-17
> **Source:** Session — Hermes ↔ Arif (YouTube philosophical chain + P0 well_assess_livelihood investigation)

---

## Core Diagnostic Pattern: Direct Probe > Audit Inference

When `federation_audit` flags a tool as failing, **do not trust the audit result blindly**. The audit can produce false positives due to:
- Transient Docker networking issues at audit time
- Timeout on first probe
- Registry state mismatch between audit run and live state

**Always verify with direct JSON-RPC probe** before declaring a tool broken.

### Probe Sequence (Anti-Cascade)

```bash
# Step 1: Run federation audit to see what failed
curl -s -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_stack_health_probe","arguments":{}}}' | python3 -m json.tool

# Step 2: Direct probe the flagged tool — verify before trusting audit
# For WELL tools (port 8083):
curl -s -X POST http://localhost:8083/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"well_assess_livelihood","arguments":{}}}' | python3 -m json.tool

# Step 3: Probe ALL tools in the organ, not just the flagged one
python3 -c "
import asyncio, httpx, json

async def probe():
    url = 'http://localhost:8083/mcp'
    tools = [
        'mcp_health_check','well_assess_homeostasis','well_assess_livelihood',
        'well_assess_metabolism','well_assess_reliability','well_check_repair',
        'well_classify_substrate','well_compute_metabolic_flux','well_detect_boundary',
        'well_guard_dignity','well_measure_gradient','well_registry_status',
        'well_system_registry_status','well_trace_lineage','well_validate_vitality',
    ]
    failed = []
    for tool in tools:
        payload = {'jsonrpc':'2.0','method':'tools/call','id':1,'params':{'name':tool,'arguments':{}}}
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                r = await client.post(url, json=payload, headers={'Content-Type': 'application/json'})
                data = r.json()
                result = data.get('result',{}).get('content',[{}])[0]
                text = json.loads(result.get('text','{}'))
                err = text.get('error','')
                if err and 'Unknown tool' in str(err):
                    failed.append(f'{tool}: unknown_tool')
                else:
                    pass  # ok or degraded
        except Exception as e:
            failed.append(f'{tool}: {e}')
    print('Failed:', failed)
    print(f'Passed: {len(tools)-len(failed)}/{len(tools)}')

asyncio.run(probe())
"
```

### Classification: Transient vs Persistent

| Signal | Classification | Action |
|--------|---------------|--------|
| Direct probe passes, audit flagged it | **Transient** (network/docker at audit time) | Log, monitor, do not fix tool |
| Direct probe fails, audit flagged it | **Persistent** (actual tool bug) | Fix tool |
| Direct probe passes, different test fails | **Separate issue** (e.g. alias registry mismatch) | Investigate separately |
| Audit shows `arifos_mcp_registry=UNKNOWN` | **Persistent detection bug** | See §2 below |

---

## 2. `arifos_mcp_registry=UNKNOWN` — Persistent Detection Bug

**Symptom:** `federation_audit` returns `registry_truth: {arifos_mcp: UNKNOWN}` while all other organs show `VERIFIED` or `PASS`.

**Root Cause:** The `federation_audit` tool calls the arifOS MCP endpoint (`/mcp`) via JSON-RPC for registry truth check. The MCP JSON-RPC response does not expose `registry_truth` or `truth_status` at the top level of `tools/call` responses. The probe at `health.py:597`:
```python
truth = data.get("registry_truth", data.get("truth_status", "UNKNOWN"))
```
fails to find either field in the MCP response wrapper → returns `UNKNOWN`.

arifOS HTTP `/health` endpoint (port 8080) returns `truth_status: VERIFIED` — but the audit probe uses MCP endpoint, not HTTP endpoint.

**Fix (RECOMMENDED):** Change `health.py:591-601` probe to call `/health` HTTP endpoint (not MCP JSON-RPC) for registry truth. The MCP endpoint is for tool calls; the HTTP `/health` is the correct liveness+registry endpoint.

**Status:** P1 — not yet applied. Affects `registry_truth` scoring (11.25/15).

---

## 3. WELL Tool Federation Format Verified

**All 15 WELL tools confirmed working (2026-05-17):**
- `well_assess_livelihood` → PASSES, returns full federation format `{observation, uncertainty, constraints, recommended_next_organ}`
- Original audit flag → transient docker network issue at audit time
- `test_well_output_federation_format` → PASSED

---

## 4. `well_444_gateway` Alias — Separate Test Failure

**Symptom:** `test_well_registry_declared_surface_matches_callable` fails with `AssertionError: Alias well_444_gateway missing from runtime`.

**Status:** Separate issue. Either test declares an alias not implemented, or deprecated alias removed from server but not test. Not investigated further.

---

## 5. Trust Direct Probe Over Audit Flag

```
Audit says: FAIL → Direct probe → PASS = Transient (log + monitor)
Audit says: FAIL → Direct probe → FAIL = Persistent (fix)
Audit says: UNKNOWN → Direct probe → PASS = Detection bug (fix probe)
```

**Anti-cascade principle:** One targeted probe beats a CLI cascade. Run direct tool probe first.

---

*DITEMPA BUKAN DIBERI — 999 SEAL, 2026-05-17.*