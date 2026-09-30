---
name: forge-so-what-deliverables
description: Use when Arif hands an audit/spec and asks so what.
---

# forge-so-what-deliverables

> **One input → diagnose → fork into three outputs → close with F13 binaries as A/B/C.** The user hands a long audit, spec, or essay (often his own past work, sometimes a peer agent's) and asks for the same shape every time: tight diagnosis + human-language version for sharing + a copy-paste prompt for coding agents + what will happen if executed + F13-class choices framed as multiple-choice, not a menu.

## When to use

Trigger phrases (any one is enough):
- "so what" / "so what will happen if all that being executed"
- "turn that to full human language"
- "give me prompt / coding agent prompt / I copy paste"
- "what to prompt coding agents"
- An attached PDF/essay/audit followed by "so what" with no further instruction

Distinct from `pasted-material-analysis` (which is general reading of material he pasted). This skill triggers when the ask is specifically "fork this into deliverables" — diagnosis + human-version + coding-prompt + consequence-forecast + F13-binary. `pasted-material-analysis` covers the wider case of pasted material he wants read, summarised, or kept; this skill covers the narrower case where he already knows what the input is and wants the three named outputs produced.

## Procedure (in this exact order)

### 1. Extract the doc (PDF/DOCX/essay)

```bash
which pdftotext && pdftotext -layout "<path>" - | head -400   # default fallback
# Try pymupdf / pdfplumber / python-docx if pdftotext is not enough
```

Read every cited source before responding. A spec with citations it cannot defend is investigation by gloss. Cheap sources (PubMed/PMC/arXiv/Wikipedia/Royal Society) can be `web_extract`ed in the same turn the user is reading.

### 2. Tight diagnosis (3-7 lines)

Three buckets, never a verdict on the input as a whole:

- **What holds** — claims already ratified here / well-grounded / cited from primary source.
- **What's weak** — claims that contradict docs already on disk, math that doesn't reconcile across phases, unspecified call sites, F13 punts left open.
- **What needs you** — single binary that only Arif can decide, named as such, with the cost of each side.

Lead with the diagnosis the user actually needs (the load-bearing one), not the most clever one. If the doc lists 5 failures, pick the 2-3 that change downstream action; the rest go in one line.

### 3. Full human-language version (for sharing)

Plain BM Penang register. NOT formal English. NOT bullet-list-only — when the material has paragraphs, keep paragraphs. Strip jargon: F-numbers, SCAR, ΔS, "trace", "node", "witness mode", "J-SPACE", "constitutional membrane" all stay internal.

Three sections in this order:

1. **Sekarang** — current state, no spin. Numbers and dates stay concrete.
2. **Apa yang berubah** — what runs differently for the user / the friend / the colleague after this ships.
3. **So what untuk manusia biasa** — one paragraph that lands on a concrete surface: their phone, their chat group, their next morning.

If the doc carries a Failure Modes / Watch List table, keep it but translate each row to plain language. If the doc has arithmetic that doesn't reconcile (Phase 2 vs Phase 4 byte targets), say so explicitly — do not smooth.

### 4. Copy-paste prompt for coding agents

One self-contained markdown block. Rule: a future agent receiving this prompt should produce the right work without seeing any prior context.

Mandatory sections in this exact order:

```
# ROLE — who the agent is, who authorised, signing form
# MISSION — one sentence, the deliverable
# HARD CONSTRAINTS — never-authorise, trace_id receipts, state-transition discipline,
#                    probe-before-panic, F13 binaries (one short ask), no jargon in chat
# CURRENT AUDIT FINDINGS — the live numbers (byte counts, line counts, gap claims)
# DELIVERABLES — Phase 2 / Phase 3 / Phase 4, each with concrete output contract
# FAILURE MODES TO PREVENT — from the spec, with mechanism named
# OUTPUT CONTRACT — node declaration, transition state not Boolean, HOLD = gate name + ranked options
# OPERATIONAL RULES — which AAA instructions to read first, musyawarah before consequential mutation
# WHAT YOU DON'T DO — anti-bangang-law-3 reminder, no new canon unless failure class real
# AUTHORITY — MAY / MAY NOT modify, archive, deploy
```

Hard rule: every "DO" first must come with a receipt schema (`{trace_id, action, file_path, byte_delta, test_pass, evidence, unknown}`). Every "DONE" must come with `{state, scope, evidence, unknown}`. No Booleans.

### 5. Consequence forecast (real outcome)

Two sections. Short.

- **Best case — semua smooth ship:** what happens when each phase lands clean. Concrete deltas: latency, byte size, capability count, identity stack layers, fail-mode surface area.
- **Realistically — what risks:** name the 3-5 highest-probability failures, each with one sentence on the mechanism. If a Phase target (-70%) contradicts a quick-reference (-94%), name both. If a F13 punt (identity-interceptor, gate-hook parity, channel_prompts, SOUL.md STYLE_ONLY) is unresolved, name it — the prompt cannot ship past it.

Close with **"macam mana rupanya sebulan dari sekarang"** — one paragraph. If everything ships vs if there's a slip. Two readings, both honest.

### 6. F13 binaries as A/B/C, never a menu

Two rules:

- **Three options, no more.** A is "do nothing / HOLD", B is the named minimal move, C is the next-step. If you can only think of one option, present A/B (A = HOLD, B = that one option) and stop.
- **Each option carries one concrete cost in plain language.** Not jargon. "Identity stays where it is" beats "P0-1a state holds". "Code goes onto the live kernel" beats "promotion to apex tier".
- **End with one recommendation.** Rank the options by what the user already said they care about in this session. Do not ask "which do you prefer" — name the option that matches their stated bias and ask them to confirm or override.

Forbidden closing shapes: "would you like me to…", "let me know which", "Option 1 / Option 2 / Option 3" with no recommendation, anything that re-emits the question as a menu.

## Pitfalls (durable rules)

- **Diagnosis ≠ verdict.** The diagnosis names what holds vs what is weak. The user decides what to do. Never collapse into "this is good / this is bad" — that is exactly the pattern the user pastes these inputs to escape.

- **Three outputs share facts, not prose.** The same byte count, the same F13 punt, the same citation must appear in all three (diagnosis / human-version / coding-prompt) when load-bearing. If the diagnosis names `-94%`, the human-version names `-94%`, and the coding-prompt constraints name `-94%`. Drift across the three forks is the failure shape.

- **The human-language version is for sharing with non-coders.** When the user says "turn that to full human language", the audience is his friend Syed, his mum, a friend who asked "apa ni semua" — not a peer agent. Strip the verdict words that read as jargon (`RATIFIED`, `DRAFT`, `GO`, `SEAL`, `FAIL_CLOSED`, `REVIEW_ONLY`, `STYLE_ONLY`, `state-transition`). Translate or omit. Translate "F13 binaries awaiting GO" to "F13 questions waiting for Arif's word".

- **The coding-agent prompt must be self-contained.** A future session receiving it produces the right output even if the conversation is in error. That means: full file paths, full commands (not "see /root/AAA/instructions/X"), explicit byte deltas, explicit authority list. The user pastes this prompt into a separate worker (kimi / qwen / opencode) and never references back to us.

- **Never ship a consequence forecast with no slip case.** If everything ships perfectly, the forecast is theatre. Always name the realistic failure surface — even if the user already mentioned it.

- **F13 binaries are read once, not re-asked.** Once the user names the binary (count = 9 vs 8, byte target = -70% vs -94%, restore vs update claim, ROLE hint vs remove), the next session must NOT re-ask. The state-transition discipline applies to the audit answer too.

- **Quote NO back at the user.** When the user asks "so what", do not echo "so what" back at him. Lead with the diagnosis. The reflection-theatre trap ("here is the question you asked, here is what I noticed about your question") is exactly the pattern he pastes these inputs to escape.

- **Anti-bangang law 8 holds here.** One fork = three outputs, not five. Don't add a fourth deliverable (a slide deck, an exec summary PDF, a Notion page) unless the user asks. Two binaries ≠ three binaries; the closing option count stays at three.

- **The audience for the coding-agent prompt is the worker, not the user.** Worker register is technical: AAA-instruction references, `python3 -c` calc requirements, `trace_id` schema, `HOLD = gate name + ranked options`. The user-facing message in the same reply is BM Penang. Two registers, same reply — keep them clearly separated by `## N. Coding Prompt for ...` headers, not by interleaving.

- **Do not mutate canon to satisfy a doc.** If the doc says "12 attributes" and runtime has 9, the diagnosis names the gap; the user decides. The agent does not patch canon to match the doc, and does not patch runtime to match canon. The gap is the finding.

## Quick shape of one full reply

```
[Diagnosis — 3-7 lines, plain text, dialect voice]

## 1. Full Human-Language Version
[for sharing with non-coders]

## 2. Coding Agent Prompt — Copy-Paste Ready
[technical, self-contained]

## 3. Consequence Forecast
[best case + slip case + one-month read]

[Closing]
Three options. C is my pick, because [reason in one line from this session's bias].
Confirm C, or say which to swap.
```

Length: diagnosis under 10 lines. Human-version about half the doc length. Coding-prompt sized to fit one chat-paste (≤4000 chars). Consequence forecast 5-10 lines. Closing 3-5 lines.

---

*DITEMPA BUKAN DIBERI ⚒️ — class-level skill for the "so what + human-language + coding-prompt + F13-binary" fork workflow.*