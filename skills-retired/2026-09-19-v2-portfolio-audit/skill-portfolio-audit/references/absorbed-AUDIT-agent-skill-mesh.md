# Absorbed: AUDIT-agent-skill-mesh

> **Provenance.** Pre-merge body of the `AUDIT-agent-skill-mesh` skill, tombstoned 2026-09-16T22:42:00Z by Wave 2 (`moved_to: core/governance/skill-portfolio-audit/SKILL.md`).
> Recovered verbatim from `/root/.hermes@entropy-wave2-pre-act-20260916T144144Z:skills/AUDIT-agent-skill-mesh/SKILL.md` — content was never carried into the target by the
> original consolidation; recovered 2026-09-17 to complete the recorded merge.
> Original sha256 (tombstone `sha256_before`): `e42c1df82e812f54ca202658eeae9b417b1d1c8720e8053748400903b92a098c`
> Recovery sha256: `e42c1df82e812f54ca202658eeae9b417b1d1c8720e8053748400903b92a098c`
> The `AUDIT-agent-skill-mesh` routing name stays retired — this file is a reference, not a skill.

---

# AUDIT — Agent Skill Mesh Sync

> **Answers: "Are my agents in sync right now?"**
> **DITEMPA BUKAN DIBERI** — sync is verified, not assumed. Divergence is invisible until it causes a bug.

## What This Skill Is

A read-only protocol that compares the **core skill set and versions** across the
three agent skill trees in the federation:

| Tree | Agent | Path |
|---|---|---|
| AAA | Catalog (source of truth) | `/root/AAA/skills` |
| Hermes | Telegram bridge agent | `/root/.hermes/skills` |
| Kimi | Kimi Code agent | `/root/.kimi-code/skills` |

It does NOT copy, patch, or deploy anything itself. It lists, compares,
classifies, and escalates. **AAA is the catalog; Hermes and Kimi are views.**

## Trigger

Use this skill whenever you (or a sibling agent) need to answer:

- "Are my agents in sync right now?"
- "Did skill X get propagated everywhere?"
- "Why is an agent behaving differently from AAA?"

## §1. Compare command

Run this to list every `SKILL.md` with its declared version, per tree, sorted:

```bash
find /root/AAA/skills /root/.hermes/skills /root/.kimi-code/skills -maxdepth 1 -name 'SKILL.md' | xargs grep '^version:' | sort
```

**PITFALL (observed 2026-08-08):** on this mesh, skill directories nest ONE level
deeper (`/root/AAA/skills/<SKILL>/SKILL.md`), so the canonical `-maxdepth 1`
command returns **empty output**. Use `-maxdepth 2` for a live comparison:

```bash
find /root/AAA/skills /root/.hermes/skills /root/.kimi-code/skills -maxdepth 2 -name 'SKILL.md' | xargs grep '^version:' | sort
```

Observed scale: **281 SKILL.md bodies** across the three trees (AAA + Hermes +
Kimi). Note: a few files carry non-semver placeholders (`version: semver`,
`version: {semver}`, dated `1.0.0-2026.07.06` styles) — treat those as
**UNPARSEABLE → flag**, do not silently equate.

## §2. Health report format

After running the compare, emit a report with exactly these columns:

```
skill_name | AAA_version | hermes_version | kimi_version | status
```

Example:

```
skill_name               | AAA_version | hermes_version | kimi_version | status
-------------------------+-------------+----------------+--------------+----------------
AGI-skill-unification    | 1.0.1       | 1.0.1          | 1.0.1        | SYNC
FORGE-mcp-probe          | 1.0.0       | 1.0.0          | 1.0.0        | SYNC
skill-substrate-framework| 3.0.0       | 3.0.0          | —            | MISSING_FROM_kimi
AUDIT-drift-detector     | 2.0.0       | 1.0.0          | 2.0.0        | DIVERGED
```

Rules:
- One row per skill **present in ≥1 tree** (union of all three trees).
- `—` for a tree that does not carry the skill.
- Sort by skill_name. Status is derived, never hand-typed.

## §3. Status values

| Status | Meaning | Condition |
|---|---|---|
| `SYNC` | Skill present in all trees that carry it, same version everywhere | all versions equal |
| `DIVERGED` | Skill present in ≥2 trees with different versions | any version differs |
| `MISSING_FROM_X` | Skill absent from tree X but present in AAA (or another tree) | X ∈ {aaa, hermes, kimi} |

Edge cases:
- Skill in AAA only → `MISSING_FROM_hermes` + `MISSING_FROM_kimi` (two flags).
- Skill in Hermes+Kimi but NOT AAA → `MISSING_FROM_aaa` **and escalate as
  catalog drift** — AAA is the source of truth; a non-AAA orphan violates the
  catalog-first rule (see AUDIT-skill-atlas).

## §4. Escalation protocol

| Detection | Action | Owner |
|---|---|---|
| `DIVERGED` | **Flag** — log the row in the session report; no mutation | AUDIT agent |
| `DIVERGED` persisting **> 3 sessions** (observed on 3+ separate runs/health checks) | **Fix** — align the divergent tree(s) to the AAA version | A-FORGE (via forge execution) |
| `MISSING_FROM_X` | **Propagate from AAA** — copy AAA's `SKILL.md` (+ assets) into the missing tree, preserving the AAA version | A-FORGE (via forge execution) |
| `MISSING_FROM_aaa` (orphan) | **Flag + reverse-propagate** — bring the orphan into AAA first, then re-run | AUDIT agent → A-FORGE |

Fix steps (DIVERGED or MISSING, after authority granted):
1. Re-run §1 to confirm current state (do not fix from a stale report).
2. `rsync`/copy the AAA version into the target tree, or apply the version
   bump; never hand-edit versions in views.
3. Re-run §1; confirm the row flips to `SYNC` or is fully populated.
4. Record the receipt (before/after rows) in the session report.

## §5. Verification / exit criteria

A sync check is complete when:
- [ ] §1 command ran (with `-maxdepth 2` on this mesh)
- [ ] Health report emitted with all 5 columns, one row per union skill
- [ ] Every row carries one of: `SYNC` | `DIVERGED` | `MISSING_FROM_X`
- [ ] Each `DIVERGED` row is flagged; each `MISSING_FROM_X` row has a propagation target
- [ ] Answer to "are my agents in sync right now?" is a one-liner:
      `N skills SYNC, M DIVERGED, K MISSING` — never "probably fine"

## Pitfalls

- **`-maxdepth 1` returns empty** on this mesh — skill dirs nest one level deep. Use `-maxdepth 2` (see §1).
- **Placeholder versions** (`semver`, `{semver}`) are unparseable — flag, don't equate.
- **Dated versions** (`1.0.0-2026.07.06`) sort oddly — compare the prefix, not the date suffix.
- **Views drift silently** — Hermes/Kimi trees are populated by propagation, not by live symlink; a propagation that failed quietly shows up as `MISSING_FROM_X`, not as an error.
- Do NOT fix on first sight of `DIVERGED` — flag first; the >3-sessions rule exists to catch mid-flight propagation, not real drift.
