#!/bin/bash
# AAA Federated Skills Sync — Rebuild agent skill dirs from canonical registry
# Forged: 2026-07-10 | Authority: F13 SOVEREIGN
# Usage: skill-sync.sh [audit|sync|agent:<name>]

set -euo pipefail

AAA_SKILLS="/root/AAA/skills"
AGENTS_SKILLS="/root/.agents/skills"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log() { echo -e "${GREEN}[SYNC]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

find_canonical() {
    local skill_id="$1"
    if [ -d "$AAA_SKILLS/$skill_id" ]; then
        echo "$AAA_SKILLS/$skill_id"
    elif [ -d "$AGENTS_SKILLS/$skill_id" ]; then
        echo "$AGENTS_SKILLS/$skill_id"
    else
        local found
        found=$(find "$AAA_SKILLS" "$AGENTS_SKILLS" -maxdepth 2 -name "SKILL.md" -path "*/$skill_id/*" 2>/dev/null | head -1)
        if [ -n "$found" ]; then
            dirname "$found"
        fi
    fi
}

link_skill() {
    local skill_id="$1"
    local target_dir="$2"
    local source
    source=$(find_canonical "$skill_id")

    if [ -z "$source" ]; then
        warn "Cannot find canonical source for: $skill_id (skipping)"
        return 0
    fi

    local link_path="$target_dir/$skill_id"

    # Skip if already correct symlink
    if [ -L "$link_path" ]; then
        local current_target resolved_source
        current_target=$(readlink -f "$link_path" 2>/dev/null || true)
        resolved_source=$(readlink -f "$source" 2>/dev/null || true)
        [ "$current_target" = "$resolved_source" ] && return 0
    fi

    [ -e "$link_path" ] && rm -rf "$link_path"
    ln -sf "$source" "$link_path"
}

# Skills available to all agents (canonical set)
ALL_SKILLS=(
    # Governance
    aaa-agent-invariants aaa-agentic-governance arifos-governance arifos-act
    constitutional-reasoning f1-gate sovereign-recognize phase-escalation-discipline
    parallel-authority-detection incident-escalation incident-triage
    pr-review-governance nusantara-intelligence-substrate spatial-grounding
    # Engineering
    aforge-apex-9-execution aforge-apex-9-execution-reference kernel-verbs-aforge-hands
    precommit-gate precommit-review docker docker-entropy-ops docker-thermodynamics
    vps-docker-runbook vps-docker-ops mcp-ops mcp-federation-ops mcp-builder-doctrine
    mcp-zen-authoring mcp-smoke-test arif-mcp-governor arifos-mcp-federation
    github github-ops github-runbook github-ci-diagnose github-issue-triage
    github-pr-review secret-hygiene secret-safety-scan infra-guardian
    # Domain
    geox-grounding geox-basin-engines geox-claim-grammar geox-constitution
    geox-contradiction-engine geox-earth-evidence geox-epistemic-ladder
    geox-petrophysics-bounds geox-redteam-hantu geox-scientific-writing
    geox-well-tie-pipeline geological-artifact-rigor prospect-maturation-workflow
    wealth-capital-reasoning wealth-capital-thermodynamics wealth-collapse-signature
    wealth-law-anthropology well-substrate-readiness
    # Meta
    skill-creator skill-trigger-linter recursive-skill-forge recursive-self-improvement
    arifos-recursive-audit arifos-evals arifos-observability arifos-plan-dag
    multi-discipline-critique meta-mesa-skill-atlas unified-skill-binding
    drift-watch drift-response service-health-triage verify-runtime
    code-wiki code-analysis-skills readme-truth-check repo-hygiene-audit summarize-pro
    # Memory
    vault999-integrity vault999-reader vault-integrity 999-vault-seal-immutable
    session-continuity-inhabit agent-memory-bridge unified-memory-federation
    knowledge-graph-query asi-knowledge-writeback agentic-dream-engine
    claim-receipt-v1 claim-verification-gate truth-receipt-enforcer
    # Trinity
    # Consciousness
    symbolic-order-collective-bias symbolic-order-trust-architecture
    transport-physics-intelligence cooling-ledger-rsi zen-organ-memory
    # Special
    explorer-intelligence-architecture ask-search seek federation-orchestrator
    mcp-lifeguard model-fallback-monitor telegram-security-audit google-workspace-cli
    agentic-web-optimization subagent-spawn-template
)

sync_agent() {
    local agent_name="$1"
    local target_dir="$2"
    log "Syncing $agent_name → $target_dir"
    mkdir -p "$target_dir"

    for skill in "${ALL_SKILLS[@]}"; do
        link_skill "$skill" "$target_dir"
    done

    local count
    count=$(ls "$target_dir" 2>/dev/null | wc -l)
    log "$agent_name: $count skills linked"
}

sync_claude() {
    sync_agent "Claude Code" "$HOME/.claude/skills"
    # Restore Claude-specific symlinks from backup if they existed
    local bak="$HOME/.claude/skills.bak-20260711"
    for special in forge-opencode-spawn opencode-acp opencode minimax-cli warga-skills; do
        if [ -L "$bak/$special.md" ] && [ ! -e "$HOME/.claude/skills/$special.md" ] && [ ! -e "$HOME/.claude/skills/$special" ]; then
            ln -sf "$(readlink "$bak/$special.md")" "$HOME/.claude/skills/$special.md" 2>/dev/null || true
        elif [ -L "$bak/$special" ] && [ ! -e "$HOME/.claude/skills/$special" ]; then
            ln -sf "$(readlink "$bak/$special")" "$HOME/.claude/skills/$special" 2>/dev/null || true
        fi
    done
}

sync_codex() {
    sync_agent "Codex CLI" "$HOME/.codex/skills"
}

sync_grok() {
    sync_agent "Grok Build" "$HOME/.grok/skills"
}

audit() {
    echo "═══════════════════════════════════════════════════"
    echo "  AAA Federated Skills Audit — $(date -Iseconds)"
    echo "═══════════════════════════════════════════════════"
    echo ""
    echo "Skill counts:"
    for d in "$AAA_SKILLS" "$AGENTS_SKILLS" "$HOME/.claude/skills" "$HOME/.kimi/skills" "$HOME/.codex/skills" "$HOME/.grok/skills"; do
        local name=$(basename "$d")
        local count=$(ls -d "$d"/*/ 2>/dev/null | wc -l)
        [ -d "$d" ] && echo "  $name: $count dirs"
    done
    echo ""
    echo "Registry total: $(grep -c 'id:' /root/AAA/skills/FEDERATED_SKILLS_REGISTRY.yaml 2>/dev/null || echo 0) entries"
}

case "${1:-sync}" in
    audit)   audit ;;
    sync)    sync_claude; sync_codex; sync_grok ;;
    agent:*) 
        case "${1#agent:}" in
            claude) sync_claude ;;
            codex)  sync_codex ;;
            grok)   sync_grok ;;
            *)      echo "Unknown agent"; exit 1 ;;
        esac
        ;;
    *)  echo "Usage: $0 [audit|sync|agent:<claude|codex|grok>]"; exit 1 ;;
esac
