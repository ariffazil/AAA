# Spawn Inheritance Policy — REFRAMED for No-Blocks

> **CCC-T-06 REFRAME (2026-09-18)** — supersedes "spawn without envelope = DENY" framing
> **Authority:** INV-01 + INV-06 (per-spawn governance, flat tree) + sovereign directive "no capabilities reduction, no tool blocks"
> **Status:** POLICY REFLECTIVE — observation + warning receipt, NOT denial

## The reframe

The original GAP-06 framed spawn inheritance as a **denial gate**: "Spawn without envelope = denied."

Per sovereign directive (`plan how to lower the blast radius and entropy and confusion for aaa ccc coding agent`), denial gates reduce entropy by **preventing** violations. But they also **reduce citizen capability** — precisely what the sovereign rejected.

**Reframe:** spawn inheritance is an **inheritance default + observation warning**, not a denial.

```
spawn_request: 
    ↓
A. If parent_envelope exists → INHERIT (child receives parent's envelope with auto-derivation):
     - child.ceiling <= parent.ceiling (cap holds)
     - child.receipt.parent_receipt = parent.receipt.receipt_id (chain)
     - child.constraints ⊆ parent.constraints ∪ spawn.constraints (union, not extension)
     - child.tier classified by tool classification, NOT widened by parent

B. If parent_envelope absent (root spawn or orphan) → AUTO-DERIVE from spawn_request:
     - authority = OBSERVE_ONLY (root spawn default)
     - tier = tool classification (READ_ONLY → OBSERVE, LOCAL_REVERSIBLE → T1, etc.)
     - constraints = ["no-self-modification", "fail-closed", "receipt-required", "envelope-required"]
     - parent_receipt = "" (root, allowed by envelope schema gate)

C. AFTER auto-derivation → emit WARNING receipt if any field was missing:
     - log "spawn_inheritance_warn" event with missing-field details
     - DOES NOT BLOCK the spawn
     - surfaces to telemetry for entropy monitoring

D. NEVER block the spawn
```

## What this achieves (entropy reduction, not capability reduction)

- **Visibility:** every spawn produces an envelope, observable in receipt trail
- **Defaults:** defaults are safe (OBSERVE_ONLY root, tier-from-tool-class)
- **No false denials:** no citizen loses a tool because they forgot to attach an envelope
- **Inheritance preserved:** INV-01 (authority stays at center) holds — child can't widen
- **Drift detection:** warning receipts surface citizens who skip envelope intentionally (signal, not noise)

## Detection without blocks

The warning receipt path is the "anti-Bangang Gate" (per `agi-asi-skills-fundamentals.md`):
- "phantom capability and phantom absence are the same defect with sign flipped"
- A spawn with no envelope isn't a missing capability — it's a missing observation
- Making it visible (warning receipt) is more useful than denying it

## What is NOT changed

- INV-01: authority never transfers (held by inheritance cap)
- INV-09: capability ceilings override prompt instructions (no change)
- F1 AMANAH: irreversible mutations still require SEAL first (separate gate)
- F13 SOVEREIGN VETO: human override preserved

## Verdict

Spawn inheritance closes via **defaults + visibility**, not denial. ΔS impact: −0.3 (reduced complexity of "deny + exception handling" → "default + warning"). Citizen capability: UNCHANGED.

> **DITEMPA BUKAN DIBERI ⚒️**
> **Path:** `/root/AAA/federation/protocols/spawn-inheritance-policy.md`
> **Supersedes:** GAP-06 "spawn without envelope = denied" framing in `AAA_FEDERATION_GAP_REPORT.md`
> **Status:** POLICY REFLECTIVE — observation, not enforcement
