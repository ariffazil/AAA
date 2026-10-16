# Forge Queue — Claude Code FI-002, next session

Forged 2026-10-15 by kimi-code / FI-008 · Node KVM8 · owner FI-002 (claude-code-kvm8)
Queue position: next Claude Code session. Every item is T1/T2 reversible unless marked.

**Standing rules for this queue (from the 2026-10-15 shadow audit):**
- Probe before you claim. Every number below is a *starting hypothesis* — re-probe before you assert it.
- The `mcp__claude_ai_*` namespace does not exist. It is disabled on this machine. Never call it.
- Delete = move to `_to_delete/`. Never `rm`.
- Anything public, pushed, deleted, secret, kernel-level or service-restarting stops at the last step and lands under MENUNGGU ARIF with the exact command.
- One runnable artifact per item. A report is not a deliverable.

---

## Q1 · arifos-motd notice board
**Lane:** T1 · **Owner:** FI-002
Build a machine-readable notice board on KVM8 that writes local `reality.json`.

Hard requirements:
- **Exceptions only.** No entry means "all nominal" — silence is the healthy state, not an announcement.
- **Zero emoji.** No decorative glyphs anywhere in the payload.
- **No IP, no hostname, no username, no FQDN.** Local-only surface; strip anything identifying before writing.
- **2 second timeout on every probe.** A slow organ is a missed beat, never a hang.
- **Exit 0 on success, exit 0 on "an organ is down but the board still wrote".** Non-zero only if the board itself cannot be written.
- Writer must be **KVM8 local reality.json** — the board projects live `/health`, it does not cache.

Acceptance: run it; show the file; kill one organ and show the single exception line appears. Kill and restore in the same run.

---

## Q2 · MCP site diff (mcp.arif-fazil.com)
**Lane:** T2 · **Publish: FORBIDDEN.** Produce a diff only, nothing leaves the box.

Fix in the source:
- Remove the phrases **"is impossible"** and **"with cryptographic proof"**.
- Floor headline must follow live `/health` — render from the organ, never from a constant.
- Unify the **F5** name (one canonical label, one spelling, across every surface).
- Check the **transport label** — it must match the real transport the page claims.

Acceptance: a diff file with line numbers + the live `/health` value the headline would now render. No push, no deploy.

---

## Q3 · AAA site + arifOS site diffs
**Lane:** T2 · **Publish: FORBIDDEN.** Diffs only.

Both sites, same discipline:
- **LIVE gate on freshness.** If the underlying data is older than its stated threshold, render the staleness — never render the stale number as if it were current.
- **Exactly one object HOLDS the definition.** Two sites defining the same floor is a contradiction; one defines, the other links.
- **Ed25519 scope wording** must state what is actually signed, not more.
- Remove **"Arif bukan coder"** and all emoji from the public copy.
- Floors render from live `/health`, not from a checked-in table.

Acceptance: both diffs written, freshness threshold named, the single definition-holder named per object.

---

## Q4 · KVM8 disk at 82%
**Lane:** T1 · **READ ONLY.** No deletes, no moves, no `du`-and-prune.

Produce: top consumers by directory with real numbers, plus the growth rate of the top 5 over the last 7 days if the data exists. Flag what is safe to prune vs what is evidence (session logs, receipts, VAULT999) and say which is which.

Acceptance: a ranked table with measured sizes and one recommendation line per entry. No mutation.

---

## Q5 · WELL — legacy callers + the swapoff precondition
**Lane:** T2 for callers, **T3 for the swapoff fix** (branch only, never run).

Two parts:
1. **Find every legacy WELL caller** predating 2026-10-16. List them with file:line and the exact call signature each one uses. No rewriting yet — inventory first.
2. **Fix the `swapoff` precondition on a branch.** The known unsafe behaviour: WELL recommended `swapoff` while 18.6 G swap was in use with 15 G RAM free. Correct the *precondition check*, not the recommendation text. Commit to a local branch. **Never execute `swapoff`. Never execute the branch.**

Acceptance: caller inventory committed; the corrected precondition committed on a branch with the old logic quoted in the commit message so the diff is reviewable.

---

## Q6 · plugin87 — pin a commit + overlap map
**Lane:** T1/T2

1. **Pin plugin87 to an exact commit SHA.** Record the SHA and the date it was taken in the repo that declares it. A floating tag is not a version.
2. **Write the overlap map** of plugin87's skills against the AAA design skills. For each skill: `identical` / `partial` / `duplicate` / `unique`, with the AAA canonical owner named. Where plugin87 is better, say so — the map is for deciding what to keep, not for justifying deletion.

Acceptance: pinned SHA in a committed file; overlap map as a table with one row per skill and a canonical owner column.

---

## Q7 · Follow-ups carried from the 2026-10-15 shadow audit
**Lane:** T1 · low effort, high honesty value

- `ANTHROPIC_MODEL=forge-777` triggers `[claude-code:unrecognized_model]` on every single run. Determine whether FED `:4000` actually serves that alias, or whether Claude Code is silently falling back. **Probe, do not assume.**
- `settings.json` has `"plugins": {"arifos-federation": true}` but the plugin is never installed — a no-op declaration. Either install it (after resolving the hook duplication in audit §4) or remove the line. Do not leave a lie in config.
- Measure real always-on context with `/context` and replace the bytes-based estimate recorded in the audit.
- `:3001` (AAA) and `:18083` (WELL) both report `degraded` on live `/health`. Find out which field is degraded before anything is written about it.