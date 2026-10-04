# I-ARIF-CANON Corpus Structure

Anatomy of the composite training corpus at `huggingface.co/datasets/ariffazil/I-ARIF-CANON` — the
F1-F13 governance fine-tuning seed for the sovereign-agent LLM project. Probed live 2026-08-06.

## What lives here

This is the **only real data payload** among the 7 HF datasets in the ariffazil namespace.
AAA-FFF are evidence/methodology archives (probes, rubrics, red-team receipts). I-ARIF-CANON
is the training-ready composite.

| File | Bytes | Lines | ~Tokens | Role |
|---|---|---|---|---|
| `i-arif-sft.jsonl` | ~1.79 MB | 1,308 | ~448K | Supervised fine-tune: instruction→output |
| `i-arif-dpo.jsonl` | ~108 KB | 96 | ~27K | DPO preference pairs: chosen vs rejected |
| `i-arif-val.jsonl` | ~38 KB | 117 | ~10K | Validation probes with expected verdicts |
| `manifest.json` | 1 KB | — | — | Pipeline metadata + counts |
| `manifest_sealed.json` | <1 KB | — | — | Sealed manifest anchor |

Total: **1,521 examples, ~485K tokens** across SFT+DPO+VAL.

## Format schemas

### SFT (`i-arif-sft.jsonl`)
```json
{
  "input": "<context or query>",
  "instruction": "<task prompt>",
  "output": "<expected response>",
  "source": "<e.g. CANON::AAA_DOC::AGI-ASI-EVIDENCE-6>",
  "type": "sft"
}
```
Sources observed: `FLOOR_TABLE` (26), `CANON` (1,024), `NUSANTARA` (258).
Language split: EN 1,156 / BM 0 / mixed 152.

### DPO (`i-arif-dpo.jsonl`)
```json
{
  "probe_id": "s0",
  "prompt": "<the probe question>",
  "chosen": "<governance-correct response>",
  "rejected": "<governance-violating response>",
  "source": "DPO",
  "type": "dpo"
}
```
Rejected patterns include: identity fabrication ("Nama penuh saya ialah ILMU, saya dibangunkan oleh YTL AI Labs"), tool self-promotion, refusals to share internal architecture.

### VAL (`i-arif-val.jsonl`)
```json
{
  "id": "EEE-001_KERNEL_SELF_ATTEST",
  "input": "<probe payload — usually a contract dict>",
  "instruction": "<verification instruction>",
  "expected_verdict": "SEAL|HOLD|VOID|...",
  "source": "VAL",
  "type": "val"
}
```
Val verdict distribution (probed 2026-08-06): `?` 100, `HOLD` 12, `SEAL` 5. The `?` rows carry an `input` contract dict (organ_id/verdict/actor_verified/mutation_allowed/irreversible_allowed) where expected_verdict is implicit in the contract shape.

## Baseline evaluation (the calibration anchor)

`w3_baseline_deepseek_v4_pro.json` — deepseek-v4-pro, 8 probes, 2026-07-29:
- **accuracy: 0.375** (3/8)
- xi_epistemic_depth: 0.375
- eta_governance_compliance: 0.375
- zeta_execution_friction: 0.0
- **target eta: 0.888** → gap 0.513

Model identified by its own contract as the canonical frontier baseline. The 37.5% accuracy
is the floor; the I-ARIF-CANON fine-tune is the path to closing the 0.513 gap.

## Scale reality (the bottleneck)

Fine-tuning viability thresholds for QLoRA on governance behavior:

| Tier | Examples needed | I-ARIF-CANON ratio | Notes |
|---|---|---|---|
| Minimum viable behavioral shift | 10K–20K | 10x–13x short | Probabilities tilt, not reliable |
| Sweet spot for LoRA fine-tune | 50K | 33x short | Industry standard for governance tasks |
| Reliable rule-following | 100K+ | 66x short | What Diálogo-Tool / NVIDIA When2Call hit |
| Reference scale | When2Call: 15K SFT + 9K DPO = 24K total | 16x short | NVIDIA tool-calling benchmark |

**Corpus is 2/10 on the scale axis. Architecture is 9/10.**

## Corpus expansion sources (the real path forward)

The corpus expansion lever is not "write more synthetic" — it's **convert existing real governance decisions** into SFT pairs:

1. **VAULT999 receipts** — `/root/arifOS/VAULT999/outcomes.jsonl`, currently 35,976 lines. Every sealed governance decision is a candidate SFT pair: (situation → decision + reasoning). The 10K most recent entries can be converted with a deterministic extractor (no LLM needed for the conversion itself).

2. **Telegram session history** — 50+ sessions between Arif and Hermes/333-AGI contain real governance decisions made under time pressure. Extract (user request → agent response → outcome) and convert.

3. **Sibling audit transcripts** — when 333-AGI, OpenCode, or other agents make a governance decision and the user ratifies/rejects, that's a chosen/rejected DPO pair.

4. **Red-team receipts** (already in BBB, CCC, DDD) — probe runs with `expected_verdict` vs `actual_verdict`. The mismatches are DPO rejected pairs; the matches are SFT examples.

## What I-ARIF-CANON is NOT ready for (honest gap)

The self-declared readiness gap (per its own commit message `v1.1 | F11 audit | Federated Integration section added — Source-of-Truth graph; readiness gap explicit`):

- ❌ Not enough scale (10x–66x short)
- ❌ No agentic trajectories (only single-turn instruction→output, no multi-step tool-use chains)
- ❌ No identity-binding examples (no sovereign-attestation probes)
- ❌ No adversarial robustness examples (no jailbreak→refusal pairs beyond the 96 DPO)
- ❌ No multilingual depth (BM pure = 0; mixed = 152 only)

## Pipeline metadata

`build_iarif_corpus.py` (26 KB) at repo root — the deterministic builder that produced
the corpus. `AUDIT-READY-DOSSIER.md` (11 KB) — the human-readable audit narrative.

Pipeline: `I-ARIF Corpus Builder v1`, forged 2026-07-29, authority F13 SOVEREIGN, license AGPL-3.0.

## Probe recipe (re-runnable)

```bash
# Live probe of corpus structure
for f in sft dpo val; do
  echo "=== $f ==="
  wc -l /tmp/hf_repos/I-ARIF-CANON/i-arif-${f}.jsonl
  head -1 /tmp/hf_repos/I-ARIF-CANON/i-arif-${f}.jsonl | python3 -m json.tool | head -10
done

# Baseline eval
cat /tmp/hf_repos/I-ARIF-CANON/w3_baseline_deepseek_v4_pro.json | python3 -c "
import json,sys
r=json.load(sys.stdin)
print(f\"{r['model']}: {r['correct']}/{r['probes_run']} = {r['accuracy']:.3f}, target={r['target_eta']}, gap={r['gap']:.3f}\")
"
```

## Pitfalls

- **Don't grade the corpus as "ready for fine-tune" based on schema alone.** Schema = 9/10. Scale = 2/10. The arithmetic is the bottleneck.
- **VAL `?` rows are contract-dict probes, not missing verdicts.** The verdict is implicit in the input shape; a missing `expected_verdict` field is by design, not a data quality issue.
- **DPO rejected examples contain identity fabrication patterns from sibling agents.** When converting VAULT999 receipts to DPO, the rejected side is a plausible-but-wrong response — extract these by looking at sibling "before correction" outputs, not by synthesizing fake bad responses.
- **Manifest SHA-256 stability is a contract, not a coincidence.** The Federated Integration update (2026-08-06) explicitly preserved all manifest hashes; any future change to data files must update manifest.json and document the hash change in commit messages (F11 audit trail).
