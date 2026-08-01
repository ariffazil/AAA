# Nine-Signal Overview

> **CLAIM** | Source: `observability/nine_signal_alerts.yml` + `arifos.init` | **Confidence:** 0.95 | **Epoch:** 2026-04-23

## Summary

Nine-Signal is arifOS's observability framework — nine metrics that collectively determine the health, governance state, and epistemic quality of a running agent session.

---

## The Nine Signals

| Signal | Domain | What it Measures |
|--------|--------|------------------|
| **Delta (dS)** | Entropy | Change in system uncertainty — dS < 0 = increasing order |
| **Psi (Ψ)** | Grounding | How well claims map to physical/observable reality |
| **Omega (Ω)** | Confidence | Agent's self-reported confidence in current verdict |
| **Kappa (κ)** | Consistency | Cross-session consistency of claims |
| **Kappa_r** | Resilience | System-level resilience under component failure |
| **Floor drift** | Governance | Deviation from constitutional floor baseline |
| **Plane drift** | Geography | Deviation from spatial/geological expectation |
| **F3 consensus** | Tri-witness | Human + AI + Earth alignment score |
| **F9 anti-hantu** | Ethics | Dark pattern / manipulation detection score |

---

## Alert Thresholds

From `observability/prometheus/nine_signal_alerts.yml`:

| Signal | Alert | Threshold |
|--------|-------|-----------|
| delta | NineSignalDelta | < -0.15 or > 0.20 |
| omega | NineSignalOmega | < 0.10 (false certainty) or > 0.97 (overconfidence) |
| psi | NineSignalPsi | < 0.20 |
| kappa_r | NineSignalKappaR | < 0.10 |
| floor_drift | NineSignalFloorDrift | > 2 floors deviation |
| f3_consensus | NineSignalF3Consensus | < 0.50 |
| f9_antihantu | NineSignalF9AntiHantu | > 0.80 (high manipulation potential) |

---

## F9 Anti-Hantu — False Certainty Detection

**Critical rule:** Omega (Ω) suspiciously low (< 0.10) is a false certainty signal — the agent is claiming high confidence while ground truth is uncertain. This triggers `NineSignalFalseCertainty` alert.

---

## Prometheus Scraping

- arifOS-MCP: `http://localhost:8080/metrics/json` (15s)
- arifOS-API: `http://localhost:8000/api/status` (30s)
- GEOX: `http://localhost:8081/metrics` (30s)
- OpenClaw: `:18789/metrics` (30s)

---

## Cross-References

- [[arifos/FLOORS]] — F9 anti-hantu is signal #9
- [[arifos/888_JUDGE]] — 888_JUDGE checks Nine-Signal before issuing SEAL
- [[infrastructure/OBSERVABILITY]] — Prometheus + Grafana stack setup

---

## Status

**Stable** — Nine-Signal framework is fully defined with Prometheus alerting rules.

---

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE