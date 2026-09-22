---
name: mailbox-triage
description: "Use when triaging an inbox for what needs the principal."
version: 1.0.0
risk_tier: low
floor_scope: [F2, F4, F7, F11]
autonomy_tier: T1
tags: [mail, gmail, mailread, triage, inbox, urgency, human-interface]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Mailbox Triage

Class: the principal asks some form of *is anything urgent in my mail* — or repeats it later as
*refresh*. The deliverable is not a message list. It is a **severity verdict**: what needs him,
what does not, and which of it originated from a person.

Read-only throughout. The governed read path has no send/forward/delete by construction, so nothing
here can mutate the mailbox — do not go looking for an approval gate you will not use.

## 0. Mechanism and access live elsewhere

**Reading is not this skill.** The token-custody broker, the `mailread` wrapper, group membership,
granting access to another identity, and the boundary's known limits are documented in
`google-workspace-gws` (section *Reading Gmail — use `mailread`*) and
`/root/AAA/instructions/mail-access.md`. Load those for access work. This skill starts once you
can read.

`mailread check` answers *can I read?* — exit 0 ok, 2 not in group / socket denied, 3 broker down.
Run it first when anything looks wrong.

## `mailread` invocation pitfalls

All four are invocation shape, not broker faults. Each cost real calls when skipped.

1. **The count is POSITIONAL, never a flag.** `mailread list --limit 5` fails with
   `Invalid --params JSON: invalid number at line 1 column 30` — arguments are forwarded into a
   Google `--params` JSON blob, so a `--flag` form is consumed as a numeric field and the parse
   dies. Write `mailread list 5` and `mailread search "<query>" 20`.
2. **The output is NOT clean JSON.** Every call is prefixed with a banner line
   (`Using keyring backend: keyring`), so `json.load` on stdout raises
   `Extra data: line 1 column 14`. Parse from the first brace:
   `json.loads(out[out.find('{'):])`. **A parse error here is the banner, not a broken lane** —
   do not report the mail path down off it.
3. **`MAILREAD_PURPOSE` has an 8-character minimum.** A terse value is refused with
   `{"status": "PURPOSE_REQUIRED", ...}`. Always set a full sentence naming why the read matters —
   that is also what makes the receipt worth anything later.
4. **Do not pipe `mailread` into an interpreter inside one shell string.** The safety scanner
   flags pipe-to-interpreter, and nested shell-to-python quoting mangles bracketed regexes. Write
   the helper to a file, then run it. `scripts/mail_triage.py` already does this.

Set `MAILREAD_ACTOR` and `MAILREAD_PURPOSE` in the environment rather than relying on defaults
whenever the read is for a reason worth recording.

## Procedure

### 1. Establish the window before reading

The question is *since when*. Read the clock, then pull a bounded page and report the window it
covers. A list with no window cannot be judged urgent or not — and on a mailbox that is mostly
machine mail, a page of 25 can still be under a day.

### 2. Pull headers in a batch, to a file

```bash
python3 scripts/mail_triage.py 60     # ids -> header rows -> /tmp/heads.jsonl
```

Headers (`From`, `Subject`, `Date`, `labelIds`, snippet), never bodies, for the first pass. Bodies
only for ids you decide are candidate-urgent — a body is the expensive read and the one that
contains other people's private content. Fetch in batches that append rather than one mega-call, so
a timeout does not lose the pass.

### 3. Classify by SENDER, not by subject

This is the step that turns a list into a verdict, and the one most easily skipped.

| Class | Signal | Default urgency |
|---|---|---|
| **Human** | a person's name or personal address in `From` | read the body, judge individually |
| **Machine — project CI** | own repos' automation, build/repo notifications | digest only; never "urgent" |
| **Machine — external status** | hosting/deploy failures, quota, paused services | check whether the thing is supposed to be live |
| **Machine — commerce** | receipts, invoices, newsletters | never urgent |
| **Security/account** | bank, provider, credential, breach notices | highest machine class |

**The primary answer is almost always "no human wrote".** Establish that explicitly — it is the
finding, not the absence of one. On a mailbox dominated by your own infrastructure's notifications,
the honest verdict is that the mail is a mirror of machine chatter.

### 4. Collapse to a short severity list

Order by *consequence to the principal*, not by arrival: real-world blocking (money, credentials,
an external obligation); something he believes is running that is not; a gate of his own that is
red; noise worth one line.

### 5. When CI/automation mail is in scope, name the failing STEP

A red pipeline notification is not a diagnosis. Before repeating it as a finding, resolve the run
to its failing job and step, and say which one it was — *secret-scan*, *lockfile invariant*, *lint*,
*contract drift*, *governance gate*. A list of seven red repos is noise; five distinct named cause
classes with an owner is a work list.

Also check whether a red item is already stale: a lane that was transiently down and recovered
before you read the mail is not a live finding. State the recovery.

### 6. Report the DELTA on a refresh

`refresh` means *what changed since the last pass*, not *re-run the whole report*. Name the new
arrivals and the count, restate the standing verdict in one line, and stop. Reproducing the previous
answer in full teaches him to stop asking.

## Reporting register

The reply is a verdict, not a table of messages. Its rules belong to `federation-state-report`
(section *Reporting shape (Arif)*) — in particular: **do not assemble the account out of component
names.** A sentence built from service names, schema fields, or checker vocabulary is illegible
even when every word is correct, and the correction you will receive is a request to re-explain in
human terms.

- Lead with the verdict: does anything here need him. Then the few items, then one bounded decision.
- Translate each finding into consequence before mechanism.
- Keep senders, subjects and ids in the trace, not the prose.
- A mailbox with nothing human in it is a *quiet* result. Say so plainly; do not manufacture
  urgency out of machine chatter to justify the read.

## Do not

- Do not open bodies across the whole page. Other people's mail is not the deliverable.
- Do not describe the mailbox as a monitoring channel for the principal's own CI. Its mail is
  notification traffic, not a health surface; use the state-report probes for that.
- Do not claim the lane is healthy beyond what you read. Reading inbox headers proves the *read*
  path; it says nothing about send.

## Support files

- `scripts/mail_triage.py` — bounded header pull (ids → JSONL) that tolerates the keyring banner
  and sets a compliant actor + purpose.
