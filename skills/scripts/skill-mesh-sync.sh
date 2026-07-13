#!/usr/bin/env bash
# skill-mesh-sync.sh — rebind CLI harness skill views to AAA + .agents catalog
# Usage:
#   skill-mesh-sync.sh              # dry-run (default)
#   skill-mesh-sync.sh --apply      # create missing symlinks
#   skill-mesh-sync.sh --check      # exit 1 if drift/broken links
#
# Canon: AAA/skills + .agents/skills. Harnesses are views.
# Does NOT delete harness-native skills. Does NOT touch Hermes/Kimi trees.
set -euo pipefail

MODE="${1:---dry-run}"
AAA="${AAA_SKILLS:-/root/AAA/skills}"
AGENTS="${AGENTS_SKILLS:-/root/.agents/skills}"
CODEX_PROFILE="${CODEX_SKILL_PROFILE:-/root/AAA/skills/CODEX_SKILL_PROFILE.json}"
OPENCODE_PROFILE="${OPENCODE_SKILL_PROFILE:-/root/AAA/skills/OPENCODE_SKILL_PROFILE.json}"
HARNESSES=(
  "${GROK_SKILLS:-/root/.grok/skills}"
  "${CLAUDE_SKILLS:-/root/.claude/skills}"
  "${CODEX_SKILLS:-/root/.codex/skills}"
  "${OPENCODE_SKILLS:-/root/.arifos/agents/opencode/skills}"
)

# Names that must remain real dirs on Grok (not force-overwritten)
GROK_NATIVE_KEEP=(
  arif-governed-autonomous-execution
  grok-zen-aaa-substrate
  grok-federation-skill-upgrader
  orthogonal-skill-update
  create-skill
  check-work
  help
  imagine
)

SKIP_DIRS='^(substrate|knowledge|warga|runtime|reflective|fastmcp|scripts|knowledge|\.|\.\.|compile\.py|validate\.py|.*\.(yaml|yml|json|md|sha256))$'

is_native_keep() {
  local name="$1" h="$2"
  [[ "$(basename "$h")" == "skills" && "$h" == *".grok"* ]] || return 1
  for k in "${GROK_NATIVE_KEEP[@]}"; do
    [[ "$name" == "$k" ]] && return 0
  done
  return 1
}

declare -A CODEX_KEEP=()
if [[ -f "$CODEX_PROFILE" ]]; then
  while IFS= read -r name; do
    [[ -n "$name" ]] && CODEX_KEEP[$name]=1
  done < <(python3 -c 'import json,sys; print("\n".join(x["name"] for x in json.load(open(sys.argv[1]))["skills"]))' "$CODEX_PROFILE")
fi

declare -A OPENCODE_KEEP=()
if [[ -f "$OPENCODE_PROFILE" ]]; then
  while IFS= read -r name; do
    [[ -n "$name" ]] && OPENCODE_KEEP[$name]=1
  done < <(python3 -c 'import json,sys; print("\n".join(x["name"] for x in json.load(open(sys.argv[1]))["skills"]))' "$OPENCODE_PROFILE")
fi

is_codex_harness() {
  [[ "$1" == *"/.codex/skills" ]]
}

codex_keeps() {
  [[ -n "${CODEX_KEEP[$1]:-}" ]]
}

is_opencode_harness() {
  [[ "$1" == *"/opencode/skills" ]]
}

profile_active() {
  (is_codex_harness "$1" && [[ ${#CODEX_KEEP[@]} -gt 0 ]]) ||
    (is_opencode_harness "$1" && [[ ${#OPENCODE_KEEP[@]} -gt 0 ]])
}

profile_keeps() {
  local h="$1" name="$2"
  if is_codex_harness "$h"; then
    [[ -n "${CODEX_KEEP[$name]:-}" ]]
  elif is_opencode_harness "$h"; then
    [[ -n "${OPENCODE_KEEP[$name]:-}" ]]
  else
    return 0
  fi
}

collect_sources() {
  # print: name|abs_path for every skill body
  local root home
  for home in aaa agents; do
    if [[ "$home" == aaa ]]; then root="$AAA"; else root="$AGENTS"; fi
    [[ -d "$root" ]] || continue
    # top-level
    for p in "$root"/*; do
      [[ -e "$p" ]] || continue
      local base; base="$(basename "$p")"
      [[ "$base" =~ $SKIP_DIRS ]] && continue
      if [[ -d "$p" && ( -f "$p/SKILL.md" || -L "$p" ) ]]; then
        # only real skill bodies (prefer real dirs over pure link-out for source)
        if [[ -f "$p/SKILL.md" ]]; then
          echo "${base}|$(readlink -f "$p" 2>/dev/null || echo "$p")"
        elif [[ -L "$p" && -f "$(readlink -f "$p")/SKILL.md" ]]; then
          echo "${base}|$(readlink -f "$p")"
        fi
      fi
    done
    # substrate / knowledge nested
    for nest in substrate knowledge; do
      [[ -d "$root/$nest" ]] || continue
      for p in "$root/$nest"/*; do
        [[ -d "$p" && -f "$p/SKILL.md" ]] || continue
        echo "$(basename "$p")|$(readlink -f "$p")"
      done
    done
  done
}

declare -A BEST=()
# Prefer AAA path over agents when both exist
while IFS='|' read -r name path; do
  [[ -z "$name" || -z "$path" ]] && continue
  if [[ -z "${BEST[$name]:-}" ]]; then
    BEST[$name]="$path"
  else
    # keep existing if already AAA
    if [[ "${BEST[$name]}" == "$AAA"* ]]; then
      :
    elif [[ "$path" == "$AAA"* ]]; then
      BEST[$name]="$path"
    fi
  fi
done < <(collect_sources | sort -u)

missing=0
broken=0
created=0
ok=0

echo "skill-mesh-sync mode=$MODE sources=${#BEST[@]} $(date -u +%Y-%m-%dT%H:%M:%SZ)"

for h in "${HARNESSES[@]}"; do
  [[ -d "$h" ]] || { echo "SKIP missing harness $h"; continue; }
  echo "--- harness $h"
  if profile_active "$h"; then
    archive="$h/.profile-archive"
    for entry in "$h"/*; do
      [[ -e "$entry" || -L "$entry" ]] || continue
      name="$(basename "$entry")"
      if ! profile_keeps "$h" "$name"; then
        if is_codex_harness "$h" && [[ ! -L "$entry" ]]; then
          continue
        fi
        echo "EXTRA $entry (not in harness profile)"
        if [[ "$MODE" == "--apply" ]]; then
          mkdir -p "$archive"
          rm -f "$archive/$name"
          mv "$entry" "$archive/$name"
          echo "  ARCHIVED $name"
          created=$((created+1))
        else
          missing=$((missing+1))
        fi
      fi
    done
  fi
  # broken links first
  for link in "$h"/*; do
    [[ -L "$link" ]] || continue
    if [[ ! -e "$link" ]]; then
      echo "BROKEN $link -> $(readlink "$link")"
      broken=$((broken+1))
      if [[ "$MODE" == "--apply" ]]; then
        name="$(basename "$link")"
        if [[ -n "${BEST[$name]:-}" ]]; then
          rm -f "$link"
          ln -s "${BEST[$name]}" "$link"
          echo "  REFIXED $name -> ${BEST[$name]}"
          created=$((created+1))
          broken=$((broken-1))
        fi
      fi
    fi
  done

  for name in "${!BEST[@]}"; do
    if profile_active "$h" && ! profile_keeps "$h" "$name"; then
      continue
    fi
    target="${BEST[$name]}"
    dest="$h/$name"
    if is_native_keep "$name" "$h"; then
      continue
    fi
    if [[ -L "$dest" ]]; then
      cur="$(readlink -f "$dest" 2>/dev/null || true)"
      if [[ "$cur" == "$target" ]]; then
        ok=$((ok+1))
      else
        echo "DRIFT $dest -> $cur (want $target)"
        if [[ "$MODE" == "--apply" ]]; then
          rm -f "$dest"
          ln -s "$target" "$dest"
          echo "  RELINKED $name"
          created=$((created+1))
        else
          missing=$((missing+1))
        fi
      fi
    elif [[ -d "$dest" ]]; then
      # real dir: leave (harness-local or vendored)
      ok=$((ok+1))
    else
      echo "MISSING $dest (would link -> $target)"
      if [[ "$MODE" == "--apply" ]]; then
        ln -s "$target" "$dest"
        echo "  LINKED $name"
        created=$((created+1))
      else
        missing=$((missing+1))
      fi
    fi
  done
done

echo "summary ok≈$ok missing_or_drift=$missing broken=$broken created=$created"

if [[ "$MODE" == "--check" ]]; then
  if [[ $missing -gt 0 || $broken -gt 0 ]]; then
    exit 1
  fi
fi
exit 0
