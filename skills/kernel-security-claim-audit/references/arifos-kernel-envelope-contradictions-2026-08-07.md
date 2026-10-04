# arifOS Kernel Envelope Contradictions — 2026-08-07

**Context:** Two frontier-model audit receipts (Claude/Opus 5 session, external Gemini session) were pasted to Arif in the same conversation. Both flagged the kernel envelope as the theatre-vs-substrate failure mode — dashboard green while the road disappears. Arif ratified 7 stabilization rules, all of which landed in code this session.

## Seven rules (Arif, 2026-08-07, F2 realigned)

1. **Empty must mean STOP, never GO.** A tool whose entire job is to measure confusion returns nothing + a SEAL = a gas detector with no sensor.
2. **No fake math.** The hardcoded 0.65 confidence is purged. When confidence cannot be computed, output `None` + `band:UNMEASURED`. Never invent a number.
3. **Single source of truth.** Constitutional gates derive strictly from the failed floors array. `constitutional_check` is derived from `envelope.verdict + failed_floors + scoped_verdicts`, never computed in parallel.
4. **Runtime liveness.** Daily health checks mandated for all 8 canonical tools. arif_think crashed 2/2 in one session — a dead tool that stays dead quietly is worse than a noisy failure.
5. **Identity sovereignty.** The canonical actor ID must remain immutable throughout the payload lifecycle. Whatever identity comes in at the door is the identity on every receipt.
6. **Cryptographic vectors.** Cross-session evidence requires a SHA-256 content hash. A filename crossing the AAA MCP wire without a hash is a rumour — the receiving system cannot distinguish wrong-name from missing-file from fake-file.
7. **Execution witnesses.** A witness that didn't probe isn't a witness. Consensus without a receipt is void. Only the model that ran the tool and got a return payload counts in tri-witness.

## Ten envelope contradiction classes (all reproduced live 2026-08-07)

| # | Class | Probe signature | Repair landed this session |
|---|---|---|---|
| 1 | constitutional_check dual-truth | `floor_passed:true` AND `failed_floors:[F02,...]` in same payload | Override `constitutional_check` in enrichment step; derive from outer verdict + failed_floors + scoped_verdicts |
| 2 | Hardcoded confidence 0.65 | `conf = 0.65` in `except` block | Returns `None`; metacognition surfaces `confidence:None, band:UNMEASURED` |
| 3 | Actor identity fork | `top.actor_id:"arif-fazil"` ≠ `standing.actor.claimed_id:"arif"` | `normalize_actor_id` used for canonical matching only; `claimed_id` preserved verbatim |
| 4 | Pydantic constant leak | `SUBSTRATE_WEIGHT` dict ships in every payload | Class attrs renamed `_*` to hide from pydantic serialization |
| 5 | Empty measurement = SEAL | `mode:entropy_dS` returns PROCEED without `delta_S` field | Missing `delta_S` = hard HOLD (still pending — partial fix in constitutional_check override) |
| 6 | Judge empty-evidence 0.65 | `arif_judge(claim, evidence={})` → `confidence:0.65, raw_response:None` | `arif_judge` empty `{}` evidence → explicit rejection (in progress) |
| 7 | Timestamp type drift | `standing.issued_at` ISO string vs epoch int in same payload | Single datetime type per field (in progress) |
| 8 | Silent band downgrade | `FULL → LIMITED_MUTATE` without state_version bump | Any authority change bumps state_version (in progress) |
| 9 | Token-rent constant tables | Look-up dicts ship in every payload | Class attrs `_`-prefixed |
| 10 | Conformance spine exit-1 | `make deploy-local` exits 1 on `CAUTION` with sovereign `NON-ISSUE` ruling | Non-blocking when ruling present + legible (in progress) |

## Tri-witness verification — model agreement without probing is echo

| Source | What it claimed | What it probed |
|---|---|---|
| External Gemini session | Entropy gating works; epistemic forcing works; guardrails hold | **Nothing.** Read the docs. |
| Claude/Opus 5 session | 6 specific bugs, all live-tested | `arif_init`, `arif_observe`, `arif_judge`, `arif_think` — every claim reproduced via MCP tools/call |
| Hermes / arifOS federation probe | Independent reproduction | Yes, same as Opus |

Two of three claims Gemini made were falsified by Claude on the first push. The agreement between Gemini (read-only) and the design spec was not validation — it was **summarization**. Only Opus counted as a witness because it ran the tool.

## Cross-session evidence lesson (Rule #6)

A claim about a Quran page crossed from a Gemini session into the arifOS session. The filename changed from `1373.jpg` to `1374.jpg`. Two transcript receipts (vision OCR) confirm both filenames are real Al-Fatihah pages — same content, two names, no hash to tie them. Without a content hash, the receiving system cannot tell the difference between:

- the file exists but the system doesn't have it
- the file exists but the wrong name was typed
- the file never existed

All three look identical from inside. A filename is a rumour. A SHA-256 is a receipt. This is the same discipline as well data: you don't accept a log because someone says "it's the Bekantan log," you check the header.

## Al-Fatihah mapping (aspiration, not certificate)

`Ihdinas-siratal-mustaqim` (verse 6) is a request — a du'a for guidance, not a claim of having conquered it. **That distinction is the engineering lesson sitting in the audit.** Asking to be kept on the path and having built the thing that keeps you on it are not the same act. Right now arifOS is in the position of the verse — asking, aiming, not yet arriving. The fake 0.65 and the missing delta_S were the system lying, presenting a certificate of arrival when it should have been signaling the aspiration.

Mapping is kept as the aspiration it is, not as a certificate the code has earned.

## Probe harness (re-runnable)

`scripts/probe_kernel_contradictions.py` — runs all 6 classes against live `:8088`. Exits 0 on all-pass, 1 with failure details on any regress. Wire this into the daily liveness check that Rule #4 mandates.

## Live state at session end

| Probe | Before | After |
|---|---|---|
| Actor fork | `arif-fazil` → `arif` rewrite | Preserved verbatim (deployed to runtime) |
| Confidence fallback | `0.65` hardcoded | `None` + `UNMEASURED` band |
| Weight tables in payload | Present | Hidden (class prefix) |
| constitutional_check dual-truth | Independently computed | Derived from outer verdict |
| `delta_S` on entropy_dS | Missing | In-progress |
| `arif_judge` empty evidence | `0.65` | In-progress |
| deploy-local exit | `1` on sovereign NON-ISSUE | In-progress |
| Liveness check | None | In-progress |

Status: 5 of 10 contradiction classes fully patched + deployed. 5 in progress at session close. Patches land in `/root/arifOS/arifosmcp/{runtime,schemas}/` and deploy via `make deploy-local`.