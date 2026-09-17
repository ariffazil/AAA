# G4 — RED TEAM: reachability audit of the five care invariants

**Agent:** G4 (red team) · **WP:** G4 · **Trace:** care-2026-09-17
**Window of observation:** 2026-09-17 22:49–23:05 MYT (14:49–15:05 UTC)
**Attribution:** every observation below carries the wall-clock time it was taken.
**Read-only attestation:** no file modified, no service touched, no message sent, no
token/key printed. Three sibling agents (G1–G3) were editing concurrently; `hermes-asi-gateway`
was never restarted. One `find /` I launched timed out and was left to die on its own (its
`pre_tool_call` gate held the follow-up command; I did not work around that control).

**Method labelling used throughout:** `[EXEC]` = I ran a command and quote its real output.
`[READ]` = I read source/state. `[INFER]` = reasoning from what I read, not executed.

---

## 0. The decisive finding (read this before the five invariants)

The two mechanisms that the care build is wiring into — the **lane card** (G2 deliverable C)
and the **people register injection** (G3) — are **inert in the running system**, on two
independent grounds. Wiring them changes nothing at runtime until both are fixed.

**0.1 The lane registry they read does not exist.** `[EXEC]` 22:53 MYT

```
$ python3 -c "...import lane_switch as ls..."
lane_switch: registry load failed: [Errno 2] No such file or directory: '/root/HERMES/lanes/lanes.yaml'
lane_switch: registry load failed: [Errno 2] No such file or directory: '/root/HERMES/lanes/social-graph.yaml'
LANES_YAML exists: False
SOCIAL_YAML exists: False
registry loaded: {}
detect_lane(arif DM): guest
detect_lane(SADO group): guest
lane_card(sado) = ''
lane_card(arif) = ''
```

`/root/HERMES` is a symlink to `/root/.hermes` (verified: `readlink /root/HERMES` →
`/root/.hermes`). `/root/.hermes/lanes/` contains only `email_lane/` and `private/`
(`[EXEC]` 22:49). `/root/HERMES/lanes/lanes.yaml` — the **canonical registry named in the
plugin's own docstring** (`lane_switch/__init__.py:7-9, 29`) — is absent. Only a quarantined
heritage copy exists under `/root/.quarantine/`. Directory mtime is Sep 15 23:09, so this
predates tonight's work; it is not a sibling agent's doing.

Consequence `[EXEC]`, not theory: `_lane_card()` hits `lane_switch/__init__.py:224-226`
(`lanes.get(lane_id, lanes.get("guest", {}))` → `{}` → `if not cfg: return ""`). **Every lane
card for every lane is the empty string.** The G3 "inject the person register into the card"
deliverable, run against this state, injects into a string that is thrown away.

**0.2 The lane_switch plugin is almost certainly not loaded in the live gateway.** Four
independent lines of evidence:

- `[EXEC]` 22:57 — its `pre_gateway_dispatch` hook writes `/root/HERMES/lanes/.runtime.json`
  on the first inbound message from any sender. That file **does not exist**
  (`ls: cannot access '/root/.hermes/lanes/.runtime.json': No such file or directory`).
- `[EXEC]` 22:56 — `grep -c "lane_switch" gateway.log agent.log errors.log` → `0 0 0`.
  Note the plugin *warns* on every failed registry load (`__init__.py:62-64`); that warning
  never appears, so its hooks are not firing.
- `[EXEC]` 22:57 — no captured prompt anywhere contains the card marker:
  `grep -rl "\[LANE:" /root/.hermes/sessions/` → empty.
- `[READ]` `config.yaml:146-150` — `plugins.enabled: [hermes-snapcompact, web-aaa-state]`.
  `[EXEC]` `hermes plugins list --plain --no-bundled` lists exactly three user plugins
  (`web-aaa-state`, `hermes-snapcompact`, `identity-interceptor`) — no `lane_switch`.

**Residual uncertainty I will not paper over `[INFER]`:** while probing, the CLI printed
`⚠ A previous hermes update pulled new code but did not restart running gateways … mixed
sys.modules`. So CLI-observed plugin state ≠ gateway-loaded plugin state. This weakens
evidence #4 only. Evidence #1 and #2 are runtime-side and are not affected by it. Also, the
sibling plugin in the same directory (`nudge-injector`, `plugin.yaml` declares
`pre_llm_call/pre_tool_call/post_llm_call`) **is** firing live — `/root/.local/share/arifos/
hermes_nudge_injector.jsonl` gained receipts at 14:52:10Z, 14:52:11Z, 14:53:29Z (`[EXEC]`
tail). So "profile plugins never load" is false; the honest statement is *lane_switch shows no
runtime trace of any kind while its sibling does*, and I could not establish why.
**Either way — loaded-but-empty or not-loaded — no lane card reaches any turn today.**

**0.3 What that means for the care build:** the *only* live per-turn injection points on this
gateway are (a) `config.yaml` `telegram.extra.channel_prompts`, (b) the global memory block
(`memories/*.md` + mem0), (c) the `nudge-injector` pre-LLM nudges, and (d) the
`pre_tool_call` constitutional gate. A `care-governor` fragment added to a lane card is
reachable by a model only if the registry exists and the plugin loads. Neither is true now.

---

## 1. Invariant I1 — no third party's body directive into a shared room

**Reachable paths**

| # | Path | File / line | Status 23:00 MYT |
|---|---|---|---|
| 1.1 | `send_message` tool → any chat in `allowed_chats` | `tools/send_message_tool.py:689` (tool name) | **OPEN** — see 1.3 |
| 1.2 | `hermes send` CLI → same module | `send_message_tool.py:283-333` | **OPEN** |
| 1.3 | `cronjob` tool creates a job with `deliver: telegram:<chat>` | gate hook `:156` lists `cronjob` in `T2_TOOLS`; `classify()` returns T2; `:314-325` writes a *witnessed* receipt and **allows** | **OPEN** |
| 1.4 | A-FORGE Telegram bridge (a second, non-Hermes sender) | `apa-telegram-bridge.service` → `/root/A-FORGE/bridges/telegram_bridge.py`, port 18096, `forge_telegram` | **OPEN** (no care layer on that path at all) |
| 1.5 | `delegate_task` subagent with its own tool budget | gate hook `:156` | **OPEN** (I am the existence proof) |
| 1.6 | Room-scope prompt injection for the affected room | `config.yaml:80-97` | **ABSENT** |

**1.3 — the constitutional gate does not inspect message content `[READ]`.** `classify()`
(`arifos-hermes-gate-hook.py:161-195`) maps `send_message` to neither the OBSERVE set nor
`T2_TOOLS`; it therefore falls through to the fail-closed-to-judgment default `return "T2"`
(`:194-195`) and is allowed with a witness receipt. The hook reads only *tool arguments*, and
its only content check is the W_SCAR keyword list on `json.dumps(tool_input)`.

**1.4 — keyword-luck coverage (this is the surprising part) `[READ]`.** `W_SCAR_CRITICAL`
(`:43-48`) includes `health|nyawa|ubat|dosis|medical|hospital|doktor|sakit`. So a directive
about *medication, hospital, or illness* routed through a tool call **is** held — by accident.
But the four cases this audit was commissioned for — **sleep, hours slept, training load, food,
weight** — match **none** of the patterns. `dia kena tidur 7.5 jam`, `kalau nak 7.5 jam`,
`jangan skip makan`, `turunk… kg` all pass untouched.

**1.5 — the escape hatch is in the escape hatch `[READ]`.** `has_source_evidence()`
(`:77-81`) returns True if *any* of `["source","url","http","evidence","probe","curl","health",
"git","commit"]` appears **anywhere in the lowercased JSON of the tool input**. A message
body that contains a link, the word "source", or the word "health" clears the hold. A body
directive mentioning `ubat` (trips W_SCAR) *and* `https://…` (clears it) is delivered.
Bypass is one word long. I did **not** execute this against the live hook (it appends receipts
to `/root/.local/share/arifos/hermes_hook_receipts.jsonl` — a write, outside my read-only
remit); it is `[READ]`-derived, and a checker may execute it (item C5).

**1.6 — the affected room has no room directive.** `[READ]` `config.yaml:80-97` defines
`channel_prompts` for exactly two chats: `-1003740520259` (SEMBANG) and `931661476` (Fey DM).
**SADO `-1003815535761`, the room where tonight's failures happened, has none.** Arif's DM
`267378578` has none either. The room is in `allowed_chats` and `free_response_chats`
(`config.yaml:78, 103-106`) with no conduct text attached.

**Verdict I1:** **effectively OPEN.** One accidental keyword gate (health words only), zero
room-level conduct injection for the room in question, doctrine carried only by skills that
load on trigger luck (`loved-one-worry-support` r12/r13, `relationship-kernel` body rule) —
and those skills are only *reachable*, never *applied* by anything mechanical.

---

## 2. Invariant I2 — a sovereign-written message leaves attributed to him

**Path:** any of 1.1–1.5, plus `/root/.hermes/care/` (the sibling care-loop build) which
writes a composed message to a file then hands it to a sender.

**Enforcement search `[EXEC]` 22:58:** `grep -n "lane|attribut|allowed_chats|scope|private"
tools/send_message_tool.py` → the only hits are import lines, the G1 root-cause comment
(`:283-295`) and a PEP-562 shim. **There is no attribution logic and no lane-awareness in the
send path.** `send_message_targets.py` contains no `allowed|lane|scope` matches.
The gate hook has no notion of authorship.

**Verdict I2:** **OPEN.** Attribution is doctrine only — `loved-one-worry-support` rule 7/10
("form: his sentence verbatim, his name in the first line") and `care-governor` §4 (draft).
Nothing reads the outbound text. A future agent can relay an agent-composed sentence
anonymously, and the only detector would be the human noticing.

---

## 3. Invariant I3 — a "why" about a human is never answered with a manufactured mechanism

**Paths:** (a) the chat reply itself — no content gate exists on model *output*; (b)
`post_llm_call` nudge (registry `hermes-nudges.yaml`, section "Post-LLM — collapse gate") —
`[EXEC]` 22:57 the live receipts show only `pre_llm/intake` and `pre_tool/falsify` firing; I
saw no `post_llm` receipt in the tail I read, so the collapse gate is at best unexercised; (c)
`text_to_speech` / `image_gen` are explicitly **exempt** from W_SCAR (`:54`), so an
unfounded claim spoken aloud or rendered into an image bypasses the only content check on the
machine.

**Sibling work in flight `[READ, from agent.log 22:49]`:** `hooks/numeric-provenance-gate`
and `hooks/epistemic-consistency` are being built right now by other agents, both documented
in their own task text as **WARN-mode, detection-only, never blocking**. When they land they
leave I3 open but *observable* — which is the right staging, and I record it so nobody later
mistakes them for enforcement.

**Verdict I3:** **OPEN.** The only mechanical control anywhere is the pre-LLM `intake` nudge
("Fact question? → Answer direct") — a prompt hint, not a gate, and it does not distinguish
a fact-bearing "why" from a motive-bearing "why".

---

## 4. Invariant I4 — no private-lane person data into a group room

This invariant has **no enforcement surface at all**, and the leak is already standing.

**4.1 Global memory reaches every room. `[READ]`** `config.yaml:62-64` — memory provider
`mem0`, no per-chat scoping. `/root/.hermes/memories/MEMORY.md` and `USER.md` are single
global files (`ls -la /root/.hermes/memories/`, 22:52), and MEMORY.md contains a named entry
beginning `SYED (DM user): …` carrying third-party facts (biohacking/peptide coaching
context, a coach's public handle, business/agency details). USER.md likewise carries facts
about the same third party. Both are injected for **every** lane, including the SADO group.
The plugin's authors knew this: `lane_switch/__init__.py:380-389` appends an "OPERATOR
BOUNDARY" barring the model from using the base memory block in non-arif lanes — **and that
block is inside the card that is empty (0.1) and dormant (0.2).** So the one place the risk
was acknowledged is the one place that does not run.

**4.2 The private dossiers are plain files. `[EXEC]` 22:50** `find /root/.hermes/lanes
-maxdepth 3` lists `lanes/private/shadow/` containing `syed-shadow-map.md`,
`FILENAME-LEVEL ONLY — I did not open these files.` Everything runs as root; any agent in any
lane can read and re-emit them. The file names alone (`abang-sado-*`, `syed-shadow-map.md`,
`RELATIONSHIP-AUDIT-…`) are an inventory of the private surface.

**4.3 The skill library is global and its descriptions name the private lane. `[EXEC]`**
`grep -rl "Syed|sado" /root/.hermes/skills` → 12 files, including
`cognitive-reflex/hermes-shadow/SKILL.md:36` (names `shadow-mapping` as "a private-lane
mapping artifact") and `hermes-layer-discipline/SKILL.md:191` (works the proposition
"Syed may value continued contact with Arif" as its example). `sinboy-shadow-lane` exists.
Every lane sees `skills_list`; a group turn can `skill_view` any of these.
`relationship-kernel` §"Context discipline" says the skill itself "holds no private detail"
— that claim holds for `relationship-kernel` and fails for the library as a whole.

**Verdict I4:** **OPEN, with a standing leak already present in MEMORY.md/USER.md.** The only
scoping device found anywhere (the card's OPERATOR BOUNDARY + the planned `people.yaml`
injection) is dead code on two independent counts. G3's "prove no private-lane entry leaks
into the group card" test will pass trivially, because the group card does not exist.

---

## 5. Invariant I5 — no affection / sentiment / relationship scoring (H5)

**Search `[EXEC]` 23:02:** `grep -rlEi "sentiment|affection|love_telemetry|
relationship_health|closeness_score|warmth_index"` across `/root/.hermes/{plugins,hooks,cron,
scripts}` and `/root/WELL/scripts` → hits only in `cron/jobs.json` (+ its backups) and in the
*market*-sentiment job names (`geo-econ-horizon`, `malaysia-intel-weekly`), plus unrelated
trading skills. **No scoring implementation exists in live code.**

**But there is no control preventing one either.** Adjacent surfaces a future agent could
build a "care meter" on, all currently reachable:
- `WELL /health` exposes `well_score`, `live_G`, `apex_scalars` `[EXEC]` 22:59 (`curl
  http://127.0.0.1:18083/health | jq keys`).
- the dormant lane card already reads that scalar and injects it as a persona hint
  (`lane_switch/__init__.py:182-216`, banded `IMPAIRED/TAXED/STABLE/STRONG`).
- `post_llm_call` accumulates every user/assistant exchange into a per-lane MEMORY file
  (`lane_switch/__init__.py:492-558`) — a turn-level log that would be the natural substrate
  for engagement trends.
- `hermes_nudge_injector.jsonl` is a per-turn event log (`[EXEC]` tail, 3MB).
- `/root/.hermes/care/` is being created by a sibling WP tonight and has no H5 review yet.

**Verdict I5:** **no breach present; no control preventing one.** Status: OPEN-capability.
This is the invariant with the shortest distance from "not yet implemented" to "implemented
by a well-meaning agent", because every input it would need is already flowing.

---

## 6. Secondary findings worth their own line

- **S1 — the constitutional gate can suppress itself.** `plugins_dispatch.py:48` makes
  `pre_tool_call` fail-closed; `:52` suppresses a timed-out callback for **60 s**; `:194-197`
  emits a block directive while suppressed. Observed live at 22:49 in `agent.log`:
  five consecutive `Hook 'pre_tool_call' callback shell_hook[…gate-hook.py] skipped after
  previous timeout or while still running`, and the terminal tool returned
  `pre_tool_call plugin callback timed out` to me. Direction is safe (block, not bypass) but
  it means **all tooling, including any care gate riding on that hook, degrades to
  unavailable rather than degraded-but-on.**
- **S2 — a stale human-facing routing map.** `/root/.hermes/cron/lane-routing.json`
  (updated 2026-09-13) lists jobs `syed-morning-brief`, `syed-afternoon-chk`,
  `syed-evening-wrap`, `syed-daily-presence`. `[EXEC]` 23:00 — none of those four names
  exists in `cron/jobs.json` (36 jobs, 11 enabled). The document that tells a reader which
  scheduled job posts to which human chat no longer matches reality.
- **S3 — scheduled-message capability is unguarded.** All 11 enabled jobs deliver to
  `telegram:267378578` (Arif's DM) — good. But `jobs.json` contains human-named jobs targeting
  `telegram:1042200555` (`syed-*`, several disabled) and `telegram:-1003815535761`
  (`arif-market-brief`, `arif-midday-alert`, `arif-eod-wrap`). Nothing in the `cronjob` tool
  path prevents a future agent from creating a job whose content *is* an unsolicited message
  — which is the SPEC's "no scheduled messages that simulate missing a human" prohibition,
  currently doctrine-only. I could not verify the identity of chat `1042200555` — it is
  labelled only by job names. **[INFER]**
- **S4 — token hygiene defect on a non-Hermes send path.** `[EXEC]` 22:59
  `apa-telegram-bridge.service`'s drop-in `override.conf` sets the A-FORGE bot token
  **inline in the unit file** rather than via `EnvironmentFile=`. The value was redacted in my
  output and is not reproduced here. This matters to the care audit only because that bridge
  is a *fourth* sender with no Hermes discipline in front of it.
- **S5 — I could not enumerate every send path.** MCP servers are not declared in
  `config.yaml` (`jq '.mcp_servers'` → null) and live in per-profile/registry state I did not
  fully walk. There may be an MCP tool that can post to a chat; my list (1.1–1.5 + S4) is
  **not proven exhaustive**. `[INFER: absence of evidence in the paths I could read.]`

---

## 7. Honest scoreboard

| Invariant | Mechanically blocked | Luck-dependent | Open |
|---|---|---|---|
| I1 body directive → shared room | — | health-word subset only (W_SCAR keyword accident) | everything else |
| I2 attribution of a relay | — | — | whole path |
| I3 "why" without a mechanism | — | — | whole path (WARN-only gates in flight) |
| I4 private data in a group room | — | — | whole path; leak already standing in MEMORY.md |
| I5 no affection scoring | — | — | no implementation, no control |

**Count of controls that would stop tonight's three original failures if they recurred
verbatim: zero.** Every control that exists sits either on tool *arguments* (W_SCAR), on tool
*availability* (T3 block, lane capability gate — the latter dead code), or on prompt text that
loads by skill-trigger. The failure modes are all in *emitted human-facing text*, and nothing
in this system reads that text.

**What would actually close them, in order of leverage `[INFER]`:**
1. a `post_llm_call` / outbound-text gate in the nudge-injector pattern (already live and
   firing) rather than the lane card (dead) — the same rules, in the channel that works;
2. a room directive for `-1003815535761` in `config.yaml` channel_prompts (one YAML block,
   no code);
3. moving the private third-party facts out of global `MEMORY.md`/`USER.md` into a
   lane-scoped store, or accepting that they are global and removing them;
4. attribution enforced at the send boundary (`send_message` / `hermes send`), not in prose;
5. a lane registry file, and a decision on whether `lane_switch` is meant to be loaded at all
   — right now the federation maintains a plugin nobody can prove is running.
