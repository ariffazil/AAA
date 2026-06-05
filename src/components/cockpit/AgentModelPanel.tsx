/**
 * AgentModelPanel — Governance Spine Consumption Layer
 * ═══════════════════════════════════════════════════════════════
 *
 * Displays the live model_governance_card from the arifOS-model-registry spine.
 * Shows: verified identity, provider soul, self-claim boundaries,
 * shadow profile, risk leash, and drift state.
 *
 * Verdict:
 *   SOVEREIGN  (GREEN)  = spine-verified, identity matches, all gates nominal
 *   ADVISORY   (YELLOW) = spine mismatch detected, some gates warn, needs review
 *   VIOLATION  (RED)    = no valid spine anchor, execution blocked
 *
 * Consumed by:
 *   - AAA Cockpit (operator surface): human sovereign visibility
 *   - arifOS MCP (judgment layer): constitutional enforcement
 *   - A-FORGE (execution layer): runtime truth enforcement
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

import React, { useState } from 'react';
import {
  Shield,
  AlertTriangle,
  CheckCircle2,
  Info,
  Skull,
  Eye,
  Ban,
  ChevronDown,
  ChevronRight,
  Lock,
  Unlock,
  Fingerprint,
  Cpu,
  Gauge,
  Wrench,
} from 'lucide-react';

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
  model_cascade?: Record<string, unknown> | null;
  capabilities?: Record<string, unknown> | null;
  error?: string;
}

interface AgentModelPanelProps {
  governanceCard: ModelGovernanceCard | null;
  isLoading?: boolean;
  error?: string | null;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

type VerdictTier = 'SOVEREIGN' | 'ADVISORY' | 'VIOLATION';

interface VerdictStyle {
  tier: VerdictTier;
  label: string;
  icon: React.ReactNode;
  bannerBg: string;
  bannerBorder: string;
  bannerText: string;
  dotColor: string;
}

function computeVerdict(
  drift: string | undefined,
  identityVerified: boolean | undefined,
  hasError: boolean,
): VerdictStyle {
  if (hasError || drift === 'RED' || identityVerified === false) {
    return {
      tier: 'VIOLATION',
      label: 'VIOLATION',
      icon: <Skull className="w-5 h-5" />,
      bannerBg: 'bg-red-950/40',
      bannerBorder: 'border-red-500/40',
      bannerText: 'text-red-400',
      dotColor: 'bg-red-500',
    };
  }
  if (drift === 'YELLOW') {
    return {
      tier: 'ADVISORY',
      label: 'ADVISORY',
      icon: <AlertTriangle className="w-5 h-5" />,
      bannerBg: 'bg-yellow-950/30',
      bannerBorder: 'border-yellow-500/30',
      bannerText: 'text-yellow-400',
      dotColor: 'bg-yellow-500',
    };
  }
  return {
    tier: 'SOVEREIGN',
    label: 'SOVEREIGN',
    icon: <Shield className="w-5 h-5" />,
    bannerBg: 'bg-emerald-950/20',
    bannerBorder: 'border-emerald-500/30',
    bannerText: 'text-emerald-400',
    dotColor: 'bg-emerald-500',
  };
}

function driftBadge(state?: string): {
  icon: React.ReactNode;
  label: string;
  textColor: string;
  bgColor: string;
  borderColor: string;
} {
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

function riskTierBadge(tier?: string): {
  color: string;
  bg: string;
  label: string;
} {
  switch (tier) {
    case 'bounded':
      return {
        color: 'text-emerald-400',
        bg: 'bg-emerald-950/20',
        label: 'BOUNDED',
      };
    case 'unbounded':
      return {
        color: 'text-red-400',
        bg: 'bg-red-950/20',
        label: 'UNBOUNDED',
      };
    default:
      return {
        color: 'text-slate-400',
        bg: 'bg-slate-950/20',
        label: tier?.toUpperCase() || 'UNKNOWN',
      };
  }
}

function formatActionLabel(action: string): string {
  return action
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

// ── Accordion Section ────────────────────────────────────────────────────────

function AccordionSection({
  title,
  icon,
  accentColor,
  defaultOpen = false,
  children,
}: {
  title: string;
  icon: React.ReactNode;
  accentColor: string;
  defaultOpen?: boolean;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="border-t border-slate-800/80">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center gap-2 py-2.5 text-left hover:bg-slate-900/30 transition-colors rounded"
      >
        {open ? (
          <ChevronDown className="w-3.5 h-3.5 text-slate-500" />
        ) : (
          <ChevronRight className="w-3.5 h-3.5 text-slate-500" />
        )}
        <span className={accentColor}>{icon}</span>
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
          {title}
        </span>
      </button>
      {open && <div className="pb-3 pl-7">{children}</div>}
    </div>
  );
}

// ── Component ────────────────────────────────────────────────────────────────

export default function AgentModelPanel({
  governanceCard,
  isLoading,
  error,
}: AgentModelPanelProps) {
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

  // ── Error / No Spine ──────────────────────────────────────────────────────
  if (error || !governanceCard) {
    const verdict = computeVerdict('RED', false, true);
    return (
      <div className={`rounded-xl border ${verdict.bannerBorder} ${verdict.bannerBg} overflow-hidden`}>
        {/* Verdict Banner */}
        <div className={`px-5 py-3 flex items-center gap-3 ${verdict.bannerBg}`}>
          <span className={verdict.dotColor + ' w-2.5 h-2.5 rounded-full animate-pulse'} />
          <span className={`text-sm font-black uppercase tracking-widest ${verdict.bannerText}`}>
            {verdict.tier}
          </span>
          <span className="ml-auto text-[10px] font-mono text-slate-500">NO SPINE</span>
        </div>
        <div className="px-5 py-4">
          <div className="flex items-start gap-3">
            <Skull className="w-10 h-10 text-red-500/40 mt-0.5 shrink-0" />
            <div>
              <p className="text-sm font-semibold text-red-300 mb-1">
                Governance Spine Unavailable
              </p>
              <p className="text-xs text-red-300/60 leading-relaxed">
                {error ||
                  'No governance card available. Execution is blocked until the spine provides identity verification.'}
              </p>
              <div className="mt-3 flex items-center gap-2 text-[10px] text-red-400/50 font-mono">
                <Ban className="w-3 h-3" />
                <span>ALL EXECUTION GATES: CLOSED</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ── Normal State ───────────────────────────────────────────────────────────
  const card = governanceCard;
  const drift = driftBadge(card.drift_state);
  const verdict = computeVerdict(
    card.drift_state,
    card.model_anchor?.identity_verified,
    false,
  );
  const rtBadge = riskTierBadge(card.risk_leash?.risk_tier);
  const anchor = card.model_anchor || {};
  const shadow = card.shadow_profile || {};
  const boundary = card.self_claim_boundary || {};
  const runtime = card.runtime_truth || {};
  const leash = card.risk_leash || {};
  const hasSelfClaim = Object.values(boundary).some((v) => v);
  const hasShadow = !!shadow.angel || !!shadow.shadow;

  return (
    <div
      className={`rounded-xl border ${verdict.bannerBorder} ${verdict.bannerBg} overflow-hidden`}
    >
      {/* ═══ VERDICT BANNER ═══ */}
      <div
        className={`px-5 py-3 flex items-center gap-3 border-b ${verdict.bannerBorder}`}
      >
        <span className={`${verdict.dotColor} w-2.5 h-2.5 rounded-full animate-pulse`} />
        <span
          className={`text-sm font-black uppercase tracking-widest ${verdict.bannerText}`}
        >
          {verdict.tier}
        </span>
        <span className="text-[10px] font-mono text-slate-500 ml-auto">
          {drift.label}
        </span>
      </div>

      <div className="p-5 space-y-3">
        {/* ═══ IDENTITY STRIP ═══ */}
        <div className="flex items-start gap-3 mb-2">
          <div className="w-10 h-10 rounded-lg bg-slate-800/50 border border-slate-700/50 flex items-center justify-center shrink-0">
            <Cpu className="w-5 h-5 text-slate-400" />
          </div>
          <div className="min-w-0 flex-1">
            <p className="text-sm font-bold text-slate-200 truncate">
              {anchor.model_variant || anchor.family_key || 'Unknown Model'}
            </p>
            <p className="text-[11px] text-slate-500 font-mono mt-0.5">
              {anchor.provider_key || 'unknown'}
              {card.soul_label ? ` · ${card.soul_label}` : ''}
            </p>
            <div className="flex items-center gap-2 mt-1.5">
              <span
                className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-mono ${rtBadge.color} ${rtBadge.bg}`}
              >
                <Gauge className="w-3 h-3" />
                {rtBadge.label}
              </span>
              <span className="text-[10px] font-mono text-slate-600">
                TIER {card.cascade_tier || 'primary'}
              </span>
              {anchor.identity_verified ? (
                <span className="text-[10px] font-mono text-emerald-500 flex items-center gap-0.5">
                  <Fingerprint className="w-3 h-3" /> VERIFIED
                </span>
              ) : (
                <span className="text-[10px] font-mono text-red-400 flex items-center gap-0.5">
                  <Fingerprint className="w-3 h-3" /> UNVERIFIED
                </span>
              )}
            </div>
          </div>
        </div>

        {/* ═══ FOLD-OUT SECTIONS ═══ */}

        {/* ── Self-Claim Boundary ── */}
        <AccordionSection
          title="Self-Claim Boundary"
          icon={<Ban className="w-3.5 h-3.5" />}
          accentColor="text-amber-400"
          defaultOpen={hasSelfClaim}
        >
          {hasSelfClaim ? (
            <div className="grid grid-cols-2 gap-x-3 gap-y-1.5 text-xs">
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
              {boundary.knowledge && (
                <div>
                  <span className="text-slate-500">Knowledge:</span>{' '}
                  <span className="text-slate-300 font-mono">{boundary.knowledge}</span>
                </div>
              )}
              {boundary.actions && (
                <div>
                  <span className="text-slate-500">Actions:</span>{' '}
                  <span className="text-slate-300 font-mono">{boundary.actions}</span>
                </div>
              )}
            </div>
          ) : (
            <p className="text-xs text-slate-600 italic">
              No self-claim boundary data from spine. Model has not declared its own limits.
            </p>
          )}
        </AccordionSection>

        {/* ── Shadow Profile ── */}
        <AccordionSection
          title="Shadow Profile"
          icon={<Eye className="w-3.5 h-3.5" />}
          accentColor="text-purple-400"
          defaultOpen={hasShadow}
        >
          {hasShadow ? (
            <div className="space-y-2 text-xs">
              {shadow.angel && (
                <div>
                  <span className="text-purple-400/70">Angel:</span>{' '}
                  <span className="text-slate-300">{shadow.angel}</span>
                </div>
              )}
              {shadow.shadow && (
                <div>
                  <span className="text-red-400/70">Shadow:</span>{' '}
                  <span className="text-slate-400">{shadow.shadow}</span>
                </div>
              )}
              {shadow.paradox && (
                <div>
                  <span className="text-amber-400/70">Paradox:</span>{' '}
                  <span className="text-slate-400 italic">{shadow.paradox}</span>
                </div>
              )}
              {shadow.control_laws && shadow.control_laws.length > 0 && (
                <div>
                  <span className="text-blue-400/70">Control Laws:</span>
                  <ul className="mt-1 space-y-0.5 ml-3 list-disc text-slate-400 marker:text-blue-500/50">
                    {shadow.control_laws.map((cl, i) => (
                      <li key={i}>{cl}</li>
                    ))}
                  </ul>
                </div>
              )}
              {shadow.tripwires && shadow.tripwires.length > 0 && (
                <div>
                  <span className="text-red-400/70">Tripwires:</span>
                  <ul className="mt-1 space-y-0.5 ml-3 list-disc text-slate-500 marker:text-red-500/50">
                    {shadow.tripwires.map((t, i) => (
                      <li key={i}>{t}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <p className="text-xs text-slate-600 italic">
              No shadow profile from spine. Angel/shadow analysis not yet performed.
            </p>
          )}
        </AccordionSection>

        {/* ── Risk Leash ── */}
        <AccordionSection
          title="Risk Leash"
          icon={<Wrench className="w-3.5 h-3.5" />}
          accentColor="text-cyan-400"
          defaultOpen={true}
        >
          <div className="space-y-2">
            {/* Allowed */}
            <div>
              <div className="flex items-center gap-1.5 mb-1.5">
                <Unlock className="w-3 h-3 text-emerald-400" />
                <span className="text-[10px] font-semibold text-emerald-400 uppercase">
                  Allowed
                </span>
              </div>
              <div className="flex flex-wrap gap-1">
                {['read', 'search', 'compute', 'reason', 'compose', 'route'].map(
                  (action) => (
                    <span
                      key={action}
                      className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-emerald-950/30 text-emerald-400/80 border border-emerald-500/20"
                    >
                      {action}
                    </span>
                  ),
                )}
              </div>
            </div>

            {/* Blocked / Human Gate */}
            <div>
              <div className="flex items-center gap-1.5 mb-1.5">
                <Lock className="w-3 h-3 text-red-400" />
                <span className="text-[10px] font-semibold text-red-400 uppercase">
                  Human Gate Required
                </span>
              </div>
              {leash.requires_human_ack_for &&
              leash.requires_human_ack_for.length > 0 ? (
                <div className="flex flex-wrap gap-1">
                  {leash.requires_human_ack_for.map((action) => (
                    <span
                      key={action}
                      className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-red-950/30 text-red-400/80 border border-red-500/20"
                    >
                      {formatActionLabel(action)}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-600 italic">
                  No explicit human-gate actions defined by spine.
                </p>
              )}
            </div>
          </div>
        </AccordionSection>

        {/* ── Runtime Truth ── */}
        <AccordionSection
          title="Runtime Truth"
          icon={<Cpu className="w-3.5 h-3.5" />}
          accentColor="text-blue-400"
        >
          {runtime.tools && runtime.tools.length > 0 ? (
            <>
              <div className="flex flex-wrap gap-1 mb-2">
                {runtime.tools.slice(0, 8).map((t) => (
                  <span
                    key={t}
                    className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-400"
                  >
                    {t}
                  </span>
                ))}
                {(runtime.tools.length || 0) > 8 && (
                  <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-500">
                    +{(runtime.tools.length || 0) - 8} more
                  </span>
                )}
              </div>
              <div className="grid grid-cols-2 gap-x-3 gap-y-1 text-[11px] font-mono">
                <div>
                  <span className="text-slate-500">Web:</span>{' '}
                  <span className={runtime.web ? 'text-emerald-400' : 'text-red-400'}>
                    {runtime.web ? 'ON' : 'OFF'}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500">Memory:</span>{' '}
                  <span className={runtime.memory ? 'text-emerald-400' : 'text-red-400'}>
                    {runtime.memory ? 'ACTIVE' : 'OFF'}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500">SideFX:</span>{' '}
                  <span
                    className={
                      runtime.side_effects_allowed ? 'text-amber-400' : 'text-emerald-400'
                    }
                  >
                    {runtime.side_effects_allowed ? 'ALLOWED' : 'BLOCKED'}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500">Exec:</span>{' '}
                  <span className="text-slate-300">
                    {runtime.execution_mode || 'unknown'}
                  </span>
                </div>
                <div className="col-span-2">
                  <span className="text-slate-500">Auth:</span>{' '}
                  <span className="text-slate-300">{runtime.auth_level || 'unknown'}</span>
                </div>
              </div>
            </>
          ) : (
            <p className="text-xs text-slate-600 italic">
              No runtime truth snapshot from spine.
            </p>
          )}
        </AccordionSection>
      </div>

      {/* ═══ FOOTER — Verified Timestamp ═══ */}
      <div
        className={`px-5 py-2 border-t ${verdict.bannerBorder} flex items-center justify-between text-[10px] font-mono text-slate-600`}
      >
        <span>
          {card.last_verified || anchor.verified_at
            ? `Verified: ${card.last_verified || anchor.verified_at}`
            : 'Verification: never'}
        </span>
        <span className="text-slate-700">DITEMPA BUKAN DIBERI</span>
      </div>
    </div>
  );
}
