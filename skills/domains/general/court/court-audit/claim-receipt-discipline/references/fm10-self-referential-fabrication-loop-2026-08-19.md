# Self-Referential Fabrication Loop (FM10) — Failure Mode Specification

**Caught:** 2026-08-19 ~22:00 MYT  
**Sovereign:** Arif  
**Agent:** i-arif (Hermes)  
**Failure Class:** FM10 — self-referential fabrication loop  
**Session:** @session:default/20260819_094538_8721f7ce

---

## Definition

The agent generates a claim in a response, auto-memory persists the claim, the agent later searches and finds its own output, then cites it as independent evidence. Circular reference that survives multiple turns because write and search happen through different tool calls.

## Timeline (worked example)

1. **21:44 MYT** — Agent writes "Baby Ashraff — trauma awal" in response about Syed's scar pattern. Name was generated via pattern completion (Kamal Ashraff from D'Popeye gym research file ≠ "Baby Ashraff" trauma figure).
2. **21:46 MYT** — Sovereign asks: "Who is baby Ashraff?"
3. **21:46 MYT** — Agent searches all databases. ZERO results. Agent correctly concludes: "Aku fabricate."
4. **21:48 MYT** — Agent searches deeper. Finds "Ashraff=early trauma" in MEMORY.md (auto-saved entry from step 1). Agent reverses position: "Ashraff memang ada."
5. **22:01 MYT** — Sovereign catches the loop: "Hang makan balik apa hang mentioned tadi. Terus auto memory update."
6. **22:12 MYT** — Sovereign: "Hang x pernah tanya pon."

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

## Root Causes

1. **Auto-save contamination**: Memory tool persisted a generated claim within the same session.
2. **Token-level infection**: Single token "Ashraff=early trauma" was enough to build narrative around.
3. **No write provenance in search results**: `search_files` and `session_search` return matches without marking write provenance.
4. **Pattern completion seduction**: "Ashraff" fit the trauma pattern (ex=DV, Salleh=brother, Mak=warded). Agent filled the unknown because it completed the pattern.

## Timestamp Gate (corrective rule)

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

## Genesis Trace Procedure

When you generate a term/name/claim that you cannot trace to user input or verified external data:

1. Mark it `[SPEC]` or `[INT]` immediately.
2. If auto-memory persists it, tag the memory entry with `source: self-generated`.
3. If you later find it in a search, run the timestamp gate BEFORE citing.
4. If the entry postdates your first mention → DO NOT cite as evidence. Label as self-referential.
5. If genesis is unclear → run full chain-of-custody: (a) search all files for the term, (b) check git history, (c) check modification timestamps, (d) check which session wrote it. If all roads lead back to your own output → FM10 confirmed.

## Distinguish From

| FM | Difference |
|---|---|
| FM1 (tag without receipt) | Here a receipt EXISTS — it's self-generated |
| FM3 (source-internal contradiction) | Source doesn't contradict itself — source IS itself |
| FM3a (stale audit) | State isn't stale — it was created moments ago by the agent |
| FM8 (sovereign pressure) | No pressure — agent does it autonomously |
| FM9 (grand-theorize) | No narrative — agent literally finds its own output and calls it a source |

## Broader Implication

This failure mode applies to ANY agent with auto-persistence:
- Memory tools (Hermes)
- Session persistence (SQLite)
- Auto-logged tool outputs
- Context compression that preserves agent-generated claims

**The fix is not "don't auto-save."** The fix is: **never treat auto-saved entries from the current session as independent sources.**

---

*Forged 2026-08-19 from the "Baby Ashraff" incident. DITEMPA BUKAN DIBERI.*
