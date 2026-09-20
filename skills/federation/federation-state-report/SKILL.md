---
name: federation-state-report
description: "Use when asked for the state of the machine or system."
risk_tier: low
floor_scope:
  - F2
  - F7
  - F11
tags: [probe, federation, health, systemd, docker, mcp, state-report, narrative-vs-state]
---

# Federation State Report

Class: the sovereign asks for "the latest state of the machine / system / agents / intelligence" — or pastes a public console, landing page, or dashboard and wants it reconciled with what is actually running. This is a narrative-vs-state audit: banners, pages, and dashboards are narratives; only probes are witnesses.

Read-only throughout. Nothing here needs an approval gate; a mutation discovered along the way gets reported, not done.

## Probe ladder — four layers, in this order

```bash
# 1. MACHINE — identity + resources. Never report specs from memory.
hostname; date -u '+%Y-%m-%dT%H:%M:%SZ'; date '+%Y-%m-%d %H:%M:%S %Z'
uptime; free -h; df -h /; nproc
cat /proc/pressure/cpu /proc/pressure/memory /proc/pressure/io

# 2. SYSTEM — service inventory. list-units, NOT is-active on guessed names.
systemctl --failed --no-pager --plain                       # the only authoritative failure list
systemctl list-units --type=service --state=running --no-pager --plain | grep -iE '<organ>|<agent>'
docker ps --format '{{.Names}}\t{{.Status}}\t{{.Ports}}'
ss -tlnp                                                    # what is bound, and to which interface

# 3. AGENT — sessions, gateway, organ surfaces
ps -eo pid,etime,pcpu,rss,args --sort=-pcpu | grep -iE '<agent-cli>' | grep -v grep
curl -s -m 5 http://127.0.0.1:4000/health/liveliness        # FED no-auth liveness (401/403 = up, auth-gated)
curl -s -m 5 http://127.0.0.1:<organ-port>/health

# 4. INTELLIGENCE — ledgers and loops, not vibes
python3 -c "import json;d=json.load(open('/root/.hermes/cron/jobs.json'));j=d if isinstance(d,list) else d.get('jobs',[]);print(len(j),'jobs,',sum(1 for x in j if x.get('enabled')),'enabled')"
tail -5 /root/AAA/eurekas/eureka-entries.jsonl
```

A ready-made run of all four layers: `scripts/probe.sh`.

```bash
# 5. INTELLIGENCE ENVELOPE — what cognition this box can actually buy
curl -s -m 5 http://127.0.0.1:11434/api/tags   # local model ceiling; empty = no local inference
curl -s -m 5 http://127.0.0.1:<fed-port>/v1/models -H "Authorization: Bearer $KEY"   # frontier endpoints
python3 -c "import json;d=json.load(open('/root/.hermes/cache/mcp_schema_cache.json'));s=d.get('mcpServers',d);print(len(s),'MCP servers',sum(len((v or {}).get('tools') or []) for v in s.values()),'tools')"
```

Full battery, per-process swap attribution, and the diagnosis protocol: `references/intelligence-envelope.md`.

## Coding-agent fleet (FI seats) — layer 5

The agent layer of a state report is rarely systemd units: the coding seats are CLIs on PATH, each with its
own config home and its own seat id. Enumerate, read the one health SOT, then gather per-harness facts.

```bash
# roster — which coder CLIs exist here
for c in claude codex opencode qwen kimi gemini grok aider agy continue copilot; do \
  p=$(command -v $c); [ -n "$p" ] && echo "$c -> $p"; done

# health SOT + freshness, then re-probe if stale (7 serial marker probes, minutes)
python3 -c "import json;d=json.load(open('/run/arifos/mesh-health.json'));print(d['generated_at_utc'],d['summary'])"
bash /root/AAA/scripts/mesh-health-probe.sh

# skills visible to one harness — MUST dereference (symlink farm into the AAA mesh)
find -L <harness-config>/skills -name SKILL.md | wc -l
```

Report six fields per seat: binary + version, model/route, config path, MCP server count, skills visible,
FI seat + role. What each registry file is worth, and the worker-host probe: `references/coding-agent-fleet.md`.

## Rules

- **A guessed unit name returns `inactive` with no error.** `systemctl is-active hermes-gateway arifos-forge aforge geox wealth well frame fed` reports "inactive" for every name that is not a unit — while `hermes-asi-gateway`, `arifos.service`, `a-forge.service`, `geox-mcp.service`, `wealth-organ.service`, `frame-organ.service`, `fed-router.service` are all running. Never declare a service DOWN from `is-active` on a remembered name. Enumerate first, and take failures from `systemctl --failed`. The probe's identifier must come from the box, not from memory.
- **A health-port 000/DOWN is a port fact, not an organ fact.** Take ports from `ss -tlnp`, and check `docker ps` for containerised organs. Containers and systemd units are two namespaces — postgres/qdrant/redis/falkordb are containers, the organs are units; check both before calling anything down.
- **Probe `/ready` as well as `/health`.** A health endpoint can honestly report `healthy` while the machine readiness probe returns `status: fail` with a named failing-subsystem list (`ops_health`, `mind_check`, `heart_check`, `memory_dry_run`). Health that delegates its infra verdict to `/ready` is being honest; a front-door banner reading "Operational" while `/ready` is 503 is not. Report both, and say which one the banner is standing on.
- **A readiness check that says `human_decision_required: true` is F13 territory.** Surface it as the one open question and stop there — do not resolve it, do not re-run it until it goes green.
- **Advertised counts and endpoints are hardcoded until proven live.** A public console advertising "10 prompts, 4 resources" while `prompts/list` returns 13 and `resources/list` returns 35 is a stale page, not a live surface. Same class: `GET /metrics/json` and `GET /sse` advertised on the page and returning 404. Probe each advertised endpoint for a real status code, and each advertised count against the wire (`tools/list`, `prompts/list`, `resources/list`, `.well-known/mcp/server.json`) before repeating it. A count that matches no surface is a finding even when it is small.
- **Registry size > public wire is BY DESIGN, not hidden capability.** Read the endpoint's own `tool_count_semantics` before treating the gap (registry / declared / diagnostic vs exposed) as a lie.
- **A self-reported human metric is not sensor data.** `truth_status: OPERATOR_REPORTED` with `is_sensor_verified: false` means quote the number only with that provenance attached — record freshness does not upgrade source class. Machine-substrate telemetry and human-biometric telemetry are separate fields; never merge them into one "the system is healthy".
- **A page's "0 open gaps" is scoped.** Tracked-gap tables usually cover one named list only; the issue tracker and the readiness probe carry the rest. Reconcile against the tracker before echoing "all clear".
- **PSI before you call a machine loaded or fine.** High `some` with `full` ≈ 0 is contention, not saturation. Swap near-full with `MemAvailable` healthy and `full` = 0 is cold pages, not thrashing — say which one it is rather than guessing from the raw free/swap numbers. **Resident working set, not CPU, is the binding constraint on a busy agent box:** 85% idle CPU alongside 5% swap-free means there is room to compute and no room to hold state — every added daemon, agent session, or resident context eats the budget the CPU is waiting on. Never read idle CPU as evidence of spare capacity; check swap-free and swap activity (`vmstat 1 5`, per-process `VmSwap` from `/proc/*/status`) and name the RSS leaders and idle agent CLIs before proposing anything new to run. `journalctl -u earlyoom` is the cheapest canary: it reports avail-vs-free every few minutes, so a falling swap-free line is a trend you can cite, not just a snapshot.
- **Two writers may share the box.** Other agent sessions can restart services mid-probe. Before attributing a restart to anyone, check `journalctl --since` and the sessions' own state — a single probe window is not the world.
- **One call measures nothing; two identical calls reveal the cache.** Fire the same prompt twice at an inference endpoint and compare wall time (e.g. 0.97s cold → 0.011s). A single latency figure describes whatever happened to be cached or cold at that instant, not the lane. Same discipline for `.well-known`/`tools/list` counts: the same call twice, or you are quoting noise.
- **Deduplicate roots before quoting a manifest count.** Scanning two mirrors of one tree (e.g. `~/.hermes/skills` and the canonical `AAA/skills`) inflates every file count and char total. Resolve realpaths, dedupe, then quote — and when the runtime's rendered size cannot be isolated, report UNKNOWN rather than publishing an inflated number as measured. An honest gap outranks a precise-looking lie.
- **Measure the ceiling, not the catalogue.** A local model list, an endpoint count, and a tool count are three different ceilings. Report which one bounds the box (a 7B local ceiling with 51 idle frontier endpoints is a routing problem, not a compute problem).
- **A missing seat probe is usually a PATH bug, not an absent binary.** Part of the fleet lives under nvm or `~/.local/bin`; a non-login SSH or a stripped environment reports those CLIs as MISSING and manufactures a "half-migrated" verdict. Source the interpreter's PATH — or reuse the boot string the dispatch script itself carries — before concluding a harness is gone.
- **`find` without `-L` measures the map, not the territory.** Symlinked skill/config trees return 0 entries and manufacture an "empty tree" or "zero skills" verdict. Dereference every tree count, and say which command produced the number.
- **Two registry docs can disagree about the same identifier.** When a roster file, the MCP registry, and a harness's own overlay carry different labels for one seat, report all of them and let the sovereign arbitrate — never silently pick one. A role carried by an existing agent (clerk, pruner, on-demand helper) is not an additional agent; do not inflate the fleet with it.
- **Cross-host version drift has no fixed direction.** Neither host is "the" version: record both, per harness, and never quote one host's numbers as the federation's. Wrap every `--version` in `timeout` — node CLIs hang under load and eat the probe budget.
- **A quota wall is not a defect.** A subscription-gated CLI answering 402/429 is EXTERNAL — money-gated, alive — not DOWN. Classify it separately from a broken lane, or the report sends a repair where a top-up is needed.
- **A config flag is a posture, not a status — and its name is not evidence.** A boolean whose name embeds a failure mode (`..._on_db_unavailable`, `allow_requests_on_X_unavailable`, `disable_...`) states what the system *would* do if that failure happened; it says nothing about whether it is happening now. Quoting one before you have measured the subsystem manufactures an incident the operator then chases. Probe first (`pg_isready`, the readiness body, `systemctl --failed`), state that, and only then the stance. Read a settings *block* as one intent — flags that ship together usually mean one thing together, and pulling one line out of the block invents an alarm the others explain away.
- **Extract config facts from a script file, not an inline pipeline.** Piping into an interpreter is refused by the safety scanner, and nested shell-to-python quoting mangles bracketed regexes (unterminated character set). Write the probe to a file, then run it.

## Reporting shape (Arif)

Plain BM Penang, short, no tables and no receipt labels. Lead with what is actually wrong or what changed, then the layers in order, then one bounded decision.

- Pattern that works: *"Tulang belakang kuat, tiada yang tumbang."* followed by the one or two things that are genuinely off, then the exact question you will not answer yourself.
- Never say "semua OK" when `/ready` is red — name the failing checks and keep the two verdicts separate.
- Close with at most one decision. If a probe returned `human_decision_required`, that is the decision; do not offer a menu.
- Do not paste raw JSON at the sovereign. Extract the fields, state the delta, keep evidence paths for when he asks.
- **An internal identifier in the sentence becomes the question he asks.** A config key, env var, table name or unit name quoted bare reads as an incident report — most of all one whose name contains a failure mode. Name the subsystem's measured state first, with its probe in the same breath ("Postgres up, accepting connections, 0 restarts"), *then* the stance in plain words. A healthy subsystem must never be quoted in the middle of a fault list; the keys belong in the receipt, not the sentence. If he comes back with "why is X unavailable?" or "should it be?", the framing failed — answer in two separate moves: (a) the measured state now, (b) whether anything is supposed to depend on it, because those are different questions with different owners.
- **A report assembled from component names is not a report.** The rule above governs one sentence; this governs the whole account. A sweep narrated as *which daemon pinned which baseline*, *which external service noticed a schema change*, *which endpoint answered cold then warm* is a chain of proper nouns — he can follow every word and still not know whether anything is wrong. **The trigger that tells you it failed:** he asks, in any phrasing, for the same content *"in full human language"* / *"apa benda ni semuanya"*. That is not a request for more detail; it is a report of illegibility, and re-explaining with better structure does not fix it.
  - **The fix is translation, not simplification.** Replace each component with what it *does*, then attach ONE everyday analogy for the whole mechanism (a warden checking a house before anyone moves in; a fence with seven loose nails; a key that no longer fits its door). One analogy per report — a zoo of metaphors is the same failure in a friendlier costume.
  - **Say what it means for him before what it is.** Not smoke / not a collapse / nothing that needs him tonight, *then* the mechanism. The severity verdict is the payload; the architecture is the explanation.
  - **Separate what you opened from what you only saw.** Name the items you read to the line and the items where you only have a failing step's name. An honest map of your own coverage costs one clause and is the difference between a report and a performance.
  - **Close on the machine/human split.** End with whether any of it originated from a person. A sweep that is entirely machine noise is a different message from one carrying a human message, and collapsing the two invents urgency.

## Related

- `live-probe-audit-pattern` — auditing *someone else's* claim; this skill is producing the state picture. Same probe discipline, different trigger.
- `federation-machine-verification` — machine/organ/port identity before multi-machine ops.
