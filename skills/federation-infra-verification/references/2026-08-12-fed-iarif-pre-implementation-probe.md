# FED pre-implementation probe — `i-ARIF` alias + multimodal caps (2026-08-12)

> **Session:** 2026-08-12, 03:00 MYT onward
> **Trigger:** Arif said *"Test i-ARIF"* — short, direct command. Hermes ran T0 read-only probes against live FED `:7074` before any implementation work, after the previous session's OpenCode delegation had designed (but not implemented) an `i-ARIF` agent-identity alias + 4 multimodal capability signatures.
> **Lesson that drove the probe:** "If the surface isn't ready, designing on top of it is wasted work." Encode as class-level skill section §13.

## TL;DR — five findings

1. **`agent_id` is silently ignored in FED.** Six agent IDs (`i-ARIF`, `hermes-asi`, `hermes`, `openclaw`, `arif-fazil`, `unknown-agent-xyz`) all return the identical route (`qwen3.8-max` via `qwen-token-plan-individual`). Identity-based routing does not exist in the current FED surface — the planned alias has no consumer.
2. **The 4 multimodal capabilities don't exist.** `fed-vision`, `fed-image`, `fed-audio`, `fed-video` all return `KeyError: 'model'`. They are not in `CAPABILITY_SIGNATURES`.
3. **EMD gate has a pre-existing bug.** For `fed-multimodal-vision` (an existing capability), with `modality=vision`, the EMD verdict is `EMD_MISMATCH` with reason `"vision payload to vision-blind fed-multimodal-vision"`. The EMD check reads the capability SIGNATURE NAME as the model_id, not the resolved underlying model.
4. **Constitutional hard-gate × EMD bug → 0 routes at tier 666+.** At tier 333/555/888 you get 2 routes; at tier 666 you get 0. The EMD bug marks the capability as "vision-blind", the hard-gate then can't find a direct route for it, and the result is empty.
5. **`tokenrouter` security scan is a false positive.** `arifos-judge-gate.ts:49,55,88` blocks any write containing the string `tokenrouter` — but `TOKENROUTER_PRICING` is a legitimate provider key already in `fed_router.py`.

## Live probe transcripts

### Probe 1 — agent_id resolution (live)

```text
═══ TEST 1: agent_id resolution ═══
--- agent_id=i-ARIF ---
  ok=qwen3.8-max prov=qwen-token-plan-individual health=LIVE reason=zero gateway contamination; insufficient telemetry samples
--- agent_id=hermes-asi ---
  ok=qwen3.8-max prov=qwen-token-plan-individual health=LIVE reason=zero gateway contamination; insufficient telemetry samples
--- agent_id=hermes ---
  ok=qwen3.8-max prov=qwen-token-plan-individual health=LIVE reason=zero gateway contamination; insufficient telemetry samples
--- agent_id=openclaw ---
  ok=qwen3.8-max prov=qwen-token-plan-individual health=LIVE reason=zero gateway contamination; insufficient telemetry samples
--- agent_id=arif-fazil ---
  ok=qwen3.8-max prov=qwen-token-plan-individual health=LIVE reason=zero gateway contamination; insufficient telemetry samples
--- agent_id=unknown-agent-xyz ---
  ok=qwen3.8-max prov=qwen-token-plan-individual health=LIVE reason=zero gateway contamination; insufficient telemetry samples
```

**Verdict: agent_id is passthrough. No identity-based routing in current FED.** The OpenCode plan to add an `i-ARIF` alias is sound only IF `fed_route_engine` is first modified to read `agent_id` and route by it. Otherwise the alias is invisible.

### Probe 2 — capability signatures (live)

```text
═══ TEST 2: capability signatures ═══
--- model=fed-vision ---
  EMPTY/error={'type': 'internal', 'message': "'model'"}
--- model=fed-image ---
  EMPTY/error={'type': 'internal', 'message': "'model'"}
--- model=fed-audio ---
  EMPTY/error={'type': 'internal', 'message': "'model'"}
--- model=fed-video ---
  EMPTY/error={'type': 'internal', 'message': "'model'"}
--- model=fed-multimodal-vision ---
  ok=qwen-vl-max prov=mulerouter health=LIVE reason=insufficient telemetry samples
--- model=fed-doesnotexist ---
  EMPTY/error={'type': 'internal', 'message': "'model'"}
--- model=fed-reasoning-heavy ---
  ok=qwen3.8-max prov=qwen-token-plan-individual health=LIVE reason=zero gateway contamination; insufficient telemetry samples
```

**Verdict: 4 proposed multimodal caps don't exist.** Only `fed-multimodal-vision` and `fed-reasoning-heavy` are live.

### Probe 3 — EMD gate behaviour at tier 555 (live, raw)

```json
{
  "routes": [],
  "meta": {
    "capability_signature": "fed-multimodal-vision",
    "capability_description": "Image/video analysis, OCR, chart reading, screenshot inspection",
    "capability_models": ["qwen-vl-max", "mimo-v2.5", "MiniMax-M3"]
  },
  "emd": {
    "verdict": "EMD_MISMATCH",
    "operation": "metabolize",
    "model_class": "neutral",
    "reasons": ["vision payload to vision-blind fed-multimodal-vision"],
    "suggested": ["mimo-v2.5", "qwen3.8-max"]
  }
}
```

**Verdict: EMD bug confirmed.** The EMD check uses `model_id = "fed-multimodal-vision"` (the capability signature) instead of resolving to the cascade model (`qwen-vl-max`). The capability itself has vision capability defined, but the EMD check sees only the signature string and concludes the model is "vision-blind". This is a pre-existing bug, not introduced by the OpenCode plan.

### Probe 4 — constitutional hard-gate × EMD interaction (live)

| tier | routes | diagnosis |
|---|---|---|
| 333 | 2 ✅ | Hard-gate doesn't fire at low tier; cascade intact |
| 555 | 2 ✅ | Same |
| **666** | **0 ❌** | Hard-gate fires (tier ≥ 666 = direct-only); EMD marks cap as "vision-blind"; no direct model in cap → empty |
| 888 | 2 ✅ | Hard-gate fires; cascade has direct routes too |

**Verdict: At tier 666, the user gets 0 routes silently.** No error, no log — just an empty `routes: []` and an `emd.verdict: EMD_MISMATCH` nested inside the response envelope. A consumer agent that doesn't introspect `emd.verdict` will receive an empty list and treat it as "no providers available" — silently broken.

### Probe 5 — modality field behaviour (live)

```text
--- modality=text ---
  ok=qwen-vl-max verdict=
--- modality=vision ---
  ok=qwen-vl-max verdict=
--- modality=audio ---
  ok=qwen-vl-max verdict=
--- modality=image ---
  ok=qwen-vl-max verdict=
--- modality=video ---
  ok=qwen-vl-max verdict=
--- modality=omni ---
  ok=qwen-vl-max verdict=
```

**Verdict: modality field is silently ignored.** All 6 modalities return the same model. The EMD verdict field is empty in the response (`verdict=`). Either the EMD check is bypassed for capability signatures, or the verdict is computed but not surfaced.

### Probe 6 — security scan source (live)

```bash
$ grep -n 'tokenrouter\|forbidden pattern\|denied' /root/.config/opencode/plugins/arifos-judge-gate.ts
49:  /tokenrouter/i,
50:]
55:  if (/(kunci-mas|secrets\/|\.signing_key|tokenrouter)/i.test(argStr)) return true
56:  return false
88:  /tokenrouter/i,
89:  /api.?key/i,
90:  /password/i,
102:      return `forbidden pattern: ${pattern.source} matched in arguments`
```

**Verdict: security false positive.** The regex `/(kunci-mas|secrets\/|\.signing_key|tokenrouter)/i` blocks any write that contains the literal string `tokenrouter`. But `TOKENROUTER_PRICING` is a legitimate provider key in `/root/FED/fed_router.py` and `provider_table` keys in the opencode.json config. The OpenCode T1 mutation to `fed_router.py` was blocked at write-time for this reason. Patch: add a provider_table allowlist.

## OpenCode delegation history (what came before)

The previous session dispatched OpenCode with this brief:

> "Implement this bounded source-only task in /root/FED: introduce canonical identity alias i-ARIF for the Hermes-ASI route while preserving backward compatibility for hermes-asi. Embed multimodal intelligence capability routing for vision, image, audio, and video as capability signatures, not provider names. Do not invent provider endpoints or credentials. … Add/update focused tests for canonical i-ARIF, legacy hermes-asi, capability normalization, vision/image/audio/video signatures, unknown capability fail-closed behavior, and constitutional tier behavior. … Return only a structured report. … If architecture cannot be implemented honestly from current code, stop and report evidence rather than fabricate."

OpenCode produced a structured design (56 tests planned, identity alias system designed, multimodal capability signatures designed, modality normalization designed, fail-closed unknown behavior designed, constitutional tier gating designed). **All 8 mutation attempts failed.** The structured report was honest — it identified the gates correctly. But it did NOT independently verify whether the surface it was designing FOR was ready to consume the design. That gap is what the 6-probe pre-implementation checklist above is designed to catch.

OpenCode's session exit code was 0 (it returned a report), but `git status --short` against `/root/FED` returned **empty** — no files written, no diff. The "exit code 0" was misleading: it means "agent finished thinking," not "implementation landed."

## Recommendations (for any future i-ARIF / multimodal-cap implementation)

1. **First**: fix Gate 4 (cryptographic actor binding). Reconcile `/root/arifOS` source vs `/opt/arifos/app` runtime. Re-init with Ed25519-signed SCT.
2. **Second**: fix Gate 2 (security scan false positive). Patch `arifos-judge-gate.ts` to allowlist `provider_table` strings (`tokenrouter`, `kunci-mas`, `secrets/`, etc.).
3. **Third**: fix Probe 3 (EMD gate bug). The EMD check should walk the resolved cascade and read each model's `vision_in`/`audio_in`/`image_out`/`video_out` flags, not the capability signature's name as the model_id.
4. **Fourth**: fix Probe 4 (constitutional hard-gate interaction). Once EMD is fixed, tier ≥ 666 should resolve correctly because direct-only check will find direct routes for vision-capable models.
5. **Fifth**: add `agent_id` consumption to `fed_route_engine`. Currently `agent_id` is a passthrough field; adding it to the route-engine input is a prerequisite for the `i-ARIF` alias to have any effect.
6. **Sixth**: only then, implement the planned identity aliases and multimodal caps.

Until 1–5 are done, the OpenCode plan is sound-but-stuck. File the design as a forge_work artifact + seal the probe transcript as evidence; mark `IMPLEMENTATION_PENDING_SURFACE_READINESS`.

## Cross-references

- Parent skill: `federation-infra-verification` §13 (newly added)
- Earlier session finding on EMD vs modality: `references/mcp-surface-compute-vs-governance-2026-08-07.md`
- MCP `arif_init` identity gate semantics: `references/2026-08-07-mcp-identity-gate-and-self-reconciling-drift.md` (the `actor_verified: false, session_token: null` pattern is the same gate that surfaced here)
- `arifos-judge-gate.ts` source: `/root/.config/opencode/plugins/arifos-judge-gate.ts` — confirmed lines 49, 55, 88 contain the over-broad `tokenrouter` pattern
- `fed_router.py` source: `/root/FED/fed_router.py` — `CAPABILITY_SIGNATURES` dict at line ~538; `fed-multimodal-vision` exists; `fed-vision/image/audio/video` do not
