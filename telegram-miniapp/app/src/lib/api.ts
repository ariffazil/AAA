/**
 * API Client — talks to the Hono gateway
 */

const BASE = import.meta.env.DEV ? "" : (import.meta.env.VITE_API_URL || "");

async function fetchJSON<T>(path: string, opts?: RequestInit): Promise<T> {
  const resp = await fetch(`${BASE}${path}`, {
    ...opts,
    headers: { "Content-Type": "application/json", ...opts?.headers },
  });
  if (!resp.ok) throw new Error(`API ${resp.status}: ${resp.statusText}`);
  return resp.json();
}

// ─── GEOX ──────────────────────────────────────────────────
export async function getAtlas(lat: number, lon: number) {
  return fetchJSON<any>(`/api/geox/atlas?lat=${lat}&lon=${lon}`);
}

export async function getBasin(name: string) {
  return fetchJSON<any>(`/api/geox/basin?name=${encodeURIComponent(name)}`);
}

export async function getDeepTime(params: { age_ma?: number; period?: string; biozone?: string }) {
  const qs = new URLSearchParams();
  if (params.age_ma) qs.set("age_ma", String(params.age_ma));
  if (params.period) qs.set("period", params.period);
  if (params.biozone) qs.set("biozone", params.biozone);
  return fetchJSON<any>(`/api/geox/deep-time?${qs}`);
}

export async function getEarthquakes(minMag?: number) {
  return fetchJSON<any>(`/api/geox/earthquakes?min_mag=${minMag || 4.5}`);
}

// ─── WEALTH ────────────────────────────────────────────────
export async function getFinance(mode?: string) {
  return fetchJSON<any>(`/api/wealth/finance?mode=${mode || "summary"}`);
}

export async function getFiscal() {
  return fetchJSON<any>("/api/wealth/fiscal");
}

export async function getMarket(mode?: string) {
  return fetchJSON<any>(`/api/wealth/market?mode=${mode || "commodity"}`);
}

// ─── WELL ──────────────────────────────────────────────────
export async function getReadiness() {
  return fetchJSON<any>("/api/well/readiness");
}

// ─── Federation ────────────────────────────────────────────
export async function getFederationHealth() {
  return fetchJSON<any>("/api/federation/health");
}
