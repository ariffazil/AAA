# COOLING_RECEIPT v1 — VAULT999 Seal Type

> **SealType:** COOLING
> **Status:** DRAFT — constitutional draft for F13 ratification
> **Date:** 2026-07-13
> **Author:** Hermes (on Arif F13 directive, EUREKA architecture)
> **Supersedes:** None (new seal type)
> **Requires:** arif_seal mode `seal` with `event_type: "cooling.receipt"`

---

## 1. Purpose

COOLING_RECEIPT is the metabolic seal type that closes the learning loop.
It records what Reality observed after execution that the plan did not predict, and routes the insight back through GOVERNANCE — never directly to EXECUTION.

Without COOLING, the system is a 6-plane diagram.
With COOLING, the system is a metabolic cycle:

```
intent → judge → execute → verify → seal
                                    ↓
                              COOLING → drift? → improvement? → governance_path
                                    ↓
                              re-judge → (maybe) new seal
```

---

## 2. Envelope Schema

```json
{
  "seal_version": 3,
  "event_type": "cooling.receipt",
  "epoch": "<ISO8601>",
  "actor": "<actor_id>",

  "session_id": "<session_id of the cooled session>",
  "original_seal_seq": "<seq of the SEAL being cooled>",

  "original_verdict": {
    "verdict": "SEAL | HOLD | SABAR | VOID",
    "judge_hash": "<sha256 of the arif_judge verdict envelope>",
    "judge_summary": "<1-line summary of what 888 decided>"
  },

  "drift_detected": {
    "present": true | false,
    "observations": [
      {
        "dimension": "runtime_commit | tool_behavior | memory_staleness | authority_leak | unexpected_output | timing_anomaly | prediction_failure | human_reaction | other",
        "delta": "<what Reality saw that the plan didn't predict>",
        "epistemic_label": "OBS | DER | INT",
        "severity": "INFO | MINOR | SIGNIFICANT | CRITICAL"
      }
    ]
  },

  "proposed_improvement": {
    "hypothesis": "<what the cooling suggests would fix this drift>",
    "evidence": "<what supports this hypothesis>",
    "epistemic_label": "INT | SPEC",
    "risk_if_applied": "LOW | MEDIUM | HIGH",
    "risk_if_not_applied": "<what degrades without this fix>",
    "alternatives": ["<option A>", "<option B>"]
  },

  "governance_path": {
    "target_organ": "arifOS | A-FORGE | AAA | GEOX | WEALTH | WELL",
    "target_floor": "F1 | F2 | ... | F13",
    "required_authority": "AUTO | OBSERVE_ONLY | 888_HOLD | F13_SOVEREIGN",
    "judge_required": true | false,
    "reason": "<why this organ must judge this improvement>"
  },

  "supersedes": {
    "seal_seq": "<original seal seq>",
    "type": "COLD_LINK",
    "note": "This is lineage, not overwrite. The original SEAL is immutable."
  },

  "witness": {
    "human": "<human signal or null>",
    "ai": "<ai agent id or null>",
    "external": "<external evidence or null>"
  },

  "metabolism": {
    "cycle_count": "<how many COOLING receipts chain from this original SEAL>",
    "previous_cooling_seq": "<previous COOLING on same original seal, or null>",
    "convergence": "CONVERGING | DIVERGING | STABLE | first_cooling"
  },

  "cooling_source": "post_execution | post_verification | human_correction | scheduled_reflection | session_close"
}
```

---

## 3. Constitutional Invariants

### 3.1 COOLING-MUST-NOT-SELF-DEPLOY (keystone)

A COOLING_RECEIPT must NEVER directly trigger a mutation.
Its `proposed_improvement` is a **hypothesis**, not a patch.
It must return through `arif_judge` (or the governance path's required authority) for the improvement to reach execution.

**Enforcement:**
- `event_type: "cooling.receipt"` is always `action_class: "OBSERVE"`, never `"MUTATE"`
- `arif_forge` MUST NOT accept a COOLING_RECEIPT as an execution lease
- Only `arif_judge` can issue a new SEAL based on a COOLING improvement

**Rationale (F2 TRUTH + F9 ANTI-HANTU):**
If cooling could self-deploy, the agent would be authoring its own capabilities.
That is recursive self-authorisation — the exact catch-22 the EUREKA architecture was designed to eliminate.

### 3.2 COLD_LINK — Not Overwrite

`supersedes.type: "COLD_LINK"` means the original SEAL is NOT modified, replaced, or deleted.
The COOLING_RECEIPT creates a **forward reference** from the original seal.
This preserves:
- F1 AMANAH (irreversible actions stay irreversible)
- F11 AUDIT (original decision is still inspectable)
- F3 WITNESS (the cooling is independent evidence, not revisionist history)

### 3.3 Drift Must Be Named

`drift_detected` must contain at least one observation if `present: true`.
Observations must carry `epistemic_label` of OBS, DER, or INT — never SPEC for drift claims.
This enforces F2 TRUTH + F7 HUMILITY.

### 3.4 Governance Path Must Be Explicit

`governance_path.target_organ` must name a single organ.
`governance_path.judge_required` must be true unless `required_authority` is `AUTO`.
This prevents "routing to nobody" — every improvement goes somewhere.

---

## 4. Lifecycle

```
STEP 1: Session completes
    ↓
STEP 2: Hermes/agent detects drift
    (runtime hash mismatch, unexpected output, human correction,
     tool behavior change, memory staleness, timing anomaly)
    ↓
STEP 3: Classify drift
    OBS — directly observed (file hash differs)
    DER — derived from evidence (test count changed but root unknown)
    INT — interpreted pattern (3 similar drift events → systemic)
    ↓
STEP 4: Formulate improvement hypothesis
    Must be labeled INT (interpreted) or SPEC (speculated)
    Never OBS — improvements are not facts
    ↓
STEP 5: Determine governance path
    Which organ must judge this improvement?
    What authority level is required?
    ↓
STEP 6: Write COOLING_RECEIPT to VAULT999
    Immutable append. Cannot be retracted.
    ↓
STEP 7: Route to governance
    → arif_judge if judge_required
    → organ-specific review if AUTO authority
    → F13 if SOVEREIGN required
    ↓
STEP 8: Governance decides
    SEAL → new capability, new policy, or new SEAL
    HOLD → cooling insight stored but action deferred
    VOID → cooling insight was incorrect
    SABAR → waiting for more evidence
    ↓
STEP 9: If SEAL, new execution enters the cycle
    This time with the cooling insight as prior evidence
```

---

## 5. Governance Path Routing Rules

| `required_authority` | `judge_required` | Behaviour |
|---|---|---|
| AUTO | false | Cooling stored. Improvement applied autonomously if within existing capability. Receipt appended. |
| OBSERVE_ONLY | false | Cooling stored for human review. No auto-action. |
| 888_HOLD | true | Cooling routed to `arif_judge` with full envelope. Kernel decides SEAL/HOLD/VOID/SABAR. |
| F13_SOVEREIGN | true | Cooling routed to `arif_judge` with F13 escalation flag. Only Arif can approve the improvement. |

### Default routing by drift severity:

| Severity | Default Authority | Rationale |
|---|---|---|
| INFO | AUTO | Cosmetic — harmless recording |
| MINOR | OBSERVE_ONLY | Low-risk improvement, human review before action |
| SIGNIFICANT | 888_HOLD | Medium-risk — needs constitutional check |
| CRITICAL | F13_SOVEREIGN | High-risk — only sovereign can approve |

---

## 6. Cooling Source Types

| Source | Trigger | Typical Use |
|---|---|---|
| `post_execution` | After A-FORGE mutation completes | "The deploy changed 2 files more than planned" |
| `post_verification` | After verification step | "The test passed but coverage dropped 3%" |
| `human_correction` | Arif says "that was wrong" | "You misinterpreted my intent" |
| `scheduled_reflection` | Cron-triggered periodic audit | Weekly drift scan across all organs |
| `session_close` | 999-SEAL triggers automatic cooling | Standard post-session metabolism |

---

## 7. Metabolism Tracking

Each COOLING_RECEIPT carries a `metabolism` block that tracks the cooling chain for a given original SEAL:

```json
"metabolism": {
  "cycle_count": 3,
  "previous_cooling_seq": 9876,
  "convergence": "CONVERGING"
}
```

Convergence states:

| State | Meaning |
|---|---|
| `first_cooling` | First COOLING on this original seal |
| `CONVERGING` | Successive coolings have decreasing drift magnitude |
| `DIVERGING` | Successive coolings have increasing drift magnitude → escalate |
| `STABLE` | Multiple coolings report zero drift → coolings can become less frequent |

If `convergence: DIVERGING` persists for 3+ coolings, the system should escalate to `required_authority: F13_SOVEREIGN` regardless of individual severity — the pattern itself is the signal.

---

## 8. Integration Points

### 8.1 VAULT999 Writer

```python
# Pseudocode for seal_chain.js / seal_chain.py
if event_type == "cooling.receipt":
    validate_envelope(schema=COOLING_RECEIPT_v1)
    assert supersedes.type == "COLD_LINK"
    assert governance_path.judge_required or governance_path.required_authority in {"AUTO", "OBSERVE_ONLY"}
    append_to_chain(seq, prev_hash, this_hash, merkle_root, payload)
    route_to_governance(governance_path, seal_id)
```

### 8.2 arif_judge Integration

```python
# Pseudocode for arif_judge
if incoming_envelope.event_type == "cooling.receipt":
    cooling = incoming_envelope
    original = fetch_seal(cooling.supersedes.seal_seq)
    evidence = original.witness + cooling.drift_detected.observations
    verdict = compute_cooling_verdict(
        drift=cooling.drift_detected,
        improvement=cooling.proposed_improvement,
        evidence=evidence,
        floors=resolve_floors(cooling.governance_path.target_floor)
    )
    # verdict can be: SEAL (approve improvement), HOLD (defer),
    # VOID (improvement rejected), SABAR (more evidence needed)
    return verdict
```

### 8.3 Hermes Agent Integration

Hermes, sitting in the Intelligence plane, is the primary COOLING node:
- After every session close, Hermes checks for drift
- Hermes formulates the COOLING_RECEIPT
- Hermes routes it to governance
- Hermes does NOT execute the improvement

This respects SOUL.md §"How I Act": "I think, not build."

---

## 9. Example: Minimal COOLING_RECEIPT

```json
{
  "seal_version": 3,
  "event_type": "cooling.receipt",
  "epoch": "2026-07-13T01:00:00Z",
  "actor": "hermes-prime",

  "session_id": "SEAL-arifOS-deploy-2026-07-12",
  "original_seal_seq": 9906,

  "original_verdict": {
    "verdict": "SEAL",
    "judge_hash": "sha256:a1b2c3d4",
    "judge_summary": "Deploy arifOS commit b7374f2 to production"
  },

  "drift_detected": {
    "present": true,
    "observations": [
      {
        "dimension": "runtime_commit",
        "delta": "Deployed commit b7374f2 but /opt/arifos/app/.git_commit reads b7374f2-dirty (unstaged change in docs/)",
        "epistemic_label": "OBS",
        "severity": "MINOR"
      }
    ]
  },

  "proposed_improvement": {
    "hypothesis": "Add pre-deploy dirty-repo check to deploy-bridge.sh: git diff --quiet HEAD before rsync",
    "evidence": "3 of last 5 deploys had dirty-repo warnings post-deploy",
    "epistemic_label": "DER",
    "risk_if_applied": "LOW",
    "risk_if_not_applied": "Production runs code with uncommitted docs changes — minor but erodes runtime-truth discipline",
    "alternatives": [
      "Add post-deploy git status check to observatory MOTD",
      "Hard-fail deploy on dirty repos"
    ]
  },

  "governance_path": {
    "target_organ": "A-FORGE",
    "target_floor": "F9",
    "required_authority": "888_HOLD",
    "judge_required": true,
    "reason": "Pre-deploy verification is a safety workflow change — needs constitutional review"
  },

  "supersedes": {
    "seal_seq": 9906,
    "type": "COLD_LINK",
    "note": "Lineage only. Original deploy seal is immutable."
  },

  "witness": {
    "human": null,
    "ai": "hermes-prime",
    "external": "observed /opt/arifos/app/.git_commit path"
  },

  "metabolism": {
    "cycle_count": 1,
    "previous_cooling_seq": null,
    "convergence": "first_cooling"
  },

  "cooling_source": "post_verification"
}
```

---

## 10. What COOLING Does NOT Do

| Does NOT | Because |
|---|---|
| Mutate filesystem | That's A-FORGE's job |
| Issue new SEAL | That's arif_judge's job |
| Override original verdict | COLD_LINK preserves original |
| Self-authorise improvement | COOLING-MUST-NOT-SELF-DEPLOY |
| Replace human judgment | `required_authority: F13_SOVEREIGN` when needed |
| Run autonomously at critical severity | Escalates to 888_HOLD or F13 |

---

## 11. Implementation Order

| Step | What | Dependencies |
|---|---|---|
| 1 | Add `COOLING_RECEIPT` schema to VAULT999 schema registry | None |
| 2 | Add `event_type: "cooling.receipt"` validation to seal_chain.js | Step 1 |
| 3 | Add `arif_judge` mode `cooling_verdict` | Step 2 |
| 4 | Add `cooling_source` enum to `session_close` trigger | Step 2 |
| 5 | Wire Hermes `/seal_it` cognitive verb to emit COOLING after session seals | Step 3 |
| 6 | Add `metabolism.convergence` tracking to VAULT999 reader | Step 4 |
| 7 | Wire DIVERGING escalation to F13 | Step 6 |

---

*This spec is a constitutional draft. It will be ratified when F13 says "seal it."*
*DITEMPA BUKAN DIBERI — Cooling is forged, not given.*
