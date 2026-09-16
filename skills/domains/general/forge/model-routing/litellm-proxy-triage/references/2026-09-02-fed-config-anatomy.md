# FED Config Anatomy — measured 2026-09-02 (Zen-FED audit)

Session: Arif asked to "zen the FED". Copilot 888 verdict: probe-before-propose,
lane≠model, inventory-before-mutation. This file is the measured baseline —
re-measure before trusting any number (config drifts).

## Config census (as of 2026-09-02 15:3x MYT)

- File: /root/A-FORGE/litellm-config.yaml — 1923 lines, mtime 2026-09-02 06:16.
- model_name entries: 152 across ~9 alias lanes:
  agi-333 ×40, hermes-asi-vision ×21, fed/vision ×21, i-arif ×17 (+5 commented),
  asi-555 ×12 (+3 commented), apex-888 ×10 (+3 commented), forge-777 ×9,
  fed/audio ×5, fed/image-gen ×2, agi-333 commented ×4.
- Dead snapshot models found (trim candidates): qwen3.7-max-2026-05-17,
  qwen3.7-max-2026-05-20, qwen3.7-max-2026-06-08, qwen3.7-plus-2026-05-26,
  qwen3-max-preview, qwen-plus-latest (rolling aliases — always pin or drop).
- Embedding/rerank entries: ZERO. `aembedding` only appears in redis cache
  supported_call_types. 999-ARCHIVE lane needs fed/embed: tongyi-embedding-vision-plus
  + qwen3-rerank via DASHSCOPE PAYG lane (not on Token Plan allowlist).
- Token Plan: 58 entries on https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1,
  api_key via env (os.environ), never hardcoded. Verified correct.
- Team Edition models present: kimi-k2.7-code ×3, kimi-k2.6 ×3, glm-5.1 ×3,
  MiniMax-M2.5 ×5, deepseek-v3.2 ×6, wan2.7 ×2.
- router_settings: simple-shuffle, num_retries 2, allowed_fails 2, cooldown 60s,
  enable_pre_call_checks true. context_window_fallbacks chain present per alias.
- litellm_settings: callbacks [] (PrometheusLogger removed 2026-09-02 — it caused
  AttributeError litellm_requests_metric on every success log = 100% CPU burn).
- Process: systemd litellm-federation on port 4013 (drop-ins override the base
  unit; CPUQuota=200%). HAProxy :4000 → 127.0.0.1:4013 (fed_primary).
- Note: `mcp fed fed_status` may throw "dictionary update sequence element" —
  do not trust it; probe with curl + systemctl + config census instead.

## 3-call probe recipe (ps/ss/config)

```bash
# 1. Process + port ownership (systemd vs orphan)
ps aux | grep -i litellm | grep -v grep
ss -tlnp | grep -E ':40(00|13)'

# 2. Config census (alias lanes + rot classes)
grep -c 'model_name:' /root/A-FORGE/litellm-config.yaml
grep 'model_name:' /root/A-FORGE/litellm-config.yaml | sort | uniq -c | sort -rn
grep -oE 'model: openai/qwen[0-9a-z.-]+-202[0-9]-[0-9-]+' /root/A-FORGE/litellm-config.yaml | sort -u
grep -cE 'embedding|rerank' /root/A-FORGE/litellm-config.yaml

# 3. Steal time (hypervisor, not litellm, is usually the top CPU consumer)
vmstat 2 3   # st column > 15% = hypervisor steal; see autonomous-substrate law in AGENTS
```

## Zen-FED proposal shapes (graded, 888-reviewed)

- P1 ZEN-SLIM: trim dead snapshots + commented blocks, archive retired entries to a
  registry JSON (fields: model, alias, last_verified, reason) — never raw delete.
  Backup config first, restart via systemd. Low risk, fully reversible.
- P2 ZEN-LANE: hot/cold split — flash-class models stay in shuffle pool; max/pro
  models called by explicit name only. Add fed/embed alias (tongyi-embedding-vision-plus
  + qwen3-rerank, DASHSCOPE PAYG) as 999-ARCHIVE retrieval spine. Medium risk.
- P3 ZEN-SWAP: replace LiteLLM with fed-router native (Rust, :7074). Multi-day,
  high risk — this is the inference heart. HOLD until P1+P2 proven.
- Recommended combo: P1+P2 in one pass. P3 parked.

## Orthogonal stack mapping (capability lanes, not models)

i-ARIF (voice/audio/constitutional interface), 333-AGI (reasoning/planning),
555-ASI (human-meaning), 777-FORGE (reality compression/eureka),
888-APEX (constitutional reflex/godel lock), 999-ARCHIVE (retrieval/embeddings —
currently NO substrate in config). A single vendor model (e.g. qwen3.8-max) can
and does serve multiple lanes — that is correct by doctrine, not redundancy.
