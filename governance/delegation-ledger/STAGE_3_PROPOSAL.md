# Stage 3 Proposal — Cedar policy compilation OR A2A extension

**Status:** PROPOSAL ONLY — NOT EXECUTED per CONTRACT_TEMPLATE_v0.1.md Clause 4
**Chain lineage:** Stage 0 → Stage 2 → Stage 3 PROPOSAL (this file)
**IBCT token_id:** sha256:25d2f4fed0da8f056dab958a90efcb824ba64123415b0551e7738ada92c001f1
**IBCT chain_hash:** sha256:e90206dd535e8374462a442d7c399636d818da84f04ddce082f7913e20efbb10
**Chain index:** 2 (parent = Stage 2 chain_hash `sha256:7bb94ef8525a8d42a...`)
**Issued:** 2026-08-17T05:51:19Z

---

## Why this proposal exists

Stage 0 (schema + contract + proposals) and Stage 2 (B1+B2+B3 reference impl + wrapper + demo + LIVE service) are FORGED. The remaining work in the original delegation-ledger proposal document is:

1. **Cedar policy compilation** — express F1-F13 floors as Cedar policies at the AgentGateway
2. **A2A extension** — add IBCT fields to A2A Agent Cards

Per the IBCT contract template (CONTRACT_TEMPLATE_v0.1.md Clause 4), this is OUT OF SCOPE for Stage 0/2 execution. This is the PROPOSAL for Stage 3.

---

## Option A — Cedar policy compilation

### What it would do
Replace the existing `cedar_bridge.py` Phase 2 stub (always returns ALLOW with override=True) with actual Cedar policy compilation. Express F1-F13 floors as Cedar policies with `@tier("hard")` for non-compensatory enforcement.

### Existing assets
- `/root/arifOS/arifosmcp/arifos_policy/cedar_bridge.py` — Phase 2 stub (27 lines)
- Cedar semantics research: "explicit Deny for any one policy always overrides any Allow" + `@tier("hard")` for absolute floors

### What needs to happen
1. Install Rust Cedar engine (Cargo dependency, or use AWS-verifiedpermissions)
2. PyO3 binding for Python integration
3. Map each F1-F13 floor to a Cedar policy with @tier("hard") annotation
4. Test: each floor blocks corresponding action (e.g., F1 AMANAH blocks rm -rf)
5. Resolve the existing override=True semantic — does arifOS still bypass Cedar, or is Cedar now non-compensatory?

### Risk
- MEDIUM — touches kernel source. The override=True semantic must be resolved before deploy.
- Backward-compat: any tools relying on the override=True path would break.

---

## Option B — A2A extension

### What it would do
Add IBCT fields to A2A Agent Cards at `/root/AAA/aaa-a2a/src/aaa_a2a/extensions/ibct/`. Per the strategic pivot doc, this would engage A2A Discussion #741 + Issue #2026.

### Existing assets
- A2A gateway already running on :3001
- Agent Card schema at `/root/AAA/aaa-a2a/`

### What needs to happen
1. Read A2A Discussion #741 + Issue #2026 to confirm scope alignment
2. Define IBCT field subset for A2A Agent Cards
3. Mint + verify test tokens with the new schema
4. Publish contribution back to A2A

### Risk
- LOW — additive only, new dir, no modifications to existing A2A code
- A2A spec is still in flux; contributing early might lock in bad design (mitigated by marking as proposal)

---

## Recommended sequencing

1. **Option A first** (smaller blast radius — just kernel + cedar_bridge.py)
2. **Option B after** (extends to A2A ecosystem)

OR

1. **Option B first** (additive only, lower risk)
2. **Option A after** (requires kernel changes)

---

## F13 ratification questions

1. Authorize Option A (Cedar policy compilation)?
2. Authorize Option B (A2A extension)?
3. Set sequence (A-then-B or B-then-A)?
4. Override semantic: does Cedar's "explicit Deny" still allow arifOS kernel override, or is F1-F13 non-compensatory?

---

DITEMPA BUKAN DIBERI ⚒️ — Stage 0 → Stage 2 sealed. Stage 3 PROPOSAL awaits F13 ratification per Clause 4.
