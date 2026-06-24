import { useEffect, useState } from 'react';
import { Activity, MessageSquare, Cpu, AlertCircle } from 'lucide-react';

interface HermesTelemetry {
  timestamp: string;
  agent_id: string;
  active_sessions: number;
  sessions_24h: number;
  message_count_24h: number;
  tool_calls_24h: Record<string, number>;
  token_usage_24h: number;
  error_rate_24h: number;
  last_updated: string;
}

export default function HermesTelemetryPanel() {
  const [telemetry, setTelemetry] = useState<HermesTelemetry | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTelemetry = async () => {
      try {
        const res = await fetch('/api/telemetry/hermes', { cache: 'no-store' });
        if (!res.ok) {
          const data = await res.json().catch(() => ({}));
          throw new Error(data.error || `HTTP ${res.status}`);
        }
        const data = await res.json();
        setTelemetry(data.telemetry);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchTelemetry();
    const interval = setInterval(fetchTelemetry, 60000);
    return () => clearInterval(interval);
  }, []);

  const formatNumber = (n: number) =>
    typeof n === 'number' ? n.toLocaleString() : '—';

  const totalToolCalls = telemetry?.tool_calls_24h?._total ?? 0;

  return (
    <div className="border border-white/10 rounded-xl bg-black/40 backdrop-blur-sm overflow-hidden">
      <div className="px-5 py-4 border-b border-white/10 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-emerald-400" />
          <h3 className="text-sm font-semibold text-white/90">Hermes Telemetry</h3>
        </div>
        <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          L1/L2 bridge
        </span>
      </div>

      <div className="p-5">
        {loading ? (
          <div className="text-xs text-white/50 animate-pulse">Loading telemetry…</div>
        ) : error ? (
          <div className="flex items-start gap-2 text-xs text-red-400">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        ) : telemetry ? (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div className="px-3 py-2 rounded bg-white/5">
                <div className="text-[10px] text-white/50 uppercase tracking-wider">Active sessions</div>
                <div className="text-lg font-mono text-white">{formatNumber(telemetry.active_sessions)}</div>
              </div>
              <div className="px-3 py-2 rounded bg-white/5">
                <div className="text-[10px] text-white/50 uppercase tracking-wider">24h sessions</div>
                <div className="text-lg font-mono text-white">{formatNumber(telemetry.sessions_24h)}</div>
              </div>
              <div className="px-3 py-2 rounded bg-white/5">
                <div className="text-[10px] text-white/50 uppercase tracking-wider flex items-center gap-1">
                  <MessageSquare className="w-3 h-3" /> Messages 24h
                </div>
                <div className="text-lg font-mono text-white">{formatNumber(telemetry.message_count_24h)}</div>
              </div>
              <div className="px-3 py-2 rounded bg-white/5">
                <div className="text-[10px] text-white/50 uppercase tracking-wider flex items-center gap-1">
                  <Cpu className="w-3 h-3" /> Tool calls 24h
                </div>
                <div className="text-lg font-mono text-white">{formatNumber(totalToolCalls)}</div>
              </div>
            </div>

            <div className="flex items-center justify-between text-xs">
              <span className="text-white/50">Token usage 24h</span>
              <span className="font-mono text-white">{formatNumber(telemetry.token_usage_24h)}</span>
            </div>

            <div className="flex items-center justify-between text-xs">
              <span className="text-white/50">Error rate 24h</span>
              <span className={`font-mono ${telemetry.error_rate_24h > 0.05 ? 'text-red-400' : 'text-emerald-400'}`}>
                {(telemetry.error_rate_24h * 100).toFixed(2)}%
              </span>
            </div>

            {telemetry.tool_calls_24h && Object.keys(telemetry.tool_calls_24h).filter(k => k !== '_total').length > 0 && (
              <div className="pt-3 border-t border-white/10">
                <div className="text-[10px] text-white/50 uppercase tracking-wider mb-2">Tool calls by source</div>
                <div className="space-y-1">
                  {Object.entries(telemetry.tool_calls_24h)
                    .filter(([key]) => key !== '_total')
                    .map(([source, count]) => (
                      <div key={source} className="flex items-center justify-between text-xs">
                        <span className="text-white/60 capitalize">{source}</span>
                        <span className="font-mono text-white/80">{formatNumber(count as number)}</span>
                      </div>
                    ))}
                </div>
              </div>
            )}

            <div className="text-[10px] text-white/30 pt-2">
              Last updated: {new Date(telemetry.last_updated).toLocaleTimeString()}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
