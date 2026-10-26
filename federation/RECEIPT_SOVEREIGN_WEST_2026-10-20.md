# RECEIPT — SOVEREIGN-WEST last-resort rung (origin diversification)

- Date: 2026-10-20 12:41–12:52 UTC (20:41–20:52 MYT)
- Actor: claude-code-kvm8 (FI-002, engineer lane)
- Trigger: Arif — "deep research and upgrade the system current state after u stabilize all"
- Lane: B (local, reversible, deployed + verified)

## Finding (OBS)

Live probe of `/root/A-FORGE/litellm-config.yaml` + work-path calls through
`127.0.0.1:4013`:

| item | state 2026-10-20 |
|---|---|
| model groups | 60 before → 61 after |
| seat fallback ladders | 17 seats, **100% Chinese-origin rungs** |
| CN-only groups | 53 / 60 |
| OPENCODE_GO rungs (go-*) | **dead** — "Insufficient account funds" |
| MISTRAL rungs | **dead** — `billing_payment_failure` + bad `openai/mistral/<model>` prefix |
| OPENROUTER | **dead** — insufficient credits |
| GEMINI key | direct generateContent OK, **proxy 402** "prepayment credits depleted" |
| `apply-litellm-config.sh` | **broken**: key stored quoted, grep missed it, `set -e` exited rc=1 with no output |
| DeepSeek live | `deepseek-flash` = DeepSeek-V4.1-Flash, 1,048,576 ctx, 393,216 out |

Meaning: one origin cut-off (account, policy, network) would have stopped every
seat. The 2026-10-17 DeepSeek release / DHS order is the news hook; the failure
class is provider withdrawal, which had already happened to four Western paths.

## Change (OBS + DER)

1. Added model group **`sovereign-west`** — 2 Groq deployments (`gpt-oss-120b`,
   `gpt-oss-20b`), OpenAI-compat route, `GROQ_API_KEY`.
2. Appended `sovereign-west` as the **final rung of all 33 fallback ladders**
   (17 seats + 16 model-group ladders). CN stays primary; West is insurance.
3. Fixed 3 Mistral groups: `openai/mistral/<id>` → `openai/<id>` (when billing returns).
4. Fixed `apply-litellm-config.sh` key extraction (quote-tolerant) + explicit
   failure line instead of silent `set -e` death.
5. Bumped writer-of-record header per the file's own concurrency rule.

Files:
- `/root/A-FORGE/litellm-config.yaml` — sha256 `a70f2d9d71c5…`, immutable bit restored
- `/root/A-FORGE/scripts/apply-litellm-config.sh` — sha256 `be5c152a2ecc…`
- `/root/AAA/scripts/upgrade_sovereign_west_20261020.py` (idempotent, `--write`)
- `/root/AAA/scripts/upgrade_sovereign_west_fix_20261020.py`

## Verification (OBS)

- `apply-litellm-config.sh`: YAML OK 148 deployments / 33 ladders; restart; health 200 in ~28s; canary `APPLY_OK`; marker `a70f2d9d71c5`.
- `POST /v1/chat/completions model=sovereign-west` → `WEST_OK` (Groq gpt-oss-120b).
- `POST /v1/chat/completions model=apex-888` → `APEX_OK` (glm-5.3-flash — CN primary intact).
- `/v1/model/info` → 2 `sovereign-west` entries loaded in-process.
- `fed-fallback-validator.py` → warnings only on pre-existing CN groups; none on `sovereign-west`.

## Not proven (INT / UNKNOWN)

- Fallback **firing** end-to-end was not forced (no fault injection). Ladder is
  loaded in-process (OBS); that it switches on CN failure is litellm router
  behaviour (DER), not observed today.
- Groq free tier is rate-limited — emergency rung, not production capacity.

## Rollback

`git show HEAD:litellm-config.yaml` = pre-change `01e717fc08a41781` (exact;
file was identical to HEAD before edit) → restore, `chattr -i`, write,
`chattr +i`, run apply script. A-FORGE change is **uncommitted** (repo owned by
AAA infra; commit not requested).

## Cost decisions left to Arif (not blocking)

Paying for one second Western provider (OpenRouter / Gemini / Mistral) turns a
free-tier emergency rung into real capacity. Nothing in the system depends on it.
