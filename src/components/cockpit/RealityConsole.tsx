/**
 * RealityConsole — The AREP Cockpit
 * ═══════════════════════════════════════
 * 
 * Three-pane reality engineering console that replaces prompt engineering.
 * 
 * Pane 1: INTENT BOARD   — Active tasks, delegation chains, lifecycle state
 * Pane 2: REALITY FEED    — Live evidence: health probes, organ status, layer progression
 * Pane 3: VERDICT QUEUE   — HOLDs awaiting Arif, floor vetoes, governance posture
 * 
 * The prompt was never visible. The reality was.
 * 
 * Coined by Muhammad Arif bin Fazil (F13 SOVEREIGN), forged 2026-06-04.
 * DITEMPA BUKAN DIBERI
 */

import React, { useState, useEffect, useCallback } from 'react';
import type { TaskState } from '../../gateway/schema';
import {
  realityLayerBadge,
  autonomyBandBadge,
  type AREPTask,
  type RealityLayer,
  type AutonomyBand,
  type DelegationLink,
  type GovernanceVerdict,
} from '../../gateway/arep-types';

// ═══════════════════════════════════════════════════════════════════

interface OrganHealthProbe {
  organ: string;
  name: string;
  critical: boolean;
  healthy: boolean;
  status: 'GREEN' | 'YELLOW' | 'RED';
  statusCode: number;
  latencyMs: number;
}

interface RealityFeedState {
  organs: OrganHealthProbe[];
  allHealthy: boolean;
  criticalHealthy: boolean;
  summary: string;
  probedAt: string | null;
  loading: boolean;
  error: string | null;
}

interface VerdictItem {
  taskId: string;
  intent: string;
  verdict: GovernanceVerdict;
  reason: string;
  timestamp: string;
  evidenceLayer: RealityLayer;
  autonomyBand: AutonomyBand;
}

type HoldsResponse = {
  holds?: HoldRecord[] | number;
};

type HoldRecord = {
  task_id?: string;
  id?: string;
  intent?: string;
  description?: string;
  verdict?: GovernanceVerdict;
  reason?: string;
  message?: string;
  created_at?: string;
  timestamp?: string;
  evidence_layer?: RealityLayer;
  autonomy_band?: AutonomyBand;
};

function errorMessage(error: unknown, fallback: string): string {
  return error instanceof Error ? error.message : fallback;
}

// ═══════════════════════════════════════════════════════════════════
// MAIN COMPONENT
// ═══════════════════════════════════════════════════════════════════

export default function RealityConsole() {
  const [activePane, setActivePane] = useState<'intent' | 'reality' | 'verdict'>('intent');
  const [tasks, setTasks] = useState<AREPTask[]>([]);
  const [realityFeed, setRealityFeed] = useState<RealityFeedState>({
    organs: [],
    allHealthy: false,
    criticalHealthy: false,
    summary: 'Probing...',
    probedAt: null,
    loading: true,
    error: null,
  });
  const [verdicts, setVerdicts] = useState<VerdictItem[]>([]);

  // ── Reality Feed: probe federation health ──────────────────────
  const probeReality = useCallback(async () => {
    setRealityFeed(prev => ({ ...prev, loading: true, error: null }));
    try {
      const organPorts: Record<string, { url: string; name: string; critical: boolean }> = {
        arifos: { url: 'https://arifos.arif-fazil.com/health', name: 'arifOS Kernel', critical: true },
        geox: { url: 'https://geox.arif-fazil.com/health', name: 'GEOX Earth', critical: false },
        wealth: { url: 'https://wealth.arif-fazil.com/health', name: 'WEALTH Capital', critical: false },
        well: { url: 'https://well.arif-fazil.com/health', name: 'WELL Vitality', critical: false },
        aforge: { url: 'https://forge.arif-fazil.com/health', name: 'A-FORGE Execution', critical: true },
        aaa: { url: '/health', name: 'AAA Control Plane', critical: true },
      };

      const probes: OrganHealthProbe[] = [];
      for (const [key, cfg] of Object.entries(organPorts)) {
        const start = Date.now();
        try {
          const res = await fetch(cfg.url, {
            signal: AbortSignal.timeout(5000),
          });
          probes.push({
            organ: key,
            name: cfg.name,
            critical: cfg.critical,
            healthy: res.ok,
            status: res.ok ? 'GREEN' : 'RED',
            statusCode: res.status,
            latencyMs: Date.now() - start,
          });
        } catch {
          probes.push({
            organ: key,
            name: cfg.name,
            critical: cfg.critical,
            healthy: false,
            status: 'RED',
            statusCode: 0,
            latencyMs: Date.now() - start,
          });
        }
      }

      const allHealthy = probes.every(p => p.healthy);
      const criticalHealthy = probes.filter(p => p.critical).every(p => p.healthy);
      let summary: string;
      if (allHealthy) summary = 'GREEN — all organs healthy';
      else if (criticalHealthy) summary = 'YELLOW — critical OK, non-critical degraded';
      else summary = 'RED — critical organ(s) unhealthy';

      setRealityFeed({
        organs: probes,
        allHealthy,
        criticalHealthy,
        summary,
        probedAt: new Date().toISOString(),
        loading: false,
        error: null,
      });
    } catch (err: unknown) {
      setRealityFeed(prev => ({
        ...prev,
        loading: false,
        error: errorMessage(err, 'Probe failed'),
      }));
    }
  }, []);

  // ── Fetch AREP tasks from operator endpoint ────────────────────
  const fetchTasks = useCallback(async () => {
    try {
      const res = await fetch('/operator/tasks?state=all');
      if (!res.ok) return;
      const data = await res.json() as { tasks?: AREPTask[] };
      if (data.tasks) setTasks(data.tasks);
    } catch {
      // gracefully degrade
    }
  }, []);

  // ── Fetch verdicts ─────────────────────────────────────────────
  const fetchVerdicts = useCallback(async () => {
    try {
      const res = await fetch('/operator/holds');
      if (!res.ok) return;
      const data = await res.json() as HoldsResponse;
      const holds = Array.isArray(data.holds) ? data.holds : [];
      if (holds.length > 0) {
        setVerdicts(holds.map((h) => ({
          taskId: h.task_id || h.id || 'unknown',
          intent: h.intent || h.description || 'unknown',
          verdict: (h.verdict || 'HOLD') as GovernanceVerdict,
          reason: h.reason || h.message || '',
          timestamp: h.created_at || h.timestamp || '',
          evidenceLayer: (h.evidence_layer || 'INFERRED') as RealityLayer,
          autonomyBand: (h.autonomy_band || 'YELLOW') as AutonomyBand,
        })));
      }
    } catch {
      // gracefully degrade
    }
  }, []);

  // ── Lifecycle ──────────────────────────────────────────────────
  useEffect(() => {
    probeReality();
    fetchTasks();
    fetchVerdicts();
    const interval = setInterval(() => {
      probeReality();
      fetchTasks();
      fetchVerdicts();
    }, 15000);
    return () => clearInterval(interval);
  }, [probeReality, fetchTasks, fetchVerdicts]);

  // ═══════════════════════════════════════════════════════════════
  // RENDER
  // ═══════════════════════════════════════════════════════════════

  const overallVerdict = realityFeed.allHealthy ? 'GREEN' : realityFeed.criticalHealthy ? 'YELLOW' : 'RED';

  return (
    <div className="space-y-4">
      {/* ── Header ─────────────────────────────────────────── */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex min-w-0 flex-wrap items-center gap-3">
          <h2 className="text-lg font-semibold text-white font-mono tracking-tight">
            ⊜ REALITY CONSOLE
          </h2>
          <span className={`px-2 py-0.5 rounded text-xs font-mono ${
            overallVerdict === 'GREEN' ? 'bg-emerald-900/50 text-emerald-400 border border-emerald-700' :
            overallVerdict === 'YELLOW' ? 'bg-amber-900/50 text-amber-400 border border-amber-700' :
            'bg-red-900/50 text-red-400 border border-red-700'
          }`}>
            {overallVerdict}
          </span>
          <span className="text-xs text-zinc-500 font-mono">
            AREP v1.0
          </span>
        </div>

        {/* Pane tabs */}
        <div className="max-w-full overflow-x-auto bg-zinc-800 rounded-lg p-0.5">
          <div className="flex w-max gap-1">
          {(['intent', 'reality', 'verdict'] as const).map(pane => (
            <button
              key={pane}
              onClick={() => setActivePane(pane)}
              className={`px-3 py-1 rounded text-xs font-mono transition-colors ${
                activePane === pane
                  ? 'bg-zinc-700 text-white'
                  : 'text-zinc-500 hover:text-zinc-300'
              }`}
            >
              {pane === 'intent' ? 'INTENT BOARD' : pane === 'reality' ? 'REALITY FEED' : 'VERDICT QUEUE'}
            </button>
          ))}
          </div>
        </div>
      </div>

      {/* ── Reality Feed Status Strip ────────────────────────── */}
      <div className="grid grid-cols-6 gap-2">
        {realityFeed.organs.map(org => (
          <div
            key={org.organ}
            className={`flex items-center gap-1.5 px-2 py-1 rounded text-xs font-mono border ${
              org.healthy
                ? 'bg-emerald-900/20 border-emerald-800 text-emerald-400'
                : org.critical
                  ? 'bg-red-900/30 border-red-800 text-red-400'
                  : 'bg-amber-900/20 border-amber-800 text-amber-400'
            }`}
          >
            <span className={`w-1.5 h-1.5 rounded-full ${
              org.healthy ? 'bg-emerald-400' : org.critical ? 'bg-red-400' : 'bg-amber-400'
            }`} />
            <span className="truncate">{org.organ}</span>
            {org.critical && <span className="text-[10px] opacity-60">★</span>}
          </div>
        ))}
      </div>

      {/* ── Pane Content ─────────────────────────────────────── */}
      <div className="border border-zinc-800 rounded-lg bg-zinc-900/50 min-h-[300px]">
        {activePane === 'intent' && <IntentBoard tasks={tasks} />}
        {activePane === 'reality' && <RealityFeedPane feed={realityFeed} onRefresh={probeReality} />}
        {activePane === 'verdict' && <VerdictQueuePane verdicts={verdicts} />}
      </div>

      {/* ── Footer: evidence layer summary ───────────────────── */}
      <div className="flex items-center gap-2 text-xs font-mono text-zinc-500">
        <span>Evidence floor:</span>
        <span className="text-emerald-400">VERIFIED_STATE ← live probes</span>
        <span className="text-zinc-600">|</span>
        <span>Probed: {realityFeed.probedAt ? new Date(realityFeed.probedAt).toLocaleTimeString() : 'never'}</span>
        <span className="text-zinc-600">|</span>
        <span>Model: F9 verified_only active</span>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════
// PANE 1: INTENT BOARD
// ═══════════════════════════════════════════════════════════════════

function IntentBoard({ tasks }: { tasks: AREPTask[] }) {
  if (tasks.length === 0) {
    return (
      <div className="p-6 text-center text-zinc-500 font-mono text-sm">
        <div className="text-lg mb-2">⊜</div>
        <div>No active AREP tasks.</div>
        <div className="text-xs mt-1 text-zinc-600">
          Submit intent via Mission Intake above
        </div>
      </div>
    );
  }

  return (
    <div className="divide-y divide-zinc-800">
      {tasks.map(task => (
        <IntentCard key={task.telemetry?.task_id || task.intent?.statement} task={task} />
      ))}
    </div>
  );
}

function IntentCard({ task }: { task: AREPTask }) {
  const state = task.task_lifecycle?.current_state || 'submitted';
  const stateColors: Record<TaskState, string> = {
    'submitted':      'bg-blue-900/30 text-blue-400 border-blue-700',
    'working':        'bg-amber-900/30 text-amber-400 border-amber-700',
    'input-required': 'bg-red-900/30 text-red-400 border-red-700',
    'completed':      'bg-emerald-900/30 text-emerald-400 border-emerald-700',
    'failed':         'bg-red-900/50 text-red-400 border-red-700',
    'canceled':       'bg-zinc-800 text-zinc-500 border-zinc-700',
    'rejected':       'bg-red-900/50 text-red-400 border-red-700',
    'auth-required':  'bg-purple-900/30 text-purple-400 border-purple-700',
    'unknown':        'bg-zinc-800 text-zinc-500 border-zinc-700',
  };

  const band = task.reality_constraints?.autonomy_band || 'GREEN';
  const bandBadge = autonomyBandBadge(band);
  const evidenceLayer = task.task_lifecycle?.state_history?.slice(-1)[0]?.evidence_layer_at_transition || 'INFERRED';
  const layerBadge = realityLayerBadge(evidenceLayer as RealityLayer);

  return (
    <div className="p-4 space-y-3">
      {/* Intent statement */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1">
          <div className="text-sm text-white font-mono">
            {task.intent?.statement || '(no intent)'}
          </div>
          {task.intent?.success_criteria && (
            <div className="flex flex-wrap gap-1 mt-1.5">
              {task.intent.success_criteria.map((c, i) => (
                <span key={i} className="text-[10px] px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 font-mono">
                  ✓ {c}
                </span>
              ))}
            </div>
          )}
        </div>
        <div className="flex flex-col items-end gap-1 shrink-0">
          <span className={`px-2 py-0.5 rounded text-[10px] font-mono border ${stateColors[state]}`}>
            {state.toUpperCase()}
          </span>
          <span
            className="px-2 py-0.5 rounded text-[10px] font-mono border"
            style={{ color: bandBadge.color, borderColor: bandBadge.color, backgroundColor: `${bandBadge.color}15` }}
          >
            {bandBadge.label}
          </span>
        </div>
      </div>

      {/* Delegation chain */}
      {task.delegation_chain && task.delegation_chain.length > 0 && (
        <div className="flex items-center gap-1 text-[10px] font-mono text-zinc-500">
          {task.delegation_chain.map((link: DelegationLink, i: number) => (
            <React.Fragment key={i}>
              {i > 0 && <span className="text-zinc-700">→</span>}
              <span className={link.role === 'PRINCIPAL' ? 'text-amber-400' : 'text-zinc-400'}>
                {link.actor_id}
              </span>
              <span className="text-zinc-700">({link.role})</span>
            </React.Fragment>
          ))}
        </div>
      )}

      {/* Evidence layer + lifecycle history */}
      <div className="flex items-center gap-2">
        <span
          className="px-1.5 py-0.5 rounded text-[10px] font-mono border"
          style={{ color: layerBadge.color, borderColor: layerBadge.color, backgroundColor: `${layerBadge.color}15` }}
        >
          {layerBadge.label}
        </span>
        <span className="text-[10px] text-zinc-600 font-mono">
          floor: {task.reality_constraints?.evidence_floor || 'VERIFIED_STATE'}
        </span>
        {task.task_lifecycle?.state_history && task.task_lifecycle.state_history.length > 1 && (
          <span className="text-[10px] text-zinc-600 font-mono">
            {task.task_lifecycle.state_history.length} transitions
          </span>
        )}
      </div>

      {/* Constitutional binding */}
      {task.constitutional_binding?.governance_verdict && (
        <div className="text-[10px] font-mono">
          <VerdictBadge verdict={task.constitutional_binding.governance_verdict} />
          {task.constitutional_binding.floor_vetoes && task.constitutional_binding.floor_vetoes.length > 0 && (
            <span className="text-red-400 ml-2">
              ⚠ {task.constitutional_binding.floor_vetoes.length} vetoes
            </span>
          )}
        </div>
      )}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════
// PANE 2: REALITY FEED
// ═══════════════════════════════════════════════════════════════════

function RealityFeedPane({ feed, onRefresh }: { feed: RealityFeedState; onRefresh: () => void }) {
  return (
    <div className="p-4 space-y-4">
      {/* Summary */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${
            feed.allHealthy ? 'bg-emerald-400' : feed.criticalHealthy ? 'bg-amber-400' : 'bg-red-400'
          } ${feed.loading ? 'animate-pulse' : ''}`} />
          <span className="text-sm font-mono text-white">{feed.summary}</span>
        </div>
        <button
          onClick={onRefresh}
          disabled={feed.loading}
          className="px-2 py-1 rounded text-[10px] font-mono bg-zinc-800 text-zinc-400 hover:text-white hover:bg-zinc-700 transition-colors disabled:opacity-50"
        >
          {feed.loading ? 'PROBING...' : 'REFRESH'}
        </button>
      </div>

      {/* Reality layer stack visualization */}
      <div className="space-y-1">
        <LayerRow layer="GROUND_TRUTH" active={false} />
        <LayerRow layer="VERIFIED_STATE" active={feed.allHealthy} />
        <LayerRow layer="CACHED_STATE" active={feed.probedAt !== null && !feed.allHealthy} />
        <LayerRow layer="INFERRED" active={feed.loading} />
      </div>

      {/* Organ detail grid */}
      {feed.organs.length > 0 && (
        <div className="grid grid-cols-2 gap-2">
          {feed.organs.map(org => (
            <div
              key={org.organ}
              className={`flex items-center justify-between px-3 py-2 rounded border text-xs font-mono ${
                org.healthy
                  ? 'bg-emerald-900/10 border-emerald-800/50 text-emerald-400'
                  : org.critical
                    ? 'bg-red-900/20 border-red-800/50 text-red-400'
                    : 'bg-amber-900/10 border-amber-800/50 text-amber-400'
              }`}
            >
              <div className="flex items-center gap-2">
                <span className={`w-1.5 h-1.5 rounded-full ${org.healthy ? 'bg-emerald-400' : org.critical ? 'bg-red-400' : 'bg-amber-400'}`} />
                <span>{org.name}</span>
                {org.critical && <span className="text-[10px] opacity-60">★</span>}
              </div>
              <div className="flex items-center gap-2 text-zinc-500">
                <span>{org.status}</span>
                <span>{org.latencyMs}ms</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Error state */}
      {feed.error && (
        <div className="px-3 py-2 bg-red-900/20 border border-red-800 rounded text-xs text-red-400 font-mono">
          {feed.error}
        </div>
      )}

      {/* Evidence floor note */}
      <div className="text-[10px] text-zinc-600 font-mono bg-zinc-900 rounded p-2">
        <strong>Layer upgrade rules:</strong> INFERRED → CACHED (auto after one reasoning loop).
        CACHED → VERIFIED (requires live probe). VERIFIED → GROUND_TRUTH (requires VAULT999 seal + F13 human ratification).
      </div>
    </div>
  );
}

function LayerRow({ layer, active }: { layer: RealityLayer; active: boolean }) {
  const badge = realityLayerBadge(layer);
  return (
    <div className={`flex items-center gap-2 px-3 py-1.5 rounded border text-xs font-mono transition-all ${
      active
        ? 'bg-emerald-900/20 border-emerald-700 text-emerald-400'
        : 'bg-zinc-900/30 border-zinc-800 text-zinc-600'
    }`}>
      <div className={`w-2 h-2 rounded-full ${active ? 'bg-emerald-400' : 'bg-zinc-700'}`} />
      <span style={{ color: active ? badge.color : undefined }}>{badge.label}</span>
      <span className="text-zinc-600">
        — {active ? 'ACTIVE' : layer === 'GROUND_TRUTH' ? 'requires vault seal + F13' : layer === 'VERIFIED_STATE' ? 'requires live probe' : 'pending verification'}
      </span>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════
// PANE 3: VERDICT QUEUE
// ═══════════════════════════════════════════════════════════════════

function VerdictQueuePane({ verdicts }: { verdicts: VerdictItem[] }) {
  if (verdicts.length === 0) {
    return (
      <div className="p-6 text-center text-zinc-500 font-mono text-sm">
        <div className="text-lg mb-2">⚖</div>
        <div>No pending verdicts.</div>
        <div className="text-xs mt-1 text-zinc-600">
          HOLDs and SABAR items appear here
        </div>
      </div>
    );
  }

  const pending = verdicts.filter(v => v.verdict === 'HOLD' || v.verdict === 'SABAR');
  const sealed = verdicts.filter(v => v.verdict === 'SEAL');
  const voided = verdicts.filter(v => v.verdict === 'VOID');

  return (
    <div className="divide-y divide-zinc-800">
      {/* Summary bar */}
      <div className="flex items-center gap-4 px-4 py-2 bg-zinc-900 text-xs font-mono text-zinc-500">
        <span className="text-red-400">{pending.length} pending</span>
        <span className="text-emerald-400">{sealed.length} sealed</span>
        <span className="text-zinc-600">{voided.length} voided</span>
      </div>

      {verdicts.map((v, i) => (
        <div key={v.taskId || i} className="p-3 space-y-1.5">
          <div className="flex items-start justify-between gap-2">
            <div className="text-xs text-white font-mono truncate flex-1">{v.intent}</div>
            <VerdictBadge verdict={v.verdict} />
          </div>
          {v.reason && (
            <div className="text-[10px] text-zinc-500 font-mono">{v.reason}</div>
          )}
          <div className="flex items-center gap-2 text-[10px] font-mono">
            <span
              className="px-1 py-0.5 rounded border"
              style={{
                color: realityLayerBadge(v.evidenceLayer).color,
                borderColor: realityLayerBadge(v.evidenceLayer).color,
                backgroundColor: `${realityLayerBadge(v.evidenceLayer).color}15`,
              }}
            >
              {realityLayerBadge(v.evidenceLayer).label}
            </span>
            <span
              className="px-1 py-0.5 rounded border"
              style={{
                color: autonomyBandBadge(v.autonomyBand).color,
                borderColor: autonomyBandBadge(v.autonomyBand).color,
                backgroundColor: `${autonomyBandBadge(v.autonomyBand).color}15`,
              }}
            >
              {autonomyBandBadge(v.autonomyBand).label}
            </span>
            <span className="text-zinc-600">{v.timestamp ? new Date(v.timestamp).toLocaleTimeString() : ''}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════
// SHARED: VERDICT BADGE
// ═══════════════════════════════════════════════════════════════════

function VerdictBadge({ verdict }: { verdict: GovernanceVerdict }) {
  const colors: Record<GovernanceVerdict, string> = {
    SEAL:    'bg-emerald-900/20 text-emerald-400 border-emerald-700',
    SABAR:   'bg-amber-900/20 text-amber-400 border-amber-700',
    HOLD:    'bg-red-900/20 text-red-400 border-red-700',
    VOID:    'bg-zinc-800 text-zinc-500 border-zinc-700',
    PENDING: 'bg-blue-900/20 text-blue-400 border-blue-700',
  };

  return (
    <span className={`px-1.5 py-0.5 rounded text-[10px] font-mono border ${colors[verdict]}`}>
      {verdict}
    </span>
  );
}
