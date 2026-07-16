/**
 * MCP Apps Panel — AAA Cockpit
 * ==============================
 * Host-side MCP Apps UI for SEP-1865 ext-apps protocol.
 * Manages iframe lifecycle, app registry, and governance overlay.
 *
 * Ports the existing MCPAppsHostBridge into a React component
 * with app launcher, active app tabs, and 888 HOLD / F13 VETO
 * governance overlay rendering.
 *
 * DITEMPA BUKAN DIBERI
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import {
  X,
  Maximize2,
  Minimize2,
  ShieldAlert,
  AlertCircle,
  LayoutGrid,
} from 'lucide-react';
import { MCPAppsHostBridge } from '../host/MCPAppsHostBridge';

// ── App Registry ────────────────────────────────────────────────────────────
// Canonical list of registered MCP Apps with metadata.
// Each app has an id (matching the url path /mcp-apps/{id}),
// a label, description, and which organ it belongs to.

export interface MCPAppDescriptor {
  id: string;
  label: string;
  description: string;
  organ: 'geox' | 'wealth' | 'well' | 'arifos' | 'a-forge';
  icon?: string;
  defaultDisplayMode?: 'inline' | 'fullscreen';
}

const REGISTERED_APPS: MCPAppDescriptor[] = [
  {
    id: 'well-desk',
    label: 'WellDesk',
    description: '1D/2D well log viewer — petrophysics, rock physics, formation evaluation',
    organ: 'geox',
    icon: '📊',
    defaultDisplayMode: 'inline',
  },
  {
    id: 'earth-volume',
    label: 'Earth Volume',
    description: '3D seismic volume viewer — horizon interpretation, attribute analysis',
    organ: 'geox',
    icon: '🌍',
    defaultDisplayMode: 'inline',
  },
  {
    id: 'judge-console',
    label: 'Judge Console',
    description: '888 JUDGE deliberation console — verdict history, HOLD resolution',
    organ: 'geox',
    icon: '⚖️',
    defaultDisplayMode: 'inline',
  },
  {
    id: 'aforge-preview',
    label: 'Forge Preview',
    description: 'A-FORGE two-phase commit preview — stage diff, blast radius, F13 SEAL/HOLD/VOID gate',
    organ: 'a-forge',
    icon: '⚒️',
    defaultDisplayMode: 'inline',
  },
];

// ── Governance envelope types (mirrors arifOS) ──────────────────────────────

type ArifOsPolicyState =
  | 'observe'
  | 'review_required'
  | 'hold'
  | 'veto'
  | 'approved'
  | 'rejected';

interface ArifOsHold {
  code: string;
  reason: string;
  severity?: 'low' | 'medium' | 'high' | 'critical';
  blocking: boolean;
  requiredWitness?: Array<'human' | 'ai' | 'earth'>;
  expiresAt?: string | null;
}

interface ArifOsConstraintVeto {
  active: boolean;
  reason: string | null;
  authority: string | null;
}

interface ArifOsConstraints {
  policyState: ArifOsPolicyState;
  disabledActions: string[];
  requiredFloors: string[];
  veto: ArifOsConstraintVeto;
}

interface ArifOsAction {
  id: string;
  label: string;
  tool: string;
  arguments?: Record<string, unknown>;
  requiresConfirmation: boolean;
  requiredFloors?: string[];
}

interface ArifOsEnvelope {
  schemaVersion: string;
  summary: string;
  viewModel: Record<string, unknown>;
  actions: ArifOsAction[];
  holds: ArifOsHold[];
  constraints: ArifOsConstraints;
  provenance: {
    sources: string[];
    confidence: number;
    epistemicTag: string;
    timestamp?: string;
  };
  telemetry?: Record<string, unknown>;
}

// ── Active App State ────────────────────────────────────────────────────────

interface ActiveApp {
  descriptor: MCPAppDescriptor;
  state: 'initializing' | 'ready' | 'error';
  errorMessage?: string;
  displayMode: 'inline' | 'fullscreen';
  governanceState: ArifOsEnvelope | null;
}

interface PendingRequest {
  resolve: (value: unknown) => void;
  reject: (reason?: unknown) => void;
}

type JsonRpcId = string | number;

interface JsonRpcMessage {
  jsonrpc: '2.0';
  id?: JsonRpcId;
  method?: string;
  params?: Record<string, unknown>;
  result?: unknown;
  error?: { message?: string };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object';
}

function parseJsonRpcMessage(value: unknown): JsonRpcMessage | null {
  let parsed: unknown = value;
  if (typeof value === 'string') {
    try {
      parsed = JSON.parse(value) as unknown;
    } catch {
      return null;
    }
  }
  if (!isRecord(parsed) || parsed.jsonrpc !== '2.0') return null;
  return parsed as JsonRpcMessage;
}

// ── Component ───────────────────────────────────────────────────────────────

export default function MCPAppsPanel() {
  const [activeApps, setActiveApps] = useState<Map<string, ActiveApp>>(new Map());
  const [fullscreenApp, setFullscreenApp] = useState<string | null>(null);
  /** G3: mount points for double-iframe Sandbox Proxy via MCPAppsHostBridge */
  const mountRefs = useRef<Map<string, HTMLDivElement>>(new Map());
  const bridgesRef = useRef<Map<string, MCPAppsHostBridge>>(new Map());

  // ── Launch an MCP App ─────────────────────────────────────────────────

  const launchApp = useCallback((descriptor: MCPAppDescriptor) => {
    setActiveApps(prev => {
      if (prev.has(descriptor.id)) return prev;
      const next = new Map(prev);
      next.set(descriptor.id, {
        descriptor,
        state: 'initializing',
        displayMode: descriptor.defaultDisplayMode || 'inline',
        governanceState: null,
      });
      return next;
    });
  }, []);

  // ── Close an MCP App ──────────────────────────────────────────────────

  const closeApp = useCallback((appId: string) => {
    const bridge = bridgesRef.current.get(appId);
    if (bridge) {
      try {
        bridge.teardownApp(appId, 'user_closed');
      } catch {
        /* ignore */
      }
      bridgesRef.current.delete(appId);
    }
    mountRefs.current.delete(appId);

    setActiveApps(prev => {
      const next = new Map(prev);
      next.delete(appId);
      return next;
    });
    if (fullscreenApp === appId) setFullscreenApp(null);
  }, [fullscreenApp]);

  // ── Toggle display mode ────────────────────────────────────────────────

  const toggleDisplayMode = useCallback((appId: string) => {
    setActiveApps(prev => {
      const app = prev.get(appId);
      if (!app) return prev;
      const next = new Map(prev);
      next.set(appId, {
        ...app,
        displayMode: app.displayMode === 'inline' ? 'fullscreen' : 'inline',
      });
      return next;
    });
    setFullscreenApp(prev => prev === appId ? null : appId);
  }, []);

  // ── G3: mount Sandbox Proxy when mount node is ready ─────────────────

  const setMountNode = useCallback((appId: string, node: HTMLDivElement | null) => {
    if (!node) {
      mountRefs.current.delete(appId);
      return;
    }
    mountRefs.current.set(appId, node);
    if (bridgesRef.current.has(appId)) return;

    const bridge = new MCPAppsHostBridge(node);
    bridgesRef.current.set(appId, bridge);

    bridge.onToolResult((_id, envelope) => {
      setActiveApps(prev => {
        const app = prev.get(appId);
        if (!app) return prev;
        const next = new Map(prev);
        next.set(appId, {
          ...app,
          governanceState: envelope as ArifOsEnvelope,
        });
        return next;
      });
    });

    // tools/call from guest → AAA host proxy (connect-src none on guest).
    // OBSERVE allowlist → GEOX session path; mutate → 403 HOLD (arifOS lease later).
    bridge.onToolCall(async (id, name, args) => {
      console.info(`[MCP Apps] tools/call app=${id} tool=${name}`, args);
      try {
        const res = await fetch('/api/mcp-apps/tools/call', {
          method: 'POST',
          credentials: 'same-origin',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({
            appId: id,
            tool: name,
            arguments: args || {},
          }),
        });
        const data = await res.json().catch(() => null);
        if (!data || typeof data !== 'object') {
          return {
            ok: false,
            isError: true,
            message: `Host proxy HTTP ${res.status} — empty body`,
            tool: name,
          };
        }
        if (!res.ok && data.hold) {
          // Policy HOLD — return envelope so guest can render
          return data;
        }
        if (!res.ok && data.ok === false) {
          return data;
        }
        return data;
      } catch (err) {
        console.error(`[MCP Apps] tools/call proxy failed app=${id} tool=${name}`, err);
        return {
          ok: false,
          isError: true,
          message: err instanceof Error ? err.message : 'tools/call proxy failed',
          tool: name,
        };
      }
    });

    try {
      bridge.mountApp(appId, {
        displayMode: 'inline',
        onReady: () => {
          setActiveApps(prev => {
            const app = prev.get(appId);
            if (!app) return prev;
            const next = new Map(prev);
            next.set(appId, { ...app, state: 'ready' });
            return next;
          });
        },
      });
    } catch (err) {
      setActiveApps(prev => {
        const app = prev.get(appId);
        if (!app) return prev;
        const next = new Map(prev);
        next.set(appId, {
          ...app,
          state: 'error',
          errorMessage: err instanceof Error ? err.message : 'mount failed',
        });
        return next;
      });
    }
  }, []);

  // Cleanup bridges on unmount
  useEffect(() => {
    const bridges = bridgesRef.current;
    return () => {
      for (const [appId, bridge] of bridges) {
        try {
          bridge.teardownApp(appId, 'panel_unmount');
        } catch {
          /* ignore */
        }
      }
      bridges.clear();
    };
  }, []);

  // ── Render ────────────────────────────────────────────────────────────

  const sortedApps = Array.from(activeApps.entries());

  return (
    <section className="mb-24">
      {/* Header */}
      <div className="flex items-baseline gap-4 mb-10">
        <span className="text-4xl font-black text-red-500/20 font-mono italic">⊞</span>
        <h2 className="text-2xl font-bold tracking-tighter text-white uppercase">MCP Apps</h2>
        <span className="text-[9px] font-mono text-white/30 uppercase tracking-widest">
          SEP-1865 · {REGISTERED_APPS.length} registered · {activeApps.size} active
        </span>
      </div>

      {/* App Launcher Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        {REGISTERED_APPS.map(app => {
          const isActive = activeApps.has(app.id);
          return (
            <button
              key={app.id}
              onClick={() => !isActive && launchApp(app)}
              disabled={isActive}
              className={`p-6 border rounded-lg text-left transition-all ${
                isActive
                  ? 'border-emerald-500/30 bg-emerald-950/10 cursor-default'
                  : 'border-white/10 bg-white/[0.02] hover:border-red-500/50 hover:bg-red-950/5 cursor-pointer'
              }`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="text-2xl">{app.icon || '⊞'}</div>
                {isActive && (
                  <span className="text-[8px] font-mono px-2 py-0.5 bg-emerald-950/30 text-emerald-400 border border-emerald-500/20 rounded uppercase tracking-widest font-black">
                    ACTIVE
                  </span>
                )}
              </div>
              <div className="text-sm font-black text-white tracking-tight mb-1">{app.label}</div>
              <div className="text-[10px] font-mono text-white/40 mb-2">{app.description}</div>
              <div className="text-[8px] font-mono text-white/20 uppercase tracking-widest">
                {app.organ.toUpperCase()} · {app.defaultDisplayMode || 'inline'}
              </div>
            </button>
          );
        })}
      </div>

      {/* Active Apps */}
      {sortedApps.length === 0 ? (
        <div className="p-12 border border-dashed border-white/10 rounded-lg text-center">
          <LayoutGrid className="w-8 h-8 text-white/10 mx-auto mb-4" />
          <p className="text-sm text-white/30 font-mono tracking-widest uppercase">
            Launch an MCP App above to see its interface here
          </p>
          <p className="text-[10px] text-white/20 font-mono mt-2">
            SEP-1865 · G3 double-iframe Sandbox Proxy · postMessage JSON-RPC
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {sortedApps.map(([appId, app]) => (
            <div
              key={appId}
              className={`border rounded-lg overflow-hidden transition-all ${
                app.displayMode === 'fullscreen'
                  ? 'fixed inset-0 z-[9999] bg-[#050505] border-0'
                  : 'border-white/10 bg-white/[0.02]'
              }`}
            >
              {/* App Header Bar */}
              <div className={`flex items-center justify-between px-4 py-3 border-b ${
                app.displayMode === 'fullscreen' ? 'border-white/10 bg-black' : 'border-white/5 bg-white/[0.03]'
              }`}>
                <div className="flex items-center gap-3">
                  <span className="text-sm">{app.descriptor.icon || '⊞'}</span>
                  <span className="text-xs font-black text-white uppercase tracking-wider">
                    {app.descriptor.label}
                  </span>
                  <span className={`text-[8px] font-mono px-1.5 py-0.5 rounded uppercase tracking-widest font-black ${
                    app.state === 'ready'
                      ? 'text-emerald-400 bg-emerald-950/30'
                      : app.state === 'error'
                      ? 'text-red-400 bg-red-950/30'
                      : 'text-amber-400 bg-amber-950/30 animate-pulse'
                  }`}>
                    {app.state === 'ready' ? 'READY' : app.state === 'error' ? 'ERROR' : 'INIT'}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  {/* Governance State Badge */}
                  {app.governanceState && (
                    <GovernanceBadge envelope={app.governanceState} />
                  )}
                  {/* Display Mode Toggle */}
                  <button
                    onClick={() => toggleDisplayMode(appId)}
                    className="p-1.5 rounded hover:bg-white/10 transition-colors text-white/40 hover:text-white"
                    title={app.displayMode === 'fullscreen' ? 'Minimize' : 'Fullscreen'}
                  >
                    {app.displayMode === 'fullscreen'
                      ? <Minimize2 className="w-3.5 h-3.5" />
                      : <Maximize2 className="w-3.5 h-3.5" />
                    }
                  </button>
                  {/* Close */}
                  <button
                    onClick={() => closeApp(appId)}
                    className="p-1.5 rounded hover:bg-red-500/20 transition-colors text-white/40 hover:text-red-500"
                    title="Close app"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>

              {/* G3 double-iframe mount (Sandbox Proxy + guest) */}
              <div className={`relative ${app.displayMode === 'fullscreen' ? 'h-[calc(100vh-48px)]' : 'min-h-[500px]'}`}>
                {app.state === 'error' && (
                  <div className="absolute inset-0 flex items-center justify-center bg-red-950/20 z-10">
                    <div className="text-center">
                      <AlertCircle className="w-8 h-8 text-red-500 mx-auto mb-2" />
                      <p className="text-sm text-red-400 font-mono">Failed to load {app.descriptor.label}</p>
                      {app.errorMessage && (
                        <p className="text-xs text-red-400/60 font-mono mt-1">{app.errorMessage}</p>
                      )}
                    </div>
                  </div>
                )}
                <div
                  ref={(node) => setMountNode(appId, node)}
                  data-app-id={appId}
                  data-g3="true"
                  className="w-full h-full min-h-[500px]"
                  title={app.descriptor.label}
                />
                <div className="absolute bottom-2 right-2 text-[8px] font-mono text-white/25 uppercase tracking-widest pointer-events-none">
                  G3 Sandbox Proxy · double-iframe
                </div>

                {/* Governance Overlay */}
                {app.governanceState && renderGovernanceOverlay(app.governanceState)}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

// ── Governance Badge ────────────────────────────────────────────────────────

function GovernanceBadge({ envelope }: { envelope: ArifOsEnvelope }) {
  const { constraints, holds } = envelope;
  const isVetoed = constraints?.veto?.active === true;
  const hasHolds = Array.isArray(holds) && holds.some(h => h.blocking !== false);

  if (isVetoed) {
    return (
      <span className="flex items-center gap-1 px-1.5 py-0.5 bg-red-950/40 text-red-400 border border-red-500/20 rounded text-[8px] font-mono uppercase tracking-widest font-black">
        <ShieldAlert className="w-3 h-3" /> F13 VETO
      </span>
    );
  }

  if (hasHolds) {
    const blockingCount = holds.filter(h => h.blocking !== false).length;
    return (
      <span className="flex items-center gap-1 px-1.5 py-0.5 bg-amber-950/40 text-amber-400 border border-amber-500/20 rounded text-[8px] font-mono uppercase tracking-widest font-black">
        <AlertCircle className="w-3 h-3" /> {blockingCount} HOLD{blockingCount > 1 ? 'S' : ''}
      </span>
    );
  }

  return (
    <span className="flex items-center gap-1 px-1.5 py-0.5 bg-emerald-950/30 text-emerald-400 border border-emerald-500/20 rounded text-[8px] font-mono uppercase tracking-widest font-black">
      SEAL
    </span>
  );
}

// ── Governance Overlay ──────────────────────────────────────────────────────

function renderGovernanceOverlay(envelope: ArifOsEnvelope) {
  const { constraints, holds } = envelope;
  const isVetoed = constraints?.veto?.active === true;
  const blockingHolds = Array.isArray(holds) ? holds.filter(h => h.blocking !== false) : [];
  const disabledActions = constraints?.disabledActions || [];

  if (!isVetoed && blockingHolds.length === 0 && disabledActions.length === 0) return null;

  return (
    <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 via-black/70 to-transparent p-4 pointer-events-none">
      <div className="pointer-events-auto max-w-lg mx-auto">
        {/* F13 VETO Banner */}
        {isVetoed && (
          <div className="bg-red-950/80 border border-red-500/30 rounded-lg p-3 mb-2">
            <div className="flex items-center gap-2 mb-1">
              <ShieldAlert className="w-4 h-4 text-red-400" />
              <span className="text-[10px] font-black text-red-400 uppercase tracking-widest">F13 SOVEREIGN VETO</span>
            </div>
            <p className="text-[11px] text-red-300/80 font-mono">
              {constraints.veto?.reason || 'This action has been vetoed by the sovereign'}
            </p>
            {constraints.veto?.authority && (
              <p className="text-[9px] text-red-400/60 font-mono mt-1">
                Authority: {constraints.veto.authority}
              </p>
            )}
          </div>
        )}

        {/* 888 HOLD Banner */}
        {blockingHolds.length > 0 && (
          <div className="bg-amber-950/80 border border-amber-500/30 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <AlertCircle className="w-4 h-4 text-amber-400" />
              <span className="text-[10px] font-black text-amber-400 uppercase tracking-widest">
                888 HOLD — {blockingHolds.length} BLOCKING
              </span>
            </div>
            {blockingHolds.slice(0, 3).map((hold, i) => (
              <div key={i} className="text-[10px] font-mono text-amber-200/70 ml-6">
                [{hold.code}] {hold.reason}
              </div>
            ))}
            {blockingHolds.length > 3 && (
              <div className="text-[9px] font-mono text-amber-400/50 ml-6 mt-1">
                +{blockingHolds.length - 3} more
              </div>
            )}
          </div>
        )}

        {/* Disabled Actions */}
        {disabledActions.length > 0 && !isVetoed && (
          <div className="text-[8px] font-mono text-white/30 mt-1 text-center">
            Disabled tools: {disabledActions.join(', ')}
          </div>
        )}

        {/* Epistemic Tag */}
        <div className="text-[8px] font-mono text-white/20 mt-1 text-center">
          {envelope.provenance?.epistemicTag && (
            <span className="uppercase tracking-wider">
              Epistemic: {envelope.provenance.epistemicTag} ·
            </span>
          )}
          Confidence: {(envelope.provenance?.confidence * 100).toFixed(0)}%
        </div>
      </div>
    </div>
  );
}
