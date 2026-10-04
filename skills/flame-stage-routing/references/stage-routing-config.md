# Stage Routing Config — Full Reference (2026-08-12)

## Source: `/root/FLAME/flame_config.json` → `routing.stage_routing`

### Tiers

```json
{
  "T0_SOVEREIGN": {
    "description": "Local Ollama — owned layer, zero cost, zero network",
    "provider": "ollama",
    "model": "qwen2.5:3b",
    "fallback_chain": "RM0-TOOLS-FREELOOP",
    "est_traffic_share": 0.75
  },
  "T1_EXECUTION": {
    "description": "Free cloud — Groq/SEA-LION/Gemini for medium tasks",
    "chain": "RM0-TOOLS-FREELOOP",
    "est_traffic_share": 0.18
  },
  "T2_FRONTIER": {
    "description": "Governed/paid — DeepSeek V4 Pro for complex reasoning",
    "chain": "GOVERNED-ONLY",
    "est_traffic_share": 0.07
  }
}
```

### Rules

| Tier | match_type | Patterns | Description |
|------|-----------|----------|-------------|
| T0_SOVEREIGN | tool_name | grep, grep_search, glob, read_file, list_directory, run_shell_command:curl, run_shell_command:git status/log/diff, run_shell_command:cat/head/tail/wc/echo/ls, monitor, health_probe, fed_health/status/probe, drift_check, symlink_check | Read/grep/probe — trivial compute, send to Ollama |
| T1_EXECUTION | tool_name | edit, write_file, notebook_edit, replace, run_shell_command:pytest/npm run/python3 -m/make/systemctl restart/docker/pip install | File mutations, tests, builds — medium complexity, free cloud |
| T2_FRONTIER | tool_name | agent, create_sub_session, exit_plan_mode, enter_plan_mode, artifact | Multi-step reasoning, architecture, subagents — needs frontier |
| T2_FRONTIER | domain_tag | [DOMAIN:PETRONAS], [CLASS:LEGAL_PROSE], [DOMAIN:PARLIAMENT], [CLASS:CREATIVE_PROSE] | PETRONAS/legal/parliamentary — F2 exception, always frontier |
| T2_FRONTIER | context_keyword | surat, tuntutan, audit, PAC, parlimen, constitutional, floor_check, APEX SWOT, QQQ, musyawarah, VAULT999, SEAL | Constitutional/governance keywords — must not degrade |

### Payload Auto-Classifier (classify_payload)

When no `task_class` is explicitly provided, `classify_payload(prompt)` runs AFTER stage routing:

| Class | Patterns | Route |
|-------|----------|-------|
| domain_petronas | [DOMAIN:PETRONAS], petronas, PETRONAS, upstream oil | SEA-LION BM-native |
| tool_local | grep, read_file, cat, curl, git log/diff/status/show, find/, ls/, wc - | Ollama → Groq |
| architect | architecture, refactor, schema design, system design, DRY | Groq deep cloud |
| (empty) | none matched | default chain |

Order: domain > tool_local > architect (specificity wins).

## Related Provider Config

### Z.ai Direct Coding Plan (for OpenCode + FED)

```yaml
# OpenCode direct provider (opencode.json → provider.zai-direct)
baseURL: https://api.z.ai/api/coding/paas/v4
apiKey: {env:ZAI_API_KEY}
models: glm-5.2, glm-5, glm-5-turbo, glm-5.1, glm-4.7, glm-4.6, glm-4.5-air, glm-4.5

# FED litellm route (A-FORGE/litellm-config.yaml)
- model_name: zai-pro
  litellm_params:
    model: openai/glm-5.2
    api_base: os.environ/ZAI_API_BASE
    api_key: os.environ/ZAI_API_KEY
```

**Z.ai Coding Plan Pro limits:** 12,000 credits/5h, 60,000 credits/week.
**Sovereignty caveat:** US Entity List + PRC infra — non-sensitive workloads only.
**Endpoint:** `/api/coding/paas/v4` (Coding Plan, NOT pay-as-you-go `/api/paas/v4` which returns 1113).

## Key Env Vars

```bash
ZAI_API_KEY=...          # 49 chars, vault.env
ZAI_API_BASE=https://api.z.ai/api/coding/paas/v4
ZAI_DIRECT_ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
ZAI_DIRECT_OPENAI_BASE_URL=https://api.z.ai/api/coding/paas/v4
```
