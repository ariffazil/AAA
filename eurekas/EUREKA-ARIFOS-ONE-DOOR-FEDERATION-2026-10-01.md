---
eureka_id: EUREKA-ARIFOS-ONE-DOOR-FEDERATION-2026-10-01
status: RECEIPT (not SEAL)
canonical_session: 2026-10-01-arf-via-cli
modified: 2026-10-01T22:05Z
ratifiers: 555 AUDITOR only (boundary check)
sovereign_sah: pending — 10 sovereign priorities queued (#21-#30)
type: receipt + diagnostic
extends: [[EUREKA-AFORGE-SEMANTIC-COMPRESSION-2026-10-01]] [[EUREKA-NOAR-FLIGHT-DEPENDENCY-2026-10-01]]
---

# EUREKA — arifOS One-Door Federation (Arif's federation-β diagnostic)

## 1. The rule Arif filed

\[
\boxed{\text{One Door} \neq \text{One Pipe}}
\]

arifOS = constitutional ingress only (identity, intent, routing, authority, judgment, evidence policy, sealing). Not byte-pipe. Organs feed bounded lanes; arifOS issues governed execution envelope; organs do physical compute and return evidence.

## 2. Live federation reality today

| Component    | Physically alive | Own surface healthy | Routable by arif_route | Status |
|-----------|----------------------|----------------------|------------------------|--------|
| arifOS    | Yes    | DEGRADED (source/built deployment drift) | Kernel itself | P0 blocker |
| A-FORGE    | Yes, ~5 ms    | Federation surface scan PASS | Yes (as a_forge) | Near-ready |
| GEOX    | Internally alive, ~55 ms    | Internal clean; external connector rejects advertised tools | Yes | Ingress drift |
| WEALTH    | Internally alive, ~24 ms    | External MCP timed out twice | Yes | Transport reliability gap |
| WELL    | Yes, ~19 ms    | 10/10/10/10, zero phantoms | Yes | Ready |
| HERMES    | Yes; registry clean    | 15 tools, 13 capability families, no drift | **No** | Missing from router |
| CHRON    | Yes    | 106,994 episodes, 38 predictions | **No** | Missing from router |

Canonical arifOS routing coverage = 4/6 = 67%. Federated components ≠ federated ingress.

## 3. Constitutional router unknown_organ evidence

```
organ = "aforge"  →  UNKNOWN_ORGAN
organ = "a_forge" →  ACCEPTED
organ = "hermes"  →  UNKNOWN_ORGAN
organ = "chron"   →  UNKNOWN_ORGAN
```

Known organs in router: a_forge, aaa, arifos, geox, wealth, well.

## 4. Two federation fabrics

GEOX → **internal alive ≠ external advertised**. `geox_system_registry_status` / `mcp_health_check` rejected as "not on canonical or compat surface"; canonical surface has 26 tools but `geox_surface_status(mode='registry')` not exposed through connector.

WEALTH → **internal alive ≠ external connector reachable**. Two external `wealth.fastmcp.app` calls timed out.

An external agent must NOT need to choose between localhost WEALTH, FastMCP WEALTH, a bridge, or A-FORGE. It must ask arifOS: "I need capital evidence." Then infrastructure decides.

## 5. The architecture (Arif's canonical diagram)

```
HUMAN / AAA AGENT
   │
   ▼
╔══════════════╗
║    arifOS    ║   ← ONE DOOR (identity, intent, authority, routing,
╚══════╤═══════╝     policy, judgment, sealing)
       │
       ├─────────────────┬─────────────────┐
       ▼                 ▼                 ▼
    HERMES             CHRON           A-FORGE
    meaning             time            actuation
       │                 │                 │
       │          ┌──────┴───────┐         │
       │          │              │         │
       ▼          ▼              ▼         ▼
     GEOX       WEALTH          WELL     physical
     Earth      capital       vitality    tools
       │          │              │         │
       └──────────┴──────┬───────┴─────────┘
                         ▼
                      REALITY
                         │
                         ▼
               evidence / consequences
                         │
             HERMES + CHRON + witnesses
                         │
                         ▼
                      arifOS
                         │
               memory / judge / seal
```

## 6. Constitutional ingress, not API aggregation

> Any agent can begin with only the eight arifOS verbs and does not need prior knowledge of organ-specific MCP APIs.

Acceptance criterion:
- A fresh agent knows only `arif_init`, `arif_observe`, `arif_think`, `arif_route`, `arif_memory`, `arif_judge`, `arif_forge`, `arif_seal`.
- "Interpret this seismic section" → routes to GEOX.
- "Is this financial allocation viable?" → routes to WEALTH.
- "Is the machine healthy enough to proceed?" → routes to WELL.
- "Separate fact, inference and perspective" → routes to HERMES.
- "What did we expect and were we wrong?" → routes to CHRON.
- "Change this repository" → routes to A-FORGE.

Agent must NOT need `geox_*` / `wealth_*` / `well_*` / `hermes_*` / `chron_*` / `forge_*` unless arifOS progressively discloses.

## 7. HERMES vs CHRON: distinct reasons to add

HERMES (meaning integrity): claims / provenance / perspective / qualia / contradictions / counterstories / consent / moral physics / institutional decay / reality grounding. **Meaning integrity ≠ constitutional authority. Keep separation.**

CHRON (temporal spine): 106,994 episodes (observe 106,955 / predict 25 / verify 11 / learn 3), 38 predictions (15 active / 13 verified). Already understands **prediction_birth ≠ observation ≠ verification ≠ calibration**.

For every consequential arifOS decision:
```
arifOS judgment
  → CHRON registers expected consequence
  → A-FORGE executes
  → Reality changes
  → CHRON observes later outcome
  → prediction vs reality
  → arifOS memory / policy update
```

Without CHRON behind the door, the federation governs now but does not systematically govern whether yesterday's decision was actually right.

## 8. The 10 priorities (compiled into hold queue)

| # | Priority | Lane | Queue ID |
|---|----------|------|----------|
| 1 | Fix arifOS itself (source 74d17d7 vs built/deployed 297abcb; deployment_drift) | arifOS kernel P0 | f13-kernel-truth-20261001-0021 |
| 2 | Register HERMES and CHRON in organ registry + arif_route | arifOS router | f13-register-20261001-0022 |
| 3 | One FederationManifest as the only topology SOT | federation manifest | f13-manifest-20261001-0023 |
| 4 | Separate internal vs external health (organ_state / internal_transport_state / external_mcp_state / surface_conformance_state) | federation health | f13-health-20261001-0024 |
| 5 | Normalize every identity/alias (aforge/A-FORGE/a_forge/forge → a_forge; same for HERMES, CHRON) | arifOS identity | f13-identity-20261001-0025 |
| 6 | arifOS session propagation universal (one arif_init session through all downstream organs) | arifOS + organs | f13-session-uni-20261001-0026 |
| 7 | Common handoff envelope (session/actor/intent/claim_evidence_refs/authority_class/time/provenance/capability/consent/return_schema) | federation envelope | f13-handoff-20261001-0027 |
| 8 | Organs return evidence packet, not verdict (GEOX=earth, WEALTH=capital, HERMES=meaning, CHRON=temporal, WELL=wellness, A-FORGE=execution) | organs verdict boundary | f13-verdict-20261001-0028 |
| 9 | Health-aware route degradation (ORGAN_ALIVE_EXTERNAL_INGRESS_DOWN → internal bridge/fallback) | arifOS router | f13-degrade-20261001-0029 |
| 10 | End-to-end federation conformance test (fresh agent + 8 arifOS tools → 6 organs → S_declared = S_routed = S_callable = S_observed) | conformance suite | f13-conformance-20261001-0030 |

## 9. The S-invariant (when federation is real)

\[
S_{declared} = S_{routed} = S_{callable} = S_{observed}
\]

Until this holds, federation is not real.

## 10. Maturity estimate (Arif's analytic estimates)

| Dimension | Current |
|-----------|--------:|
| Organ specialization | 9/10 |
| Individual organ capability | 8–9/10 |
| Internal reachability | 8.5/10 |
| Constitutional separation | 8/10 |
| Common session/authority model | 7/10 |
| Canonical router coverage | ~6.5/10 |
| Surface truth across all ingress paths | 5.5/10 |
| External MCP reliability | 5–6/10 |
| Cross-organ temporal learning | 5/10 |
| True "one door" experience | ~6/10 |

Verdict: **federation-ready architecture, but not federation-complete runtime.**

## 11. Scar class

Extends the chain: [[scar-2026-09-28-claimed-before-checking-twice]] [[scar-2026-09-30-hermes-mcp-organs-alive-vs-healthy]] [[EUREKA-NOAR-FLIGHT-DEPENDENCY-2026-10-01]].

New scar element: **"One Door ≠ One Pipe"**:

> Constitutional ingress must NOT collapse into a single byte-pipe. arifOS governs; organs execute over bounded lanes.

## 12. Constitutional verdict

- F1 AMANAH: read-only hold queue over the diagnostic. ✓
- F2 TRUTH: cited live state (`source_commit 74d17d7` etc.) and the org registry. ✓
- F13: hold; 10 F13 binaries queued. ✓
- human-attention-membrane: do not re-ask; do not menu; offer one binary only. ✓

## 13. Reversibility

This receipt is a markdown artifact. No kernel mutation, no registry mutation, no schema mutation, no MCP call. If Arif reads and concludes "not my lane, ignore," this receipt is sealed-and-stale in 7 days and archived.

## 14. Receipt path

- This receipt: `/root/AAA/eurekas/EUREKA-ARIFOS-ONE-DOOR-FEDERATION-2026-10-01.md`
- Hold queue: `/root/AAA/data/hold_queue_30day_f13_binaries_2026-10-01.jsonl` (30 binaries, all SOVEREIGN_HOLD)
- Memory index: `/root/.claude/projects/-root/memory/MEMORY.md`