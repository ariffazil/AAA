# TELEMETRY_GAP_REPORT — APEX-ZEN Sweep v1
> Can CD / DD / IAR / DCR actually be measured today? Evidence-based. Session `SEAL-42dad7d3d9334310`.

## 1. Measurability matrix

| Metric | Definition | Detector exists | Collector runs | Stream | Data state | Scheduled | Consumer |
|---|---|---|---|---|---|---|---|
| **CD** Confirmation Debt | confirm-loops ÷ GO signals | ✅ `apex-zen-telemetry.py` (17 patterns incl. Malay) | ✅ manual (verified live) | `/root/VAULT999/apex-zen-telemetry.jsonl` | **1 record** (created 2026-09-13T10:56Z) | ❌ none | ❌ none (Layer-4 router TBD) |
| **DD** Discussion Debt | turns per closed decision | ✅ (turns counter) | ✅ manual | same | same | ❌ | ❌ |
| **IAR** Intent→Artifact Ratio | artifacts ÷ GO signals | ✅ (12 artifact patterns) | ✅ manual | same | same | ❌ | ❌ |
| **DCR** Decision Closure Rate | closed ÷ raised | 🟡 (script field; semantics = verbose-leak-derived — needs definition fix) | ✅ manual | same | same | ❌ | ❌ |

**Verdict: MEASURABLE-IN-PRINCIPLE, UNMEASURED-IN-PRACTICE.** All four metrics can be computed today from existing code + existing transcript fuel. None are measured on a schedule. The bottleneck is wiring, not capability.

## 2. First live measurement (kimi session, 81 turns, 451 wire records)

```
GO signals:    626
Confirmations: 663   → CD = 1.0591   (target < 0.05)  ✗
Artifacts:     110   → IAR = 0.1757  (target > 0.80)  ✗
Turns:          81   → DD = 0.74     (target < 2)     ✓
Verbose leaks:  56   → DCR = 0.1423  (target > 0.90)  ✗
Verdict: ⚠️ TARGETS NOT MET
```

**Calibration caveats (must fix before trusting trends):**
1. Raw JSONL scanned — counts include system prompts, tool payloads, and doctrine text that *names* the forbidden phrases. Inflates CD/confirmations.
2. No role filter (assistant turns only should count for CD).
3. DCR field semantics need F13-ratified definition (currently verbose-leak-derived).
4. Targets themselves are PROVISIONAL (doctrine v1) — ratify after 7 days of calibrated data.

## 3. Gaps (ranked)

| Gate | Gap | Fix |
|---|---|---|
| **G1** | No schedule — collector never runs | cron: nightly, per-harness input dirs (Top-20 #1) |
| **G2** | Detector calibration (saturation, role filter, dedupe) | Top-20 #2 |
| **G3** | Harness coverage: only kimi `wire.jsonl` proven; claude-code / opencode / codex / qwen formats unverified | Top-20 #4 |
| **G4** | No consequence loop — Layer 4 router TBD; data has no consumer | Top-20 #3 |
| **G5** | DCR definition divergence (script vs doctrine) | ratify definition; consider arifFlow `flow_gov_events` (seal/seal_refused) as authoritative DCR source |
| **G6** | Privacy/scope: transcripts contain sensitive content; output stream path under `/root/VAULT999/` — scope check needed (biometric/sanctuary rules) | review before scheduling |

## 4. Available fuel (OBS)

- Kimi: `/root/.kimi-code/sessions/**/agents/main/wire.jsonl` ✅ parsed live
- Hermes: `agents/hermes-asi/runtime/sessions/**` (json + jsonl) — format variance
- arifFlow `:7073` — receipts + gov events (LIVE, structured) — best DCR source today
- Seal chain: `VAULT999/seal_chain.jsonl` (append-only) — closure receipts

DITEMPA BUKAN DIBERI — 2026-09-13
