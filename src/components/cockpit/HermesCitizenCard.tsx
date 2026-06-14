import { Shield, Zap, Eye, Cpu, Activity, CheckCircle2, AlertTriangle, ChevronRight } from 'lucide-react';

interface RightsBundle {
  id: string;
  label: string;
  description: string;
  granted: boolean;
}

interface McpStatus {
  name: string;
  transport: string;
  status: 'connected' | 'degraded' | 'down';
}

const RIGHTS_BUNDLES: RightsBundle[] = [
  {
    id: 'A',
    label: 'Cognitive',
    description: 'Reason, summarize, decompose, plan, generate skills, Kanban task graphs',
    granted: true,
  },
  {
    id: 'B',
    label: 'Evidence',
    description: 'Cross-organ observation, fetch, discovery via arifOS kernel route',
    granted: true,
  },
  {
    id: 'C',
    label: 'Execution',
    description: 'A-FORGE actions — Tier 0-1 auto-pass, Tier 2 needs plan, Tier 3 888_HOLD',
    granted: true,
  },
  {
    id: 'D',
    label: 'Protection',
    description: 'Auditable, attributable, interruptible, revocable. No self-escalation.',
    granted: true,
  },
];

const MCP_SERVERS: McpStatus[] = [
  { name: 'arifOS', transport: 'streamable-http :8090', status: 'connected' },
  { name: 'A-FORGE', transport: 'streamable-http :18081', status: 'connected' },
  { name: 'GEOX', transport: 'streamable-http :8081', status: 'connected' },
  { name: 'WEALTH', transport: 'streamable-http :18082', status: 'connected' },
  { name: 'WELL', transport: 'streamable-http :18083', status: 'connected' },
  { name: 'Playwright', transport: 'stdio :8931', status: 'connected' },
  { name: 'agentmail', transport: 'npx', status: 'connected' },
  { name: 'Supabase', transport: 'npx', status: 'connected' },
  { name: 'Hostinger', transport: 'script', status: 'connected' },
  { name: 'GitHub', transport: 'npx', status: 'connected' },
  { name: 'PostgreSQL', transport: 'npx', status: 'connected' },
  { name: 'Brave Search', transport: 'npx', status: 'connected' },
  { name: 'Time', transport: 'npx', status: 'connected' },
  { name: 'Seq Thinking', transport: 'npx', status: 'connected' },
  { name: 'Composio', transport: 'venv', status: 'connected' },
  { name: 'MiniMax Code', transport: 'sse :18091', status: 'connected' },
  { name: 'MiniMax Media', transport: 'sse :18090', status: 'connected' },
  { name: 'Perplexity', transport: 'npx', status: 'connected' },
  { name: 'Cloudflare', transport: 'npx', status: 'connected' },
];

const HOLD_SCOPE = [
  'Cross-organ autonomous composition (GEOX→WEALTH→WELL)',
  'Production deploy without verified build pass',
  'External comms to non-federation third parties',
  'Constitutional file mutation (F1-F13, GENESIS/)',
  'Destructive infra (rm -rf /, DROP DATABASE)',
];

export default function HermesCitizenCard() {
  const connectedCount = MCP_SERVERS.filter((m) => m.status === 'connected').length;
  const allConnected = connectedCount === MCP_SERVERS.length;

  return (
    <div className="border border-white/10 rounded-xl bg-black/40 backdrop-blur-sm overflow-hidden">
      {/* Header — Citizen Identity */}
      <div className="px-5 py-4 border-b border-white/10 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/20 flex items-center justify-center">
            <Cpu className="w-4 h-4 text-emerald-400" />
          </div>
          <div>
            <div className="text-white/90 font-semibold text-sm">Hermes ASI</div>
            <div className="text-white/30 text-[10px] font-mono uppercase tracking-wider">
              Sovereign Citizen · AAA
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <div
            className={`w-2 h-2 rounded-full ${allConnected ? 'bg-emerald-400' : 'bg-amber-400'} animate-pulse`}
          />
          <span className="text-white/30 text-[10px] font-mono uppercase">
            {allConnected ? 'ALL SYSTEMS NOMINAL' : `${connectedCount}/${MCP_SERVERS.length}`}
          </span>
        </div>
      </div>

      {/* Rights Bundles */}
      <div className="px-5 py-3 border-b border-white/5">
        <div className="text-white/30 text-[10px] font-mono uppercase tracking-widest mb-2">
          Rights Bundles — F13 SOVEREIGN GRANTED
        </div>
        <div className="grid grid-cols-2 gap-2">
          {RIGHTS_BUNDLES.map((bundle) => (
            <div
              key={bundle.id}
              className="flex items-start gap-2 p-2 rounded-lg bg-white/[0.02] border border-white/5"
            >
              <div className="w-5 h-5 rounded bg-emerald-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                <CheckCircle2 className="w-3 h-3 text-emerald-400" />
              </div>
              <div>
                <div className="text-white/70 text-[11px] font-semibold">
                  {bundle.id}. {bundle.label}
                </div>
                <div className="text-white/30 text-[10px] leading-relaxed">
                  {bundle.description}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Model Stack */}
      <div className="px-5 py-3 border-b border-white/5">
        <div className="text-white/30 text-[10px] font-mono uppercase tracking-widest mb-2">
          Model Rotation Loop
        </div>
        <div className="flex items-center gap-1.5 text-[10px] font-mono">
          <span className="text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">
            DeepSeek v4-pro
          </span>
          <ChevronRight className="w-3 h-3 text-white/20" />
          <span className="text-white/50 bg-white/5 px-2 py-0.5 rounded">
            MiniMax M3
          </span>
          <ChevronRight className="w-3 h-3 text-white/20" />
          <span className="text-white/50 bg-white/5 px-2 py-0.5 rounded">
            Ilmu Nano
          </span>
          <span className="text-white/20 ml-1">↻ auto</span>
        </div>
      </div>

      {/* MCP Server Grid */}
      <div className="px-5 py-3 border-b border-white/5">
        <div className="text-white/30 text-[10px] font-mono uppercase tracking-widest mb-2">
          MCP Servers ({connectedCount})
        </div>
        <div className="grid grid-cols-4 gap-1">
          {MCP_SERVERS.map((mcp) => (
            <div
              key={mcp.name}
              className="flex items-center gap-1.5 px-2 py-1 rounded text-[10px] font-mono bg-white/[0.02]"
            >
              <div
                className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${
                  mcp.status === 'connected'
                    ? 'bg-emerald-400'
                    : mcp.status === 'degraded'
                      ? 'bg-amber-400'
                      : 'bg-red-400'
                }`}
              />
              <span className="text-white/60 truncate">{mcp.name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* 888 HOLD Scope */}
      <div className="px-5 py-3 border-b border-white/5">
        <div className="text-white/30 text-[10px] font-mono uppercase tracking-widest mb-2 flex items-center gap-1.5">
          <Shield className="w-3 h-3" />
          888 HOLD Triggers
        </div>
        <div className="space-y-1">
          {HOLD_SCOPE.map((item, i) => (
            <div key={i} className="flex items-start gap-2 text-[10px] text-white/40">
              <AlertTriangle className="w-3 h-3 text-amber-400/50 flex-shrink-0 mt-0.5" />
              <span>{item}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Footer — Operational Stats */}
      <div className="px-5 py-3 flex items-center justify-between text-[10px] font-mono text-white/20">
        <div className="flex items-center gap-4">
          <span>
            Toolsets: <span className="text-white/40">17</span>
          </span>
          <span>
            Skills: <span className="text-white/40">130+</span>
          </span>
          <span>
            Rotation:{' '}
            <span className="text-emerald-400/60">active</span>
          </span>
        </div>
        <div className="flex items-center gap-2">
          <Activity className="w-3 h-3 text-emerald-400/50" />
          <span className="text-emerald-400/50">LIVE</span>
        </div>
      </div>
    </div>
  );
}
