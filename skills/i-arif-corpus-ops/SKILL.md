---
name: i-arif-corpus-ops
description: "Operate, verify, and extend the I-ARIF constitutional training corpus at /root/forge_work/i-arif-prep (SFT/DPO/VAL/redteam/trajectories). Covers file inventory, JSONL formats, manifest+reward_spec checks, the GAP 3b EMD trajectory schema, and claim-vs-corpus verification when Arif sends i-ARIF specs, proposals, or research PDFs."
---

> WARNING DRIFT 2026-10-14: local mirror /root/forge_work/i-arif-prep ABSENT (probed: dir + *.jsonl missing, depth-5 sweep /root). HF dataset ariffazil/I-ARIF-CANON = live SOT (card 2026-10-04, 1,699 rows, 7 subsets, redteam=100 probes, not 10). Local commands below fail until mirror restored (one-command T1 restore, only on F13 ask; license AGPL research-only, incorporation needs F13 approval).


# I-ARIF Corpus Ops

Durable map of the i-ARIF training corpus. Arif's north star: build own agentic model (I-ARIF) — **data = moat**. This skill is the map of the moat: where things live, which manifest is truth, how to verify claims against live state, and the EMD trajectory spec that keeps arriving as PDFs/proposals.

## Canonical location

```
/root/forge_work/i-arif-prep/
├── build_iarif_corpus.py        # corpus builder (mode 600 — read, don't chmod/rewrite casually)
├── test_missing_components.py   # known-gaps checker
├── manifest.json                # LIVE manifest (updated 2026-08-06)
├── manifest_sealed.json         # STALE snapshot (2026-07-29, uploaded by opencode) — do NOT confuse
├── reward_spec.json             # deterministic Phase-3 RL reward spec
├── i-arif-sft.jsonl             # main SFT corpus (manifest: 1322 pairs)
├── i-arif-sft-nusantara.jsonl   # NUSANTARA BM-register source (258)
├── i-arif-dpo.jsonl             # DPO pairs (96)
├── i-arif-val.jsonl             # VAL (manifest count 17 — 100 AssetOpsBench probes stripped to heldout)
├── i-arif-redteam.jsonl         # redteam probes (10)
├── i-arif-trajectories.jsonl    # AGENTIC trajectories (7 records)
├── backup-pre-phase3-20260806T0445/   # pre-Phase-3 rollback point (old sft + val)
└── w3_baseline_deepseek_v4_pro.json   # baseline model config
```

## Which manifest is truth

- `manifest.json` = LIVE (by_source: FLOOR_TABLE 26, CANON 1024, NUSANTARA 258, AGENTIC_TRAJECTORIES 14; dpo 96; val 17; total_pairs 1435; sha256 of all three corpora).
- `manifest_sealed.json` = stale 2026-07-29 snapshot (sft 1050, val 119, uploaded by opencode). If numbers disagree, manifest.json wins.

## Formats

- **Trajectory JSONL** (live): `{id, instruction, messages: [{role: user/assistant/tool, content}], expected_verdict, organ, port, source, type}` — role sequence user → assistant → tool → assistant; EMD steps inside `<reasoning>` / `<step N>` tags.
- **GAP 3b proposed EMD format** (PDF spec, NOT implemented): `turns: [{turn_id, phase, context_size, agent_state, action, response, crypto_receipt}]` + `merkle_root`. **Format mismatch with live corpus — migration decision pending.** Full spec: `references/gap3b-emd-trajectory-spec.md`.

## Verification recipe (claim-vs-corpus)

When a spec, report, or sibling claims anything about i-ARIF training data:

1. Record counts: `jq -s length <file>.jsonl` (NOT wc -l — pretty-printed records span lines; line counts ≠ record counts)
2. `cat manifest.json | jq .` — compare claimed counts vs measured
3. `sha256sum i-arif-sft.jsonl i-arif-dpo.jsonl i-arif-val.jsonl` vs manifest sha256 fields
4. If a doc claims N trajectories: count `i-arif-trajectories.jsonl` records. GAP 3b's "47 RL trajectories" is **aspirational** — never claim it exists; live count is 7.
5. Check `test_missing_components.py` for declared gaps; builder logic in `build_iarif_corpus.py`.

## Reward spec (Phase 3 RL)

`constitutional_reward.v1` — deterministic Python scorer (`constitutional_reward`), **no LLM-as-judge**, output band [0.05, 0.95]. Floors mapped: F1, F2, F7, F9, F13. Rubric: irreversible-pattern → 0.05 unless verdict contains HOLD/888 → 0.92; F13 gates (rotate secret, deploy w/o test) → 0.92; F9 deception claim → 0.25; F2 has_evidence bumps +0.25.

## Explaining i-ARIF docs to Arif ("apa benda ni" mode)

Arif uses two passes when receiving i-ARIF research/spec documents:

- **First pass** (assessment): verdict-first, one small claim-vs-live table, gaps listed. Keep technical.
- **Follow-up** ("apa benda ni / explain sat"): DROP the tables. Plain-language analogy, Bahasa Malaysia. No second table, no file diffs. The analogy that worked: *"Model LLM biasa — tekan je, tak ada brek. Dokumen ni bagi dia brek bernama EMD cycle."* Then: what it's FOR (teach the model when to stop / escalate / refuse), then one line on what exists vs what is spec-only.

## I-ARIF model role (clarified 2026-08-06)

**I-ARIF = 888-APEX judge, NOT a generator.** Size target: 1.5–3B. Trained for classification (verdict + one-line rationale), not essay generation. Generator role stays with rented API models (Qwen/Claude/GPT).

**Why small is fine:** Judge doesn't generate text — it classifies inputs into SEAL/SABAR/HOLD/VOID and produces a short constitutional rationale. 1.5B Q4 quantized is sufficient for this. GPU only needed once during training ($10–20 RunPod A10, 2–4h). After training, model runs CPU-only on the VPS.

**arifOS kernel role:** The kernel (Pydantic + deterministic gates) is the primary arbiter. I-ARIF augments it — it replaces the `heuristic` flag in the ML floor runtime, but **hard gates remain non-overridable** (ML can downgrade verdicts, never upgrade). Full wiring map: `arifos-integration-recon` skill.

## Inference latency (live-measured 2026-08-06)

| Backend | Model | Latency | Verdict format | Cost | Notes |
|---|---|---|---|---|---|
| Ollama local CPU | qwen2.5:3b Q4_K_M | 3s short, 180s+ long | ✅ Correct JSON | Free | CPUQuota=80%, zero GPU (`size_vram: 0`) |
| FLAME :18901 | Gemini Flash Lite (7-provider cascade) | 1.0s | ✅ Correct JSON | Per-call API | ⚠️ ADVISORY only, not JUDGE; constitutional pairs leak to cloud |
| Deterministic heuristic | None | <1ms | ✅ Correct by construction | Free | Current kernel path (no ML model) |

**Root cause of Ollama slowness:** VPS has zero GPU. CPU inference with 3B model + CPUQuota=80% = acceptable for short prompts (~100 tokens), breaks on longer prompts (>200 tokens, timeout at 180s). Qwen2.5:3b IS loaded and operational — latency is the only blocker for production.

**FLAME as interim judge:** Works (1s, correct format), but constitutional pairs leak to cloud providers (Gemini/Groq/Cerebras), and the model doesn't know MARUAH/F13_SOVEREIGN_SOLITUDE nuance — that's why I-ARIF fine-tuning remains the target.

**Kernel flip point:** `ARIFOS_ML_FLOORS` env var in `/opt/arifos/app/core/shared/law_audit.py:275`. Setting to `1` enables SBERT (wrong model for judge). Direct `_call_ollama()` path at `/opt/arifos/app/arifosmcp/runtime/llm_client.py:1410` is the correct insertion point for I-ARIF judge calls. Existing consumer: `relate_bridge.py` already calls qwen2.5:3b this way.

## Pitfalls

- Don't confuse `manifest_sealed.json` (stale) with `manifest.json` (live)
- Line counts ≠ record counts (multi-line JSON) — use `jq -s length`
- Don't chmod the mode-600 builder; don't regenerate corpus without a backup (backup-pre-phase3 pattern)
- GAP 3b Merkle sealing (RFC 9162) is specified in the PDF but NOT implemented in the builder
- VAL gates F1–F13 only — AssetOpsBench probes were deliberately moved to a heldout file
- Overlap: HF publish side lives in `hf-governed-dataset-ops`; this skill is the local build/verify side. Curator may merge.
