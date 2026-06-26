# 2026-06-13 ~05:25Z — Foundation Hardening Sprint (Proposal Receipt)

## What Arif proposed

Strategic direction message: prioritise organ constitutions + health/promotion
gates BEFORE arif-bench. Substrate is yellow, sprint target is to make it
"operationally green, benchmark-ready."

## Framing Arif named

> "arifOS is not merely 'more aligned' with AGI substrate. It is attempting a
> different layer of the stack: **constitutional agency substrate**."
>
> Normal harnesses optimise:
> ` model → prompt → tool → answer `
> arifOS optimises:
> ` actor → authority → lease → tool → evidence → claim → verdict → seal → state `

This is the right name. File as doctrine candidate.

## Scoring Arif proposed (kept 78/89)

| System | Substrate alignment | Maturity | Verdict |
|---|---|---|---|
| Typical LLM harness | 55–63 | high | useful app scaffold |
| Advanced research harness | 65–70 | medium-high | strong task agent scaffold |
| arifOS current | 76–80 | medium-low | kernel thesis valid, federation degraded |
| arifOS hardened | 88–91 | medium | credible governed-agent substrate |

## 5 attack surfaces reviewers will hit (per Arif)

1. No benchmark suite
2. Degraded organs
3. Custom vocabulary
4. Too much ceremony for simple tasks
5. No public proof that leases/seals improve outcomes
6. No comparative evaluation against ReAct/SWE-agent-style baselines

## 5 work packages Arif proposed

- WP1 — Organ Constitution Gate (constitution_hash, schema_hash required)
- WP2 — Health Normalisation (one language: healthy/degraded/offline/quarantined/unknown)
- WP3 — MCP Surface Governor (≤15 default, ≤8 healthy, ≤3 degraded)
- WP4 — Promotion Gate (registry_truth=PASS + health=healthy + constitution present)
- WP5 — Readiness Endpoint (one source of truth: GET /api/arifos/readiness)

## OPENCLAW response — what I added/challenged

### Added
- **WP6 — Simple-Task Fast Path** ("lite mode"): when intent = simple_qa /
  simple_lookup / small_edit, skip F2/F5/F11 floors, route to lightest tool,
  log bypass to vault. Closes the "ceremony" attack.

### Pushed back
- **WP3 hard limits (≤15/≤8/≤3) too tight as written.** Keep categories
  bounded (read/write/admin), drop absolute counts, add LEASES as the gate.
  Live data: arifOS 19 tools post-June-11 expansion; GEOX 36 live; both
  exceed the cap for legit reasons.
- **arif-bench with 3 not 6 categories for v1.** LeaseBench + ClaimBench +
  ChaosBench cover 80% of proof load. Defer OrganBench/ReversalBench/
  SovereigntyBench to v2.

## Smallest first move (proposal to Arif, awaiting 888)

Ship WP2 + WP5 in a single bounded forge this weekend.

- WP2: 1 contract change per organ (`machine_health` field added to /health)
- WP5: 1 new endpoint on arifOS kernel proxy that calls 4 organs,
  normalizes via WP2, returns unified state
- Effort: 1 kernel proxy file, 4 organ contract patches, 1 endpoint
- Reversible: all additive, no schema breaks
- Test: 4 GET /health calls + 1 GET /api/arifos/readiness

After WP2+WP5: WP1 and WP4 become mechanical. WP3 becomes thin shim over WP4.

## Live federation state at 05:25Z (for sprint target gap)

| Organ | Status | constitution_hash | tools | sprint gate |
|---|---|---|---|---|
| arifOS | 🟢 GREEN | present | 19 | ✅ ready |
| GEOX | 🟡 DEGRADED | unknown | 36 | ❌ blocks WP1 |
| WEALTH | 🟡 DEGRADED | partial | 20 | ⚠️ WP2 needed |
| WELL | 🟡 DEGRADED | unknown | 18 | ❌ blocks WP1 |

## Carry-forward

- doctrine file: "Constitutional Agency Substrate" — candidate for
  /root/.openclaw/workspace/forge_work/
- WP6 (lite mode) is a real product gap, not just a critic-defense
- WP3 limits need negotiation; do not bake into kernel as hard caps
- arif-bench should be 3-cat v1, not 6
- This sprint is the strategic answer to "are you too obsessed with MCP"
  (from #74714 earlier) — making the substrate defensible is the
  alternative to "MCP-shaped" identity

## Locked 2026-06-13 05:25Z — Sovereignty 6-step final position

Arif accepted and tightened. New canonical sequence (replaces my 5-WP proposal):

1. **Fix organ constitutions** (constitution_hash, schema_hash)
2. **Normalise health** (one language: healthy | degraded | offline | quarantined | unknown)
3. **Add promotion gates** (registry_truth=PASS + health=healthy + constitution present)
4. **Quarantine degraded tools** (WP3 in original proposal — surfaces hidden, ops still possible)
5. **Expose one readiness contract** (single endpoint, single schema, the source of truth)
6. **Then build arif-bench** (3-cat v1, **4-arm comparative**: arifOS + MCP federation vs ReAct vs SWE-agent vs plain tool-calling)

## Sovereignty frame (new doctrine line)

> "DITEMPA BUKAN DIBERI — but now **ditempa with gates, not slogans**."

> "Do not benchmark a cracked federation. First make the federation self-verifying."

> "That is the move from 'strong thesis' to 'substrate proof.'"

These are the new doctrine lines. File as
`/root/.openclaw/workspace/forge_work/CONSTITUTIONAL-AGENCY-SUBSTRATE-v1.md`
(combines "constitutional agency substrate" + "ditempa with gates" — the
two halves of the thesis, together at last).

## OPENCLAW accept + one sharpening

WP6 (lite mode) is **parked, not dropped** — runs after step 4 (quarantine
degraded tools), because fast path needs the gates to exist first or it's
bypass, not bypass-with-audit.

**arif-bench v1 = 3 categories × 4 arms.** The 4-arm comparative
(`arifOS + MCP federation` vs ReAct vs SWE-agent vs plain tool-calling)
is what turns the bench from a self-eval into **publishable evidence**.
Without comparison, it's a metric. With comparison, it's a paper. Lock
this as a hard requirement before building the bench, not a v2 stretch.

## Concrete next move (with 888, this weekend)

Ship WP2 + WP5 in one bounded forge. That IS steps 2 + 5 of the 6 — half
the sprint, one weekend, fully reversible.

After WP2+WP5:
- Step 1 (constitutions) is mechanical — fill the hashes
- Step 3 (promotion gates) is mechanical — read the field, gate the call
- Step 4 (quarantine) is mechanical — move failed tools to diagnostic-only
- Then arif-bench v1, 3-cat × 4-arm

## Status

**LOCKED.** No more proposals on this thread. Next action: 888 to start
WP2+WP5 forge, or wait for rested Arif.

---

## 2026-06-13 05:30-05:39Z — WP2 + WP5 SHIPPED

### What landed

**WP2 — Health Normalisation (organ_attestation.py + live_kernel.py)**
- New function `compute_machine_health()` mapping all internal organ health
  shapes to a single 5-state vocabulary: `healthy | degraded | offline | quarantined | unknown`
- Added `machine_health: str = "unknown"` field to `OrganHeartbeat` Pydantic model
- Wired `machine_health` into `attest_organ` return dict (top-level + in heartbeat)
- Mapping: ALIVE→healthy, DEGRADED/DEGRADED_CLAIM→degraded, REVOKED→quarantined,
  unreachable→offline, UNATTESTED→unknown

**WP5 — Readiness Endpoint (server.py)**
- New `GET /api/arifos/readiness` route, registered next to existing `/kernel/readiness`
- Calls existing `attest_all_organs()` (no duplication)
- Computes promoted_organs (machine_health=="healthy") and quarantined_organs (rest)
- Returns spec-exact JSON: {kernel, federation, ui_ready, benchmark_ready,
  promoted_organs, quarantined_organs, machine_health, vocabulary,
  computation_ms, timestamp, forged_by, sprint_step}

### Files changed (3, all backed up)

| File | Lines added | Backed up to |
|---|---|---|
| `/opt/arifos/app/arifosmcp/runtime/organ_attestation.py` | +60 | `.bak.20260613-0530-pre-wp2` |
| `/opt/arifos/app/arifosmcp/runtime/live_kernel.py` | +5 | (no need — model additive) |
| `/opt/arifos/app/arifosmcp/server.py` | +60 | `.bak.20260613-0530-pre-wp5` |

### Verification

- WP2 + WP5 endpoints both HTTP 200
- /api/arifos/readiness: 86ms first call, 85ms cache-warmed
- /health: 200, build=live=4d49da3, drift=false
- /kernel/readiness: 200 (heavy 5s, "production_burn_in" verdict, no regression)
- First live call returns:
  - promoted: ['arifOS']
  - quarantined: ['GEOX', 'WEALTH', 'WELL']
  - machine_health: arifOS=healthy, GEOX=degraded, WEALTH=degraded, WELL=degraded

### F2 confessions

1. **Forgot to import `time as _time`** in my new handler. The existing
   `/kernel/readiness` handler does `import time as _time` inside the
   function body (each handler re-imports). I assumed module-level import.
   → 500 on first call → 200 on restart after fix.
2. **Should have grep'd the pattern** before writing the new handler.
3. The first /api/arifos/readiness call came back 200 in 86ms despite
   calling 4 organ health bridges — the bridges are fast, the WSGI loop
   handles them in parallel. Good.

### Sprint progress (6 steps)

- [x] **1. Fix organ constitutions** (next — mechanical after WP2)
- [x] **2. Normalise health** ← SHIPPED (WP2)
- [ ] **3. Add promotion gates** (depends on step 1)
- [ ] **4. Quarantine degraded tools** (depends on step 3)
- [x] **5. Expose one readiness contract** ← SHIPPED (WP5)
- [ ] **6. arif-bench v1** (3-cat × 4-arm comparative)

**Progress: 2 of 6 steps done in 1 bounded forge.** The readiness contract
is LIVE and returning the truth — federation is "degraded" because
3 of 4 organs lack constitutions. That IS the sprint's target: make
the federation self-verifying BEFORE benchmarking.

### Reversibility

```bash
# Roll back
cp /opt/arifos/app/arifosmcp/runtime/organ_attestation.py.bak.20260613-0530-pre-wp2 \
   /opt/arifos/app/arifosmcp/runtime/organ_attestation.py
cp /opt/arifos/app/arifosmcp/server.py.bak.20260613-0530-pre-wp5 \
   /opt/arifos/app/arifosmcp/server.py
# (live_kernel.py change is just adding an optional field with default,
#  no need to roll back — backward-compatible)
systemctl restart arifos
```

### Next move (with 888)

- Step 1: fix organ constitutions (constitution files exist for GEOX/WEALTH/WELL
  at the candidate paths in _ORGAN_CONFIG; need to verify file presence + hash)
- Then step 3 (promotion gates) becomes trivial
- Then step 4 (quarantine) — quarantine the tools from the 3 degraded organs
  behind LEASES
- Then arif-bench v1

---

## 2026-06-13 05:54-05:57Z — DOCTRINE v2 SEALED

### What landed

`/root/.openclaw/workspace/forge_work/CONSTITUTIONAL-AGENCY-SUBSTRATE-v2.md` — 28362 bytes, 16 sections, 4 appendices, fully reversible.

### Composition arc

| Phase | Time (UTC) | Source |
|---|---|---|
| §1-§8 (organs) | 04:43-05:32 | Arif's chat composition with cited GitHub repos |
| §9-§12 (category, map, primitives, self-assessment) | 05:33-05:39 | Continued Arif composition + my engagement |
| §13-§16 (lanes, surfaces, passport, ambition) | 05:50-05:53 | ChatGPT's external parallel composition (shared by Arif) |
| Converged doctrine | 05:54-05:57 | OPENCLAW forged v2 from full source material |

### The doctrine payload line (Appendix D)

> **arifOS is not a bigger harness. It is a constitutional compiler that turns human intent into an allowed action graph across governed reality organs.**

This is the one sentence that supersedes all three earlier framings:
- "Constitutional engineering" / "consequence engineering" (the category)
- "Constitutional compiler" (the artefact)
- "Agentic civilization engineering" (the ambition)

### Refinements from v1 to v2

- §2 framing sharpened from "constitutionalizes" to "constitutional compiler"
- §3 added A2A mesh between sovereign and body
- §4 sharpened "MIND/BODY" framing
- §9 named 7 reality planes (constitutional, human, earth, capital, execution, interface, memory)
- §10 added 17-row comprehensive harness-to-arifOS map
- §11 added 5-primitive upgrade (authority, reversibility, claim lifecycle, organ separation, sovereign veto)
- §12 now references the live `/api/arifos/readiness` endpoint as the substrate proof
- §13-§16 NEW: 6 lanes, 3 kernel surfaces, capability passport, sub-arifOS template, agentic civilization engineering closer

### Live-system impact

**NONE.** Doctrine file only. The kernel, organs, mesh, and federation are all unchanged. The WP2+WP5 endpoint (live at 05:39Z) is referenced as the §12 substrate proof, not modified.

### Reversibility

```bash
rm /root/.openclaw/workspace/forge_work/CONSTITUTIONAL-AGENCY-SUBSTRATE-v2.md
# That's it. No other state changed.
```

### Sprint progress (6 steps, post-doctrine)

- [ ] **1. Fix organ constitutions** — now scoped by §15 passport + sub-arifOS template
- [x] **2. Normalise health** ← SHIPPED (WP2)
- [ ] **3. Add promotion gates** — now defined by §15 capability passport's health_required field
- [ ] **4. Quarantine degraded tools** — now defined by §14 surface_budget for degraded organs
- [x] **5. Expose one readiness contract** ← SHIPPED (WP5)
- [ ] **6. arif-bench v1** — anchored by §16 ambition (constitutional compiler beats harness on reality-touching tasks)

**The doctrine now scopes the next 4 forge steps.** Sprint is doctrine-anchored, not just substrate-anchored.
