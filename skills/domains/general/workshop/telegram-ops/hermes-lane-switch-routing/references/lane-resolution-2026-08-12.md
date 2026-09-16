# SADO-group "reacts differently" diagnostic — 2026-08-12

Case: Arif asked "why does my Hermes agent react differently with me and others in the SADO group?" Full probe of the lane_switch system. This is a reproducible method for ANY "why does the bot answer differently" report.

## Live runtime state (.runtime.json — the smoking gun)

```json
{
  "user:267378578": "arif",
  "user:1042200555": "syed",
  "user:1024343313": "aliff",
  "user:1237635275": "izzu",
  "chat:-1003815535761": "arif",   // SADO group stamped as "arif room" — BUG
  "chat:1042200555": "syed-dm",
  "chat:1024343313": "aliff",
  "chat:1237635275": "izzu",
  "chat:-1003521544074": "arif"    // AIA group also stamped arif
}
```

Key finding: the SADO group chat `-1003815535761` is stamped `"arif"` in runtime — because `pre_gateway_dispatch` records the last sender's lane against the chat id. Shared groups must NOT be person-stamped.

## Lane table (lanes.yaml)

| Lane | authority | capabilities | voice | chat trigger |
|------|-----------|--------------|-------|--------------|
| arif | SOVEREIGN | FULL | BM intelek + EN technical | user_id `267378578` ONLY (no group chat ids) |
| syed | WARGA | ADVISORY, TRACKING, REMINDER | BM Pasar | SADO `-1003815535761` + user `1042200555` |
| syed-dm | WARGA | + CAREGIVER | BM Pasar personal | DM `1042200555` |
| aliff | WARGA | ADVISORY, TRACKING, REMINDER | BM casual | DM `1024343313` |
| aliff-aia | WARGA | ADVISORY | BM casual | AIA `-1003521544074` |
| izzu / izzu-aia | WARGA | ADVISORY | neutral BM/EN | DM / AIA group |
| guest | TAMU | READ_ONLY | polite minimal | triggers `{}` |

## Why the agent "reacts differently"

- Arif in SADO group → Pass 1 fails (arif lane has no SADO chat_id), Pass 2 person-fallback → **arif lane** (SOVEREIGN, FULL, arif-private memory, strategic voice).
- Syed in SADO group → Pass 1 exact match → **syed lane** (WARGA, BM Pasar, group-safe, nasi-lemak/medical-privacy doctrines).
- Same chat, two different lane cards injected per sender. That is the visible "different reaction" — by design (F13 per-person isolation).

## The 3 frictions to fix

1. **arif lane has no group register** → sovereign context leaks into shared rooms via person-fallback. Fix: add `sado-group` (or `arif-sado`) register capping authority.
2. **Chat-stamping bug** → `chat:-1003815535761: "arif"` pollutes `.runtime.json`, can confuse Pass 3 room-fallback. Fix: don't person-stamp shared groups.
3. **Per-chat history vs per-person lane** → shared thread history + flipping lane context = mid-thread tone shifts.

## Fix proposals (reversible T2 — announce then execute)

- **A (recommended):** add `sado-group` register as default for `-1003815535761`; voice group-safe consistent, per-user memory still isolated, authority capped to WARGA for everyone INCLUDING Arif in that room. Sovereign stays sovereign in DM; in group he's "beb".
- **B:** add `arif-sado` register — Arif gets a distinct casual group register instead of sovereign.
- **C:** clear `chat:<group>:` stamps from runtime so rooms aren't person-attributed.
- **A + C together** is the most zen for a shared room.

## Diagnostic method (reuse for any "reacts differently" report)

1. Read `/root/HERMES/profiles/aaa-hermes/plugins/lane_switch/__init__.py` — the 3-pass `detect_lane` + hook wiring.
2. Read `/root/HERMES/lanes/lanes.yaml` — build the lane table, note which lane owns each chat_id.
3. Read `/root/HERMES/lanes/.runtime.json` — find chat-stamp pollution.
4. Simulate `detect_lane(user_id=<reporter>, chat_id=<group>)` mentally through the 3 passes to see which lane they actually land in.
5. Check `telegram.allowed_chats` + `free_response_chats` in `/root/.hermes/config.yaml` only if transport access is in question (usually NOT the problem — lanes are upstream of transport).
6. Report: by-design behavior vs the 3 frictions. Recommend A/C, ask only if the sovereign wants a different group-register direction.