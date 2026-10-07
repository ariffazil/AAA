# Handoff / Transfer Patch Falsifier Recipe

The F2/F9 handoff-invariant violation has a specific shape and a specific falsifier. This file is the reusable recipe — load when patching any handoff, transfer, cross-organ, or evidence-routing function in the federation.

## The defect class

A function receives a structured input (claim, event, evidence packet) and emits a "compressed" envelope to a downstream consumer. The compression silently:

1. Synthesizes a certainty string from the *presence* of certain fields (e.g. "HERMES-validated (PASS)" because `claim_id` and `verdict` are present)
2. Drops limitation fields without recording the drop (`dropped[]` stays empty)
3. Upgrades a low-confidence / UNKNOWN epistemic_state to a label that the downstream trusts ("validated", "trusted", "verified")

The mechanism: the function uses field PRESENCE as a proxy for field VALIDATION. A caller can supply `verdict="PASS"` with `epistemic_state=UNKNOWN`, `confidence=0.2`, `evidence_status=UNSUPPORTED` — and the function sees the pair, decides "must be validated", rewrites the uncertainty string, drops the four limitation fields, and emits "PASS" as if hermes_claim_validate had run.

## The F2/F9 law

> May compress evidence, must not increase certainty, expand permission, or remove a limitation.

Translation:
- Compress = you may strip qualia, paraphrase, drop redundant context
- Must not increase certainty = never write "validated" if upstream said UNKNOWN
- Must not expand permission = if `authorizes_action=False`, do not pass `authorizes_action=True`
- Must not remove a limitation = every limitation field (`evidence_status`, `authorizes_action`, `storage_class`, `confidence`, `engine`, `falsifier`) must either be forwarded verbatim OR recorded in `dropped[]` with the field name

## The falsifier shape

A handoff patch's falsifier is the **exact input from the original bug report**, re-run against the live system. Build it as a JSON object that exercises every failure mode in one shot:

```json
{
  "statement": "Upstream hermes-agent is unaffected by this fork",
  "epistemic_state": "UNKNOWN",
  "provenance_class": "UNKNOWN",
  "evidence_status": "UNSUPPORTED",
  "authorizes_action": false,
  "storage_class": "UNSTRUCTURED_NARRATIVE",
  "confidence": 0.2,
  "claim_id": "TEST-001",
  "verdict": "PASS",
  "engine": {"mode": "keyword", "reason": "not_invoked"}
}
```

Pre-patch: function rewrites this to `uncertainty="HERMES-validated (PASS)"`, drops all five limitation fields, emits "PASS" as a certainty upgrade.

Post-patch: function returns
- `epistemic_state: "UNKNOWN"` (preserved, not synthesized-over)
- `evidence_status: "UNSUPPORTED"` (forwarded verbatim)
- `authorizes_action: false` (forwarded verbatim)
- `storage_class: "UNSTRUCTURED_NARRATIVE"` (forwarded verbatim)
- `confidence: 0.2` (forwarded verbatim)
- `engine: {mode: keyword, reason: not_invoked}` (forwarded verbatim)
- `verdict: "PASS"` (carried as label, not as certainty upgrade)
- `claim_id: "TEST-001"` (carried)
- NO `uncertainty` field (not synthesized)
- `dropped[]` contains 1 entry: `{field: "falsifier", reason: "upstream did not supply 'falsifier'..."}` (the one field that was actually absent)

## How to test in isolation

When the function lives in a package whose `__init__.py` imports heavy deps unavailable in the test env (e.g. `hermes_mcp/__init__.py` imports `fastmcp`):

```python
import importlib.util, sys, types
pkg = types.ModuleType("hm"); pkg.__path__ = ["/root/.hermes/hermes_mcp"]
sys.modules["hm"] = pkg
spec = importlib.util.spec_from_file_location("hm._handoff", "/root/.hermes/hermes_mcp/_handoff.py")
m = importlib.util.module_from_spec(spec)
# Stub cross-module imports
m.scan_injection = lambda t: {"injection_detected": False, "categories": []}
m.INSTITUTIONS = ["PETRONAS"]; m.INTERIOR_STATES = ["love"]
m._hits = lambda t, terms: [x for x in terms if x in t]
spec.loader.exec_module(m)
# Now call m.build(claims=[falsifier_input], target_organ="arifOS", purpose="security_audit")
```

Run the falsifier. Pre-patch: output contains the synthesized "validated" string. Post-patch: output matches the post-patch shape above.

## How to test on live wire

The function is exposed via MCP. The MCP session handshake for the legacy sessionful 2025-03-26 mode (still used by hermes-mcp-server :18087):

```python
import json, urllib.request

def post(body, session=None):
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if session: headers["Mcp-Session-Id"] = session
    req = urllib.request.Request("http://127.0.0.1:18087/mcp", data=json.dumps(body).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.read().decode()

# 1. initialize
init = {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"falsifier","version":"0"}}}
req = urllib.request.Request("http://127.0.0.1:18087/mcp", data=json.dumps(init).encode(), headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream"})
with urllib.request.urlopen(req, timeout=10) as r:
    session = r.headers.get("Mcp-Session-Id")

# 2. initialized notification
post({"jsonrpc":"2.0","method":"notifications/initialized"}, session=session)

# 3. tool call with the falsifier input
call = {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"hermes_handoff_package","arguments":{"claims":[falsifier_input],"target_organ":"arifOS","purpose":"security_audit"}}}
raw = post(call, session=session)
```

Without step 1, the tool call returns HTTP 400. Without step 2, the session stays in `uninitialized` state. With both, the tool call returns the envelope.

## The structural fix

```python
LIMITATION_FIELDS = ("evidence_status", "authorizes_action", "storage_class", "confidence", "engine", "falsifier")

for claim in claims:
    entry = {"statement": ..., "epistemic_state": claim.get("epistemic_state", "UNKNOWN"), ...}
    if "uncertainty" in claim:
        entry["uncertainty"] = claim["uncertainty"]   # forward verbatim if supplied
    # else: do NOT synthesize
    
    limitation_drops = []
    for field in LIMITATION_FIELDS:
        if field in claim:
            entry[field] = claim[field]    # forward verbatim
        else:
            limitation_drops.append(field)
    
    if limitation_drops:
        for f in limitation_drops:
            dropped.append({"field": f, "reason": f"upstream did not supply '{f}' — preserved remainder recorded; destination must treat as absent (not unknown, not failed)"})
    
    # claim_id and verdict may be carried as LABELS, not as certainty upgrades
    if claim.get("claim_id"): entry["claim_id"] = str(claim["claim_id"])
    if claim.get("verdict"): entry["verdict"] = str(claim["verdict"])
```

The `law_note` must state the v2.1 contract explicitly so downstream consumers know they cannot trust a synthesized uncertainty string.

## Why this matters

The downstream consumer (arifOS kernel, governance reviewer, audit log) sees the envelope and decides whether to trust the claim. If the envelope says "validated" when upstream said "UNKNOWN", the consumer trusts a phantom. A patch that fixes the handoff function does not fix the consumer's prior conclusions — those still carry phantom certainty. The patch must therefore be paired with a backfill audit: any prior handoff that emitted "HERMES-validated (...)" must be re-evaluated against the corrected semantics. This is why the falsifier must run on the LIVE wire, not just in unit tests: the wire is what downstream consumers see.

## Anti-patterns

1. **Asserting `claim_id + verdict present → "validated"`.** Presence is not validation. The caller may have constructed the claim from any source.
2. **Synthesizing an `uncertainty` string when upstream did not supply one.** The destination must infer from `epistemic_state` + `evidence_status` — that is the lawful path.
3. **Forwarding only `claim_id` + `verdict` and dropping everything else.** The destination loses the constraints that made the verdict meaningful in the first place.
4. **Recording drops as a count, not a list.** `dropped_count: 4` is the same defect as `dropped: []` — the destination cannot know which fields were lost.
5. **Updating the unit test to match the buggy behavior.** If a legacy test asserts `"HERMES-validated" in uncertainty`, the test was wrong by design. Update the test to the new contract (epistemic_state + evidence_status preserved, no synthesized string), do not preserve the old assertion.
