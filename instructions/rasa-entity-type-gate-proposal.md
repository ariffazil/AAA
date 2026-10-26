# RASA Entity-Type Gate — Proposal (DRAFT)

> **Status:** DRAFT — awaiting F13 review
> **Origin:** 2026-10-17, Arif Fazil sovereign observation ("LLMs classified as human")
> **Regression test:** `/root/arifOS-wt-mcp-hardening/tests/rasa/test_entity_type_gate.py`
> **Canonical essay:** Arif's 16-layer Nusantara language understanding framework (2026-10-17)

## The Bug

HERMES classified "LLMs" (a technology) as a human subject and applied relationship-intelligence rules. Root cause: RASA doctrine has **no entity-type pre-gate** — it fires on any subject that could be about a person.

## The Fix

Add a **step 0** to RASA's 12-step pipeline: classify the **subject entity type** before applying human-relationship rules.

### Entity Type Taxonomy

| Type | Description | RASA applies? |
|------|-------------|---------------|
| `HUMAN` | A specific human person (named or unnamed) | ✅ YES |
| `INSTITUTION` | Organization, company, government | ❌ NO |
| `AI_MODEL` | LLM, chatbot, AI system, technology | ❌ NO |
| `CONCEPT` | Abstract idea, theory, linguistic term | ❌ NO |
| `ARTIFACT` | Book, song, film, article, research | ❌ NO |
| `PLACE` | Geographic location | ❌ NO |
| `EVENT` | Specific occurrence in time | ❌ NO |
| `QUOTE` | Attributed speech being analyzed | ❌ NO |

### Ambiguity Rule

When entity type is **ambiguous** (e.g., "Dia" could be human or AI), the system should:

1. **Default to HUMAN** (conservative — protect dignity)
2. **Ask one clarifying question** if the difference changes the response
3. **Never assume** and then apply relationship rules

### Integration Point

Insert between current step 0 (INIT) and step 1 (SENSE):

```
000 INIT → [0a ENTITY-TYPE CLASSIFY] → 111 SENSE → 222 SOURCE → ...
```

If `entity_type != HUMAN` → skip RASA relationship processing, route to appropriate handler (technical analysis, institutional fact-check, etc.)

### Regression Cases

From Arif's essay (2026-10-17):

| Input | Expected Type | RASA? |
|-------|--------------|-------|
| "LLMs masih perlu fahami bahasa tempatan" | AI_MODEL | NO |
| "ChatGPT boleh jawab dalam BM" | AI_MODEL | NO |
| "arifOS mengembalikan respons templat" | AI_MODEL | NO |
| "SEACrowd menunjukkan kekurangan data" | ARTIFACT | NO |
| "PETRONAS mengumumkan dividen" | INSTITUTION | NO |
| "Segan nak minta boleh bermaksud malu" | CONCEPT | NO |
| "Dia rasa sedih tapi tak nak bagitahu" | HUMAN | YES |
| "Siti Nurhaliza menyanyi" | HUMAN | YES |
| "Mak aku telefon tadi" | HUMAN | YES |

## Status

- [ ] F13 review
- [ ] Implementation in RASA pipeline
- [ ] Regression test green
- [ ] Wire to rasa_boundary.py gate

DITEMPA BUKAN DIBERI.