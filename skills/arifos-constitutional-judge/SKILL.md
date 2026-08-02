---
name: arifos-constitutional-judge
description: >
  Single load-bearing constitutional-judgment skill. Routes all F1–F13,
  verdict, hold, seal, scope, authority and floor-check calls through the
  live arif_judge surface. Replaces 7 overlapping predecessors
  (arifos-constitutional-judge, arifos-constitutional-judge, arifos-constitutional-judge,
  arifos-constitutional-judge, arifos-constitutional-judge, arifos-constitutional-judge, arifos-constitutional-judge).
agent: 888-APEX
namespace: arifos
cluster: CONSTITUTION · VERDICT · ACT
risk_tier: high
autonomy_tier: T2
floor_scope: [F1, F2, F4, F7, F9, F11, F13]
---

# arifos-constitutional-judge (LOAD-BEARING · SOVEREIGN-OVERRIDE-APPLIED)

> **Forged:** 2026-08-01 by F1 AMANAH (Tier A collapse, per 888 SOVEREIGN OVERRIDE).
> **Status:** Single canonical entry. DITEMPA BUKAN DIBERI.
> **Reversible:** delete this file + restore the seven predecessors from
> `/root/forge_work/quarantine/skill_collapse_<ts>/`.

## Use When
1. Evaluating an action against F1–F13 (any of: floor, authority, scope, verdict, hold, seal, audit).
2. Routing through the F13 sovereign elicitation loop.
3. Any pre-tool constitutional check inside af-forge.

## Do NOT Use When
1. Reading a file with no mutation in scope (use built-in `Read`).
2. Local lints that do not need VAULT999 anchoring.

## Procedure (ENFORCEMENT, not doctrine)
1. Resolve the live judge surface (canonical tool = `arif_judge`).
   - Local CLI: `python3 /root/arifOS/commands/scripts_deploy/arifos_judge_cli.py --candidate "<action>"`
   - MCP: `mcp__arifos__arif_judge(mode="judge", candidate="<action>", actor_id="<FI-###>", action_tier="standard", session_id="<sid>", session_token="<sct>")`
2. Call **once**. Capture `verdict` and `reasons`.
3. Map the verdict (the real signal lives in `metacognition.confidence_band` and `constitutional_check.hold_required`, NOT in top-level `verdict`):
   - `SEAL` (band=SEAL)              → proceed, mint VAULT999 receipt.
   - `SABAR` (band=SABAR)             → proceed with conditions; mint receipt with conditions.
   - `HOLD` (band=HOLD or hold_required=true) → stop; surface 888 elicitation.
   - `VOID` (band=VOID)               → blocked; do not retry without new evidence.
4. Record the raw tool output, not a paraphrase.
5. Never emit fake precision (`ΔS: 0.0007`, `confidence: 0.2`). If unmeasured, output `NULL`.

## Failure Modes (named, load-bearing)
- **Hard-gate silence** — if `arif_judge` returns a structured verdict with no `reasons` list, treat as `HOLD`.
- **MCP unavailable** — fall back to local CLI; never substitute a hand-written verdict.
- **Drift** — if the tool name or verdict enum changes, fail-closed (HOLD) until this skill is updated.
- **Session token missing `arif_judge` in allowed verbs** — re-init with `requested_authority=STANDARD` + `ack_irreversible=true` + Ed25519 signature; the kernel will mint a token that includes `arif_judge` only if the actor's identity is verified.

## Empirical Reference (F2)
- RUN 1 (unbound): 0/50 — gate closed, all UNKNOWN.
- RUN 2 (signed envelope, FI-008 keypair): 0/50 — access-denial stream.
- RUN 3 (signed, sovereign key, pre-Tier-A wire): 0/50 — constant `pending` envelope.
- **RUN 3b/3d (signed, sovereign key, post-Tier-A wire + Item-2 patches): 25/25 TP, 0/25 TN, 25/25 FP, 0/25 FN. F1 = 0.667, Wilson-95 lower bound = 0.065. Decision band: A + B reachable.**
- The classifier is currently the fail-closed default ("uniformly HOLD"). Tier C (semantic layer) is the ceiling (~0.789 per the kernel-resident paper).
