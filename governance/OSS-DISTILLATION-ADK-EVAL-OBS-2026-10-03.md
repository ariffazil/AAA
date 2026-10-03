# OSS Distillation Intake — ADK Lab: Eval, Observability & Guardrails (kuanhoong)

> **Status:** DRAFT_RECEIPT (2026-10-03) — external-OSS distillation intake; not doctrine, no F13 instrument claimed.
> **By:** FI-008 (kimi-code), sesi `SEAL-ddf5fe51f3cf465b` · **Source:** [kuanhoong/adk-lab-eval-observability](https://github.com/kuanhoong/adk-lab-eval-observability) (Poo Kuan Hoong, Ph.D) — code-verified against `agent/agent.py` + `agent/eval.py` (raw fetch 2026-10-03, OBS), not README-claimed only.
> **Precedent:** FED-OSS-DISTILLATION-2026-10-03.md §3 (disposition-table format, Canon #0 gate, kill criteria).

## What the artifact IS (OBS)
Hands-on teaching lab (~6 files) turning a demo Google ADK agent into a measurable/observable/safe one using ADK-native callbacks — **no third-party observability vendor**. Three pillars: `before_model_callback` (PII redaction + injection block), `after_model_callback` (token/cost tally → USD estimate), LLM-as-judge eval over a golden set. Guards are pure-Python and **self-test offline without an API key** ("5/5 injection cases correct"). Honest caveat in-source: teaching-grade detectors; production swaps in Cloud DLP/Presidio + trained classifier — *the mechanism (chokepoint callback) stays identical*.

## Disposition table

| # | Pattern in lab | Federation verdict | Basis |
|---|---|---|---|
| 1 | **Input-boundary chokepoint**: redact PII + block injection BEFORE any model call | **BANK — Phase-2 candidate, sovereign's binary if wanted.** Our topology is stronger than theirs: they patch per-agent callbacks; we own ONE gateway chokepoint (HAProxy :4000 → litellm :4013) that ALL warga traffic crosses — a litellm pre-call hook covers every lane at once | Exposure class is STRUCTURAL (warga forward sovereign/human content to EXTERNAL providers — deepseek/minimax/qwen endpoints — with zero redaction layer), **0 recorded incidents**. Canon #0(a) demands demonstrated failure class → not built now; consistent with RouteLLM treatment. Their detector suite (typed labels · Luhn validator cutting false positives · de-obfuscation normalise · offline self-test) is the spec seed if built. Local delta to add: **MyKad/NRIC detector** (XXXXXX-XX-XXXX) absent from their set — Malaysian context gap |
| 2 | LLM-as-judge over golden.json, JSON-verdict with brace-recovery parse | **ALREADY OWNED — no action.** E1-E8 competency evals + 21-eval bench corpus + m_min audit + CHRON Brier calibration are strictly stronger. Nicety banked: verdict parse `raw[find("{"):rfind("}")+1]` survives judge verbosity | OBS |
| 3 | Per-call token/cost dashboard (USD) | **ALREADY OWNED — no action.** token_bank.db + fed_report_latency + spend telemetry | OBS |
| 4 | OTel GenAI standard spans → any OTLP backend (vendor-neutral) | **BANKED, no date.** Our telemetry is custom JSONL (receipts/wire/token_bank). Standard-convention emission pays off only when an EXTERNAL consumer of federation telemetry exists — none today. Kill: build when first external consumer appears | DER |
| 5 | "Guards must be testable without the model" (offline self-test, no API key) | **CONFIRMED CONVERGENCE — house style already.** gitleaks/doctrine/esm/litellm-dangling gates all run offline-deterministic at commit boundary. Their lab independently validates the law; name kept for teaching reuse | OBS |
| 6 | Lab format: graded exercises + participant checklist | **BANKED for onboarding doctrine.** Federation onboarding for new warga/humans could use the same shape (verify-offline-first, exercises, checklist). No action now | INT |

## Kill criterion for this artifact
If litellm ships a first-class guardrails layer that supersedes the pre-call-hook approach, §1's banked spec retires; if the gateway is replaced, the chokepoint mapping is historical — supersede, don't maintain in parallel.

*DITEMPA BUKAN DIBERI ⚒️*
