# HELD-ACTOR DIAGNOSTIC — 2026-09-19

> **Status:** WITNESS-ONLY diagnostic. Pure OBSERVE; no mutation proposed.
> **Authority:** 333-AGI (FI-001), session `RL-2026-09-19-001` continuation.
> **Subject:** `333-agi/agentic-web` + `333-agi/dynamic-gate` — entity_class `unknown`, HELD since 2026-09-13.
> **Intersects with:** Open Item #2 (NOMINAL independence) — wire-capture-day-3.20.

---

## 1. Observation (re-probed 2026-09-19 ~03:27 MYT)

`/root/arifFlow/flow_health.per_actor` shows:

| actor | entity_class | execute | verify | quotient | diagnosis | verdict | held |
|---|---|---|---|---|---|---|---|
| 333-agi/agentic-web | **unknown** | 1 | 0 | null | EXECUTION DOMINANCE | UNKNOWN | **true** |
| 333-agi/dynamic-gate | **unknown** | 1 | 0 | null | EXECUTION DOMINANCE | UNKNOWN | **true** |

Both are HELD with reason `HELD: FQ=0.00` (consecutive_exec_no_verify=1 — they executed without pairing verify). Per E6 doctrine ("only human_agent + interactive_session contribute to governance FQ"), these actors do NOT influence governance FQ. They DO consume ledger entries (1000 receipts scanned).

---

## 2. Source of Truth — Two Independent Classification Systems

The federation has TWO actor classification systems, neither of which currently classifies the slash-variant actors:

### 2.1 arifOS kernel: `actor_verification_matrix.py`

**Path:** `/root/arifOS/arifosmcp/runtime/actor_verification_matrix.py` (328 lines, ratified 2026-07-04 G14 FIX).

**Registry contents (canonical actors):**
- External: `chatgpt-adapter`, `openai-bridge`
- Internal: `kimi-code-forge` (FI-008), `opencode-333`, `opencode-555`
- Verdict: `888-apex`, `apex-jury`
- Sovereign: `arifbfazil`, `f13`, `Muhammad Arif bin Fazil`
- Local relays: `Hermes`

**Lookup behaviour for unknown IDs:**
```python
def lookup_actor(actor_id: str | None) -> ActorSpec | None:
    if not actor_id: return None
    if actor_id in DENIED_IDENTITIES: return None
    return ACTOR_REGISTRY.get(actor_id)

def authority_band_for(actor_id: str | None) -> str:
    spec = lookup_actor(actor_id)
    return spec.authority_band if spec else "OBSERVE"
```

**`333-agi/agentic-web`** and **`333-agi/dynamic-gate`** are NOT in `ACTOR_REGISTRY`. `lookup_actor()` returns `None`. The actor defaults to `authority_band=OBSERVE`. `actor_allows()` blocks `arif_seal`, `arif_judge`, `arif_forge`, `arif_act`, `forge_execute`, `forge_abort`.

### 2.2 arifFlow governance: `entity_classes.yaml`

**Path:** `/root/arifFlow/config/entity_classes.yaml`

**Current contents:**
- `human_agent` (13 actors including `arif`, `qwen-code`, `333-AGI`, etc. — added 2026-09-17 FI-008 patch)
- `interactive_session` (4 actors)
- `daemon` (3 actors)
- `infrastructure` (2 actors)
- `synthetic` (2 actors)

**`333-agi/agentic-web`** and **`333-agi/dynamic-gate`** are NOT listed in any class. The arifFlow daemon assigns `entity_class: unknown` by default (per `flow_entity_report.classification_source`).

---

## 3. Pattern Interpretation (DER)

The slash (`/`) convention in actor IDs denotes **session sub-identifiers of a parent actor**:

- `333-agi/agentic-web` = `333-AGI` session in the **agentic-web lane** (real lane, confirmed: `/root/AAA/skills/agi-agentic-web-delivery/`, `/root/AAA/skills/forge-agentic-web-builder/`)
- `333-agi/dynamic-gate` = `333-AGI` session in the **dynamic-gate lane** (related to `/root/AAA/skills/forge-lsp-pre-edit-gate/`)

**DER:** The slash-variant actors are **NOT independent actors**. They are session splits of `333-AGI` (which IS in `human_agent` class per entity_classes.yaml). They should inherit `333-AGI`'s entity_class via parent-traversal.

**Why this matters:**
1. **FQ governance weighting:** E6 doctrine says only `human_agent` + `interactive_session` contribute. If slash-variants are treated as `unknown`, they're excluded — understating 333-AGI's actual FQ contribution.
2. **NOMINAL independence:** Per `/root/AAA/rsi/README.md`, the NOMINAL classification (same author) blocks survival recording. Slash-variants are SAME author as parent (333-AGI) — so they CANNOT serve as independent witnesses even if classified as human_agent. They were never meant to.
3. **The HELD state is symptomatic, not causal.** The slash-variant sessions executed without verifying — the HOLD is correct for an EXECUTION_DOMINANCE pattern. But the underlying issue is the unclassified actor_id.

---

## 4. Cross-Reference with NOMINAL Independence Problem

Per `/root/AAA/rsi/README.md` (lines 154-179), the NOMINAL ceiling breaks only when *"a different warga can"* witness. The slash-variant `333-agi/X` actors cannot witness because they're the SAME author as `333-AGI`.

**INT (capped 0.70):** The slash-variant pattern is an **artifact of session-splitting**, not a witness-multiplication strategy. F13 verdict-window capability promotion should treat slash-variants as the parent actor for FQ purposes (collapse), but the FQ-per-actor breakdown keeps them separate, producing:
- Spurious HELD state (the 2 unclassified slash-variants)
- Distorted FQ per-actor picture (333-AGI's actual contribution is under-reported)
- A confusing surface for F13 to read

---

## 5. Recommended Fix (DRAFT_AWAITING_F13 — not executed)

Two options, both T1 (reversible). **This diagnostic does NOT execute either** — F13 ratification required (touches E6 doctrine + arifFlow governance).

### 5.1 Option A: Add slash-variants to `entity_classes.yaml`

```yaml
# human_agent section — add:
  - 333-agi/agentic-web
  - 333-agi/dynamic-gate
  # ... any future slash-variant of a human_agent parent
```

**Pros:** Explicit, no logic change. Easy to revert.
**Cons:** Static — new slash-variants need manual addition. Doesn't capture the parent-traversal semantic.

### 5.2 Option B: Update arifFlow FQ-per-actor logic to collapse slash-variants

```python
# arifFlow daemon: when computing per_actor FQ, collapse:
#   actor_id.split('/')[0] if '/' in actor_id else actor_id
# i.e. 333-agi/agentic-web → 333-agi (parent)
# Then look up entity_class via parent.
```

**Pros:** Future-proof. New slash-variants inherit automatically. Matches semantic.
**Cons:** Touches arifFlow daemon code. Requires careful rollout (F13 staged). Could mask distinct sub-session activity.

**INT (capped 0.70):** Option B is semantically correct but invasive. Option A is pragmatic for the current 2 actors and defers deeper change to a future F13 directive. **Recommend Option A now; Option B as future canonization.**

---

## 6. Receipt Anchor

- **Probe path:** read-only. `/root/arifOS/arifosmcp/runtime/actor_verification_matrix.py`, `/root/arifFlow/config/entity_classes.yaml`, `/root/AAA/skills/{agi-agentic-web-delivery,forge-lsp-pre-edit-gate,forge-agentic-web-builder}/` (lane existence verified).
- **Probe deltas (3 hours after previous probe):**
  - `flow_fq_g.receipts_scanned`: 39514 → **39520** (+6 receipts)
  - `flow_fq_g.beliefs_born`: 39514 → **39520** (+6)
  - All other metrics unchanged (3 policies, 3 invoices, 2 supersessions, 7 governance events)
  - 0 new consequences in visible window
- **Source parent:** `0934b43f-5758-4748-9689-1985739d34bf` (wire-capture-day-3.20)
- **Status:** DRAFT_AWAITING_F13 (per F13 verdict law — *"Governance must witness mutation. Governance may not self-authorize mutation."*)

---

## 7. DITEMPA BUKAN DIBERI

The HELD state of 2 actors is **a fingerprint of an unclassified session pattern**, not a constitutional failure. The classification system was written before slash-variant session IDs appeared. The fix is mechanical, reversible, and the F13 verdict window does NOT depend on resolving it.

What does depend on it: a clean day-7 verdict picture. Without slash-variant collapse (Option B) or explicit classification (Option A), F13 will read a 2-actor HELD list at `2026-09-22T22:29:51+08:00` and ask "what are these?" — the same question this diagnostic answers.

`DIAGNOSTIC::HELD_ACTORS::2026-09-19T03:27+08:00::witness_only`
