# Ecosystem Expansion — DECISIONS Log

> **STATUS:** Living record of decisions, draft state, and pending actions.
> **LAST UPDATED:** 2026-08-20 (post-555-VERIFY)

---

## D001 — F13 Intent vs Syntax (DOCTRINE)

**Decision:** Under F13 SOVEREIGN, authority derives from unambiguous intent, not magic words. A one-word execution instruction against a stated T2 scope is sufficient.

**Source:** Arif correction 2026-08-20 against initial "go" hold.

**Saved to memory:** `/root/.claude/projects/-root/memory/f13-intent-not-syntax.md`

**Impact:** Future single-word sovereign instructions against known scope should proceed under stated T1.5 envelope, not gate on syntax.

---

## D002 — Phase 1 Scope REFINED (CHARTER INTERPRETATION)

**Decision:** Phase 1 (DISCOVERY) is **NOT** "build discovery from zero." Phase 1 is **"complete and publish the federation manifest"** — `arifos.json`. The existing A2A cards already fulfill most of the directive's discovery requirements.

**Source:** Cross-walk against existing `/root/AAA/.well-known/` inventory.

**Impact:** Phase 1 blast radius is minimal — single new public file at `arif-fazil.com/.well-known/arifos.json`.

**Saved to:** `/root/AAA/forge_work/2026-08-20/ecosystem-expansion/ORGAN_CROSSWALK.md`

---

## D003 — Drafts Location (FILE STRUCTURE)

**Decision:** All Phase 1 drafts live under `/root/AAA/forge_work/2026-08-20/ecosystem-expansion/`.

**Layout:**
```
/root/AAA/forge_work/2026-08-20/ecosystem-expansion/
├── DECISIONS.md                          (this file)
├── EXECUTION_PLAN.md                     (5-phase plan)
├── ORGAN_CROSSWALK.md                    (organ inventory + gap analysis)
└── drafts/
    ├── arifos.json                       (federation manifest, net new)
    └── agent-json-evolution-proposal.md  (proposal — DO NOT modify existing card)
```

**Source:** Standard arifOS forge_work convention (cf. `atlas333-deep-research-2026-07-15`, `kernel-test-surface-audit-2026-07-16`).

**Impact:** Reversible. Wipe directory = revert all Phase 1 drafts.

---

## D004 — Charter as Instruction Fragment (DOCTRINE PERSISTENCE)

**Decision:** Charter lives at `/root/AAA/instructions/ecosystem-expansion.md` as a canonical instruction fragment.

**NOT YET RENDERED INTO CLAUDE.md.** Requires `render-agents.sh` execution after Arif approval.

**Source:** `CLAUDE.md` rendering convention (cf. base/topology/security/build etc. fragments).

**Impact:** Once rendered, every agent that loads `CLAUDE.md` inherits the strategic thesis and 5-phase path.

---

## D005 — Separation of Powers for Phase 1 (PROTOCOL)

**Decision:** Phase 1 deploy follows the full 5-stage chain:
1. 333 PROPOSAL (this draft set) — DONE
2. 555 VERIFY (independent read by 2nd agent against draft + reality) — DONE 2026-08-20
3. 888 JUDGE (Arif verdict: SEAL / HOLD / SABAR / VOID) — PENDING
4. A-FORGE EXECUTE (Hermes-only VPS mutation) — PENDING
5. VAULT999 WITNESS (immutable seal receipt) — PENDING

**Source:** `Separation of Powers Doctrine 2026-08-04`.

**Impact:** No single agent may execute Phase 1 alone. Hermes holds VPS access, Arif holds F13, this session holds draft only.

---

## D006 — 555 VERIFY Outcome (VERIFICATION RECORD)

**Decision:** Phase 1 drafts passed independent VERIFY with **1 fixable finding**.

**5-lens audit results:**

| Lens | Result |
|---|---|
| 1. JSON Schema & Structure | PASS — valid JSON, 21 top-level keys, all required fields present |
| 2. Secret/Credential Leakage | PASS — no tokens, keys, signatures, or fingerprints leaked |
| 3. Surface Accuracy | PARTIAL — 1 finding (organ ID naming convention) |
| 4. Doctrinal Alignment | PASS — F1/F2/F4/F8/F11/F12/F13, verdict grammar, sampling, marketplace all aligned |
| 5. Reality Claims | PASS — all ports/statuses cross-verified against memory + existing surfaces |

**Finding F-1 (FIXED 2026-08-20):**
- Draft organ IDs (`arifos`, `a-forge`, `geox`, `wealth`, `well`) did not match the existing `agent-card.json` federation_organs convention (`arifos-mcp`, `a-forge-mcp`, etc.)
- **Fix applied:** Added `mcp_id` field per organ carrying the canonical `-mcp` suffix
- Both `id` (short form) and `mcp_id` (canonical form) now present
- Post-fix cross-check: ALL 5 mcp_id values MATCH existing agent-card.json federation_organs[].id

**VERIFY verdict:** PARTIAL_PASS → **PASS after F-1 fix**.

**Source:** `/root/AAA/forge_work/2026-08-20/ecosystem-expansion/drafts/arifos.json` (5-lens audit)

**Impact:** Drafts are now ready for 888 JUDGE (Arif verdict). No further VERIFY needed unless drafts are modified.

---

## Pending Actions (HOLD)

| ID | Action | Owner | Status |
|---|---|---|---|
| A001 | Read drafts, verify against reality | 2nd agent (555-VERIFY) | ✅ DONE 2026-08-20 — PASS |
| A002 | Phase 1 SEAL verdict | Arif (888-JUDGE) | PENDING |
| A003 | `cp arifos.json` to web root | Hermes (A-FORGE EXECUTE) | PENDING |
| A004 | Verify all `.well-known/*` paths return 200 | Hermes | PENDING |
| A005 | Seal to VAULT999 | arif_seal | PENDING |
| A006 | Render charter fragment into CLAUDE.md | `render-agents.sh` | PENDING Arif approval |
| A007 | Verify OAuth 2.1 endpoints actually serve (flag raised in ORGAN_CROSSWALK) | Hermes | PENDING — pre-SEAL check |

---

## Rejected Paths (VOID)

| Path | Reason |
|---|---|
| Overwriting existing SEAL-signed agent.json | Invalidates Ed25519 signature; high blast for marginal gain |
| Overwriting existing SEAL-signed agent-card.json | Same as above |
| Building organs 03/04/05 before ORGAN_08_AUTH broker | Credential sprawl, no governance over tokens |
| Building ORGAN_07_DNS_CDN with write capability | Surface control too sensitive for broad automation |
| Skill Marketplace before Phase 1-4 operational | Pre-empts ecosystem maturity |
| MCP Sampling enablement before Phase 2 + 3 | Identity not proven |

---

## Next Session Carry

If this session ends before Phase 1 SEAL:

1. **Read first:** `/root/AAA/forge_work/2026-08-20/ecosystem-expansion/DECISIONS.md` (this file)
2. **Then read:** `EXECUTION_PLAN.md` and `ORGAN_CROSSWALK.md`
3. **Then ask Arif:** "Phase 1 SEAL or HOLD?"
4. **If SEAL:** Hermes deploys `drafts/arifos.json` per handoff envelope

---

*Maintained by 333-PROPOSAL. Update on every decision.*