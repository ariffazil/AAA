# Fallback-chain collapse — wawa node (srv1642546), 2026-08-15

Verified incident + fix. Reported to F13 as: "bot replies raw JSON and leaks function-call
schema after `/model` switch". Banner claimed provider `af-forge-fed`, model `hermes-asi`.

## The chain, in failure order (from live gateway log)

| Tier | Provider | Failure signature | Root cause |
|---|---|---|---|
| 1 primary | `af-forge-fed` (FED haproxy on af-forge) | Connection error | haproxy bound `127.0.0.1:4000` only + no UFW rule for Tailscale subnet → ping 1ms OK, TCP dead |
| 2 | Gemini 3.5 flash | HTTP 400 | Hermes v0.17 tool schema rejected upstream (`actions.items: missing field`) |
| 3 | MiniMax (Token Plan) | HTTP 401 invalid key | stale key in node `.env`; wrapper never sourced the vault |
| 4 | ILMU | HTTP 402 | plan exhausted, no allocation |
| 5 terminal | Ollama `qwen2.5-coder:1.5b` | "success" | 1.5B local model answered → garbage JSON + schema leak |

## Cross-node network diagnosis ladder

1. `ping` proves nothing about TCP — ICMP passes while UFW drops the port.
2. `nc -zv <ts-ip> 4000` from the remote node is the real test.
3. On the host, check the proxy bind: haproxy `127.0.0.1:4000` = unreachable from any
   other node regardless of firewall rules.
4. `ufw status` on the host: no `100.64.0.0/10` (Tailscale) rule = remote nodes blocked.
5. LiteLLM may run on a different port than the proxy frontend (observed: LiteLLM `:4011`
   on `0.0.0.0`, haproxy frontend `:4000`). Test the port the CLIENT actually uses.

## Fix (all commands verified live)

```bash
# host (af-forge): expose frontend to Tailscale only — haproxy injects the key,
# so subnet-only exposure is the sanctioned perimeter
#   haproxy.cfg: bind *:4000
ufw allow from 100.64.0.0/10 to any port 4000 proto tcp

# remote node: live chat-test BEFORE any config change
curl -s http://<ts-ip>:4000/v1/chat/completions -H 'Content-Type: application/json' \
  -d '{"model":"i-arif","messages":[{"role":"user","content":"reply WAWA-OK"}]}'
# expect a real completion containing WAWA-OK

# remote config: primary = verified proxy; DELETE 401/402 tiers from the fallback chain
# wrapper: source the vault env (else every direct provider 401s)
# restart: hermes ... --replace   (stale pidfile makes a fresh instance exit — race seen live)
```

## Post-restart verification checklist

- Exactly one process; pidfile matches its PID (a second spawn attempt racing an old
  pidfile writes scary ERROR lines — confirm which PID actually owns the log lines).
- `ss -tnp | grep api.telegram.org` → ESTABLISHED connections (Telegram polling alive).
- Age every scary log error by line number/timestamp BEFORE owning it: Telegram connect
  timeouts with 120s backoff and old `No connected db` proxy errors were chronic node
  noise that predated the restart — not regressions.

## Nodes involved

- wawa node `srv1642546` — `hermes-agent.service` ("Hermes ASI Gateway for Azwa"), Hermes v0.17
- af-forge — FED LiteLLM `:4011` (`0.0.0.0`) behind haproxy `:4000`, UFW perimeter
