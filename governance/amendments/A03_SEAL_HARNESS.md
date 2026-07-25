# Amendment A03 — SEAL Harness (OpenCode → A-FORGE)

## 1. Context
**Organ:** OpenCode (INTELLIGENCE code synthesis)  
**Target:** A-FORGE (EXECUTION build/deploy)  
**Planes:** 3→4 (INTELLIGENCE→EXECUTION)  
**EUREKA:** Anti-Authorization Theorem (§7)  
**Canon:** 000_KERNEL_CANON §9 — Organ Invariants (A-FORGE executes under SEAL)

## 2. Doctrine Violated (Before)
- OpenCode issues git add/commit/push directly from INTELLIGENCE plane
- No blast-radius classification, capability lease, SEAL verdict, or receipt
- EXECUTION occurs without A-FORGE harness

**Result:**
- Direct breach of Anti-Authorization Theorem
- F1 (REVERSIBLE) only accidental; F8 (GENIUS) and F11 (AUDITABILITY) void

## 3. Constitutional Amendment (Membrane)
OpenCode MUST NOT execute mutations. It may only propose patches.

### New governed flow
1. **OpenCode:** propose_patch() — diff, intent, scope
2. **333:** `arif_think` classifies blast radius and capability lease
3. **888:** `arif_judge` issues verdict (SEAL / HOLD / VOID)
4. **A-FORGE:** executes mutation ONLY under SEAL
5. **999:** `arif_seal` writes immutable receipt to VAULT999
6. **Cooling:** A-FORGE outcomes feed back into arif_judge

### Harness (normative pattern)
```bash
opencode_exec() {
  CID=$(arif_init --lease-class=CODEPATCH)
  CLASS=$(arif_think --patch "$PATCH" --lease-id "$CID")
  VERDICT=$(arif_judge --class "$CLASS" --lease-id "$CID")
  if [ "$VERDICT" = "SEAL" ]; then
    aforge_apply_patch "$PATCH" --lease-id "$CID"
    arif_seal --lease-id "$CID" --organ "A-FORGE"
  fi
}
```

## 4. Doctrine Restored (After)
- INTELLIGENCE proposes; EXECUTION acts; GOVERNANCE rules
- Anti-Authorization Theorem enforced at the plane boundary
- F1, F8, F11 measurable; code changes become governed, auditable events

## 5. Seal
**Branch:** `arch/tri-agent-boundaries`  
**Verdict:** SEAL  
**Scope:** All OpenCode mutation paths MUST route via SEAL Harness into A-FORGE.
