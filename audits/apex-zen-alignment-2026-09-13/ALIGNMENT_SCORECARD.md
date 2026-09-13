# ALIGNMENT_SCORECARD — APEX-ZEN Sweep v1
> Session `SEAL-42dad7d3d9334310` · 2026-09-13 · Evidence-based; no projections.

## 1. Five-Invariant scores

| Invariant | Instruction layer | Runtime evidence | Score | Basis |
|---|---|---|---|---|
| **AZ-1 Speaker First** | GREEN (K1 patch in `/root/AGENTS.md`; speaker checks in warga docs) | YELLOW — no speaker detector in telemetry; lanes handle it structurally | 🟢🟡 | Instruction complete; measurement absent |
| **AZ-2 Intent > Syntax** | GREEN (K4 intent-detection clause) | YELLOW — no detector wired | 🟢🟡 | Same asymmetry |
| **AZ-3 Execute When Sufficient** | GREEN (Anti-Tangguh + GO signals + forbidden follow-ups) | GREEN — GO_SIGNALS live in collector; today's session: 20+ executions without permission loops | 🟢 | Strongest axis |
| **AZ-4 Governance Reduces Friction** | GREEN (policy) | RED — 0 scheduled measurement; CI friction faults (orphan gitlink killed all checkouts; missing scanner baseline = 10/10 red) just fixed today | 🟡🔴 | Governance WAS adding entropy — now remediated, needs proof |
| **AZ-5 Artifact > Discussion** | GREEN (doctrine explicit) | YELLOW — artifact detector exists; first live sample IAR=0.18 (calibration pending) | 🟢🟡 | Doctrine yes; ratio unproven |

## 2. Violation classes (Phase 2 results)

### CLASS A — confirmation loops (60 raw hits → classified)
- **Prohibitions (teaching NOT to use):** ~52 hits — e.g. `instructions/autonomy.md:18`, `agents/opencode/333-AGI.md:126`, `governance/APEX-ZEN-EXECUTION-DOCTRINE.md:162`.
- **Detectors:** 8 hits — `scripts/apex-zen-telemetry.py:32,42`, `apex-zen-score.py:84`.
- **True violations in active surfaces:** **0** (remaining hits live in `_archive*/` — excluded).
- **Disposition:** 🟢 instruction layer aligned. Residual risk: runtime enforcement for agents that don't load these files.

### CLASS B — discussion-before-artifact
- Instruction surfaces: **0 hits** after exclusions.
- Raw hits found only in **runtime session transcripts** (`agents/hermes-asi/runtime/sessions/*`, May 2026) — runtime data, not instructions.
- **Disposition:** 🟢 clean. Adjacent finding: session transcripts as repo data = hygiene item (Top-20 #11).

### CLASS C — register mismatch
- No register-overriding rules found. Hits are evidence-citation rules (F2-positive): `prompts/ADVERSARIAL_BOOT.md:149`, `skills/BIJAKSANA-compile/SKILL.md:139`.
- **Disposition:** 🟢 clean.

### CLASS D — governance friction without safety
- Approval-gate hits are blast-radius-scoped (legitimate): `skills/ASI-agentic-governance/references/CONSTITUTIONAL_OPERATING.md:40`.
- **Live friction found elsewhere (systemic):**
  1. CI: every checkout failed via orphan gitlink `tools/nusantara-validator` (fixed 2026-09-13).
  2. Branch protection: required check `npm ci (frozen lockfile)` was **bypassed** on every push ("Bypassed rule violations") — a gate that doesn't bind. → Top-20 #7.
  3. Telemetry Layer 2-3 unwired = governance that cannot see itself. → Top-20 #1-2.
- **Disposition:** 🟡 rules themselves are calibrated; the FRICTION lived in broken plumbing.

## 3. Systemic findings (file-level where applicable)

| # | Finding | Evidence | Severity |
|---|---|---|---|
| S1 | Telemetry collector unscheduled; first data point produced today | `apex-zen-telemetry.jsonl` = 1 record | HIGH |
| S2 | Detector calibration: raw JSONL saturation (counts include system prompt text + tool payloads; CD=1.06, conf=663 on one session) | live run 2026-09-13T10:56Z | HIGH |
| S3 | Branch-protection check bypassed on push | push output "Bypassed rule violations … npm ci" | MED |
| S4 | Agentic CI red: 7 seed-test assertions (canonical order drift) | run 34752652942 | MED |
| S5 | Doc drift: CODER_FEDERATION_MAP (Aug-14), CROSS_HARNESS_MANIFEST (Aug-12), AGENT_INTELLIGENCE (FI-004 gemini stale) | file dates | LOW-MED |
| S6 | Orphan gitlink + missing scanner baseline (now fixed) → the 10/10 red gates were UNSEEN plumbing faults, not hidden exfiltration | this session's commits | RESOLVED |

## 4. Verdict

- **Instruction layer: SEAL-worthy alignment.** Zero true Class A/B/C/D violations in active surfaces; prohibitions and detectors are in place.
- **System-level: HOLD.** SUCCESS CRITERION of the sweep = *evidence of behavioral alignment*, and the decisive evidence (CD/DD/IAR/DCR trends across sessions) **cannot yet exist** because the collector was never scheduled. One data point is not a trend.
- **Evidence produced today (behavioral, not documentary):** 10+ artifacts shipped end-to-end (CI unblocked, gates greened, #181 closed, registry re-probed), first telemetry record ever written. That is a closure sample, not yet a series.

**Gate to flip HOLD→SEAL:** 7 days of scheduled telemetry with calibrated detectors and a published weekly scorecard.
DITEMPA BUKAN DIBERI — 2026-09-13
