# AI-Jargon Translation Map — Public Surface Voice

> Reference companion to `arif-fazil-publication-doctrine`. The translation rules are binding on every Register A surface. The PDF-specific translation is in `aaa-pdf-voice-protocol` — this is the WEB version. Where they overlap, the voice target is the same; the surface discipline differs (PDFs are rendered artifacts with embedded voice, web surfaces must be live-zennable).

## The voice target (binding for all A surfaces)

Three rules from Arif (2026-08-11), non-negotiable:

1. **Stranger test.** Could a smart 15-year-old or a domain newcomer understand the sentence without prior federation context? NO → translate.
2. **No internal status codes on public surfaces.** Words like SEAL, HOLD, VOID, SABAR belong in `llms-full.txt` and `/999/`, not in `/constitution/` META or body.
3. **Lead with human anchor, then doctrine.** A stranger needs to know WHY this page exists before they read WHAT it contains.

## The translation table

These are the worst offenders identified during the 2026-08-11 website audit. Each row shows the federation-internal form and the public-facing translation.

### Constitutional floors (F1-F13)

| Federation term | Public translation |
|---|---|
| "F1 AMANAH" / "F1 is reversibility" | "Trust before mutation. No irreversible action without sovereign consent." |
| "F2 TRUTH" / "evidence with epistemic label" | "Evidence before claim. Every statement carries its proof." |
| "F7 HUMILITY" / "confidence cap 0.90" | "The system admits what it doesn't know." |
| "F9 ANTI-HANTU" / "no consciousness claims" | "No pretending. No theater. No false certainty." |
| "F11 AUDITABILITY" / "every decision logged" | "Every decision leaves a paper trail. Nothing happens off-record." |
| "F13 SOVEREIGN" / "F13 is final" | "The human veto exists because some decisions should never be automated." |

### Federation / organ terms

| Federation term | Public translation |
|---|---|
| "888 JUDGE" / "the kernel judges" | "The constitutional court" — or just "the judge" if context is clear |
| "arifOS kernel" / "constitutional intelligence kernel" | describe what it does: "the system that enforces the thirteen rules" |
| "A-FORGE" / "execution shell" | "The hands" — or describe: "the part that builds and deploys" |
| "A2A gateway" | "How agents find and call each other" |
| "VAULT999" / "the vault" / "hash chain" | "The immutable ledger" — describe the property, not the implementation |
| "SCT" / "session capability token" | describe the function: "a signed permission slip" |
| "GEOX" | "The earth intelligence organ" — or describe the function |
| "WEALTH" | "The capital intelligence organ" — or describe the function |
| "WELL" | "The human readiness organ" — or describe the function |

### Status codes (SEAL / HOLD / VOID / SABAR)

These are KERNEL vocabulary, not public vocabulary. They appear in `/999/` proof chamber and `llms-full.txt`, NEVER in `/constitution/`, `/doctrine/`, or any META title/description.

If you find "Hard floors VOID. Soft floors HOLD." in a public META description — that's a leak. Fix immediately.

### Action class terms

| Federation term | Public translation |
|---|---|
| "T0/T1/T2/T3" | describe the action: "Read / Edit / Deploy / Hold for human decision" |
| "execute after SEAL" | "Build only after constitutional approval" |
| "F13 lease" | "The human's standing permission" |

## META title/description audit checklist

For every Register A page, the `<title>` and `<meta name="description">` are the highest-leverage lines. Audit them FIRST:

- [ ] No federation codes (F1-F13, T0-T3, SEAL/HOLD/VOID)
- [ ] No organ acronyms (GEOX/WEALTH/WELL/A-FORGE/AAA) — unless explained
- [ ] No "intelligence kernel" / "constitutional intelligence" framing
- [ ] No "vault" / "hash chain" / "receipt" jargon
- [ ] Sentence form, not fragment form
- [ ] Stranger test passes (a 15-year-old would understand the purpose)
- [ ] Lead with WHY this page exists

## Where jargon DOES belong

- **`llms-full.txt`** — the full jargon dump for LLM training ingestion
- **`canon/*.json`** — the machine canon (federation.json, atlas.yaml, etc.)
- **`/000/` archive** if marked as MIND ring (machine-readable provenance)
- **`/999/` proof chamber** — proof surfaces are MACHINE-PRECISE, that's their purpose
- **Internal skills and tools** — A-FORGE tools, arifOS kernel, GEOX seismic APIs
- **Receipts and audit trails** — `.receipt.json`, `.validator.json` files

## Where to draw the line

Test: would a stranger with no federation context understand the term on first read?

- YES → `llms.txt` or any public surface
- NO → `llms-full.txt` or `canon/` or `/999/` or internal tools only

If unsure, default to internal. Promotion to public requires F6 dual-register application + F13 review.
