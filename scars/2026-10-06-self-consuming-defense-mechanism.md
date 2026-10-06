Status: FILED (F13-named scar-seed, 2026-10-06 chat)
# SCAR — Self-Consuming Defense Mechanism (defense yang makan dirinya sendiri)

**Named by:** F13 SOVEREIGN (chat 2026-10-06, "Akar bukan sensing. Bukan logging. Akar = dedup. System yang dibuat untuk lindung manusia dari noise, sorok signal")
**Class:** protection-inversion · **w_scar: 0.8** (proposed; final weight per scar-weight registry process)
**Detection:** a defense mechanism with no decay/escalation term inverts — the protector becomes the blind spot.

## Specimen 1 — NATS dedup (2026-09-20 → 2026-10-06)
22,208 firings of P1 `arifos.floor.breach` suppressed to invisibility by the dedup layer built to protect human attention from noise. The alarm never stopped; the *visibility* of the alarm died. 16 days, zero inspections. Root: false-positive probe + dedup-without-age-escalation.
Receipt: `/root/AAA/reports/surface-guard-p1-inspection-2026-10-06.md`

## Specimen 2 — systemd ProtectSystem=full (2026-09-15 → 2026-10-06)
The sandbox protection on the arifos unit **silently blacklisted the scar_events file write** — the federation's own memory-writing was eaten by its own hardening for 21 days ("event file kering sejak 15 Sep bukan kerana tiada parut — kerana tulisannya gagal secara senyap", session 2026-10-06 02:16 UTC). Same class, different subsystem: the shield blocked the wound-report.

## The invariant (extracted, now in canon v1.1)
> **Every defense mechanism must carry an escalation-on-age term. Suppression without escalation = deletion.** Applies to: alert dedup, sandbox allow/deny lists, rate limits, permission gates, ignore-files. Any mechanism whose purpose is noise-reduction must be auditable for signal-loss: "what has this shield eaten, and how old is it?"

**Cheapest probe (any lane):** list suppressed/blocked items older than N days; if any is >7d with no inspection receipt, this scar fired.

**Anti-fossilization:** this scar constrains *defense mechanisms*, not action selection — it may not be used to justify removing protections, only to require their age-escalation and auditability.
