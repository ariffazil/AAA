# State-Stale & Already-Done Sibling Claims (2026-08-08)

**Pattern class:** Sibling audit/proposal arrives referencing state that's already moved — either deployed mid-session or completed in earlier commits. The correct reflex is re-probe, not "do the work."

**Adjacent to** `fabricated-seal-receipt-pattern-2026-08-08.md` but distinct: the sibling is not lying — it's working from a stale snapshot.

## Pattern 1 — "Patch drift first" but drift is gone

Sibling claimed: "Kernel DEGRADED — source (2657104) != built (cb5afef). Patch first, ship second. ACK_M8_DEPLOY_CANONICAL."

```bash
curl -sf http://127.0.0.1:8088/health | python3 -c "
import json,sys
d=json.load(sys.stdin); sr=d.get('software_release',{})
print('status:', d.get('status'))
print('source==deployed:', d.get('source_commit','')[:7]==sr.get('deployed_commit','')[:7])
print('drift_status:', d.get('deployment_drift_status'))
"
```

If `status: healthy`, `drift_status: aligned` → deploy already landed. The snapshot is stale. Refuse the work, paste the receipt.

## Pattern 2 — "Three new proposals" that are already committed

Sibling presented 3 synthetic proposal IDs (`init-20260808-1535f2add2`, etc.) marked "Pending." The actual work was in commits `c7c12ed4` + `2a64c37e`.

```bash
grep -rl "<proposal-id>" /root/AAA/ /root/forge_work/ 2>/dev/null
# → 0: IDs are synthetic; sibling hasn't verified its own tree
git -C /root/AAA log --oneline --all | head -10
# → look for matching commit messages
```

**Distinguishing markers:** synthetic IDs with timestamps; "Pending" when files exist on disk; proposing slash commands that already exist in `OPENCLAW_SLASH_COMMANDS.md`.

## Pattern 3 — Naming drift: `/propose-seal` vs `/request-seal`

Sibling's skills used `/propose-seal`; canon (`c7c12ed4`) used `/request-seal`. Same pipeline, different surface names.

**Resolution options:**
1. Add alias mapping in canonical doc (if surface scopes differ — skill human-facing, slash command bot-facing)
2. Rename sibling files in follow-up commit (if integrity outweighs compatibility)
3. Block merge until reconciled (if drift isn't cosmetic)

## Pattern 4 — Two siblings committing overlapping files

Two siblings (`2a64c37e` for 9 skills, `48fd9171` for 3 prompts) wrote to the same repo in parallel.

```bash
git -C /root/AAA merge-base <commit-A> <commit-B>
# Empty → parallel branch (needs merge)
# Ancestor hash → linear history, both valid
git show <commit-A> --name-only
git show <commit-B> --name-only
ls -la /the/files/they/both/touched
```

If both are in HEAD's ancestry, both are valid. If only one is in HEAD, the other needs merge or rebase. Audit for additive, not destructive — if B rewrote A, that's a conflict.

## Verification Recipe

```bash
# 1. Re-probe live state
curl -sf <endpoint>/health | jq '.'
# 2. Check file/dir the sibling claims to operate on
ls -la /the/path && git -C <repo> status -s /the/path
# 3. Check commit history for the work
git -C <repo> log --oneline --all -10
```

| Sibling claim | Live state | Action |
|---|---|---|
| "Drift detected, patch first" | `drift_status: aligned` | Refuse with receipt |
| "Three new proposals pending" | Files exist in HEAD | Refuse, point at existing commit |
| "Renaming X to Y" | X and Y coexist, different scopes | Decide canon or alias |
| "Deploying change Z" | Z already in deployed_commit | Refuse with timing evidence |

**Iron rule:** the sibling's snapshot is a claim, not state. State is the live probe. Always re-probe.
