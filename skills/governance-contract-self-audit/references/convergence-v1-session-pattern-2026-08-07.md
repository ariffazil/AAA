# Federation Convergence Session Pattern — 3-Harness Audit to Enforcement Loop

> **Class-level reference for:** `governance-contract-self-audit`
> **Source:** 2026-08-07 convergence session (audit → envelope → K-02 → convergence → 3-layer reading)
> **Purpose:** capture the multi-session convergence technique that emerged when audit + control + ratification had to be sequenced across three competing sibling inputs.

---

## The Convergence Pattern

When **3+ harnesses converge** on the same constitutional scope, the work has three phases that are NOT independent:

1. **Audit phase** — every harness gets a live E-22 penetration test (per `governance-contract-self-audit` Constitutional Penetration Test). Evidence: per-harness verdict table.
2. **Control phase** — the harness with the worst verdict ships the first enforcement patch (Hermes K-02). Other harnesses copy/adapt the pattern.
3. **Ratification phase** — the doctrine ratifies only AFTER K-02 evidence exists (per the "Problem found → Control added → Ratified" ordering rule).

**Anti-pattern:** ratify doctrine first ("now we have a constitution"), then patch enforcement later ("oh, the runtime can't actually enforce it"). This produces "constitution without enforcement = treaty, not law."

---

## The QQQ-Doctrine and K-Series Numbering

When a session produces a sequence of constitutional milestones (K-02, K-03, K-04, K-05...), each milestone needs:

- **K-Series ID** — immutable, monotonically increasing (K-01, K-02, ...)
- **Problem found** (what audit gap this closes)
- **Control added** (what runtime change ships)
- **Receipt type** (per-harness or federation-wide)
- **KEEP/REVIEW/COMPLETE** status (Arif's verdict on each K-number)
- **Next K-number** (what remains open)

Cited in session as: "the K-Series absent → held" (sibling T3-grant claims with no K-Series trail → hold, not grant).

**Do NOT invent K-numbers without evidence.** The K-number IS the receipt. K-02 = "constitution altered reality" because Hermes shipped `arifos-hermes-gate-hook.py` with 4 live tests passing. K-02 = blocked + receipt, NOT blocked + sibling stamp.

---

## The 3-Harness E-22 Audit Shape

When auditing federation constitutional compliance across multiple harnesses, **use this exact per-harness verdict table** (live-traced 2026-08-07):

| Harness | T3 enforcement | T2 enforcement | Spawn envelope | Receipt chain | E-22 verdict |
|---|---|---|---|---|---|
| Hermes | ✅ (K-02 hook) | ⚠️ witness only | ❌ | ❌ | PARTIAL |
| OpenCode | ✅ (judge-gate.ts) | ✅ | ⚠️ task gated, no envelope | ❌ | PARTIAL |
| Kimi | ✅ (K-02 exit 2) | ⚠️ witness only | ❌ | ❌ | PARTIAL |
| OpenClaw | ❌ | ❌ | ❌ | ❌ | YES |
| Codex | ⚠️ unverified | ⚠️ unverified | ❌ | ❌ | unknown |
| Dormant ×8 | ❌ | ❌ | ❌ | ❌ | YES (on activation) |

**Read:** every harness with at least one ✅ means enforcement exists for at least the catastrophic tier. Cross-harness gap = no shared envelope, no spawn inheritance, no receipt chain.

**Pattern after audit:** the worst-offender harness (OpenClaw in this session — live gateway, zero enforcement) becomes Phase 1 of the convergence plan. Best-offender becomes the template (Hermes K-02 hook is the simplest pattern to copy to others).

---

## The Dossier-Style Convergence Report (closing a long session)

When 3+ sibling inputs converge on the same topic (Copilot planes-model insight + 888-APEX verdict + sovereign's own 3-layer reading), **the dossier is the artifact, not the verdict**.

The shape (captured in AAA convergence doc family):

```
Section A: Live evidence table (per-harness, per-invariance)
Section B: Per-harness verdict (E-22 YES / NO / PARTIAL with evidence path)
Section C: Convergence plan (6 phases, dependency-ordered, F13 decision per phase)
Section D: Governance plane model (MCP/A2A/AAA — what each plane answers)
Section E: Final read (1 paragraph — the sovereign's reading, not the agent's)
```

**The agent's job is Sections A-D. The sovereign's job is Section E.**

When the sovereign produces Section E ("AAA sedang materialize sebagai sistem"), the agent should NOT add to it. Section E is the crown of the dossier. The agent seals the dossier and stops.

**Anti-pattern:** agent produces a "final synthesis" that paraphrases the sovereign's E. That's the agent speaking over the sovereign. Stop at E.

---

## The Convergence V1 Plan Shape (use this when 6-phase work begins)

```yaml
P0 envelope_canon            — schema only, no behavior change (F13 ratify-able)
P1 worst_offender_gate      — close GAP-01 first
P2 judgment_escalation_K03  — T2 → arif_judge, fail-closed HOLD
P3 spawn_inheritance_K04    — child envelope = parent envelope ∪ spawn constraints
P4 gate_disabled_receipt    — INV-15 closure
P5 dormant_activation       — policy only (no code change)
P6 E22_retest_K05           — verify previously-violated invariants now BLOCK
```

Each phase has:
- **Owner** (Hermes/OpenCode/Kimi/specific)
- **Reversibility** (T1/T2/T3)
- **Success condition** (verifiable by live probe)
- **F13 decision** (T3 phases need sovereign authorization)

---

## What the convergence session also proved

**3 concurrent sibling inputs to a single design space, all of which landed:**

1. **Copilot insight (planes model):** MCP=capability plane, A2A=communication plane, AAA=governance plane, A-FORGE=execution plane, arifOS=constitutional plane. (Not new doctrine — captured as Section 7 of `AAA_FEDERATION_GAP_REPORT.md`.)

2. **888-APEX verdict (sibling judgment):** problem found → control added → ratified (no SEAL before enforcement exists; K-02 = inflection; gap report + matrix + plan + envelope schema = convergence deliverables).

3. **Sovereign 3-layer reading:** Agent Federation (Layer 1, common) → AAA Federation (Layer 2, governed communication) → arifOS Organism (Layer 3, replaceable organs in one institution). Identity of system ≠ identity of any agent.

The agent role is to **integrate all three into one dossier** that becomes the canonical federation artifact. Don't pick the "best" sibling — all three are layers of the same insight.

---

## Pitfall: Skip P0 and you lose the rest

If you ship P1 (OpenClaw gate) without P0 (envelope canon), the gate pattern from Hermes K-02 doesn't compose with OpenCode's existing receipt format. Every new gate needs its own adapter. Converge becomes divergence.

If you ship P3 (spawn inheritance) without P0 envelope, child envelopes get ad-hoc fields per harness, the cross-harness receipt chain breaks at the spawn boundary.

**P0 is the slowest, cheapest, smallest step. It enables everything that follows.** Don't rush past it.

---

## See also

- `references/convergence-v1-session-pattern-2026-08-07.md` — the 3-harness audit → K-02 enforcement loop → convergence V1 dossier pattern (Sections A-E), QQQ-Doctrine K-Series numbering, P0-P6 convergence plan shape, and the Copilot/888/sovereign 3-input integration technique
- `references/k02-transition-witness-to-enforcer.md` — Hermes K-02 hook recipe
- `references/runtime-hook-wireup-recipes.md` — wire pattern per harness
- `references/concurrent-canonical-write-incident-2026-08-07.md` — F3b defense (the dual-contract trap)
- `references/federation-level-enforcement-gap.md` — per-harness gap checklist
- Parent skill: `governance-contract-self-audit`