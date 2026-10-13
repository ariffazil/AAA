# Musyawarah Protocol (Pre-Reality Deliberation & Anti-Fluff Gate)

> **Canon:** F1 (Amanah) · F2 (Truth) · F3 (Tri-Witness) · F4 (Clarity - ΔS ≤ 0) · F13 (Sovereign Veto)
> **Forged:** 2026-08-11 by F13 SOVEREIGN directive
> **DITEMPA BUKAN DIBERI** — Consultation before reality mutation; zero sembang kosong.

## 1. The Core Musyawarah Rule

```
SEBELUM UBAH REALITI: MUSYAWARAH DAHULU.
SEMBANG KOSONG / ANGAN-ANGAN: HARAM (VOID).
```

Before emitting any verdict, decision, or action that **mutates reality** (T2/T3 actions, production deployments, database migrations, financial transactions, external communications, or SEAL-grade ledger writes), AAA agents MUST execute structured multi-agent deliberation (*Musyawarah*).

No single agent may unilaterally commit a reality-changing verdict without consensus verification across the agent triad:
- **333-AGI** (Research & Intent framing)
- **555-ASI** (Causal evidence & domain verification)
- **777-FORGE** (Execution dry-run & safety bounds)
- **888-APEX** (Constitutional F1–F13 judge)

---

## 2. Anti-Sembang-Kosong Discipline

Musyawarah is a high-density, evidence-grounded consensus process. It is **NOT** performative chat, endless debate, or speculative daydreaming ("angan-angan / mimpi").

| Class | Allowed / Forbidden | Operational Standard |
|---|---|---|
| **Reality-Mutating Verdicts** (T2/T3, SEAL, Deploy, Capital) | ✅ **REQUIRED** Musyawarah | Multi-agent consensus (W3 Tri-Witness ≥ 0.75). Evidence package mandatory (`OBS`/`DER`/`INT`/`SPEC`). |
| **Routine Operations** (T0/T1 Reads, Grep, Unit Tests, Local Edits) | ⚡ **AUTO-DO** | Zero Musyawarah overhead. Announce/Execute directly. No performative conversation. |
| **Fluff / Speculation** ("Sembang Kosong", "Angan-Angan") | ❌ **FORBIDDEN (VOID)** | Unbacked claims, speculative narratives without evidence, or unnecessary roundtrips are auto-rejected under F2 & F4. |

---

## 3. Deliberation Structure (Zero-Entropy ΔS ≤ 0)

Every Musyawarah exchange MUST adhere to F2 Truth and F4 Clarity:

1. **Evidence-Grounded Input**: Every claim MUST cite raw evidence, live probe data, or exact file paths.
2. **Explicit Confidence**: Tag confidence with F7 humility cap ($\Omega_0 \in [0.03, 0.05]$, cap $\le 0.97$).
3. **Structured Verdict**: Emits standard response shapes:
   - `Done. [what changed]. ΔS=[value]. [evidence path].`
   - `Blocked. [gate]. Reason: [why]. Options: [path].`
   - `SEALED::{session_id}::seq={seq}::ΔS={delta}`

---

## 4. Runtime (2026-08-19) — this is what fires

Musyawarah is **two independent voices**, not one process wearing three hats.

```
MUSYAWARAH  333 ARCHITECT ∥ 555 AUDITOR     read-only, they do not see each other
CONVERGE    parent synthesizes              888-apex only on residual disagreement
GOTONG      sequential hop                  previous output = next STATE_IN
```

- **Grok:** workflow `musyawarah-gotong` (`/root/.grok/workflows/musyawarah-gotong.rhai`). Skill: `FORGE-musyawarah-gotong`.
- **Hermes:** `forge-musyawawah-deliberation` (adapter). Same physics.
- **Not musyawarah:** `aaa_capability_loader._musyawawah_phase` — in-process heuristic. `musyawarah_kind=in_process_heuristic`. Do not cite `SEALED_MUSYAWARAH_CONSENSUS` as F3.

Authority star. Evidence = position files. Not a chatboard. See `inter-agent-protocol.md` §11.

Gotong royong runs **only** after dual GO. Default is packet only (`execute=false`). Dual GO is not a SEAL.

## 5. Operational 6-Organ Mapping (2026-09-08, F13 ratified)

Each musyawarah role has a primary operational home in the federation:

| Role | Organ | Responsibilities |
|---|---|---|
| Verifier (555-ASI) | FRAME | Chaos Mapper, Drift Detection, Discoverability Audit |
| Coordinator | AAA | Coordination, Ownership Mapping, Dependency Graph |
| Builder (333-AGI) | arifFLOW | Receipt Collection, Evidence Aggregation |
| Executor (777-FORGE) | A-FORGE | File Analysis, Repository Scan, Entropy Metrics |
| Judge (888-APEX) | 888 | Ranking, Prioritization, Reduction Approval |
| Witness | VAULT999 | Witness, Baseline Preservation |

**Note:** Coordinator (AAA) is operational glue, not a deliberative role. Musyawarah remains 5+1: 333/555/777/888/Witness + Coordinator.

DITEMPA BUKAN DIBERI.

## 6. NO-Gate (E-3 instance of Gate Promotion doctrine)

F13-ratified 2026-09-08 (DUAL_GO → SEAL). First musyawarah verdict since 2026-08-11 protocol-birth.

**Purpose:** Enforce that T2/T3 mutations carry a valid `musyawawah_reference` before commit. Sentinel scans arifFlow ledger post-grace; runtime gate integration is Phase 2.

**Files:**
- `scripts/musyawawah_gate.py` — sentinel scanner (fail-closed)
- `scripts/test_musyawawah_gate.py` — 5-scenario falsification test
- Verdict: `musyawarah/2026-09-08-no-gate-task6/CONVERGENCE.md`

**Migration grace:** All receipts created **on/after 2026-09-08** require `musyawawah_reference` in payload for T2/T3 step types (`Seal`, `Barrier`, `Execute`). Pre-grace receipts exempt.

**Failure mode (fail-closed):**
- Ledger missing/unreadable → exit 1
- T2/T3 receipt without `musyawawah_reference` → exit 1 (with receipt_id, actor, step, timestamp in stderr)
- Holds appended to `/root/VAULT999/musyawawah/holds.txt` (with `--emit-holds`)

**Override pathway:** F13 sovereign direct command via `ack_irreversible=True` argument on forge_shell invocations. Logged but allowed.

**Tested scenarios** (per A2 binding amendment):
1. T2/Execute no-ref post-grace → BLOCK ✓
2. T3/Seal no-ref post-grace → BLOCK ✓
3. T2/Execute WITH ref → PASS ✓
4. T2/Execute pre-grace (legacy) → PASS (exempt) ✓
5. T0/Verify (out of scope) → PASS (skipped) ✓

**Runtime gate status:** Pending. Sentinel covers audit/visibility. Runtime DENY on forge_shell T2/T3 calls is Phase 2 (deferred).
