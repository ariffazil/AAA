# Izzu-in-AIA Incident — 2026-08-09 full trace

Multi-user Telegram: Izzu (1024343313) silently ignored in AIA group (-1003521544074), then agent showed amnesia about an email it sent. Root causes found, all fixed.

## Symptom chain

1. Izzu posts in AIA group → bot never replies (silent drop)
2. Agent later replies "Hang yang hantar hang buat lupa" — no memory of sending Izzu an email
3. Agent told Izzu "Aku tak boleh generate gambar" — despite image gen being available

## Root causes (4 independent failures)

| # | Cause | Detection | Fix |
|---|---|---|---|
| 1 | `kunci-mas.env` `TELEGRAM_ALLOWED_USERS` lacked Izzu+Aliff → adapter dropped them pre-lane | `grep TELEGRAM_ALLOWED_USERS /root/.secrets/kunci-mas.env` vs config `allow_from` | Added `1024343313,1237635275` to all 3 env allowlists + regenerated flat.env |
| 2 | No `post_llm_call` hook → lane memory never accumulated | `MEMORY-izzu-aia.md` stayed at skeleton size; no interaction entries | Added `_on_post_llm_call` to lane_switch `__init__.py` + declared in `plugin.yaml` |
| 3 | Stale `.runtime.json` had `chat:-1003521544074 → arif` → shadowed per-user detection | Read `.runtime.json` | Cleared all `chat:*` keys, kept `user:*` |
| 4 | Lane skills were `gemini-media-gen` (nonexistent) + `comfyui` (no GPU) → agent believed it had no media ability | `find` for skill dirs; capability map absent | Unified 8 real skills for all lanes + injected CAPABILITY MAP into lane card |

## Additional find: lanes.yaml corruption

`lanes.yaml` contained `18|    skills:` — line-number prefixes from `cat -n` output had been written back into the file. This broke every string-match patch until stripped:

```python
import re
content = re.sub(r"^\d+\|", "", content, flags=re.MULTILINE)
```

## The capability-map lesson

The agent said "I cannot generate images" because (a) `check_image_generation_requirements()` returned False (no FAL key, no provider configured) and (b) no skill was loaded. Both fixed: Gemini scripts created (`gemini-image.py`, `gemini-video.py` — both tested working) and the lane card now injects:

```
CAPABILITY MAP (you HAVE these abilities — do NOT say you cannot):
- IMAGE GEN: /root/HERMES/scripts/gemini-image.py
- VIDEO GEN: /root/HERMES/scripts/gemini-video.py
...
GOVERNANCE LADDER: banter=none, media=auto, memory=receipt, publish=judge...
```

## Verified state after fixes

- Gateway @ASI_arifos_bot, allowlists contain all 4 humans
- Lane card visible in agent context (social graph + capability map + ladder injected)
- 435 skills validated, 0 broken (2 repaired: hermes-propose-seal YAML colon, well-governance-ops missing frontmatter)
