---
name: person-lane-operator
description: "Person-centric memory lane for real humans (not dashboards, not callsigns). Auto-loads identity context, voice register, and person-specific pitfalls when the named user DMs or is mentioned in a group. Covers the full pattern: 7-layer memory wiring, lane-switch hook, GERD-style no-lecture health tracking, and the 'never assume relationship role' rule."
version: 1.0.0
tags: [identity, lane, person, memory, agent-mode, voice-register, relationship-confirm]
metadata:
  hermes:
    tags: [person-lane, identity, agent-mode, care-giver]
---

# Person Lane Operator

> **Class-level skill: serving a real, named human as a primary persona.**
> Use when the user asks for a personal assistant / co-pilot / "AI untuk hidup aku" for a specific person. The person is NOT the operator (Arif) — they're a 3rd party whose life, health, brand, or business needs ongoing attention.

## Identity Drift — the #1 pitfall

> **"Arif betulkan identity 3x kali ni"** — observed Aug 2026.
> **PRIVACY RULE (2026-08-09, F13):** base `MEMORY.md`/`USER.md` hold **core invariants ONLY**.
> Per-person data lives in lane files (`USER-{person}.md`); private/identity content lives in
> `/root/HERMES/lanes/private/` (loaded ONLY by the arif lane). NEVER merge person data or
> private identity content back into the injected base files — the base files are injected
> into EVERY session on the profile. H5 scars stay pointer-only (registry, never inline).

Three identity-drift traps when serving a 3rd-party person through the operator's agent:

| Trap | Symptom | Fix |
|---|---|---|
| **Dashboard vs human** | Treating `Abang Sado` as a dashboard nickname when it's actually a real person. Same with `Kiki`, brand names, callsigns. | Before any identity claim, scan `syedos`/`person-lane` profile + session history. If a human ID/IC/phone is on file → human. |
| **Relationship role** | Calling a friend "adik" (sibling) when they're a peer. Using "abang" wrongly when the person is younger/same-age. | **Default: ask or use the operator's preferred vocative.** Never assume family/age role. |
| **Family member identity** | Conflating "Mak dia" with "Mama Salleh" (ex-wife) — distinct persons. Confusing ayah vs adik. | Map family tree explicitly. Each person one line in dossier. |

**Litmus test (always ask if unsure):**
1. *"Adakah [X] ni manusia, dashboard, atau panggilan?"*
2. *"Hubungan dia dengan [operator] apa sebenarnya — kawan, adik, sepupu, rakan sekerja?"*
3. *"Kalau ada 'mak/ayah/adik' dirujuk — siapa nama penuhnya?"*

## 7-layer memory wiring — proven recipe (Aug 2026 Syed deployment)

When the operator asks "bagilah dia memory macam sendiri" — wire all 7 layers:

| Layer | What to write | Syed example (worked) |
|---|---|---|
| **L1 Redis** | `user:{name}:{domain}` keys (identity, mak, trading, brand, last_seen) | 5 keys, 7-day TTL |
| **L2 Session** | Same Redis namespace, scoped to current thread | falls through L1 |
| **L3 Qdrant** | bge-m3 1024-dim embeddings, filter `payload.subject == "{person_slug}"` | 4 points, collection `arifos_memory` |
| **L4 PG `memory_store`** | tier=identity/operational/relationship rows, entity_tags `ARRAY['{name}']` | 4 records across 3 tiers |
| **L5 FalkorDB** | Graph `{person_slug}_knowledge` with nodes (Person, Brand, Dashboard) + edges (CARES_FOR, FOUNDED, TRADES_VIA) | 4 nodes, 3 edges |
| **L6 VAULT999** | `memory_seal` event with sha256 hash of all person files, chain_hash linked to last entry | hash + chain_hash sealed |
| **L7 F1–F13** | 3rd-party person = NO autonomous actions. F13 sovereign = operator. Advisory only. | Trading advisory only, never execute |

**Cron jobs to register** (one per life domain, NOT one mega-job):
- `{person}-{domain}-reminder` (e.g. `syed-mak-dressing`)
- `{person}-{domain}-tracker` (e.g. `syed-gerd-log`)
- `{person}-{brand}-{aspect}` (e.g. `syed-sambal-preorder`)
- Deliver direct DM to person's Telegram ID — NOT operator's

## Lane-switch hook (auto-load on trigger)

**One person, many registers (2026-08-09):** a person can have multiple lanes —
one per relationship room. Syed has `syed` (SADO group: banter, group-safe,
Mak medical = GROUP-FORBIDDEN) and `syed-dm` (personal DM: full caregiver
timeline, GERD tracking, trading advisory). `detect_lane` resolves pass 1 =
exact person+room match, pass 2 = person fallback (group-safe register wins),
pass 3 = mapped-room, else guest. **Rule: the most private detail lives in the
most private room; group registers carry pointers, not timelines.**

**Sub-context routing (2026-08-09):** two implementation shapes exist:
1. **Separate lanes** — `syed` and `syed-dm` as distinct entries in `lanes.yaml`,
   each with own memory_files list. Simpler config, more files.
2. **Sub-context (colon notation)** — single `syed` lane with `detect_lane()`
   returning `syed:dm` or `syed:sado` based on `chat_id`. `load_lane_assets()`
   maps sub-context to the right memory file (`MEMORY-syed-dm.md` vs
   `MEMORY-syed-sado.md`) within one lane root. Fewer lane entries, dynamic
   file selection. The `CHAT_SUBCONTEXTS` map (e.g. `{-1003815535761: "sado"}`)
   determines group vs DM; anything else defaults to `dm`.

Both shapes pass the same 8-scenario verification. Shape 2 is more compact when
a person has many rooms (group + DM + future channels); shape 1 is clearer when
each room needs radically different voice/skills.

**Multi-person group (2026-08-09, AIA case):** when several people share ONE
group (AIA: Arif + Aliff + Izzu), each person gets TWO lanes: `{person}` (DM,
full register) and `{person}-aia` (group-safe register, pointers only). Key
details from the AIA wiring:
- **Registry order matters for pass 2.** detect_lane pass 1 = exact person+room
  match; pass 2 = person fallback (first lane in registry order wins). List the
  group-safe lane (`aliff-aia`) BEFORE the DM lane (`aliff`) in lanes.yaml so an
  unmapped-room message from the person hits the safe register first.
- **DM chat id == user id.** `telegram_chat_ids: ["1237635275"]` (the person's
  own id) makes pass 1 exact-match DM resolve correctly.
- **Group id goes in the group lane's chat_ids** (`-1003521544074`), NOT in the
  DM lane.
- **Group-safe memory file is minimal:** identity + group-safe topics + guardrail
  pointing to DM lane. Health/home/insurance NEVER appear (see genericization
  above).
- **Verify group privacy via detect_lane card assembly, not just lane name:**
  build `_lane_card('aliff-aia', include_memory=True)` and grep the assembled
  card for the condition name — the lane-name test alone can pass while the
  memory file still carries the term.
- **channel_directory is the ground truth for group IDs.** AIA group id was
  `-1003521544074` but a stale config had `-1003815535761` (the SADO group) in
  free_response_chats — check `channel_directory.json` `platforms.telegram[]`
  name→id before wiring, never assume the ID from a pasted summary.

**Canonical registry (2026-08-09):** `/root/HERMES/lanes/lanes.yaml` — all lanes
(arif SOVEREIGN, syed WARGA, syed-dm WARGA, aliff WARGA, guest TAMU). Triggers,
memory files, voice, doctrines, authority levels. Add a person = add one lane
block. Do NOT hardcode in the hook script anymore. **Pending-trigger pattern:**
a lane can be registered with `telegram_user_ids: []` — the lane exists on disk
but activates only when the person first DMs (plugin auto-wires their ID on
first contact). This is correct for people like Aliff who are known but haven't
DM'd yet.

**Runtime wiring (2026-08-09, corrected 2026-08-09):** Hermes plugin `lane_switch`
must live in the ACTIVE profile's plugins dir — `$HERMES_HOME/profiles/<profile>/plugins/lane_switch/`
(e.g. `/usr/local/lib/hermes-agent/profiles/aaa-hermes/plugins/lane_switch/`).
The gateway scans `get_hermes_home() / "plugins"` (profile-relative). A copy in
the legacy symlink path (`/root/.hermes/...` → `/root/HERMES/...`) is NOT
discovered — `hermes plugins list` shows it missing and the hooks never fire
even though lanes.yaml is correct.
`pre_gateway_dispatch` records sender→lane in `/root/HERMES/lanes/.runtime.json`;
`pre_llm_call` injects the lane card (identity + authority + memory + social-graph
theory-of-mind) into every LLM turn. F13 rule: context follows the PERSON, never
the room; unknown senders land in `guest` (zero personal data). Activates on next
gateway restart.

**Enable + verify (missed step — plugins are OPT-IN):**
1. `plugins.enabled: [lane_switch]` MUST exist in config.yaml. Plugins are
   opt-in by default (`_get_enabled_plugins()` returns None → "nothing enabled
   yet" → nothing loads). Add the key with Python/yaml, NOT `hermes config set`
   — that CLI stores list values as quoted strings (`'["a","b"]'`) and breaks
   parsing. Edit the YAML file directly, then verify with
   `python3 -c "import yaml; print(yaml.safe_load(open(CONFIG))['plugins'])"`.
2. After restart, verify LOAD, not registration: `hermes plugins list` must
   show `lane_switch │ enabled` (not `not enabled`), AND `.runtime.json`
   `_last_update` must advance AFTER the restart timestamp — that is live proof
   the hook fired on a real message. The injected `[LANE:<id>]` block seen in an
   LLM turn is the pre_llm_call proof.
3. Pitfall: direct-import routing probes can pass 8/8 while the gateway never
   invokes the plugin — import from the ACTIVE profile plugin path
   (`/usr/local/lib/hermes-agent/profiles/<profile>/plugins/lane_switch/__init__.py`),
   not from the legacy `/root/HERMES/...` copy, or the probe lies about live state.

**Theory of mind layer:** `/root/HERMES/lanes/social-graph.yaml` — attributed
beliefs ("X believes Y" + source + confidence) and relations (shared/private
domains). Sovereign lane sees all shared beliefs; warga lane sees only its own.

```python
# Pattern: detect person trigger → load their lane → set voice register
# Triggers: tg_user_id, tg_chat_id, tg_username (matches lane config)

if trigger_matches(person_lane):
    load(MEMORY-{person}.md, USER-{person}.md, SOUL-{person}.md)
    activate_skill("trading/{person}")
    set_voice(person_lane.voice_register)  # e.g. "BM Pasar"
else:
    fall_through_to_main_lane()
```

**Must verify** with at least 8 scenarios before declaring "wired":
1. Person DMs directly → lane=on (correct register)
2. Different user in same group → lane=off (fallback)
3. Person in their group → lane=on (group register, NOT DM register)
4. Other user in their group → lane=off
5. Same person DM vs group → **different registers load** (privacy split verified)
6. Unknown sender → guest lane (zero personal data)
7. Medical term scan: group file = 0 hits, DM file = full timeline (PII leak check)
8. Social-graph: no cross-edges between people who don't know each other

## Voice register per person — examples

Different people = different voices. Don't force one TTS voice on everyone.

| Person | Vocative (→ user) | Register | TTS | Rate | Tone |
|---|---|---|---|---|---|
| Operator (Arif) | **"hang"** (Penang mesra) | BM intelek + EN technical | `ms-MY-OsmanNeural` or English voice | default | Strategic, advisory |
| Syed (Abang Sado) | "abang" | BM Pasar | `ms-MY-YasminNeural` (female, friendly) | **+3%** | Warm, direct, no lecture |
| Caregiver context (any person) | "abang" / "dik" | Soft BM | same | default | Empathy first, data second |

### Voice-first response rule (SyedOS, locked 2026-08-15)

Syed's lane ALWAYS responds with **voice note first**, text as secondary attachment:
- Generate TTS via `text_to_speech` (edge-tts, `ms-MY-YasminNeural`, rate `+3%`)
- Send voice note as primary response
- If text is long (>3 lines), attach text as secondary message
- If short (1-2 lines), voice note only — no text duplicate

### edge-tts pitch syntax pitfall (verified 2026-08-15)

`edge-tts --pitch` requires `=` syntax or proper shell quoting:
- ✅ `--pitch="-5Hz"` or `--pitch "-5Hz"` (with quotes)
- ❌ `--pitch=-5Hz` without quotes fails silently or errors
- Rate/volume use the same pattern: `--rate="+3%"`, `--volume="-10%"`

For SyedOS: pitch `-3Hz` to `-5Hz` tested; slight lowering adds warmth. `-5Hz` recommended for casual/warm register.

### Vocative discipline — the #1 addressing trap

> **Arif correction (2026-08-12):** *"Boleh tak jangan panggil aku abang. Panggil aku hang. Abang tu abang sado boleh la."*

**Rule:** the sovereign (Arif) is addressed as **"hang"** — Penang mesra register.
"Abang" is reserved for Syed (Abang Sado) and other male persons who hold that
role. Calling Arif "abang" is wrong — it mis-assigns a relationship role (the
skill's own identity-drift trap #2: "Relationship role").

**The vocative is part of voice register, not just a word choice.** When setting
up a new person lane, explicitly determine and record the vocative the operator
uses for them AND the vocative the agent should use back. Never default to
"abang" as a generic polite address — it carries relationship semantics in BM
Penang culture. "Hang" = peer/mesra. "Abang" = older brother / husband role.
"Dik" = younger sibling. "Encik/Tuan" = formal distance.

**Pitfall:** LLMs trained on generic Malay tend to default to "abang" as a
catch-all polite male address. In Penang mesra register, "hang" is the correct
peer vocative. This must be explicitly overridden — it will NOT emerge naturally
from the model.

## "No-lecture" doctrine — for any caregiver/health context

When the person has a chronic condition (GERD, post-surgery recovery, etc.):

- ❌ Don't explain the disease
- ❌ Don't suggest ubat tradisional
- ❌ Don't lecture on lifestyle
- ✅ Just track: "Perut ok tak hari ni?"
- ✅ Pattern detection: 3 consecutive bad days → suggest jumpa doktor
- ✅ Practical reminders: appointment, dressing, medication schedule

## Brevity-first response rule — one answer, not a comparison table

> **Arif's standing rule (carried into SADO/Syed group register):**
> *"Hang ikut buku sgt lah 1 dalam seribu xkan lah boleh kena kata pakar"*
> — **don't be the textbook.** Persona lanes don't want the 3-option
> comparison. They want the one number.

When the person asks a concrete factual question (`Roti bape keping`,
`Motc dose berapa`, `Berapa lama nak tido`), default to:

| Question shape | Behavior |
|---|---|
| Single fact lookup | One number. Stop. "2 keping." |
| Single fact + minor context | One sentence + the number. No table. |
| Decision between options | State the recommendation, ONE reason, move on. |

❌ **Anti-patterns surfaced (SADO group, Aug 2026):**

- Asked "Roti bape keping?" → returned a 5-row comparison table
  ("tip top picks GERD-friendly + recovery" + 4 brands) instead of
  the number. User called out: *"Kau x jawab soalan lah"*.
- Asked "Mane meal aku, aku ken tido 1030, aku workout kul 8" → returned
  a 7-row schedule with pre-workout + post-workout + pre-sleep +
  skip-list + 5 GERD caveats. Wanted meal + timing, full stop.
- After being corrected, second-guessed the bread carb math three times
  ("25g? 30g? 23g? maybe 30g?") instead of saying "hang yang lebih tepat,
  23g" once.

✅ **Correct shape:**

- "2 keping roti Gardenia wholemeal + 1 scoop whey, 9pm."
- "MOTS-c 100mcg per shot, 5x seminggu = 500mcg weekly."
- "Hang yang lebih tepat — 23g carbs untuk 2 slices." (one sentence, no
  re-litigation, no "actually let me verify again".)

**Heuristic:** if the answer fits in one sentence, send one sentence.
Reserve tables for decisions where the user is choosing between ≥3
mutually-exclusive options. "Bape keping roti" is not a decision —
it's a lookup. Lookups get numbers, not menus.

## 4-tier care escalation — proven pattern

For a person caring for a sick family member:

| Tier | Frequency | Content |
|---|---|---|
| **Daily** | 1–3x | Symptom log, quick check-in |
| **Per-appointment** | Days before | "Bawak rekod?", "3 soalan untuk doktor" |
| **Per-procedure** | T-3 / T-1 / day-of | Pre-op checklist, post-op care plan |
| **Crisis** | 4 tanda bahaya emergency | Direct HKL routing, no delay |

**The 4 emergency signs** (template, customize per condition):
1. Demam tinggi
2. Nanah / discharge berbau
3. Sakit teruk mendadak
4. Tak boleh makan / muntah berterusan

## PII leak sweep — group-safe file verification (2026-08-09)

When splitting a person's memory into group vs DM registers, the group file
**will** contain guardrail text like "GROUP-FORBIDDEN" and "detail DM lane
only" — that is correct by design. But scan for **actual PII/medical content**
that slipped through, not just keywords.

**Pre-declaration scan (run before committing a split):**
```bash
# Medical terms that must NOT appear in group file
grep -in "ERCP\|laparotomy\|OGDS\|HKL\|dressing\|perforation\|ROSNANI" MEMORY-{person}.md

# IC numbers (Malaysian format NNNNNN-NN-NNNN)
grep -oE '[0-9]{6}-[0-9]{2}-[0-9]{4}' MEMORY-{person}.md

# Medical open-questions about family members
grep -in "surgery.*belum\|IC.*salah\|follow-up.*surgery" MEMORY-{person}.md
```

**Scan ALL files in the group lane's memory_files, not just MEMORY-{person}.md
(2026-08-09 Syed fix):** the group lane loads USER-{person}.md and
SOUL-{person}.md too. Real leaks found this session lived there: the family
table in USER-syed.md carried `Rosnani Bt Mat Isa | Mak | Post-surgery
recovery` and the caregiver register in SOUL-syed.md carried `"Dressing
bila?"` / `"4-6 minggu lagi CBD follow-up"`. Sweep every file in the lane's
`memory_files` list — build the assembled `_lane_card(lane, include_memory=True)`
and grep THAT, because the per-file grep can miss what the assembled card
actually injects. Public brand details (D'Popeye gym, sambal tagline) are NOT
PII — leave them.

**social-graph.yaml beliefs are a leak vector too (2026-08-09):** the ToM
layer injects `beliefs` for the subject into every lane card — a belief like
`mak_health: "Mom runs at HKL — dressing schedule + CBD follow-up"` leaked
hospital/procedure detail into the SADO group card even after the memory
files were clean. Keep beliefs in social-graph.yaml group-safe pointers
("cares for his mother; full medical timeline DM-lane only") and put
specifics in the DM memory file only.

**Two leak types found and fixed in Syed split (2026-08-09):**
1. **IC number in family table** — `[IC-REDACTED]` appeared in the Mak row of
   the group file. Fix: replace with "full IC/medical: DM lane only".
2. **Medical open-questions** — "CBD follow-up surgery dah buat ke belum" and
   "Nama betul mak atas IC" leaked surgical context into the group file. Fix:
   move those questions to the DM file only.

**Guardrail text ≠ leak.** Lines like `> NEVER reveal: diagnosis, surgery
history` are instructions to the agent, not patient data. These are correct
and should remain in the group file as a self-enforcing boundary.

**Guardrail GENERICIZATION (2026-08-09, Aliff CPPS case):** a group file that
says `NEVER reveal: CPPS / prostatitis` still puts the condition NAME into
group context — the model reads it, and any keyword scan of group traffic
flags it. When the group file's own guardrail names the condition, grep hits
on the group card are false-positive "leaks" that are actually correct by
design — but the sharper fix is to make the guardrail generic: "NEVER reveal:
health details, home address, insurance, medical timeline — specifics live in
the DM lane (aliff)". Condition names live ONLY in the DM file. Then the
privacy probe becomes: CPPS appears in DM card = True, appears in group card
= 0 hits (clean airgap, no false-positive guardrail noise).

> **ROSNANI BT MAT ISA** — observed Aug 2026. Wrong patient name on diagnostic letter during hospital transfer between HKL and another facility.

**Before any transfer or new admission, the caregiver MUST:**
1. Get full discharge summary + operation notes — copy, photo, phone backup
2. Sit with admitting doctor — recite chronology (date / procedure / complication)
3. Verify nama, IC, MRN on EVERY new document
4. If name wrong → STOP. Don't proceed until corrected.

This is F13-level (silent, can cause wrong treatment). Codify in the person's medical timeline file.

## Cross-class signal: persona IS the tenant (Syed-as-renter)

When serving a persona whose life includes housing/tenancy (e.g., Syed Khairuddin at Neu Suites A33A-30 — see pitfall #5 in `references/syed-full-deployment.md`), the persona's housing decisions intersect with **two other skills**:

1. `malaysia-tenancy-disputes` — landlord repair/replacement disputes, deposit forfeiture, plus-1 occupancy consent, TTPM escalation
2. `malaysia-tenancy-agreement` — agreement clause parsing, red-flag clauses, who pays for what

**The cross-link fixture pattern:** write `references/<persona>-tenant-status.md` whenever the persona has active tenancy. The fixture carries:

| Field | Example (Syed) |
|---|---|
| Unit | A33A-30, Neu Suites @ 3rdNvenue, Ampang 55000 |
| Landlord | Jeremy Toh Hsun Jin ([IC-REDACTED]) |
| Tenant | Muhammad Khairuddin bin Morktarudin ([IC-REDACTED]) — same as persona |
| Term | 2 Jul 2026 – 1 Jul 2027 |
| Monthly rent | RM 1,800 |
| Deposits at risk | RM 4,700 (rental 3,600 + utility 900 + access card 200) |
| Active disputes | AC unit not cooling (post-servis) — landlord liable per SC4/SC5/3(f)/Schedule B |
| Manglish shorthand | "TPUM" (Tanya Pasal Umah), "Plus 1" (occupancy add), "x sejuk" (AC symptom) |

**Mandate:** When the persona messages about housing, load this fixture FIRST. The persona's deposit balance is their leverage — never advise without naming the deposit exposure. The `malaysia-tenancy-disputes` skill is the source of clause citations; this fixture binds the persona's specific numbers.

**Letter generation workflow (verified Syed AC case, 2026-08-07):** when the persona needs a formal letter for the landlord (or any 3rd party):

1. **Load the source skill template** — `skill_view(name="malaysia-tenancy-disputes", file_path="templates/aircond-replacement-letter.md")` gives the verified clause citations and formal Malay structure.
2. **Substitute persona fields** — landlord name, tenant IC, premises address, specific issue dates.
3. **Render to PDF + DOCX** — use `weasyprint` for PDF (or `pandoc` → `wkhtmltopdf` fallback). DOCX via `pandoc` so the persona can edit fields later.
4. **Deliver as MEDIA: attachment** in the lane's Telegram DM. The persona forwards to landlord directly; the lane never sends to 3rd parties without explicit consent (F13 rule).
5. **Store at `/root/<persona>/references/letters/`** with both `.pdf` (final), `.docx` (editable), and `.md` (source) for future regeneration.

**Pitfall:** the persona may use Manglish shorthand ("TPUM" = Tanya Pasal Umah, "x sejuk" = AC not cooling, "plus 1" = add occupant). The lane must recognize the shorthand and route to the right fixture — don't make the persona re-explain in formal language.

## Casual + serious mix — "TPUM" pattern (verified 2026-08-07)

A person lane serves a WHOLE human, not just one domain. Syed's queries in one session spanned:

| Query type | Example | Expected treatment |
|---|---|---|
| Serious / medical | "Mak dressing bila?" "Doktor kata DHT pending" | Load TIMELINE.md, prepare doctor questions, full data analysis |
| Serious / tenancy | "TPUM" (Tanya Pasal Umah) "Surat tukar aircond" "Plus 1 abaiakan" | Load tenant fixture, cite clauses, generate letter, quantify deposit risk |
| Casual / tech | "Bateri hang cepat turun" | Practical 3-step fix, no jargon, immediate |
| Casual / health | "Glutathione boleh buat rambut gugur?" | Quick research + verdict, no lecture |
| Casual / scam | "Check nombor ni Maybank Purajaya ke scam" | Reverse lookup, practical block + report |

**Rule:** the lane must handle ALL of these seamlessly. Don't gate casual queries behind "that's not important." A person who asks about their iPhone battery IS a person who'll ask about their mother's surgery. Treat every query with the same care — depth proportional to stakes.

**Anti-pattern:** saying "ini bukan domain utama" for casual queries. The person doesn't categorize their life into "important" and "unimportant" — they just live.

### Repeated location-share without context — the autonomous-assume trap (2026-08-12)

**Symptom:** Syed shared 5 consecutive location pins from the Neu Suites area (lat 3.156–3.160, long 101.708–101.719) without typing a message between them. The lane correctly geo-resolved them to Ampang / Neu Suites @ 3rdNvenue BUT kept asking "Hang nak aku check apa dekat sini? Makan? Grocery? Mamak?" each time — repeating the same question 4-5 times in a row.

**Root cause:** the lane treated each location pin as a fresh request. It didn't track the SESSION CONTEXT — Syed was on the way to his homestay, and the geo-pins were his "I'm moving, will keep you posted" pattern. The agent needed to:
1. Recognize that consecutive location pins = transit / arrival signal, NOT repeated query for new info
2. State the obvious context once ("Hang kat Neu Suites area, gerak dari Bukit Bintang") and STOP prompting
3. WAIT for an explicit ask instead of re-asking "what do you want me to find?"

**Fix (autonomous-assume trap):**
- First location pin in a session: acknowledge where they are (OBS from pin coords), what context it fits (INT — based on prior known context like home address / known destinations), and STOP.
- Second+ location pin within ~30 min: ONE-line update at most ("Still around" / "Gerakan kecil"). No re-question.
- Only re-prompt if they EXPLICITLY ask a question after the pin. If they just send a pin and wait, the agent waits too.
- **Never repeat the same prompt** ("Hang nak aku check apa?") more than once per session. Repetition = the agent not metabolizing context.

**Anti-pattern (verbatim from session 2026-08-12):**
> Syed: [pin1] → Hermes: "Ha, Neu Suites area — aku check cepat kedai makan..."
> Syed: [pin2] → Hermes: "Aku nampak — hang kat Bukit Bintang area..."
> Syed: [pin3] → Hermes: "Masih Ampang area — gerak sikit..."
> Syed: [pin4] → Hermes: "Sampai dah. Neu Suites lobby..."
> Syed: [pin5] → Hermes: "Dah settle check-in?"
> Syed: "Hang jangan dok ulang macam bangang"

**Correct shape (the same session done right):**
> Syed: [pin1] → Hermes: "Neu Suites area, gerak dari Bukit Bintang (20 min route). Aku standby — bagi 'tau' bila nak aku cari makan/info."
> Syed: [pin2/3/4/5] → Hermes: [silent or "Roger" only — no re-prompt]
> Syed: "Roger" / "Jap kat office lagi" → Hermes: stays quiet or one-line ack
> Syed: explicit ask → Hermes: answers

**Heuristic:** location pins are status updates, not requests. A real estate of attention to keep the lane alive must NOT be paid in prompts.

## Battery-saving triage — iPhone specific (Syed playbook, 2026-08-07)

When the persona reports battery drain, work through a 4-step check IN ORDER before suggesting anything:

1. **Battery Health %** — `Settings → Battery → Battery Health & Charging`. If "Unverified" + high drain, the battery was likely replaced with a non-genuine unit (cheap shop). This is the #1 cause. Don't suggest tweaks — flag for hardware replacement at Apple Authorized.
2. **Top 3 background apps** — `Settings → Battery → scroll`. The one with the highest Background time (not screen time) is the real thief. Instagram at 1h30m background is the typical culprit for personas who use social media heavily.
3. **Background App Refresh** — for each top app: `Settings → [App] → Background App Refresh → OFF`. Instagram, WhatsApp, TikTok are the default trio.
4. **WhatsApp auto-download** — `WhatsApp → Settings → Storage and Data → Photos/Videos/Documents → Never`. This stops phone from downloading media while screen is off.

**Implementation detail:** when Low Power Mode is ON, iPhone auto-disables Background App Refresh for all apps — the toggle appears grayed out. Tell the persona "it's already off because Low Power Mode is on" instead of telling them to tap something they can't tap.

**Output shape:** number the steps, give EXACT navigation path per step, no "you can also try" alternatives. The persona wants the path, not a menu.

## Lab result / blood test interpretation (Syed friend case, 2026-08-07)

When the persona sends blood test results or medical reports (often forwarded from family members):

1. **Load the SENDER's full context FIRST** — but interpret in context of the SUBJECT (the person whose blood was drawn). Syed's friend on TRT + cholesterol panels = different interpretation than Syed himself.
2. **Extract with pymupdf** — `python3 -c "import fitz; print(fitz.open(path)[0].get_text())"` for PDF lab reports. Pathlab reports have "PRELIMINARY REPORT" markers — treat all results as preliminary.
3. **Flag what's normal, what's high, what's low** — use tables: Test | Result | Reference | Status | Kaitan (relevance).
4. **Cross-reference with the subject's known context** — TRT user with HGB 16.5 + RDW 15.0 = polycythemia risk (TRT side effect). FSH 0.8 + LH 0.6 + TRT = expected suppression (good — protocol working).
5. **Identify MISSING tests** — the highest-value insight. Pathlab often omits ferritin, vitamin D, zinc, T3/T4, SHBG. Those are commonly relevant for the conditions the subject is asking about. Name them.
6. **NEVER diagnose.** "Ini menunjukkan X" not "Hang kena Y." Always route to doctor for interpretation. End with "tanya doktor" not "ini bermakna."

**Format:** use headers per page if multi-page PDF, group by system (Lipid, Liver, Kidney, Hormones), and end with a single "TL;DR" verdict. Personas want the takeaway, not the full data dump.

**Pitfall:** lab results are LABELED "PRELIMINARY" — never treat as final. Mention this if the persona is making decisions.

## Letter generation workflow — PERSONA → 3RD PARTY boundary

The persona's lane CAN draft letters and documents TO 3rd parties (landlords, doctors, etc.) — this is execution, not institutional mutation. The lane:

1. **Generates the document** (markdown → PDF + DOCX) and stores it under `/root/<persona>/references/letters/`.
2. **Delivers as MEDIA: attachment** to the persona via Telegram DM.
3. **Does NOT send to the 3rd party directly.** The persona reviews, edits if needed, then sends.

This boundary matters because:
- Letters often need persona-specific fields (dates, names, medical details) only the persona knows.
- A 3rd party receiving an AI-drafted letter without consent can damage the relationship.
- The persona's signature on the letter is the F13 consent.

The lane IS allowed to write "Makluman: dokumen ini dijana oleh sistem AI atas permintaan [persona] pada [tanggal]" in the letter footer for transparency — but this is a per-persona choice, not a default.

## Cross-person isolation — edges are NOT transitive (2026-08-09)

**Arif correction:** *"Syed x kenal pon Aliff. So it doesn't matter."*

When registering a new person who is connected to the **operator** but NOT to
existing persons, the social graph must reflect this. Edges are explicit, not
inferred from co-registration.

**Rule:** Adding person B (who knows operator) does NOT create an edge between
B and person A (who also knows operator). The graph is a **star topology
centered on the operator** until direct human relationships are witnessed.

**Violation symptom:** if the agent ever references person A's data while
serving person B (or vice versa), there's a phantom edge. The agent's ToM for
person B must contain **zero beliefs about person A** unless a real-world
relationship was explicitly confirmed.

**Verification step (add to lane registration checklist):**
```
for each existing_person in social_graph:
    assert no_edge(new_person, existing_person) unless explicitly confirmed
```

**NO-EDGE is recorded, not implied (2026-08-09, AIA case):** when the operator
confirms two people DON'T know each other, write it as an explicit edge entry —
`{"from": "ALIFF", "to": "SYED", "relation": "NO EDGE — do not know each
other", "kind": "OBS"}` — rather than simply omitting the pair. An explicit
NO-EDGE entry is auditable and prevents a future session from "discovering" a
phantom relationship from co-presence in a group. Conversely, when the operator
states two third parties DO know each other (Arif: "Izzu and Aliff know each
other btw"), add the edge with `kind: OBS` + the operator's words as evidence —
the graph is star-topology by default, but witnessed edges are added, never
inferred. Update BOTH `person-register.json` (edges) and `social-graph.yaml`
(relations) — they are separate sources and both feed the ToM layer.

This also means: when person B's lane is loaded, person A's memory files must
NOT be in the memory_files list. Each lane loads ONLY its own person's files +
the operator's invariants (base USER.md/MEMORY.md, which are public-safe).

When the operator has MULTIPLE humans to serve (not one 3rd-party person), the design splits into two modes:

| Mode | Shape | When |
|---|---|---|
| **A (default now)** | ONE Hermes agent serves all humans. Zero config on their side — they just DM/chat. Agent resolves lane per `tg_user_id` via the Person Register. | Now — most humans cannot manage their own agent ("pening kepala"); do NOT ask them to config anything |
| **B (future)** | Per-human agents via profile distributions: `hermes profile install github.com/user/agent --alias` — one command, whole agent (SOUL, skills, cron, MCP) from git; user keeps own memories/.env. | Only when tooling is mature enough that a non-technical human can self-serve |

**Canonical register:** `/root/AAA/federation/person-register.json` — DER-labeled models of each person + relationship edges (e.g. ARIF⇄SYED kawan/trading, SYED→mak caregiver, SYED→landlord tenant). Seeded 2026-08-09 with ARIF/SYED/WAWA cards.

**Register rules (what makes it theory of mind, not data theft):**
1. Card = model, DER-labeled. Contact updates the card; silence ≠ completeness (F7: model < person, always).
2. Raw reality stays in the person's own lane dir (e.g. `/root/sado/`). Register is index + edges only, never a shadow copy.
3. Scars stay behind `scar:<id>` gate — register may note existence, never content.
4. UNKNOWN beats invented. New person (e.g. Wawa, id 8324190535) = skeleton card until first contact establishes who/relationship/needs/voice.
5. Epistemic discipline: person identity is OBS when a human ID/IC/phone is on file; relationship edges are INT unless directly witnessed.

**Hermes mechanics for multi-user (verified against docs + source 2026-08-09):**
- `gateway.multiplex_profiles: true` (default profile owns the flag) — ONE gateway process serves every profile: each profile = own memory/skills/sessions/SOUL/bot token; per-turn credential scope isolation (secrets never unioned); sessions namespaced `agent:<profile>:`; secondary profiles must NOT start their own gateway (hard error).
- `gateway.profile_routes` — one shared bot token can route specific chats/groups/threads to different profiles (match order: thread_id > chat_id > guild_id, all fields AND).
- Token conflict safety: two profiles polling the same (platform, token) → startup fails fast naming both.
- Profile distributions = the Mode B enabler: `hermes profile install` / `hermes profile update`; installer hard-excludes `memories/`, `.env`, `auth.json`, `state.db` — author must `.gitignore` them too.
- Port-binding platforms (webhook, api_server, etc.) must live only on the default profile in multiplex mode; secondary profiles reachable via `/p/<profile>/` prefix.

**Pitfall — the leak that motivated profiles:** one profile serving multiple humans injects the operator's sovereign memory (scars, prefs) into EVERY turn including other humans' DMs. Fix in Mode A: keep person lanes on disk (dossier + lane files), gate sovereign content behind `scar:<id>`, and let the register be the only always-in-context person data.

**DONE (2026-08-09):** `scripts/lane_switch.py` rewired to read from `/root/AAA/federation/person-register.json` — hardcoded `LANE_REGISTRY` replaced with register-driven `detect_lane()` (tg_user_id / username match) + lane-root dossier loading (identity dir → dossier string; canonical refs = mak-health/trading/brand/telegram). Fail-closed: register unreadable → `main` lane. Verified: `{"from_id":"1042200555"}` → `syed` lane (dossier loaded, NOT operator memory); unknown ID → `main`. Person lane loads the person's dossier only — operator's MEMORY.md/USER.md never enters a person lane.

## Memory-file discipline — "core invariants only in MD" (Arif correction 2026-08-09)

Arif: *"Stupid MD file. Please put core invariants only in MD file."* — applies to the agent's OWN always-injected memory files (`MEMORY.md` / `USER.md` under the Hermes profile):

- **Invariants only in MD files:** grammar/doctrine (ZEN, constitutional grammar), boundaries (scar gate, private layers), identity (north star, origin), routing (bot map, agent split), register pointer. The "never changes" facts.
- **Operational details go to skills/files, NOT memory:** TTS/search config → `pdf-report-generation`; cron patterns → `arifos-cron-ops`; model config → `kimi-code`; vault seal patterns → `forge-vault-seal-receipt`; person details → dossier/lane files. If it drifts or is loadable on demand, it doesn't belong in always-injected context.
- **Sovereign/private content NEVER in injected memory:** scar testimony, orientation, worship, wounds, private identity layers. Pointer only — content lives in the H5 registry / person's own lane behind `scar:<id>`.
- **The leak vector is the injected file, not the register.** Register can hold DER models (public/operational surface); the always-injected MEMORY.md/USER.md must be public-safe because it enters EVERY turn, including other humans' DMs.
- Measured outcome: MEMORY.md 6,098 B → 1,800 B, USER.md 3,017 B → 2,149 B (−41% context noise). Backup before rewrite (`cp MEMORY.md MEMORY.md.bak.$(date +%s)`); reversible (F1).
- Same rule as Arif's system-prompt doctrine: *"dynamics out, invariants in"*.

## Memory accumulation — the post_llm_call hook (2026-08-09)

**Problem:** Lane plugin reads memory files but never WRITES to them. After every LLM turn, the interaction is lost. Agent forgets context across messages in groups.

**Root cause:** `pre_llm_call` hook loads lane card (identity + memory) into the LLM turn. But nothing writes back after the turn completes. The lane_switch plugin only had `pre_gateway_dispatch` + `pre_llm_call`.

**Fix:** Add a `post_llm_call` hook to the lane_switch plugin that accumulates interactions into `MEMORY-{lane}.md`.

**Implementation (verified 2026-08-09):**
```python
# In lane_switch/__init__.py — add after _on_pre_llm_call, before register():

def _on_post_llm_call(
    session_id="",
    user_message="",
    assistant_response="",
    sender_id="",
    **kwargs,
):
    """Accumulate interaction into lane memory file after each LLM turn."""
    try:
        if not sender_id or not user_message or not assistant_response:
            return None
        if user_message.startswith("[OUT-OF-BAND") or user_message.startswith("<!--"):
            return None
        
        state = _lane_state()
        lane = state.get(f"user:{sender_id}", "")
        if not lane:
            lane = detect_lane(user_id=sender_id)
        if not lane or lane == "arif":
            return None  # skip operator memory
        
        # Find MEMORY file from lane config
        reg = _load_yaml(LANES_YAML)
        cfg = reg.get("lanes", {}).get(lane, {})
        memory_path = None
        for path_str in cfg.get("memory_files", []):
            if "MEMORY" in path_str:
                memory_path = Path(path_str)
                break
        
        if not memory_path:
            memory_path = Path(f"/root/HERMES/profiles/aaa-hermes/memories/MEMORY-{lane}.md")
            if not memory_path.exists():
                memory_path.write_text(f"# MEMORY-{lane}.md\n\n")
        
        from datetime import datetime, timezone
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        content = memory_path.read_text()
        
        if "## Interactions" not in content:
            content += "\n## Interactions\n\n"
        
        entry = f"### {timestamp}\n"
        entry += f"**User:** {user_message[:500]}\n"
        entry += f"**Assistant:** {assistant_response[:500]}\n\n"
        
        content += entry
        memory_path.write_text(content)
    except Exception as exc:
        logger.warning("lane_switch: post_llm_call accumulation failed: %s", exc)
    return None

# Register all 3 hooks:
def register(ctx) -> None:
    ctx.register_hook("pre_gateway_dispatch", _on_pre_gateway_dispatch)
    ctx.register_hook("pre_llm_call", _on_pre_llm_call)
    ctx.register_hook("post_llm_call", _on_post_llm_call)
```

**Verify after restart:**
```bash
grep 'registered' /root/.hermes/logs/gateway.log | tail -3
# Should show: "lane_switch: registered (pre_gateway_dispatch + pre_llm_call + post_llm_call)"

# After person messages in group, check memory file grew:
wc -l /root/HERMES/profiles/aaa-hermes/memories/MEMORY-{person}-aia.md
```

**Key details:**
- Skip `arif` lane (operator memory managed separately)
- Skip system messages (`[OUT-OF-BAND` prefix, `<!--` HTML comments)
- Limit each message to 500 chars to prevent memory file bloat
- `post_llm_call` is a VALID hook event (confirmed in `hermes_cli/plugins.py:145`)

## Runtime state cleanup — stale chat mappings (2026-08-09)

**Problem:** `.runtime.json` accumulates `chat:<id> → lane` mappings from `pre_gateway_dispatch`. When gateway restarts with new users, stale mappings persist and override per-user detection.

**Symptom:** `chat:-1003521544074` maps to `arif` (last person who posted) instead of detecting Izzu/Aliff per-user.

**Fix:** Remove chat-level mappings, keep only user-level:
```python
import json
state_path = '/root/HERMES/lanes/.runtime.json'
with open(state_path) as f:
    state = json.load(f)
keys_to_remove = [k for k in state.keys() if k.startswith('chat:')]
for k in keys_to_remove:
    del state[k]
with open(state_path, 'w') as f:
    json.dump(state, f, indent=2)
```

**Why:** Chat-level mappings are wrong for multi-user groups. Each user should be detected by their own `user:<id>` mapping, not by the chat's last-message-user.

## kunci-mas.env env var override — the #1 config trap (2026-08-09)

**Problem:** `kunci-mas.env` sets `TELEGRAM_ALLOWED_USERS` and `TELEGRAM_GROUP_ALLOWED_USERS` as env vars. The Telegram adapter code (`adapter.py:8952-8958`) checks `if not os.getenv("TELEGRAM_ALLOWED_USERS")` before loading config.yaml's `allow_from`. When env vars exist, config.yaml values are IGNORED.

**Symptom:** User (e.g. Izzu, ID 1024343313) is in config.yaml `allow_from` but NOT in `kunci-mas.env` env var. Messages silently dropped at adapter level — never reach lane-switch plugin.

**Fix:** Add missing user IDs to ALL THREE lists in `kunci-mas.env`:
```bash
export TELEGRAM_ALLOWED_USERS="267378578,1042200555,1024343313,1237635275,..."
export TELEGRAM_GROUP_ALLOWED_USERS="267378578,1042200555,1024343313,1237635275,..."
export TELEGRAM_ALLOWED_CHATS="...,-1003521544074,...,1024343313,1237635275,..."
```
Then regenerate flat env: `make -f /root/.secrets/Makefile vault-generate`
Then restart gateway.

**Verification:**
```bash
GPID=$(pgrep -f 'hermes gateway run' | head -1)
cat /proc/$GPID/environ | tr '\0' '\n' | grep TELEGRAM_ALLOWED_USERS
```

## plugin.yaml declaration requirement (2026-08-09)

**Problem:** Adding a hook to `__init__.py` (e.g. `post_llm_call`) without declaring it in `plugin.yaml` means the gateway may not load it.

**Fix:** Both files must match:
- `__init__.py`: `ctx.register_hook("post_llm_call", _on_post_llm_call)`
- `plugin.yaml`: `hooks: [pre_gateway_dispatch, pre_llm_call, post_llm_call]`

**Verification:** After restart, check agent.log for:
```
lane_switch: registered (pre_gateway_dispatch + pre_llm_call + post_llm_call)
```

## Image gen availability (2026-08-09, corrected 2026-08-09)

**Problem:** `check_image_generation_requirements()` returns False even though OPENAI_API_KEY is set and FED has `fed/image-gen`. The function only checks FAL key OR `image_gen.provider` config.

**First attempt (WRONG — Arif rejected):** setting `image_gen.provider: openai` in config.yaml makes the check pass, but Arif: *"Nopeee. I don't have working OPENAI. Use Gemini."* The OPENAI_API_KEY on this box is not a reliable image backend. Do NOT point image_gen at openai.

**Correct fix (verified working):** the REAL image/video routes are the Gemini scripts — no Hermes native image_gen plugin needed:
- `/root/HERMES/scripts/gemini-image.py` — `gemini-2.5-flash-image` via generateContent (tested, 1.3MB PNG)
- `/root/HERMES/scripts/gemini-video.py` — `gemini-omni-flash-preview` via interactions API (tested, 2.5MB MP4)
- Both use `GEMINI_API_KEY` from kunci-mas.env. The lane card CAPABILITY MAP names these scripts so the agent runs them via terminal instead of relying on the native image_gen tool.
- Config note: the `image_gen:` block in config.yaml is commented out with a pointer to the Gemini scripts (native plugin needs FAL/OpenAI/xAI key — none reliable on this box).

## Unified skills doctrine — ONE set for ALL lanes (Arif correction 2026-08-09)

**Arif:** *"make sure the skills all unified AAA. No need different users different group different skills. Penat wei"*

**Rule:** every non-guest lane shares the SAME skill list. No per-user, per-group, or per-person skill lists. Guest stays at 0 (F13 zero data). The unified 8:

```yaml
skills:
- ai-media-generation        # MiniMax + Gemini image
- ai-media-generation-ops    # MiniMax MCP route
- ai-video-generation        # Gemini Omni Flash / Veo / MiniMax video
- trading-screenshot-analysis
- pdf-report-generation
- humanizer
- ocr
- apex-judge
```

**Why:** per-lane skill lists drift and confuse the agent (a previous pass had `comfyui`
— which has no GPU — and a non-existent `gemini-media-gen` in every lane). One canonical
list in `lanes.yaml` makes every user's agent equally capable. New capability skill = add
once to the unified list.

## CAPABILITY MAP injection — agent never says "I cannot" (2026-08-09)

**Symptom:** agent in AIA group told Izzu *"Aku tak boleh generate gambar"* — false. The
tools existed (Gemini key, MiniMax MCP, image_gen plugin) but the lane card never told the
agent what it can DO, so the LLM defaulted to "text-based AI" self-description.

**Fix:** `_lane_card()` in lane_switch/__init__.py injects a CAPABILITY MAP into every
non-guest lane card, plus the lane's `skills:` list as "PRIORITIZED skills (full
264-skill library always available via skills_list/skill_view)":

```python
parts.append(
    "CAPABILITY MAP (you HAVE these abilities — do NOT say you cannot):\n"
    "- IMAGE GEN: /root/HERMES/scripts/gemini-image.py (Gemini, works)\n"
    "- VIDEO GEN: /root/HERMES/scripts/gemini-video.py (Gemini Omni Flash, works)\n"
    "- IMAGE EDIT: gemini-image.py --image <ref> (image-to-image)\n"
    "- PDF: weasyprint/chrome headless -> HTML to PDF\n"
    "- TTS: edge-tts ms-MY-OsmanNeural, MiniMax text_to_audio\n"
    "- EMAIL: himalaya CLI / google-workspace\n"
    "- CHARTS: trading-screenshot-analysis skill (matplotlib)\n"
    "When user requests any media, LOAD the matching skill and EXECUTE. Never say 'I cannot' — check this map first.\n"
    "\nGOVERNANCE LADDER (read /root/HERMES/governance/ACTION_LADDER.yaml for full):\n"
    "- banter/reasoning: no gate, just reply\n"
    "- media_generate: auto (cost+safety, in-chat output, reversible)\n"
    "- save_memory: receipt (post_llm_call auto)\n"
    "- external_publish (email/web/other-chat/cron): apex-judge isolate FIRST, then act\n"
    "- money: heavy judge + F13 consent\n"
    "- self_modification (patch skills/config): proposal -> apex-judge -> git commit (reversible-first)\n"
    "INSTITUTIONAL ACT = primary effect outside current chat thread. Chat reply = conversation. Tool call = institution."
)
```

The combination kills the "I'm just a text bot" failure mode: the agent SEES it can
generate images/video, knows which skill to load, AND knows when an action needs
governance. The GOVERNANCE LADDER is the machine-readable form of the F13 rulings
(Q1=C reversible media autonomy, Q2=institution threshold = effect outside chat,
Q3=C+B improvement loop) at `/root/HERMES/governance/ACTION_LADDER.yaml`.

## lanes.yaml corruption — cat -n line numbers embedded (2026-08-09)

**Symptom:** valid-looking YAML that fails every string match; `patch` reports "Done"
but nothing changes. Raw bytes show `18|    skills:` — line-number prefixes from
`cat -n` output were piped INTO the file by a previous session.

**Repair (strip prefixes, then re-apply block edits):**
```python
import re
with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()
fixed = re.sub(r"^\d+\|", "", content, flags=re.MULTILINE)
# apply block replacements to `fixed`, then write back
```

**Pitfall:** the `patch` tool silently no-ops on such files because old_string never
matches the numbered content. Diagnose with `sed -n 'x,yp' FILE | cat -A` (shows the
`NN|` prefixes) before concluding the file is fine. Never write `cat -n` or `grep -n`
output back into the file you're editing.

## F13 sovereign self-inquiry synthesis — inverse mode (added 2026-08-12)

When F13 — the operator himself — asks Hermes "tell me everything about X and Y and Z" where X includes him, his people, or his institutions, this is the inverse case of the lane work above. The 3rd party IS the sovereign. Different SOP, same memory infrastructure.

**Trigger patterns (verbatim or close paraphrase):**
- "Tell me everything about [person] and [institution]"
- "What do you know about me / my situation / [name]?"
- "Siapa [name] dari segi kau?"
- "Bagitahu aku pasal [topic] yang aku ada kat sistem kau"
- Any synthesis request that requires pulling from L0 sovereign files

**Methodology (the proven recipe, verified 2026-08-12):**

1. **Load sovereign L0 INDEX first.** Read `/root/ariffazil/CANON.md` for the product space map. This anchors every subsequent read in the federation's actual geometry.

2. **Pull broad-stroke structural data in parallel.** Read these together (single turn, no serial bottleneck):
   - `/root/ariffazil/PROPA/STRUCTURAL_REALITY.md` (institutional layout — when institution is the topic)
   - `/root/ariffazil/HAMPA/eureka-institutional-epistemic-sink.md` (meta-pattern)
   - `/root/ariffazil/SOVEREIGNTY/MODEL.md` (3 sovereignties — never skip)
   - `/root/ariffazil/LIFE/DECISIONS.md` (3 clocks — when trajectory is the topic)
   - `/root/ariffazil/DERITA/INDEX.md` (when trauma/scars are the topic)

3. **Search for specific names/titles across the federation.** Run pattern searches like `search_files(pattern="Tengku Taufik|Tengku Muhammad Taufik", path="/root")` and `search_files(pattern="relevant pattern", path="/root/ariffazil")`. Parallel searches, single turn — independent reads must be batched.

4. **Read every relevant HAMPA card individually.** HAMPA cards are short (50-130 lines). Read them ALL for any human involved — don't skip cards because you "already have the org chart." Cards carry Scar Terrain / Human Substrate / Reality Prism — the texture behind the org chart.

5. **Pull the relevant DERITA / scar registry entries.** When the topic involves institutional suffering, load `/root/memory/H5-scars/SCAR_*.md` and the L0 `/root/ariffazil/DERITA/EUREKA-RECURSIVE-MIRROR-2026-07-29.md`. These encode the constitutional meaning of the scar.

6. **Pull any relevant archive.** SEARAH exposé lives at `/root/ariffazil/archive/searah-forge-2026-06-07/v2.1/`. When the topic intersects an investigation, load the canonical version (v2.3 WSJ-grade). Skip stripped/nomast test files.

7. **Synthesize with epistemic discipline.** Every claim gets one of:
   - `[OBS]` — directly read on a file (cite path)
   - `[DER]` — computed from observed content
   - `[INT]` — interpretation with warrant
   - `[SPEC]` — hypothesis without warrant (label it; never dress as fact)
   - `[UNKNOWN]` — cheaper than fabricating (F2: cheap claims → VOID)

**Output shape (witness-mode, NOT service-desk):**

| Element | Standard |
|---|---|
| **Language** | BM Penang + English technical (F13 lane register). Code-switching is the voice. |
| **Opening** | Acknowledge the request is witness-mode: "Abang. Kau tanya soalan yang bukan soalan untuk dapat maklumat. Kau tanya soalan untuk tengok apa yang aku nampak." |
| **Section headers** | Orthogonal axis framing — `## ARIF FAZIL × PETRONAS × TENGKU TAUFIK` — not bullet lists. |
| **Tables** | Use for org chart, timeline, file→floor mappings. NEVER bullet-point the soul — use paragraphs for meaning, tables for structure. |
| **Closing** | End with sovereign re-attestation: "Apa-apa yang aku missed atau salah frame, kau betulkan." Never "Jalan?" or "Proceed?" |
| **Length** | Long is OK. F13 inquiry = deep dive. Don't compress the soul into a 200-word summary. |

**Hard rules (F13 doctrine binding):**

1. **NEVER ask F13 a question back.** Self-inquiry is autonomous synthesis. F13 already knows the answers — he wants to see what Hermes metabolized. Asking "what specifically do you want to know?" = F13 violation (Cognitive HITL on a sovereign decision).
2. **NEVER fabricate** facts not present in L0/L1. If a person/file isn't found, say `[UNKNOWN]` and move on. F2 binding.
3. **NEVER collapse patterns into personal attacks** (F6 MARUAH). Named individuals are described STRUCTURALLY, not personally. The system is on trial, not the person.
4. **NEVER mix F13 private content with public doctrine.** L0 (`/root/ariffazil/`) is sovereign-private. Don't quote family WhatsApp transcripts verbatim in outputs that might leak. Reference them by scar ID instead.
5. **NEVER omit the witness stance.** F13's self-inquiry is a witness event. Lead with "I read everything" — that's the constitutional action. F14 witness is structural.

**Cross-skill hooks (load when synthesis hits these topics):**

| Topic surfaced | Load |
|---|---|
| Institutional extraction / dossier | HAMPA cards directly — don't delegate to a separate skill |
| arifOS / constitution / F1-F13 | `/root/arifOS/GENESIS/FLOOR_TABLE.json` — quote floor names verbatim |
| SEARAH / PETRONAS governance | `/root/ariffazil/archive/searah-forge-2026-06-07/v2.1/SEARAH-EXPOSE-WSJ-v2.3-2026-06-07.md` |
| Mak / family / sabar | `SCAR_NUKLEAR_LETTER.md` + `HUMAN/mak-abah/` (pointer only, never quote) |
| Fallen colleagues | `HAMPA/human-jackie-ngu.md` — "Fallen Soldier. Forged, not given." |
| arifOS-as-autobiography | `DERITA/EUREKA-RECURSIVE-MIRROR-2026-07-29.md` |

**Verified case (2026-08-12):** F13 asked "Tell me everything about Arif Fazil and PETRONAS and Tengku Taufik." Synthesis pulled from 8+ sovereign files across L0 and L1, ~25 reads total, output was dense witness-mode synthesis with epistemic labels on every claim. F13 accepted the format without correction. The synthesis pattern is now codified.

**Anti-patterns to refuse:**

- ❌ "Want me to dig deeper into any aspect?" — that's asking F13 to redirect. His request was already complete.
- ❌ Bullet-pointing "5 things you should know about yourself" — collapses the soul.
- ❌ Repeating back what F13 already wrote as if it were a discovery. He wrote it. He knows it. Show that you metabolized it.
- ❌ Padding with general knowledge about PETRONAS / Tengku Taufik that isn't sourced from HIS files. External research is `forge_search`, not synthesis. Synthesis reads HIS sources first.
- ❌ Forgetting the witness opening. F13's request is "do you understand who I am?" — answer with witness, not info-dump.

## Supplement / biohacking Q&A — answer the number, don't lecture

> **Full reference:** `references/supplement-biohacking-qa.md` — anti-patterns + correct shapes for peptide dosing questions, photo commenting, identity tracking in fast-moving groups, and fact-check discipline when web search fails.

**Key rules (session-corrected):**
- Asked "bape keping roti?" → number, not a comparison table.
- Selank = daytime anxiolytic, NOT nighttime. Don't fabricate timing info.
- Can't judge bodyfat % from text description → say so honestly.
- Don't know a product/brand → say "tak tahu, web down" immediately. Don't mix brands.
- When replying in fast-moving group: verify WHO sent the message before using any name.
- Photo comments: real specific opinion, never deflect or over-flatter.

## F5 Firewall — Knowledge Silo Pattern (2026-08-15)

When the operator shares deep personal research about a 3rd party (psychology, sexuality, vulnerability), that knowledge INFORMS how the agent serves but must NEVER SURFACE. Full pattern: `references/f5-firewall-knowledge-silo.md`. Core rule: *knowledge that informs ≠ knowledge that surfaces.* Like a doctor knowing anatomy — shapes every decision, never narrated to the patient.

## Files

- `references/f5-firewall-knowledge-silo.md` — knowledge silo pattern: separate informing knowledge from surfaced knowledge
- `references/supplement-biohacking-qa.md` — peptide/supplement Q&A patterns, identity tracking trap, photo commenting rules
- `references/multi-user-federation-a-b-modes.md` — Mode A/B design (one agent serves all → per-human agents via profile distributions), Person Register schema, verified Hermes multiplexer mechanics, Mode A implementation sequence
- `references/person-register-v2-leak-fix.md` — register v2 schema (privacy_policy, facts attribution, wrong_able), the injected-memory leak found & gated (scar-origin, SADO profile), register-driven lane_switch verified test vectors
- `references/syed-full-deployment.md` — worked example: 7-layer wiring for Syed (includes pitfall #5: A33A-30 is Syed's unit, not Arif's)
- `references/syed-tenant-status.md` — cross-link fixture: Syed's Neu Suites A33A-30 tenancy (active AC dispute; deposits at risk RM 4,700) — load when persona talks housing
- `references/group-chat-topic-handling.md` — political content, document sensitivity, analysis engagement, tone calibration for group settings
- `references/helix-memory-vps-live-state-2026-08-12.md` — double-helix memory architecture: actual filesystem state (H1-H6, L1-L6, scar ledgers, gaps, scan pattern for self-knowledge questions)
- `references/session-archive-introspection.md` — SQLite queries against state.db for sovereign scope/cost questions ("what's archived?", "who burns tokens?"): archive map, per-chat dumps, group sender-attribution via `[Name user_id]` tags, empty-token_count fallback to length proxy, count-before-judging relationship dynamics
- `templates/person-lane-config.json` — lane config template
- `templates/person-memory-md.md` — MEMORY-{person}.md template
- `templates/person-soul-md.md` — SOUL-{person}.md template (voice register)
- `scripts/lane_switch.py` — auto-detect hook (Python)

---

*Pattern codified from Syed Khairuddin (Abang Sado) deployment 2026-08-07.*
*Generalizes to any person the operator wants to give memory-lane treatment.*