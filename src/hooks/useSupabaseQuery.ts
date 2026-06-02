/**
 * useSupabaseQuery — generic read-only Supabase query hook
 * Phase 3A: Read-only, no writes, no mutations.
 */
import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';

export interface QueryState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useSupabaseQuery<T>(
  tableOrView: string,
  options: {
    select?: string;
    order?: string;
    limit?: number;
    filters?: Record<string, string | number | boolean | null>;
  } = {}
): QueryState<T> {
  const { select = '*', order, limit, filters } = options;

  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetch = async () => {
    setLoading(true);
    setError(null);
    try {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      let query: any = supabase.from(tableOrView).select(select);
      if (order) {
        const [col, dir] = order.split(' ');
        query = query.order(col, { ascending: dir === 'ASC' });
      }
      if (limit) query = query.limit(limit);
      if (filters) {
        for (const [key, value] of Object.entries(filters)) {
          if (value !== null) query = query.eq(key, value);
        }
      }
      const { data: result, error: err } = await query;
      if (err) throw new Error(err.message);
      setData(result as T);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetch();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tableOrView]);

  return { data, loading, error, refetch: fetch };
}

/** Check Supabase connection health */
export function useSupabaseHealth() {
  const [healthy, setHealthy] = useState<boolean | null>(null);
  const [latencyMs, setLatencyMs] = useState<number | null>(null);

  useEffect(() => {
    const check = async () => {
      const start = Date.now();
      try {
        const { error } = await supabase.from('aaa.memory_health').select('table_name').limit(1);
        setLatencyMs(Date.now() - start);
        setHealthy(!error);
      } catch {
        setHealthy(false);
      }
    };
    check();
    const interval = setInterval(check, 30000);
    return () => clearInterval(interval);
  }, []);

  return { healthy, latencyMs };
}
