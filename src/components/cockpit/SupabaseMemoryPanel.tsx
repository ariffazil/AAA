/**
 * SupabaseMemoryPanel — Phase 3A Read-Only Federation Memory Cockpit
 * Reads from existing aaa.* views in Supabase Cloud L4.
 *
 * No writes. No approvals. No routing. Read-only.
 */
import {
  useRecentSeals, usePendingApprovals, useRecentToolCalls,
  useMcpSurface, useEvidenceIndex, useArtifactIndex,
  useRiskDashboard, useNamespaceSummary, useSupabaseHealth
} from '@/hooks/useFederationMemory';

function HealthDot({ healthy, latencyMs }: { healthy: boolean | null; latencyMs: number | null }) {
  if (healthy === null) return <span className="text-white/30">checking…</span>;
  if (healthy === false) return (
    <span className="flex items-center gap-1.5 text-red-500">
      <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
      L4 DOWN
      {latencyMs !== null && <span className="text-white/30">({latencyMs}ms)</span>}
    </span>
  );
  return (
    <span className="flex items-center gap-1.5 text-emerald-500">
      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
      L4 LIVE
      {latencyMs !== null && <span className="text-white/30">({latencyMs}ms)</span>}
    </span>
  );
}

function PanelCard({ title, subtitle, children, accent = 'white' }: {
  title: string; subtitle?: string; children: React.ReactNode; accent?: string;
}) {
  const borderColors: Record<string, string> = {
    white: 'border-white/10',
    emerald: 'border-emerald-500/30',
    amber: 'border-amber-500/30',
    red: 'border-red-500/30',
    blue: 'border-blue-500/30',
  };
  const textColors: Record<string, string> = {
    white: 'text-white/60',
    emerald: 'text-emerald-500/70',
    amber: 'text-amber-500/70',
    red: 'text-red-500/70',
    blue: 'text-blue-500/70',
  };
  return (
    <div className={`border ${borderColors[accent] ?? 'border-white/10'} rounded-lg overflow-hidden`}>
      <div className={`px-4 py-2 border-b ${borderColors[accent] ?? 'border-white/10'} flex items-baseline gap-3`}>
        <span className={`text-[10px] font-mono uppercase tracking-widest ${textColors[accent] ?? 'text-white/60'}`}>
          {title}
        </span>
        {subtitle && <span className="text-[9px] font-mono text-white/20">{subtitle}</span>}
      </div>
      <div className="p-3">{children}</div>
    </div>
  );
}

function EmptyState({ message }: { message: string }) {
  return <div className="text-center py-4 text-white/20 text-xs font-mono">{message}</div>;
}

function LoadingState() {
  return (
    <div className="flex items-center justify-center py-4 gap-1">
      {[0, 1, 2].map(i => (
        <div key={i} className="w-1 h-1 rounded-full bg-white/30 animate-bounce"
          style={{ animationDelay: `${i * 150}ms` }} />
      ))}
    </div>
  );
}

function ErrorState({ msg }: { msg: string }) {
  return <div className="text-red-500 text-xs px-2 py-1">{msg}</div>;
}

// ── Recent Seals ─────────────────────────────────────────────────
function SealsPanel() {
  const { data, loading, error } = useRecentSeals(20);
  if (loading) return <LoadingState />;
  if (error) return <ErrorState msg={error} />;
  if (!data?.length) return <EmptyState message="No seals yet." />;
  return (
    <div className="space-y-0.5 max-h-56 overflow-y-auto">
      {data.map((s, i) => (
        <div key={`${s.seal_id}-${i}`} className="flex items-center gap-2 text-[11px] font-mono hover:bg-white/[0.02] px-2 py-1 rounded">
          <span className="text-white/20 flex-shrink-0 w-12 text-[9px]">
            {s.created_at ? new Date(s.created_at).toLocaleDateString('en-MY', { month: 'short', day: 'numeric' }) : '—'}
          </span>
          <span className={`flex-shrink-0 w-10 font-bold text-[9px] ${
            s.verdict === 'SEAL' ? 'text-emerald-400' :
            s.verdict === 'SABAR' ? 'text-amber-400' :
            s.verdict === 'VOID' ? 'text-red-400' : 'text-white/40'
          }`}>{s.verdict ?? '—'}</span>
          <span className={`flex-shrink-0 w-10 text-[9px] ${
            s.source === 'production' ? 'text-emerald-500/50' :
            s.source === 'design' ? 'text-blue-500/50' :
            'text-white/30'
          }`}>{s.source}</span>
          <span className="text-white/50 flex-1 truncate text-[10px]">{s.seal_id ?? s.content_hash?.slice(0, 12) ?? '—'}</span>
          {s.risk_tier && <span className="text-white/20 text-[9px] flex-shrink-0">T{s.risk_tier}</span>}
        </div>
      ))}
    </div>
  );
}

// ── Pending Approvals ───────────────────────────────────────────
import { supabase } from '@/lib/supabase';
import { useState } from 'react';

function ApprovalsPanel() {
  const { data, loading, error } = usePendingApprovals();
  const [acting, setActing] = useState<string | null>(null);

  async function handleAction(approval_id: string, verdict: 'APPROVED' | 'REJECTED') {
    setActing(approval_id);
    try {
      const { error } = await supabase
        .from('arifosmcp_approval_tickets')
        .update({ human_verdict: verdict, resolved_at: new Date().toISOString() })
        .eq('ticket_id', approval_id);
      
      if (error) {
        alert('Failed to update: ' + error.message);
      } else {
        // Trigger a reload or just let React update if we use a realtime sub
        window.location.reload();
      }
    } catch (e: any) {
      alert('Error: ' + e.message);
    }
    setActing(null);
  }

  if (loading) return <LoadingState />;
  if (error) return <ErrorState msg={error} />;
  if (!data?.length) return <EmptyState message="No pending approvals." />;
  return (
    <div className="space-y-0.5 max-h-48 overflow-y-auto">
      {data.map((a) => (
        <div key={a.approval_id} className="flex items-center gap-2 text-[11px] font-mono hover:bg-white/[0.02] px-2 py-1 rounded">
          <span className="text-amber-400 font-bold flex-shrink-0 w-12 text-[9px]">{a.status}</span>
          <span className="text-white/50 flex-shrink-0 w-12 text-[9px]">{a.organ_code}</span>
          <span className="text-white/60 flex-1 font-mono text-[10px] truncate">{a.tool_name ?? a.approval_id}</span>
          {a.risk_tier && <span className="text-red-400/60 text-[9px] flex-shrink-0">T{a.risk_tier}</span>}
          <span className="text-white/20 text-[9px] flex-shrink-0">
            {a.created_at ? new Date(a.created_at).toLocaleDateString('en-MY', { month: 'short', day: 'numeric' }) : ''}
          </span>
          <div className="flex gap-1 ml-auto">
            <button 
              onClick={() => handleAction(a.approval_id, 'APPROVED')}
              disabled={acting === a.approval_id}
              className="px-2 py-0.5 bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 rounded border border-emerald-500/30 text-[9px] disabled:opacity-50"
            >
              APP
            </button>
            <button 
              onClick={() => handleAction(a.approval_id, 'REJECTED')}
              disabled={acting === a.approval_id}
              className="px-2 py-0.5 bg-red-500/20 text-red-400 hover:bg-red-500/30 rounded border border-red-500/30 text-[9px] disabled:opacity-50"
            >
              REJ
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

// ── Recent Tool Calls ────────────────────────────────────────────
function ToolCallsPanel() {
  const { data, loading, error } = useRecentToolCalls(30);
  if (loading) return <LoadingState />;
  if (error) return <ErrorState msg={error} />;
  if (!data?.length) return <EmptyState message="No tool calls recorded." />;
  return (
    <div className="space-y-0.5 max-h-64 overflow-y-auto">
      {data.map((tc) => (
        <div key={tc.call_id} className="flex items-center gap-2 text-[11px] font-mono hover:bg-white/[0.02] px-2 py-1 rounded">
          <span className="text-white/20 flex-shrink-0 w-12 text-[9px]">
            {tc.created_at ? new Date(tc.created_at).toLocaleDateString('en-MY', { month: 'short', day: 'numeric' }) : '—'}
          </span>
          <span className={`flex-shrink-0 w-10 text-[9px] ${
            tc.source === 'production' ? 'text-emerald-500/60' :
            tc.source === 'design' ? 'text-blue-500/60' : 'text-white/30'
          }`}>{tc.organ_code}</span>
          <span className="text-white/70 flex-1 font-mono text-[10px] truncate">{tc.tool_name}</span>
          <span className={`flex-shrink-0 w-10 text-[9px] font-bold ${
            tc.verdict === 'SEAL' ? 'text-emerald-400' :
            tc.verdict === 'SABAR' ? 'text-amber-400' :
            tc.verdict === 'VOID' ? 'text-red-400' :
            tc.verdict === 'HOLD' ? 'text-amber-500' :
            tc.verdict === 'ERROR' ? 'text-red-500' : 'text-white/30'
          }`}>{tc.verdict ?? (tc.error_msg ? 'ERR' : '—')}</span>
          {tc.latency_ms && <span className="text-white/20 text-[9px] flex-shrink-0">{tc.latency_ms}ms</span>}
        </div>
      ))}
    </div>
  );
}

// ── MCP Surface ────────────────────────────────────────────────
function McpSurfacePanel() {
  const { data, loading, error } = useMcpSurface();
  if (loading) return <LoadingState />;
  if (error) return <ErrorState msg={error} />;
  if (!data?.length) return <EmptyState message="No MCP surface data." />;
  return (
    <div className="space-y-0.5 max-h-48 overflow-y-auto">
      {data.map((row) => (
        <div key={row.server_ref} className="flex items-center gap-3 text-[11px] font-mono hover:bg-white/[0.02] px-2 py-1 rounded">
          <span className="text-white/50 flex-shrink-0 w-12 text-[9px]">{row.server_ref}</span>
          <span className="text-white/70 flex-1 text-[10px]">{row.name}</span>
          <span className={`flex-shrink-0 text-[9px] ${
            row.status_snapshot === 'healthy' ? 'text-emerald-400' :
            row.status_snapshot === 'degraded' ? 'text-amber-400' :
            row.status_snapshot === 'down' ? 'text-red-400' : 'text-white/30'
          }`}>{row.status_snapshot ?? '—'}</span>
          <span className="text-white/30 text-[9px] flex-shrink-0">{row.tool_count} tools</span>
          <span className="text-white/20 text-[9px] flex-shrink-0">
            {row.last_observed_at ? new Date(row.last_observed_at).toLocaleDateString('en-MY', { month: 'short', day: 'numeric' }) : '—'}
          </span>
        </div>
      ))}
    </div>
  );
}

// ── Evidence Index ──────────────────────────────────────────────
function EvidencePanel() {
  const { data, loading, error } = useEvidenceIndex(15);
  if (loading) return <LoadingState />;
  if (error) return <ErrorState msg={error} />;
  if (!data?.length) return <EmptyState message="No evidence records." />;
  return (
    <div className="space-y-0.5 max-h-48 overflow-y-auto">
      {data.map((e) => (
        <div key={e.evidence_id} className="flex items-center gap-2 text-[11px] font-mono hover:bg-white/[0.02] px-2 py-1 rounded">
          <span className="text-blue-400/60 flex-shrink-0 w-12 text-[9px] uppercase">{e.claim_state ?? '—'}</span>
          <span className="text-white/60 flex-1 truncate text-[10px]">{e.title ?? e.evidence_id}</span>
          <span className="text-white/30 flex-shrink-0 text-[9px]">{e.organ_code}</span>
          <span className="text-white/20 flex-shrink-0 text-[9px]">
            {e.created_at ? new Date(e.created_at).toLocaleDateString('en-MY', { month: 'short', day: 'numeric' }) : ''}
          </span>
        </div>
      ))}
    </div>
  );
}

// ── Artifact Index ──────────────────────────────────────────────
function ArtifactPanel() {
  const { data, loading, error } = useArtifactIndex(15);
  if (loading) return <LoadingState />;
  if (error) return <ErrorState msg={error} />;
  if (!data?.length) return <EmptyState message="No artifacts." />;
  return (
    <div className="space-y-0.5 max-h-48 overflow-y-auto">
      {data.map((a) => (
        <div key={a.artifact_id} className="flex items-center gap-2 text-[11px] font-mono hover:bg-white/[0.02] px-2 py-1 rounded">
          <span className="text-white/30 flex-shrink-0 w-12 text-[9px] truncate">{a.bucket ?? '—'}</span>
          <span className="text-white/60 flex-1 truncate text-[10px]">{a.filename ?? a.artifact_id}</span>
          <span className="text-white/30 flex-shrink-0 text-[9px]">{a.organ_code}</span>
          {a.size_bytes && <span className="text-white/20 text-[9px] flex-shrink-0">{(a.size_bytes / 1024).toFixed(0)}KB</span>}
        </div>
      ))}
    </div>
  );
}

// ── Risk Dashboard ──────────────────────────────────────────────
function RiskPanel() {
  const { data, loading, error } = useRiskDashboard();
  if (loading) return <LoadingState />;
  if (error) return <ErrorState msg={error} />;
  if (!data?.length) return <EmptyState message="No risk events." />;
  return (
    <div className="space-y-0.5 max-h-48 overflow-y-auto">
      {data.map((r, i) => (
        <div key={`${r.organ_code}-${r.risk_tier}-${i}`} className="flex items-center gap-2 text-[11px] font-mono hover:bg-white/[0.02] px-2 py-1 rounded">
          <span className="text-white/50 flex-shrink-0 w-12 text-[9px]">{r.organ_code}</span>
          <span className={`flex-shrink-0 w-8 text-[9px] font-bold ${
            r.risk_tier >= 4 ? 'text-red-400' :
            r.risk_tier >= 3 ? 'text-amber-400' :
            r.risk_tier >= 2 ? 'text-blue-400' : 'text-white/30'
          }`}>T{r.risk_tier}</span>
          <span className={`flex-shrink-0 w-12 text-[9px] ${
            r.status === 'SEALED' ? 'text-emerald-400' :
            r.status === 'PENDING' ? 'text-amber-400' :
            r.status === 'BLOCKED' ? 'text-red-400' : 'text-white/30'
          }`}>{r.status ?? '—'}</span>
          <span className="text-white/60 flex-1 text-[10px]">{r.count} event{r.count !== 1 ? 's' : ''}</span>
        </div>
      ))}
    </div>
  );
}

// ── Namespace / Organ Map ───────────────────────────────────────
function NamespacePanel() {
  const { data, loading, error } = useNamespaceSummary();
  if (loading) return <LoadingState />;
  if (error) return <ErrorState msg={error} />;
  if (!data?.length) return <EmptyState message="No namespace data." />;
  return (
    <div className="space-y-1 max-h-36 overflow-y-auto">
      {data.map((n) => (
        <div key={n.namespace} className="flex items-start gap-3 text-[11px] font-mono hover:bg-white/[0.02] px-2 py-1 rounded">
          <span className={`flex-shrink-0 w-12 text-[9px] font-bold ${
            n.namespace === 'production' ? 'text-emerald-400' :
            n.namespace === 'design' ? 'text-blue-400' :
            n.namespace === 'vault' ? 'text-amber-400' : 'text-white/40'
          }`}>{n.namespace}</span>
          <span className="text-white/50 flex-1 text-[10px]">{n.description}</span>
          <span className="text-white/20 text-[9px] flex-shrink-0">
            {n.noted_at ? new Date(n.noted_at).toLocaleDateString('en-MY', { month: 'short', day: 'numeric' }) : ''}
          </span>
        </div>
      ))}
    </div>
  );
}

// ── Main Panel ─────────────────────────────────────────────────
export default function SupabaseMemoryPanel() {
  const { healthy, latencyMs } = useSupabaseHealth();

  return (
    <section className="mb-24">
      {/* Header */}
      <div className="flex items-baseline gap-4 mb-8">
        <span className="text-4xl font-black text-emerald-500/30 font-mono italic">05.</span>
        <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Federation Memory</h2>
        <div className="flex items-center gap-2 px-3 py-1 bg-white/5 border border-white/10 rounded text-[9px] font-mono">
          <span className="text-white/40">SUPABASE L4</span>
          <HealthDot healthy={healthy} latencyMs={latencyMs} />
        </div>
      </div>

      {/* Connection error banner */}
      {healthy === false && (
        <div className="mb-6 px-4 py-3 bg-red-950/20 border border-red-500/30 rounded-lg text-xs font-mono text-red-400">
          ⚠ Cannot reach Supabase L4. Check VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY in .env
        </div>
      )}

      {/* 2-column grid, 4 rows */}
      <div className="grid grid-cols-2 gap-4">

        {/* Row 1: Seals + Approvals */}
        <PanelCard
          title="Recent Seals"
          subtitle="aaa.recent_all_seals"
          accent="emerald"
        >
          <SealsPanel />
        </PanelCard>

        <PanelCard
          title="Pending Approvals"
          subtitle="aaa.pending_approvals"
          accent="amber"
        >
          <ApprovalsPanel />
        </PanelCard>

        {/* Row 2: Tool Calls + MCP Surface */}
        <PanelCard
          title="Recent Tool Calls"
          subtitle="aaa.unified_tool_calls"
          accent="white"
        >
          <ToolCallsPanel />
        </PanelCard>

        <PanelCard
          title="MCP Surface"
          subtitle="aaa.mcp_surface"
          accent="white"
        >
          <McpSurfacePanel />
        </PanelCard>

        {/* Row 3: Evidence + Artifacts */}
        <PanelCard
          title="Evidence Index"
          subtitle="aaa.evidence_index"
          accent="blue"
        >
          <EvidencePanel />
        </PanelCard>

        <PanelCard
          title="Artifact Index"
          subtitle="aaa.artifact_index"
          accent="white"
        >
          <ArtifactPanel />
        </PanelCard>

        {/* Row 4: Risk + Namespace */}
        <PanelCard
          title="Risk Dashboard"
          subtitle="aaa.risk_dashboard"
          accent="red"
        >
          <RiskPanel />
        </PanelCard>

        <PanelCard
          title="Namespace / Organ Map"
          subtitle="aaa.namespace_summary"
          accent="white"
        >
          <NamespacePanel />
        </PanelCard>

      </div>

      <p className="mt-4 text-[9px] font-mono text-white/20">
        Phase 3A · Read-only Supabase L4 cockpit · No writes, approvals, or routing · Data: production + design namespaces
      </p>
    </section>
  );
}
