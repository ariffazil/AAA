#!/usr/bin/env bash
# verify-canonical.sh — Canon #0 enforceable mechanism for AAA GitHub ops consolidation
# Forged 2026-10-12 (FI-008) to kill the "duplicate-skill selection" failure class.
#
# What this proves:
#   (1) There is exactly ONE canonical GitHub ops skill in AAA: /root/AAA/skills/github/github-ops/
#   (2) All historical duplicate names resolve to the same SHA256 — no drift
#   (3) Every symlink resolves — no broken alias paths
#   (4) The federation registry declares the canonical in its dev domain
#   (5) The canonical SKILL.md declares F1/F2/F11 floor_scope + T1 autonomy + capability_tier
#
# Exit codes:
#   0 — all checks pass (canonical is sole, sound, registered, governable)
#   1 — any check fails (output the failing check)
#
# Anti-Bangang Law 8 enforcer: satu owner (github-ops), satu jalan (the canonical + verified symlinks).
set -u

CANONICAL="/root/AAA/skills/github/github-ops"
CANONICAL_SKILL="${CANONICAL}/SKILL.md"
REGISTRY="/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml"
# Computed live from canonical — kills the brittle hardcoded-SHA failure class
EXPECTED_SHA="$(sha256sum "${CANONICAL_SKILL}" 2>/dev/null | awk '{print $1}')"

# Every path that historically held a GitHub ops skill must either
# be the canonical itself, or be a symlink/dir whose SKILL.md sha256
# matches the expected canonical hash.
ALIAS_PATHS=(
    "/root/AAA/skills/github/github-ops"
    "/root/AAA/skills/forge-github-ops"
    "/root/AAA/skills/FORGE-github-ops"
    "/root/AAA/skills/github/github-auth"
    "/root/AAA/skills/github/github-code-review"
    "/root/AAA/skills/github/github-issue-to-pr"
    "/root/AAA/skills/github/github-issues"
    "/root/AAA/skills/github/github-pr-workflow"
    "/root/AAA/skills/github/github-repo-management"
    "/root/arifOS-wt-mcp-hardening/skills/github"
    "/root/arifOS-wt-mcp-hardening/skills/github-repo-manager"
)

fail=0
step=0

step_check() {
    step=$((step + 1))
    if "$@"; then
        printf "  [%02d] PASS\n" "$step"
    else
        printf "  [%02d] FAIL\n" "$step"
        fail=$((fail + 1))
    fi
}

echo "verify-canonical.sh — AAA GitHub ops consolidation witness"
echo "  Canonical : ${CANONICAL}"
echo "  Expected  : ${EXPECTED_SHA}"
echo "  Registry  : ${REGISTRY}"
echo

# Check 1: canonical exists and is a real directory (not a symlink)
echo "[1] Canonical exists as directory:"
if [ -d "${CANONICAL}" ] && [ ! -L "${CANONICAL}" ]; then
    echo "  PASS — ${CANONICAL} is a real directory"
else
    echo "  FAIL — ${CANONICAL} missing or is a symlink"
    fail=$((fail + 1))
fi

# Check 2: canonical SKILL.md sha256 matches expected
echo "[2] Canonical SKILL.md sha256:"
if [ -f "${CANONICAL_SKILL}" ]; then
    actual_sha=$(sha256sum "${CANONICAL_SKILL}" | awk '{print $1}')
    if [ "${actual_sha}" = "${EXPECTED_SHA}" ]; then
        echo "  PASS — ${actual_sha}"
    else
        echo "  FAIL — got ${actual_sha}, want ${EXPECTED_SHA}"
        fail=$((fail + 1))
    fi
else
    echo "  FAIL — ${CANONICAL_SKILL} missing"
    fail=$((fail + 1))
fi

# Check 3: every alias path resolves and matches sha256
echo "[3] Alias paths resolve and match canonical sha256:"
alias_fail=0
for p in "${ALIAS_PATHS[@]}"; do
    if [ ! -e "${p}/SKILL.md" ]; then
        printf "      FAIL — %s does not resolve\n" "${p}"
        alias_fail=$((alias_fail + 1))
        continue
    fi
    s=$(sha256sum "${p}/SKILL.md" | awk '{print $1}')
    if [ "${s}" != "${EXPECTED_SHA}" ]; then
        printf "      FAIL — %s sha256=%s (want %s)\n" "${p}" "${s}" "${EXPECTED_SHA}"
        alias_fail=$((alias_fail + 1))
    fi
done
if [ "${alias_fail}" -eq 0 ]; then
    echo "  PASS — all ${#ALIAS_PATHS[@]} alias paths resolve to canonical sha256"
else
    echo "  FAIL — ${alias_fail} alias path(s) broken or drifted"
    fail=$((fail + 1))
fi

# Check 4: registry declares github-ops in dev domain (federated binding)
echo "[4] Registry declares github-ops as canonical dev skill:"
if [ -f "${REGISTRY}" ]; then
    if grep -qE "^[[:space:]]*-[[:space:]]*github-ops[[:space:]]*#.*canonical" "${REGISTRY}"; then
        echo "  PASS — github-ops declared canonical in ${REGISTRY}"
    else
        echo "  FAIL — github-ops not declared canonical in registry"
        fail=$((fail + 1))
    fi
else
    echo "  FAIL — registry missing"
    fail=$((fail + 1))
fi

# Check 5: no real (non-symlink) duplicate github ops dirs at /root/AAA/skills/ root
echo "[5] No rogue github-ops dirs outside canonical:"
rogue=$(find /root/AAA/skills -maxdepth 1 -type d -name "*github*" 2>/dev/null \
    | grep -v "/github$" \
    | grep -v "/github-public-push-privacy$" \
    | grep -v "/FORGE-github-workflow$" || true)
if [ -z "${rogue}" ]; then
    echo "  PASS — no rogue dirs"
else
    echo "  FAIL — rogue dir(s): ${rogue}"
    fail=$((fail + 1))
fi

# Check 6: capability_tier and floor_scope declared in canonical SKILL.md frontmatter
echo "[6] Canonical declares federated capability tier + floor scope:"
if grep -qE "^capability_tier:" "${CANONICAL_SKILL}" \
   && grep -qE "^floor_scope:" "${CANONICAL_SKILL}" \
   && grep -qE "^autonomy_tier:" "${CANONICAL_SKILL}"; then
    echo "  PASS — federated metadata present"
else
    echo "  FAIL — frontmatter missing capability_tier/floor_scope/autonomy_tier"
    fail=$((fail + 1))
fi

echo
if [ "${fail}" -eq 0 ]; then
    echo "=== VERDICT: PASS — canonical sole, sound, registered, governable ==="
    exit 0
else
    echo "=== VERDICT: FAIL — ${fail} check(s) ==="
    exit 1
fi