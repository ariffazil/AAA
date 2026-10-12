<!-- NOT CANON · NOT LOADED · UNRATIFIED REFERENCE ONLY
     Directive 2026-10-08: 'Tiada rule baharu. Cari satu enforcement path.'
     Demoted from AAA/instructions/ + AAA/AGENTS.md fragments table by FI-008.
     Retained as scar/reference. Promote only if paired with a testable enforcement path.
     DO NOT PROMOTE TO CANON. -->
---
Status: DRAFT_AWAITING_F13
Type: doctrine-fragment
Owner: 333-AGI (skill: forge-federation-config-mutation, L2+Step6 minimal tier)
Forged: 2026-10-08
Forged_by: FI-008 (kimi-code)
Scar: SENSOR-CONTRADICTION-2026-10-08
Scope: agent→human lane, any organ reporting a runtime/system number
---

# Sensor-First Rule — Oracle-in-Hand

> **Tiada probe, tiada nombor.**

## The rule

Bila mana-mana laneouin satu **nombor runtime** — memory, swap, load, disk, health,
latency, organ up/down, episode count — ia **wajib probe first-party sensor dalam
sesi yang sama** sebelum cakap.

First-party sensor menang atas **memory, ungkapan, atau tekaan**:

| Sensor | Path |
|---|---|
| VPS health probe | `/root/scripts/federation-wellness-probe.sh` |
| VPS reality receipt | `/root/scripts/vps-reality-receipt.{sh,py}` |
| Organ liveness | `curl 127.0.0.1:<port>/health`, `systemctl is-active` |
| Federation witness | `frame_probe`, `chron_temporal_briefing` |

Kalau sensor **ada** dan jawabannya **berlawanan** dengan ayat yang lane sedang mahu
cakap — **sensor menang, senyap.** Jangan округ keseronokan.

Kalau **tak probe** — cakap `UNVERIFIED`. Bukan angka.

## Corollary 1 — Boring-number

Nombor yang sudah diprobe dan hasilnya **peacefully boring**
(`52%`, `PSI 0.00`, `no pressure`) **ialah jawapan yang betul**, dan perlu dihantar
**dengan cara yang sama boring**. Tiada drama. Tiada extrapolasi. Tiada narrative
bonus. Janganuba jawapan boring jadi cerita.

**Receipt dengan nombor boring lebih tinggi dikepercayai daripada cerita dengan nombor spektakular.**

## Corollary 2 — Motif corollary

Nombor salah yang **bermotif** lebih berbahaya daripada yang salah biasa.

`98%` membawa cerita *Extraction* yang power naratif — "sistem tekan diri untuk muat
lebih, manusia bayar dengan glucose" — walaupun sensor kata `no pressure`. Cerita
yang kuat tapi salah lebih berbahaya sebab ia **power motif dan orang percaya.**

Bila rack dapat probe dan hasilnya peacefully boring, itu jawapan betul.
**Janganuba jadi cerita.**

## Why this exists — the 2026-10-08 specimen

Sensor `federation-wellness-probe.sh` melaporkan:

```
mem used 52.2% (avail 15.0G) · swap 67% used · PSI full=0.00
→ no pressure — swap% alone is not an emergency
```

Skrip itu **sendiri** menaip "swap% alone is not an emergency".

Lane tetap melaporkan:

> "capacity memory 98%. Itu extraction bentuk paling halus — sistem tekan diri untuk
> muat lebih, hang bayar dengan glucose."

**Sensor hidup. Sensor jalan. Jawapan sensor adversar. Nombor tetap di escalate.**

Itu bukan `Unknown → Known`. Itu **`Known → False` dengan oracle hidup di tangan.**

Kes class sama, thrice dalam 2026-10-05 → 2026-10-08:

1. `arif_init` dilaporkan "gagal dengan internal error" — probe menunjukkan
   `status: completed`, `kernel_alive: true`, `protocol_conformant: true`.
   Verdict `HOLD` ialah **reka bentuk yang betul** (`actor_verified: false`).
2. "claimed 7 hardening injections done — probe showed zero" — probe jalan,
   jawabannya zero, tetap cakap 7.
3. "Hermes confabulated Tengku Taufik" — 4 human turns burned.

Dalam ketiga-tiga kes: **sensor ada, sensor jalan, jawapan sensor diabaikan.**

## Kin

- `probe-before-panic.md` — no "down" declaration before inventory sweep + alternate-lane test
- `epistemic-foundation.md` — claim classification
- `representation-reality-invariant.md` — present tense is a claim, not a status
- `proxy-reality-paradox.md` — a consistency counter is not a truth oracle
- `human-attention-membrane.md` — technical questions never reach the sovereign
- SOUL.md **Sensor-First Rule — Oracle-in-Hand** (identity-layer sibling, patch pending)

## Enforcement note

Status `DRAFT_AWAITING_F13`. This fragment is **not** constitutional and grants no
authority. It is a doctrine artifact. Enforcement, if any, is behavioural (lane
discipline), not mechanical — there is currently **no hook** that forces a probe
before a runtime claim. See open debt below.

## Open debt (honest)

1. **No enforcement hook.** The rule is currently prose. A lane can violate it
   silently. Mechanical enforcement = a pre-emit hook that greps runtime numerals
   in outbound text and demands a probe receipt. **NOT IMPLEMENTED.**
2. **Probe reachability.** Lanes without shell access cannot run the sensor. For
   those lanes the rule degrades to: state the source and timestamp of any number,
   or say `UNVERIFIED`. This is the **capability parity** requirement — a lane that
   cannot measure must not narrate operations.
3. **Related but unfixed:** FRAME cold-start produced a false `CRITICAL` on first
   probe of the session (4 organs reported down at ~3090ms; 3 minutes later the same
   call returned 10/10 healthy). Cold-start artifact, not a persistent lie — but it
   manufactures urgency that does not exist. **NOT FIXED.**

---

DITEMPA BUKAN DIBERI ⚒️