# Federation Conformance Score Semantics

> **Date:** 2026-09-04 | **Purpose:** Replace raw pass count with deployment-posture classification

---

## 1. Problem with Raw Pass Count

A 6/9 partial score can conceal a critical failure (e.g., session minting on modern path).
A 4/9 legacy score can be safe if deliberately isolated and unavailable to modern clients.

**Raw pass count is not a security or deployment metric.**

---

## 2. Classification System

| Classification | Criteria | Deployment Posture |
|----------------|----------|-------------------|
| **Modern Conformant** | All mandatory modern probes pass; no session leakage; cache envelope present | Eligible for normal modern-client traffic |
| **Modern Partial** | Modern route exists; non-security/low-impact gaps remain (e.g., missing cache) | Canary/internal only |
| **Modern Unsafe** | Session minting, header mismatch, auth bypass, state bleed, or discovery deception | **Block modern endpoint** |
| **Legacy Isolated** | Old protocol only, explicitly routed, no modern claim | Permit only known legacy clients |
| **Dual-Stack Verified** | Both routes pass respective suites; no semantic cross-contamination | Preferred migration state |
| **Unknown** | No reliable probe evidence | No federation trust / no broad routing |

---

## 3. Current Federation Classification

| Organ | Classification | Evidence | Action |
|-------|---------------|----------|--------|
| **arifOS** | Modern Partial | 6/10 pass; server/discover works; no session; missing cache | Complete cache envelopes → Modern Conformant |
| **A-FORGE** | Legacy Isolated | 3/10 pass; session-bound; no discover | Dual-stack migration (888_HOLD) |
| **AAA** | N/A (A2A-first) | 1/10 on MCP; A2A gateway, not MCP server | Keep A2A; no automatic MCP |
| **GEOX** | **Modern Unsafe** | Session minted on modern path (P0) | **Contain immediately** |
| **WEALTH** | Legacy Isolated | 4/10 pass; auth discovery works; no discover | Upgrade after reference pattern |
| **WELL** | Dual-Stack Candidate | 4/10 pass; legacy initialize works; origin validation | Formalize isolation → Dual-Stack Verified |

---

## 4. Probe Weights

Not all probes are equal. Weight by security impact:

| Probe | Weight | Why |
|-------|--------|-----|
| P01 server/discover | HIGH | Modern capability discovery |
| P02 tools/list cache | LOW | Optimization, not security |
| P03 tools/call headers | MEDIUM | Correct routing |
| P04 header/body mismatch | HIGH | Anti-confused-deputy |
| P05 unsupported version | MEDIUM | Graceful rejection |
| P06 no session header | **CRITICAL** | State model correctness |
| P07 legacy initialize | LOW | Backward compat |
| P08 MRTR awareness | LOW | Extension support |
| P09 origin validation | MEDIUM | SSRF protection |
| P10 auth discovery | LOW | OAuth readiness |

**Weighted score formula:**
```
score = Σ(probe.pass × probe.weight) / Σ(probe.weight)
```

---

## 5. Deployment Gate

```text
No organ may claim "2026-07-28 compliant" unless:
  P01 server/discover = PASS
  P06 no-session invariant = PASS (CRITICAL)
  P04 header/body validation = PASS
  P02 result typing = PASS
  P02 cache fields = PASS
  P05 supported-version response = PASS
  P07 legacy compatibility = explicit and tested
```

---

## 6. CI Regression Thresholds

```yaml
conformance:
  critical_probes: [P01, P04, P06]
  critical_must_pass: true
  weighted_score_minimum: 0.7
  regression_tolerance: 0.05  # 5% degradation allowed
  classification_required: true
```

---

*Classification system for federation MCP conformance. Replaces raw pass count.*
