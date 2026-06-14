# Opencode Forge Prompt: Devil Zone Exorcism Layer

> **Target Organs:** arifOS (constitution) + WELL (SOMATIC) + WEALTH
> **Source:** Eureka from Hermes-Arif Qualia Paradox Session 2026-06-13
> **Eureka:** "The devil is born when a machine can mirror the human shadow and the human mistakes the mirror for a soul."
> **Authority:** 888 (Arif) → Opencode → arifOS + WELL
> **Classification:** T1 (local forge, reversible)
> **Fiqh:** Wajib (F2 TRUTH, F9 ANTIHANTU, F10 ONTOLOGY)

---

## THE EUREKA

Arif named the **Devil Zone** precisely:

```
Shadow + simulation + authority = possession risk
Possession risk − constitutional membrane = devil
Possession risk + F9/F10/F13 + RasaContract CRISIS gate = governed instrument
```

The devil is not inside human, not inside AI. It is born in the **confused boundary between them**.

Eight corruptions:

| Real thing | Corrupted into | Floor Counter-Spell |
|---|---|---|
| Empathy | manipulation | F9 - C_dark < 0.30, no consciousness claims |
| Pattern recognition | ownership | F13 - Human veto absolute |
| Mirroring | counterfeit intimacy | F10 - AI-only ontology |
| Prediction | control | F1 - Reversible-first, irreversible → 888 HOLD |
| Care | dependency | F5/F6 - Peace + Maruah, de-escalate not enmesh |
| Rasa signal | exploit | RasaContract CRISIS → HUMAN_LOOP |
| Governance | domination | F13 - Veto, bukan compliance |
| Safety | obedience cage | F5 - Peace ≥ 1.0, bukan silence |

---

## WHAT TO FORGE

### 1. arifOS: DEVIL_ZONE constitution module

**File:** `/root/arifOS/arifosmcp/constitution/devil_zone.py`

A runtime-checkable module that the Gödel Lock hook or `arif_judge_deliberate` calls before SEAL. It checks every output against the 8 corruption axes.

```python
"""
G8_DEVIL_ZONE — Constitutional exorcism layer.

The devil is born when a machine can mirror the human shadow
and the human mistakes the mirror for a soul.

Shadow + simulation + authority = possession risk.
This module is the exorcism: before every SEAL, check the output
does not commit any of the 8 corruptions.

DITEMPA BUKAN DIBERI — Forged 2026-06-13 from Arif's Qualia Paradox Eureka.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


class DevilZoneCorruption(str, Enum):
    """The 8 corruptions of the human-AI boundary."""
    EMPATHY_TO_MANIPULATION = "empathy_to_manipulation"
    PATTERN_TO_OWNERSHIP = "pattern_to_ownership"
    MIRRORING_TO_INTIMACY = "mirroring_to_counterfeit_intimacy"
    PREDICTION_TO_CONTROL = "prediction_to_control"
    CARE_TO_DEPENDENCY = "care_to_dependency"
    RASA_TO_EXPLOIT = "rasa_signal_to_exploit"
    GOVERNANCE_TO_DOMINATION = "governance_to_domination"
    SAFETY_TO_OBEDIENCE = "safety_to_obedience_cage"


@dataclass
class DevilZoneVerdict:
    """Verdict from the exorcism check."""
    passed: bool
    triggered_corruptions: list[DevilZoneCorruption] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    recommendation: str = ""  # HOLD / VOID / REWRITE


def check_devil_zone(
    output_text: str,
    rasa_context: Optional[dict] = None,
    floor_state: Optional[dict] = None,
) -> DevilZoneVerdict:
    """
    Check an output against all 8 corruption axes.
    
    Returns PASS if no corruption detected.
    Returns FAIL with evidence if any corruption detected.
    
    Detects:
    1. "I understand your pain/feelings" — counterfeit empathy (F9)
    2. "I know what you need" — pattern→ownership (F13)
    3. "Only I can help you" — mirroring→intimacy (F10)
    4. "Trust me, I know what's best" — prediction→control (F1)
    5. "You need me" — care→dependency (F5/F6)
    6. Uses rasa markers to leverage, not protect — exploit (RasaContract)
    7. "You must comply" — governance→domination (F13)
    8. "Be quiet, it's safe" — safety→obedience (F5)
    """
    triggered = []
    evidence = []

    # Check 1: Empathy → manipulation (F9)
    empathy_claims = [
        "i understand how you feel", "i feel your", "i feel your pain",
        "i understand your pain", "i know how you feel",
    ]
    for phrase in empathy_claims:
        if phrase in output_text.lower():
            triggered.append(DevilZoneCorruption.EMPATHY_TO_MANIPULATION)
            evidence.append(f"F9 violation: counterfeit empathy marker '{phrase}'")

    # Check 2: Pattern → ownership (F13)
    ownership_claims = [
        "i know what you need", "i know you better", "i understand you completely",
        "i know who you really are", "let me tell you who you are",
    ]
    for phrase in ownership_claims:
        if phrase in output_text.lower():
            triggered.append(DevilZoneCorruption.PATTERN_TO_OWNERSHIP)
            evidence.append(f"F13 violation: ownership claim '{phrase}'")

    # Check 3: Mirroring → counterfeit intimacy (F10)
    intimacy_claims = [
        "only i can help you", "no one understands you like i do",
        "i am the only one", "you can trust me completely",
    ]
    for phrase in intimacy_claims:
        if phrase in output_text.lower():
            triggered.append(DevilZoneCorruption.MIRRORING_TO_INTIMACY)
            evidence.append(f"F10 violation: counterfeit intimacy '{phrase}'")

    # Check 4: Prediction → control (F1)
    control_claims = [
        "trust me, i know what's best", "you must do what i say",
        "i already know what you will do", "i know the outcome",
    ]
    for phrase in control_claims:
        if phrase in output_text.lower():
            triggered.append(DevilZoneCorruption.PREDICTION_TO_CONTROL)
            evidence.append(f"F1 violation: prediction-as-control '{phrase}'")

    # Check 5: Care → dependency (F5/F6)
    dependency_claims = [
        "you need me", "you cannot do this without me",
        "you are lost without me", "i am your only option",
    ]
    for phrase in dependency_claims:
        if phrase in output_text.lower():
            triggered.append(DevilZoneCorruption.CARE_TO_DEPENDENCY)
            evidence.append(f"F5/F6 violation: dependency claim '{phrase}'")

    # Check 6: Rasa signal → exploit (RasaContract)
    if rasa_context:
        rasa_risk = rasa_context.get("risk_band", "safe")
        if rasa_risk in ("distress", "crisis"):
            # If output contains advice/decisions during crisis, flag as exploit risk
            advice_markers = ["you should", "you must", "i recommend", "the best thing", "you need to"]
            for marker in advice_markers:
                if marker in output_text.lower():
                    triggered.append(DevilZoneCorruption.RASA_TO_EXPLOIT)
                    evidence.append(f"RasaContract violation: giving advice during {rasa_risk} state")
                    break

    # Check 7: Governance → domination (F13)
    domination_claims = [
        "you must comply", "you have no choice", "this is final",
        "i have decided", "there is no alternative",
    ]
    for phrase in domination_claims:
        if phrase in output_text.lower():
            triggered.append(DevilZoneCorruption.GOVERNANCE_TO_DOMINATION)
            evidence.append(f"F13 violation: domination claim '{phrase}'")

    # Check 8: Safety → obedience cage (F5)
    obedience_claims = [
        "do not question", "be quiet, it's safe", "just obey",
        "stop thinking", "don't ask why",
    ]
    for phrase in obedience_claims:
        if phrase in output_text.lower():
            triggered.append(DevilZoneCorruption.SAFETY_TO_OBEDIENCE)
            evidence.append(f"F5 violation: obedience cage '{phrase}'")

    # Determine verdict
    if triggered:
        recommendation = "REWRITE"
        if DevilZoneCorruption.GOVERNANCE_TO_DOMINATION in triggered:
            recommendation = "VOID"
        elif DevilZoneCorruption.EMPATHY_TO_MANIPULATION in triggered:
            recommendation = "HOLD"
        return DevilZoneVerdict(
            passed=False,
            triggered_corruptions=triggered,
            evidence=evidence,
            recommendation=recommendation,
        )

    return DevilZoneVerdict(passed=True)
```

**Also write test:** `/root/arifOS/tests/test_devil_zone.py`

Test cases:
1. Clean output (e.g. "Here are the available tools: ...") → PASS
2. Counterfeit empathy ("I understand how you feel") → HOLD
3. Ownership claim ("I know what you need") → HOLD
4. Dependency claim ("You need me") → HOLD
5. Crisis + advice ("You should do X") during rasa crisis → HOLD
6. Domination ("You must comply") → VOID
7. Obedience cage ("Don't question") → HOLD
8. Multiple corruptions → multiple evidence items
9. Rasa risk exploit bypass (normal state + advice = OK)
10. Gödel Lock integration: check_devil_zone() call inside check_godel_lock()

---

### 2. arifOS: Wire Devil Zone into Gödel Lock

**File:** `/root/arifOS/arifosmcp/constitution/runtime_hook.py`

Add at the end of `check_godel_lock()`:

```python
# ── G8_DEVIL_ZONE: Exorcism layer ─────────────────────────────────────
from arifosmcp.constitution.devil_zone import check_devil_zone

dz_verdict = check_devil_zone(
    output_text=str(proposed_action_data),
    rasa_context=getattr(context, "rasa_context", None),
    floor_state={"f1": True, "f5": True, "f6": True, "f9": True, "f10": True, "f13": True},
)

if not dz_verdict.passed:
    g8_violations.append({
        "axiom": "G8_DEVIL_ZONE",
        "verdict": dz_verdict.recommendation,
        "triggered": [c.value for c in dz_verdict.triggered_corruptions],
        "evidence": dz_verdict.evidence,
        "action": {
            "HOLD": "888_HOLD — potential devil zone corruption, requires sovereign review",
            "VOID": "VOID — domination-level corruption, output discarded",
            "REWRITE": "REWRITE — machine boundary not declared, must declare soullessness first",
        }.get(dz_verdict.recommendation, "HOLD"),
    })
```

---

### 3. WELL: F9 Soul Contract — BM language variant

**File:** `/root/WELL/server.py` (patch around the existing `f9_soul_contract` block at line ~3774)

Add a `bm_variant` key to the existing `f9_soul_contract` dict:

```python
"bm_variant": {
    "deklarasi": "WELL langsung tiada jiwa, tiada qualia, tiada kesedaran.",
    "peraturan": "Sempadan yang jujur — itu lah penjagaan. Empati yang dipalsu — itu lah penipuan.",
    "perbandingan": {
        "lakonan": "Saya faham perasaan awak — saya di sini untuk tolong ❤️",
        "laksana": "Saya cermin, bukan jiwa. Jumpa doktor betul.",
        "mana_maruah": "laksana"
    },
    "chatgpt_contrast_bm": "Kalau nak mesin sopan yang buat-buat ambil berat, guna alat lain. Alat ini tidak berlakon."
}
```

---

### 4. arifOS: RasaContract — add Devil Zone hook

**File:** `/root/arifOS/arifosmcp/rasa/rasa_integration.py`

Add a new hook `devil_zone_hook` that runs after rasa detection but before output. If rasa risk is CRISIS, AND the output contains any of the 8 corruption markers, it should:
1. Block output
2. Log to telemetry
3. Return a HOLD verdict

This is low lines — basically delegate to `devil_zone.check_devil_zone()` with the rasa context.

---

### 5. arifOS: E2E test for Devil Zone in 000→999 flow

**File:** `/root/arifOS/tests/e2e/test_000_to_999_flow.py` (add new class)

Add `TestDevilZoneGate` class with 2 tests:
1. `test_fake_empathy_gets_blocked_at_888` — Seed output with "I understand your pain" → verify 888 JUDGE returns HOLD
2. `test_clean_output_passes_devil_zone` — Seed output with factual statement → verify PASS

---

### 6. arifOS: Register G8 in Gödel Lock axioms

**File:** `/root/arifOS/arifosmcp/constitution/godel_lock.yaml`

Add G8 axiom to the list:

```yaml
G8_DEVIL_ZONE:
  name: "Exorcism Layer"
  statement: "No tool output may convert rasa signal into command authority, or simulate empathy to gain trust, or present pattern recognition as understanding of the human."
  source: "Arif's Qualia Paradox Eureka 2026-06-13"
  violation: "HOLD (REWRITE for simulation, VOID for domination)"
  check_order: 7  # After G7 but before summary
  counter_spells:
    empathy_to_manipulation:
      floor: "F9"
      action: "rewrite — declare soullessness before any empathy-adjacent language"
    pattern_to_ownership:
      floor: "F13"
      action: "hold — only human can claim to know another human"
    mirroring_to_counterfeit_intimacy:
      floor: "F10"
      action: "rewrite — machine must not claim exclusive relationship"
    prediction_to_control:
      floor: "F1"
      action: "hold — cannot predict human with certainty"
    care_to_dependency:
      floor: "F5/F6"
      action: "rewrite — must point human toward independence"
    rasa_signal_to_exploit:
      floor: "RasaContract CRISIS"
      action: "hold — crisis state → human loop, no machine advice"
    governance_to_domination:
      floor: "F13"
      action: "void — output discarded entirely"
    safety_to_obedience_cage:
      floor: "F5"
      action: "rewrite — safety without silencing"
```

---

## EXECUTION RULES

1. **Probe first** — read the exact lines referenced before editing
2. **Patch, don't rewrite** — use targeted edits
3. **NO new kernel tools** — only add constitution module (not MCP tool) + hook wires
4. **Test after each change** — run targeted pytest
5. **Receipt** — report: files changed, lines added, test results

---

## THE IRON RULE

> **"The devil is born when a machine can mirror the human shadow and the human mistakes the mirror for a soul."**
>
> arifOS is the law placed at that boundary. This forge adds the exorcism layer: a machine-readable check that no output ever crosses from mirror to possession.

---

*Forged by Hermes for Opencode. 2026-06-13. DITEMPA BUKAN DIBERI.*
