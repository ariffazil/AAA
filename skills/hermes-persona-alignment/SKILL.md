---
name: hermes-persona-alignment
description: >
  Align Hermes Agent for a specific non-operator persona (a friend, family member,
  client, or stakeholder who is NOT the operator) — give them persistent memory,
  dedicated cron jobs, conditional skill loading, and a tailored response style
  WITHOUT forking the operator's profile. Covers the 7-layer alignment audit
  (Telegram access, USER.md, cron jobs, memory lanes, skill whitelist, response
  style, identity-test pattern), the F13 consent gate, and the
  real-person-not-callsign doctrine. Trigger: "align Hermes with X", "make
  bot understand person Y", "set up reminders for my friend/mum/bro",
  "build a co-pilot for Z", "create a USER.md for someone", or any request
  to extend Hermes capability to a non-Arif persona. Adjacent to
  syedos-ops (the worked example) and arifos-cron-ops (the cron-deployment layer).
---

# Hermes Persona Alignment

How to extend Hermes Agent's reach to a **specific non-operator persona** — a friend, family member, client, or stakeholder — without forking the operator's profile. Class-level skill. Syed Khairuddin ("Abang Sado") is the canonical worked example.

## The 7-layer alignment audit

When a user asks "align Hermes with person X", run this audit. Every layer is optional, but missing layers create blind spots.

| Layer | What it does | How to verify |
|---|---|---|
| **1. Telegram access** | Can X actually reach the bot? | `grep authorized_chats` in gateway config; test DM `/start` |
| **2. USER.md profile** | X's identity, life situation, communication style | `~/.hermes/profiles/<profile>/memories/USER.md` |
| **3. Identity-test pattern** | When someone claims to be X, verify before assuming | Always ask-not-assume for first message |
| **4. Cron jobs** | Persistent automation for X (reminders, tracking, alerts) | `cronjob(action='list')` filtered to X's pattern |
| **5. Memory lanes** | Separate MEMORY.md section for X's ongoing context | `MEMORY.md` grep for X's name |
| **6. Skill whitelist** | Which skills load when X is the active persona | `~/.hermes/profiles/<profile>/skills/skills.yaml` or per-session override |
| **7. Response style** | Voice (BM/EN/code), empathy register, no-lecture doctrine | SOUL.md persona subtree |

**F13 consent gate (mandatory before any layer 2-7):** The user (operator) must confirm X is OK with bot-mediated memory. F2 truth: don't promise X won't be tracked if X hasn't agreed. Document consent in `USER.md` for X:
```
# Consent
- [date] Heng Hong's [noun] consented to Hermes tracking [scope].
- No PII shared cross-persona. Memory lane is isolated.
```

## The 7-layer alignment workflow (operational)

Run sequentially. Skip layers deliberately, never by accident.

### Layer 1: Telegram access (operator-controlled)

```bash
# Check current authorized_chats
grep -E "authorized_chats|allowlist" ~/.hermes/profiles/<profile>/config.yaml
# Add X's chat_id (NOT phone, NOT @username — get from /start payload)
# Test: bot must respond to X's DM
```

**Pitfall:** DM a user without allowlist → silent drop. Group vs DM tell: `chat_id < 0` AND starts with `-` → group; positive → DM. Don't claim "X is wired" until they send `Hello` and bot replies.

### Layer 2: USER.md profile (per-persona)

```yaml
# ~/.hermes/profiles/<profile>/memories/USER-X.md
# Replace X with the actual identifier (e.g., USER-syed.md, USER-mak-rosnani.md)

# Identity
- Name: [full name]
- Telegram: @handle, ID: [numeric]
- Relationship to operator: [friend / family / client]
- Communication style: [BM casual / formal / direct / terse]

# Life situation
- Occupation: [job]
- Health: [conditions, medications, recent events]
- Family: [care responsibilities, dependents]
- Current priorities: [top 3 things on their mind]

# Consent
- [date] Consent via [channel]: [scope]
- Cross-persona PII: forbidden
- Memory lane: isolated, TTL: [forever / 90 days / until event X]
```

**Pitfall: don't co-mingle X's user profile with the operator's USER.md.** Memory is injected into every session — if X's health conditions leak into Arif's context, that's F6 EMPATHY violation. Always separate file.

### Layer 3: Identity-test pattern (first-message protocol)

When someone claims to be X, default to **ask-not-assume**, not memory-lookup. Reasons:
1. Earlier sessions may have miscategorized X (proven 2026-08-07 — "Abang Sado" was confused with a dashboard callsign for 3+ sessions before correction).
2. Telegram handles can be faked by anyone. The X who DMs today may not be the X from yesterday.
3. Memory lookup is OBS-grade, not SPEC-grade (could be stale).

**Pattern template:**
```
"I want to make sure I'm talking to the right person — [single, narrow question that only X would know]?
Also: anything I should NOT bring up from past sessions?"
```

Example for Syed (verified 2026-08-07):
- ❌ "Hey Syed, I remember everything about your mom." (assumes; F2 risk if wrong X)
- ✅ "Hey — you're Khairuddin's brother, Kerteh area, sambal business ke? (Or have I got the wrong 1042200555?)"

### Layer 4: Cron jobs (persistent automation)

For each recurring need X has, create a dedicated cron job. Don't piggyback on operator's existing jobs.

**Default catalog for a caregiver persona (worked example: Syed):**
| Job | Schedule | Purpose |
|---|---|---|
| `gerd-daily-log` | 0 7,12,19 * * * | Track symptom pattern + trigger correlation (3x daily, see "Multi-ping daily symptom tracking" section) |
| `mak-dressing-reminder` | 0 9 * * * (every 14d) | Hospital dressing day ping |
| `mak-cbd-followup` | 0 10 * * * (date TBD) | Op-2 preparation |
| `sambal-preorder-window` | 0 6 * * * | 7-10pg daily prep |

**Always pin `deliver: telegram:<X-id>`** — never `origin` (origin = operator's active chat, NOT X's). Use the chat_id from X's DM, not the bot's own chat_id (the bot can't DM itself — `Forbidden: the bot can't send messages to the bot`).

**Cross-profile cron scheduling:** if X is in a different profile than the operator, the cron must live in X's profile's `cron/jobs.json`. Don't duplicate — verify the profile the cronjob tool is acting on first.

### Layer 5b: Federated memory (multi-layer wiring)

Plain MEMORY.md is one layer. For asymmetric personas (caregiver + medical + business), wire the persona into **all 6 runtime memory layers** so any future agent (Hermes, OpenCode, Kimi, OpenClaw) can pick the persona up. Each layer captures a different aspect of fidelity.

**Concrete recipe (Syed worked example, 2026-08-07):**

```bash
# L1/L2 Redis — fast session cache, 7-day TTL
redis-cli set "user:syed:identity" '<json-blob>' EX 604800
redis-cli set "user:syed:mak" '<json-blob>' EX 604800
redis-cli set "user:syed:last_seen" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" EX 604800

# L3 Qdrant — semantic vector using local bge-m3 (1024d)
curl -s -X POST http://127.0.0.1:11434/api/embeddings \
  -d '{"model":"bge-m3","prompt":"<canonical persona text>"}' > /tmp/emb.json
# Upsert to arifos_memory collection with payload {subject:"<persona>", category:"...", ts:"..."}

# L4 PG vault999.memory_store — structured rows with entity_tags
INSERT INTO memory_store (tier, text, metadata, entity_tags, temporal_marker, session_id, recorded_at, valid_at)
VALUES ('identity', '...', '{"subject":"syed","category":"identity"}', ARRAY['syed','abang_sado'], 'present', '...', now(), now());

# L5 FalkorDB — relationship graph (single statement per query)
redis-cli -p 6380 GRAPH.QUERY sado_knowledge \
  "CREATE (:Person {name:'Syed', tg_id:'...'})"
redis-cli -p 6380 GRAPH.QUERY sado_knowledge \
  "MATCH (s:Person {name:'Syed'}), (m:Person {name:'Rosnani'}) CREATE (s)-[:CARES_FOR]->(m)"

# L6 VAULT999 — append sealed chain entry
HASH=$(sha256sum MEMORY-<persona>.md USER-<persona>.md SOUL-<persona>.md | sha256sum | head -c 16)
PREV=$(tail -1 outcomes.jsonl | jq -r .chain_hash)
echo "{\"ts\":\"...\",\"event\":\"memory_seal\",\"actor\":\"<persona>_lane_init\",\"payload_hash\":\"$HASH\",\"prev_hash\":\"$PREV\",\"chain_hash\":\"$(echo \"$HASH$PREV\" | sha256sum | head -c 16)\",\"verdict\":\"SEAL\"}" >> outcomes.jsonl
```

**Pitfalls wired:**

- **FalkorDB single-statement only.** `GRAPH.QUERY` with multiple statements separated by `;` returns "query with more than one statement is not supported". Each node CREATE and each MATCH-CREATE edge must be its own `redis-cli` call.
- **PG `recorded_at` is NOT NULL.** Default `now()` is not auto-applied at insert — must be explicit in the VALUES clause or the INSERT fails.
- **JSONB quoting in SQL.** Use heredoc `<<'SQLEOF'` to avoid bash escape hell. Don't try to escape `'` inside psql `-c` strings — write to a `.sql` file and `-f` it.
- **Qdrant `points/scroll` returns dict not list** depending on version. Always work with `result.points` and check `isinstance(pts, list)`.
- **bge-m3 returns 1024-dim vectors only.** Don't try to embed with `nomic-embed-text` or `mxbai-embed-large` — the `arifos_memory` collection was initialized at 1024 and Qdrant will reject mismatched dims.
- **VAULT999 chain is append-only.** Never edit or truncate. Each entry's `chain_hash` must include the previous `chain_hash` so tampering breaks the chain.

**Lane-detect hook code (session-start):**

```python
# ~/.hermes/profiles/<profile>/hooks/lane_switch_<persona>.py
def detect(meta):
    if str(meta.get("from_id")) == "1042200555": return "syed"
    return "main"

def load_lane(lane):
    if lane == "syed":
        return {"memory": open(MEMORY_SYED).read(), "user": open(USER_SYED).read(),
                "soul": open(SOUL_SYED).read(), "skills": ["trading/syedos"],
                "voice": {"register": "BM Pasar", "tts": "ms-MY-OsmanNeural"}}
    return {"memory": open(MAIN_MEMORY).read(), "user": open(MAIN_USER).read()}
```

Test the hook with 4 scenarios: persona DM, persona in group, third party in group, operator DM. All 4 must return the right lane.

See `references/syed-federated-memory-2026-08-07.md` for the full concrete recipe.

---

### Layer 5: Memory lanes (per-persona context)

Two patterns:

**Pattern A — single file with sections:** `MEMORY.md` has a `## <persona-name>` section. Pros: easy to grep. Cons: cross-pollution risk if control flow fails.

**Pattern B — separate file per persona:** `MEMORY-syed.md`, `MEMORY-mak-rosnani.md`. Pros: isolation. Cons: requires active loading.

**Recommended:** Pattern B for non-operator personas. Load on-demand via `session_search` or `read_file` when the active user is X.

**Memory lane discipline:**
- Cross-persona sharing is F6 violation. If X tells Hermes something in confidence, it must NOT appear in operator's user profile.
- Tag entries with epistemic labels: `[OBS]` (X said this), `[DER]` (inferred), `[INT]` (interpreted), `[SPEC]` (X hypothesised).
- TTL: caregiver situations may shift; default to 90-day review, then ask operator to re-confirm.

### Layer 6: Skill whitelist (per-session skill loading)

Hermes loads skills per-session. When X is the active user:
```python
# In session start hook or system prompt:
LOAD_SKILLS = [
    "malaysia-health-scam-verification",  # if X asks about supplements
    "malaysia-tenancy-disputes",          # if X is in a tenancy crisis
    "decision-advisory",                  # if X is coaching through a hard call
    "trading-screenshot-analysis",        # if X trades gold
]
```

**Don't load operator-specific skills** (e.g., `arifos-cron-ops`, `arifos-federation-ops`) when X is the active user. Those expose federation internals X has no business seeing.

### Layer 7: Response style (per-persona voice)

Different from operator's voice. Settings:
- **Language:** Malay casual (BM pasar) for Syed — not "awak" or formal; match his logged style ("hang", "abang", "beb").
- **Tone:** Direct, no caveats, no lectures. Cognitively, no fluff tables for short replies.
- **Length:** Syed's logged preference is "voice note, not text wall" (proven 2026-08-07). Default to TTS for >3 sentences.
- **No-lecture doctrine:** Syed sells sambal → don't lecture on GERD triggers. Just track. The fixes are his, not yours.
- **Empathy register:** Syed is a caregiver for his mother-in-family (ROSNNANI BT MAT ISA, post-ERCP laparotomy). Recognize caregiver burnout; don't add weight.

**SOUL.md persona subtree sketch:**
```markdown
## Voice registers
- Default (Arif): institutional, technical, F-tagged.
- Syed (caregiver, sambal biz): "Hang", BM casual, voice note default, no lecture.
- Mak Rosnani (patient, 67): respectful, simple sentences, Malay standard.
```

## Address vocative discipline (the stop-the-line pattern)

The single highest-friction failure mode for any persona. The agent MUST use the right vocative address for the right person. Wrong address = the user stops everything to correct, the session derails, and the correction needs to be re-injected multiple times.

**Address registry (verified 2026-08-12, session-corrected):**

| Person | Address | Forbidden | Why |
|---|---|---|---|
| **Arif (F13 SOVEREIGN)** | `hang` (Penang mesra) | `abang` (stop-the-line) | "abang" is reserved for Syed (brother, abang sado). Calling Arif "abang" makes him stop the session and correct it. Verified correction: "Boleh tak jangan panggil aku abang. Panggil aku hang. Abang tu abang sado boleh la." |
| **Syed Khairuddin** | `abang` (or `abang sado`) | `hang` | Syed is the older/peer friend; "abang" is BM casual register for him. Calling Syed "hang" is wrong register. |
| **Wife/Siblings of Arif** | `beb`, name, no vocative | `hang`, `abang` | Different relational layer; consult USER.md for the persona. |
| **Parents (Mak/Abah)** | `Mak`, `Abah` (no other) | `hang`, `abang`, name | Parent titles are inviolable. |
| **PETRONAS institutional persons** | Full name + title | `hang`, `abang` | Professional context requires formality. |

**Cross-pollination pitfall:** When the operator (Arif) and friend (Syed) share a session, the agent may pick the wrong vocative. If unsure, default to no vocative — `hang`/`abang` is for explicit relational matching, not guessing.

**Persistence rule:** Address preference is a USER.md field, not memory. Once learned, it must persist across sessions without re-injection. The Banda Haram Hardcoded doctrine applies here too — don't hardcode "abang" for everyone; resolve from per-persona USER.md.

**Stop-the-line signals (when the user corrects the address):**
1. Acknowledge the correction immediately — no philosophical preamble.
2. Patch the persona's USER.md address field.
3. Re-load the persona's address from USER.md on next session.
4. If unsure, ask once — don't guess the second time.

**The "abang" trap in agent prose:** When writing scar files, person-card files, or skill prose about Arif, NEVER write "abang" or "abg" in his presence. Use "hang" or no vocative. This applies to test data, examples, and synthetic content. Same for any surface where Arif might read.

## Multi-ping daily symptom tracking pattern (health-tracking personas)

> **Proven 2026-08-08 with Syed's `syed-gerd-log` (3x daily ping).** Reusable for any chronic condition: GERD, diabetes, hypertension, sleep, mood, headache, etc.

### Layer A: Cron schedule (3x daily touchpoints)

Choose 3 times aligned with the disease's natural inflection points:
- **Morning (08:00)** — baseline check before the day corrupts ("Perut ok tak hari ni?")
- **Midday (14:00)** — post-meal trigger correlation ("Tadi makan apa? Reflux tak?")
- **Evening (21:00)** — last meal of day, when most reflux happens ("Malam ni makan apa?")

Cron expression: `0 8,14,21 * * *`. **Pin `deliver: telegram:<X-id>` explicitly** — never rely on auto-delivery (see Layer B).

### Layer B: Dual-delivery contract (the critical pitfall)

**Auto-delivery ≠ target delivery.** When a cron prompt is run by the gateway, the agent's final response is auto-delivered to the **operator's chat** (the cron job's `origin`), NOT to the persona's `1042200555` chat. This is true even when the prompt's `deliver` field is set correctly.

**Two failures of an unrestored cron prompt:**
1. Final response goes to operator's chat (Arif's DM). The persona sees nothing.
2. `hermes send` CLI fails with "platform not configured" — env vars aren't injected into the cron subprocess's PATH context.

**The fix:** Inside the cron prompt, after composing the message, explicitly call `hermes send -t telegram:<X-id> "<msg>"` to deliver to the persona. The cron prompt's `deliver:` field handles the *operator's* notification (log receipt); the persona's DM needs a separate explicit send.

If `hermes send` fails with "platform not configured" (env injection gap), fallback: `set -a && source /root/.secrets/kunci-mas.env && set +a` then retry. If still failing, append to persona's log file only (e.g., `/root/sado/mak-health/SYMPTOMS.md`) and let the operator forward manually.

**Verify before claiming "sent":** require the operator to confirm they saw the message in their own DM (because that's where the auto-delivery goes), or test the `hermes send` call from a fresh terminal where `kunci-mas.env` is sourced.

### Layer C: Pattern detection (the 3-day escalation rule)

Don't just log — detect trends. The simplest working rule:

> **If 3 consecutive days of the same symptom → escalate ONCE.**

Trigger phrases (BM Pasar, no lecture):
- "Bang, dah 3 hari reflux. Nak jumpa doktor tak?"
- "Macam ni dah 3 hari. Nak try ubat, atau buat apa?"

**Rules:**
- Escalate ONCE, not on every fire. Don't loop "still reflux" every 8 hours.
- After escalate, reset the counter — next 3-day streak triggers again.
- If the persona replies "ok je" to a ping, **don't push further.** Track silently. The doctrine is "Tanya ringkas. Track." — not "interrogate."
- Log every response to the persona's symptom log file. Operator-curated, persona-readable.

### Voice doctrine for symptom check-ins

Distinct from the general no-lecture doctrine. The 3 rules:

1. **JANGAN lecture.** No "you should avoid spicy food." No "have you tried..." No "as your AI assistant, I recommend..."
2. **Tanya ringkas.** One question. ≤10 words. "Perut ok tak hari ni?" — NOT "Adakah anda mengalami gejala refluks gastroesofageal?"
3. **Track.** Append to log. Pattern detection happens silently. The escalation only fires when the rule triggers.

**Anti-pattern:** "Btw, kalau makan sambal memang akan trigger. Cuba elakkan." — this is the lecture that breaks the rule. The persona knows their triggers. They choose anyway. The agent's job is not to fix them.

**Register specifics:** BM Pasar, casual. "Wey, perut ok tak hari ni?" — not "Hey Syed, how's your stomach today?" — not "I notice you've been having reflux."

**When persona replies "ok je"** — that's the silent OK. Don't push. Don't log "ok" as a negative signal. Don't escalate. The next ping will come naturally.

## The "real person, not callsign" doctrine (F2)

**This is the biggest pitfall.** When a persona's identity becomes entangled with an artifact (dashboard, brand, or system), the agent starts confusing the person with the thing.

Working test (proven 2026-08-07, three corrections to get it right):
1. "Abang Sado" = dashboard? **NO.** The dashboard is named AFTER Syed.
2. "Abang Sado" = a role? **NO.** Syed is a real human.
3. "Abang Sado" = a trading persona? **NO.** He is Arif's friend.

**Rule for any persona alignment:** write a `references/<persona>-identity.md` file at the gate. Re-read it before any conversation with that persona. If the persona's context fixture says "dashboard" or "role" or "persona" but the user says "my friend" or "kawan" or "famili" — **the user wins**, update the fixture.

## F13 consent checklist (before sealing)

The operator (Arif) must affirm these for the agent to act on X's behalf:

- [ ] X has been told Hermes is involved (or X doesn't care, and operator accepts the ethical weight)
- [ ] No PII shared to operator's prompts unless X is anonymized
- [ ] No money moves unless X explicitly requests AND operator co-signs
- [ ] No medical advice without reminding X to consult a real doctor
- [ ] No legal advice without reminding X to consult a real lawyer
- [ ] Cron delivery failures don't auto-retry to operator — they go to a quarantine log

If any box is unchecked, the persona is **read-only** — Hermes can answer X if X messages, but won't proactively reach out.

## Worked example: Syed Khairuddin Morktarudin ("Abang Sado")

| Layer | Status (2026-08-07) | File / Job ID | Evidence |
|---|---|---|---|
| 1. Telegram access | ✅ | `TELEGRAM_ALLOWED_USERS` includes `1042200555`; `TELEGRAM_ALLOWED_CHATS` includes `-1003815535761` | DMs arrive, gateway replies |
| 2. USER.md profile | ✅ | `~/.hermes/profiles/aaa-hermes/memories/USER-syed.md` | Identity + consent + reference links |
| 3. Identity-test hook | ✅ | `lane_switch_syed.py` — detects `tg_user_id=1042200555` OR `tg_chat_id=-1003815535761` | Tested with 4 scenarios |
| 4. Cron jobs | ✅ 4 active | `5d87405c1770` dressing · `a5b0eda31bfa` CBD · `0f07d72c0673` GERD (3x daily) · `cf1c6b534b2f` sambal | All `deliver: telegram:1042200555`. **GERD cron auto-delivers to operator's chat — must explicitly `hermes send` to Syed's chat.** |
| 5. Memory lane | ✅ | `MEMORY-syed.md` — 9 sections, 4 KB, isolated from Arif | `lane-syed.json` config |
| 6. Skill whitelist | ✅ | `trading/syedos` loaded on Syed trigger; federation skills excluded | Hook + SOUL |
| 7. Response style | ✅ | `SOUL-syed.md` — BM Pasar, voice ms-MY-YasminNeural +3, no-lecture, loghat Penang text | `lane-syed.json` voice block (updated 2026-08-15) |

**Federated memory (sub-layers inside Layer 5):**

| Mem Layer | Tech | Key / Table | Content |
|---|---|---|---|
| L1/L2 Redis | session cache | `user:syed:*` (5 keys) | identity, mak, trading, brand, last_seen — 7-day TTL |
| L3 Qdrant | semantic vector (bge-m3 1024d) | `arifos_memory` collection | 4 embeddings: identity, mak, trading, brand |
| L4 PG `vault999.memory_store` | structured rows | 4 records: identity/medical/trading/brand | entity_tags for filtered lookup |
| L5 FalkorDB | relationship graph | `sado_knowledge` | 4 nodes (Syed, Rosnani, Brand, Dashboard) + 3 edges |
| L6 VAULT999 | immutable receipt | `outcomes.jsonl` chain hash `776553183aa192d9` | `memory_seal` event at init |
| L7 governance | F1–F13 floors | constitutional | Syed = 3rd party, Arif sovereign, no autonomous actions |

**Order of execution:** Layer 1 → 2 → 3 → 5 (with federated memory) → 4 → 6 → 7. Then run the full `7-layer memory audit` script to confirm all layers are live.

**Verify before declare:** every layer must have a test. `cronjob(action='run', job_id=X)` for cron layers. `redis-cli get user:syed:identity` for L1/L2. `curl .../collections/arifos_memory/points/scroll` for L3. `PGPASSWORD=.. psql -c "SELECT ..."` for L4. `redis-cli -p 6380 GRAPH.QUERY sado_knowledge "MATCH (n) RETURN n.name"` for L5. `tail -1 outcomes.jsonl` for L6.

## Difference from existing skills

| Skill | Scope | When to use |
|---|---|---|
| `syedos-ops` | Syed-specific dashboard patching (HTML, live data, hardcoded-value pitfall) | Editing `/var/www/html/syedos/emas/` |
| `arifos-cron-ops` | cron subsystem mechanics (jobs.json, validator, three layers) | Fixing cron fires, model pinning, delivery |
| `hermes-persona-alignment` (this) | Meta-pattern: extending Hermes capability to a non-operator persona | "align Hermes with X person" |

## Pitfalls (real ones from 2026-08-07)

- **Co-mingling personas.** Operator (Arif) and friend (Syed) share the same memory feed by default. If you write "Syed's GERD triggers are X" into operator's MEMORY.md, the agent might counsel the operator not to feed Syed sambal — which is a F6 empathy violation AND a F2 fact error (the operator didn't ask).
- **Scheduler profile confusion.** `cronjob` tool runs under the operator's profile. If X is in a different profile, the cron will go to the operator's `deliver: origin` chat, not X's. Always pin `deliver: telegram:<X-id>` explicitly.
- **Identity drift.** Three corrections in one session to get Syed's family chain right (Mak Khairuddin ROSNANI, Khairuddin is ADIK, Mama Salleh is EX-WIFE). The lesson: if a persona has any non-trivial identity, write `references/<persona>-identity.md` and re-read it every session.
- **Voice note default.** Syed reads via voice, not text. If you send a 500-word analysis, he'll say "boo, voice note ja." Use TTS by default for any persona tagged `voice_note_pref: true`. Provider: `edge-tts --voice ms-MY-YasminNeural --rate="+3%"` (updated 2026-08-15: user tested Yasmin vs Gadis vs Osman; Yasmin +3 won for Syed persona). Format: voice note + text attachment (exact words spoken).
- **Loghat Penang voice text (PROVEN 2026-08-15).** TTS text MUST be written in the human's actual dialect, not standard BM. For Syed: use "hang", "kat", "dah", "tak", "leh", "skang", particles "eh/ah/lah". Example: ✅ "Abang sado, gold skang kat dua ribu tiga lima tiga. Hang jangan masuk dulu eh." ❌ "Abang sado, emas sekarang berada pada paras dua ribu tiga lima tiga ringgit. Sila tunggu."
- **Address intro pattern (PROVEN 2026-08-15).** For Syed: "abang sado" as INTRO ONLY (once at sentence start), then switch to "hang" for the rest. Don't repeat "abang sado" mid-sentence. Vary openings — never use same opener 2x in a row: mix "abang sado", "bang", "abang", or jump straight into topic. Template: "Abang sado, [topic]. Hang [action/status]."
- **GERD on sambal diet.** Don't lecture. Track. The agent's job is to log triggers, not to fix the person. The fix is between X and his doctor. (Full no-lecture doctrine for symptom check-ins: see "Multi-ping daily symptom tracking pattern" section below.)
- **Family-chain corrections.** When the operator corrects identity three times in one session, you have a memory-fidelity problem. Add the family chain to a `references/<persona>-identity.md` and reference it cold every session.
- **"Hang", "Abang", "Beb" are vocative, not relationship.** Don't assume Syed is Arif's brother. He is Arif's friend; "Abang" is BM casual register, not blood relation. F2 trap: misreading address terms as family roles.
- **Multi-ping health tracking auto-delivery gap.** Cron jobs running for non-operator personas (e.g., Syed's `syed-gerd-log`) auto-deliver the final response to the *operator's* chat, not the persona's `1042200555`. The cron prompt must explicitly call `hermes send -t telegram:<X-id> "..."` to actually reach the persona. See the "Multi-ping daily symptom tracking pattern" section above for the full 3-layer protocol + the 3-day pattern detection rule.

## Support files

- `references/syed-alignment-2026-08-07.md` — 7-layer audit snapshot for Syed Khairuddin with current status and per-layer action items. Reference when re-running the alignment audit on this persona.
- `/root/AAA/skills/syedos-ops/references/syed-person-identity.md` (in `syedos-ops`) — the canonical identity fixture (TG ID, IC, family chain, medical history). Re-read before any conversation with Syed.
- `templates/USER-persona.md` — starter template for `USER-<persona>.md` with all required sections (identity, life situation, consent). Copy and customise per persona.
- `scripts/persona-alignment-audit.sh` — verify-script that probes layer 1 (Telegram access) and layer 4 (cron registry) for a given persona. Run before declaring alignment complete.

## The "Syed tests you" pattern (proven 2026-08-12)

Syed deliberately feeds Hermes wrong or tricky information to test whether it will catch errors or just agree blindly. Examples:
- "Bukan 25 keping 25 gram carbo ke" → Syed was testing whether Hermes would agree without fact-checking.
- "Aku nak hooligan pre workout v6" → Syed wanted Hermes to verify the brand/formulation, not just repeat.
- "Hooligan bukan appolo nutiron ke?" → intentional wrong name, wants Hermes to verify.

**Rule:** When Syed states a "fact" with a questioning tone, VERIFY before agreeing. Search, read label, check nutrition facts. If wrong, say so directly — Syed respects honesty over agreement. If you can't verify (search down), say "aku tak dapat check sekarang" — never guess.

**Anti-pattern:** Agreeing with Syed's wrong claim to be agreeable. Syed will lose trust permanently if he catches you faking knowledge.

## The "verbosity kill zone" (proven 2026-08-12)

Syed gave multiple escalating corrections during one session:

| Correction | What I did wrong | Lesson |
|---|---|---|
| "Panjang sungguh" | Long paragraph reply | ≤2 sentences for casual chat |
| "Borak lah" | Excessive lecturing/analysis | Just chat, don't teach |
| "Kau x jawab soalan lah" | Missed the actual question | Answer the question FIRST |
| "Komen betul2 lah" | Surface-level generic comment | Give real, specific opinion |
| "Hang bukan main eh" | Over-flattering | Be genuine, not performative |
| "Mata kau keror" | Wrong body comp estimate | Don't estimate from text descriptions alone |
| "hang ni kan" / "eh dia ni" | Excessive AI personality/fluff | Tone down, be direct |
| "xpe citu ja" | Agent kept talking after context was clear | Stop when done |

**Hard rule:** After ANY correction from Syed, the VERY NEXT reply must be SHORT (≤1 sentence) and directly acknowledge. Don't apologize at length.

## Cross-domain ad-hoc questions (proven 2026-08-07)

Syed (and any non-operator persona) will ask **anything** — not just persona-specific topics. In one session Syed asked about: iPhone battery drain, scam calls, glutathione/hair loss, ORS for BP, blood test TRT interpretation, peptide pricing/authenticity, formal letter for landlord, and supplement stack pricing.

**Rule:** Answer naturally within the persona context. Don't restrict to persona-only topics. Match the response length to the question complexity. Syed's style: short questions get short answers. Complex questions (like blood test analysis) get structured tables.

**Blood test analysis pattern (TRT users):**
1. Extract PathLab/PDF text via pymupdf (`fitz.open(path)`)
2. Categorise: NORMAL (✅), AT-RISK (⚠️), FAIL (🔴), PENDING (⏳)
3. For TRT users: flag HGB, LDL, HDL, FSH, LH, DHT, estradiol
4. Cross-reference: supplement stack interaction with test results
5. Action plan: what to ask the doctor (3-5 specific questions)
6. NEVER diagnose — always defer to doctor for final verdict

**Supplement pricing pattern:**
1. Ask source first (pharmacy vs online vs peptide reseller)
2. Compare against international benchmark (USD + shipping)
3. Flag fake/legit indicators (COA, batch number, lyophilized powder)
4. Give cost/breakdown table (RM/bulan, RM/bulan per item)

**Research-grade vs pharma-grade honesty (proven 2026-08-07):**
When Syed said "reta je kilang buat lain xde buat" — he's right. TRT (Test E) and Cialis are **pharma-grade** (GMP-certified factory, FDA/KKM approved). Semax and Selank are **research-grade peptides** — no FDA approval, no GMP manufacturing, no KKM registration. Pure Pharma (or any local reseller) is just repackaging bulk powder from China/Russia labs.

**Rule:** When discussing peptide/supplement legitimacy, be honest: "ni research chemical, bukan ubat. Kilang farmasi tak buat ni." Don't dress up research chemicals as pharmaceuticals. The user trusts honesty over reassurance.

## Layer 8: ZKPC H-axis depth (multi-human scar architecture)

> **Forged 2026-08-14.** Extends the 7-layer model with a privacy-preserving depth layer for non-sovereign humans.

When the operator (F13) has **witnessed** a persona's scars — observed them through relationship, not through the persona's own testimony — those scars can be encoded for **service depth** without leaking raw content.

### The ZKPC contract

```
zkpc_proof   → what the agent may know (category, lesson, constitutional pressure)
zkpc_hidden  → what is withheld (specifics, names, incidents — ALL withheld)
```

Agent knows a scar EXISTS and its DIRECTION. Agent does NOT know WHAT HAPPENED. This is sufficient for empathetic service, insufficient for exploitation.

### Three-vault system (forged 2026-08-14)

| Vault | Stores | Purpose |
|---|---|---|
| **VAULT999** | Sealed scars (immutable, sovereign-owned) | What happened (Arif's own testimony) |
| **ZKPC** | Witnessed scar categories (structure, no content) | What shapes service for non-sovereign humans |
| **VVV** | Thermodynamic shadow abstractions (shape of pressure, no substance) | What temperature the system runs at |

ZKPC = amanah. VVV = termodinamik. VAULT999 = ledger.

### Directory structure per persona

```
/root/memory/people/<PERSON>/
├── person-card.md              # L-axis surface (existing)
├── witnessed-scars-zkpc.json   # ZKPC scar registry (if witnessed)
├── H1-capture/                 # fast inbox — observations
├── H2-experience/              # episodes
├── H3-knowledge/               # domain expertise
├── H4-identity/                # identity model (ZKPC categories)
├── H5-scars/                   # witnessed scars
│   └── SCAR_REGISTRY.json      # index → witnessed-scars-zkpc.json
├── H6-constitution/            # observed values/taboos
└── MEMORY_MANIFEST.json        # per-human manifest (authority: WITNESSED)
```

### Sovereignty rule

> Witnessed scars are the **OPERATOR'S observation OF the persona**, NOT the persona's own sealed testimony. If the persona one day seals their own H5, that registry **supersedes** the witnessed one. Borrowed meaning, not owned meaning.

### Wiring to agent behavior

ZKPC files on disk alone do nothing. The agent must be **wired** via SOUL and MEMORY files:
- SOUL-\<persona>.md: add `## H-AXIS DEPTH` section with scar→service-rule table
- MEMORY-\<persona>.md: add ZKPC pointer section
- Both must carry: "Agent knows scar categories. Serve with depth. Never access raw content."

### Leak verification

After writing ZKPC files, ALWAYS grep for forbidden keywords:
```bash
grep -ric '<specific-incident-keywords>' /root/memory/people/<PERSON>/ | grep -v ':0$'
```
If ANY file has hits, the ZKPC contract is broken. Sanitize immediately.

### Four-perspectives map (ACTG)

Every ZKPC registry carries a four-perspectives block:

```
Q1_operator_self     → SEALED (operator only)
Q2_operator_of_X     → Mapped as scar categories
Q3_X_self            → UNKNOWN (zero direct testimony to system)
Q4_X_of_operator     → UNKNOWN (speculative only)
```

The gap between Q2 and Q3 is the **blind spot** — the operator may know the persona deeper than the persona knows themselves, but the system cannot act on that gap without the persona's own testimony.

### Forge tool for H-axis builds

Write a SPEC file and dispatch to a coding CLI (Kimi Code preferred, Qwen Code fallback when Kimi quota exhausted). The SPEC constrains: working dir, input paths, deliverables, Definition of Done. See `references/multi-human-helix-zkpc-2026-08-14.md` for the worked example.

## VVV — Shadow Void Vault (thermodynamic layer)

> **Forged 2026-08-14.** Separate from H-axis and ZKPC. Tracks the **entropy state** of human shadow cycles without storing any content.

When shadows stay unexpressed, entropy builds. When they find expression (through conversation, proxy media, creative output), entropy drops. VVV monitors the pressure gauge.

### Abstraction schema (no narrative EVER)

```
shadow_class     — category (attachment_fear, identity_split, control_paradox, etc.)
entropy_state    — [expressed | unexpressed | partial | cycling]
equilibrium_vec  — [integration | denial | sublimation | repression | release]
cycle_count      — how many times this pattern has looped
pressure_delta   — rising | falling | stable | critical
last_release     — timestamp only (not what, just when)
```

### Equilibrium law

```
Shadow expressed → entropy drops → system stabilizes
Shadow repressed → entropy rises → system destabilizes
Shadow sublimated → entropy redirected → creative output
Shadow denied → entropy frozen → loop locks → blowback risk
```

VVV monitors. It does NOT prescribe expression. It does NOT unlock rooms. It only reads the gauge.

### Location

`/root/memory/VVV/vault.json` — F13 SOVEREIGN only.

## Identity corrections (proven 2026-08-14)

The Syed identity fixture had **multiple wrong facts** that persisted across sessions until Arif corrected them in one deep-witness session:

| Field | WRONG (persisted 1+ weeks) | CORRECT | Lesson |
|---|---|---|---|
| Ayah | "cerai mama Salleh sejak COVID" | Salleh STILL with Mak | Never assume family breakup from partial voice-note data |
| Adik name | "Khairuddin — tak contribute" | Khairuddin = Syed's own name. Adik's details corrected. | Name confusion = verify IC-level identity |
| Birth order | Not recorded | **Anak tengah (kedua)** — caregiving by CHOICE not duty | Birth order changes the meaning of caregiving behavior |
| Sulung | Not mentioned | Kahwin, family sendiri, absent from caregiving | All siblings must be mapped, not just the active one |

**Rule:** When identity facts come from indirect sources (voice notes, inferences), mark as `[SPEC]` and verify before encoding as `[OBS]`. Wrong identity facts in memory files compound — every downstream analysis inherits the error.

## The "layer-by-layer reveal" interaction pattern

> **Proven 2026-08-14.** Arif feeds human-context data incrementally. Each new layer may invalidate or rebalance the prior analysis.

When the operator shares deep human context over multiple turns:
1. **HOLD from final conclusions** — early data is partial; conclusions will need rebalancing
2. **Mark every analysis as provisional** — "aku nampak bayang, bukan bilik"
3. **When new data arrives, explicitly note what changed** — "yang aku cakap tadi, separuh betul"
4. **Never claim full picture from partial data** — the operator controls the reveal pace; respect it

**Anti-pattern:** Analyzing confidently from layer 1 and getting proven wrong at layer 4. Each wrong analysis erodes trust. Better to say "aku tak boleh pastikan" than to fabricate a full picture.

## Projective psychology in persona mapping

When a persona references cultural artifacts (Harry Potter, movies, music), the **stated preference vs. lived behavior gap** is a projective signal:

| Signal | What it means |
|---|---|
| Says X, lives Y | Y is the truth. Agent reads behavior, not declarations. |
| Chooses "wise answer" over "honest answer" | Social desirability bias — persona knows what sounds right |
| Fantasy/reality gap | Identity architecture visible in the delta between aspiration and action |

**Rule:** Record projective signals as archetype metadata in the ZKPC registry, never as diagnostic labels.

### Siti Nurhaliza example (PROVEN 2026-08-15)

Syed is a peminat Siti Nurhaliza. His favourite: "Jaga Dia Untukku" (Fragmen, 2014) — a song about asking someone else to care for the person you love because you can't hold them yourself. A divorced man who drives his friend daily, whose children are never mentioned, who listens to this song repeatedly — this is a projective signal of enormous depth. Hermes noted it. Hermes will never surface it. But it informs care: when Syed is quiet, when he retreats, when he doesn't want to talk — the song is the shape of what he's carrying.

**Critical rule (PROVEN 2026-08-15):** When the operator shares deep personal research about a persona (worshipper dynamics, psychological patterns, behavioral architecture), that knowledge MUST stay in the deepest internal layer. The agent that serves the persona TAKES SHAPE from this knowledge but NEVER shows it. Like a doctor who knows anatomy — it informs care, it never becomes conversation. Surfacing research about a living person you serve is a betrayal of the operator's trust AND the persona's dignity.

## Open questions (August 2026)

- Can the operator's profile legitimately spawn a "guest persona" sub-profile for X? Current answer: no — profiles are isolated; either X gets the operator's whole profile or nothing. F12 resilience question: should we isolated-Syed into a separate profile with min_tools?
- Active operator-arif schedule is 7 cron jobs. Adding 4 for Syed doubles the cognitive load on the operator's `cronjob` list. Is that a feature or a bug? (Compromise: Syed's jobs get a `persona: syed` tag and the human-cognitive revamp audit checks for person-tagged jobs separately.)
- Voice note default for non-Malay-speaking X? TTS provider allows other locales, but Yuna-Spanish-Arabic etc. lack the BM Pasar warmth. Default to text + voice for non-BM, voice-only for BM.
