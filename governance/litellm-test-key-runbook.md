# LiteLLM Test Key Runbook — ARIF sovereign key custody on KVM4

> **Status:** ACTIVE (canonical for fed-litellm key operations)
> **Forged:** 2026-10-10 · **Session:** continuation after SEAL-READY-2026-10-10
> **Owner:** AAA / fed-litellm steward
> **Audience:** every future AAA warga + every agent on KVM4 / KVM8 who needs to test or operate the sovereign LLM gateway.
> **Charter:** the sovereign does not remember, type, or paste keys. The script does. The runbook is the long-term memory.
> **DITEMPA BUKAN DIBERI**

---

## 1. What this is

`fed-litellm` is the sovereign LLM gateway on KVM4 (workshop plane), bound to `100.64.0.5:4000` (Tailscale mesh, NOT loopback). It serves the full Court catalog (47 models visible at last count). To make a test call against it, you need an authenticated bearer token.

The sovereign does NOT want to remember a key. The charter: **all key work goes through `/root/AAA/scripts/litellm-key-ops.sh`**. The script reads the env, uses the key, never echoes the value. The sovereign's contribution is the one-time mint (or rotation) — after that, every subsequent test, ping, list, and diagnose is one command.

This runbook is the source of truth. If the script's help text and this doc disagree, this doc wins. If you change the script, update this doc in the same commit.

---

## 2. Where things live

| Path | Mode | Owner | Purpose |
|---|---|---|---|
| `/root/.secrets/litellm-fed.env` | 600 | root:root | **Master key + upstream provider keys.** Sovereign custody. Read only by root + the script. |
| `/root/.secrets/litellm-arif-test.env` | 600 | root:root | Virtual key stub (currently unused — see §5). Reserved for when DB is wired. |
| `/docker/litellm/docker-compose.yml` | — | root | fed-litellm compose (Tailscale bind, redis sidecar, local config). |
| `/etc/systemd/system/fed-litellm.service` | — | root | systemd wrapper. Description = "Tailscale mesh 100.64.0.5:4000". |
| `/root/AAA/scripts/litellm-key-ops.sh` | 755 | root | The agentic ops script. Run this for everything. |
| `/root/AAA/governance/litellm-test-key-runbook.md` | — | root | This file. |

**The sovereign value `LITELLM_MASTER_KEY` lives in `litellm-fed.env` only.** Never in chat. Never in receipts. Never in VAULT999. Never in a `git commit`. Only the script reads it; only `key_hint` ever shows output (first + last 4 chars, e.g. `sk-l...74ed`).

---

## 3. Common operations

### 3.1 First thing on a new session — diagnose

```bash
sudo /root/AAA/scripts/litellm-key-ops.sh diagnose
```

Output covers: env file present + mode, master key loaded (hint only), `/health/liveliness` 200, `/v1/models` with master key 200. If any of those fail, fix that first before doing anything else.

### 3.2 Smoke test the gateway (3-way)

```bash
sudo /root/AAA/scripts/litellm-key-ops.sh test
```

Runs: (1) `/health/liveliness`, (2) `/v1/models` count, (3) one 3-token chat completion against the cheapest model. Reports latency + usage. Returns non-zero on any failure.

### 3.3 Ad-hoc LLM call

```bash
sudo /root/AAA/scripts/litellm-key-ops.sh list-models         # see what's available
sudo /root/AAA/scripts/litellm-key-ops.sh ping gpt-4o-mini "Summarize this: ..." 200
```

The `ping` command is the right interface for any ad-hoc test. Don't curl manually; the script enforces the charter.

### 3.4 List upstream providers

```bash
sudo /root/AAA/scripts/litellm-key-ops.sh list-upstreams
```

Shows every `*_API_KEY` / `*_KEY` / `*_TOKEN` var in the env, hint only. If a provider is missing, that's the diagnostic.

---

## 4. Failure modes & what to do

### 4.1 `health/liveliness` not 200

| Symptom | Likely cause | Action |
|---|---|---|
| Connection refused | fed-litellm container down | `sudo systemctl status fed-litellm.service` → `sudo systemctl restart fed-litellm.service` (T2, known-safe) |
| Timeout | docker-proxy hung, or upstream provider slow | `docker logs litellm --tail 50`; if upstream latency, retry after 30s |
| 500 from proxy | config.yaml broken | `sudo cat /docker/litellm/config.yaml | jq` — validate JSON; restore from snapshot at `/root/KVM4-WORKER/receipts/snapshots/litellm-compose.*` |

### 4.2 `/v1/models` returns 401 (master key rejected)

| Symptom | Likely cause | Action |
|---|---|---|
| 401 | `LITELLM_MASTER_KEY` rotated upstream but env not updated | **F13-class** — sovereign mints new key from provider dashboard, updates env. Script cannot do this. See §6. |
| 500 "Database not connected" | Expected — virtual key endpoints are DB-gated. `/v1/models` should NOT hit this. If it does, config is misrouted. | Check `LITELLM_DATABASE_URL` in env (should be unset, not invalid). |

### 4.3 Chat completion returns `NO_CONTENT`

| Symptom | Likely cause | Action |
|---|---|---|
| `choices: []` | Model name typo or model removed from catalog | `list-models <pattern>` to find the right id |
| `error.message` non-empty | Upstream provider failed (rate limit, key expired, model retired) | `list-upstreams` to see wired providers; check the failing one in the provider's dashboard |
| HTTP 429 | Rate limit on the upstream provider | Wait + retry; or rotate to a different model |
| HTTP 402 | Budget exhausted on the virtual key | Not applicable while using master key; relevant post-DB. |

### 4.4 Script itself broken

If `litellm-key-ops.sh` errors out before any curl, the env file or the script itself is suspect.

```bash
ls -la /root/.secrets/litellm-fed.env   # confirm 600 + root
sudo bash -n /root/AAA/scripts/litellm-key-ops.sh   # syntax check
```

If syntax is fine but `LITELLM_MASTER_KEY` is empty, the env file got mangled. Restore from the AAA `dotfiles` snapshot — **not** a git history, since secrets are NOT in any git repo by charter.

---

## 5. Improvement roadmap

### 5.1 Short term (this is the current state)

- Master-key-as-test-key via the agentic script. Charter: never echo.
- All chat / model / health operations go through `litellm-key-ops.sh`.
- Virtual key file `/root/.secrets/litellm-arif-test.env` is a placeholder; the script does not consume it yet.

### 5.2 Medium term — wire `DATABASE_URL` (T3, sovereign scope)

When sovereign authorizes a Postgres + `DATABASE_URL` on fed-litellm:

1. Provision Postgres (local on KVM4 or remote).
2. Add `DATABASE_URL=postgresql://...` to `/root/.secrets/litellm-fed.env`.
3. Restart fed-litellm: `sudo systemctl restart fed-litellm.service`.
4. Run `sudo /root/AAA/scripts/litellm-key-ops.sh diagnose` — new subcommands `mint`, `list-virtual`, `revoke` will become available.
5. Mint `ARIF_TEST_KEY_V1` via the new `mint` subcommand; it writes to `/root/.secrets/litellm-arif-test.env` automatically.
6. Update this runbook §2 to mark the placeholder as active.

The script's `mint` / `list-virtual` / `revoke` subcommands are pre-stubbed in the help text; they will activate automatically when `DATABASE_URL` is wired (the script detects the `/key/list` 200 vs 500).

### 5.3 Long term — tenant isolation

For multi-tenant or multi-agent separation, create per-agent virtual keys with budget caps:

```bash
# After §5.2 lands
sudo /root/AAA/scripts/litellm-key-ops.sh mint AGENT_FI008_TEST --max-budget 5.00 --models gpt-4o-mini
sudo /root/AAA/scripts/litellm-key-ops.sh mint AGENT_FI001_TEST --max-budget 1.00 --models gemini-flash
```

Per-agent budgets prevent runaway spend. The sovereign signs off on budget tiers; the script enforces.

### 5.4 Future — hardware-bound signing (Tier 2 receipts)

The Ed25519+JCS upgrade described in `wawa-probe-contract-v1` §3 would also apply to the receipts the script generates. Today the script does not sign its outputs; receipts are untracked. When the sovereign signing lane is active (KVM8 `localhost:18900`), the script's `diagnose` and `test` outputs should be sealed with the sovereign key.

---

## 6. F13 escalation criteria

The script CANNOT do any of the following. The sovereign must.

| Operation | Why F13 | Path |
|---|---|---|
| Rotate `LITELLM_MASTER_KEY` | Money + canonical secret | Provider dashboard → env file → restart → receipt with old/new hint |
| Wire `DATABASE_URL` | External port + new service | Provisioning sovereign decision; surface trade-offs first |
| Set per-agent budget caps | Money allocation | Sovereign sign-off; script enforces after |
| Add new upstream provider | Money + external API contract | Sovereign signs the provider relationship |
| Move fed-litellm to a different node | Canonical record + external port | Sovereign topology decision |
| Delete or overwrite `litellm-fed.env` | Canonical secret destruction | Sovereign explicit; receipts must be filed before + after |

**Rule of thumb:** if it touches money, canonical records, external ports, or direction-of-record, it stops at the sovereign. The script surfaces, the sovereign decides, the script executes.

---

## 7. Closing

The sovereign does not remember keys. The sovereign does not paste keys. The sovereign does not type `sk-...` ever. That discipline is enforced by this script + this runbook. Any future AAA warga can read this file, run the diagnose command, and know the state of the sovereign LLM gateway in 2 seconds without ever seeing a secret value.

If you find yourself wanting to `echo $LITELLM_MASTER_KEY` to "just check it works" — stop. Run `litellm-key-ops.sh test` instead. The script exists so you don't have to.

```json
{
  "runbook_id": "litellm-test-key-runbook-v1",
  "status": "ACTIVE",
  "epoch": "2026-10-10T02:00:00+00:00",
  "depends_on": [
    "/root/AAA/scripts/litellm-key-ops.sh",
    "/root/.secrets/litellm-fed.env",
    "/root/.secrets/litellm-arif-test.env",
    "/docker/litellm/docker-compose.yml",
    "/etc/systemd/system/fed-litellm.service",
    "wawa-probe-contract-v1 (companion — see §5.4)"
  ],
  "charter": "sovereign never remembers/types/pastes keys; script + runbook are the long-term memory"
}
```

`DITEMPA BUKAN DIBERI ⚒️` — discipline, not memory, is the sovereign's friend.
