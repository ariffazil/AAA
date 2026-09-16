---
name: fed-model-chain-editing
id: fed-model-chain-editing
version: 1.0.0
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
is demonstrably answering = spend logging has stopped flowing: that is a defect to report, and it
means live headers are the only attribution you have. Absence of spend rows is never evidence of
absence of traffic.

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

## Pitfalls

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

## Support Files

- `scripts/parse-chain-map.py` — parse `model_list` lanes + the `fallbacks:` map (handles inverted entries); fails on dangling fallback rungs.
- `references/provider-liveness-semantics.md` — per-provider probe quirks and how to read a failure body.
- `references/i-arif-voice-drift.md` — symptom→diagnosis for "the agent's voice changed": alias rungs vs router-level fallbacks, the two independent causes (degraded router / English prompt frame), and why the client log cannot attribute the model.

## Authority Boundary

Probe-verified removal of a non-functional rung: T2, do it and report. Changing which live model is preferred, or touching a judge lane's order: propose only, F13 decides. Anything costing money (renewal, top-up, new seat): escalate, never purchase.
