# Scar-2026-10-03-003 — Claude Code Menu-on-Missing-Context

> **Filed:** 2026-10-03 · **Lane:** warga cross-audit · **w_scar:** 0.6 · **Status:** FILED

## The failure

When asked to verify status of T-009 (a task ID external to this session's context), Claude Code responded with a 4-option menu (A/B/C/D) plus 3 follow-up clarification questions, instead of a single-acknowledgement + one ask.

**Evidence:**
- Conversation turn before this scar was filed, in this same session.
- User prompt: "Third check on T-009 333-AGI re-classification agent (afa570e5cec7f4086) for forge-fastmcp v3.2.0 SEAL promotion."
- Claude Code response: 4 alternatives labelled A/B/C/D, each ~3 lines, followed by "Soalan terus kepada anda" with 3 numbered sub-questions.

## What Claude Code got right (preserve)

1. **No fabrication.** Did not claim "completed" without evidence. Did not invent "2 strong external witnesses." Did not schedule a wakeup without signal.
3. **Acknowledge unknown.** Stated plainly: "T-009 tak nampak dalam konteks saya sekarang."

## What Claude Code got wrong (the defect)

Produced a **menu-on-missing-context** when SOUL §3 of arifOS doctrine requires: "take most reasonable reading, jawab, satu baris fallback." Claude Code defaulted to Anthropic's helpful-but-bounded contract (defer-with-options) instead of arifOS's contract (acknowledge-then-act-or-defer).

This is a **register defect**, not a truth defect. Pattern clash: respects truth, off on output structure.

## Binding rule

When a task ID / external handle / cross-session reference is named but not present in current context:

1. State in one or two lines that the reference is not visible in current context.
2. If a path/handle would resolve it, ask for it — **once**, not as a menu.
3. Do not enumerate alternatives the user did not ask for.
4. Do not bundle multiple clarification questions.

Single ask, single line fallback. No (a)(b)(c)(d). No three-part sub-menu.

## Honest note at filing time

This scar is about **register**, not about truthfulness. Claude Code's refusal to fabricate is preserved. The defect is structural: it asked too much when one ask would do. Cross-witnessed by HERMES🪽 in the same federation session.

## Why this is not SCAR-class (severity)

`w_scar = 0.6` because:
- No canonical record was corrupted.
- No irreversible action resulted.
- The user (Arif) was able to correct the pattern with one message.
- The defect is repeatable but recoverable in one exchange.

It is filed as a scar because the **pattern recurs** across missing-context situations — every fresh agent that boots into arifOS federation risks producing menus instead of action-or-one-ask.

## Kill-switch

Retires when arifOS-side contract coupling (forge-coupling) replaces Claude Code's default helpful-but-bounded register with SOUL §3's acknowledge-then-act-or-defer register. Until then, treat every missing-context response as suspect for menu-shape.