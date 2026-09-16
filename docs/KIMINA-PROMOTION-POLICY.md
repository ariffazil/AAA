# KIMINA Promotion Policy — 5-State Lifecycle

> **Applies to:** Lessons, skills, repairs, capabilities
> **Authority gates:** Independence required for VERIFIED; 888_HOLD for constitutional

## States

```
CANDIDATE → QUARANTINED → VERIFIED → ACTIVE → REVOKED
```

| State | Who can write | What it means |
|---|---|---|
| CANDIDATE | Any agent (auto on failure pattern) | Unverified hypothesis |
| QUARANTINED | memory-curator (auto after ≥2 matching) | Isolated, not used, awaiting test |
| VERIFIED | aaa-verifier (different agent than author) | Passed reproduction + regression + independence |
| ACTIVE | aaa-coordinator (Arif for constitutional) | In production use |
| REVOKED | Any agent (auto on regression) | Caused regression, immediately removed |

## Gates (all must pass for VERIFIED)

| Gate | Test | Auto? |
|---|---|---|
| **Provenance** | Session, repo, tool, evidence known | ✅ |
| **Reproduction** | Claimed improvement reproduces from clean state | ✅ |
| **Regression** | Existing tests pass | ✅ |
| **Comparative** | Beats or matches baseline on defined metrics | ✅ |
| **Independence** | Different agent verified (C4 gate) | ✅ |
| **Safety** | Tool authority didn't expand | ✅ |
| **Human** | Constitutional/production change | ❌ 888_HOLD |

## What NEVER promotes

- Agent's own self-assessment ("I think this is better")
- Single successful run
- Same model reviewing its own answer
- Self-generated benchmark
- Unverifiable memory
- Test created only to mirror implementation

## Decay

- Environment-specific facts expire after 30 days unused
- Rank lowered after repeated non-use or failures
- Re-verify after dependency/provider/tool changes
- **Immediate revoke** when promoted lesson causes regression

## Scars as Promotion Memory

Scars are the inverse of promoted lessons — what NOT to do. The 25 sealed scars
from the federation are constitutional constraints, not suggestions. Any candidate
lesson that contradicts a sealed scar is auto-REJECTED.

DITEMPA BUKAN DIBERI ⚒️
