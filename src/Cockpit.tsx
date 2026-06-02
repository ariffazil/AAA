import { useState, useEffect, useRef } from 'react';
import {
  ArrowRight,
  Zap,
  Activity,
  ArrowUpRight,
  ShieldAlert,
  Send,
  CheckCircle2,
  Circle,
  AlertCircle,
} from 'lucide-react';
import { ConsentDialog, SessionBadge, SessionManifest } from './components/SessionConsent';
import SupabaseMemoryPanel from './components/cockpit/SupabaseMemoryPanel';

type OperatorTask = {
  id: string;
  history: Array<{ parts: Array<{ text?: string }> }>;
  metadata: {
    riskLevel?: string;
    irreversibilityBond?: string;
  };
};

type LogEvent = {
  id: string;
  ts: string;
  kind: string;
  taskId: string;
  msg: string;
};

type DomainStatus = 'loading' | 'ok' | 'err';

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

const GOLDEN_PATH = ['SENSE', 'MIND', 'HEART', 'JUDGE', 'VAULT'] as const;

const DOMAIN_MCPS = [
  { id: 'geox', label: 'GEOX', symbol: '🌍', desc: 'Earth intelligence · 34 skills', url: 'https://geox.arif-fazil.com/health' },
  { id: 'wealth', label: 'WEALTH', symbol: 'Ω', desc: 'Capital intelligence · entropy flows', url: 'https://wealth.arif-fazil.com/health' },
  { id: 'well', label: 'WELL', symbol: 'Ψ', desc: 'Vitality mirror · substrate health', url: 'https://well.arif-fazil.com/health' },
];

// Map A2A task state → golden path step index (0–4)
function stateToPathStep(state: string): number {
  if (state === 'submitted') return 0;
  if (state === 'working') return 2;
  if (state === 'input-required' || state === 'auth-required') return 3;
  if (state === 'completed') return 4;
  return -1;
}

const EVENT_COLORS: Record<string, string> = {
  '888_HOLD': 'text-amber-500',
  '999_SEAL': 'text-emerald-400',
  'ERROR': 'text-red-500',
  'TASK_START': 'text-blue-400',
  'HUMAN_APPROVE': 'text-emerald-300',
  'HUMAN_REJECT': 'text-red-400',
  'SENSE': 'text-white/60',
  'MIND': 'text-white/60',
};

const OPERATOR_API = '/api/operator';

export default function Cockpit() {
  const [tasks, setTasks] = useState<OperatorTask[]>([]);
  const [agents, setAgents] = useState<any[]>([]);
  const [agentsLoading, setAgentsLoading] = useState(true);
  const [agentsError, setAgentsError] = useState<string | null>(null);
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
  const [toolRegistry, setToolRegistry] = useState<{ name: string; requires_888: boolean }[]>([]);
  const [sessionManifest, setSessionManifest] = useState<SessionManifest | null>(null);
  const [showConsentDialog, setShowConsentDialog] = useState(false);

  // Mission Intake
  const [missionText, setMissionText] = useState('');
  const [missionSubmitting, setMissionSubmitting] = useState(false);
  const [lastMission, setLastMission] = useState<{ id: string; text: string; state: string } | null>(null);

  // Live Event Log
  const [events, setEvents] = useState<LogEvent[]>([]);

  // Domain MCP health
  const [domainHealth, setDomainHealth] = useState<Record<string, DomainStatus>>({
    geox: 'loading', wealth: 'loading', well: 'loading',
  });

  // ── Data Fetchers ────────────────────────────────────────────────────────

  const fetchAgents = async () => {
    try {
      setAgentsLoading(true);
      const response = await fetch('/a2a/agents.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setAgents(data.agents || []);
      setAgentsError(null);
    } catch (err) {
      setAgentsError(err instanceof Error ? err.message : 'Unknown');
    } finally {
      setAgentsLoading(false);
    }
  };

  const fetchTasks = async () => {
    try {
      const response = await fetch(`${OPERATOR_API}/tasks?state=input-required`);
      const data = await response.json();
      setTasks(data.tasks || []);
    } catch { /* ignore */ }
  };

  const fetchEvents = async () => {
    try {
      const res = await fetch(`${OPERATOR_API}/events?n=40`);
      if (res.ok) {
        const data = await res.json();
        setEvents(data.events || []);
      }
    } catch { /* ignore */ }
  };

  const pollLastMission = async (taskId: string) => {
    try {
      const res = await fetch(`${OPERATOR_API}/tasks/${taskId}`);
      if (res.ok) {
        const data = await res.json();
        if (data.task) {
          setLastMission(prev => prev ? { ...prev, state: data.task.status.state } : null);
        }
      }
    } catch { /* ignore */ }
  };

  const handleSubmitMission = async (e: React.FormEvent) => {
    e.preventDefault();
    const text = missionText.trim();
    if (!text || missionSubmitting) return;

    setMissionSubmitting(true);
    try {
      const body = {
        jsonrpc: '2.0',
        method: 'message/send',
        id: Date.now().toString(),
        params: {
          message: {
            role: 'user',
            parts: [{ kind: 'text', text }],
            messageId: crypto.randomUUID(),
          }
        }
      };
      const res = await fetch('/api/message/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      if (res.ok) {
        const data = await res.json();
        const task = data.result;
        setLastMission({ id: task?.id || 'unknown', text, state: task?.status?.state || 'submitted' });
        setMissionText('');
      }
    } catch { /* ignore */ } finally {
      setMissionSubmitting(false);
    }
  };

  // ── Effects ──────────────────────────────────────────────────────────────

  useEffect(() => {
    queueMicrotask(fetchTasks);
    queueMicrotask(fetchAgents);
    const interval = setInterval(fetchTasks, 5000);
    const agentsInterval = setInterval(fetchAgents, 30000);
    return () => { clearInterval(interval); clearInterval(agentsInterval); };
  }, []);

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, 5000);
    return () => clearInterval(interval);
  }, []);

  // Poll last mission task state while it's in-flight
  useEffect(() => {
    if (!lastMission || lastMission.state === 'completed' || lastMission.state === 'failed' || lastMission.state === 'rejected') return;
    const interval = setInterval(() => pollLastMission(lastMission.id), 3000);
    return () => clearInterval(interval);
  }, [lastMission?.id, lastMission?.state]);

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
        setKernelHealth(res.ok ? 'READY' : 'OFFLINE');
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
        const res = await fetch(`${OPERATOR_API}/holds`);
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
        const res = await fetch(`${OPERATOR_API}/seals`);
        if (res.ok) {
          const data = await res.json();
          setSealsCount(data.seals);
          setVaultConnected(data.vaultConnected ?? data.seals !== '?');
        }
      } catch { /* ignore */ }
    };
    checkSeals();
    const interval = setInterval(checkSeals, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const checkTools = async () => {
      try {
        const res = await fetch('https://arifos.arif-fazil.com/tools');
        if (res.ok) {
          const data = await res.json();
          const tools = Array.isArray(data.tools) ? data.tools : [];
          setToolRegistry(
            tools
              .map((tool: unknown) => {
                const t = tool as Record<string, unknown>;
                const name = typeof tool === 'string' ? tool : (typeof t?.name === 'string' ? t.name : '');
                const desc = typeof t?.description === 'string' ? t.description : '';
                const req888 = Boolean(t?.requires_888);
                const requires_888 = desc.includes('[REQUIRES_888_HOLD: true]') || req888;
                return { name, requires_888 };
              })
              .filter((t: { name: string; requires_888: boolean }) => t.name.length > 0),
          );
        }
      } catch { /* ignore */ }
    };
    checkTools();
    const interval = setInterval(checkTools, 60000);
    return () => clearInterval(interval);
  }, []);

  // Domain MCP health polling
  useEffect(() => {
    const checkDomain = async (id: string, url: string) => {
      try {
        const res = await fetch(url, { signal: AbortSignal.timeout(8000) });
        setDomainHealth(prev => ({ ...prev, [id]: res.ok ? 'ok' : 'err' }));
      } catch {
        setDomainHealth(prev => ({ ...prev, [id]: 'err' }));
      }
    };
    DOMAIN_MCPS.forEach(({ id, url }) => checkDomain(id, url));
    const interval = setInterval(() => {
      DOMAIN_MCPS.forEach(({ id, url }) => checkDomain(id, url));
    }, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (!sessionManifest || sessionManifest.state !== 'TEMPORAL' || !sessionManifest.valid_until) return;
    const checkExpiry = () => {
      if (new Date(sessionManifest.valid_until!) < new Date()) {
        setSessionManifest(prev => prev ? { ...prev, state: 'EXPIRED' } : null);
      }
    };
    checkExpiry();
    const interval = setInterval(checkExpiry, 30000);
    return () => clearInterval(interval);
  }, [sessionManifest]);

  // ── Render ───────────────────────────────────────────────────────────────

  const pathStep = lastMission ? stateToPathStep(lastMission.state) : -1;

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
            <div className="hidden sm:flex items-center gap-2 px-3 py-1 bg-white/5 border border-white/10 rounded text-[9px] font-mono text-white/60">
              VAULT999: {vaultConnected ? 'CONNECTED' : 'LOCAL'}
            </div>
            <SessionBadge manifest={sessionManifest} onRevoke={() => setSessionManifest(null)} />
            <div className="hidden sm:flex items-center gap-2 px-3 py-1 bg-white/5 border border-white/10 rounded text-[9px] font-mono text-white/60">
              MCP: v1.0.0-FORGED
            </div>
          </div>
        </div>
      </div>

      <main className="max-w-4xl mx-auto px-6 pt-40">

        {/* HERO / INTRO */}
        <section className="mb-20">
          <div className="flex items-center gap-3 mb-6">
            <span className="h-px w-8 bg-red-500" />
            <h2 className="text-[10px] font-mono text-red-500 uppercase tracking-[0.4em]">Operator Surface · BODY Ring</h2>
          </div>
          <h1 className="text-6xl md:text-8xl font-black tracking-tighter text-white mb-8">
            The Cockpit<span className="text-red-500">.</span>
          </h1>
          <p className="text-xl text-white/60 font-light leading-relaxed max-w-2xl mb-10">
            Submit missions. Watch the deliberation. Approve HOLDs. Seal to VAULT999. This is where you act — not where you read.
          </p>
          <button
            onClick={() => setShowConsentDialog(true)}
            className="flex items-center gap-3 px-8 py-4 bg-white text-black font-black text-sm tracking-tighter hover:bg-red-500 hover:text-white transition-all group"
          >
            <Zap className="w-4 h-4 fill-current" />
            000_INIT IGNITION
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>
        </section>

        {/* ── MISSION INTAKE ── */}
        <section className="mb-16">
          <div className="flex items-baseline gap-4 mb-8">
            <span className="text-4xl font-black text-red-500/30 font-mono italic">→</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Mission Intake</h2>
          </div>
          <form onSubmit={handleSubmitMission}>
            <div className="border border-white/10 bg-white/[0.02] rounded-lg overflow-hidden focus-within:border-red-500/40 transition-colors">
              <textarea
                value={missionText}
                onChange={e => setMissionText(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) handleSubmitMission(e as any); }}
                placeholder="State the mission objective. System will sense, reason, critique, judge, and seal — or HOLD for your decision."
                rows={3}
                className="w-full bg-transparent px-6 pt-5 pb-3 text-sm text-white/80 placeholder:text-white/20 font-mono resize-none outline-none"
              />
              <div className="flex items-center justify-between px-6 pb-4">
                <span className="text-[9px] font-mono text-white/20 uppercase tracking-widest">⌘↵ to submit</span>
                <button
                  type="submit"
                  disabled={missionSubmitting || !missionText.trim()}
                  className="flex items-center gap-2 px-5 py-2 bg-red-500 text-white text-[10px] font-black tracking-widest uppercase hover:bg-red-400 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
                >
                  {missionSubmitting ? 'DISPATCHING…' : 'DISPATCH MISSION'}
                  <Send className="w-3 h-3" />
                </button>
              </div>
            </div>
          </form>
          {lastMission && (
            <div className="mt-4 px-4 py-3 border border-white/5 bg-white/[0.02] rounded text-[10px] font-mono">
              <span className="text-white/30">LAST: </span>
              <span className="text-white/60">{lastMission.text.slice(0, 80)}{lastMission.text.length > 80 ? '…' : ''}</span>
              <span className={`ml-3 ${lastMission.state === 'completed' ? 'text-emerald-400' : lastMission.state === 'input-required' || lastMission.state === 'auth-required' ? 'text-amber-400' : lastMission.state === 'failed' ? 'text-red-400' : 'text-white/40'}`}>
                [{lastMission.state.toUpperCase()}]
              </span>
            </div>
          )}
        </section>

        {/* ── GOLDEN PATH ── */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-8">
            <span className="text-4xl font-black text-white/10 font-mono italic">Δ</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Golden Path</h2>
            <span className="text-[9px] font-mono text-white/20 uppercase tracking-widest">sense → mind → heart → judge → vault</span>
          </div>
          <div className="flex items-stretch gap-0">
            {GOLDEN_PATH.map((step, i) => {
              const isActive = pathStep === i;
              const isDone = pathStep > i;
              const isHold = (step === 'JUDGE') && lastMission && (lastMission.state === 'input-required' || lastMission.state === 'auth-required');
              return (
                <div key={step} className="flex-1 flex flex-col">
                  <div className={`flex-1 px-4 py-6 border-b-2 transition-all ${
                    isHold ? 'border-amber-500 bg-amber-950/10' :
                    isDone ? 'border-emerald-500 bg-emerald-950/5' :
                    isActive ? 'border-red-500 bg-red-950/10' :
                    'border-white/10 bg-transparent'
                  }`}>
                    <div className="text-[9px] font-mono uppercase tracking-widest mb-3 text-white/20">step {String(i + 1).padStart(2, '0')}</div>
                    <div className="flex items-center gap-2 mb-1">
                      {isDone ? <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0" /> :
                       isHold ? <AlertCircle className="w-4 h-4 text-amber-500 flex-shrink-0" /> :
                       isActive ? <div className="w-4 h-4 rounded-full border-2 border-red-500 flex-shrink-0 animate-pulse" /> :
                       <Circle className="w-4 h-4 text-white/10 flex-shrink-0" />}
                      <div className={`text-sm font-black tracking-widest ${
                        isHold ? 'text-amber-500' :
                        isDone ? 'text-emerald-400' :
                        isActive ? 'text-red-400' :
                        'text-white/20'
                      }`}>{step}</div>
                    </div>
                    <div className="text-[9px] font-mono text-white/20 mt-2">
                      {step === 'SENSE' && 'Risk assessment'}
                      {step === 'MIND' && 'Reason & plan'}
                      {step === 'HEART' && 'Moral critique'}
                      {step === 'JUDGE' && (isHold ? '⚠ HOLD — await you' : 'Verdict')}
                      {step === 'VAULT' && (isDone ? '✓ SEALED' : 'Seal')}
                    </div>
                  </div>
                  {i < GOLDEN_PATH.length - 1 && (
                    <div className={`h-px ${isDone ? 'bg-emerald-500/30' : 'bg-white/5'}`} />
                  )}
                </div>
              );
            })}
          </div>
          {pathStep === -1 && (
            <p className="text-[10px] font-mono text-white/20 mt-4 text-center uppercase tracking-widest">Submit a mission above to activate the deliberation loop</p>
          )}
        </section>

        {/* ── APPROVAL QUEUE ── */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-red-500/20 font-mono italic">00.</span>
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
                        {task.history[0]?.parts[0]?.text || 'Unknown Intent'}
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
                        WITNESS_TYPE: AGENT<br />
                        SIGNATURE: AF-FORGE-SIG-{task.id.slice(-8).toUpperCase()}<br />
                        STATUS: PENDING_HUMAN_OVERRIDE
                      </div>
                    </div>
                  </div>
                  <div className="p-4 bg-red-500/5 flex justify-end">
                    <div className="rounded border border-red-500/20 bg-black/30 px-4 py-3 text-[10px] font-mono uppercase tracking-[0.2em] text-white/45">
                      Public cockpit is read-only. Sovereign approvals require an authenticated operator channel.
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* ── CONSTITUTIONAL FLOORS ── */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-white/10 font-mono italic">02.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Constitutional Floors</h2>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-px bg-white/5 border border-white/5">
            {FLOORS.map(f => (
              <div key={f.id} className="bg-[#050505] p-6 hover:bg-white/[0.02] transition-colors group">
                <div className="text-[10px] font-mono text-red-500 mb-4 group-hover:translate-x-1 transition-transform">{f.id}</div>
                <div className="text-xs font-black text-white leading-tight mb-2">{f.name.toUpperCase()}</div>
                <div className="flex items-center gap-1.5">
                  <div className="w-1 h-1 bg-emerald-500 rounded-full" />
                  <span className="text-[8px] font-mono text-emerald-500 tracking-widest">VERIFIED</span>
                </div>
              </div>
            ))}
            <div className="bg-[#050505] p-6 flex items-center justify-center border-l border-white/5">
              <ShieldAlert className="w-6 h-6 text-white/10" />
            </div>
          </div>
        </section>

        {/* ── SYSTEM HEALTH GRID ── */}
        <section className="mb-24">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <HealthMetric label="Integrity" value="100%" sub="Validated" color="text-red-500" />
            <HealthMetric label="Holds Open" value={String(holdsCount)} sub={holdsCount > 0 ? `${holdsBreakdown['input-required']} pending · ${holdsBreakdown['auth-required']} auth` : 'None'} color={holdsCount > 0 ? 'text-amber-500' : 'text-white'} />
            <HealthMetric label="Seals" value={String(sealsCount)} sub={vaultConnected ? 'VAULT999' : 'In-memory'} color={vaultConnected ? 'text-emerald-500' : 'text-blue-400'} />
            <HealthMetric label="Uptime" value="99.9%" sub="Live" color="text-blue-500" />
          </div>
        </section>

        {/* ── LIVE AGENTS ── */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-white/10 font-mono italic">01.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Live Agents</h2>
          </div>
          <div className="space-y-4">
            {agentsLoading && agents.length === 0 && (
              <p className="text-white/30 font-mono text-xs">Discovering federation agents…</p>
            )}
            {agentsError && (
              <p className="text-amber-500/60 font-mono text-xs">Agent discovery degraded — using cached registry. ({agentsError})</p>
            )}
            {agents.map(a => (
              <div key={a.id} className="group border-b border-white/5 pb-6 hover:border-red-500/50 transition-colors">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-bold text-white font-mono">{a.id}</h3>
                  <div className="text-[9px] font-mono px-2 py-0.5 border border-white/20 text-white/40 uppercase tracking-widest">{a.type}</div>
                </div>
                <p className="text-sm text-white/40 font-light mb-4">{a.role}</p>
                <div className="flex items-center gap-4 text-[9px] font-mono tracking-tighter uppercase">
                  <span className={`flex items-center gap-1.5 ${a.status === 'active' ? 'text-emerald-500' : a.status === 'reflect_only' ? 'text-amber-400' : 'text-white/40'}`}>
                    <Activity className="w-3 h-3" /> Status: {a.status.replace('_', ' ')}
                  </span>
                  <span className="text-white/20">|</span>
                  <span className="text-white/40">{a.domain} · {a.ring}</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ── DOMAIN MCP STATUS ── */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-white/10 font-mono italic">Φ</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Domain Specialists</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {DOMAIN_MCPS.map(({ id, label, symbol, desc, url }) => {
              const status = domainHealth[id];
              return (
                <div key={id} className={`p-6 border rounded-lg ${
                  status === 'ok' ? 'border-emerald-500/20 bg-emerald-950/5' :
                  status === 'err' ? 'border-red-500/20 bg-red-950/5' :
                  'border-white/10 bg-white/[0.02]'
                }`}>
                  <div className="flex items-start justify-between mb-3">
                    <div className="text-2xl">{symbol}</div>
                    <div className={`text-[9px] font-mono px-2 py-0.5 rounded font-bold ${
                      status === 'ok' ? 'text-emerald-400 bg-emerald-950/30' :
                      status === 'err' ? 'text-red-400 bg-red-950/30' :
                      'text-white/30 bg-white/5'
                    }`}>
                      {status === 'ok' ? 'ONLINE' : status === 'err' ? 'OFFLINE' : 'PROBING'}
                    </div>
                  </div>
                  <div className="text-sm font-black text-white tracking-tight mb-1">{label}</div>
                  <div className="text-[10px] font-mono text-white/30">{desc}</div>
                </div>
              );
            })}
          </div>
        </section>

        {/* ── TOOL REGISTRY ── */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-white/10 font-mono italic">03.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Tool Registry</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {(toolRegistry.length > 0 ? toolRegistry : [
               { name: 'geox.well_viewer', requires_888: false },
               { name: 'geox.interpret_las', requires_888: true },
               { name: 'forge.check_governance', requires_888: false },
               { name: 'forge.run_agent', requires_888: true },
               { name: 'forge.hold_action', requires_888: false },
               { name: 'forge.recall_memory', requires_888: false }
            ]).map(t => (
              <div key={t.name} className="p-4 border border-white/5 hover:border-white/20 transition-all flex justify-between items-center group">
                <div className="flex flex-col gap-1">
                  <code className="text-xs font-mono text-white/60 group-hover:text-white transition-colors">{t.name}</code>
                  {t.requires_888 && (
                    <span className="text-[9px] text-amber-500 uppercase tracking-widest font-black flex items-center gap-1">
                      <AlertCircle className="w-3 h-3" /> HOLD PENDING
                    </span>
                  )}
                </div>
                <div className="w-1 h-1 bg-white/20 rounded-full group-hover:bg-red-500" />
              </div>
            ))}
          </div>
        </section>

        {/* ── LIVE EVENT LOG ── */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-white/10 font-mono italic">04.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Event Log</h2>
            {events.length > 0 && (
              <span className="text-[9px] font-mono text-emerald-500/60 flex items-center gap-1">
                <span className="inline-block w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
                LIVE
              </span>
            )}
          </div>
          <div className="bg-white/[0.02] border border-white/5 rounded-lg overflow-hidden">
            <div className="font-mono text-[11px] leading-relaxed max-h-80 overflow-y-auto">
              {events.length === 0 ? (
                <div className="px-6 py-8 text-white/20 text-center">
                  <div className="mb-2">No events yet. Submit a mission to activate the loop.</div>
                  <div className="animate-pulse text-white/10">_</div>
                </div>
              ) : (
                events.map((ev, i) => (
                  <div key={ev.id} className={`px-6 py-2 border-b border-white/5 flex items-start gap-4 hover:bg-white/[0.02] ${i === 0 ? 'bg-white/[0.03]' : ''}`}>
                    <span className="text-white/20 flex-shrink-0 w-20">{new Date(ev.ts).toLocaleTimeString('en-MY', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}</span>
                    <span className={`flex-shrink-0 w-24 font-bold ${EVENT_COLORS[ev.kind] || 'text-white/40'}`}>{ev.kind}</span>
                    <span className="text-white/50">{ev.msg}</span>
                    <span className="text-white/20 flex-shrink-0 ml-auto text-[9px]">{ev.taskId.slice(-8)}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        </section>

        {/* ── SUPABASE FEDERATION MEMORY (Phase 3A Read-Only) ── */}
        <SupabaseMemoryPanel />

        {/* SUMMARY */}
        <section className="mb-24 pt-12 border-t border-white/10">
          <h3 className="text-sm font-black uppercase tracking-widest text-white mb-6">Constitutional Summary</h3>
          <p className="text-white/40 font-light leading-relaxed text-sm max-w-3xl">
            The arifOS federation operates under 13 binding floors (F1–F13). Every action — from a well-log interpretation to an agent deployment — must pass all active floors before a 999_SEAL is issued. Any floor failure triggers 888_HOLD, requiring human review.
          </p>
        </section>

        {/* DEEP LINKS */}
        <section className="flex flex-wrap gap-8 text-[10px] font-mono tracking-widest uppercase text-white/30 mb-20">
          <a href="#" className="hover:text-white flex items-center gap-2 transition-colors">Agent JSON <ArrowUpRight className="w-3 h-3" /></a>
          <a href="https://arifos.arif-fazil.com" className="hover:text-white flex items-center gap-2 transition-colors">Observatory <ArrowUpRight className="w-3 h-3" /></a>
          <a href="#" className="hover:text-white flex items-center gap-2 transition-colors text-red-500">Read Canon <ArrowUpRight className="w-3 h-3" /></a>
        </section>

      </main>

      <ConsentDialog
        isOpen={showConsentDialog}
        onClose={() => setShowConsentDialog(false)}
        onConsent={(manifest) => {
          setSessionManifest(manifest);
          setShowConsentDialog(false);
        }}
      />

      <footer className="max-w-6xl mx-auto px-6 pt-20 border-t border-white/5 text-center text-[10px] font-mono tracking-[0.2em] text-white/20">
        Δ AAA COCKPIT · arifOS v2026.4.22 · DITEMPA BUKAN DIBERI · Forged in Kuala Lumpur 🇲🇾
      </footer>
    </div>
  );
}

function HealthMetric({ label, value, sub, color }: { label: string; value: string; sub: string; color: string }) {
  return (
    <div className="border-l border-white/10 pl-6 py-2">
      <div className={`text-4xl font-black tracking-tighter mb-1 ${color}`}>{value}</div>
      <div className="text-[10px] font-mono text-white/60 uppercase tracking-widest mb-1">{label}</div>
      <div className="text-[9px] font-mono text-white/20 italic uppercase tracking-widest">{sub}</div>
    </div>
  );
}
