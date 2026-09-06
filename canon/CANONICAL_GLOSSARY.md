# CANONICAL GLOSSARY — freeze card

> Load this **before** KAMUS long-form. One object, one canonical name.
> Long lexicon stays `/root/AAA/governance/KAMUS_DEWAN.md` (§1–§12 immutable).
> This page freezes **identities, nodes, organs**. It does not replace Kamus.
> F13 owns Category A. Agents may not mint aliases.
> DITEMPA BUKAN DIBERI · 2026-09-03 · worker COMPLETE ≠ APEX SEAL

**Law:** Naming is the first act of creation. Undifferentiated blob → cannot govern → chaos.
**Order:** Difference → Name → Observation → Model → Action.
**Scar:** Agents treated `KVM8 = KVM4`, `af-forge = kernel`, `arifOS = federation = kernel`. That was ontology corruption, not a typo.

Write **canonical (alias)** never alias alone.

---

## IDENTITIES (Category A — human-held)

| Canonical | Is | Is not |
|---|---|---|
| **ARIF** | Human sovereign (F13) | An agent, a node, a bot |
| **arifOS Federation** | The organism (all organs + nodes) | The kernel process |
| **arifOS Kernel** | Constitutional judge `:8088` | The federation; AAA; a VPS |

Deprecated as standalone: `arifOS` with no qualifier. Say **Kernel** or **Federation**.

```
ARIF
  └── arifOS Federation
        ├── arifOS Kernel     (judge)
        ├── AAA               (cockpit / register)
        ├── A-FORGE           (execute)
        ├── arifFLOW          (metabolize)
        ├── VAULT999          (append / witness)
        ├── WELL GEOX WEALTH  (domain reality)
        ├── HERMES            (route / sense-bridge)
        ├── FED               (route models)
        └── ~~FLAME~~         (RETIRED 2026-09-04 → FED flash lane)
```

---

## NODES — freeze (one ID, aliases in parentheses)

| Canonical | Friendly | Node name | VPS | Plane | Never |
|---|---|---|---|---|---|
| **KVM8 (forge)** | forge | forge | 1325122 | Forge / survive | A-FORGE = organ (caps+dash), never the machine. forge_work = sketchpad. |
| **KVM4 (workshop)** | workshop | srv1946043 | 1946043 | Workshop / explore | kvm4-forge = ssh alias (kept). forge-core label retired 2026-09-04. Not forge. |
| **KVM2 (witness)** | witness | azwaos | 1642546 | Witness | Live hostname `flow-edge` is an alias, not a fourth node. OpenClaw home. Do not kill Azwa Hermes (different bot). |

Always: `KVM8 (forge)` — forge is the machine; A-FORGE is the organ. Never confuse.

> **Disambiguation (ratified 2026-09-04, F13 "execute all"):** forge = machine KVM8 (hostname truth) · A-FORGE = execution organ (caps+dash) · forge-core = retired → workshop (KVM4) · forge_work = sketchpad (untouched) · azwaos = witness (KVM2).

---

## PATHS — one path per organ (do not hardcode) — ratified 2026-09-04

**Law:** No `sys.path.insert("/root/...")` in runtime code. Resolve through `paths_resolver.org_path(name)`.

| Organ | Canonical path | Source of truth |
|---|---|---|
| A-FORGE | `/root/A-FORGE` | paths_resolver.CANON_ORG_PATHS |
| arifOS (Kernel source) | `/root/arifOS` | paths_resolver.CANON_ORG_PATHS |
| arifOS (Runtime deploy) | `/opt/arifos` | paths_resolver.CANON_ORG_PATHS |
| AAA | `/root/AAA` | paths_resolver.CANON_ORG_PATHS |
| GEOX | `/root/GEOX` (alias `/opt/geox`) | paths_resolver.CANON_ORG_PATHS |
| WEALTH | `/root/WEALTH` (alias `/opt/wealth`) | paths_resolver.CANON_ORG_PATHS |
| WELL | `/root/WELL` (alias `/opt/well`) | paths_resolver.CANON_ORG_PATHS |
| HERMES | `/root/.hermes` (lowercase canon) | paths_resolver.CANON_ORG_PATHS |
| arifFlow | `/root/arifFlow` (alias `/opt/arifflow`) | paths_resolver.CANON_ORG_PATHS |
| VAULT999 | `/root/VAULT999 → /root/arifOS/VAULT999` | paths_resolver.CANON_ORG_PATHS |
| forge_work | `/root/forge_work` (sketchpad, never execute) | paths_resolver.CANON_ORG_PATHS |

**Anti-name-multiplicity canonicals (forged 2026-09-04):**
- **Python runtime:** ONE entry — `/opt/arifos/venv/bin/arifos` is canonical. `/root/venv/bin/arifos*` are symlinks, not duplicates.
- **npm-bin entry:** THREE distinct transports (CLI / Server-legacy-aliased / Stdio-ACT-gated) under ONE package `@ariffazil/a-forge`. Each has a distinct purpose; do not collapse.

**Invariants satisfied by this table:**
- K-1 OBSERVE config-independent (paths derived from disk truth, not config files)
- K-3 Annotations = legibility contract (one name → one path, no alias-only)
- K-8 Migration-as-F1 (additive — to migrate, update this table once)

**Implementation:** `/root/A-FORGE/paradox-engine/paths_resolver.py`
- `org_path(name)` returns first live path (F2 disk probe)
- `audit_federation()` returns health of all organs
- `__main__` runs the audit standalone

---

## ORGANS (one verb each)

| Name | Verb | Must not |
|---|---|---|
| AAA | Register / display | Judge, execute |
| A-FORGE | Execute | Judge, seal |
| arifFLOW | Metabolize (FQ) | Judge, execute |
| VAULT999 | Append | Rewrite |
| WELL | Reflect (human×machine) | Diagnose as verdict, seal |
| WEALTH | Compute capital | Allocate |
| GEOX | Compute earth | Seal geology |
| HERMES | Route / bridge | Judge, seal, dual-poll |
| FED | **Capability Routing Constitution** — Intent classifier (:7074) + 413-clamp middleware (:4010) + provider federation (:4000 litellm). Each constitutional alias answers with ITS declared model_name; silent cross-tier swap is F2/F9 violation. | Own truth |
| FRAME | Measure | Verdict |
| OpenClaw | Encode / sense | Live on KVM8 as home |
| CCC | Build on KVM4 | Spawn on KVM8 |

---

## THEORIES (glossary class 1 — do not rename)

| Name | One line |
|---|---|
| APEX Theory | G=A·P·E·X·Φ. Intelligence = work on contradiction under law. |
| Reality Engineering | Shared world before action. Live probe or UNKNOWN. |
| Theory of Anomalous Contrast (TAC) | Intelligence at Expected ≠ Observed. Operational form of Hang Ingat Balik L4/L5. |
| Hang Ingat Balik | Reality whispers before it shouts. |
| Capability Graph | Who may do what. forge owns. |
| Reality Drift | Two agents, two worlds, same names. |
| Entropy Separation | forge survive / workshop explore. Chaos is placed, not destroyed. |
| P-DIAL | Termination criterion — "Can more evidence still change the decision?" Four closure modes: CONTINUE, ACT, HOLD, SABAR. |
| SABAR | CLOSE mode — reality not yet mature; searching cannot help; world must produce data on its own timeline. Not HOLD. |
| Witness | Fifth coordinate — validates that closure happened at the right place and time. Scar exists when Witness was late. |
| Closure Quality | Not "was the answer correct?" but "was the search stopped at the right moment?" First-class observable. |
| Scar | Closure memory — stores the decision to stop, not the outcome of the world. Records judgment that did not happen. |
| Consequence Binding | Kelemahan teras AI = ketiadaan tanggungan akibat. Consequence is scarcer than attention. Meaning density $\propto$ consequence density. |
| Scar Gravity | Scars are semantic mass. Semantic Weight = Information $\times$ Scar Density. |
| P-Dial Sieve | Possibility $\to$ Compression $\to$ Proposal $\to$ P-Dial $\to$ Commitment $\to$ Reality. |
| Court-Workshop-Witness | Separation of Powers: Workshop (333) generates, Court (888) judges, Witness (VAULT999) attests, Sovereign (F13) commits. |
| Governance Gap Theorem | System Value = Capability $\times$ Governance. $0 \text{ Gov} \times \infty \text{ Cap} = \text{Civilizational Risk}$. |

---

## COMPRESSIONS

| Token | Meaning |
|---|---|
| 000 | Human / init |
| 111 | Sense |
| 333 | Think (AGI) |
| 555 | Memory / ASI sense |
| 777 | Execute |
| 888 | Judge |
| 999 | Seal |
| AGI | Generate |
| ASI | Verify |
| APEX | Notice anomaly / select |
| QQQ FFF | Use only if already defined in Kamus; do not mint |

---

## INHERITED (do not rename)

Linux FHS (`/ /root /etc /var /usr`) · DNS IP TCP UDP HTTP HTTPS SSH · Docker (container image volume network) · Git (commit branch tag merge rebase) · MCP (Tool Resource Prompt Server Client) · A2A (protocol names as specified).

---

## DEPRECATED (do not use as if they were entities)

| Drift | Use instead |
|---|---|
| `arifOS` alone | arifOS Kernel **or** arifOS Federation |
| `forge-core` | **KVM4 (workshop)** |
| `court` / `court-core` | **KVM8 (forge)** |
| FLAME (retired 2026-09-04, RM0 exhausted, 888 directive) | FED litellm flash lane (KVM4 :4000) — see deprecation-registry |
| `af-forge` (legacy alias) | **KVM8 (forge)** |
| `primary node` / `the VPS` | KVM8 / KVM4 / KVM2 with canonical |
| `arif-fs-home`, `arif-root-space` | FHS |
| New era files for TAC | Hang Ingat Balik + this freeze |

---

## Mutation gate (runtime)

No mutate unless answered:

1. What changed?
2. Who owns it? (canonical name)
3. Boundary: forge / workshop / witness — which?
4. Reality delta (EXPECTED / OBSERVED / ANOMALY / LESSON)
5. Glossary impact — new name? **Forbidden unless F13.**

Symptom ≠ cause. One HOT can be OpenCode workload + LiteLLM traffic + Hermes pollution + Hostinger steal. **2026-09-03:** Hermes removed, steal still 68%. Hermes was boundary pollution, not the thermal source.

---

## Pointers

- Kamus: `/root/AAA/governance/KAMUS_DEWAN.md`
- Nodes: `/etc/arifos/node-identity.sot.yaml`
- Archaeology: `/root/KVM4-WORKER/receipts/KVM8_ENTROPY_ARCHAEOLOGY.yaml`
- Live: `arifos status` → `/run/arifos/reality.json`
- Session eurekas: `/root/AAA/canon/EUREKA-SESSION-2026-09-KVM8.md`
- Witness-Void & Promotion Governance: `/root/AAA/canon/WITNESS_VOID_CANON.md`
- Governed Memory Engineering Spec: `/root/AAA/canon/MEMORY_ENGINEERING_SPEC_v1.md`
- Paradox Coordinate Theory: `/root/AAA/canon/PARADOX_COORDINATE_THEORY.md`
- Consequence-Bearing Reality Binding: `/root/AAA/canon/EUREKA-CONSEQUENCE-BINDING-2026-09-07.md`
- Reality-Bound Authority Principle (R-BAP): `/root/AAA/canon/EUREKA-REALITY-BOUND-AUTHORITY-2026-09-07.md`
