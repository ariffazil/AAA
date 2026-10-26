# Name-Mention — CURRENT Runtime Flow (as-built, read-only)

> Scope: document the live path from "a human name appears in an inbound Telegram
> message" to "the agent sees / handles it". Every claim is anchored to
> `file:line`. Read-only audit — no code was changed. Anchors are to the live tree
> as of this pass; verify line drift before acting.
>
> **Headline finding:** there is **no per-message name-mention router** today.
> Identity is resolved only from the **sender's numeric Telegram id + room id**
> (`detect_lane`), never from the words of the message. The "people" the agent is
> shown are the people **present in the active lane**, injected as a constant
> per-room section of a lane card on **every** LLM turn. Name→person mapping, if
> any, happens **semantically inside the model** from that card + the room
> `channel_prompt`, not in code.

---

## 1 · Exact call chain (inbound message → lane card → people block)

### 1.1 Transport → gateway event
- Telegram adapter builds a `MessageEvent` and, for group/observe turns, stamps the
  sender header as `[<user_name>|<user_id>]` prepended to the text:
  `plugins/platforms/telegram/adapter.py:6248-6250` (`_telegram_group_observe_attributed_text`).
- The bot-mention gate (whether a group message is treated as addressed to the bot)
  lives at `plugins/platforms/telegram/adapter.py:6240` (`_telegram_require_mention`
  / reply-to-bot / mention check). Config: `require_mention: false` at
  `/root/.hermes/config.yaml:155` — i.e. the bot answers group messages without
  needing an `@` mention.

### 1.2 Gateway inbound pipeline
- `GatewayInboundMixin._handle_message` — `gateway/run_inbound.py:1281`.
- Admission/auth gate `_hm_admit_event` — `gateway/run_inbound.py:161`; it fires the
  dispatch hook at `gateway/run_inbound.py:226`:
  `event = await self._hm_pre_gateway_dispatch_hook(event, source)`.
- `_hm_pre_gateway_dispatch_hook` — `gateway/run_inbound.py:67-102`; it calls the
  `pre_gateway_dispatch` plugin hook (`ainvoke_hook`, line 75-79) and honours
  `skip` / `rewrite` / `allow` return actions (`gateway/run_inbound.py:84-101`).
- Per-message text prep `_prepare_inbound_message_text` — `gateway/run_inbound.py:1703`;
  sender attribution prefix `_prefix_inbound_sender_context` — `gateway/run_inbound.py:1420`,
  applied at `gateway/run_inbound.py:1719`. For shared multi-user sessions it prepends
  `[{_safe_user_name}] ` to the message (`gateway/run_inbound.py:1435`).
- `@`-reference expansion `_expand_inbound_context_references` —
  `gateway/run_inbound.py:1672-1701`, gated by `if "@" in message_text` at
  `gateway/run_inbound.py:1727`. This resolves `@file:`/`@folder:`/`@git:`/`@url:` and
  **plugin-registered prefixes** (see §5).

### 1.3 Agent construction carries sender identity
- Gateway constructs the turn agent and passes the **sender identity from `source`**
  into the agent params:
  `gateway/run_turn.py:2560-2563`
  ```python
  platform=platform_key,
  **{k: getattr(source, k) for k in (
      "user_id", "user_id_alt", "user_name", "chat_id", "chat_name", "chat_type", "thread_id",
  )},
  ```
- `init_agent` stores these as `agent._<name>`:
  `agent/agent_init.py:2350-2353` (the tuple `_GATEWAY_IDENTITY_PARAMS`) and
  `agent/agent_init.py:2409-2410`:
  ```python
  for _name in _GATEWAY_IDENTITY_PARAMS:
      setattr(agent, f"_{_name}", _params[_name])
  ```
  So `agent._user_id` = sender's numeric Telegram id, `agent._chat_id` = chat id.

### 1.4 pre_llm_call → lane card → people section
- Turn prologue runs the hook and collects injected context:
  `agent/turn_context.py:1127-1131`
  ```python
  plugin_user_context = _collect_pre_llm_call_context(
      agent, effective_task_id=effective_task_id, turn_id=turn_id,
      original_user_message=original_user_message, messages=messages,
      conversation_history=conversation_history,
  )
  ```
- `_collect_pre_llm_call_context` — `agent/turn_context.py:749-804`; it invokes the hook
  with the sender/chat ids at `agent/turn_context.py:760-773`:
  ```python
  _pre_results = _invoke_hook(
      "pre_llm_call",
      ...
      sender_id=getattr(agent, "_user_id", None) or "",
      chat_id=getattr(agent, "_chat_id", None) or "",
  )
  ```
  and joins each returned `{"context": ...}` / str into one string
  (`agent/turn_context.py:784-801`). Docstring is explicit
  (`agent/turn_context.py:753-755`): *"their context is injected into the user message
  (never the system prompt)."*
- Injection point at API time: `agent/turn_context.py:1236-1249`
  (`compose_user_api_content(... , plugin_user_context)`), and the field rides the
  turn as `TurnContext.plugin_user_context` (`agent/turn_context.py:467`, returned at `1164`).
- `lane_switch` implements the hook:
  - hook registered: `profiles/aaa-hermes/plugins/lane_switch/__init__.py:995`
    (`ctx.register_hook("pre_llm_call", _on_pre_llm_call)`).
  - `_on_pre_llm_call` — `__init__.py:693-738`; resolves lane (`_resolve_active_lane`,
    `693` → `676`) and builds the card at `__init__.py:727-732`:
    ```python
    card = _lane_card(
        lane,
        include_memory=bool(is_first_turn),
        sender_id=sender_id,
        chat_id=chat_id,
    )
    ...
    return {"context": card}          # __init__.py:735
    ```
  - `_lane_card` — `__init__.py:560-622`. Section order and sources:
    ```python
    598    # 1. lane_id (~20 B)
    599    sections.append(f"lane={lane_id}")
    601    # 2. recent_history (≤500 B, last 5 messages)
    602    recent = _recent_lane_history(lane_id, cfg, max_blocks=5, max_total_bytes=500)
    ...
    606    # 3. people_facts (≤200 B, sourced only)
    607    pf = _people_facts_skeleton(lane_id, cfg, max_total_bytes=200)
    608    if pf:
    609        sections.append(pf)
    611    # 4. well_snapshot (≤100 B, one-liner)
    612    well = _well_snapshot_skeleton(max_bytes=100)
    ...
    616    # 5. room_stamp (≤130 B)
    617    sections.append(
    618        f"chat={chat_id or '?'} · sender={sender_id or '?'} · lane={lane_id}"
    619    )
    ```
  - **The people section is built by `_people_facts_skeleton` (`__init__.py:259-361`),
    NOT by `_people_block`.** `_people_block` (`__init__.py:463-557`) is defined but
    **never called** — same dead-code class the file already documents for
    `_care_governor_block` (`__init__.py:38-49`, `426-431`). Grep confirms only
    `_lane_card(...)`, `_people_facts_skeleton(...)` are referenced; `_people_block(`
    has no call site.

---

## 2 · WHERE a human name/alias is resolved today (or NOT)

**It is NOT resolved per-message.** No code path reads the message body to turn a
name like "Syed" / "Abang Sado" / "@Jia" into a person identity.

What exists instead, all **sender-side and room-side**:

1. **Sender id → lane** — `detect_lane(user_id, chat_id)` (`__init__.py:99-141`) matches
   the sender's numeric `telegram_user_ids` / `telegram_chat_ids` against
   `/root/HERMES/lanes/lanes.yaml` `triggers` (pass 1/2/3, `__init__.py:113-141`). It
   never inspects `message_text`.
2. **Lane → people present** — `_people_facts_skeleton` iterates `people.yaml` and keeps
   a person only if the lane's `telegram_user_ids` / `telegram_chat_ids` intersect that
   person's `identities` (`__init__.py:294-301`):
   ```python
   present = bool({str(i.get("value")) for i in uid_idents} & lane_uids) or bool(
       {str(i.get("value")).split(":")[0] for i in cid_idents} & lane_cids
   )
   ```
   The displayed string is `person.get("display_name", pid)` (`__init__.py:317`) — so
   `display_name` resolution happens here, keyed on the **lane**, not on any name in the
   message.
3. **chat_id → friendly name** — `/root/.hermes/channel_aliases.json` is a display-name
   overlay applied to the channel *directory* (`gateway/channel_directory.py:65-86`,
   `_apply_channel_aliases`; applied on build at `165` and on read at `395/398`). Used for
   `send_message` target resolution / directory display (`lookup_channel_type:402`,
   `resolve_channel_name:408`). It is **not** consulted for inbound mention resolution.
4. **Name → person, semantically** — falls to the model. The lane card prints
   `display_name` values (`__init__.py:317-332`) and the room prompt tells the model who
   is in the room. Actual matching of a name spoken in a message to a person is done by
   the LLM from that text. There is no server-side name index.

Net: today a name in the message resolves to an identity **only if the LLM chooses to map
it**, using the room-scoped people block + `channel_prompt`. Code has no name→identity
step.

---

## 3 · WHAT is injected, and WHEN

| Hook | Cadence | What it injects | Anchor |
|---|---|---|---|
| `pre_gateway_dispatch` | per inbound message | **nothing** (side-effect only: writes `.runtime.json` lane stamps; returns `None`) | `__init__.py:626-672` |
| `pre_llm_call` | **every LLM turn** | the lane card as `{"context": card}`, appended to the **user message** (not system prompt) | `__init__.py:693-735`; `agent/turn_context.py:753-755`, `1236-1249` |
| `post_llm_call` | per assistant turn | mode-shape enforcement; appends the exchange to lane `MEMORY-<lane>.md` | `__init__.py:741-879` (memory write `863-867`) |
| channel prompt | per turn (stable per room) | `config.extra.channel_prompts[chat_id]` → **ephemeral system prompt** | `gateway/run_turn_runner.py:1839-1853`; `gateway/platforms/base.py:1846`; source data `/root/.hermes/config.yaml:108-114` |

Details:

- **`_on_pre_gateway_dispatch`** (`__init__.py:626-672`): resolves lane and persists
  `user:<id>` / `chat:<id>` stamps to `/root/HERMES/lanes/.runtime.json`
  (`__init__.py:650-669`). It has the raw `event` in hand but ignores `event.text`;
  it returns `None` ("allow normal dispatch", `__init__.py:672`). It is **not** an
  injection point today.
- **`_on_pre_llm_call`** (`__init__.py:693-738`): **per turn**, builds the card and also
  records `session:<id> → lane` for the tool gate (`__init__.py:718-726`).
  `include_memory=bool(is_first_turn)` is a **no-op** — the parameter is explicitly
  dead ("`include_memory` parameter preserved for API compat; the parameter is a no-op
  now", `__init__.py:586-588`; docstring `563-566`). So the card is effectively the same
  every turn; only `recent_history` (from lane MEMORY, `_recent_lane_history`, `168-256`)
  and `room_stamp` (`617-619`) carry per-turn/per-room variation.
- **Card section budgets** (`__init__.py:560-622`): `lane` ~20 B; `recent_history`
  ≤500 B from the lane's `MEMORY` file; `people_facts` ≤200 B sourced-only; `well_snapshot`
  ≤100 B from WELL (`_well_cognitive_hint`, HTTP `127.0.0.1:18083/health`, `389-423`);
  `room_stamp` ≤130 B.
- **`_people_facts_skeleton`** output (`__init__.py:290`): a one-line-per-person section
  headed `PEOPLE (sourced):`, each line `- <display>: <fact> [src:<source>]`
  (`__init__.py:317-332`), max 2 facts per person (`304-315`).
- **Room prompt:** `channel_prompts` (per `chat_id`, e.g. Arif DM `267378578`
  `config.yaml:109`; SADO group `-1003815535761` `config.yaml:113`) is merged into the
  ephemeral system prompt by `_combined_ephemeral_prompt` (`gateway/run_turn_runner.py:1839-1853`),
  resolved by `resolve_channel_prompt` (`gateway/platforms/base.py:1846-1856`). The SADO
  prompt itself instructs the model to "sentiasa rujuk header `[Sender|ID]`" and that
  `@ASI_arifos_bot` is stripped before it reads — i.e. name/entity disambiguation is
  **delegated to the prompt + model**, not to code.

---

## 4 · The scope `dm` / `shared` gate (verbatim, with anchors)

The room-shape helper (fail-closed) — `__init__.py:446-460`:

```python
def _is_shared_room(cfg: dict) -> bool:
    """True when this lane is a shared room (multi-human) — fail closed."""
    try:
        if (cfg.get("doctrines") or {}).get("group_capability_scoped") is True:
            return True
        for cid in (cfg.get("triggers") or {}).get("telegram_chat_ids", []) or []:
            head = str(cid).split(":")[0].strip()
            try:
                if int(head) < 0:  # Telegram group / supergroup
                    return True
            except (TypeError, ValueError):
                continue
        return False
    except Exception:  # noqa: BLE001
        return True  # unknown room shape -> treat as shared (fail closed)
```

**LIVE gate** (the one that actually runs), in `_people_facts_skeleton` —
`__init__.py:285` + `308-312`:

```python
285        shared_room = _is_shared_room(cfg)
...
308                scope = str(f.get("scope") or "shared").strip().lower()
309                if scope == "dm" and (shared_room or not (
310                    lane_id in [str(x) for x in (person.get("dm_lanes") or [])]
311                )):
312                    continue
```

Semantics: a `scope: dm` fact is shown only when the lane is **not** a shared room **and**
the active lane is listed in that person's `dm_lanes`. Otherwise it is skipped
(`continue`). Default scope when absent is `shared` (documented in
`/root/HERMES/lanes/people.yaml:20-28`).

**DEAD gate** (not called), in `_people_block` — `__init__.py:511-518`:

```python
511                scope = str(f.get("scope") or "shared").strip().lower()
512                # Policy flip 2026-09-29: only withhold when explicit scope:dm
513                # AND sharing would leak to a non-private context.
514                if scope == "dm" and (shared_room or not (
515                    lane_id in [str(x) for x in (person.get("dm_lanes") or [])]
516                )):
517                    withheld += 1
518                    continue
```

Because `_people_block` has no call site, its "DAMAGE RULE" tail
(`__init__.py:548-553`) and its witness-first prose (`528-553`) are also **not injected**.
The live path injects only the terse `PEOPLE (sourced):` block from
`_people_facts_skeleton`.

---

## 5 · Three concrete hook points for a per-message name-mention router

Each point is real, with the minimal change required. (Line refs are to the live tree.)

### Hook A — `pre_gateway_dispatch` (per message, has `event.text`; cheapest)
- **Where:** `profiles/aaa-hermes/plugins/lane_switch/__init__.py:626` (`_on_pre_gateway_dispatch`).
- **Why it fits:** it already runs once per inbound message, already holds `event`
  (with `event.text`) and `source`, and already resolves the lane (`__init__.py:650`).
  Today it returns `None` and ignores the text (`__init__.py:672`).
- **Minimal change:** add a `_resolve_mentioned_people(text)` helper (build an index from
  `/root/HERMES/lanes/people.yaml` `display_name` + `identities`) and, after line `650`,
  either (a) stamp the matched person id into the runtime state
  (`state[f"mention:{chat_id}:{user_id}"] = pid`) so the later `pre_llm_call` can read it,
  or (b) return `{"action": "rewrite", "text": <prefixed resolved-mention note + text>}`
  — the gateway's rewrite path is already wired at `gateway/run_inbound.py:95-99`.
- **Cost/risk:** touches the per-message hot path; the rewrite branch only allows a single
  string rewrite and `break`s (`run_inbound.py:95-99`), so ordering vs other plugins matters.

### Hook B — `pre_llm_call` inside lane_switch (per turn, has `user_message`; smallest diff)
- **Where:** `profiles/aaa-hermes/plugins/lane_switch/__init__.py:693` (`_on_pre_llm_call`,
  which already receives `user_message` at `694`) and `_lane_card` at `__init__.py:560`.
- **Why it fits:** the card is already assembled here every turn; adding a `mentions`
  section keeps all person-context in one place.
- **Minimal change:** add a new section between §3 and §4 of `_lane_card`
  (insert after `__init__.py:609`), e.g.
  `sections.append(_mentioned_people_skeleton(user_message))`, where the helper scans
  `user_message` for `people.yaml` display_name/alias tokens present in the active lane and
  emits `MENTIONED: <display> (<pid>)`. Requires threading `user_message` into `_lane_card`
  (new kwarg) and passing it in `_on_pre_llm_call` at `__init__.py:727`.
- **Cost/risk:** grows the ≤950 B card budget; must respect the existing byte truncation
  logic (`__init__.py:356-358`).

### Hook C — a dedicated plugin on the hook bus (isolated from lane_switch)
- **Where:** a **new** plugin dir, e.g.
  `/root/.hermes/profiles/aaa-hermes/plugins/name_mention_router/__init__.py` with
  `ctx.register_hook("pre_llm_call", ...)`, modeled on `probe-first-reflex`
  (`profiles/aaa-hermes/plugins/probe-first-reflex/__init__.py:303-306`); enable it in
  `/root/.hermes/config.yaml:168-177` (`plugins.enabled`). The bus merges every plugin's
  `{"context": ...}` (`hermes_cli/plugins_dispatch.py:209-243`; merged in
  `agent/turn_context.py:784-801`).
- **Why it fits:** zero edits to `lane_switch`; the mention router can own its own
  people/alias index and its own receipts; it can also read `channel_aliases.json`
  directly. Independent fail-open (a raising hook is isolated, `plugins_dispatch.py:239-242`).
- **Minimal change:** read `people.yaml` + `channel_aliases.json`, token/regex-scan
  `user_message`, return `{"context": "<resolved mention note>"}`. Optionally also
  register an `@`-prefix provider via the documented plugin API
  (`agent/context_references.py:58-70`, `register_context_reference_provider`) so a user
  can type `@person:...`; that provider would be invoked at
  `gateway/run_inbound.py:1727` (`_expand_inbound_context_references`) — a second,
  user-explicit router surface.
- **Cost/risk:** a second context contributor on every turn; must be byte-budgeted like
  the others.

### (non-code alternates, for completeness)
- The `@`-reference expander is already a per-message resolution surface:
  `gateway/run_inbound.py:1672-1701` + `agent/context_references.py`. A plugin-prefix
  provider (Hook C variant) plugs in here without touching the gateway.
- The room prompt (`config.yaml:108-114`) already instructs the model how to read
  `[Sender|ID]` and mentions — a pure prompt edit is possible but is **not code** and
  cannot enforce a resolved identity.

---

## 6 · One-line summary of the current behaviour
Inbound Telegram message → gateway fires `pre_gateway_dispatch` (lane stamp only, no
text use) → agent built with `agent._user_id`/`_chat_id` from source → every LLM turn,
`pre_llm_call` builds a lane card whose `PEOPLE (sourced):` section is the people **present
in the lane** (`_people_facts_skeleton`, keyed on sender+room ids, `scope:dm` gated
fail-closed), injected into the user message; the room `channel_prompt` gives the model
the room register. **No code path maps a name spoken inside the message to an identity —
that mapping is left to the model.**

---
*Read-only audit. No files modified except this document.
DITEMPA BUKAN DIBERI ⚒️*
