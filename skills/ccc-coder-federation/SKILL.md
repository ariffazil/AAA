---
name: ccc-coder-federation
version: 1.0.0
description: "Use when spawning coders or dispatching to CCC pipeline."
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [ccc, coder-federation, agi, asi, apex]
    related: [kimi-code, opencode, codex]
---

# CCC — Codex Coder Compiler

The coder federation. Every CCC member is universal: can reason, build, test, deploy. Role is adat (anchor), not cage.

## Pipeline

```
CCC ──forge/build──► AAA ──govern/seal──► FED ──route/cascade──► arifFlow ──metabolize──► VAULT999
```

## Roster (F13 2026-08-14)

| Coder | Adat Role | Model | Specialty |
|---|---|---|---|
| Kimi Code | AGI | MiniMax-M3 | reason, plan, build |
| Qwen Code | ASI | GLM-5.2 | sense, memory, vision, fast |
| OpenCode | APEX | MiniMax-M3 (Go-zen) | judge, forge, validate, Hermes validator |
| Aider | ROOT | DeepSeek V3 | github, deploy, housekeep |
| Codex | Router | FED cascade | backup, cascade |
| Gemini CLI | Review | Gemini | read-only, NO execution |

## The Adat Agentic Principle

> Role is anchor, not cage. Each coder carries other roles when needed.

"333-AGI" can be Kimi today, Qwen tomorrow. The label describes what the coder IS DOING in this session, not a permanent binding.

**Pitfall:** Do NOT over-formalize with FI numbers until the system is stable. Labels (AGI/ASI/APEX/ROOT/Router/Review) are sufficient. Numbers add entropy when the binding is fluid.

## Universal Init

Every CCC member loads:
1. `/root/AGENTS.md` — constitution
2. `/root/AAA/prompts/INIT.md` — boot ritual
3. `/root/AAA/governance/ZEN_EXECUTION_DOCTRINE.md` — execution rules
4. Full skill library + all repo access

## Inner Loop (per session)

```
MEANING → OBSERVE → ENCODE → IMPROVE → VERIFY → SEAL → RETURN
```

## Outer Loop (72h, synced with Dream Engine)

```
DEPLOY → MONITOR → DRIFT CHECK → ENTROPY AUDIT → SOT SYNC → README TRUTH
```

## Dispatch Pattern

SPEC is CLI-agnostic. Write once, dispatch to whoever has quota. Verify all outputs independently — never trust self-report.

## Canonical Repo Map (F13 2026-08-14)

| Organ | GitHub | Local | Notes |
|---|---|---|---|
| AAA | ariffazil/AAA | /root/AAA | **Canonical root** — all governance |
| arifOS | ariffazil/arifOS | /root/arifOS | Kernel |
| A-FORGE | ariffazil/A-FORGE | /root/A-FORGE | Execution |
| HERMES | ariffazil/HERMES | /root/HERMES | Bridge |
| GEOX | ariffazil/GEOX | /root/GEOX | Earth |
| WEALTH | ariffazil/WEALTH | /root/WEALTH | Capital |
| WELL | ariffazil/WELL | /root/WELL | Human readiness |
| arifFlow | ariffazil/arifFlow | /root/arifFlow | Metabolism |
| FRAME | ariffazil/FRAME | /root/FRAME | Measurement (private) |
| arifOS-model-registry | ariffazil/arifOS-model-registry | /root/arifOS-model-registry | Model provenance |

**GitHub repos that DO NOT EXIST (archived 2026-08-14):**
- `ariffazil/FED` — code lives in `AAA/scripts/fed_router.py`
- `ariffazil/FLAME` — code at `/root/FLAME/` (systemd `flame-api.service`), no remote

## Pitfalls

- **Don't lock role = CLI permanently.** Kimi quota dies → Qwen becomes AGI. That's adat.
- **Don't create FI numbers for coders until system stabilizes.** Names suffice.
- **Gemini CLI = review only.** No execution evidence — do not trust its output as deployed.
- **OpenCode tools fail silently.** Check opencode logs when a tool silently doesn't work.
- **MiniMax auth inside Kimi harness: use `minimax-coding-plan`, NOT `minimax-direct`.** Direct sends wrong header format (Authorization: Bearer vs X-Api-Key).
- **FED/FLAME/FRAME are NOT independent repos.** They are AAA-internal organs. FED GitHub repo was deleted; code is in `AAA/scripts/`. FLAME GitHub repo was deleted; code is at `/root/FLAME/` with a live systemd service. FRAME exists on GitHub (private). **Do not create new repos for these.** Pushing to nonexistent remotes wastes auth attempts.
- **Pre-push hooks may require `REPO=` trailer.** Some repos (e.g. WELL) reject pushes without `REPO=<name>` in every commit message. Fix with `git filter-branch --msg-filter` to add trailers retroactively.
- **SSH agent not loaded = push failures.** `eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519` before pushing to `git@github.com:` remotes.

DITEMPA BUKAN DIBERI ⚒️
