# AAA Federation State — Live Map

> Forged 2026-08-14. One source of truth. Probe before trust.
> **Live re-verified 2026-10-18T12:04Z** — CLI versions and organ statuses below are probe output from that run, not carried-over memory. Per-harness model routing lives in each harness config; not duplicated here.

## CLI Coders (verified installed)

| CLI | Version | Path | Status (2026-10-18) |
|---|---|---|---|
| OpenCode | 2.0.32 | /root/.opencode/bin/opencode | ✅ alive (FED forge-777; running TUI 2.0.28 until relaunch) |
| Kimi Code | 2.2.0 | /root/.kimi-code/bin/kimi | ✅ alive |
| Qwen Code | 0.25.2 | /root/.local/bin/qwen | ✅ alive |
| Codex | 0.163.0 | /root/.npm-global/bin/codex | ✅ alive |
| Claude Code | 2.1.300 | /root/.local/bin/claude | ✅ alive |
| Gemini CLI | 0.59.0 | /root/.npm-global/bin/gemini | ✅ alive |
| Agy (Antigravity) | 1.4.2 | /root/.local/bin/agy | ✅ alive |
| Aider | — | not found on PATH | ❌ absent (dropped from table, do not claim) |

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

| Organ | Port | Status (live 2026-10-18) | Function |
|---|---|---|---|
| arifOS | 8088 | ⚠️ degraded — G=0.5498, QDF=0.4263 below band | Constitutional kernel, F1-F13 |
| A-FORGE | 7071/7072 | ✅ healthy | Execution/mutation gate |
| arifFlow | 7073 | ✅ ok-v3-vector | Metabolism, receipts |
| WEALTH | 18082 | ✅ healthy | Capital domain |
| WELL | 18083 | ⚠️ degraded (reachable; no fresh biometric source) | Human wellness |
| GEOX | 8081 | ⚠️ degraded — kernel_verdict HOLD | Geoscience |
| AAA | 3001 | ✅ healthy (G=0.5498, C_dark=0.2246, QDF=0.4263, ceiling DISPLAY_ONLY) | A2A gateway |
| FED | 4000 (HAProxy→litellm 4013) | ✅ 401 without auth = live | Model router |
| FRAME / CHRON / SIGNAL | 18085 / 18102 / 18084 | ✅ live | Witness / temporal / signal organs |
| OpenClaw | 18789 | ❌ COLD | AGI gateway (edge mesh, cold-stored 2026-09-07) |
| FLAME / graphiti-mcp / qwen server | 18901 / 18412 / 4357 | ❌ DOWN | Retired or cold |

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
Source: arifOS :8088/health + AAA :3001/health, measured 2026-10-18T12:04:05Z
G:      0.5498  MEASURED  (below healthy band → arifOS /health = degraded)
C_dark: 0.2246  MEASURED
W3:     0.8736  MEASURED  (independence UNMEASURED — rank needs witness sample vectors)
h:      0.8084  MEASURED
QDF:    0.4263  MEASURED  (below healthy band)
authority: DISPLAY_ONLY
```

## Health Check

```bash
bash /root/AAA/scripts/federation-health.sh
# → GREEN/YELLOW/RED | organs:N | vvv:N | apex_replicated:N/5 | reasons
```

Last result (2026-10-18T12:04Z): `STATE_DEGRADED — fail=1 warn=1` · organs 8/8 alive · FED liveliness ✅ · AAA status=healthy drift=False vault=CONNECTED ceiling=DISPLAY_ONLY · **fail: G=0.5498, QDF=0.4263 below band** · warn: openclaw/opencode units inactive (openclaw cold; `opencode.service` is a legacy bot unit — live 333-AGI runs as CLI processes + `opencode serve --service`, not that unit)

## Repos (GitHub sync state as of 2026-08-14 19:10 MYT)

| Repo | Remote | Branch | Sync |
|---|---|---|---|
| A-FORGE | github.com/ariffazil/A-FORGE | main | ✅ pushed |
| arifOS | github.com/ariffazil/arifOS | main | ✅ pushed (6bfcc4858 FI-003 Ω calibration) |
| arif-fazil.com (arif-sites) | github.com/ariffazil/arif-fazil.com | feat/trilogy-languages-of-trust-20260814 | ✅ pushed (makcikgpt prev/next nav + nav zen) — PR needed (main protected) |
| web-canon | github.com/ariffazil/web-canon | fix/nav-align-live-reorg-20260814 | ✅ pushed — PR #7 open (nav primary_links /words /work) |

## Missing Components (backlog)

1. Memory promotion gate (observations → episodes → patterns → canon)
2. Contradiction ledger (no silent overwrite)
3. Minimum-sufficient retrieval (governed, not vector dump)
4. Non-executing reflection (Dream Engine Phase 2)
5. mgrep federation rollout (F12 audit pending)
6. ~~arif-fazil.com/000 page (not built)~~ — RESOLVED 2026-08-14: /000 live, nav zen'd to canon 5-link invariant
7. Nav invariant enforcer: arif-sites scripts/zen-nav.cjs (canon v7 primary_links → all static surfaces; see FORGE-agentic-web-builder OP 7)

DITEMPA BUKAN DIBERI ⚒️

## Phone Body State (2026-10-19)

> Canonical: `/root/AAA/federation/PHONE_BODY_STATE-2026-10-19.md`
> Honor 600 Pro `100.64.0.6` = ACTIVE body; S24 `100.64.0.1` = STANDBY; both bridge `:8765` health 200.
> SSH `vps`=KVM8, `kvm`=KVM4, `kvm2`=KVM2 via `ProxyJump vps` (no KVM2 password). Phone one-word `arif` menu 0–7.
