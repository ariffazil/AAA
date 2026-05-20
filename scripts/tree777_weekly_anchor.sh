#!/usr/bin/env bash
set -euo pipefail

AGENT=""
for arg in "$@"; do
  case "$arg" in
    --agent=*) AGENT="${arg#*=}" ;;
  esac
done

if [[ -z "${AGENT}" ]]; then
  echo "Usage: $0 --agent=<agent-name>" >&2
  exit 1
fi

WIKI_ROOT="/root/AAA/wiki"
RUNTIME_DIR="${WIKI_ROOT}/_runtime/reports"
ANCHOR_DIR="/root/AAA/VAULT999/tree777"
LOG_FILE="${WIKI_ROOT}/log.md"
STAMP_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DAY_UTC="$(date -u +%Y-%m-%d)"

mkdir -p "${RUNTIME_DIR}" "${ANCHOR_DIR}"

HEALTH_FILE="$(ls -1t "${RUNTIME_DIR}/tree777-health-${AGENT}-"*.json 2>/dev/null | head -n 1 || true)"
PROMO_FILE="$(ls -1t "${RUNTIME_DIR}/tree777-promotion-review-${AGENT}-"*.json 2>/dev/null | head -n 1 || true)"
OUT_FILE="${RUNTIME_DIR}/tree777-weekly-anchor-${AGENT}-${DAY_UTC}.json"

python3 - <<'PY' "${OUT_FILE}" "${AGENT}" "${STAMP_UTC}" "${HEALTH_FILE}" "${PROMO_FILE}"
import hashlib
import json
import sys
from pathlib import Path

out_file = Path(sys.argv[1])
agent = sys.argv[2]
timestamp = sys.argv[3]
health_path = Path(sys.argv[4]) if sys.argv[4] else None
promo_path = Path(sys.argv[5]) if sys.argv[5] else None

health = None
promo = None
if health_path and health_path.exists():
    health = json.loads(health_path.read_text(encoding="utf-8"))
if promo_path and promo_path.exists():
    promo = json.loads(promo_path.read_text(encoding="utf-8"))

payload = {
    "report_type": "TREE777_999_WEEKLY_ANCHOR",
    "agent": agent,
    "timestamp_utc": timestamp,
    "inputs": {
        "health_report": str(health_path) if health_path else None,
        "promotion_review_report": str(promo_path) if promo_path else None,
    },
    "summary": {
        "markdown_files": (health or {}).get("counts", {}).get("markdown_files"),
        "orphan_links": (health or {}).get("orphan_links", {}).get("count"),
        "proposed_total": (promo or {}).get("proposed_total"),
    },
}
digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
payload["anchor_receipt"] = f"TREE777-999-{agent}-{digest[:16]}"
payload["anchor_hash"] = digest
payload["status"] = "SEALED_LOCAL_LEDGER"

out_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(json.dumps(payload))
PY

cat "${OUT_FILE}" >> "${ANCHOR_DIR}/tree777_anchors.jsonl"
echo "" >> "${ANCHOR_DIR}/tree777_anchors.jsonl"

RECEIPT="$(python3 - <<'PY' "${OUT_FILE}"
import json,sys
print(json.load(open(sys.argv[1], encoding="utf-8"))["anchor_receipt"])
PY
)"

cat >> "${LOG_FILE}" <<EOF

## [${DAY_UTC}] seal | TREE777 999 weekly anchor (${AGENT})

- **Who:** cron:${AGENT}
- **Scope:** weekly TREE777 growth anchor
- **Anchor report:** \`wiki/_runtime/reports/$(basename "${OUT_FILE}")\`
- **Anchor receipt:** \`${RECEIPT}\`
- **Ledger:** \`VAULT999/tree777/tree777_anchors.jsonl\`
- **When:** ${STAMP_UTC}

---
EOF

echo "TREE777 999 weekly anchor complete for ${AGENT}: ${OUT_FILE}"
