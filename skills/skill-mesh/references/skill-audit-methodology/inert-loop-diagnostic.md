# Inert-Loop Diagnostic — Ceremony vs Metabolism (2026-08-31)

## The tell (one sentence)

A process can be **wired AND populated AND running** yet never actually do its job — it heartbeats on schedule but produces zero measured improvement. Trust the measured delta, never the label or the volume of log entries.

## The live example

Audited the RSI self-improvement loop: the ledger `/root/.local/share/arifos/rsi-ledger.jsonl` held **1,494 entries**, every one:
- `actor:"opencode"` (never the sovereign/Hermes actor)
- `improvements_proposed:0`
- `last_delta_s:0`

So the loop ran every turn as a heartbeat (`turn_rsi.pulse`) but **never installed or measured a single fix**. That is a CEREMONIAL loop, not a METABOLIC one — and it is precisely the gap the AGI→ASI literature flags: recursive self-improvement is the pathway to ASI, and a loop that reports zeros is *posing*, not learning.

## The diagnostic (run before concluding "self-improvement works")

```python
python3 - <<'PY'
import json
n = imp = delta = 0
for line in open('/root/.local/share/arifos/rsi-ledger.jsonl'):
    try: d = json.loads(line)
    except Exception: continue
    if not isinstance(d, dict): continue
    n += 1
    if d.get('improvements_proposed', 0) > 0: imp += 1
    if d.get('last_delta_s', 0) != 0: delta += 1
print(f'total={n} improvements_proposed>0={imp} last_delta_s!=0={delta}')
PY
```

- Both `improvements_proposed>0` AND `last_delta_s!=0` near zero across hundreds of entries → loop is inert. Fix the loop, do not decorate it.
- A LIVE improvement entry carries ALL FOUR: (1) a trace-observed bottleneck (`REPETITION` / `EVIDENCE_GAP` / ...), (2) a concrete reversible fix, (3) a non-zero `delta_entropy`, (4) a `next_session_hint`. Absence of any one = theatrical.
- Zero-delta heartbeat entries (`turn_rsi.pulse`) are noise, not learning. Count them separately from real cycles before drawing conclusions.
- **ASI lever:** the highest-value move is to make the loop produce + measure a real fix. Do NOT add more tools — make the existing loop metabolic.

## Second live example — the curator's rate limiter that could not fire (2026-09-15)

The Hermes background-review fork ("curator") refuses writes to bundled, pinned, hub and
user-owned skills. Measured over one day on KVM8: **16 refusals against 12 completed
reviews**, with targets repeating across sessions — one skill refused 3× inside 13 minutes,
another twice six hours apart. The guard carried a retry limiter whose counter lived in a
ContextVar reset to `{}` at every review fork, so cross-session repetition was structurally
invisible and the "STOP after 3" branch could never fire across sessions. A limiter that
cannot observe what it limits is decoration, not control.

Three rules distilled:

1. **Count the OUTCOME, not the mechanism.** Reviews-that-landed vs attempts-blocked. A guard
   that refuses is not a guard that teaches — and "no failure signal" is not "learning works".
2. **A blocked attempt must leave a durable trace.** Ownership refusals now append audit-only
   rows (`action: "refused"`, actor `curator`, empty before/after) to the existing skill ledger,
   so a lesson whose only natural home is a protected skill stays visible after the review ends
   instead of evaporating with the chat line. Audit rows are never rollback targets.
3. **When you add state, declare its lifetime in the code next to it.** A per-session counter is
   not a repetition metric; left undocumented, the next reader assumes persistence that is not
   there.

**Meter (one command):** `/root/AAA/scripts/curator-loop-meter.py` — reads the gateway journal
(attempt rate + refusal classes), the skill ledger (blocked targets) and the same ledger's
mutation rows (what actually landed). Baseline T0:
`/root/AAA/registries/hermes-selfimprove-meter-T0-2026-09-15.json`.
**Falsifiable test:** repeat targets must be empty on the next run; if a target repeats, the
loop is posing — the boundary declaration, not the counter, is what needs fixing.

## Reusable principle

Applies to any automatic process, not just RSI: cron jobs, monitoring, catch-up schedulers, memory consolidation. If the log grows but the *measured outcome* (delta, count, completion rate) stays flat, the thing is posing. Always key the verdict on the outcome metric, not on the entry count or the "running" status.
