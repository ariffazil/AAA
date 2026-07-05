/**
 * Autonomy Bands — Reconstruction A Foundation / Track 4
 * ═══════════════════════════════════════════════════════════════
 *
 * Visualizes the constitutional autonomy gradient for the federation.
 * Maps tools to risk bands: Green → Yellow → Orange → Red → Black.
 *
 * DITEMPA BUKAN DIBERI
 */

import { Shield, Eye, FlaskConical, PenTool, Bomb, Skull } from 'lucide-react';

type BandKey = 'green' | 'yellow' | 'orange' | 'red' | 'black';

interface BandDef {
  key: BandKey;
  label: string;
  actionClass: string;
  description: string;
  icon: React.ReactNode;
  textColor: string;
  bgColor: string;
  borderColor: string;
  dotColor: string;
}

const BANDS: BandDef[] = [
  {
    key: 'green',
    label: 'OBSERVE',
    actionClass: 'READ / INSPECT / SUMMARIZE',
    description: 'Auto-allow. No receipts required.',
    icon: <Eye className="w-4 h-4" />,
    textColor: 'text-emerald-500',
    bgColor: 'bg-emerald-950/20',
    borderColor: 'border-emerald-500/30',
    dotColor: 'bg-emerald-500',
  },
  {
    key: 'yellow',
    label: 'PREPARE',
    actionClass: 'PLAN / DRY-RUN / VALIDATE',
    description: 'Auto-allow with receipt. No human gate.',
    icon: <FlaskConical className="w-4 h-4" />,
    textColor: 'text-blue-400',
    bgColor: 'bg-blue-950/20',
    borderColor: 'border-blue-500/30',
    dotColor: 'bg-blue-400',
  },
  {
    key: 'orange',
    label: 'MUTATE',
    actionClass: 'WRITE / MODIFY / EXECUTE',
    description: 'Gated. Requires observe receipt + verified authority.',
    icon: <PenTool className="w-4 h-4" />,
    textColor: 'text-amber-500',
    bgColor: 'bg-amber-950/20',
    borderColor: 'border-amber-500/30',
    dotColor: 'bg-amber-500',
  },
  {
    key: 'red',
    label: 'ATOMIC',
    actionClass: 'DEPLOY / SEAL / IRREVERSIBLE',
    description: 'Requires Arif ack (F13) + verified authority.',
    icon: <Bomb className="w-4 h-4" />,
    textColor: 'text-red-500',
    bgColor: 'bg-red-950/20',
    borderColor: 'border-red-500/30',
    dotColor: 'bg-red-500',
  },
  {
    key: 'black',
    label: 'VOID',
    actionClass: 'DESTRUCTIVE / UNRECOVERABLE',
    description: 'Default VOID. Extraordinary sovereign approval only.',
    icon: <Skull className="w-4 h-4" />,
    textColor: 'text-white/60',
    bgColor: 'bg-neutral-950/40',
    borderColor: 'border-white/10',
    dotColor: 'bg-white/40',
  },
];

// Canonical tool risk map — mirrors Python risk_classifier.py
const TOOL_BAND_MAP: Record<string, BandKey> = {
  // Green — OBSERVE
  'arif_sense_observe': 'green',
  'arif_ops_measure': 'green',
  'arif_reply_compose': 'green',
  'arif_evidence_fetch': 'green',
  'arif_ping': 'green',
  'arif_selftest': 'green',
  'arif_stack_health_probe': 'green',
  'arif_scan_local_instructions': 'green',
  'arif_session_budget': 'green',
  'arif_floor_status': 'green',
  'arif_mcp_drift_check': 'green',
  'arif_wiki_map': 'green',
  'arif_wiki_search': 'green',
  'arif_wiki_ask': 'green',
  // Yellow — PREPARE
  'arif_mind_reason': 'yellow',
  'arif_wiki_ingest': 'yellow',
  // Orange — MUTATE
  'arif_kernel_route': 'orange',
  'arif_gateway_connect': 'orange',
  'arif_memory_recall': 'orange',
  // Red — ATOMIC
  'arif_forge_execute': 'red',
  'arif_judge_deliberate': 'red',
  'arif_vault_seal': 'red',
  'arif_heart_critique': 'red',
  'arif_session_init': 'red',
};

function classifyTool(name: string): BandKey {
  // Exact match
  if (TOOL_BAND_MAP[name]) return TOOL_BAND_MAP[name];
  // Prefix match for organ namespaced tools
  if (name.startsWith('geox.') || name.startsWith('geox_')) return 'orange';
  if (name.startsWith('wealth.') || name.startsWith('wealth_')) return 'orange';
  if (name.startsWith('well.') || name.startsWith('well_')) return 'green';
  if (name.startsWith('forge.') || name.startsWith('forge_')) return 'orange';
  // Default heuristic
  const lower = name.toLowerCase();
  if (lower.includes('delete') || lower.includes('drop') || lower.includes('wipe')) return 'black';
  if (lower.includes('deploy') || lower.includes('seal') || lower.includes('judge')) return 'red';
  if (lower.includes('write') || lower.includes('modify') || lower.includes('update') || lower.includes('execute')) return 'orange';
  if (lower.includes('plan') || lower.includes('validate') || lower.includes('check')) return 'yellow';
  if (lower.includes('read') || lower.includes('get') || lower.includes('list') || lower.includes('view')) return 'green';
  return 'green';
}

interface ToolItem {
  name: string;
  requires_888?: boolean;
}

interface AutonomyBandsProps {
  tools?: ToolItem[];
}

export default function AutonomyBands({ tools = [] }: AutonomyBandsProps) {
  // Group tools by band
  const bandTools: Record<BandKey, string[]> = {
    green: [],
    yellow: [],
    orange: [],
    red: [],
    black: [],
  };

  for (const t of tools) {
    const band = classifyTool(t.name);
    bandTools[band].push(t.name);
  }

  // Counts
  const counts = BANDS.map(b => ({
    ...b,
    count: bandTools[b.key].length,
  }));

  const total = tools.length;

  return (
    <section className="mb-24">
      <div className="flex items-baseline gap-4 mb-10">
        <span className="text-4xl font-black text-white/10 font-mono italic">Λ.</span>
        <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Autonomy Bands</h2>
        <span className="text-[9px] font-mono text-white/30 uppercase tracking-widest">
          {total} tools classified
        </span>
      </div>

      {/* Band bars */}
      <div className="space-y-3 mb-10">
        {counts.map(band => {
          const pct = total > 0 ? Math.round((band.count / total) * 100) : 0;
          return (
            <div
              key={band.key}
              className={`relative border ${band.borderColor} ${band.bgColor} rounded-sm overflow-hidden`}
            >
              {/* Progress fill */}
              <div
                className={`absolute inset-y-0 left-0 ${band.dotColor} opacity-20 transition-all duration-500`}
                style={{ width: `${pct}%` }}
              />
              <div className="relative flex items-center justify-between px-4 py-3">
                <div className="flex items-center gap-3">
                  <div className={`${band.textColor}`}>{band.icon}</div>
                  <div>
                    <div className={`text-xs font-mono font-bold uppercase tracking-widest ${band.textColor}`}>
                      {band.label}
                    </div>
                    <div className="text-[9px] font-mono text-white/40 tracking-wider">
                      {band.actionClass}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <div className={`text-lg font-mono font-black ${band.textColor}`}>
                      {band.count}
                    </div>
                    <div className="text-[9px] font-mono text-white/30 uppercase tracking-widest">
                      {band.description}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Tool listing by band */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {counts
          .filter(b => b.count > 0)
          .map(band => (
            <div key={band.key} className={`border ${band.borderColor} ${band.bgColor} p-4`}>
              <div className="flex items-center gap-2 mb-3">
                <div className={`w-1.5 h-1.5 rounded-full ${band.dotColor}`} />
                <span className={`text-[10px] font-mono font-bold uppercase tracking-widest ${band.textColor}`}>
                  {band.label}
                </span>
                <span className="text-[9px] font-mono text-white/30">({band.count})</span>
              </div>
              <div className="space-y-1">
                {bandTools[band.key].map(name => (
                  <code
                    key={name}
                    className="block text-[10px] font-mono text-white/50 truncate"
                    title={name}
                  >
                    {name}
                  </code>
                ))}
              </div>
            </div>
          ))}
      </div>

      {/* Legend */}
      <div className="mt-8 flex flex-wrap items-center gap-4 text-[9px] font-mono text-white/30 uppercase tracking-widest">
        <div className="flex items-center gap-1.5">
          <Shield className="w-3 h-3 text-white/20" />
          <span>Federation envelope required for Orange+</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Eye className="w-3 h-3 text-white/20" />
          <span>Legacy clients auto-allow Green/Yellow only</span>
        </div>
      </div>
    </section>
  );
}
