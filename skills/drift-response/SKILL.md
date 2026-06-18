# Drift Response Skill — OpenClaw

## Purpose
Standard operating procedure for detecting, verifying, classifying, and responding to runtime drift signals across the arifOS federation. Replaces ad-hoc improvisation with a 5-step constitutional procedure.

## Trigger
- AGI🦞 drift alert (arifOS `/health` reports `runtime_drift: true`)
- Two-copy drift detected (`/root/arifOS/` vs `/opt/arifos/app/` divergence)
- Gateway MCP config vs live endpoint mismatch
- Contract version mismatch between organs

## 5-Stage Procedure

### Stage 1: DETECT
**What**: Probe all known drift signals.
**How**: Run `federation_health_scan.py` + compare `build_commit` vs `live_commit` + check `.pth` file existence.
**Output**: `drift_signals[]` — list of detected anomalies with source.

### Stage 2: VERIFY
**What**: Confirm drift is real, not a false positive.
**How**: 
- Call `/health?nocache=1` on arifOS — bypasses cached health
- Check NATS governance stream for recent drift events
- Compare file modification times (`stat`) between `/root/arifOS/` and `/opt/arifos/app/`
- Check if gateway was recently restarted (config may be stale)
**Output**: `verified: true|false` + `verification_evidence[]`

### Stage 3: CLASSIFY
**What**: Assign severity based on blast radius.
**How**:
| Class | Criteria | Example |
|-------|----------|---------|
| **NUISANCE** | Build vs live mismatch with no tool behavior change | Hash drift on same commit, cosmetic only |
| **IMPORTANT** | Code divergence could affect tool behavior | Two-copy drift where `core/` differs |
| **CRITICAL** | Drift affects constitutional floors or governance | E7 enforcement broken, vault unreachable |
**Output**: `class: NUISANCE|IMPORTANT|CRITICAL` + `reasoning`

### Stage 4: PROPOSE
**What**: Concrete remediation, gated by severity.
**How**:
- NUISANCE: Log and defer. No action needed.
- IMPORTANT: Propose fix (restart, re-deploy, rsync). Mark 888_HOLD for any systemd restart.
- CRITICAL: Immediate summary to Arif. Mark 888_HOLD. Propose emergency procedure.
**Output**: `proposed_actions[]` — ordered list with risk level per action.

### Stage 5: ROUTE
**What**: Deliver verdict to correct destination.
**How**:
- NUISANCE → Log to memory. No human notification.
- IMPORTANT → Log + present to Arif with 888_HOLD.
- CRITICAL → Log + alert Arif immediately (Telegram DM).
**Output**: `routed: true` + `destination`

## Output Schema
```json
{
  "drift_response": {
    "detected_at": "ISO8601",
    "stage_1_detect": {
      "drift_signals": [
        {"source": "arifOS /health", "signal": "runtime_drift", "detail": "build_commit=X vs live_commit=Y"}
      ],
      "total_signals": 1
    },
    "stage_2_verify": {
      "verified": true,
      "verification_evidence": ["/health?nocache=1 confirms drift", "NATS governance: no prior drift events for this hash"],
      "false_positive": false
    },
    "stage_3_classify": {
      "class": "IMPORTANT",
      "reasoning": "Two-copy drift between /root/arifOS/ and /opt/arifos/app/ — tool behavior may diverge"
    },
    "stage_4_propose": {
      "proposed_actions": [
        {"action": "rsync /root/arifOS/arifosmcp/ → /opt/arifos/app/arifosmcp/", "risk": "LOW", "reversible": true},
        {"action": "systemctl restart arifos", "risk": "888_HOLD", "reversible": true, "downtime_sec": 5}
      ]
    },
    "stage_5_route": {
      "destination": "Arif Telegram DM",
      "verdict": "888_HOLD — awaiting sovereign approval"
    }
  }
}
```

## Reversibility
- Stages 1-3: Read-only. No mutations.
- Stage 4: Proposal only. No auto-execution.
- Stage 5: Logging only.
- **Never auto-executes restarts.** Always routes through 888_HOLD.

## F2 Note
This skill observes live system state. It does not attempt to fix drift autonomously — that would violate F13 + E7 PRINCIPAL band boundary.
