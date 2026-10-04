#!/usr/bin/env bash
# skill-mesh-probe.sh — Pattern #7 (skill mesh SOT) probe
#
# Reads every SKILL.md across AAA / Hermes / Kimi trees, parses the
# declared `version:` field, and classifies each skill as SYNC /
# DIVERGED / MISSING_FROM_X. Prints the "are my agents in sync right now?"
# summary line and a per-skill table.
#
# PITFALL: the skill directories nest one level deeper on this mesh
# (`/root/AAA/skills/<skill>/SKILL.md`), so the spec'd `-maxdepth 1`
# returns zero rows. We use `-maxdepth 2` here as the operational variant.
# The `AUDIT-agent-skill-mesh` SKILL.md documents both.
#
# Usage:
#   ./skill-mesh-probe.sh           # one-shot probe
#   ./skill-mesh-probe.sh --json    # machine-readable output
#   ./skill-mesh-probe.sh --help
#
# Exit codes:
#   0 = full SYNC across all three trees
#   1 = DIVERGED or MISSING present (verify and remediate via AUDIT-agent-skill-mesh)
#   2 = probe itself failed (e.g. trees missing)

set -u

AAADIR="/root/AAA/skills"
HERDIR="/root/.hermes/skills"
KIMDIR="/root/.kimi-code/skills"

usage() {
    cat <<EOF
skill-mesh-probe.sh — Pattern #7 (skill mesh SOT) probe

Reads SKILL.md across:
  AAA:    $AAADIR
  Hermes: $HERDIR
  Kimi:   $KIMDIR

Usage:
  $0 [options]

Options:
  --json   Emit JSONL: one line per skill (machine-readable)
  --help   Show this message

Exit codes:
  0  All present skills are SYNC
  1  ≥1 DIVERGED or MISSING (see AUDIT-agent-skill-mesh for escalation)
  2  Probe failed (missing trees, permission denied, etc.)
EOF
}

case "${1:-}" in
    --help|-h) usage; exit 0 ;;
    --json)    JSON=1 ;;
    "")        JSON=0 ;;
    *)         echo "Unknown arg: $1" >&2; usage; exit 2 ;;
esac

# Sanity: all three trees must exist
for d in "$AAADIR" "$HERDIR" "$KIMDIR"; do
    [ -d "$d" ] || { echo "FAIL: missing tree $d" >&2; exit 2; }
done

# Helper: extract version (or UNPARSEABLE) from a SKILL.md
version_of() {
    local f="$1"
    local v
    v=$(grep -E '^version:' "$f" 2>/dev/null | head -1 | sed -E 's/^version:[[:space:]]*//; s/^["'\''"]//; s/["'\''"]$//')
    if [ -z "$v" ]; then
        echo "NO_VERSION"
    elif [ "$v" = "semver" ] || [ "$v" = "{semver}" ]; then
        echo "UNPARSEABLE"
    else
        echo "$v"
    fi
}

# Build a 3-column map: skill_name|aaa_version|hermes_version|kimi_version
declare -A AAA_V HER_V KIM_V
ALL_SKILLS=()

add_skill() {
    local tree="$1" path="$2"
    local name
    name=$(basename "$(dirname "$path")")
    case "$tree" in
        AAA)    AAA_V["$name"]="$(version_of "$path")" ;;
        Hermes) HER_V["$name"]="$(version_of "$path")" ;;
        Kimi)   KIM_V["$name"]="$(version_of "$path")" ;;
    esac
    # Add to skill list if not already present
    case " ${ALL_SKILLS[*]:-} " in
        *" $name "*) ;;
        *) ALL_SKILLS+=("$name") ;;
    esac
}

while IFS= read -r f; do add_skill AAA "$f"; done < <(find "$AAADIR" -maxdepth 2 -name 'SKILL.md' 2>/dev/null)
while IFS= read -r f; do add_skill Hermes "$f"; done < <(find "$HERDIR" -maxdepth 2 -name 'SKILL.md' 2>/dev/null)
while IFS= read -r f; do add_skill Kimi "$f"; done < <(find "$KIMDIR" -maxdepth 2 -name 'SKILL.md' 2>/dev/null)

# Sort
IFS=$'\n' SORTED=($(printf '%s\n' "${ALL_SKILLS[@]:-}" | sort))
unset IFS
ALL_SKILLS=("${SORTED[@]}")

# Classify
SYNC=0
DIVERGED=0
MISSING=0
UNPARSEABLE=0

classify() {
    local name="$1"
    local a="${AAA_V[$name]:-—}" h="${HER_V[$name]:-—}" k="${KIM_V[$name]:-—}"
    local status="SYNC"
    local reasons=()

    # Build the list of declared versions (skip —)
    local have=()
    [ "$a" != "—" ] && have+=("$a")
    [ "$h" != "—" ] && have+=("$h")
    [ "$k" != "—" ] && have+=("$k")

    # Detect presence
    local aa=0 hh=0 kk=0
    [ "$a" != "—" ] && aa=1
    [ "$h" != "—" ] && hh=1
    [ "$k" != "—" ] && kk=1

    # MISSING
    local missing=()
    [ $aa -eq 0 ] && missing+=("MISSING_FROM_aaa")
    [ $hh -eq 0 ] && missing+=("MISSING_FROM_hermes")
    [ $kk -eq 0 ] && missing+=("MISSING_FROM_kimi")

    # UNPARSEABLE
    local unparse=()
    [ "$a" = "UNPARSEABLE" ] && unparse+=("AAA")
    [ "$h" = "UNPARSEABLE" ] && unparse+=("hermes")
    [ "$k" = "UNPARSEABLE" ] && unparse+=("kimi")

    # DIVERGED
    local diverged=0
    if [ "${#have[@]}" -ge 2 ]; then
        local first="${have[0]}"
        for v in "${have[@]}"; do
            if [ "$v" != "$first" ]; then diverged=1; break; fi
        done
    fi

    # Compose status (priority: UNPARSEABLE > DIVERGED > MISSING > SYNC)
    if [ "${#unparse[@]}" -gt 0 ]; then
        status="UNPARSEABLE(${unparse[*]})"
        UNPARSEABLE=$((UNPARSEABLE+1))
    elif [ $diverged -eq 1 ]; then
        status="DIVERGED"
        DIVERGED=$((DIVERGED+1))
    elif [ "${#missing[@]}" -gt 0 ]; then
        status=$(IFS=','; echo "${missing[*]}")
        MISSING=$((MISSING+1))
    else
        SYNC=$((SYNC+1))
    fi

    if [ "${JSON:-0}" = "1" ]; then
        # JSONL: one line per skill
        printf '{"skill":"%s","aaa":"%s","hermes":"%s","kimi":"%s","status":"%s"}\n' \
            "$name" "$a" "$h" "$k" "$status"
    else
        printf "%-32s | %-12s | %-12s | %-12s | %s\n" "$name" "$a" "$h" "$k" "$status"
    fi
}

# Emit
if [ "${JSON:-0}" != "1" ]; then
    printf "%-32s | %-12s | %-12s | %-12s | %s\n" "skill_name" "AAA_version" "hermes_version" "kimi_version" "status"
    printf -- "-%.0s" $(seq 1 88); echo
fi

for s in "${ALL_SKILLS[@]}"; do
    classify "$s"
done

if [ "${JSON:-0}" != "1" ]; then
    echo
    TOTAL=$((SYNC + DIVERGED + MISSING + UNPARSEABLE))
    echo "=== summary ==="
    echo "Total:  $TOTAL"
    echo "SYNC:   $SYNC"
    echo "DIVERGED: $DIVERGED"
    echo "MISSING:  $MISSING (one row per MISSING_FROM_X)"
    echo "UNPARSEABLE: $UNPARSEABLE"
    echo
    echo "Verdict: $SYNC sync, $DIVERGED diverged, $MISSING missing, $UNPARSEABLE unparseable."
fi

# Exit code
if [ $DIVERGED -gt 0 ] || [ $MISSING -gt 0 ] || [ $UNPARSEABLE -gt 0 ]; then
    exit 1
fi
exit 0
