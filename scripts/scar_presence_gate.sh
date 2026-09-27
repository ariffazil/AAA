#!/usr/bin/env bash
# scar_presence_gate.sh — F2 TRUTH + F11 AUDIT pre-commit gate
# Blocks commits that remove constitutional scar terms from SOUL.md
# Canonical: /root/AAA/scripts/scar_presence_gate.sh
# Installed as: /root/.hermes/.git/hooks/pre-commit
set -euo pipefail

SOUL="/root/.hermes/SOUL.md"

# Only gate SOUL.md changes — skip if SOUL.md not in staging area
if ! git diff --cached --name-only | grep -qFx "SOUL.md"; then
	exit 0
fi

# Required scar-anchored terms that MUST survive any SOUL.md rewrite
# Format: "exact grep term|label"
REQUIRED_TERMS=(
	"SCAR-2026-09-04-001|PROBE-FIRST-DOCTRINE"
	"SCAR-2026-09-19-TEMPORAL|MANDAAT-TEMPORAL"
	"SCAR-2026-09-24-001|KALIBRASI-PERBUALAN"
	"SCAR-2026-09-24-002|KAWAN-BUKAN-PENJAGA"
	"State-Transition Discipline|TRANSITION-DISCIPLINE"
	"Confidence ≠ Authority|AUTHORITY-ENVELOPE"
	"KAWAN, BUKAN PENJAGA|KAWAN-REGISTER"
)

MISSING=()
for entry in "${REQUIRED_TERMS[@]}"; do
	term="${entry%%|*}"
	label="${entry##*|}"
	if ! grep -qF "$term" "$SOUL" 2>/dev/null; then
		MISSING+=("$label ($term)")
	fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
	echo "╔══════════════════════════════════════════════════════════╗"
	echo "║  SCAR PRESENCE GATE — BLOCKED                           ║"
	echo "╠══════════════════════════════════════════════════════════╣"
	echo "║  Required constitutional scars missing from SOUL.md:    ║"
	for m in "${MISSING[@]}"; do
		printf "║  - %-52s ║\n" "$m"
	done
	echo "╠══════════════════════════════════════════════════════════╣"
	echo "║  Gate: /root/AAA/scripts/scar_presence_gate.sh          ║"
	echo "║  F2 TRUTH: scars are constitutional memory — never      ║"
	echo "║  deleted by edit; only promoted/replaced by F13 seal.   ║"
	echo "╚══════════════════════════════════════════════════════════╝"
	exit 1
fi

exit 0
