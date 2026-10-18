# EXECUTION RECEIPT — Entity-Type Fix (F13 "execute all") · 2026-10-17

## VERDICT (measured, not sealed)
The "capitalization → PERSON" bug is **fixed and verified live**, both directions:
- Model token → SYSTEM → no false CL-03 → PASS.
- Human token → PERSON → CL-03/RASA_GATE → 888_HOLD (protection intact).

## CHANGES (2 files + 1 new test)

### `mcp/hermes-rasa/principal_type_classifier.py` (fine classifier)
1. `_TECHNOLOGIES` += `gpt-5`, `claude-2` (hyphenated variants were falling through Layer 6).
2. `_AI_ORGANS` += `rasa` (HERMES RASA organ → AI_ORGAN, never PERSON).
3. `_PERSONS` += `arif`, `arif fazil`, `syed khairuddin`, `syed khairuddin morktarudin`, `alice` (explicit person signal).
4. **Typo fix:** `"anthony lok"` → `"anthony loke"` (was masked by the capitalization heuristic).
5. Added `_TITLE_PREFIX_RE` (Dr./Mr./Ms./Datuk/Dato'/Tan Sri/Puan Sri/Tun/Prof./Ir./Sr./Haji/Hajah) → independent person signal.
6. **Layer 4.5:** title-prefix → PERSON.
7. **Layers 5 & 6 RETIRED:** `capitalized → PERSON` heuristics removed → fall through to UNKNOWN.

### `hermes_mcp/_perspective.py` (coarse fallback)
1. `SYSTEM_TERMS` += `gpt-5`, `claude-2`, `rasa` (belt-and-suspenders).
2. **Fallback retired:** `name[:1].isupper() → PERSON` → `UNDEFINED` (F1 deny-by-default, F2 truth).

### `hermes_mcp/test_entity_type_regression.py` (NEW)
Standalone assert script: 21 non-human (≠PERSON), 6 human (==PERSON), 4 ambiguous (≠PERSON), 3 pronoun (==UNDEFINED).

## TEST
- **BEFORE:** FAIL — 7 regressions (GPT-5, RASA, Claude-2, Hope, Justice, Apple, Amazon → PERSON).
- **AFTER:** PASS — all green. + classifier docstring canaries (Anthony Loke/DAP/WEALTH/Parliament/Malaysia/September/PETRONAS/The/Unity Government) all OK.

## LIVE VERIFICATION (post-restart)
| claim | principal | verdict | violations |
|---|---|---|---|
| "LLMs cannot understand Malay nuance and idiom." | SYSTEM | PASS | [] |
| "Arif feels betrayed by the decision." | PERSON | 888_HOLD | RASA_GATE_888_HOLD |

## SHA-256
| file | before | after |
|---|---|---|
| hermes_mcp/_perspective.py | 7cf93f70… | 56cf8869… |
| mcp/hermes-rasa/principal_type_classifier.py | 227a82c8… | 6b1160df… |

## AFFECTED SERVICES
- `hermes-mcp-server.service` — restarted (active), picks up both files.

## ROLLBACK (exact)
```bash
git -C /root/HERMES checkout -- hermes_mcp/_perspective.py mcp/hermes-rasa/principal_type_classifier.py
rm /root/HERMES/hermes_mcp/test_entity_type_regression.py
systemctl restart hermes-mcp-server.service
```

## UNKNOWN / OPEN
- Changes are **uncommitted** (working tree). Commit not performed — per directive "return measured status only, do not seal on test-pass".
- `CL-03 fires on {PERSON, UNDEFINED}` (F6 conservative) is UNCHANGED — unknown model tokens still route conservatively; that's the F13 design question flagged in the APEX-ZEN model, not part of this bounded patch.
- `_PERSONS` is not exhaustive of all federation humans — full person registry should come from canonical source (people.yaml / USER.md).

## NOT SEALED
Measured status only. Finality (commit + VAULT999) awaits sovereign "sah".
