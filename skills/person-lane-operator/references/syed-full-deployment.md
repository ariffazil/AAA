# Syed Lane — Worked Deployment Reference

> Concrete example of wiring a person-lane from scratch (Aug 7, 2026).
> Updated: 2026-08-07 after second pass (formal letters, blood test, casual support).

## Identity

| Field | Value |
|---|---|
| Person | Syed Khairuddin Morktarudin (aka Abang Sado) |
| TG | @rico_ricaldo_33 · ID 1042200555 |
| IC | 850905-14-6217 |
| Domain | XAUUSD trading + sambal brand + mak caregiver + tenancy + casual life |
| Voice register | BM Pasar, masculine, direct |
| Operator | Arif (TG 267378578) |

## Dossier path

`/root/sado/identity/SYED-DOSSIER.md` — single source-of-truth.

## 7-layer wiring results

| Layer | What | Result |
|---|---|---|
| L1/L2 Redis | `user:syed:*` keys | 5 keys (identity, mak, trading, brand, last_seen) |
| L3 Qdrant | bge-m3 embeddings (1024d) | 4 points, collection `arifos_memory`, subject filter |
| L4 PG `memory_store` | tier + entity_tags | 4 rows (identity, medical, trading, brand) |
| L5 FalkorDB | `sado_knowledge` graph | 4 nodes (Person ×2, Brand, Dashboard) + 3 edges |
| L6 VAULT999 | memory_seal event | chain_hash `776553183aa192d9` linked to prev entry |
| L7 F1–F13 | 3rd party = advisory only | No autonomous actions, F13 sovereignty = Arif |

## Cron jobs created

| Job ID | Name | Schedule |
|---|---|---|
| `5d87405c1770` | syed-mak-dressing | 0 8 * * * |
| `a5b0eda31bfa` | syed-mak-cbd-followup | 0 9 * * 1 |
| `0f07d72c0673` | syed-gerd-log | 0 8 * * * |
| `cf1c6b534b2f` | syed-sambal-preorder | 30 6 * * * |

## Files created

| Path | Purpose |
|---|---|
| `/root/sado/identity/SYED-DOSSIER.md` | Master reference |
| `/root/sado/mak-health/TIMELINE.md` | Rosnani medical state |
| `/root/sado/mak-health/SYMPTOMS.md` | Health symptoms log |
| `/root/sado/brand/README.md` | Sambal brand assets |
| `/root/sado/trading/README.md` | XAUUSD system |
| `/root/sado/telegram/GROUP-CONTEXT.md` | SADO group rules |
| `/root/sado/references/letters/SURAT-AIRCOND.pdf` | AC replacement letter (final) |
| `/root/sado/references/letters/SURAT-AIRCOND.docx` | AC replacement letter (editable) |
| `/root/sado/references/SURAT-PLUS-1-LANDLORD.md` | Plus-1 occupancy template |
| `MEMORY-syed.md` | Memory lane |
| `USER-syed.md` | User profile |
| `SOUL-syed.md` | Voice register (BM Pasar) |
| `lane-syed.json` | Lane config |
| `lane_switch_syed.py` | Auto-detect hook |

## Pitfalls discovered (updated 2026-08-07)

1. **Dashboard vs human confusion** — "Abang Sado" was originally Arif's dashboard name, but Syed is the real person the dashboard was named AFTER. Confusion arose because memory said "Abang Sado = dashboard" when Arif said "Abang Sado = manusia betul la." → Always ask: human, dashboard, or callsign?

2. **Family member misidentification** — confusing ayah (Mama Salleh, cerai) with adik (Khairuddin, no contribution). Each family member gets one line in dossier.

3. **"gerd" vs GERD** — Syed typed "aku gerd lah" (Malay for "aku geram/frustrated" OR medical GERD). Context resolved it — he was reporting a condition, not expressing emotion. → Watch for loanword ambiguity in BM.

4. **Wrong-name-on-transfer-letter** — ROSNANI appeared on a hospital diagnostic letter but was the wrong name. Patient's actual name not yet confirmed. → Always verify IC/nama on every medical document.

5. **A33A-30 Neu Suites is Syed's unit** — memory initially recorded this as Arif's address. Syed is the tenant (IC 850905-14-6217), Jeremy Toh is landlord. → Don't copy operator address to person dossier without verifying tenancy agreement.

6. **"TPUM" shorthand** — Syed used "TPUM" (Tanya Pasal Umah) and "plus 1 abaiakan" (ignore plus 1). The lane must recognize Malaysian slang abbreviations and route to the right fixture without asking for clarification. "TPUM" → load tenant-status fixture. "plus 1" → occupancy consent discussion.

7. **"Battery 100% health" claim contradicted by screen** — Syed said health was 100% but the actual screenshot showed "Battery Health & Charging: Unverified" + "Low Power Mode: ON." The UNVERIFIED status means non-genuine battery was likely installed at some point. Always verify against the screenshot, not just the verbal report.

8. **Blood test interpretation requires FULL context** — when interpreting a lab report, load the SUBJECT's medical context (TRT protocol, supplements, conditions) AND the SENDER's context (who sent the report). A testosterone of 5.31 for a TRT user means something different than for a natural user. Missing tests (ferritin, DHT, vitamin D, T3/T4) are the highest-value insight — name them explicitly.

9. **"Unverified" battery = scam replacement** — "Battery Health & Charging: Unverified" on iPhone means the battery was replaced with a non-genuine unit (likely a cheap third-party shop). The persona needs to visit Apple Authorized for a genuine replacement (~RM359). DO NOT suggest software tweaks — the battery is fundamentally not genuine.

10. **Scam call spoofing** — numbers like 017-620 7613 appearing to call from "Maybank" are VoIP-spoofed scam calls. Bank never asks for OTP/password over phone. Report to SKMM (aduan.skmm.gov.my), block the number, install Truecaller/Whoscall.

11. **Glutathione + hair loss = indirect** — glutathione doesn't directly cause hair loss, but injectables can trigger telogen effluvium via hormonal shifts or nutrient depletion. Blood test context (DHT pending, FSH/LH low from TRT) is the more likely cause. Always cross-reference supplement questions with the person's medical data.
