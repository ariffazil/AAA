# GEOX Tool Shape Drift — the 3-mismatch class (2026-08-06)

A sibling report diagnosed `geox_evidence` as `EVIDENCE_SCHEMA_VIOLATION`. The
diagnosis was directionally right (the tool was failing) but the root cause
was deeper than the sibling's prose reached. **Three shapes had drifted
independently**, and each one had to be reconciled before the wire form would
pass. This is a class of drift that's distinct from the audit-trail errors
covered by `references/files-changed-table-verification-2026-08-06.md`
(per-file row taxonomy) — it's about the **shape contract** between a tool's
three layers.

## The 3-shape pattern

```
┌──────────────────────────────────────────────────────────────────┐
│                  WIRE WRAPPER (@mcp.tool decorator)               │
│   defines: parameter signature visible to MCP clients            │
│   errors when caller passes params not in this signature         │
│   → ValidationError: unexpected keyword argument 'X'             │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                  IMPL (the async function called)                │
│   defines: parameter signature + return-shape contract           │
│   _safe_forward() filters out args not in impl signature         │
│   → impl may run with EMPTY args if wrapper shape != impl shape  │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│              POSTCONDITION (evidence_postcondition.py)           │
│   defines: required_keys for the tool's success result           │
│   downgrades to FAILURE if claimed success + zero required keys  │
│   → EVIDENCE_SCHEMA_VIOLATION when contract ≠ what was returned  │
└──────────────────────────────────────────────────────────────────┘
```

When a sibling reports `EVIDENCE_SCHEMA_VIOLATION: all required fields
null/empty`, the natural reaction is "the impl is broken — produce the
required fields". Often wrong. The first probe is: **what shape does the wire
wrapper expose, and does that shape match the impl's signature?**

## Diagnostic sequence (verified 2026-08-06 on GEOX `geox_evidence`)

1. **Find the wire wrapper.** `grep -n "@mcp.tool(name=\"<tool>\"" /root/<organ>/src/.../tools_wiring.py`
   - Read its parameter signature — these are the only params callers can pass.
2. **Find the impl.** `grep -n "async def <tool>\\|def <tool>" /root/<organ>/src/.../<tool>.py`
   - Read its parameter signature — what the impl actually accepts.
3. **Find the postcondition contract.** `grep -n "<tool>" /root/<organ>/src/.../evidence_postcondition.py`
   - Read the required_keys list — what the postcondition demands in success results.
4. **Three-way diff.** If wrapper.shape ≠ impl.shape ≠ postcondition.shape, that's the bug class.

### Real GEOX case (2026-08-06, all three shapes were wrong)

| Layer | Shape | Probe result |
|---|---|---|
| Wire wrapper `@mcp.tool geox_evidence` | `evidence_id, evidence_type, claim_id, claim_text, epistemic_label, ...` (lifecycle) | calls `_impl(evidence_id=..., evidence_type=...)` |
| Impl `geox_evidence()` | `mode=Literal[discover/synthesize/abduct/contradict/spatial_block/ingest_literature], query, scope, basin_name, ...` (synthesis) | impl signature does NOT include `evidence_id` etc. |
| Postcondition | `required_keys = ["evidence_items", "synthesis", "sources"]` | expects synthesis-shape outputs |

Three shapes, two mismatches. A caller calling the wire with `mode=...` got
`ValidationError: mode is not in wrapper signature`. A caller calling the wire
with `evidence_id=...` got `_safe_forward()` filtering all params (impl
signature doesn't include them) → impl defaulted to `mode=synthesize` with no
real data → `evidence_items=[]` → postcondition DOWNGRADED.

## The fix path (verified)

Pick (c): **split the tool into two**, each with one consistent shape.

```python
# 1. Register the unused Pattern A wrapper (often present as dead code)
#    under a NEW name, with the correct shape:
@mcp.tool(name="geox_evidence_synthesize",
          annotations=_geox_annotations("geox_evidence_synthesize"))
async def _evidence_synthesize(
    mode: str = "synthesize", query: str = "", ...
) -> dict[str, Any]:
    """Mode-driven evidence synthesis."""
    return await _impl(mode=mode, query=query, ...)  # impl-shape match

# 2. Keep the existing wire wrapper as lifecycle (or rename/replace
#    depending on whether lifecycle is the actual wire contract):
@mcp.tool(name="geox_evidence", ...)
async def _evidence(
    evidence_id: str = "", evidence_type: str = "supporting", ...
) -> dict[str, Any]:
    """Lifecycle wrapper. Wire form."""
    ...

# 3. Update the postcondition contract to match the SHAPE the wrapper exposes,
#    not the synthesis contract the impl thinks it needs:
EVIDENCE_CONTRACTS["geox_evidence"] = None  # lifecycle: bypass postcondition
EVIDENCE_CONTRACTS["geox_evidence_synthesize"] = ["evidence_items", "synthesis", "sources"]
```

## The non-obvious step — pycache stale-source trap

After editing `evidence_postcondition.py`, the live service STILL serves the
old contract because the running `python3 -m geox_mcp.server` interpreter
loaded `__pycache__/evidence_postcondition.cpython-*.pyc` at startup.

**Verification:** I patched `evidence_postcondition.py` with the new
`geox_evidence_synthesize` contract, restarted `geox-mcp.service`, called the
tool — STILL got `postcondition.verdict: DOWNGRADED` with the OLD
`missing_evidence: [evidence_items, synthesis, sources]` set pointing at the
right keys but the wrong tool name. The service was running the OLD code.

**Fix:**

```bash
# Clear pycache before restart — otherwise .pyc files shadow .py edits
find /root/<organ>/src -name "*.cpython-*.pyc" -path "*<changed_module>*" -delete
# OR the broader sweep (slower, broader blast radius):
find /root/<organ>/src -name "__pycache__" -type d -exec rm -rf {} +

systemctl restart <organ>-mcp.service
```

**This is the `.py` cousin of the existing `Source patched ≠ runtime patched`
pitfall** (which covers `.ts`→`.js` compile-time gap). New pitfall entry
needed: `.py`→`.pyc` runtime cache gap. Distinct mechanism, same shape: the
running process holds an in-memory copy of the file from boot; file edits
don't take effect until restart AND the bytecode cache is invalidated.

## The CANONICAL_PUBLIC_SURFACE gate (organ-specific quirk)

Adding `@mcp.tool(name="<new_tool>")` to `tools_wiring.py` is necessary but
not sufficient. The canonical public surface gate (verified on GEOX):

```bash
# 1. Register the @mcp.tool decorator (your new tool is now in the live
#    wiring layer, but won't appear in tools/list yet)

# 2. Update TWO manifest files (not one):
/root/GEOX/tools_sot.yaml                      # canonical docs/registries
/root/GEOX/src/geox_mcp/tools_manifest.yaml    # the source generate_canonical reads

# 3. Regenerate the canonical surface:
/root/GEOX/.venv/bin/python3 scripts/generate_canonical_surface.py
# → writes /root/GEOX/CANONICAL_PUBLIC_SURFACE.json
# → writes /root/GEOX/src/geox_mcp/generated/CANONICAL_PUBLIC_SURFACE.json
# → writes /root/GEOX/docs/canonical_public_tools.json
# public_count should increment by 1; if it doesn't, the manifest didn't
# pick up your entry (check visibility: public field).

# 4. Restart:
systemctl restart geox-mcp.service

# 5. Verify:
curl :8081/health | jq '.surface_drift'
# canonical_count and live_count should both equal the new public_count.
```

Without the manifest + regenerate + restart sequence, the new tool is in
`tools_wiring.py` (which the live server imports) but the gate (which
`/health` reads to compute `surface_drift.drift_count`) still claims 33 tools
canonical / 33 live / drift=0 — the registration is invisible to the audit
surface. The next SABAR loop or integrity check sees a passing gate while
the wire already serves 34 tools.

## Detection cues

When a sibling reports a tool as "broken" but the live service is healthy,
look for the 3-shape drift before patching the impl:

| Symptom | Likely 3-shape drift |
|---|---|
| `ValidationError: <param> is not in signature` | wrapper.shape ≠ impl.shape |
| `EVIDENCE_SCHEMA_VIOLATION` on EVERY call (including valid ones) | wrapper.shape ≠ postcondition.shape |
| Tool returns success but postcondition downgrades anyway | impl.shape ≠ postcondition.shape, or wrapper filters all params out |
| Drift = 0 but tool claims to be "registered" doesn't appear in `/health` | manifest/canonical-surface gate not refreshed |

If any of these match, the fix is shape reconciliation (split, realign, or
bypass) — not impl patching.

## Worked transcript (2026-08-06, GEOX session)

| Step | Command | Result |
|---|---|---|
| Probe 1 | `curl :8081/mcp tools/call geox_evidence(mode=derived)` | `ValidationError: mode is not in wrapper signature` |
| Probe 2 | `curl :8081/mcp tools/call geox_evidence(evidence_id=...)` | `EVIDENCE_SCHEMA_VIOLATION: missing evidence_items, synthesis, sources` |
| Diagnose | grep wrapper signature, impl signature, postcondition contract | 3 shapes drifted |
| Fix | re-register Pattern A as `geox_evidence_synthesize`, update contract | postcondition contract split |
| Restart | `systemctl restart geox-mcp.service` | tools=33/33, drift=0 (canonical not refreshed) |
| Manifest | edit tools_sot.yaml + tools_manifest.yaml, run generate_canonical_surface.py | public_count=34 |
| Restart + pycache clear | `find /root/GEOX/src -name "*.cpython-*.pyc" -delete && systemctl restart geox-mcp.service` | tools=34/34, drift=0 |
| Verify 1 | `geox_evidence(evidence_id=..., claim_id=...)` | isError=False, no error |
| Verify 2 | `geox_evidence_synthesize(mode=synthesize)` | execution_status=ERROR (correct — bad basin name); postcondition DOWNGRADED (correct — empty synthesis rejected) |

Both tools verified: lifecycle wrapper passes through cleanly; synthesize
correctly rejects empty synthesis as `DOWNGRADED` (F2 enforced). The
previous behavior (every call downgraded, including valid lifecycle calls)
is gone.

## Two-file type widening technique

When introducing `None` into a previously `list[str]`-typed contract dict,
Pydantic strict types will reject. The fix is **widen the type AND keep the
key present**:

```python
# Before:
EVIDENCE_CONTRACTS: dict[str, list[str]] = {
    "geox_evidence": ["evidence_items", "synthesis", "sources"],
    ...
}

# After:
EVIDENCE_CONTRACTS: dict[str, list[str] | None] = {
    "geox_evidence": None,  # explicit bypass — wrapper shape mismatch
    "geox_evidence_synthesize": ["evidence_items", "synthesis", "sources"],
    ...
}
```

`None` is the documented bypass path in `check_evidence_postcondition`
(line ~293: `if required_keys is None: return original`). Using an empty
list `[]` instead of `None` would fall through to the postcondition loop
and silently pass — which is the worse failure mode (false POSITIVE on a
tool that produces no evidence).

## Audit verdict taxonomy (extend §4.2c for this class)

| Verdict | Meaning |
|---|---|
| ✅ TRUE | All 3 shapes consistent (wrapper ≡ impl ≡ postcondition) |
| ⚠️ PARTIAL — wrapper≠impl | Wire callers cannot reach impl's intended entry path |
| ⚠️ PARTIAL — impl≠postcondition | Impl produces shape that postcondition rejects |
| ❌ BROKEN | All 3 shapes drifted — no caller path produces a passing result |

When auditing a sibling's "tool X is broken" claim, run the 3-shape diff
BEFORE accepting the broken verdict. Often the report is correct on
direction (the tool fails on real calls) but wrong on root cause (it's a
shape drift, not an impl bug). The fix is shape reconciliation, not
impl patching — saves the impl from speculative edits that don't address
the actual contract violation.