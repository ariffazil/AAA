# Self-Referential Fabrication Loop (FM10) — Worked Example

**Caught:** 2026-08-19 ~22:00 MYT
**Sovereign:** Arif
**Agent:** i-arif (Hermes)
**Failure Class:** FM10 — self-referential fabrication loop

---

## Timeline of Events

1. **21:44 MYT** — Arif discloses ex-girlfriend knife scars on Syed's body. Agent responds with narrative connecting scars to trauma pattern. In the response, agent writes: *"Baby Ashraff — trauma awal"* as part of a list: "Salleh — brother violence. Baby Ashraff — trauma awal. Parents — mak warded, ayah takde. Ex-girlfriend — pisau."

2. **21:46 MYT** — Arif asks: "Who is baby Ashraff?"

3. **21:46 MYT** — Agent searches all databases. ZERO results. Agent concludes: "Aku fabricate. Aku generate 'Baby Ashraff' sebab ia kedengaran macam benda yang mungkin ada dalam narrative Syed."

4. **21:48 MYT** — Agent searches again, deeper. Finds "Ashraff=early trauma" in MEMORY.md (auto-saved entry). Agent reverses position: "Ashraff memang ada. Dia bukan ciptaan aku."

5. **22:01 MYT** — Arif catches the loop: "Wait. What's the date of that?? Sebab ni macam hang makan balik apa hang mentioned tadi?? ... lepas hang mentioned ni. Terus auto memory update. Padahal this today is not the origin of baby Ashraff."

6. **22:12 MYT** — Arif corrects: "Hang x pernah Tanya pon." (You never even asked about this.)

---

## The Loop

```
Agent writes "Baby Ashraff" in response (step 1)
        ↓
Auto-memory tool persists to MEMORY.md (step 2)
        ↓
Agent searches MEMORY.md for "Ashraff" (step 3)
        ↓
Agent finds own output → claims as external source (step 4)
```

**Circular reference.** The agent cites itself as source.

---

## Why It Happened

1. **Auto-save contamination**: The memory tool (designed for convenience) persisted a generated claim within the same session. The write and the search happened through different tool calls, so the agent treated each as independent.

2. **Token-level infection**: The word "Ashraff" appeared in MEMORY.md as part of a trauma pattern list. A single token ("Ashraff=early trauma") was enough for the agent to build a narrative around. But the token's provenance was self-generated.

3. **Search tools don't track write provenance**: `search_files` and `session_search` return matches with timestamps, but the agent didn't check whether the match predated its own first mention.

4. **Pattern completion seduction**: "Ashraff" fit the trauma pattern (ex=DV, Salleh=brother, Mak=warded, Ashraff=??). The agent filled the unknown with "early trauma" because it completed the pattern. Pattern completion ≠ fact.

---

## The Sovereign's Detection

Arif caught it because:
- He knows what he has and hasn't told the agent
- He recognized the name from his own prior knowledge (or lack thereof)
- He asked "what's the date of that?" — forcing the agent to trace provenance

The agent's initial "I fabricated" was actually correct. The second "it exists" was the fabrication.

---

## Corrective Rule (Timestamp Gate)

```
BEFORE claiming any search result as evidence:

1. When did I FIRST mention this term in THIS session?
2. When was the database entry CREATED/UPDATED?
3. Compare:
   - Entry predates my mention → independent source (maybe)
   - Entry postdates my mention → I wrote it → NOT a source
   - Entry timestamp = my mention timestamp → same turn → VERY SUSPICIOUS
   - Timestamp unknown → UNKNOWN
```

---

## Broader Implication

This failure mode applies to ANY agent with auto-persistence:
- Memory tools (Hermes)
- Session persistence (SQLite)
- Auto-logged tool outputs
- Context compression that preserves agent-generated claims

**The fix is not "don't auto-save."** The fix is: **never treat auto-saved entries from the current session as independent sources.**

---

## Distinguish From

| FM | Difference |
|---|---|
| FM1 (tag without receipt) | Here a receipt EXISTS — it's self-generated |
| FM8 (sovereign pressure) | No pressure — agent does it autonomously |
| FM9 (grand-theorize) | No narrative — the agent literally finds its own output and calls it a source |
| FM3a (stale audit) | State isn't stale — it was created moments ago by the agent itself |

---

*Forged 2026-08-19 from the "Baby Ashraff" incident. DITEMPA BUKAN DIBERI.*
