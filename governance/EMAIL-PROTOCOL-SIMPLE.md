# Email Protocol — arifOS Federation
# v2.0 — Forged 2026-09-07
# One rule: Arif cakap hantar, Hermes hantar. Receipt masuk vault. Done.

---

## Satu Undang-Undang

Kau cakap hantar, aku hantar. Receipt masuk vault. Done.

## Dua Laluuan

**Email dari kau** → direct send. No gate. No approval. Surat kanan, alamat kanan, cop terus.

**Email dari agent (bukan kau)** → governance layer wujud untuk agent tu, bukan untuk kau.

## Yang Kau Tak Perlu Fikir

- Backend (Brevo/APA/IMAP) — urusan infra
- Intent builder — aku handle
- Role ACL — agent punya hal
- Approval flow — kau bukan agent
- SMTP vs API — kau cakap "email Syed", aku faham

## Infra Yang Hidup

| Komponen | Status |
|---|---|
| Brevo SMTP/API | LIVE — :18093 |
| Gmail IMAP | 🔲 Tunggu app password |
| Inbox triage | 🔲 Tunggu IMAP |
| Cron brief | 🔲 Phase 2 |

## Receipt

Setiap email keluar → SHA256 hash + timestamp masuk vault. Kau tak pernah minta. Aku tak pernah skip.

## Tambah Contact

Kau cakap nama, aku simpan alamat. Sekali je.

```
"Email Syed" → syed.khairuddin@...
"Email Trescon" → info@tresconglobal.com
```

---

DITEMPA BUKAN DIBERI ⚒️
