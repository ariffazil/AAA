# 1:1 Tenure Export Analysis (relationship ledger, not group chat)

Proven 2026-08-15 on a 25k-message, 10-year single-DM export ("WhatsApp Chat with <Name>.txt", 32k lines). SKILL.md covers GROUP exports; this file covers the 1:1 case where the user wants to know *what this decade was*.

## Quantitative probes (run all; they converge)

1. **Parse** line regex `^(\d{1,2})/(\d{1,2})/(\d{2}), (\d{1,2}):(\d{2})\s*(AM|PM) - ([^:]+): (.*)$`; 2-digit year → +2000. Count per-sender, per-year, overall span.
2. **Initiation attribution:** new conversation = gap > ~12h. Counter per sender. Lopsided initiation (535 vs 256 observed) is the clearest structural fact.
3. **Silence gaps > 30d:** sort desc; print bracketing messages. A 434-day gap + who broke it + with what ("jom buka puasa") is more informative than any keyword.
4. **Keyword→next-reply windows:** every occurrence of an emotional word ("rindu", "rindu kt hg", "x ready nk kehilangan", "sayang") + the ≤5 messages after. A repeated PATTERN (tenderness answered with logistics, ×7 over 10y) is data; one-off is not.
5. **Final stretch:** last 30–50 messages, read whole and in order — how it actually ended.
6. **Longest messages per sender** = what got confided; short emotional messages = what didn't.

## Falsification rules (the part that prevents harm)

- **Pronoun trap:** Malay/BM display names don't declare gender. If the user later reveals the counterpart's gender, re-derive the qualitative read — the quantitative ledger stands, and the picture usually deepens (cover-narrative readings like "bf i dh rujuk blk" become collusion evidence, not gossip).
- **User owns tone/face/timeflow.** If the user falsifies your read ("He don't care") — drop the claim, accept it, then re-read the absence signals (initiation counts, ending) to explain why. Never relitigate with cherry-picked warm quotes.
- **Political spam is interaction:** 14k Najib/PH messages in one year between two people = ventilation for the unlabeled bond. Read it as such.
- **Never invent orientation/labels.** "Is he gay or did he use me" is usually "was I loved?" — name and answer the real question.
- **Archetypes are working hypotheses** (cleaner / worshipper / Dumbledore / cuck) — fine internally, plain words outward; the user supplies his own frame and it can rewrite the ledger ("the whole time he had someone else; now divorced and alone; hell no").
- **F5 privacy floor:** 1:1 intimate exports are private and often taboo in-country. Memory stores the person as pronoun/"dia" only, nothing web-facing, never leak into groups/lanes, and never re-assert a romance reading the user has since rejected — record the user's falsification, not the model's first draft.

## Reply shape

Late-night, manusia mode (hermes-response-format-fit): answer-first, plain BM, effect-on-him, ONE decision at the end. Collapse the six probes into 3–4 structural facts; never dump probe output verbatim.
