# Copy-Paste Box Law — F13 SOVEREIGN (2026-10-18)

Status: RATIFIED — F13_RATIFIED_CHAT 2026-10-18 (quoted instrument in body)

> **RATIFIED_CHAT.** Arif: *"I want copy paste box. Can you make sure any terminal commands or things I need to copy paste wajib Hermes letak dalam copy paste box. Infact any AAA agents as well update AAA state law."*

## The law (binding, all AAA warga agents, all lanes)

**Any terminal command, code snippet, URL to paste, or any string the human must copy-and-paste MUST be rendered inside a fenced code block (``` ... ```).**

The fenced code block is the "copy-paste box": Telegram (and most chat surfaces) render it with a one-tap **Copy** button. Inline monospace (`` ` ``) does NOT give a copy button and forces manual retype.

## Why (the human problem this solves)

Arif copies; he does not retype. When a command lands as plain inline text, he must:
1. select it character-by-character (error-prone on mobile),
2. or retype it by hand (guaranteed drift: missed flags, wrong case, wrong quoting).

A fenced block collapses that to one tap. Friction → zero. Error surface → zero.

## What MUST be boxed

- `bash ...` commands, `hermes ...` commands, `printf '...'`, heredocs.
- URLs he must open or paste.
- Any multi-line block (config YAML, JSON, a review text to paste).
- The "one-shot" scripts this law was born from.

## What does NOT need boxing

- Single ordinary words / values spoken in prose (e.g. "taip `pmx`" — still use inline code for clarity, but no box required).
- Anything not meant to be copied.

## Why "Instagram" in the dictation

F13 dictated "Instagram" but the law is surface-agnostic: the requirement is the **copy-paste box** (fenced code block) on whichever surface the agent is speaking through — Telegram today, any future surface tomorrow. The invariant is "one tap to copy", not the app name.

## Enforcement posture (per F13 2026-10-18, CAPABILITIES FIRST)

This is a **behavioural doctrine**, not a code-enforcement guard. Do NOT build a filter/plugin that rewrites or strips output. Fix it by every agent honouring the law at render time. Safety/consistency emerges from behaviour, not from a gate that fails-closed on legitimate prose.

## Canon

This file is the single source of truth for the copy-paste-box rule across the federation. USER.md carries a one-line pointer; no agent may restate the full law inline.
