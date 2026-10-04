# Sibling Ops Report — Extended Verification Patterns (2026-08-08)

> Source: verify-sibling-ops-reports verification of Arif's AGENTS.md + opencode.json
> forge session 2026-08-08. Covers three failure modes the base skill does not
> address: multi-step sync claims, sealed-vs-committed conflations, and
> semantics-drift in self-chosen field names.

## 1. Three-tier verification ladder (edit + sync + render)

A sibling claiming "Card synced to dist/ and public/, AGENTS.md now contains …"
in one shot requires probing all three tiers, not one:

| Tier | What to check | How |
|---|---|---|
| Edit | field/value/line exists in canonical source | `grep -n "field" <canonical>` |
| Sync | claimed copies match canonical source | `diff -q <canonical> <claimed_copy>` for EACH destination |
| Render | downstream artifacts regenerated and consistent | `git diff --stat HEAD` in the repo |

**Common false positive:** sync to destination A verified, destination B not
probed. `public/` may be regenerated while `dist/` is stale — partial sync is
not sync. Don't reject the report; correct the tier and flag the probe gap.

## 2. Sealed ≠ Committed ≠ Rendered (three distinct states)

These are routinely conflated by sibling agents. Every report claiming
"done" or "sealed" should be graded on all three:

| State | Meaning | Probe |
|---|---|---|
| **Sealed** | VAULT999 receipt exists; kernel `arif_seal` ingest happened | `vault999-verify` or `grep <commit_hash> /root/VAULT999/outcomes.jsonl` |
| **Committed** | Git HEAD has a new commit | `git log --oneline -1` in the affected repo |
| **Rendered** | AGENTS.md / public/ / dist/ regenerated and consistent | `diff -q` against source |

**Example (2026-08-08):** Sibling wrote "both edits verified. AGENTS.md now
contains the full harness routing section." — `git status` showed modified
working tree with no commit. The report was **accurate for working tree only**.
Correct verdict: "T1 follow-up needed: commit not landed." Don't repeat "sealed"
back to the user.

## 3. Semantics-drift in self-chosen field names

When a sibling invents a new card field (not from an upstream schema), read
it **literally as every downstream consumer would**, not as the author
intended. If the field name implies deletion but existing artifacts persist,
flag the drift.

**Verified example:** `"replaces": ["codex","claude-code"]` on opencode.json.

- Author intent: "this routes first, those route second"
- Literal reading by A2A gateway: "codex and claude-code cards are obsolete"
- Actual state: vendor cards still exist, deletion explicitly forbidden
- Corrected phrasing: `"routing_priority": "PRIMARY"` + `"fallback_to": ["codex","claude-code"]`

Self-chosen field names are not audited by any schema validator — that's
your job as the verifier.

## 4. Per-claim grading table (extended)

When verifying a multi-part sibling report, use this table shape:

| # | Claim | Tier | Probe | Verdict | Action |
|---|---|---|---|---|---|
| 1 | edit opencode.json | rendered | `grep -n priority opencode.json` | ✅ L18 | — |
| 2 | sync to public/ | rendered | `diff -q canonical public/` | ✅ matches | — |
| 3 | AGENTS.md updated | rendered | `grep -n "Harness Routing" AGENTS.md` | ✅ L752 | — |
| 4 | commit landed | committed | `git log --oneline -1` | ❌ none | T1: `git add -A && git commit` |
| 5 | sealed (VAULT999) | sealed | `vault999-verify` | ❌ none | kernel ingest needed |
| 6 | field semantics safe | logical | `ls <claimed_replaced>` | ⚠️ vendor cards exist | rename `replaces` → `routing_priority` |

This produces the precise follow-up action (T1 auto-do or F13 hold) without
the user having to ask "but is it really done?"
