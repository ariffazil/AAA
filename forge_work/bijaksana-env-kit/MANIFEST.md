# BIJAKSANA ENV KIT v1 — KVM8 → KVM4 → KVM2

Apa benda ni (satu ayat): Kit yang buat terminal mana-mana node nampak realiti mesin
sendiri — satu kad `reality`, satu probe fail `fileprobe`, prompt yang tunjuk lokasi,
sejarah bertarikh, dan seatbelt rm — semua idempotent, boleh undur, ber-resit.

## Isi
- reality-card.sh        — kad realiti 12 baris (organs, writers, secrets-count, canon hash)
- fileprobe.sh           — probe jujur satu fail (safety: UNKNOWN|CLEAR|HOLD, tak pernah "safe")
- bashrc-bijaksana.block — blok .bashrc bertanda (v1.2) — untuk SHELL MANUSIA sahaja
- bijaksana-env-install.sh — pemasang idempotent (backup + syntax gate + auto-revert + resit)
- deploy-node.sh         — arahan satu baris: probe → ship → install → verify

## Pasang pada node
    bash deploy-node.sh root@100.64.0.5   # KVM4 (kvm4-forge)
    bash deploy-node.sh root@100.64.0.4   # KVM2 (azwaos)

## Undur pada node
    ssh <node> 'cp /root/.bashrc.bak.<ts> /root/.bashrc'
    ssh <node> 'rm -f /usr/local/bin/reality /usr/local/bin/fileprobe'

## Perkara yang NODE LAIN mungkin beza (periksa dulu, jangan anggap)
1. VAULT999 append-only (+a) dasar — jika wujud di node lain, apex-zen-compact akan beku sama.
2. Timers dengan `Timezone=` — systemd abaikan; jadual lari UTC sedangkan penulis fikir MYT.
3. Port 18789 (openclaw bridge) — KVM4 port ni mati walaupun peer alive.
4. /root/bin mungkin tiada dalam PATH node — sebab itu kit pasang symlink /usr/local/bin.

DITEMPA BUKAN DIBERI · receipts KVM8: /root/AAA/receipts/bijaksana-env.jsonl
