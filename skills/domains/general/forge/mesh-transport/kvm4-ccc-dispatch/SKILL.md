---
id: kvm4-ccc-dispatch
name: kvm4-ccc-dispatch
version: 1.0.0
description: "Use when HERMES ASI dispatches coding to KVM4 CCC workers."
owner: Hermes-Prime
risk_tier: T1
floor_scope: [F1, F2, F4]
autonomy_tier: T1
capability_tier: coding-fabric-gateway
ecology_state: WARM
---

# KVM4 CCC Worker Dispatch

HERMES ASI (Telegram, KVM8) dispatches coding tasks to the KVM4-forge CCC
worker pool over tailscale mesh SSH. KVM4 is a dedicated 4-core/15GB worker
box (srv1946043, 100.64.0.5) with 5 coding harnesses installed and ZEN-aligned
to route through the sovereign FED gateway — **zero local secrets**.

## Topology

```
HERMES ASI (KVM8 Telegram)
   │  ccc-remote <harness> "<task>"
   ▼
ssh root@100.64.0.5 (tailscale mesh)
   ▼
KVM4 CCC harnesses: opencode · codex · qwen · kimi · aider
   ▼  (all point at http://100.64.0.2:4000/v1)
KVM8 haproxy :4000 → litellm :4013 (auth injected)
   ▼
59 lanes: forge-777 (default), deepseek-v4-flash, agi-333, qwen3.8-max…
```

## Dispatch Commands (run from KVM8)

```bash
# Default worker (opencode, forge-777 lane)
ccc-remote opencode run --model litellm-federation/forge-777 "<task>"

# Codex (pinned deepseek-v4-flash; responses API)
ccc-remote codex exec --skip-git-repo-check "<task>"

# Qwen (needs --auth-type openai)
ccc-remote qwen -p "<task>" --auth-type openai

# Kimi
ccc-remote kimi --prompt "<task>"

# Aider (needs gateway flags; model prefixed openai/)
ccc-remote aider --message "<task>" --model openai/deepseek-v4-flash --openai-api-base http://100.64.0.2:4000/v1 --openai-api-key fed-injected --no-auto-commits --yes-always
```

## Verified 2026-09-02

| Harness | Version | Probe | Status |
|---|---|---|---|
| opencode | 1.18.25 | OPENCODE-KVM4-OK | PASS |
| codex | 0.152.0 | CODEX-KVM4-OK | PASS |
| qwen | 0.22.3 | QWEN-KVM4-OK | PASS |
| kimi | 0.38.0 | KIMI-KVM4-OK | PASS |
| aider | 0.86.2 | AIDER-KVM4-OK | PASS |

## M1 Migration (2026-09-02) — opencode server NOW on KVM4

- `opencode.service` ACTIVE on KVM4 (localhost:4096, `/root/.opencode/bin/opencode`, PATH set in unit). Binary 1.18.25, RSS ~350MB.
- KVM8 `opencode.service` STOPPED (unit untouched — rollback = `systemctl start opencode` on KVM8).
- KVM4 config uses FED gateway (`litellm-federation/forge-777`) — NO zai-direct creds, zero secrets by design.
- Receipt: `/root/work/receipts/M1_RECEIPT.json`.

## Pitfalls

- codex 0.152 requires `wire_api = "responses"` (chat is removed); pin model
  to `deepseek-v4-flash` — forge-777 responses cascade can hit quota-dead rungs.
- qwen non-interactive needs `--auth-type openai` (no auth prompt on headless).
- kimi config schema: `[providers.*]` + `[models."provider/model"]` blocks.
  A wrong `[models.fed-gateway]`-style config crashes the CLI with a stack dump.
- aider needs python3-dev/build-essential to compile numpy/scipy on Python 3.14;
  prefer `pip install --only-binary :all:` in a venv.
- haproxy health check must be `/health/liveliness` (litellm) — `/health/readiness`
  times out and marks the backend DOWN (fixed 2026-09-02).
- KVM4 gateway is `http://100.64.0.2:4000/v1` (OpenAI) or `http://100.64.0.2:4000`
  (Anthropic compat). Zero secrets: haproxy injects Authorization.

## Verification

```bash
curl -s http://100.64.0.2:4000/health/liveliness   # expect "I'm alive!"
ccc-remote opencode --version                       # expect 1.18.x
```
