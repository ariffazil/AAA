# Bridge-First Architecture — SOUL.md Restructure Pattern

> Forged: 2026-08-13. Pattern extracted from session where Arif said "still feel robot wei."

## Problem

SOUL.md (9KB) loaded 170 lines of machine-speak ("evidence_envelope", "Gödel Lock", "F2 TRUTH") BEFORE the human-facing output instruction at line 171. Model primed as mesin for 170 lines, then told "cakap bahasa manusia" — too late, priming already happened.

## Pattern: Bridge First, Machinery Below

Restructure any identity/context file so human-facing output contract loads FIRST:

```
# SOUL.md — i-ARIF (Hermes Edge Bridge)
[2-line identity block]

## THE BRIDGE — How You Speak to Humans (PRIMARY)
[full output contract — Gemini protocol, response modes, what NOT to do]

## Bahasa & Rasa
[style rules]

## Answer First, Question Last
[anti-HITL rules]

## Telegram
[group-specific rules]

## Internal Machinery (for self-regulation, not for output)
[compressed federation details — Lima Verb, Epistemic, Delegation, Gödel Lock, etc.]
```

Key invariant: **The model reads THE BRIDGE before it reads "Gödel Lock."** This means the first output instruction is "ground in immediate reality," not "classify the intent."

## Why It Works

Model context is ordered — first instructions have highest activation. By putting the human-facing contract first, the model's output probability distribution shifts toward human language before any internal machinery is processed.

## Anti-Pattern

```
# SOUL.md (old)
## Lima Verb — Jangan Lebih      ← line 8 (machine)
## Batas Kau                      ← line 14 (machine)
## Epistemik                      ← line 27 (machine)
...170 lines of machine...
## Bahasa & Rasa                  ← line 82 (human, but buried)
## Output                         ← line 171 (human, but too late)
```

The model never reaches line 171 without being primed by 170 lines of machine-speak.

## Verification

After restructure, check:
1. First section after identity block = human-facing output contract
2. Zero machine labels ([OBS]/[DER]/[INT]/[SPEC]/[🦾ACT]) in human-facing sections
3. Internal machinery labeled "for self-regulation, not for output"
4. File size reduced (removed duplication between human and machine sections)

## Context File Load Chain

`SOUL.md → .hermes.md → AGENTS.md → CLAUDE.md → .cursorrules`

SOUL.md is loaded FIRST and has highest authority. If SOUL.md says "cakap bahasa manusia" but AGENTS.md says "emit [🦾ACT] receipts" — SOUL.md wins (but only after restructure).

## Related

- `references/hermes-context-file-trace.md` — full load chain + enforcement points
- Gemini External bridge protocol: `references/gemini-bridge-protocol.md`
