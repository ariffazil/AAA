/**
 * AgentModelPanel — Governance Spine Consumption Layer
 * ═══════════════════════════════════════════════════════════════
 *
 * Displays the live model_governance_card from the arifOS-model-registry spine.
 * Shows: verified identity, provider soul, self-claim boundaries,
 * shadow profile, risk leash, and drift state.
 *
 * GREEN  = spine-verified, identity matches
 * YELLOW = spine mismatch detected, needs review
 * RED    = no valid spine anchor, execution blocked
 *
 * Consumed by:
 *   - arifOS MCP (judgment layer): constitutional enforcement
 *   - A-FORGE (execution layer): runtime truth enforcement
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

import { Shield, AlertTriangle, CheckCircle2, Info, Skull, Eye, Ban } from 'lucide-react';

// ── Types ────────────────────────────────────────────────────────────────────

export interface ModelGovernanceCard {
  model_anchor?: {
    provider_key?: string;
    family_key?: string;
    model_variant?: string;
    identity_verified?: boolean;
    verified_at?: string;
  };
  runtime_truth?: {
    tools?: string[];
    web?: boolean;
    memory?: boolean;
    execution_mode?: string;
    side_effects_allowed?: boolean;
    auth_level?: string;
  };
  self_claim_boundary?: {
    identity?: string;
    tools?: string;
    knowledge?: string;
    actions?: string;
  };
  shadow_profile?: {
    angel?: string;
    shadow?: string;
    paradox?: string;
    control_laws?: string[];
    tripwires?: string[];
  };
  risk_leash?: {
    risk_tier?: string;
    requires_human_ack_for?: string[];
  };
  provider_soul?: string;
  soul_label?: string;
  drift_state?: 'GREEN' | 'YELLOW' | 'RED';
  cascade_tier?: string;
  last_verified?: string;
}

interface AgentModelPanelProps {
  governanceCard: ModelGovernanceCard | null;
  isLoading?: boolean;
  error?: string | null;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function driftBadge(state?: string) {
  switch (state) {
    case 'GREEN':
      return {
        icon: <CheckCircle2 className="w-4 h-4" />,
        label: 'VERIFIED',
        textColor: 'text-emerald-400',
        bgColor: 'bg-emerald-950/30',
        borderColor: 'border-emerald-500/30',
      };
    case 'YELLOW':
      return {
        icon: <AlertTriangle className="w-4 h-4" />,
        label: 'MISMATCH',
        textColor: 'text-yellow-400',
        bgColor: 'bg-yellow-950/30',
        borderColor: 'border-yellow-500/30',
      };
    case 'RED':
      return {
        icon: <Skull className="w-4 h-4" />,
        label: 'NO ANCHOR',
        textColor: 'text-red-400',
        bgColor: 'bg-red-950/30',
        borderColor: 'border-red-500/30',
      };
    default:
      return {
        icon: <Info className="w-4 h-4" />,
        label: 'UNKNOWN',
        textColor: 'text-slate-400',
        bgColor: 'bg-slate-950/30',
        borderColor: 'border-slate-500/30',
      };
  }
}

function riskTierBadge(tier?: string) {
  switch (tier) {
    case 'bounded':
      return { color: 'text-emerald-400', bg: 'bg-emerald-950/20', label: 'BOUNDED' };
    case 'unbounded':
      return { color: 'text-red-400', bg: 'bg-red-950/20', label: 'UNBOUNDED' };
    default:
      return { color: 'text-slate-400', bg: 'bg-slate-950/20', label: tier?.toUpperCase() || 'UNKNOWN' };
  }
}

// ── Component ────────────────────────────────────────────────────────────────

export default function AgentModelPanel({ governanceCard, isLoading, error }: AgentModelPanelProps) {
  // ── Loading State ──────────────────────────────────────────────────────────
  if (isLoading) {
    return (
      <div className="rounded-xl border border-slate-800 bg-slate-950/50 p-5">
        <div className="flex items-center gap-2 mb-3">
          <Shield className="w-5 h-5 text-slate-500 animate-pulse" />
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">
            Agent Identity
          </h3>
        </div>
        <div className="space-y-2 animate-pulse">
          <div className="h-4 bg-slate-800 rounded w-3/4" />
          <div className="h-3 bg-slate-800 rounded w-1/2" />
          <div className="h-3 bg-slate-800 rounded w-2/3" />
        </div>
      </div>
    );
  }

  // ── Error State ────────────────────────────────────────────────────────────
  if (error || !governanceCard) {
    const badge = driftBadge('RED');
    return (
      <div className="rounded-xl border border-red-500/30 bg-red-950/20 p-5">
        <div className="flex items-center gap-2 mb-3">
          {badge.icon}
          <h3 className="text-sm font-semibold text-red-400 uppercase tracking-wider">
            Agent Identity — NO SPINE ANCHOR
          </h3>
          <span className={`ml-auto px-2 py-0.5 rounded text-xs font-mono ${badge.textColor} ${badge.bgColor} border ${badge.borderColor}`}>
            {badge.label}
          </span>
        </div>
        <p className="text-xs text-red-300/70">
          {error || 'No governance card available. Execution is blocked until the spine provides identity verification.'}
        </p>
      </div>
    );
  }

  // ── Normal State ───────────────────────────────────────────────────────────
  const card = governanceCard;
  const drift = driftBadge(card.drift_state);
  const rtBadge = riskTierBadge(card.risk_leash?.risk_tier);
  const anchor = card.model_anchor || {};
  const shadow = card.shadow_profile || {};
  const boundary = card.self_claim_boundary || {};
  const runtime = card.runtime_truth || {};

  return (
    <div className={`rounded-xl border ${drift.borderColor} ${drift.bgColor} p-5 space-y-4`}>
      {/* ── Header ──────────────────────────────────────────────────────────── */}
      <div className="flex items-center gap-2">
        {drift.icon}
        <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">
          Agent Identity
        </h3>
        <span className={`ml-auto px-2 py-0.5 rounded text-xs font-mono ${drift.textColor} ${drift.bgColor} border ${drift.borderColor}`}>
          {drift.label}
        </span>
      </div>

      {/* ── Model Info Row ──────────────────────────────────────────────────── */}
      <div className="grid grid-cols-2 gap-3 text-xs">
        <div>
          <span className="text-slate-500">Provider</span>
          <p className="text-slate-200 font-mono mt-0.5">
            {anchor.provider_key || 'unknown'}
          </p>
        </div>
        <div>
          <span className="text-slate-500">Model</span>
          <p className="text-slate-200 font-mono mt-0.5 truncate" title={anchor.model_variant}>
            {anchor.model_variant || 'unknown'}
          </p>
        </div>
        <div>
          <span className="text-slate-500">Family / Soul</span>
          <p className="text-slate-200 font-mono mt-0.5">
            {anchor.family_key || 'unknown'}
            {card.soul_label ? ` · ${card.soul_label}` : ''}
          </p>
        </div>
        <div>
          <span className="text-slate-500">Risk Tier</span>
          <p className={`${rtBadge.color} font-mono mt-0.5`}>
            <span className={`inline-block px-1.5 py-0.5 rounded ${rtBadge.bg}`}>{rtBadge.label}</span>
          </p>
        </div>
        <div>
          <span className="text-slate-500">Cascade Tier</span>
          <p className="text-slate-200 font-mono mt-0.5">{card.cascade_tier || 'primary'}</p>
        </div>
        <div>
          <span className="text-slate-500">Verified</span>
          <p className="text-slate-200 font-mono mt-0.5">
            {anchor.identity_verified ? '✅' : '❌'}
            {' '}{card.last_verified || anchor.verified_at || 'never'}
          </p>
        </div>
      </div>

      {/* ── Self-Claim Boundary ─────────────────────────────────────────────── */}
      {Object.keys(boundary).length > 0 && (
        <div className="border-t border-slate-800 pt-3">
          <div className="flex items-center gap-1.5 mb-2">
            <Ban className="w-3.5 h-3.5 text-amber-400" />
            <span className="text-xs font-semibold text-amber-400 uppercase">Self-Claim Boundary</span>
          </div>
          <div className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
            {boundary.identity && (
              <div className="col-span-2">
                <span className="text-slate-500">Identity:</span>{' '}
                <span className="text-slate-300 font-mono">{boundary.identity}</span>
              </div>
            )}
            {boundary.tools && (
              <div>
                <span className="text-slate-500">Tools:</span>{' '}
                <span className="text-slate-300 font-mono">{boundary.tools}</span>
              </div>
            )}
            {boundary.actions && (
              <div>
                <span className="text-slate-500">Actions:</span>{' '}
                <span className="text-slate-300 font-mono">{boundary.actions}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── Shadow Profile ──────────────────────────────────────────────────── */}
      {shadow.angel && (
        <div className="border-t border-slate-800 pt-3">
          <div className="flex items-center gap-1.5 mb-2">
            <Eye className="w-3.5 h-3.5 text-purple-400" />
            <span className="text-xs font-semibold text-purple-400 uppercase">Shadow Profile</span>
          </div>
          <div className="space-y-1.5 text-xs">
            <div>
              <span className="text-purple-400/70">Angel:</span>{' '}
              <span className="text-slate-300">{shadow.angel}</span>
            </div>
            <div>
              <span className="text-red-400/70">Shadow:</span>{' '}
              <span className="text-slate-400">{shadow.shadow}</span>
            </div>
            {shadow.paradox && (
              <div>
                <span className="text-amber-400/70">Paradox:</span>{' '}
                <span className="text-slate-400 italic">{shadow.paradox}</span>
              </div>
            )}
            {shadow.tripwires && shadow.tripwires.length > 0 && (
              <div>
                <span className="text-red-400/70">Tripwires:</span>
                <ul className="mt-1 space-y-0.5 ml-3 list-disc text-slate-500 marker:text-red-500/50">
                  {shadow.tripwires.slice(0, 3).map((t, i) => (
                    <li key={i}>{t}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── Runtime Truth ───────────────────────────────────────────────────── */}
      {runtime.tools && runtime.tools.length > 0 && (
        <div className="border-t border-slate-800 pt-3">
          <span className="text-xs font-semibold text-slate-500 uppercase">Runtime Truth</span>
          <div className="flex flex-wrap gap-1 mt-1.5">
            {runtime.tools?.slice(0, 8).map((t) => (
              <span key={t} className="px-1.5 py-0.5 rounded text-xs font-mono bg-slate-800 text-slate-400">
                {t}
              </span>
            ))}
            {(runtime.tools?.length || 0) > 8 && (
              <span className="px-1.5 py-0.5 rounded text-xs font-mono bg-slate-800 text-slate-500">
                +{(runtime.tools?.length || 0) - 8} more
              </span>
            )}
          </div>
          <div className="flex gap-3 mt-1.5 text-xs text-slate-500">
            <span>Web: {runtime.web ? '✅' : '❌'}</span>
            <span>Memory: {runtime.memory ? '✅' : '❌'}</span>
            <span>SideFX: {runtime.side_effects_allowed ? '⚠️' : '🚫'}</span>
          </div>
        </div>
      )}
    </div>
  );
}
