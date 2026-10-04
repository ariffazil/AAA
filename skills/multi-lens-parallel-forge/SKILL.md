---
name: multi-lens-parallel-forge
description: For high-stakes artifacts (civic letters, code reviews, audit reports, strategic decisions), dispatch the SAME specification to N parallel agents with DIFFERENT cognitive lenses as Gödel E3 (provider diversity) operationalization. Synthesize strongest elements from independent drafts. Class-level umbrella for breaking convergence traps in long iteration trajectories. Triggers when iterations converge (v[N+1] ≈ v[N]), when artifact has multiple valid framings, or when sovereign explicit demands multi-perspective generation.
version: 1.0.0
forged: 2026-08-12
owner: F13 SOVEREIGN
risk_tier: medium
autonomy_tier: T2
floor_scope: [F1, F2, F4, F6, F7, F11, F13]
agent: 333-AGI × 555-ASI × 777-FORGE (multi-lane orchestration)
source_convergence: PETRONAS letter v12 multi-lens dispatch + Gödel E3 doctrine
dependencies:
  skills: [civic-petition-forge (domain-specific), arifos-constitutional-judge, FORGE-route-least-power, constitutional-publication-audit]
  servers: []
  tools: [delegate_task (parallel), terminal (CLI harness spawn), weasyprint, sha256sum]
triggers:
  - "iteration convergence trap (v[N+1] ≈ v[N])"
  - "high-stakes artifact needs multi-perspective"
  - "Gödel E3 operationalization for forge"
  - "parallel dispatch for provider diversity"
  - "multi-lens synthesis"
  - "3 agents different cognitive lenses same brief"
---

# Multi-Lens Parallel Forge

> **Class:** Dispatch same spec to N parallel agents with different cognitive lenses.
> **Lane:** Orchestration (333-AGI intent + 555-ASI evidence + 777-FORGE execution).
> **Output:** N independent artifacts + synthesized canonical version.

## When to use

Trigger when ANY high-stakes artifact needs multiple perspectives to escape convergence trap or maximize quality:

| Scenario | Why multi-lens works |
|----------|---------------------|
| Letter v[N+1] ≈ v[N] (polish, no breakthrough) | Different cognitive lenses surface different breakthroughs |
| Code review with multiple valid framings (security, performance, readability) | Each lens is a different risk model |
| Strategic decision with multiple stakeholders | Each lens surfaces different stakeholder impact |
| Audit report with multiple verification frameworks | Each lens is a different verification standard |
| Constitutional question with multiple floor interactions | Each lens is a different floor priority |
| Sovereign explicitly demands "do it 3 different ways" | Direct multi-perspective request |

**Do NOT use for:**
- Single trivial artifact (overhead exceeds benefit)
- Time-critical decisions (N×delay not affordable)
- When single perspective is clearly correct (e.g., F2 fact verification)

## The Core Principle

**Provider diversity IS the Gödel E3 operationalization.** This is not just for retrieval (web search) — it applies to artifact generation too.

The pattern:
```
SAME SPECIFICATION
        │
        ├─── Lens 1 (sovereign rigor)
        ├─── Lens 2 (creative reconciliation)  ── isolated contexts
        ├─── Lens 3 (compressed / surgical)    ── parallel execution
        │
        ▼
THREE INDEPENDENT DRAFTS
        │
        ▼
SYNTHESIZE STRONGEST ELEMENTS → CANONICAL ARTIFACT
        │
        ▼
APEX_JUDGE ISOLATE → VAULT999 SEAL → F13 DISPOSITION
```

Each lens catches what the others miss. Each lens surfaces different priorities. The synthesis is STRONGER than any single lens.

## The 3-Lens Standard

For most high-stakes artifacts, 3 lenses is the sweet spot:
- 2 lenses = one-axis comparison (insufficient for complex artifacts)
- 3 lenses = Gödel E3 minimum (different provider + different priority + different cognitive frame)
- 4+ lenses = diminishing returns + coordination overhead

### Lens 1 — Sovereign Rigor (777 EXECUTOR lane, audit-grade model)

**Cognitive priority:** F2/F11 verification, conservative voice, all scars/evidence integrated as named proof, fewer rhetorical flourishes.

**When this lens wins:**
- Artifact will face high-stakes external audit
- Sovereign wants maximum institutional weight
- Evidence integrity is the primary value

**Anti-pattern:** This lens produces SAFE artifacts. It misses breakthrough moments.

### Lens 2 — Creative Reconciliation (333 THINKER lane, vendor model)

**Cognitive priority:** Handle the most difficult emotional/tension element with grace + truth. One passage of tenderness toward real (not archetypal) witnesses, then re-ratify the rupture. Vary sentence rhythm.

**When this lens wins:**
- Artifact has tension between rupture and dignity (e.g., sovereign writing about family)
- Voice breakthrough is the primary value
- Audience includes humans (not just institutions)

**Anti-pattern:** This lens produces BEAUTIFUL artifacts that may lack structural precision.

### Lens 3 — Compressed / Surgical (333 THINKER lane, vendor model)

**Cognitive priority:** 6-8 pages max. Every sentence must earn its place. Less mak material, more institutional critique density. Less metaphor, more fact.

**When this lens wins:**
- Reader fatigue is a risk
- Sovereign wants efficiency over elegance
- Artifact must be readable in single sitting

**Anti-pattern:** This lens produces EFFICIENT artifacts that may lack emotional resonance.

## The Specification Pattern

Each lens gets the SAME constitutional frame and base context, but DIFFERENT lens-specific directive:

```yaml
# Base context (SAME for all lenses)
constitutional_frame:
  - F1-F13 floors
  - F13 SOVEREIGN authorization
  - arifOS Federation institutional witness
base_files_to_read:
  - /path/to/v[N-1]_letter.txt (previous iteration as base)
  - /path/to/SCAR_registry.json
  - /path/to/CANON.md
output_spec:
  - HTML file at /path/to/<slug>-<lens>.html
  - PDF render via weasyprint
  - SHA-256 hash printed in letter
  - File paths returned

# Lens-specific directive (DIFFERENT per lens)
lens_1_sovereign_rigor:
  priority: F2/F11 verification + conservative voice
  directive: integrate all SCAR_* as named proof points, fewer rhetorical flourishes
  output_name: <slug>-sovereign.html

lens_2_creative_reconciliation:
  priority: handle difficult element with grace + truth
  directive: one passage of tenderness toward real witnesses, then re-ratify rupture
  output_name: <slug>-reconciliation.html

lens_3_compressed:
  priority: 6-8 pages max, every sentence earns its place
  directive: less mak material, more institutional critique density
  output_name: <slug>-compressed.html
```

## The Dispatch Pattern

Three dispatch mechanisms (pick by environment):

### Mechanism A: delegate_task batch (preferred)

```python
delegate_task(
    tasks=[
        {
            "goal": "[full context + lens 1 specific directive]",
            "context": "[base spec]",
            "role": "leaf"
        },
        {
            "goal": "[full context + lens 2 specific directive]",
            "context": "[base spec]",
            "role": "leaf"
        },
        {
            "goal": "[full context + lens 3 specific directive]",
            "context": "[base spec]",
            "role": "leaf"
        }
    ]
)
```

**Pros:** Single API call, parallel execution, isolated contexts, structured return.
**Cons:** All subagents inherit parent model (no actual provider diversity). Configuration-driven provider override required for true diversity.

### Mechanism B: parallel terminal spawn (CLI harnesses)

```bash
# Spawn 3 CLI coding agents in parallel as background processes
terminal(
    command="kimi --prompt '[lens 1 directive]' --output /path/to/lens1.md",
    background=true
)
terminal(
    command="opencode --model deepseek --prompt '[lens 2 directive]' --output /path/to/lens2.md",
    background=true
)
terminal(
    command="qwen --prompt '[lens 3 directive]' --output /path/to/lens3.md",
    background=true
)
```

**Pros:** TRUE provider diversity (different CLIs, different models). Each harness has its own capability signature.
**Cons:** Requires multiple CLI harnesses installed. Coordination overhead.

### Mechanism C: hybrid (delegate_task for orchestration + CLI for one lens)

Use delegate_task for 2 lenses (general capability), spawn CLI for 1 lens (specialized capability, e.g., DeepSeek for sovereign rigor).

## The Synthesis Pattern

When N drafts return, synthesize:

```
┌─────────────────────────────────────────────────────┐
│  SYNTHESIS DECISION TREE                             │
├─────────────────────────────────────────────────────┤
│  1. Did any lens FAIL the constitutional audit?      │
│     → Discard failed lens. Use others.               │
│                                                      │
│  2. Did all lenses converge on same structure?       │
│     → Strong signal — synthesize from best of breed │
│                                                      │
│  3. Did lenses DIVERGE on structure?                 │
│     → Compare trade-offs. Pick based on:            │
│       - recipient (audience priority)               │
│       - constitutional weight (institutional need)  │
│       - sovereign preference (voice priority)       │
│                                                      │
│  4. Did any lens surface a breakthrough the others  │
│     missed?                                          │
│     → Adopt the breakthrough. Carry it forward.      │
│                                                      │
│  5. Did the lenses reveal UNKNOWN territory?         │
│     → F7 humility. Acknowledge. Do not pretend.      │
└─────────────────────────────────────────────────────┘
```

### The Marcus Aurelius Cut

When synthesizing, use the Marcus Aurelius test:

> *"If thou wouldst know aught to the purpose, ask of those who know; but ask with discrimination, and let each answer be weighed in the scales of reason."*

For each element across the N drafts, ask:
- Does this serve the sovereign's intent?
- Does this pass constitutional audit?
- Does this resonate with the recipient?
- Is this defensible if challenged?

If yes to all 4 → keep. If no to any → revise or discard.

## The Verification Chain

Multi-lens parallel forge follows the SAME verification chain as single-lens forge:

1. Each draft: render → SHA-256 → token-leak check → key-fact verification
2. Synthesis: merge strongest elements → re-render → re-hash
3. apex_judge isolate T3 (expect HOLD + f13_required=TRUE)
4. VAULT999 seal the CANONICAL synthesis (not each draft)
5. F13 disposition for dispatch

**Iron rule:** VAULT999 seals the SYNTHESIS, not the individual drafts. The drafts are working artifacts; the synthesis is the canonical artifact.

## Anti-Patterns

### AP1: Single-lens parallel dispatch
Dispatching same spec to N agents with SAME lens is NOT Gödel E3. It's just parallel execution. Different cognitive lenses are required.

### AP2: Synthesis that picks everything
Trying to include "best of all worlds" usually produces incoherent artifact. Marcus Aurelius cut requires DISCARDING elements that don't serve all 4 criteria.

### AP3: Treating each draft as equally valid
Lens 1 (sovereign rigor) and Lens 3 (compressed) may produce drafts of different lengths but different WEIGHTS. The sovereign rigor draft may be the canonical base even if compressed is the optimization target.

### AP4: Dispatching without convergence trap detection
Multi-lens is for breakthrough. If the trajectory has NOT converged (v[N+1] is structurally different from v[N]), single-lens iteration is still productive. Multi-lens is for convergence trap.

### AP5: Provider diversity without cognitive diversity
Using 3 different model providers with same prompt and same lens is NOT Gödel E3. The lens must change, not just the provider. Provider changes the lens capability; cognitive change is what E3 requires.

### AP6: Synthesis by averaging
"Don't make it too long, don't make it too short" = averaging = lowest common denominator. Synthesis must be DECISIVE, not statistical.

## Pitfalls

### P1: Convergence trap undetected
The 5-7 iteration cap means after 7 iterations, the trajectory HAS converged even if you don't notice. Run multi-lens at iteration 5+ by default.

### P2: Lens-specific directive too narrow
"Lens 3: keep it short" produces short artifacts without breakthrough. Lens directives must specify COGNITIVE priority (what to optimize for), not just one parameter.

### P3: Synthesis loses constitutional protection
When merging drafts, easy to drop the institutional witness, the F13 authorization, or the cryptographic anchor. Re-run constitutional audit on synthesis.

### P4: VAULT999 sealed individual drafts instead of synthesis
Drafts are working artifacts. The canonical artifact is the synthesis. Seal the synthesis, not the drafts.

### P5: F13 disposition confusion
Multi-lens produces multiple drafts. F13 must disposition the SYNTHESIS, not each draft. If F13 rejects synthesis, fall back to single best draft (typically sovereign rigor lens).

## When NOT to Use Multi-Lens

| Situation | Why single-lens is better |
|-----------|---------------------------|
| Trivial artifact | Overhead exceeds benefit |
| Time-critical | N×delay not affordable |
| Single clearly-correct perspective | Forced diversity creates noise |
| Iteration 1-3 | Convergence trap hasn't happened yet |
| Pure technical verification | F2 single-source verification is correct |

## Relationship to Other Skills

| Skill | Relationship |
|-------|--------------|
| civic-petition-forge | Domain-specific application of multi-lens pattern for letters |
| arifos-constitutional-judge | Constitutional audit gate after synthesis |
| FORGE-route-least-power | Routing for each individual lens |
| constitutional-publication-audit | Final audit before dispatch |
| output-attestation | Cryptographic verification for synthesis |

---

*Forged: 2026-08-12 from the PETRONAS letter v12 dispatch (3 lenses: sovereign rigor, mak reconciliation, compressed).*

*DITEMPA BUKAN DIBERI — Multi-perspective is forged, not averaged.*