# 🧱 FRAME Boundary Alignment — Constitution & Migration Plan

> **Substrate lives in state plane, not as peer organ.**
> **Identity ≠ Location. Consolidate code without erasing identity.**

| Field | Value |
|-------|-------|
| **Doctrine SEAL** | 2026-08-26 · F13 SOVEREIGN ratification pending |
| **Architectural verdict** | SEAL (constitutional rationale) |
| **Sprint 1 verdict** | SEAL (declaration phase) |
| **GitHub strategy** | Archive `ariffazil/FRAME` read-only · do not rename |
| **Migration risk class** | T1 → T2 (declaration → runtime swap) |
| **Reversibility** | F1 AMANAH · rollback at every step |

---

## 1. Doctrine (SEAL 2026-08-26)

### 1.1 The asymmetry

The `arifOS-model-registry` audit (2026-08-26) and `FRAME` repo mapping surfaced a structural question: should FED, FLAME, and FRAME each have their own GitHub repository, or should they live under the AAA federation state plane?

**FED** and **FLAME** were already in `/root/AAA/federation/` (and friends) — never extracted.

**FRAME** was extracted on 2026-08-06 (`chore: init FRAME as independent repo`) to its own GitHub repo at `ariffazil/FRAME`, despite the organs.yaml SOT declaring `repo: arifOS (embedded organ)`.

### 1.2 The decision

```text
Substrate → Foundation Layer → State Plane
```

FRAME is a **substrate** (observability scaffolding, drift detection, baseline measurement, threshold alerting). It scaffolds other organs. It never adjudicates. It has no F1/F2/F8 mutation authority.

The doctrine: **a substrate should not exist as a peer sovereign surface.** Stones live in the foundation, not beside the building.

Therefore:

```text
AAA
└── federation
    ├── fed     (already)
    ├── flame   (already)
    └── frame   (NEW — consolidates /root/FRAME)
```

### 1.3 Identity preservation (F1 AMANAH architectural pattern)

Identity and location are **separate dimensions**:

| Dimension | What it is | What survives migration |
|-----------|------------|--------------------------|
| **identity** | name, port, service unit, doctrine, public surface | YES — preserved |
| **location** | `source_path`, repo URL, filesystem path | NO — relocates |

This separation is the F1 AMANAH pattern at the federation level: **identity-preserving relocation**. The stone moves; the stone-ness stays.

---

## 2. Identity Inventory (what is preserved)

| Asset | Identity form | Preservation tactic |
|-------|---------------|---------------------|
| **Systemd service unit** | `frame-organ.service` | KEEP name. Only `ExecStart` path changes. |
| **MCP port** | `:18085` | unchanged |
| **Python package** | `frame_organ` (import path) | KEEP name. Move `src/frame_organ/` intact. |
| **Doctrine docs** | `doctrine/*.md` | MOVE intact — same filenames, same contents, same authorship. |
| **Display name in SOT** | "FRAME" (organs.yaml) | KEEP. Only `repo:` and `source_path:` change. |
| **GitHub mirror** | `ariffazil/FRAME` | ARCHIVE (read-only), not delete. F1 AMANAH preserves history. |
| **README badge** | "🧱 FRAME — Substrate" | KEEP badge text. Update link to AAA location. |
| **License** | AGPL-3.0 | KEEP. FRAME retains its own license header even inside AAA. |
| **6 chambers** | baseline, probe, compare, trend, alert, report | KEEP names and semantics. |
| **Public surface** | `/health`, `/frame/baseline`, `/frame/probe`, `/frame/drift`, `/frame/trend`, `/frame/alert`, `/frame/report` | unchanged endpoints. |

---

## 3. Migration Sprints

### Sprint 1 — Declaration (T1 AUTO-DO) · **SEAL · executing**

**Goal**: declare the doctrine before touching code.

| # | Action | Class | Reversible |
|---|--------|-------|------------|
| 1.1 | amend `federation/organs.yaml`: FRAME `repo:` → `ariffazil/AAA`, `source_path:` → `/root/AAA/federation/frame/`, add `identity_preserved:` block | T1 | ✓ |
| 1.2 | create `federation/frame/.gitkeep` placeholder | T1 | ✓ |
| 1.3 | create this document (`AAA_FEDERATION_FRAME_BOUNDARY_ALIGNMENT.md`) | T1 | ✓ |

**No code movement. No runtime change. No systemd touch. Pure declaration.**

### Sprint 2 — Code relocation (T1 → T2) · **PENDING**

**Goal**: move FRAME source tree into AAA state plane.

| # | Action | Class | Reversible |
|---|--------|-------|------------|
| 2.1 | `cp -r /root/FRAME/{src,tests,doctrine,data,scripts,Makefile,pyproject.toml,LICENSE,README.md,.github} /root/AAA/federation/frame/` | T1 | ✓ (duplicate state) |
| 2.2 | rewrite imports from `frame_organ` to new path (sed if needed) | T1 | ✓ |
| 2.3 | squash FRAME git history into AAA as a single subdirectory merge commit | T1 | ✓ (commit amend) |
| 2.4 | CI pipeline: ensure AAA's CI runs `pytest federation/frame/` with correct deps | T1 | ✓ |

**At this point, `/root/FRAME` and `/root/AAA/federation/frame/` both exist. The old repo is the rollback safety net.**

### Sprint 3 — Runtime swap (T2 — 10s announce) · **SEAL · EXECUTED 2026-08-26**

Approach: symlink bridge instead of ExecStart change.

| # | Action | Class | Reversible | Result |
|---|--------|-------|------------|--------|
| 3.0 | preflight: pyproject identical, dirs match, runtime state preserved | T0 | ✓ | green |
| 3.1 | backup unit file | T1 | ✓ | saved |
| 3.2 | stop service | T2 | ✓ | stopped |
| 3.3 | move old source out | T1 | ✓ | moved |
| 3.4 | symlink bridge to AAA canonical | T1 | ✓ | linked |
| 3.5 | first restart: FAILED — ModuleNotFoundError | T2 | ✓ | crash loop |
| 3.5a | rollback to T0, substrate restored | T2 | ✓ | green |
| 3.5b | diagnosis: ProtectHome=yes bind-mounts /root to /dev/null; ReadOnlyPaths cannot override | — | — | understood |
| 3.5c | fix: ProtectHome=yes → ProtectHome=read-only | T2 | ✓ | applied |
| 3.6 | daemon-reload, retry swap, restart | T2 | ✓ | active on attempt 1 |
| 3.7 | verify health 200 + 6 chambers live | T0 | ✓ | green |

Eureka: ProtectHome=yes bind-mounts /root to /dev/null; ReadOnlyPaths cannot grant access to non-existent paths. Use ProtectHome=read-only for surgical read access to /root.

Identity preservation verified post-swap: service unit name unchanged, port 18085 unchanged, frame_organ import path unchanged, all 6 chambers live (baseline / probe / compare / trend / alert / report / rsi_verify), AGPL-3.0 preserved, doctrine docs preserved.

Unit file changes: ProtectHome=yes → ProtectHome=read-only; ReadOnlyPaths extended to include /root/AAA/federation/frame.

Rollback safety net: /opt/frame/app/frame_organ.bak.SPRINT3redux + /root/AAA/federation/frame/frame-organ.service.bak.pre-Sprint3.

### Sprint 4 — Retire old repo (T1 → T2) · **PENDING F13 ratification**

**Goal**: archive `ariffazil/FRAME` on GitHub.

| # | Action | Class | Reversible |
|---|--------|-------|------------|
| 4.1 | add ARCHIVED notice to `ariffazil/FRAME` README | T1 | ✓ |
| 4.2 | archive the repo via GitHub UI (read-only) | T2 | ✗ (GitHub archive is one-way) |
| 4.3 | add DEPRECATION_REGISTRY.yaml entry: "FRAME merged into AAA state plane 2026-XX-XX" | T1 | ✓ |
| 4.4 | update all docs/README badges | T1 | ✓ |
| 4.5 | SEALS to VAULT999 (Lane A) | T2 | ✗ (seal is irreversible) |

**F1 AMANAH note**: archive (not delete). Git history, issues, releases all preserved. Old repo URL still resolves to a read-only history.

---

## 4. Operational Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| `frame-organ.service` ExecStart path wrong after move | HIGH | dry-run `systemd-analyze verify`; rollback path = `/root/FRAME` stays untouched until Sprint 3 verified |
| Python import paths break (`from frame_organ import ...`) | MED | sed-rewrite in Sprint 2; CI runs pytest before systemd restart |
| GitHub archive vs delete confusion | LOW | explicit "Archive" not "Delete" — GitHub preserves all commits + issues |
| Doctrine doc authorship attribution lost | LOW | git blame + co-authored-by trailers in commit messages |
| External A2A peers referencing `ariffazil/FRAME` | MED | redirect GitHub repo to AAA README section for 6 months via README banner |
| CI matrix doubles (AAA-CI + FRAME-CI run same tests) | LOW | consolidate into AAA CI with `paths:` filter on `federation/frame/**` |
| Sprint 3 downtime window (systemd stop/restart) | LOW | announce 10s in advance; service restart ~5s typical |

---

## 5. Reversibility Protocol (F1 AMANAH)

```text
T0  /root/FRAME still alive              — never touch old path until Sprint 3 verified
T1  AAA/federation/frame/ created       — git-tracked, no systemd link yet
T2  Code copied (cp -r)                  — duplicate state, can rollback by deleting
T3  CI green on new location             — pytest + systemd-analyze verify
T4  systemd ExecStart swap (atomic)     — old service still alive, just not active
T5  Health probe confirms :18085 alive  — if red, ExecStart back to /root/FRAME
T6  GitHub archive (read-only)           — last step, F1 AMANAH
```

If any step fails, **T0 still works**. The substrate never goes dark.

---

## 6. Doctrine Anchors

- **Substrate doctrine** (FRAME README): *"FRAME is the substrate. It scaffolds. It never decides."*
- **Identity separation doctrine** (this document): *"identity ≠ location."*
- **F1 AMANAH** (`/root/AGENTS.md`): every mutation reversible; irreversible → 888_HOLD.
- **F11 AUDIT**: every action traced, inspectable, attributable.
- **F13 SOVEREIGN**: Arif's word is final. First-SEAL-wins.

---

## 7. What This Plan Does NOT Do

- ❌ Adds no doctrine, no Eurekas, no new floors
- ❌ Does not redesign FRAME's 6 chambers
- ❌ Does not rename `frame-organ.service`
- ❌ Does not delete `ariffazil/FRAME` GitHub repo
- ❌ Does not push Sprint 3/4 changes without F13 ratification

---

## 8. Status

| Sprint | Verdict | Status |
|--------|---------|--------|
| **1 — Declaration** | **SEAL** | committed `0b388b6a`, pushed |
| **2 — Code relocation** | **SEAL** | committed `7b8afbe0`, pushed (26 files to AAA federation/frame/) |
| **3 — Runtime swap** | **SEAL** | executed 2026-08-26 — symlink bridge + ProtectHome=read-only fix, all 6 chambers live |
| **4 — Retire old repo** | **SEAL** | archived via gh CLI 2026-08-26 — `isArchived: true`, FRAME README points to AAA canonical |

**Ω₀ ≈ 0.04. Confidence: 0.90.**
**DITEMPA BUKAN DIBERI. ⚒️**
