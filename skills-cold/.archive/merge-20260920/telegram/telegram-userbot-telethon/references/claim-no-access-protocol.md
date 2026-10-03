# Claim-No-Access Protocol — Quick-Reference Audit Steps

When the user (especially Arif, F13 sovereign) asks Hermes to "read group X / see Telegram messages," follow this audit sequence BEFORE claiming "no capability":

## Step 1 - Self-check: Did I already see it this session?
- Look back at this conversation's tool results.
- `state.db` queries from THIS session often return recent group activity (24-48h window).
- If I already saw messages via state.db but then claimed "no live access" → that's misleading. Cite state.db origin instead.

## Step 2 - Archive scan (always run)
```bash
ls -la /root/_archive/*/userbot/ 2>/dev/null
ls -la /root/userbot/ 2>/dev/null
ls -la /root/.hermes/*.session 2>/dev/null
find /root -maxdepth 4 -name "*.session" 2>/dev/null
find /root -maxdepth 4 -path "*userbot*" 2>/dev/null
```

Look for: `.session` files (Telethon session persistence) + `auth*.py` (hardcoded API_ID/HASH) + `auth_state.json` (live phone_code_hash).

## Step 3 - Live token scan
```bash
grep -h TELETHON_API_ID /root/.secrets/kunci-*.env 2>/dev/null
grep -h TELETHON_API_HASH /root/.secrets/kunci-*.env 2>/dev/null
```

## Step 4 - State.db window check
```sql
SELECT timestamp, role, substr(content, 1, 400)
FROM messages
WHERE content LIKE '%<unique phrase from group>%'
ORDER BY timestamp DESC
LIMIT 30;
```

## Step 5 - Only AFTER exhausting steps 1-4: claim no access

When stating "no live access," include the audit trail:
> "Checked state.db (24h window: not found), archive userbot dir (`/root/_archive/2026-08-04/userbot/` shows sess+creds but expired 19 days), live env (no TELETHON_API_ID/HASH), service (none running). For real-time read we'd need either a fresh telethon auth or a currently-running userbot service."

## Why this matters

2026-08-19 SADO group episode: Arif asked "U can read from SADO group right" after I had already quoted state.db messages from that group in a previous turn. The right move was: cite the state.db source (already in context), acknowledge its 24-48h limit, and ask if a fresh live read is wanted. The wrong move (which I started with): "aku takde Telegram live access" - which got called "Lie" because state.db IS that live-ish source within its window.

## Floor rule (F2 TRUTH)

If a capability is sitting on disk (a session file + archived API credentials), state it accurately. The 2026-08-19 correction: capabilities exist on disk that I didn't surface; that's a truth failure.

The authorization gate (F1 AMANAH) still applies - discovering capability ≠ using it without ask. Once discovered, surface to Arif with explicit Go/Stop/Setup choice, as I did after the userbot evidence surfaced.
