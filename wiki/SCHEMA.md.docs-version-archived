# arifOS Wiki — Schema

**Version:** 1.0.0 | **Epoch:** EPOCH-2026-04-23 | **Authority:** Muhammad Arif bin Fazil

> *"The wiki is a persistent, compounding artifact."* — Karpathy/autoresearch

---

## Purpose

The wiki is the structured knowledge layer between raw sources and query answers.
It pre-synthesizes context so the agent doesn't re-derive it from scratch every session.

---

## Wiki Structure

```
docs/wiki/
├── SCHEMA.md          ← This file. Conventions for maintaining the wiki.
├── INDEX.md           ← Catalog of all wiki pages with one-liners.
├── LOG.md             ← Chronological append-only record of wiki evolution.
├── geox/              ← GEOX spatial reasoning concepts
├── arifos/            ← arifOS constitutional kernel concepts
├── federation/        ← AAA federation and agent-to-agent protocol
├── nine-signal/       ← Nine-Signal monitoring and observability
└── investigations/    ← Structured findings from investigations
```

---

## Page Convention

Every wiki page must have:

```markdown
# [Topic Name]

> **CLAIM** | **PLAUSIBLE** | **HYPOTHESIS** | **ESTIMATE** | **UNKNOWN**
> Source: [file or URL] | **Confidence:** [0.0–1.0] | **Epoch:** [date]

## Summary
One-paragraph answer to: "What do I need to know about this?"

## Key Claims
- **Claim:** [fact] — Evidence: [source]
- **Claim:** [fact] — Evidence: [source]

## Cross-References
- [[arifOS/Floors]] — related concept
- [[GEOX/RATLAS]] — related concept

## Status
- **Stable** | **Evolving** | **Stale** | **Orphan**
```

---

## Naming Convention

- Directory: `Topic/Subtopic.md` (capitalized, no spaces)
- Cross-reference: `[[Topic/Subtopic]]`
- Tags: `#arifos` `#geox` `#federation` `#observability`

---

## Ingest Rules

When a new source is added to the workspace:
1. Create or update a wiki page under the appropriate directory
2. Add entry to LOG.md with `+` prefix (new page) or `~` prefix (updated)
3. If existing page contradicts new source → flag in **Status** as `⚠️ CONFLICT`
4. Update INDEX.md to reflect new/updated pages

---

## Lint Rules (Run on every memory consolidation)

Check each page for:
- [ ] Orphan links (references to non-existent pages)
- [ ] Stale claims (evidence source no longer accessible)
- [ ] Untagged assertions (no CLAIM/PLAUSIBLE/HYPOTHESIS marker)
- [ ] Missing cross-references (related concept not linked)

---

## Maintenance

- **Ingest:** On new source addition
- **Lint:** On every memory consolidation cycle
- **Log:** On every page create/update
- **Prune:** Every 90 days — remove pages with `Status: Orphan` > 30 days

---

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE