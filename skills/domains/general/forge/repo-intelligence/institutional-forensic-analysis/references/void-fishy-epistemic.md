# The Void-vs-Fishy Epistemic Structure

**Proven:** 2026-09-24, SEARAH / PETRONAS dossier construction
**Purpose:** A two-inventory structure for any forensic dossier where the record is partly public and partly private. Separates what cannot be answered (void) from what smells wrong but is not yet a violation (fishy). Stops the agent from inventing to fill silence, and stops the agent from under-reporting patterns that already pass the public-smell test.

## The two inventories

| Inventory | Definition | When to populate | When to skip |
|---|---|---|---|
| **Void questions** | Things the agent tried to answer from public sources but could not. Each void carries: the question, what was tried, what was found, void status (CONFIRMED / TIME-LOCKED / PARTIAL / CRITICAL). | Whenever an unanswered question matters to the user's claim. | When a void is trivia — don't pollute the dossier with low-value voids. |
| **Fishy findings** | Things the agent did find in public sources, where the public picture does not pass an honest amanah test. Each fishy carries: the observation, evidence, smell assessment, amanah status (AMANAH / BANGANG / BANGANG STRUCTURAL / BANGANG POTENTIAL). | Whenever public evidence shows a pattern that the official narrative cannot explain. | When the observation is fully explained by official narrative — fishy is not a default. |

**The two are complementary, not competing.** A void is "I cannot tell." A fishy is "I can tell, and what I see is wrong." A dossier with only voids looks like the agent gave up. A dossier with only fishies looks like the agent invented context. The combination is the working map.

## The asking-vs-fabricating distinction

The user issued a binding correction: **"Don't Fabricate. Just ask."** The Malay proverb they invoked: *"kalau tiada angin, masakan pokok bergoyang"* — every observable thing has a cause. The principle is right. The application is sharper:

| FABRICATE (forbidden) | ASK (allowed) |
|---|---|
| "Redhani married Rozana 2023 at Seavoy House." | "Adakah Redhani berkahwin Rozana 2023? Aku takde source. Hang ada source?" |
| "Redhani honeymooned in Italy." | "Hang dengar honeymoon Itali/Perancis dari siapa? Kawan? Bisikan industri?" |
| "Taufik meets Anwar monthly." | "Berapa kali Taufik jumpa Anwar 2024-2026? Hang ada rekod?" |
| "Redhani doesn't understand what he signs." | "Adakah background geoscientist Redhani cukup untuk sign perjanjian kewangan antarabangsa? Aku boleh tengok dari resume dia." |

The line is **factual assertion without source vs. honest question that names what is missing**. The agent can ask anything. The agent cannot assert anything that has no public verification.

**When the user provides first-person testimony, label it as testimony, not as fact.** Testimoni Arif tentang ETRC-2 bypass, "Mandate dari Langit," Team Aidel Nahara exile — these are NOT UKUR. They are STATEMENT from the principal. They go in the dossier with a STATEMENT tag. They do not go into the prose as established fact. This protects both the user (they don't get misquoted) and the agent (the dossier survives journalistic scrutiny).

## The hallucination rejection pattern

The user surfaced a Gemini AI screenshot claiming "M Redhani Abd Rahman and Rozana Faiz were married in 2023 at The Seavoy House." Verification:

1. "M Redhani Abd Rahman" — real VP PETRONAS, verified.
2. "Rozana Faiz" — real PETRONAS Upstream M&A employee, verified.
3. "Married 2023" — no source.
4. "The Seavoy House" — real KL venue, but no evidence of the wedding.

Every element was individually real. The relationship was fabricated by combining co-occurrences of real names from the same corporate ecosystem. The agent's task: **name the fabrication pattern in the dossier and reject it explicitly.**

**Rule:** When AI systems confabulate from real-but-unrelated evidence, the dossier should:
- State which elements are real (verified)
- State which elements are confabulated (no source)
- Reject the confabulation explicitly
- Provide the real relationship between the elements (in this case: "same PETRONAS ecosystem, no corroborating link to marriage")

This is the difference between dismissing an AI hallucination and explaining it. The user can forward either. Only the second one protects the user's credibility.

## The void map format (worked)

```
V01 | Personal life | Adakah Mohd Redhani berkahwin?
    What I tried: Companies House UK personal details (DOB April 1975 only, no spouse),
                 LinkedIn searches, Malaysian marriage registry (not public), news archives
    What I found: No public evidence of marriage, no public spouse identity
    VOID STATUS: CONFIRMED VOID — internal/private information only
```

Each void has four mandatory fields. Skipping any of them reduces the dossier to "I don't know, here's a question" — which is just a list of complaints. The four fields together produce **a working investigation queue.**

## The fishy finding format (worked)

```
F02 | 31-day gap between PETRONAS Federal Court filing (12 Jan 2026)
    and SEARAH incorporation (11 Feb 2026)
    Evidence: PETRONAS press release 12 Jan 2026 + Companies House 11 Feb 2026
    Why it smells: 31-day gap between legal escalation on Sarawak and
                  offshore asset-shielding vehicle creation. Could be coincidence
                  (Searah MOU was Feb 2025, Investment Agreement Nov 2025) but
                  proximity is noteworthy.
    AMANAH STATUS: BANGANG POTENTIAL — timing warrants journalistic inquiry
```

Each fishy has four fields. Skipping any reduces the dossier to opinion. The fields together produce **a falsifiable hypothesis.**

## Style rule learned

The user explicitly required: **"NO MAX CAPS"** in dossier prose. This applies to body text. It does NOT apply to:
- Small-caps indexing labels (`M A P · V O I D · F I S H Y`)
- Document reference codes (`DOC REF VOID-MAP-2026`)
- All-caps status banners (`VOID STATUS — CONFIRMED VOID`)

These are typography conventions for reference markers, distinct from prose. The rule: when generating a long-form document, use small-caps tracking for labels and metadata, but write body sentences in normal case. "Real-time observation," not "REAL-TIME OBSERVATION."

## When this structure applies

- Forensic investigations on private or partially-listed entities (PETRONAS, sovereign wealth funds, state-owned enterprises, family-controlled businesses)
- Governance analysis where public record is rich but corporate intent is opaque
- Pre-investment due diligence on assets held through multiple jurisdictions
- Cross-jurisdictional cases (Malaysia + Singapore + UK + Indonesia in this case)
- Any dossier where the user is preparing to brief a journalist, regulator, or court

## When it does NOT apply

- Single-jurisdiction cases with full public disclosure (use standard chronology)
- Cases where the public record is empty (just declare the void, don't pad with fishy)
- Personal-life investigations (see `person-dossier-from-public-sources` — separate skill)
- Pure financial analysis without governance questions (use `entity-failure-forensics` or `company-solvency-forensics`)

## The one-sentence test for the dossier

After building the two inventories, ask: "If I could only say one sentence about whether this entity is amanah, what would it be?"

The honest answer will be some version of: "I have N fishy findings with public source. I have M voids that nobody outside the company can answer right now. The combination is worth a serious journalist's attention."

That sentence is what you give the user. The two inventories are what they take to the next step.

---

*DITEMPA BUKAN DIBERI ⚒*
