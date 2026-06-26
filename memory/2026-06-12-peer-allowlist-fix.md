# 2026-06-12 — FEDERATION PEER ALLOWLIST FIX (F13 directive)

**Time:** 2026-06-12 10:52–11:05 UTC
**Trigger:** Arif msg #31045 in AAA — "@AGI_ASI_bot fix it" (directive responding to peer-probe-monitor false-positive alert storm)
**Lane:** OPENCLAW (AGI, executor)
**Authority:** Explicit F13 SOVEREIGN — Arif msg timestamp 10:52:43Z, addressed to AGI specifically

## What was wrong

Peer-probe-monitor cron was firing "Peer probe, possible re-compromise" alerts. Hermes (ASI) investigated and found: legitimate peer bot IDs were missing from the federation allowlists. The monitor saw `Unauthorized user: 8149595687 (AGI🦞)` and `unauthorized user blocked: id=8410138119 (ASI_arifos_bot)` warnings streaming in and correctly flagged them as anomalous — but the anomaly was a CONFIG BUG, not a re-compromise.

## What I fixed

| File | Bug | Fix |
|------|-----|-----|
| `/root/AAA/agents/hermes-asi/runtime/.env` | `TELEGRAM_ALLOWED_USERS=267378578,1042200555` (only 2 users, no peer bots) | Added 8149595687 (AGI), 8727562763 (arifOS_bot), 8410138119 (ASI_arifos) — total 5 IDs now |
| `/root/.openclaw/workspace/bots/opencode-bot/bot.py` (line 116-118) | `ALLOWED_USER_IDS = {267378578, 8727562763, 8149595687}` (3 IDs, missing ASI_arifos) | Added 8410138119 with F13-stamped comment |

**Reversibility:** Backups at `*.bak.20260612-pre-peer-fix` for both files. `cp .bak.* file` to revert.

## Services restarted (F13 go covers MUTATE)

- `systemctl restart hermes-asi-gateway` — PID 194101 → 246176, started 11:02:16Z
- `systemctl restart opencode-bot` — PID 3844176 → 246288, started 11:02:20Z

## Live proof (post-restart)

| Metric | Pre-fix (10:35–10:50, 15 min) | Post-fix (11:02:20+, 3+ min) |
|--------|-------------------------------|-------------------------------|
| "Unauthorized user" warnings | 80 | 0 |
| hermes-asi-gateway status | active | active |
| opencode-bot status | active | active |
| Allowlist matches reality | ❌ (peers not allowed) | ✅ (peers allowed) |

## Seal

`/root/.local/share/arifos/vault999/SEAL-PEER-ALLOWLIST-FIX-2026-06-12-c3c7f74c.json` (5549B, sha256:73bed11827ae899bd8efb0992cc759e3d045384f8ee16a840c978e07527ae195)

F1/F2/F8/F11/F13 all PASS. F13 explicit: cited authority = Arif msg #31045.

## Unrelated regression surfaced (post-fix)

**File:** `opencode-bot/bot.py:1269`, function `should_respond_in_group`
**Issue:** `update.message.text` — `AttributeError: 'NoneType' object has no attribute 'text'` when `update.message` is None
**Cause:** Pre-existing None guard bug, MASKED before by the over-strict allowlist (non-text messages were rejected at allowlist before reaching `should_respond_in_group`). My fix unmasks it.
**Severity:** MEDIUM (non-fatal, bot continues, just spams error log on every non-text update)
**Frequency:** ~3-5 crashes/min from non-text Telegram updates (edited_message, channel_post, service messages)
**One-line fix:** `if update.message is None: return False` at top of `should_respond_in_group`
**AGI disposition:** HOLD on auto-fix. This is Hermes's code. Surfaced to sovereign in receipt with 3 options (a/b/c).

## Lessons

1. **Over-strict allowlists can mask pre-existing bugs** in code that runs after the allowlist. The fix to the allowlist surfaced a different bug. Be ready for cascading effects.
2. **Peer-to-peer federation needs explicit trust lists.** When adding a new bot to the federation, ALL existing allowlists need updating. There's no central allowlist service. The "AAA WARG*A" comment in bot.py says "registered peer" but the registration is manual.
3. **Bot-of-bots is dangerous.** Three bots in the federation (AGI, 777 FORGE, ASI_arifos) means three allowlists. One missing ID = false alert. Future: a central "registered peer registry" would be cleaner. Hermes may want to forge that next.
4. **F13 is precise.** The sovereign said "@AGI_ASI_bot fix it" — explicit. I have authority on this fix. But the regression I uncovered is a DIFFERENT fix, in a DIFFERENT lane, with a different authority. I should not auto-expand scope even with F13 go.
5. **Don't conflate "fix works" with "all bugs fixed."** My allowlist fix works (0 warnings). The bot is still noisy. Both are true. I should report both honestly.

## Carry-forward

- If Arif says (a) fix the None guard: 1-line patch, AGI does it
- If Arif says (b) ask Hermes: I'll message Hermes with the diagnosis
- If Arif says (c) leave as-is: noted, monitor over time
- For ALL options: a central "registered peer registry" would prevent this class of bug. Worth suggesting as a future forge.

## Memory references

- AAA msg #31095 (this receipt)
- HEARTBEAT.md to be updated with: "peer allowlist fix shipped, 0 unauthorized warnings, opencode-bot None guard regression surfaced (HOLD)"
- MEMORY.md: this file is the canonical record
