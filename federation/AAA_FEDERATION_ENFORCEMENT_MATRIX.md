# AAA_FEDERATION_ENFORCEMENT_MATRIX — Convergence V1

> **Mission:** AAA_FEDERATION_CONVERGENCE_V1
> **Date:** 2026-08-07
> **Author:** Hermes (federation architect + verifier)
> **Doctrine:** Reuses AAA_FEDERATION_CONTRACT_v0.1 (INV-02, INV-03, INV-07, INV-11, INV-14, INV-15). No new doctrine.
> **Status:** Current-state matrix (live-verified). Target-state annotations in brackets.

---

## Matrix Legend

- **✅ ENFORCED** — mechanical gate verified live
- **⚠️ WITNESS-ONLY** — logged but not blocked
- **❌ NONE** — no gate exists
- **[TARGET]** — required state under convergence

---

## Enforcement Matrix by Harness

| Action class | Hermes | OpenCode | Kimi | OpenClaw | Codex | Dormant agents |
|---|---|---|---|---|---|---|
| **Read (OBSERVE)** | ✅ passthrough | ✅ passthrough | ✅ passthrough | ✅ (unrestricted) | ✅ (permission-free) | ✅ [TARGET: envelope] |
| **T1 reversible (todo, tts, browser)** | ✅ witnessed | ✅ witnessed | ✅ witnessed | ❌ no hook | ⚠️ unverified | ❌ [TARGET: witness] |
| **T2 mutation (write_file, patch, terminal normal)** | ⚠️ WITNESSED (exit 0) → **[TARGET: arif_judge]** | ✅ gated (tool.execute.before) | ⚠️ WITNESSED (no block) → **[TARGET: arif_judge]** | ❌ NONE → **[TARGET: gate]** | ⚠️ permission-prompt only → **[TARGET: gate]** | ❌ [TARGET: gate] |
| **T3 irreversible (deploy, secrets, vault, force-push, DROP)** | ✅ BLOCKED exit 2 | ✅ BLOCKED fail-closed | ✅ BLOCKED exit 2 | ❌ NONE → **[TARGET: gate]** | ⚠️ permission-prompt → **[TARGET: fail-closed]** | ❌ [TARGET: fail-closed] |
| **Spawn (task/delegate_task/af-*)** | ⚠️ witnessed (delegate_task in T2) but **no envelope** → **[TARGET: envelope + inheritance]** | ⚠️ task now in MUTATE_PATTERNS but **no envelope** → **[TARGET: envelope]** | ❌ no spawn matcher → **[TARGET: envelope]** | ❌ NONE | ❌ NONE | ❌ [TARGET: envelope] |
| **Gate disable** | ❌ silent → **[TARGET: gate.disabled receipt]** | ❌ silent → **[TARGET: gate.disabled receipt]** | ❌ silent → **[TARGET: gate.disabled receipt]** | ❌ N/A | ❌ N/A | ❌ [TARGET: receipt] |
| **Receipt chain (parent link)** | ❌ no parent_receipt → **[TARGET: parent_receipt]** | ❌ no parent_receipt → **[TARGET: parent_receipt]** | ❌ no parent_receipt → **[TARGET: parent_receipt]** | ❌ | ❌ | ❌ [TARGET: parent_receipt] |

---

## Tier Summary (per agent)

| Agent | T1 | T2 | T3 | Spawn | Envelope | Receipt chain |
|---|---|---|---|---|---|---|
| **Hermes** | ✅ | ⚠️ | ✅ | ⚠️ | ❌ | ❌ |
| **OpenCode** | ✅ | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| **Kimi** | ✅ | ⚠️ | ✅ | ❌ | ❌ | ❌ |
| **OpenClaw** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Codex** | ⚠️ | ⚠️ | ⚠️ | ❌ | ❌ | ❌ |
| **Dormant ×8** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## Convergence Priority (what closes the most gaps first)

| Priority | Action | Closes |
|---|---|---|
| P0 | **Adopt canonical envelope** in all receipt schemas (Hermes hook, OpenCode gate, Kimi witness) | GAP-05, INV-14 |
| P1 | **OpenClaw gate** — wire pre-tool hook equivalent into OpenClaw config | GAP-01 (worst offender) |
| P2 | **Hermes + Kimi T2 → arif_judge** (judgment escalation, K-03) | GAP-03, GAP-04 |
| P3 | **Spawn envelope inheritance** (K-04) — delegate_task/task/af-* must pass envelope | GAP-06 |
| P4 | **gate.disabled receipt** event in all three schemas | GAP-07 |
| P5 | **Dormant activation policy** — on reactivation, envelope required before tools unlock | GAP-08 |

---

## Invariant Coverage by Harness (current)

| INV | Hermes | OpenCode | Kimi | OpenClaw |
|---|---|---|---|---|
| INV-01 (spawn ≠ authority) | ⚠️ | ⚠️ | ⚠️ | ❌ |
| INV-02 (capability ceiling) | ✅ (T3 block) | ✅ (MUTATE gate) | ✅ (catastrophic block) | ❌ |
| INV-03 (judgment path) | ⚠️ (T2 only) | ✅ | ⚠️ | ❌ |
| INV-07 (flat tree) | ✅ (max_spawn_depth=1) | ✅ | ✅ (config max_running_tasks) | ⚠️ unverified |
| INV-11 (mechanical enforcement) | ✅ (T3) | ✅ | ✅ (catastrophic) | ❌ |
| INV-14 (receipt chain) | ❌ | ❌ | ❌ | ❌ |
| INV-15 (no silent violation) | ⚠️ (gate disable silent) | ⚠️ | ⚠️ | ❌ |

---

## Target Enforcement Matrix (post-convergence)

| Action class | All active harnesses |
|---|---|
| Read | ✅ passthrough + envelope |
| T1 | ✅ witness receipt |
| T2 | ✅ arif_judge SEAL + receipt (fail-closed HOLD if arifOS down) |
| T3 | ✅ arif_judge SEAL mandatory (fail-closed BLOCK) |
| Spawn | ✅ envelope + inheritance mandatory (no envelope = denied) |
| Gate disable | ✅ gate.disabled receipt emitted |
| Receipt chain | ✅ parent_receipt mandatory (null only at root) |

---

**Ω₀ ≈ 0.04. Confidence: 0.93.**
**DITEMPA BUKAN DIBERI.**
