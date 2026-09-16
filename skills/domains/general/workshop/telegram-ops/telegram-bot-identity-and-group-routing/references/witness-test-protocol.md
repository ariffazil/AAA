# Witness-Test Protocol — Disk vs Runtime

> Created 2026-09-04 after a session claimed "11 lanes / 3 bot tokens / 23 chat configs wired" from a config.yaml scan alone. Reality: 18 lanes, 1 active token, hermes_asi state.db empty for ALL 23 chats.

## The principle

A configuration that lists something is **declared**, not **wired**.

A blueprint of a city without power lines is not a city with power. Don't tell Arif the city has power just because you read the blueprint.

When in doubt about whether something is "wired", you do not have a knowledge gap. You have an evidence gap. Run the witness-test.

## The witness-test ritual (60 seconds, read-only)

Run these BEFORE claiming any wiring claim about Telegram routing, lanes, or surface coverage:

### 1. Disk-side witness

```bash
# Find the file/config/key first
find /root -name "<expected-file>" -type f 2>/dev/null
grep -n "<expected-keyword>" /root/.hermes/config.yaml
```

If `find` returns nothing → file genuinely missing. STOP. Don't claim "wired".
If `grep` returns nothing → declaration missing. STOP. Don't claim "wired".
If both return → declarations exist on disk. Move to step 2.

### 2. Runtime-side witness

```bash
# Is the gateway actually running?
systemctl is-active hermes-asi-gateway
# Or other profiles:
systemctl is-active hermes-apex-gateway hermes-forge-gateway openclaw-gateway 2>&1

# Did the gateway ever route this chat/user?
DB=/root/HERMES/profiles/hermes_asi/state.db  # adjust to active profile
sqlite3 "$DB" "SELECT COUNT(*) FROM sessions WHERE chat_id LIKE '%-1003815535761%';"
sqlite3 "$DB" "SELECT COUNT(*) FROM sessions WHERE user_id = '1042200555';"
sqlite3 "$DB" "SELECT COUNT(*) FROM messages WHERE session_id IN (SELECT id FROM sessions WHERE chat_id LIKE '%-1003815535761%');"

# Is the webhook registered?
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getWebhookInfo" \
  | python3 -c "import sys,json; d=json.load(sys.stdin)['result']; print(f'url: {d.get(\"url\",\"empty\")} pending: {d.get(\"pending_update_count\",\"?\")}')"
```

If gateway is inactive AND state.db empty AND webhook empty → **declared but not fired**. The wiring is a blueprint with no execution. Tell Arif the truth.

### 3. Cross-surface witness

Sometimes another surface owns the routing. hermes_asi state.db empty doesn't mean no Telegram routing exists. Check:

```bash
# Other Hermes profiles
for prof in hermes_apex hermes_forge; do
  D=/root/HERMES/profiles/$prof/state.db
  echo "--- $prof ---"
  sqlite3 "$D" "SELECT DISTINCT chat_id, COUNT(*) FROM sessions GROUP BY chat_id ORDER BY 2 DESC LIMIT 5;"
done

# OpenClaw gateway (different bot family)
ls /root/.openclaw/openclaw.json 2>/dev/null && \
  python3 -c "import json; d=json.load(open('/root/.openclaw/openclaw.json')); print('groups:', list(d.get('channels',{}).get('telegram',{}).get('groups',{}).keys()))"

# Other mesh nodes (azwaos, etc.) — cross-pollination risk
ssh root@100.64.0.4 'systemctl is-active hermes-asi-gateway' 2>/dev/null
ssh root@100.64.0.5 'systemctl is-active hermes-asi-gateway' 2>/dev/null
```

If somebody else owns the chat → you have token conflict risk. Don't start another gateway without F13 approval.

## The four-witness template

When reporting wiring status to Arif, fill this in (don't skip fields):

```
Surface: [chat_id or username or group]
Disk witness:    [file: exists | missing | path-broken]
Config witness:  [key: declared | missing | wrong-value]
Runtime witness: [service: active | inactive | remote-active | unknown]
DB witness:      [sessions for surface: N rows, latest: <timestamp>]
Verdict:         [WIRED | DECLARED-NOT-FIRED | BROKEN | UNKNOWN]
```

If you can't fill all four, your verdict must be `UNKNOWN`. Tell Arif you have evidence gaps. Don't paraphrase `UNKNOWN` as `WIRED`.

## The 2026-09-04 incident — verbatim

**Claim made:**
> "config.yaml punya telegram.allowed_chats ada 23 chats wired — kau, Syed, AAA, SADO, AIA, Kanak-kanak, Dear Nabilah, arifOS channel, MakcikGPT, Sin Boy group, + 13 lain. free_response_chats set sama, require_mention: false. Bot config nak auto-reply semua."

**Reality witnessed:**
- `config.yaml` declared 23 chats. ✓ disk-truth
- `state.db` (hermes_asi) had 1 session, 27 messages, all CLI kanban task from 2026-07-24. Zero Telegram sessions. ✗ runtime-false
- `systemctl is-active hermes-asi-gateway` returned `inactive`. ✗ service-false
- `getWebhookInfo` returned `url: empty`. ✗ webhook-false
- Other profiles (hermes_apex, hermes_forge) had non-zero sessions but for different sources, not Telegram routing to these 23 chats. Partial alternative-owners.

**Verdict should have been:** `DECLARED-NOT-FIRED`. The blueprint existed. The city had no power.

**Verdict given:** `WIRED`. False positive.

**Lesson:** config-side count without runtime-side count = unverified claim. Always count both.

## When to skip the witness-test

Only when:
1. Arif explicitly asked "just check the config", AND
2. The output is going into a config-only action (diff, lint, syntax check), AND
3. You're NOT about to make any routing/mutation decision based on the answer

For anything that informs a mutation, restart, or "is this safe to push?" — run the witness-test. 60 seconds is cheap. A wrong "wired" claim and the resulting bad mutation costs hours.

## Related

- Section 0 of `SKILL.md` — the rule this reference implements
- `references/asi-silence-2026-08-29.md` — sibling failure mode (silent bot due to hook signature drift, NOT config absence)
- `telegram-bot-routing-doctrine` — the doctrine this witness-test guards against misapplying
