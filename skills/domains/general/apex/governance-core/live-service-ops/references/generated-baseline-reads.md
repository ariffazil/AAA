# Generated Baselines, Censuses and Integrity Manifests

A "converge runtime to reality" pass starts by reading what the box already says about itself —
censuses, health manifests, hash manifests, dashboards. Those artefacts were produced by other
processes at other times. Read one without its stamp, or read it as a live probe, and you
manufacture divergence that does not exist while hiding the divergence that does.

## First-pass sweep (read-only; batch it)

Each line answers a different class of divergence. Run them all before touching anything.

```bash
date '+%Y-%m-%d %H:%M %Z %z'                       # never guess the clock
uptime; free -h; df -h /                           # pressure — read the SWAP line, not just RAM
docker ps --format '{{.Names}}|{{.Status}}|{{.Ports}}'
docker ps -a --format '{{.Names}}|{{.Status}}' | grep -v '|Up'      # exited / restarting
systemctl --failed --no-legend                     # the classic blind spot
ss -tlnp                                           # who listens, and on WHICH address
for p in <ports>; do curl -s -m 2 -o /dev/null -w "$p=%{http_code} " http://127.0.0.1:$p/health; done
for d in <repos>; do echo "$d $(git -C $d rev-parse --short HEAD) dirty=$(git -C $d status --porcelain | wc -l)"; done
ps -eo rss,comm --sort=-rss | head -12             # who is ACTUALLY eating memory
pgrep -c <agent-cli>                               # accumulated agent sessions, per CLI
```

## Reading rule 1 — a generated baseline is a snapshot

Every machine-generated census/manifest carries a `generated` (or equivalent) stamp. If that stamp
is hours old, its contents describe that hour, and every finding drawn from it is history wearing
the present tense.

- Regenerate before quoting: `python3 /root/scripts/mcp-health-census.py` (writes
  `/root/.hermes/MCP_HEALTH.json`).
- State the stamp you actually read. "The manifest says the box is degraded" is a claim about the
  manifest, not about the box.
- A stale census is not drift — it is an old measurement. Reporting it as current state is the drift.

## Reading rule 2 — status and routable are different axes

Censuses typically carry both a `status` word and a `routable` boolean, and the status vocabulary
includes non-fault values. `disabled_intentional` is a configuration choice; `stdio_present` means
the launcher exists but the server is not a network route; only `healthy` is routable.

Collapsing status into a single up/down boolean manufactures outages out of settings — and makes
your report disagree with a live probe for a reason that is not a fault at all.

## Reading rule 3 — a hash manifest over live files reports drift by design

An integrity manifest that hashes live append-only artefacts — `*.jsonl` ledgers, active logs, a
producer script that gets re-run — returns `FAILED` on **every** verification, because the content
grew after the manifest was stamped. Measured shape: a `SOURCES.sha256` over 63 paths returned 3
`FAILED` — an append-only event ledger, a live log, and the manifest's own builder.

Classify that as `EXPECTED_APPEND`, not corruption, and fix the manifest: hash immutable inputs
only, or record the stamped size and compare *expected* growth. **A hash mismatch is evidence only
against a file that is not supposed to change** — establish the file's update semantics before
calling it tampering. A confident wrong negative costs the credibility of the findings that are real.

## Reading rule 4 — attribute resource pressure before blaming a service

On a box shared with agents, sustained memory pressure is usually the agents, not the organs.
Measured: swap fully consumed (7.1G/7.1G, ~19M free) and 23/31G RAM in use while every container
was healthy — the top RSS holders were coding-agent CLI sessions (a 4.5G process; node sessions at
2.3G and 1.4G) plus the gateway, not any organ.

Count live sessions per CLI tool (`pgrep -c <cli>`) before naming a suspect, and report the count —
accumulated idle sessions are themselves the finding. Load average alone is not a fault either: read
it against the RSS table and the swap line, because a busy box that is serving and a thrashing box
look identical in `uptime` and nothing alike in `free -h`.

**A full swap line is not thrashing.** Swap at 100% with no movement is old pages parked by a
long-running box; it becomes a fault only when pages are actively moving. `free -h` cannot tell the
two apart — `vmstat` can, and only through its swap-in/swap-out columns:

```bash
vmstat 1 4        # si/so ≈ 0 across samples = parked, NOT thrashing
```

Take several samples: one non-zero row after a burst is noise, a sustained column is the fault. Load
average must be read against `nproc` — a load of 1.5 on 8 cores is an idle box.

**PSI prints two lines and the second is the one that means anything.** `/proc/pressure/{cpu,memory,io}`
each emit a `some` line (any task stalled) and a `full` line (all tasks stalled — work actually
blocked). Reading only `some` overstates pressure; reading only `full` misses contention. Print both,
and read the windows together: `avg10` vs `avg60` vs `avg300` separate a live spike from a settled old
event, so a quoted `avg60` of a few percent beside an `avg10` near zero is *recovery*, not crisis.

**`docker ps` showing `Up` with no `(healthy)` suffix means the container declares no healthcheck —
not that it is unhealthy.** The parenthetical only ever appears for containers that define one, so a
monitor grading on its presence reports every healthcheck-less container as failing. Confirm which
case you are in before writing the finding:

```bash
docker inspect <c> --format 'State={{.State.State}} Health={{if .State.Health}}{{.State.Health.Status}}{{else}}NO_HEALTHCHECK_DEFINED{{end}} Restarts={{.RestartCount}}'
```

`State=running` + `NO_HEALTHCHECK_DEFINED` is a container doing its job with no self-report. The probe
that actually settles it is one real request through it — never the status word.

**`is-active` reading `activating` is a transition, not an outage.** Re-read after a minute before
classifying, and pair any service-down claim with the port's listener state plus one real request.
A unit that is running minutes after you called it down means you sampled its transition window, and
that correction belongs in your report: a peer or a panel that graded the same box from the status
word alone will otherwise carry the false outage forward as settled fact.

## Reading rule 5 — a listener is not a working service

`ss` showing LISTEN proves a bind, never a working handler. A half-dead process accepts TCP and
never answers, so `curl` returns `000` while every port scan calls it up. Discriminator, re-launch
rule, and the readiness proof are in the parent SKILL.md under *A refusal is address-specific*.
