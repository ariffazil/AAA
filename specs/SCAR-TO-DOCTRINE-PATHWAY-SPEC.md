# SCAR → DOCTRINE PATHWAY — Formal Specification

> **Status:** [CANDIDATE — Lane B DRAFT] · 2026-09-08
> **Source:** Void-mapping research session SEAL-compile-2026-09-08
> **Predecessor:** `dunbar-constraint.md` §4b · `EUREKA-CONSEQUENCE-BINDING-2026-09-07.md` · `civ-21.md` E20 · `forge_scar` operational primitive
> **Axiom:** F1 AMANAH · F2 TRUTH · F7 HUMILITY · F9 ANTI-HANTU (pathway is structural, not psychological) · F11 AUDIT · F13 SOVEREIGN
> **Lane:** B (DRAFT pending 888-APEX verdict → Lane A CANONICAL)

---

## §0. The Problem

The void-mapping research identified the chain:

```
Experience → Scar → Memory → Rule → Policy → Institution
```

Current canon names pieces of this chain:

- **Experience:** `forge_experience_trace` ✓
- **Scar:** `forge_scar(mode=seal)` ✓ + `civ-21.md` E20 "Truth has a metabolism"
- **Memory:** `arif_memory(mode=promote)` ✓
- **Rule:** ??? — implicit only; distributed across `forge_policy` etc.
- **Policy:** `forge_policy` ✓
- **Institution:** ??? — no explicit "this scar is now institutional doctrine" primitive

**The chain is distributed across 4-5 tools with no auditable pathway.** A scar can be sealed but never promoted. Without promotion, scars accumulate as noise — the opposite of institutional learning.

---

## §1. The Pathway (6 transitions)

### Transition 1: Experience → Scar (already exists)

```
Trigger:   forge_experience_trace with new_scar set
Primitive: forge_scar(mode=seal)
Input:     failure_mode, severity, scar_pressure, domain
Output:    scar_pressure_receipt, scar_<id> sealed
F-floor:   F1 (reversible scar), F2 (evidence required)
Status:    ✓ OPERATIONAL
```

### Transition 2: Scar → Cooling Receipt (already exists)

```
Trigger:   recurring exception (>3 in 90 days)
Primitive: forge_cool_drift / forge_cool_pattern
Input:     scar_id, recurrence_count, first_seen, last_seen
Output:    cooling_receipt with governance_organ/floor proposal
F-floor:   F11 (every cooling is a receipt)
Status:    ✓ OPERATIONAL
```

### Transition 3: Cooling → Memory Promotion (partial)

```
Trigger:   cooling_receipt.severity = HIGH or scar_pressure > 0.5
Primitive: arif_memory(mode=promote, tier=L2 → L3)
Input:     scar_id, cooling_receipt_id
Output:    memory_promoted (L3 = institutional scar memory)
F-floor:   F11 (memory receipts)
Status:    ⚠ PARTIAL — no explicit promotion primitive
```

### Transition 4: Memory → Rule (MISSING — this spec)

```
Trigger:   L3 scar memory cited in ≥3 distinct decisions
Primitive: forge_scar_rule (NEW — proposed)
Input:     scar_id, memory_id, rule_text, scope, falsification
Output:    rule_<id> sealed with scar_lineage
F-floor:   F2 (rule carries epistemic label), F7 (cap confidence)
Status:    ✗ MISSING — gap in pathway
```

### Transition 5: Rule → Policy (MISSING — this spec)

```
Trigger:   rule cited in ≥3 distinct policy drafts
Primitive: forge_scar_policy (NEW — proposed)
Input:     rule_id(s), policy_text, scope, jurisdiction
Output:    policy_<id> sealed with rule_lineage
F-floor:   F11 (policy receipts)
Status:    ✗ MISSING — gap in pathway
```

### Transition 6: Policy → Institution (MISSING — this spec)

```
Trigger:   policy surviving ≥365 days without revision
Primitive: forge_scar_institution (NEW — proposed)
Input:     policy_id(s), institution_name, lineage
Output:    institution_<id> sealed with policy_lineage
F-floor:   F13 (institutional status requires sovereign ack)
Status:    ✗ MISSING — gap in pathway
```

---

## §2. The Pathway Diagram

```
Experience (forge_experience_trace)
       ↓ [T1, OP]
Scar (forge_scar)
       ↓ [T2, OP]
Cooling Receipt (forge_cool_drift)
       ↓ [T3, PARTIAL]
Memory L3 (arif_memory promote)
       ↓ [T4, MISSING]
Rule (forge_scar_rule)           ← NEW PRIMITIVE
       ↓ [T5, MISSING]
Policy (forge_scar_policy)       ← NEW PRIMITIVE
       ↓ [T6, MISSING]
Institution (forge_scar_institution) ← NEW PRIMITIVE
```

Each transition is auditable (F11). Each carries lineage back to the original scar (and the original experience that produced it).

---

## §3. Three New Primitives Proposed

### §3.1 forge_scar_rule (T4)

```python
def forge_scar_rule(
    scar_id: str,           # lineage
    memory_id: str,          # lineage
    rule_text: str,          # the rule itself
    scope: str,              # where it applies
    falsification_test: str, # what would falsify the rule
    confidence_cap: float = 0.90,  # F7
    epistemic_label: Literal['OBS','DER','INT','SPEC'],
) -> RuleReceipt:
    """
    Seal a rule derived from a scar memory.
    F2: rule_text must carry epistemic label
    F7: confidence capped at 0.90
    F11: receipt emitted with full lineage
    F12: falsification_test required (no test → HOLD)
    """
```

### §3.2 forge_scar_policy (T5)

```python
def forge_scar_policy(
    rule_ids: list[str],     # lineage
    policy_text: str,        # the policy itself
    scope: str,
    jurisdiction: str,
    conflict_check: bool = True,
) -> PolicyReceipt:
    """
    Seal a policy derived from rules.
    F11: receipt emitted with rule_lineage
    Conflict check: if policy contradicts an existing Lane A policy → HOLD
    """
```

### §3.3 forge_scar_institution (T6)

```python
def forge_scar_institution(
    policy_ids: list[str],
    institution_name: str,
    institution_type: str,  # doctrine, ritual, contract, norm
    f13_ack_required: bool = True,
) -> InstitutionReceipt:
    """
    Seal an institution derived from policies.
    F13: institutional status requires sovereign ack
    F1: institution is immutable once sealed
    """
```

---

## §4. Constitutional Constraints (HARAM)

The pathway **MUST NOT**:

- Skip transitions (no scar → policy shortcut; lineage breaks)
- Auto-promote scar to institution without citation count (noisy)
- Modify F1-F13 floors (no F14 yet)
- Hide transitions (F11 every step)
- Manufacture scar from non-failure (F9 + scar integrity)

The pathway **MUST**:

- Carry lineage through every transition (F11 + provenance)
- Emit receipt per transition (F11)
- Allow F13 to block any promotion (Lane A)
- Be reversible at any non-institutional transition (F1)

---

## §5. Falsification Tests

| Test | Discriminates | Pass condition |
|---|---|---|
| **Lineage test** | Inject scar, run full pathway to institution | InstitutionReceipt cites every transition back to original scar |
| **Citation count** | Scar cited 3 times → rule; cited 5 times → policy | Rule + policy promoted at correct thresholds |
| **F13 gate** | Try to auto-promote to institution | HARD HOLD; F13 ack required |
| **Reversibility** | F13 vetoes rule promotion | Rollback to T3 (memory L3) within 24h |
| **F11 audit** | Run pathway; inspect lineage | Every transition has receipt with scar_id |

---

## §6. F2 Audit Summary

| Component | Class | Falsifiable? | Survives? |
|---|---|---|---|
| T1-T3 (existing) | OBS | yes (forge_*, arif_*) | yes |
| T4-T6 (new primitives) | SPEC | yes (Lane A ratification) | yes |
| Citation thresholds | SPEC | yes (Lane A ratification) | yes |
| F13 gate at T6 | OBS | yes (ack receipt) | yes |

---

## §7. Ratification Path

```
Step 1 [DONE 2026-09-08]   : File as DRAFT (Lane B) — this artifact
Step 2 [T1, queued]        : contradiction_scan via geox_claim(mode=scan)
Step 3 [T2, 888-APEX]      : lane determination
Step 4 [T3, F13]           : if CANONICAL → VAULT999 append (constitutional pathway)
```

---

## §8. Provenance

**Session:** SEAL-compile-2026-09-08 · 2026-09-08
**Actor:** 333-AGI Δ MIND — proposer
**Trigger:** Void-mapping research identified VOID-4 (Scar Metabolism) — chain partially named, pathway missing
**Axiom-9 boundary:** pathway is structural, not psychological; transitions are auditable, not interpretive

---

*DITEMPA BUKAN DIBERI ⚒️*
