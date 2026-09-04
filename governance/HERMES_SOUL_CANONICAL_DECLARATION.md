# HERMES SOUL Canonical Declaration — 2026-09-04 (FI-003, F13 directive)

## Verdict
**SOUL.md truth = 13899 bytes (KVM8 /root/.hermes/SOUL.md, modified 2026-09-04 12:02 MYT)**

This is the LIVE kernel-rendered copy. It supersedes all prior 7625B / 13257B / 14436B
drafts as the single source of truth for Hermes identity.

## Single-owner rule
- **Owner**: hermes-asi kernel agent (F13 lane)
- **Render site**: arifOS kernel :8088 → /root/.hermes/SOUL.md
- **Distribution**: KVM8 + KVM4 must read this OR via kernel L0
- **No local copies**: `git log --diff-filter=D -- 'SOUL.md'` is the merge audit

## Drift history (4-way, now resolved to 1-way)
| Source | Size | Last touch | Status |
|---|---|---|---|
| KVM8 /root/.hermes/SOUL.md | **13899B** | 2026-09-04 12:02 | **CANONICAL** |
| KVM4 /root/.hermes/SOUL.md | 13257B | 2026-09-03 20:54 | Will symlink/fetch in Phase 4 |
| KVM8 /root/HERMES/SOUL.md | 14436B | 2026-09-02 | Archive on Phase 3 (reclaim) |
| KVM8 /root/Hermes/SOUL.md (shadow) | — | — | Quarantine on Phase 2 (now) |

## Reversibility
- `git revert HEAD` restores pre-declaration state
- Original 13899B SOUL.md untouched (kernel owns it)
- Decision is in doctrine, not in the SOUL itself

Refs: Hermes attention-theft remediation Phase 2.
