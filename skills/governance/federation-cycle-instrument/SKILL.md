---
name: federation-cycle-instrument
id: federation-cycle-instrument
version: 1.0.0
description: Use when measuring a system's cycle stage or ungated paths.
owner: Hermes
risk_tier: low
floor_scope: [F2, F3, F4]
autonomy_tier: T1
tags: [asabiyyah, measurement, enforcement-coverage, doctrine-decay, ibnu-khaldun, instrument]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Federation Cycle Instrument (asabiyyah)

> A cycle story that cannot be measured is a comfort, not a tool.

Load when asked whether a system is decaying, over-producing doctrine, or silently ungated — and when
you need an answer that survives being checked. Kernel: `arifOS/arifosmcp/runtime/asabiyyah.py`,
schema: `AAA/schemas/asabiyyah-reading.schema.json`, readings: `/var/lib/arifos/asabiyyah/*.json`.

## The three signals

| Signal | Formula | Failure it names |
|---|---|---|
| **CER** | ceremony artifacts / exercised capabilities | Luxury: doctrine production outruns exercised capability |
| **ASD** | executors / doctrine holders | Kafes: doctrine inherited, execution extinct |
| **ENC** | gated paths / total paths | Kerkoporta: a mutation path bypasses the gate |

Plus `mirror_check(claim, refs)` (provenance present = MIRROR, absent = STORY) and
`kampung_gadai_risk(relinquished, total)` (share of capacity signed away).

## Laws that make it honest

- **Observe, never judge.** The instrument emits numbers and bands. It does not rule on anyone.
  An organ may veto its own reading.
- **`NOT_APPLICABLE` beats an invented number, and is preferred.** "No data" is not "all clear".
- **Raw additive counts in `evidence`; never pre-divided ratios.** The kernel sums counts across
  organs then re-derives — averaging ratios lets a quiet organ dilute a loud one.
- **An organ measures its own substrate.** The kernel only federates.
- **Always emit `path_out`.** An instrument that can only report decline is a sad story. Meiji 1868
  and Korea 1953 rebuilt asabiyyah inside one generation; the way back is part of the reading.
- **Never score a human.** Where the only honest subject would be a person, emit `NOT_APPLICABLE`.

## Pitfalls (each one cost a real defect)

- **`float('inf')` is not JSON.** `json.dumps` writes the literal `Infinity`, which is invalid RFC 8259
  and `jq` rejects the file. For an undefined ratio (doctrine > 0, exercise = 0) emit `value: null`
  with `state: MEASURED` and the band — never a non-finite float. Gate it with
  `json.dumps(..., allow_nan=False)` in a test.
- **Classify on BANDS, never on raw values.** After the null fix, a classifier reading `m.value`
  silently treated an undefined-but-measured signal as "not measured" and softened the verdict from
  DECLINE to FOUNDATION. Read `m.band` (falling back to the band function); the band functions are
  the single source of the thresholds.
- **`@dataclass` + `from __future__ import annotations` breaks the naive standalone load.**
  `importlib.util.spec_from_file_location` + `exec_module` without registering the module in
  `sys.modules` first dies with `AttributeError: 'NoneType' object has no attribute '__dict__'`.
  Assign `sys.modules[name] = mod` before `exec_module`.
- **A substring grep for `Infinity` false-positives on prose.** It matches the word inside a quoted
  note. Use `json.loads(raw, parse_constant=raise)` for the real check.
- **A page count near double the block count is not a defect gate.** Chapter-per-block documents
  legitimately run ~2 pages per block; the ratio only signals a fault when blocks have a fixed
  height. Judge by the ink-coverage sweep, not the ratio.
- **Enumerate mutation paths adversarially, and name them.** A percentage hides the only useful
  output — the postern list. 99% coverage is one open door: Byzantium fell through Kerkoporta, not a
  breached wall. Count a path as gated only when a **mechanistic check precedes the write**; a logger
  is not a gate (a post-commit hook whose own source says "logging can never break the commit" is a
  logger), and a high-level wrapper whose default tier "proceeds regardless" is not a gate.
- **`total_paths = 0` must be `NOT_APPLICABLE`, never 1.0.** No paths enumerated is not the same as
  no paths unprotected.

## Reporting the result

Age each number to its `observed_at`, name the file that holds it, and hand the reader the exact
re-run command. Then state the limits in the artifact itself — a proxy denominator, a unit mismatch
between numerator and denominator (executor identities vs doctrine units makes an ASD band
*directional, not literal*), and any concurrent writer that moved the source mid-run.

## Remediation: the three levers, and the order they must be pulled in

Measuring decay is the easy half. These are the three levers back, cheapest first — and the
escalation rule that keeps each one from being disabled in week one.

1. **Close the postern.** Re-enumerate the ungated mutation paths and route them through the gate
   that already exists. Needs no new capability. The instrument's `ungated` list *is* the work queue.
   Never summarise it into a percentage — a percentage hides the only useful output.
2. **Install the measurement.** `AAA/lib/invocation_log.py` is the shared telemetry contract: one JSON
   line per real invocation to `/var/lib/arifos/metrics/tool_invocations.jsonl`, stdlib only,
   append-only, and it **never raises into the caller**. `exercise_count(organ, window_days)` is the
   readback that turns `exercised_capabilities` and `executors` from proxies into measurements.
   Log the tool NAME and the actor id — never arguments. A tool name is MAP; an argument is STORY.
3. **Declare the artifact.** `AAA/scripts/doctrine-declaration-gate.py` requires every new doctrine
   artifact to name its `origin` (exercised / observed / synthesised / inherited) and the capability
   it `changes` (or an honest `NONE`). Schema: `AAA/schemas/doctrine-artifact.schema.json`.

**Escalate a gate one way only: ATTENTION → RATCHET → ENFORCE.** Pointing a brand-new gate at a
corpus that was never declared produces a 100%-failure result on day one — 3,822 gated artifacts,
0 declared — and a gate that fails everything is waived everywhere within a week. Ship it recording
findings and exiting 0; make the exit code meaningful only at the ratchet, against a stated cutover
date. Then it means something.

### Pitfalls from building the remediation

- **A `path=` test hook that the wrapper forgets to forward writes test data into the PRODUCTION log.**
  `timed()` and `instrument()` took `**kw`, swallowed `path` into the context dict, and never passed it
  to the logger — so every test run appended fake receipts to the live telemetry file and corrupted the
  baseline. Make sink overrides explicit keyword-only parameters and route them to the logger, never
  into the context. Then clean any pollution out of the live file before trusting a count: a telemetry
  log with fake rows is worse than no log.
- **JSON cannot carry an HTML-comment declaration.** The gate worked on markdown and silently could
  not be satisfied by the JSON schemas it was first pointed at. Support a top-level
  `x-doctrine-declaration` key for JSON/YAML. Find this by dogfooding — declare your own artifacts
  first, before pointing the gate at anyone else's.
- **Verify idempotency on any forwarder.** A log-parsing forwarder that re-emits on every run inflates
  `distinct_tools` without bound. Prove it by running twice and asserting the second run emits zero.
- **Restarting a live service is an availability mutation, not a wiring step.** Instrument in-process,
  prove the call site works with a test, and hand the restart back as a reportable requirement instead
  of doing it. Same for anything that would block or deny on a running system.
