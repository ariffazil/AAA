# AAA Federation State — Live Map

> Forged 2026-08-14. One source of truth. Probe before trust.

## CLI Coders (verified installed)

| CLI | Version | Path | Default Model | Status |
|---|---|---|---|---|
| Kimi Code | 0.35.0 | /root/.kimi-code/bin/kimi | MiniMax-M3 | ✅ alive |
| Qwen Code | 0.21.10 | /root/.local/bin/qwen | GLM-5.2 z.ai | ✅ alive |
| OpenCode | 1.18.11 | /root/.npm-global/bin/opencode | FED router | ✅ alive |
| Codex | 0.147.0 | /root/.npm-global/bin/codex | FED codex alias | ✅ alive |
| Claude Code | 2.1.226 | /root/.local/bin/claude | claude-sonnet | ✅ alive |
| Aider | 0.86.2 | /home/arifos/.local/bin/aider | DeepSeek V3 | ✅ alive |
| Gemini CLI | 0.43.0 | /usr/bin/gemini | gemini-3.x | ✅ alive |
| Agy | 1.1.12 | /root/.local/bin/agy | gemini-3.x | ✅ alive |

## FED Router (LiteLLM — localhost:4000)

27 model aliases. Key routes:

```
i-arif          → Hermes edge bridge (universal floor)
hermes-asi      → Hermes ASI
agi-333         → Kimi/MiniMax/DeepSeek cascade
asi-555         → Qwen/GLM cascade
apex-888        → apex-judge (OpenCode/Zen)
codex           → FED codex alias
opencode        → OpenCode Zen
kimi-code       → Kimi managed
openclaw        → OpenClaw gateway
zai-pro         → GLM-5.2 direct
gemini-flash    → Gemini flash
gemini-pro      → Gemini pro
fed/vision      → multimodal routing
fed/image-gen   → image generation
fed/audio       → audio/voice
```

Two LiteLLM instances:
- `:4000` — main FED router (litellm-config.yaml)
- `:4011` — secondary (litellm-config.yaml, 1.4GB RAM)
- `:4012` — escape/fallback (escape-config.yaml)

## Organs (live health)

| Organ | Port | Status | Function |
|---|---|---|---|
| arifOS | 8088 | ✅ healthy | Constitutional kernel, F1-F13 |
| A-FORGE | 7071/7072 | ✅ healthy | Execution/mutation gate |
| arifFlow | 7073 | ✅ healthy | Metabolism, receipts |
| WEALTH | 18082 | ⚠️ degraded | Capital domain |
| WELL | 18083 | ⚠️ degraded | Human wellness |
| GEOX | 8081 | ⚠️ degraded | Geoscience |
| AAA | 3001 | ✅ alive | A2A gateway |
| OpenClaw | 18789 | ✅ alive | AGI gateway |

## Memory Architecture

```
H-axis (H1-H6)     → Arif's self-memory (/root/memory/)
P-axis (people/)   → Arif's model of others (ZKPC-encoded)
VVV (shadow void)  → Abstractions only, no content
L-axis (agent)     → Operational memory (flat, scattered)
VAULT999           → Immutable witness ledger
```

### H-axis layers (file counts verified 2026-08-14)

| Layer | Files | Status |
|---|---|---|
| H1 Capture | 4 | ✅ active |
| H2 Experience | 52 | ✅ classified |
| H3 Knowledge | 22 | ✅ includes ZKPC specs |
| H4 Identity | 6 | ✅ bio + humans + family |
| H5 Scars | 25 | ✅ v3.0.0, 24 scars |
| H6 Constitution | 1 | ✅ scar roots → F1-F13 |

### P-axis status

| Person | Card | ACTG | Shadows |
|---|---|---|---|
| Syed | v4 | A✅ C✅ T❌ G-inferred | 7 ZKPC attested |
| Others (16) | v1 stubs | DRAFT generated | 0 |

### VVV (Shadow Void Vault)

6 entries. 5 active loops. 1 equilibrium (THE_TRIPLE_WITNESS).
Dream engine integration: advisory telemetry only. HOLD on promotion gate.

## Dream Engine

- Timer: `arif-dream.timer` — 72h cadence (F13 2026-08-14)
- Script: `/root/AAA/dream_engine/dreams/consolidate.py`
- Last run: 2026-08-14 04:01 MYT — ΔS -0.0013 STEADY
- Next run: 2026-08-17 04:02 MYT
- Status: entropy maintenance, not learning engine (Phase 2 counterfactual unbuilt)

## Apex Scalars (live)

```
A-FORGE :7071 reads from arifOS :8088
G:      0.4716  REPLICATED
C_dark: 0.1226  REPLICATED
W3:     0.7439  REPLICATED
h:      0.7668  REPLICATED
QDF:    0.4138  REPLICATED
latency: 6ms
```

## Health Check

```bash
bash /root/AAA/scripts/federation-health.sh
# → GREEN/YELLOW/RED | organs:N | vvv:N | apex_replicated:N/5 | reasons
```

Last result: `YELLOW | organs:6 | vvv:6 | apex_replicated:5/5 | DEGRADED:GEOX,WELL,arifOS`

## Repos (GitHub sync state as of 2026-08-14 04:30 MYT)

| Repo | Remote | Branch | Sync |
|---|---|---|---|
| A-FORGE | github.com/ariffazil/A-FORGE | main | ✅ pushed |
| arifOS | github.com/ariffazil/arifOS | main | ✅ pushed |
| arif-fazil.com | github.com/ariffazil/arif-fazil.com | chore/housekeeping-2026-08-14 | ⚠️ PR needed (main protected) |

## Missing Components (backlog)

1. Memory promotion gate (observations → episodes → patterns → canon)
2. Contradiction ledger (no silent overwrite)
3. Minimum-sufficient retrieval (governed, not vector dump)
4. Non-executing reflection (Dream Engine Phase 2)
5. mgrep federation rollout (F12 audit pending)
6. arif-fazil.com/000 page (not built)

DITEMPA BUKAN DIBERI ⚒️
