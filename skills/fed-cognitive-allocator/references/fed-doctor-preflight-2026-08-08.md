# FED Doctor + OpenCode Pre-Flight (2026-08-08)

> **Forged:** 2026-08-08 by 333-AGI after opencode reported "FED failed" and the actual cause was `LITELLM_MASTER_KEY` missing from the opencode process environment.
> **Doct:** Probe before declare. Surface real upstream errors instead of swallowing them.
> **Pair with:** `references/provider-wiring-qwen-individual-2026-08-08.md`, `references/live-state-2026-08-08.md`.

## The problem this addresses

opencode's chat UI collapses every upstream error from `litellm-federation` (`127.0.0.1:4000`) into a one-word status:

```
FED failed
```

The actual upstream body — the part that tells you *why* it failed — never reaches the user. Operators chasing this symptom have three plausible hypotheses: (a) FED is genuinely down, (b) the API key is missing, (c) the opencode config has a bad alias. Distinguishing them takes two curl probes and 4 seconds. The wrapper installs that probe as a pre-flight so the answer surfaces every launch, no thinking required.

## The two FED surfaces (verified 2026-08-08)

| | `fed-router` MCP | `litellm-federation` proxy |
|---|---|---|
| Port | `:7074` | `:4000` (forwarded to `100.64.0.2:4000`) |
| Transport | FastMCP 3.4.4 / Streamable-HTTP | OpenAI-compatible HTTP |
| Tools | `fed_route`, `fed_status`, `fed_probe`, `fed_contrast`, `fed_health` | `agi-333`, `asi-555`, `apex-888`, `opencode`, `openclaw`, `dispatch`, … |
| Consumer | agentic MCP clients (route advisor) | opencode / Hermes / all chat-completion clients |
| Symptom when down | MCP error envelope with `code` + `message` | UI says "FED failed" — opaque |

**Rule of thumb:** if the symptom comes from opencode / Hermes / a chat UI → it's almost always the proxy. If the symptom comes from an MCP client calling `fed_*` → it's the MCP advisor.

## Probe recipe (the doctor's two-probe core)

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a

# Probe 1: with key (does the gateway work?)
curl -s -w '\nHTTP %{http_code} TIME %{time_total}s\n' --max-time 5 \
  http://127.0.0.1:4000/v1/models \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  | head -c 400

# Probe 2: without key (mirrors what opencode sees if its env is empty)
curl -s -w '\nHTTP %{http_code} TIME %{time_total}s\n' --max-time 5 \
  http://127.0.0.1:4000/v1/models \
  -H "Authorization: Bearer no-key-test" \
  | head -c 400
```

### Reading the result

| Probe 1 | Probe 2 | Verdict | Action |
|---|---|---|---|
| 200 with model list | 401 | **KEY_MISSING in opencode env** | `source /root/.secrets/kunci-mas.env` before launching opencode |
| 200 with model list | 200 | **FED alive, upstream problem elsewhere** | Check opencode agent whitelist vs provider roster |
| 5xx / connection refused | 5xx / connection refused | **Gateway genuinely down** | `systemctl status litellm-federation litellm-local-forward` |
| 401 | 401 | **Key wrong / revoked** | Cross-check `LITELLM_MASTER_KEY` in `kunci-mas.env` |

## The wrapper: `opencode-fed-preflight.sh`

```bash
#!/usr/bin/env bash
# opencode-fed-preflight.sh — wraps `opencode` invocations with a 1-shot FED health probe.
# T0 read-only. No path mutation. Safe to alias.
set -u

diag=$(/root/scripts/fed-doctor.sh --json 2>/dev/null)
state=$(echo "$diag" | jq -r '.gateway' 2>/dev/null)

if [ "$state" != "UP" ]; then
  echo "⚠️  FED pre-flight: $state"
  echo "$diag" | jq -r '"  diagnostic: \(.diagnostic)\n  fix:        source /root/.secrets/kunci-mas.env"'
fi

exec /usr/local/bin/opencode "$@"
```

Install in `~/.bashrc`:
```bash
alias opencode='/root/scripts/opencode-fed-preflight.sh'
```

After install: every opencode launch prints a one-line status. UP → silent (zero noise). KEY_MISSING → "FED pre-flight: KEY_MISSING" + the actual upstream body + the fix command.

## The doctor: `fed-doctor.sh`

Returns four signals:

| Signal | Healthy | Unhealthy |
|---|---|---|
| `gateway` | `UP` | `KEY_MISSING` / `DOWN` |
| `models` | 12 (the live roster) | 0 |
| `advisor` | `healthy` | `DOWN` |
| `local_forward` | `UP` | `DOWN` |
| `key_test_with_auth` | `http_200` | non-200 |
| `key_test_without_auth` | `http_401` | anything else |

```bash
# Human-readable
$ /root/scripts/fed-doctor.sh
FED gateway  : UP (12 models)
FED advisor  : healthy (:7074)
Local fwd    : UP (:4000 → 100.64.0.2:4000)
Auth probe   : with-key=OK · without-key=http_401

# Machine-readable
$ /root/scripts/fed-doctor.sh --json
{"gateway":"UP","models":12,"advisor":"healthy","local_forward":"UP",
 "key_test_with_auth":"http_0","key_test_without_auth":"http_401","diagnostic":"healthy"}

# Strict mode (for cron / health-checks)
$ /root/scripts/fed-doctor.sh --strict; echo "rc=$?"
FED gateway  : KEY_MISSING (0 models)
...
rc=1
```

## Why this isn't a permanent fix to FED itself

The "FED failed" string lives in opencode's UI, not in the litellm-federation gateway. To permanently fix the swallowing we'd need to either (a) fork opencode or (b) wrap every chat-completion in a smarter error handler. Both are T3 territory (vendor modification / cross-process dispatcher change). The pre-flight is **T0/T1-only** and surfaces the truth without forking anything. It's the same posture as `fed-doctor` itself: probe before declare, surface before hide.

## Reversibility

| Piece | Location | Revert |
|---|---|---|
| Doctor script | `/root/scripts/fed-doctor.sh` | `rm /root/scripts/fed-doctor.sh` |
| Pre-flight wrapper | `/root/scripts/opencode-fed-preflight.sh` | `rm /root/scripts/opencode-fed-preflight.sh` |
| Bashrc alias | `~/.bashrc` (3 lines after the `forge` alias) | delete the alias line |
| Federation services | not touched | n/a |

No systemd unit was added or modified. No `/root/.secrets/` file was modified. No service was restarted. The fix is **reversible in three commands**, and no production state changed.

## The "don't auto-codify" doctrine

This skill's wrapper exists because the symptom is recurring and silent. **Don't** add it as a permanent tool, agent, or cron job without F13 — it's a T0 probe wired as a personal diagnostic. If a sibling agent later proposes "let's wrap every MCP call with fed-doctor", push back: that pattern would become a permanent monitoring layer and we'd accumulate the same entropy the doctrine warns against. The wrapper stays in `~/.bashrc` because it's the operator's terminal, not the kernel's.

## Reference transcripts

Live probe that triggered this:

```text
# Symptom: opencode reports "FED failed"
# Probe without key (mirrors opencode):
$ curl -s -w '\nHTTP %{http_code}\n' --max-time 5 \
    http://127.0.0.1:4000/v1/models -H "Authorization: Bearer no-key-test"
{"error":{"message":"Authentication Error, No api key passed in.","type":"auth_error","param":"None","code":"401"}}
HTTP 401

# Probe WITH key (real state):
$ curl -s --max-time 5 -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
    http://127.0.0.1:4000/v1/models
{"data":[{"id":"hermes-asi",...},{"id":"agi-333",...},{"id":"asi-555",...},{"id":"opencode",...},
{"id":"openclaw",...},{"id":"apex-888",...},{"id":"dispatch",...},{"id":"asi-555-audio",...},
{"id":"asi-555-video",...},{"id":"fed/vision",...},{"id":"fed/audio",...},{"id":"fed/image-gen",...}],
"object":"list"}
```

Twelve models visible when the key is loaded. Zero when missing. Same gateway. Two different truths. The wrapper collapses that into "FED pre-flight: KEY_MISSING" so the next operator doesn't have to rediscover the dual-probe.