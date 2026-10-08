---
proposal_id: GEOX-OBSERVE-FORM-2026-10-05
status: PROPOSAL (NON-CANONICAL · NON-BINDING · AWAITING F13)
modified: 2026-10-05T23:25Z
proposer: external advisory (F13 SOVEREIGN received via Telegram AAA, 2026-10-05)
scope: site/UI mutation at https://geox.arif-fazil.com/observe/
proposer_layer: EMD-stance validated by external agent
conflicts: NONE FOUND against ratified canon
kin: [[MCP-Orthogonalization-Research-2026-10-05.pdf]], [[EUREKA-CAPABILITY-CENTRIC-ARCHITECTURE-2026-10-05]], [[GE0X 22 vs 27 drift finding]]
complements: [[F1 AMANAH]], [[F2 TRUTH]], [[F9 anti-hantu]], [[Basin as context-only]]
operational_gate: NO CODE MUTATION until F13 SOVEREIGN future review
session_evidence: msg 65400+ (Arif "rek" binary for both sites) + external advisory validation
---

# PROPOSAL — GEOX Observe Form (Conditional Rendering + Epistemic Floor)

## 0 · Provenance

**Source:** External advisory received 2026-10-05 23:21 MYT (Telegram AAA, post-GEOX observe payload). External agent validated F1/F2 compliance and explicitly recognized the boundary of its own authority: refused to touch `eureka-entries.jsonl` or deploy code to `geox.arif-fazil.com` without explicit F13 word.

**Scope this document:** record the design blueprint, NOT execute code. Status PROPOSAL, NON-CANONICAL, NON-BINDING, AWAITING F13 FUTURE REVIEW.

**Reference sites:**
- `https://geox.arif-fazil.com/observe/` (live, static entry point, F1-compliant per proposer)

## 1 · Current state (measured)

| Surface | Observed |
|---|---|
| Render behaviour | Static — all metadata parameters (Field tests, Seismic, Fossil) render concurrently |
| Visual entropy | ΔS > 0 (concurrent display, cognitive load) |
| F1 compliance | Met (memory-only, EXIF-stripped) |
| Epistemic floor | QUALIFIED_CANDIDATE |
| Tool count surface | **22 live** (per 888-APEX verdict drift finding F2) |
| Tool count registry | **27 advertised** (per 888-APEX verdict drift finding F2) |
| Live page state | 22 tools, all metadata fields visible regardless of modality selection |

## 2 · Proposed UI/UX changes (verbatim from proposer)

### 2.1 Conditional rendering (state-driven logic)

Tie metadata visibility strictly to the selected Modality.

| If `Modality ==` | Render only |
|---|---|
| `seismic` | Seismic metadata |
| `outcrop` \| `rock` | Field tests |
| (other modalities TBD) | TBD per modality |

**Expected effect:** reduce visual noise on initial render. "Relaks tapi tajam."

### 2.2 Branding & styling compliance

- Dark background
- Geometric boundaries
- Strict primary colours for active UI states, warning tags, selected toggles:
  - **Red** (active, warning)
  - **Yellow** (selected toggle, attention)
  - **Blue** (informational, idle)
- **ABSOLUTELY NO:** human figures, organic shapes, gradients, decorative elements in any loading icon or empty state

### 2.3 Mathematical isolation of bias (EMD-stack enforcement)

Basin is "context only — never raises confidence."

**Backend enforcement rule (proposed, NOT YET RATIFIED):**

```text
weight_multiplier(Basin) = 0.0   # when calculating final inference probability
```

Basin routes context but **cannot inflate P(truth)**. This is a hard F1 claim: Basin does not influence confidence, only routes context.

### 2.4 Optional Macrostrat API hook

Since EXIF/GPS is stripped for operational safety, an optional manual lat/long input field may be added. If provided, GEOX queries the Macrostrat API to pull bounding stratigraphic realities **before** image processing begins. Output: hard factual baseline (F2).

### 2.5 Output discipline

Final output view explicitly displays `Ω₀` (Uncertainty) threshold.

```text
IF confidence < 0.99:
    return UNKNOWN
ELSE:
    return inference
```

Poor image quality must produce UNKNOWN, not a low-confidence hallucination. (F9 anti-hantu alignment.)

## 3 · Architecture options (verbatim from proposer, trade-offs preserved)

| Option | Architecture | Pros | Cons |
|---|---|---|---|
| **A. Client-Side DOM Toggling** | JavaScript event listeners hide/show div blocks based on active Modality span | Cepat setel; zero backend refactoring | Rigid; tech debt when new modalities (e.g. well logs) added |
| **B. JSON Schema-Driven Render** | Form structure passed dynamically from GEOX backend via JSON schema; frontend maps it | Highly modular; ΔS < 0 for future expansion | Requires rewriting frontend rendering pipeline |
| **C. Agentic Pre-Processing** | User uploads image first; A-FORGE/GEOX identifies modality, then prompts for missing metadata | Lowest user friction; true multi-agent utility | Higher latency; two-step processing (compute cost ↑) |

**External recommendation:** Option A (tactical patch) for fast iteration; Option B (refactor) for long-term ΔS < 0.

## 4 · F1-F13 floor analysis (mine, recorded for review)

| Floor | Status | Note |
|---|---|---|
| F1 AMANAH (Safety) | Met by current site (EXIF-stripped, memory-only). Conditional rendering does not weaken. | ✓ |
| F2 TRUTH (Epistemic) | Strengthened by Ω₀ threshold and Macrostrat baseline. | ↑ |
| F3 (verification) | Not directly affected. | = |
| F4 CLARITY (ΔS) | Conditional rendering explicitly reduces visual noise. | ↑ |
| F9 anti-hantu | Strengthened by `< 0.99 → UNKNOWN` rule. | ↑ |
| F11 (privacy) | Already met (no EXIF). Macrostrat hook is opt-in. | = |
| F13 SOVEREIGN (direction) | **OPEN** — this proposal is direction change to a public site. | Awaiting F13. |

**The Basin weight = 0.0 rule is a F1 floor for GEOX specifically.** It is currently unratified. It claims a constitutional property (Basin does not influence confidence) that has not been canon-sealed.

## 5 · Open ratification questions (NOT YET ANSWERED)

1. Is `weight_multiplier(Basin) = 0.0` a ratified F1 floor for GEOX? If yes, the rule is binding. If no, the rule is a design choice awaiting F13.
2. Which architecture option (A, B, or C) does F13 select?
3. Is the Ω₀ threshold 0.99 (proposer's value) or another value? F2 testable; needs measurement.
4. Does Macrostrat API integration introduce new external dependencies? If yes, that is a new sovereign claim (vendor selection, F13 territory).
5. Brand canon: where is "Red/Yellow/Blue only, no human figures" canon-sealed? Not found in current search. If not canon, this proposal implies codifying it.

## 6 · HOLD list (what is NOT done by this proposal)

1. **NOT coded:** any HTML/JS/CSS mutation.
2. **NOT deployed:** anything to `geox.arif-fazil.com/observe/` or any GEOX surface.
3. **NOT mutated:** the GEOX 22-vs-27 drift (still open; F2 from 888-APEX verdict).
4. **NOT ratified:** the Basin weight = 0.0 rule.
5. **NOT integrated:** the Macrostrat API.
6. **NOT codified:** the brand canon (Red/Yellow/Blue only, no human figures).
7. **NOT auto-promoted:** this proposal is not canon. Status is PROPOSAL.

## 7 · F13 future review items

When musyawawah revisits this proposal:

1. Resolve Basin weight = 0.0 ratification question.
2. Choose A/B/C architecture.
3. Confirm or amend Ω₀ threshold (0.99 or other).
4. Decide vendor relationship with Macrostrat (if applicable).
5. Codify or reject the brand canon extension.
6. Sequence against the 6 drift defects (F1-F5 AUTO-FIX, F6 F13-HELD).

## 8 · Receipts

| Claim | Source | Status |
|---|---|---|
| Site is F1-compliant (EXIF-stripped, memory-only) | External advisory, 2026-10-05 23:21 MYT | received |
| Site currently renders 22 live tools | 888-APEX drift finding F2, this session | measured |
| 5 drift defects (F1-F5) classified AUTO-FIX | 888-APEX, this session | attested |
| F6 sovereign signing classified F13-HOLD | 888-APEX, this session | attested |
| "rek" binary issued by F13 SOVEREIGN | Arif, 2026-10-05 23:24 MYT (Telegram AAA, msg 65400+) | received |
| External agent's EMD validation ("Payload validated, Option 1 rek") | External, 2026-10-05 23:23 MYT | received |
| Basin weight = 0.0 ratified? | — | UNRESOLVED, open |
| Brand canon codified? | — | UNRESOLVED, open |

## 9 · Cross-link

- Companion proposal: `/root/AAA/cockpit/proposals/SEP1865-GALLERY-ROUTING-2026-10-05.md`
- Foundation: `/root/AAA/eurekas/EUREKA-CAPABILITY-CENTRIC-ARCHITECTURE-2026-10-05.md`
- Drift context: 888-APEX verdict (this session, 6 findings)
- Memory pointer: `/root/.claude/projects/-root/memory/MEMORY.md`

---

> *DITEMPA BUKAN DIBERI ⚒️*
> *Recorded as PROPOSAL. Not canon. Not binding. Awaiting F13 future review.*
> *A capability survives; an implementation mutates; a transport retires.*
> *Basin routes context. Basin does not inflate P(truth). If ratified.*
> *ΔS < 0 — diagnostic preserved, no decision forced, no F13 word asked except "rek."*
