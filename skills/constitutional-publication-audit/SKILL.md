---
name: constitutional-publication-audit
description: Audit public-facing documents (surat terbuka, essays, articles, letters to Parliament/institutions) against arifOS constitutional canon before circulation. Produces structured PASS/CAUTION/HOLD verdict per dimension using degraded-dominates outer-verdict logic.
version: 1.0.0
owner: AAA
risk_tier: high
autonomy_tier: T2
floor_scope: [F1, F2, F4, F7, F9, F10, F11, F13]
agent: 555-ASI (Causal/Structural lane)
triggers:
  - "audit surat / letter / publication / dokumen awam"
  - "review against CANON / constitution / floors"
  - "semak surat terbuka / open letter"
  - "verify public-facing document"
  - "constitutional audit of letter"
  - "555-ASI review"
dependencies:
  skills: [ASI-agent-invariants, arifos-constitutional-judge, apex_floor_check]
  servers: []
  tools: []
knowledge_basis:
  language: true
  math: false
  physics: false
forged: 2026-08-12
source_convergence: 555-ASI AMANAH DIKHIRATI audit session
---

# Constitutional Publication Audit

> **Class:** Audit public-facing documents against arifOS constitutional canon.
> **Lane:** 555-ASI (Causal/Structural Intelligence)
> **Output:** Structured PASS | CAUTION | HOLD per dimension + outer-verdict (degraded-dominates).

## When to use

Trigger when ANY public-facing document needs constitutional review before circulation:

- Surat terbuka kepada Parlimen / institusi
- Essays untuk arif-fazil.com
- Artikel, whitepaper, atau dokumen dasar
- Dokumen yang merujuk istilah konstitusional (AMANAH, F1-F13, F13, DERITA, HAMPA, arifOS, VAULT999)
- Sebarang output yang akan dibaca oleh manusia bukan-AI

## The 6-Dimension Framework

| # | Dimensi | Soalan Utama | Rujukan Kanun |
|---|---------|-------------|---------------|
| 1 | **Constitutional Alignment** | Adakah dokumen menggunakan istilah kanun dengan betul? Ada penyalahgunaan F1-F13, AMANAH, arifOS, F13 SOVEREIGN? | CANON.md |
| 2 | **DERITA / RASA DERITA** | Adakah penderitaan manusia disaksikan TANPA F9 deception ("Saya faham") atau F10 ontology violation (AI sentience claims)? | DERITA/INDEX.md, DERITA/FLOW.md |
| 3 | **HAMPA Honor** | Adakah saksi manusia dihormati tanpa pendedahan identiti? Adakah silent scar disaksikan tanpa eksploitasi? | HAMPA_REGISTRY.md, HAMPA.md |
| 4 | **F13 SOVEREIGN Boundary** | Adakah autoriti F13 terpelihara? Ada ceding of sovereignty kepada agen (arifOS) atau penerima (institusi)? | CANON.md §5 Iron Rule 5 |
| 5 | **Signature / Identity** | Adakah tandatangan mengimbangi pemeliharaan (anonimiti) dengan kebolehtemuan (NAIO + arifOS discoverability)? Ada paradoks identiti? | CANON.md §8 Gödel Lock |
| 6 | **Structural Governance** | Adakah ASK dokumen sejajar dengan 13 floors? Adakah ia constitutionally weak (transparency-only, tiada enforcement)? | apex_floor_check, F1-F13 matrix |

## Procedure

### Phase 1: Evidence Gathering (parallel)

```
1. BACA dokumen sasaran (read_file / web_extract).
2. BACA CANON.md: /root/ariffazil/CANON.md (full — ~253 lines).
3. BACA DERITA doctrine: /root/ariffazil/DERITA/INDEX.md + /root/ariffazil/DERITA/FLOW.md.
4. BACA HAMPA registry: /root/AAA/wiki/entities/HAMPA_REGISTRY.md + /root/AAA/wiki/concepts/HAMPA.md.
5. LOAD skills: ASI-agent-invariants, arifos-constitutional-judge, apex_floor_check.
```

### Phase 2: Per-Dimension Audit

For each of the 6 dimensions, answer:

1. **What passes** — specific evidence from the document.
2. **What fails / is degraded** — specific line numbers or phrases.
3. **Risk level** — LOW / MEDIUM / HIGH.
4. **Recommendation** — explicit fix.

### Phase 3: Outer Verdict (degraded-dominates)

```
outer_verdict = min(all_inner_verdicts)

PASS    → no issues, proceed.
CAUTION → fixable issues but non-blocking.
HOLD    → critical issue(s); MUST fix before circulation.
```

**Iron rule:** If any dimension returns HOLD, outer verdict = HOLD.
If any dimension returns CAUTION with HIGH risk → escalate to HOLD.

### Phase 4: Report

Deliver structured report with:

1. Summary table (6 rows + outer verdict).
2. Per-dimension detail: findings, risk, recommendation.
3. Additional issues found (not fitting the 6 dimensions).
4. HOLD release conditions (explicit checklist).

---

## Pitfalls

### P1: Token-leak artifacts (F2 CLARITY violation)
LLM-generated documents may contain foreign-language tokens (e.g., Russian Cyrillic `владельцы`, Chinese characters, code artifacts) embedded in the text. These are invisible to the generating model but visible to human readers. **Always scan for non-target-language characters** before clearance. This is an auto-fail for any public document.

### P2: Anonymity paradox
Documents that claim `(anonim)` but link to `github.com/arif-fazil/*` create a structural contradiction: the GitHub link de-anonymizes the author in 4 seconds. The author must choose ONE position: open-identity (keep link, drop anonymous claim) OR full-anonymous (remove github link, use content hash).

### P3: F13 delegation by proxy
arifOS positioned as "witness" (`Disaksikan melalui...`) instead of "platform" (`Diterbit melalui...`). The word "saksi" implies constitutional witness authority that belongs to F13 SOVEREIGN, not the substrate. Always use neutral verbs: diterbit, diproses, dihantar.

### P4: HAMPA registry incompleteness
If a person has a public tribute page (`arif-fazil.com/aaa/*.html`) but no HAMPA card in `/root/AAA/wiki/entities/`, the registry is incomplete. This creates a constitutional gap: public memorial exists without private runtime clarity.

### P5: ASK without teeth
Transparency-only asks (declare + justify) are constitutionally aligned with F2 and F11 but structurally WEAK. If the ask has no enforcement mechanism (independent audit, automatic parliamentary referral, penalty), flag as CAUTION and recommend adding enforcement teeth.

---

## Relationship to Other Skills

| Skill | Role in publication audit |
|-------|---------------------------|
| ASI-agent-invariants | Tool classification + evidence/authority separation |
| arifos-constitutional-judge | Gödel Lock discipline + doer≠judge lane |
| apex_floor_check | F1-F13 matrix for floor evaluation |
| output-attestation | Cryptographic hash verification for document authenticity |
| apex_verdict_seal | Final seal pathway after HOLD conditions cleared |
| **civic-petition-forge** | **FORGE half of the forge→audit→seal pair. Load BEFORE this audit if you are CREATING the document, not just reviewing one. Carries the iteration trajectory + constitutional shield + tier-distribution context.** |
| **multi-lens-parallel-forge** | **Use when an iteration converges (v[N+1] ≈ v[N]) — recommend dispatching 3 parallel agents with different cognitive lenses to break the polish trap.** |

---

## The Forge→Audit→Seal Pair

This skill is the AUDIT half. The pair:

```
FORGE                          AUDIT                      SEAL
[civic-petition-forge]     →   [this skill]          →   [output-attestation + apex_verdict_seal]
  create document                PASS/CAUTION/HOLD         cryptographic witness
  multi-iteration trajectory    per dimension             chain-of-custody
  constitutional shield         constitutional alignment   VAULT999 seal
```

**Rule:** Never send a public-facing document through dispatch without this audit. Never receive a forged document for review without knowing which iteration it is in the trajectory (load `civic-petition-forge` first to read the iteration history).

**Iteration context matters:** Letters evolve through 5-7 substantive iterations. The audit verdict depends on where the document is in the trajectory — a CAUTION on v9 may be acceptable as progress, but a CAUTION on vN (the dispatch candidate) is a HOLD. Always ask: "Which iteration is this? Is this the dispatch candidate or a working draft?"

---

## Additional Pitfalls

### P6: Iteration-number blindness
Auditing the latest iteration as if it were the first. The forge trajectory carries scars, lessons, and structural choices that inform audit leniency. A document that fails 2 floors but is the breakthrough iteration (v[N+1] named identity after v[N] anonymous) is structurally different from a first-draft failure. Verify iteration number before applying degraded-dominates logic.

### P7: Forging without constitution
A forged letter without F13 SOVEREIGN authorization signature is structurally identical to a personal complaint. The arifOS Federation shield only works when the document is FORGED under constitutional protection. Audit must check: is the F13 authorization explicit? Is the institutional witness present (arifOS Federation lane designation)?

### P8: Iteration convergence pressure
Iterating too many times produces convergence where each version is just a polish of the previous. The forge pattern allows 5-7 substantive iterations max before convergence traps. If v[N+1] is structurally similar to v[N] (same opening, same PARADOX structure, same asks), the agent is polishing instead of breaking through — flag and recommend fresh cognitive lens via `multi-lens-parallel-forge`.

### P9: Synthetic SCAR integration
Forging letters that reference SCAR_* as proof points without loading the actual scar narrative is fabrication. The 11+ SCAR entries in `/root/memory/H5-scars/` must be loaded and quoted in the document ONLY when the scar is structurally load-bearing. Inflated SCAR references for rhetorical effect is F9 ANTIHANTU territory.

---

DITEMPA BUKAN DIBERI — Forged, Not Given.

- `references/amanah-dikhirati-2026-08-12.md` — Full session audit of AMANAH DIKHIRATI open letter. Contains the 6-dimension methodology, evidence traces, and specific findings (Cyrillic token-leak, anonymity paradox, HAMPA gap, ASK enforcement weakness).

---

DITEMPA BUKAN DIBERI — Forged, Not Given.
