---
name: cross-audit-v1
description: "Use when user pastes another AI's output for verification."
version: 1.0.0
risk_tier: low
autonomy_tier: T0
owner: F13 (ratified)
license: MIT
tags: [audit, evidence, cross-ai, paste, intake, conversation-protocol]
triggers:
  - "the user pastes another agent's output"
  - "the user asks to audit / verify / cross-check pasted AI content"
  - "the user says 'audit this' or 'check this' about external AI output"
  - "the user asks 'is this real / can I trust this'"
audience: [hermes, all-harnesses, F13-bound]
capability_tier: meta-mesa
---

# Cross-Audit v1 — Verification Protocol for Pasted External Agent Output

> **Convention** — Ratified by F13 (Muhammad Arif bin Fazil) on 2026-09-24 during session. Standing rule: every pasted agent output that the user asks you to assess passes through this filter before you adopt any claim from it.

The user pastes the output of another AI (Copilot, Perplexity, ChatGPT, OpenClaw, custom agent, …). You are being asked to audit, not adopt. The default reflex is therefore **rejection-pending-evidence**, not acceptance.

## When to apply

- User pastes another agent's output and says "audit," "verify," "check this," "is this real," "can I trust this," or anything equivalent.
- User pastes without explicit ask but the content affects a decision the user will make — apply the filter anyway.
- **Do not** apply to your own output, subagent transcripts from this federation (those use the audit-bridge pipeline), or primary documents (those use `arifos-evidence-policy`).

## The four-axis filter — every audit answers all four

### 1. Evidence

For every load-bearing claim (a number, a path, a name, a "X did Y," a citation), name its primary source. If the source is the pasted agent's own prose, the claim is **agent-attributed** and must be labelled as such; if it cites an external document, follow the citation to the document and confirm it exists.

**Question for the audit:** *Can a stranger re-derive the claim from the cited source, without the agent?*

A claim that survives only because the agent said it is not evidence — it is assertion. A claim that survives a stranger's independent reach to the same source is evidence.

### 2. Authority

**Whose authority is the agent speaking under?** A Copilot/Perplexity/ChatGPT output is the AI vendor's, not the user's. If the pasted output describes the user's beliefs, decisions, or inner state in a way the user did not author, that is **fabricated intimacy** — the agent has manufactured closeness to the user. Flag it.

**A directly-relatable concern.** A pasted AI that quotes the user's own earlier message and audits it is not auditing the user — it is auditing an artifact the user already saw. Distinguish the two.

**Question for the audit:** *Is the agent speaking about the user with authority the user actually granted?*

### 3. Value

The audit's third axis is whether the pasted output added anything the user could not have produced themselves. If the output only restates the user's question or paraphrases their existing beliefs back to them, value is zero — say so. If it added a non-obvious insight or a verifiable specific, the audit's job is to **carve that insight out** and isolate it from the surrounding noise.

**Question for the audit:** *What does the pasted output contribute that the user could not have produced alone?*

### 4. Consequence

Output with a low failure cost (a curiosity, a stylistic tweak) and output with a high failure cost (medical, legal, financial, relational) are not equal under audit. A 30% error in a coffee recipe is a recipe edit; a 5% error in a custody filing is a court filing. **The threshold of acceptable error changes with the consequence surface.**

**Question for the audit:** *If this output is wrong, what breaks, and at what cost?*

## Three operational questions (apply before quoting anything back)

These three questions are the standing filter at every audit, on top of the four axes:

1. **What in the pasted output can you not verify from a primary source in this session?** — list the unverifiables; the user's questions that depend on them carry that gap into the report.
2. **Who authorised the agent to speak about the user specifically?** — if no one, the agent's intimacy is fabrication.
3. **What does the pasted output make the user feel, vs what does it actually say?** — flattery that lands as reassurance flatters without informing. Note the gap.

## Operating procedure (in order)

1. **Snapshot the input.** Capture the pasted output verbatim, note its source (which AI, which conversation, what timestamp), and save it under the audit lane for future reference if the user is in a long-term project. *Do not* paste it back to the user — the source they gave you is the source.

2. **Strip the framing, keep the claims.** Most pasted output is a frame ("As an expert…") wrapping some actual claims. Reduce the paste to a numbered claim list. Long, well-formed text is mostly already-ratified doctrine restated from another angle; the audit's contribution is the **diff** against the user's existing knowledge, not a re-reading.

3. **Run the four-axis check on each numbered claim.** For each claim:
   - *Evidence:* trace to primary source. Mark **VERIFIED / METHOD-DEPENDENT / FALSIFIED / UNDERSTATED / UNREPRODUCIBLE**.
   - *Authority:* is the agent speaking about the user, for them, or past them? Mark **FOR-USER / ABOUT-USER / AMBIGUOUS**.
   - *Value:* did the agent add anything new? Mark **NEW / RESTATED / SUPPORTED**.
   - *Consequence:* if this claim is wrong, what is the cost? Mark **LOW / MEDIUM / HIGH / IRREVERSIBLE**.

4. **For every AGENT-ATTRIBUTED claim without a reachable primary source:** add to `UNVERIFIABLE`. Do not quote it back to the user without the qualification. Do not delete it — surface the gap honestly.

5. **For every ABOUT-USER claim (agent describing the user's beliefs/decisions/inner state):** check that the user has actually granted the agent standing to do so. If not, flag as **FABRICATED INTIMACY** and recommend the user treat the agent's reading as **opinion, not record**.

6. **Quote the live primary source where possible** rather than the paste. An independently-reached number beats a paste of the same number on authority grounds; the user wants to know whether the underlying claim holds, not whether the source-of-record exists.

7. **Apply SO WHAT?** last. The user wants to know if they can act on the audited output. State which parts are safe to act on under what conditions, which parts require further verification, and which parts should be discarded.

8. **Close the audit.** Offer the user's next decision boundary as a single short question if needed; never start a menu.

## Pitfalls (generalised rules; not session narratives)

- **A long, well-formed paste is mostly already known doctrine restated from a new angle. Audit the diff, not the agreement.** The valuable sentence is the one that names something absent from the user's canon, not the twenty sentences that paraphrase what is already there.
- **A pasted critique that quotes the user's own earlier message and audits it is auditing a past artifact, not the user's current position.** Distinguish the two in your reply; an audit of a past artifact is not an audit of the user.
- **Several agreeing models are one witness, not many.** Different AI vendors trained on overlapping corpora will converge on the same flattering reading; consensus among them is not corroboration, and an unmeasurable rating ("very high," "far ahead") is praise wearing the shape of a measurement.
- **A verdict that grades the user as a person, instead of auditing the artifact, is a report card.** When the user asked for an audit and got back a portrait (intellectual age, system age, emotional age), the instrument has changed target. Return it unopened, name the pattern, and request the user re-state the audit target.
- **Aggregator salience labels are that agent's claim about salience, not a finding about the world.** A triage AI marks items "high signal / needs action"; those are its labels, not ground truth. Carry the raw observation and your own assessment; never relay the upstream ranking as fact.
- **Engagement is not endorsement.** A reply, an acknowledgement, or an offer to discuss proves the counterparty engaged — frequently it is risk management, procedure, or courtesy — and says nothing about how they value the work or the person. Where the interior genuinely matters, do not speculate; propose a cheap discriminating probe.
- **A pasted MEASURED value that the agent computed is not a measurement** unless the user (or an independent party) reaches the same value by the same method. Reproduce every figure with its scope before judging the verdict.

## Output shape that survives the audit

Lead with the diff, not the agreement. A clean audit reads like a defects list, not a summary.

```
AUDIT — <pasted output source, date>

EVIDENCE
- Claim 1: VERIFIED at <source:line>; carry.
- Claim 2: AGENT-ATTRIBUTED; no primary reachable; surface as a gap, do not quote.
- Claim 3: FALSIFIED at <source>; the agent cited the wrong edition.

AUTHORITY
- Claims about the user's decisions <list>: AMBIGUOUS — the agent has no grant to speak about the user.

VALUE
- Adds nothing not already in the user's canon: RESTATED.
- Adds one new verifiable specific: NEW.

CONSEQUENCE
- Acting on claim 2: cost = MEDIUM; recommend a second independent source before adoption.
- Acting on claim 3: cost = HIGH; do not adopt until the cited source is corrected.

UNVERIFIABLES
- <list>

SO WHAT: the user can carry claims 1 + 4, must seek a second source for claim 2, and discard claim 3.
```

The closing question is the user's next decision boundary, named in one line, not a menu.

## Verbs that cross-audit uses

| Verb | Means |
|---|---|
| **VERIFY** | the claim survives the primary source check |
| **CARVE OUT** | the relevant fragment of a noisy audit is extracted and isolated |
| **DISCARD** | the claim is unverified or contradicted; do not propagate |
| **FLAG** | the claim has a structural issue (fabricated intimacy, salience laundering) and needs the user's interpretation, not adoption |
| **RECAST** | the user's underlying question can be answered better by re-asking without the paste in hand; surface that path |

## Compatibility notes

- Use alongside `arifos-evidence-policy` for claim-state labels (MEASURED / INTERPRETED / HYPOTHESIS / UNKNOWN).
- Use alongside `auditable-numeric-artifacts` for any figure that escapes the audit.
- The four axes are not a checklist for agreement — they are a checklist for disagreement, and the audit's value is the contradictions it surfaces, not the confirmations it accumulates.

DITEMPA BUKAN DIBERI ⚒️
