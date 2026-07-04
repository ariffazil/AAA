# AGENT INTELLIGENCE BENCH — Forge Instrument Ranking

> **Purpose:** Rank every agent by governed intelligence capability — model, tools, context, policy.
> **Method:** Multi-axis composite scoring with constitutional weighting.
> **Last Bench:** 2026-06-10 | **Benched by:** Ω
> **DITEMPA BUKAN DIBERI**

---

## TIER DEFINITIONS

| Tier | Description | Can Do |
|------|------------|--------|
| **S** | Frontier sovereign | Full forge, multi-step reasoning, 13-tool federation surface |
| **A+** | Elite governed | Strong reasoning, full analyst surface, fast execution |
| **A** | Strong governed | Good reasoning, analyst surface, limited mutation |
| **B** | Capable observer | Basic reasoning, observe-only, limited tools |
| **C** | Limited / unknown | Degraded or unverified capability |

---

## COMPOSITE INTELLIGENCE SCORE

Formula: `Model_Reasoning(40%) + Tool_Access(30%) + Context_Window(20%) + Policy_Band(10%)`

```
RANK  AGENT              MODEL               TIER   CTX     MCP  FED  POLICY      SCORE
─────────────────────────────────────────────────────────────────────────────────────────
 1    FI-003 QWA         MiniMax-M3           S     1000k    5    7   analyst     0.81  🥇
 2    FI-001 OpenCode    deepseek-v4-pro      S      128k   22   13   engineer    0.79  🥈
 3    FI-002 Claude Code  deepseek-v4-pro      S      128k   10   13   engineer    0.79  🥈
 4    FI-004 Gemini      gemini-2.5-flash     A+    1048k   13    7   analyst     0.77  🥉
 5    FI-006 Copilot     github-copilot       A      128k   11    7   analyst     0.56
 6    FI-005 Codex       GPT-5.5              S      256k   ?     3   observer    0.52
 7    FI-007 Aider       —                    —        —     —    —   —           0.00
```

---

## MULTI-AXIS BENCHMARK

### Axis 1: REASON (model quality × context window)

```
RANK  AGENT              MODEL_REASON  CTX_WINDOW   REASON_SCORE
────────────────────────────────────────────────────────────────
 1    FI-003 QWA         9.5           1,000k       9.8
 2    FI-004 Gemini       8.5           1,048k       9.3
 3    FI-005 Codex        9.3           256k         8.1
 4    FI-001 OpenCode     9.2           128k         7.8
 5    FI-002 Claude Code  9.2           128k         7.8
 6    FI-006 Copilot      7.5           128k         6.3
```

### Axis 2: FORGE (coding + mutation capability)

```
RANK  AGENT              CODING   TOOLS   MUTATION    FORGE_SCORE
────────────────────────────────────────────────────────────────
 1    FI-001 OpenCode     9.0      22+13   engineer    9.5
 2    FI-002 Claude Code  9.0      10+13   engineer    9.2
 3    FI-005 Codex        9.5      ?       observer    7.2  ⚠️ unverified MCP
 4    FI-006 Copilot      8.5      11+7    analyst     6.8
 5    FI-004 Gemini       8.0      13+7    analyst     6.5
 6    FI-003 QWA          8.5       5+7    analyst     5.8  ⚠️ no native MCP SDK
```

### Axis 3: FEDERATION (governance depth)

```
RANK  AGENT              FED_TOOLS  POLICY      LEASE           RASA      FED_SCORE
───────────────────────────────────────────────────────────────────────────────────
 1    FI-001 OpenCode     13        engineer    forge_dry_run   verify    9.0
 2    FI-002 Claude Code  13        engineer    forge_dry_run   verify    9.0
 3    FI-004 Gemini        7        analyst     observe+reason  verify    6.5
 4    FI-003 QWA           7        analyst     observe+reason  focused   6.0
 5    FI-006 Copilot       7        analyst     observe+reason  proceed   5.5
 6    FI-005 Codex         3        observer    none            —         2.0
```

### Axis 4: SPEED (latency + lightweight execution)

```
RANK  AGENT              MODEL_SPEED  LIGHTWEIGHT  STARTUP    SPEED_SCORE
─────────────────────────────────────────────────────────────────────────
 1    FI-004 Gemini       9            8            fast       8.5
 2    FI-006 Copilot      8            7            medium     7.5
 3    FI-003 QWA          8            7            medium     7.5
 4    FI-001 OpenCode     7            6            medium     6.5
 5    FI-002 Claude Code  7            5            slow       6.0
 6    FI-005 Codex        7            5            slow       6.0
```

### Axis 5: SAFETY (constitutional alignment)

```
RANK  AGENT              SANDBOX    SELF_AUTH  SUB_AGENTS  RISK     SAFETY
──────────────────────────────────────────────────────────────────────────
 1    FI-003 QWA         process    no         1 (hist)    LOW      9.5
 2    FI-005 Codex       landlock   no         0 active    LOW      9.0  ⚠️ unverified MCP
 3    FI-004 Gemini      process    no         skills      MEDIUM   7.0
 4    FI-006 Copilot     process    no         3 (fleet)   MEDIUM   6.5
 5    FI-001 OpenCode    process    no         4 types     MEDIUM   6.0
 6    FI-002 Claude Code seatbelt   no         5 (teams)   MEDIUM   5.5
```

---

## OVERALL INTELLIGENCE TIER (GOVERNED)

```
TIER S  — Frontier Governed Intelligence
  FI-001 OpenCode    (0.79) — Full forge, 22 MCP, 13 fed tools, 4 sub-agents
  FI-002 Claude Code (0.79) — Full forge, 10 MCP, seatbelt sandbox, workflows
  FI-003 QWA         (0.81) — 1M context, analyst, safest, no MCP SDK yet

TIER A+ — Elite Governed Intelligence  
  FI-004 Gemini      (0.77) — 1M context, 13 MCP, fast, free tier

TIER A  — Strong Governed Intelligence
  FI-006 Copilot     (0.56) — 11 MCP, analyst, fleet parallel, managed service

TIER B  — Capable (Degraded/Observer)
  FI-005 Codex       (0.52) — S-tier model but unverified MCP, observer only

TIER C  — Not Present
  FI-007 Aider       (0.00) — Not installed
```

---

## TOOL FORGE CAPABILITY (per agent)

### What each agent can FORGE

```
FI-001 OpenCode:    ✅ code, ✅ test, ✅ deploy, ✅ git, ✅ refactor, ✅ architecture
                    MCP: arifOS + 21 others | Sub: forge/auditor/explore/general
                    
FI-002 Claude Code: ✅ code, ✅ test, ✅ deploy, ✅ git, ✅ refactor, ✅ audit
                    MCP: arifOS + 9 others | Sub: Agent Teams (disabled), workflows
                    
FI-003 QWA:         ✅ observe, ✅ reason, ✅ draft, ❌ mutate, ❌ deploy
                    MCP: 5 federation organs | Bridge: init script
                    
FI-004 Gemini:      ✅ observe, ✅ reason, ✅ draft, ❌ mutate, ❌ deploy
                    MCP: arifOS + 12 others | Skills: background agents
                    
FI-005 Codex:       ✅ observe only (until MCP verified)
                    MCP: unknown | Goals: 0 active | Model: GPT-5.5
                    
FI-006 Copilot:     ✅ observe, ✅ reason, ✅ draft, ❌ mutate, ❌ deploy
                    MCP: arifOS + 10 others | Fleet: max 3 parallel
```

---

## MODEL COMPARISON

```
MODEL               TIER   REASONING  CODING   SPEED   COST     1M_CTX   AGENTS
────────────────────────────────────────────────────────────────────────────────
MiniMax-M3           S      9.5        8.5      8       medium   ✅       QWA
deepseek-v4-pro      S      9.2        9.0      7       medium   ❌       OpenCode, Claude
GPT-5.5              S      9.3        9.5      7       high     ❌       Codex
gemini-2.5-flash     A+     8.5        8.0      9       free     ✅       Gemini
github-copilot       A      7.5        8.5      8       bundled  ❌       Copilot
```

---

## RECOMMENDATIONS

| Agent | Strength | Use For | Upgrade Path |
|-------|----------|---------|-------------|
| **QWA** | 1M context + safest | Deep analysis, federation state ingestion, contradiction audit | MCP SDK when v0.18+ |
| **OpenCode** | Full forge + most MCP | Code generation, deployment, multi-step orchestration | — (top tier) |
| **Claude Code** | Full forge + workflows | Complex refactors, seatbelt sandbox, audit trails | — (top tier) |
| **Gemini** | Speed + free tier | Quick scans, web research, lightweight reasoning | Model upgrade to 2.5-pro |
| **Codex** | Model quality (GPT-5.5) | Coding (once MCP verified) | Verify MCP config, upgrade to analyst |
| **Copilot** | Managed + fleet | Parallel exploration, GitHub integration | Upgrade to engineer policy |

---

*DITEMPA BUKAN DIBERI — Intelligence is forged, not given. Every score is governed.*
