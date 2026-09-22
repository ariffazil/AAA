---
name: alert-inbox-triage
description: "Use when triaging an alert inbox for what's real."
version: 1.0.0
risk_tier: low
floor_scope: [F1, F2, F11]
autonomy_tier: T1
tags: [triage, mail, inbox, alerts, ci, notifications, signal]
triggers:
  - "read my mail"
  - "ada benda urgent"
  - "anything urgent"
  - "check my inbox"
  - "triage this"
  - "what needs my attention"
  - "inbox sweep"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Alert Inbox Triage

> An alert is a hypothesis someone else formed. Your job is the finding, not the forward.

## The one rule

**Never relay an alert's headline as the state of the world.** Open the referenced
run/commit/deployment and read the actual failing check before reporting anything. A notification
says a job went red; only the job's own output says why, and those two disagree often enough that
reporting the first is a defect, not a shortcut.

## Reading the principal's Gmail — the `mailread` lane

Read-only by construction: `send`, `forward` and `delete` are absent and require an F13 token.
Never offer to reply to mail from this lane; outbound is a separate lane. Doctrine:
`/root/AAA/instructions/mail-access.md`.

```
mailread check                     # diagnose access: socket, group, live read
mailread list [N]                  # latest N ids (default 5)   <-- POSITIONAL
mailread search "QUERY" [N]
mailread meta   MESSAGE_ID         # headers only
mailread body   MESSAGE_ID         # full body
mailread labels
```

**Pitfall — the count is positional.** `mailread list --limit 3` forwards `--limit` into the
broker's `--params` JSON and returns `Invalid --params JSON: invalid number`. Write
`mailread list 3`.

**Pitfall — `check` short-circuits for root.** Its group line reads
`group 'mailgw-clients': YES (uid 0 bypasses the check)` when run as root, so a passing `check`
proves the lane works *for this uid* and nothing about other citizens. Verify group membership
separately before claiming anyone else can read.

Attach actor and purpose so the receipt is meaningful:
```bash
MAILREAD_ACTOR=<agent> MAILREAD_PURPOSE="<why this read matters>" mailread list 25
```

## Procedure — a sweep

1. `check`, then `list N` with N >= 25. A 5-message window is not a sweep.
2. **Headers first, bodies last.** Loop `meta` over every id and keep only
   `Date / From / Subject / labelIds`. Load `body` for the handful of candidates only.
3. **Sort by sender before sorting by subject.** A human correspondent outranks every machine
   notification. If nothing in the window is human, that is the first sentence of the report — it
   answers "anything urgent?" more often than any individual alert does.
4. **Group machine alerts by timestamp before judging any of them.** A cluster landing within a
   few minutes across many projects/services is *one event* — an automated bulk push, a shared
   workflow change, a platform incident — not N independent failures. Find the common trigger
   before enumerating.
5. **Diagnose the top candidates.** `gh run view <id> --log-failed` returns mostly runner
   provisioning noise; grep it for the signal (`##[error]`, `Traceback`, the check's own verdict
   line) instead of reading it top to bottom.
6. **Reproduce locally where you can.** Running the same checker against the checkout turns a
   verdict into evidence and exposes false positives the remote log hides.

## Classifying what you find

- **Synchronized red across many repos** → look for one shared cause (a coordinated commit wave, a
  shared reusable workflow, a runner-image bump). Do not report it as N breakages.
- **A secret-scan gate red** → classify by detector *type* before reading any file.
  `Hex High Entropy String` / `Base64 High Entropy String` in `.json` artifacts (ledgers, receipts,
  agent cards, manifests, snapshots) are hashes and UUIDs, not credentials. Only credential-shaped
  detectors escalate: AWS Access Key, GitHub Token, Private Key, Slack/Stripe/Telegram token, Basic
  Auth. A step-change in count is usually a change in *scan surface* — a bulk merge, a backup or
  quarantine directory, a `*-retired/` tree — so count by top-level directory and compare the
  baseline's mtime against the surge. Fake tokens under `tests/` are fixtures.
- **A gate whose name says mandatory** → verify it in the branch's required status checks before
  calling it enforcement. See `enforcement-coverage-verification`: a gate name is a claim, the
  required-check list is the substrate.
- **A third-party deploy failure** → check whether the service is still referenced anywhere in the
  repos before escalating. An unreferenced hosted copy of something you already run locally is an
  abandoned experiment, not an outage. Say which reading you hold and what would settle it.

## Reporting to the principal

Answer-first, in his register: **is anything on fire — yes or no.** Then the one thing he could not
have seen on his own, then the single decision that is his. Do not enumerate everything you read;
the mailbox is not the deliverable, the triage is. Load `bridge-protocol` before composing.

Two hard boundaries on what you may clear yourself:

- **Do not paste third-party correspondence in full**, and mask anything credential-shaped.
- **Any change to the control that produced the alert is a decision, not cleanup.** Refreshing a
  scan baseline, widening an exclusion, or relaxing a threshold lowers sensitivity for every future
  commit and belongs to the principal as one binary ask. Fixing a *crash in the reporter* is yours:
  it changes no verdict and strictly increases what can be seen.

## Pitfalls

- **Reporting the alert instead of the finding.** "Secrets audit failed" is not a finding. "1,100
  hits, 1,048 are hex hashes in JSON ledgers, the only credential-shaped ones are fixtures under
  `tests/`" is.
- **Treating a count as evidence.** A scanner that prints `N findings` and then dies has told you
  nothing about the N. Read the list or say the verdict is unreadable.
- **Burying the answer.** The principal asked one question. An inventory of the inbox is not an
  answer to it.
- **Escalating a control change as a fix.** Clearing a red by relaxing the control is the one action
  that looks like progress and destroys the signal.
