# Federation Skill Auditor — Specification

> **Status:** DRAFT  
> **Date:** 2026-06-23  
> **Authority:** ARIF directive `ARIFOS::AAA_FEDERATED_SKILL_ALIGNMENT::v1`  
> **Purpose:** Convert the skill-portfolio cleanup from manual inspection into an objective, repeatable, regression-testable auditor.

---

## 1. Why this auditor exists

We now have skills scattered across multiple scopes:

| Scope | Path |
|---|---|
| Kimi Code user-scope | `/root/.arifos/agents/kimi/skills/` |
| Project-scope | `/root/.agents/skills/` |
| AAA-scope | `/root/AAA/skills/` |
| OpenCode-scope | `/root/.arifos/agents/opencode/skills/` |
| HERMES-scope | `/root/HERMES/skills/` |
| arifOS-scope | `/root/arifOS/skills/` |
| WELL-scope | `/root/WELL/skills/` |

Without an auditor, entropy re-accumulates the moment we look away. The auditor is the objective function for skill hygiene.

---

## 2. What it audits

### 2.1 Structural hygiene

For every skill directory found in configured scopes:

| Check | Rule | Severity |
|---|---|---|
| `SKILL.md` exists | Required | ERROR |
| Frontmatter is valid YAML | Must parse cleanly | ERROR |
| `name` field present | Required, must match directory name | ERROR |
| `description` field present | Required, ≤ 400 chars | WARNING |
| `version` field present | Required | WARNING |
| `EXAMPLES_MD.md` exists | Required for promotion-ready skills | WARNING |
| `tests.md` exists | Required for promotion-ready skills | WARNING |
| `bindings/cli.yaml` exists | Required for CLI-hostable skills | INFO |
| No stray files at scope root | e.g., `software-development.md` flat file | WARNING |

### 2.2 Content quality

| Check | Rule | Severity |
|---|---|---|
| `description` is not vague | Reject words like "help", "assist", "improve" without object | WARNING |
| "Use When" section exists | Required | WARNING |
| "Do Not Use When" section exists | Required for high-risk skills | INFO |
| Trigger keywords are explicit | No hidden workflows in prose | INFO |

### 2.3 Cross-scope integrity

| Check | Rule | Severity |
|---|---|---|
| Duplicate `name` across scopes | Flag; suggest canonical owner | WARNING |
| Similar descriptions | Cosine similarity ≥ 0.85 → collision risk | INFO |
| References to quarantined paths | Any path containing `.quarantine-*` | ERROR |
| Broken internal links | `mem:`, `reference/`, relative `.md` links | WARNING |

### 2.4 Federation alignment

| Check | Rule | Severity |
|---|---|---|
| AGI/ASI constraint fields | If present, must include `mutation.class`, `blast_radius`, `approval_policy` | INFO |
| Risk tier consistent | `approval_policy: auto` must pair with `mutation.class: read_only` | WARNING |
| Authority order respected | Skill must not claim constitutional/judge authority | ERROR |

---

## 3. CLI interface

```bash
# Audit all configured scopes
python scripts/federation_skill_auditor.py

# Audit specific scopes
python scripts/federation_skill_auditor.py --scopes opencode,aaa

# Fail on ERROR severity (CI gate)
python scripts/federation_skill_auditor.py --fail-on error

# Output formats
python scripts/federation_skill_auditor.py --format markdown   # default
python scripts/federation_skill_auditor.py --format json       # machine-readable
python scripts/federation_skill_auditor.py --format github     # GitHub Actions annotations
```

## 4. Configuration

Config file: `/root/AAA/config/skill_auditor.yaml`

```yaml
scopes:
  kimi:
    path: /root/.arifos/agents/kimi/skills
    required_files: [SKILL.md, EXAMPLES_MD.md, tests.md]
    required_bindings: [cli.yaml]
  project:
    path: /root/.agents/skills
    required_files: [SKILL.md]
    required_bindings: []
  aaa:
    path: /root/AAA/skills
    required_files: [SKILL.md]
    required_bindings: []
  opencode:
    path: /root/.arifos/agents/opencode/skills
    required_files: [SKILL.md]
    required_bindings: []

severity_weights:
  ERROR: 10
  WARNING: 3
  INFO: 0

thresholds:
  max_errors: 0
  max_warnings: 10
```

## 5. Output format (markdown)

```markdown
# Federation Skill Audit — 2026-06-23T09:00:00Z

## Summary
- Scopes audited: 4
- Skills scanned: 140
- ERROR: 2
- WARNING: 12
- INFO: 34

## Findings

### ERROR — Duplicate skill name
| Skill | Scopes |
|---|---|
| `skill-trigger-linter` | project, aaa |

### WARNING — Missing EXAMPLES_MD.md
| Skill | Scope |
|---|---|
| `github-issues` | opencode |

## Rot classification
- doc-rot: 5
- trigger-rot: 2
- unused-rot: 1
```

## 6. Implementation notes

- Use `pathlib` for filesystem traversal.
- Use `pyyaml` for frontmatter parsing.
- Use simple string/token overlap for description similarity (no heavy ML needed).
- Keep it read-only by default; never move/delete files.
- Run in ≤ 5 seconds for the current portfolio.
- Exit code: `0` if under thresholds, `1` if exceeded.

## 7. Test cases

| # | Input | Expected |
|---|---|---|
| 1 | Skill dir without `SKILL.md` | ERROR |
| 2 | Duplicate `name` in two scopes | WARNING |
| 3 | Description contains only "help with X" | WARNING |
| 4 | Reference to `.quarantine-2026-06-23/` path | ERROR |
| 5 | Valid skill with all required files | No findings |
| 6 | Two skills with ≥ 0.85 description similarity | INFO |

## 8. Success criteria

The auditor is successful when:
1. It runs in CI on every skill-related PR.
2. It catches the 15 contrast-skill similarity cluster before a human does.
3. It prevents new skills from being added without `SKILL.md`.
4. Its findings match manual audit results ≥ 95% of the time.

## 9. Risk gating

- **READ_ONLY:** Running the auditor.
- **PROPOSE_ONLY:** This spec document.
- **GUARDED_WRITE:** Adding the auditor to CI or Makefile.
- **IRREVERSIBLE:** None.

## 10. Next action

Implement `scripts/federation_skill_auditor.py` and wire it into `/root/AAA/Makefile` as `make audit-skills`.
