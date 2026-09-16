# Learning pipeline — probe bundle

Copy-pasteable probes for the six hops in SKILL.md. Paths below are the arifOS
federation's learning surfaces; adjust if an organ has moved, and verify rather than
assume.

## 1. Producer — what is queued?
```bash
ls -la /root/AAA/skills/.learning/queue/     # atoms: *.json = pending, *.json.done = consumed
ls -la /root/AAA/scars/candidates/           # auto-crystallized scar candidates (quarantined)
```

## 2. Scheduler — is the drain firing?
```bash
crontab -l | grep -iE "learn|skill|scar"
ls /etc/cron.d/                              # federation jobs often live here, not in crontab
systemctl list-timers --all --no-pager | head -25
```

## 3. Consumer — what does the job itself say?
```bash
tail -25 /root/AAA/skills/.learning/cron.log
tail -3  /root/AAA/skills/.learning/ledger.jsonl
```
Reject lines are the highest-signal output. `merged=N rejected=M` repeating with the same
item name means a resolver defect, not a bad item.

## 4. Landing — did the write reach the artifact?
```bash
grep -n "## Lessons (auto)" -A6 <target>/SKILL.md   # does the lesson text actually appear?
```
Three-way agreement is the proof: queue item consumed → ledger row → text in artifact.

## 5. Measurement — is the instrument characterized?
Call the RSI instruments live (via MCP, not the module on disk):
`forge_rsi_impulse_response(window_days=30)`, `forge_rsi_dual_rate_fq()`.
Read the payload, not the status: look for `h_characterized`,
`mean_half_life_sessions`, `governance_window_sufficient`, and sample counts.
A success status with all-null fields is an empty gauge.

## 6. Backlog — how much is waiting on a decision?
```bash
python3 -c "
import json,collections
c=collections.Counter()
for l in open('/root/.local/share/arifos/reexamination_queue.jsonl'):
    try: c[json.loads(l).get('status','?')]+=1
    except Exception: c['unparseable']+=1
print(c)"
```

## Ledger volume check (hop 5 companion)
```bash
python3 -c "
import json,collections
ev,improved,n=collections.Counter(),0,0
for line in open('/root/.local/share/arifos/rsi-ledger.jsonl'):
    try: d=json.loads(line)
    except Exception: continue
    n+=1; ev[d.get('event','?')]+=1
    if d.get('improvements',0) or d.get('improvements_proposed',0): improved+=1
print(f'{n} rows, {improved} carrying improvement>0'); print(ev.most_common())"
```

## Interpretation table

| Observation | Read it as |
|---|---|
| Queue empty, ledger row present, payload text in artifact | loop CLOSED at this hop |
| Same item rejected with the same reason every run | resolver / search-space defect, not a bad item |
| Ledger rows >> rows with a non-zero improvement field | activity recorded, not improvement |
| Instrument returns success with null characterization fields | wired but uncharacterized — empty gauge |
| Queue dominated by PROPOSED with few APPLIED | misplaced gate; split by reversibility |
| Producer emits the same item twice within minutes | missing dedupe at the producer |
| A named governor/sweep resolves to no path, unit or cron line | unresolved label — do not repeat it as fact |
| Producer writes items, consumer drains them, artifact unchanged | UNLANDED — inspect the consumer's write path |
