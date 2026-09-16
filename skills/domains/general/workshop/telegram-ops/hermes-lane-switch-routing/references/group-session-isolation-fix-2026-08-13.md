# Group Session-Isolation Fix — Implemented 2026-08-13

Implements the fix for the SADO-group ("agent tak nampak previous message") +
"reacts differently per person" complaints. Companion to
`lane-resolution-2026-08-12.md` (diagnosis only). This is the patch.

## Root cause (verified, not assumed)

- **"Can't read previous message" = SESSION ISOLATION across time gaps**, NOT the
  observe pipeline.
  - SADO (`-1003815535761`) is in `free_response_chats`, `require_mention=false`.
  - `observe_unmentioned_group_messages` is mutually-exclusive with
    `require_mention=false` (adapter.py gate, default false) → every message is a
    full turn (`observed=0` on all 37 user msgs in state.db).
  - Live DB has 4+ sessions for SADO split by idle gaps; a new session starts with
    an empty thread → agent genuinely has no memory pre-gap.
- **"Reacts differently per person" = lane design** (by design) but three real
  frictions: sovereign missing a group register (person-fallback drops Arif to
  FULL sovereign in shared room), chat-stamp pollution, and rigid persona flip.

## The four edits

### 1. lanes.yaml — `arif-sado` register
```yaml
  arif-sado:
    display_name: Arif — SADO group register (shared room)
    authority_level: SOVEREIGN
    triggers:
      telegram_user_ids: ['267378578']
      telegram_chat_ids: ['-1003815535761']
    capabilities: [INTELLIGENCE, ADVISORY, TRACKING, REMINDER]
    doctrines: { group_capability_scoped: true, dynamic persona: true, ... }
```
Must sit BEFORE the deeper `arif` personal register so Pass 1 exact-match wins.

### 2. lane card — capability-aware map
Branch on `doctrines.group_capability_scoped`:
- SCOPED: `CAPABILITY MAP (SCOPED — shared group room, intelligence tools only)`
  + `GROUP SCOPE BOUNDARY` (may SEARCH/REASON/ANALYZE/in-chat media; may NOT build
  /deploy MCP GUI apps, stage/forge artifacts, external publish)
  + scoped `GOVERNANCE LADDER (group scope)`.
- else: FULL map (previous behaviour).

### 3. lane card — dynamic persona + recent history
- `dynamic persona` doctrine → instruction to calibrate voice to the human's
  current tone/energy/state from recent context (not rigid register flip).
- `_recent_lane_history(lane_id, cfg, max_blocks=6)` → reads tail of lane MEMORY
  file, extracts last N `### timestamp · chat=... · user=...` blocks, injects as
  `RECENT THREAD HISTORY (cross-session carry — read before replying)` on EVERY
  turn. This is the cross-session carry that bridges the time-gap session split.

### 4. pre_gateway_dispatch — stop stamping shared groups
```python
try:
    _is_group = int(chat_id) < 0
except (TypeError, ValueError):
    _is_group = False
if chat_id and not _is_group and state.get(f"chat:{chat_id}") != lane:
    state[f"chat:{chat_id}"] = lane
```
Then clear stale `chat:-1003815535761 = arif` etc. from `.runtime.json`
(keep `user:<id>` and DM `chat:<id>` stamps).

## Deploy steps (the part that bites)

1. **Plugin dir is gitignored** — `git add -f <plugin>` (load-bearing logic, F11).
2. **Gateway holds plugin in memory at startup** — a file edit does NOT take
   effect until restart:
   ```bash
   systemctl restart hermes-asi-gateway.service
   systemctl is-active hermes-asi-gateway.service
   ```
   New MainPID (`systemctl show -p MainPID`) = fresh plugin import.
3. **Verify before commit**:
   - `ast.parse` on the plugin.
   - `detect_lane` full matrix: Arif-in-SADO→arif-sado, Syed-in-SADO→syed,
     Arif-DM→arif, Syed-DM→syed-dm, Aliff-AIA→aliff-aia, Izzu-AIA→izzu-aia,
     Unknown→guest (8/8).
   - `_lane_card('arif-sado')` contains SCOPED + GROUP SCOPE BOUNDARY + DYNAMIC
     PERSONA + RECENT THREAD HISTORY markers.

## Verification evidence (this session)

- detect_lane matrix 8/8 pass.
- `_recent_lane_history('syed')` returned Syed's Hooligan V6 exchanges (15:34 /
  15:36) — cross-session carry works.
- `_lane_card('arif-sado')` emitted all four markers.
- Commits: `de0d8c9` (fix), `b7536b9` (model switch), `7463db5` (docs) → main.
- Gateway `hermes-asi-gateway` restarted, active, no errors, new PID 3344440.