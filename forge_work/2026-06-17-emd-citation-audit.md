# emd_citation_audit.md — F2 Truth Closing Chain
# Forged: 2026-06-17 by FORGE (000Ω) — Task #1 of routing doctrine table
# Purpose: Audit and label the empirical claims from the multi-source
# synthesis (CLI vs MCP + multi-agent orchestration). Per F2 TRUTH,
# claims without sources cannot enter canon as OBS or DER.
#
# DITEMPA BUKAN DIBERI — Verify, then canonize.

version: 1
schema: arifos.citation_audit/v1
owner: opencode-333-agi
last_updated: 2026-06-17

# ─────────────────────────────────────────────────────────────────────
# EPISTEMIC LADDER (per geox-epistemic-ladder)
# OBS     = directly observed, has source
# DER     = derived from OBS by rule
# INT     = interpreted, plausible but unverified
# SPEC    = speculation, hypothesis to test
# PLAUSIBLE = practitioner consensus, multiple credible sources
# ESTIMATE = bounded but unmeasured
# HYPOTHESIS = conceptual framing, not empirical claim
# ─────────────────────────────────────────────────────────────────────

# ════════════════════════════════════════════════════════════════════
# BLOCK A: CLI vs MCP synthesis (initial video + extension)
# ════════════════════════════════════════════════════════════════════

block_A_cli_vs_mcp:
  claim_id: CLI-MCP-001
  claim: "MCP adds non-trivial context overhead by injecting schemas per turn"
  evidence_status: PLAUSIBLE
  evidence_chain: [synthesis citing [1][2][3][4] without source URL]
  notes: |
    Plausible by construction — any JSON schema consumes tokens. But the
    exact magnitude (e.g. "4.5k tokens per call" for 30 tools × 150 tokens)
    is back-of-envelope, not measured.
  recommended_label: PLAUSIBLE (keep in canon, not OBS)
  confidence: 0.75

  claim_id: CLI-MCP-002
  claim: "CLI sessions show higher token efficiency on coding/debugging benchmarks"
  evidence_status: INT
  evidence_chain: [synthesis citing [5][6][2][7] without source URL]
  notes: |
    Practitioner folklore. Plausible, but no benchmark URL cited. Without
    the source, the "30%+ savings" figure is unverified.
  recommended_label: INT (mark as estimate, not claim)
  confidence: 0.55

  claim_id: CLI-MCP-003
  claim: "Recommended MCP tool counts per server are 5-12"
  evidence_status: PLAUSIBLE
  evidence_chain: [synthesis citing [8][9][10]]
  notes: |
    Multiple practitioner sources cite this range. Treat as PLAUSIBLE
    consensus, not measured optimal. Our A-FORGE has ~50 tools and
    GEOX has 37 — both exceed ceiling by 2-3x. This is an audit finding.
  recommended_label: PLAUSIBLE → target binding
  confidence: 0.80
  binding: tool_budget.target_per_server = 12 (in routing_policy.yaml)

  claim_id: CLI-MCP-004
  claim: "MCP sessions degrade as schema + history fill context window"
  evidence_status: INT
  evidence_chain: [synthesis citing [1][3]]
  notes: |
    Anthropic / Claude Code practitioner observation. Plausible — context
    windows are finite. But the claim lacks measurement of degradation curve.
  recommended_label: INT → SPEC (test via Task #5 session-bloat test)
  confidence: 0.50

  claim_id: CLI-MCP-005
  claim: "Multi-agent systems consume 4x-220x more tokens than single-agent"
  evidence_status: ESTIMATE
  evidence_chain: [synthesis citing [3][4]]
  notes: |
    This is a range estimate, not a measurement. The 220x figure
    almost certainly reflects naive forwarding, not typed-handoff design.
    The 4x figure reflects well-designed systems. We should target
    the lower bound, not the range.
  recommended_label: ESTIMATE (do not cite the 220x as fact)
  confidence: 0.40

# ════════════════════════════════════════════════════════════════════
# BLOCK B: Multi-agent orchestration patterns
# ════════════════════════════════════════════════════════════════════

block_B_multi_agent:
  claim_id: MAO-001
  claim: "Narrow spine topology (orchestrator, planner, executors, reviewer) is the convergence point"
  evidence_status: PLAUSIBLE
  evidence_chain: [multiple practitioner sources, no specific URL]
  notes: |
    Matches arifOS HEXAGON topology (333-AGI / 555-ASI / 888-APEX / A-AUDIT /
    A-ARCHIVE). Federation already implements this. No new finding.
  recommended_label: PLAUSIBLE (consensus, federation-aligned)
  confidence: 0.85

  claim_id: MAO-002
  claim: "Reviewer must be zero-trust, not passive mirror"
  evidence_status: PLAUSIBLE
  evidence_chain: [synthesis citing [2][4]]
  notes: |
    Strong principle. Federation's 888_JUDGE / 999_SEAL is exactly this.
    Reviewer receives evidence packet only, not full chain.
  recommended_label: PLAUSIBLE → binding
  confidence: 0.85
  binding: handoff_schema.deny_fields includes full_planner_chain

  claim_id: MAO-003
  claim: "Typed handoff objects shrink handoffs from thousands to hundreds of tokens"
  evidence_status: PLAUSIBLE
  evidence_chain: [synthesis citing [11]]
  notes: |
    Matches our handoff_schema design (max 500 tokens, 12 fields). No
    specific benchmark, but the principle is sound: typed > chat blob.
  recommended_label: PLAUSIBLE
  confidence: 0.75

  claim_id: MAO-004
  claim: "Reviewer received > X tokens of raw history = architecture broken"
  evidence_status: INT
  evidence_chain: [synthesis citing [1][2]]
  notes: |
    Useful heuristic alarm. Codify in observability.alerts.
  recommended_label: INT → SPEC (test in real federation traffic)
  confidence: 0.65
  binding: observability.alerts includes "reviewer received > X tokens of raw history"

# ════════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════════

summary:
  total_claims: 9
  by_status:
    PLAUSIBLE: 5
    INT: 3
    ESTIMATE: 1
  consensus_findings:
    - "CLI moves bits, MCP moves authority" (PLAUSIBLE motto)
    - "5-12 tools per MCP server" (PLAUSIBLE target)
    - "Typed handoffs > chat blobs" (PLAUSIBLE principle)
    - "Reviewer is zero-trust validator" (PLAUSIBLE principle)
    - "Narrow spine topology" (PLAUSIBLE, federation-aligned)
  contested_or_weak:
    - "30% token savings" — INT, no source
    - "4x-220x multi-agent cost" — ESTIMATE, range not measurement
    - "MCP degrades with schema accumulation" — INT, no curve measured
  next_actions:
    - "Task #5 (session-bloat test) — measure CLI vs MCP context growth over 50 steps"
    - "Task #4 (tool-budget audit) — partition A-FORGE ~50 tools into 4 domain-coherent sub-servers"
    - "VAULT999 seal awaits 888_HOLD (Task #6)"

# ─────────────────────────────────────────────────────────────────────
# DITEMPA BUKAN DIBERI — Verify before canonize.
# ─────────────────────────────────────────────────────────────────────
