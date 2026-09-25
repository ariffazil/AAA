# Hermes MCP Self-Schema Drift — 2026-09-25

> **Pattern:** When auditing an MCP server's *own self-description*, three classes of drift surface
> that cross-surface scans miss. They live inside one resource or one tool, between fields the
> server itself controls.

## The Three Classes

### Class A — Resource description metadata vs resource content

A `hermes://...` resource carries a top-level `description` string (server-set metadata) and a
`content` body. Both are read in one call. The server is free to keep them in sync — and free not to.

**Tell:** `description` makes a numeric claim (`"all N capability families"`) while `content` is a
structured array whose length is a different number.

**Recipe:**
```python
desc = response["result"]["description"]                  # "all 10 capability families"
content_families = response["result"]["content"]["families"]
n_actual = len(content_families)                          # 13
# drift = (numeric claim in desc) != n_actual
```

**Mechanism:** the description string is hand-written; the content array is data-driven. When the
data grows, the description lags. Version field (`version: 1.0.0`) usually lags with it — a triple
that all need bumping.

**Fix shape:** one-line patch. Bump description + bump `version` to reflect the new content length.
Do not retrofit the data to match a stale description.

### Class B — Detector that returns `status: OK` while not processing input

A tool that *should* scan its `claims` argument returns `claims_scanned: 0`,
`contradictions: []`, and `status: "OK"` — all three simultaneously, on every input shape.

**Tell:**
- The success field is `status: "OK"` (truthy) AND
- the work field is `claims_scanned: 0` (zero) AND
- the result field is empty list (falsy)
- All three green on three different input shapes (bare strings, dict, dict-with-time+principal)

**Mechanism:** the success branch never gates on whether the scan loop ran. Either the input
parser rejects silently (no error), or the loop short-circuits before processing. The result looks
healthy because every diagnostic field defaults to its "all clear" value.

**Recipe to detect:**
```
1. Pass one bare string:                → claims_scanned=N? expected ≥ 1
2. Pass dict with principal + source:   → claims_scanned=N?
3. Pass dict with time field:           → claims_scanned=N?
If all three return claims_scanned=0 → silent input loss, not sensitivity weakness.
```

**Fix shape:** server-side. The scan loop must guard on `len(claims) > 0` before assigning
`status: "OK"` — or return an explicit `status: "EMPTY_INPUT"` field. From the audit side, no
fix is possible without server patch; report as a P1 defect.

### Class C — Tool schema declares permissive, server validates strict

Schema for `evidence` parameter says `items: {type: string}` (any string array). Server rejects
valid strings with `"is not of type 'string'"` at argument validation.

**Tell:** the JSON schema is permissive (`items: {}` accept-anything, or `items: {type: string}`
explicit-string), but the server-side validator is stricter (e.g. requires prefix-tagged strings
like `"MEASURED: ..."` even though untagged strings are flagged as `untagged — provenance is never
silently promoted` in the tool description).

**Mechanism:** the tool description says one thing ("untagged defaults to REPORTED, never promoted
silently"), the JSON schema says another ("any string works"), and the server-side validator says
a third ("no string at all works"). Three surfaces, three contracts.

**Recipe to detect:**
```
1. Read tool description for unstated constraints.
2. Read JSON schema for declared constraints.
3. Try the simplest valid input that satisfies the schema.
4. If rejected: schema lies. Try a tagged input.
5. If accepted: the contract lives in the description, not the schema.
```

**Fix shape:** server-side. Either (a) align the schema to the validator (`minLength`, `pattern`,
or nested object schema), or (b) align the validator to the schema and trust `untagged → REPORTED`
as the description promises. From the audit side, document the actual contract; do not invent a
third "fix" that adds a wrapper.

## Why These Hide From Cross-Surface Scans

Cross-surface scans (the parent skill's main mode) compare two surfaces. Classes A, B, C are
**single-surface drift** — the contradiction lives inside one resource or one tool, between two
fields the same payload carries. A two-surface scan that reads `description` from one probe and
`content` from another will MISS class A because both probes return their own clean numbers.

**Diagnostic:** run a single-surface audit only when the surface is the target. Run a
cross-surface audit only when comparing declared-vs-observed across systems. The two are different
problems with different recipes.

## The Probe-Order That Surfaces All Three

For any MCP server audit:

1. **First:** `tools/list` + `resources/list` — establish the surface size and shape.
2. **Second:** for each resource, pull it via `hermes_retrieve` (or equivalent) and check
   description-vs-content on **numeric** fields (counts, versions, family indexes).
3. **Third:** for each detector tool, send three input shapes (string, dict, dict-with-time)
   and compare `claims_scanned` or equivalent work-counter. Any zero on a non-empty input is
   silent input loss.
4. **Fourth:** for each tool whose schema says `items: string` or `items: {}`, try the simplest
   valid input — confirm schema truthfulness.
5. **Fifth:** for each `status: OK` result, check the work-counter or coverage field. `OK` with
   `claims_scanned: 0` is a no-op surface.

This order surfaces all three classes with the minimum number of probes.

## Relationship To Other References

- **MCP Resource Zen (`mcp-resource-zen-2026-07-28.md`)** covers cross-surface noise reduction.
  Class A is the inverse problem: a single surface that lies about itself.
- **Hermes MCP Deep Scan (`hermes-mcp-deep-scan-2026-08-02.md`)** covers existence + capability
  enumeration of an MCP server. The current reference covers self-schema consistency of one that
  is already known to exist.
- **MCP Response Pipeline Audit (`mcp-response-pipeline-audit.md`)** covers server-side output
  trimming. Classes B and C live at the input side, not the output side.
