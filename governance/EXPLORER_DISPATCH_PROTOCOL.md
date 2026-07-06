# Explorer Dispatch Protocol v1

> **Status:** IMPLEMENTED (wired to live tools)
> **Date:** 2026-07-06
> **Sovereign:** ARIF (F13)
> **Seal:** pending

---

## What This Is

The Explorer Dispatch Protocol (EDP) binds the federation's organs into a governed OBSERVE→HYPOTHESIZE→FALSIFY→VERIFY loop. Not aspirational — wired to live tools that exist today.

**One sentence:** EDP turns every query into an evidence-governed exploration cycle with explicit uncertainty, falsification, and verdict.

---

## Architecture

```
USER QUERY
    │
    ▼
┌─────────────────────────────────────────────────┐
│  DISPATCHER (Hermes)                            │
│  1. arif_route(intent) → organ                  │
│  2. Classify decision_context                    │
│  3. Build Explorer Packet                        │
└─────────────┬───────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    ▼                   ▼
┌──────────┐    ┌──────────────┐
│ OBSERVE  │    │ HYPOTHESIZE  │
│ organ    │───▶│ arif_think   │
│ tool     │    │ (LLM reason) │
│ call     │    │              │
└──────────┘    └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │  FALSIFY     │
                │  forge_eval  │
                │  forge_scar  │
                │  sandbox_run │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │  VERIFY      │
                │  arif_judge  │
                │  → SEAL      │
                │  → SABAR     │
                │  → HOLD      │
                │  → VOID      │
                └──────────────┘
```

---

## Stage Contracts

### Stage 1: OBSERVE

**Input:** User query + domain hint
**Process:**
1. `arif_route(intent=query)` → returns organ, tool_prefix, domain_law
2. Call organ-specific observation tool:
   - GEOX: `geox_evidence`, `geox_basin`, `geox_seismic_compute`
   - WEALTH: `wealth_compute_emv`, `wealth_monte_carlo_simulate`
   - WELL: `well_readiness`, `well_validate_vitality`
   - arifOS: `arif_observe(mode=search|fetch|ingest)`
3. Tag all evidence with class: OBS / DER / INT / SPEC
4. Record missing evidence explicitly

**Output:** Explorer Packet — observation section populated

**Gate:** All evidence must carry provenance + confidence + falsifiable_by

---

### Stage 2: HYPOTHESIZE

**Input:** Explorer Packet (observation section)
**Process:**
1. `arif_think(mode=reason)` with observation context
2. Generate minimum 2 ranked hypotheses
3. Each hypothesis must include:
   - Statement (falsifiable claim)
   - Prior (0-1, based on domain knowledge)
   - Supporting evidence IDs
   - Missing tests
   - Alternative explanations (minimum 1)
4. Compute combined prior via Nash product if multiple evidence sources

**Output:** Explorer Packet — hypotheses section populated

**Gate:** No hypothesis without alternatives. No prior above 0.90 (F7).

---

### Stage 3: FALSIFY

**Input:** Explorer Packet (hypotheses section)
**Process:**
1. For each hypothesis, list falsification tests:
   - What test would kill this hypothesis?
   - Has it been run? (passed / failed / not_run / impossible)
   - What's the cost to run? (LOW / MEDIUM / HIGH)
2. `forge_scar(domain=organ)` — check if hypothesis pattern matches known failure scars
3. If code/pipeline involved: `forge_sandbox_run(test_suite=...)` — execute actual tests
4. `forge_evaluate(tool_name, description, ...)` — compute G score for strongest hypothesis

**Output:** Explorer Packet — falsification section populated

**Gate:** Every hypothesis must have at least one falsification test listed. Scar check mandatory before VERIFY.

---

### Stage 4: VERIFY

**Input:** Explorer Packet (falsification section)
**Process:**
1. Compute verification metrics:
   - G score (from forge_evaluate or manual A·P·E·X·Φ)
   - C_dark (dark counterpart — want < 0.30)
   - W3 tri-witness (human × AI × external)
2. `arif_judge(actor, intent, domain, reversibility_level, blast_radius)` with evidence package
3. Render verdict:
   - **SEAL** — evidence sufficient, proceed with confidence
   - **SABAR** — evidence partial, wait for more data
   - **HOLD** — evidence insufficient or conflicting, stop
   - **VOID** — evidence contradicts, abandon hypothesis
4. If SEAL: `arif_seal(mode=seal)` to VAULT999
5. If SABAR/HOLD: return to OBSERVE with explicit gap list

**Output:** Explorer Packet — verification section populated + verdict

**Gate:** Verdict requires all three witnesses (human, AI, external). DIVERGENT → HOLD.

---

## Explorer Packet Schema

```yaml
explorer_packet:
  id: "exp_<uuid>"
  stage: "observe|hypothesize|falsify|verify|seal|return"

  origin:
    actor_id: string
    session_id: string
    organ: string
    intent: string
    decision_context: string

  observation:
    evidence:
      - id: string
        class: "OBS|DER|INT|SPEC"
        source: string
        content: string
        confidence: 0.0-1.0
        provenance: string
        alternatives: [string]
    missing_evidence: [string]
    contradictions: [{evidence_a, evidence_b, nature}]

  hypotheses:
    - id: string
      statement: string
      priors: {domain_specific: float}
      combined_prior: float
      supporting_evidence: [string]
      missing_tests: [string]
      alternatives: [string]

  falsification:
    - hypothesis_id: string
      tests:
        - test: string
          result: "passed|failed|not_run|impossible"
          would_falsify: bool
          cost: "LOW|MEDIUM|HIGH"
    scar_findings: [string]

  verification:
    strongest_hypothesis: string
    g_score: float
    c_dark: float
    w3: {human, ai, external, consensus}
    verdict: "SEAL|SABAR|HOLD|VOID"
    verdict_reason: string
    next_action: string

  governance:
    session_id: string
    actor_id: string
    lease_id: string|null
    cc_id: string|null
    floors_checked: {f1..f11}
    arif_ack_required: bool
```

---

## Invocation (Hermes Entry Point)

```python
# Pseudocode — Hermes dispatcher logic

def dispatch(query: str) -> ExplorerPacket:
    # 1. Init governance session
    session = arif_init(mode="init", intent=query)

    # 2. Route to organ
    route = arif_route(intent=query, session_id=session.id)

    # 3. OBSERVE — call organ tool
    evidence = call_organ_tool(route.organ, route.suggested_tools, query)
    packet = ExplorerPacket(stage="observe", evidence=evidence)

    # 4. HYPOTHESIZE — reason over evidence
    reasoning = arif_think(mode="reason", query=f"Evidence: {evidence}")
    packet.hypotheses = extract_hypotheses(reasoning)
    packet.stage = "hypothesize"

    # 5. FALSIFY — check scars + run tests
    scars = forge_scar(mode="consult", domain=route.organ)
    packet.falsification = run_falsification_tests(packet.hypotheses, scars)
    packet.stage = "falsify"

    # 6. VERIFY — judge and verdict
    verdict = arif_judge(
        actor="hermes-prime",
        intent=query,
        domain=route.organ,
        evidence=packet.evidence,
        reversibility_level="PARTIAL",
        blast_radius="LOW"
    )
    packet.verification = verdict
    packet.stage = "verify"

    # 7. Return
    return packet
```

---

## What This Replaces

| Before | After |
|---|---|
| User asks → Hermes answers directly | User asks → OBSERVE → HYPOTHESIZE → FALSIFY → VERIFY → answer |
| Evidence optional | Evidence mandatory |
| Confidence vibes | Confidence computed with caps |
| No falsification | Every hypothesis has kill tests |
| No governance | arif_judge verdict required |
| Single answer | Ranked alternatives with uncertainty |

---

## What This Does NOT Do

- **Does NOT replace organ tools** — GEOX still does geology, WEALTH still does capital
- **Does NOT add new MCP servers** — uses existing arif_route, arif_think, forge_scar, arif_judge
- **Does NOT automate irreversible actions** — SEAL still needs F13 ack
- **Does NOT build the 555-ASI graph** — that's Phase 2 (Postgres schema)
- **Does NOT make agents smarter** — it makes their reasoning *governed*

---

## Phase 2 (Future)

- [ ] Postgres schema for knowledge graph edges
- [ ] Auto-dispatch on query (no manual invocation)
- [ ] Cross-session memory integration (L3 recall into OBSERVE)
- [ ] Multi-packet parallel exploration (fork hypotheses)
- [ ] Graph visualization (AAA cockpit)
- [ ] Explorer metrics dashboard (G score trends, falsification rate)

---

## Sovereign

Protocol ratified by ARIF (F13) on 2026-07-06.
Constitutional chain: pending seal.
