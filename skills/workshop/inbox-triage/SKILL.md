---
name: inbox-triage
description: Use when asked to read mail or flag what is urgent.
version: 1.0.0
author: hermes
license: proprietary
tags: [mail, gmail, mailread, triage, inbox]
floor_scope: [F1, F2, F13]
autonomy_tier: T1
metadata:
  hermes:
    tags: [mail, gmail, mailread, triage, inbox]
    related_skills: [email-outbound]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Inbox Triage — Reading Mail and Deciding What Needs the Human

Class-level skill for "read my mail", "check my inbox", "ada benda urgent?", "is Gmail ready".
The deliverable is not a message list — it is a decision: what needs him, what merely needs to be
known, and what is machine noise.

## Route by direction first

Sending mail is a different lane (Brevo / governed send — see the `email-outbound` skill). Reading
mail never needs Brevo, OAuth consent, or a new credential. Do not open outbound work for a read
task, and do not read a stale "Gmail is down" claim as covering the read lane — name the lane
(OAuth bridge vs broker socket) before declaring any capability absent or present.

## The read lane is `mailread`

`mailread` (`/usr/local/bin/mailread`) wraps the Token-Custody Broker. Read-only by construction:
no send, forward or delete exists on this lane for it to leak through.

```bash
mailread check               # diagnose: identity, group, socket, client, live read
mailread list [N]            # latest N message ids (default 5)
mailread search "QUERY" [N]  # Gmail search syntax, same positional shape
mailread meta MESSAGE_ID     # headers only (from / subject / date / labels)
mailread body MESSAGE_ID     # full body
mailread labels              # label inventory
```

`mailread --help` is authoritative on the whole contract; read it before improvising flags.

## Gates and lane facts

- **Arguments are POSITIONAL, never flags.** `mailread list --limit 5` dies with
  `error[validation]: Invalid --params JSON` — the wrapper forwards unrecognised args as the raw
  Gmail params blob, so a `--flag` becomes malformed JSON. Write `mailread list 5`.
- **Purpose gate:** `MAILREAD_PURPOSE` must be a specific falsifiable sentence, minimum 8
  characters. A one-word `probe` is refused (`PURPOSE_REQUIRED`). The purpose is what makes the
  read auditable — write it as if the witness, not you, will read it.
- **Access** = membership in group `mailgw-clients` (uid 0 bypasses the check). Broker socket
  `/run/mailgw/broker.sock`; units `mailgw-broker.service`, `apa-gmail-bridge.service`,
  `apa-email-bridge.service`.
- **Readiness ≠ config present.** Before answering "is Gmail ready", prove it end to end:
  `mailread check` → a real `mailread list N` (live ids + `nextPageToken`) → one `meta` (headers
  resolve). Services showing `active (running)` proves nothing on its own.
- **Never claim a mailbox is empty from a failed read.** No data ≠ all clear; it means you could
  not witness.

## Parsing rule

The `Using keyring backend: keyring` banner is on the wrapper's **stderr**. If you pipe with
`2>/dev/null` and then strip line 1 to remove that banner, you delete the opening `{` and parsing
dies (`Extra data: line 1 column 14`). Locate the first `{` in stdout and parse from there — never
line-strip.

One `meta` call per message id; there is no bulk endpoint behind the wrapper. Use
`scripts/mail_triage.py` for batch pulls instead of hand-looping.

## Triage is collapse, not relay

- **Answer the question in the first line.** "Tak ada yang urgent dari manusia" is a complete
  answer, not a preamble to one.
- **State the window you actually covered** ("60 mesej, 20 Sep 17:54 → 23:33"). A mailbox of 200+
  messages is not read by reading its latest 60 — never imply otherwise, and sweep older mail
  (`search "in:inbox is:unread newer_than:7d ..."`) before declaring it clean.
- **Rank by consequence:** infra/service down > money > personal > vendor noise. Everything that is
  not urgent gets one clear line saying so.
- **Report state, not the email.** Verify a reported failure before repeating it — an email saying
  a run failed is REPORTED, not OBSERVED, and you must say which one you are handing over.
- **Collapse the vendor tail** into a sentence; name only the notable ones.
- **Close with ONE recommendation** in his register plus a stop-check ("cakap kalau nak aku hold").
  Never a menu, and never hand the triage work itself back to him — the reading is yours, the
  deciding is his.
- No tables, no bullet-per-message. Short lines, bold for names and services.

## Pitfalls

- `gh run view --log-failed` on an unnamed workflow step prints `UNKNOWN STEP`, and its tail can be
  pure post-job teardown (git config removal, "Cleaning up orphan processes"). That is not the
  cause — find the failing step's own output rather than quoting the last 25 lines.
- Sender display names lie in both directions: a "Grok" / "Automation" sender can be Arif's own
  automation emailing him; a friendly name can be a marketing alias. Read the body before
  attributing anything to a person or a service.
- Live-location shares, receipts and reflection pulses are personal, not urgent. One line each; do
  not analyse the human behind them (bridge / RASA doctrine governs what may be said).
- A wall of red CI is his agents' pipeline state, not a task queue for him. Report the count and the
  newest failure, then offer to go in — do not enumerate twenty run URLs.
- Do not paste message bodies into context wholesale; read bodies only for the candidates that
  survive classification.

## Files

- `references/inbox-triage.md` — classification buckets, the machine-noise filter, verification
  commands, report template.
- `scripts/mail_triage.py` — batch header pull through the broker to JSONL, ready to aggregate in
  code.
