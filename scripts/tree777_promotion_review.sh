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
LOG_FILE="${WIKI_ROOT}/log.md"
STAMP_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DAY_UTC="$(date -u +%Y-%m-%d)"
OUT_FILE="${RUNTIME_DIR}/tree777-promotion-review-${AGENT}-${DAY_UTC}.json"

mkdir -p "${RUNTIME_DIR}"

python3 - <<'PY' "${WIKI_ROOT}" "${OUT_FILE}" "${AGENT}" "${STAMP_UTC}"
import json
import re
import sys
from pathlib import Path

wiki = Path(sys.argv[1])
out_file = Path(sys.argv[2])
agent = sys.argv[3]
timestamp = sys.argv[4]

frontmatter_re = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
status_re = re.compile(r"^status:\s*(.+?)\s*$", re.MULTILINE)

targets = []
for section in ("skills", "concepts", "scars", "workflows"):
    d = wiki / section
    if not d.exists():
        continue
    for f in d.rglob("*.md"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        m = frontmatter_re.match(text)
        if not m:
            continue
        fm = m.group(1)
        sm = status_re.search(fm)
        status = sm.group(1).strip().lower() if sm else None
        if status == "proposed":
            targets.append({
                "path": str(f.relative_to(wiki)),
                "section": section,
                "status": status,
            })

report = {
    "report_type": "TREE777_888_PROMOTION_REVIEW",
    "agent": agent,
    "timestamp_utc": timestamp,
    "proposed_total": len(targets),
    "by_section": {
        "skills": sum(1 for t in targets if t["section"] == "skills"),
        "concepts": sum(1 for t in targets if t["section"] == "concepts"),
        "scars": sum(1 for t in targets if t["section"] == "scars"),
        "workflows": sum(1 for t in targets if t["section"] == "workflows"),
    },
    "proposed_pages": targets[:300],
    "recommended_next_step": "Route proposed pages through 888_JUDGE review and promote evidence-backed patterns only.",
}

out_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report))
PY

cat >> "${LOG_FILE}" <<EOF

## [${DAY_UTC}] review | TREE777 888 promotion review (${AGENT})

- **Who:** cron:${AGENT}
- **Scope:** proposed page review for 888 promotion queue
- **Report:** \`wiki/_runtime/reports/$(basename "${OUT_FILE}")\`
- **When:** ${STAMP_UTC}

---
EOF

echo "TREE777 888 promotion review complete for ${AGENT}: ${OUT_FILE}"
