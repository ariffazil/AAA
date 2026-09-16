# Guardrail Audit Methodology — 3-Tier Safety Classification

> Forged: 2026-08-13. Extracted from session auditing Hermes/OpenCode/OpenClaw guardrails.
> Context: Arif asked "who determine what's safe?" — this methodology answers it for ANY agent system.

## The Three Tiers

Every "safety mechanism" in an agent system falls into exactly one of these:

### TIER 1: MECHANICAL (code enforces, model cannot bypass)

These are physical barriers. The model literally cannot override them.

**Characteristics:**
- Written in code (Python, TypeScript, regex), not prompts
- Runs BEFORE the model sees the output
- Has a hard exit (exit code, exception, block response)
- Cannot be bypassed by prompt injection, yolo, or clever rewording

**Examples from our federation:**
- Hermes `approval.py` DANGEROUS_PATTERNS (100+ regex) — blocks rm -rf, DROP TABLE, chmod 777, etc. Even with --yolo
- OpenCode `arifos-judge-gate.ts` — T3 tools route to arif_judge :8088; if judge is down, HOLD (fail-closed)
- OpenCode `aaa-autonomy.ts` HOLD_PATTERNS — rm -rf outside safe zones, force-push main, reboot → stops autonomy
- Hermes `arifos-hermes-gate-hook.py` W_scar auto-HOLD — critical-variable claims without source → physical block (exit 2)

**How to verify:** Read the source code. If the guardrail is in a regex list, plugin hook, or gate function with hard exit — it's mechanical.

### TIER 2: ADVISORY (prompt-injected, model may ignore)

These are rules written in the system prompt, AGENTS.md, or skill files. The model SHOULD follow them, but CAN choose not to.

**Characteristics:**
- Written in natural language or YAML config
- Loaded into system prompt or context window
- Model reads it, but compliance is voluntary
- No code-level enforcement

**Examples from our federation:**
- OpenClaw `boundaries` dict in openclaw.json — "irreversible_requires_888: true" — only injected into prompt
- Skills like `verify-gate`, `observe-ground` — instructions, not enforcement
- SOUL.md bridge protocol — "ground in immediate reality" — behavioral guidance
- All constitutional floor descriptions in AGENTS.md

**How to verify:** If the guardrail is a sentence in a .md file or a YAML key with no corresponding code check — it's advisory. Test: can the model ignore it without triggering a hard error? If yes → advisory.

### TIER 3: THEATRE (claim exists, enforcement doesn't)

These give the FEELING of safety without actual enforcement. The most dangerous tier because they create false confidence.

**Characteristics:**
- Documented in governance files or agent cards
- Referenced in claims ("we have safety guardrails")
- No corresponding code, no prompt injection, no mechanical check
- When tested, nothing happens

**Examples from our federation (before fixes):**
- OpenClaw `exec-approvals.json` — was `{"defaults": {}, "agents": {}}` (empty) — the mechanism existed but was unconfigured
- Agent card `authority_boundary` — "cannotDo: Issue SEAL/HOLD" — text in JSON, not enforced by any code
- `sycophancy-detector.ts` — explicitly says "non-blocking — cannot HOLD mid-stream"
- OpenCode `permission: {"*": "allow"}` — the permission system is wide open

**How to verify:** Search for the guardrail's NAME in source code (.py, .ts, .js). If zero results in code files → theatre. If it only appears in .md/.json/.yaml → likely advisory or theatre.

## Audit Procedure

For any agent system's safety mechanisms:

1. **List every claimed guardrail** (from docs, configs, cards, prompts)
2. **For each, search source code** for the guardrail's name/function
3. **Classify:** MECHANICAL (code) / ADVISORY (prompt) / THEATRE (nothing)
4. **Report:** Table of guardrail → tier → evidence
5. **Recommend:** Upgrade THEATRE → ADVISORY minimum, ADVISORY → MECHANICAL where critical

## Why This Matters

Theatre is worse than no safety at all, because:
- It creates false confidence ("we have guardrails" → stops looking)
- It allocates cognitive load (model reads rules it won't follow)
- It satisfies auditors without protecting users

A system with 3 MECHANICAL guardrails is safer than one with 30 ADVISORY + 10 THEATRE guardrails.

## Application

This methodology applies to ANY agent system — not just ours. When evaluating:
- OpenAI's function calling safety
- Anthropic's Constitutional AI
- Google's Gemini safety layers
- Any custom agent framework

Ask: is this MECHANICAL, ADVISORY, or THEATRE?

## Related

- Gate hook implementation: `/root/AAA/federation/protocols/arifos-hermes-gate-hook.py`
- W_scar doctrine: `/root/AAA/governance/W_SCAR_EPISTEMIC_FLOOR.md`
- Falsification Engine: `/root/AAA/governance/FALSIFICATION_ENGINE.md`
