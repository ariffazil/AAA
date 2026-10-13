---
canon_id: verdict-vocabulary
status: ACTIVE
authority: ARIF (F13 sovereign override 2026-10-11)
compiled_by: FI-008 (kimi-code) — single-writer integration per ARIF Path-A verdict
compiled_on: 2026-10-11
version: 1.0
fs_flag: i  # file-level immutable; matches F13 enforcement convention
canonical_spec: /root/AAA/canon/verdict-vocabulary-2026-10-11.json
verifier: /root/AAA/scripts/verdict_vocabulary.py
test_suite: /root/AAA/scripts/test_verdict_vocabulary.py (35 tests, all passing)
staging_supersedes: /root/AAA/_registry_2026-10-11/verdict-vocabulary-v0.1.json (NON_CANONICAL audit trail)
supersedes: NONE (first-of-kind)
evidence:
  - /root/AAA/_registry_2026-10-11/PASS2-REGISTRY-DELTA.md (333-AGI delta handoff)
  - Gemini external deep-research, "Bounded Intelligence and the Architecture of the Void" §"Verdict Vocabulary"
related:
  - /root/AAA/canon/CONSTITUTIONAL-ARCHITECTURE-CANON-2026-09-21.md (3-state P(a,S)→{ALLOW,HOLD,DENY} is coarser; this canon formalizes the 10 verdict register)
  - /root/AAA/governance/RETENTION.md (5-state lifecycle ACTIVE/DRAFT/SUPERSEDED/ARCHIVED/VOID — orthogonal to this 10-state runtime verdict)
fingerprint_pending: F2 (Truth) verification run attached below
last_reviewed: 2026-10-11
---

# Verdict Vocabulary — 10-State Constitutional Register (v1.0 ACTIVE)

## Principle (constitutional)

> **Descriptive label ≠ authorization token.** Each verdict word has a unique
> consequence class. A state that conveys "the system completed something"
> cannot be silently promoted to "the system is authorized to execute something."
> Conflation is a constitutional violation.

This canon encodes the 10-state verdict register from the Bounded-Intelligence
paper as a single canonical ACTIVE artifact, with a verifier that enforces the
classification rule at runtime.

## Why this canon exists

The arifOS federation must distinguish:

- "software ran successfully" → `SUCCEEDED` / `RECORDED` (event-logged, no authority)
- "simulation passed"  → `DRYRUN_ACCEPTED` (technical-feasibility)
- "reality was measured correctly" → `VERIFIED` (epistemic-validation)
- "human said yes"       → `AUTHORIZED` (contractual-readiness)

These four events have **four distinct consequence classes**. The Bounded-Intelligence
paper §"Danger of Generic Execution States" warns that agentic frameworks routinely
collapse these distinctions: a sandbox `SUCCEEDED` becomes authorization to deploy to
production. This canon refuses that collapse.

## 10-State Register

| # | State | Synonyms | consequence_class | terminal | requires_human | scope_required | time_bound_required |
|---|---|---|---|---|---|---|---|
| 01 | `HEALTHY` | `VALID` | system-readiness | no | no | no | no |
| 02 | `DRYRUN_ACCEPTED` | — | simulation-confirmed | no | no | no | no |
| 03 | `SUCCEEDED` | `RECORDED` | event-logged | no | no | no | no |
| 04 | `VERIFIED` | — | epistemic-validation | no | no | no | no |
| 05 | `PARTIAL` | — | bounded-verified | no | no | yes | no |
| 06 | `SABAR` | — | temporal-boundary | no | no | no | yes |
| 07 | `AUTHORIZED` | — | contractual-readiness | no | yes | no | no |
| 08 | `HOLD` | — | human-veto-required | no | yes | no | no |
| 09 | `SEAL` | — | verified-authorized-mutation-allowed | **yes** | yes | yes | no |
| 10 | `VOID` | — | terminal-rejection | **yes** | no | no | no |

**Unique consequence classes** (`conflation_detector` enforces):
```
system-readiness        : [HEALTHY]
simulation-confirmed    : [DRYRUN_ACCEPTED]
event-logged            : [SUCCEEDED]
epistemic-validation    : [VERIFIED]
bounded-verified        : [PARTIAL]
temporal-boundary       : [SABAR]
contractual-readiness   : [AUTHORIZED]
human-veto-required     : [HOLD]
verified-authorized     : [SEAL]
terminal-rejection      : [VOID]
```

## Composition Rule for SEAL (irreversible execution)

`SEAL` requires **both** `VERIFIED` (epistemic) AND `AUTHORIZED` (human-contractual).
Either alone is insufficient:

```
VERIFIED     → SEAL    ALLOWED but warns: AUTHORIZED must also be obtained separately
AUTHORIZED   → SEAL    ALLOWED but warns: VERIFIED must also be obtained separately
PARTIAL      → SEAL    BLOCKED (PARTIAL alone is not VERIFIED + AUTHORIZED)
SUCCEEDED    → SEAL    BLOCKED (SUCCEEDED is event-logged; cannot be promoted)
```

The composition invariant is encoded in `authorities_required_for_irreversible: [VERIFIED, AUTHORIZED]`.

## Forbidden Transitions (runtime enforced)

The verifier surfaces these cases explicitly:

```
SUCCEEDED       → AUTHORIZED     BLOCKED  (canonical bug class)
SUCCEEDED       → SEAL            BLOCKED
RECORDED        → AUTHORIZED      BLOCKED  (synonym inherits)
DRYRUN_ACCEPTED → AUTHORIZED      BLOCKED  (simulation ≠ authority)
HOLD            → anything        BLOCKED  (absolute veto)
VOID            → anything        BLOCKED  (terminal — only new evidence exits)
```

## Bounds & Refusals (each state declares its `forbidden_implications`)

The runtime surfaces these warnings so an operator can refuse silent promotion:

```
SUCCEEDED:  "this is not AUTHORIZATION for live deployment"
VOID:       "retrying a VOID proposal without new evidence is a constitutional violation"
AUTHORIZED: "AUTHORIZED alone is NOT a SEAL — VERIFIED also required"
SEAL:       "scope-exhausted or human-override is the only exit"
SABAR:      "SABAR is not a soft YES; cooling must elapse before re-evaluation"
```

## Test Suite

35 tests; all passing. Located at `/root/AAA/scripts/test_verdict_vocabulary.py`.
Test classes (14):

| Class | Tests | Coverage |
|---|---|---|
| `TestVocabularyLoad` | 4 | spec file, 10 states, names match doc, principle present |
| `TestConflationDetector` | 2 | no consequence-class duplication; per-state uniqueness |
| `TestTerminalStates` | 3 | SEAL/VOID terminal; others not |
| `TestHumanAuthorityRequired` | 4 | AUTHORIZED/SEAL/HOLD require human; SUCCEEDED/VERIFIED don't |
| `TestHeadlinePromotionGuards` | 5 | the Bounded-Intelligence bug class — must BLOCK |
| `TestSilentPromotionRiskWarning` | 2 | SUCCEEDED warns; HEALTHY doesn't |
| `TestHoldIsBlocking` | 3 | HOLD blocks forward, only re-evaluation allowed |
| `TestVoidIsTerminal` | 2 | VOID blocks everything; only exits via new evidence |
| `TestSabarIsTimeBound` | 1 | SABAR declares `time_bound_required` |
| `TestScopeRequiredForIreversible` | 3 | SEAL/PARTIAL need scope; benign states don't |
| `TestUnknownStateRaises` | 2 | defensive — unknown raises, doesn't silently pass |
| `TestForbiddenImplicationClause` | 2 | explicit forbidden_implications text present |
| `TestScopeClassComposition` | 1 | VERIFIED + AUTHORIZED → SEAL composition invariant |
| `TestAnticonflation` | 1 | zone definitions match — 1 state per zone |

## Verifier CLI

`/root/AAA/scripts/verdict_vocabulary.py` exposes:

```bash
verdict_vocabulary.py stats                       # spec integrity report
verdict_vocabulary.py conflate                    # consequence-class uniqueness
verdict_vocabulary.py check   <name>              # class + terminal + human + risk
verdict_vocabulary.py promote <current> <to>      # refuses silent label→authority promotion
```

Exit codes map to constitutional consequence:
```
0  ALLOWED   — transition permitted
1  WARN      — soft issue (cooling not elapsed, etc.)
2  HOLD      — agent must stop; awaits human
3  VOID      — rejection; do not retry without new evidence
4  INVALID   — vocabulary/spec violation
```

## Single-Writer Integration Discipline

Per ARIF Path-A verdict (2026-10-11): Kimi/FI-008 is the single canonical writer
for this registry. Scanner ≠ Writer. 333-AGI scanner produced evidence; Kimi
integrated; ARIF ratified. No concurrent mutator. No `chattr -i` bypass; the
lift-write-reflag ritual honored: directory flag lifted, files written with
file-level `i` flag, directory flag re-applied.

## Out of Scope (orthogonal, do not extend here)

- **Lifecycle states** (`ACTIVE/DRAFT/SUPERSEDED/ARCHIVED/VOID`) live in `governance/RETENTION.md`. They are NOT verdict words; they are file-lifecycle. A `SUCCEEDED` verdict does NOT make a file `SUPERSEDED`.
- **Constitutional 3-state gate** (`P(a,S) → {ALLOW, HOLD, DENY}`) lives in `CONSTITUTIONAL-ARCHITECTURE-CANON-2026-09-21.md`. Denormalized here to 10 verdict states.
- **Storage / receipt** of verdict transitions → VAULT999 (not formalized here).

---

**Maintainer:** ARIF. **Canonical writer:** FI-008. **Evidence:** 333-AGI delta + Gemini deep-research. **Status:** ACTIVE 2026-10-11. **Verification:** `python3 /root/AAA/scripts/test_verdict_vocabulary.py`.
