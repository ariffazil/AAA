---
name: federation-llm-gateway-debug
description: Use when debugging litellm routing, wallets, or drift.
---

# Federation LLM Gateway Debugging (litellm)

Class of task: figure out *which* model/wallet/seat is failing and *why*, without
changing anything and without leaking secrets. This comes up constantly in the
AAA federation (litellm gateway in front of MiniMax / Qwen token-plan / DeepSeek /
z.ai / mimo).

## Credential hygiene (always-on — user-corrected, binding)

- **Never echo a key/token into chat or into command output that gets pasted to a
group.** A secret that enters a chat log is compromised by definition — rotate it,
don't just "be careful next time."
- Check presence/length with `printenv VAR | wc -c` (length only, no value), NEVER
`echo $VAR` and NEVER `docker inspect <c> | jq '.Config.Env'` — that dumps the key
into pasteable output.
- When the other agent or the human pastes a key in-chat, the FIRST move is flag it
as compromised + rotate, before any other diagnosis.

## Attribution discipline (the core pitfalls)

- **`served_by` / `model` on a SUCCESSFUL completion names who answered that call —
NOT which wallet/upstream failed on a different call.** Don't infer the dead wallet
from the live one. A call that succeeded via fallback tells you the fallback, not
the failure.
- **"Insufficient Balance" (OpenAIException) is a generic router message, not a
wallet name.** Two seats can emit different wallet-dead messages
(`DeepseekException: Insufficient Balance` vs `OpenAIException: Insufficient Balance`)
for different upstreams. Anchor on the EXACT literal you are asserting — grepping a
guessed literal (e.g. `402 Payment Required`) returns a false zero.
- **Two nodes = two worlds.** KVM8 and KVM4 run separate litellm containers with
separate configs and separate keys. Never generalize one seat's finding ("0 rungs
use this wallet") to the other. State which seat each probe ran on; a claim that
holds on one seat is UNQUANTIFIED on the other until probed there.
- **`db: Not connected` is by design** when `database_url` is unset in the container
(`allow_requests_on_db_unavailable: true`). It means spend logs are memory-only
(lost on restart), not a fault. Don't flag it as a defect.

## Probe technique (fast, no-mutation)

- To name a dead model: POST `/v1/chat/completions` with `max_tokens: 1` to that
alias and read the error body + the cooldown dump it returns.
- `/v1/models` lists what is CONFIGURED, not whether a model can actually serve.
Absence there ≠ disabled; a live completion is the real test.
- **The cooldown dump (`Cooldown Deployments=[...]`) carries `api_base` per
deployment id** — that is how you name the wallet, not the completion log.
- `model_list` group count vs `/v1/models` id count differs because of
`model_group_alias` dedup + provider ids — it is not drift. Don't report the delta
as a defect.
- Models without a `fallbacks:` key are the hard-break class: when their upstream
fails, litellm returns `no fallback model group was found`. Fallbacks that point at
models currently in cooldown are *effectively* no-fallback even though declared.

## Config source-of-truth (per seat)

- Verify the live bind mount before editing anything:
  `docker inspect <container> --format '{{json .Mounts}}'`.
- KVM8: container `litellm-federation`, config `/root/A-FORGE/litellm-config.yaml`
  bind-mounted to `/app/config.yaml`. KVM4: container `litellm`, config
  `/docker/litellm/config.yaml`. They are DIFFERENT files — one patch does not fix
  both seats.

## Single-writer rule (shared repo / shared config)

- Before writing to a repo or config another agent may be touching, probe
  `git log --oneline -1`, `git status --short`, and file `mtime`. If a concurrent
  writer has uncommitted work, STOP and get a single-owner decision — do not fight
  over the same file (two editors corrupt it).
- If you wrote an edit and then discover it collided with someone else's
  in-flight work, revert YOUR orphaned edit (`git checkout -- <file>`) rather than
  leaving a half-merged mess.

See `references/litellm-probes.md` for ready-to-run probe commands and the
wallet-attribution decision table.
