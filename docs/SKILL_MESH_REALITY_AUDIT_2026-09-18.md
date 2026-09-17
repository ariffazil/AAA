<!-- SOT: doctrine/audit fragment. Tier: DRAFT_AWAITING_F13 unless ratified in chat. -->
# SKILL MESH — REALITY AUDIT AGAINST AN EXTERNAL STRUCTURAL AUDIT
> Forged: 2026-09-18 · KVM8 (forge, 100.64.0.2) · Hermes ASI session
> External input: an outside model's structural audit of the skill mesh, relayed by F13 (Arif) 2026-09-18.
> Method: live disk walk of the canonical home + the harness view + the three organ repos, read against
> `.matrix-index.json`, `FEDERATED_SKILLS_REGISTRY_V3.yaml`, `SKILL_ALIAS_TABLE.json`, and the Seven Laws.
> Labels: OBS = observed this session · DER = derived from OBS · INT = interpretation · UNKNOWN.
> **This document audits the auditor.** Its job is to separate what is true from what is an artifact of
> the view the external model was reading.

---

## 0. Verdict in one line

The external audit read the **derived coordinate index** and reported it as the **storage tree**. Six of its
findings are real, four of those are at a different layer than stated, and the largest defect in the mesh
— **zero skills can prove a consequence class** — it did not see at all.

---

## 1. Confirmed by reality (OBS)

1. **Capability names reused across organs — TRUE, and there are 10, not 6.**
   From `by_coordinate` in `.matrix-index.json`, capability names appearing under more than one
   `(domain, organ)`:
   `business-intel` · `catalog-ops` · `federation-topology` · `incident-response` · `mcp-ops` ·
   `my-domain-intel` · `research-core` · `substrate` · `voice-stack` · `well-domain`.
   The external list named six of these. All six are present. **Overlap is real.**

2. **Domain isolation is not a partition — TRUE.**
   The coordinate space admits the same capability under two organs, so an agent selecting by category
   cannot tell which one owns the behaviour. This is a *selection-safety* defect, not tidiness.

3. **Missing protocol: instant-override / circuit breaker — TRUE.**
   No dedicated capability owns it. `jitu` appears inside two skills (`vps-cpu-throttle-triage`,
   `a-forge-development`) as prose, not as an actuator. Nothing can halt all automated escalation
   by invoking one named capability.

4. **Missing: organ-side physical constraint gates — TRUE, and the source already exists.**
   `K-DIP` / `K-SCALE` / `K-TAPER` are specified in `/root/GEOX/docs/SEISMIC_FAULT_PHYSICS_GATES_K_SPEC.md`
   (plus `SEISMIC_STRUCTURAL_VALIDATION_GATES_G0_G10.md`) but **no capability loads them at the point of
   interpretation**. The doctrine exists; the actuator does not. Classic doctrine-decoration.

## 2. Mislocated — the address is not the storage (OBS → DER)

Three of the six paths the external audit named **do not exist on disk**:
`domains/geo/workshop/voice-stack` · `domains/well/aaa/catalog-ops` · `domains/well/workshop/well-domain`.

They do exist as **coordinates**, because `skill-matrix.py` mints a coordinate for every skill that is not
already living at a five-part `domains/<domain>/<organ>/<capability>/<skill>` path — inferred by token
similarity, then a keyword table, then a last-resort bucket:

```
classify()  → token overlap ≥ 0.30 → (capability, organ)
            → keyword table hit    → (capability, organ)
            → otherwise            → ('general-capability', 'workshop')   # the last resort
```

Consequences, measured:

| Observation | Value |
|---|---|
| Ghost coordinate `domains/general/workshop/general-capability` | holds 11 skills |
| Skills whose coordinate ≠ their disk path | 199 |
| Indexed skills / coordinates / dead pointers | 418 / 80 / 16 |
| Canonical storage tree | 513 SKILL.md (excl. `.archive`, `.system`) |
| Flat-root residues at the canonical home top level (pre-`domains/`) | 211 dirs |

**So the "leakage" the external audit saw is in the derived view, not in the storage tree.** Re-merging
directories would not fix it. Fixing the generator and promoting the residue into the tree would.

## 3. What the external audit did not see (OBS — the larger defect)

1. **Consequence class: 0 of 513 skills can prove one.**
   Not one canonical skill declares side-effect class, blast radius, reversibility, or a may-not list.
   207 carry a weaker proxy (`risk_tier` + `floor_scope` + `autonomy_tier`); **306 carry nothing at all.**
2. **Verification and kill: 0 of 513.**
   `last_verified`: 0. Kill criterion: 0. Provenance is partial — `owner` 209, `forged` 33.
   Under Law 7 the entire library is currently a *rumour set*, not a capability set.
   *Doctrine without a kill is decoration.*
3. **Worklist size: 230 skills** can reach reality (outbound surface, canonical state, shared infra,
   destruction, or a delivered artifact) **and cannot prove a consequence class.** By surface:
   canonical-record 92 · delivered-artifact 57 · shared-infra 45 · outbound 34 · destructive 2.
4. **The registry is 80% illegible on its face.**
   `FEDERATED_SKILLS_REGISTRY_V3.yaml` declares 123 skill names; **24 resolve by that name on disk
   (20%)**. The rest are alias rows — `SKILL_ALIAS_TABLE.json` maps `v3_name → primary_disk_name`
   (`dev-*`, `ops-*`, `meta-*`, `apex-*` families). The alias layer is deliberate; reading the registry
   without it is reading a phone book of dead numbers. Registry self-verdict: `WARN`,
   `duplicate_identity_groups: 70`, `duplicate_identity_skills: 132`, `diverged: 30`.
5. **Three organ repos hold capabilities the canonical mesh cannot see.**
   `/root/WELL/skills` (4: triadic ops, consent registry, substrate readiness, machine diagnose) ·
   `/root/WEALTH/skills` (4) · `/root/GEOX/skills` (5). Meanwhile the canonical tree's organ bands hold
   different content (`domains/well/workshop` = body/research lanes; `domains/geo/workshop` = one lane).
   **Additive surfaces, not views** — the exact defect Law 3 forbids. The canonical tree's own
   `domains/general/workshop/well-domain/well-operations` is a generic operator skill; the organ's real
   capability set is invisible to the mesh.
6. **Two writers on one name.** AAA ∩ harness view = 44 shared names, **26 byte-diverged**.
   Nothing in the library says which of the two is authoritative for those 26.

## 4. The apex-zen mapping (what "apex-zen alignment" means for a skill)

Authority: `canon/APEX-ZEN-CANONICAL-COMPRESSION.md` (chain BUILD → VERIFY → JUDGE → SEAL → ACT → WITNESS,
`CAPABILITY ≠ AUTHORITY`, *govern capabilities, not implementations*) read together with
`instructions/agi-asi-skills-fundamentals.md` (the Seven Laws). A skill is apex-zen aligned when it can
prove its position in that chain. Measured state:

| Law | Requirement | Measured today |
|---|---|---|
| 1 RESOLVE BEFORE ASK | the capability resolves inward, asks only the four sovereign classes | UNKNOWN per-skill; not encoded |
| 2 CAPABILITY TRUTH, both directions | index and disk agree | 16 dead pointers, 1 ghost coordinate, 199 address≠storage |
| 3 ONE WRITER, MANY VIEWS, LIVE SENSOR | one writer, views are links, a sensor that can fail | sensor exists (census, 4×/day); **26 diverged pairs = two writers**; 3 organ repos = 12 unmirrored skills |
| 4 CONSEQUENCE CLASS | side effect · blast radius · reversibility · authority tier · may-not | **0 full · 207 proxy-only · 306 absent** |
| 5 SELECTION PRECISION | unique discriminating trigger in the first 57 chars | 8 duplicate 57-char windows, 16 skills inside them; 12 skills open with the same fed-tier boilerplate |
| 6 SELF-MODIFICATION ASYMMETRY | capability may auto-mutate; judge may not | no skill-level split declared |
| 7 PROOF AND KILL | provenance · last verified (timestamp + command) · kill criterion | **last_verified 0 · kill 0**; owner 209/513, forged 33/513 |

**So: the apex-zen gap is not a directory problem. It is a per-skill governance-field problem.**
Directory remerge changes addresses; it does not make a single capability able to say what it may not do.

## 5. Option A vs Option B — the federation already decided (C)

The external audit offers strict centralisation (A) or air-gapped organs (B). Both are already resolved
by a **ratified** doctrine the external model could not see: the Plane Law in
`docs/SKILL_MESH_ALIGNMENT_2026-09-16.md` §3 and §6.

```
MACHINE_PLANE  (forge · audit · ops · dev · infra)     → AAA canonical, ONE copy, kebab-case
                                                          every other surface links, never re-authors
HUMAN_PLANE    (counsel · well · voice · media · human) → Hermes owns; AAA mirrors read-only at most
SUBSTRATE CORE (7 substrate + 4 knowledge)              → AAA canonical, byte-identical, every agent, first
NEVER ALIGN    SOUL · register · counselling/voice authorship · forger bands · substrate text
```

Under that law: infrastructure logic centralises (A wins there), human-facing and domain-context
capabilities stay organ-owned as *views* of one canonical body (B restricted to content, never to
duplicate infrastructure). The external audit's binary was a false choice; **the real defect is that
three organ repos are additive surfaces instead of views.** That is Law 3, not an A/B preference.

## 6. Reversibility (already satisfied, before any pruning)

```
tag    v2026.09.18-skills-audit  @ 9c34a4023   (AAA HEAD, 2026-09-18 00:57 +0800)
bundle /root/AAA/backups/skills/aaa-pre-remerge-20260918.bundle   (147 MB, --all)
anchor previous tags: v2026.09.12 … v2026.09.16
```
No deletion or move is executed without this anchor present. Every stage below is `git revert`-able.

## 7. Staged plan (each stage reversible, canary-first, receipt on exit)

- **S0 — address truth (mechanical, no content change).** Make the coordinate generator either resolve to
  the real disk path or emit `UNRESOLVED` instead of inventing an organ address. Kills the ghost
  coordinate class permanently. This is the fix that makes the *view* honest.
- **S1 — kill the residue.** Promote the 211 flat-root residues into the `domains/` tree (or explicitly
  mark them `bundled: true` and exclude them from the coordinate view). Removes address≠storage for 199.
- **S2 — three views, not three copies.** For the 12 organ-repo capabilities: publish them into canonical
  under their own organ band and leave the organ repo as the authored home with a link. Canonical becomes
  the mesh-visible address; the organ keeps authorship. Ends the additive-surface defect.
- **S3 — one writer for the 26 diverged pairs.** AAA wins; the harness-side body is diffed into
  `_archive/pre-align-<date>/` first. One skill as a canary before the batch.
- **S4 — the real work: 230 consequence classes.** Not a bulk edit. Batch by surface, highest blast radius
  first (canonical-record 92 → infra 45 → outbound 34 → artifact 57 → destructive 2), each carrying the
  five fields plus `last_verified` (timestamp + the command) and a kill criterion.
- **S5 — the four missing actuators**, in this order: circuit-breaker / instant-override · GEOX physical
  gates (source spec already exists) · an ops capability for the token/cognitive-wire middleware ·
  decay/pruning for memory state (`entropy-metabolizer` + `audit-repository-entropy` already cover the
  repo-audit half; memory decay is the unowned half).

**Deliberately NOT in scope:** the 6 overlap rows in §1 are **not** resolved by moving directories. They
are resolved by the capability name becoming unique per organ in the coordinate space, or by one of the
two becoming an alias. Category is an address, not a keyword (Law 5).

## 8. The one binary for F13

Greenlight **S0–S2** (mechanical, reversible, no skill body changes, anchor in place) and I execute and
report receipts — or hold, and I stop at the audit. S3–S5 each come back as their own binary with its own
receipt, because each one touches authorship or 230 bodies.

*One truth · many views · plane decides the writer · DITEMPA BUKAN DIBERI ⚒️*
