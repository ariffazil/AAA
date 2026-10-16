# DECISION RECORD — 5 KONFLIK MEMORI (Phase 0 rulings)
Status: DIRATIFKAN OLEH ARIF (chat "Ok", 14 Okt 2026) · berdasarkan audit "Human Reality and Memory Architecture for AAA and arifOS" (doc_ac05fae6e479) + hand-audit snapshot /root/arifOS/CURRENT_VERIFIED_STATE.md (2026-10-11)
Scope: decision record sahaja — tiada kod ditukar, tiada canon baru. Rulings ini mengikat kerja coding yang menyentuh memor, health surface, dan memory substrate mulai 14 Okt 2026.
Precedence: hand-audit 2026-10-11 > self-reported health, sampai sebaliknya dibuktikan dengan independent witness.

---

## C1 — Quorum tulisan memory
**Konflik:** Kontrak lama kata store succeed jika ≥1 leg succeed; failure matrix pulang menjadikan Qdrant failure fatal. Dua durabiliti guarantee, dua kepercayaan penulis.
**RULING:** Satu atomic write quorum sahaja — ditakrifkan dalam kod, dibekalkan sebagai policy yang dijana (code-generated), bukan prose. Policy mesti nyatakan: primary store, secondary store, dan apa yang berlaku pada bila-bila satu mati. Sebelum ruling ini dilaksanakan, anggap: **tulisan memory gagal = fail seluruhnya (fail-closed), bukan partial success.**

## C2 — Graphiti status
**Konflik:** Graphiti dilabel L5 memory layer dalam kontrak, tetapi runtime laporkan disabled/degraded/retired.
**RULING:** Graphiti = `EXPERIMENTAL/DERIVED` di semua surface, berkuat kuasa serta-merta. **Tak boleh jadi source of truth**, tak boleh jadi authority untuk apa-apa keputusan, sampai live conformance test membuktikan sebaliknya. Semua dokumentasi yang label Graphiti sebagai layer operasional mesti dibetulkan bila disentuh — bukan sweep besar-besaran, betul on-touch.

## C3 — Forget/prune disabled (MENDESAK)
**Konflik:** Forget/prune didokumen sebagai fungsi governed, tetapi enforcement sengaja dimatikan menunggu F13 flow. UI boleh janji padam bila substrate tak padam.
**RULING:** **Tiada permukaan manapun boleh mengaku "deleted" tanpa resit substrate.** Semua delete response mesti pulangkan `DELETION_PENDING` atau `SUPPRESSION_ACTIVE` — bukan `deleted`. Deletion theatre adalah defect kelas pertama (lihat risiko purge 2026-10-14: 416MB dipadam tanpa sweep vector/index/backup = deletion pending, bukan deletion done). Enforcement forget kekal disabled, dan status disabled itu mesti terpapar kepada pengguna, bukan disembunyi.

## C4 — Health tanpa as_of (MENDESAK, disahkan hidup)
**Konflik:** Health surface boleh laporkan floor hijau sementara hand-audit 2026-10-11 laporkan fail/unmeasured. Disahkan live 14 Okt: AAA /health tiada `as_of` field; G self-reported 0.875 vs live session 0.43 — dua deria tak setuju.
**RULING:** Setiap health assertion mesti bawa: `as_of` (timestamp ukuran), `evidence_scope` (siapa ukur: self-probe / hand-audit / independent witness), `population`, dan `precedence` (hand-audit > self-report). Sebelum field-field ni wujud: **apa-apa health claim yang bercanggah dengan CURRENT_VERIFIED_STATE.md ialah UNRESOLVED, dan yang lebih konservatif menang.** Self-reported hijau tidak menolak hand-audit merah.

## C5 — SEAL identity/verdict collision
**Konflik:** A-FORGE docs kata execution follows SEAL; audit laporkan action-class/budget gating dan verdict/identity label collision. Executor boleh silap authorization dengan authentication.
**RULING:** **Recursive improvement kekal observe/propose mode** (888 HOLD, disahkan) sampai: (a) actor verification end-to-end terbukti (actor → signature → session → action hash), (b) verdict/authorization/execution/approval tak boleh berbeza antara sinks, (c) identity tidak boleh di-derive dari verdict string — SEMUA empat ditutup dengan bukti witnessed, bukan self-attestation. Setiap kolum verdict mesti dirujuk semula kepada actor identity yang berasingan; dua field yang sama nilai tak bermaksud sama semantik.

---

## Exit gate tunggal (dari dokumen, diratifikasi)
Satu transaksi end-to-end yang externally replayable membuktikan: actor → memory proposal → judgment → write → read → correction → deletion/suppression → receipts. Sebelum exit tu: ruling C1–C5 memerintah; selepas exit: semak semula.

**Invariant pemerintah:** Memory may inform intelligence. Memory may constrain authority. Memory must never manufacture consent, identity, or sovereignty.
