# FED_ZEN_MANIFEST.md
Generated: 2026-09-08 (Asia/Kuala_Lumpur) · Executor: Hermes/forge-777 · Authority: ARIF (F13)

## Verdict: SEAL (advisory) — executed with evidence

## What Changed (all reversible, backups listed)

1. **Context truth fixed** — `/root/.hermes/config.yaml` `model.context_length: 1000000`
   (was silent 256k default from probe-down; upstream qwen3.8-max real limit 1M).
2. **LiteLLM config deduped** — 213 → 85 model_list entries.
   Mega-cascades trimmed to proven/strong upstreams (cap 5/group):
   agi-333 37→5 · opencode 37→5 · openclaw 37→5 · hermes-asi 43→11. 128 dead entries removed.
   Evidence: 30d SpendLogs — only 4 of agi-333's 37 upstreams ever served traffic.
3. **DB wired back to LiteLLM** — DATABASE_URL re-enabled in systemd override +
   `general_settings.database_url` in config. Key management + virtual keys now work
   (broken since 2026-09-06 FQ fix; `allow_requests_on_db_unavailable: true` hid it).
   Root cause chain: prisma query-engine binary for openssl-3.5.x missing → fetched +
   placed at expected paths.
4. **Zen 9-lane key minted** — alias `fed-zen-9-lanes`, stored `/root/.secrets/fed-zen-key.env` (600).

## The 9 Visible Lanes

| Lane | Alias | Purpose |
|---|---|---|
| ARIF | i-arif | Sovereign seat — chat, doctrine, strategy |
| THINK | agi-333 | Deep reasoning |
| RESEARCH | asi-555 | Search + synthesis, witness |
| COURT | apex-888 | Governance judgment |
| FORGE | forge-777 | Execution, mutation, coding |
| VISION | fed/vision | OCR, image understanding |
| IMAGE | fed/image-gen | Image generation |
| VOICE | fed/audio | ASR + TTS |
| CODE | opencode | Coding workflows |

Verified live: zen key → /v1/models returns exactly these 9.
Blocked model via zen key → 401 "key not allowed to access model". Enforcement real.

## Topology (corrected truth, supersedes skill aaa-litellm-ops)

```
Hermes gateway (KVM8)
  → HAProxy :4000 (master-key injection)
      ├─ primary: KVM4 :4000 (LiteLLM, same config via A-FORGE repo)
      └─ backup:  KVM8 :4013 (litellm-federation.service, venv, DB-wired)
Config (both): /root/A-FORGE/litellm-config.yaml (md5-identical copies)
DB: postgres 127.0.0.1:5432/litellm (KVM8)
```

## Rollback

- Config: `cp /root/A-FORGE/litellm-config.yaml.bak-fedzen-v3-20260907 /root/A-FORGE/litellm-config.yaml && systemctl restart litellm-federation`
- Systemd: `override.conf.bak-fedzen-db2-20260907` in same .d dir
- Hermes: `cp /root/.hermes/config.yaml.bak-20260907-fedzen /root/.hermes/config.yaml`
- Zen key: harmless if unused; revoke via /key/delete or ignore.
