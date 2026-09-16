# Canon Lock Protocol — chattr +i trees & the only legal mutation path

> **Status:** ACTIVE (F13 GO 2026-09-16, applied by release lane 11:37–11:57 MYT;
> kernel interceptor gates protected trees since 12:00Z — journal `AUTHORITY_GATE`).
> **Wired:** 333-AGI 2026-09-16 (canon-mutate v1.1 hardening + seal-skill routing).

## Protected trees (immutable)

| Tree | State |
|---|---|
| `/root/AAA/governance` | chattr +i (dirs + files) |
| `/root/AAA/canon` | chattr +i (dirs + files) |
| `/root/arifOS/GENESIS` | chattr +i (dirs + files) |

## The only legal write path

```bash
ARIFOS_TRACE_ID=trc-<trace> /root/scripts/canon-mutate run <tree> -- <command...>
```

- `canon-mutate status` — live lock state of all three trees
- `canon-mutate run <tree> -- <cmd...>` — unlock → run → relock → receipt (crash-safe: EXIT/INT/TERM trap relocks)
- `canon-mutate unlock|lock <tree>` — manual multi-step mode (you MUST relock; receipt records `lock_restored:false` until you do)

Receipts: `/var/lib/arifos/canon_mutations.jsonl` — `{receipt_id, ts, trace_id, actor, tree, action, command, exit_code, lock_restored, scheme}`.
`lock_restored` is **verified by lsattr**, not assumed (v1.1 fix — v1.0 logged a hardcoded true).

## Rules

1. Direct write to a locked tree → `EPERM`. **That is the lock working.** Do not "fix" it by hand.
2. Never run bare `chattr -i`. An unlock outside the cycle is an unauthorized bypass.
3. Always set `ARIFOS_TRACE_ID` — receipts without it are stamped `trc-canon-unattributed` (visible defect).
4. Kernel `arif_seal`/`arif_judge` targeting these trees get 888_HOLD by the interceptor —
   legal path per the interceptor's own message is this script.

## Honest limits (documented, not hidden)

- **Root-soft:** a root actor can bypass by hand; the cycle converts silent one-step
  writes into deliberate, logged two-step actions and is a hard wall for non-root writers.
- **SIGKILL window:** `kill -9` between unlock and relock leaves a tree unlocked silently.
  Residual mitigation (open): cron sweep that relocks any tree unlocked > 30 min.
- **Single-host:** no external key custody; references trees inside git repos — read ops unaffected.
