import { useState, useEffect } from 'react';
import { supabase } from '../lib/supabase';
import { Database, AlertCircle, CheckCircle2, ShieldAlert, FileText, Activity, Box, DatabaseZap, Terminal, Map } from 'lucide-react';

type ConnectionHealth = 'CHECKING' | 'ONLINE' | 'ERROR';

export default function SupabaseCockpit() {
  const [health, setHealth] = useState<ConnectionHealth>('CHECKING');
  const [lastRefresh, setLastRefresh] = useState<string>('Never');
  const [viewsData, setViewsData] = useState<{
    toolCalls: any[];
    pendingApprovals: any[];
    recentSeals: any[];
    mcpSurface: any[];
    evidenceIndex: any[];
    artifactIndex: any[];
    riskDashboard: any[];
  }>({
    toolCalls: [],
    pendingApprovals: [],
    recentSeals: [],
    mcpSurface: [],
    evidenceIndex: [],
    artifactIndex: [],
    riskDashboard: [],
  });
  
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setHealth('CHECKING');
      
      // Probe health
      const { error: healthError } = await supabase.from('aaa_recent_seals').select('*').limit(1);
      
      if (healthError) {
        if (healthError.message.includes('FetchError') || healthError.message.includes('Failed to fetch')) {
           setHealth('ERROR');
           setErrorMsg('Network error: Cannot reach Supabase API.');
           setLoading(false);
           return;
        }
        setHealth('ONLINE');
      } else {
        setHealth('ONLINE');
      }

      // Fetch all required panels concurrently
      const [
        toolCallsRes,
        approvalsRes,
        sealsRes,
        mcpRes,
        evidenceRes,
        artifactRes,
        riskRes
      ] = await Promise.all([
        supabase.from('arifosmcp_tool_calls').select('*').order('timestamp', { ascending: false }).limit(5),
        supabase.from('aaa_pending_approvals').select('*').limit(5),
        supabase.from('aaa_recent_seals').select('*').limit(5),
        supabase.from('aaa_mcp_surface').select('*').limit(5),
        supabase.from('aaa_evidence_index').select('*').limit(5),
        supabase.from('aaa_artifact_index').select('*').limit(5),
        supabase.from('aaa_risk_dashboard').select('*').limit(5),
      ]);

      setViewsData({
        toolCalls: toolCallsRes.data || [],
        pendingApprovals: approvalsRes.data || [],
        recentSeals: sealsRes.data || [],
        mcpSurface: mcpRes.data || [],
        evidenceIndex: evidenceRes.data || [],
        artifactIndex: artifactRes.data || [],
        riskDashboard: riskRes.data || [],
      });
      setLastRefresh(new Date().toLocaleTimeString());
      setErrorMsg(null);
    } catch (err: any) {
      setHealth('ERROR');
      setErrorMsg(err.message || 'Unknown connection error occurred.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const renderCard = (title: string, source: string, icon: React.ReactNode, data: any[], emptyMsg: string) => (
    <div className="bg-[#111] border border-gray-800 rounded-lg p-5 flex flex-col gap-4">
      <div className="flex flex-col gap-1 border-b border-gray-800 pb-3">
        <div className="flex items-center gap-2">
          {icon}
          <h3 className="font-mono text-sm uppercase tracking-wider text-gray-300">{title}</h3>
        </div>
        <span className="font-mono text-[10px] text-gray-500 bg-gray-900 self-start px-2 py-0.5 rounded">
          Source: {source}
        </span>
      </div>
      <div className="flex-1 overflow-auto min-h-[120px] max-h-[300px]">
        {loading ? (
          <div className="text-gray-500 font-mono text-xs animate-pulse">Querying {source}...</div>
        ) : errorMsg ? (
          <div className="text-red-400 font-mono text-xs">{errorMsg}</div>
        ) : data.length === 0 ? (
          <div className="text-gray-500 font-mono text-xs italic flex items-center justify-center h-full">
            {emptyMsg}
          </div>
        ) : (
          <pre className="text-gray-300 font-mono text-[11px] leading-relaxed">
            {JSON.stringify(data, (k, v) => (k === 'secret' || k === 'password' || k === 'token' ? '[REDACTED]' : v), 2)}
          </pre>
        )}
      </div>
    </div>
  );

  const renderPermissionMap = () => (
    <div className="bg-[#111] border border-gray-800 rounded-lg p-5 flex flex-col gap-4 md:col-span-2 lg:col-span-3">
      <div className="flex items-center gap-2 border-b border-gray-800 pb-3">
        <Map className="w-4 h-4 text-emerald-500" />
        <h3 className="font-mono text-sm uppercase tracking-wider text-gray-300">Organ Write-Permission Map</h3>
        <span className="font-mono text-[10px] text-gray-500 bg-gray-900 px-2 py-0.5 rounded ml-2">
          Source: SUPABASE_MCP_CONTRACT.md
        </span>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-black border border-gray-800 p-3 rounded">
          <h4 className="text-emerald-400 font-mono text-xs uppercase mb-2">arifOS</h4>
          <ul className="text-gray-400 font-mono text-xs space-y-1">
            <li>+ tool_calls</li>
            <li>+ approval_tickets</li>
            <li>+ canon_records</li>
            <li>+ vault_sealed_events</li>
            <li className="text-gray-600 mt-2">Authority: High-Risk, Seals</li>
          </ul>
        </div>
        <div className="bg-black border border-gray-800 p-3 rounded">
          <h4 className="text-blue-400 font-mono text-xs uppercase mb-2">GEOX</h4>
          <ul className="text-gray-400 font-mono text-xs space-y-1">
            <li>+ tool_calls</li>
            <li>+ canon_records</li>
            <li>+ evidence_items</li>
            <li>+ artifacts</li>
            <li className="text-gray-600 mt-2">Authority: Earth Domain</li>
          </ul>
        </div>
        <div className="bg-black border border-gray-800 p-3 rounded">
          <h4 className="text-amber-400 font-mono text-xs uppercase mb-2">WEALTH</h4>
          <ul className="text-gray-400 font-mono text-xs space-y-1">
            <li>+ tool_calls</li>
            <li>+ portfolio_snapshots</li>
            <li>+ transactions</li>
            <li>+ artifacts</li>
            <li className="text-gray-600 mt-2">Authority: Capital Domain</li>
          </ul>
        </div>
        <div className="bg-black border border-gray-800 p-3 rounded">
          <h4 className="text-purple-400 font-mono text-xs uppercase mb-2">A-FORGE</h4>
          <ul className="text-gray-400 font-mono text-xs space-y-1">
            <li>+ tool_calls</li>
            <li>+ artifacts</li>
            <li>+ canon_records</li>
            <li className="text-gray-600 mt-2">Authority: Execution Domain</li>
          </ul>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-black text-gray-200 p-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header & Health */}
        <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 border-b border-gray-800 gap-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-3">
              <DatabaseZap className="w-6 h-6 text-emerald-400" />
              AAA Supabase Cockpit
            </h1>
            <p className="text-gray-400 mt-1 font-mono text-xs">Phase 3A Blueprint: Read-Only Views Dashboard</p>
          </div>
          
          <div className="flex items-center gap-4 bg-gray-900 border border-gray-800 px-4 py-3 rounded-md">
            <div className="flex flex-col">
              <span className="text-[10px] uppercase font-mono text-gray-500">Connection</span>
              <div className="flex items-center gap-2 mt-1">
                {health === 'CHECKING' && <Circle className="w-3 h-3 text-amber-500 animate-pulse" />}
                {health === 'ONLINE' && <CheckCircle2 className="w-3 h-3 text-emerald-500" />}
                {health === 'ERROR' && <AlertCircle className="w-3 h-3 text-red-500" />}
                <span className={`font-mono text-xs font-bold ${
                  health === 'ONLINE' ? 'text-emerald-500' : 
                  health === 'ERROR' ? 'text-red-500' : 'text-amber-500'
                }`}>
                  {health}
                </span>
              </div>
            </div>
            
            <div className="h-8 w-px bg-gray-800 mx-2"></div>
            
            <div className="flex flex-col">
              <span className="text-[10px] uppercase font-mono text-gray-500">Last Refresh</span>
              <span className="font-mono text-xs text-gray-300 mt-1">{lastRefresh}</span>
            </div>
            
            <button 
              onClick={fetchData}
              disabled={loading}
              className="ml-4 px-3 py-1 bg-gray-800 hover:bg-gray-700 text-xs font-mono text-gray-200 rounded transition-colors disabled:opacity-50"
            >
              REFRESH
            </button>
          </div>
        </div>

        {/* Dashboard Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {renderCard(
            '1. Recent Tool Calls',
            'arifosmcp_tool_calls',
            <Terminal className="w-4 h-4 text-emerald-400" />, 
            viewsData.toolCalls,
            'No tool calls found in arifosmcp_tool_calls'
          )}
          
          {renderCard(
            '2. Pending Approvals',
            'aaa_pending_approvals',
            <AlertCircle className="w-4 h-4 text-amber-400" />, 
            viewsData.pendingApprovals,
            'No pending approvals requiring Sovereign action'
          )}

          {renderCard(
            '3. Recent Seals', 
            'aaa_recent_seals',
            <ShieldAlert className="w-4 h-4 text-emerald-400" />, 
            viewsData.recentSeals,
            'No recent seals found in aaa_recent_seals'
          )}
          
          {renderCard(
            '4. MCP Surface', 
            'aaa_mcp_surface',
            <Box className="w-4 h-4 text-blue-400" />, 
            viewsData.mcpSurface,
            'No tool manifest snapshots found'
          )}
          
          {renderCard(
            '5. Evidence / Canon Records', 
            'aaa_evidence_index',
            <FileText className="w-4 h-4 text-indigo-400" />, 
            viewsData.evidenceIndex,
            'No canon records or evidence items found'
          )}
          
          {renderCard(
            '6. Artifact Index', 
            'aaa_artifact_index',
            <Database className="w-4 h-4 text-purple-400" />, 
            viewsData.artifactIndex,
            'No artifacts registered in L4 storage'
          )}
          
          {renderCard(
            '7. Risk Dashboard', 
            'aaa_risk_dashboard',
            <Activity className="w-4 h-4 text-red-400" />, 
            viewsData.riskDashboard,
            'No active risk telemetry or floor violations'
          )}

          {renderPermissionMap()}
        </div>
      </div>
    </div>
  );
}
