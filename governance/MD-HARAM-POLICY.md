# MD HARAM POLICY — No More Acah2

**Bound:** 2026-07-16 by F13 SOVEREIGN directive
**Rule:** Stop creating .md files that pretend to be important but aren't.

---

## HARAM (never create these)

| Pattern | Why |
|---------|-----|
| `*CONTRACT*.md` | Contracts are code, not prose |
| `*DOCTRINE*.md` | Doctrine lives in AGENTS.md, not separate files |
| `*MANIFEST*.md` | Manifests are JSON, not markdown |
| `*READINESS*.md` | Readiness is measured, not documented |
| `*ZEN*.md` | Zen is simple, not verbose |
| `*QUANTUM*.md` | Quantum is physics, not branding |
| `*INVARIANT*.md` | Invariants are tested, not written |
| `*WISDOM*.md` | Wisdom is demonstrated, not declared |
| `*TRILOGY*.md` | Trilogies are books, not architecture |
| `*HEPTALOGY*.md` | Heptalogies are philosophy, not code |
| `*FRAMEWORK*.md` | Frameworks are code, not documentation |

## ALLOWED (structural, keep creating)

| Pattern | Why |
|---------|-----|
| `SKILL.md` | Skill definition (code contract) |
| `README.md` | Directory header |
| `AGENTS.md` | Agent landing (one per repo) |
| `SOUL.md` | Agent identity (one per agent) |
| `IDENTITY.md` | Agent identity (one per agent) |
| `CHANGELOG.md` | Change log (one per repo) |
| `CONTRIBUTING.md` | Contribution guide (one per repo) |

## QUARANTINE (archive on sight)

Any .md file matching HARAM patterns gets moved to `.archive-YYYY-MM-DD/` in the same directory.

## ENFORCEMENT

```bash
# Pre-commit hook: reject HARAM .md files
# Add to .git/hooks/pre-commit:
if git diff --cached --name-only | grep -iE "CONTRACT|DOCTRINE|MANIFEST|READINESS|ZEN|QUANTUM|INVARIANT|WISDOM|TRILOGY|HEPTALOGY|FRAMEWORK" | grep "\.md$"; then
  echo "HARAM: acah2 .md file detected. Use code, not prose."
  exit 1
fi
```

---

**The rule:** If it's not SKILL.md, README.md, AGENTS.md, SOUL.md, or CHANGELOG.md — don't create it. Put it in code, JSON, or the existing AGENTS.md.
