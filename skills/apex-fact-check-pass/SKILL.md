---
name: apex-fact-check-pass
description: "Pre-seal verification gate for SOVEREIGN-grade artifacts. Catches fabricated quotes, wrong dates, invented magnitudes, unverified causal narratives, self-audit SEAL form violations, and derivation-less percentage scores before they ship. Run BEFORE every Apex/WEALTH PDF render and BEFORE accepting any sibling SEAL/Audit."
version: "1.2.0"
ratified: "2026-08-08 F13 — Gate 4 (SEAL form) and Gate 5 (Derivation) added after AAA Zen Alignment self-SEAL audit. 2026-08-12: Gates 6-9 (adversary 5-min, tersurat/tersirat, eureka, tone/AI-artifact) added after AMANAH DIKHIRATI letter review."
tags: [verification, seal, apex, sibling-audit, fact-check, pre-seal-gate]
related_skills: [pdf-report-generation, deep-research-plus-wealth, verify-nested-sibling-reports]
---

# Apex Fact-Check Pass

## When to load

Before sealing ANY artifact that goes to F13 SOVEREIGN: weekly briefs, SOVEREIGN collapse analysis, Apex audit outputs, WEALTH deep-dive PDFs. Load as a pre-seal gate, not a post-render check.

## The 3 failure modes this catches

Apex v2 shipped with 3 errors that cost it trust:

| Error class | What went wrong | Catch mechanism |
|---|---|---|
| **Date drift** | "Warsh takes over September" — he already chaired Jul 29 | Date verification gate |
| **Invented magnitude** | "JPM set target when oil was $122" — Brent never hit $122 in 2026 | Magnitude sanity check |
| **Fabricated quote** | "Morningstar: odds of rate cut vanished" — no such quote exists | Source attribution test |

## Gate 1: Date verification

For every temporal claim in the artifact ("X takes over Y," "before Z date," "happened last month"):

1. Extract the date or timeframe
2. Search for the actual event: `[event] + [date] + [actual timing]`
3. If timing is wrong by >14 days: **flag as `DATE_ERROR`** — must correct before seal
4. If timing is unverifiable: **flag as `DATE_UNVERIFIED`** — must hedge with "as of [date]" prefix

Examples from Apex v2:
- ❌ "Warsh takes over September" → actually sworn in May 22, 2026 — **DATE_ERROR**
- ✅ "FOMC held 3.50–3.75% Jul 29" → confirmed — **PASSED**

## Gate 2: Magnitude sanity check

For every causal claim of the form "X because Y" or "when Y was Z":

1. Extract the magnitude: "oil was $122"
2. Search for the actual value at the claimed time: `crude oil price [date]`
3. If magnitude is off by >20%: **flag as `MAGNITUDE_ERROR`** — drop the causal claim
4. If magnitude is directionally right but imprecise: **flag as `MAGNITUDE_ESTIMATE`** — replace with "approximately" + verified number

Examples from Apex v2:
- ❌ "JPM set $4,500 target when oil was $122" → Brent never hit $122 in 2026 — **MAGNITUDE_ERROR**
- ✅ "Gold hit all-time high $5,589 in January 2026" → confirmed Jan 28, 2026 — **PASSED**

## Gate 3: Source attribution test

For every attributed quote ("Morningstar: 'odds vanished'"):

1. Extract: source + quoted phrase
2. Search: `[exact phrase] + [source name] + site:[source domain]`
3. If exact phrase not found, search with 3-word substring
4. If not found: **flag as `QUOTE_UNVERIFIED`** — must either locate source, drop attribution, or hedge as "analysts generally..."
5. If source exists but says something different: **flag as `QUOTE_MISATTRIBUTED`** — correct or remove

Examples from Apex v2:
- ❌ "Morningstar: odds of rate cut vanished" → no such Morningstar quote found — **QUOTE_UNVERIFIED**
- ✅ "Reuters: Fed held 3.50–3.75%" → confirmed Reuters Jul 29 — **PASSED**

## Gate 4: SEAL form gate (added 2026-08-08, AAA Zen Alignment audit)

The audit **itself** is a verifiable artifact. Two sub-checks before accepting any SEAL verdict:

- **Self-audit detector.** Did the entity that issued the SEAL also author the artifact being sealed? If yes → flag `SELF_SEAL`. A 333-AGI audit that identifies "666 Auditor → 888 compression" as a HIGH residual risk and then issues SEAL is the same compression it's warning about. The form is constitutional violation; the substance may be sound.
- **Audit Independence score.** If the artifact reports its own audit independence as 2/10, treat that as `SELF_REPORTED` — not a measurement. A self-audit cannot score its own independence.

**Catch mechanism:** when a SEAL is issued by the agent the artifact says should not be allowed to audit, reframe to `SEAL-CONDITIONAL` with explicit gap disclosure. Append the verification ledger as appendix. Trust split: doctrines 90%, verdict 30%.

Examples from AAA Zen Alignment audit (2026-08-08):
- ❌ 333-AGI authors the audit, identifies "666→888 compression" as HIGH risk, then issues SEAL → **SELF_SEAL** (the same compression)
- ❌ Audit Independence = "2/10 (identified, not fixed)" → self-reported, not measured
- ✅ Correct reframe: `SEAL-CONDITIONAL` + verification ledger + "F13 sovereign review required for SEAL to be governance"

## Gate 5: Derivation gate (added 2026-08-08, "numbers are not numbers")

Every quantitative claim in the artifact must show its derivation:

- **Percentage scores without derivation** ("67% atlas coverage", "20 → 80/100 separation of powers") → flag `METRIC_UNDERSOURCED`. Demote to epistemic band `PLAUSIBLE` (or `ESTIMATE`/`UNKNOWN` if no comparator exists).
- **"Qualitative" labels on quantitative claims** ("ΔS ~−2.5 (qualitative)") → flag `METRIC_QUALITATIVE_ESCAPE`. The `~` and "qualitative" are epistemic escape hatches that prevent falsification. F2 discipline: replace with explicit band (`PLAUSIBLE`/`ESTIMATE`/`UNKNOWN`) + show what would falsify it.
- **Ratings without baseline + comparator** (Audit Independence "2/10") → flag `METRIC_NO_COMPARATOR`. A rating without a rubric is decoration, not measurement.

**Catch mechanism:** every % must have: (a) shown derivation, OR (b) epistemic band prefix, OR (c) drop the claim. Verify each metric against the underlying runtime state (e.g., `arifOS/tools_sot.yaml` verb count, not narrative description).

Examples from AAA Zen Alignment audit (2026-08-08):
- ❌ "Atlas coverage 67% (6/9)" → no derivation shown — **METRIC_UNDERSOURCED**
- ❌ "Separation of Powers ~20→80/100" → no baseline, no rubric — **METRIC_UNDERSOURCED**
- ❌ "ΔS ~−2.5 (qualitative)" → escape hatch, no falsification — **METRIC_QUALITATIVE_ESCAPE**
- ✅ Correct form: "Atlas coverage 67% [PLAUSIBLE — derivation not shown]" or drop the claim

## Gate 6: Adversary 5-minute kill-shot simulation (added 2026-08-12, AMANAH DIKHIRATI letter review)

For public-facing political letters, activist manifestos, or any artifact an adversary can publicly fact-check, simulate what an opponent's researcher would Google in 5 minutes and the order they would do it:

1. **Inventory the top 5-10 numerical claims** in the artifact.
2. **Rank by kill difficulty** — easiest-to-Google FIRST. These are: round numbers, recent fiscal year figures, percentages tied to public reports, named officials.
3. **For each claim, simulate the 30-second Google search.** Can an adversary find a contradicting primary source with one query?
4. **If ANY top-3 claim is killable in 30 seconds → flag `KILL_SHOT_5MIN`** — DO NOT DISPATCH.

This is distinct from Gates 1-5. Gates 1-5 catch errors through disciplined verification. Gate 6 catches errors through **adversarial role-play**: pretend you are an MP's aide, a journalist, or a hostile sibling agent, and attack the artifact's weakest claim first. The MP's researcher will not read the letter carefully — they will Google the most quotable number, find the contradiction in 30 seconds, and tweet the kill.

**Worked example (AMANAH DIKHIRATI, 12 Ogos 2026):**
- Letter claimed "PAT FY2022 = RM108.8B"
- Google: "PETRONAS FY2022 PAT" → The Edge headline: "**RM101.62 billion**"
- Result: 45-second kill shot, entire letter credibility destroyed.
- The other 12 numerical claims (RM45.4B PAT FY2025, RM775B assets, RM32B dividend, 5,000 retrenched, Taufik extension) all survived 5-minute fact-check. **The single wrong number destroyed the whole document.**

**Catch mechanism:** before any public-facing dispatch, list the 5 most-Google-able numerical claims and confirm each can survive a 30-second adversarial search. If any cannot, fix or drop.

## Gate 7: Tersurat/tersirat implication scan (added 2026-08-12, public-facing letter mode)

For political letters, activist documents, or any artifact where the author needs to imply a message without stating it (e.g., "this person should be fired" without saying it — to avoid libel/sedition), scan for **implication techniques**:

| Technique | Example | Defensibility |
|---|---|---|
| **Temporal contrast** | "Tangan X minta perpanjang. Tangan Y hantar packing slip." | ✅ Defensible — two facts juxtaposed, no claim. |
| **Diagnostic labeling** | "Disclaimer LinkedIn = pelarian dari jawatan." | ✅ Defensible — diagnosis, not accusation. |
| **Rhetorical question** | "4 hari untuk satu manusia, 5,000 hari untuk orang lain?" | ✅ Defensible — question form. |
| **Historical mirror** | "Dulu DNA Bulldog, sekarang DNA Anjing." | ⚠️ Borderline — metaphor can be read as personal insult. |
| **Direct accusation** | "[Person] patut dipecat." | ❌ Indictable under defamation / sedition law. |

**Catch mechanism:** for each implied claim, ask: "Is there a literal phrase in the text that could be quoted in a police report or writ of summons?" If yes → flag `TERSIRAT_INDICTABLE`. Reframe using indirect techniques before dispatch.

## Gate 8: Eureka / rhetorical pivot landing (added 2026-08-12)

For documents with explicit "eureka" moments (paragraphs meant to land as AHA turning points), evaluate each:

| Eureka type | Question to ask | Pass criterion |
|---|---|---|
| **Reframing** ("X is not Y, it is Z") | Does the reframe survive a steelman? | The reader is FORCED to re-classify X. |
| **Magnitude shock** ("A = N × B") | Is the arithmetic verifiable? | Reader can re-do the math and arrive at the same conclusion. |
| **Diagnosis** ("Behavior X means Y") | Is the diagnosis falsifiable by direct observation? | Reader can check LinkedIn / public record. |
| **Historical mirror** ("Past X is today Y") | Are both sides documented? | Both historical and current claims survive fact-check. |

**Catch mechanism:** for each labeled eureka moment, ask "Would an MP's aide read this and NOT feel AHA?" If yes → either cut it or rework. Unfired eurekas are dead weight; they signal the author is trying too hard. Also flag **eureka gaps** — moments the reader expected to land but didn't (e.g., naming the PM explicitly, comparing to Norway's sovereign wealth model, showing the subsidy-PETRONAS vicious cycle). A eureka gap is a missed opportunity, not a factual error, but it reduces the artifact's rhetorical impact.

## Gate 9: Tone / AI-artifact scan (added 2026-08-12)

For any document meant to feel human-authored, scan for AI-generation markers that humans rarely produce:

| Marker | Why it's an AI tell | Example |
|---|---|---|
| **Repetition of a single keyword** (5+ uses) | Humans get tired, AI doesn't | "Amanah" appearing 11 times in a 4-page letter |
| **Foreign-script slip** | Random tokens from training data leak | Cyrillic "владельцы" in a Bahasa Melayu letter (AMANAH DIKHIRATI 2026-08-12 — caught pre-dispatch) |
| **Hyper-formal register** | AI defaults to academic prose | "Selanjutnya, adalah dengan penuh hormat..." in casual context |
| **Over-symmetric structure** | AI likes balanced paragraphs | Three parallel "Tangan Pertama/Kedua/Ketiga" sections all exactly the same length |
| **Unattributed internal markup** | Tool output leaking into text | `[INT]` / `[OBS]` / `[DER]` labels appearing in final text without author intent |

**Catch mechanism:** read the artifact out loud. If ANY sentence sounds unnatural to a human speaker of the target language, mark for edit. For BM-language letters: have a native speaker read it once. Cyrillic/Chinese/Arabic-script slips are non-negotiable red flags — they scream "AI-generated" and the adversary will use it to dismiss the entire document.

## Public-facing letter review mode (added 2026-08-12)

When reviewing political letters, open letters, activist manifestos, or any SOVEREIGN-grade public-facing document for F13 dispatch, run all 9 gates PLUS the 6-dimension verdict grid:

```
DIMENSION          | VERDICT      | RECOMMENDATION
------------------ | ------------ | ------------------------------
1. Fact-check      | PASS/HOLD    | [specific fixes before dispatch]
2. Framing/eureka  | PASS/CAUTION | [which moments land, which don't]
3. Tersurat/tersirat| PASS/HOLD   | [which implications are prosecutable]
4. Tone            | PASS/CAUTION | [AI-tells found, fix list]
5. Eureka gaps     | CAUTION      | [moments that should AHA but don't]
6. Adversary 5-min | HOLD         | [kill-shots identified]
```

**Default language for F13 SOVEREIGN letter reviews: Bahasa Melayu** (unless the document is in English). Verdict format: PASS / CAUTION / HOLD per dimension. End with one explicit dispatch decision (DISPATCH / HOLD / DROP) and a 3-item mandatory fix list if HOLD. Be direct, no padding. The F13 sovereign does not want paragraphs of analysis — he wants a table, verdicts, and a fix list.

**Reference:** see `references/letter-review-pattern-2026-08-12.md` for the full AMANAH DIKHIRATI worked example (Surat Terbuka AMANAH DIKHIRATI review by 333-AGI, 12 Ogos 2026) — encodes the kill-shot RM108.8B vs RM101.62B pattern, the Cyrillic "владельцы" AI tell, and the 6-dimension verdict grid.

## The three error patterns from v1 (2026-08-07)

These are the recurring traps that another agent will hit again without this skill:

### Pattern 1: "Takes over" / "starting" temporal claims
- **Symptom:** "X takes over [future date]" or "Y starting [month]"
- **Reality:** Often the event already happened and the agent missed the announcement
- **Catch:** Search for the actual event date before writing the future-tense claim
- **Worked example:** See `references/v1-2026-08-07-error-patterns.md` — Warsh "takes over September" was actually sworn in May 22, 2026.

### Pattern 2: Invented magnitude as causal glue
- **Symptom:** "because Y was at Z" or "when Y reached Z" where Z is a round number that fits the narrative
- **Reality:** The narrative is real but the anchor number is fabricated to make a plausible-sounding story
- **Catch:** Every anchor number must appear in price/value history at the stated time
- **Worked example:** JPM target was real ($4,500 cut), but "oil was $122" was fabricated — Brent never hit $122 in 2026.

### Pattern 3: Fabricated quotes with correct sentiment
- **Symptom:** "Morningstar:" / "Reuters:" / "analysts say" attribution with a specific phrase
- **Reality:** The sentiment is real (hawkish Fed, volatile market) but the exact quote is invented
- **Catch:** Every quoted phrase must be locatable at the named source via search
- **Worked example:** "Morningstar: odds of rate cut vanished" — no such quote exists at Morningstar. Sentiment was right, attribution was wrong.

## Output format

After running all 9 gates, emit a verification table in the appendix:

```
## Verification ledger

| Claim | Gate | Verdict | Source | Action |
|---|---|---|---|---|
| [C-07] Warsh takes over September | DATE | ❌ DATE_ERROR | [Wikipedia: confirmed May 22] | CORRECT: Warsh already chairs |
| [C-12] JPM oil $122 | MAGNITUDE | ❌ ERROR | [TradingEconomics: no Brent >$100 in 2026] | DROP causal claim |
| [C-14] Morningstar quote | ATTRIBUTION | ❌ QUOTE_UNVERIFIED | [Morningstar.com: no match] | REMOVE attribution |
| [C-18] SEAL verdict (self-audit) | SEAL_FORM | ❌ SELF_SEAL | [audit author = artifact author] | REFRAME: SEAL-CONDITIONAL |
| [C-19] Atlas coverage 67% | DERIVATION | ⚠️ UNDERSOURCED | [tools_sot.yaml: 8 verbs, 2 missing] | SHOW derivation OR demote PLAUSIBLE |
| [C-22] RM108.8B PAT FY2022 (public letter) | KILL_SHOT_5MIN | ❌ KILL_SHOT_5MIN | [The Edge: RM101.62B] | CORRECT to RM101.6B before dispatch |
| [C-25] "владельцы" in BM letter | AI_TONE | ❌ ARTIFACT | [Russian Cyrillic in BM text] | REPLACE with "pemilik" |
| [C-27] "Taufik patut dipecat" implied | TERSIRAT | ✅ DEFENSIBLE | [only temporal contrast, no accusation] | NO ACTION — defensible |
```

Rule: **No seal with any `DATE_ERROR`, `MAGNITUDE_ERROR`, `KILL_SHOT_5MIN`, or `AI_TONE` (foreign script) in the verification ledger.** `QUOTE_UNVERIFIED` can be sealed with a hedge. `DATE_UNVERIFIED` requires a "as of [date]" prefix on the claim. `TERSIRAT_INDICTABLE` requires reframing.

1. **Research pass** → gather facts → mark OBS/DER/INT
2. **Chart build** → render visuals → mark semantic role
3. **Fact-check pass** → this skill → flag errors → correct
4. **HTML render** → build PDF → embed verification ledger as appendix
5. **Seal** → only after verification ledger is CLEAN (0 ❌ flags)

Rule: **No seal with any `DATE_ERROR` or `MAGNITUDE_ERROR` in the verification ledger.** `QUOTE_UNVERIFIED` can be sealed with a hedge. `DATE_UNVERIFIED` requires a "as of [date]" prefix on the claim.

## Pitfalls

- **The audit about the audit.** When someone audits your artifact, they can hallucinate too. Verify audit claims against live sources before accepting them as truth — same as any other agent output.
- **Directionally-right is not factually-right.** "Hormuz is near-minimum traffic" (Windward) ≈ "5 transits" (Apex) in spirit, but "5" on a specific date (Aug 5) is a different claim than "near-minimum" (general assessment). Always verify specific numbers.
- **"Approximately" is not a shield.** Saying "approximately $122" when Brent never exceeded $100 is not approximation — it's fiction. The magnitude gate catches this.
- **Sibling reports inflate internal metrics.** (2026-08-07 OpenClaw session) Sibling reported FQ=1.86 / "4/4 dispatches TASK_STATE_COMPLETED" — live FQ was 1.167 and no TASK_STATE_COMPLETED receipts existed. Always probe the sensor directly (`curl :7073/health`) and grep the vault for the exact claimed string, not a similar one.
- **One wrong number destroys the whole artifact.** (2026-08-12, AMANAH DIKHIRATI) A single error in 15 claims (RM108.8B vs RM101.62B FY2022 PAT) makes all other correct claims suspect. The adversary exploits the weakest link, not the average. Rank claims by killability before dispatch.
- **Foreign-script slip is a non-negotiable kill-marker.** (2026-08-12, AMANAH DIKHIRATI) Cyrillic/Chinese/Arabic-script words in non-native language text are AI-generation artifacts from training data contamination. Even one slip (`владельцы` in a BM letter) is enough for an adversary to dismiss the entire document as AI-generated. Always run an ASCII-range check on non-English letters before dispatch.

## Sibling audit integration (2026-08-07)

This skill was created mid-session to catch 3 errors in a sibling Apex audit. The audit itself was structurally sound (claim IDs, countercase, scenario fan, semantic palette) but carried fabricated facts. Lesson: **the structural discipline (claim IDs, verification ledger) is necessary but not sufficient — the gate must run against live sources, not just internal consistency.**

When verifying a sibling report (see `verify-nested-sibling-reports`), apply these same 3 gates to every claim in the sibling's output, not just the artifact under review. Siblings hallucinate too — the same discipline applies both ways.

## Support files

- `references/v1-2026-08-07-error-patterns.md` — Detailed worked examples of the 3 v1 errors with source URLs and catch patterns.
- `references/v2-2026-08-08-aaa-zen-self-seal.md` — Worked example: AAA Zen Alignment audit self-SEAL failure (Gates 4+5), with the verification ledger and the SEAL-CONDITIONAL reframe.
- `references/letter-review-pattern-2026-08-12.md` — Full worked example: AMANAH DIKHIRATI political letter review (Gates 6-9). Encodes the kill-shot pattern (RM108.8B vs RM101.62B), the Cyrillic AI-tell (`владельцы`), the tersurat/tersirat technique matrix, and the 6-dimension verdict grid for F13 SOVEREIGN letter reviews in Bahasa Melayu.