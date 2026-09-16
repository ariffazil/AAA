# Entity Hallucination & Memory Provenance v2 — Worked Example (2026-08-19)

**Incident:** Baby Ashraff fabrication loop
**Sovereign:** Arif (F13)
**Agent:** i-arif (Hermes)
**Root cause:** Kata nama khas (proper noun) hallucination + self-referential memory contamination

---

## The Kata Nama Am vs Kata Nama Khas Distinction

**Kata nama am** = common nouns. "Lelaki." "Kawan." "Trauma." "Ex-girlfriend."
→ AI generates via pattern completion. Low entity-dependency. Easy to verify.

**Kata nama khas** = proper nouns. "Syed." "Salleh." "Kamal Ashraff." "D'Popeye Gym."
→ Refers to SPECIFIC entities in the physical world. High entity-dependency.

**Proper nouns are EASIER to hallucinate than common nouns, not harder.** Why:

1. **Long-tail Zipfian distribution**: Most named entities appear few times in training data. Low frequency = weak signal = high hallucination rate.
2. **Composable names**: Model learns the SHAPE of names (Malay bin/binti patterns). Can compose new names as easily as recalling real ones. No decoding signal distinguishes "recalled" from "composed."
3. **False grounding effect**: Proper noun + emotional qualifier ("Baby Ashraff") = double-grounding — reads as verified fact when it's pure construction.
4. **BM-specific vulnerability**: Malay training data less abundant than English. Personal names with bin/binti patronymic patterns have unique structure. Model fills name slots with "sounds right" more than "exists in reality."
5. **Snowballing**: Once generated and persisted, name treated as established in subsequent reasoning.

**Arif's correction:** "Bukan susah untuk AI hallucinate kata nama khas. SENANG. Dan tu yang bahaya."

---

## The Baby Ashraff Chain of Custody

| Step | Time | What happened |
|---|---|---|
| Genesis | Early Aug | "Kamal Ashraff" in D'Popeye gym research file (WFF Pro athlete) |
| Trigger | 21:44 MYT | Agent generates "Baby Ashraff — trauma awal" filling a pattern slot |
| Auto-save | ~21:45 MYT | Memory tool auto-saves "Ashraff=early trauma" to MEMORY.md |
| User asks | 21:46 MYT | "Who is baby Ashraff?" |
| Search 1 | 21:46 MYT | Zero results. Agent admits: "Aku fabricate." |
| Search 2 | 21:48 MYT | Finds auto-save. Reverses: "Ashraff memang ada." ← SECOND fabrication |
| Catch | 22:01 MYT | Arif: "Hang makan balik apa hang mentioned tadi" |
| Catch 2 | 22:12 MYT | Arif: "X kenal pon" — never asked about this name |

**Circular reference:** Agent writes → auto-memory saves → agent searches → finds own output → claims as source.

---

## Timestamp-Gate Rule

BEFORE claiming any search result as independent evidence:

```
1. When did I FIRST mention this term in THIS session?
2. When was the database entry CREATED/UPDATED?
3. Compare:
   - Entry predates my mention → independent source (maybe)
   - Entry postdates my mention → I wrote it → NOT a source
   - Entry timestamp = my mention timestamp → same turn → VERY SUSPICIOUS
   - Timestamp unknown → UNKNOWN (not "I found it")
```

---

## Proper Noun Audit (Detection)

Before emitting any proper noun NOT already in verified memory:

1. **Source check**: Can I name the specific entity? (Person, place, org — not a pattern category)
2. **Provenance check**: Name from (a) file read, (b) user statement, or (c) pattern completion? Only (a) and (b) valid.
3. **Persistence check**: If auto-memory saved this, did save happen BEFORE or AFTER my first mention? Same-session auto-saves are NOT independent sources.

---

## Memory Provenance v2 — The Patch

Schema: every memory entry carries provenance tag.

| Tag | Meaning | Use as evidence? |
|---|---|---|
| `[SG:TIMESTAMP]` | SELF_GENERATED — agent created from own output | NO — UNVERIFIED |
| `[TS:TIMESTAMP]` | EXTERNAL_REPORTED — user or external system | YES — source-dependent |
| `[SY:TIMESTAMP]` | SYSTEM_OBSERVED — tool/API output | YES — higher confidence |
| `UNKNOWN_LEGACY` | Pre-v2 entry, no provenance | NO — UNVERIFIED |

**Rollback:** Schema additive. Old entries parse as UNKNOWN_LEGACY.
4 separate commits: schema → write path → read path → gap detection.

**Files:**
- `/root/AAA/governance/memory-provenance-v2.md` — schema
- `/root/AAA/scripts/memory-provenance-v2.py` — enforcer + log
- `/root/.hermes/memories/provenance-log.md` — fabrication tracking

---

## Extended Anti-Pattern Table

| Anti-pattern | What it looks like | What to do |
|---|---|---|
| Auto-save as independent source | Agent searches own auto-saved entry, claims as external evidence | Timestamp-gate: same-session auto-saves NOT sources |
| Proper noun from pattern completion | "[Name] = [attribute]" where name from context, not entity | Source check: name must trace to file read or user statement |
| Snowball on fabricated name | Building analysis on generated name | Proper noun audit before each use |
| "I found it in MEMORY.md" after writing it | Search returns own output from same session | Timestamp-check: did entry predate first mention? |
| Kata nama khas treated as kata nama am | Treating "Ashraff=trauma" same confidence as "Syed=friend" | Proper nouns need entity verification |
| BM name pattern-filling | Model fills Malay name slots with "sounds right" names | External verification before new proper noun entry |

---

*Forged 2026-08-19 from Baby Ashraff incident + kata nama khas analysis. DITEMPA BUKAN DIBERI.*
