import { useState } from 'react';
import { 
  Shield, 
  Activity, 
  Terminal, 
  Clock, 
  CheckCircle2,
  AlertCircle,
  AlertTriangle,
  Database,
  Globe,
  ArrowUpRight,
  Info
} from 'lucide-react';

const FLOORS = [
  { id: 'F1', name: 'Amanah', status: 'PASS', time: '2026-04-22T02:41:00Z', desc: 'Reversibility' },
  { id: 'F2', name: 'Truth', status: 'PASS', time: '2026-04-22T02:41:00Z', desc: 'Accuracy' },
  { id: 'F3', name: 'Tri-Witness', status: 'PASS', time: '2026-04-22T02:41:00Z', desc: 'Consensus' },
  { id: 'F4', name: 'Clarity', status: 'PASS', time: '2026-04-22T02:41:00Z', desc: 'Entropy ↓' },
  { id: 'F5', name: 'Peace²', status: 'PASS', time: '2026-04-22T02:41:00Z', desc: 'Non-destruction' },
  { id: 'F6', name: 'Empathy', status: 'PASS', time: '2026-04-22T02:41:00Z', desc: 'RASA' },
  { id: 'F7', name: 'Humility', status: 'PASS', time: '2026-04-22T02:41:00Z', desc: 'Uncertainty Ω' },
  { id: 'F8', name: 'Genius', status: 'PASS', time: '2026-04-22T02:41:00Z', desc: 'Systemic Health' },
  { id: 'F9', name: 'Anti-Hantu', status: 'PASS', time: '2026-04-22T02:41:00Z', desc: 'No Persona' },
  { id: 'F10', name: 'Ontology', status: 'PASS', time: '2026-04-22T02:41:00Z', desc: 'No False Claims' },
  { id: 'F11', name: 'Auditability', status: 'PASS', time: '2026-04-22T02:41:00Z', desc: 'Transparency' },
  { id: 'F12', name: 'Resilience', status: 'PASS', time: '2026-04-22T02:41:00Z', desc: 'Graceful Failure' },
  { id: 'F13', name: 'Sovereign', status: 'PASS', time: '2026-04-22T02:41:00Z', desc: 'Human Override' },
];

const AGENTS = [
  { id: 'forge-explorer', role: 'Structural Analysis', state: 'IDLE', last: '2s ago' },
  { id: 'forge-coordinator', role: 'Task Orchestration', state: 'ACTIVE', last: '1s ago' },
  { id: 'arifos-guardian', role: 'Floor Enforcement', state: 'ACTIVE', last: '1s ago' },
  { id: 'geox-witness', role: 'Earth Verification', state: 'WAITING', last: '12s ago' },
];

const TOOLS = [
  { ns: 'geox.', name: 'interpret_las', risk: 'HIGH', floors: 'F1, F11, F13' },
  { ns: 'geox.', name: 'well_compute_petrophysics', risk: 'READ', floors: 'F2, F7' },
  { ns: 'forge.', name: 'check_governance', risk: 'READ', floors: 'F11' },
  { ns: 'forge.', name: 'run_agent', risk: 'HIGH', floors: 'F1, F11, F13' },
  { ns: 'vault.', name: 'seal_999', risk: 'HIGH', floors: 'F1, F11, F13' },
];

const EVENTS = [
  { time: '02:45:22', level: 'INFO', msg: 'Kernel connection established.' },
  { time: '02:45:23', level: 'INFO', msg: 'Sovereignty check complete (F13).' },
  { time: '02:46:01', level: 'WARN', msg: '888_HOLD raised: F1 Amanah violation' },
  { time: '02:46:15', level: 'OK', msg: '888_HOLD resolved: GEOX identity verified.' },
  { time: '02:47:15', level: 'INFO', msg: '999_SEAL issued: geox.interpret_las' },
];

export default function Cockpit() {
  return (
    <div className="min-h-screen bg-[#050505] text-[#e8eaf6] font-sans selection:bg-red-900/30">
      
      {/* 2️⃣ Status Header (Canonical) */}
      <header className="fixed top-[33px] left-0 right-0 z-50 bg-[#0b0d14] border-b border-[#1e2344] px-6 py-4 shadow-2xl">
        <div className="max-w-7xl mx-auto flex flex-col gap-3">
          <div className="flex justify-between items-center">
            <h1 className="text-sm font-black tracking-[0.2em] text-white">Δ AAA COCKPIT · arifOS v2026.4.22 · DITEMPA BUKAN DIBERI</h1>
            <div className="flex gap-4 text-[10px] font-mono text-[#7b82a3] tracking-widest uppercase">
              <span className="text-white/60">Ψ Identity</span>
              <span className="text-white/60">Theory</span>
              <span className="text-white font-bold border-b border-white">Constitution</span>
            </div>
          </div>
          <div className="flex justify-between items-center border-t border-[#1e2344]/50 pt-3">
            <div className="flex gap-8 text-[10px] font-mono tracking-widest uppercase">
               <span className="text-white/40 italic">Φ Earth</span>
               <span className="text-[#d4a853] font-bold">Ω Wealth</span>
               <span className="text-white font-bold">Ω★ Kernel</span>
            </div>
            <div className="flex gap-4">
              <StatusBadge label="KERNEL" value="ONLINE" color="emerald" pulse />
              <StatusBadge label="VAULT999" value="CONNECTED" color="emerald" />
              <StatusBadge label="MCP" value="v2.0.0-FORGED" color="amber" />
              <StatusBadge label="A2A" value="0.3.0-HEALTHY" color="emerald" />
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 pt-44 pb-20">
        
        {/* 1️⃣ Core Purpose Banner */}
        <section className="mb-10 p-6 rounded-lg border border-emerald-900/20 bg-emerald-950/5 flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <h2 className="text-md font-bold text-white mb-1 flex items-center gap-2">
              <Activity className="w-4 h-4 text-emerald-500" />
              AAA Cockpit is a live constitutional observatory for the arifOS federation.
            </h2>
            <p className="text-xs text-[#7b82a3] font-light">It shows state, not control. This is the instrument panel, not the engine.</p>
          </div>
          <div className="flex flex-wrap gap-4 text-[9px] font-mono uppercase tracking-widest">
            <span className="text-emerald-500 flex items-center gap-1.5"><CheckCircle2 className="w-3 h-3"/> Real-time Visibility</span>
            <span className="text-red-500 flex items-center gap-1.5"><Circle className="w-3 h-3 fill-red-500"/> No Agent Control</span>
            <span className="text-emerald-500 flex items-center gap-1.5"><CheckCircle2 className="w-3 h-3"/> Human Transparency</span>
            <span className="text-red-500 flex items-center gap-1.5"><Circle className="w-3 h-3 fill-red-500"/> No Tool Execution</span>
          </div>
        </section>

        <div className="grid grid-cols-12 gap-6">
          
          {/* 3️⃣ Constitutional Floors Panel */}
          <div className="col-span-12 lg:col-span-8">
            <div className="mb-3 flex items-center gap-2 text-[#7b82a3] font-mono text-[10px] uppercase tracking-widest">
              <Shield className="w-3 h-3" />
              <span>01 · CONSTITUTIONAL FLOORS (F1–F13)</span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-2">
              {FLOORS.map((f) => (
                <div key={f.id} className="p-2.5 rounded border border-[#1e2344] bg-[#0b0d14] flex flex-col justify-between min-h-[90px]">
                  <div className="flex justify-between items-start">
                    <span className="text-[10px] font-mono text-red-600 font-black">{f.id}</span>
                    <span className={`text-[8px] font-bold ${f.status === 'PASS' ? 'text-emerald-500' : 'text-red-500'}`}>{f.status}</span>
                  </div>
                  <div>
                    <div className="text-[10px] font-bold text-white uppercase">{f.name}</div>
                    <div className="text-[8px] text-[#444] mb-1">{f.desc}</div>
                    <div className="text-[7px] font-mono text-[#333]">{f.time.split('T')[1].replace('Z', '')}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 4️⃣ Live System Health */}
          <div className="col-span-12 lg:col-span-4">
            <div className="mb-3 flex items-center gap-2 text-[#7b82a3] font-mono text-[10px] uppercase tracking-widest">
              <Activity className="w-3 h-3" />
              <span>02 · SYSTEM HEALTH</span>
            </div>
            <div className="grid grid-cols-2 gap-2 h-[calc(100%-24px)]">
              <MetricCard label="Integrity" value="100%" color="red" />
              <MetricCard label="Holds Open" value="0" color="amber" />
              <MetricCard label="Seals Issued" value="1,284" color="emerald" />
              <MetricCard label="Uptime" value="99.9%" color="blue" />
            </div>
          </div>

          {/* 5️⃣ Live Agents Registry */}
          <div className="col-span-12 lg:col-span-6">
            <div className="mb-3 flex items-center gap-2 text-[#7b82a3] font-mono text-[10px] uppercase tracking-widest">
              <Terminal className="w-3 h-3" />
              <span>03 · LIVE AGENT REGISTRY</span>
            </div>
            <div className="overflow-hidden rounded border border-[#1e2344] bg-[#0b0d14]">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-[#11142a] text-[9px] font-mono text-[#7b82a3] uppercase tracking-widest border-b border-[#1e2344]">
                    <th className="px-4 py-2 font-normal">agent_id</th>
                    <th className="px-4 py-2 font-normal">role</th>
                    <th className="px-4 py-2 font-normal">state</th>
                    <th className="px-4 py-2 font-normal">last_heartbeat</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1e2344]/50">
                  {AGENTS.map(a => (
                    <tr key={a.id} className="text-[10px] font-mono">
                      <td className="px-4 py-3 text-white font-bold">{a.id}</td>
                      <td className="px-4 py-3 text-[#7b82a3]">{a.role}</td>
                      <td className="px-4 py-3">
                         <span className={a.state === 'ACTIVE' ? 'text-emerald-500' : 'text-[#444]'}>{a.state}</span>
                      </td>
                      <td className="px-4 py-3 text-[#333]">{a.last}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* 6️⃣ Tool Registry */}
          <div className="col-span-12 lg:col-span-6">
            <div className="mb-3 flex items-center gap-2 text-[#7b82a3] font-mono text-[10px] uppercase tracking-widest">
              <Terminal className="w-3 h-3" />
              <span>04 · TOOL REGISTRY</span>
            </div>
            <div className="overflow-hidden rounded border border-[#1e2344] bg-[#0b0d14]">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-[#11142a] text-[9px] font-mono text-[#7b82a3] uppercase tracking-widest border-b border-[#1e2344]">
                    <th className="px-4 py-2 font-normal">namespace.tool</th>
                    <th className="px-4 py-2 font-normal">risk</th>
                    <th className="px-4 py-2 font-normal">bound_floors</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1e2344]/50">
                  {TOOLS.map(t => (
                    <tr key={t.name} className="text-[10px] font-mono">
                      <td className="px-4 py-3">
                        <span className="text-blue-500">{t.ns}</span>
                        <span className="text-white">{t.name}</span>
                      </td>
                      <td className="px-4 py-3">
                         <span className={t.risk === 'HIGH' ? 'text-red-500 font-bold' : 'text-[#7b82a3]'}>{t.risk}</span>
                      </td>
                      <td className="px-4 py-3 text-[#444]">{t.floors}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* 7️⃣ Event Log */}
          <div className="col-span-12 lg:col-span-4">
            <div className="mb-3 flex items-center gap-2 text-[#7b82a3] font-mono text-[10px] uppercase tracking-widest">
              <Clock className="w-3 h-3" />
              <span>05 · EVENT LOG (APPEND-ONLY)</span>
            </div>
            <div className="h-[180px] overflow-y-auto rounded border border-[#1e2344] bg-[#000] p-4 font-mono text-[9px] tracking-tight leading-relaxed">
              {EVENTS.map((e, i) => (
                <div key={i} className="mb-1.5 flex gap-3 opacity-70">
                   <span className="text-[#333]">{e.time}</span>
                   <span className={`w-8 font-bold ${e.level === 'WARN' ? 'text-amber-500' : e.level === 'OK' ? 'text-emerald-500' : 'text-blue-500'}`}>{e.level}</span>
                   <span className="text-[#7b82a3]">{e.msg}</span>
                </div>
              ))}
              <div className="w-1.5 h-3 bg-red-600 animate-pulse mt-2" />
            </div>
          </div>

          {/* 8️⃣ Constitutional Summary */}
          <div className="col-span-12 lg:col-span-8">
            <div className="mb-3 flex items-center gap-2 text-[#7b82a3] font-mono text-[10px] uppercase tracking-widest">
              <Shield className="w-3 h-3" />
              <span>06 · CONSTITUTIONAL SUMMARY</span>
            </div>
            <div className="rounded border border-[#1e2344] bg-[#0b0d14] p-6">
              <div className="grid md:grid-cols-2 gap-8 text-[11px] leading-relaxed">
                <div className="space-y-4">
                  <p>
                    <strong className="text-white block mb-1">The 13 Floors</strong>
                    The arifOS federation operates under 13 binding constitutional floors (F1–F13). Every agent action must pass all active floors before a 999_SEAL is issued.
                  </p>
                  <p>
                    <strong className="text-white block mb-1">999_SEAL</strong>
                    Represents the terminal state of a governed action. It is an immutable cryptographic commitment to the Vault999 ledger.
                  </p>
                </div>
                <div className="space-y-4">
                  <p>
                    <strong className="text-white block mb-1">888_HOLD</strong>
                    Any floor violation or high-stakes uncertainty triggers an 888_HOLD, which suspends the action and requires manual human review.
                  </p>
                  <p>
                    <strong className="text-white block mb-1">Final Authority</strong>
                    Muhammad Arif bin Fazil (888_JUDGE) holds ultimate sovereign authority over the federation, acting as the external oracle for system consistency.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* 9️⃣ Read-Only Deep Links */}
          <div className="col-span-12">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <DeepLink label="View Constitutional Canon" url="https://apex.arif-fazil.com" />
              <DeepLink label="Kernel Health Diagnostics" url="#" />
              <DeepLink label="VAULT999 Receipt Explorer" url="#" />
              <DeepLink label="Agent Card (/.well-known)" url="https://aaa.arif-fazil.com/.well-known/agent.json" />
            </div>
          </div>

        </div>
      </main>

      <footer className="border-t border-[#1e2344] py-12 bg-[#050505] text-center">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-[9px] font-mono text-[#333] uppercase tracking-[0.4em] mb-4">
             AAA Cockpit is the altimeter, not the engine. The compass, not the wheel.
          </div>
          <div className="text-[10px] font-mono text-[#7b82a3] uppercase tracking-[0.1em]">
             Δ AAA COCKPIT · arifOS v2026.4.22 · DITEMPA BUKAN DIBERI · Forged in Kuala Lumpur 🇲🇾
          </div>
        </div>
      </footer>
    </div>
  );
}

function StatusBadge({ label, value, color, pulse }: { label: string, value: string, color: string, pulse?: boolean }) {
  const colorMap: any = {
    emerald: 'text-emerald-500 border-emerald-500/20 bg-emerald-500/5',
    amber: 'text-[#d4a853] border-[#d4a853]/20 bg-[#d4a853]/5',
  };
  return (
    <div className={`flex items-center gap-2 px-2.5 py-1 rounded border text-[8px] font-mono font-black tracking-widest ${colorMap[color]}`}>
      {pulse && <div className="w-1.5 h-1.5 rounded-full bg-current animate-pulse" />}
      <span>{label}: {value}</span>
    </div>
  );
}

function MetricCard({ label, value, color }: { label: string, value: string, color: string }) {
  const colorMap: any = {
    red: 'text-red-600',
    amber: 'text-[#d4a853]',
    emerald: 'text-emerald-500',
    blue: 'text-blue-500',
  };
  return (
    <div className="p-4 rounded border border-[#1e2344] bg-[#0b0d14] flex flex-col items-center justify-center">
      <div className={`text-xl font-mono font-black ${colorMap[color]}`}>{value}</div>
      <div className="text-[8px] text-[#444] uppercase font-bold tracking-widest mt-1">{label}</div>
    </div>
  );
}

function DeepLink({ label, url }: { label: string, url: string }) {
  return (
    <a href={url} className="flex items-center justify-between p-3 rounded border border-[#1e2344] bg-[#11142a]/20 hover:border-red-900/40 hover:bg-red-950/5 transition-all group">
      <span className="text-[9px] font-bold text-[#7b82a3] group-hover:text-white uppercase tracking-wider">{label}</span>
      <ArrowUpRight className="w-3 h-3 text-[#333] group-hover:text-red-500" />
    </a>
  );
}
