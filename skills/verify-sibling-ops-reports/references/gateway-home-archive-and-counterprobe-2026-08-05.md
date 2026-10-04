# Gateway-home archive + OpenClaw counter-probe — 2026-08-05 evidence chain

Two episodes in one session: (A) verifying+executing a sibling's archive proposal,
(B) being corrected by OpenClaw on a probe misread. Both are reference material for
the verify-sibling-ops-reports workflow.

## A. "Archive gateway-hermes/forge/openclaw dirs" — the false-empty trap, executed

Sibling report: "Nak aku archive gateway-hermes/forge/openclaw directories yang kosong"
(claimed empty). Probe sequence that actually ran:

1. `find <dir> -type f | wc -l` + `du -sh` → **504 files / 30M each** (gateway-openclaw 7.8M).
   Claim "kosong" was FALSE — full runtime homes (channel_directory.json, SOUL.md,
   kanban.db.*.lock, gateway_state.json, cron locks, skills tree).
2. PID liveness: `ps -p 996359,1029791,1029807,1029803` → **all dead**. Every
   gateway_state.json said `"gateway_state":"running"` with telegram "disconnected" —
   state files lie about liveness; the PID check is truth.
3. Path references: `grep -rl "AAA/gateway" /etc/systemd/system/ /root/scripts/
   /root/HERMES/scripts/` → **zero refs**.
4. Live gateway home: `/proc/<MainPID>/environ` → `HERMES_HOME=/usr/local/lib/hermes-agent`
   — NOT /root/AAA/gateway*. The four dirs were experiment homes from the 2026-08-05
   gateway-drift incident (three `hermes gateway run` at 11:40, all killed).
5. Executed: `mv` all four → `/root/_archive/2026-08-05-gateway-homes/` + README receipt.
   Reversible (F1). Git: the dirs were tracked in AAA repo; a sibling commit
   `fix(aaa): untrack gateway runtime dirs — committed by mistake` landed same minute —
   siblings often converge on the same verdict independently.
6. Post-archive verify: gateway still live (PID 1120496 on :8444; 404 on `/health`
   is the webhook listener's route shape, NOT a dead service), repo clean.

## B. The 401 ≠ DOWN misread — and the counter-probe that caught it

My probe: `curl -sf http://100.64.0.2:4000/health` → failed → I reported
"❌ LiteLLM :4000 DOWN". OpenClaw's counter-probe (right):

```
ss -tlnp → litellm PID 1048931 LISTENING on 100.64.0.2:4000 + socat on 127.0.0.1:4000
curl /health → 401 (auth required) — the endpoint EXISTS, it's auth-gated
journal: 10/11 fed/opencode calls 200 OK sub-second; one AbortError 67s at 12:06
        (Sentinel cron, LiteLLM had restarted 11:44 — warm-up blip)
```

Lessons:
- `curl -sf` fails on 401 → "DOWN" verdict from `-f` alone is a misread.
  Listener check (`ss -tlnp`) must come FIRST; 401 = UP but auth-gated.
- `401` on `/health` for a model proxy is normal (no key passed) — not evidence of death.
- One AbortError ≠ systemic outage: count occurrences over a window before claiming
  "model route merah" (see flow-claim row in SKILL.md §1).

## C. Flow-report number drift (also in SKILL.md §1)

Sibling flow report: FQ 0.818, receipts 21. Live :7073/health: fq.quotient **0.909**
(execute 10 / verify 11), receipts 22. Numbers in flow reports are snapshots from
write-time; always re-probe and report declared-vs-measured.

## D. Gateway identity cross-check (repeatable commands)

```bash
# which home does the live gateway use?
for pid in $(pgrep -f "hermes.*gateway.*run"); do
  tr '\0' '\n' < /proc/$pid/environ | grep -E "HERMES_HOME="
done
# are state-file PIDs actually alive?
ps -p $(cat /root/AAA/gateway*/gateway.lock 2>/dev/null | grep -oE '"pid": [0-9]+' | awk '{print $2}') 2>/dev/null
# auth-gated or dead? LISTENER first:
ss -tlnp | grep ":4000"
```
