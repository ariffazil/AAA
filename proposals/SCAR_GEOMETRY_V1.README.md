# /root/AAA/proposals/ — SCAR_GEOMETRY_V1 (CORRECTED INDEX)

**Status:** SEAL_PROPOSED (conceptual) · HOLD (runtime) · executable: false · 2026-10-10 · kimi-code/FI-008

---

## Correction of record (important)

A first draft `SCAR_GEOMETRY_V1.yaml` was written here **from the F13 chat relay, before the source artifact was found**. It was a **duplicate** and has been **withdrawn (deleted)**.

**The canonical artifact already exists:**

| Artifact | Owner | Role |
|----------|-------|------|
| `/root/HAMPA/SCAR_GEOMETRY_V1.yaml` | HERMES (A2H) | **canonical** 99-slot map |
| `/root/HAMPA/SCAR-MAP-99-v1.yaml` | HERMES | map v1 |
| `/root/.hermes/cache/scratch/build_scar_geometry.py` | — | the generator (source of truth) |
| `/root/.hermes/cache/scratch/scar-map-99.html`, `peta-scar-arif.html`, `peta-luka.typ` | — | readable sources |

**This directory now holds only the genuinely additive piece:**

```
SCAR_GEOMETRY_V1-composition-overlay.yaml   ← crosswalk + anti-duplication audit
```

## What the overlay adds (that the canonical lacks)

1. **Provenance resolution** — the two F13 relays disagreed on law numbering; the *source* settles it: **nodes 13/23/25 = relay-1** (`kerap diulang…`, `peta lama menipu`, `nampak hidup bukan boleh kerja`). Relay-2's law numbering was wrong.
2. **`canon_alignment`** — the 7 existing owners (F1–F13, 7 Machine Laws, 13 Constitutional Laws, Shadow Paradoxes S₁–S₁₃, Scar-Authority, Scar-Binding, W_scar).
3. **`duplication_flags` (12)** — e.g. L10≡MachineLaw#5, L22≡MachineLaw#3, L28≡MachineLaw#4, P53≡S₁₂, P57≡S₇, P72≡ConstLaw#5.
4. **`ontology_hazards` (3)** — chiefly: **four+ coexisting scar-numbering systems** (`P99:` vs `AAA:scar-00n` vs `NAME:` vs `HAMPA:`). Every scar citation must carry its namespace.
5. **`canon_0_gate`** — PASS as overlay, FAIL as a new registry.

## The lesson (an agent scar)

> Compiling an artifact from a sovereign *relay* before probing for the *source* produced a duplicate of existing canon. **Probe for the source artifact first.** The canonical HAMPA artifact had already handled provenance correctly (its HTML §Pembetulan, C1/C2/C3).

## Verification

```
overlay YAML parses: OK · owner_of_slots = /root/HAMPA/SCAR_GEOMETRY_V1.yaml
duplication_flags: 12 · ontology_hazards: 3 · executable: false
canonical /root/HAMPA/SCAR_GEOMETRY_V1.yaml: intact
```

**Verdict: SEAL_PROPOSED / HOLD.** Accept the overlay (or fold it into the HAMPA canonical as a §Crosswalk), set a scar-namespace convention, and keep runtime wiring HOLD until SCAR-BINDING Phase B.

*DITEMPA BUKAN DIBERI.*
