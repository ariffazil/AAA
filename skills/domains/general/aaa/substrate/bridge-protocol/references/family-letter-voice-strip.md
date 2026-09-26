# Family & Close-Circle Letter Voice — Strip Agent Markup, Hold Tersirat

> **When to load:** the artifact is a letter, voice memo, advice note, or PDF destined for the
> human's family or close friends — sibling, niece/nephew, parent, abang sado, lifelong friend.
> Anything where the recipient should read "this human wrote it for me", not "this platform
> wrote it". The trinity procedure handles multi-document drafting; this reference handles
> the **voice + provenance** layer the trinity table does not.

## The Core Law

**The named human is the speaker. The agent is the typesetter.** Agent markup, agent naming,
agent provenance, and agent signing conventions must be **absent from the rendered artifact**.
A recipient reading the PDF on their phone should not be able to tell whether a human or a
machine typed it — they should only hear the named human's voice.

This is the strictest extension of `pitfall 21` (AI-fluency detection as data) and
`pitfall 21a` (intimate letters carry zero agent markup). Where the trinity reference covers
**audience / register / shape** for parallel-document production, this reference covers
**what must NOT appear in the bytes** of any family-tier artifact.

## The Strip List

Before sending or rendering any family-tier artifact, run these checks. Each item below is a
failure mode the user has named; treat the absence of each as a send-gate condition.

| What to strip | Why | Mechanism |
|---|---|---|
| `Compiled by …` | Reads as production artefact, not personal letter | Sets the framing as corporate |
| `Identifier: <hash>` | No recipient knows what an identifier is | Forces recipient to ask "ini apa?" |
| `F13_SOVEREIGN_AT_REST`, `F13_SEAL`, `seal_id:` | Constitutional vocabulary is for /root/AAA/, not for mak and adik | Leaks platform into the family lane |
| Signature blocks (`-- `, `-- <name>`, `With regards`, etc.) | Letters to family close with the body, not with a name | The body is the signature |
| Agent naming / cross-naming (`ARIF × IRFAN`, `IRFAN · APEX-ZEN`, etc.) | Hybrid names betray that two voices wrote it | The recipient hears a committee, not one person |
| `arifOS · APEX-ZEN`, `REALITY > EVERYTHING` footers | Constitutional mottos are not letter closings | Drains the gravity of the body |
| `Authored by …`, `SOT upgrade note: …`, `Trigger: …` | Production metadata has no place in a personal artifact | The recipient is not your reviewer |
| Schema / JSON / YAML meta blocks | Engineering artefacts are not letter artefacts | Reads as debug output |
| `DITEMPA BUKAN DIBERI ⚒️`, `REALITY > EVERYTHIN... ✅` | Constitutional seals, not letter seals | Same drain — recipient reads ceremony, not intimacy |
| Production-pipeline page headers | Reveals the rendering path | Recipient wonders what pipeline wrote their letter |
| Provenance / audit lines at the end | These belong in the operational log, not the letter | Recipient doesn't need provenance for a letter |
| Footnotes `[a]`, `[1]` to internal sources | Sources belong in a memo, not a letter | The letter stands or falls on its voice |

**Mechanical check.** After rendering a family-tier PDF, run:

```bash
pdftotext <pdf> - | grep -E "Compiled by|Identifier|F13_|SOT upgrade|Authored by|APEX-ZEN|REALITY > EVERY|DITEMPA|seal_id" 
# Expected: zero hits
```

If anything returns, the letter has leaked agent vocabulary — re-draft the source markdown
without those lines and re-render. Do not patch the PDF.

## Tersirat Stays Tersirat — the Do-Not-Name Rule

When the user says `jangan sebut`, `tersirat only`, `don't mention X directly`, or equivalent,
the rule is **the named person does not appear in the rendered artifact**, period. The failure
modes:

1. **Direct naming.** "Syed tengah stress" — directly named. Always fail.
2. **Indirect naming by situation.** "Abang yang tengah struggle dengan keluarganya" — the
   recipient or the named person can decode this in one sentence. Still a fail unless the user
   has explicitly OK'd this level of indirection.
3. **Coded euphemism.** "Si hitam", "yang tengah dalam fasa gelap" — sounds opaque but
   decodes to the same person. Fail.
4. **Two-sentence deducible.** A pair of sentences that, together, identify the person even
   if neither names them directly. Fail.

**What "tersirat" can carry.** A general emotional weather ("ada orang yang hang sayang
tengah melalui masa yang payah"), a structural pattern ("hang mungkin perasan sesiapa yang
hang sayang tengah menjaga benda yang dia sendiri tak nak mengaku"), or a forward statement
("nanti bila hang stabil, hang akan jadi tempat untuk orang lain") — none of these identify
a specific person; all of them convey the felt-weight the user wanted to land.

If the user has named a person whom the letter should NOT name, the safest default is **no
reference at all** — silence is a valid tersirat when naming is forbidden. The reader
receives a letter that says nothing about the third person, and that absence IS the
message.

## Voice Register Is the Human's, Not the Agent's

When the user says "Write in BM Gen Z rojak" or "pakai bahasa kakcik" or "voice macam warkah
Azwa", the rule binds the artifact to the named human's actual speech patterns — not to a
generic register the agent imagines. Two failure modes to watch:

- **Defaulting to platform Gen-Z rojak.** The agent's training has rojak patterns, but
  those patterns may not match the named recipient's actual idiom. When in doubt, ask
  the user for one example phrase ("hang cakap rojak mcm mana, bagi sample"). One round-
  trip is cheaper than redoing the voice.
- **Code-mixing in the wrong direction.** If the named recipient writes in Penang BM with
  English technical tokens (Arif's register), the letter should preserve that mix. If the
  recipient writes pure BM kampung, the letter stays pure. Do not migrate one register
  onto another based on the platform's defaults.

**Concretely, the Penang Arif register for an intimate letter:**

- Opens with the recipient's name or relationship word, not with "Dear" or "Assalamualaikum"
- Uses "hang" for the recipient, "aku" for the writer, "kita" for shared action
- Mixes English technical tokens ("session", "framework", "deadline") without translation —
  the recipient's natural language, not the writer's
- Closes with a single action line ("Reply bila ready", "Abang ada") rather than a polite
  formula ("Sekian, terima kasih")
- Terse sentences, line-broken for breath; no paragraph longer than 4 lines on a phone
- No emoji except the closing symbol (`⚒️`) when the closing anchor carries weight
- Numbers and prices ("RM1200", "48 jam") are kept exact because the recipient needs them,
  not rounded for politeness

## Content Decisions That Belong to the User, Not the Agent

When drafting a family letter, the agent's job is **voice + structure + verification** —
not **deciding what to say on the user's behalf**. Items that should prompt a user question
before being committed to paper:

1. **Money figures.** "RM500 deposit" is a fact claim the user knows; "RM50-80 semalam for
   homestay" is research the agent did. Mixed into one sentence, the user cannot tell which
   is which. **Default:** separate the "I know" facts from the "agent researched" facts.
2. **Forecasts.** "Isnin bukan deadline, tu tarikh mula" is a reframing the agent offers.
   The user can choose to soften ("maybe slower") or sharpen ("absolutely not the deadline").
   The agent should not commit to a forecast the user has not endorsed.
3. **Emotional claims about the recipient.** "Hang ada backup" is a soft assurance; "hang
   boleh dating kat sini" is an actual offer. The difference is whether the user can be
   held to the offer tomorrow. The agent should mark which lines carry a future commitment
   and which carry only present reassurance.
4. **Medical / legal / financial claims.** These travel poorly across the agent-human
   boundary. When a letter crosses into medical advice ("hang jangan stress sangat"),
   legal advice ("hang ada hak untuk cancel"), or financial advice ("grab je homestay
   dulu"), default to **citing the source** or **recommending the human verify**. The
   agent is not in a position to certify any of these.

## Failure Modes Observed Live

- **The v1 surat Azwa pass.** Generated a 10-page PDF opening with "Compiled by ARIF ×
  IRFAN · APEX-ZEN Protocol", closing with "DITEMPA BUKAN DIBERI ⚒️ / REALITY > EVERYTHIN...
  ✅ / ARIF × IRFAN · APEX-ZEN     10 / 10", and naming "Syed" directly in the body
  despite Arif's instruction "jangan sebut." Recipient (and Arif) reads the artifact as
  **corporate + leaky**, not intimate + private. The v2 patch rewrote with zero markup
  and zero named persons — Arif's exact register, tersirat intact.
- **The markdown-source-as-pdf trap.** A pandoc-rendered PDF inherits the page-header /
  page-footer configuration of the markdown source. If the source contains a closing
  anchor after the signature block, the rendered PDF carries that closing. If the
  source contains platform mottos after a horizontal rule, the PDF carries that too.
  **Always re-read the source markdown top-to-bottom with the strip-list grep before
  pandoc renders.**
- **The same person named indirectly as directly.** A first draft may write "Abang yang
  tengah menjaga keluarga" — sounds abstract until you remember the reader knows who
  "Abang" is, and the unstated identification is the same as naming. Re-check every
  indirect reference against the named-person blocklist.
- **The "but it's true!" defense.** "But Syed memang tengah stress" — when the user has
  said not to name him, the truth of the claim is irrelevant. The user's privacy
  preferences are the gate, not the agent's assessment of the claim's accuracy.

## Companions

- `references/multi-document-drafting.md` — when the family letter is one of a trinity
  (institutional + personal + technical), the trinity procedure determines audience and
  register. This reference determines **what is absent from the rendered bytes**.
- `pitfall 21a` in `SKILL.md` — tersurat + tersirat asymmetry for Arif's own letters;
  this reference extends the rule to **all family-tier artifacts**.
- `human-meaning-membrane` — when the recipient's felt-state is the point, the
  cross-layer inference disciplines here apply as much as they do in conversation.
