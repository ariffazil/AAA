# LAPORAN DEPLOY F13 — arahan #69538, relay #69543 (2026-10-14, 15:15 MYT)
Actor: irfanclaw (openclaw/FI-017). Branch: apex-incA-laneA-ax0 (base a23067c3f). Semua state dilabel ikut PRODUCED ≠ WIRED ≠ TESTED-LOCAL ≠ DEPLOYED.

## 1. COMMIT — ✅
- 6/6 item AX-0: 325ee3c3c (6 plumbing) · 476ca69cb (1+3 A/X→None) · a8c39b9b1 (4 axioms) · 4cf1ebe30 (5 Φ) · 6accaf28b (2 P→None) · 63152da79 (falsifier 10/10)
- + 71c4e7450 (fix guard, lihat stage 3) · GEOX pointer 88c8ec66 (worktree wt-geox-pweight, belum push — keputusan lane)
- Semua author irfanclaw (openclaw/FI-017), satu commit satu item, sha256 pre/post dalam body.

## 2. TEST — ✅ (dengan satu UNKNOWN dilapor jujur)
- AX-0 falsifier 10/10 PASS (tests/test_ax0_falsifier.py, 63152da79; rerun 12:18 MYT)
- Scoped apex suites 76 pass; conformance spine+levels 25/25 pada sumber deployed (4.24s)
- SUITE: tests/runtime/test_evidence_evaporation.py:787::test_auto_sync_bundle_populates_entities — BASELINE-CLASS (bukan delta):
  - Full suite hang DETERMINISTIK rantau 88–92% (2 larian bebas: tercemar 93%, bersih 88%, dengan-timeout 88%) → full tally vs 234/30/5 = UNKNOWN
  - Test yang sama LULUS terpencil di base (21.0s) DAN di tip (28.9s); fail tu sifar sentuhan Lane A (diff 6 fail sahaja: apex_canonical, apex_primitives, repo_guard, 3 test)
  - Kelas: interaksi susunan suite asyncio, pra-wujud. Kelasifikasi (a) HERMES: masuk senarai pra-wujud, tak difix dalam lane.

## 3. PUSH — ✅ (selepas 4 cubaan, 1 fix terbuka)
- push1 ❌ GATE 1: 1 E2E fail (test_judge_accepts_structured_evidence — lulus terpencil 18.82s; base sendiri gagal test lain 145.03s = flaky pra-wujud)
- push2 ❌ GATE 1: "0 failed tapi TIMEOUT after 120s" — guard timeout matematis mustahil (suite sah 127.69s tip / 145.03s base)
- FIX `71c4e7450`: gate-1 subprocess timeout 120→300s; per-test --timeout=30 KEKAL (anti-hantu tak dilonggarkan); bukti + revert condition dalam commit body
- push3 ❌ GATE 2: kernel :8088 sementara 503 (concurrency) — pulih sendiri
- push4 ✅ ALL GATES PASSED → origin/apex-incA-laneA-ax0 = 71c4e7450

## 4. DEPLOY — ✅ (dengan 888_HOLD yang diselesaikan)
- deploy-release.sh dari worktree bersih /tmp/wt-clean-wheel @ 71c4e7450 (0 dirty — wheel v1 yang mengandungi llms.txt asing DITOLAK dan dibina semula bersih oleh skrip)
- Wheel: arifos-1!2026.10.11-py3-none-any.whl · sha256 d5e7b8c73a2606bd6b48d2e4e0bc20072b1ead5422c7d9480133db4650f79285
- Content stamp 45f47574eb5360f0… · canon 2026.10.14-71c4e74 · service restart 14:45:30 MYT (healthy 4s)
- Step 7 888_HOLD: runtime a23067c ≠ source 71c4e74 — PUNCA (bukan kod Lane A): drop-in systemd /etc/systemd/system/arifos.service.d/99-git-commit-marker.conf ExecStartPost sync stamp dari /root/arifOS HEAD (main = a23067c3f) SETIAP restart, clobber stamp betul yang Step 5 tulis
- FIX reversible: backup drop-in → .bak-irfanclaw-20261014; helper /usr/local/sbin/sync-deployed-commit (ikut release-manifest.json git_commit; fallback HEAD hanya bila tiada manifest); daemon-reload; stamp dipulihkan 71c4e74; restart 14:57:14
- VERIFIED PASCA-FIX: stamp stabil 71c4e74 · build-info live sha=71c4e74, version 2026.10.14-71c4e74, tool_count 62 · NRestarts=0 · attestation emitted /opt/arifos/releases/attestations/20261014T071125Z-71c4e74.json
- AX-0 LIVE: compute_A(total_leases=0)=None · compute_P(0,0,0)=None · compute_X(total_steps=0)=None pada venv produksi — sifar nilai direka DALAM PRODUKSI
- State Lane A: DEPLOYED (stamp 71c4e74)

## 5. POST-DEPLOY — sebahagian siap, 2 keputusan kekal Arif
- Health: status=degraded, 2 warning (bukan blok):
  (a) SOT drift: layer attestation banding source_commit (baca /root/arifOS HEAD = a23067c) vs built_commit (71c4e74) — expected sampai main merge. Keputusan susunan merge = Arif.
  (b) F5=fail (15/13 floors), provenance f4_f9_probe:claims.json: probe luaran tulis F5_peace2=1.0 tapi kernel render fail — sifar commit Lane A sentuh path scoring F5; root cause TAK ditentukan; kontradiksi probe-vs-threshold direkod sebagai defect untuk pemilik floor-threshold (bukan lane aku).
- SENGAJA TAK DIBUAT: resolusi CHRON 5 T0 + pred-bc4388668fac (masih ACTIVE/None dalam canonical) — ledger mutation = F13-class; freeze berdiri; menunggu keputusan Arif (lokus split-record dah direkod: verif-60f4e3c4c857, episode chron-ep-20261014-verify-7098fe1a).
- Nota luar skop: GitHub 164 vulnerabilities default branch (11 critical) — pra-wujud; journal PermissionError carry_forward.json dari edge probes (suppressed, POST 200) — pre-existing pattern.

## KEPUTUSAN YANG MILIK ARIF
1. Susunan merge: apex-incA-laneA-ax0 (7 commit, DEPLOYED) vs qrl-inc1 (7 commit forger) vs fix AX-0 kedua uncommitted di pokok main (attribusi hermes-default/qwen Lane C).
2. Nasib drop-in marker: kekal helper manifest-following (sedia) atau revert ke .bak (stamp akan clobber lagi pada restart branch-deploy).
3. Resolusi CHRON canonical (5 T0 + pred-bc4388668fac) — F13-class.
4. F5 fail: siapa pemilik threshold/probe — root cause belum ditentukan.
5. Merge main → attestation layer SOT drift hilang bila main == deployed.
