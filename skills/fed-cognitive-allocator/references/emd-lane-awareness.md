# EMD Lane Awareness — Reference (2026-08-08)

**Commit:** `a3a1bf36` (AAA main) · **Status:** live on FED :7074
**Source:** `/root/AAA/scripts/fed_router.py` (+92 lines, `_emd_check` + `EMD_MODEL_CLASS` + `AGENT_DEFAULT_OPERATION`)

## EMD_MODEL_CLASS (live, 2026-08-08)

| Model | lane | vision_in | audio_in | image_out | audio_out |
|---|---|---|---|---|---|
| MiniMax-M3 | sense | ✓ | ✗ | ✗ | ✗ |
| qwen3.8-max | sense | ✓ | ✗ | ✗ | ✗ |
| mimo-v2.5 | sense | ✓ | ✓ | ✗ | ✗ |
| mimo-v2.5-pro | sense | ✓ | ✓ | ✗ | ✗ |
| qwen3.6-flash | sense | ✓ | ✗ | ✗ | ✗ |
| deepseek-v4-pro | act | ✗ | ✗ | ✗ | ✗ |
| deepseek-v4-flash | act | ✗ | ✗ | ✗ | ✗ |
| wan2.7-image | act | ✗ | ✗ | ✓ | ✗ |
| wan2.7-image-pro | act | ✗ | ✗ | ✓ | ✗ |
| qwen-audio-3.0-tts-plus | act | ✗ | ✗ | ✗ | ✓ |
| glm-5.2 | neutral | ✗ | ✗ | ✗ | ✗ |
| qwen3.7-plus | neutral | ✗ | ✗ | ✗ | ✗ |
| kimi-k2.7-code | neutral | ✗ | ✗ | ✗ | ✗ |
| flame-free | neutral | ✗ | ✗ | ✗ | ✗ |

Source audit: LiteLLM `/model/info` (vision/audio flags), Qwen individual plan `/v1/models` (gen models).

## AGENT_DEFAULT_OPERATION

| agent_id | default operation |
|---|---|
| openclaw | sense |
| asi-555 | sense |
| hermes | metabolize |
| agi-333 | metabolize |
| apex-888 | metabolize |
| opencode | act |
| kimi | act |
| (unknown) | metabolize (fallback) |

## Mismatch rules

| Rule | Trigger | Verdict | Cadangan |
|---|---|---|---|
| R1 agent-shift | `operation` ≠ agent default + explicit operation set | MISMATCH | — |
| R2 model-lane | act+SENSE model or sense+ACT model | MISMATCH | opposite-lane models |
| R3 modality-gate | vision/audio/generation payload to capability-blind model | MISMATCH | vision/audio-capable alternatives |

**Note on R1:** `operation=""` or `"auto"` (default) does NOT trigger R1 — only explicit forced values do.

## Verified test matrix (2026-08-08)

| # | Call | Expected | Got | Notes |
|---|---|---|---|---|
| T1 | openclaw+sense+MiniMax-M3+vision+eff=med | EMD_MISMATCH | MISMATCH R2+R3 | effort=med overrides → deepseek-v4-pro, vision stripped |
| T2 | openclaw+forced ACT | EMD_MISMATCH | MISMATCH R1 | agent shift flag fires |
| T3 | opencode+act | EMD_ALIGNED | ALIGNED | ACT ↔ ACT |
| T4 | hermes+vision+deepseek-v4-pro | EMD_MISMATCH | MISMATCH R3 | vision to blind model |
| T5 | hermes+act+MiniMax-M3 | EMD_MISMATCH | MISMATCH R1 | hermes is metabolize, forced act |

**T1 is the most important finding:** effort_level silently overrides the requested model via EFFORT_MODEL_MAP. Asking for a vision-capable model with effort_level set lands on deepseek-v4-pro (vision-blind). EMD catches this automatically. This is NOT a bug in effort-level — it's working as designed. EMD provides the missing telemetry about the *consequence* of the override.

## effort-override × EMD interaction

The `EFFORT_MODEL_MAP` (lines 640+) maps effort_level to a fixed model, overriding any `model` param:

| effort_level | forced model | EMD lane |
|---|---|---|
| low | flame-free | neutral |
| medium | deepseek-v4-pro | act |
| high | deepseek-v4-pro | act |
| ultra | deepseek-v4-pro | act |

So any `fed_route` with `effort_level` + `operation=sense` + vision modality → double MISMATCH (R2 + R3). This is correct telemetry: "you asked for sense work but the effort dial forced an act model." If that's intentional, the caller should know.

## Revert recipe

```bash
cd /root/AAA
git log --oneline -3  # find a3a1bf36
git revert a3a1bf36
systemctl restart fed-router.service
# litellm-federation: NOT touched by Fasa 1 — no restart needed
```
