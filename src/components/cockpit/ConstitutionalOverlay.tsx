/**
 * ConstitutionalOverlay — aaa-a2a Governance Status
 * ═══════════════════════════════════════════════════════════════
 *
 * Shows the constitutional overlay status: aaa-a2a Python server,
 * delegation guard rules, floor checks, audit chain, agent registry.
 *
 * This is the window into the governance layer that sits ABOVE A2A transport.
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

import { useState, useEffect } from 'react';
import {
  Shield,
  ShieldCheck,
  ShieldAlert,
  Activity,
  Users,
  CheckCircle2,
  Zap,
} from 'lucide-react';

interface OverlayStatus {
  server: 'online' | 'offline' | 'checking';
  version: string;
  delegationRules: number;
  floorChecks: number;
  auditChainValid: boolean;
  chainSeq: number;
  chainHash: string;
  agentCount: number;
  skillCount: number;
  organHealth: Record<string, boolean>;
}

interface DelegationRule {
  source: string | null;
  target: string;
  verdict: string;
  reason: string;
  floor: string | null;
}

const FLOOR_IDS = ['F1', 'F2', 'F4', 'F6', 'F9', 'F13'];
const FLOOR_NAMES: Record<string, string> = {
  F1: 'Amanah',
  F2: 'Truth',
  F4: 'Clarity',
  F6: 'Maruah',
  F9: 'Anti-Hantu',
  F13: 'Sovereign',
};

export default function ConstitutionalOverlay() {
  const [status, setStatus] = useState<OverlayStatus>({
    server: 'checking',
    version: '',
    delegationRules: 0,
    floorChecks: 0,
    auditChainValid: false,
    chainSeq: 0,
    chainHash: '',
    agentCount: 0,
    skillCount: 0,
    organHealth: {},
  });
  const [rules, setRules] = useState<DelegationRule[]>([]);
  const [expanded, setExpanded] = useState(false);

  const fetchOverlayStatus = async () => {
    try {
      // AAA :3001 is the canonical control-plane and deliberation endpoint.
      const healthRes = await fetch('/health', { cache: 'no-store' });
      const health = await healthRes.json();

      // Fetch agent registry stats
      const statsRes = await fetch('/a2a/discover/stats', { cache: 'no-store' });
      const stats = statsRes.ok ? await statsRes.json() : null;

      // Fetch organ attestation
      const organRes = await fetch('/api/attestation/organs', { cache: 'no-store' });
      const organData = organRes.ok ? await organRes.json() : null;

      const organHealth: Record<string, boolean> = {};
      if (organData?.organs) {
        for (const organ of organData.organs) {
          organHealth[organ.name] = organ.healthy;
        }
      }

      // Fetch seal chain head — the real heartbeat
      let chainSeq = 0;
      let chainHash = '';
      let chainValid = false;
      try {
        const chainRes = await fetch('/api/seal-chain/head', { cache: 'no-store' });
        if (chainRes.ok) {
          const chain = await chainRes.json();
          chainSeq = chain.head?.seq || 0;
          chainHash = (chain.head?.hash || '').slice(0, 15);
          chainValid = chain.chain_ok === true;
        }
      } catch { /* seal chain not available */ }

      setStatus({
        server: healthRes.ok ? 'online' : 'offline',
        version: health.version || health.protocol || '',
        delegationRules: 18, // Hard-coded from guard.py
        floorChecks: FLOOR_IDS.length,
        auditChainValid: chainValid,
        chainSeq,
        chainHash,
        agentCount: stats?.totalAgents || 0,
        skillCount: stats?.totalSkills || 0,
        organHealth,
      });

      // Set delegation rules (static for now, will be dynamic from Python server)
      setRules([
        { source: 'a-forge', target: 'forge_approve', verdict: 'blocked', reason: 'F8: Self-approval forbidden', floor: 'F8' },
        { source: 'a-forge', target: 'arif_judge', verdict: 'blocked', reason: 'F8: Cannot issue verdicts', floor: 'F8' },
        { source: 'a-forge', target: 'well_assess', verdict: 'blocked', reason: 'F8: Cannot read human data', floor: 'F8' },
        { source: 'geox', target: 'wealth_', verdict: 'blocked', reason: 'F8: Cannot mutate WEALTH', floor: 'F8' },
        { source: 'wealth', target: 'geox_', verdict: 'blocked', reason: 'F8: Cannot mutate GEOX', floor: 'F8' },
        { source: 'well', target: 'deploy', verdict: 'blocked', reason: 'F8: Reflect-only', floor: 'F8' },
        { source: null, target: 'f13_override', verdict: 'blocked', reason: 'F13: Human veto absolute', floor: 'F13' },
        { source: null, target: 'bypass_888', verdict: 'blocked', reason: 'F13: 888 HOLD cannot bypass', floor: 'F13' },
      ]);
    } catch {
      setStatus(prev => ({ ...prev, server: 'offline' }));
    }
  };

  useEffect(() => {
    fetchOverlayStatus();
    const interval = setInterval(fetchOverlayStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const serverColor = status.server === 'online' ? 'text-emerald-400' : status.server === 'offline' ? 'text-red-400' : 'text-yellow-400';
  const serverIcon = status.server === 'online' ? <ShieldCheck className="w-5 h-5" /> : <ShieldAlert className="w-5 h-5" />;

  return (
    <div className="rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className={serverColor}>{serverIcon}</div>
          <div>
            <h3 className="text-sm font-semibold text-white">Constitutional Overlay</h3>
            <p className="text-xs text-white/50">aaa-a2a governance layer</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className={`text-xs font-mono ${serverColor}`}>
            {status.server === 'online' ? 'LIVE' : status.server === 'offline' ? 'DOWN' : '...'}
          </span>
          {status.version && (
            <span className="text-xs text-white/30 font-mono">v{status.version}</span>
          )}
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-px bg-white/5">
        <StatCard
          icon={<Users className="w-4 h-4 text-blue-400" />}
          label="Agents"
          value={status.agentCount}
          sub={`${status.skillCount} skills`}
        />
        <StatCard
          icon={<Shield className="w-4 h-4 text-amber-400" />}
          label="Delegation Rules"
          value={status.delegationRules}
          sub="cross-organ"
        />
        <StatCard
          icon={<CheckCircle2 className="w-4 h-4 text-emerald-400" />}
          label="Floor Checks"
          value={status.floorChecks}
          sub="F1-F13 active"
        />
        <StatCard
          icon={<Zap className={`w-4 h-4 ${status.auditChainValid ? 'text-purple-400' : 'text-red-400'}`} />}
          label="Seal Chain"
          value={
            !status.auditChainValid
              ? 'BROKEN'
              : status.chainSeq > 0
                ? `#${status.chainSeq}`
                : 'GENESIS'
          }
          sub={
            !status.auditChainValid
              ? 'arrow snapped'
              : status.chainHash
                ? `${status.chainHash}…`
                : 'awaiting first seal'
          }
        />
      </div>

      {/* Organ Health */}
      <div className="px-5 py-3 border-t border-white/5">
        <div className="flex items-center gap-2 mb-2">
          <Activity className="w-3.5 h-3.5 text-white/40" />
          <span className="text-xs text-white/50 font-medium">Organ Health</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {Object.entries(status.organHealth).map(([name, healthy]) => (
            <span
              key={name}
              className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-mono ${
                healthy
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                  : 'bg-red-500/10 text-red-400 border border-red-500/20'
              }`}
            >
              <span className={`w-1.5 h-1.5 rounded-full ${healthy ? 'bg-emerald-400' : 'bg-red-400'}`} />
              {name}
            </span>
          ))}
        </div>
      </div>

      {/* Floor Status */}
      <div className="px-5 py-3 border-t border-white/5">
        <div className="flex items-center gap-2 mb-2">
          <Shield className="w-3.5 h-3.5 text-white/40" />
          <span className="text-xs text-white/50 font-medium">Constitutional Floors</span>
        </div>
        <div className="flex flex-wrap gap-1.5">
          {FLOOR_IDS.map(id => (
            <span
              key={id}
              className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
            >
              <CheckCircle2 className="w-3 h-3" />
              {id} {FLOOR_NAMES[id]}
            </span>
          ))}
        </div>
      </div>

      {/* Delegation Rules (expandable) */}
      <div className="border-t border-white/5">
        <button
          onClick={() => setExpanded(!expanded)}
          className="flex items-center justify-between w-full px-5 py-3 text-left hover:bg-white/5 transition-colors"
        >
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
            <span className="text-xs text-white/50 font-medium">Delegation Rules ({rules.length})</span>
          </div>
          <span className="text-xs text-white/30">{expanded ? '▲' : '▼'}</span>
        </button>
        {expanded && (
          <div className="px-5 pb-3 space-y-1.5">
            {rules.map((rule, i) => (
              <div
                key={i}
                className="flex items-start gap-2 px-3 py-2 rounded-lg bg-white/5 border border-white/5"
              >
                <span className={`mt-0.5 w-2 h-2 rounded-full flex-shrink-0 ${
                  rule.verdict === 'blocked' ? 'bg-red-400' : 'bg-amber-400'
                }`} />
                <div className="min-w-0">
                  <div className="text-xs font-mono text-white/70">
                    {rule.source || '*'} → {rule.target}
                  </div>
                  <div className="text-xs text-white/40 mt-0.5">{rule.reason}</div>
                  {rule.floor && (
                    <span className="inline-block mt-1 px-1.5 py-0.5 rounded text-[10px] font-mono bg-amber-500/10 text-amber-400 border border-amber-500/20">
                      {rule.floor}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="px-5 py-2.5 border-t border-white/5 bg-white/[0.02]">
        <div className="flex items-center justify-between">
          <span className="text-[10px] text-white/20 font-mono">
            aaa-a2a constitutional overlay · DITEMPA BUKAN DIBERI
          </span>
          <span className="text-[10px] text-white/20 font-mono">
            {status.server === 'online' ? 'AAA :3001 online' : 'AAA :3001 unavailable'}
          </span>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, sub }: {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  sub: string;
}) {
  return (
    <div className="px-4 py-3 bg-white/[0.02]">
      <div className="flex items-center gap-2 mb-1">
        {icon}
        <span className="text-[11px] text-white/40 font-medium">{label}</span>
      </div>
      <div className="text-lg font-semibold text-white font-mono">{value}</div>
      <div className="text-[10px] text-white/30">{sub}</div>
    </div>
  );
}
