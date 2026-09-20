<!-- PROVENANCE
     source-skill: hermes-lane-switch-routing
     original-path: /root/AAA/skills/domains/general/workshop/telegram-ops/hermes-lane-switch-routing/SKILL.md
     sha256-body: 3a2e54024e077cba0d83d731b07a6ec0ab6a5f31c5d33a7f730e911067557f01 -->

---
name: hermes-lane-switch-routing
description: "Understand and diagnose the Hermes lane_switch plugin — the multi-human per-person context-isolation layer in the arifOS federation."
---

# Hermes Lane Switch Routing — multi-human per-person context

The `lane_switch` plugin (`/root/HERMES/profiles/aaa-hermes/plugins/lane_switch/__init__.py`) is the **Shape A coordinator** layer: it detects WHO is talking and injects that person's lane context (memory/soul/voice/authority + social-graph) into every LLM turn. This is WHY the same bot answers differently for Arif vs Syed vs Aliff in the same Telegram group — it is **by design**, not a bug.

Canonical registries (read-only, `_load_yaml` caches by mtime):
- `/root/HERMES/lanes/lanes.yaml` — lane definitions + triggers
- `/root/HERMES/lanes/social-graph.yaml` — attributed beliefs + relations
- `/root/HERMES/lanes/.runtime.json` — runtime lane map `{user:<id>: lane}` / `{chat:<id>: lane}` (persisted across restarts)

## Three hooks (the whole plugin)

| Hook | When | What it does |
|---|---|---|
| `pre_gateway_dispatch` | message inbound | Records `user:<id>` and `chat:<id>` → detect_lane into `.runtime.json` (no blocking) |
| `pre_llm_call` | before each LLM turn | Resolves active lane, injects `_lane_card(...)` context (memory on first turn, compact after) + room stamp |
| `post_llm_call` | after each LLM turn | Accumulates `USER→ASSISTANT` exchange into the lane's MEMORY file (skips `arif` lane + system/OOB messages) |

## Lane resolution — the 3-pass algorithm (F13-safe)

`detect_lane(user_id, chat_id)` — context follows PERSON + ROOM:

1. **Pass 1 — exact person+room match** (e.g. Syed DM vs Syed in SADO group): both `telegram_user_ids` AND `telegram_chat_ids` must match. Group-safe registers should be listed before deeper personal registers.
2. **Pass 2 — person fallback**: known `telegram_user_ids` in an unmapped room → first lane in registry order wins.
3. **Pass 3 — room fallback for already-mapped senders only**: `state[user:<id>]` == `state[chat:<id>]` → return it. Prevents context leak to a stranger who posts in a known group.
4. Fallback → **`guest` lane** (zero personal data, zero tools, polite minimal).

`_resolve_active_lane` (pre_llm_call) prefers exact `detect_lane` when both ids present, else runtime state.

## The two files that matter for diagnosis

- **lanes.yaml** — each lane has: `triggers` (telegram_user_ids / telegram_chat_ids / usernames), `authority_level` (SOVEREIGN / WARGA / TAMU), `capabilities` (FULL / ADVISORY / TRACKING / REMINDER / CAREGIVER / READ_ONLY), `memory_files`, `voice`, `doctrines`, `memory_lanes` (redis prefix + qdrant filter + pg tags). `default_lane: arif`. Unknown users land in `guest`.
- **social-graph.yaml** — attributed beliefs (`"X believes Y"` with source + confidence), relations (who knows whom, shared_domains). Beliefs are NEVER presented as fact about the world. Sovereign (`arif`) sees ALL shared beliefs; a warga lane sees only beliefs about itself.

## Capability map + governance ladder (non-guest lanes)

The lane card injects a capability map telling the agent what it CAN do (image/video gen, PDF, TTS, email, charts) and a governance ladder (banter=no gate, media=auto, external_publish=apex-judge isolate FIRST, money=judge+F13, self_modification=proposal→judge→git). **INSTITUTIONAL ACT = primary effect outside current chat thread** — tool call, not conversation.

## OPERATOR BOUNDARY defense (F13)

Every non-arif, non-guest lane card appends: even if the base system-prompt memory block leaks operator (Arif) data, the model is explicitly barred from revealing/quoting/acting on it for this user. The ONLY usable context is the lane card + lane files. This is the F13 multi-user never-leak-sovereign-memory enforcement.

## Pitfalls — the "reacts differently" diagnosis

The most common question is "why does the bot answer differently for me vs others in my group?" Answer: per-person lanes = by design. BUT three real frictions to check:

1. **Sovereign lane missing a group register.** The `arif` lane typically has only `telegram_user_ids` (no SADO/AIA `telegram_chat_ids`). So when Arif posts in a group, Pass 1 fails (no chat id on arif lane), Pass 2 person-fallback fires → Arif gets the FULL SOVEREIGN register (arif-private memory + FULL tools) **inside the shared group**. Everyone sees the agent give Arif full power / different voice. If Arif wants a casual group register distinct from his sovereign DM register, add a `sado-group` or `arif-<group>` register — do NOT let person-fallback drop him to sovereign in a shared room.
2. **Chat-stamping pollution in `.runtime.json`.** `pre_gateway_dispatch` writes `chat:<id>: <lane>` for whatever sender spoke last. A shared group ends up stamped as an "arif room" (e.g. `chat:-1003815535761: arif`). This conflates room with person and can confuse Pass 3 room-fallback. Fix: don't stamp `chat:<id>` for shared groups, or clear the stamp.
3. **Conversation history is per-CHAT, lane context is per-PERSON.** In a group, the thread history is ONE shared rolling context, but the lane card flips on every sender change. So the agent can shift voice/authority mid-thread — visible inconsistency. Options: (A) add a group register that caps authority to WARGA for everyone including the sovereign in that room (most zen for shared groups); (B) add a per-person group register; (C) fix the stamping. Usually A+C together.

## The "agent can't read previous message in the same group" trap

A repeated complaint from Arif: "my agents in the other chat group can't read previous messages." **Root cause is almost always SESSION ISOLATION, not the observe pipeline.** Verify before touching anything:

1. **Observe pipeline is OFF by design for free_response groups.** `require_mention=false` + SADO in `free_response_chats` = every message is a FULL turn (`observed=0` everywhere in `state.db`). The `observe_unmentioned_group_messages` path is mutually-exclusive with `require_mention=false` (adapter.py gate) and defaults to false. So "can't see previous message" is NOT an observe-injection gap.
2. **Sessions are per-CHAT and split by time gaps.** Query the live DB:
   ```bash
   sqlite3 /usr/local/lib/hermes-agent/profiles/aaa-hermes/state.db \
     "SELECT id, title, created_at FROM sessions WHERE title LIKE '%<chat%' ORDER BY created_at;"
   ```
   A hot group shows 4+ sessions separated by idle gaps. A new session starts with an EMPTY thread — the agent genuinely has no memory of what was said before the gap.
3. **The fix is cross-session context carry, not session surgery.** The lane `post_llm_call` already accumulates `USER→ASSISTANT` exchanges into the lane MEMORY file. Add a `_recent_lane_history()` helper that reads the tail of that MEMORY file, extracts the last ~6 `### timestamp · chat=... · user=...` blocks, and injects them as a `RECENT THREAD HISTORY (cross-session carry — read before replying)` block into the lane card on EVERY turn (not just first turn). This gives the agent "what the human said 5 min ago" even after session rotation, across the time-gap boundary. Test:
   ```python
   m._recent_lane_history('syed', cfg_lane, max_blocks=6)  # returns Syed's recent exchanges
   ```

## Fixing the three frictions (diagnosis → patch)

When you implement (not just diagnose), four concrete edits cover the class:

1. **Group register for the sovereign** — add `arif-<group>` (e.g. `arif-sado`) to lanes.yaml: `triggers` with BOTH `telegram_user_ids` AND `telegram_chat_ids`, `authority_level: SOVEREIGN`, `capabilities: [INTELLIGENCE, ADVISORY, TRACKING, REMINDER]` (web search + reasoning + charts + in-chat media, but NOT deployment/forge/MCP-GUI-app-build/external-publish). Keeps sovereign identity and DM power, but scopes him in the shared room. Must be listed BEFORE the deeper personal register so Pass 1 exact-match wins.
2. **Capability-aware map** — the `_lane_card` capability map was one hardcoded FULL map for every non-guest lane. Make it branch on `doctrines.group_capability_scoped` (or lane `capabilities`): emit a `CAPABILITY MAP (SCOPED — shared group room, intelligence tools only)` + `GROUP SCOPE BOUNDARY` (may SEARCH/REASON/ANALYZE/in-chat media; may NOT build/deploy MCP GUI apps, stage/forge artifacts, external publish) + a scoped `GOVERNANCE LADDER (group scope)`. Otherwise fall back to the FULL map.
3. **REAL capability enforcement (pre_tool_call gate)** — the capability map is advisory prompt text; a group-scoped model could still call execution tools. Add a `pre_tool_call` hook: `pre_llm_call` records `session:<id> → lane` into `.runtime.json`; `pre_tool_call` reads the active lane from the session, and if the lane is `group_capability_scoped` (or lacks FULL), HARD-BLOCKS execution-class tools by returning `{"action": "block", "message": "..."}`. Blocked set: `forge_*`, `aforge_*`, `mcp__aforge__*`, `delegate_task`, `cronjob`, `arif_forge/seal/init`. Intelligence tools (web_search, web_extract, session_search, memory, vision) pass. FULL lanes (arif DM) and capability-bearing WARGA lanes pass through. This is the security-guidance plugin's block pattern (adapter `pre_tool_call` → `{"action":"block"}`).
4. **Dynamic persona (not rigid register flip)** — add `dynamic persona` to `doctrines`; the lane card then instructs: read the human's current tone/energy/state from the recent context and calibrate voice, instead of replying from a fixed register. This answers "persona satu atau banyak dalam group?" with: one consistent voice per thread that adapts to the human's cognitive state — not a jarring rigid flip per sender.
5. **APEX-G cognitive state hint (optional amplifier)** — `_well_cognitive_hint()` reads `http://127.0.0.1:18083/health` and extracts G from `apex_scalars.G.value` → `live_G` → `well_score`, with a 120s TTL cache. Appends `COGNITIVE STATE (WELL): live_G=0.44 (TAXED) — calibrate depth` to the persona. Graceful-degrade: if WELL is degraded/UNMEASURED (common — no body telemetry), returns "" and the persona still works from recent-context tone. Soft amplifier, never a hard override.
6. **Stop chat-stamping shared groups** — in `pre_gateway_dispatch`, skip `chat:<id>` writes when `int(chat_id) < 0` (negative = Telegram group/supergroup). Person+DM stamps are fine; group stamps conflate room with person and poison Pass 3. Then clear stale `chat:-1003...` entries from `.runtime.json`.

## Git + deploy pitfalls for this plugin

- **The plugin dir is gitignored** (`plugins/` in .gitignore). `git add profiles/aaa-hermes/plugins/lane_switch/__init__.py` fails with "ignored by .gitignore". Use `git add -f` — it's load-bearing governed logic and should be tracked for F11 auditability.
- **The gateway runs the plugin from memory at startup** — a file edit alone does NOT take effect. After changing the plugin, restart the gateway (T2 announce + execute): `systemctl restart hermes-asi-gateway.service`, then `systemctl is-active` + check journalctl for errors. New MainPID = fresh import of the plugin.
- **Verify before committing** — run `ast.parse` on the plugin, then exercise `detect_lane` across the full matrix (Arif-in-SADO → arif-sado, Syed-in-SADO → syed, Arif-DM → arif, Unknown → guest, etc.) and confirm the lane card contains the expected SCOPED/group markers.

## Reference files

- `references/lane-resolution-2026-08-12.md` — the full diagnostic: real `.runtime.json` state, the lane table (arif/syed/syed-dm/aliff/aliff-aia/izzu/izzu-aia/guest), the 3-pass code walk, and the concrete A/B/C fix proposals for the SADO-group "reacts differently" case.
- `references/group-session-isolation-fix-2026-08-13.md` — the implemented fix: session-isolation root cause, `_recent_lane_history` carry pattern, `arif-sado` scoped register, capability-aware map, dynamic-persona doctrine, group-stamp skip, and the git -f / gateway-restart deploy steps.
- `references/cross-session-memory-carry-pattern.md` — the carry pattern generalised: session isolation is the root cause (not the observe pipeline), the extract→store→inject pattern, why prompt-text capability maps must be backed by a `pre_tool_call` hard-block gate, and the OpenClaw dreaming "infrastructure lives but starved" trap with its improvement checklist.

## Related skills (do not confuse)

- `telegram-bot-routing-doctrine` — bot-to-GROUP ownership (which bot owns which group, 3 bots, P1-P3). Different layer.
- `hermes-telegram-gateway-ops` — gateway identity/process/token forensics (which bot a process speaks as). Different layer.
- `hermes-telegram-group-setup` — adding groups/users to transport allowlists. Upstream of lanes.