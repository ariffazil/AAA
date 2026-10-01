# Channel Prompt Authoring Doctrine — Kernel-Level

> Forged: 2026-09-29 | Source: Shadow Authority #1 audit (config.yaml SADO prompt)
> Status: **F13_RATIFIED_CHAT (2026-09-29)** by Arif F13 sovereign
> Constitutional binding: F1 (AMANAH), F2 (TRUTH), F11 (AUDITABILITY)

---

## Failure Class (Why This Doctrine Exists)

**3 documented shadow authorities found in one session** (all "Documentation ≠ Runtime" pattern):

1. `mode_first_enforcement.py` — flat .py file claiming pre_llm_call hook, never loaded
2. `restart-gateway.sh` — script pointing to masked `hermes-gateway.service`, real runtime is `hermes-asi-gateway.service`
3. **config.yaml `channel_prompts` SADO** — inline hardcoded HARD LIMITS that overrode both `lane_switch._people_block` policy flip AND `people.yaml` scope filter. Bot's "kirim ke DM" deflection traced HERE, not to lane_switch as originally assumed.

The pattern: **cross-cutting rules baked into per-instance artifacts create shadow authority**. Fix at the wrong layer (lane_switch code) and the real override (inline prompt) wins. Real fix requires elevating the rule to canonical source.

---

## Axiom 1: Source-of-Truth Doctrine

**`people.yaml` is the source of truth for "what may be said about whom".**

Channel prompts in `config.yaml` may HINT at context (register, voice, room shape) but MUST NOT contradict `people.yaml` scope filter.

If channel prompt says "never mention X" and `people.yaml` says `scope: shared` for X → BUG. Fix one or the other with F13 review.

---

## Axiom 2: Permitted Channel Prompt Content

A channel prompt MAY contain:
- Room identification (chat name, purpose, members)
- Register (BM santai, English professional, etc.)
- Voice (TTS voice_id, voice bonding)
- Format rules (HARAM = markdown headers, essays, sermons)
- Anti-hijack rules (GAP-5: don't insert in human-to-human chat)
- Minimum Sufficient Response discipline
- Voice bonding ("Suara Arif = iarif-sovereign-v9, jangan campur")
- Group-specific scope HINT (e.g., "lepak group, keep it casual")

---

## Axiom 3: Forbidden Channel Prompt Content

A channel prompt MUST NOT contain:
- Blanket bans on facts already authorized by `people.yaml` scope:shared
- Hardcoded privacy rules that contradict people.yaml scope filter
- Per-person privacy denials (use `people.yaml` `scope: dm` for that)
- Identity assumption ("andaikan siapa bercakap")
- Preachy directives to humans about body/health/sleep/etc. (F1 amanah + F5 dignity)

If such content is needed, encode it as `scope: dm` in `people.yaml`, NOT as channel prompt text.

---

## Axiom 4: Anti-Hijack Layer Separation

GAP-5 anti-hijack ("don't insert in human-to-human chat") belongs in channel prompt because it is ROOM-LEVEL context (humans in this room are talking, not invoking bot).

But "what facts can be said about person X" is PERSON-LEVEL context, which belongs in `people.yaml`.

Mixing these layers creates shadow authority.

---

## Axiom 5: Revision Discipline

Channel prompt changes:
1. Backup original to `_archive/`
2. Edit with explicit F13 reference
3. Verify YAML parses
4. Restart gateway to activate
5. Log receipt in `RECEIPTS.md`
6. If change affects a group chat with multiple humans, notify in F13 ledger

---

## Operational Test (apply to any channel_prompt revision)

For each candidate line:
1. Does this contradict `people.yaml`? If yes, fix at people.yaml layer.
2. Does this add room-level context (register/voice/format/anti-hijack)? If yes, valid.
3. Does this deny facts authorized at scope:shared in people.yaml? If yes, REMOVE.
4. Does this encode person-level privacy? If yes, move to people.yaml.
5. Is the change scoped to one chat, or is it a general principle? If general, elevate to kernel doctrine.

---

## Current Authorized Channel Prompts (4 chats)

| Chat ID | Name | Status |
|---|---|---|
| `267378578` | Arif DM | Full sovereign lane, kept as-is |
| `931661476` | Fey DM | Household/staff, kept (legitimate protection) |
| `-1003740520259` | SEMBANG | Work colleagues, refactored |
| `-1003815535761` | SADO | Friends lepak, refactored |

All 4 reviewed and aligned with this doctrine on 2026-09-29.

---

## Scar Lines

> **Inline prompt ≠ source of truth for cross-cutting rules.**

> **Channel prompts hint at room context. people.yaml decides what can be said.**

> **Mixing room-level with person-level context creates shadow authority.**

---

## Provenance

Forged 2026-09-29 during shadow-authority audit session (Kimi Code FI-008 + HERMES musyawarah).

Anchor audit: `/root/.hermes/_archive/message_path_trace_2026-09-29.json` (37.6 KB transformation trace, identified channel_prompts as Shadow Authority #1)

---

*Status: DRAFT_AWAITING_F13. To ratify, Arif reviews + musyawarah (333 + 555 + 666) + receipt chain.*