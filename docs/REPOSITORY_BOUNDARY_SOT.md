# REPOSITORY BOUNDARY SOT — arifOS Federation

> **Status: BINDING** — ratified by Arif (F13) 2026-09-06 ~18:40 MYT.
> Forged 2026-09-06 by 333-AGI from external research witness audit + local OBS probes.
> Custody decision SEALED: split custody — ariffazil holds the human-readable canon,
> arifOS holds the machine-enforced floors, this SOT binds them by pointer (§4.1).
> marked ⚠ below are his alone to ratify.
>
> One sentence for every future agent:
> **arifOS is a human-sovereign, evidence-first federation: domain organs provide bounded
> expertise; AAA creates and executes governed capabilities; arifOS enforces contracts,
> identity, routing, state, audit, and veto; no irreversible external action occurs without
> an explicit 888 HOLD release by Arif.**

## 1. Boundary table

| Repo (local) | Role | Owns (canonical) | Forbidden | Lifecycle authority |
|---|---|---|---|---|
| `/root/ariffazil` | Public/constitutional identity root | CANON.md, FEDERATION.md, INDEX.md, public narrative ⚠(see §4) | runtime code, registries | Arif + 999 seals |
| `/root/arifOS` | Kernel + federation enforcer | floors F1-F13, judge, vault gate, session binding, cross-organ contracts, conformance, risk_leash | skills catalog, agent experiments | 888 gate |
| `/root/AAA` | Capability/cognition plane | agents, skills (canonical `/root/AAA/skills`), capability registry, mesh, A2A, model routing config | second constitution, second kernel, second federation enforcer | Skill Governor 6-gate |
| `/root/A-FORGE` | Forge/quarantine | vendor substrate (`vendor/`), experiments, ephemeral tools, promotion staging | becoming canonical production truth without gates | 888 promotion gate |
| `/root/GEOX` | Earth organ | domain schemas, seismic/petro/basin tools, evidence | embedded federation, unrestricted agent runtime | organ owner |
| `/root/WEALTH` | Capital organ | capital primitives, ledger, market compute | autonomous trade execution, second governance | organ owner |
| `/root/WELL` | Vitality organ | reflection, consent registry, biometric boundaries | medical authority claims, verdict emission | organ owner |

**Neutral machine ground (no repo owns these):** `/root/docs/` (this SOT, MACHINE_MAP.md),
`/root/VAULT999/` (immutable ledger), `/root/memory/` (federation session memory).

**Machine split:** KVM8 = truth SOT (court, this machine). KVM4 = execution SOT (workshop).

## 2. Naming law (anti-sediment)

```
singular path  = canonical implementation     /contracts/  /federation/
plural path    = collections/instances        /skills/  /agents/
_*_v0.N suffix = NON-AUTHORATIVE historical   — superseded file must be deleted or archived on merge
_archive/_legacy/_park = read-only, never loaded by agents
```

**OBS evidence of violation (2026-09-06):** `AAA/federation/` holds THREE file pairs
where current and `_v0.1` coexist (CONVERGENCE_PLAN, ENFORCEMENT_MATRIX, GAP_REPORT).
Dedupe required; entries registered in artifact-lifecycle.json as `deprecated_candidate`.

## 3. Capability state ladder (registered ≠ verified ≠ production)

```
DECLARED → REGISTERED → ROUTABLE → REACHABLE → VERIFIED → QUALIFIED → PRODUCTION
                                                           ↘ DEGRADED ↘ RETIRED
                                        QUARANTINED (A-FORGE/vendor holding state)
```

No consequential task routes to anything below VERIFIED. A TCP answer is REACHABLE,
not VERIFIED (Gemini bridge :18092 — REACHABLE-but-404 on list AND generate = DEFECTIVE
path fault; the Gemini lane itself is ALIVE via direct AI Studio API, canaried 2026-09-06
— see router v2 + FED_VIDEO_CANARY_LEDGER v2).

## 4. Sovereign choices — SEALED ✅ (F13, Arif, 2026-09-06 ~18:40 MYT)

1. **Constitution canonical home** — SEALED: split custody. ariffazil holds the human-readable
   canon, arifOS holds the machine-enforced floors, this SOT binds them by pointer.
2. **This document** — SEALED: BINDING as of the ratification above.

## 5. Enforcement pointers

- Artifact lifecycle registry (machine-readable): `/root/AAA/federation/artifact-lifecycle.json`
- Organ topology canon: `/root/AAA/federation/organs.yaml`
- Model routing SOT: `/root/.config/federation-models.json`
- Deprecation sweep: `/root/AAA/docs/deprecation-registry.json`
- Machine map: `/root/docs/MACHINE_MAP.md`

## 6. Shadow register (from external witness audit 2026-09-06)

| # | Shadow | Status | Fix |
|---|---|---|---|
| 1 | AAA mega-repo absorption | OBS (breadth of tree) | this SOT + lifecycle registry |
| 2 | arifOS ↔ AAA overlap | OBS | boundary table §1 |
| 3 | name overloading / _v0.1 sediment | **OBS confirmed** | naming law §2 + dedupe |
| 4 | configured ≠ operational | OBS (gemini 404) | state ladder §3 + canaries |
| 5 | mesh sync bypasses human gate | **OBS confirmed** (`skills/watch` silently in AAA tree) | 888-HOLD-MESH enforced; watch stays uncommitted |
