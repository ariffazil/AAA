# Provider Liveness Semantics

> Read the response **body**, not only the status code. Status codes collide across
> causes; the body names the cause and, for quota, the reset time.

## The Codes That Matter

| Code | Body says | Real meaning | Right move |
|---|---|---|---|
| 200 | model list | key authenticates | **not** proof of liveness — run a 1-token completion |
| 200 | chat completion | live | keep the rung |
| 402 | "check your subscription" | plan/seat lapsed | renewal — no auto-reset; remove or park the rung |
| 402 | balance/credit message | prepaid balance gone | top-up — the sovereign decides |
| 429 | quota exhausted + reset time | quota window | demote now, re-probe after the timestamp |
| 403 | plan limit | license scope | e.g. a coding-only seat rejecting direct API calls — key is fine, lane is not |
| 401 | auth | key rotated/revoked | fix the secret, not the chain |

## Per-Provider Quirks

- **Gemini** — `list-models` returning 200 says nothing about credit. Probe the model path (`:generateContent`). A depleted prepaid balance answers 429 while the key stays valid, so "key valid + 429" reads as *top-up needed*, not *dead key*.
- **Coding-plan seats** (Z.ai, MiMo, OpenCode Go, and similar) — often bill against a plan whose license scope is *coding tools only*. Direct chat calls can be rejected even while the seat is paid and healthy. Check the scope before declaring the seat dead.
- **Xiaomi MiMo** — the token-plan lane is one OpenAI-compatible base (the chain config points `api_base` at `os.environ/MIMO_BASE_URL`, the vendor host is `token-plan-sgp.xiaomimimo.com/v1`) and carries the whole family behind it: `mimo-v2.5-asr`, the `tts` / `tts-voiceclone` / `tts-voicedesign` trio, plus `mimo-v2.5` and `mimo-v2.5-pro`. Only **`mimo-v2.5` is omni-modal** (image/audio input); `mimo-v2.5-pro` is **text-only** — a vision rung pointed at `-pro` fails in a way that reads like a provider outage. The **MiMo Code CLI** at `/root/.config/mimocode/mimocode.json` is a separate consumer of the same key; do not read it as the chain config, and note its own permission map deny-lists edits to the secrets dir.
- **`.mmx` is MiniMax, not MiMo.** `/root/.mmx/config.json` points at `api.minimax.io`; the `mmx` CLI is MiniMax's. A credential hunt for Xiaomi under `.mmx*` finds the wrong vendor's key, and both vendors are live in this stack at once — read the `base_url` before believing a directory name.
- **OpenCode Go** — requires the `x-opencode-session` header on the chat path; without it the request fails for a reason unrelated to the provider's health.
- **Weekly/monthly quota walls** are common on Chinese token plans and coding plans. The reset timestamp lives in the 429 body; capture it rather than guessing.
- **Hybrid vendors** — the same vendor can be reachable through a direct key and through a router with different health. A router 200 does not testify to the direct lane, or vice versa.

## Probe Discipline

1. Probe **every** rung in the lane, not just the one you suspect — a chain is only as fast as its first dead hop.
2. Save bodies to files (`-o /tmp/_p`) and read them; do not eyeball a status alone.
3. Record the reset timestamp when you find a 429; that is the earliest meaningful re-probe.
4. Re-probe at answer time, not from memory or from a report — another agent's status view is a hypothesis.
5. Distinguish *provider dead* from *key dead* from *quota dead* from *scope dead*. Each has a different fix, and only one of them is a chain edit.
6. **Know which question the model list answers.** For a **capability census** — "does this stack route this model id at all?" — the router's own list is the right read (`curl -s http://127.0.0.1:4000/v1/models`, or `:4013` on the node itself). For **attribution** — which deployment served this request — it is worthless (see the parent skill's *Attribution*). Same endpoint, two different questions: a successful census must never be passed off as attribution.
