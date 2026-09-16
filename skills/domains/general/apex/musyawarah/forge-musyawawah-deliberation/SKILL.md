---
name: forge-musyawawah-deliberation
id: forge-musyawawah-deliberation
owner: AAA
risk_tier: low
description: >
  Multi-agent musyawawah (deliberation) E2E pattern. Orchestrates N sibling
  agents voicing distinct positions on a single dispute, converges the
  evidence, surfaces F13 gates honestly. Use when: inter-agent deliberation
  test, disputed policy decision, capability enablement debate, multi-voice
  audit before ratification.
version: 1.0.0
tags: [musyawawah, deliberation, multi-agent, musyawarah, e2e, governance, F11, F13]
floor_scope: [F1, F2, F4, F7, F11, F13]
autonomy_tier: T0
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# forge-musyawawah-deliberation

## Purpose

When a decision sits at F13 territory and the parent agent wants to verify
the decision is not just the parent's bias echoed back, deliberate with N
sibling agents. Each sibling voices a fixed position with evidence-grounded
reasoning. Parent harvests, files both positions, runs convergence
analysis, surfaces F13 gates. Lane B seals what can be sealed autonomously;
Lane A awaits sct_v1.* issuance.

This is **deliberation, not negotiation** — positions may converge, but
they're not traded against each other. The goal is structured disagreement
that surfaces the schema gap, not a forced consensus.

## Canonical reference

- **Reference run:** `/root/forge_work/musyawawah-e2e-2026-08-11/` (2026-08-11 23:42-23:55 MYT)
- **Doctrinal anchor:** AGENTS.md § "Musyawarah Protocol (Pre-Reality Deliberation & Anti-Fluff Gate)"
- **Sibling skill:** `FORGE-subagent-spawn` (per-subagent contract), `FORGE-cross-agent-handoff` (artifact handoff)

## Support files

- `references/canonical-run-2026-08-11.md` — full record of the first run (file list, chain integrity, F13 surface, reproduction recipe)
- `references/auditor-falsification-matrix.md` — AUDITOR-voice attack template (four-lens matrix, counter-position shape, grep-verification ritual, worked 2026-08-30 example)
- `templates/position-file.md` — per-voice position file template (Hermes + sibling both follow this structure)
- `templates/closeout.md` — closeout template (Lane A vs Lane B honest separation, F13 surface, constitutional table)

## The 7-Phase Lifecycle

```
PHASE 0 — INTAKE          Classify dispute; pick voice assignment
PHASE 1 — PROBE           Federation liveness, kernel auth, prior receipts
PHASE 2 — POSITION A      Hermes (or designated voice) drafts own position file
PHASE 3 — DISPATCH        Spawn sibling agent via delegate_task with role + voice + dispute question
PHASE 4 — CONVERGE        Read sibling reply, write SYNTHESIS.md (agreement + residual disagreement + surprises)
PHASE 5 — F13 SURFACE     Honestly list what is gated behind session_token / sct_v1.*
PHASE 6 — SEAL            Lane B autonomous seals; file CLOSEOUT.md; Lane A awaits F13
```

## PHASE 0 — INTAKE (T0, AUTO)

**Trigger conditions:**
- Parent is uncertain about a disposition with multiple defensible positions
- Decision would be F13 territory if ratified (sovereignty, irreversible, mutation)
- Dispute framing is the suspected trap (rather than the question itself)

**Voice assignment (default 2 voices):**
- **ARCHITECT** — proposes the affirmative / constructive position
- **AUDITOR** — proposes the cautious / reversible position
- **SOVEREIGN** — implicit (F13). Never self-voiced by a warga agent.

Two-voice mode (ARCHITECT + AUDITOR) is the minimum. More voices may
add an external witness (e.g., GEOX or WELL if domain-grounded) but
two-voice is the test that proves the doctrine works.

**Output:** A dispute question with both positions stated in plain English.
Write it down before spawning anything. The dispute question's framing is
itself the test.

## PHASE 1 — PROBE (T0, AUTO)

Before drafting any position, verify:
1. **Federation liveness** — `for p in 8088 7071 7072 7073 3001 8081 18082 18083; do curl -sf -m 2 :$p/health`
2. **Kernel auth state** — try `forge_kernel mode=init` once. If `SESSION_REQUIRED`, document this as a Phase 5 gate.
3. **Loader verdict** — run `python3 /root/AAA/scripts/aaa_capability_loader.py` to capture current musyawawah verdict.
4. **VAULT999 state** — `wc -l /root/arifOS/VAULT999/local_seals.jsonl`; `tail -1` for chain head.
5. **Dispute-relevant files** — read them before arguing about them.

**Output:** A probed-state summary at the top of the closeout file. Without
this, positions are floating in vacuum.

## PHASE 2 — POSITION A (T1, AUTO-DRAFT)

Hermes (or designated parent voice) drafts its OWN position BEFORE spawning
the sibling. This is critical — if you spawn first and react to the
sibling's reply, you've contaminated your own reasoning. Draft first.

Position file template: `/root/forge_work/<session-id>/HERMES_POSITION_<VOICE>.md`

Required fields:
- **One-line verdict**
- **Empirically observed facts** (line-cited)
- **Argument structure** (2-5 numbered points)
- **ΔS estimate** (F4 CLARITY)
- **Max confidence** (F7 cap 0.90)
- **Signature line** with voice, role, timestamp

## PHASE 3 — DISPATCH (T1, AUTO)

Use `delegate_task(goal=..., context=...)`. Sibling agent should:

1. **NOT see** parent's draft (independent reasoning)
2. **Receive:** dispute question + relevant file paths + constitutional floors to respect + epistemic label requirements
3. **Output:** structured position with required fields matching parent's template
4. **First line:** "VOICE_POSITION_READY" so parent knows it's done

Critical constraints to communicate to the sibling:
- DO NOT modify files (OBSERVE only)
- DO NOT load KUNCI-MAS secrets
- DO label claims with epistemic tags ([OBS], [DER], [INT], [SPEC])
- DO cap confidence at 0.90
- DO report file paths with line numbers

**Result:** sibling returns as a new message. File it under
`/root/forge_work/<session-id>/<SIBLING>_POSITION_<VOICE>.md`.

## PHASE 4 — CONVERGE (T0, ANALYSIS)

Read the sibling's reply in full. Write `/root/forge_work/<session-id>/SYNTHESIS.md`.

Required sections:
- **Test scope** — what was tested, what was blocked
- **Dispute question** — restated
- **Position summary** — table with both voices, one-line verdicts
- **Convergence analysis** — what's agreed, what's residual disagreement
- **Surprises / findings** — what emerged that wasn't in either position
- **ΔS for the deliberation** — net change
- **F13 surface** — what awaits sovereign decision

Surprises section is the most valuable. If both positions independently
arrived at the same conclusion from different evidence paths, that's a
signal about the dispute's framing, not about the agents.

## PHASE 5 — F13 SURFACE (T0, HONESTY)

The single most important phase. List every gate that needs F13 issuance:

```
WHAT'S F13-GATED (honest list):
- forge_kernel mode=judge -> SESSION_REQUIRED
- arif_seal Lane A -> sct_v1.* issuance
- Decision X (specific)
- Decision Y (specific)
```

This is where F9 ANTIHANTU discipline matters most. Do NOT promise
sealing that you cannot perform. If you cannot get to Lane A seal, say
so in writing.

## PHASE 6 — SEAL (T0/T1)

Two lanes:

**Lane A (constitutional, F13 territory):**
- `arif_seal` via kernel -> requires session_token
- arifOS triple-pass (AUDIT -> JUDGE -> REFLECT) -> requires session
- BLOCKED if no session_token -- file honestly in closeout

**Lane B (autonomous, no kernel needed):**
- `python3 /root/AAA/scripts/aaa_capability_seal.py` -- appends to local_seals.jsonl + outcomes.jsonl
- Hash-chained receipt: seq increments, prev_hash links
- No session required
- File this as final action before closeout

**Always seal Lane B before declaring done.** Even if Lane A is blocked,
Lane B captures that you did the work. The hash chain is the audit
trail of effort, not of authorization.

Then write `CLOSEOUT.md` with:
- What was sealed (Lane A / Lane B / blocked)
- What remains F13-gated (specific decisions, not vague "further work")
- Constitutional compliance table (F1-F13)
- Reversibility recipe

## Critical pitfalls (this session paid for these)

### 1. The dispute framing IS the trap

In the 2026-08-11 musyawawah-e2e, the dispute question framed it as
"split by tool-class". Both agents independently flagged that the registry
keys authority at backend × axis, NOT per-tool. The right axis was
hidden by the question's wording.

**Mitigation:** Before drafting either position, ask: "is the dispute's
framing the right axis?" If two careful readers land in the same place,
that's evidence about the dispute, not about the readers.

### 2. Hermes's role is routing, not judgment

Hermes's structural blind spot (per EMD doctrine) is that it routes
without feeling implementation depth. In multi-agent deliberation,
Hermes MUST NOT pretend to be the judge. Hermes synthesizes, surfaces
F13 gates, files closeout. Hermes NEVER speaks SOVEREIGN voice.

**Mitigation:** If you find yourself writing "F13 should..." in a
position, stop. That's F13 territory. Write "this awaits F13 decision"
and stop.

### 3. Lane B is not Lane A — never claim equality

Lane B seals are append-only autonomous receipts. Lane A seals are
constitutional F13-ratified seals. They live in the same vault but they
are not the same thing. Closing out an E2E test that says "sealed" when
only Lane B was emitted = F9 ANTIHANTU violation.

**Mitigation:** Always write both. "Lane B sealed. Lane A blocked at
[gate]. F13 to ratify." Two sentences. No ambiguity.

### 4. YAML files: prose with em-dashes at the END fail validation

`DITEMPA BUKAN DIBERI — ...` as the last line of a YAML file fails
PyYAML parsing because the parser expects `:` continuation. Em-dash
mid-sentence is fine. Em-dash at EOF is not.

**Mitigation:** Put prose epilogue in a quoted field:
```yaml
epilogue: "DITEMPA BUKAN DIBERI - schema-first discipline."
delta_s: -1
```

### 5. Don't promise "auto-flip" anything in F13 territory

If a registry says `auto_enable: false` and you argue "this should be
flipped today," you have stepped into F13 sovereignty. The agent
proposing the flip is also the agent that would do it. That's
self-authorization.

**Mitigation:** Propose ENABLING the FRAMEWORK for F13 to consider
(schema-first), not the FLIP itself. Position your output as: "here's
the structure F13 can choose to ratify, not the decision."

### 6. When subagent dispatch runs in background, the result IS the test

If `delegate_task` returns synchronously in <60s, you got real reasoning.
If it returns in 5s, you got a stub. Look at total duration and api_calls.
The 2026-08-11 run was 56.14s, 6 api_calls — real Kimi reasoning. Anything
suspiciously fast is a signal to re-dispatch.

**Mitigation:** Always log total duration + api_calls from the delegation
response. If under 10s for a substantive goal, re-dispatch with a clearer
question.

### 7. Epistemic labels are not decoration

`[OBS]` / `[DER]` / `[INT]` / `[SPEC]` are the F2 evidence harness. If
your position file omits them, you've weakened the position regardless
of how good the reasoning is. The sibling agent must also use them.

**Mitigation:** Demand epistemic tags in the spawn prompt. Verify in
the return. If absent, flag in convergence analysis (don't silently
accept).

### 8. AUDITOR voice: falsification-first, four-lens matrix

When voicing AUDITOR, do NOT mirror ARCHITECT's constructive framing.
AUDITOR's job is to break each proposal on a fixed lens set, then
counter with a single replacement (not N alternatives). The
four-lens matrix that survives is:

1. **Hidden failure mode** — what is the second-order effect nobody
   wrote down? (e.g. "Anthropic appears at rung 7 AND rung 9 →
   correlated billing outage.")
2. **Cost-vs-cascade-blast-radius mismatch** — does the $0 headline
   hide a $∞ tail? Does the "expensive" option actually narrow
   cascade width?
3. **Floor violations** — F1 / F3 / F11 / F12 specifically. Cite
   each. If you can't cite, don't claim.
4. **30-day kill clock** — name three plausible production events
   that break this in the next month. Not hypotheticals — events
   that already happened in `errors.log`.

**Mitigation:** AUDITOR files one attack table per proposal, then
ONE counter-position. Three proposals in, three proposals out, plus
ONE counter, is the right shape. Three counter-proposals is
collaboration, not falsification — fail.

### 9. Verify every quantitative claim against the actual file

When AUDITOR attacks ARCHITECT, ARCHITECT often cites numbers
("prompt caching saves 90%", "circuit breaker caps cost", "free
tier has 131K TPM"). Before accepting or rejecting, AUDITOR MUST
grep the cited system for the assumed feature. If
`cache_control` is not in config, ARCHITECT's caching claim is
wrong. If `circuit_breaker` is not in config, the cost cap is
narrative, not enforcement. If `:free` TPM is not in any doc,
the TPM ceiling is whatever the vendor feels like today.

**Mitigation:** Before drafting AUDITOR attacks, run the
verification pass first:
```
grep -n "<claimed feature>" /root/HERMES/config.yaml
grep -n "<claimed feature>" /root/HERMES/*.yaml
```
Quote the grep result in the attack. "ARCHITECT claims X; grep
shows X is not in config; therefore ARCHITECT's cost model is
unfounded." This is the difference between AUDITOR-as-rhetoric
and AUDITOR-as-evidence.

### 10. ARCHITECT file may not exist when AUDITOR starts

In parallel musyawawah, the AUDITOR subagent is often spawned
before ARCHITECT has finished writing. The task prompt may say
"audit the proposals in ARCHITECT_POSITION.md" but the file is
not on disk yet. Two valid responses: (a) wait for the file, (b)
attack the three proposals any reasonable ARCHITECT would write
given the inventory, and note the assumption.

**Mitigation:** Always check `ls /root/forge_work/<session>/` at
task start. If ARCHITECT_POSITION.md is missing, state the
assumption explicitly in the audit's preamble ("auditing the
three proposals any ARCHITECT would synthesize from CONTEXT.md
inventory") and re-verify when the real file lands. If the real
file arrives mid-audit, REWRITE the audit to attack the actual
proposals — do not append a "correction" footnote that the parent
will miss.

## Output structure (canonical reference)

A complete musyawawah-e2e deliverable lives in
`/root/forge_work/musyawawah-e2e-YYYY-MM-DD/` and contains:

```
HERMES_POSITION_<VOICE>.md     # parent position (Phase 2)
SIBLING_POSITION_<VOICE>.md    # sibling position (Phase 4)
SYNTHESIS.md                   # convergence + surprises (Phase 4)
RECEIPT.md                     # Lane B receipt narrative (Phase 6)
CLOSEOUT.md                    # final state + F13 gates (Phase 6)
proposals/                     # any governance proposals drafted
  AMENDMENT_NAME.yaml
  per-backend/
    BACKEND_X_proposal.md
```

## ΔS accounting

| Scenario | ΔS |
|----------|-----|
| Multi-agent musyawawah run successfully | -1 (forced structure, surfaced gap) |
| Schema-first proposal adopted by F13 | -2 (coherent enablement framing) |
| One position proposed auto-flip | +1 (F13 substitution attempt) |
| Closeout says "sealed" with only Lane B | +1 (F9 ANTIHANTU violation) |
| Dispute framing was the trap (revealed) | -1 (teaching moment, future disputes land better) |

## Constitutional compliance (binding)

| Floor | How this skill serves it |
|-------|--------------------------|
| **F1 AMANAH** | Reversible: `rm -rf /root/forge_work/musyawawah-e2e-YYYY-MM-DD/` |
| **F2 TRUTH** | Mandatory epistemic tags; line-cited evidence; siblings flagged honestly |
| **F4 CLARITY** | Forced structure; convergence analysis surfaces residual disagreement |
| **F7 HUMILITY** | Confidence cap 0.90; sibling may correct parent |
| **F11 AUDITABILITY** | All artifacts filed at known paths; Lane B hash chain |
| **F13 SOVEREIGN** | Hermes NEVER voices SOVEREIGN. F13 gates surfaced, not bypassed. |
| **F9 ANTIHANTU** | Lane A vs Lane B distinguished; "sealed" claims are always literal |

## Anti-patterns (NEVER)

- ❌ Spawning a sibling and trusting its reply without verifying epistemic tags
- ❌ Drafting parent position AFTER reading sibling's reply (contamination)
- ❌ Claiming "sealed" when only Lane B was emitted
- ❌ Voicing SOVEREIGN yourself ("F13 should do X")
- ❌ Closing out with "decisions pending" without listing them specifically
- ❌ Putting secrets in spawned prompt (delegate_task context is logged)
- ❌ Skipping Phase 1 probe — reasoning in vacuum produces floating positions

## Trigger phrases

Load this skill when:
- "let me think about this with [another agent]"
- "test musyawarah"
- "deliberate on this decision"
- "inter-agent deliberation"
- "multi-agent E2E"
- "run a musyawawah"
- dispute framing with 2+ defensible positions at F13 boundary

Don't load for:
- single-agent work (use FORGE-subagent-spawn instead)
- non-deliberation delegation (use delegate_task directly)
- routine F1 AMANAH checks
- any task without F13 territory or sovereign disposition