---
name: code-security-static-auditor
description: Multi-stage automated code health, type-checking, linting, unit test coverage, and AST security vulnerability auditor combining Ruff, Pyright, Pytest, and Semgrep.
capability_tier: fed-long-context
ecology_state: WARM
---

# Code Quality & Security Static Auditor Skill (`code-security-static-auditor`)

Standardizes F8 Genius and F4 Clarity code quality checks across Python and TypeScript codebases.

## Unified Diagnostic Pipeline

### Pass 1: Syntax & Style Linting (`Ruff`)
```bash
uv run ruff check . --fix
```

### Pass 2: Strict Type Verification (`Pyright`)
```bash
uv run pyright
```

### Pass 3: Test Execution & Coverage Computation (`Pytest`)
```bash
uv run pytest -v --cov=. --cov-report=term-missing
```

### Pass 4: Security Vulnerability & AST Audit (`Semgrep` / `Bandit`)
```bash
uv run semgrep --config=p/security-audit .
```

---

## Best Practices for Federation Agents

1. **Zero Untested PRs**: Guarantee minimum 80% test coverage before submitting PRs or requesting 888 JUDGE seal.
2. **Deterministic Fixes**: Use `ruff check --fix` and `pyright` to resolve type errors before running tests.
