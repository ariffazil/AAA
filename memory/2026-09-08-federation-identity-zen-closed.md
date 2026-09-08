# MEMORY::FEDERATION_IDENTITY_ZEN_CLOSED::2026-09-08

- **Session Date:** 2026-09-08T09:54:00+08:00 (01:54:00Z)
- **Authority:** F13 Sovereign Ratification
- **Actors:** Arif Fazil (F13) · Antigravity · Hermes-Prime
- **Scope:** AAA / A2A Identity Layer, Discovery Plane, and Constitutional Division of Labor

---

## 1. Closed vs Pending (C-1 through C-10)

| Item | Description | Enforcement Mechanism | Terminal Reality Evidence |
|---|---|---|---|
| **C-1** | Triple Identity (10 cards shadowed) | Invariant INV-005: Canonical `/agent-cards/` precedence | `/a2a/discover` returns 51 unique agents; canonical L1 cards preserved |
| **C-2** | 9 INADMISSIBLE cards / parse errors | Schema filter: `isLikelyAgentCardFile` & `SKIP_DIRS` | `validate-a2a-cards.mjs`: 8/8 PASS; 0 parse errors |
| **C-3** | Three competing protocols | Pinned A2A v1.0.0 wire contract | Conformance validated across active gateways |
| **C-4** | Discovery 400s (`/a2a/agents`, `/a2a/discover`) | GET exemption in `a2a-version-middleware.js` + router alias | `curl -i http://127.0.0.1:3001/a2a/discover` and `/a2a/agents` return 200 OK |
| **C-5** | Schema fragmentation | 51 cards strictly classified across 4 CIV-33 layers | Layer distribution: `identity: 5`, `harness: 14`, `binding: 30`, `retired: 2`, `unclassified: 0` |
| **C-6** | `species` vs `species_proxy` drift | Symmetric normalization in `normaliseCard()` | Both accessors available simultaneously across all cards |
| **C-7** | Cards missing explicit `id` (`aaa-gateway`, `skill-auditor`) | Layer-aware deterministic fallback from directory structure/slug | Cards loaded and addressable via `/a2a/agents/:id` |
| **C-8..10** | README governance inflation | Canonical 4-organ division of constitutional labor in `AAA/README.md` | `arifOS = JUDGE`, `AAA = REGISTER & DISPLAY`, `arifFlow = METABOLIZE`, `A-FORGE = EXECUTE` |

---

## 2. The Non-Obvious Lesson: The 76-Day Doctrine Gap

> **76 days elapsed between schema v2.3.0 forge (2026-07-16) and INV-005 enforcement (2026-09-08).**

- **The Failure Mode:** Doctrine existed in prose, but bouncers were not at the door. Writing a specification or creating a canonical folder (`agent-cards/`) does not prevent a runtime loader from wandering into secondary folders (`agents/`) and overwriting canonical identities unless code actively rejects/bounces the intruder.
- **The Constitutional Rule:** **Detection is debt until it can say NO.** An invariant that merely logs a warning is not an invariant; it is documentation. Invariant INV-005 only became real when `register()` unconditionally blocked secondary scans from clobbering L1 identities.

---

## 3. Residuals (Honest Shadows Under 888_HOLD)

Per F2 TRUTH and the Witness-First Doctrine, the following remain unexecuted and unmasked:

1. **Item 7 (Physical File Collapse on Disk):**
   - INV-005 bouncers are at the door (routing and discovery level deduplication is active).
   - Duplicate files still physically exist across `agents/_lanes/` and `agents/_external/`.
   - Physical deletion/archival of 37 secondary cards and migration of survivors requires explicit F13 sovereign authorization (`888_HOLD`).

2. **KVM4 / KVM2 Cross-Node Verification:**
   - All live verification probes in this session were KVM8-local.
   - The 3-node invariant (`MACHINE_MAP.md` / `federation-invariants.md`) requires an end-to-end cross-node handshake probe across Tailscale mesh (`100.64.0.5` KVM4, `100.64.0.4` KVM2).

3. **FRAME as Independent Witness:**
   - FRAME (`:18085`) observer contract remains an external probe surface.
   - Promotion of FRAME from heuristic observer to certified independent witness requires dedicated challenge testing before formal promotion.

---

**DITEMPA BUKAN DIBERI — Forged, Not Given.**
