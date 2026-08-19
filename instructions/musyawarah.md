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
