# Amir joins Syed Sado Agent Client — member-add + lane registration session (2026-08-30)

Session context: Arif asked to add Amir Ridzwan (athlete #1, Coach Syed client, user_id `317849404`) to the live client group `-1003747272167` ("Syed Sado Agent Client"). Amir already had a DM lane (`amir-ridzwan`).

## What actually happened (chronology)

1. Searched lanes.yaml → found `amir-ridzwan` DM lane, no group lane.
2. Hunted for the group's chat_id: gateway.log had no group-name strings. **Found it in agent.log** — session turn-context lines and a webhook test payload (`'chat': {'id': -1003747272167, 'title': 'Syed Sado Agent Client', 'type': 'supergroup'}`). Lesson: **agent.log, not gateway.log, is where chat titles live.**
3. Token discovery: `TELEGRAM_BOT_TOKEN` env var does not exist. The live token is `ASI_ARIFOS_BOT_TOKEN` (referenced from config.yaml `bot_token_env`). `getMe` → `@ASI_arifos_bot`, id `8410138119`.
4. `getChatMember(group, 317849404)` → `status: "member"` — **Amir had already joined himself.** Nothing to add; the whole task collapsed to lane registration + allowlist verification.
5. Allowlist check: `317849404` already in `TELEGRAM_ALLOWED_USERS`, `TELEGRAM_GROUP_ALLOWED_USERS`; `-1003747272167` already in `TELEGRAM_FREE_RESPONSE_CHATS`. No env changes needed.
6. Added `amir-sado-group` lane (17 lanes total) via Python yaml roundtrip — cloned DM doctrines (`athlete_privacy_strict`, `coach_syed_owns_calls`, `prescribe_neither_workout_nor_macro`, `diagnose_dont_prescribe`), dropped DM-only CAREGIVER capability, added group-safety doctrines (`group_medical_privacy`, `never_location_pin`, `no_operator_data`).
7. Announced in-group (message_id 127).
8. **Gateway restart killed the session mid-turn** (see pitfall below). Session restored; gateway completed its deferred drain-restart on its own; lane verified present.

## Lane-clone pattern for group registers

```
DM lane                          →  group lane
triggers: user_id + user_id(chat) → user_id + GROUP chat_id
memory_files: USER+MEMORY+SOUL    → MEMORY only (lighter)
skills: full DM set               → group-scoped subset
doctrines: DM set                 → DM set ∪ {group_medical_privacy, never_location_pin, no_operator_data}
capabilities: - CAREGIVER         → ADVISORY/TRACKING/memedia only
memory_lanes: scope: dm           → scope: group, prefix user:<name>:group:
```

## Gateway self-restart kill (the big lesson)

`systemctl restart hermes-asi-gateway.service` from a session **running through that gateway** = suicide:
- The terminal call returned exit -15 immediately (own process group killed).
- Follow-up `systemctl is-active` polls from a NEW shell showed `deactivating` for many minutes — "Restart deferred: waiting on N active work unit(s)" (own turn among them).
- Correct approach: defer with `systemd-run --on-active=90s systemctl restart ...` after the reply lands, or lean on the gateway's already-pending deferred restart.

Recovery checklist on session restore: (1) `systemctl is-active` until `active`, (2) re-read lanes.yaml to confirm the lane persisted, (3) do NOT re-add the lane blindly.

## Minor gotchas

- `getChatMember` with `user_id="me"` → 400 invalid user_id. Use `getMe` first.
- Bot API quirk: supergroup invite link was already present in `getChat` result — reusable for future member adds without `createChatInviteLink`.
- `find /root -name '*.pdf' -mmin -20` from execute_code timed out at 300s (whole-root walk). Scope finds to known work dirs (`/root/forge_work`, `/root/HERMES`) — sub-second.
