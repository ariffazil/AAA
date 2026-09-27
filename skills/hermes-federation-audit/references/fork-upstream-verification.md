# Fork-vs-Upstream Verification (hermes-agent fork lineage)

## When this fires

Any identity question whose answer hinges on the relationship between the local Hermes fork and its upstream — examples:

- "Are we following upstream?"
- "What's our divergence point?"
- "Is the local still in sync with Nous?"
- Any sovereign/audit probe that needs an honest answer about lineage, not a marketing claim.

This is a SUPPORT file to `hermes-federation-audit`. Do not duplicate the parent SKILL.md's 12-step probe order; this file only adds the FORK-SPECIFIC step that lives outside that list.

## The lie to avoid

Local commit count low + `git remote -v` showing an upstream URL + a stale `FETCH_HEAD` together produce a false sense of synchronization. None of them prove the local is current with upstream. A fork can sit diverged for months and still print a plausible-looking remote.

## Live probe order (do this and ONLY this)

Run all of these in one batched turn; do not interleave with narrative.

```bash
# 1. Count local commits on the active branch
git rev-list --count HEAD

# 2. Divergence from the configured origin (NOT necessarily upstream)
git rev-list --left-right --count main...origin/main

# 3. Is there a merge-base with the *real* upstream?
git fetch https://github.com/NousResearch/hermes-agent.git refs/heads/main 2>&1 | tail
git merge-base HEAD FETCH_HEAD   # if no common ancestor, diverged before fork

# 4. Upstream HEAD short SHA
git ls-remote https://github.com/NousResearch/hermes-agent.git refs/heads/main

# 5. Local first-commit date vs upstream first-commit date — proves divergence pre-fork if the diverged base is much later than upstream genesis
git log --reverse --format='%h %ad %s' --date=short | head -3
```

What each line tells you:

- `rev-list --count HEAD` — local depth
- `left-right main...origin/main` — `(ahead, behind)` — direction of drift; if `behind > 0`, local is stale vs the configured remote
- `merge-base` — empty/absent means the two histories share no common commit; the fork was created via copy or the histories diverged so far back the merge-base is lost
- `ls-remote upstream` — ground truth for upstream HEAD
- Log dates — sanity check that the local "initial" commit isn't secretly an upstream snapshot

## Reading the result (the four honest answers)

State ONE of these honestly — do not soften:

| Evidence pattern | Honest claim | Forbidden paraphrase |
|---|---|---|
| `merge-base` exists + `behind=0` | "synced with upstream" | OK |
| `merge-base` exists + `behind>0` | "forked, N commits behind upstream" | "we follow upstream" / "current with Hermes Agent" |
| `merge-base` ABSENT | "fully independent fork; no shared history" | "based on Hermes Agent" (vague enough to be misleading) |
| `FETCH_HEAD` older than 7 days | "FETCH_HEAD stale; recent claims about upstream state are UNVERIFIED" | "I know what upstream looks like" |

## Pitfalls

**1. Treating `git remote -v` as proof of relationship.** A URL in the remote list is configuration, not lineage. Two histories can share no commits and still both display a `hermes-agent` URL.

**2. Conflating `origin` with upstream.** `origin` is whatever the local repo calls "the configured remote" — it may be `ariffazil/HERMES` (a personal mirror), not `NousResearch/hermes-agent`. Always disambiguate before claiming.

**3. Reporting "we're still on Hermes Agent" without a `merge-base` line.** The phrase "based on Hermes Agent" survives in README and SOT-MANIFEST — and may still be literally true at the moment of the fork — but is dishonest if it implies ongoing inheritance. If `merge-base` is absent or the local has diverged past a known inheritance point, say "forked; lineage historical only."

**4. Skipping the `merge-base` step because it feels pedantic.** It is the SINGLE line that disambiguates "fork in maintenance mode" from "fork gone independent." The cost is one command; missing it produces a category-error verdict.

**5. Treating stale `FETCH_HEAD` as if it were a recent probe.** A `FETCH_HEAD` timestamp tells you when you last fetched, not what is currently true. If the timestamp is older than the conversation, refuse to make upstream-state claims and downgrade to UNKNOWN.

## Output contract (the field to put in /000 audit JSON)

When this fires inside a `/000 INIT` audit, populate `runtime.upstream_commit` AND add a sibling field:

```json
"runtime": {
  "hermes_version": "...",
  "local_commit": "...",
  "upstream_commit": "...",     // from `git ls-remote` of canonical upstream
  "lineage_relation": "synced | forked_n_behind | forked_independent | unknown",
  "merge_base_present": true,
  "behind_count": 0,
  "fetch_head_age_hours": ...
}
```

`lineage_relation` MUST be one of the four values in the table above. Anything else is fabrication.
