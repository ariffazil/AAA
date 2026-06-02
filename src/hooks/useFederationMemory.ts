/**
 * useFederationMemory — Phase 3A Read-Only
 * Hooks for each Supabase aaa.* view (existing schemas)
 */
import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';

// ── Shared types ─────────────────────────────────────────────────

export interface QueryState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

function useQuery<T>(tableOrView: string, select = '*', limit = 50): QueryState<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetch = async () => {
    setLoading(true);
    setError(null);
    try {
      const { data: result, error: err } = await supabase
        .from(tableOrView)
        .select(select)
        .limit(limit);
      if (err) throw new Error(err.message);
      setData(result as T);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetch(); }, [tableOrView]);
  return { data, loading, error, refetch: fetch };
}

// ── Supabase health ─────────────────────────────────────────────

export function useSupabaseHealth() {
  const [healthy, setHealthy] = useState<boolean | null>(null);
  const [latencyMs, setLatencyMs] = useState<number | null>(null);

  useEffect(() => {
    const check = async () => {
      const start = Date.now();
      try {
        const { error } = await supabase.from('aaa.namespace_summary').select('namespace').limit(1);
        setLatencyMs(Date.now() - start);
        setHealthy(!error);
      } catch { setHealthy(false); }
    };
    check();
    const i = setInterval(check, 30000);
    return () => clearInterval(i);
  }, []);

  return { healthy, latencyMs };
}

// ── Recent All Seals (unified vault) ────────────────────────────

export interface AaaSeal {
  source: string;
  seal_id: string;
  seal_type: string | null;
  session_id: string | null;
  signed_by_ref: string | null;
  verdict: string | null;
  risk_tier: string | null;
  content_hash: string | null;
  created_at: string;
}

export function useRecentSeals(limit = 20) {
  return useQuery<AaaSeal[]>('aaa.recent_all_seals', 'source, seal_id, seal_type, session_id, signed_by_ref, verdict, risk_tier, content_hash, created_at', limit);
}

// ── Pending Approvals ────────────────────────────────────────────

export interface AaaApproval {
  approval_id: string;
  status: string;
  requested_by_ref: string | null;
  created_at: string;
  tool_name: string | null;
  organ_code: string | null;
  risk_tier: number | null;
}

export function usePendingApprovals() {
  return useQuery<AaaApproval[]>('aaa.pending_approvals', 'approval_id, status, requested_by_ref, created_at, tool_name, organ_code, risk_tier', 50);
}

// ── Unified Tool Calls ───────────────────────────────────────────

export interface AaaToolCall {
  source: string;
  call_id: string;
  organ_code: string;
  session_ref: string | null;
  tool_name: string;
  actor_ref: string | null;
  verdict: string | null;
  floor_triggered: string | null;
  latency_ms: number | null;
  created_at: string;
  result_code: string | null;
  peace2: string | null;
  error_msg: string | null;
  arguments: string | null;
  result: string | null;
  risk_tier: number | null;
  status: string | null;
}

export function useRecentToolCalls(limit = 30) {
  return useQuery<AaaToolCall[]>('aaa.unified_tool_calls', 'source, call_id, organ_code, session_ref, tool_name, actor_ref, verdict, floor_triggered, latency_ms, created_at, result_code, peace2, error_msg, risk_tier, status', limit);
}

// ── MCP Surface ─────────────────────────────────────────────────

export interface AaaMcpSurface {
  server_ref: string;
  name: string;
  status_snapshot: string | null;
  last_observed_at: string | null;
  tool_count: number;
}

export function useMcpSurface() {
  return useQuery<AaaMcpSurface[]>('aaa.mcp_surface', 'server_ref, name, status_snapshot, last_observed_at, tool_count', 50);
}

// ── Evidence Index ──────────────────────────────────────────────

export interface AaaEvidence {
  evidence_id: string;
  source_type: string | null;
  claim_state: string | null;
  title: string | null;
  organ_code: string | null;
  created_at: string;
}

export function useEvidenceIndex(limit = 20) {
  return useQuery<AaaEvidence[]>('aaa.evidence_index', 'evidence_id, source_type, claim_state, title, organ_code, created_at', limit);
}

// ── Artifact Index ──────────────────────────────────────────────

export interface AaaArtifact {
  artifact_id: string;
  bucket: string | null;
  filename: string | null;
  artifact_type: string | null;
  organ_code: string | null;
  size_bytes: number | null;
  created_at: string;
}

export function useArtifactIndex(limit = 20) {
  return useQuery<AaaArtifact[]>('aaa.artifact_index', 'artifact_id, bucket, filename, artifact_type, organ_code, size_bytes, created_at', limit);
}

// ── Risk Dashboard ─────────────────────────────────────────────

export interface AaaRisk {
  organ_code: string;
  risk_tier: number;
  status: string;
  count: number;
}

export function useRiskDashboard() {
  return useQuery<AaaRisk[]>('aaa.risk_dashboard', 'organ_code, risk_tier, status, count', 50);
}

// ── Namespace Summary ──────────────────────────────────────────

export interface AaaNamespace {
  namespace: string;
  description: string;
  noted_at: string;
}

export function useNamespaceSummary() {
  return useQuery<AaaNamespace[]>('aaa.namespace_summary', 'namespace, description, noted_at', 10);
}
