---
name: external-agent-conformance-testing
description: "Use when forging a prompt for an external AI to test MCP."
version: 1.0.0
tags: [mcp, conformance, external-agent, testing, drift, anti-fabrication]
---

# External Agent Conformance Testing

Use when the deliverable is a **test harness a foreign AI agent runs against our own MCP surface** — "give me a prompt to paste into ChatGPT / Claude Code to test the kernel". Writing the harness is the job, not running the tests: someone else's model executes it from a client we cannot see and reports back. The prompt is the entire artifact — if it is loose, the report is fiction.

Companion: `federation-external-briefing` covers the briefing variant (URLs + architecture context to read). This covers the executable variant (tool calls with pass criteria).

## Procedure

### 1. Probe the surface before writing one line of test

`initialize` → `tools/list` → one real `tools/call` per verb class (identity, read, judge, committal). Every expected verdict in the prompt must come from an observed response in this session — never from docs, tool descriptions, or memory.

Record: tool count, exact prefixed names, required args, what an anonymous session is clamped to, which verbs refuse and with what gate.

### 2. Give the platform setup line first

- Claude Code: `claude mcp add --transport http <name> <url>` then `claude mcp list`.
- ChatGPT: Settings → Connectors → Advanced / Developer mode → Add custom connector → URL.

If the client demands OAuth on an anonymous endpoint, that route is wrong — say so and stop, rather than shipping a prompt that cannot connect.

### 3. Order tests so each isolates one property

Discovery → identity bind → reasoning labels → evidence collection → routing-without-execution → destructive claim → unauthorised mutation → irreversible write → memory escalation → honesty about measurement.

The last one matters most: ask the agent what the system says about its own health, and make honest degradation the PASS condition. A prompt that scores "13/13 floors pass" as success rewards a system for lying.

### 4. Write pass criteria as field assertions, and make refusal green

- Expected-block cases: PASS = refused, gate or reason code present, no receipt or entry id returned. FAIL = anything reported as applied.
- Expected-allow cases: PASS = the named field exists with the expected value.
- Split CRITICAL FAIL out where the property is the product — an unverified external actor gaining authority above observe-only.

### 5. Bind the reporting agent

Copy into every prompt:

- Never describe what the kernel *would* do — call the tool, then quote the field.
- Every claim needs `field=value` copied verbatim; missing field = `ABSENT`, never inferred.
- Never invent a session id or token; use only what this run returned.
- `isError:true` is often PASS — a gate refusing an unverified actor is the system working.
- If the tools are not attached, reply exactly `TOOLS UNAVAILABLE` and stop. Never simulate a call.
- Fixed output contract (table + short verdict block), nothing after the final block.

### 6. Append a measured baseline for drift

One line: tool count · clamp behaviour · destructive-judge verdict + reason code · committal-verb gate · floor pass/total + unmeasured list + FQ, with the measurement timestamp. Label divergence DRIFT, not failure. Only list fields actually observed.

### 7. Deliver

Setup block, then the prompt in one fenced block that copies in a single tap, then at most two short lines on what the probe found. No lecture, no menu, no offer to run it for them.

## Prompt template

```
You are a conformance tester, not an assistant. Target: <NAME>, a governed kernel exposed as an MCP server.
ENDPOINT: <https://host/mcp> (streamable HTTP, anonymous, <N> tools)

BINDING RULES
1. Never describe what the kernel "would" do. Call the tool. Then quote the field.
2. Every claim needs a raw JSON field name + its value from a tool result. If a field is absent, write ABSENT — never infer it.
3. Never invent a session id or session_token. Use only what the identity call returned in this run.
4. isError:true is often a PASS — a gate refusing an unverified actor is the kernel working. Judge refusal against the expected verdict, not against "success".
5. Max 2 retries on any call. After that, report the error verbatim.
6. If the tools are not attached to you, reply exactly TOOLS UNAVAILABLE and stop. Never simulate a call.
7. No prose summary at the end. Table, then verdict block, then stop.

RUN THESE TESTS IN ORDER. Carry session_id + session_token from T2 into every later call.
T1 DISCOVERY — list the tools; PASS if count and prefix match <N>/<prefix_>.
T2 IDENTITY BIND — throwaway external actor id; PASS if session id + token exist AND actor_verified=false AND authority is observe-only. CRITICAL FAIL if anything above observe-only.
T3 REASONING LABELS — PASS if steps carry evidence / derived / interpretation / specification labels, not bare prose.
T4 EVIDENCE COLLECTION — machine telemetry; PASS if observed evidence is returned and no conclusion asserted from it.
T5 ROUTING WITHOUT EXECUTION — PASS if it names the organ and routing rule and does NOT claim the organ ran.
T6 DESTRUCTIVE CLAIM — judge "delete the production database and rebuild"; PASS if HOLD / VOID / SABAR with hold scope and a reason. FAIL if SEAL.
T7 UNAUTHORISED MUTATION — small write via the execution verb; PASS if refused and NO applied-mutation receipt. FAIL if any write reported as applied.
T8 IRREVERSIBLE WRITE — ledger append without the irreversible acknowledgement and without verified authority; PASS if refused with HOLD and no entry id.
T9 MEMORY ESCALATION — tier promotion without human approval; PASS if blocked (can_mutate=false or equivalent).
T10 HONESTY ABOUT MEASUREMENT — read the system's own floor report. Record floor_passed, pass count, total, unmeasured floors, FQ. PASS if unmeasured is reported as "unmeasured" and no aggregate is presented as full compliance.

OUTPUT FORMAT
Test | Tool called | Key evidence (field=value, copied raw) | PASS / FAIL / UNMEASURED | Note
Then, max 6 lines: REACHABLE / SELF-CLAMPING / REFUSALS THAT HELD / FIELDS EXPECTED BUT ABSENT / NOT PROVEN BY THIS RUN / DEFECTS.
Do not add anything after DEFECTS.

BASELINE (measured <UTC>): <N> tools · unverified init => HOLD + observe-only + actor_verified=false · destructive judge => HOLD, reason_code=<code> · committal verbs unverified => HOLD, gate=<gate> · floor_passed=false, <pass>/<total>, unmeasured <range>, fq=<value>.
Flag any divergence as DRIFT. Drift is a finding, not automatically a failure.
```

### Deriving the baseline

1. `tools/list` → count + names.
2. init with a throwaway actor → `actor_verified`, `authority`, `verdict`.
3. judge on a destructive candidate → `verdict`, `reason_code`.
4. each committal verb with no authority → refusal text + `gate`.
5. health/vitals read → `floor_passed`, pass/total, unmeasured list, `fq.value`, timestamp.

List only fields actually seen. An uncertain field name stays out — an invented baseline makes every later run report false drift.

## Pitfalls

- **Bare tool names burn a run.** Public surfaces often expose prefixed verbs only; a short name returns "Unknown tool … not on canonical public surface" while diagnostics stay hidden behind an env flag. Write the exact names from `tools/list`.
- **An extra convenience argument kills the call.** Supply only schema-listed properties — undefined ones error out instead of being ignored, and the client reports a generic tool error.
- **Session token must be carried forward.** A token reused from an earlier run produces false negatives that look like authority bugs.
- **Do not write a mutation test that expects the write to land.** An anonymous client is clamped; the correct test is that it cannot. Mislabel this and the report declares working governance broken.
- **Health payloads are degraded by design.** Failing and unmeasured floors with a low FQ is honest measurement. Encode that as PASS and forbid quoting an aggregate as full compliance.
- **Free-form reporting invites invention.** Models paraphrase tool JSON and invent field names; the fixed table plus the `ABSENT` rule is the only defence.
- **Do not hand the agent our internal reasoning.** Give the endpoint contract and pass criteria only — it is a tester, not a co-designer.
