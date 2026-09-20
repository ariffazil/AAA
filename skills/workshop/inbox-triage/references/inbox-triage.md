# Inbox Triage — working notes

## Why this needs a procedure

His inbox is dominated by his own automation: GitHub Actions notifications, deploy bots, AI vendor
newsletters. One night can produce 60+ unread messages inside a six-hour window, most of it machine
noise. Reporting the raw list spends the one resource that matters here. Collapse it.

## Procedure

1. **Pull a window, then stop pulling.** `scripts/mail_triage.py triage 60` → list, then one `meta`
   per id, written to JSONL (~0.3s per call). Keep rows on disk; aggregate in code.
2. **State the window covered.** Sort by `ts` and say it aloud.
3. **Filter machine mail before reading anything.** GitHub Actions and bots are the bulk:

   ```
   \[ariffazil/|notifications@github|Run failed|workflow run
   ```

   Filter them out of the *human-items* list, then treat them as their own section. Do not silently
   drop `Deployment failed` — that one is a real service signal, not notification churn.
4. **Classify:** human/personal · money & receipts · infrastructure or service failure ·
   automation & vendor · his own CI. Only *human* and *infra down* ever compete for "urgent".
5. **Read bodies only for candidates** (`mailread body <id>`).
6. **Verify a failure before repeating it.** For GitHub:

   ```bash
   gh run list --repo <owner>/<repo> --limit 12
   gh run view <run-id> --log-failed
   ```

   Now you can name workflow + commit + time instead of relaying a subject line. For a hosted
   service (Manufact and similar), check whether the thing is actually up before calling it down.
7. **Sweep older mail** before declaring the inbox clean:

   ```bash
   mailread search "in:inbox is:unread newer_than:7d -from:notifications@github.com -from:noreply" 25
   ```

## Report template

```
Dah baca. <N> mesej terbaru (<window>), <unread state>.

Tak ada yang urgent dari manusia.        <- one line, plainly, if true

Yang patut hang tahu:
1. <highest consequence, with verified state + commit/time>
2. ...

Lepas tu bunyi biasa: <vendor/automation tail in one sentence>.

<cadangan + stop-check>
```

Rank by consequence; collapse noise; end with one recommendation and a stop-check, never a menu.

## Pitfalls

- `meta` is one call per id — no bulk header endpoint exists.
- A `--log-failed` tail of teardown lines is not the cause. Look for the failing step's own output.
- "Your instance was paused", "quota used up", "free trial ended" are resource-state notices: report
  them as one line with the resume/remedy action, not as emergencies.
- Receipts are money but not urgency — record the amount, move on.
- Do not treat a live-location share as a safety event or a message to interpret; it is a share.
