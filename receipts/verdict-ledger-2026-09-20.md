# Verdict Ledger — 2026-09-20 FI-008
> Triggered by external verdict: "BIJAKSANA di tulang, biasa di dading, satu bahagian memang bangang"
> Method: every number below is measured, not asserted. Probe → measure → verify → repair → witness.

---

## 1. Claimed Numbers vs Measured Numbers

| Claim | Measured | Δ | Status |
|---|---|---|---|
| 186 doktrin fragment dalam AAA/instructions | **186** .md files | 0 | ✅ TRUE |
| 34 masuk briefing agent | **18** curated in /root/AGENTS.md header | −16 | ❌ overstated by 47% |
| 217 pointer tergantung bawah "unrendered" | **168** in UNRENDERED_FRAGMENTS footer | −49 | ❌ overstated by 29% |
| 712 fail doktrin | **6,497** .md under /root/AAA (excl backups/retired) | — | ❌ ambiguous metric |
| 668 skills | **606** SKILL.md in AAA/skills + 74 in .kimi-code/skills | — | ~close |
| 34 service hidup | **38** federation-relevant running (of 104 total) | +4 | ~close |
| 52k receipt | **244,999** jsonl lines in VAULT999; **3,142** in wealth/receipts.jsonl | — | understated (if counting all) |

### Key facts from measured data:
- 168 unrendered fragments ≠ dead. **165 of 186** are referenced somewhere in scripts/config/other docs.
- Only **21 instruction fragments** are neither rendered nor referenced by any surface — true orphans (on-demand reachable only).
- 12 fragments in the fragment table carry unratified status (7 DRAFT + 3 DRAFT_AWAITING_F13 + 2 PENDING_F13).

---

## 2. The Real Defect Found (not in the verdict)

**Phantom provenance**: 13 live warga identity files cited `/root/AAA/instructions/citizen-status-binding.md` as "canonical, F13-ratified 2026-09-14".

**Probed state**: file does not exist; never tracked in git; absent on all accessible federation nodes; no successor file found. The citation is unverifiable.

**11 dangling pointers total** in live AGENTS*.md:
- 4 files in agents/opencode/ → archived elsewhere
- 1 KERNEL_SCRIBE.md → NONE
- 1 AAA_HUMAN_SPEECH_RULE.md → archived at governance/.archive-2026-08-29/
- 1 citizen-status-binding.md → PHANTOM (no file, no archive)
- 1 cbi-doctrine-bridge.md → NONE
- 1 nist-rmf-oecd-mapping.md → NONE
- 1 AUDIT-skill-atlas/SKILL.md → moved to skills-retired-20260826/
- 1 prompts/INIT.md → archived

---

## 3. Repair Executed (17 edits, 16 files)

All reversible; changes tracked in git working tree.

| Class | Files | Action |
|---|---|---|
| Phantom citizen-status-binding.md citation | 13 agent identity files | Marked `⚠️ PHANTOM` with probed date and F13 binary requirement |
| nist-rmf-oecd-mapping.md in AAA/AGENTS.md | 1 | Status → `MISSING_SOURCE (probed 2026-09-20)` |
| cbi-doctrine-bridge.md in AAA/AGENTS.md | 1 | Status → `MISSING_SOURCE (probed 2026-09-20)` |
| AUDIT-skill-atlas/SKILL.md | 1 (skill-auditor) | Retargeted to skills-retired-20260826/ (real location) |
| AAA_HUMAN_SPEECH_RULE.md | 1 (grok-build) | Retargeted to governance/.archive-2026-08-29/ (real location) |

Verification: `grep 'citizen-status-binding.md (canonical' agents/ | wc -l` → **0** (was 13).

---

## 4. What Was NOT Done (and Why)

| Candidate | Why not |
|---|---|
| Mass prune of 168 unrendered fragments | 165/186 are referenced; 21 true orphans are on-demand reachable. Deletion = canonical-record mutation = F13-class binary required. |
| Mass retirement of 606 skills | Retirement requires F13-class binary (direction-of-record change). Precedent: 175 skills already retired (skills-retired-20260826/). |
| Fix 4 opencode archived pointers | Pointers live in archived files; no impact on live systems. Not prioritised. |

---

## 5. Diagnosis (honest, from evidence)

The verdict's **three core insights survive**:
1. Capability-not-authority is correct engineering. The reference monitor design is sound.
2. Produced ≠ sent ≠ delivered ≠ observed ≠ acknowledged — the receipt chain is real.
3. "Tiada data" = not safe ≠ safe — the failsafe design is genuinely humble.

The verdict's **structural critique is substantially correct**:
- More written than executed: 168 unrendered vs 18 curated.
- Single point of failure: F13 seal is bottleneck (every HOLD depends on one person).
- Internal-only validation: the system grades itself.

The verdict's **numbers are partly wrong** (see table above). The most serious factual error: it diagnosed 217 dangling pointers as "unrendered fragments" — but the real dangling pointers are **11 provenance citations** pointing at files that don't exist, including a phantom canonical source cited in 13 warga identity files. That defect was not in the verdict.

The verdict's **prescription (buang)** is directionally correct but operationally requires F13 binary for doctrine/skill corpus changes. What FI-008 executed today is the class of removal that IS autonomous: removing false claims from provenance records.

---

DITEMPA BUKAN DIBERI ⚒️