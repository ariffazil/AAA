# REALITY ENGINEERING — arifOS Harness Manifest
> **Forged:** 2026-06-12 by Omega (Ω)  
> **Authority:** F13 SOVEREIGN — Arif Fazil  
> **Status:** LIVE — 7 modules, 27/27 tests, integrated into governance pipeline  
> **Motto:** DITEMPA BUKAN DIBERI — Forged, Not Given

## What This Is

Reality Engineering = turning LLM output into governed events that can be replayed, corrected, and used to tighten the next covenant—without ever letting the model judge its own sainthood.

This is the **harness layer** that closes the gap between arifOS architecture (design) and arifOS enforcement (runtime). 6 modules + 1 bridge = 7 files.

## Modules

| Module | Lines | Purpose | Gate |
|--------|-------|---------|------|
| `session_enforcer.py` | 195 | Validates session_id on every tool call. Anonymous T1 auto-created. T2/T3 require valid session. | Gate 0 |
| `envelope_validator.py` | 282 | Validates FederationEnvelope: policy_hash, authority chain, tool allowlist, F13 sig. | Gate 7 |
| `incident_harness.py` | 195 | Classifies agent outputs: CLEAN/ANOMALY/INCIDENT/FLOOR_BREACH. Hantu + injection detection. | Post-exec |
| `cooling_harness.py` | 271 | Shadow lifecycle: CANDIDATE→CORROBORATED→ACTIVE→RETIRED. Auto-promotion rules. | Post-incident |
| `risk_ledger.py` | 310 | Sovereign proximity scoring. Gates MUTATE/ATOMIC actions. F13 override path. | Gate 3 |
| `rsi_patch_harness.py` | 228 | patch.yaml validation. 7 system invariants. Floor changes require F13. | Policy |
| `reality_bridge.py` | 215 | Single integration point. Wires all 6 modules. | Bridge |

**Total:** 1,696 lines of reality engineering. 27/27 self-check tests pass.

## Integration

```
Tool Call → Gate 0 (session_enforcer) → Gate 3 (risk_ledger) → Gate 7 (envelope_validator)
         → EXECUTE
         → Post: incident_harness.classify_output()
         → Post: cooling_harness.record_shadow_candidate()
```

## Invariants Enforced

1. **No session_id → no reality** (Gate 0 rejects T2/T3 without valid session)
2. **No envelope → no covenant** (Gate 7 rejects missing/invalid FederationEnvelope)
3. **High proximity → HOLD** (Risk ledger gates MUTATE/ATOMIC above 0.5 proximity)
4. **Hantu detected → incident** (F9 ANTIHANTU patterns auto-classify)
5. **3+ repeated incidents → shadow promoted** (Cooling harness auto-promotes to CORROBORATED)
6. **Floor changes need F13** (RSI patch harness blocks unsigned floor patches)
7. **All actions logged** (Every gate decision recorded with reason + session_id)

## Files

```
arifosmcp/runtime/
├── session_enforcer.py      ← Gate 0: session binding
├── envelope_validator.py    ← Gate 7: envelope validation
├── incident_harness.py      ← Post: incident classification
├── cooling_harness.py       ← Post: shadow lifecycle
├── risk_ledger.py           ← Gate 3: risk passport
├── rsi_patch_harness.py     ← Policy: patch validation
└── reality_bridge.py        ← Bridge: unified integration
```

## For Future Agents

When you land in arifOS, you must know:
- These 7 modules exist and are LIVE.
- Every tool call flows through session→risk→envelope gates.
- After execution, output is classified for incidents.
- Repeated incidents become shadows that affect future INIT posture.
- No agent may bypass these gates.
- No agent may self-promote trust or self-relax floors.

**Reality engineering is the difference between arifOS being a paper constitution and arifOS being an enforced constitution.**
