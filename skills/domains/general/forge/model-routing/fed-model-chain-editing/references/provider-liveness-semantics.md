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
- **OpenCode Go** — requires the `x-opencode-session` header on the chat path; without it the request fails for a reason unrelated to the provider's health.
- **Weekly/monthly quota walls** are common on Chinese token plans and coding plans. The reset timestamp lives in the 429 body; capture it rather than guessing.
- **Hybrid vendors** — the same vendor can be reachable through a direct key and through a router with different health. A router 200 does not testify to the direct lane, or vice versa.

## Probe Discipline

1. Probe **every** rung in the lane, not just the one you suspect — a chain is only as fast as its first dead hop.
2. Save bodies to files (`-o /tmp/_p`) and read them; do not eyeball a status alone.
3. Record the reset timestamp when you find a 429; that is the earliest meaningful re-probe.
4. Re-probe at answer time, not from memory or from a report — another agent's status view is a hypothesis.
5. Distinguish *provider dead* from *key dead* from *quota dead* from *scope dead*. Each has a different fix, and only one of them is a chain edit.
