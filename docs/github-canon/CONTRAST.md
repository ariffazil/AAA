# CONTRAST — AAA GitHub Canon vs Other Agent Conventions

> **Generated:** 2026-06-24
> **Author:** FORGE (000Ω) — A-FORGE lane

---

## The Matrix

| Dimension | **AAA (arifOS canon)** | **Kimi Code** | **Claude Code** | **Grok Build** | **OpenAI Codex** | **GitHub Copilot CLI** |
|---|---|---|---|---|---|---|
| **Project instructions** | `AGENT.md` (singular) | `.kimi/AGENTS.md` or `AGENTS.md` | `CLAUDE.md` | `AGENTS.md` (assumed) | `AGENTS.md` | `AGENTS.md` (templates) |
| **Capability manifest** | `SKILL.md` (root) | `.kimi/skills/<n>/SKILL.md` | `.claude/skills/<n>/SKILL.md` | `skills/<n>/SKILL.md` | `codex.md` / `AGENTS.md` | Copilot-managed skills |
| **Execution loop** | `TASKS.md` | `.kimi/TASKS.md` (assumed) | (implicit in CLAUDE.md) | (implicit) | (implicit) | (implicit) |
| **GitHub skill count** | **12 explicit** | Scattered; 1-2 known | ~3 (PR/Issue/Action) | Undocumented | ~2-3 | ~5 (native GitHub APIs) |
| **Constitutional binding** | **F1-F13 enforced** | None | None | None | None | None |
| **Self-seal prohibition** | **YES (F1)** | NO | NO | NO | NO | NO |
| **F13 SOVEREIGN veto** | **YES — absolute** | NO | NO | NO | NO | NO |
| **VAULT999 audit trail** | **YES — hash-chained** | NO | NO | NO | NO | NO |

---

## Key Differences (Honest)

### 1. Constitutional binding
**Only AAA's canon binds GitHub actions to F1-F13.** Other tools treat git/GitHub as raw substrate.

### 2. Filename convention
- **AAA:** `AGENT.md` (singular) per sovereign ruling 2026-06-24
- **Claude Code:** `CLAUDE.md` — model-specific
- **OpenAI Codex / Copilot / Grok / Kimi:** `AGENTS.md` (plural)

AAA's singular is the **outlier** but reflects: one organ = one canonical agent.

### 3. Skill count
| Tool | GitHub skills | Granularity |
|---|---|---|
| **AAA** | **12** | One per cognitive dimension |
| Claude Code | ~3-5 | PR, Issue, Action |
| Copilot CLI | ~5-8 | Native GitHub API |
| Kimi / Grok / Codex | ~2-4 | PR + Issue + minimal |

### 4. Tools namespace
- **AAA:** canonical A-FORGE namespace `forge_github_*`, `forge_git_*`, `forge_shell_dryrun`
- **Claude Code:** native Bash + MCP
- **Copilot CLI:** `gh` CLI + GitHub API
- **Codex / Kimi / Grok:** model-specific

AAA's `forge_github_*` routes through A-FORGE lease + governance — most canonical and audited.

### 5. Audit trail
- **AAA:** every action seals to VAULT999 (hash-chained, append-only)
- **Other tools:** audit logs but no constitutional chain

---

## What AAA Borrows From Each

| Tool | Borrowed pattern |
|---|---|
| **Kimi Code** | Minimal frontmatter convention |
| **Claude Code** | Auto-loading project instructions → adapted as AGENT.md |
| **Grok Build** | (limited public info) |
| **OpenAI Codex** | Progressive disclosure for skills |
| **GitHub Copilot CLI** | `gh` CLI integration as fallback |

---

## What AAA Innovates

| Innovation | Why |
|---|---|
| **3-file invariant** (AGENT.md + SKILL.md + TASKS.md) | Removes model-specific fragmentation |
| **12-skill GitHub canon** | One skill per cognitive dimension |
| **Constitutional binding (F1-F13)** | No other tool makes git actions floor-checked |
| **VAULT999 seal for tags/releases** | Date-stamp tags are historical anchors, sealed forever |
| **Issue-as-intent** | Issues are units of governance, not tickets |
| **PR-as-hearing** | Constitutional framing changes PR review |
| **CI-as-doctrine** | CI is the non-human ASI conscience |
| **Main-as-canon** | main is federation's reality anchor |
| **Hash-as-memory** | Every action has content-addressed forensic anchor |

---

*Forge receipt: 2026-06-24 · A-FORGE lane · DITEMPA BUKAN DIBERI*
