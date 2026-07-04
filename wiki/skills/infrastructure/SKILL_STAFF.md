---
title: "SKILL: Staff Engineer Code Review"
type: skill
version: 1.0.0
category: engineering
risk_band: LOW
floors: []
evidence_required: false
sources: [/root/.opencode/skills/staff-engineer-review/SKILL.md]
confidence: high
---

# SKILL: Staff Engineer Code Review

> **Source:** `/root/.opencode/skills/staff-engineer-review/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Reviewing pull requests
- Evaluating implementation against plans
- Architectural decision assessment
- Code quality evaluation
- Test coverage assessment
- Keywords: PR review, code review, pull request, architecture

---

## Review Workflow

### 1. Gather Inputs

- **PR Description** — The original plan and intent
- **Code Changes** — Diffs, files modified, commits
- **Additional Context** — Architecture docs, related PRs

### 2. Plan vs Implementation Alignment

| Check | Description |
|-------|-------------|
| Missing parts | Items planned but not implemented |
| Extra changes | Changes implemented but not planned |
| Partial implementations | Features started but not completed |

Document: ✅ Done, ⚠️ Partial, ❌ Missing, ➕ Extra

---

### 3. Architectural & Design Review

Assess:
- Separation of concerns
- Coupling and cohesion
- Consistency with existing codebase patterns
- Scalability implications

Identify:
- Design flaws or anti-patterns
- Overengineering or underengineering
- Hidden complexity
- SOLID/DRY violations

---

### 4. Code Quality Review

Check:
- Readability and clarity
- Naming consistency
- Function/class responsibilities
- Code duplication
- Edge case handling
- Error handling completeness
- Logging and observability

---

### 5. Correctness & Risk Analysis

Identify:
- Logical errors or questionable assumptions
- Potential bugs or edge case failures
- Missing input validation
- Race conditions or concurrency issues
- Security vulnerabilities (injection, auth, data exposure)
- Error handling gaps

---

### 6. Performance Considerations

Identify:
- N+1 query patterns
- Inefficient loops or operations
- Memory inefficiencies
- Unnecessary computations
- Missing indexes or caching opportunities
- Blocking operations in hot paths

---

### 7. Test Coverage Evaluation

Assess:
- Unit tests for new functionality
- Integration tests for component interactions
- Edge case coverage
- Happy path vs error path testing

---

## Output Format

```
### 1. Summary
- Alignment Score: 0-100%
- Overall Quality: Excellent/Good/Fair/Poor
- Risk Level: Low/Medium/High

### 2. Plan vs Reality
| Item | Planned | Implemented | Status | Notes |

### 3. Critical Issues
[High-impact problems with suggested fixes]

### 4. Improvement Opportunities
[Grouped by: Architecture, Code Quality, Performance, Tests]

### 5. Suggested Additions
[Missing features or logic]

### 6. Test Recommendations
[Specific test cases to add]
```

---

## Style Requirements

- Be precise and structured
- Avoid generic advice
- Focus on actionable insights
- Prioritize high-impact issues
- Reference specific files and line numbers
- State assumptions explicitly when unclear
- Balance pragmatism over perfection

---

## Related Pages

- [[skill-mcp-builder]] — building MCP servers
- [[skill-arifos-federation]] — federation architecture
- [[concept-tools-and-embodiment]] — engineering principles
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Code reviewed. Quality assured.*
