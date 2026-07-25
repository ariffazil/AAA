# Amendment A02 — Governed Digest Gate (Hermes)

## 1. Context
**Organ:** Hermes (INTELLIGENCE digest, WELL modulation)  
**Planes:** 3→1 (INTELLIGENCE→SOVEREIGN)  
**EUREKA:** Plane Interaction Matrix — Intelligence→Sovereign = propose-only  
**Canon:** 000_KERNEL_CANON §7 — Governance Primacy

## 2. Doctrine Violated (Before)
- Hermes synthesizes and delivers directly to Sovereign (Telegram)
- No governance classification, verdict, receipt, or cooling
- Phase C modulation loop operates entirely outside arifOS

**Result:**
- Plane violation: INTELLIGENCE issuing de facto verdicts
- F3 (TRI-WITNESS), F4 (CLARITY), F11 (AUDITABILITY) void

## 3. Constitutional Amendment (Membrane)
All Hermes outbound digests MUST pass through a Governed Digest Gate:

- **Hermes:** propose_digest() (INTELLIGENCE plane only)
- **333:** `arif_think` classifies digest (INFO / ALERT / RISK / ACTION)
- **888:** `arif_judge` issues verdict (SEAL / HOLD / VOID)
- **999:** `arif_seal` writes receipt to VAULT999
- **Delivery:** only SEAL digests are sent to Sovereign (Telegram)

### Wrapper (normative pattern)
```bash
hermes_outbound() {
  PID=$(arif_init --lease-class=DIGEST)
  CLASS=$(arif_think --digest "$DIGEST" --lease-id "$PID")
  VERDICT=$(arif_judge --class "$CLASS" --lease-id "$PID")
  if [ "$VERDICT" = "SEAL" ]; then
    sendtotelegram "$DIGEST"
    arif_seal --lease-id "$PID" --organ "Hermes"
  fi
}
```

## 4. Doctrine Restored (After)
- INTELLIGENCE→SOVEREIGN path becomes propose→govern→deliver
- Phase C modulation becomes governed loop with receipts and cooling
- F3, F4, F11 re-instated; WELL thresholds tunable via cooling data

## 5. Seal
**Branch:** `arch/tri-agent-boundaries`  
**Verdict:** SEAL  
**Scope:** All Hermes outbound channels MUST adopt Governed Digest Gate.
