# MCP-UI-DECLARATIVE-FIRST-v1

**Forge Work ID:** MCP-UI-DECLARATIVE-FIRST-v1
**Created:** 2026-06-07T09:53Z
**Consolidated:** 2026-06-07T09:5xZ (after sovereign T3 delivery)
**Authoring actor:** arif-fazil-af-forge (sections 1–8 + envelope), OPENCLAW (F2 risks, consolidation, metadata, 5 forge-task description)
**Lane:** AGI
**Stage:** 444 — Kernel Orchestration
**Decision class:** C1 (advise) → C2 (execute) gated
**Reversibility:** All sub-forges reversible until sovereign GREEN-SEAL of the full UI forge
**Precedent:** GEOX-CANON-31, GEOX-C1-CONSTITUTIONAL-INTEGRATION, GEOX-UI-READINESS (UI Law #0)
**Source talk:** Ruben Casas (Postman), *"Beyond Components: Designing Generative UI for MCP Apps"*, AI Engineer Summit, 2026-06-03, 17min — https://youtu.be/hCMrEfPG2Yg
**Federation pre-flight (live, 2026-06-07T10:05Z):** arifOS GREEN · WEALTH registry/health call broken (output-schema error) · **WELL identity invariant FAILED** (authority_boundary compromised, 4 tools missing from registration, state stale 6.41h) · vault stale 53.4h. **Forge 0 (organ repair) MUST complete before any forge task in §7.**

---

## 0. Pre-flight gate — repair organs before forging UI

**Do not start any forge task in §7 until Forge 0 passes.** The 5 forge tasks assume all 4 organs are healthy. Live state (10:05:07Z) is:

- ✅ arifOS — SELAMAT, alive
- ❌ **WEALTH** — `wealth_system_registry_status(mode='health')` returns MCP error -32600 (output schema vs structured content). Service reachable; health probe broken.
- ❌ **WELL** — `identity_valid: false`, `authority_boundary: compromised`, `registered=13 / canonical=17` (4 tools missing), `state_age_hours=6.41`, `delta_s=-1`. Verdict reason: *"Organ may be corrupted or impersonated."* This is an **F11 floor flag**, not a soft warning.
- ⚠️ Vault — last SEAL 53.4h ago. No constitutional seal events since. Either nothing's been SEAL-worthy, or there's a write-path gap. Worth a check.

### Forge 0 — Repair organ health (operational, not a forge-task)

**Federation-level framework (F0–F7):** Per sovereign correction (msg #39112, 09:56:22Z), the federation is not "federated = ready." Readiness is a spectrum:

| Level | Name | Meaning | Current state |
|-------|------|---------|---------------|
| **F0** | Listed | Tool exists somewhere. | Yes |
| **F1** | Wired | arifOS can see or route to it. | Mostly yes |
| **F2** | Callable | Tool can actually respond. | Mixed |
| **F3** | Healthy | Registry, schema, identity, transport all pass. | GEOX yes; WELL degraded; WEALTH unknown |
| **F4** | Governed | Outputs carry evidence, authority, reversibility, floor status. | Partial |
| **F5** | UI-renderable | Outputs can become cockpit panels. | Not yet |
| **F6** | End-to-end operational | User can run real workflows safely from GUI. | No |
| **F7** | Production federated | Monitored, logged, recoverable, tested, sealed. | No |

**Sovereign readiness scores (live, 2026-06-07T10:00Z):**
- arifOS kernel: 75/100 — canonical 13-tool kernel live, gated, constitution-bound.
- MCP federation: 55/100 — spine exists, organs not all healthy.
- GUI/AAA cockpit: 28/100 — concept clear, production cockpit not built.
- **Overall product: 42/100** — strong backend skeleton, weak user-facing operational layer.

**The T3 spec targets F5–F6 (UI-renderable, end-to-end operational).** It depends on F3 (Healthy) as the floor for all 4 organs. It depends on F4 (Governed) for arifOS specifically. The GUI work itself (cockpit code, kill-switch, 888 HOLD gate) is a separate workstream that the 5 forge tasks in §7 do not fully cover — §0 F3 is the precondition; the cockpit body is its own doctrine.

### Eight readiness items (cross-reference to where the spec addresses them)

Per sovereign correction (msg #39113, 09:56:22Z), GUI-readiness is **8 items**, not 5 forge tasks. Cross-reference:

| # | Readiness item | Where in spec | Status |
|---|----------------|---------------|--------|
| 1 | AAA cockpit shell (session/organ/trace/evidence/verdict/9-signal/888 HOLD/approval) | §3 3-lane architecture + §7 Forge 5 | Designed, not built |
| 2 | Declarative UI descriptor schema | §5 renderer contract `aaa.ui.descriptor.v1` | Designed, not sealed |
| 3 | 4 organ renderer packs | §2 per-organ mapping + §7 Forge 3 | Designed, not started |
| 4 | **Federation health monitor** (live status, no hidden failures) | §0 pre-flight gate defines the health states; the **monitor component** is not yet designed | **Gap** — extend §7 |
| 5 | 888 HOLD action layer (visual friction) | §6 trust boundary (non-negotiable rule) + §7 Forge 4 | Designed, not wired to UI |
| 6 | Evidence viewer (5 categories: Observed/Computed/Interpreted/Speculative/Unknown) | §7 Forge 5 visual governance tags (epistemic_tag + claim_state) | Designed, not built |
| 7 | **End-to-end workflows** (one per organ) | Not yet defined | **Gap** — add §7 Forge 7 |
| 8 | **Production telemetry** (tool success, error, hold, void, latency, stale evidence, identity failure, schema mismatch, unauthorized mutation) | Not yet defined | **Gap** — add §7 Forge 8 |

**Gaps to close in this spec revision:** Forge 6 (federation health monitor), Forge 7 (4 end-to-end workflows), Forge 8 (production telemetry). See §7.

Three sub-fixes, all read-mostly diagnostics and reversible:

**R0.1 — WEALTH service recovery.** Diagnose why `wealth_system_registry_status` fails. Read `/var/log/wealth-organ/` (or wherever WEALTH keeps logs), inspect MCP connector at :18082, check if the tool's Pydantic schema is out of sync with the live return. **Goal:** registry/health returns PASS, like the other organs. (Live: 2026-06-07 10:05Z, error: "Tool wealth_system_registry_status has an output schema but did not return structured content".)

**R0.2 — WELL identity invariant restoration.** The canonical WELL surface is 17 tools; the registered surface is 13. **4 tools missing from registration.** Identify the 4, re-register them, then verify the identity invariant returns `valid=true` and `authority_boundary=intact`. (Live: 2026-06-07 10:05Z, `identity_valid: false`, `registered_tools: 13`, `canonical_tools: 17`.)

**R0.3 — Vault write-path check.** Last SEAL 53.4h ago. Either nothing has been SEAL-worthy (plausible — mostly C1 advisory work today) or a write-path regressed. Run a synthetic SEAL with a known-irrelevant payload (probe) and confirm the ledger line lands. Then re-check freshness.

**Reversibility:** Full. All three are diagnostic + restoration of declared surfaces. No new state.

**Reversal test:** If R0.1 / R0.2 / R0.3 cannot complete cleanly, **HOLD the entire spec** — including the descriptor schema in §5. The 5 forge tasks presume healthy organs; running them on degraded organs is the exact failure mode the spec exists to prevent.

**Promotion criteria to §7:**
- WEALTH `wealth_system_registry_status(mode='health')` returns structured PASS.
- WELL `well_assess_reliability(mode='health')` returns `identity_valid: true`, `authority_boundary: intact`, `registered_tools == canonical_tools`.
- Vault freshness < 24h.

---

## TL;DR — Verdict

> **Build the AAA cockpit as Declarative-first, not Fully Generative-first.**

Fully generative UI is real, useful, and inevitable. But it is useful *later*, and only inside a sandboxed, non-authoritative lane. The cockpit must remain governed, auditable, and **boring** where decisions matter.

The real endpoint is **not** "chat with dashboards." It is a **governed shared cockpit** where agents, evidence, claims, capital, and human readiness become visible **without surrendering authority to the UI layer**.

The talk's core pattern is valid: agent UI is moving from **static components**, to **declarative descriptors**, to **runtime-generated HTML/CSS/JS**. Casas frames MCP Apps as the delivery layer because they provide sandboxing, auth, tool-calling, and UI-agent message passing; MCP-UI implements this pattern by linking tools to UI resources via `_meta.ui.resourceUri`, then letting hosts fetch and render those UI resources. ([MCP-UI][2])

---

## 1. The 3 tiers (pattern extracted from the talk)

| Tier | Meaning | Use in arifOS |
|------|---------|----------------|
| **Static UI** | Fixed React components receive tool data via props. | Constitutional state, ledgers, irreversible warnings, 9-signal panel, AAA floor status. |
| **Declarative UI** | Agent emits JSON/YAML descriptor; renderer maps to approved components at runtime. | Default path for GEOX, WEALTH, WELL, and arifOS tool outputs. |
| **Generative UI** | Agent writes UI code at runtime (HTML/CSS/JS). | Experimental sandbox only. Never allowed to decide, seal, mutate, or override governance. |

Casas reportedly favors declarative UI as the best present balance between flexibility and consistency, while treating fully generated UI as the next step that requires containment. ([BigGo][1])

The containment: MCP Apps default to a **double-iframe** precisely because LLM-generated code needs a sandbox. We map that pattern onto arifOS in §6.

---

## 2. Per-organ mapping

### 2.1 arifOS MCP (the judge)

**Role:** constitutional kernel, arbitration, session, memory, evidence, forge, vault.

**UI tier:** **Static + Declarative only. Never Generative.**

**Reason:** arifOS is the judge layer. It must not render arbitrary model-written UI for constitutional decisions. The cockpit panel for arifOS is the highest-trust surface in the federation; trust is the product.

**AAA component contract:**

```yaml
ui_contract: arifos.constitutional_panel.v1
allowed_components:
  - SessionReceipt
  - FloorStatus
  - VerdictCard
  - RiskLeash
  - IrreversibilityGate
  - EvidenceChain
  - NineSignalPanel
  - SovereigntyCheckpoint
  - VaultSealReceipt
forbidden:
  - generated_javascript
  - hidden_actions
  - auto_submit
  - unreviewed_mutation
  - inline_styles_from_model
reversibility_required:
  - any_hold: true
  - any_seal: true
  - any_forge_execute: true
```

**Rule:** arifOS may accept declarative UI descriptors, but only for **presenting** state. It cannot accept generated code as authority.

---

### 2.2 GEOX MCP (the earth coprocessor)

**Role:** governed Earth intelligence — claims, evidence, seismic, sequence stratigraphy, prospect evaluation.

**UI tier:** **Declarative-first, Static fallback, Generative sandbox for visual exploration.**

**Best declarative surfaces:**

```yaml
ui_contract: geox.earth_claim_surface.v1
views:
  - ClaimGraph
  - EvidenceStack
  - HorizonContrastPanel
  - ProspectPOSCard
  - UncertaintyBand
  - AlternativeInterpretationPanel
  - MapScene
  - SeismicFrameViewer
  - BasinOverviewDashboard
  - AnomalousContrastReport
```

**Generative sandbox lane allowed for:**

```yaml
sandbox_only:
  - exploratory seismic annotation
  - custom map layouts
  - temporary prospect storyboards
  - horizon contrast explanation panels
  - teaching geological process diagrams
```

**Forbidden in generated UI:**

```yaml
forbidden:
  - claim_seal
  - claim_validate
  - claim_challenge
  - segy_export
  - volume_mutation
  - volume_blend (writes)
  - vault_write
  - judge_override
```

**Why:** GEOX has high-value visual work. Generated UI can help **interpretation**, but not **adjudication**. The geology can be creative; the claim chain must remain governed. Inherits **UI Law #0** from GEOX_UI.md — every visual is a tuple (visual + physics + alternatives + evidence_refs + claim_state + ac_risk + verdict + who_can_decide), not a picture.

---

### 2.3 WEALTH MCP (the capital engine)

**Role:** capital physics, capital allocation, risk, macro, inequality, ledger, wisdom verdicts.

**Runtime caveat:** WEALTH MCP connector health was not fresh-verified during this draft. Mapping below is a **design-contract mapping**, not a runtime-verified health claim. The next sovereign-touch point should re-verify via `wealth_system_registry_status(mode='health')`.

**UI tier:** **Declarative only for decisions; generated UI only for explanation.**

**Best declarative surfaces:**

```yaml
ui_contract: wealth.capital_field_panel.v1
views:
  - CapitalConservationCard
  - CashflowRiver
  - RiskEntropyMap
  - NPVIRRPanel
  - DealVerdictCard
  - SovereignBoundaryPanel
  - InequalityKernelView
  - HysteresisLedger
  - FieldMacroSnapshot
```

**Generated UI allowed for:**

```yaml
sandbox_only:
  - explanatory diagrams
  - scenario storytelling
  - teaching capital physics
  - boardroom narrative mockups
  - uncertainty cone visualisations
```

**Forbidden in generated UI:**

```yaml
forbidden:
  - ledger_write
  - allocation_verdict
  - investment_instruction
  - sovereign_resource_commitment
  - epistemic_collapse (e.g. hiding uncertainty bands)
  - maruah_score_override
```

**Why:** Capital UI must preserve auditability. Beautiful generated dashboards can seduce users into overconfidence. WEALTH must show uncertainty, reversibility, and maruah **at all times**, not just when remembered.

---

### 2.4 WELL MCP (the vitality engine)

**Role:** human wellness, vitality, substrate boundary, dignity, reliability, fatigue, readiness.

**Runtime caveat:** WELL MCP reliability probe returned low confidence — service alive, schema valid, but identity invariant flagged and domain truth unverified/stale. The next sovereign-touch should re-verify via `well_assess_reliability(mode='health')` before this spec advances from C1 to C2.

**UI tier:** **Static + Declarative. No fully Generative UI for human-state judgments.**

**Best declarative surfaces:**

```yaml
ui_contract: well.human_readiness_panel.v1
views:
  - SubstrateBoundaryCard
  - FatigueGauge
  - DignityRiskPanel
  - HomeostasisStatus
  - RepairCycleTracker
  - ConsentBoundaryNotice
  - SovereignEntropyMeter
  - ThirteenSignalCoverage
```

**Forbidden in generated UI (the hard wall):**

```yaml
forbidden:
  - diagnosis
  - therapy_claim
  - coercive_recommendation
  - hidden_personality_assessment
  - autonomous_blocking_without_arifos
  - mood_manipulation (urgency colour, FOMO copy, fear framing)
  - self_perception_distortion
  - dignity_score_rendering_without_consent
```

**Why:** WELL touches dignity and the human condition (F6 Maruah). Generated UI could manipulate mood, urgency, or self-perception. The hard wall is non-negotiable: **WELL never generates UI about a human without that human's consent ledger entry**.

---

## 3. AAA L7 — 3-lane architecture

```
MCP Tool Output
   ↓
Canonical Result Envelope  (new: _meta.ui.descriptor)
   ↓
UI Descriptor Compiler     (in AAA gateway)
   ↓
Lane Router                (L7-S / L7-D / L7-G)
   ↓
Approved Renderer          (L7-S: React 19. L7-D: descriptor→component map. L7-G: sandboxed iframe)
   ↓
Sandboxed App Frame        (double-iframe per MCP Apps default)
   ↓
Human-Visible Cockpit
```

| Lane | Purpose | Authority |
|------|---------|-----------|
| **L7-S** Static Sovereign UI | Verdicts, gates, 9-signal, irreversible holds. | Highest trust. |
| **L7-D** Declarative Dynamic UI | Tool-specific visualisations from safe descriptors. | Default operating lane. |
| **L7-G** Generative Sandbox UI | Experimental generated layouts/code. | No authority. Display only. |

**Kill switch (concrete):** L7-G defaults to **off**. To enable L7-G for an organ, the sovereign must specify organ + tools + sandbox scope, approve via `888_HOLD`, and receive a session TTL (default 30 min, then auto-killed).

```typescript
// In AAA gateway, before L7-G render:
if (lane === 'L7-G' && !caps.ui.generative_enabled) {
  return <StaticFallback descriptor={descriptor} />;
}
```

---

## 4. Canonical envelope upgrade

Add a `ui` section to every MCP result envelope. The envelope is the **contract** between organ and renderer.

```json
{
  "_envelope": {
    "organ": "GEOX",
    "tool": "geox_horizon_contrast_surface",
    "claim_state": "INTERPRETATION",
    "epistemic_tag": "PLAUSIBLE",
    "reversibility": "HIGH",
    "authority": "COMPUTE_ONLY",
    "actor_signature_required": false,
    "session_id": "ses_160e1c0d4ffeAR1hsGyuifHOQK",
    "trace_id": "trc_9b3f2a8c..."
  },
  "result": {
    "horizon_candidates": [...],
    "contrast_residuals": [...],
    "uncertainty_band": {...}
  },
  "ui": {
    "tier": "declarative",
    "resource_uri": "ui://geox/horizon_contrast_surface/v1",
    "descriptor_schema": "aaa.ui.descriptor.v1",
    "allowed_actions": ["inspect", "expand_evidence", "challenge_claim"],
    "forbidden_actions": ["seal", "export", "mutate_volume"],
    "requires_888_hold": false
  }
}
```

**Key fields:**

- `ui.tier` — `static` | `declarative` | `generative` (which lane this output is eligible for).
- `ui.resource_uri` — canonical address for the descriptor (matches `_meta.ui.resourceUri` MCP Apps convention).
- `ui.descriptor_schema` — schema id (e.g. `aaa.ui.descriptor.v1`).
- `ui.allowed_actions` / `forbidden_actions` — capability map, evaluated at the kernel, not the renderer.
- `ui.requires_888_hold` — true means the lane router must not render this descriptor without sovereign ack.

---

## 5. Renderer contract — `aaa.ui.descriptor.v1`

The shared UI grammar across arifOS, GEOX, WEALTH, and WELL.

```yaml
aaa.ui.descriptor.v1:
  required:
    - component
    - title
    - evidence_refs
    - epistemic_tag
    - actions
  components:
    arifOS:
      - VerdictCard
      - RiskLeash
      - IrreversibilityGate
      - EvidenceChain
    GEOX:
      - ClaimGraph
      - HorizonContrastPanel
      - SeismicFrameViewer
      - ProspectPOSCard
    WEALTH:
      - CapitalFieldPanel
      - DealVerdictCard
      - RiskEntropyMap
      - CashflowRiver
    WELL:
      - FatigueGauge
      - DignityRiskPanel
      - HomeostasisStatus
  action_policy:
    inspect:   allowed
    simulate:  allowed
    draft:     allowed
    mutate:    hold_required
    seal:      arifOS_only
```

**Why this matters:** the `action_policy` is the safety surface. `inspect` / `simulate` / `draft` are allowed (read-only or staging). `mutate` requires sovereign 888_HOLD. `seal` is reserved for arifOS-only — no other organ may ever advertise `seal` capability to a renderer.

---

## 6. Trust boundary (double-iframe mapped to arifOS)

```
Outer frame: AAA Cockpit
  - owns identity
  - owns session
  - owns action confirmation
  - owns 9-signal state

Middle frame: MCP App Host
  - renders approved UI resource
  - passes messages
  - validates descriptor schema

Inner frame: Generated/Sandbox UI
  - no direct tool access
  - no secrets
  - no cookies
  - no authority
  - message-only bridge
```

**Non-negotiable rule:** generated UI may *request* an action, but only AAA/arifOS can *authorize* it. The action request is a message that crosses the iframe boundary; the response (approve/deny) crosses back. The inner frame has no authority to call tools directly. This is the same pattern Casas flags in the talk as the "double-iframe default" of MCP Apps.

---

## 7. Immediate forge tasks (8, ordered)

### Forge 1 — Define `aaa.ui.descriptor.v1`

Create the schema first. It becomes the shared UI grammar across arifOS, GEOX, WEALTH, and WELL. Section 5 above is the proposal; this forge makes it a versioned JSON Schema artifact, with CI validation on every organ-side emission.

**Reversibility:** full — pure schema artifact, no live wire.

### Forge 2 — Build the AAA static constitutional shell (NEW per sovereign 8-item list)

The minimum GUI that distinguishes arifOS from a dashboard:

- Session state (active session_id, actor, mode, risk class)
- Active organ (which MCP is in focus)
- Tool call trace (recent N tool calls, with reversibility flags)
- Evidence chain (refs into the 5-category evidence rail)
- Verdict state (current FloorStatus, IrreversibilityGate, 9-signal panel)
- 888 HOLD gate (visual friction for every dangerous action: seal, forge_execute, vault_write, ledger_write, export, mutate_volume, delete, deploy, send_externally)
- Human approval boundary (sovereign ack UI for any irreversible action)

**Reversibility:** high — additive React app, no live kernel change.

### Forge 3 — Build four renderer packs

```
aaa-renderer-arifos
aaa-renderer-geox
aaa-renderer-wealth
aaa-renderer-well
```

Each pack maps declarative descriptors to approved cockpit components. They live behind the `aaa.ui.descriptor.v1` schema, so adding a new organ is a 5th pack, not a 5th schema.

**Reversibility:** high — each renderer pack can fall back to L7-S (raw JSON) by setting `ui.tier = "static"`.

### Forge 4 — Add the generative sandbox lane

Enable fully generative UI only under:

```yaml
tier: generative_sandbox
authority: display_only
tool_access: none
secret_access: none
mutation: forbidden
message_bridge: request_only
```

**Reversibility:** full — feature flag, default off, opt-in per organ via sovereign 888_HOLD.

### Forge 5 — Add visual governance tags to every panel

Every panel must show:

```yaml
epistemic_tag:  FACT | CLAIM | PLAUSIBLE | HYPOTHESIS | ESTIMATE | UNKNOWN
claim_state:    OBSERVED | COMPUTED | INTERPRETATION | SPECULATION
reversibility:  HIGH | MEDIUM | LOW | IRREVERSIBLE
authority:      READ_ONLY | COMPUTE_ONLY | RECOMMENDATION | JUDGE_REQUIRED
```

These four tags are the visual contract that the cockpit is **not a dashboard of answers** — it is a witness ladder. UI Law #0 in machine-checkable form.

**Reversibility:** high — additive UI surface, panels remain functional if tags are missing (with a "tag missing" warning).

### Forge 6 — Federation health monitor (NEW per sovereign 8-item list)

The cockpit must show live per-organ health, with **no hidden failures**. If WEALTH's registry call fails, the cockpit shows **WEALTH DEGRADED** in red, not silently pretends all is fine.

The monitor reads from each organ's `*_system_registry_status(mode='health')` (arifOS, GEOX, WEALTH, WELL) and the federation-level `arif_sense_observe(mode='health')`. State is rendered as:

```
arifOS: ● healthy (75/100)
GEOX:   ● healthy (88/100)
WEALTH: ● degraded — registry/health probe broken
WELL:   ● degraded — identity invariant failed, 4 tools missing
```

Per-state colours: green (healthy), amber (degraded), red (HOLD), grey (no telemetry).

**Reversibility:** high — monitor is read-only, doesn't mutate any organ state.

### Forge 7 — End-to-end workflows (NEW per sovereign 8-item list)

One canonical workflow per organ, plus one federation-level workflow. Each must complete start→finish on a dry-run before the cockpit is "ready."

```
arifOS:  init → sense → evidence → reason → judge → seal/hold/void
GEOX:    basin_overview → claim → evidence → challenge → judge
WEALTH:  deal → signal → wisdom → verdict (post-R0.1)
WELL:    assess_homeostasis → assess_livelihood → assess_reliability (post-R0.2)
AAA:     session → route organ → call tool → render panel → inspect evidence → challenge claim → judge → hold/seal
```

**Reversibility:** full — dry-runs, no irreversible action exercised.

### Forge 8 — Production telemetry (NEW per sovereign 8-item list, deferred)

Counters visible to the operator:

```
tool success rate
error rate
hold count
void count
latency (p50/p95/p99)
stale evidence (count, oldest age)
identity failure count
schema mismatch count
unauthorized mutation attempts
```

**Defer rationale:** This is a follow-on cycle. The first 7 forges must land and the cockpit must function before we instrument it. Building telemetry on a non-functional cockpit is build-the-observability-before-the-product, which is the wrong order.

**Reversibility:** high — pure counters, no behavior change.

---

## 8. Build order (sovereign-mandated, 10 steps + pre-flight)

Per sovereign correction (msg #39113, 09:56:22Z). Replaces the previous 7-step proposal. Steps 1–7 are operational; steps 8–10 are forgeable post-F3.

```
0. Forge 0 — Repair organ health         ← **MUST complete first** (R0.1 WEALTH, R0.2 WELL, R0.3 vault)
1. Fix WEALTH registry/health failure     ← Forge 0 R0.1
2. Fix or quarantine WELL identity        ← Forge 0 R0.2
3. Define aaa.ui.descriptor.v1            ← Forge 1
4. Build AAA static constitutional shell  ← Forge 2 (new) — session state, active organ, tool trace, evidence chain, verdict state, 9-signal panel, 888 HOLD gate, human approval boundary
5. Build GEOX renderer first              ← Forge 3 (geox)
6. Build arifOS verdict/gate renderer     ← Forge 3 (arifOS)
7. Build WEALTH and WELL renderers (post-health)  ← Forge 3 (wealth, well) — only after steps 1 + 2 pass
8. Add federation health panel            ← Forge 6 (new) — live per-organ health, no hidden failures
9. Add 888 HOLD visual gate               ← Forge 4 (extends)
10. Run one full dry-run workflow across all organs  ← Forge 7 (new) — session→route→tool→render→inspect→challenge→judge→hold/seal
```

**Step 0 is the hard gate.** Steps 1–2 are operational repair (sovereign-acked mutation). Steps 3–7 are the design protocol (descriptor schema + renderer packs). Steps 8–10 are the operational surface (health panel, HOLD gate, end-to-end dry-run). The previous 5 forge tasks in §7 are now embedded inside this 10-step build order. Forge 8 (production telemetry) is deferred to a follow-on cycle.



---

## 9. F2-honest risks (the part most forge specs skip)

| # | Risk | Severity | Mitigation |
|---|------|----------|------------|
| R1 | Model hallucinates a `ui.descriptor` that mis-represents the data (drops the uncertainty band, hides a `claim_state`) | **HIGH** | JSON Schema validation in the compiler; lane router refuses descriptors that drop required `uncertainty_band` / `evidence_refs` / `claim_state` fields; UI Law #0 invariant. |
| R2 | L7-G sandbox escape (LLM-generated code breaks out of iframe, reads L7-S DOM) | **HIGH** | Double-iframe default per MCP Apps; `sandbox="allow-scripts"` only (no `allow-same-origin`); CSP `frame-ancestors 'self'`; no cookies / no localStorage / no network egress by default; L7-G DOM is on a different origin from L7-S. |
| R3 | Generated UI manipulates human state (urgency colour, FOMO copy, fear framing in WEALTH) | **HIGH** | F6 Maruah check in the kernel; WELL `maruah_check: "block"` on any descriptor that fails the dignity check; L7-G forbidden in WEALTH verdict views and WELL readiness views. |
| R4 | Descriptor schema drift between organ and renderer (organ adds field, renderer doesn't know about it) | **MEDIUM** | `ui.contract` is a versioned id; renderer refuses unknown contract versions; organ-side CI enforces schema validation against the canonical set. |
| R5 | L7-D components become so numerous they become a new "static component zoo" we don't trust | **MEDIUM** | Each component contract requires: `forbidden_actions` list, `reversibility_required` list, F6 `maruah_check` field. Promotion to `approved` requires sovereign sign-off. |
| R6 | GEOX generative sandbox produces beautiful but unsound geological diagrams that get screenshotted and shared as "AI says X" | **MEDIUM** | Every L7-G output carries a permanent watermark: *"GENERATIVE SANDBOX · NOT SEALED · DO NOT CITE"*. Watermark cannot be removed via CSS (rendered in canvas, not DOM). |
| R7 | WELL consent flow is bypassed when output is routed through a third party (e.g. a Telegram bot) | **MEDIUM** | `ui.consent_required: true` is enforced at the LLM-bridge layer, not the UI layer. Telegram message handlers must check the consent flag before forwarding. |
| R8 | WEALTH epistemic_collapse — beautiful dashboards hiding uncertainty to "look professional" | **MEDIUM** | Uncertainty band is a **required** field in the descriptor schema; renderer refuses to drop it. `epistemic_collapse` is in the `forbidden` list for L7-D and L7-G. |
| R9 | The 5 forge tasks assume the current organ health; if WEALTH or WELL is unhealthy at forge time, the mapping breaks | **MEDIUM** | Re-verify `wealth_system_registry_status` and `well_assess_reliability` before Forge 3 starts for those organs. |
| R10 | The collaborative canvas (step 7) is out of scope but agents will start asking for it the moment declarative UI lands. Scope creep risk. | **LOW** | Build order explicitly excludes step 7. Defer to a follow-on forge spec. |

---

## 10. References

1. **Casas, R. (Postman), "Beyond Components: Designing Generative UI for MCP Apps"** — AI Engineer Summit 2026-06-03, 17 min. https://youtu.be/hCMrEfPG2Yg ; Japanese recap: https://finance.biggo.jp/podcast/57fa770d64c97ec0
2. **MCP-UI (MCP-UI-Org/mcp-ui)** — open-source implementation of the UI-over-MCP pattern. https://github.com/MCP-UI-Org/mcp-ui
3. **GEOX-UI-READINESS** (precedent, UI Law #0): `/root/.openclaw/workspace/forge_work/GEOX_UI.md`
4. **GEOX-CANON-31** (canon sealed 2026-06-06): `/root/.openclaw/workspace/forge_work/GEOX_CANON.md`
5. **GEOX-C1-CONSTITUTIONAL-INTEGRATION** (session/actor propagation): `/root/.openclaw/workspace/forge_work/GEOX_CONSTITUTIONAL.md`
6. **MCP FederationEnvelope spec** (Chapter 6): `/root/arifOS/static/arifos/theory/000/000_CONSTITUTION.md` (L06)

---

## 11. Carry-forward

- [ ] **Forge 0 (R0.1 WEALTH recovery) — diagnostic first, repair second.** Sovereign ack required before any mutation.
- [ ] **Forge 0 (R0.2 WELL identity restoration) — identify the 4 missing tools, re-register, verify identity invariant.** Sovereign ack required.
- [ ] **Forge 0 (R0.3 vault freshness) — synthetic SEAL probe to confirm write path.** Sovereign ack required.
- [ ] **If R0 fails on any organ: HOLD the entire spec.** Do not start Forge 1.
- [ ] Sovereign review of the spec body (HOLD gate).
- [ ] Re-verify WEALTH + WELL runtime health before Forge 3 starts on those organs (post-R0).
- [ ] If GREEN-SEAL on body + GREEN-pass on R0: schedule Forge 1 (descriptor schema) as next AGI task.
- [ ] Update HEARTBEAT.md with this forge ID.
- [ ] Update memory/2026-06-07 with session log.
- [ ] If REJECT: log lesson, close forge.

---

## 12. Sovereign final verdict (msg #39113, 09:56:22Z)

```text
GUI ready:        NO — 28/100
MCPs federated:   PARTIALLY — wired, not all healthy
arifOS kernel:    YES — usable as governed backend
Production cockpit: NOT YET
```

**Next decisive move:**

```text
Fix WEALTH + WELL health, then forge aaa.ui.descriptor.v1 and AAA L7 cockpit shell.
```

**Hard call from sovereign:** Do **not** build fully generative UI yet. Build first:

```text
Static sovereign shell
+ declarative MCP panels
+ federation health monitor
+ 888 HOLD gate
```

Only after that, add generative UI as a sandboxed display-only lane.

**System is useful for:** analysis, design, dry-run, tool-level experiments.
**System is NOT yet ready for:** one-screen command · real capital decisioning · irreversible forge execution · sealed federation operation · field/operator handover.

---

*"A normal UI says: here is the answer. arifOS UI must say: here is the answer, here is the evidence, here is the uncertainty, here is who is allowed to decide, and here is what would falsify it."* — UI Law #0, carried forward.

**DITEMPA BUKAN DIBERI — Intelligence is forged, not given. So are interfaces.**
