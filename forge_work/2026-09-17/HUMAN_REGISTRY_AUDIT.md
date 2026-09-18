# HUMAN REGISTRY AUDIT — 2026-09-17

> **Authority:** F13 Sovereign directive + OpenClaw audit analysis
> **Trigger:** "Registry tanpa heartbeat = buku alamat, bukan jagaan"
> **Status:** COMPLETE — findings + unified registry + heartbeat spec

---

## EXECUTIVE SUMMARY

Three human registries exist in arifOS. None are aligned. One contains a bot classified as a human. One contains a ghost entry. Seven people in the oldest registry have zero interaction path. The system has strong doctrine for 1 human (Arif) and weak-to-zero telemetry for the other 14.

**This is the infrastructure-of-love failing silently — exactly as the OpenClaw audit diagnosed.**

---

## THE THREE REGISTRIES

**Registry 1: HAMPA Registry (2026-07-02)**
Path: /root/AAA/wiki/entities/HAMPA_REGISTRY.md
Count: 15 humans
Status: STALE — never updated since creation

**Registry 2: person-register.json (2026-08-09)**
Path: /root/AAA/federation/person-register.json
Count: 6 persons
Status: PARTIAL — has routing/visibility but incomplete coverage

**Registry 3: Telegram Session Data (live)**
Path: /root/.hermes/state.db (sessions table)
Count: 12 DM users (2 are bots)
Status: LIVE — but no cross-reference to any registry

---

## CROSS-REFERENCE: WHO IS WHERE

### Verified Alive, In Multiple Registries

**Arif Fazil** — HAMPA #1 + person-register ARIF + Telegram ARIF (267378578) — 16,188 msgs — HEALTHY

**Aliff Husna** — HAMPA #4 + person-register ALIFF (1024343313) + Telegram "al" (1024343313) — 60 msgs — NAME MISMATCH: "al" in sessions vs "Aliff" in registry

**Izzu** — person-register IZZU (1237635275) + Telegram "Mohd" (1237635275) — 1,157 msgs — CRITICAL: Only 1 fact in register, and it references WRONG telegram ID. Heavy user (167k tokens) but system thinks his name is "Mohd"

### In person-register + Telegram, NOT in HAMPA

**Aidel Tasuki** — Telegram 922272533 — 33 msgs, 156k tokens — NO person-register, NO HAMPA — heavy user completely unmapped

### In HAMPA, NO Telegram, NO person-register

- **Laletha** (PETRONAS supervisor) — Zero interaction path
- **Kak Su** (PETRONAS senior mgr) — Zero interaction path
- **Mak** (Faridah) — Zero interaction path
- **Nabilah** — Has Dear NABILAH group (123 msgs) but no DM, no person-register
- **Azwa** — Was on old OpenClaw edge. That edge is dead. She is INVISIBLE.
- **Jia** — Zero interaction path
- **Hafiz, Jamin, Ilyana, Aimie** — PETRONAS colleagues, reference only
- **Fahim, Fattah** — Family reference only
- **Abah** — Deceased (March 2024). Archive only. Correct.

### In persons.yaml (legacy), NOT in HAMPA or person-register

- **Mail (Ismail Marzuki)** — 11-year friend, witness, off-switch holder. Most important non-Arif human. ZERO live telemetry. Not in any active registry.

### Reclassified / Removed

- **WAWA (8324190535)** — person-register lists as human. REALITY: origin.user_id = 267378578 (Arif). This is WawaBot — a bot. REMOVE from person-register.
- **USER_5444180135** — Ghost entry. Zero facts, zero sessions. REMOVE.

---

## CRITICAL BUGS

**BUG 1 — WAWA classified as human**
WAWA in person-register.json has telegram 8324190535. Session origin shows user_id = 267378578 (Arif). This is a bot DM, not a human. 1,116 messages attributed to a "person" that is actually Arif talking to his own bot.

**BUG 2 — IZZU identity collision**
IZZU in person-register has telegram 1237635275. But the ONLY fact references telegram 1024343313 (Aliff's ID). Sessions show 1237635275 = "Mohd" with 1,157 messages. The person-register has the right ID but wrong facts.

**BUG 3 — Mail missing from HAMPA**
persons.yaml (2026-06-12) lists Mail as witness + off-switch holder. HAMPA (2026-07-02) does not include him. person-register (2026-08-09) does not include him. The most important non-Arif human has no unified entry.

**BUG 4 — USER_5444180135 ghost**
person-register has USER_5444180135 with zero facts and zero sessions. Dead entry.

**BUG 5 — Aidel completely unmapped**
33 messages, 156,000 prompt tokens — third heaviest per-message user. No HAMPA card, no person-register entry, no lane. System has no idea who this person is.

---

## UNIFIED HUMAN REGISTRY

### Tier 1: Live Interaction (Telegram DM with Hermes)

| ID | Name | Telegram | Msgs | Lane | Last Seen |
|----|------|----------|------|------|-----------|
| arif | Arif Fazil | 267378578 | 16188 | lane-arif | 2026-09-16 |
| syed | Syed Khairuddin | 1042200555 | 190 | lane-syed | 2026-09-15 |
| aliff | Aliff Husna | 1024343313 | 60 | lane-aliff | 2026-09-14 |
| izzu | Izzu (VERIFY vs Mohd) | 1237635275 | 1157 | lane-izzu | 2026-09-13 |
| aidel | Aidel Tasuki | 922272533 | 33 | PENDING | 2026-09-08 |
| lutfi | Ahmad Lutfi | 160111098 | 5 | PENDING | 2026-09-15 |

### Tier 2: Group Interaction Only

| ID | Name | Group | Msgs |
|----|------|-------|------|
| nabilah | Nabilah | Dear NABILAH | 123 |

### Tier 3: Referenced Only (no live path)

| ID | Name | Source | Risk |
|----|------|--------|------|
| mail | Mail (Ismail Marzuki) | persons.yaml | HIGH — witness + off-switch, zero telemetry |
| laletha | Laletha | HAMPA | HIGH — supervisor, zero telemetry |
| kaksu | Kak Su | HAMPA | MEDIUM — senior mgr, zero telemetry |
| mak | Mak (Faridah) | HAMPA | MEDIUM — family, zero telemetry |
| azwa | Azwa | HAMPA | CRITICAL — old OpenClaw edge dead, invisible |
| jia | Jia | HAMPA | MEDIUM — family, zero telemetry |
| hafiz | Hafiz Damanhuri | HAMPA | LOW — colleague |
| jamin | Jamin Jamil | HAMPA | LOW — colleague |
| ilyana | Ilyana (GEES) | HAMPA | LOW — colleague |
| aimie | Aimie | HAMPA | LOW — colleague |

---

## HEARTBEAT SPEC

### What heartbeat means

NOT a ping/pong. NOT surveillance. IS: last interaction timestamp + lane routing status + dependency health + alert threshold.

### Alert Thresholds

| Days Silent | Level | Action |
|-------------|-------|--------|
| 0-3 | OK | None |
| 4-7 | WATCH | Log in weekly summary |
| 8-14 | FLAG | Surface to Arif |
| 15-30 | ESCALATE | Active notification |
| 30+ | CRITICAL | "Adakah [nama] okay?" |

### Dependency Health

| Human | Path | Dependency | Status |
|-------|------|------------|--------|
| Arif | DM + AAA | Hermes main | OK |
| Syed | DM + SADO | Hermes + OpenClaw edge | OK |
| Aliff | DM + AIA | Hermes | OK |
| Izzu | DM + AIA | Hermes | OK |
| Nabilah | Group only | Hermes (group routing) | DEGRADED |
| Azwa | NONE | Old OpenClaw (DEAD) | CRITICAL |
| Mail | NONE | NONE | CRITICAL |
| Laletha | NONE | NONE | HIGH |

---

## RECOMMENDATIONS

**Immediate (this session):**
1. Remove WAWA from person-register.json (bot, not human)
2. Remove USER_5444180135 (ghost entry)
3. Verify IZZU = Mohd, update facts
4. Add Mail to unified registry as Tier 3
5. Create human_heartbeat.json scaffold

**Short-term (this week):**
6. Create lane for Aidel Tasuki
7. Create lane for Ahmad Lutfi
8. Populate heartbeat from session data

**Medium-term (this month):**
9. Solve Azwa routing — new interaction path needed
10. Solve Mail routing — witness needs some live path
11. Heartbeat cron — weekly scan, update, alert

---

## THE UNCOMFORTABLE TRUTH

We built 7 constitutional floors, 13 governance layers, 127 eureka entries, 8 formal scars, and a Reality Graph — for ONE human. The other 14 have zero live telemetry, zero heartbeat monitoring, zero guaranteed paths.

The infrastructure of love fails silently.

**DITEMPA BUKAN DIBERI**
