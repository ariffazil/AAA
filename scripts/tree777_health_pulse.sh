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
OUT_FILE="${RUNTIME_DIR}/tree777-health-${AGENT}-${DAY_UTC}.json"

mkdir -p "${RUNTIME_DIR}"

python3 - <<'PY' "${WIKI_ROOT}" "${OUT_FILE}" "${AGENT}" "${STAMP_UTC}"
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

wiki = Path(sys.argv[1])
out_file = Path(sys.argv[2])
agent = sys.argv[3]
timestamp = sys.argv[4]

md_files = [p for p in wiki.rglob("*.md") if p.is_file()]
total_files = [p for p in wiki.rglob("*") if p.is_file()]
now = datetime.now(timezone.utc)

def age_days(path: Path) -> int:
    dt = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return int((now - dt).total_seconds() // 86400)

fresh_1d = sum(1 for p in md_files if age_days(p) <= 1)
fresh_3d = sum(1 for p in md_files if age_days(p) <= 3)
fresh_7d = sum(1 for p in md_files if age_days(p) <= 7)

slug_to_file = {}
for f in md_files:
    slug_to_file[f.stem.lower()] = f

wikilink_re = re.compile(r"\[\[([^\]]+)\]\]")
all_outbound = {}
for f in md_files:
    text = f.read_text(encoding="utf-8", errors="ignore")
    links = []
    for m in wikilink_re.finditer(text):
        target = m.group(1).split("|")[0].strip().lower()
        target = target.replace(".md", "")
        if target:
            links.append(target)
    all_outbound[f] = links

inbound_count = {f: 0 for f in md_files}
for _, links in all_outbound.items():
    for slug in links:
        target = slug_to_file.get(slug)
        if target:
            inbound_count[target] += 1

orphans = sorted(
    [str(f.relative_to(wiki)) for f, c in inbound_count.items() if c == 0 and f.name not in {"index.md", "SCHEMA.md", "log.md"}]
)[:200]

report = {
    "report_type": "TREE777_777_HEALTH_PULSE",
    "agent": agent,
    "timestamp_utc": timestamp,
    "wiki_root": str(wiki),
    "counts": {
        "total_files": len(total_files),
        "markdown_files": len(md_files),
        "skills": len([p for p in (wiki / "skills").rglob("*.md")]) if (wiki / "skills").exists() else 0,
        "workflows": len([p for p in (wiki / "workflows").rglob("*.md")]) if (wiki / "workflows").exists() else 0,
        "concepts": len([p for p in (wiki / "concepts").rglob("*.md")]) if (wiki / "concepts").exists() else 0,
        "scars": len([p for p in (wiki / "scars").rglob("*.md")]) if (wiki / "scars").exists() else 0,
        "entities": len([p for p in (wiki / "entities").rglob("*.md")]) if (wiki / "entities").exists() else 0,
    },
    "freshness": {
        "updated_le_1d": fresh_1d,
        "updated_le_3d": fresh_3d,
        "updated_le_7d": fresh_7d,
    },
    "orphan_links": {
        "count": len(orphans),
        "sample": orphans,
    },
}

out_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report))
PY

cat >> "${LOG_FILE}" <<EOF

## [${DAY_UTC}] update | TREE777 777 health pulse (${AGENT})

- **Who:** cron:${AGENT}
- **Scope:** 777 health pulse (counts, freshness, orphan links)
- **Report:** \`wiki/_runtime/reports/$(basename "${OUT_FILE}")\`
- **When:** ${STAMP_UTC}

---
EOF

echo "TREE777 777 pulse complete for ${AGENT}: ${OUT_FILE}"
