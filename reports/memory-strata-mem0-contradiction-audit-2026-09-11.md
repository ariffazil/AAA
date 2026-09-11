# AUDIT — Mem0 Contradiction in `institutional-memory-strata.md`

> **Status:** WITNESSED_CONTRADICTION · awaiting F13 correction
> **Auditor:** Hermes (KVM8, gateway runtime)
> **Probed:** 2026-09-11 ~12:1x MYT
> **Class:** Registry override Witness — dalam canon yang di-ratify hari ini
> **Companion doctrine violated:** `institutional-memory-strata.md` (self-referential), `witness-zen-doctrine.md`, Anti-HARAM #1 (Berpura-pura)

---

## The Claim Under Audit

`/root/AAA/instructions/institutional-memory-strata.md` — rendered **2026-09-11 12:10**, marked `F13_RATIFIED_CHAT`, loaded into every agent session via `render-agents.sh`.

Verbatim, section "Witnessed Corrections (live probe 2026-09-11)":

> 1. **"Hermes ada Mem0"** — SALAH. Mem0 REJECTED di intake gate (`ARCHITECTURE_BLUEPRINT_3NODE.md`: *"middleman on a deeper stack"*). `~/.hermes/mem0.json` = remnant, bukan wiring. Semantic recall kanonikal = `arif_memory` + `forge_memory` (Qdrant live 9+ hari).

The fragment asserts this correction was itself "applied after live probe (F2 — witnessed, bukan narrated)."

**It was not. Live probe falsifies it.**

---

## Witness (probe evidence, 2026-09-11)

### W1 — Mem0 is the configured Hermes memory provider

`/root/.hermes/config.yaml`:

```yaml
33:memory:
34-  provider: mem0
```

Not a remnant. The active provider line of the running gateway.

### W2 — The `mem0` Qdrant collection is the largest in the federation

`GET 127.0.0.1:6333/collections` → 17 collections. Point counts:

| Collection | Points | Note |
|---|---|---|
| **mem0** | **11,277** | ← Hermes S3. Largest by 7.7× |
| petronas_knowledge | 1,460 | |
| arifos_precedent | 255 | |
| arifOS_skill_mesh | 191 | |
| arifos_memory | 99 | ← what the fragment names as "canonical" |
| atlas333_eureka | 74 | |
| federation_memory_patterns | 73 | |
| arifos_session_memory | 56 | |
| federation_shared | 30 | |
| arif_evidence | 16 | |
| arifos_constitution | 14 | |
| arifos_vault_canon | 13 | |
| openclaw_memory | 9 | |
| arifos_vault_working | 7 | |
| identity_vault | 2 | |
| arifos_audio_memory | 2 | |
| mem0migrations | 0 | |

Qdrant: docker container, `Up 9 days (healthy)`, bound `127.0.0.1:6333-6334` (LOCALHOST_IS_PASSWORD respected).

The fragment names `arif_memory`/`forge_memory` as the canonical S3 path — **99 points**, against **11,277** in `mem0`. Whatever the *intended* architecture, the *witnessed* architecture runs on Mem0.

### W3 — Read AND write paths exercised live, minutes before the probe

Within the session that produced this audit, Hermes executed against Mem0:

- `mem0_search` × 4 (semantic recall returned ranked results with scores 0.72–0.87)
- `mem0_delete` × 8 — **all returned `{"result": "Memory deleted."}`**

8 mutations succeeded. A remnant cannot accept writes. This is F2-grade evidence: not inferred, executed.

### W4 — The fragment is self-inconsistent

It opens by claiming corrections were "applied after live probe (F2 — witnessed, bukan narrated)", then asserts as witnessed fact something a live probe contradicts. The F2 label is doing rhetorical work the probe did not do.

---

## Why This Matters More Than It Looks

The fragment is **ratified and propagating**. `render-agents.sh` injects it into `AGENTS.md` for every organ — witnessed in `/root/.hermes/AGENTS.md` and `/root/AAA/AGENTS.md` fragment tables (both list it `F13_RATIFIED_CHAT (2026-09-11)`).

Consequences already live:

1. **Every agent booting today is told Hermes has no Mem0.** Agents that trust canon will route around the actual S3 backend and conclude Hermes recall is unavailable.
2. **The "Corrected Harness Matrix" rests on the false premise.** Its central distinction — *"Beza Hermes vs coding agents bukan akses — reflex default"* — was derived partly from "Mem0 rejected." If Mem0 is live, the Hermes/coding-agent difference is partly an **access** difference too, not purely reflex. The matrix needs re-derivation, not just re-labelling.
3. **It violates the doctrine it sits beside.** `memory-promotion-gate.md` (rendered 12:04, six minutes earlier) requires evidence before promotion. This fragment promoted a falsified claim to ratified canon.
4. **It is exactly the wallet failure, instantiated.** Registry says Mem0 is a remnant. Witness says 11,277 points and 8 successful deletes. Registry is overriding Witness inside ratified canon.

---

## Boundary — What This Audit Does NOT Do

This note does **not** amend the fragment. `institutional-memory-strata.md` carries `F13_RATIFIED_CHAT`. Amending ratified canon is F13 SOVEREIGN authority, not auditor authority — **Actor ≠ Authorizer** (Anti-HARAM #4, Authority Drift).

Hermes wrote evidence. Arif decides correction.

---

## Proposed Correction (for F13, reversible, one patch)

Replace claim #1 with the witnessed state:

> 1. **"Hermes semantic recall = arif_memory only"** — SALAH. Witnessed 2026-09-11: `/root/.hermes/config.yaml` L33-34 `memory: provider: mem0`; Qdrant collection `mem0` = 11,277 points (largest in federation vs `arifos_memory` 99); read + write paths exercised live in-session (4× search, 8× delete succeeded). Mem0 is the **live** Hermes S3 backend, not a remnant. `ARCHITECTURE_BLUEPRINT_3NODE.md` rejection is **intent** (Registry), not **runtime** (Witness) — the gap between them is unbuilt work, not a settled fact.

And add, so the gap stops being re-litigated:

> **Open loop:** Mem0 (Hermes S3, 11k points) and `arif_memory`/`forge_memory` (federation S3, 99 points) are two parallel semantic stores with no reconciliation path. Decide: converge, or declare Mem0 Hermes-private and stop calling `arif_memory` canonical for Hermes.

---

## Compression

> Canon yang claim "witnessed" tanpa probe ialah Registry menyamar sebagai Witness.
> Ia lebih bahaya daripada Registry yang jujur — sebab ia membawa label F2.

**Test it falsifiably:** `grep -A2 '^memory:' /root/.hermes/config.yaml` + `curl -s 127.0.0.1:6333/collections/mem0 | grep points_count`. Two commands. Either reproduces W1+W2 or refutes this audit.

---

DITEMPA BUKAN DIBERI ⚒️
