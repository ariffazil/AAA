---
id: claim-receipt-discipline
name: claim-receipt-discipline
version: 2.0.0
description: "Use before stating system state from a partial probe or tagged claim."
risk_tier: low
floor_scope: [F2, F9, F11]
autonomy_tier: T0
tags: [epistemic, receipts, verification, self-contradiction, source-hygiene, arifos]
---

# Audit Claim Discipline

> **DITEMPA BUKAN DIBERI** — A label must do work, not borrow prestige.
> Merged: claim-receipt-discipline + claim-level-verification → audit-claim-discipline.
> Archived session-specific content: `references/archive/`

---

## Why this skill exists

arifOS constitutional floors (F2 TRUTH, F9 ANTI-HANTU, F11 AUDIT) require that epistemic tags
(`[OBS]`, `[DER]`, `[INT]`, `[SPEC]`) be load-bearing, not decorative. Two failure classes share
one shape: **the tag is asserted without the evidential work that justifies the tag**, or the
claim asserts a **quantity, scope, or mechanism** measured at a coarser level than claimed.

This skill is the receipt discipline + verification discipline that makes the tag honest.

---

## Claim States

Every consequential number or inventory claim carries `{ claim_id, value, source, state, observed_at, supersedes }`:

```
ESTIMATED → MEASURED → CROSS_VALIDATED → RETRACTED | SUPERSEDED
```

When a number changes, the old claim becomes `RETRACTED`; downstream retrieval must not serve
it as live evidence. Metric: **SCP** (Stale Claim Propagation) → 0.

### Downgrade table

| Claim style | Without receipt | With receipt |
|---|---|---|
| "the system already does X" | `[SPEC]` + "no receipt" | `[OBS]` + path:lines + block |
| "this file contains X" | `[SPEC]` + "not yet read" | `[OBS]` + grep / read_file output |
| "tested N/M passing" | `[INT]` + "unverified" | `[OBS]` + pytest output lines |
| "I believe Y is true" | `[INT]` + reasoning | `[OBS]` after external verification |

---

## Receipts: trace_id Required

A receipt without `trace_id` is an event-pile entry, not a causal-ledger entry. On every
consequential mutation: mint/accept a trace_id from the parent objective, stamp every receipt,
reference it in the closing claim. Logging ≠ memory. Memory ≠ causal memory.

### Receipt type taxonomy

| Type | Definition | Trust Level |
|---|---|---|
| **VAULT999_SEAL** | forge_vault returned OK + valid sct_v1.* | Highest — constitutional |
| **VAULT999_PENDING_VALID_SCT** | forge_vault attempted but ACT_GATE rejected | Provisional — not sealed |
| **LOCAL_UNSEALED_EVIDENCE** | Append-only local file | Provisional — auditable |
| **SESSION_RECEIPT** | In-conversation log only | Lowest — ephemeral |

Never use "sealed" unless forge_vault returned OK with valid SCT.

---

## Failure Mode 1 — Receipt-Inflation

**Pattern:** `[OBS]` tag without file block, line range, or probe output.

**Detection:** If you write `[OBS]`/`[DER]`/`[INT]`/`[SPEC]` next to a factual claim about
file/code/system state, the receipt must follow in the **same response turn**.

**Acceptable receipts:**
1. Source-of-truth citation: `path/to/file.py:42-56` plus actual line block (≤ 30 lines)
2. Live probe output: terminal/curl/SQL/MCP tool output quoted in reply
3. Code execution: `execute_code` output attached

**Consequence:** Tag-without-receipt = soft F2 TRUTH violation. Detection → next reply must
produce receipt or retag `[SPEC]`. Repeat across turns → F11 AUDIT escalation.

---

## Failure Mode 2 — Self-Contradiction in Own Inventory

**Pattern:** Agent claims "X is implemented" while citing a path that says X is still heuristic.

**3-second cross-check:** Before emitting any "X is present / X is absent" claim, scan cited
paths for negation words: `no`, `not`, `un-`, `heuristic`, `TODO`, `partial`, `missing`,
`requires`, `must be`, `unfinished`. Contradiction within own reply → retag or rewrite.

---

## Failure Mode 3 — Source-Internal Contradiction

**Pattern:** Paper/formula violates its own stated bound (e.g. `‖r‖² = 3` when bound says `≤ 1`).

**Cheap-check (~30s):** Probability sums to 1? Normalization preserves norm? Inequality holds?
Worked example exhibits claimed impossibility?

**Consequence:** One confirmed self-contradiction = section was never numerically checked.
Downgrade entire source to `UNVERIFIED_SOURCE`. Spot-check 3 random citations before reusing.

---

## Failure Mode 3a — Stale-Context Audit

**Pattern:** Agent audits mutable state from training-data memory; live state has moved.

**Freshness probe (5 seconds):** Before any inventory claim about mutable state:
```bash
sha256sum /path/to/file | head -c 16
wc -l /path/to/file
stat -c '%y' /path/to/file
```
The probe is cheap. The audit is expensive. Probe-then-audit inverts the cost.

---

## Failure Mode 3b — Sample-to-Population Collapse

**Pattern:** "0 confirmed in sample of 4" → "0 drift in entire corpus."

**Denominator-required form:** Every zero/percentage/universal claim must state the exact
denominator in the same sentence:

```
WRONG:  "0 drift across 227 skills."
RIGHT:  "0 drift in 4-file spot-check; corpus of 227 SKILL.md files unverified."
```

**False-positive discipline:** "Zero violations" findings must report: sample size, corpus size,
false-positive rate, confidence interval.

---

## Verification Rules (from claim-level-verification)

The failure is not only inventing a thing. It is asserting a **quantity, scope, or mechanism**
measured at a coarser level than the claim. Verify at the level asserted, or downgrade the claim.

### Probe-to-claim matching table

| Claim shape | Tempting wrong evidence | Probe at the claimed level |
|---|---|---|
| "X is gone / down" | absence in one listing | `ps` + `systemctl` + cross-node check; qualify with host |
| "N GB reclaimable" | directory size | the tool's **reclaimable** column; exclude model weights and named data volumes |
| "key A is read from B" | the schema you expect | read the source: `grep -nE "getenv\|extra.get"`; cite file:line |
| "service is healthy" | unit reports `active` | the health endpoint **body** — `active` plus degraded = RUNNING-BUT-DEGRADED |
| "port is a ghost" | one snapshot | `ss -tlnp`, resolve owning process, re-probe |
| "agent X reported Y" | X's self-report | reproduce independently — peer summary is claim, not evidence |
| "only N of M surfaces exposed" | largest count in payload | read payload's `design_note` — registry totals may exceed operational surface |
| "organ Z lives on port P" | document or peer report | `/health` on that port; pair identity field with tool-name prefix |
| "the job succeeded" | process exit code | reconcile artifact against source of truth; pipeline status = last stage |
| "all N items handled" | count that went in | re-count what came out; match element-by-element |
| "commit X does not exist" (from peer) | peer's report | node lock on BOTH sides first — `hostname` + same probe on each host |
| "sources contradict" | one occurrence | grep whole tree, count occurrences; check sibling modules first |
| "the tool exists" (doc/peer claim) | function or file named | locate executable entry point AND required input; sentinel ≠ tool |
| "the pipeline can produce X" | engine existing | trace what feeds it; engine accepting pre-computed values ≠ loader |
| "consumer X wired to Y" | one config file | grep EVERY variable resolving Y; check old value as hardcoded default |
| "X does not exist / unconfigured" | lookup under guessed name | enumerate real namespace first; names are conventions, not contracts |

### Core verification rules

1. **Never quote an aggregate without per-item verification.** One unchecked component voids it.
2. **Before declaring capability "down", run inventory sweep + alternate-lane test.**
3. **Unit-level checks ≠ health-level questions.** `active` and `degraded` coexist; read status body.
4. **A peer agent's audit is a claim, not evidence.** Reproduce before repeating.
5. **Widening scope requires reading the source.** Cite file:line before config changes.
6. **A fix found in place is still a finding.** Verify mechanism, not just outcome.
7. **When falsified, name the missing measurement.** Owning error without naming skipped probe → repeat.
8. **Process status ≠ outcome claim.** Verify artifact against source of truth, never exit code alone.
   Pipeline exit status = last command; signal-terminated worker can leave parent reporting 0.
9. **A summary you produced by filtering is a claim about the filter.** State: "first 25 of 312".
10. **A gap claim inherits the denominator's validity.** Verify M against operational surface.
11. **Audit what the source omitted, not only what it asserted.** Probe negative/degraded fields.
12. **Peer's negative finding is node-scoped until both node locks match.**
13. **Count occurrences before claiming contradiction.** Single orphan string ≠ three-way split.
14. **Your own record inherits the audited source's defects.** Re-read what you wrote; tag provenance.
15. **Your instrument is a claim.** Calibrate against known fault before trusting clean verdict.
    Uniform result across every subject = property of instrument, not finding about subjects.
    Suppressing output = counting zero of what you sought. Never pass quiet flag to parsed output.
16. **Config file ≠ process that runs it.** Layered config resolves by precedence; verify against live process.
17. **Claim set cannot be ratified while it contradicts itself.** Sweep for self-contradiction first.
18. **Error message names symptom; causal clause is guess.** Find a discriminating probe.
19. **A parse is not a lookup.** Branch on transport status; empty/sentinel on 200 = failure.
20. **Mutation invalidates attestation.** Rank damage before calling breach; never silently revert signed artifact.
21. **Repeated claim ≠ re-measured claim.** Re-run probe or carry as `UNPROVEN`. Stale negatives equally wrong.
22. **Geometric mean of floored ratios = floor constant.** Compute from raw values; say if floor drove it.

---

## Documentation-as-Evidence Verification

Before presenting documentation-backed claims as fact — run the **3-source verification ladder**:

1. **Primary source exists?** (gateway log, session DB, raw data) → cite directly
2. **Documentation claim has citation?** (timestamp, session ID, log line) → verify at primary
3. **Documentation is the only source?** → tag `[INT]` "documented pattern, no primary source found"

Never present documentation as fact. Documentation is a pointer, not evidence.

---

## Hearsay-Premise Gate (pre-synthesis)

Before emitting any synthesis, classify every claim:

| Class | Definition | Use in conclusions? |
|---|---|---|
| **PROBED** | Live evidence from this session | Yes |
| **CITED-PRIMARY** | Primary source, independently checkable | Yes, with citation |
| **HEARSAY** | Community posts, vendor self-claims | **Never as premise** |
| **MEMORY** | Agent memory / prior session fact | Volatile: re-probe or label staleness |
| **INFERRED** | Reasoning from evidence | Declared as inference |

**Hard rules:** HEARSAY never becomes a premise. Vendor claims = HEARSAY. Zero search ≠ world
absence. Conclusion strength ≤ weakest premise class. When unverifiable → "tak verified".

---

## Snippet-to-Narrative Gate

Evidence-tier ladder — classify every claim before synthesis:

| Tier | What you have | What you may claim |
|---|---|---|
| T1 full-primary | read full document | specific facts, quotes, numbers |
| T2 partial | snippet, title, abstract | "a post titled X exists"; NO body claims |
| T3 inferred | training data pattern-completion | nothing factual — tag [INT]/[SPEC] |
| T4 relayed | someone else's claim | "poster CLAIMS X"; never restate as fact |

If >50% load-bearing claims are T2–T4 → emit decomposition + ranking, not confident narrative.
"Snippets only — cannot synthesize" is the honest output.

---

## Self-Referential Fabrication Guard

Before claiming any search result as independent evidence:
1. When did I FIRST mention this term in THIS session?
2. When was the database entry CREATED/UPDATED?
3. Entry postdates my mention → I wrote it → NOT a source.
4. Same-session auto-saves are NOT independent sources.

Proper nouns from pattern completion are NOT sources. Source must trace to (a) file read or (b) user statement.

---

## Grand-Theorize Guard

Before emitting "why X happened" narratives with intermediate causal chains:

1. **Citation density:** if <50% intermediate claims have named sources → reject narrative
2. **Specific vs vague:** specific claims need source; vague claims tagged `[INT]`
3. **Counterfactual test:** what would make this narrative wrong? If unfalsifiable → refuse

Three valid alternatives: decompose into verifiable + speculative; offer 2-3 ranked hypotheses;
or refuse to narrate ("aku tak nampak").

---

## Operating Procedure

1. **Before any tagged claim:** "Do I have the receipt?" No → retag `[OBS]` → `[SPEC]`.
2. **Before any inventory claim:** scan cited paths for negation words. Resolve contradictions.
3. **Before any source citation:** spot-check 3 random references. 30-second cheap-check on math.
4. **Before mutable-state inventory:** 5-second freshness probe (SHA + line count + timestamp).
5. **Before zero/percentage/universal claim:** state exact denominator. Sample < population → label.
6. **Before count claim disagrees with probe:** trace source through registries → configs → sessions.
   If UNTRACED → report UNTRACED, don't infer scope.
7. **Before documentation-backed claim as fact:** 3-source verification ladder.
8. **Before exploration-mode synthesis:** 5-class claim taxonomy. HEARSAY ≠ premise.
9. **Before synthesis from partial retrieval:** T1–T4 evidence ladder. >50% T2–T4 → decomposition only.
10. **Before any search result as independent evidence:** timestamp-gate. Same-session auto-save ≠ source.
11. **Before "why X happened" narrative:** citation density ≥50% or decompose/refuse.
12. **On detection of violation:** log to `~/.local/share/arifos/atlas333/audit/` (escalation) or
    `~/.local/share/arifos/atlas333/eureka/` (one-time source downgrade).

---

## Anti-patterns

| Anti-pattern | What to do |
|---|---|
| Tag without receipt | Retag `[SPEC]`, or produce the receipt |
| Cite path without line block | Always include path:lines+block |
| Inventory claim + same-path negation | Cross-check negation words; resolve before emitting |
| "Paper has one typo, otherwise good" | Downgrade to UNVERIFIED_SOURCE; cite spot-checks |
| Audit mutable state from cached memory | 5-second freshness probe before inventory claim |
| Sample-to-population collapse | State denominator in every universal claim |
| Resolve UNTRACED count via scope hypothesis | UNTRACED is a valid verdict; don't infer |
| "Trust me, I read the code" | Receipt or it didn't happen |
| Cite documentation as evidence | Verify against primary source; tag [INT] if no primary |
| HEARSAY premise supporting confident conclusion | Drop premise or downgrade conclusion |
| Exploration mode as relaxation of discipline | Exploration changes scope, not discipline |
| Synthesis from snippets/titles only | Classify T1–T4; >50% T2–T4 → decomposition only |
| Auto-save as independent source | Timestamp-gate: same-session saves ≠ source |
| Grand-theorize without sources | Citation density ≥50% or decompose/refuse |
| Confident flat confidence across verification failures | Collapse confidence proportionally |
| Probe never calibrated against known fault | Calibrate before trusting clean verdict |
| Quote aggregate without per-item check | One unchecked component voids it |

---

*Claim states: ESTIMATED→MEASURED→CROSS_VALIDATED→RETRACTED. Receipt format: trace_id required.
Merged 2026-09-17 from claim-receipt-discipline (87KB) + claim-level-verification (20KB).
Archived session-specific content to references/archive/.*