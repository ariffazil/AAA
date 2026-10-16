# Verdict Map — seven seals → QRL-4

One rule: **a mapping may only keep or lower authority. Never map upward.**

| Raw kernel verdict | QRL-4 mapping | Condition |
|---|---|---|
| SEAL | SEAL | Only if returned by arif_judge in THIS run, raw string in record |
| PROVISIONAL | SABAR | With conditions recorded |
| PARTIAL | SABAR | With conditions recorded |
| SABAR | SABAR | Direct |
| HOLD | HOLD | Direct |
| HOLD_888 | HOLD | Escalated — flag for F13 |
| VOID | VOID | Direct |
| (unknown token) | HOLD | reason_code: unknown_verdict_token |
| (no verdict / kernel unreachable) | NONE | Stop before ACT |

Canonical vocabulary conflict (open F13 ruling, 14 Okt 2026): README says four
(SEAL/HOLD/SABAR/VOID); models/verdicts.py defines seven. Until ruled, the raw
string is truth and this table does the translation. After ruling, update this
file in ONE place, no skill rewrite.
