# NEVER COPY-PASTE BETWEEN AGENTS — Implementation Guide

> **Status:** SPEC (operational guidance for arif + the federation)
> **Forged:** FI-008 · 2026-09-21 ~02:46 MYT
> **Premise:** state-carrying envelopes + A2A constitutional layer = no human as middleware

---

## The principle (compressed)

\[
\boxed{\text{Machine carries state; human carries meaning.}}
\]

Eight things machines must carry so humans never have to:

\[
\{\text{state, context, provenance, routing, formatting, memory, verification, retries, bookkeeping}\}
\]

Six things humans must contribute (and only these):

\[
\{\text{intent, meaning, values, consent, judgment, sovereignty}\}
\]

---

## What changes TODAY (Arif's behavior)

| Before | After |
|---|---|
| Read agent A output | State envelope arrives at agent B with full context |
| Copy/paste to agent B | Agent A's `arif_init` session-id is the thread — B inherits it |
| Re-explain context to agent B | B reads the conversation state from VAULT999 |
| Verify agent A's claim manually | A's claim carries provenance + trust envelope; B sees evidence chain |
| Translate formatting manually | Agents share canonical schema; formatting is automatic |
| Repeat "yes continue" between agents | Authority envelope carries ACT scope; agents continue within scope |
| Download/upload artifacts between tools | Artifact routing via A2A Message + Artifact semantics |
| Remember what was done | VAULT999 receipts are the memory; artifact IDs are stable |

---

## What's already in place (arifOS primitives)

The 7 operating chain verbs each carry envelopes by design:

```
arif_init     → identity envelope (actor, session, scope, intent)
arif_observe  → observation envelope (what, when, source, confidence)
arif_think    → reasoning envelope (claim, basis, alternatives, uncertainty)
arif_route    → dispatch envelope (organ, tool, target, authority)
arif_memory   → persistence envelope (artifact_id, retention, provenance)
arif_judge    → verdict envelope (claim, evidence, weight, dissent)
arif_seal     → ratification envelope (sovereign authorization, immutable)
```

Plus this session's deliverables:

| Artifact | What it eliminates |
|---|---|
| `/etc/arifos/canon/federation-release.json` (G0c) | "Which version is running?" — manual probing |
| `/root/scripts/federation_verifier.py` + ledger | "Did the substrate move?" — manual drift detection |
| `/root/scripts/federation_quiet_detector.py` | "Is the federation stable?" — manual substrate observation |
| `/etc/arifos/federation/surface-schema.json` | "What does each organ offer?" — manual discovery |
| `/root/AAA/specs/a2a-constitutional-layer.md` | "Can I trust this agent?" — manual trust propagation |
| `/root/AAA/specs/epoch-binding-canonical-candidates.md` | "Is this canon still valid?" — manual staleness check |

---

## What needs to be built (the A2A wiring)

The constitutional envelopes already specified. Three implementation steps:

### Step 1: arif_route emits constitutional envelopes (T1 patch)

Every `arif_route` call already carries intent, organ, tool, args. Add:
- identity envelope (who)
- capability envelope (what the target organ actually offers right now)
- authority envelope (what scope the caller is operating in)
- trust envelope (epistemic trust of source claim)

This is a small change to `arif_route`. Reversible. ~½ day.

### Step 2: A2A federation conversations use constitutional envelopes (T2)

When agents talk to agents (not just arifOS calling one organ), the same envelopes ride along. The 13 constitutional laws from `/root/AAA/canon/13-CONSTITUTIONAL-LAWS.md` govern each hop.

Implementation: extend the existing MCP wire to carry envelope headers (MCP 2026-07-28 already supports this).

### Step 3: Authority delegation chain (T3 — F13 binary)

The biggest gain. Once authority envelopes flow:
- Arif says "process this FOIA request end-to-end" (intent + scope)
- arifOS routes to HERMES for claim validation
- HERMES delegates to GEOX for context verification
- GEOX delegates to WEALTH for cost analysis
- All without Arif copying anything
- All receipts back to arifOS in one chain
- One verdict at the end: SEAL or HOLD

**Time to implement:** 1-2 days of arifOS kernel work + ½ day of agent integration + F13 binary to activate.

---

## The receipt template (what "no copy-paste" looks like in practice)

Before:

```
Arif: (reads GEOX output)
Arif: (copies 3 paragraphs)
Arif: (switches to Kimi)
Arif: (pastes)
Arif: (adds "verify this against WEALTH cost")
Kimi: (re-reads, doesn't know what was verified before)
Kimi: (asks Arif for context)
Arif: (re-explains)
```

After:

```
Arif: "GEOX, validate this. WEALTH, ground-truth the cost. ARIFOS, route."
        ↓ intent + authority envelope
arifOS: routes to GEOX with conversation_state_ref
        ↓ capability + provenance envelope
GEOX: validates, emits artifact_id=v_seismic_2026_09_21_001
        ↓ routes to WEALTH with reference to v_seismic_2026_09_21_001
WEALTH: grounds, emits artifact_id=v_cost_2026_09_21_001
        ↓ routes back to arifOS
arifOS: merges, presents to Arif
        ONE message, ONE verdict, all receipts in VAULT999
```

Arif sees:
```
VERDICT: SEAL
  GEOX validation: v_seismic_2026_09_21_001
  WEALTH cost:    v_cost_2026_09_21_001
  Receipts: /root/VAULT999/RECEIPTS/2026-09-21-foia-{hash}.jsonl
```

Zero copy-paste. Zero context reconstruction. Zero "where did this come from?".

---

## Quick verification — is the federation ready for this?

The user's three-tier canon state right now:

```
fed-001: HISTORICAL ARTIFACT (was active canon at 02:15 MYT)
fed-002: INVALIDATED_BY_DRIFT (Q_during violated)
ACTIVE:  (none — CanonicalEligible = false)
```

**The federation is stable enough to OBSERVE but not yet stable enough to CANONIZE.** This is the architecturally correct state. But it means: until quiet interval ≥ 1h + A-FORGE /health gap closed, the foundation for agent-to-agent state-carrying conversations is incomplete.

**What this means for the user:**
- Today: agents can already route, observe, and remember. The remaining friction is the constitutional envelopes (Step 1 + Step 2 above).
- After Step 1 (½ day work): arifOS-mediated calls carry envelopes. Arif no longer re-explains context to organs.
- After Step 2 (1 day): agents can talk to agents. Arif becomes intent-setter only.
- After Step 3 (F13 binary): authority delegation. Agents do multi-step work without per-step confirmation.

---

## The honest answer to "how do I never copy-paste between agents"

You build the constitutional layer above A2A. The substrate for it exists:
- Federation identity (G0c) — agents know what version is running
- Verifier — drift is caught automatically
- Quiet detector — substrate state is observed, not judged
- Surface contracts — every organ declares its surface
- Epoch-binding — canon dies when reality moves

What remains: wire constitutional envelopes into arif_route and the MCP wire, then activate authority delegation.

**When F13 authorizes Step 3, you will write intent once and never copy-paste again. The state carries itself. The meaning stays yours.**

⚒️ DITEMPA BUKAN DIBERI
