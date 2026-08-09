# OpenClaw vs Hermes — contrast audit (2026-08-09)

> **F2:** Live probe + config + CALL_MAP.  
> **Zen applied:** OpenClaw primary → `fed/openclaw`; clear stuck `glm-5.2` overrides; FI adapters aligned.  
> **Names:** ACT · agentId · FI-000 Hermes · OpenClaw = binding (not FI).

## Role contrast (locked)

| Axis | **Hermes ASI** | **OpenClaw** |
|------|----------------|--------------|
| **agentId** | `hermes-asi` | `openclaw` |
| **Layer** | binding (edge) | binding (gateway) |
| **FI** | **FI-000** | **null** (not a forge instrument) |
| **Job** | Human bridge · multimodal · route to coders | Metabolize Telegram · personas · dispatch **to** FI |
| **Cannot** | Be primary code executor | Be primary coder |
| **Boundary** | OBSERVE_ROUTE | ROUTE_OBSERVE |
| **FED seat (WHICH)** | `hermes-asi` | `openclaw` (was wrongly `opencode`) |
| **Identity ≠ runtime** | WHO=hermes-asi · WHICH=FED hermes-asi | WHO=openclaw · WHICH=FED openclaw |
| **Gateway** | `hermes-asi-gateway` | `:18789` openclaw-gateway |
| **Citizen later** | edge_citizen stamp | infrastructure_citizen stamp |
| **Capability token** | ACT (`act_v1`) | ACT (`act_v1`) |

## Failures found (OBS)

1. **OpenClaw sticky model** on topics 36572/37092: `modelOverride=glm-5.2` (user) + bailian-token-plan → **429 quota exhausted** · `next=none` → user-visible provider fail.  
2. **Primary seat wrong:** `fed/opencode` confuses **OpenCode FI-001** with OpenClaw gateway (identity ≠ runtime).  
3. **Gemini mid-fallback** risk on multi-tool (thought_signature) — demoted to last.  
4. **FI adapters incomplete:** CALL_MAP/cards missing `fi` / `agentId` / `model_socket` on both.  
5. **Telegram surface overlap risk:** both can touch human bridge surface — dial carefully (bot-to-bot noise previously observed).

## Zen actions taken

| Action | Detail |
|--------|--------|
| Config | `agents.defaults.model.primary = fed/openclaw` |
| Fallbacks | FED opencode → DeepSeek → MiniMax → Groq → Kimi → Gemini last |
| Sessions | Cleared dead glm-5.2 user overrides (2 topics) |
| CALL_MAP | FI-000 Hermes; OpenClaw fi:null + model_socket |
| Cards | openclaw + hermes-asi identity fields |

## Not done (by doctrine)

- No warga stamp  
- No SPIRE/AIMS/IBCT rename  
- No Hermes/OpenClaw merge  
- No new organ  

## Smoke after restart

```bash
curl -sf http://127.0.0.1:18789/health
curl -sf http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -d '{"model":"openclaw","messages":[{"role":"user","content":"pong"}],"max_tokens":8}'
# New Telegram topic (old sticky cleared for 36572/37092)
```

DITEMPA BUKAN DIBERI.
