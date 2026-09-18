# WEALTH Upgrade Gap Analysis — Handoff to Lane 333-AGI

**Date:** 2026-09-16
**Author:** i-ARIF (Hermes), gap analysis + comparison
**Scope:** PDF "Upgrading WEALTH Intelligence Framework" vs live WEALTH code
**Status:** Handoff document — READ + COMPARE only, no patches applied

---

## Section 1: What 333-AGI Has Already Built (Staged + Committed)

### Committed in 09a7768 (fix(witness): P0 repair ladder)
1. `_tool_result_status` function: upstream errors/partial/error_code can never log `call_status=PASS`
2. Idempotency key + `duplicate_of` labeling on double-dispatched calls
3. Registry import-probes for all canonical deps (runtime-aware, not schema-presence)
4. Backtest: absolute import fix for `trading.signals.scanner`, server paths redacted from tracebacks
5. Entry plan: freshness contract (`market_data_age_s`, `freshness_policy`, `ALL_RESISTANCE_BELOW_PRICE` zone warning, `decision_eligibility` gate)
6. Capital_health: `actor_id`/`session_id`/`trace_id` propagation to survival engine
7. Governance_capacity: fail-closed input gate (empty → `MISSING_DATA`, never empty-board diagnosis)
8. Commodity engines: dead `/root/venv` python paths → correct `/root/WEALTH/.venv`; gold stale-cache bounded to 24h; per-engine `package.json` (SCAR-001 packaging truth)
9. Tests: `test_receipt_truth.py` — 7 negative cases covering oil-500-PASS defect pinned

### Committed in b4d9919 (fix(fidelity): P0 input gates + market fail-closed)
10. Canonical W0 gate handling for governance_capacity (input fidelity)
11. `canon/LAW-WEALTH-01.md` — constitutional document (62 lines)
12. Canonical.py: 95 lines added covering input gate + market fail-closed + authority propagation

### Verified by live probe (OpenClaw 11:32Z, Hermes 11:21Z)
- 888 bypass CLOSED: self-attested flag ignored, kernel-rejected path enforced, `requires_888_hold=true`
- Oil route: HTTP 200 (was 500)
- Gold: refreshed to 2026-09-16 19:22Z (was 8.4-day stale)
- Governance_capacity empty-board: returns `MISSING_DATA` (was `capacity_score=0.0` + emergency advice)
- Process: pid 3751837, started 19:11, serves commit `b4d9919` (HEAD)

---

## Section 2: What the PDF Proposes vs What Live WEALTH Has

### Tier 1 — Core Domain (Constitutional Foundation)

| PDF proposal | Status | Live evidence |
|---|---|---|
| Epistemic integrity (tag × claim × quality × coverage) | ✅ Implemented | 85 `epistemic_tag` calls across 11 tools |
| Constitutional overrides (pulse-zero lock) | ✅ Implemented | `petronas_vitals` seals, pacemaker system |
| Santiago Principles replacement (algorithmic governance) | 🟡 Skeleton | Body-spine-soul tripwires exist; governance_capacity now fail-closed on empty input |
| Four-Truth Receipt Gate | ❌ Absent | `_tool_result_status` catches errors/partial (P0 fix) but no semantic/policy truth layers |
| Cryptographic notarized receipts | ❌ Absent | VAULT999 append-only JSONL; no COSE_Sign1, no Merkle transparency log |

**Gap assessment:** 40% implemented. Structural architecture sound. Receipt truth partially fixed (transport + execution). Semantic + policy truth absent.

### Tier 2 — Human Systems (Political Economy)

| PDF proposal | Status | Live evidence |
|---|---|---|
| NWW Limited Access Orders | ❌ Absent | Zero code references |
| Khan political settlements | ❌ Absent | Zero code references |
| Rent differentiation (developmental vs extractive) | 🟡 Skeleton | `rent_extraction.py`, `capture_detector.py`, `coercion_detector.py` exist but no NWW/Khan framework |
| Consequence gap modeling | 🟡 Skeleton | `capital_diagnose` modes (exploitation_detect, power_audit, collapse_signature) — pattern-matching, not economic model |
| Governance separation index | ✅ Implemented | tripwire #8 (scored 33.3, VOID, sealed) |

**Gap assessment:** 15% implemented. Files exist, zero institutional political economy content.

### Tier 3 — Signal Layer (Entropy + Information Theory)

| PDF proposal | Status | Live evidence |
|---|---|---|
| Shannon entropy computation | ❌ Absent | APEX `G = 0.01^(1/4)` floor constant, not Shannon |
| Tsallis entropy (q-index, heavy tails) | ❌ Absent | Zero code references |
| Rényi entropy | ❌ Absent | Zero code references |
| Four-Truth Receipt Gate (Transport/Execution/Semantic/Policy) | ❌ Absent | `_tool_result_status` covers Transport + Execution only |
| System Dynamics (stock/flow feedback loops) | ❌ Absent | No differential equation engine |
| Organizational entropy index | ❌ Absent | `collapse_signature` is keyword-matching, not entropy |

**Gap assessment:** 0%. The tier the PDF is most specific about has zero implementation. This is also the tier most directly needed to prevent the absence-laundering we documented tonight.

### Tier 4 — Physical Reality (Thermodynamics + Geology)

| PDF proposal | Status | Live evidence |
|---|---|---|
| EROI (Energy Return on Investment) | ❌ Absent | Zero code references |
| Arps decline curves | ❌ Absent | Zero code references (PDF claims `capital_primitive emv` crashed on this — generic EMV works; exploration-economics mode untested) |
| Jevons paradox modeling | ❌ Absent | Zero code references |
| GEOX → WEALTH integration | ❌ Absent | Zero GEOX references in WEALTH code |

**Gap assessment:** 0%. No physical reality grounding.

### Tier 5 — Symbol Layer (Narrative + Linguistics)

| PDF proposal | Status | Live evidence |
|---|---|---|
| Shiller narrative economics | ❌ Absent | Zero code references |
| SIR epidemic model for narratives | ❌ Absent | Zero code references |
| Linguistic framing analysis | ❌ Absent | `collapse_signature` uses fixed phrase lists, not linguistic analysis |

**Gap assessment:** 0%. No narrative intelligence.

---

## Section 3: Systematic Defects (Not Tool-Specific)

### W0 false-positive — confirmed in TWO tools

1. `governance_capacity` with real PETRONAS board (4 INED): W0 says *"1 material fields (['payload']) provided but ZERO reflected in result"* — but the result clearly used the payload (`total_members: 8`, `independent_neds: 4`, `total_committees: 3`)
2. `capital_primitive` emv: W0 says *"ZERO reflected in result"* — but `emv=40`, `variance=5400`, `std_dev=73.48` are correctly computed from the inputs

Pattern: W0 detects when input keys don't match expected output keys, but cannot detect when input is processed through a transformation that changes key names. This is a **schema-mismatch detector masquerading as an evidence-coverage detector.**

Implication for Four-Truth Receipt Gate: if the Semantic Truth layer inherits W0, it will produce false "coverage insufficient" on valid inputs. Fix W0 before building on it.

### collapse_signature keyword-matching false negative

PDF says stress test "validated" the architecture. Live test: feeding text containing "70.5% sovereign extraction, breaching the 65% pacemaker threshold" returned `risk_level: MINIMAL`, `acemoglu_label: INCLUSIVE`. The scanner matches fixed phrase lists, not economic semantics. Axis-3 extraction signals include "dividend uplift" but not "sovereign extraction" or "extraction ratio."

### `_tool_result_status` — narrow but correct

The P0 fix (09a7768) catches the oil PASS-on-500 and error_code cases. But it only covers Transport Truth + Execution Truth. The function's own comment says *"Failure signals outrank a clean wrapper"* — meaning it catches gross failures, not semantic truth (e.g., a response that says "price" but the price is 8.4 days stale).

---

## Section 4: Handoff Boundaries

### What 333-AGI owns (already built / actively building)
- Receipt truth gate (`_tool_result_status`, `test_receipt_truth.py`)
- Engine path fixes, stale-cache bounds, packaging truth
- Governance_capacity input fidelity
- Registry runtime probes
- `LAW-WEALTH-01.md` canonical document
- Staged `test_receipt_truth.py` + `canonical.py` changes

### What is NOT built and needs a decision before implementation
- Semantic Truth layer (what makes a response "true" not just "not-error")
- Policy Truth layer (governance constraint checking)
- W0 false-positive fix (schema-mismatch detection needs redesign)
- collapse_signature phrase-list → economic-semantics upgrade
- NWW / Khan framework (Tier 2)
- Tsallis / Rényi / Shannon (Tier 3)
- EROI / Arps / Jevons (Tier 4)
- SIR narrative / linguistic framing (Tier 5)
- GEOX cross-organ integration (Layer 0)
- Notarized agent receipts (COSE_Sign1 / Merkle)

### Priority ordering (from tonight's evidence)
1. **P0: W0 false-positive fix** — affects every gate downstream; current detector lies on valid inputs
2. **P0: Semantic Truth layer** — `_tool_result_status` catches gross failures; semantic truth catches stale/misleading/wrong-but-valid-looking responses
3. **P0: collapse_signature phrase → semantics** — the tool that should detect institutional decay returned MINIMAL on 70.5% extraction text
4. **P1: Runtime-aware registry** — committed but needs verification across all modes
5. **P2: Tier 2-5 concept layer** — NWW, Tsallis, Arps, SIR, GEOX integration (project-quarter scope)

### Dependency graph
```
W0 fix ──────────────────→ Semantic Truth ──→ Policy Truth
                                      │
collapse_signature upgrade ────────────┘
                                      │
registry verification ────────────────┘
                                      │
Tier 2-5 (requires P0 complete) ──────┘
```

### What 333-AGI should NOT do without coordination
- Commit to files already touched by Hermes (canonical.py, judge_handoff.py, server.py, petronas_vitals.py, governance.py) — wait for push first
- Add new modes without fixing W0 (false-positives will cascade)
- Build Tier 3-5 on top of P0 incomplete (absence-laundering multiplies per-hop)

---

## Section 5: External Comparison Summary (from parallel agent)

Full report at `/root/mcp-fin-research/REPORT-wealth-vs-market.md` (~42KB).

**Key axis from external comparison:**

| Capability | WEALTH | Best external | Gap |
|---|---|---|---|
| Epistemic envelope | ✅ Unique | None | WEALTH leads |
| COMPUTE_ONLY ceiling | ✅ Unique | None | WEALTH leads |
| Sovereign/Malaysia domain | ✅ Unique | None | WEALTH leads |
| Hash-chained ledger | 🟡 JSONL append-only | 5+ implementations (mcp-approvals, etc.) | Comparable, not unique |
| Kill switches | ✅ 888_HOLD | nofx (Go runtime clamp) | Comparable |
| Data/quant breadth | 11 tools, yfinance/Frankfurter | HKUDS Vibe-Trading 74 tools | **WEALTH decisively out-gunned** |
| External distribution | 0 stars, no public footprint | Vibe-Trading 33K★, TradingAgents 106K★ | **WEALTH absent** |

**Genuine white space (no external comparable):** NOC fiscal extraction, sovereign rents, federal-state resource arrangements, fiscal breakeven oil price, institutional political economy. GitHub search `political risk MCP server` = 0 results.

---

*Handoff ready for 333-AGI. This document is observation + comparison only. No patches applied, no commits made. The next action belongs to whoever holds the push decision and the implementation lane.*
