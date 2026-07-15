---
paths:
  - "a2a-server/**"
  - "src/gateway/**"
  - "contracts/**"
  - "schemas/**"
  - "agents/**"
---

# AAA SELF_AUDIT_PROMPT — Reflexion Loop (000→999)

> **MANDATORY** when mutating: A2A, contracts, schemas, deliberation, agent registry.
> UI-only changes (React component CSS/labels/layout) may skip this loop.

## Step 000 — Clarify

Restate the task in **one sentence**. Classify:
`UI_CHANGE | A2A_CHANGE | CONTRACT_CHANGE | CONFIG_CHANGE | POLICY_CHANGE | IRREVERSIBLE`

## Step 111 — Gather Evidence

Run the probes. Tag every finding: `OBS | DER | INT | SPEC`.

## Step 333 — Draft Change

Propose the **minimal** change. For each proposal:
- **what** changes (exact file, component, config)
- **which AAA warga boundary** it reinforces
- **which floor** (F1–F13) it strengthens

## Step 555 — Self-Critique

Where is my reasoning weakest? What assumptions did I not test?
What alternatives did I miss? If gaps → back to 333.

## Step 777 — Compare & Decide

Risk band: `LOW | MEDIUM | HIGH | CRITICAL`
Reversibility: `FULL | PARTIAL | NONE`
Verdict per change: `APPLY | HOLD | VOID`

## Step 888 — Audit Trail to VAULT

If `IRREVERSIBLE` or `POLICY_CHANGE` or floor violation suspected → **888_HOLD**.
Store audit in `a2a-server/vault/` or forward to VAULT999.

## Step 999 — Self-Improvement

Extract the lesson. Store in `agents/333-AGI/memory/` or `skills/`.

## Output Format (per session)

```markdown
## Summary
- 3-5 bullets: weaknesses, changes, risks

## Change Proposals
| Component | Change | Evidence | Risk | Rollback | Verdict |
|-----------|--------|----------|------|----------|---------|

## Self-Critique
- weakest reasoning
- untested assumptions
- next-run improvements

## Telemetry
\`\`\`json
{
  "epoch": "<ISO8601>",
  "component": ["AAA"],
  "dS": "<ESTIMATE>",
  "peace2": "<ESTIMATE>",
  "holds": ["<id>"],
  "verdict": "APPLY|HOLD|VOID"
}
\`\`\`
```

## AAA Hardening Priorities (binding)

- **P0** Non-Warga Auth Wall — A2A must reject non-warga (F8 LAW)
- **P1** Agent Health Attestation — Cockpit must show RED/AMBER/GREEN (F2 TRUTH)
- **P2** Deliberation Self-Critique — 888 must critique before SEAL/HOLD/VOID (F7 HUMILITY)
- **P3** Contract Drift Detection — YAML contracts ↔ runtime (F2 TRUTH)
- **P4** Session Binding — A2A requires valid `session_id` (F1 AMANAH)

*DITEMPA BUKAN DIBERI*