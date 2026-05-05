import { useState, useEffect } from 'react';
import {
  ArrowRight,
  Lock,
  Zap,
  Activity,
  ArrowUpRight,
  ShieldAlert,
  Check,
  X,
  Clock
} from 'lucide-react';

const FLOORS = [
  { id: 'F1', name: 'Amanah', status: 'PASS' },
  { id: 'F2', name: 'Truth', status: 'PASS' },
  { id: 'F3', name: 'Tri-Witness', status: 'PASS' },
  { id: 'F4', name: 'Clarity', status: 'PASS' },
  { id: 'F5', name: 'Peace²', status: 'PASS' },
  { id: 'F6', name: 'Empathy', status: 'PASS' },
  { id: 'F7', name: 'Humility', status: 'PASS' },
  { id: 'F8', name: 'Genius', status: 'PASS' },
  { id: 'F9', name: 'Anti-Hantu', status: 'PASS' },
  { id: 'F10', name: 'Ontology', status: 'PASS' },
  { id: 'F11', name: 'Auditability', status: 'PASS' },
  { id: 'F12', name: 'Injection', status: 'PASS' },
  { id: 'F13', name: 'Sovereign', status: 'PASS' },
];

const AGENTS = [
  { id: 'forge-explorer', role: 'Codebase exploration and structural analysis', type: 'Explore' },
  { id: 'forge-coordinator', role: 'Multi-agent task orchestration', type: 'Coordinator' },
  { id: 'arifos-guardian', role: 'Constitutional floor enforcement', type: 'Guardian' },
  { id: 'geox-witness', role: 'Earth physics verification', type: 'Witness' },
];

// ═══════════════════════════════════════════════════════════════════════
// HUMAN COGNITIVE HELPERS
// ═══════════════════════════════════════════════════════════════════════

type HealthLevel = 'NOMINAL' | 'DEGRADED' | 'CRITICAL';

function computeOverallHealth(
  kernelStatus: 'ONLINE' | 'OFFLINE',
  kernelHealth: 'READY' | 'OFFLINE',
  vaultStatus: string | undefined
): { level: HealthLevel; explanation: string } {
  const a2aOk = kernelStatus === 'ONLINE';
  const kernelOk = kernelHealth === 'READY';
  const vaultOk = vaultStatus === 'CONNECTED';

  if (a2aOk && kernelOk && vaultOk) {
    return { level: 'NOMINAL', explanation: 'All systems operational' };
  }
  if (!a2aOk) {
    return { level: 'CRITICAL', explanation: 'A2A gateway unreachable' };
  }
  if (!kernelOk && !vaultOk) {
    return { level: 'CRITICAL', explanation: 'Kernel and vault both offline' };
  }
  const down: string[] = [];
  if (!kernelOk) down.push('Kernel');
  if (!vaultOk) down.push('Vault');
  return { level: 'DEGRADED', explanation: `${down.join(' + ')} offline` };
}

function timeAgo(isoString: string | undefined): string {
  if (!isoString) return '—';
  const date = new Date(isoString);
  if (isNaN(date.getTime())) return '—';
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (seconds < 0) return 'just now';
  if (seconds < 10) return 'just now';
  if (seconds < 60) return `${seconds}s ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 30) return `${days}d ago`;
  return `${Math.floor(days / 30)}mo ago`;
}

function HealthHero({
  level,
  explanation,
  a2aOk,
  kernelOk,
  vaultOk,
}: {
  level: HealthLevel;
  explanation: string;
  a2aOk: boolean;
  kernelOk: boolean;
  vaultOk: boolean;
}) {
  const config: Record<HealthLevel, { emoji: string; bg: string; border: string; text: string; glow: string }> = {
    NOMINAL: {
      emoji: '🟢',
      bg: 'bg-emerald-950/20',
      border: 'border-emerald-500/30',
      text: 'text-emerald-500',
      glow: 'shadow-emerald-500/10',
    },
    DEGRADED: {
      emoji: '🟡',
      bg: 'bg-amber-950/20',
      border: 'border-amber-500/30',
      text: 'text-amber-500',
      glow: 'shadow-amber-500/10',
    },
    CRITICAL: {
      emoji: '🔴',
      bg: 'bg-red-950/20',
      border: 'border-red-500/30',
      text: 'text-red-500',
      glow: 'shadow-red-500/10',
    },
  };
  const c = config[level];

  return (
    <div className={`mb-16 p-8 border ${c.border} ${c.bg} rounded-lg shadow-lg ${c.glow}`}>
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div className="flex items-center gap-4">
          <span className="text-4xl">{c.emoji}</span>
          <div>
            <div className={`text-3xl font-black tracking-tighter ${c.text}`}>{level}</div>
            <div className="text-sm text-white/60 font-light">{explanation}</div>
          </div>
        </div>
        <div className="flex items-center gap-3 text-[10px] font-mono tracking-widest uppercase">
          <span className={`flex items-center gap-1.5 px-3 py-1.5 border rounded ${a2aOk ? 'border-emerald-500/30 text-emerald-500' : 'border-red-500/30 text-red-500'}`}>
            {a2aOk ? '✅' : '❌'} A2A
          </span>
          <span className={`flex items-center gap-1.5 px-3 py-1.5 border rounded ${vaultOk ? 'border-emerald-500/30 text-emerald-500' : 'border-red-500/30 text-red-500'}`}>
            {vaultOk ? '✅' : '❌'} Vault
          </span>
          <span className={`flex items-center gap-1.5 px-3 py-1.5 border rounded ${kernelOk ? 'border-emerald-500/30 text-emerald-500' : 'border-red-500/30 text-red-500'}`}>
            {kernelOk ? '✅' : '❌'} Kernel
          </span>
        </div>
      </div>
    </div>
  );
}

export default function Cockpit() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [kernelStatus, setKernelStatus] = useState<'ONLINE' | 'OFFLINE'>('OFFLINE');
  const [lastCheck, setLastCheck] = useState<string>('never');
  const [latency, setLatency] = useState<number | null>(null);
  const [kernelHealth, setKernelHealth] = useState<'READY' | 'OFFLINE'>('OFFLINE');
  const [kernelLastCheck, setKernelLastCheck] = useState<string>('never');
  const [kernelLatency, setKernelLatency] = useState<number | null>(null);
  const [holdsCount, setHoldsCount] = useState<number>(0);
  const [holdsBreakdown, setHoldsBreakdown] = useState<{ 'input-required': number; 'auth-required': number }>({ 'input-required': 0, 'auth-required': 0 });
  const [sealsCount, setSealsCount] = useState<number>(0);
  const [vaultConnected, setVaultConnected] = useState<boolean>(false);
  const [toolRegistry, setToolRegistry] = useState<string[]>([]);
  const [cockpitState, setCockpitState] = useState<any>(null);
  const [events, setEvents] = useState<{time: string; text: string; type: string; timestamp: string}[]>([
    { time: new Date().toLocaleTimeString('en-GB'), text: 'Cockpit initialized. Waiting for kernel...', type: 'info', timestamp: new Date().toISOString() }
  ]);
  const [initLoading, setInitLoading] = useState(false);
  const [tick, setTick] = useState(0); // forces relative-time re-render

  const fetchTasks = async () => {
    try {
      const response = await fetch('/operator/tasks?state=input-required');
      const data = await response.json();
      setTasks(data.tasks || []);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
    const interval = setInterval(fetchTasks, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const checkKernelHealth = async () => {
      const start = Date.now();
      try {
        const res = await fetch('/health');
        const ms = Date.now() - start;
        setLatency(ms);
        const now = new Date().toLocaleTimeString('en-MY', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        setLastCheck(now);
        if (res.ok) {
          const data = await res.json();
          setKernelStatus(data.status === 'healthy' ? 'ONLINE' : 'OFFLINE');
        } else {
          setKernelStatus('OFFLINE');
        }
      } catch {
        setKernelStatus('OFFLINE');
        setLatency(null);
      }
    };
    checkKernelHealth();
    const interval = setInterval(checkKernelHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const checkArifOSHealth = async () => {
      const start = Date.now();
      try {
        const res = await fetch('https://arifos.arif-fazil.com/health');
        const ms = Date.now() - start;
        setKernelLatency(ms);
        const now = new Date().toLocaleTimeString('en-MY', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        setKernelLastCheck(now);
        if (res.ok) {
          setKernelHealth('READY');
        } else {
          setKernelHealth('OFFLINE');
        }
      } catch {
        setKernelHealth('OFFLINE');
        setKernelLatency(null);
      }
    };
    checkArifOSHealth();
    const interval = setInterval(checkArifOSHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const checkHolds = async () => {
      try {
        const res = await fetch('/operator/holds');
        if (res.ok) {
          const data = await res.json();
          setHoldsCount(data.holds);
          setHoldsBreakdown(data.breakdown);
        }
      } catch { /* ignore */ }
    };
    checkHolds();
    const interval = setInterval(checkHolds, 20000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const checkSeals = async () => {
      try {
        const res = await fetch('/operator/seals');
        if (res.ok) {
          const data = await res.json();
          setSealsCount(data.seals);
          setVaultConnected(data.seals !== '?');
        }
      } catch { /* ignore */ }
    };
    const checkStatus = async () => {
      try {
        const res = await fetch('https://af-bridge.arif-fazil.com/status');
        if (res.ok) {
          const data = await res.json();
          setHoldsCount(data.metabolic?.open_holds ?? holdsCount);
        }
      } catch { /* ignore */ }
    };
    checkSeals();
    checkStatus();
    const interval = setInterval(() => { checkSeals(); checkStatus(); }, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const checkTools = async () => {
      try {
        const res = await fetch('https://arifos.arif-fazil.com/tools');
        if (res.ok) {
          const data = await res.json();
          setToolRegistry(data.tools || []);
        }
      } catch { /* ignore */ }
    };
    checkTools();
    const interval = setInterval(checkTools, 60000);
    return () => clearInterval(interval);
  }, []);

  // ═══════════════════════════════════════════════════════════════════════
  // COCKPIT STATE POLLING — Dynamic SOT
  // ═══════════════════════════════════════════════════════════════════════
  useEffect(() => {
    const fetchCockpitState = async () => {
      try {
        const res = await fetch('/api/cockpit/state', { cache: 'no-store' });
        if (res.ok) {
          const data = await res.json();
          setCockpitState(data);
        }
      } catch { /* ignore */ }
    };
    fetchCockpitState();
    const interval = setInterval(fetchCockpitState, 5000);
    return () => clearInterval(interval);
  }, []);

  // ═══════════════════════════════════════════════════════════════════════
  // SSE EVENT STREAM
  // ═══════════════════════════════════════════════════════════════════════
  useEffect(() => {
    let es: EventSource | null = null;
    try {
      es = new EventSource('/api/cockpit/events');
      es.onmessage = (e) => {
        try {
          const ev = JSON.parse(e.data);
          if (ev.kind === 'heartbeat') return;
          const now = new Date();
          const time = now.toLocaleTimeString('en-GB');
          const text = ev.message || `[${ev.kind}] ${JSON.stringify(ev).slice(0, 120)}`;
          setEvents(prev => {
            const next = [...prev, { time, text, type: ev.kind === 'init' ? 'ok' : 'info', timestamp: now.toISOString() }];
            return next.slice(-100); // bounded
          });
        } catch (_) {}
      };
    } catch { /* SSE not supported, fallback to polling-only */ }
    return () => { if (es) es.close(); };
  }, []);

  // ═══════════════════════════════════════════════════════════════════════
  // RELATIVE TIME TICK — re-render every 30s so "Xm ago" stays fresh
  // ═══════════════════════════════════════════════════════════════════════
  useEffect(() => {
    const interval = setInterval(() => setTick(t => t + 1), 30000);
    return () => clearInterval(interval);
  }, []);

  const handleIgnition = async () => {
    if (!confirm('WARNING: Triggering 000_INIT will derive new session keys and write a SEAL to VAULT999. Continue?')) return;
    setInitLoading(true);
    try {
      const res = await fetch('/api/cockpit/init', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ confirm: true, intent: 'cockpit_manual_000_init' })
      });
      const data = await res.json();
      const now = new Date();
      if (data.ok) {
        setEvents(prev => [...prev, { time: now.toLocaleTimeString('en-GB'), text: `IGNITION SEALED: ${data.session_id}`, type: 'ok', timestamp: now.toISOString() }]);
      } else {
        setEvents(prev => [...prev, { time: now.toLocaleTimeString('en-GB'), text: `Ignition rejected: ${data.error || 'Unknown'}`, type: 'warn', timestamp: now.toISOString() }]);
      }
    } catch (e: any) {
      const now = new Date();
      setEvents(prev => [...prev, { time: now.toLocaleTimeString('en-GB'), text: `Ignition failed: ${e.message}`, type: 'warn', timestamp: now.toISOString() }]);
    } finally {
      setInitLoading(false);
    }
  };

  const handleApprove = async (taskId: string) => {
    try {
      await fetch(`/operator/tasks/${taskId}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ humanId: 'Arif-Sovereign', signature: 'SIG-' + Date.now() })
      });
      fetchTasks();
    } catch (error) {
      alert('Approval failed');
    }
  };

  const handleReject = async (taskId: string) => {
    try {
      await fetch(`/operator/tasks/${taskId}/reject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reason: 'Sovereign Veto' })
      });
      fetchTasks();
    } catch (error) {
      alert('Rejection failed');
    }
  };

  const health = computeOverallHealth(kernelStatus, kernelHealth, cockpitState?.vault?.status);

  return (
    <div className="min-h-screen bg-[#050505] text-[#e2e2e5] font-sans selection:bg-red-500/30 selection:text-white pb-20">

      {/* CANONICAL HEADER STRIP */}
      <div className="fixed top-[33px] left-0 right-0 z-50 bg-[#050505]/90 backdrop-blur-md border-b border-white/5">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <div className="text-sm font-black tracking-widest text-white">Δ AAA COCKPIT</div>
            <div className="hidden md:flex gap-6 text-[10px] font-mono tracking-widest uppercase text-white/40">
              <span className="hover:text-red-500 cursor-pointer transition-colors">Ψ Identity</span>
              <span className="text-red-500 font-bold">Constitution</span>
              <span className="hover:text-red-500 cursor-pointer transition-colors">Theory</span>
            </div>
            <div className="hidden lg:flex gap-6 text-[10px] font-mono tracking-widest uppercase text-white/40 border-l border-white/10 pl-6">
              <span className="hover:text-red-500 cursor-pointer transition-colors">Φ Earth</span>
              <span className="hover:text-red-500 cursor-pointer transition-colors text-[#d4a853]">Ω Wealth</span>
              <span className="text-white">Ω★ Kernel</span>
            </div>
          </div>
          <div className="flex items-center gap-4">
              <div className="flex items-center gap-3">
              <div className={`flex flex-col gap-1 px-3 py-1 border rounded text-[9px] font-mono ${kernelStatus === 'ONLINE' ? 'bg-emerald-950/20 border-emerald-500/30 text-emerald-500' : 'bg-red-950/20 border-red-500/30 text-red-500'}`}>
                 <div className="flex items-center gap-2">
                   <div className={`w-1.5 h-1.5 rounded-full ${kernelStatus === 'ONLINE' ? 'bg-emerald-500' : 'bg-red-500 animate-pulse'}`} />
                   A2A: {kernelStatus}
                 </div>
                 <div className="text-white/40">Last: {lastCheck} {latency !== null ? `· ${latency}ms` : ''}</div>
              </div>
              <div className={`flex flex-col gap-1 px-3 py-1 border rounded text-[9px] font-mono ${kernelHealth === 'READY' ? 'bg-blue-950/20 border-blue-500/30 text-blue-400' : 'bg-red-950/20 border-red-500/30 text-red-500'}`}>
                 <div className="flex items-center gap-2">
                   <div className={`w-1.5 h-1.5 rounded-full ${kernelHealth === 'READY' ? 'bg-blue-400' : 'bg-red-500 animate-pulse'}`} />
                   KERNEL: {kernelHealth}
                 </div>
                 <div className="text-white/40">Last: {kernelLastCheck} {kernelLatency !== null ? `· ${kernelLatency}ms` : ''}</div>
              </div>
              </div>
             <div className={`hidden sm:flex items-center gap-2 px-3 py-1 border rounded text-[9px] font-mono ${cockpitState?.vault?.status === 'CONNECTED' ? 'bg-emerald-950/20 border-emerald-500/30 text-emerald-500' : 'bg-red-950/20 border-red-500/30 text-red-500'}`}>
                VAULT999: {cockpitState?.vault?.status || 'UNKNOWN'}
             </div>
             <div className="hidden sm:flex items-center gap-2 px-3 py-1 bg-white/5 border border-white/10 rounded text-[9px] font-mono text-white/60">
                MCP: {cockpitState?.gateway?.version || 'v1.0.0-FORGED'}
             </div>
          </div>
        </div>
      </div>

      <main className="max-w-4xl mx-auto px-6 pt-40">

        {/* HERO / INTRO */}
        <section className="mb-20">
          <div className="flex items-center gap-3 mb-6">
            <span className="h-px w-8 bg-red-500" />
            <h2 className="text-[10px] font-mono text-red-500 uppercase tracking-[0.4em]">Governance Layer</h2>
          </div>
          <h1 className="text-6xl md:text-8xl font-black tracking-tighter text-white mb-8">
            The Cockpit<span className="text-red-500">.</span>
          </h1>
          <p className="text-xl text-white/60 font-light leading-relaxed max-w-2xl mb-10">
            Real-time constitutional monitoring for the arifOS federation. Every floor, every agent, every tool.
          </p>
        </section>

        {/* 00. HEALTH HERO BANNER */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-red-500/20 font-mono italic">00.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">System Health</h2>
          </div>
          <HealthHero
            level={health.level}
            explanation={health.explanation}
            a2aOk={kernelStatus === 'ONLINE'}
            kernelOk={kernelHealth === 'READY'}
            vaultOk={cockpitState?.vault?.status === 'CONNECTED'}
          />
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <HealthMetric
              label="Integrity"
              value={cockpitState?.vault?.status === 'CONNECTED' ? '100%' : '0%'}
              sub={cockpitState?.vault?.status === 'CONNECTED' ? 'Validated' : 'OFFLINE'}
              color={cockpitState?.vault?.status === 'CONNECTED' ? 'text-emerald-500' : 'text-red-500'}
            />
            <HealthMetric
              label="Holds Open"
              value={String(cockpitState?.tasks?.holds ?? holdsCount)}
              sub={(cockpitState?.tasks?.holds ?? holdsCount) > 0 ? `${cockpitState?.tasks?.holds ?? holdsCount} pending` : "None"}
              color={(cockpitState?.tasks?.holds ?? holdsCount) > 0 ? "text-amber-500" : "text-white"}
            />
            <HealthMetric
              label="Seals"
              value={String(cockpitState?.vault?.seals ?? sealsCount)}
              sub={cockpitState?.vault?.status === 'CONNECTED' ? "VAULT999" : "Vault Unreachable"}
              color={cockpitState?.vault?.status === 'CONNECTED' ? "text-emerald-500" : "text-red-500"}
            />
            <HealthMetric
              label="Uptime"
              value={cockpitState?.gateway?.uptime_seconds ? `${(cockpitState.gateway.uptime_seconds / 3600).toFixed(1)}h` : '—'}
              sub={cockpitState?.gateway?.version || 'Live'}
              color="text-blue-500"
            />
          </div>
        </section>

        {/* 01. EVENT LOG */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-white/10 font-mono italic">01.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Event Log</h2>
          </div>
          <div className="bg-white/5 p-8 font-mono text-[11px] leading-relaxed text-white/40 max-h-96 overflow-y-auto">
            {events.length === 0 ? (
              <div className="mb-2"><span className="text-white/20">--</span> No events received yet.</div>
            ) : (
              events.map((ev, idx) => (
                <div key={idx} className={`mb-2 ${ev.type === 'ok' ? 'text-emerald-500/80' : ev.type === 'warn' ? 'text-red-500/80' : ''}`}>
                  <span className={ev.type === 'warn' ? 'text-red-900' : 'text-white/20'}>{timeAgo(ev.timestamp)}</span> {ev.text}
                </div>
              ))
            )}
            <div className="animate-pulse">_</div>
          </div>
        </section>

        {/* 02. ACTION APPROVAL QUEUE */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-red-500/20 font-mono italic">02.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Approval Queue</h2>
            {tasks.length > 0 && (
              <span className="px-2 py-0.5 bg-red-500/10 text-red-500 border border-red-500/20 rounded text-[9px] font-mono uppercase tracking-widest">
                {tasks.length} PENDING
              </span>
            )}
          </div>

          {tasks.length === 0 ? (
            <div className="p-12 border border-dashed border-white/10 rounded-lg text-center">
              <ShieldAlert className="w-8 h-8 text-white/10 mx-auto mb-4" />
              <p className="text-sm text-white/30 font-mono tracking-widest uppercase">No actions pending sovereign witness</p>
            </div>
          ) : (
            <div className="space-y-6">
              {tasks.map(task => (
                <div key={task.id} className="bg-red-950/10 border border-red-500/20 rounded-lg overflow-hidden">
                  <div className="p-6 border-b border-red-500/10 flex justify-between items-start">
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="px-2 py-0.5 bg-red-500 text-black text-[9px] font-black uppercase tracking-widest rounded">CONSEQUENTIAL ACTION</span>
                        <span className="text-[10px] font-mono text-white/40 tracking-tighter">ID: {task.id}</span>
                      </div>
                      <p className="text-lg font-bold text-white mb-1">
                        {task.history[0]?.parts[0]?.text || "Unknown Intent"}
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-[10px] font-mono text-white/40 uppercase mb-1">Risk Tier</div>
                      <div className="text-red-500 font-black">{task.metadata.riskLevel}</div>
                    </div>
                  </div>

                  <div className="p-6 bg-black/40 grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>
                       <div className="text-[9px] font-mono text-white/30 uppercase tracking-widest mb-3">Irreversibility Bond</div>
                       <div className="p-3 bg-white/5 border border-white/10 rounded font-mono text-xs text-white/60">
                         {task.metadata.irreversibilityBond}
                       </div>
                    </div>
                    <div>
                       <div className="text-[9px] font-mono text-white/30 uppercase tracking-widest mb-3">Authorization Proof</div>
                       <div className="p-3 bg-white/5 border border-white/10 rounded font-mono text-[10px] text-emerald-500/80 break-all leading-tight">
                         WITNESS_TYPE: AGENT<br/>
                         SIGNATURE: AF-FORGE-SIG-{task.id.slice(-8).toUpperCase()}<br/>
                         STATUS: PENDING_HUMAN_OVERRIDE
                       </div>
                    </div>
                  </div>

                  <div className="p-4 bg-red-500/5 flex justify-end gap-4">
                    <button
                      onClick={() => handleReject(task.id)}
                      className="px-4 py-2 flex items-center gap-2 text-[10px] font-bold text-white/40 hover:text-white transition-colors"
                    >
                      <X className="w-3 h-3" /> VETO ACTION
                    </button>
                    <button
                      onClick={() => handleApprove(task.id)}
                      className="px-6 py-2 bg-red-500 text-black font-black text-[10px] tracking-widest hover:bg-white transition-all flex items-center gap-2"
                    >
                      <Check className="w-3 h-3" /> AUTHORIZE EXECUTION
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* 03. LIVE AGENTS */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-white/10 font-mono italic">03.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Live Agents</h2>
          </div>
          <div className="space-y-4">
            {(cockpitState?.agents || AGENTS).map((a: any) => (
              <div key={a.id} className="group border-b border-white/5 pb-6 hover:border-red-500/50 transition-colors">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-bold text-white font-mono">{a.id}</h3>
                  <div className={`text-[9px] font-mono px-2 py-0.5 border uppercase tracking-widest ${a.status === 'online' ? 'border-emerald-500/30 text-emerald-500' : a.status === 'standby' ? 'border-amber-500/30 text-amber-500' : 'border-white/20 text-white/40'}`}>{a.status?.toUpperCase() || a.type}</div>
                </div>
                <p className="text-sm text-white/40 font-light mb-4">{a.name ? `${a.name} · ${a.role}` : a.role}</p>
                <div className="flex items-center gap-4 text-[9px] font-mono tracking-tighter uppercase">
                  <span className={`flex items-center gap-1.5 ${a.status === 'online' ? 'text-emerald-500' : a.status === 'standby' ? 'text-amber-500' : 'text-white/40'}`}>
                    <Activity className="w-3 h-3" /> State: {a.status === 'online' ? 'Active' : a.status === 'standby' ? 'Standby' : 'Unknown'}
                  </span>
                  {a.lane && <><span className="text-white/20">|</span><span className="text-white/40 italic">Lane: {a.lane}</span></>}
                  {a.organ && <><span className="text-white/20">|</span><span className="text-white/40 italic">Organ: {a.organ}</span></>}
                  {a.lastHeartbeat && <><span className="text-white/20">|</span><span className="text-white/40">{timeAgo(a.lastHeartbeat)}</span></>}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* 04. CONSTITUTIONAL FLOORS */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-white/10 font-mono italic">04.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Constitutional Floors</h2>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-px bg-white/5 border border-white/5">
            {(cockpitState?.floors || FLOORS).map((f: any) => (
              <div key={f.id} className="bg-[#050505] p-6 hover:bg-white/[0.02] transition-colors group">
                <div className="text-[10px] font-mono text-red-500 mb-4 group-hover:translate-x-1 transition-transform">{f.id}</div>
                <div className="text-xs font-black text-white leading-tight mb-2">{f.name.toUpperCase()}</div>
                <div className="flex items-center gap-1.5">
                   <div className={`w-1 h-1 rounded-full ${f.status === 'pass' ? 'bg-emerald-500' : 'bg-red-500'}`} />
                   <span className={`text-[8px] font-mono tracking-widest ${f.status === 'pass' ? 'text-emerald-500' : 'text-red-500'}`}>{f.status === 'pass' ? 'VERIFIED' : 'FAILED'}</span>
                </div>
              </div>
            ))}
            <div className="bg-[#050505] p-6 flex items-center justify-center border-l border-white/5">
              <ShieldAlert className="w-6 h-6 text-white/10" />
            </div>
          </div>
        </section>

        {/* 05. TOOL REGISTRY */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-white/10 font-mono italic">05.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Tool Registry</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {(toolRegistry.length > 0 ? toolRegistry : ['geox.well_viewer', 'geox.interpret_las', 'forge.check_governance', 'forge.run_agent', 'forge.hold_action', 'forge.recall_memory']).map(t => (
              <div key={t} className="p-4 border border-white/5 hover:border-white/20 transition-all flex justify-between items-center group">
                <code className="text-xs font-mono text-white/60 group-hover:text-white transition-colors">{t}</code>
                <div className="w-1 h-1 bg-white/20 rounded-full group-hover:bg-red-500" />
              </div>
            ))}
          </div>
        </section>

        {/* 06. PROTOCOL SURFACES + SUMMARY */}
        <section className="mb-24 pt-12 border-t border-white/10">
          <h3 className="text-sm font-black uppercase tracking-widest text-white mb-6">Constitutional Summary</h3>
          <p className="text-white/40 font-light leading-relaxed text-sm max-w-3xl">
            The arifOS federation operates under 13 binding floors (F1–F13). Every action — from a well-log interpretation to an agent deployment — must pass all active floors before a 999_SEAL is issued. Any floor failure triggers 888_HOLD, requiring human review.
          </p>
        </section>

        {/* DEEP LINKS */}
        <section className="flex flex-wrap gap-8 text-[10px] font-mono tracking-widest uppercase text-white/30 mb-20">
          <a href="#" className="hover:text-white flex items-center gap-2 transition-colors">Agent JSON <ArrowUpRight className="w-3 h-3" /></a>
          <a href="#" className="hover:text-white flex items-center gap-2 transition-colors">Kernel Health <ArrowUpRight className="w-3 h-3" /></a>
          <a href="#" className="hover:text-white flex items-center gap-2 transition-colors text-red-500">Read Canon <ArrowUpRight className="w-3 h-3" /></a>
        </section>

        {/* 07. IGNITION */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-red-500/20 font-mono italic">07.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Ignition</h2>
          </div>
          <button
            onClick={handleIgnition}
            disabled={initLoading}
            className="flex items-center gap-3 px-8 py-4 bg-white text-black font-black text-sm tracking-tighter hover:bg-red-500 hover:text-white transition-all group disabled:opacity-50"
          >
            <Zap className="w-4 h-4 fill-current" />
            {initLoading ? 'IGNITING...' : '000_INIT IGNITION'}
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>
        </section>

      </main>

      <footer className="max-w-6xl mx-auto px-6 pt-20 border-t border-white/5 text-center text-[10px] font-mono tracking-[0.2em] text-white/20">
        Δ AAA COCKPIT · arifOS v2026.4.22 · DITEMPA BUKAN DIBERI · Forged in Kuala Lumpur 🇲🇾
      </footer>
    </div>
  );
}

function HealthMetric({ label, value, sub, color }: { label: string, value: string, sub: string, color: string }) {
  return (
    <div className="border-l border-white/10 pl-6 py-2">
      <div className={`text-4xl font-black tracking-tighter mb-1 ${color}`}>{value}</div>
      <div className="text-[10px] font-mono text-white/60 uppercase tracking-widest mb-1">{label}</div>
      <div className="text-[9px] font-mono text-white/20 italic uppercase tracking-widest">{sub}</div>
    </div>
  );
}
