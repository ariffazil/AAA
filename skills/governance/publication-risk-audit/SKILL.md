---
name: publication-risk-audit
description: "Use when auditing published content for legal exposure."
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [audit, publication, defamation, employment, insider-claims, provenance, risk]
    category: governance
    related_skills: [makcikgpt-article-forging, civic-shadow-editorial, claim-receipt-discipline]
    floors_protected: [F1, F2, F4, F6, F13]
---

# Publication Risk Audit

Audit a body of already-published or about-to-publish material for claims that carry legal,
employment, or institutional exposure — and hand back a candidate inventory, not an opinion.

## When to use

- The principal publishes adversarial commentary about his own employer, a GLC, a ministry, or a
  named individual — while still employed by one of them.
- He asks any variant of: "kalau kena saman?", "is this safe?", "will this get me fired?",
  "what can they come after me for?", "audit my articles".
- A corpus has grown large enough that no one remembers what each piece claims.
- Before a publication push, a cross-post, or handing content to a third party.

## ⛔ THE FOUR STANDING RULES

These hold on every instance. They are not negotiable by convenience.

**1. You produce an inventory, never a legal conclusion.**
You are not a lawyer and must not reason as one. Output = *sentences a lawyer would pull first*,
with the reference and the class. Always close with: this is not legal advice; a Malaysian
employment/defamation solicitor should read it before any action. Saying this once is enough — do
not hedge on every line.

**2. The PAIRING rule — employer-identifying byline + non-public claims.**
Either half alone is survivable. Together they are the exposure. A piece may carry an
employer-identifying byline, or it may carry non-public operational detail, but a piece that does
BOTH has, in writing, established *serving employee + insider knowledge + criticism of the employer*.
When auditing, always report the two sets separately and state the overlap explicitly.

**3. Citable-or-labelled — every number.**
Each figure needs either a public source named inline, or an explicit label that it is unverified.
Failing that label is not a style problem; it is the sentence that turns a comment into an
asserted fact. The good pattern usually already exists somewhere in the corpus — find it and hold
every number to it, e.g. *"angka RM… ialah anggaran dilaporkan — bukan quantum yang ditetapkan
mahkamah."* Quote that line back as the house standard.

**4. Inference must present as inference.**
Phrases that assert intent from a coincidence of dates or events are the hardest class to defend
because the *fact* is true and the *inference* is the publication. Flag every construction that
links two neutral facts to a motive. Rewriting them as first-person opinion is both more honest
and legally weaker — that is the point.

## Procedure

### Step 1 — Locate the corpus and confirm the shape

Source is usually TypeScript data modules with the body in a template literal:

```bash
ls /root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/*.ts | wc -l
```

Each article module has `html: \`…\`` — a single template literal holding the full HTML body.
`index.ts` is the registry (skip it); `types.ts` is the schema (skip it).

### Step 2 — Extract and score

Run `scripts/sweep-corpus.py` (packaged with this skill) — it extracts every template literal,
strips HTML, splits to paragraphs, and scores each against the risk classes:

```bash
python3 scripts/sweep-corpus.py /path/to/corpus/dir /tmp/risk-audit
```

It emits `corpus.jsonl` (every paragraph, per file) and `flagged.jsonl` (scored candidates with
the class tags that fired). **Score, then read.** The script ranks; it does not judge. Print the
top candidates and read them yourself before writing anything.

### Step 3 — Two-pass discipline (the false-positive trap)

**Pass 1 finds the SAFE material and you will mistake it for the risky material.** Keyword scoring
over-weights anything well-cited — court records, named media, statute references — because those
sentences are dense with the *vocabulary* of risk while actually being the safest content in the
corpus.

Correct sequence:
1. Run the broad keyword pass (`EMPLOYER`, `SECRET_VERB`, `LEGAL_MATTER`, `PROJECT_NAME`, `NAMED_SENIOR`).
2. Read the top hits. Expect most to be properly-sourced reporting. **Do not report them.**
3. Run the narrow pass on the classes that actually carry exposure:
   - **Invented or unattributed speech** — quoted words attributed to an unnamed person, especially
     from a closed meeting the author was not in.
   - **Causal insinuation** — neutral fact + asserted motive.
   - **Unsourced operational figure** — segment P&L, internal asset transfers, headcount, burn rates.
   - **Impropriety innuendo against an identifiable person.**
   - **First-person insider standing** — any sentence where the narrator claims to know what only
     insiders know.
   - **Reference to an unpublished internal artifact** cited as a verifying source on a public page.
4. **Search for the self-attribution sentence specifically.** Corpora like this often contain one
   line — a provenance note or byline — that names the employer and claims proprietary intelligence
   in the same clause. That single sentence can be the finding that matters most: it converts an
   anonymous-voice publication into a *named-source* publication. Grep for the employer name in
   bylines and footers, not just in the body — `--top` output in the script prints these first.

### Step 4 — Tier the findings

| Tier | What it is | Why it ranks there |
|---|---|---|
| **1 — Employment-coupled** | Articles whose text self-identifies the author as a serving employee AND carries non-public claims | This is a fidelity/confidentiality question, not a defamation one — different forum, lower bar, and the employer does not need to sue |
| **2 — Unsourced insider figure** | Specific non-public numbers with no citation | Either citable (fix by adding the source) or inside information (fix does not exist) |
| **3 — Attributed speech** | Quoted words from unnamed or private persons | Highest fabrication exposure; the one class with no defence in any regime |
| **4 — Causal insinuation** | True facts + asserted intent | Reporting ends and *adoption* begins; adoption forfeits the reporting defences |
| **5 — Named-person innuendo** | Impropriety hinted at, nothing specified | Unspecified allegations are harder to defend than specific ones — you cannot prove what you never stated |

Tier 3 is the only tier that cannot be repaired by adding a label.

### Step 5 — Write the inventory

Structure: the single most important finding first, then the tiers as tables, then the
**safe set** (material that is already properly grounded and must NOT be touched), then the
remediation menu. Include the caveat that coverage is a **floor, not a ceiling** — a claim can be
insider-only without matching any pattern used.

## Remediation menu (present as options, let the principal choose)

1. **Cite-or-label every unsourced figure** — one clause per number. Cheapest fix, largest removal of risk.
2. **Convert asserted inference to stated opinion** — "bukan kebetulan" becomes "bagi aku, urutan ni mencurigakan".
3. **Delete attributed speech from closed settings** — no label can repair it.
4. **Cut the self-attribution sentence** — the provenance note claiming proprietary intelligence.
5. **Break the pairing** — keep the byline and strip the insider claims, or keep the claims and
   strip the byline. Present this as **one binary choice**, never a menu of five; it is the decision
   that resolves Tier 1 and only the principal can make it.

Do the mechanical fixes (1–4) yourself when asked. **Never make the choice in 5 for him** — it is a
career decision, not an editorial one.

## Reporting the result — lead with the consequence

Deliver the finding, not an inventory of the artifact. The correction that fires when handed a
well-organised document instead of a verdict: *"So what??"* — meaning, land on the decision it forces.

Order of delivery:
1. **The one sentence that matters most** — usually the self-attribution line, quoted verbatim.
2. **The mechanism** — why it converts the piece from anonymous voice to named source.
3. **The asymmetry** — who is actually dangerous. Institutions that sue are rarely the threat; the
   ones that are quiet, patient, and hold a contract are. A show-cause letter is cheaper than a writ.
4. **The tier tables** — reference material, after the point is made.
5. **One binary decision** at the end.

Do not open with the file path, the page count, or the method.

## Pitfalls

- **Do not report the well-cited material as risk.** Dense legal vocabulary is a signature of careful
  sourcing. Flag the *uncited* sentences, not the cited ones — reporting both buries the finding.
- **A source list is not verification.** Labelling a figure "grade C / analyst forecast" is honest
  about a gap; it does not close the gap. If asked in court what was done to verify, "it was labelled
  C" is not an answer. Say this plainly — it is the difference between the audit being useful and
  being reassurance.
- **Anonymity is not protection when the text claims insider standing.** A pen-name creates
  deniability *for the other side* as much as for the author. If the corpus also asserts, in
  writing, that the author is an employee with proprietary intelligence, the deniability is gone and
  the pen-name now reads as *concealment*, which is worse.
- **Institutional silence is not safety.** Expect no reply, ever. A quiet correspondent holds the
  option; the risk is asymmetric in time, and the deadline that matters may be years out.
- **Do not verify claims against primary sources as the main deliverable.** The audit's job is to
  rank sentences by defensibility. Verifying whether each figure is *true* is a different, much
  larger task — state clearly that you did not do it, or the inventory will be read as a truth audit.
- **Legal context is jurisdiction-specific and time-sensitive.** Reason from the anchors in
  `references/insider-claim-legal-anchors.md`, and treat them as starting points for a solicitor —
  not as settled positions.

## Files

- `scripts/sweep-corpus.py` — extract template-literal bodies, strip HTML, score paragraphs against the risk classes, emit `corpus.jsonl` + `flagged.jsonl`.
- `references/insider-claim-legal-anchors.md` — Malaysian defamation and employment anchors: the fair-comment elements, what forfeits the reporting defences, the social-media dismissal line, and the criminal confidentiality provision.
