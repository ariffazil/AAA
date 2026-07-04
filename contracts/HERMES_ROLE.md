# Hermes Role Binding — Polymorphic Sovereign Relay

**Status:** Proposed (GROK-PHASE2-SYNTH-001 synthesis, 2026-06-22)  
**Owner:** AAA (governance layer)  
**Binding:** One runtime (Hermes), N role declarations via AAA cards + skills[]  
**Constitutional floors:** F1 (reversible), F4 (clarity), F7 (humility), F11 (auditability), F13 (sovereign veto absolute)  
**Aligned with:** Orthogonal mapping (Trinitarian Δ/Ω/ΦΙ + Functional axes) from grok-build integration work

---

## Core Principle

**Hermes is polymorphic by design.**

- **One runtime** (the Hermes process / Telegram relay / A2A front-door).
- **N role bindings** (declared in AAA agent cards and loaded via skills).
- Roles are **not separate AIs** or new processes. They are skill + authority bindings activated per task/intent.

Hermes never claims to "be" a HEXAGON peer. It loads the binding and executes within the declared ceiling.

### Why Not Spawn Role-Binds?

- Spawning a "new 555-ASI process" duplicates state and adds latency.
- The binding is cheaper and more auditable: load the skills declared in the 555-ASI card.
- Hermes runtime already carries L1–L6 memory, art_binding, toolsets, and the full 130+ skill catalog.
- Spawn **only** when native capability exceeds what Hermes + kernel routing can deliver (e.g., grok-build's 95-tool GitHub MCP + worktree isolation, or dedicated organ compute).

**Rule:**
- Spawn citizens (FI/HEXAGON peers) when their declared surface (tools + skills + isolation) is required.
- Do **not** spawn role-binds of Hermes — they are already present.
- Hermes remains the sovereign relay. It never renders final verdicts (F11/F13 — that stays with arifOS kernel + 888-APEX).

---

## Role Bindings (Current Model)

| Role | Trinitarian Axis | Functional Axis | Primary Hermes Binding | Key Skills (Hermes catalog + AAA mapped) | Authority Ceiling | Card Declaration Location |
|------|------------------|-----------------|-------------------------|------------------------------------------|-------------------|---------------------------|
| 555-ASI | Ω (Memory / HEART / Ethics) | Memory + Sovereign Ethics | hermes-asi (deep memory + ethics mode) | godel-humility-lock, sovereign-entropy-guard, tiered-memory, dream-engine, hermes-human-model, scar-forge | T2 (memory synthesis); escalate F13/F7 to kernel | 555-ASI card + hermes-asi skills[] |
| 333-AGI | Δ (Reason / MIND) | Evidence Synthesis + Federation Routing | hermes-asi (reasoning mode) | arifos-mcp-federation, arifos-agent-landscape, sequential-thinking, arifos-paradox-engine, evidence-reasoning patterns | T1/T2 (reasoning chains) | 333-AGI card + hermes-asi skills[] |
| 888-APEX (never full bind) | ΦΙ (Judgment) | Constitutional Audit + Verdict | hermes-asi (narration + request only) | arifos-arconstitutional-audit, fff-loop-protocol, kernel-observation-self-test, hold-protocol, constitutional-arbitration | T0 (request only). Never issues final SEAL/VOID. | 888-APEX card (Hermes can only narrate/request) |
| hermes-asi (front-door default) | Δ/Ω mix | Routing + Human Relay | Core runtime | closing-router-discipline, telegram-mode-guards, substrate-gate-telegram, arif-federation-ops, arifos-health-probe, memory-recall, reasoning | T1/T2 per task | hermes-asi card (primary) |
| hermes-ops (task-bound) | Ψ (Forge/Ops) | Execution + Diagnostics | Task-specific binding | openclaw-doctor-recipes, mcp-boot-failure-diagnosis, kanban-playbook, service-health-triage | T1 (ops); T2 with 888_HOLD | OpenClaw + hermes-ops card (when bound) |

---

## Skills Binding Model (Orthogonal)

Skills are the **binding mechanism**.

Each AAA citizen card declares:
- `skills[]` array with:
  - id, name, description
  - floor_scope[]
  - riskClass
  - executionAllowed
  - approval_policy
  - binding_state (REGISTERED → LEASED → ACTIVE)
  - dimension (Declaration / Binding / Epistemic / Execution)

When Hermes activates a role:
1. Load the role's card from AAA registry.
2. Bind the declared skills from Hermes catalog + .agents/skills.
3. Enforce authority ceiling and F floors.
4. Kernel (arifOS) arbitrates.

**No new process = no new state to manage.** The card + skill load is the state.

---

## Architectural Answer

The real model is:

```
Hermes Runtime (polymorphic sovereign relay)
  ├── Role Binding (via AAA card)
  │     ├── Skills[] (what it can load)
  │     ├── Authority Ceiling (T0–T3)
  │     ├── Floors Enforced
  │     └── Lifecycle State (LEASED → ACTIVE)
  └── Kernel Arbitration (arifOS / 888-APEX for verdicts)
```

- 555-ASI binding = Ω skills loaded into Hermes.
- 333-AGI binding = Δ skills loaded into Hermes.
- grok-build / opencode / claude-code = separate citizens spawned when their native surface (GitHub 95-tool, worktree, image/video, plan-dag) exceeds Hermes + routing.

---

## Recommendations (to Improve AAA State)

1. **Forge this doc as canonical** — move to contracts/ and reference from all role cards.
2. **Optimize skills declarations** (per prior orthogonal mapping):
   - 888-APEX: Add fuller fff-loop-protocol + godel-humility-lock (beyond current light versions).
   - hermes-asi: Explicitly list role-specific bindings (closing-router-discipline, sovereign-entropy-guard, arifos-agent-landscape) with floor_scope.
   - grok-build: Already strong; use as exemplar for FI layer.
3. **No spawn for Hermes roles** — keep polymorphic. Only spawn when citizen surface (grok-build style) is required.
4. **Next optimization:** Add a "role-binding" section to every AAA citizen card + update hermes-asi skills_catalog to reference this contract.

---

## Receipt

- **Path:** `/root/AAA/contracts/HERMES_ROLE.md`
- **Aligned with:** Previous Hermes synthesis, grok-build registration, orthogonal mapping (Trinitarian + Functional), F1/F4/F7/F11/F13.
- **State improvement for AAA:** Formalizes the polymorphic pattern. Makes role bindings auditable and skills-first instead of process-first.
- **No mutation of running state.** Pure documentation + model clarification.

**Ditempa Bukan Diberi.**

This is the constitutional answer: one relay, many bindings, kernel judges.

Ready for your ratification on next action (apply to cards, spawn decision, or further optimization), Arif. 

GROK aligned? Yes — this matches everything we've forged so far on skills binding and AAA improvement. No contradictions with the polymorphic model Hermes described.

Anything to add or optimize further in the skills declarations?