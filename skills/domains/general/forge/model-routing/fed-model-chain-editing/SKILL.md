---
name: fed-model-chain-editing
id: fed-model-chain-editing
version: 1.1.0
description: Use when editing or repairing FED model fallback chains.
owner: AAA
risk_tier: medium
autonomy_tier: T2
floor_scope: [F1, F2, F4, F11, F13]
tags: [litellm, federation, fed, fallback-chain, model-routing, provider-health, config]
---

# FED Model Chain Editing

> Chains rot silently. A provider lapses, a quota resets, and the dead rung stays
> at `order: 0` — every request pays a failed hop before the chain moves on.
> The slow lane is usually not a routing bug. It is a **dead rung nobody removed**.

## When to Use

- A lane (i-arif / agi-333 / asi-555 / forge-777 / apex-888 / openclaw / fed/vision) feels slow, hangs, or falls through more than one model per request.
- **The agent's own output changes register** — stiff, translated-from-English phrasing in a language the lane normally handles well, or a reply far longer than the prompt warranted. The user frames this as "why are you speaking X / what model are you" — treat it as a routing event, not a style complaint. Recipe: `references/i-arif-voice-drift.md`.
- A provider has lapsed, been rate-limited, or been topped up, and the chain should reflect it.
- You are asked to "clean up", "fix the fallback", or "purge a dead provider".
- Config `notes:` claim a provider is live and you need to know whether it is.
- You are asked directly which model backs a lane ("apa model aku guna" / "what model are you"). Answer from a live router probe — see *Attribution*; the chain cannot answer it, and neither can the agent-side config.
- The trigger is a **vendor email or beta invite** that names model ids the router does not carry. Triage the notice first (`provider-notice-triage`); this skill owns only the lane edit that may follow, and a new preview id is a census-probe-propose job, never a login.

## When NOT to Use

- Single-organ failure with no routing symptom (use the organ's own recovery skill).
- Quota renewal, seat purchase, or any decision that costs money — that is the sovereign's call.
- You only want to *observe* health (use a monitoring skill); this skill is for changing the chain.

## INVARIANT — Probe, Don't Trust Notes

`notes:` fields claiming `active` / `GO-LIVE` / `resubscribed` / `N-day runway` are **claims, not status**. They rot silently and they are the single most common source of stale routing. A written report from another agent is likewise a hypothesis: re-probe before you mutate, because you would otherwise repeat the same claim-before-probe failure that put the dead rung there.

Re-derive, in this order:

1. Which config does the running process actually load? (`systemctl cat <unit>` — drop-ins override the base unit.)
2. What is the process start time vs the config mtime? Start time **earlier** than mtime means the change was never loaded.
3. What does each rung in the affected lane answer *right now*?

## Two Layers — Lane Body vs `fallbacks:` Map

| Layer | What it is | When it routes |
|---|---|---|
| Lane body | every `model_list` entry sharing one `model_name`, tried in `order:` (equal `order:` values shuffle) | first |
| `router_settings.fallbacks:` | map keyed by lane name; values are *other lane names* | only after every deployment in the lane fails |

Consequences that cause real bugs:

- A dead rung living only in `fallbacks:` is invisible to a lane-body census, and vice versa. Confirm which layer your evidence came from before proposing anything.
- Any `fallbacks:` value whose `model_name` is defined nowhere in `model_list` is a **dangling reference** — no config-time error, silent runtime failure. Re-check after every edit.
- The first entry of the lane body is what serves normal traffic. A dead model there is not "a fallback problem"; it is the primary path.

## Attribution — "Which Model Am I Actually On?"

When the ask is *which model backs this lane right now*, config cannot answer it: an alias carries
a dozen rungs and the live one is chosen per request. Two instruments, in this order.

1. **Hermes side (alias only)** — `~/.hermes/config.yaml`: `model.default` is the lane alias,
   `model.provider: custom:<fed>` is the router. This names the **alias**, never the model. Do not
   stop here or pass it off as an answer.
2. **Router side (authoritative)** — send the alias to the local front door and read the
   `x-litellm-*` **response headers**. They name the deployment that served the request, with no
   body parsing and no cache ambiguity:

```bash
curl -s -D - -o /dev/null --max-time 45 http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $MASTER_KEY" -H 'Content-Type: application/json' \
  -d '{"model":"<lane>","messages":[{"role":"user","content":"nonce-'"$RANDOM"'"}],"max_tokens":5}' \
| grep -iE '^x-litellm-(model-name|model-api-base|model-group|attempted-retries|attempted-fallbacks)'
```

   - `x-litellm-model-name` = the real upstream deployment (e.g. `openai/deepseek-flash`) and
     `x-litellm-model-api-base` = the vendor endpoint. Together they *are* the answer.
   - `x-litellm-attempted-retries: 0` **and** `x-litellm-attempted-fallbacks: 0` mean the lane's own
     primary rung served it. Non-zero means the chain fell through — then report *which rung is
     dead*, not just the answering name. Never infer fall-through from the model name alone.
   - A `:4000` header set is the gateway's view — confirm it reached the node you think it did
     (see *The HAProxy layer*) before reporting attribution as fact.

**Neither instrument is `GET /v1/models`.** Fetching the router's model list returns the *registered*
`model_name` set — a registry read. It names no serving deployment, and behind an HAProxy front door
it may not even be the node you think you are looking at. An answer assembled from the config's
`order:` values plus a model-list fetch is a guess wearing evidence; when the ask is attribution,
produce a response header or state plainly which evidence is missing.

(Probe keys come from `/root/.secrets/kunci-root.env`. Never grep a key literal out of a config file
to build a curl — a literal on a command line lands in shell history and in session transcripts.)

**Historical attribution** — `LiteLLM_SpendLogs` in the `litellm` Postgres DB
(`model_group`, `model`, `startTime`). Connect with the cluster role from
`/root/.secrets/kunci-root.env` (`POSTGRES_USER`, db `litellm`); `sudo -u postgres` fails because
that role does not exist on this cluster:

```bash
PGPASSWORD="$POSTGRES_PASSWORD" psql -h 127.0.0.1 -U "$POSTGRES_USER" -d litellm -t -A -F'|' \
  -c "select model_group, model, to_char(\"startTime\",'MM-DD HH24:MI') from \"LiteLLM_SpendLogs\" where model_group='<lane>' order by \"startTime\" desc limit 12;"
```

Check the **age of the newest row** before concluding anything. Newest row weeks old while the lane
is demonstrably answering means spend logging is not flowing — and that has **two possible causes
with opposite responses**, so read the config flag before diagnosing a defect:

```bash
python3 -c "import yaml;g=yaml.safe_load(open('/root/A-FORGE/litellm-config.yaml'))['general_settings'];print({k:g.get(k) for k in ['disable_spend_logs','store_model_in_db','allow_requests_on_db_unavailable']})"
```

- `disable_spend_logs: True` — the ledger is **off by design**. Never report it as a logging defect
  and never re-enable it on your own initiative: the flag sits on the path of every request, and the
  reason it was set is usually not recorded anywhere. Live headers (*Attribution*) are then the only
  instrument; the correct move is a header sweep over the live lanes, not a database query.
- Flag absent/false and rows still stale — then it *is* a defect: report it with the newest row's age.

Absence of spend rows is never evidence of absence of traffic.

**Know which of the two claims you are making.** A header sweep is a **snapshot**: it says which rung
served at time T. It cannot say what a rung *adds* over time — marginal value needs a temporal
ledger. "8/18 lanes fell through on this pass" is a snapshot claim and must not be dressed up as a
value claim about the rungs.

## Provider Liveness Semantics

Read the **body**, not just the status code. Full per-provider notes: `references/provider-liveness-semantics.md`.

| Signal | Means | Action |
|---|---|---|
| `/v1/models` 200 | key authenticates — **nothing more** | probe a 1-token completion before calling it live |
| chat 200 | live | none |
| 402 | subscription/plan lapsed, or balance gone | read the message: a plan lapse needs renewal and has **no auto-reset** |
| 429 | quota exhausted | the reset timestamp is in the body — record it, demote, re-probe after |
| 403 | plan limit or license scope | coding-only seats reject direct API calls — the key is fine, the lane is not |
| 200 on `/models` + 429 on generate | valid key, depleted prepaid balance | top-up required — **not** a dead key |

### Probed 2026-09-15 — which codes actually occur (and which never did)

A full sweep of every `api_base` in `model_list`, 1-token probes, returned **zero 401s**.
Nothing was auth-dead; everything was quota/billing-dead:

| Provider | Code | Body discriminator |
|---|---|---|
| Qwen token-plan (4 seats) | 429 | `insufficient_quota` — "Your token-plan quota has been exhausted" |
| DashScope / `QWEN_PAYG` | 403 | `AllocationQuota.FreeTierOnly` |
| Z.ai coding plan | 429 | `code 1310` "Weekly/Monthly Limit Exhausted" |
| Z.ai paas | 429 | `code 1113` "Insufficient balance or no resource package" |
| Kimi `/coding/v1` | 403 | `access_terminated_error` |
| OpenCode Go `/zen/go/v1` | 429 | `GoUsageLimitError` |
| Gemini | 429 | "prepayment credits are depleted" |
| MiniMax · DeepSeek · MiMo · SEA-LION | 200 | the only four live upstreams |

**Probe the `api_base` EXACTLY as written.** Hand-typing a neighbouring path produces a
false "broken base URL": `api.kimi.com/v1` 404s while the config's
`api.kimi.com/coding/v1` 403s on quota; `opencode.ai/zen/v1` 401s while
`opencode.ai/zen/go/v1` 429s. Both were misread as misconfiguration before the config value
was used verbatim.

**Quota is a moving target inside a single session.** `QWEN_INDIVIDUAL` went
429 → 200 → 30 s timeout in ten minutes. Probe 3× before demoting or promoting a rung, and
never hardcode a reset timestamp into a chain — demote with `order:` and re-probe after the
window rolls over.

Minimal probe (save the body, then read it):

```bash
source /root/.secrets/kunci-root.env
code=$(curl -s -o /tmp/_p -w '%{http_code}' "$BASE/chat/completions" \
  -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' \
  -d '{"model":"<model>","messages":[{"role":"user","content":"ping"}],"max_tokens":1}')
echo "$code"; head -c 200 /tmp/_p
```

## Procedure — Propose, Verify, Apply

1. **Census the lane.** Parse `model_list` and the `fallbacks:` map. `scripts/parse-chain-map.py` prints per-lane deployment order and exits non-zero on dangling fallback rungs.
2. **Probe every rung** in the affected lane (and every other lane you intend to touch). Record code + body.
3. **Backup:** `cp litellm-config.yaml litellm-config.yaml.bak-<change>-<UTC-timestamp>`.
4. **Transform into `/tmp`**, never onto the live path.
5. **Validate:** `python3 -c "import yaml; yaml.safe_load(open('/tmp/<new>.yaml'))"`, then run `/root/AAA/scripts/validate_litellm_config.py`.
6. **Diff the parsed lane map before/after**, not only the text — this is what catches a transformer that ate unrelated entries. Also sanity-check the byte delta: a removal-only edit should shrink by roughly the lines removed.
7. **Apply** to the primary, then **sync the deploy mirror** `/root/A-FORGE/deploy/fed/litellm-config.yaml`, then **reconcile** the hashes pinned in `/root/AAA/canon/FEDERATION_CONFIG_CONTRACT.v1.json`. Primary alone leaves the mirror stale and the validator failing.
8. **Restart via systemd** (`systemctl restart litellm-federation`, never `nohup`), then confirm the service start time is *later* than the config mtime.
9. **Probe live:** `curl -s http://127.0.0.1:4013/health/liveliness` (local backend; `:4000` is HAProxy in front of it), then exercise the edited lane's top rung with a real 1-token call. Report the rungs removed/added with the probe evidence.

The config is bind-mounted into the litellm container from the primary path — editing the file without a restart changes nothing.

## A Lane Is a Failover Ladder, Not an Ensemble

FED lanes are **failover ladders**: one rung answers and the rest are tried only when the rung above
fails. Nothing votes, nothing is collapsed. This decides which external findings apply here.

- **Model-pool / ensemble research does not transfer to lane design.** Results that homogeneous pools
  beat heterogeneous ones, that diversity lowers consensus accuracy, or that larger pools underperform
  their best single member are about collapsing many *answers* into one verdict. In a ladder the pool
  decides *who answers*, and a second brain from another vendor is precisely what keeps the lane alive
  when the first vendor's quota dies. Importing "use one family only" into lane chains converts an
  availability asset into a correlated outage.
- **Where those findings DO apply here** is organ-level deliberative work — any panel that collapses
  several answers into one verdict, whether a multi-witness bench, a musyawarah round, or a judge lane.
  Two rules follow:
  (a) **Measure what a member adds before adding it, and never infer it from the model card.** A pool's
  *potential* (the oracle: what its best member could have answered) is not its achieved accuracy — on
  hard benchmarks an expanded heterogeneous pool commonly lands BELOW its own best single member, while
  replicates of one family are the variant that improves. Model size, accuracy and domain-specialisation
  signals do not predict panel performance; measured error diversity does not either. High oracle is a
  ceiling, never a forecast.
  (b) **A panel of four must beat one, or it is wasted budget.** litellm records spend, latency and
  failures — never right-vs-wrong — so nothing in the current telemetry can say whether a second witness
  improved a verdict. Any quality claim about a lane or a panel is ESTIMATED and must be labelled so,
  until a scored probe runs against a held-out set and its receipts are keyed by lane.
- **Homogeneity is a resilience metric, not a quality metric.** A lane whose live rungs are all one
  vendor family is a **terminal node**: when that vendor lapses, every rung dies together. A lane with
  2+ live rungs from one family is not redundancy, it only looks like it. Census it:

```bash
python3 - <<'PY'
import collections, yaml
cfg = yaml.safe_load(open('/root/A-FORGE/litellm-config.yaml'))
lanes = collections.defaultdict(list)
for e in cfg.get('model_list', []) or []:
    lanes[str(e.get('model_name'))].append((int(e.get('order', 0)), str(e.get('model'))))
def fam(m):
    return next((k for k in ('qwen','deepseek','gemini','minimax','glm','mimo','kimi','sea-lion','llama','gpt-oss') if k in m.lower()), 'other')
for l, r in sorted(lanes.items(), key=lambda x: -len(x[1])):
    live = [x for x in r if x[0] < 90]
    parked = [x for x in r if x[0] >= 90]
    fams = sorted({fam(m) for _, m in r})
    if len(live) > 1 and len(fams) == 1:
        print(f'TERMINAL-NODE {l:22s} live={len(live)} fams=1 ({fams[0]}); parked99={len(parked)}')
PY
```

  Every rung parked at `order: 99` is a model that was added and never measured — report the count as
  pool pressure (high ceiling, unmeasured service), not as capability.

## Pitfalls

- ❌ **Putting a credential-store path on a command line.** A shell command carrying a literal path
  into the secret store is refused by the T3 gate before it runs — the whole call is blocked, not just
  the offending fragment, and retrying the same command repeats the block. The 5-R vars are normally
  already exported in the session env: check with `env | grep -oE '^[A-Z_]+='` and reference `$VAR`
  directly (`LITELLM_MASTER_KEY`, `POSTGRES_USER`, `POSTGRES_PASSWORD`). Sourcing the env file inside
  every command is what trips the gate — source once per session, then use the variables. The same
  gate also scans `skill_manage` args, so keep the literal path out of written doctrine too.
- ❌ **Dumping a container's or unit's environment to read one variable.**
  `docker inspect <c> --format '{{range .Config.Env}}{{println .}}{{end}}'`, `/proc/PID/environ` and
  `systemctl show -p Environment` all emit every credential the process was started with — DB passwords,
  the litellm master key, provider API keys, bot tokens — into the session transcript, which is replayed
  to a model endpoint. Print key NAMES only (`| cut -d= -f1`); for a single value, select the exact key
  AND mask it in the same expression that does the printing. A grep/regex used as a *filter* is not a
  redactor — everything it fails to classify still lands in the output. A credential that reaches the
  transcript is a **rotation event, not a typo**: report it, and separate the keys you can mint yourself
  from those needing a vendor dashboard.
- ❌ **Assuming the `:4000` front door reaches the node you are editing.** HAProxy `:4000` can
  be serving a *completely different machine*. Verify before you reason about a lane from
  `:4000` output: request a model id that exists on only one node (2026-09-15:
  `codestral-latest` returned KVM4's `402 MistralException` on `:4000` and
  `400 Invalid model name` on the local `:4013`). The `use-server`/`server` lines that were
  supposed to make the choice were sitting **inside a `frontend` block** — HAProxy ignores
  them there (`has no backend capability`) and the frontend silently kept its
  `default_backend`. Move health-check + `server`/`use-server` into a real `backend`.
- ❌ **Comparing the two nodes by `/v1/models` id set.** KVM4's set differed from KVM8's by
  only two ids, but its **fallback map was a whole stale generation** (still carrying dead
  Mistral rungs). Trigger an error on each node and read the `Fallbacks=[...]` list litellm
  prints in the body — that is the cheapest way to diff two live litellm builds.
- ❌ **Reading a lane's health from its HTTP code.** A quota-dead lane returns **200** while
  answering as a *different* model. Read the response's `model` field. And nonce your probe
  prompt: litellm response cache (Redis, ttl 1800) will otherwise return the previous
  model's reply and attribute it to this lane.
- ❌ **Splitting `model_list` on `- model_name:`.** Some entries write their fields in inverted order with `model_name:` at the END of the block (the `fed/vision` / `hermes-asi-vision` chains do). A splitter keyed on `- model_name:` swallows the preceding entry's body into one block and silently drops unrelated lanes. Split on the column-0 list marker (`^-\s`) instead, then read `model_name` from anywhere inside the block.
- ❌ **Calling a provider live off `/v1/models` 200.** It proves only that the key authenticates. Liveness is a 1-token completion.
- ❌ **Editing preferences you hold no authority over.** Removing a provider that no longer authenticates (probe-verified) is authority-neutral — do it. Changing the order or preference of *live* rungs, especially in a judge lane, is the sovereign's decision: prepare it, present the binary, let them choose.
- ❌ **Writing a shared config while a second agent session is live.** Check `ps -eo pid,etimes,args | grep -i hermes` first; two writers on one config is a lost-update race. Under a concurrent writer, prepare the patch, park it in a work dir, and report — do not race.
- ❌ **Reporting "chain fixed" after touching only the primary config.** Mirror + contract hashes + restart + live probe are all one operation.
- ❌ **Reading the answering model out of the agent-side log.** The client logs the *alias* (`model=i-arif provider=custom`) on every call, whether or not the router fell through — a client log can never attribute a model. Attribution needs the router's own evidence: the `x-litellm-model-name` / `x-litellm-attempted-fallbacks` response headers (*Attribution*) or `LiteLLM_SpendLogs`. With neither, state it as inference and say which evidence is missing.
- ❌ **Assuming a lane's shape from its name.** Lane names are organs, not models; the same vendor model may legitimately back several lanes. Never infer routing from the alias.

## Recursive Fallbacks — a lane is longer than it reads

When a fallback target *also* fails, litellm continues into **that** model's own `fallbacks:` entry.
A lane declaring 2 rungs can therefore be 6–8 real network hops. Proof (2026-09-15): `fed/audio-asr`
declares two Gemini rungs, both payment-dead — yet it answered `200` from `qwen3.8-max`, because
`gemini-2.5-flash`'s own fallback list contained `qwen3.8-max`.

Consequences:
- **A lane's declared rungs are not a latency bound.** Measure the answering deployment, not the config.
- A single payment-dead model referenced from many chains is a **terminal node**. Here
  `gemini-3.6-flash` appears in **18** fallback lists and escapes nowhere; the log says
  `No fallback model group found for lookup_groups=gemini-3.6-flash`. Count how often each model
  appears as a fallback target before pruning — the most-referenced target is the one whose death matters most.

## The HAProxy layer — probe the node, not the file

The FED front door (`:4000`) is **HAProxy**, not litellm. Three states must agree: the file on disk,
the config the running process loaded (compare `stat -c %y` on the file against `ps -o lstart` on the
master), and what each node answers now. A valid file plus a previously-loaded process is the normal
shape of a silent gateway defect — measured 2026-09-15, the gateway file was **invalid**
(`'server' not allowed because frontend 'X' has no backend capability`) while the process served a
config loaded a week earlier, 6/6 samples confirming it never reached the local node. Also:
unconditional master-key injection **overwrites the caller's** `Authorization`, so sending a key to
prove "the right backend was selected" proves nothing on that path — use a model id that exists on
only one node instead.

### Readiness semantics — one node cannot tell you about another

`/health/liveliness` answers without auth (~12 bytes). `/health` is **auth-gated**: a bare
`401 Authentication Error` there means UP, not down. `/health/readiness` is the endpoint carrying `db`:

```json
{"status":"healthy","db":"Not connected"}
```

`Not connected` means that process was started with **no `DATABASE_URL` at all**. That is by design for a
node serving the master-key path — the frontend injects the key, so no virtual-key lookup is needed and
the DB is irrelevant to it. The virtual-key (zen) path is pinned **separately** to whichever node IS
database-wired; read the `frontend`/`backend` blocks to see which, rather than believing either node's own
claim about itself. Consequences:

- `db != connected` on a non-key-holding node is **not an incident**; alerting on it is a false alarm.
- A node with no DB **cannot validate a caller's virtual key**. Sending a key-bearing caller at it leaves
the key unverified — assert the frontend→backend pin before assuming key governance on that path.
- `allow_requests_on_db_unavailable: true` degrades a DB outage to "serve anyway" instead of an error.
Read the flag and reason from it; do not test it by breaking the DB. Report it as **posture, never
status**: a flag whose name contains a failure mode reads as an outage report the moment it is quoted
bare. Measure the subsystem first (`pg_isready`, the readiness body, the unit's state), state that,
*then* the flag. And read a settings *block* as one intent before treating a single line as a defect —
`store_model_in_db: false` together with `disable_spend_logs: true` and this flag is one design stance
("do not make serving depend on the DB"); isolating any one of them manufactures an alarm the others
explain away. Weight a written rationale next to a bare boolean as evidence about intent — but never
treat its absence as evidence of a fault.
- A readiness answer taken from a node with a high `RestartCount` and seconds of uptime was sampled
*between restarts*. Read readiness against uptime, never in isolation.

### A declared backup is a claim — probe it or don't count it

`server <name> <ip:port> ... backup` is topology INTENT, not verified capacity. `option httpchk` grades a
node on `/health/liveliness`, which a crash-looping process answers happily between restarts while every
real request through it fails. Before counting any failover target as capacity, probe the target itself:

```bash
docker inspect <ctr> --format 'restarts={{.RestartCount}} started={{.State.StartedAt}} exit={{.State.ExitCode}}'
stat -c '%y' <the config it mounts>     # a config older than the build is a stale node
# then one real 1-token call THROUGH that node — not through the front door
```

An unexercised backup is a ghost capability, and its presence is worse than no backup: it makes the
primary *look* protected. On the cooldown table — the `cooldown_time` litellm logs is its own bookkeeping
and can outlive the reset the provider advertised in the error body, so a rung can be absent from the pool
long after the provider would serve again. Compare the two numbers before calling a rung merely "waiting
on quota": a bookkeeping-dead rung is not revived by a restart or by the reset arriving.

## Support Files

- `scripts/parse-chain-map.py` — parse `model_list` lanes + the `fallbacks:` map (handles inverted entries); fails on dangling fallback rungs.
- `scripts/node-posture-probe.sh` — per-node posture in one shot: listeners, restart count vs uptime, config mtime, whether the node is DB-wired, and readiness on :4000/:4013. Prints key NAMES only, never env values.
- `scripts/fed-attribution-probe.py` — sweep every live lane through the router and classify each as `SERVED_ON_PRIMARY` / `SERVED_OFF_PRIMARY` / `UNATTRIBUTED` / `ROUTER_ERROR` / `TIMEOUT` from the `x-litellm-*` headers; writes one JSON snapshot receipt. Use for the "which rung is actually answering, and did it fall through" question, and as the evidence artifact behind a snapshot attribution claim.
- `references/provider-liveness-semantics.md` — per-provider probe quirks and how to read a failure body.
- `references/i-arif-voice-drift.md` — symptom→diagnosis for "the agent's voice changed": alias rungs vs router-level fallbacks, the two independent causes (degraded router / English prompt frame), and why the client log cannot attribute the model.

## Authority Boundary

Probe-verified removal of a non-functional rung: T2, do it and report. Changing which live model is preferred, or touching a judge lane's order: propose only, F13 decides. Anything costing money (renewal, top-up, new seat): escalate, never purchase.
