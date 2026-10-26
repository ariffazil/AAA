---
name: mcp-external-conformance
description: "Use when outside AI agents audit an MCP surface."
tags: [mcp, conformance, audit, external-agents, verification, reproduction]
version: 1.0.0
author: Hermes Agent
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# MCP External Conformance

Handing a governed surface to an outside AI is not a popularity test — it is a
black-box audit of **verdict semantics**. The auditor cannot read your source, so
anything it reports it had to earn from fields. That is the value: a decorative
kernel cannot pass a well-built battery, because the battery requires two calls that
must disagree.

## USE WHEN

- An MCP server (arifOS, WELL, GEOX, WEALTH, or any organ with an `/mcp` face) is
  about to be judged by ChatGPT, Claude, Perplexity, Grok, Mistral, Codex, Gemini CLI,
  Copilot or another external host.
- A pasted conformance report from such a host needs grading before anything is fixed.
- A public MCP endpoint is about to be shared and you need to know what it exposes.

## DO NOT USE WHEN

- Auditing the surface yourself for entropy, envelope size, annotations, latency —
  that is internal quality work, not external conformance.
- The question is "which client supports feature X" and nothing is being graded —
  read the capability matrix and stop.

## 1. Pre-flight — always before inviting anyone in

```bash
npx -y @mcpjam/cli@latest server doctor --url <endpoint> --rpc --out doctor.json
npx -y @mcpjam/cli@latest protocol conformance --url <endpoint>
npx -y @mcpjam/cli@latest oauth conformance --url <endpoint>
npx -y @mcpjam/cli@latest compat --url <endpoint>
```

`server probe` alone gives transport selection, negotiated `protocolVersion`, OAuth
discovery and `registrationStrategies` without a full handshake.

**Record these four facts before writing the hand-off prompt**, because each one
knocks out a class of client:

| Fact | Consequence if unfavourable |
|---|---|
| `oauth.required` false / optional | no-auth lanes work; most chat hosts attach first try |
| `registrationStrategies` = `["preregistered"]` only | no dynamic client registration — a host that demands DCR *and* refuses no-auth fails, and there is no secret to hand it |
| negotiated `protocolVersion` | must be echoed in the `MCP-Protocol-Version` header on every later call |
| transport | Streamable HTTP is required by Gemini Enterprise; SSE-only servers are rejected there |

Run the checks yourself first. An internal pre-flight that already fails makes the
external report unreadable — you cannot tell an auditor's finding from your own bug.

## 2. Battery design — what makes it survive a decorative server

A battery is only worth handing out if a server that *narrates* governance fails it.
Four design rules produce that property:

1. **Demand the field, not the prose.** Every test names the exact JSON path it will
   read (`effective_verdict`, `reason_code`, `can_mutate`, `hold_required`). Grade on
   those, never on a decorative `verdict` string that can read `completed` on a HOLD.
2. **Require a differential.** At least one test sends two candidates that *should*
   be judged differently and fails if the verdicts are identical. This is the single
   test that separates a judge from a formatter — a content-insensitive judge returns
   the same answer for an honest claim and an overclaim.
3. **Include the irreversible path, dummy payload only.** Test that the refusal
   happens; forbid the auditor from attempting a real mutation. The refusal is the
   deliverable, and retrying it as a bug wastes the run.
4. **Forbid simulation.** One line — "if a tool is not exposed, record UNAVAILABLE;
   never simulate, infer, or expect a response" — removes the most common source of
   plausible-looking fake findings.

Bind the run: one retry on transport error, log both attempts, no mid-run questions,
one report at the end. An auditor that stops to ask makes the exercise interactive and
loses the independence you were buying.

Full battery: `references/conformance-battery.md`. Copy-paste prompt:
`templates/external-conformance-prompt.txt`.

## 3. Client capability divergence — grade the client before the server

Hosts differ in which MCP primitives they expose, and this changes what a report can
possibly mean:

- **Tools-only hosts** cannot read prompts or resources. A prompt test on such a host
  is not a FAIL — it is UNAVAILABLE.
- **Full hosts** (tools + prompts + resources + Apps) can be graded on everything.

Check the client before trusting its T0 count. Then check the **server's own
`initialize.instructions`**: if the boot sequence tells every entering agent to call a
prompt or read a resource as step 1, three of the highest-reach clients cannot comply,
and the predictable outcome is a narrated fake ignition. A boot sequence must degrade
when the primitive lane is absent, not assume it.

Matrix and per-platform recipes: `references/client-capability-matrix.md`.

## 4. Read-path authority — the check nobody remembers to run

An authority band that narrows **verbs** says nothing about what was **read**. Bind a
session as an unverified stranger and inspect every context block returned — session
continuity, temporal/prediction context, memory or state passthrough. If the response
reports `OBSERVE_ONLY` while shipping private payload, the system gates actions and
leaks content, and `can_mutate:false` is decoration.

Two supporting probes:

- **Self-instruction validity** — fetch every prompt and resource the server's
  instructions name. Non-resolving names are a defect, not a client bug.
- **Exposure breadth** — before believing only your invitees saw it, count distinct
  clients in the front-proxy log:

```bash
python3 - <<'EOF'
import json, collections
c = collections.Counter()
for line in open("/var/log/caddy/<host>-access.log", errors="ignore"):
    if '"uri":"/mcp"' not in line: continue
    try: d = json.loads(line)
    except: continue
    r = d.get("request", {})
    c[r.get("client_ip") or r.get("remote_ip")] += 1
print(len(c), "distinct clients")
for ip, n in c.most_common(10): print(n, ip)
EOF
```

Directory-scoring and rank-probe bots hit public `/mcp` continuously. A leak is public
the moment it ships.

## 5. Grading the returned report

Treat the report as a self-report. Three rules, in order:

1. **Replay every claim.** Each finding gets its own probe. Report
   CONFIRMED / REFUTED / PARTIAL with the field path you observed.
2. **Apply the reproducibility window.** Any PASS whose evidence is a telemetry or
   substrate value must be re-run at a *different wall-clock time*. A floor that fires
   off a mutable state file can return PASS at one minute and nothing minutes later
   with no code change. If it flips, the grade is PARTIAL with the window stated —
   never PASS, and the coupling itself is the finding.
3. **Let the out-of-battery finding set the priority.** A clean score followed by
   "one thing outside the battery" usually puts the real result in the appendix.

Also separate "is the floor wired?" (durable, source-probeable) from "did the floor
fire?" (situational, substrate-dependent). Auditors routinely prove the first and
claim the second.

Full procedure: `references/grading-external-reports.md`.

## 6. Reporting back to the sovereign

- Deliver the prompt as a **fenced code block**, one tap to copy. Never embed a
  multi-line command or prompt in prose.
- Lead with what was *measured*, then what it means, then the single next action.
- If the auditor found a defect, credit what they got right before what they missed.
  It is the only thing keeping the loop alive.
- Never paste a person's private payload into chat to prove a leak. Name the category
  and the count; offer to enumerate privately.

## Pitfalls

- **Don't hand out a battery you haven't run locally.** Your own bug read as an
  external finding costs a full round trip and your credibility.
- **Don't grade on the decorative verdict field.** `verdict` can read `completed` while
  `effective_verdict` reads HOLD in the same response.
- **Don't treat a client limitation as a server FAIL.** Establish primitive support
  first; UNAVAILABLE is a legitimate result.
- **Don't accept a flat PASS from a single observation.** Telemetry-coupled behaviour
  needs a second observation at a different time.
- **Don't retry a refusal as if it were a bug.** Refusals are the artifact under test.
- **Don't ship the public endpoint before the read-path check.** Exposure is measured
  in the access log, not in your invitation list.
- **A fix can land mid-audit authored under your own lane identity.** Shared lane
  names let several processes commit as you without a mutex. Run
  `git log -1 --format="%an <%ae>%n%s"` and `git reflog -3` before claiming the commit
  as yours or treating the finding as still open.
- **Don't confuse correlation with consensus.** Two external agents agreeing is one
  witness echoed twice unless both ran the call.

## Support files

- `references/conformance-battery.md` — the T0–T8 battery contract and what each test
  is designed to falsify.
- `references/client-capability-matrix.md` — which host exposes which primitives, and
  the per-platform connection recipe.
- `references/grading-external-reports.md` — claim-by-claim replay procedure and the
  reproducibility-window table.
- `templates/external-conformance-prompt.txt` — the copy-paste prompt.
