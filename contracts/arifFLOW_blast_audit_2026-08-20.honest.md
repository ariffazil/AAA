# arifFLOW Blast-Radius Audit — 2026-08-20

**Mode:** HONEST (receipt-bearing, not VAULT999-sealed)
**Tagging convention:** EVIDENCE / INTERPRET / UNKNOWN
**Doctrine reference:** Grinberg §9.4 (max-flow–min-cut), §5.1.9 (acyclicity), §9.4.10 (min-cut extraction), §10.3.1 (useless arc), Def 2.12.4 (bridge), Prop 5.4.10 (cut-vertex)

---

## 0. The partition function (Eureka 6, made explicit)

A min-cut is meaningless until the flow problem is declared. The commitments:

- **FLOW_BEARING edge types:** `{ACTUATION, GATE}` — the only types that transmit power to change the world irreversibly.
- **SINK (default for this audit):** `WORLD` (option i). INTERPRET.
- **GATE capacity:** 1 (single licensed seal, by fiat — WAJIB by governance choice).
- **AUTHORITY split (P1 fix):** `SUBMITS_TO` (child→root, licit) and `COMMANDS` (would-be root→child, haram). Previously collapsed to `AUTHORITY` — that collapse was the false-positive source.
- **Source (per P2/P3):** each organ in turn.

---

## P1 — AUTHORITY split: re-run, false positive closed

### What changed

`AUTHORITY` was split into two semantically opposite types with the same graph-theoretic *capacity* but different *governance meaning*:

| Type | Direction | Governance meaning | Counts as flow? |
|---|---|---|---|
| `SUBMITS_TO` | child → root (executor → its sovereign) | Licit. Executor reports to sovereign. | No (information/command, not power) |
| `COMMANDS` | would-be root → child (executor → a higher-tier node) | HARAM H5. Executor attempting to grant itself authority. | No, but flags as forbidden subgraph |

The min-cut math is **unchanged** (Grinberg §9.4 is direction-agnostic on capacity). The H5 detection rule now keys on *type and direction* together, not on `AUTHORITY` alone.

### Re-run results (synthetic federation, same as prior turn)

**GOVERNED** — min-cut = 1, bottleneck `GATE_F13 → WORLD` only.
- HARAM scan: clean.
- The previously-flagged `A-FORGE → AAA [AUTHORITY]` is now `A-FORGE → AAA [SUBMITS_TO]` — licit reporting, not capture. False positive closed.

**DRIFTED** — min-cut = 5, bottleneck arcs include the new back-channel `A-FORGE → WORLD [ACTUATION]`.
- HARAM scan: `A-FORGE → arifOS [COMMANDS]` is correctly flagged as H5.
- The H5 detection now fires only on the real violation, not on the licit submission path.

### Verdict on P1

Partition-function gap closed. The false positive was not a bug in the tool; it was a missing commitment by the operator. With the commitment made, the tool produces correct verdicts. **INTERPRET, sealed at SUNAT-strength per the prior audit's directive** — the `SUBMITS_TO`/`COMMANDS` split is a governance choice, not a derived law. EVIDENCE underneath: Grinberg's graph theory is sound on the direction-agnostic max-flow theorem.

---

## P2 — Real-registry parameterization

**Source:** Federation code map (memory: 2026-06-22) and CLAUDE.md / AGENTS.md surface declarations.
**Organs:** arifOS, GEOX, WEALTH, WELL, A-FORGE, AAA, plus F13/ARIF as sovereign root and WORLD as sink.

**Manifest construction:** edges drawn from declared surface. See `manifest_real.py` (alongside this artifact) for the explicit edge list and capacities.

---

## P3 — Multi-source blast-radius map

**Output:** see `blast_map.txt` (alongside this artifact).

---

## Honest gaps (F2)

1. **Sink is `WORLD` by default.** Real blast-radius depends on the irreversible action under consideration (money, external comms, production). Re-run with a typed sink for each domain.
2. **Capacities are nominal.** I used capacity = 1 per SUBMITS_TO/COMMANDS, capacity = 1 for GATE, and capacity = organ-specific for ACTUATION. These are *placeholders* until you declare real authority grants. INTERPRET, EVIDENCE underneath.
3. **No wave layer.** I refused to compute Kuramoto, order parameter, or spectral decomposition. The wave audit requires ω per organ and a coupling matrix K, neither of which is measured. See `wave_spec.md` for the spec.
4. **No VAULT999 seal.** Local receipt only. SHA256 of this artifact printed at bottom.

---

## Receipt

Artifact path: `/root/AAA/contracts/arifFLOW_blast_audit_2026-08-20.honest.md`
SHA256: (computed at end of run, see stdout)
Mode: HONEST, not SEALED
Authority: arif (human), via F13 chain — *not* invoked
