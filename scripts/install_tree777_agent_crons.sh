#!/usr/bin/env bash
set -euo pipefail

ROOT="/root/AAA"
AGENTS_DIR="${ROOT}/agents"
START="# >>> TREE777_AGENT_LOOPS >>>"
END="# <<< TREE777_AGENT_LOOPS <<<"

if [[ ! -d "${AGENTS_DIR}" ]]; then
  echo "Missing agents dir: ${AGENTS_DIR}" >&2
  exit 1
fi

mapfile -t AGENTS < <(find "${AGENTS_DIR}" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)
if [[ ! " ${AGENTS[*]} " =~ " phoenix72 " ]]; then
  AGENTS+=("phoenix72")
fi

TMP="$(mktemp)"
{
  echo "${START}"
  echo "CRON_TZ=Asia/Kuala_Lumpur"
  echo "SHELL=/bin/bash"
  echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
  echo ""

  idx=0
  for agent in "${AGENTS[@]}"; do
    m1=$(( (idx * 7) % 60 ))
    m2=$(( (idx * 7 + 2) % 60 ))
    m3=$(( (idx * 7 + 4) % 60 ))
    h1=$(( 7 + (idx % 3) ))   # daily stagger 07-09
    h2=$(( 10 + (idx % 3) ))  # Tue/Fri stagger 10-12
    h3=$(( 13 + (idx % 3) ))  # Sunday stagger 13-15

    echo "# Agent: ${agent}"
    echo "${m1} ${h1} * * * ${ROOT}/scripts/tree777_health_pulse.sh --agent=${agent} >> ${ROOT}/wiki/_runtime/cron-${agent}.log 2>&1"
    echo "${m2} ${h2} * * 2,5 ${ROOT}/scripts/tree777_promotion_review.sh --agent=${agent} >> ${ROOT}/wiki/_runtime/cron-${agent}.log 2>&1"
    echo "${m3} ${h3} * * 0 ${ROOT}/scripts/tree777_weekly_anchor.sh --agent=${agent} >> ${ROOT}/wiki/_runtime/cron-${agent}.log 2>&1"
    echo ""
    idx=$((idx+1))
  done

  echo "${END}"
} > "${TMP}"

CURRENT="$(mktemp)"
crontab -l 2>/dev/null > "${CURRENT}" || true

awk -v s="${START}" -v e="${END}" '
  BEGIN{skip=0}
  $0==s {skip=1; next}
  $0==e {skip=0; next}
  skip==0 {print}
' "${CURRENT}" > "${CURRENT}.clean"

cat "${CURRENT}.clean" "${TMP}" | awk 'NF || !blank {print} {blank = (NF==0)}' > "${CURRENT}.new"
crontab "${CURRENT}.new"

echo "Installed TREE777 cron block for agents:"
printf ' - %s\n' "${AGENTS[@]}"

echo "Current TREE777 block:"
awk -v s="${START}" -v e="${END}" '
  $0==s{show=1}
  show{print}
  $0==e{show=0}
' "${CURRENT}.new"

rm -f "${TMP}" "${CURRENT}" "${CURRENT}.clean" "${CURRENT}.new"
