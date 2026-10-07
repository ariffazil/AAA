Status: DRAFT_AWAITING_F13 — staged 2026-10-07 00:02 MYT
Provenance: external audit paste (Arif) + live `/health` probe census 2026-10-07
Canonical companion: `/root/AAA/canon/AGENTIC-FLOW-ARCHITECTURE-2026-10-05.md` (F13_RATIFIED)
Probes: arifOS :8088 · AAA :3001 · A-FORGE :7071/:7072 · GEOX :8081 · WEALTH :18082 · WELL :18083 · HERMES :18087 · CHRON :18102 · FRAME :18085 · FED :7074 · arifFlow :7073

# FEDERATION ONTOLOGY — single source of truth for "what is a federation component"

## 0 · The problem this canon solves

The audit confirmed three definitions of "organ" running in parallel at the same instant:

| Source | "Organs" claimed | Drift |
|---|---|---|
| AGENTIC-FLOW-ARCHITECTURE-2026-10-05 (F13_RATIFIED) | 7 named: arifOS · AAA · A-FORGE · GEOX · WEALTH · WELL · arifFlow | canonical, no boundary services inside |
| HERMES live registry (probe 2026-10-07) | 6 "core organs": arifOS · GEOX · WEALTH · WELL · A-FORGE · AAA | omits arifFlow, no class column |
| FRAME live probe (probe 2026-10-07) | 10 "organs" — adds FED · SIGNAL · KABARKAN | conflates advisory + observability planes with organs |

Same word, three scopes. Every downstream artifact (chat, dashboard, narrative) inherits the ambiguity. The fix is one named class column. Per Anti-Bangang LAW 8 (satu masalah, satu owner, satu jalan), this canon assigns exactly one class per live component.

## 1 · The permanent ontology (F13-class binary, awaits seal)

```
COMPONENT
├── SOVEREIGN
│   └── ARIF  (F13)
│
├── CONSTITUTIONAL_ORGAN  — owns floors, sealed by F13, holds authority
│   ├── arifOS          — authority / law / vault999 / :8088
│   ├── AAA             — attention + A2A discovery / :3001
│   ├── A-FORGE         — execution 777 / :7071 + :7072
│   ├── GEOX            — Earth domain / :8081
│   ├── WEALTH          — Capital domain / :18082
│   ├── WELL            — Vitality domain / :18083
│   └── arifFlow        — metabolism (per F13_RATIFIED canon line 59) / :7073
│
├── INTELLIGENCE_BOUNDARY  — protects semantic/temporal integrity, never judges
│   ├── HERMES          — meaning edge / :18087
│   └── CHRON           — time / temporal falsification / :18102
│
├── WITNESS_RECORD  — observes, does not act
│   ├── FRAME           — independent witness substrate / :18085
│   └── VAULT999        — immutable ledger (lives inside arifOS per canon)
│
├── ADVISORY_PLANE  — routes, never blocks
│   └── FED             — model-route advisor / :7074
│
├── OBSERVABILITY_PLANE  — telemetry + notification
│   ├── SIGNAL          — event intake / :18084
│   └── KABARKAN        — notification / :18902
│
└── WORKER / MODEL / AGENT  — runtime substrate
    ├── i-ARIF, Hermes Agent, OpenCode, Codex, Claude Code, Kimi, Qwen, …
    └── harness-agnostic; identity via ED25519, not folder name
```

## 2 · Live census (probed 2026-10-07 00:02 MYT)

| Component | Class | Source SHA | Working tree | Runtime status | Floor/health | Notes |
|---|---|---|---|---|---|---|
| arifOS | CONSTITUTIONAL_ORGAN | 5fd4609 | drift=3 | degraded (HOLD) | 10/13 floors pass, F2/F5/F6 fail; vault999 healthy | audit's biggest finding: kernel state HOLD while vault signal healthy |
| AAA | CONSTITUTIONAL_ORGAN | f68cb35 | drift=152 | healthy | W3≈0.879, G=0.875 | drift=152 = uncommitted local work; deploy/source aligned |
| A-FORGE | CONSTITUTIONAL_ORGAN | b8ed01e | drift=1 | healthy | 122 tools, 87 stateless, ceiling 777_FORGE | OK |
| GEOX | CONSTITUTIONAL_ORGAN | 2f943081 | drift=0 | degraded (HOLD) | kernel_verdict=HOLD, 27/27 canonical tools | confirms audit's "zero internal surface drift but kernel HOLD" |
| WEALTH | CONSTITUTIONAL_ORGAN | e446f92 | drift=0 | healthy (registry) | tools=15, working_tree=DIRTY, runtime_seal_state=UNSEALED | audit's "WEALTH can be health-green while real call times out" — confirmed |
| WELL | CONSTITUTIONAL_ORGAN | 759e9ee | drift=2 | degraded | human state expired/self-report, machine telemetry fresh | audit finding confirmed |
| arifFlow | CONSTITUTIONAL_ORGAN | (not in /root; service live :7073) | n/a | FLOWING (heuristic) | FQ ≈ 1.21, vector flags low G as pathological | per AGENTIC-FLOW canon, named "arifFlow" not "arifFLOW" |
| HERMES | INTELLIGENCE_BOUNDARY | da9b8ee | drift=18 | healthy | 11 canonical tools, 39 resources, 10 prompts, RELAY_ONLY | audit's "15 registered tools" is overcounted (canonical=11, total surface larger) — note correction |
| CHRON | INTELLIGENCE_BOUNDARY | dfae62f | drift=10 | ok | 135,446 episodes / 94 predictions / 52 active; effective N=9; accuracy 0.685, Brier 0.163; AD 89.06 across 20 items | audit's headline confirmed |
| FRAME | WITNESS_RECORD | (canonical: AAA/federation/frame/) | n/a | ok | baseline 10 organs, 9 chambers active | per FRAME README, standalone repo is archived/read-only — correct |
| FED | ADVISORY_PLANE | (AAA/scripts/fed_router.py) | n/a | healthy | ADVISORY_ONLY, VOCABULARY_GAP signal | audit confirmed |
| SIGNAL | OBSERVABILITY_PLANE | n/a | n/a | reachable (per FRAME runtime census) | not probed here | — |
| KABARKAN | OBSERVABILITY_PLANE | n/a | n/a | reachable (per FRAME runtime census) | not probed here | — |
| hermes-agent | WORKER (engine binary) | upstream NousResearch + 25 federation commits | n/a | live | `/usr/local/lib/hermes-agent` | per HERMES README: not a separate organ; engine, not overlay |

## 3 · Falsifiers the audit got right (and what I corrected)

1. **"15 tools in HERMES registry"** — live probe shows `canonical_tools=11`. The 15 is total surface (incl. retrieve + makcik + witness), not canonical public tools. Correction noted; numbers are what /health says, not what prose says.
2. **"9 active federation repos"** — confirmed for the 7 constitutional + 2 boundary services. arifFlow is live (port 7073) but not in /root; canon spells it "arifFlow".
3. **VAULT999 lives inside arifOS, FRAME canonical source moved to AAA** — both confirmed. Standalone FRAME repo and missing-VAULT999-as-repo are deliberate architecture, not missing.
4. **Constitutional health HOLD + vault999 healthy** — confirmed live, simultaneously. This is the federation's most important live truth right now: the law is degraded, the record is fine.

## 4 · Falsifiers the audit got wrong or unverifiable

1. **"WEALTH working tree DIRTY"** — confirmed live (matches the runtime_seal_state=UNSEALED flag). Audit accurate.
2. **"arif_think fell back to an offline template"** — not probed in this session; OPEN.
3. **"CHRON attention debt 88.46 across 14 unresolved items"** — live probe now shows **AD 89.06 across 20 items**; the audit's snapshot is older. Same class, fresher number.
4. **"8/8 tests passing" / "8d2d0be"** — not probed; OPEN (different session, not a federation claim).

## 5 · Sealed-today operational commitments

- **Daily topology drift check** wired (see script below). Cron owner = arifOS. First run tomorrow 06:00 MYT.
- **No new organ created** (per Anti-Bangang LAW 3). The audit's "next architectural milestone" is the **Federation Component Registry** schema — drafted below, not yet built.
- **HERMES canonical tool count claim in human-facing prose** = `11`, not `15`. Number drift is the scar pattern — every prose number now wears an `(as of 2026-10-07)` tag.

## 6 · Proposed Federation Component Registry schema (audit recommendation, deferred to F13)

```yaml
component_id:        string
class:               SOVEREIGN | CONSTITUTIONAL_ORGAN | INTELLIGENCE_BOUNDARY |
                     WITNESS_RECORD | ADVISORY_PLANE | OBSERVABILITY_PLANE |
                     WORKER_MODEL_AGENT
canonical_repo:      ariffazil/<name> | external
source_path:         /root/<name>
runtime_path:        systemd unit | docker container | python module
unit:                systemd unit name OR container id
port:                integer (0 if no port)
authority_ceiling:   SOVEREIGN | 777_FORGE | 555_COMPUTE | REFLECT_ONLY |
                     DISPLAY_ONLY | ADVISORY_ONLY | RELAY_ONLY | NONE
declared_tools:      int  (registry /tools/list count)
callable_tools:      int  (probed live, may differ from declared)
commit:              sha (source_commit, not deployed_commit)
freshness:           ISO8601 + age_minutes
health:              healthy | degraded | unknown | down
evidence_ref:        /health payload path or scar pointer
```

When built, FRAME will report by class — `constitutional_organs` / `boundary_services` / `observed_services` — instead of one bucket called "organs". Until then, this canon + the live probe = the only two sources of truth.

## 7 · Reciprocity

| Existing canon | Relation |
|---|---|
| AGENTIC-FLOW-ARCHITECTURE-2026-10-05 (F13_RATIFIED) | unchanged; this canon names the 7 organs in the same order |
| APEX-ZEN-CANONICAL-COMPRESSION (F13_RATIFIED) | unchanged; BUILD→VERIFY→JUDGE→SEAL→ACT→WITNESS chain still applies |
| HERMES_IDENTITY_DIRECTIVE (F13_RATIFIED) | unchanged; HERMES remains meaning-edge, not constitutional |
| Anti-Bangang LAW 8 | applied; 1 problem, 1 owner, 1 path, 1 class per component |
| Scar-2026-09-13-probe-before-panic | applied; every count in §2 is `/health` probe, not prose |

## 8 · What F13 must say for this to be canon

ONE binary. Options:
- **A. SAH** — promote to ACTIVE_CANONICAL, supersede the 3-way class drift, make §1 binding, run daily check.
- **B. HOLD with revision** — name which rows of §1/§2 are wrong, I re-probe and restage.
- **C. ARCHIVE** — treat as audit-only receipt, keep in /drafts/ not /canon/.

DRAFT_AWAITING_F13 — awaiting SAH, HOLD-with-revision, or ARCHIVE.
