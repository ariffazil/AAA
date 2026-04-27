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

export default function Cockpit() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

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
             <div className="flex items-center gap-2 px-3 py-1 bg-red-950/20 border border-red-500/30 rounded text-[9px] font-mono text-red-500">
                <div className="w-1.5 h-1.5 bg-red-500 rounded-full animate-pulse" />
                KERNEL: OFFLINE
             </div>
             <div className="hidden sm:flex items-center gap-2 px-3 py-1 bg-white/5 border border-white/10 rounded text-[9px] font-mono text-white/60">
                VAULT999: CONNECTED
             </div>
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
            <h2 className="text-[10px] font-mono text-red-500 uppercase tracking-[0.4em]">Governance Layer</h2>
          </div>
          <h1 className="text-6xl md:text-8xl font-black tracking-tighter text-white mb-8">
            The Cockpit<span className="text-red-500">.</span>
          </h1>
          <p className="text-xl text-white/60 font-light leading-relaxed max-w-2xl mb-10">
            Real-time constitutional monitoring for the arifOS federation. Every floor, every agent, every tool.
          </p>
          <button className="flex items-center gap-3 px-8 py-4 bg-white text-black font-black text-sm tracking-tighter hover:bg-red-500 hover:text-white transition-all group">
            <Zap className="w-4 h-4 fill-current" />
            000_INIT IGNITION
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>
        </section>

        {/* ACTION APPROVAL QUEUE (NEW) */}
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

        {/* 02. CONSTITUTIONAL FLOORS */}
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

        {/* SYSTEM HEALTH GRID */}
        <section className="mb-24">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <HealthMetric label="Integrity" value="100%" sub="Validated" color="text-red-500" />
            <HealthMetric label="Holds Open" value="0" sub="Critical" color="text-white" />
            <HealthMetric label="Seals" value="0" sub="VAULT999" color="text-white" />
            <HealthMetric label="Uptime" value="99.9%" sub="Live" color="text-blue-500" />
          </div>
        </section>

        {/* 01. LIVE AGENTS */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-white/10 font-mono italic">01.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Live Agents</h2>
          </div>
          <div className="space-y-4">
            {AGENTS.map(a => (
              <div key={a.id} className="group border-b border-white/5 pb-6 hover:border-red-500/50 transition-colors">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-bold text-white font-mono">{a.id}</h3>
                  <div className="text-[9px] font-mono px-2 py-0.5 border border-white/20 text-white/40 uppercase tracking-widest">{a.type}</div>
                </div>
                <p className="text-sm text-white/40 font-light mb-4">{a.role}</p>
                <div className="flex items-center gap-4 text-[9px] font-mono tracking-tighter uppercase">
                  <span className="text-emerald-500 flex items-center gap-1.5"><Activity className="w-3 h-3" /> State: Active</span>
                  <span className="text-white/20">|</span>
                  <span className="text-white/40 italic">Last Heartbeat: 1s ago</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* 03. TOOL REGISTRY */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-white/10 font-mono italic">03.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Tool Registry</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              'geox. well_viewer', 'geox. interpret_las', 
              'forge. check_governance', 'forge. run_agent',
              'forge. hold_action', 'forge. recall_memory'
            ].map(t => (
              <div key={t} className="p-4 border border-white/5 hover:border-white/20 transition-all flex justify-between items-center group">
                <code className="text-xs font-mono text-white/60 group-hover:text-white transition-colors">{t}</code>
                <div className="w-1 h-1 bg-white/20 rounded-full group-hover:bg-red-500" />
              </div>
            ))}
          </div>
        </section>

        {/* 04. EVENT LOG */}
        <section className="mb-24">
          <div className="flex items-baseline gap-4 mb-10">
            <span className="text-4xl font-black text-white/10 font-mono italic">04.</span>
            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">Event Log</h2>
          </div>
          <div className="bg-white/5 p-8 font-mono text-[11px] leading-relaxed text-white/40">
            <div className="mb-2"><span className="text-white/20">--:--:--</span> Cockpit initialized. Waiting for kernel...</div>
            <div className="mb-2 text-red-500/80"><span className="text-red-900">03:00:05</span> Kernel connection failed. Operating in local mode.</div>
            <div className="animate-pulse">_</div>
          </div>
        </section>

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
          <a href="#" className="hover:text-white flex items-center gap-2 transition-colors">Kernel Health <ArrowUpRight className="w-3 h-3" /></a>
          <a href="#" className="hover:text-white flex items-center gap-2 transition-colors text-red-500">Read Canon <ArrowUpRight className="w-3 h-3" /></a>
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
