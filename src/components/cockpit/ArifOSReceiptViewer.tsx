/**
 * ArifOSReceiptViewer — VAULT999 → Cockpit Surface
 * ════════════════════════════════════════════════════
 *
 * Polls arifOS `/api/live/vault` and renders the most recent
 * sealed events as readable cards in the cockpit. Purpose:
 * let Arif glance at any recent operator action and see
 *
 *   - who acted (actor_id)
 *   - what verdict was issued (SEAL / HOLD / SABAR / VOID / OBSERVED)
 *   - which stage of the metabolic pipeline ran (000 / 333 / 666 / 888 / 999)
 *   - whether the action was irreversible
 *   - when it happened (relative + absolute)
 *
 * No mutations. No writes. Read-only witness surface.
 *
 * DITEMPA BUKAN DIBERI
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  ShieldCheck,
  ShieldAlert,
  ShieldX,
  Eye,
  PauseCircle,
  ScrollText,
  RefreshCw,
  Clock,
  Activity,
} from 'lucide-react';

// ═══════════════════════════════════════════════════════════════════════════
// Types — mirror arifOS `/api/live/vault` envelope
// ═══════════════════════════════════════════════════════════════════════════

type VerdictLabel = 'SEAL' | 'HOLD' | 'SABAR' | 'VOID' | 'OBSERVED' | 'UNKNOWN';

interface VaultWitness {
  claim_state?: string;
  binding?: boolean;
  irreversible?: boolean;
  human_ratifier?: string | null;
  trace_id?: string | null;
}

interface VaultEntry {
  event_id?: string;
  id?: number;
  event_type?: string;
  session_id?: string | null;
  actor_id?: string;
  stage?: string;
  verdict?: string;
  risk_tier?: string;
  payload?: Record<string, unknown>;
  action?: string;
  sealed_at?: string;
  signed_by?: string | null;
  witness?: VaultWitness;
  seal_hash?: string;
  chain_hash?: string;
  prev_leaf?: string;
}

interface VaultResponse {
  entries: VaultEntry[];
  count: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// Verdict styling — kept minimal; reuse the AutonomyBands palette
// ═══════════════════════════════════════════════════════════════════════════

const VERDICT_META: Record<
  VerdictLabel,
  { color: string; bg: string; border: string; icon: React.ReactNode; label: string }
> = {
  SEAL: {
    color: 'text-emerald-400',
    bg: 'bg-emerald-950/30',
    border: 'border-emerald-500/40',
    icon: <ShieldCheck className="w-3.5 h-3.5" />,
    label: 'SEAL',
  },
  HOLD: {
    color: 'text-amber-400',
    bg: 'bg-amber-950/30',
    border: 'border-amber-500/40',
    icon: <ShieldAlert className="w-3.5 h-3.5" />,
    label: 'HOLD',
  },
  SABAR: {
    color: 'text-yellow-400',
    bg: 'bg-yellow-950/30',
    border: 'border-yellow-500/40',
    icon: <PauseCircle className="w-3.5 h-3.5" />,
    label: 'SABAR',
  },
  VOID: {
    color: 'text-red-400',
    bg: 'bg-red-950/30',
    border: 'border-red-500/40',
    icon: <ShieldX className="w-3.5 h-3.5" />,
    label: 'VOID',
  },
  OBSERVED: {
    color: 'text-sky-400',
    bg: 'bg-sky-950/30',
    border: 'border-sky-500/40',
    icon: <Eye className="w-3.5 h-3.5" />,
    label: 'OBSERVED',
  },
  UNKNOWN: {
    color: 'text-zinc-400',
    bg: 'bg-zinc-900/40',
    border: 'border-zinc-700',
    icon: <ScrollText className="w-3.5 h-3.5" />,
    label: 'UNKNOWN',
  },
};

const coerceVerdict = (raw: string | undefined): VerdictLabel => {
  if (!raw) return 'UNKNOWN';
  const upper = raw.toUpperCase();
  if (upper in VERDICT_META) return upper as VerdictLabel;
  return 'UNKNOWN';
};

const formatRelative = (iso: string | undefined, now: number): string => {
  if (!iso) return '—';
  const t = Date.parse(iso);
  if (Number.isNaN(t)) return iso;
  const delta = Math.max(0, now - t);
  const sec = Math.floor(delta / 1000);
  if (sec < 60) return `${sec}s ago`;
  const min = Math.floor(sec / 60);
  if (min < 60) return `${min}m ago`;
  const hr = Math.floor(min / 60);
  if (hr < 24) return `${hr}h ago`;
  const day = Math.floor(hr / 24);
  return `${day}d ago`;
};

// ═══════════════════════════════════════════════════════════════════════════
// Component
// ═══════════════════════════════════════════════════════════════════════════

const POLL_INTERVAL_MS = 5000;
const DEFAULT_LIMIT = 8;
const ARIFOS_BASE = 'https://arifos.arif-fazil.com';

export default function ArifOSReceiptViewer({
  limit = DEFAULT_LIMIT,
  pollMs = POLL_INTERVAL_MS,
}: {
  limit?: number;
  pollMs?: number;
}) {
  const [entries, setEntries] = useState<VaultEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastFetched, setLastFetched] = useState<number>(0);
  const [now, setNow] = useState<number>(0);
  const tickRef = useRef<number | null>(null);

  const fetchReceipts = useCallback(async () => {
    try {
      const res = await fetch(`${ARIFOS_BASE}/api/live/vault?limit=${limit}`, {
        cache: 'no-store',
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = (await res.json()) as VaultResponse;
      setEntries(Array.isArray(data.entries) ? data.entries : []);
      setError(null);
      setLastFetched(Date.now());
    } catch (e) {
      setError(e instanceof Error ? e.message : 'fetch failed');
    } finally {
      setLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    fetchReceipts();
    const id = window.setInterval(fetchReceipts, pollMs);
    return () => window.clearInterval(id);
  }, [fetchReceipts, pollMs]);

  // Refresh "now" every second for relative timestamps without re-fetching
  useEffect(() => {
    setNow(Date.now());
    tickRef.current = window.setInterval(() => setNow(Date.now()), 1000);
    return () => {
      if (tickRef.current) window.clearInterval(tickRef.current);
    };
  }, []);

  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950/50 p-3 text-xs font-mono">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-zinc-400" />
          <span className="text-zinc-300 font-semibold tracking-wide">
            arifOS · Recent VAULT999 Receipts
          </span>
          {error ? (
            <span className="text-red-400">· {error}</span>
          ) : lastFetched > 0 ? (
            <span className="text-zinc-500">
              · refreshed {formatRelative(new Date(lastFetched).toISOString(), now)}
            </span>
          ) : null}
        </div>
        <button
          onClick={fetchReceipts}
          className="text-zinc-500 hover:text-zinc-300 transition-colors"
          title="Refresh now"
          aria-label="Refresh receipts"
        >
          <RefreshCw className="w-3.5 h-3.5" />
        </button>
      </div>

      {loading && entries.length === 0 ? (
        <div className="text-zinc-500 py-4 text-center">loading vault…</div>
      ) : entries.length === 0 ? (
        <div className="text-zinc-500 py-4 text-center italic">
          no sealed events yet
        </div>
      ) : (
        <ul className="space-y-1.5 max-h-[420px] overflow-y-auto pr-1">
          {entries.map((e, i) => {
            const v = coerceVerdict(e.verdict);
            const meta = VERDICT_META[v];
            const irreversible = e.witness?.irreversible ?? false;
            const stageLabel = (e.stage ?? '—').toString().toUpperCase();
            const summary =
              (e.payload && typeof e.payload === 'object'
                ? (e.payload.title as string) ||
                  (e.payload.summary as string) ||
                  (e.payload.reason as string) ||
                  (e.action as string)
                : null) ?? e.event_type ?? '—';
            return (
              <li
                key={`${e.event_id ?? e.id ?? 'row'}-${i}`}
                className={`rounded border ${meta.border} ${meta.bg} px-2 py-1.5 flex items-start gap-2`}
              >
                <span className={`flex items-center gap-1 ${meta.color} shrink-0 pt-0.5`}>
                  {meta.icon}
                  <span className="font-semibold tracking-wide">{meta.label}</span>
                </span>
                <span className="text-zinc-500 shrink-0">·</span>
                <span className="text-zinc-300 shrink-0 truncate max-w-[160px]" title={e.actor_id ?? ''}>
                  {e.actor_id ?? '—'}
                </span>
                <span className="text-zinc-500 shrink-0">·</span>
                <span className="text-zinc-400 shrink-0">stage {stageLabel}</span>
                {irreversible ? (
                  <span className="text-amber-300 shrink-0" title="irreversible">
                    · IRR
                  </span>
                ) : null}
                <span className="text-zinc-200 grow truncate" title={summary}>
                  {summary}
                </span>
                <span className="text-zinc-500 shrink-0 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {formatRelative(e.sealed_at, now)}
                </span>
              </li>
            );
          })}
        </ul>
      )}

      <div className="mt-2 pt-2 border-t border-zinc-800 text-[10px] text-zinc-600 flex items-center justify-between">
        <span>VAULT999 · append-only hash chain · witness surface</span>
        <span>
          poll {pollMs / 1000}s · limit {limit}
        </span>
      </div>
    </div>
  );
}
