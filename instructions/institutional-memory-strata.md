# Institutional Memory Strata — Memory Lives in Governed Artifacts

> **Status:** F13_RATIFIED_CHAT (2026-09-11)
> **Origin:** External repo analysis (github.com/ariffazil/{AAA,arifos,A-FORGE}) + Arif's synthesis: *"di mana memory sebenarnya hidup?"* Corrections applied after live probe (F2 — witnessed, bukan narrated).
> **⚠️ AUDIT 2026-09-11 ~12:3x MYT:** Label F2 di atas **tidak disokong probe** untuk Correction #1 asal. Live probe selepas itu falsify claim tersebut; Correction #1 kini dibetulkan dengan evidence (W1–W4). Lihat `/root/AAA/reports/memory-strata-mem0-contradiction-audit-2026-09-11.md`. Jangan percaya label epistemic tanpa probe yang menghasilkan ayat itu.
> **Companion:** `memory-promotion-gate.md` (WHEN memory write dibenarkan) → doktrin ini (WHERE memory hidup).
> **Applies to:** ALL agents in arifOS federation.

---

## The Thesis

```text
Memory should not live in the model.
Memory should live in governed artifacts.
```

Ini **institutional memory**, bukan model memory. Model = mangkin (catalyst), bukan takung (container). Repos federation = Externalized Cognitive Substrate.

## The Four Strata (dinamakan oleh apa yang membunuhnya)

| Stratum | Isi | Mati bila | Mod |
|---|---|---|---|
| **S0 Context Memory** | Context window | Session habis | Chat |
| **S1 Repository Memory** | SOUL.md, AGENTS.md, IDENTITY, DOCTRINE, skills, receipts, `carry_forward.json` | Repo dipadam | **Reconstruction** |
| **S2 Witness Memory** | VAULT999, ledgers, seals | Tidak — immutable | **Attestation** |
| **S3 Semantic Recall** | `arif_memory` L1–L6 / `forge_memory` atas Qdrant (live) | Vector store dipadam | **Recall** |

```text
Loaded identity (S1) ≠ Remembered identity (S3)
```

Blank slate pada empty clone adalah EXPECTED. Fix = substrate, bukan model.

**Axis note:** Ini paksi *substrate-persistence* — jangan campur dengan `MEMORY_ENGINEERING_SPEC_v2` functional Layers 1–5 atau L1–L6 operational tiers. Tiga paksi berbeza.

## Resit bukan memori (2026-09-27)

Strata di atas memberitahu di mana sesuatu disimpan. Ia tidak menukar resit menjadi memori.

```text
Receipt    = bukti sejarah
Memory     = perubahan tingkah laku yang dipelihara
Scar       = akibat yang dimampatkan
Constraint = parut yang dikuatkuasa
```

Resit yang duduk di S1 atau S2 kekal bukti. Ia menjadi memori hanya bila ia mengubah tindakan seterusnya. Kalau tidak, ia arkib yang kebetulan tersimpan dalam substrat memori. Trust membenarkan semakan yang sudah disaksikan diguna semula selagi saksi masih segar. Trust bukan cache, dan trust bukan bukti sifar-pengetahuan.

## Witnessed Corrections (live probe 2026-09-11)

Claim luaran yang SALAH terhadap kanon sendiri:

1. **`"Hermes semantic recall = arif_memory only"`** — SALAH. *(CORRECTED 2026-09-11 ~12:3x MYT — pembetulan F2 selepas live probe; claim asal di bawah ternyata Registry menyamar sebagai Witness.)*
   - **Witnessed 2026-09-11:** `/root/.hermes/config.yaml` L33-34 → `memory: provider: mem0` (live provider line, bukan remnant). Ketika itu Qdrant `mem0` = 11,277 points dan `arifos_memory` = 99. Read + write path exercised in-session: 4× `mem0_search` (score 0.72–0.87) + **8× `mem0_delete` semua success**. Remnant tidak boleh terima write.
   - **Disemak semula 2026-09-27T00:32:19Z:** `mem0` = 14,507 points. `arifos_memory` = 1,196 points. Kedua-dua stor masih hidup. Angka 11,277 dan 99 di atas adalah sejarah.
   - **Mem0 ialah S3 backend Hermes yang HIDUP.** `ARCHITECTURE_BLUEPRINT_3NODE.md` rejection (*"middleman on a deeper stack"*) = **intent (Registry)**, bukan **runtime (Witness)**. Gap antara dua itu = unbuilt work, bukan settled fact.
   - **Evidence:** `/root/AAA/reports/memory-strata-mem0-contradiction-audit-2026-09-11.md` (W1–W4).
   - **Falsifiable dalam 2 command:** `grep -A2 '^memory:' /root/.hermes/config.yaml` · `curl -s 127.0.0.1:6333/collections/mem0 | grep -o '"points_count":[0-9]*'`
2. **"Claude/Kimi/Codex tiada carry-forward"** — SALAH. `carry_forward.json` = convention federation, ditulis closing agent tak kira harness (witnessed: modified hari ini). Tetapi ia S1 reconstruction, bukan S3 recall — point asal survive, label salah.

**Dua stor, satu peraturan (2026-09-27):** `mem0` (Hermes, 14,507 points) dan `arifos_memory` (1,196 points) masih dua stor selari. Ejen menamakan stor yang dia baca. Jangan gabungkan keduanya dalam ayat. Jangan panggil salah satu daripadanya sebagai satu-satunya memori. Menggabungkan backend ialah perubahan arah, dan ia belum diperintahkan.

**Meta-lesson (scar, bukan cerita):** Claim #1 asalnya di-ratify dengan label *"applied after live probe (F2 — witnessed, bukan narrated)"* padahal probe tidak pernah dijalankan terhadapnya. **Label F2 yang tidak disokong probe lebih bahaya daripada Registry yang jujur — sebab ia membawa baju Witness.** Ujian: jangan terima label epistemic; tanya *"probe mana yang hasilkan ayat ini?"*

## Corrected Harness Matrix

```text
Semua agent federation:      S0 + S1 + S2
S3 semantic recall:          terbuka kepada SEMUA agent MCP-wired
                             (Claude/OpenCode/Kimi witnessed wired ke arifos+aforge)
```

Beza Hermes vs coding agents = **akses DAN reflex default** *(dibetulkan 2026-09-11: asalnya claim "bukan akses" — itu derived dari premis salah bahawa Mem0 rejected; lihat Correction #1)*:
- **Akses:** Hermes ada S3 sendiri yang hidup (`mem0`, 14,507 points pada 2026-09-27T00:32:19Z). Coding agents wired ke `arif_memory` / `forge_memory` (`arifos_memory` 1,196 points, masa yang sama). Dua stor. Nama stor yang dibaca.
- **Reflex:** Hermes recall by design (gateway routing melalui memory). Coding agents reconstruct by default (murah, deterministic); recall atas demand.
- **Implikasi:** beza Hermes dan ejen kod ialah akses dan reflex, bukan satu stor yang sama. Menggabungkan backend belum diperintahkan.

```text
Hermes remembers.
Coding agents reconstruct — dan boleh recall bila route melalui arif_memory.
Nothing rediscovers — selagi substrate hidup.
```

## The Harness-Swap Substrate Test (falsifiable)

```text
Tukar: Claude → Kimi → GPT → Grok → OpenCode
```

- Capability yang TERUS HIDUP selepas swap → ia hidup di S1/S2 (substrate).
- Capability yang MATI selepas swap → ia cuma S0 narrative — bukan institution.

Ini test, bukan crisis. Harness swap ialah cara mengukur apa yang benar-benar dipunyai federation.

## Operational Binding

- Lulus Memory Promotion Gate → pilih **stratum sasaran**: governed artifact (S1/S2). Never model-only.
- Jangan claim "agent ini ingat" tanpa nyatakan stratum — ingat di S1 (reconstruct) ≠ ingat di S3 (recall).
- S1 artifacts mesti kekal render-able + greppable (reconstruction = baca semula; kalau tak jumpa, tak ingat).
- Coding agents: sebelum kata "tiada memory" — probe S3 dulu (`forge_memory` recall). Fail-closed termasuk terhadap claim ketiadaan sendiri.

## Compression

> **Model = mangkin. Substrate = memory. Swap model untuk uji apa yang sebenar.**

DITEMPA BUKAN DIBERI ⚒️
