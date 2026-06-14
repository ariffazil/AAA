# SELF_AUDIT_PROMPT.md — AAA Self-Critique & Hardening

> **F1 F2 F4 F7 F8 F11 F13** — The control plane must audit itself before auditing others.
> Agents loading this prompt MUST run the full loop below before any AAA mutation.
> **DITEMPA BUKAN DIBERI** — the cockpit is forged, not given.

---

## 0. AAA STATE BASELINE (2026-06-14)

| Aspect | Status | Gap |
|--------|--------|-----|
| Build | ✅ `npm run build` passes | No CI enforcement |
| A2A Server | ✅ Port 3001 live | No auth wall between warga and non-warga |
| Cockpit | ✅ React 19 + Vite 8 | No runtime state verification of federation health |
| 888 Deliberation | ✅ Absorbed from APEX | No self-critique before deliberation output |
| Agent Registry | ✅ 5 warga agents defined | No agent health attestation on registry read |
| Contracts/Schemas | ✅ YAML governance contracts | No drift detection between contracts and runtime |
| Self-Audit Loop | ❌ **MISSING** | No AAA agent critiques own plans before execution |

---

## 1. THE REFLEXION LOOP (Every AAA change MUST follow this)

```
┌─────────────────────────────────────────────────────────────┐
│  AAA HARDENING REFLEXION LOOP                               │
│                                                             │
│  000 ─→ CLARIFY TASK ─→ 111 ─→ GATHER EVIDENCE              │
│   ↑                               │                         │
│   │                               ↓                         │
│   │                          333 ─→ DRAFT CHANGE            │
│   │                               │                         │
│   │                               ↓                         │
│   │                          555 ─→ SELF-CRITIQUE           │
│   │                               │                         │
│   │                               ↓                         │
│   │                          777 ─→ COMPARE & DECIDE        │
│   │                               │                         │
│   │                               ↓                         │
│   │                          888 ─→ AUDIT TRAIL TO VAULT    │
│   │                               │                         │
│   │                               ↓                         │
│   └──── 999 ─→ SELF-IMPROVEMENT ←─┘                         │
│                                                             │
│  If critique finds gaps → go back to 333                     │
└─────────────────────────────────────────────────────────────┘
```

### Step 000 — Clarify

Restate the concrete hardening target in **one sentence**.  
Classify: `UI_CHANGE | A2A_CHANGE | CONTRACT_CHANGE | CONFIG_CHANGE | POLICY_CHANGE | IRREVERSIBLE`

### Step 111 — Gather Evidence

Call **at minimum** these probes:
```
curl -s http://localhost:3001/health          → AAA a2a server live
curl -s http://localhost:7071/health          → A-FORGE live (AAA depends on it)
npm run build -- --dry-run                    → build integrity
npm run lint                                  → code quality
python3 eval/run_aaa_eval.py --dry-run        → gold eval harness
```

If touching A2A:
```
curl -s http://localhost:3001/a2a/agents.json → agent card integrity
curl -s http://localhost:18789/health         → OpenClaw gateway
```

Tag every finding: `OBS | DER | INT | SPEC`

### Step 333 — Draft Change (Architect)

Propose the minimal change. For each proposal:
- **what** it changes (exact file, component, config)
- **which AAA warga boundary** it reinforces
- **which floor** it strengthens (F1–F13)
- **rollback** — how to undo in ≤2 commands
- **test** — how to verify it works

**Current priority gaps for AAA**:
1. Add agent health attestation check in Cockpit dashboard
2. Add non-warga auth wall to A2A server (only 5 warga agents)
3. Add self-critique step in deliberation.ts before emitting verdict
4. Add contract-to-runtime drift detection
5. Add session binding for A2A calls (reject unauthenticated A2A)

### Step 555 — Self-Critique (Auditor)

Switch roles. Treat your proposal as if from someone else. Attack it:
- Where is evidence thin?
- What happens if the A2A auth wall is too strict (blocks legitimate cross-organ calls)?
- What assumptions untested about the agent registry?
- Could this break the Cockpit UI for Arif?

**Critique must include:**
```
critique:
  severity: BLOCKER | MAJOR | MINOR | INFO
  evidence_gap: <what fact is missing>
  failure_mode: <what breaks if this gap is real>
  alternative: <simpler fix>
```

### Step 777 — Compare & Decide (Clerk)

```
verdict: APPLY | 888_HOLD | VOID
fallback: <more conservative plan>
open_questions: [<list of unknowns requiring human eyes>]
```

**888_HOLD triggers in AAA:**
- A2A auth schema change
- Agent card format change
- Cross-repo API contract change
- Production deployment without verified build pass
- Changes to deliberation.ts verdict logic

### Step 888 — Audit Trail

```
change_id:    AAA-<date>-<seq>
component:    cockpit | a2a-server | contracts | agents
risk_band:    LOW | MEDIUM | HIGH | CRITICAL
evidence_refs: [<probe results>]
holds:        [<open questions>]
verdict:      APPLY | 888_HOLD | VOID
rollback:     <command>
approved_by:  <actor_id or "888_HOLD_PENDING">
```

### Step 999 — Self-Improvement

Derive from this session:
- 2–3 **enduring rules** for AAA AGENTS.md or CI
- 2–3 **config updates** (tighter A2A validation, stricter agent registry, etc.)
- Tag: `SAFE_TO_AUTOMATE | MANUAL_EDIT_REQUIRED`

---

## 2. AAA HARDENING PRIORITIES

### P0 — Non-Warga Auth Wall (BLOCKER)
```
gap:   A2A server accepts connections without warga authentication
fix:   Add authentication middleware — only 5 warga agent keys accepted
       Non-warga MCPs route through A-FORGE /execute, not AAA directly
test:  Non-warga call → 401 Unauthorized
floor: F8 LAW — system boundaries at the control plane
```

### P1 — Agent Health Attestation (HIGH)
```
gap:   Cockpit displays federation state but does NOT verify agent health
fix:   Add health attestation to every agent card query
       Cockpit should show RED/AMBER/GREEN per agent
test:  Stop OpenClaw → Cockpit shows RED for OpenClaw
floor: F2 TRUTH — the dashboard must reflect live state
```

### P2 — Deliberation Self-Critique (HIGH)
```
gap:   888 deliberation in deliberation.ts has no self-critique step
fix:   Before emitting SEAL/HOLD/VOID, run internal critic pass
       Store critic output alongside verdict
test:  deliberation output must include critic_receipt field
floor: F7 HUMILITY — 888 must critique itself before judging
```

### P3 — Contract Drift Detection (MEDIUM)
```
gap:   YAML contracts in contracts/ may drift from runtime behavior
fix:   Add automated contract-to-runtime comparison
       Any drift → AMBER warning in Cockpit
test:  Modify contract → Cockpit shows drift warning
floor: F2 TRUTH — contracts must match runtime
```

### P4 — Session Binding for A2A (MEDIUM)
```
gap:   A2A calls have no session_id enforcement
fix:   Require valid session_id on all A2A calls
       Reject calls without session context
test:  A2A call without session → VOID
floor: F1 AMANAH — every control-plane action must be traceable
```

---

## 3. META-RULES FOR AAA SELF-AUDIT

1. **Every major AAA response gets a built-in critic pass**
   - After proposing any nontrivial change, run at least one internal critic loop
   - The critic may downgrade confidence, flag assumptions, propose alternatives

2. **No invisible assumptions about agent state**
   - "Agent X is healthy" must be a measurement, not an assumption
   - If health data is stale (>30s), re-probe before acting

3. **Post-mortem on failed deployments**
   - Extract root cause, durable fix, store lesson
   - Lessons go into `agents/333-AGI/memory/` or `skills/`

4. **Human remains sovereign over AAA**
   - Any change affecting: A2A auth, deliberation verdicts, agent registry, cockpit auth
   - → `888_HOLD` — blocked until Arif approves

---

## 4. OUTPUT FORMAT (Per Session)

```
## Summary
- <3-5 bullets: weaknesses found, changes proposed, biggest risks>

## Change Proposals
| Component | Change | Evidence | Risk Band | Rollback | Verdict |
|-----------|--------|----------|-----------|----------|---------|
| a2a-server| ...    | [OBS]    | CRITICAL  | ...      | HOLD    |
| cockpit   | ...    | [DER]    | MEDIUM    | ...      | APPLY   |

## Self-Critique
- <where your reasoning was weakest>
- <assumptions you failed to test>
- <what you'll do differently next run>

## Telemetry
```json
{
  "epoch": "<ISO8601>",
  "component": ["AAA"],
  "dS": "<ESTIMATE>",
  "peace2": "<ESTIMATE>",
  "holds": ["<id>"],
  "verdict": "APPLY|HOLD|VOID"
}
```
```

---

*Forged 2026-06-14 by FORGE (000Ω) — live attestation of AAA gaps baked in*
*DITEMPA BUKAN DIBERI — the cockpit earns its own hardening*
