# Recursive Skill Portfolio Audit — Cross-Surface (v2.0)

> **Auditor:** kimi-code / FI-008 (warga-aaa) · **Lane:** OBSERVE (no skill mutations this pass)
> **Date:** 2026-09-09T13:51Z → 14:0xZ UTC · **Skill:** `skill-mesh/AUDIT-recursive-audit` v2.0
> **Authority:** 333-AGI autonomous OBSERVE; report-only. VOID/PROMOTE executions **held** (see §9).
> **Epistemic base:** OBS = probed on disk this run · DER = derived from probes · INT = judgment.

---

## 1. Executive Summary

| Metric | Value | Verdict |
|---|---|---|
| Surfaces probed | 10 (9 resolved, 1 MISSING) | doctrine-table drift found |
| AAA canonical skills | **212** (not 339 — see §2.1) | healthy |
| Alias symlinks inside AAA | 115 (capabilities 32, domains 28, primitives 19, workflows 14, +22) | intentional alias table — OK |
| Kimi user-scope skills | 93; effective view = 93 + 212 via `extra_skill_dirs` | complementary, not a copy |
| Skills >30d stale | AAA: **0** · kimi: 16 | AAA wholesale-fresh |
| Skills >90d stale | **0** anywhere | no age-based unused-rot |
| Files >500 lines | AAA: 5 · kimi: 2 (max: `seven-zen-organs-enforcement` 1039) | bloat flag |
| Archive-void-rot | **0** (AAA `.archive` and kimi `.archive*` hold 0 live SKILL.md) | hygiene PASS |
| Broken `/root/` refs | **77 of 276** unique (≈20 attributed, §7) | doc-rot cluster |
| Dual-name collisions (verified) | **11 clusters**, kimi loads BOTH sides of each | ⚠️ headline finding |
| Invocation telemetry | SkillGate Phase 1: **2 events total** | unused-rot = UNKNOWN (data-blind) |
| VOID candidates surfaced | 3 (§9) — **not executed** | HOLD, rationale in §9.4 |

**Headline:** the portfolio's worst rot is not staleness (AAA is fully fresh) but **structural duplication between kimi user-scope and AAA canonical**: because kimi loads both surfaces, every dual-name pair is a *live* trigger collision in this harness today. Second headline: one skill (`cognitive-level-assertion-protocol`) declares itself superseded by `governance/akal-cognitive-invariants`, **which does not exist** — VOIDing it would destroy the only AKAL skill copy in the federation.

---

## 2. Surface Topology (probed vs doctrine table)

| # | Surface | Doctrine says | Reality (OBS) | Skills | Drift vs AAA |
|---|---|---|---|---|---|
| 1 | `/root/AAA/skills` | SOT | DIR | 212 (+115 internal aliases) | — |
| 2 | `/root/.kimi-code/skills` | copy | **complementary user-scope** + `extra_skill_dirs=[/root/AAA/skills]` | 93 | 10 shared paths only; 81 kimi-only names |
| 3 | `/root/.arifos/agents/opencode/skills` | symlink | **DIR (copy)** | 238 | **47 names not in AAA** |
| 4 | `/root/.grok/skills` | symlink | symlink → AAA ✓ | 212 | 0 (by construction) |
| 5 | `/root/.claude/skills` | symlink | symlink → AAA ✓ | 212 | 0 |
| 6 | `/root/.codex/skills` | symlink | symlink → AAA ✓ | 212 | 0 |
| 7 | `/root/.hermes/skills` | copy | DIR | 384 files / 372 names | **235 names not in AAA** |
| 8 | `/usr/local/lib/hermes-agent/skills` | copy | DIR | 363 files / 282 names | **146 names not in AAA** |
| 9 | `/root/.openclaw/workspace/skills` | copy | **MISSING** — entire `/root/.openclaw` gone (edge moved to KVM4) | 0 | surface retired on this VPS |
| 10 | openclaw-bundled | built-in | N/A on this host | — | — |
| + | `/root/.agents/skills` (project scope) | — | symlink → AAA ✓ | 212 | 0 |

**Doctrine-table drift (doc-rot in the auditing skill itself):** rows 2, 3, 9 above no longer match reality. Recommend updating the surface table in `skill-mesh/AUDIT-recursive-audit/SKILL.md` at next revision.

### 2.1 Count caveat (DER)
`find -L /root/AAA/skills` reports 339 because it traverses the 115 internal alias symlinks (e.g. `capabilities/media/AAA-tts-engine-catalog → ../../AAA-tts-engine-catalog`). Canonical inventory = **212**. Any tooling that counts with `-L` (or after `-follow`) double-counts; topology probes must use plain `find`.

---

## 3. Staleness Analysis

- **AAA:** 0 files >30d. Oldest = 30d (`FORGE-onboarding/claude`, `knowledge/know-*`, `substrate/kernel-bind`, `warga/constitutional`…) — consistent with the 2026-09-04/09 render + RSI passes. No cross-check debts triggered.
- **Kimi user-scope >30d (16):** `kimi-skill-reflector` (53d, oldest), `kimi-primer`, `kimi-router`, `kimi-contrast`, `autonomous-governed-execution`, 6× `.system/*` (harness bundled 2026-08-06), `AGI-claude-xml-*`, `AGI-codex-chain-*`, `AGI-hermes-system-prompt-voice`, `COPILOT_AUTONOMOUS_PIPELINE`, `FORGE-grok-profile`. All are harness-native/meta except the two audit candidates flagged in §9.
- **>90d:** none on any surface → **zero age-based unused-rot**.
- **unused-rot by telemetry:** UNKNOWN — SkillGate holds 2 events total (both 2026-09-09, kimi-code/FI-008, keyword method, no outcomes). Honest UNKNOWN > fabricated classification (F2).

---

## 4. Prompt Bloat (>500 lines)

| File | Lines | Note |
|---|---|---|
| kimi `seven-zen-organs-enforcement` | **1039** | worst in federation; split/compress |
| AAA `arifos-kernel-zen-audit` | 793 | |
| AAA `ASI-summarize` | 693 | |
| AAA `RSI-federation-mesh` | 560 | also carries 3 broken refs (§7) |
| AAA `hermes-gateway-image-routing` | 545 | |
| kimi `skill-mesh/AUDIT-skill-atlas` | 568 | |
| AAA `external-artifact-verdict` | 529 | |

Borderline (450–500): `AAA-somatic-emd-pipeline` 490, `forge-vss-verifier-suite` 467, `APEX-quantum-eureka` 459.

---

## 5. Collision Audit — verified dual-name clusters (OBS: frontmatter diffed)

Kimi loads AAA via `extra_skill_dirs`, so **both rows of each pair are simultaneously triggerable** in this harness.

| # | Kimi user-scope | AAA canonical | Evidence | Verdict |
|---|---|---|---|---|
| 1 | `FORGE-telemetry-watchdog` | `engineering/telemetry-watchdog` | **identical `id: forge-telemetry-watchdog` on both sides** | ☠️ hard collision — archive kimi copy |
| 2 | `ASI-drift-watch` (v1.1.0) | `engineering/drift-watch` (v2.0.0) | AAA is superset (+baseline compare) | archive kimi copy |
| 3 | `FORGE-cicd-docker-deploy` | `engineering/cicd-deploy` | descriptions verbatim-identical | archive kimi copy |
| 4 | `FORGE-vps-docker` + `FORGE-vps-runbook` | `engineering/vps-ops` (v2.0.0) | vps-ops description merges both runbooks | archive kimi pair |
| 5 | `check-work` + `FORGE-verify-runtime` | `engineering/verify-work` (v2.0.0) | **triple** collision on verification-as-terminal-state. ⚠️ `check-work` is slash-wired (`/check-work`, `/check`, `/verify`) | keep `check-work` as harness binding; archive `FORGE-verify-runtime` |
| 6 | `forge-mcp` bundle (consolidated 2026-09-08) | `engineering/mcp-ops` (v2.0.0 "Merges: FORGE-mcp-ops, -federation-ops, -lifeguard") | **both claim to be the consolidation**; kimi bundle is newer & wider (probe/testing/smoke) | owner decision: single SOT |
| 7 | `FORGE-skill-creator` | `engineering/skill-creator` + `.system/skill-creator` | three-way | merge → AAA |
| 8 | `code-review` | `engineering/code-review` | same purpose | merge → AAA |
| 9 | `FORGE-pr-governance` + `FORGE-pr-review` + `FORGE-precommit-review` | `engineering/pr-governance` (+`engineering/code-review`) | policy/checklist split across surfaces | consolidate |
| 10 | `skill-mesh/*` bundle (7 subskills) | `engineering/skill-inventory` + `engineering/skill-drift` | overlapping audit/mesh scope | consolidate decision |
| 11 | `cognitive-level-assertion-protocol` (frontmatter name: `akal-cognitive-invariants` v2.0.0) | `governance/akal-cognitive-invariants` — **does not exist** (governance/ holds only apex-gate-evaluator, apex-verdict) | self-declared "SUPERSEDED by" a missing target | **PROMOTE, do not VOID** (§8) |

Additional soft overlaps (INT, no action unilaterally): `PETRONAS-intelligence-router` (kimi) vs `MY-REALITY-STACK` (AAA, F13 directive 2026-08-15) — both route Malaysia/PETRONAS claims; recommend explicit scope split (PETRONAS-corporate vs MY-macro). `create-skill` (kimi) vs skill-creator family. `firecrawl-web-search` (kimi) vs `hermes/web-search` (AAA router incl. Firecrawl) — acceptable layering, note only.

**Circular-reference check:** no load-cycle detected — cross-skill references are textual (host-mediated loading), no skill instructs auto-loading another in a loop. Infinite-loop failure mode: not triggered.

---

## 6. Rot Matrix (summary)

| Rot class | Count | Items |
|---|---|---|
| `archive-void-rot` | **0** | archives clean on both AAA and kimi |
| `doc-rot` | ~15 | §7 broken refs + doctrine-table drift (§2) + stale supersedence (cluster 11) |
| `api-rot` | 0 found | sample URL probe clean (§7.2); no SDK-version drift probed deep — cataloged only |
| `trigger-rot` | 11 clusters | §5 (dual exposure in kimi harness) |
| `unused-rot` | UNKNOWN | telemetry blind (2 events); age says none |
| `drift-rot` | 3 majors | opencode copy (47 names), hermes (235), hermes-asi (146) not in AAA; `AGI-audio-quantum-cognition` inverse-drift (§8) |
| `dual-name-rot` | 11 clusters | §5 |
| bloat | 7 files | §4 |

---

## 7. Broken References (77 of 276 unique `/root/` paths missing)

### 7.1 Attributed (doc-rot in AAA SOT — propagates to 4 symlink surfaces + kimi view)

| Source skill (AAA) | Broken reference | Fix |
|---|---|---|
| `RSI-federation-mesh` | `/root/AAA/skills/FORGE-skill-creator/SKILL.md` (kimi-only now) | re-point → `engineering/skill-creator` |
| `RSI-federation-mesh` | `…/RSI-federation-mesh/mesh-seal.py` (**own script missing**) | restore script or strip ref |
| `RSI-federation-mesh` | `…/RSI-recursive-improvement/SKILL.md` | re-point or drop |
| `AGI-dream-engine` | `…/agentic-dream-engine/prototype/` | drop or restore |
| `forge-vss-verifier-suite` | `/root/.kimi-code/skills/FORGE-visual-qa-w3/` (now AAA) | re-point → `/root/AAA/skills/FORGE-visual-qa-w3` |
| `media/aaa-image-editing` | self-ref to old path `AAA/skills/aaa-image-editing` | fix self path |
| `AAA-voice-cloning-qwen-cloud` | `forge-caddy-cloudflare` (renamed) | → `FORGE-infra-guardian` |
| 8 skills (`AAA-tts-engine-catalog`, `arifos-external-council`, `FORGE-document-intelligence`, `forge-multimodal-router`, `AAA-shadow-mode`, `AGI-graph-engineering-patterns`, `AGI-dream-engine`, `xauusd-trading`) | old `/root/.agents/skills/*` pre-symlink paths (e.g. `XAUUSD-trading-stack`) | re-point to AAA names |
| 4 skills (`AAA-audio-qualia-doctrine`, `forge-multimodal-router`, `cognitive-commands`, `engineering/skill-inventory`) | `/root/.hermes/skills/...` paths that don't resolve on this host's hermes copy | re-point or make host-relative |
| 4 AAA audio skills (`AAA-tts-engine-catalog`, `AAA-voice-cloning-qwen-cloud`, `AAA-audio-qualia-doctrine`, `forge-multimodal-router`) | `/root/AAA/skills/AGI-audio-quantum-cognition/SKILL.md` — **skill only exists on kimi/hermes** | PROMOTE (§8) |

### 7.2 URL probe (sample, DER)
188 unique URLs cataloged; 12 most-referenced probed: qwencloud ×6 → 200; `127.0.0.1:8088/mcp` → 200 (kernel alive); mcpjam → 405 (method-gated, alive); runpod/openrouter API roots → 404 (normal for GET on POST endpoints). **No dead domains in sample.** Remaining 176 unverified — cataloged, not probed (scope-bound).

### 7.3 Intentional negatives (NOT rot)
`.env`, `.cloudflared/tunnel-token`, `.openclaw/tg_token`, `.backups/` appear in security-skill examples ("never commit…"). Correct to be non-existent. `/root/.openclaw/*` refs reflect the retired surface (§2).

---

## 8. Classification Matrix Verdicts

| Verdict | Items |
|---|---|
| ✅ **PROMOTE** | `AGI-audio-quantum-cognition` (kimi→AAA; 4 inbound AAA refs, hermes also has it) · `cognitive-level-assertion-protocol` → **`AAA governance/akal-cognitive-invariants`** (it already self-identifies as that, v2.0.0; only AKAL skill in federation — `AAA/docs/canon/AKAL-DICTIONARY.md` is a doc, not a skill) |
| 📦 **ARCHIVE** (kimi → `_retired/`, after alias check) | `FORGE-telemetry-watchdog`, `ASI-drift-watch`, `FORGE-cicd-docker-deploy`, `FORGE-vps-docker`, `FORGE-vps-runbook`, `FORGE-verify-runtime`, `FORGE-pr-governance`*, `FORGE-pr-review`*, `FORGE-precommit-review`*, `code-review`*, `FORGE-skill-creator`* (*pending merge confirmation, cluster 6–9) |
| 🔧 **HARNESS-NATIVE** (OK, no action) | `AGI-claude-xml-*`, `AGI-codex-*`, `AGI-hermes-*`, `FORGE-grok-profile`, `kimi-*`, `apex-gates/*` (+claude/hermes subdirs), `hermes/*`, `openclaw-*`, `opencode/*`, `.system/*` |
| 🔲 **NEED MIRROR** | **none required for kimi** (AAA reachable via `extra_skill_dirs`); grok/claude/codex/.agents are symlinks → zero drift. opencode copy is 47-names drifted → **re-sync decision needed** (mirror vs maintain) |
| ⚠️ **DUAL-NAME** | 11 clusters (§5) — alias-table or archive per row |
| ☠️ **VOID** | top 3 surfaced in §9, held |

Misplacement notes: AAA `help` = Grok harness docs inside SOT (→ move to `.grok` or archive). kimi `institutional-epistemic-sink-forensics` declares `source: hermes-only` but sits in kimi (→ move). kimi `COPILOT_AUTONOMOUS_PIPELINE` = copilot-cli harness skill in kimi surface (→ §9 #1).

---

## 9. VOID Candidates (ranked, **NOT executed**)

| Rank | Skill (surface) | Evidence | Action |
|---|---|---|---|
| 1 | `COPILOT_AUTONOMOUS_PIPELINE` (kimi) | `harness: copilot-cli`; zero external references federation-wide (only self); **absent from kimi's live skill listing** → already dead weight | ☠️ VOID-ready: `SKILL.md → SKILL.md.VOID` (F1-reversible) |
| 2 | `autonomous-governed-execution` (kimi) | content absorbed into `/root/.kimi-code/AGENTS.md` §333-AGI (F13-ratified 2026-07-31); self-references that path; stale 53d… 40d | VOID **after** wiring check — it is `type: prompt` claiming "auto-triggered when session loads this AGENTS.md"; verify no hook/SYSTEM.md dependency first |
| 3 | `institutional-epistemic-sink-forensics` (kimi) | declares `source: hermes-only`; misplaced surface | MOVE to hermes (or AAA) — not a true VOID |

**Explicitly NOT a VOID candidate:** `cognitive-level-assertion-protocol` — its supersede target `governance/akal-cognitive-invariants` does not exist. VOIDing deletes the federation's only AKAL skill. Sequence: PROMOTE → re-point kimi refs → then archive the kimi copy.

### 9.4 Why executions were held (INT, F2/F7)
1. Invocation telemetry is blind (2 events) → P(dead) < 0.99 for anything not structurally provable; rank-1 is provable but is a one-line mutation that belongs in the remediation pass, not the audit pass.
2. The loaded skill's own **WAJIB-2 verification-lane doctrine**: executor and verifier must not share a trust chain. This run = observe/verify; the remediation run = execute. Mixing them would self-attest.
3. VAULT999 sealing of VOID receipts is kernel-only (`arif_seal`), out of this lane.

---

## 10. Remediation Queue (reversible-first)

**P1 — mechanical, reversible (recommend executing next pass):**
1. PROMOTE `cognitive-level-assertion-protocol` → `AAA/skills/governance/akal-cognitive-invariants/` (fix internal path refs), then retire kimi copy.
2. PROMOTE `AGI-audio-quantum-cognition` → AAA (clears 4 broken refs).
3. VOID rank-1 `COPILOT_AUTONOMOUS_PIPELINE` (+arifFlow VERIFY ingest; seal via kernel).
4. Doc repairs §7.1 (12 skills, path re-points only).

**P2 — merge decisions (owner/888 call):** clusters 5–10 (§5); `forge-mcp` vs `mcp-ops` SOT; `PETRONAS-intelligence-router` vs `MY-REALITY-STACK` scope split; `check-work` slash-wiring preservation.

**P3 — surface hygiene:** opencode re-sync (47 drifted names); hermes/hermes-asi drift audit as **separate scoped pass** (235/146 names — out of scope here, honestly declared); update the surface table in this auditing skill (§2 drift); move AAA `help` → grok surface.

**P4 — bloat:** compress `seven-zen-organs-enforcement` (1039L), `arifos-kernel-zen-audit` (793L), `ASI-summarize` (693L).

---

## 11. Independent Verification Lane checklist (per skill §WAJIB 2)

- [x] This audit ran in a distinct OBSERVE lane; remediation deferred to an executor pass — separation preserved by construction.
- [ ] Kernel rejects self-verification at contract layer — **still open substrate-wide** (documented in skill; T3 pending F13).
- [x] Original success criteria preserved: skill Procedure steps 1–7 mapped to §2–§9 of this report.
- [ ] Verifier invocable without executor cooperation — not yet a constitutional role (T3 pending).

---

## 12. Telemetry

```json
{
  "skill_name": "skill-mesh/AUDIT-recursive-audit",
  "version": "2.0",
  "trigger_phrase": "/skill-mesh.AUDIT-recursive-audit (user-slash)",
  "selected_reason": "explicit user activation",
  "latency_ms": 0,
  "token_in": 0,
  "token_out": 0,
  "commands_run": 28,
  "artifacts_written": 1,
  "postcondition_pass": true,
  "human_approval_required": false,
  "hold_code": "VOID_EXECUTION_HELD_PENDING_REMEDIATION_PASS"
}
```

## 13. Recursive Scorecard (self-assessed, INT)

| Axis | Score | Note |
|---|---|---|
| Activation Precision | 1.00 | explicit slash |
| Task Completion Rate | 1.00 | procedure 1–7 complete; postconditions met |
| Rollback Safety | 1.00 | zero mutations; single report artifact |
| Context Efficiency | 0.90 | aggregated probes, no raw dumps |
| Doc Freshness | 0.85 | URL sample clean; 77 fs refs broken |
| Cross-Skill Collision Rate | 0.10 | this bundle overlaps `engineering/skill-inventory` (cluster 10) |
| Human Trust | 0.90 | all claims OBS/DER/INT-labeled; unknowns declared |

**Shadow acknowledgment:** 176 URLs unprobed; hermes/asi/opencode drift classified by count only, not itemized; invocation telemetry effectively absent; kimi skill listing used as evidence for rank-1 VOID (listing could be filtered — re-verify at execution time).

— DITEMPA BUKAN DIBERI ⚒
