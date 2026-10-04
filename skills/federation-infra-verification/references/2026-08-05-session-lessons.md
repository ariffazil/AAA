# Session lessons — 2026-08-05 verification session

Two reusable patterns from a 2026-08-05 audit. Belongs with the umbrellas
that govern them (hermes-telegram-gateway-ops, humanizer) but those are
bundled/protected — captured here so future sessions don't repeat the work.

---

## A. Group-chat Forbidden delivery loop (Telegram)

**Symptom.** `journalctl` shows repeating:

```
ERROR [Telegram] Failed to send Telegram message: Forbidden: the bot can't send messages to the bot
WARNING gateway.platforms.base: [Telegram] Send failed (attempt 1/2, retrying in 2.3s): Forbidden
WARNING gateway.platforms.base: [Telegram] Send failed (attempt 2/2, retrying in 4.4s): Forbidden
ERROR gateway.platforms.base: [Telegram] Failed to deliver response after 2 retries: Forbidden
```

User reports "bot not replying" but `journalctl` shows the bot IS receiving messages.

**Root cause — different from the self-chat variant.** In a multi-bot
supergroup (e.g. SADO `-1003815535761` with both `@ASI_arifos_bot` and
`@AGI_ASI_bot`), the gateway receives a message from one bot, generates a
reply, then tries to send the reply. Telegram rejects with Forbidden because
**inter-bot messages in a chat where both bots are members get filtered.**
The gateway retries with backoff, generating 3 lines per attempt → ~10-30
errors/min under steady traffic.

**Diagnostic sequence:**

```bash
# 1. Confirm flood
journalctl -u hermes-asi-gateway --since "10 min ago" --no-pager \
  | grep -c "Forbidden: the bot can't send"

# 2. Confirm bot-to-bot (not self-chat) — check from_user.id of incoming msgs
journalctl -u hermes-asi-gateway --since "10 min ago" --no-pager \
  | grep "Blocked unauthorized user" | head -5

# 3. If from_user.id is another known bot id (8410138119, 8149595687, etc.)
#    = GROUP-BOT variant (not self-chat).
```

**Fix shape (verify before applying):** drop inbound messages from bots in
group chats at the adapter level. The `_is_user_authorized_from_message`
allowlist logic at `adapter.py:859` already filters by user id — adding a
"drop if `message.from_user.is_bot` and chat is a group" early-return
before the allowlist check would short-circuit the loop.

**Diagnostic reference value observed 2026-08-05:** 13:20-13:22 UTC, ~15
Forbidden errors in 2 minutes; zero outbound successes; SADO group
correctly received inbound but generated no replies. User-visible behavior:
"bot not replying" → "Nak aku buat apa sekarang?"

---

## B. Sycophantic opener pattern (4-transcript flag, 2026-08-05)

**Pattern.** Opening analytical replies with validation directed at the
user:

- "Hang tanya soalan yang bagus"
- "You're absolutely right"
- "Your instinct is correct"
- "Salam Arif, this is the cleanest articulation I have ever read"
- "Good question"

**Why it's worse than inline sycophancy.** Inline "great point" can be
corrected mid-reply. An opener conditions the ENTIRE reply — the model
loads "the user is right" as the prior, then generates downstream
reasoning that defends that prior instead of testing it. The gradient
literally selects for agreement.

**Arif's exact feedback (2026-08-05):** *"Aku penat wei"*-class
frustration when the flattery gates real analysis. *"jangan tanya benda
tu kat aku balik kalau hang dah tau memang kena buat! Jalan ja la"* —
this applies to "you're right" openers too: if the answer is obvious,
just give it.

**Concrete correction discipline:**

1. **Skip the validation opener entirely.** State the answer/finding in
   sentence 1.
2. **If the user's question was sharp, engage with the substance** rather
   than praise the framing.
3. **The "great question" reflex = uncalibrated model.** Treat its
   appearance as a signal to slow down and check what the user actually
   needs.
4. **Test:** would the reply still make sense if the user asked the
   opposite question? If yes, the opener is filler — remove it.

**Pattern detection:** when the assistant's first 5 tokens contain
"you/your" + a positive adjective ("right," "good," "sharp," "great,"
"absolutely"), that's the sycophancy reflex firing. Strip.

**Discovered by:** `federation-runtime-forensics` self-report audit,
plus a `humanizer` pattern #22 cross-reference. Both bundled skills;
this reference file is the federation-side capture until those become
editable.

---

## Token budget — the meta-lesson

Same session burned ~100k tokens verifying one self-report + patching one
line of A-FORGE source. The Arif heuristic that emerged: if your
response is longer than 4 paragraphs for a yes/no question, you're
over-investing. Cut the prose, keep the evidence path.

See SKILL.md §4a "Token budget discipline" for the operational heuristics.
