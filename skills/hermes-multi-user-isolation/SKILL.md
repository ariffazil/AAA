---
name: hermes-multi-user-isolation
description: "Isolate multiple human users on one Hermes installation via profile multiplexing — the native `gateway.multiplex_profiles: true` pattern. Covers per-human profiles with own memory/skills/sessions/credentials, one bot per human, sovereign-content leak prevention (F13/F6 MARUAH), and the migration checklist. Use when multiple humans DM the same Hermes gateway, a non-owner user is whitelisted into the owner's profile, sovereign memory (scars, doctrine, other users' identities) must not leak across users, or a new human needs their own isolated Hermes lane."
tags: [hermes, multi-user, profiles, multiplexer, isolation, f13, sovereignty, gateway]
related_skills: [hermes-telegram-gateway-ops, arifos-federation-ops, forge-vault-seal-receipt]
---

# Hermes Multi-User Isolation (Profile Multiplexer)

Class of work: **giving each human their own isolated Hermes lane on one box.** When multiple humans reach the same gateway through ONE profile, they share one memory context — sovereign content (H5 scars, F13 doctrine, other users' identities) leaks into every human's turns. That is an F13/F6 MARUAH leak, not a config nicety.

Verified incident 2026-08-09: profile `aaa-hermes` served ARIF (267378578) + Syed (1042200555, in `allow_from`) + Wawa (8324190535, in channel directory) + SADO group + AAA topics from ONE memory. Any of them DMing ran the agent with the sovereign's memory in context.

## The native fix: profile multiplexer

**`gateway.multiplex_profiles: true`** — one gateway process serves every named profile, each with its own HERMES_HOME (memory, skills, sessions, SOUL.md, config) and own credentials.

Mechanics verified from source (`gateway/run.py` + `hermes_cli/profiles.py`, 2026-08-09):

- `profiles_to_serve(multiplex=True)` = the default profile + every valid named profile dir under the profiles root — the single chokepoint for which profiles a gateway serves.
- `_start_secondary_profile_adapters()` boots each non-active profile's adapters under that profile's HERMES_HOME + secret scope (`_profile_runtime_scope`: contextvar-scoped config/skills/memory + `set_secret_scope` for that profile's `.env`), stamps `event.source.profile`, then delegates to the shared `_handle_message` — the turn resolves THAT profile's config/skills/credentials.
- **Credential collision refused:** two profiles polling the same bot token is detected at startup and blocks the adapter — each human's profile needs its OWN bot token (BotFather). One token cannot serve two profiles.
- **Fail-closed secrets:** with multiplexing on, unscoped `get_secret()` reads crash loudly instead of leaking a cross-profile value. Never cross-contaminate `.env` files.
- Config forms: `gateway.multiplex_profiles: true` in config.yaml, or `hermes config set gateway.multiplex_profiles true`. Toggle is inert when off (single-profile behavior unchanged).

## Routing model

**One bot per human profile.** Sovereign tooling (scar_read, meaning_anchor, seal paths) lives ONLY in the sovereign's profile; every other profile is a clean slate with zero scar access — "referenced, never owned" enforced by the profile boundary, not by discipline.

```
┌─ gateway (1 process) ─────────────────────────────┐
│  gateway.multiplex_profiles: true                 │
│                                                   │
│  aaa-hermes  ← your bot    ← ARIF  → HELIX HERE  │
│      memory: scars, F13, sovereign doctrine       │
│      tools:  scar_read · meaning_anchor · seals   │
│                                                   │
│  syed        ← Syed's bot ← Syed   → clean slate  │
│      memory: his own only, zero scar access       │
│                                                   │
│  wawa        ← Wawa's bot ← Wawa   → clean slate  │
│      memory: hers only, zero federation surface   │
└───────────────────────────────────────────────────┘
```

Group routing is by bot presence: whichever profile's bot is in a group serves that group. SADO/AIA groups can stay on the sovereign bot or move to a per-user bot depending on isolation needs.

## Migration checklist (all reversible; BotFather is the only human step)

1. `hermes profile create <name>` per human (own memories/, skills/, sessions/).
2. **Remove other humans' IDs from the sovereign profile's `allow_from` / `group_allow_from`** — closes the live leak immediately, even before bots exist.
3. Create one bot token per human via @BotFather → that profile's `.env` only.
4. Flip `gateway.multiplex_profiles: true`, restart gateway **from an external shell** — the gateway blocks self-restart from inside its own session (SIGTERM propagation kills the executing turn). See `hermes-telegram-gateway-ops` restart discipline.

## Where the leak hides (config keys to audit)

- `allow_from` / `group_allow_from` in the active profile's config.yaml — lists every human who can DM the sovereign profile. Multi-user DMing the owner's bot = shared memory context.
- `channel_directory.json` — shows every chat the gateway has seen (DMs from other humans appear here even when not whitelisted). Read it to enumerate who has touched the profile.
- `home_channel` + `free_response_chats` — group delivery targets; check which profile's bot owns which group.

## Pitfalls

- **Env allowlists override config — adding a user to `allow_from` alone does nothing (2026-08-09, Izzu/AIA incident).** If `TELEGRAM_ALLOWED_USERS` / `TELEGRAM_GROUP_ALLOWED_USERS` are exported (e.g. from `kunci-mas.env`), the adapter treats them as SOLE AUTHORITY and never reads `telegram.allow_from` / `group_allow_from` from config.yaml. Root cause of "bot replies to Arif but silently drops Izzu": Izzu's ID was in config but NOT in the env var. **Fix:** add the ID to the env var (kunci-mas.env) AND the systemd drop-in (`/etc/systemd/system/hermes-*-gateway.service.d/zzz-webhook-override.conf`), then restart. Diff all three sources: kunci-mas.env / flat.env / drop-in.
- **Lane memory persistence needs the hook DECLARED in plugin.yaml, not just registered in `__init__.py` (2026-08-09).** Adding `_on_post_llm_call` + `ctx.register_hook("post_llm_call", ...)` in the lane_switch plugin `__init__.py` is not enough — the gateway only loads hooks listed under `hooks:` in the plugin's `plugin.yaml`. Symptom: memory files stay empty, agent has amnesia across turns ("hang yang hantar hang buat lupa"). Fix: add `- post_llm_call` to `plugin.yaml` `hooks:` list, restart gateway.
- **Memory accumulation = the anti-amnesia pattern.** The lane_switch plugin READS memory files but nothing WRITES them until you add a `post_llm_call` hook that appends `user_message`/`assistant_response` to `MEMORY-{lane}.md`. Without it every turn is stateless. With it, each interaction appends to the lane file and the next turn loads context. Skip the operator lane (arif) — his memory is managed separately.
- **`lanes.yaml` line-number corruption (2026-08-09).** Writing `grep -n`/`cat -n` output back into a YAML file embeds `N|` prefixes on every line; the file still "looks" right in `head` but YAML parses the numbers as content and pattern matching silently fails. Repair: `python3 -c "import re; s=open(p).read(); open(p,'w').write(re.sub(r'^\d+\|','',s,flags=re.M))"`. Always validate with `yaml.safe_load` after editing lanes.yaml.
- **free_response_chats must include DM chat IDs for no-mention DM replies.** `require_mention: false` only applies to chats listed in `free_response_chats`; a DM not listed still requires mention. Add each human's numeric DM ID to `free_response_chats` (alongside groups) if the bot should reply to DMs without @mention.
- **Unified skills doctrine — ONE skill set for ALL lanes, no per-user fragmentation (F13 ruling 2026-08-09).** Arif: "make sure the skills all unified AAA. No need different users different group different skills. Penat wei." Do NOT maintain per-lane skill lists in `lanes.yaml` (syed → trading/syedos, izzu → comfyui, etc.). All non-guest lanes share the same `skills:` block (currently: ai-media-generation, ai-media-generation-ops, ai-video-generation, trading-screenshot-analysis, pdf-report-generation, humanizer, ocr, apex-judge). The lane card injects the same PRIORITIZED list + a CAPABILITY MAP for every lane; differentiation is by memory files and voice, not by skill inventory. Guest lane keeps zero skills (F13 — no data for unknown users).
- **Profile isolation is memory + credentials, not chat routing.** The multiplexer isolates per-profile state; it does NOT route one bot's chats to different profiles. Routing is by bot identity, so one bot token per profile is a hard requirement, not a choice.
- **Do NOT just remove a user's ID from `allow_from` without a plan** — they lose all access (including groups they legitimately use). Create their profile + bot first, then revoke from the sovereign profile.
- **Restart from an external shell** — `hermes gateway restart` from inside the gateway session is blocked by design (see above). Use a separate terminal or a scheduled job.
- **Profile names are validated** (`_PROFILE_ID_RE`) — lowercase, hyphens/underscores only. `hermes profile list` shows active vs stopped; a multiplexer serves all valid named profiles regardless.
- **Verify with `hermes status`** after flipping — the served-profiles list appears in runtime status; confirm all profiles show as served, not just the active one.
- **One person can need MULTIPLE lanes by room (2026-08-09).** Syed has two lanes: `syed` (SADO group: banter, trading, group-safe) and `syed-dm` (personal DM: full medical timeline for Mak, GERD tracking, CAREGIVER capability). The `lane_switch` plugin resolves which lane to activate by checking both `telegram_user_id` AND `telegram_chat_id` — DM chat_id == user_id triggers DM lane, group chat_id triggers group lane. This prevents sensitive family medical details from surfacing in a semi-public group chat. **Implementation:** `lanes.yaml` defines separate memory_files per lane; the plugin loads only the matching lane's memory. PII (IC numbers, hospital names, surgery details) must be scanned and removed from group-safe files with `grep -in` before declaring the split complete. Guardrail annotations in the group file (e.g., "GROUP-FORBIDDEN: detail in DM lane only") are acceptable — actual medical details are NOT.
- **Social graph edges must match real relationships (2026-08-09).** When registering a new person, create the edge in `social-graph.yaml` that reflects the ACTUAL relationship, not a default. Aliff = kawan rapat Arif (ARIF⇄ALIFF edge), NOT connected to Syed (no SYED⇄ALIFF edge). Wrong edges cause the agent to incorrectly assume knowledge transfer between people who don't know each other.
- **Base USER.md and MEMORY.md must contain ONLY sovereign invariants (2026-08-09).** Per-person data (Aliff's CPPS, Syed's GERD, any Telegram IDs, IC numbers) must NEVER live in the injected base files. Split to per-person files (`USER-syed.md`, `USER-aliff.md`) and lane-specific files (`MEMORY-syed.md`, `MEMORY-syed-dm.md`). The base file is injected into EVERY turn — if it carries Person B's data, Person A's session sees it (F13/F6 MARUAH leak).

## Related

- `hermes-telegram-gateway-ops` (hub pack) — identity truth, env injection, restart discipline, allowlist reconciliation. The multiplexer complements it: that skill resolves which bot speaks; this one gives each human their own bot.
- `arifos-federation-ops` — sovereign seal paths; the sovereign profile is the only one that should hold seal/scar tooling.
- `forge-vault-seal-receipt` — receipt schema; `meaning_anchor`/`scar_lineage` extension fields apply only in the sovereign profile's seal path.

<!-- SKILL-WITNESS-NOTE (auto, additive-only) -->
Witnessed reality moved this skill's selection to **ROUTE or MERGE**.
Scar signatures: SCAR-AGY-004-session-gate-confusion
Do not treat this skill as neutral until the signatures are resolved.
<!-- /SKILL-WITNESS-NOTE -->
