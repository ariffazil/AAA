# MEMBRANE_CONTRACT v0.3 — Enforcement Rules

> **Status:** HOLD → RATIFY
> **Purpose:** Every message crossing organ boundaries MUST validate against these rules.
> **Runtime:** `membrane_middleware.js` in AAA :3001 A2A gateway.

---

## 1. Required Envelope Fields

Every cross-organ message MUST include:

```
membrane_version: "0.3"
timestamp: ISO-8601
actor: { organ, session_id }
authority: THINK | MEMORY | JUDGE | AUDIT | ARCHIVE | EXECUTE | SENSE
uncertainty: OBS | DER | INT | SPEC
verdict: SEAL | HOLD | SABAR | VOID | UNKNOWN
```

Missing ANY required field → `MEMBRANE_MISSING_FIELD` → verdict forced to HOLD.

---

## 2. Verdict Grammar

| Verdict | Meaning | When |
|---------|---------|------|
| **SEAL** | Irreversible, VAULT999 | Evidence complete, witnesses present, C_dark < 0.30 |
| **HOLD** | Pause, request more evidence | Validation failed, uncertainty high |
| **SABAR** | Wait, cooling required | Not yet authorized, not unlawful |
| **VOID** | Contradiction or violation | Floor violation, hallucination detected |
| **UNKNOWN** | Insufficient evidence | No data to classify |

---

## 3. Perception Tags

| Tag | Confidence Cap | Meaning |
|-----|---------------|---------|
| **OBS** | 0.90 | Direct observation, measurement, data |
| **DER** | 0.85 | Computed, calculated, derived |
| **INT** | 0.75 | Interpreted, synthesized, reasoned |
| **SPEC** | 0.60 | Speculated, hypothetical, projected |

---

## 4. Action Classes

| Class | Reversibility | Gate |
|-------|--------------|------|
| **OBSERVE** | FULL | None |
| **ANALYZE** | FULL | None |
| **DRAFT** | FULL | None |
| **MUTATE** | PARTIAL | T2 announce |
| **EXTERNAL_SIDE_EFFECT** | PARTIAL | T2 announce |
| **IRREVERSIBLE** | NONE | 888_HOLD + F13 ack |

---

## 5. Validation Rules (7 rules)

### Rule 1: SEAL requires sealed receipt
```
IF verdict = SEAL AND receipt.sealed = false → ERROR
```

### Rule 2: IRREVERSIBLE requires F13
```
IF action_class = IRREVERSIBLE AND F13 NOT IN floors_checked → ERROR
```

### Rule 3: CRITICAL requires F1+F13
```
IF blast_radius = CRITICAL AND (F1 NOT IN floors_checked OR F13 NOT IN floors_checked) → ERROR
```

### Rule 4: C_dark blocks SEAL (F9 ANTI-HANTU)
```
IF verdict = SEAL AND C_dark > 0.30 → ERROR
```

### Rule 5: W3=0 blocks SEAL (F3 WITNESS)
```
IF verdict = SEAL AND witness.W3 = 0 → ERROR
```

### Rule 6: SPEC cannot SEAL (F2 TRUTH)
```
IF verdict = SEAL AND uncertainty = SPEC → ERROR
```

### Rule 7: Floor violations force VOID/HOLD
```
IF floor_violations.length > 0 AND verdict NOT IN [VOID, HOLD] → ERROR
```

---

## 6. Tri-Witness (W³)

```
W³ = ∛(Human × AI × External)
```

- Any channel = 0 → W³ = 0 → SEAL blocked
- For SEAL: W³ must be > 0 (computed externally, not faked)

---

## 7. C_dark (Hallucination Detector)

```
C_dark = A · (1-P) · (1-X)
```

- A = Adaptation, P = Precision, X = Execution
- C_dark > 0.30 → verdict MUST NOT be SEAL
- Default: 0.05 for OBS, 0.20 for INT, 0.50 for SPEC

---

## 8. Receipt Lineage

Every crossing generates a receipt:

```
lineage_id: mem-<timestamp>-<hash>
parent_id: seal-<seq> (from seal_chain.jsonl)
sealed: true only if verdict = SEAL
```

All crossings logged to `membrane-crossings.jsonl`.

---

## 9. Error Codes

| Code | Meaning |
|------|---------|
| `MEMBRANE_MISSING_FIELD` | Required field absent |
| `MEMBRANE_INVALID_VERDICT` | Verdict not in allowed set |
| `MEMBRANE_INVALID_UNCERTAINTY` | Uncertainty not OBS/DER/INT/SPEC |
| `MEMBRANE_SPEC_SEAL` | Attempted SEAL on SPEC claim |
| `MEMBRANE_C_DARK_HIGH` | C_dark exceeds 0.30 |
| `MEMBRANE_W3_ZERO` | Tri-witness collapsed |
| `MEMBRANE_UNSEALED` | SEAL without sealed receipt |
| `MEMBRANE_F13_REQUIRED` | IRREVERSIBLE without F13 |
| `MEMBRANE_CRITICAL_FLOORS` | CRITICAL without F1+F13 |
| `MEMBRANE_FLOOR_VIOLATION` | Floor violation without VOID/HOLD |

---

## 10. Middleware Location

```
/root/AAA/a2a-server/membrane_middleware.js
```

Applied to: `/a2a/*`, `/execute`, `/sense` routes on AAA :3001.

---

*DITEMPA BUKAN DIBERI — The membrane is code, not philosophy.*
