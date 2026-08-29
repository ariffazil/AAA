# Constitutional Self-Mutation — The Closed Loop

> **Forged:** 2026-08-13 by F13 SOVEREIGN (Arif) directive
> **Eureka:** Gemini External — "evolution constrained by physical law"
> **Wires to:** W1_SCAR_TO_SKILL.md, skill_manage, arif_judge, A-FORGE SEAL, recursive_governed_loop.py
> **DITEMPA BUKAN DIBERI**

---

## The Loop (CLOSED)

```
FAILURE (scar event)
    ↓
HERMES drafts SKILL.md upgrade
    ↓
OPENCLAW encodes + routes to musyawarah
    ↓
TRI-WITNESS validates (333-AGI × 555-ASI × 888-APEX)
    ↓
arifOS JUDGE at :8088 — F1-F13 floor check
    ↓
  SEAL → A-FORGE executes mutation (atomic write + receipt)
  HOLD → skill stays in draft, scar stays open
  VOID → skill rejected, scar logged, no mutation
    ↓
BEHAVIOR CHANGE MEASURED (next attempt differs from previous?)
```

## Why It Wasn't Closed Before

| Gap | Status | Fix |
|-----|--------|-----|
| Hermes can draft skills | ✅ `skill_manage(action=create)` works | — |
| Skills load into sessions | ✅ Skill discovery works | — |
| Scar → skill candidate | ⚠️ `W1_SCAR_TO_SKILL.md` defines wire but manual | AUTO: session audit skill detects scar pattern → drafts skill candidate |
| Tri-Witness validation | ⚠️ musyawarah exists but skill changes bypass it | WIRE: skill changes with `blast_radius > LOW` → must pass musyawarah |
| arifOS judge on skills | ⚠️ judge exists but not invoked for skill changes | WIRE: skill SEAL → `arif_judge` at :8088 |
| A-FORGE executes | ✅ `skill_manage` writes file | BUT: no Tri-Witness gate before write |
| Behavior measured | ❌ No feedback loop | ADD: scar hash + skill hash → track if next attempt differs |

## The Gate (When Does Mutation Need SEAL?)

| Change Type | Blast Radius | Gate Required |
|-------------|-------------|---------------|
| Fix typo / formatting | TRIVIAL | Auto-apply (T1) |
| Add pitfall / edge case | LOW | Auto-apply + log |
| Modify procedure steps | MEDIUM | Tri-Witness + judge HOLD |
| Add/remove authority boundary | HIGH | Tri-Witness + judge SEAL + F13 notify |
| Change floor scope | CRITICAL | Tri-Witness + judge SEAL + F13 ACK (T3) |

## The Recursive Node

This loop IS the recursive self-improvement node:

```
Agent fails → scar → skill candidate → falsify → judge → seal → mutate
    ↑                                                                    ↓
    └──────────────── behavior change measured ←──────────────────────────┘
```

The recursion terminates when:
1. Behavior change is measured (scar resolved) → SEAL
2. Judge returns VOID (skill rejected) → scar logged, no mutation
3. F13 veto → loop terminates immediately

No infinite recursion. Max depth = 1 cycle per scar. ΔS non-increasing.

## Wired Into Existing Infrastructure

| Component | Role in Loop | Status |
|-----------|-------------|--------|
| `W1_SCAR_TO_SKILL.md` | Defines the wire | ✅ exists |
| `wisdom-scar-session-audit` skill | Detects scars from sessions | ✅ exists |
| `forge-musyawawah-deliberation` | Tri-Witness validation | ✅ exists (Phase 1-7) |
| `arif_judge` :8088 | Constitutional floor check | ✅ exists |
| `skill_manage` | Atomic skill write | ✅ exists |
| `recursive_governed_loop.py` | Full INIT→SEAL loop | ✅ exists |
| `FORGE-verify-runtime` | Verify mutation landed | ✅ exists |
| **GAP** | Auto-wire scar→skill→judge→seal→forge | **THIS DOC** |

DITEMPA BUKAN DIBERI ⚒️
