---
name: security-audit
id: security-audit
version: 1.0.0
description: >
  Static analysis + README truth checking. Multi-stage automated code health,
  type-checking, linting, unit test coverage, and AST security vulnerability auditor.
  Verify that repo READMEs accurately describe current structure, ports, dependencies,
  and authority boundaries.
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope: [F1, F2, F4, F7, F9, F10, F11]
tags: [security, static-analysis, ruff, pyright, pytest, semgrep, readme, truth-check, audit]
capability_tier: fed-long-context
ecology_state: WARM
---

# Security Audit — Static Analysis & README Truth Check

> **DITEMPA BUKAN DIBERI** — Code quality and documentation truth are verified, not assumed.

## What This Skill Is

A unified security and documentation audit skill covering:

1. **Static Analysis** — multi-stage automated code health, type-checking, linting, unit test coverage, and AST security vulnerability auditing
2. **README Truth Check** — verify that repo READMEs accurately describe current structure, ports, dependencies, and authority boundaries

## When to Use

- Before submitting PRs or requesting 888 JUDGE seal
- After any reorganization
- Before releasing a new version
- When onboarding a new developer
- Quarterly doc audit
- "Security audit", "code quality", "static analysis", "README check", "doc drift"

## When NOT to Use

- Runtime health checks (use `verify-work`)
- Incident response (use `incident-response`)

## §1. STATIC ANALYSIS — Unified Diagnostic Pipeline

### Pass 1: Syntax & Style Linting (Ruff)

```bash
uv run ruff check . --fix
```

### Pass 2: Strict Type Verification (Pyright)

```bash
uv run pyright
```

### Pass 3: Test Execution & Coverage (Pytest)

```bash
uv run pytest -v --cov=. --cov-report=term-missing
```

### Pass 4: Security Vulnerability & AST Audit (Semgrep / Bandit)

```bash
uv run semgrep --config=p/security-audit .
```

### Best Practices

1. **Zero Untested PRs**: Guarantee minimum 80% test coverage before submitting PRs or requesting 888 JUDGE seal.
2. **Deterministic Fixes**: Use `ruff check --fix` and `pyright` to resolve type errors before running tests.

## §2. README TRUTH CHECK

READMEs become stale quickly. This skill compares the README's claims against the actual repo state and flags discrepancies.

### Step 1: Directory Structure Check

Compare README's directory tree against `ls -la`. Flag:
- Phantom directories (in README, not on disk)
- Missing directories (on disk, not in README)
- Renamed directories

### Step 2: Port/URL Check

Compare README's claimed ports/URLs against reality:
- `ss -tlnp` for listening ports
- `curl` for HTTP endpoints
- `systemctl status` for services

### Step 3: Dependency Check

Compare README's claimed dependencies against `package.json`, `pyproject.toml`, etc.

### Step 4: Authority Check

Verify README does not claim constitutional authority incorrectly.

### Output

```markdown
## README Truth Check: <repo>

### Structure Drift
- [ ] Phantom: `agent/` (README) vs `agents/` (disk)

### Port Drift
- [ ] Claimed: GEOX 18081 — Actual: 8081

### Dependency Drift
- [ ] None / [list]

### Recommendations
1. Update README directory structure — P1
```
