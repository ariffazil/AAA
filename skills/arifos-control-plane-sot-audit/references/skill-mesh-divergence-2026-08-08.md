# Skill Mesh Divergence — 2026-08-08

> Pattern #7 in `arifos-control-plane-sot-audit`. The shortest-distance cross-SOT
> axis in the federation, and the one `aaa-drift-check.py` doesn't cover.

## What the mesh is

The federation's skill catalog is a **3-tree mesh** where each tree carries its
own `version:` field per skill. Sync is by convention, not by symlink.

| Tree | Path | Role |
|---|---|---|
| AAA | `/root/AAA/skills/<name>/SKILL.md` | Catalog — source of truth (SOT) |
| Hermes | `/root/.hermes/skills/<name>/SKILL.md` | View — agent-visible skill surface |
| Kimi | `/root/.kimi-code/skills/<name>/SKILL.md` | View — Kimi Code's role/skills |

Answering "are my agents in sync right now?" requires reading all three trees
and diffing declarations.

## Live snapshot (2026-08-08)

```
Total versioned SKILL.md: 281   (via `find -maxdepth 2` across the 3 trees)
  AAA:    106
  hermes:  14
  kimi:   106
```

The `-maxdepth 1` variant recommended for the protocol returns **0** because
skill directories nest one level deeper on this mesh. Use `-maxdepth 2` for a
live comparison (`scripts/skill-mesh-probe.sh` does this).

## The 4 status values

| Status | Meaning | Action |
|---|---|---|
| `SYNC` | All three trees carry the skill at the same version | none |
| `DIVERGED` | ≥2 trees carry the skill at different versions | **flag**; **fix** after `>3 sessions` DIVERGED |
| `MISSING_FROM_X` | `X ∈ {aaa, hermes, kimi}` does not carry the skill | **propagate from AAA** (catalog is SOT) |
| `MISSING_FROM_aaa` | Orphan in a view tree, not in catalog | **reverse-propagate first**; violates catalog-first rule |

## The escalation protocol

```
DIVERGED  → flag (no fix on first sight; catches mid-flight propagation)
DIVERGED > 3 sessions → fix (align to AAA version)
MISSING_FROM_X → propagate from AAA (rsync or A-FORGE forge)
MISSING_FROM_aaa → reverse-propagate (orphan violates catalog-first)
```

## Pitfalls verified this session

### 1. `-maxdepth 1` returns empty

The canonical mesh-sync command:

```bash
find /root/AAA/skills /root/.hermes/skills /root/.kimi-code/skills -maxdepth 1 -name 'SKILL.md' | xargs grep '^version:' | sort
```

Returns **0 rows** on the live mesh because the skill directories nest one
level deeper (`/root/AAA/skills/<skill>/SKILL.md`). Use `-maxdepth 2` for
operational use. The `-maxdepth 1` form is correct only when the mesh is
flattened (skills as files directly under the tree root).

### 2. Placeholder versions are unparseable

A few files carry non-semver placeholders:

```
version: semver
version: {semver}
version: 1.0.0-2026.07.06
```

- `semver` / `{semver}` are linter placeholders, not real versions.
- `1.0.0-2026.07.06` is a date-suffixed dated version; the prefix is
  semver-compatible but the date suffix sorts oddly.

Treat these as **UNPARSEABLE → flag**, never silently equate.

### 3. `skill_linter.py` schema mismatches the catalog

The project's canonical linter (`/root/AAA/skills/skill-evolution/skill_linter.py`)
requires 14 invariant-schema fields (`purpose`, `owns`, `refuses`, `cause_class`,
`cost_class`, `tier`, `permissions`, `dependencies`, `precedence`,
`conflicts_with`, `contract`, `reversibility`, `owner_organ`, `accountability`)
that **no skill in the catalog currently carries.** Verified against
`FORGE-mcp-probe` (exits with the same 18 errors). The linter's `id` regex
(`^[A-Z][A-Z0-9-]+$`) rejects lowercase, but every catalog skill uses lowercase
kebab-case IDs. `--all` mode crashes (`AttributeError: 'list' object has no
attribute 'get'`).

**Treatment for a new catalog skill:**

- Match the parent spec's explicit field list (e.g. `id`/`version`/`owner`/`risk_tier`/`autonomy_tier`).
- Match the **surrounding house style** (FORGE-mcp-probe shape).
- Self-dogfood: verify the new skill is discoverable by its own §1 protocol.
- Do NOT retrofit the full 14-field contract schema on a single skill — that's
  scope creep and diverges from the catalog. The right fix is a catalog-wide
  linter/schema alignment, not a one-off departure.
- "Not passing lint" is a known artifact of an out-of-sync linter, not a defect
  in the new skill. Report it as such.

### 4. `aaa-drift-check.py` does NOT cover the mesh

`aaa-drift-check.py` checks `AAA/skills/*/SKILL.md` ↔ `skills.yaml` registration
(AAA-internal only). It does **not** compare AAA versions against
`~/.hermes/skills/` or `~/.kimi-code/skills/`. The mesh drift is invisible to
that script. Use `scripts/skill-mesh-probe.sh` (or the `AUDIT-agent-skill-mesh`
skill) instead.

## The report format

```
skill_name | AAA_version | hermes_version | kimi_version | status
-----------+-------------+----------------+--------------+----------------
FORGE-mcp-probe     | 1.0.0 | 1.0.0 | 1.0.0 | SYNC
AGI-skill-unification | 1.0.1 | 1.0.1 | 1.0.1 | SYNC
AUDIT-drift-detector | 2.0.0 | 1.0.0 | 2.0.0 | DIVERGED
AUDIT-agent-skill-mesh | 1.0.0 | — | — | MISSING_FROM_hermes, MISSING_FROM_kimi
```

Rules:
- One row per skill present in ≥1 tree (union).
- `—` for a tree that doesn't carry the skill.
- Sort by `skill_name`.
- Status is derived, never hand-typed.
- Exit-criteria one-liner: `N skills SYNC, M DIVERGED, K MISSING` — never "probably fine".

## How this skill came to be

Created via parent spec 2026-08-08. Parent mandated:
- exact `find … -maxdepth 1 | xargs grep '^version:'` command (we kept it as the canonical spec form, documented the operational `-maxdepth 2` variant)
- 5-column report format with `SYNC`/`DIVERGED`/`MISSING_FROM_X` status values
- escalation protocol (DIVERGED → flag → fix after >3 sessions; MISSING → propagate from AAA)
- frontmatter: `id: AUDIT-agent-skill-mesh`, `version: 1.0.0`, `owner: AAA`, `risk_tier: low`, `autonomy_tier: T1`
- standard liveness.json (6 canonical fields)

The skill was created, validated against its own §1 protocol (1 self-occurrence
in the 226-row mesh snapshot), and the surrounding-top-level count (281) was
recorded as the post-creation baseline.
