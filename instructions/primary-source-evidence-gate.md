# Primary-Source Evidence Gate

Status: ACTIVE UPON HUMAN RATIFICATION
Owner: AAA
Authority: ARIF
Version: 1.0
Ratification: F13 Arif, DM 2026-10-17 ("Ya, tulis P0 gate itu sekarang")
Origin: audit external × runtime probe session 2026-10-17 (von Eickstedt primary-source case)
Principle: Zero unsupported assertion at the evidence boundary.

## 1. Scope

This gate applies whenever an agent attributes a claim, quotation,
position, event, or historical interpretation to a primary source.

It governs output discipline. It does not certify source truth.

## 2. Capability States

Capability state must use this ordered vocabulary:

DECLARED → DISCOVERABLE → CALLABLE → RESPONDED → VERIFIED

VERIFIED must name the verified object:

- VERIFIED_CAPABILITY
- VERIFIED_ARTIFACT
- VERIFIED_PASSAGE
- VERIFIED_SCAN_ALIGNMENT
- SUPPORTED_CLAIM

Tool response does not imply content verification.

## 3. Source States

A primary-source claim progresses through:

SOURCE_DISCOVERED
→ SOURCE_RESOLVED
→ CONTENT_RETRIEVED
→ PASSAGE_LOCATED
→ PASSAGE_BOUND
→ CLAIM_SUPPORTED
→ CLAIM_CORROBORATED

No stage may be silently skipped.

## 4. Minimum Passage Receipt

Before an agent may assert primary-source support, it must hold:

- source_id
- artifact_sha256
- raw_snippet
- stable_locator

The locator must identify available line, page, leaf, byte,
timestamp, or equivalent source position.

Raw OCR must remain unedited. A normalized reading may be added
separately but must never replace the raw text.

## 5. Claim Relation

Every located passage must be classified as exactly one of:

- supports
- contradicts
- mentions_only
- ambiguous

Classification must inspect surrounding context, attribution,
negation, quotation, and whether the words belong to the author.

Keyword presence alone cannot produce `supports`.

## 6. Forbidden Leaps

The following implications are invalid:

- title → content
- metadata → content
- URL or DOI → claim support
- tool response → source verification
- phrase occurrence → author endorsement
- OCR occurrence → scan alignment
- one passage → broader historical interpretation

## 7. Language Gate

Without a bound passage receipt, agents must not use:

- proves
- confirms
- demonstrates
- establishes
- membuktikan
- mengesahkan

Permitted language before passage binding:

- source discovered
- metadata resolved
- content not yet verified
- candidate passage located
- interpretation remains UNKNOWN

## 8. Fail-Closed Verdicts

Missing receipt field → HOLD

Empty raw snippet → HOLD

Ambiguous OCR → UNKNOWN

Unresolved author voice → UNKNOWN

Passage only mentions the term → MENTIONS_ONLY

Contradictory context → preserve contradiction and HOLD

## 9. Negative Search Discipline

"Not found" must not be reported as "does not exist."

The agent must state:

- artifact searched
- query terms and variants
- formats inspected
- search scope
- OCR limitations

## 10. Boundary

This gate creates no authority to mutate sources, certify truth,
or issue its own SEAL.

Agents retrieve, bind, and report evidence.
AAA routes and preserves state.
arifOS judges.
ARIF remains final authority.

## Acceptance test minimum

Gate ini belum dianggap hidup hanya kerana fail wujud. Selepas tulis:

1. Hash fail dan rekod byte size.
2. Pastikan instruction loader benar-benar membaca path tersebut.
3. Uji satu kes positif dengan petikan terikat.
4. Uji satu title-only claim dan pastikan bahasa "membuktikan" ditolak.
5. Uji istilah yang muncul dalam quotation atau penafian dan pastikan ia tidak menjadi supports.
6. Simpan receipt berasingan untuk artifact, loader, dan behavior test.

Keadaan selepas fail ditulis tetapi sebelum loader/test:
DOCUMENTED, bukan ACTIVE

Keadaan selepas loader membaca dan ujian tingkah laku lulus:
EXECUTED_GATE

Ini bentuk yang betul: satu failure class, satu owner, satu gate kecil,
tiada architecture expansion.
