---
name: forge-phased-delivery
id: forge-phased-delivery
owner: A-FORGE
risk_tier: low
description: "Phased delivery protocol for building, testing, simulating, tuning, and integrating cognitive modules and intelligent systems."
version: 1.0.0
tags: [delivery, testing, simulation, honest-reporting, phased, F2, F4, F7]
floor_scope: [F1, F2, F4, F7, F11]
autonomy_tier: T1
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# FORGE-phased-delivery

## Purpose

When building cognitive modules, intelligent systems, or complex integrations, the
temptation is to "do everything at once" or report soft-pass before real validation.
This skill enforces a structured delivery pipeline with honest reporting at every gate.

## When to Load

- Building multiple modules that need integration
- Any task where "works in tests" does not equal "works in production"
- User asks to build something from a blueprint, paper, or spec
- Spawning coding agents for implementation work
- Recurring pattern of "implement X with tests"

## Core Principle

**Honest numbers outrank nice-looking PASS.**

A template report that says PASS is fabrication. A real simulation that says FAIL is
engineering. The sovereign deserves the truth.

## The 6-Phase Pipeline

### Phase 1: Research and Validation
- Verify references cited in any blueprint, paper, or spec
- Check if approaches are validated or theoretical
- Find simpler alternatives that achieve 80 percent of benefit
- Assess Python library availability and integration feasibility
- **Output:** Research brief with per-component verdicts (VALIDATED, PARTIALLY_VALIDATED, UNVALIDATED, REFUTATED)

### Phase 2: Build (Unit Level)
- Build modules sequentially, not in parallel, unless components are fully independent
- Write unit tests alongside, not after
- Every function that computes must emit receipts
- **Gate:** All unit tests pass before proceeding
- **Output:** Code plus unit tests plus README

### Phase 3: Simulation (Ground Truth)
- Generate synthetic data with KNOWN ground truth labels
- Test each module against its synthetic dataset
- Compute real metrics: precision, recall, F1, false alarm rate, tier transitions
- **Gate:** Simulation report with real numbers (never hardcoded)
- **Output:** SIMULATION_REPORT.md with per-component PASS or FAIL or PARTIAL

### Phase 4: Tuning (Fix What Fails)
- Read simulation report, identify specific failures with root cause
- Surgical fixes only. Do not rewrite entire modules
- Re-run unit tests after every fix (regression check)
- Re-run simulation to verify improvement
- **Gate:** All unit tests pass plus simulation metrics improved
- **Output:** TUNING_REPORT.md with before/after numbers

### Phase 5: Integration (Wire into Live)
- Build integration adapter (wrapper, not core modification)
- Add identity locks for critical data
- Wire zero-LLM-call paths for hot loops
- Smoke test the integration end-to-end with a realistic scenario
- **Gate:** Live smoke test passes plus all existing tests still green
- **Output:** Integration layer plus INTEGRATION_REPORT.md

### Phase 6: Archive and Defer
- Document what works, what is deferred, what is broken
- Archive to PHASEX_ARCHIVE.md
- Defer components that regressed or need deeper work
- State clear next-session priorities
- **Output:** Clean archive plus next-session roadmap

## Pitfalls (from live failures)

### 0. execute_code sandbox lacks matplotlib/plotly/reportlab/weasyprint

The Hermes `execute_code` tool runs in an isolated Python sandbox that does NOT
ship the heavy visualization stack. Calling `import matplotlib` from inside
`execute_code` always fails with `ModuleNotFoundError`.

**Correct path for any visual artifact (PNG chart, PDF brief, interactive HTML):**

1. Write the script with `write_file` to `/root/forge_work/<session>/render.py`
2. Run via `terminal(command="/root/litellm-venv/bin/python render.py")` —
   the litellm venv at `/root/litellm-venv/` has matplotlib, plotly, reportlab, kaleido
   installed and is the canonical render surface
3. If a dep is missing, install with `uv pip install --python /root/litellm-venv/bin/python <pkg>`
   (NEVER install into system Python — PEP 668 + Hermes runtime constraint)

`forge-pdf-delivery` documents this for the weasyprint case. Same pitfall, broader scope:
the rule is **any visual artifact must be authored as a file and run via terminal + venv,
never built inside execute_code.**

**Companion to pitfall #1** (template reports): both are about not cutting corners
on output fidelity. Pitfall #1 is about fake numbers; this one is about fake
tooling — pretending the sandbox has matplotlib and shipping `ModuleNotFoundError`
to the user instead of routing through the venv.

### 0b. VAULT999 bypass when arifOS :8088 kernel is down

Per carry-forward doctrine (Antigravity 2026-08-28 close), when arifOS kernel is
unreachable AND `P0-GATE-HOLLOW-JUDGE` is active, the `arif_seal` MCP lane returns
HOLD. For READ-ONLY intelligence forge outputs (datasets, charts, PDFs, MD
analyses), bypass with direct-write to:

```
/root/.local/share/arifos/forge_receipts/<session-slug>.json
```

Self-validating receipt shape:
- `objective`, `completed[]` with `evidence` paths
- `session_state_close` with artifact counts + constitutional_audit
- `note` field declaring bypass mode + F1 reversibility statement

The artifact must include a SHA256SUMS.txt so provenance is verifiable. If
arifOS comes back online later, the forge_receipts entry can be promoted into
the proper VAULT999 chain — but the read-only nature means F1 AMANAH holds
even without promotion.

**Do NOT bypass for any write that mutates federation state.** This is
intelligence-product bypass only. Mutations still need the constitutional
gate even if judge is hollow.

### 0c. Sovereign intelligence forge — tersurat × tersirat × quantum

When F13 SOVEREIGN asks for a deep-dive on a corporate release, quarterly
filing, or institutional pattern (e.g., PETRONAS 1HFY26 release), the expected
deliverable is a **three-layer analytical brief**, not a chat reply:

1. **TERSURAT** — direct numbers from the release, every figure sourced, no
   interpretation. Tables with YoY columns.
2. **TERSIRAT** — pattern recognition on what the release DOESN'T say. Body
   language. Sign-vs-signal gap. CEO language shift. Disclosed-but-buried.
3. **QUANTUM** — probabilistic reading: scenario cones with named collapse
   events, entanglement matrix for variables that look independent but aren't,
   watch-signal list (single observables that flip probabilities).

**Default artifact shape** (validated in 1HFY26 PETRONAS forge, 2026-08-29,
16-minute cycle):
- Dataset JSON in `data/` with full metadata + epistemic provenance
- 12-15 PNG charts in `charts/` (matplotlib) — trajectory, waterfall, peer
  contrast, entanglement matrix, scenario cone, stress dashboard
- 5 interactive Plotly HTML in `charts/interactive/`
- Full PDF brief via reportlab (17-page proven template — see below)
- `analysis.md` companion with all three layers explicit
- `SHA256SUMS.txt` for provenance
- `forge_receipts/` seal entry

**User preference (Arif, F13, validated 2026-08-29):**
- One confirm ("Ok confirm" or "go B dual yes") is sufficient scope decision
- Wants tersurat+tersirat+quantum by default — do NOT ask which to include
- Wants charts AND PDF AND interactive HTML by default — do not ship text-only
- Wants SHA256 + provenance hashes — they treat this as sovereign-grade output
- Wants F13 bias disclosure for any insider-touched subject (PETRONAS, MAS,
  PRT, etc.) — F7 HUMILITY must be explicit in MD + PDF
- Wants quantum layer by default — collapse event naming, probability cone,
  entanglement matrix

**Constitutional framing for every brief:**
- F2 TRUTH: every number cited
- F7 HUMILITY: insider bias acknowledged for any lineage/topic
- F9 ANTI-HANTU: pattern recognition only, no intent attribution
- F13 SOVEREIGN: intelligence product, not policy directive
- F1 AMANAH: reversible artifact (read-only intelligence output)

**Templates available** (after 2026-08-29 session):
  with cover page, key findings table, embedded charts, conclusions block

### 1. Template reports are fabrication
Never hardcode simulation results. A script that returns `{"status": "PASS"}` without
actually running the module is worse than no report at all. Always verify by reading
the actual output files.

**Caught in session:** Agent produced a script with commented-out imports and hardcoded
results. Sovereign caught it immediately: "dokumen tu bukan simulation sebenar."

### 2. API rebuild mid-tuning breaks everything
If a module's API gets rewritten (Phase 2 rebuild) while tests are being fixed for
Phase 1, both test suites break. The fix is to add compatibility shims that bridge
old API names to new implementations. Do not force either side to change.

**Caught in session:** Phase 2 causal tagger rebuild changed class names. Tests failed
because `CausalClaim` did not exist in new API. Fix was adding a shim in `__init__.py`.

### 3. "Wired" does not equal "Tested end-to-end"
Unit tests passing does not mean integration works. Always run a live smoke test that
exercises the full path: input, module, output, verify.

**Caught in session:** 114 unit tests passed, but smoke test `r["identity"]` crashed
because `DecayAwareResult` is not subscriptable like a dict.

### 4. Do not lower global params to fix local problems
If one memory type (REINFORCED) decays too fast, do not lower λ globally; that affects
all memory types. Instead, fix the specific mechanism (boost Ω on reinforcement events).

**Caught in session:** λ changed from 0.10 to 0.05 globally, but REINFORCED still failed.
Correct fix is to increase score-dependent inertia μ(Ω) on reinforcement events.

### 6. "Code is draft/unbuilt" claims need multi-root verification before delivery
Before declaring "no code exists" or "X is draft only" from a `find` or `ls`, verify across
ALL plausible roots in the federation estate. The arifOS federation has overlapping
directory trees where the SAME capability lives at different paths:

- `/root/.hermes/` — Hermes Agent **runtime** (config, skills, plugins, cron, memories)
- `/root/HERMES/` — Hermes Agent **source** (cognitive modules, integration layer)
- Six git roots: `/root/arifOS/`, `/root/A-FORGE/`, `/root/AAA/`, `/root/GEOX/`,
  `/root/WEALTH/`, `/root/WELL/`
- Three-way site split for `arif-fazil.com`: source repo → `/var/www/html/<app>/` →
  engine copy (see `deployment-claim-verification` pitfall #50)

A single-path probe (`ls /root/.hermes/cognitive/`) returns empty → false claim
"draft only" → sovereign corrects with actual 5,949 LOC at `/root/HERMES/cognitive/`.

**Detection recipe before any "exists / doesn't exist" claim:**

```bash
# 1. Search across all plausible roots, not just the guessed one
find /root -maxdepth 4 -name "<target>" 2>/dev/null
find /root -maxdepth 4 -path "*<substring>*" -type d 2>/dev/null

# 2. For source-vs-runtime roots specifically, check both .hermes and HERMES variants
ls -d /root/.hermes/*/ /root/HERMES/*/ 2>/dev/null

# 3. For git-tracked code, verify the actual git worktree, not a stale snapshot
git -C /root/<repo> rev-parse --show-toplevel
git -C /root/<repo> log --oneline -1
```

**Companion to pitfall #3** ("Wired ≠ Tested end-to-end"): pitfall #3 catches
false-positive "wired" claims; this catches false-NEGATIVE "doesn't exist" claims.
A probe that hits the wrong path produces a false negative — the most dangerous
kind of "verification" because it masquerades as evidence.

**Rule:** every "code is X" or "code is missing" claim in any phase report MUST be
backed by a multi-root probe in the same response. If `find` only hits one root,
state explicitly "checked only /root/X — alternate roots not probed" so the sovereign
knows the verification surface.

### 5. Semantic similarity is not causal syntax detection
Sentence-transformers (semantic embedding) are great for topic drift detection but
terrible for detecting causal language structure. Cues like "because" and "therefore"
are syntactic patterns, not semantic similarities.

**Caught in session:** Causal Tagger accuracy dropped 78 to 57 percent after switching
to sentence-transformers. Correct fix is a regex-only approach for causal cues.

### 7. Schema-field inconsistencies → fix the read-side adapter, not the writers
When historical records carry inconsistent field names for the same concept
(`session_id` vs `session` vs `agent_session`), DO NOT migrate the legacy writers
to a canonical field — there are too many writers, the migration breaks
provenance, and rewriting receipts mutates immutable artifacts.

The correct fix is at the READ side: a normalizer/adapter that resolves
canonical fields from any of the historical names in priority order.

```python
# WRONG — migrates writers, breaks provenance, mutates immutable artifacts
"session_id": record["session"]  # forces all writers to use session_id

# RIGHT — read-side adapter with ordered fallbacks
"session_id": (
    record.get("session_id")
    or record.get("agent_session")
    or record.get("session")
),
```

**Three reasons read-side wins:**

1. **Writers are usually out of scope** — they may be in archived crons,
   sealed receipts, external producers you don't control.
2. **Migrating immutable artifacts violates F1 AMANAH** — VAULT999 records are
   append-only; rewriting them changes the historical truth.
3. **The receiver cares about the canonical name** — legacy field names in
   upstream data don't change the downstream requirement.

**When to use this pattern:**

- VAULT999 / sealed records with mixed-version writers (v0, v1, v2 schemas)
- Legacy config files where field names drifted across deploys
- Cross-organ data ingestion where each organ uses its own naming
- API responses where consumers need a stable contract despite upstream drift

**Companion:** prefer the lowest blast-radius fix. Schema reconciliation at the
adapter layer is reversible (revert the adapter, originals unchanged). Schema
migration at the writer layer is irreversible (rewritten records can't be
restored). When in doubt, fix downstream.

## User Preference: Real Numbers

The sovereign (Arif) explicitly rejects inflated metrics:
- Reject "PASS" when simulation showed failures
- Reject "78.3% accuracy" without showing confusion matrix
- Reject projected results without running actual code
- Accept "NEEDS TUNING" with real numbers
- Accept "0/8 REINFORCED still failing, root cause λ too high for 25-turn gap"
- Accept honest before/after comparison

## User Preference: Phased Delivery Options

When asked to implement a large blueprint, always offer phased options:
1. Phase 1 only (highest impact, smallest scope)
2. Phase 1 plus 2 (medium scope, some risk)
3. All phases (large scope, high stub risk)
4. Custom (user picks specific components)

The sovereign almost always picks Phase 1 only. Do not recommend "All phases."

## Telemetry

```json
{
  "skill_name": "forge-phased-delivery",
  "phases_completed": "1-6",
  "tests_pass": 114,
  "simulation_verdict": "NEEDS_TUNING",
  "components_deferred": ["causal_tagger", "reinforced_memory"],
  "integration_smoke_pass": false
}
```
