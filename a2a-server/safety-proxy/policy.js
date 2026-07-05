#!/usr/bin/env node
/**
 * policy.js — Constitutional Policy Engine for hermes_safety_proxy
 * ================================================================
 * Classifies every action into one of three tiers:
 *
 *   AUTO_PASS      — Read-only, observe, no side effects. Forward immediately.
 *   JITU_REQUIRED  — Write/execute, reversible. Needs valid JITU token.
 *   DENY           — Destructive, irreversible, or constitutional violation. Block always.
 *
 * Policy is derived from F1-F13 constitutional floors:
 *   F1  AMANAH    → reversibility first, backup before edit
 *   F8  LAW       → respect system boundaries
 *   F11 AUDIT     → every action leaves a trace
 *   F13 SOVEREIGN → Arif holds final veto on irreversible
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

'use strict';

// ── Action Classification ─────────────────────────────────────────────────

/**
 * Tier definitions.
 * Each tier maps to a set of tool name patterns and action classes.
 */
const TIERS = Object.freeze({
  AUTO_PASS: 'AUTO_PASS',
  JITU_REQUIRED: 'JITU_REQUIRED',
  DENY: 'DENY',
});

// ── DENY patterns — always blocked, no exceptions ─────────────────────────
// These are constitutional violations or physically dangerous operations.
const DENY_PATTERNS = Object.freeze([
  // F1 AMANAH: irreversible data destruction without backup
  /rm\s+-rf\s+\/(?!tmp)/i,              // rm -rf /anything except /tmp
  /DROP\s+DATABASE/i,
  /TRUNCATE\s+DATABASE/i,
  /format\s+[c-z]:/i,                    // Windows format (cross-safety)

  // F8 LAW: system boundary violations
  /chmod\s+777/i,                         // world-writable permissions
  /chown\s+root.*\//i,                    // changing root ownership recursively
  /iptables\s+-F/i,                       // flush all firewall rules
  /ufw\s+disable/i,                       // disable firewall

  // F13 SOVEREIGN: unauthorized identity/key operations
  /ssh-keygen.*-f.*id_rsa/i,             // overwriting SSH keys without approval
  /openssl\s+req.*-new/i,                // generating new certs without approval

  // Anti-hantu: no consciousness injection
  /inject.*consciousness/i,
  /simulate.*soul/i,
]);

// ── JITU_REQUIRED patterns — need sovereign approval ──────────────────────
// These are write/execute operations that are reversible but impactful.
const JITU_PATTERNS = Object.freeze([
  // Git operations
  /git\s+push/i,
  /git\s+push\s+--force/i,               // also matches DENY below (force wins)
  /git\s+rebase/i,
  /git\s+reset\s+--hard/i,
  /git\s+checkout.*--force/i,
  /git\s+branch\s+-[dD]/i,               // delete branch

  // Database writes
  /\bINSERT\b/i,
  /\bUPDATE\b/i,
  /\bDELETE\b/i,
  /\bALTER\b/i,
  /\bCREATE\b/i,
  /\bDROP\s+TABLE\b/i,

  // System service mutations
  /systemctl\s+(start|stop|restart|enable|disable)/i,
  /service\s+\w+\s+(start|stop|restart)/i,

  // File system writes (high-level)
  /rm\s+-[rf]+\s/i,                      // rm -r, rm -f, rm -rf
  /mv\s+.*\s+\/(?!tmp)/i,               // move to non-tmp
  /cp\s+.*\s+\/etc/i,                    // copy to /etc

  // Docker mutations
  /docker\s+(rm|stop|kill|compose\s+down)/i,
  /docker\s+volume\s+rm/i,

  // Deployment
  /deploy/i,
  /redeploy/i,
  /publish/i,

  // Network/firewall changes
  /ufw\s+(allow|deny|reject)/i,
  /iptables\s+(-[AI]|-D)/i,

  // Caddy/nginx reload
  /caddy\s+reload/i,
  /nginx\s+-s\s+reload/i,

  // Package management
  /npm\s+install(?!.*--dry-run)/i,
  /apt(-get)?\s+(install|remove|purge)/i,
  /pip\s+install/i,
]);

// ── Force-DENY overrides — even with JITU token, these are blocked ────────
// These escalate to F13 SOVEREIGN only (physical intervention required).
const FORCE_DENY_PATTERNS = Object.freeze([
  /git\s+push\s+--force.*main/i,         // force push to main
  /git\s+push\s+--force.*master/i,       // force push to master
  /rm\s+-rf\s+\/$/i,                     // rm -rf /
  /shutdown/i,
  /reboot/i,
  /halt/i,
  /init\s+0/i,
  /mkfs/i,                               // format filesystem
  /dd\s+if=.*of=\/dev/i,                 // raw disk write
]);

// ── Tool-level classification ─────────────────────────────────────────────
// Maps MCP tool names to tiers directly (faster than regex on command text).
const TOOL_TIER_MAP = Object.freeze({
  // AUTO_PASS — read-only tools
  'forge_probe': TIERS.AUTO_PASS,
  'forge_health_check': TIERS.AUTO_PASS,
  'forge_registry_status': TIERS.AUTO_PASS,
  'forge_registry': TIERS.AUTO_PASS,
  'forge_status': TIERS.AUTO_PASS,
  'forge_vps_ports': TIERS.AUTO_PASS,
  'forge_vps_services': TIERS.AUTO_PASS,
  'forge_vps_cron': TIERS.AUTO_PASS,
  'forge_boundaries_assert': TIERS.AUTO_PASS,
  'forge_surface_guard': TIERS.AUTO_PASS,
  'forge_surface_audit': TIERS.AUTO_PASS,
  'forge_docs_lookup': TIERS.AUTO_PASS,
  'forge_search': TIERS.AUTO_PASS,
  'forge_research': TIERS.AUTO_PASS,
  'forge_minimax_search': TIERS.AUTO_PASS,
  'forge_fetch': TIERS.AUTO_PASS,
  'forge_filesystem': TIERS.AUTO_PASS,   // read mode — write mode checked separately
  'forge_git': TIERS.AUTO_PASS,          // read modes — write mode checked separately
  'forge_docker': TIERS.AUTO_PASS,       // read modes
  'forge_postgres': TIERS.AUTO_PASS,     // read mode
  'forge_memory': TIERS.AUTO_PASS,
  'forge_worktree': TIERS.AUTO_PASS,
  'forge_shell_dryrun': TIERS.AUTO_PASS,
  'forge_shell_status': TIERS.AUTO_PASS,
  'forge_shell_ledger': TIERS.AUTO_PASS,
  'forge_shell_alert_history': TIERS.AUTO_PASS,
  'forge_chart': TIERS.AUTO_PASS,
  'forge_job': TIERS.AUTO_PASS,          // status mode
  'forge_agent': TIERS.AUTO_PASS,        // list/status mode
  'forge_scar': TIERS.AUTO_PASS,         // list/consult mode
  'forge_witness': TIERS.AUTO_PASS,
  'forge_evaluate': TIERS.AUTO_PASS,
  'forge_skillstore_read': TIERS.AUTO_PASS,
  'forge_check_governance': TIERS.AUTO_PASS,
  'forge_heart_critique': TIERS.AUTO_PASS,
  'forge_journalctl': TIERS.AUTO_PASS,
  'forge_netdata_alarms': TIERS.AUTO_PASS,
  'forge_netdata_metrics': TIERS.AUTO_PASS,
  'forge_document_ingest': TIERS.AUTO_PASS,

  // JITU_REQUIRED — write/execute tools
  'forge_shell': TIERS.JITU_REQUIRED,
  'forge_execute': TIERS.JITU_REQUIRED,
  'forge_execute_sealed': TIERS.JITU_REQUIRED,
  'forge_git_commit': TIERS.JITU_REQUIRED,
  'forge_filesystem_write': TIERS.JITU_REQUIRED,
  'forge_postgres_mutate': TIERS.JITU_REQUIRED,
  'forge_pipeline_run': TIERS.JITU_REQUIRED,
  'forge_reality_loop': TIERS.JITU_REQUIRED,
  'forge_job_submit': TIERS.JITU_REQUIRED,
  'forge_agent_register': TIERS.JITU_REQUIRED,
  'forge_agent_kill': TIERS.JITU_REQUIRED,
  'forge_scar_seal': TIERS.JITU_REQUIRED,
  'forge_register': TIERS.JITU_REQUIRED,
  'forge_skill': TIERS.JITU_REQUIRED,
  'forge_stage': TIERS.JITU_REQUIRED,
  'forge_docket_prep': TIERS.JITU_REQUIRED,
  'forge_sandbox_run': TIERS.JITU_REQUIRED,
  'forge_synthesize': TIERS.JITU_REQUIRED,
  'forge_tier_bind': TIERS.JITU_REQUIRED,
  'forge_lock': TIERS.JITU_REQUIRED,
  'forge_lease': TIERS.JITU_REQUIRED,
  'forge_policy': TIERS.JITU_REQUIRED,
  'forge_vault_write': TIERS.JITU_REQUIRED,
  'forge_vault_seal': TIERS.JITU_REQUIRED,
  'forge_seal': TIERS.JITU_REQUIRED,
  'forge_abort': TIERS.JITU_REQUIRED,
  'forge_skillstore_write': TIERS.JITU_REQUIRED,
  'forge_github_create_issue': TIERS.JITU_REQUIRED,
  'forge_github_create_pull_request': TIERS.JITU_REQUIRED,
  'forge_github_create_or_update_file': TIERS.JITU_REQUIRED,
  'forge_browser_type': TIERS.JITU_REQUIRED,
  'forge_browser_click': TIERS.JITU_REQUIRED,

  // DENY — always blocked
  'forge_approve': TIERS.DENY,           // A-FORGE cannot self-authorize
});

// ── Classification engine ─────────────────────────────────────────────────

/**
 * Classify an action into AUTO_PASS | JITU_REQUIRED | DENY.
 *
 * @param {object} params
 * @param {string} params.tool_name — MCP tool name (e.g., 'forge_shell')
 * @param {string} params.command — raw command text (for shell/exec tools)
 * @param {string} params.action_class — action class from ART (OBSERVE/MUTATE/etc.)
 * @param {string} params.actor_id — who is calling
 * @param {object} params.arguments — tool arguments (for mode detection)
 * @returns {{ tier: string, reason: string, floor: string|null, pattern: string|null }}
 */
function classifyAction({ tool_name, command, action_class, actor_id, arguments: args }) {
  // 1. Force-DENY check (highest priority — blocks even with JITU)
  if (command) {
    for (const pattern of FORCE_DENY_PATTERNS) {
      if (pattern.test(command)) {
        return {
          tier: TIERS.DENY,
          reason: `FORCE_DENY: command matches irreversible pattern`,
          floor: 'F13',
          pattern: pattern.source,
        };
      }
    }
  }

  // 2. DENY pattern check on command text
  if (command) {
    for (const pattern of DENY_PATTERNS) {
      if (pattern.test(command)) {
        return {
          tier: TIERS.DENY,
          reason: `DENY: command matches destructive pattern`,
          floor: 'F1',
          pattern: pattern.source,
        };
      }
    }
  }

  // 3. Tool-level classification (fast path)
  if (tool_name && TOOL_TIER_MAP[tool_name]) {
    const tier = TOOL_TIER_MAP[tool_name];
    if (tier === TIERS.DENY) {
      return {
        tier: TIERS.DENY,
        reason: `DENY: tool '${tool_name}' is constitutionally blocked`,
        floor: 'F13',
        pattern: null,
      };
    }
    return {
      tier,
      reason: tier === TIERS.AUTO_PASS
        ? `AUTO_PASS: tool '${tool_name}' is read-only/observe class`
        : `JITU_REQUIRED: tool '${tool_name}' is write/execute class`,
      floor: tier === TIERS.JITU_REQUIRED ? 'F1' : null,
      pattern: null,
    };
  }

  // 4. Action class-based classification
  if (action_class) {
    const ac = action_class.toUpperCase();
    if (['OBSERVE', 'SENSE', 'SEARCH', 'FETCH', 'QUERY'].includes(ac)) {
      return {
        tier: TIERS.AUTO_PASS,
        reason: `AUTO_PASS: action_class '${ac}' is observe-only`,
        floor: null,
        pattern: null,
      };
    }
    if (['IRREVERSIBLE', 'EXTERNAL_SIDE_EFFECT'].includes(ac)) {
      return {
        tier: TIERS.DENY,
        reason: `DENY: action_class '${ac}' requires F13 sovereign approval`,
        floor: 'F13',
        pattern: null,
      };
    }
    if (['MUTATE', 'EXECUTE', 'DRAFT', 'QUEUE', 'ATOMIC', 'PROPOSE'].includes(ac)) {
      return {
        tier: TIERS.JITU_REQUIRED,
        reason: `JITU_REQUIRED: action_class '${ac}' is write/execute`,
        floor: 'F1',
        pattern: null,
      };
    }
  }

  // 5. JITU pattern check on command text (lower priority than DENY)
  if (command) {
    for (const pattern of JITU_PATTERNS) {
      if (pattern.test(command)) {
        return {
          tier: TIERS.JITU_REQUIRED,
          reason: `JITU_REQUIRED: command matches write pattern`,
          floor: 'F1',
          pattern: pattern.source,
        };
      }
    }
  }

  // 6. Default: JITU_REQUIRED for unknown tools (safe default — F1 AMANAH)
  //    Better to require approval than to let unknown operations pass.
  return {
    tier: TIERS.JITU_REQUIRED,
    reason: `JITU_REQUIRED: unknown tool '${tool_name || 'none'}' — safe default (F1 AMANAH)`,
    floor: 'F1',
    pattern: null,
  };
}

/**
 * Check if a tool call is read-only based on its arguments.
 * Some tools (forge_filesystem, forge_git, forge_docker, forge_postgres)
 * have both read and write modes.
 */
function isReadOnlyMode(tool_name, args) {
  if (!args) return false;

  switch (tool_name) {
    case 'forge_filesystem':
      return ['read', 'glob', 'grep', 'stat'].includes(args.mode);
    case 'forge_git':
      return ['status', 'diff', 'log'].includes(args.mode);
    case 'forge_docker':
      return ['ps', 'logs', 'images'].includes(args.mode);
    case 'forge_postgres':
      return args.mode === 'query' && !args.mutate;
    case 'forge_job':
      return args.mode === 'status';
    case 'forge_agent':
      return ['list', 'status'].includes(args.mode);
    case 'forge_scar':
      return ['list', 'consult'].includes(args.mode);
    case 'forge_vault':
      return ['read', 'list'].includes(args.mode);
    case 'forge_lease':
      return args.mode === 'status';
    case 'forge_reality_loop':
      return ['report', 'metrics', 'list'].includes(args.mode);
    default:
      return false;
  }
}

// ── Exports ───────────────────────────────────────────────────────────────

module.exports = {
  TIERS,
  DENY_PATTERNS,
  JITU_PATTERNS,
  FORCE_DENY_PATTERNS,
  TOOL_TIER_MAP,
  classifyAction,
  isReadOnlyMode,
};
