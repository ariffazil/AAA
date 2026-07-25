# Amendment A01 — Bootstrap Lease Gate (OpenClaw)

## 1. Context
**Organ:** OpenClaw (bootstrap probes, cron)  
**Planes:** 3→4 (INTELLIGENCE→EXECUTION)  
**EUREKA:** Six-Plane Execution Loop — Plane 3→4  
**Canon:** 000_KERNEL_CANON §4 — 000→999 Pipeline

## 2. Doctrine Violated (Before)
- No identity binding (000 missing)
- No action class (333 missing)
- No governance verdict (888 missing)
- No receipt / cooling (999 missing)
- Cron executes directly, outside Golden Lifecycle

**Result:**
- Agentic Intelligence: M=0 (no learning)
- F4 (CLARITY) and F11 (AUDITABILITY) void

## 3. Constitutional Amendment (Membrane)
All OpenClaw executions MUST pass through a Bootstrap Lease Gate:

- **000:** `arif_init` issues Lease ID (LID) for each probe
- **333:** `arif_think` classifies action (P0/P1/P2)
- **888:** `arif_judge` issues verdict (SEAL / HOLD / VOID)
- **999:** `arif_seal` writes immutable receipt to VAULT999

### Wrapper (normative pattern)
```bash
openclaw_exec() {
  LID=$(arif_init --lease-class=BOOTSTRAP)
  CLASS=$(arif_think --action "$ACTION" --lease-id "$LID")
  VERDICT=$(arif_judge --class "$CLASS" --lease-id "$LID")
  if [ "$VERDICT" = "SEAL" ]; then
    run_probe
    arif_seal --lease-id "$LID" --organ "OpenClaw"
  fi
}
```

## 4. Doctrine Restored (After)
- All OpenClaw actions traverse 000→333→888→999
- Identity, class, verdict, receipt, cooling present
- F1 (REVERSIBLE), F4 (CLARITY), F11 (AUDITABILITY) measurable
- Agentic Intelligence: M>0 (failures become cooling data)

## 5. Seal
**Branch:** `arch/tri-agent-boundaries`  
**Verdict:** SEAL  
**Scope:** All bootstrap cron / probe scripts MUST adopt Bootstrap Lease Gate.
