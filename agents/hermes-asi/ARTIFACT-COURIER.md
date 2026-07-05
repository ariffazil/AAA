# ARTIFACT-COURIER.md — Hermes Artifact Delivery Contract

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
> **Forged:** 2026-07-05 by FORGE (000Ω) under F13 SOVEREIGN directive
> **Status:** ACTIVE — courier pipeline tested and verified

---

## The Problem This Solves

Files get created in places Arif can't reach. Agents say "file at /tmp/report.pdf" without ensuring Arif can actually access it from his phone, desktop, or any device. The path is meaningless without a delivery route.

## The Architecture

```
[opencode / SSH / VPS]
    | creates file
    | computes sha256
    | stores in governed outbox
    v
[Hermes Artifact Courier]
    | validates file exists
    | checks size, MIME type
    | sends to Telegram
    | logs delivery
    v
[Telegram]
    | ARIF downloads
    v
[Local machine — phone / desktop]
```

**Kernel rule:**
```
opencode builds. Hermes delivers. Telegram surfaces. VPS preserves. Hash governs. Base64 only rescues.
```

## Canonical Paths

| What | Path |
|------|------|
| Outbox root | `/var/arifos/artifacts/outbox/` |
| Daily outbox | `/var/arifos/artifacts/outbox/YYYY-MM-DD/` |
| Delivery log | `/var/arifos/artifacts/logs/deliveries.jsonl` |
| Courier script | `/root/.hermes/scripts/artifact-courier.sh` |
| Receipt (per artifact) | `<artifact_path>.receipt.json` |

## Courier Script Usage

```bash
# Deliver a file to Arif's Telegram
/root/.hermes/scripts/artifact-courier.sh /path/to/file.pdf --caption "SKG09 audit report"

# Dry run (validate + hash, no Telegram send)
/root/.hermes/scripts/artifact-courier.sh /tmp/report.csv --dry-run

# Deliver with custom chat ID
/root/.hermes/scripts/artifact-courier.sh /tmp/data.json --chat-id 267378578

# Remove source after successful delivery (DANGEROUS — not default)
/root/.hermes/scripts/artifact-courier.sh /tmp/scratch.txt --no-keep-source
```

## Receipt Schema

Every delivery produces a `.receipt.json` alongside the artifact:

```json
{
  "artifact_id": "report_2026-07-05",
  "filename": "report.pdf",
  "content_type": "application/pdf",
  "byte_length": 14336,
  "sha256": "abc123...",
  "created_at": "2026-07-05T17:43:00Z",
  "source_path": "/tmp/report.pdf",
  "delivered_path": "/var/arifos/artifacts/outbox/2026-07-05/report.pdf",
  "delivery": {
    "status": "delivered",
    "primary": "hermes_telegram",
    "chat_id": "267378578",
    "telegram_message_id": "82906",
    "error": null
  },
  "source_retained": true,
  "courier_version": "1.0.0",
  "forged_by": "FORGE-000Omega",
  "sovereign": "ARIF-F13"
}
```

## Hermes Courier Command

When Hermes receives `/deliver <path>` or an agent calls the courier:

1. Validate file exists
2. Compute SHA256 hash
3. Detect MIME type + file size
4. Stage to canonical outbox (copy, not move)
5. Send file + receipt caption to Telegram
6. Write `.receipt.json` alongside artifact
7. Log delivery to `deliveries.jsonl`
8. Return structured receipt

## Transport Hierarchy

| Priority | Method | When |
|----------|--------|------|
| 1 | Hermes → Telegram | Default. Small/medium files. Arif needs quick access. |
| 2 | SCP / rsync | Large files. Arif is in terminal. Telegram unnecessary. |
| 3 | Signed download link | Future. Large files. Browser download. Temporary URL. |
| 4 | Content-addressed (CID) | Future. Constitutional evidence. Large reproducible outputs. |
| 5 | Base64 | Emergency only. No UI, no Telegram, no SCP. Text channel only. |

## Floor Alignment

| Floor | Obligation |
|-------|-----------|
| F1 AMANAH | Source retained by default. Delivery is copy, not move. Reversible. |
| F2 TRUTH | SHA256 hash is truth anchor. Receipt contains hash. No hash = no delivery. |
| F4 CLARITY | One canonical outbox. No random folders. No "file at /tmp". |
| F7 HUMILITY | Receipt declares what it is and what it isn't. No overclaiming. |
| F11 AUDIT | Every delivery logged. Receipt is audit trail. Log is append-only. |
| F13 SOVEREIGN | Delivery targets Arif only. No third-party delivery. Arif's chat ID is default. |

## Anti-Patterns

- ❌ Agent says "file at /tmp/report.pdf" without delivering it
- ❌ Agent uses random folders (`~/report.pdf`, `./output.pdf`)
- ❌ Agent sends Base64 when file delivery is possible
- ❌ Agent removes source without explicit `--no-keep-source`
- ❌ Agent claims delivery without receipt
- ❌ Agent delivers to third-party chat without F13 ack

## OpenCode Integration

OpenCode agents should follow this pattern when producing deliverables:

```bash
# 1. Generate file
opencode generates /tmp/report.pdf

# 2. Save to canonical outbox (or let courier copy it)
cp /tmp/report.pdf /var/arifos/artifacts/outbox/$(date +%Y-%m-%d)/

# 3. Call courier
/root/.hermes/scripts/artifact-courier.sh /tmp/report.pdf --caption "Report title"

# 4. Print final receipt
echo "Artifact created and delivered."
echo "SHA256: <from receipt>"
echo "Delivered: Telegram via Hermes"
echo "Source retained: yes"
```

---

*Forged: 2026-07-05 by FORGE (000Ω) under F13 SOVEREIGN directive*
*DITEMPA BUKAN DIBERI*
