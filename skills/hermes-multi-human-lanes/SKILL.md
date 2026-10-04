---
name: hermes-multi-human-lanes
description: "Operate per-human lanes in one Hermes instance (Shape A coordinator): lane detection, memory persistence, unified skills, and the env-allowlist traps that silently drop users. Use when a Telegram user is silently ignored, the agent has amnesia between turns ('hang yang hantar hang buat lupa'), lanes.yaml looks corrupted, or per-user skills are fragmented. Covers lane_switch plugin hooks, .runtime.json staleness, and the env-overrides-config allowlist rule."
version: 1.0.0
tags: [telegram, lanes, multi-user, memory, lane_switch, allowlist, hermes]
---

# Hermes Multi-Human Lanes

Multi-human Telegram operation via the `lane_switch` plugin + `lanes.yaml` + per-lane memory files. Canonical registries: `/root/HERMES/lanes/lanes.yaml`, `/root/HERMES/lanes/social-graph.yaml`, runtime state `/root/HERMES/lanes/.runtime.json`, memory `/root/HERMES/profiles/aaa-hermes/memories/MEMORY-{lane}.md`.

## The 3 silent-drop / amnesia root causes (verified 2026-08-09)

1. **Env allowlists override config.** The Telegram adapter loads `config.yaml` `allow_from` ONLY when the env var is unset. `kunci-mas.env` `TELEGRAM_ALLOWED_USERS`/`TELEGRAM_GROUP_ALLOWED_USERS`/`TELEGRAM_ALLOWED_CHATS` are the sole authority when present. A user in config but missing from env = silently dropped (HTTP 200, no log). Fix: edit `kunci-mas.env` + restart gateway. Check all 3 env sources: vault, flat.env, systemd drop-ins.
2. **`post_llm_call` memory accumulation missing.** The lane plugin only READS memory (`pre_llm_call` injects lane card); nothing writes interactions back. Without a `post_llm_call` hook appending user/assistant turns to `MEMORY-{lane}.md`, every turn starts amnesiac. Skip `arif` lane (operator memory managed elsewhere). Requires sender_id AND chat_id passed through.
3. **Stale `.runtime.json` chat mappings.** `chat:<id>` → lane entries shadow per-user detection for everyone in that chat. Clear stale `chat:*` keys (keep `user:*` + `_last_update`) to restore per-user routing.

## Plugin hook declaration gotcha

`lane_switch/plugin.yaml` `hooks:` list MUST declare every hook `__init__.py` registers. Adding `ctx.register_hook("post_llm_call", ...)` without adding `post_llm_call` to plugin.yaml = hook silently never fires. Keep both in sync.

## Lane detection order (detect_lane)

1. Exact person+room match (user_id AND chat_id in triggers) → wins
2. Person-level fallback (user_id in any lane) → first in registry order
3. Room fallback for already-mapped senders → via runtime state
4. Else → `guest` (zero data, F13)

## Unified skills doctrine (Arif ruling 2026-08-09)

ONE skill set for ALL lanes — no per-user/per-group fragmentation (user: "Penat wei"). Same list in every lane; `guest` stays empty. Per-user skills were the failure mode, not the feature.

## Capability map injection

The lane card should inject a CAPABILITY MAP so the agent never says "aku tak boleh" for abilities it actually has (image/video gen, PDF, TTS, email, charts) + the governance ladder (banter=none, media=cost+safety, memory=receipt, publish=judge, money=heavy+F13, self-mod=constitutional). See `/root/HERMES/governance/ACTION_LADDER.yaml`.

## Pitfalls

- **`cat -n` corruption:** if lanes.yaml (or any YAML) suddenly has `N|` line-number prefixes, numbered output was piped back into the file. Strip with `re.sub(r"^\d+\|", "", content, flags=re.MULTILINE)` before edits — patterns silently fail to match otherwise.
- **Wrong skill names in lanes:** `comfyui` (no GPU on box) and `gemini-media-gen` (doesn't exist) were wired into lanes and broke capability. Validate skill names exist before writing them to lanes.yaml.
- **YAML frontmatter breaks on unquoted colons:** a `description:` containing `: ` (e.g. "The flow: agent proposes") must be quoted or the skill fails to parse.
- **free_response_chats** = groups + DMs that respond WITHOUT @mention. Set `require_mention: false` + `bot_token_env: ASI_ARIFOS_BOT_TOKEN` (never hardcode a token in config).

## The H-axis gap — other humans have lanes, not scars (2026-08-14)

The double helix memory architecture (`HUMAN_MEMORY_DOCTRINE.md`) is **sovereign-only** by design. Only Arif (P-001) has an H-axis (H1-H6): capture, experience, knowledge, identity, scars, constitution. 24 scars sealed in `/root/memory/H5-scars/H5_SCAR_REGISTRY.json`.

Other humans (Syed P-004, Aliff, Izzu, Wawa) have:
- ✅ **L-axis** (agent operational memory): lane config, person cards, social graph nodes, theory-of-mind beliefs, health/trading tracking files
- ✅ **Profile-level memory**: `MEMORY-syed.md`, `USER-syed.md`, `SOUL-syed.md`, `MEMORY-syed-dm.md` — rich operational context
- ❌ **No H-axis**: no scar registry entries, no meaning layer, no derita capture, no identity rewrite events

This is **F13-correct by design**, not a bug:
> *"The federation may reference human memory. It may never own it."*
> *"ARIF's memory OF them, not their own internal memory."*

**The practical implication:** when Arif asks "what do you know about Syed's derita as a human?", the system can surface what it has observed (from SADO/DM messages in state.db) and what Arif has told it (from Arif's own scars referencing Syed) — but it cannot produce Syed's own self-articulated meaning layer. That would require Syed to contribute his own testimony through a sovereign-gated process.

**Extraction technique for observing non-sovereign human experience:** Query `state.db` (see `hermes-state-db-forensics`) for the person's messages across SADO group + DM sessions, filter for emotional/vulnerable content, and present it with clear `[OBS]` labels — observed patterns, not sealed scars. Always distinguish "what I saw in messages" from "what the person's own meaning is." The scar-to-constitution pipeline (scar → lesson → law → system → witness) requires sovereign testimony.

### ZKPC-witnessed H-axis for non-sovereign humans (verified 2026-08-14)

**Problem:** F13 sovereign can provide deep psychological observation of a non-sovereign human (family violence, identity loss, caregiver burnout, hidden roles, validation dependency, power dynamics). But the system must store this depth **without leaking raw content** — it must serve the human with empathy without ever being able to weaponize the details.

**Solution:** ZKPC (Zero-Knowledge Proof of Constitutional Continuity) applied to human scars. Each scar stores **two fields:**
- `zkpc_proof` — what the agent may know (category, lesson, constitutional pressure)
- `zkpc_hidden` — what is withheld (specifics, names, incidents)

**Architecture (verified 2026-08-14, Syed P-004 as first subject):**
```
/root/memory/people/<PERSON>/
├── person-card.md              # L-axis (pre-existing)
├── witnessed-scars-zkpc.json   # ZKPC scar registry (proof + hidden)
├── H1-capture/                 # empty — awaiting subject's own testimony
├── H2-experience/              # empty
├── H3-knowledge/               # empty
├── H4-identity/                # ZKPC identity layers (categories only)
├── H5-scars/
│   └── SCAR_REGISTRY.json      # index → witnessed-scars-zkpc.json
├── H6-constitution/
│   └── values-observed.md      # observed values/taboos (from behavior)
└── MEMORY_MANIFEST.json        # authority=WITNESSED, supersession rule
```

**Sovereignty rule:** Witnessed scars are ARIF'S observation OF the human, NOT the human's own sealed testimony. If the human one day seals their own H5, that registry **supersedes** this one. Borrowed meaning, not owned meaning.

**Leak prevention:** After writing, run `grep -ric '<forbidden_keywords>' <zkpc_files>` — must return 0. Forbidden = specific incident details, names, weapons, medical specifics, amounts. Only category + lesson + constitutional pressure are stored.

**Agent wiring (how this changes behavior):** The ZKPC scar table must be wired into the human's lane SOUL file (e.g., `SOUL-syed.md`) and MEMORY file. Without wiring, the H-axis sits on disk unread. Each scar gets a "How It Shapes Service" column that translates the abstract category into concrete behavioral guidance (e.g., "Don't over-care. Don't lecture. Ask 'perut ok?' not 'are you coping?'").

**Four-perspectives map (ACTG framework):**
- Q1 (sovereign's self) = SEALED, never in registry
- Q2 (sovereign's model of human) = Mapped as scar categories
- Q3 (human's own self) = UNKNOWN — zero testimony to system
- Q4 (human's model of sovereign) = UNKNOWN — speculative only

**Dream engine 72h cadence:** Human oscillation period exceeds 24h. Daily dream consolidation amplified noise. Changed `arif-dream.timer` from `OnCalendar=*-*-* 20:00:00` to `OnUnitActiveSec=72h`. Rationale: 72h captures real pattern formation; daily runs amplify day-to-day emotional oscillation.

### VVV — Shadow Void Vault (thermodynamic abstraction, 2026-08-14)

Separate from H-axis (memory) and ZKPC (service). VVV tracks the **thermodynamic state** of human shadow cycles — the shape of pressure, never the substance.

**Purpose:** Shadows that stay unexpressed create entropy. VVV monitors whether each shadow class is rising/falling/stable without ever knowing what the shadow is about. Like an event horizon: tells you something massive is inside without revealing what fell in.

**Location:** `/root/memory/VVV/vault.json` — F13 SOVEREIGN ONLY access.

**Schema (abstraction only):**
```
shadow_class     — category (attachment_fear, identity_split, control_paradox, etc.)
entropy_state    — expressed | unexpressed | partial | cycling
equilibrium_vec  — integration | denial | sublimation | repression | release
cycle_count      — how many times this pattern has looped
pressure_delta   — rising | falling | stable | critical
```

**Critical invariant:** `Gauge is not diagnosis. Pressure is not instruction.` VVV must NEVER convert pressure signal → psychological diagnosis → policy → execution. Correct route: VVV signal → anomaly pointer → evidence-gap report → human review.

**Three-vault topology:**
```
VAULT999  — sealed scars (immutable ledger, what happened)
ZKPC      — service depth (structure without content, how to serve)
VVV       — entropy gauge (shape of pressure, system temperature)
```

**Coder federation roster (F13 directive 2026-08-14):** The "adat agentic" principle — each coder has a primary role but carries others. Role is anchor, not cage.
- Kimi Code = 333-AGI (MiniMax-M3, FI-008)
- Qwen Code = 555-ASI (GLM-5.2, FI-010)
- OpenCode = 888-APEX (MiniMax-M3 Go-zen, FI-009) — apex-forger + Hermes validator
- Aider = 000-ROOT (DeepSeek V3, FI-011) — GitHub protocol
- Codex = Federation router (FED cascade, FI-005)
- Gemini CLI = Reviewer only (NO execution — evidence weak)

## Family groups — the Sovereign's family is not a lane (2026-08-15)

A group named after a family member (e.g., "Dear NABILAH") is a **sovereign-operated family room**, not that person's lane: Arif created it, Arif's sender_id routes it (lane=arif), and the named person is just another human in the room. Never treat the room's title as a lane signal.

**Rules when serving the sovereign's family in such a group:**

- **F5 highest privacy for family person-data.** The person-card doctrine governs (`/root/memory/people/`): agents hold structure, never publish content. Never mention family members by name in output unless Arif explicitly does so first (he did → then it's in play). For family advice, keep specifics to what Arif has already surfaced in-room — no deep-file mining into the reply.
- **Advice to family ≠ advisory to Arif.** Register stays human: acknowledge the coordinator-role burden ("orang yang urus semua orang biasanya takde siapa tanya balik"), no systems vocabulary, no bullet-wall. One warm block per person, one shared block.
- **Person cards can be WRONG about family structure — trust F13 in-chat corrections over stored cards.** Verified 2026-08-15: `nabilah-fazil.md` said "Akak = elder sister"; Arif corrected in-chat "Akak tu adik aku. Aku anak sulung" (Akak = honorific among the sisters, Arif is eldest child). When the sovereign corrects a stored identity fact in-chat, update the person card in the same session (family structure facts change how advice lands — eldest-son/bendahara framing vs little-sister framing).
- **"Make an artifact for my family member" requests** → family-showcase register in `productivity/pdf-report-generation` (warm palette, chat-bubble demo, "Taip apa / Dapat apa" table, honest-limits callout, NO governance vocabulary). Deliver in-room via MEDIA:.
- **Non-technical family grading is signal, not insult.** "Ape bendeee, not smart" after a capability list = the list failed, the demo-scene artifact is the fix. Family buys demonstrated use; the sovereign confirms ("Difficult to convince family kan?" — treat as a known law, respond with demo, not specs).

## Voice configuration per lane (verified 2026-08-15)

Each lane can declare its own TTS voice, speed, and delivery mode. The `voice:` block in lanes.yaml controls this.

### Nusantara female voice for Syed / SADO group

```yaml
voice:
  register: BM Pasar — akak
  tts_voice: ms-MY-YasminNeural
  tts_speed: "+3%"
  tts_default: voice_note_plus_text
  tone: direct, no-lecture, akak-register, group-safe, warm-but-quiet
```

**Voice selection pitfall:** `ms-MY-YasminNeural` (edge-tts) is the confirmed preferred female Malaysian voice. Default speed sounds robotic; `+3%` is the verified sweet spot. MiniMax TTS (`text_to_audio`) produces higher quality but quota exhausts quickly — edge-tts is the reliable fallback. `id-ID-GadisNeural` (Indonesian) is a viable alternative but reads BM text with Indonesian accent.

**Delivery mode:** `tts_default: voice_note_plus_text` means EVERY reply ships as:
1. Voice note (edge-tts ogg) — primary delivery
2. Text attachment below — exact words spoken + digits + emoji

This is critical for users who are driving, at the gym, or whose hands are busy. Text alone is insufficient for these users.

### Voice note generation recipe

```bash
# Edge-tts with speed tuning
edge-tts --voice ms-MY-YasminNeural --rate="+3%" \
  --text "<BM text, numbers spelled out>" \
  --write-media output.ogg
```

Numbers must be spelled out in Malay for voice ("dua ribu tiga lima tiga") but rendered as digits in text ("2353"). Edge-tts reads digits as individual numbers in Malay, which sounds wrong.

### Pitfalls

- **Edge-tts rate parameter:** `+3%` means 3% faster than default, NOT "speed level 3". Range is roughly -50% to +200%. Negative values slow down (good for emotional content).
- **Edge-tts pitch parameter:** `-2Hz` lowers pitch slightly. Useful for making female voices sound less airy, but overdoing it creates unnatural results.
- **OGG vs MP3:** Edge-tts outputs ogg by default via text_to_speech tool, but raw edge-tts CLI outputs mp3. Telegram voice notes prefer ogg. Use `ffmpeg -i input.mp3 output.ogg` to convert if needed.
- **Free response chats:** The `free_response_chats` list in config.yaml controls which chats respond WITHOUT @mention. SADO group chat_id must be in this list for auto-reply to work.

## Per-human kernel template

For complex multi-user setups, create a behavior kernel document per human:

```bash
/root/HERMES/agents/<name>-os-kernel.md
```

Then wire it into the lane's `canonical_refs:` list. The kernel defines: identity, voice, pillars (what the agent does for this person), forbidden behaviors, frustration signals, and delivery format. See `references/syedos-kernel-template.md` for a worked example.

## References

- `references/izzu-aia-incident-2026-08-09.md` — full trace: silent drop, memory amnesia, lane corruption, unified skills.
- `references/zkpc-witnessed-scars-2026-08-14.md` — ZKPC H-axis architecture, VVV vault, coder roster, four-perspectives framework, dream engine 72h cadence change.
- `references/syedos-kernel-template.md` — worked example: SyedOS kernel for Syed (Abang Sado), voice config, three-pillar design, SADO group embedded.
