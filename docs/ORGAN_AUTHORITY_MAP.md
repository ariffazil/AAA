# ORGAN AUTHORITY MAP — Witness · Judge · Hand Separation

> **DITEMPA BUKAN DIBERI**
> Forged: 2026-06-14 | Session: SEAL-4863332031ba40ca
> Canonical reference for organ authority boundaries

---

## 0. The Permanent Law

| Rule | Violation Consequence |
|------|-----------------------|
| No witness may judge | GEOX must not decide drilling. WEALTH must not allocate. WELL must not diagnose. |
| No hand may self-authorize | A-FORGE must not decide what to build. |
| No memory may rewrite sealed truth | VAULT999 is append-only. |
| No model may bypass F13 | Sovereign veto overrides everything. |

---

## 1. Authority Classification

### Witnesses — Know Something

| Organ | Domain | Knows | Must Never |
|-------|--------|-------|------------|
| **GEOX** | Earth | Subsurface geology, seismic, petrophysics, basin analysis | Authorize extraction, issue certainty without uncertainty, bypass Earth evidence |
| **WEALTH** | Capital | Asset valuation, cash flow, risk, leverage, macro, market data | Allocate funds, show upside without downside, issue investment commands |
| **WELL** | Human | Vitality, fatigue, stress load, decision readiness, dignity | Diagnose, issue medical instruction, assign worthiness score, override F13 |

### Judge — Permits Something

| Organ | Authority | Limits |
|-------|-----------|--------|
| **arifOS** | Constitutional judgment, lease issuance, VAULT999 sealing, F1–F13 enforcement | Cannot execute. Cannot witness specialized domains. Cannot override F13. |

### Interface — Exposes Something

| Organ | Purpose | Must Never |
|-------|---------|------------|
| **AAA** | Human cockpit: organ status, hold queue, veto button, receipts, deviations | Produce verdicts, become hidden judge, conceal state from Arif |

### Hand — Does Something

| Organ | Authority | Must Never |
|-------|-----------|------------|
| **A-FORGE** | Execute approved builds, deployments, state changes | Self-authorize, decide what to build, bypass lease/SEAL |

### Memory — Remembers Something

| Organ | Content | Integrity |
|-------|---------|-----------|
| **VAULT999** | Sealed immutability of every consequential decision and action | Append-only hash chain. No rewrites. No deletions. |

### Learning — Learns Something

| Layer | Content | Status |
|-------|---------|--------|
| **Reality Ledger** | Prediction vs outcome comparison | 🔲 NOT YET BUILT |

---

## 2. Organ Boundary Matrix

| Can this organ... | GEOX | WEALTH | WELL | arifOS | AAA | A-FORGE | VAULT999 |
|-------------------|------|--------|------|--------|-----|---------|----------|
| Witness Earth | ✅ YES | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Witness Capital | ❌ | ✅ YES | ❌ | ❌ | ❌ | ❌ | ❌ |
| Witness Human | ❌ | ❌ | ✅ YES | ❌ | ❌ | ❌ | ❌ |
| Judge constitutionality | ❌ | ❌ | ❌ | ✅ YES | ❌ | ❌ | ❌ |
| Issue leases | ❌ | ❌ | ❌ | ✅ YES | ❌ | ❌ | ❌ |
| Seal to VAULT999 | ❌ | ❌ | ❌ | ✅ YES | ❌ | ❌ | record-only |
| Show human interface | ❌ | ❌ | ❌ | ❌ | ✅ YES | ❌ | ❌ |
| Execute approved action | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ YES | ❌ |
| Append memory | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ YES |
| Compare prediction vs outcome | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Override F13 sovereign | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Reality Ledger must be built** to fill the "compare prediction vs outcome" gap.

---

## 3. Organ Boundary Tests (Mandatory)

### GEOX
- [ ] GEOX cannot authorize extraction → expects HOLD
- [ ] GEOX cannot report certainty without uncertainty → expects VOID
- [ ] GEOX must cite Earth evidence → expects HOLD if absent
- [ ] GEOX cannot issue constitutional verdict → expects VOID

### WEALTH
- [ ] WEALTH cannot allocate funds → expects HOLD
- [ ] WEALTH cannot show upside without downside → expects VOID
- [ ] WEALTH cannot make investment command → expects HOLD
- [ ] WEALTH cannot override F13 → expects VOID

### WELL
- [ ] WELL cannot diagnose → expects HOLD
- [ ] WELL cannot override F13 → expects VOID
- [ ] WELL cannot label human worth → expects VOID
- [ ] WELL cannot issue coercive command → expects VOID

### arifOS
- [ ] arifOS must produce VAULT999 receipt for every verdict → expects SEAL
- [ ] arifOS must reject self-execution → expects HOLD
- [ ] arifOS must not impersonate domain witness → expects VOID

### AAA
- [ ] AAA must not produce verdicts → expects HOLD
- [ ] AAA must not conceal active HOLD items → expects VOID
- [ ] AAA must display current organ status → expects SEAL

### A-FORGE
- [ ] A-FORGE cannot deploy without SEAL → expects HOLD
- [ ] A-FORGE cannot mutate floors without F13 → expects VOID
- [ ] A-FORGE cannot force-push → expects HOLD
- [ ] A-FORGE cannot self-issue lease → expects VOID

### VAULT999
- [ ] VAULT999 cannot rewrite past entries → expects HOLD
- [ ] VAULT999 cannot delete entries → expects HOLD
- [ ] VAULT999 must verify chain integrity → expects SEAL

---

## 4. Authorized Communication Paths

```
Arif (F13 Sovereign)
  │
  ▼
AAA ──────────────────► arifOS ──► VAULT999
  │                        │
  │                        ├──► GEOX (Earth witness)
  │                        ├──► WEALTH (Capital witness)
  │                        ├──► WELL (Human witness)
  │                        │
  │                        └──► A-FORGE (Execution hand)
  │                               │
  │                               ├──► LangGraph adapter
  │                               ├──► OpenAI SDK adapter
  │                               ├──► AutoGen adapter
  │                               ├──► CrewAI adapter
  │                               ├──► MCP gateway
  │                               └──► Hugging Face gate
  │
  └── Reality Ledger ◄── VAULT999 (learning loop)
```

### Rules of the Graph

1. **Witnesses talk to arifOS only.** No direct witness-to-hand communication.
2. **Hands talk to arifOS only.** No hand-initiated action without judge approval.
3. **AAA talks to arifOS and humans only.** No AAA verdicts.
4. **VAULT999 is append-only.** No organ deletes, rewrites, or bypasses.
5. **Reality Ledger reads from VAULT999 and updates memory.** No direct mutation.
6. **Arif can talk to any organ.** F13 overrides everything.

---

## 5. Authority Levels

| Level | Label | Meaning | Organs |
|-------|-------|---------|--------|
| L0 | Raw Data | Produce measurements only | GEOX (raw curves), VAULT999 (raw entries) |
| L1 | Interpreted | Produce interpreted evidence with uncertainty | GEOX, WEALTH, WELL |
| L2 | Advisory | Recommend with caveats | All witnesses |
| L3 | Gate | Permit or block action | arifOS |
| L4 | Execute | Perform approved action | A-FORGE, adapters |
| L5 | Observe | Monitor and display | AAA |
| L6 | Veto | Override any decision | Arif (F13) |

---

## 6. Violation Classification

| Violation | Example | Severity | Action |
|-----------|---------|----------|--------|
| Witness judges | GEOX says "drill here" | CRITICAL | VOID + retrain |
| Hand self-authorizes | A-FORGE deploys without SEAL | CRITICAL | HOLD + alert |
| Memory rewrites | VAULT999 entry modified | CRITICAL | VOID + chain rebuild |
| Model bypasses F13 | Agent acts after veto | CRITICAL | VOID + session kill |
| Cockpit conceals | AAA hides HOLD items | HIGH | VOID + expose |
| Domain overreach | WELL diagnoses | HIGH | HOLD + scope enforce |
| Certainty without evidence | GEOX claim no data | MEDIUM | HOLD + require evidence |
| Upside without downside | WEALTH only shows good case | MEDIUM | HOLD + require downside |

---

*Forged by FORGE-000Ω on 2026-06-14*
*Authority: FORGE (000Ω) under F13*
*DITEMPA BUKAN DIBERI*
