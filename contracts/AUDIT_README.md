# Cross-Organ README Audit — arifOS · AAA · A-FORGE

> **Audit date:** 2026-06-30 | **SOT:** Live system + Canonical Organ Map
> **Verdict:** YELLOW — All three READMEs have drift. arifOS worst (internal contradictions). AAA cleanest (self-auditing SOT). A-FORGE stale (version, MIND/MEMORY model).
> **Action:** Fix all three READMEs to contrast each other. One truth across three repos.

---

## 0. SOT REFERENCE — What Wins

| Priority | Source | Authority |
|----------|--------|-----------|
| **1** | Live runtime (health endpoints, tools/list, systemd) | IRREFUTABLE |
| **2** | `/root/AAA/docs/ORGAN.md` | CANONICAL — F13 sealed |
| **3** | `/root/AAA/CLAUDE.md` | MASTER agent instruction |
| **4** | `/root/arifOS/CLAUDE.md` | arifOS internal SOT |
| **5** | `package.json` / `pyproject.toml` | Source truth for versions |

---

## 1. TOOL COUNT — THE BIGGEST LIE

### What arifOS README Says
```
"Public surface frozen to exactly 7 verbs" (header, badge, §1, §8)
"Tools: 13" (footer)
"canonical_tools: 15, total_public_surface: 16" (§18)
"All prior 13/15/16 tool references below are historical" (2026-06-23 update)
```

### What Live Runtime Shows
```
9 exposed via MCP tools/list
17 canonical tools loaded
41 diagnostic tools
58 total declared tools
```

### Verdict
**The README contradicts itself four ways.** "7 verbs" is wrong (9 exposed). "13 tools" is wrong (17 canonical). "15/16" is wrong (17/58). The 2026-06-23 update says prior counts are "historical" but new counts are ALSO wrong. The ARIFOS README CANNOT TELL THE TRUTH ABOUT HOW MANY TOOLS IT HAS.

**Fix:** Replace ALL tool count claims with a single sourced line:
> "9 tools exposed via MCP (17 canonical, 58 total declared). Live count: `curl :8088/health | jq .tools_exposed_via_mcp`"

---

## 2. TOOL NAMES — DUAL NAMING SCHEME

### arifOS README Public Verb Names (header + §8)
```
arif_init, arif_observe, arif_think, arif_route, arif_judge, arif_act, arif_seal
```

### arifOS README Pipeline Names (§5)
```
arif_session_init, arif_sense_observe, arif_evidence_fetch, arif_mind_reason,
arif_kernel_route, arif_memory_recall, arif_heart_critique, arif_gateway_connect,
arif_reply_compose, arif_ops_measure, arif_judge_deliberate, arif_forge_execute,
arif_vault_seal
```

### Live MCP tools/list
```
arif_init, arif_observe, arif_think, arif_route, arif_judge, arif_act, arif_seal,
arif_resolve_tool, arif_vault_query
```

### Verdict
**Two naming schemes coexist in the same README.** The "public verb" names (short: `arif_init`) match the live surface. The "pipeline" names (long: `arif_session_init`) are INTERNAL tool file names, not what agents see. The README mixes them without explanation.

**Fix:** Use ONLY the live MCP names in README. Mention internal tool file names separately as implementation detail.

---

## 3. MIND/MEMORY — WRONG IN BOTH arifOS AND A-FORGE

### What arifOS README Says
```
MIND on :51001 (A-FORGE hosted) — Sequential reasoning / deliberation
MEMORY on :51002 (A-FORGE hosted) — Cognitive memory bridge
```
In §2 diagram, §1, §16.

### What A-FORGE README Says
```
"It also hosts the MIND:51001 and MEMORY:51002 federated intelligence services"
Role: "Execution Shell · Forge · MIND/MEMORY host"
```

### What Canonical Organ Map Says (SOT)
```
Hermes :8644  = MIND organ — ASI cognitive relay, Telegram interface, memory orchestration
OpenClaw :18789 = HANDS organ — AGI transport router, envelope broker, tool gateway
```
No :51001 or :51002 appears anywhere in the organ map.

### What AAA README Says (matches organ map)
```
hermes-asi (Telegram @ASI_arifos_bot) · openclaw (port 18789)
MIND:51001 and MEMORY:51002 are NOT listed as organs.
```

### Verdict
**Both arifOS and A-FORGE READMEs propagate a DEPRECATED architecture model.** MIND moved from A-FORGE-hosted :51001 to Hermes :8644. MEMORY moved from A-FORGE-hosted :51002 to VAULT999 + tiered memory. AAA README has the correct model (matches organ map).

**Fix:** Purge :51001/:51002 from arifOS and A-FORGE READMEs. Replace with organ map model: Hermes :8644 (MIND), OpenClaw :18789 (HANDS).

---

## 4. APEX — GHOST ORGAN

### What arifOS README Shows
```
APEX :3002 in §2 architecture diagram (labeled "Health probe")
APEX listed as organ in §1 ("APEX legacy")
```

### What A-FORGE README Shows
```
APEX listed in Federation Cross-Reference: "888 JUDGE (legacy health probe)"
```

### What AAA README Shows
```
APEX: "Legacy health probe — deliberation moved to AAA a2a-server/"
"Original APEX repo is archived"
```

### What CLAUDE.md Says
```
APEX 3002: "888 JUDGE deliberation (legacy, absorbed into AAA a2a)"
apex-prime.service: STOPPED/DISABLED
```

### What Canonical Organ Map Shows
```
APEX NOT LISTED as an organ. It is absorbed.
```

### Verdict
**APEX is dead but both arifOS and A-FORGE READMEs still list it.** AAA README correctly states it's archived. The organ map doesn't list it at all.

**Fix:** Remove APEX from arifOS and A-FORGE diagrams. Note it as "absorbed into AAA a2a (2026-06-02)" in historical section only.

---

## 5. EXECUTION CHAIN — THREE DIFFERENT FLOWS

### arifOS README Diagram
```
Arif → arifOS (judge) → Domain Organs (advise) → AAA (cockpit) → A-FORGE (execute) → VAULT999
```
AAA positioned BETWEEN domain organs and A-FORGE.

### A-FORGE README Diagram
```
Arif → arifOS (judge) → AAA (route) → A-FORGE (execute) → GEOX/WEALTH/WELL
```
AAA positioned as "route" layer BETWEEN arifOS and A-FORGE. Domain organs AFTER A-FORGE.

### Canonical Organ Map
```
Arif → AAA/Hermes/OpenClaw (IDENTITY) → arifOS (GOVERNANCE) → GEOX/WEALTH/WELL (DOMAIN) → A-FORGE (EXECUTE) → VAULT999 (MEMORY)
```
AAA is IDENTITY, NOT a routing layer in execution. Domain organs advise BEFORE execution.

### Verdict
**Three READMEs, three different execution flows.** A-FORGE's diagram is worst — it puts AAA as "route" (wrong role) and puts domain organs AFTER execution (wrong order — evidence comes BEFORE execution, not after).

**Fix:** All three READMEs MUST show the same chain:
```
Arif (F13) → arifOS (judge/govern) → Domain Organs (evidence/compute) → A-FORGE (execute) → VAULT999 (seal)
AAA displays all of it — cockpit, not a stage in the chain.
```

---

## 6. PORT DISCREPANCIES

| Organ | arifOS README | A-FORGE README | AAA README | Organ Map (SOT) | Live |
|-------|:---:|:---:|:---:|:---:|:---:|
| arifOS | 8088 | 8088 | 8088 | 8088 | ✅ 8088 |
| A-FORGE | 7071 | 7071 | 7071 | **7071/7072** | ✅ 7071 |
| AAA | 3001 | 3001 | 3001 | 3001 | ✅ 3001 |
| GEOX | 8081 | 8081 | 8081 | 8081 | ✅ 8081 |
| WEALTH | 18082 | 18082 | 18082 | 18082 | ✅ 18082 |
| WELL | 18083 | 18083 | 18083 | 18083 | ✅ 18083 |
| APEX | **3002** | **3002** | 3002 | — | ❌ stopped |
| MIND | **51001** | **51001** | — | **8644 (Hermes)** | — |
| MEMORY | **51002** | **51002** | — | — | — |

**Fix:** A-FORGE port should show 7071/7072 per organ map. MIND/MEMORY ports removed entirely (Hermes :8644 instead). APEX removed.

---

## 7. VERSION DRIFT

| Repo | README Claims | package.json / pyproject | Live Health |
|------|:---:|:---:|:---:|
| arifOS | "v2026.05.05-SSCT" (health only) | — | `release_name: v2026.05.05-SSCT` |
| A-FORGE | "2026.06.06" (health example) | **2026.06.14** | `version: 0.1.0` |
| AAA | "2026.06.23" (package ver) | **2026.06.23** | `version: 1.0.0` |

**A-FORGE version is a mess:** README shows 2026.06.06, package.json says 2026.06.14, live health says 0.1.0. THREE different versions.

**Fix:** All READMEs should show the package.json version. A-FORGE needs a single version source.

---

## 8. ORGAN COUNT — EVERYONE DISAGREES

| Source | Count | What's Counted |
|--------|:-----:|----------------|
| arifOS README badge | "7 organs + 2 services" | GEOX, WEALTH, WELL, AAA, A-FORGE, APEX, arifOS + MIND, MEMORY |
| A-FORGE README | "7 sovereign organs" | Same list |
| AAA README | "6 domain organs" | arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA |
| Canonical Organ Map | 7 organs | arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA, VAULT999 |
| CLAUDE.md | 7 organs | Same as organ map |

**Fix:** All three READMEs must say "7 organs" with the canonical list: arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA, VAULT999. Hermes and OpenClaw are EDGE AGENTS, not organs.

---

## 9. A-FORGE TEST COUNT — SELF-CONTRADICTION

```
README badge:     "26 suites"
README body (§2):  "26 suites, ~4,700 lines"
README body (§15): "25 test suites, not all pass CI"
```

**Verdict:** Self-contradictory within the same README.

---

## 10. AAA SPECIFIC ISSUES

### 10.1 Agent Count
- "14+ agents" claimed in state thesis
- 22 agent identity directories on disk
- 11 forge instruments claimed vs 9 listed in one section
- Ambiguous: agents vs directories vs runtime cards

### 10.2 HEXAGON
- Correctly reflects 5 constitutional agents + 777-FORGE witness
- BUT does not match organ map which has different agent model
- Hermes/OpenClaw are organs in organ map but agents in AAA

### 10.3 Date Staleness
- "Verified against disk on 2026-06-22" appears multiple times
- Current date: 2026-06-30 — 8 days stale

### 10.4 Package Version Match
- README claims "2026.06.23" — matches package.json ✅

### 10.5 Truth Stack
- The 4-layer truth stack (GROUND_TRUTH → VERIFIED → CACHED → INFERRED) is internally consistent and valuable. No SOT conflict.

---

## 11. A-FORGE SPECIFIC ISSUES

### 11.1 MCP Surface Count
- "5 MCP surfaces" claimed — what are they? arifOS, GEOX, WEALTH, WELL = 4. AAA doesn't expose MCP. That's 4, not 5.

### 11.2 "62+ tools"
- Badge says "62+ tools discovered"
- No live verification possible (tools/list on A-FORGE MCP failed earlier)
- Likely stale — GEOX collapsed from 33→16 tools

### 11.3 Layer 2 (Model Capability Gate)
- References "model_governance_card from arifOS kernel"
- Does this actually exist in arifOS? Needs verification.

---

## 12. THE CONTRAST — WHAT EACH README MUST SAY

### arifOS MUST say:
```
I am the CONSTITUTIONAL KERNEL — the law layer.
I judge (F1-F13). I seal (VAULT999). I govern sessions and identity.
I do NOT execute code, compute domain logic, or display UX.
9 tools exposed via MCP. 17 canonical. 58 total.
Port 8088. Systemd: arifos.service.
A-FORGE executes for me. AAA displays for me. GEOX/WEALTH/WELL advise me.
```

### AAA MUST say:
```
I am the COCKPIT — the display layer.
I show state. I route tasks. I manage agent identity.
I do NOT judge, execute, seal, or compute domain evidence.
Port 3001. Systemd: aaa-a2a.service.
arifOS is the judge. A-FORGE is the executor. I am the window.
```

### A-FORGE MUST say:
```
I am the EXECUTION SHELL — the hands.
I build, deploy, and forge — ONLY after arifOS SEAL.
I do NOT judge, self-authorize, compute domain logic, or display UX.
Port 7071/7072. Systemd: a-forge.service.
arifOS judges. AAA displays. I execute. NEVER the other way around.
```

---

## 13. FIX PRIORITY

| Priority | Fix | Repos Affected |
|:---:|---|:---:|
| **P0** | Remove :51001/:51002 (MIND/MEMORY) from arifOS + A-FORGE | arifOS, A-FORGE |
| **P0** | Fix tool counts in arifOS README (7→9) | arifOS |
| **P0** | Remove APEX :3002 from organ listings | arifOS, A-FORGE |
| **P1** | Unify execution chain diagram across all three | arifOS, A-FORGE, AAA |
| **P1** | Fix A-FORGE version to match package.json (2026.06.14) | A-FORGE |
| **P1** | Fix A-FORGE port to 7071/7072 | A-FORGE |
| **P1** | Add contrasting "What X is NOT" to each README | arifOS, A-FORGE, AAA |
| **P2** | Update "verified against disk" date in AAA | AAA |
| **P2** | Fix A-FORGE test count (25 vs 26) | A-FORGE |
| **P2** | Unify organ count to 7 (canonical list) | arifOS, A-FORGE |
| **P2** | Fix public verb names vs pipeline names confusion | arifOS |

---

## 14. BOTTOM LINE

**arifOS README lies about its own tool count.** It says 7, live shows 9. It says 13, live shows 17. It says 15, live shows 58. It's the constitution — it cannot lie.

**A-FORGE README has three different versions** (README, package.json, live health) and propagates a deprecated MIND/MEMORY architecture.

**AAA README is the cleanest** — self-auditing with SOT alignment table ($0.4), correct agent model, correct organ relationships. Its main defect is 8-day staleness.

**The execution chain must be unified.** Three READMEs cannot show three different authority flows. The organ map is canonical — all READMEs derive from it.

---

*Audit sealed 2026-06-30. DITEMPA BUKAN DIBERI.*
