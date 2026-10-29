---
id: arifos-mcp-audit
name: arifos-mcp-audit
version: 1.0.0
description: 'Audit arifOS MCP surface for quality, entropy, and gaps. Enumerate tools, measure envelope sizes, check status fields, verify annotations, map gaps to fixes, deploy, verify. Use this skill whenever the arifOS MCP surface needs quality assessment — after any tool addition/removal, after schema changes, or as a periodic health check.'
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope: [F1, F2, F4, F11]
tags: [arifos, mcp, audit, entropy, quality, gap-map]
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- hermes
- kimi
- opencode
- claude-code
dependencies:
  servers:
    - arifOS :8088
  tools: []
examples:
- "Audit the arifOS MCP surface — what are the envelope sizes, status fields, and gaps?"
- "Run a full holy-8 smoke test against the deployed kernel"
- "Check if the latest commit improved envelope entropy"
- "Verify that annotations are present on all 8 canonical tools"
tests:
- "Enumerate all 8 tools with schemas and annotations"
- "Measure envelope sizes for each tool (target: <5KB minimal)"
- "Verify status field is 'completed' for all HOLD/VOID/SEAL verdicts"
- "Check that arif_think latency is <5s with mode=apex"
---

# ⚒️ arifos-mcp-audit — arifOS MCP Surface Quality Audit

> **Forged:** 2026-08-09 by Hermes for AAA Control Plane
> **Doctrine:** DITEMPA BUKAN DIBERI
> **Reference:** FORGE-mcp-probe (for general MCP probing)

## USE WHEN

The task involves:

- Auditing the arifOS MCP surface for quality, entropy, and gaps
- Verifying that recent commits improved (not regressed) the surface
- Checking envelope sizes, status fields, annotations, and latency
- Mapping gaps to fix-next items for the next sprint
- Periodic health checks of the holy-8 tools
- Pre-SEAL verification that the surface is clean

## DO NOT USE WHEN

- Probing a non-arifOS MCP server (use FORGE-mcp-probe instead)
- Building new MCP tools (use forge_ephemeral or arifOS dev docs)
- Testing MCP protocol conformance (use FORGE-mcp-testing + MCPJam)

## The Audit Protocol

### Phase 1: Surface Enumeration

```python
import json, urllib.request

URL = "http://127.0.0.1:8088/mcp"

# Initialize (stateless or stateful)
hdrs = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "MCP-Protocol-Version": "2025-11-25",
}
body = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-11-25", "capabilities": {},
                   "clientInfo": {"name": "audit", "version": "1.0"}}}
req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=hdrs, method="POST")
with urllib.request.urlopen(req, timeout=5) as r:
    init = json.loads(r.read().decode())
    sid = r.headers.get("Mcp-Session-Id")

# tools/list
hdrs["Mcp-Session-Id"] = sid
body = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=hdrs, method="POST")
with urllib.request.urlopen(req, timeout=10) as r:
    tools = json.loads(r.read().decode())["result"]["tools"]
    print(f"Tools: {len(tools)}")
    for t in tools:
        schema = t.get("inputSchema", {})
        props = schema.get("properties", {})
        ann = t.get("annotations", {})
        print(f"  {t['name']}: {len(props)} props, ro={ann.get('readOnlyHint')}, destr={ann.get('destructiveHint')}")
```

### Phase 2: Envelope Size Measurement

For each tool, call it and measure the response size:

```python
def measure_envelope(tool_name, args):
    body = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
            "params": {"name": tool_name, "arguments": args}}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=hdrs, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read().decode()
        ms = elapsed
        # Parse response
        data = json.loads(raw) if not raw.startswith("event:") else parse_sse(raw)
        sc = data.get("result", {}).get("structuredContent", {})
        return {"bytes": len(raw), "sc_keys": len(sc), "ms": ms}

# Measure all 8 tools
for name, args in smoke_tests:
    result = measure_envelope(name, args)
    print(f"{name}: {result['bytes']}B, {result['sc_keys']} SC keys, {result['ms']:.0f}ms")
```

**Targets (post-G3 fix):**
- Envelope: <5KB for most tools (was 6-12KB pre-fix)
- SC keys: <20 (was 25+ pre-fix)
- Latency: <1s for most tools, <5s for arif_think with mode=

### Phase 3: Status Field Verification

Check that `status=completed` for all finished tool calls (G1 fix):

```python
for name, args in smoke_tests:
    result = call_tool(name, args)
    sc = result["structuredContent"]
    status = sc.get("status", "?")
    exec_state = sc.get("execution_state", "?")
    effective = sc.get("effective_verdict", "?")
    
    # G1: status should NOT be pending when tool finished
    g1_pass = status not in ("pending",) or exec_state == "COMPLETED"
    print(f"{name}: status={status} exec={exec_state} verdict={effective} G1={'PASS' if g1_pass else 'FAIL'}")
```

### Phase 4: Annotation Check

Verify that all tools have `readOnlyHint` or `destructiveHint` (P13):

```python
for t in tools:
    ann = t.get("annotations", {})
    has_ro = "readOnlyHint" in ann
    has_destr = "destructiveHint" in ann
    if not has_ro and not has_destr:
        print(f"⚠️ {t['name']}: NO ANNOTATIONS (P13 fail)")
```

### Phase 5: arif_think Latency Matrix

Test latency with and without mode= (mode-dependent behavior):

```python
for mode in [None, "apex", "observe", "deep"]:
    args = {"query": "test"}
    if mode:
        args["mode"] = mode
    result = measure_envelope("arif_think", args)
    print(f"arif_think(mode={mode}): {result['ms']:.0f}ms")
```

**Expected:**
- mode=None: ~10s (LLM path)
- mode=apex/observe/deep: ~100ms (fast template)

### Phase 6: Health Cross-Check

Compare wire surface vs /health claims:

```python
with urllib.request.urlopen("http://127.0.0.1:8088/health", timeout=5) as r:
    health = json.loads(r.read().decode())

wire_count = len(tools)
health_loaded = health.get("tools_loaded")
health_registry = health.get("tools_registry_size")
health_ops = health.get("operational_tools")

print(f"Wire: {wire_count} | Loaded: {health_loaded} | Registry: {health_registry} | Ops: {health_ops}")
if wire_count != health_loaded:
    print(f"⚠️ Wire/loaded mismatch: {wire_count} vs {health_loaded}")
```

### Phase 7: Gap Map

Compile findings into a structured gap map:

```markdown
## Gap Map (YYYY-MM-DD)

| Pri | ID | Gap | Evidence | Fix | ΔS |
|-----|----|-----|----------|-----|-----|
| P0 | G1 | status=pending on success | every tool call | Split execution vs governance | High |
| P1 | G2 | memory 59 props | tools/list | Mode-gated schema | Med |
```

## Gap Categories

| Category | What to check | Target |
|----------|---------------|--------|
| **Status clarity** | status field vs execution_state | status=completed for all finished calls |
| **Envelope entropy** | Total bytes, SC key count | <5KB, <20 keys |
| **Latency** | Per-tool response time | <1s (except arif_think: <5s with mode=) |
| **Annotations** | readOnlyHint/destructiveHint present | 8/8 tools |
| **Schema complexity** | Props count per tool | Memory: <12 (mode-gated), others: <15 |
| **Facts population** | facts field in response | Synthesized from result, not null |
| **Health alignment** | Wire count vs health.tools_loaded | Must match |

## Entropy Targets

| Metric | Pre-fix (2026-08-08) | Post-fix (2026-08-09) | Target |
|--------|----------------------|----------------------|--------|
| init envelope | 9,568B | 4,218B | <5KB |
| observe envelope | 6-7KB | 3.7KB | <4KB |
| think latency (no mode) | 28-38s | ~10s | <5s |
| think latency (mode=apex) | n/a | ~100ms | <200ms |
| status on HOLD | pending | completed | completed |
| SC keys | 25 | 18 | <20 |
| operational_tools | 3/8 | 3/8 | ≥7/8 |

## Pitfalls

- **Don't trust the first probe.** Re-probe with fresh session_id and confirm results match.
- **Surface health ≠ deployment health.** MCP surface can export cleanly while /health reports degraded.
- **Annotations may be absent on non-arifOS organs.** P13 is only partially resolved (arifOS has them; A-FORGE/GEOX/WEALTH/WELL do not).
- **arif_think without mode= is misleading.** Always test with mode=apex for production-representative latency.
- **Envelope size includes SSE framing.** Raw bytes include `event: message\ndata: ` prefix — subtract ~50B for actual JSON payload.
- **Test with the actual actor_id that production agents use.** Anonymous/guest paths have different behavior (OBSERVE_ONLY).
- **FastMCP 3.4.4 has no `_tool_manager`.** `FastMCP._tool_manager._tools` doesn't exist in 3.4.4+. Use `mcp._local_provider._components` instead — keys are `tool:<name>@`. Example: `len([k for k in mcp._local_provider._components if k.startswith('tool:')])` gives tool count. The Phase 1 HTTP-based enumeration (talking to the running server via tools/list) still works regardless of version.
- **PYTHONPATH for local testing with venvs.** When `python3` resolves to a venv (`/root/arifOS/.venv/bin/python3`) that lacks pip, system-installed packages aren't visible. Add system site-packages: `PYTHONPATH=src:/usr/local/lib/python3.13/dist-packages`. Don't waste cycles reinstalling into the venv.
- **Bulk-fix broken Python comment blocks.** When `# ZEN-CONSOLIDATED — @mcp.tool(` is commented but `name=`, `annotations=`, `description=`, `)` on subsequent lines are NOT commented, it causes syntax errors. Root cause: searching for `")" in line` to find the closing paren stops at the annotations line because `_geox_annotations(...)` contains `)`. Fix: search for lines where `.lstrip().startswith(")")` instead. Fix with a script that finds the pattern and comments out all orphaned keyword-arg lines. See `fastmcp-tool-consolidation` skill for the correct pattern.

## Output Format

```
[OBS] arifOS MCP audit results (YYYY-MM-DD HH:MM UTC)
- Surface: 8 tools, 33 resources, 13 prompts
- Envelope: init=4.2KB observe=3.7KB (target <5KB) ✓/✗
- Status: all completed ✓/✗ (was: pending)
- Annotations: 8/8 ✓/✗
- Latency: think(mode=apex)=100ms think(default)=10s ✓/✗
- Health: status=healthy drift=False ✓/✗
- Gaps: N (P0: X, P1: Y, P2: Z)
- Verdict: PASS | PARTIAL | FAIL
```

## Related

- `FORGE-mcp-probe` — general MCP probing (any server)
- `FORGE-mcp-testing` — MCPJam Inspector testing
- `verify-nested-sibling-reports` — audit report verification
- `frontier-model-audit-verification` — audit report quality

---

*DITEMPA BUKAN DIBERI — Audit what matters, not what's easy.*
<!-- AAA-SKILL-PATCH 2026-10-28 provenance=333-AGI trace=trc-skill-align-20261028T135921Z -->
### Addendum 2026-10-28 - live re-measure (Rule 3n: targets above are STALE)

Measured today against arifOS :8088/mcp (9 tools, bukan 8 - arif_report is the 9th):

- arif_think envelope 29,068B / 37 SC keys / 9,592ms WITH mode=apex (targets say
  <5KB/<20/<200ms post-G3) => either the G3 fix regressed or never shipped. Re-derive, don't trust.
- arif_memory 27,100B / 37 keys / 5,367ms - same bloated-envelope family.
- :8088/mcp throws TRANSIENT 503 while /health is 200 and NRestarts=0 (3 observations in one
  day, across two independent sessions). A 503 on /mcp with a healthy /health is a
  middleware/session finding, not an outage - probe twice before declaring the organ down.
- status=completed can coexist with execution_state=AWAIT_INPUT and verdict=HOLD on the same
  payload: read all three fields, never status alone (dual-state tell, Rule 3s family).
- arif_report carries no idempotentHint/openWorldHint - annotation coverage is 8/9, not 8/8.
- arif_observe requires mode= (query-only calls return a 608B envelope with zero SC keys).
