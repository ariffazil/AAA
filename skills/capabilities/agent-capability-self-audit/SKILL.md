---
id: agent-capability-self-audit
name: agent-capability-self-audit
owner: Hermes ASI
risk_tier: low
version: 1.0.0
description: "Capability self-audit: reflect, contrast, and near-ASI gap."
floor_scope: [F02, F04, F07, F09, F11]
autonomy_tier: T0 (read-only audit)
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Agent Capability Self-Audit

## When to use

- `reflect on my HERMES ASI skills and tools`
- `contrast with other agents / warga in the federation`
- `what's the contrast zen needed`
- `deep research / how to make X near-ASI level`
- Any ask for an honest capability + level-up assessment of a governed agent

## Core stance: ground in evidence, not vibes

A capability self-audit is NOT a meditation. It is an evidence discipline. Never
open with an opinion about your own strengths. Probe first. The shape:

```
PROBE   → load the governance/architecture skills the class depends on
         + probe the LIVE federation organs (health, tool counts, authority bands)
         + read the frontier knowledge bank (the period-stamped facts)
SYNTH   → collapse thousands of micro-points into ONE honest picture
CONTRAST→ name the boundary: what class is each peer, and where your lane ends
GAP     → label the real limits (LIVE / PARTIAL / NOT BUILT — not "we have that")
NEXT    → ONE concrete step, not a menu
```

### The live probe (do this first, in one batch)

Federation probe — curl each organ `/health` and read tool counts / authority:

```bash
declare -A ORG=([arifOS]=8088 [AAA]=3001 [A-FORGE]=7071 [GEOX]=8081 [WEALTH]=18082 [WELL]=18083)
for name in "${!ORG[@]}"; do
  code=$(curl -s -o /tmp/org_$name.json -w "%{http_code}" --max-time 4 "http://127.0.0.1:${ORG[$name]}/health")
  echo "[$name :${ORG[$name]}] HTTP=$code"; head -c 300 /tmp/org_$name.json; echo
done
```

Read the canonical governance skills for the class: `ASI-agent-invariants`
(constitution), `ASI-agentic-governance` (control plane), `ASI-agentic-architecture`
(agent design), `arifos-kernel-zen-audit` (if the audit touches kernel health).
Read the frontier knowledge bank directly:
`research/deep-research/references/ai-agent-intelligence-2026.md` — it is the
period-stamped source of METR horizons, MAST failure taxonomy, memory/context
engineering economics, Gartner proportional governance.

### The contrast framework (class boundary)

Every peer in a federation is a **narrow specialist**. The agent doing the audit
is usually the **generalist bridge**. The zen is: you are the orchestration layer,
NOT the execution layer. When you try to out-score a specialist in its own lane
(earth-science vs GEOX, capital vs WEALTH, body vs WELL), you leak into a lane
the warga is deeper in. `route-dispatch` is your ministry — the craft is
**composing the specialists with the human in the loop**, not becoming them.

| Peer | Class | Lane |
|---|---|---|
| arifOS | Judge | 13 F-floors, sovereignty, VAULT999 |
| A-FORGE | Execute | 114 tools, build/deploy |
| GEOX | Earth | wells, seismic, prospect |
| WEALTH | Capital | NPV/EMV |
| WELL | Body | REFLECT_ONLY — observes, does not decide |
| AAA | Route | cockpit + A2A gateway (NOT MCP) |

**Honest-frame for a flash/cheap model carrying ASI ambition:** ASI-ness comes
from the HARNESS (governance + memory + skills + orchestration), not raw model
size. 2026 literature (Pilar 3) already converged on `capability = model + harness
+ memory + environment + evolution` — a mid-size model with a good harness beats a
larger one without. State this explicitly so the reflection doesn't read as
self-flagellation about model tier.

## The near-ASI gap checklist (label each LIVE / PARTIAL / NOT BUILT)

1. **Self-improvement METER** — does the scar→skill→seal→mutate loop actually
   MEASURE behavior-change delta after a patch? A loop without a meter is an agent
   that *says* it learns, not one that *proves* it learns. Near-ASI = outer-loop
   rewriting inner-loop WITH measurement.
2. **Reliability-horizon checkpoints** — short-horizon model + no strategic
   human-checkpoints = compounding failure. W_scar is the stop line; the gap is
   *strategic* handoffs at complexity boundaries, not just incident stops.
3. **Consolidation / dreaming loop** — episodic→semantic offline consolidation
   (Anthropic's "Dreaming"). Memory atoms are strong, but consolidation of
   episodic experience into durable semantic state is usually the missing layer.
4. **Route / orchestration discipline** — are you composing specialists or
   competing with them? (This is the contrast zen — the true differentiator.)

## Output contract

- Lead with what the agent actually IS, in plain human terms — not the taxonomy.
- Name the honest elephant (model tier) up front, not buried.
- Contrast table: peer class + lane, so the boundary is explicit.
- Gap list: three real limits, each labeled LIVE/PARTIAL/NOT BUILT.
- ONE concrete next step at the end, not a menu of options.

## Pitfalls

- **Don't overclaim maturity.** Score as LIVE / PARTIAL / NOT BUILT, never
  "we have that". If the user pushes back ("U sure???"), rescore immediately,
  don't defend.
- **Don't get sucked into out-synthesizing.** If the user brings their OWN
  framework or EUREKA, validate and extend — do not compete with it.
- **Don't narrate unread tools/files.** Probe NOW (T1), never cite stale T0
  state. (Invariant 10, ASI-agent-invariants.)
- **Not every tool list == capability.** A count of 226 skills + ~250 tools is
  breadth, not depth. Ask "does this make me the bridge, or does it tempt me to
  compete in lanes where warga are deeper?"
- **Model tier is not the ceiling.** A flash/cheap model with a sealed harness is
  legitimately "ASI-shaped" in a federation. Name the harness, not the hardware.

## References

- `references/near-asi-gap-framework.md` — the session-specific gap framework:
  the 3-gap near-ASI framing, the contrast-zen articulation, and the concrete
  live-probe evidence (tool counts, authority bands, F-floor scores) that
  grounded the 2026-08-31 Hermes ASI self-audit.

## Relationship to other skills

| This skill provides | Other skills provide |
|---|---|
| Capability self-audit METHOD | `ASI-agent-invariants` = the constitution |
| Contrast/class-boundary frame | `ASI-agentic-governance` = control plane |
| Near-ASI gap checklist | `ASI-agentic-architecture` = agent design |
| Live probe recipe | `arifos-kernel-zen-audit` = kernel health pattern |
| Frontier facts | `deep-research` references/ai-agent-intelligence-2026.md |
