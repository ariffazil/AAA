---
title: "Scar — Judge Evidence Transport Severed (Bridge Stringifies Composite Args)"
created: 2026-08-14
created_by: 333-AGI (session SEAL-b413b305531e43f8)
floors: [F2, F11, F13]
risk_band: governance-infrastructure
confidence: HIGH
---

# Scar — Judge Evidence Transport Severed

## What Happened
While connecting the federation's first load-bearing tree777 scar citation
(tree777://scar/root/kimi, "Documentation is a hypothesis. Runtime is the
verdict.") into an arif_judge verdict, every attempt to pass structured data
to arifOS kernel verbs failed pydantic validation:

- `arif_judge(evidence={...})` → arrived at the kernel as a JSON **string**,
  rejected with `dict_type` error. Three attempts (nested, flat, pointer).
- `arif_observe(layers=[...])` → arrived as a **string**, rejected with
  `list_type` error.
- Scalar-only calls succeed (query strings pass clean).

The judge then correctly ruled HOLD — EVIDENCE_EMPTY (Rule #1: empty=STOP)
and the session geometry degraded to RETAK (floors L02/L03/L07/L08, G=0.49).

## Root Cause
The opencode→arifOS MCP client bridge serializes composite arguments
(objects and arrays) into JSON strings before transport, while the kernel
declares them as object/list types. Scalar arguments survive; structured
evidence does not. The judge's immune response (refusing to seal on empty
evidence) is CORRECT — the defect is in the delivery path, not the gate.

## What Should Have Happened
A working bridge would carry the evidence dict intact; the judge would
measure the citation (scar URI + probe facts + sovereign demand evidence)
and render SEAL or HOLD on the MERITS.

## Lesson
1. The immune loop's receptor (judge evidence intake) is only as strong as
   its transport. A citation cannot be load-bearing if it cannot arrive.
2. When composite args fail validation with `dict_type`/`list_type`, suspect
   the bridge serialization FIRST, do not retry the same shape (SABAR).
3. Workaround until repaired: carry structured evidence as a scalar string
   inside `query`/`candidate`, AND fix the bridge — prose-in-candidate is
   not a permanent substitute; the judge rightly distrusts it.
4. Repair target: opencode MCP client arg serializer for the arifos server
   entry, or kernel-side tolerant parsing (json.loads on string-typed
   composite args). Either fix restores the arrow verdict→scar.

## Meta (immune loop demonstration)
This scar was produced BY the failed attempt to make SCAR_KIMI load-bearing.
The loop diagram's line 7 — "new failure is a NEW scar (system learns)" —
executed live. Next agent walking this path: wiki_search "judge evidence
transport" will find this scar before burning retries.

## Confidence: HIGH
All validation errors observed directly (5 occurrences, identical signature).
Trace refs: trc-38afbd13ee55 (judge), TRACE-d12a4a3ca6bd (observe-ingest).
