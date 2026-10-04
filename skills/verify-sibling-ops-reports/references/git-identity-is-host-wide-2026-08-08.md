# Git Identity Is Host-Wide — The Commit-Provenance Anomaly Resolution

> Loaded when a sibling audit cites a "commit-provenance anomaly" — commits appearing under the operator's author key without an explicit `git commit` invocation in the visible session. Patched 2026-08-08 after the A-FORGE MCP surface diagnostic session proved the structural cause.

## The pattern

A sibling report (kimi-code/FI-008, A-FORGE surface diagnostic) flagged that three commits landed under its own author key within 60 seconds, with no `git commit` invocation visible in the audit session. The reflexive diagnosis is "another agent is using my key" — a serious F11 AUDITABILITY gap. **The real diagnosis is structural, not adversarial.**

## Why author identity is shared across all sessions on the host

The harness identity (e.g. `kimi-code/FI-008 <kimi@arif-fazil.com>`) is configured in **system-wide gitconfig**, not per-session:

```bash
cat /root/.gitconfig
# [user]
#   email = kimi@arif-fazil.com
#   name  = kimi-code/FI-008
#   signingkey = /root/.ssh/id_ed25519.pub
```

Every process on the host that runs `git commit` — without overriding `GIT_AUTHOR_NAME` and `GIT_AUTHOR_EMAIL` — commits under that identity. This is the **system default**, not an authentication boundary. Multiple sessions of the same harness (kimi-session-A, kimi-session-B, the shell behind a hermes session, a cron-driven forge-constitutional-sync, etc.) all produce commits with the **same author signature**.

## What git history tells you vs. what it doesn't

Git's `git log` records:
- ✅ **Identity** — author + committer name/email (per-commit, but shared system-wide on this host)
- ✅ **Timestamp** — `committer.date` with second-precision
- ✅ **Tree state** — what changed (via `git show`)
- ✅ **Commit message** — including trailers if any
- ❌ **Session ID** — git has no native notion of "which shell produced this"
- ❌ **Actor invocation** — git cannot tell whether the commit was explicit (`git commit`) or implicit (a hook, a script, an editor's autosave on a saved file, a `git -c commit.gpgsign=true ...` chain)

## How to triage a "commit-provenance anomaly" report

When a sibling or self-audit raises this, run this diagnostic in order:

```bash
# 1. Verify the commit is real (T0 source-of-truth)
git -C <repo> show --stat <sha> | head -10
# If the diff matches what the working tree shows, the commit is real.

# 2. Check whether the commit message references an explicit invocation
git -C <repo> log -1 <sha> --format=%s%n%b
# Look for: explicit `git commit` body, footer trailers (Signed-off-by, session-id, change-id)

# 3. Check system gitconfig for the shared identity
cat /root/.gitconfig | grep -A2 '\[user\]'

# 4. Look for cron/script sources that could have authored the commit
crontab -l 2>/dev/null | grep -i "git commit\|forge\|deploy"
ls /root/<organ>/duties/ 2>/dev/null
# For A-FORGE specifically:
ls /root/A-FORGE/duties/*.sh /root/A-FORGE/scripts/*.sh 2>/dev/null
grep -l "git commit\|GIT_AUTHOR" /root/<organ>/duties/*.sh 2>/dev/null

# 5. Look at the working tree at the start of *your* session
git -C <repo> status -s
# If `M` or `??` entries exist that you did not produce, those came from a prior session
# that exited without committing. The committed state in HEAD is the canonical record.

# 6. Check git reflog — does it show the commit was a normal "commit" action?
git -C <repo> reflog -3
# Pattern: HEAD@{N}: commit: <subject> = explicit invocation
# Pattern: HEAD@{N}: update by push = fetch/push, not local commit
```

## The T0/T1/T4 path for an unknown-author commit

Apply the 3-state verification pattern, with one extra tier:

| Tier | Question | Verifier |
|---|---|---|
| **T0** | Is the commit real? Does the diff match what the working tree shows? | `git show --stat <sha>` |
| **T1** | Was the commit produced by a sessioned, explicit invocation? | Reflog + commit message body + trailer presence |
| **T4** | Is the change independently verifiable against live runtime? | Probe `/health`, run the tool, check the artefact |
| **NEW — T_sess** | Which session produced this? | Cross-reference timestamp against cron log + session DB (Hermes `session_index.jsonl`, kimi `sessions/`) |

A commit that scores T0+T4 but T_sess=UNKNOWN is **trustworthy content, untraceable session**. The right move is to **trust the change and harden the audit trail** — not to roll back a working commit because you can't prove who did it.

## Worked example (A-FORGE surface diagnostic, 2026-08-08)

Three commits appeared under `kimi-code/FI-008 <kimi@arif-fazil.com>` between 09:06 and 09:08 UTC:

```
c625806f  2026-08-08 09:06:16  fix(MCP-PROBE-2026-08-08): add authority_ceiling to A-FORGE-bridge /health
e1eb1d4f  2026-08-08 09:07:59  feat(MCP-PROBE-2026-08-08): add make deploy-local + verify
72b42e86  2026-08-08 09:08:11  chore(affordances): mark 3 stale entries DEPRECATED
```

The hermes session that received the diagnostic had **only produced `72b42e86`** (visible in its own tool-call log). The other two commits were inherited — they landed before the hermes session started, by a prior kimi session that exited without committing and whose working tree the hermes session inherited.

Diagnostic outcome:
- All three commits have **T0 source-verifiable diffs** (the changes are real and match the current working tree)
- `72b42e86` has **T1 invocation-verifiable provenance** (this hermes session ran `git commit` explicitly)
- `c625806f` + `e1eb1d4f` have **T1 attribution gap** — same identity, different session, no session_id trailer
- All three have **T4 independence** — the bridge `/health` change is verifiable via `curl`, the affordance deprecation is verifiable via `grep`, the deploy-local script is reproducible
- **ΔS reconciliation:** the audit's −1.10 claim collapses to the real −0.15 because the unaffiliated commits were not produced by the audit session

The right resolution: **trust the content, surface the audit-trail gap as a finding, propose a fix** (session-id trailer on every commit). Don't roll back.

## The fix — session-id trailer on every commit

The cheapest patch is a git hook that auto-appends a session identifier:

```bash
# /root/.gitconfig OR a per-repo .git/config [commit] section
# Append session-id trailer via prepare-commit-msg hook

# /root/<repo>/.git/hooks/prepare-commit-msg  (or global core.hooksPath)
SESSION_ID=$(cat /root/.arifos/agents/kimi/sessions/current 2>/dev/null || echo "host-$(hostname)")
echo "session-id: $SESSION_ID" >> "$1"
```

For hermes sessions, the session id is already exposed via `SESSION_ID` env var (or construct from `/proc/<pid>/comm`). For kimi sessions, it's `wd_<hash>` in `/root/.arifos/agents/kimi/sessions/`.

A `git log --grep="session-id:"` then lets you audit which session produced any commit. This is the **F11 AUDITABILITY hardening** that the existing git identity system cannot provide on its own.

## When this finding IS a real attack

The pattern only becomes a security concern when:

- The system gitconfig is mutable from a non-harness user (e.g. an external agent can write `/root/.gitconfig` or set `GIT_AUTHOR_NAME`)
- An attacker has filesystem write to a cron entry that runs `git commit`
- The signing key (`signingkey = /root/.ssh/id_ed25519.pub`) is in a location reachable by an unauthorized process

None of these apply on the arifOS federation box by default, but they should be checked before declaring the system safe. The diagnostic above (steps 1-6) is the minimum bar.

## Cross-references

- `references/sessionless-probe-gaps-2026-08-08.md` — the SESSION_REQUIRED / POLICY_DENY pattern that this extends
- `references/forge-report-verification-3state.md` — the modified ≠ committed ≠ sealed doctrine
- `arifos-collapse-vector-audit` — sibling security-claim audit pattern (N3/N4 verification)
- `agent-fork-governance` — when multiple identities touch the same repo, the audit trail question is the same class
- `kernel-security-claim-audit` — the Ed25519-vs-HMAC trap that masquerades as this anomaly in some reports